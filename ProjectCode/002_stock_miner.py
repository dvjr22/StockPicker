#!/usr/bin/env python
# coding: utf-8

# # References
# http://theautomatic.net/yahoo_fin-documentation/
# http://theautomatic.net/2020/05/05/how-to-download-fundamentals-data-with-python/
# https://algotrading101.com/learn/yahoo-finance-api-guide/>
# https://blog.quantinsti.com/quantitative-value-investing-strategy-python/
# https://www.activestate.com/blog/top-10-python-packages-for-finance-and-financial-modeling/
# https://medium.com/automation-generation/teaching-your-computer-to-invest-with-python-commission-free-automated-investing-5ade10961e08


# # Imports
import pandas as pd
import yahoo_fin.stock_info as si
import time
import timeit

start = timeit.default_timer()


# # Variables
ratio_valuation_function=['Price/Book (mrq)','Trailing P/E','Forward P/E 1',                          'PEG Ratio (5 yr expected) 1','Price/Sales (ttm)']

ratio_stat=['Total Debt/Equity (mrq)', 'Diluted EPS (ttm)', 'Trailing Annual Dividend Yield 3',            'Forward Annual Dividend Yield 4', '% Held by Insiders 1','% Held by Institutions 1',            'Return on Equity (ttm)','Return on Assets (ttm)','Quarterly Earnings Growth (yoy)',            'current_price']

# ratio_stat=['Total Debt/Equity (mrq)', 'Diluted EPS (ttm)', 'Trailing Annual Dividend Yield 3',\
#             'Forward Annual Dividend Yield 4', '% Held by Insiders 1','% Held by Institutions 1',\
#             'Return on Equity (ttm)','Return on Assets (ttm)','Quarterly Earnings Growth (yoy)', \
#             'current_price','Beta (5Y Monthly)']


# # Get Updated S&P 500

# complete sp 500 list
# file generated: get_sp_500_update.py
# ticker_df = pd.read_csv('../ProjectDatasets/sp_500_symbols.csv', sep=',')
# tickers = ticker_df['Symbol'].tolist()

# get latest sp500
tickers = si.tickers_sp500()

# tickersDF = si.tickers_sp500(True)
# tickers = tickers[:4].copy()

print(len(tickers))


# # Company Info

tickersDF = si.tickers_sp500(True)
tickersDF.index = tickersDF['Symbol']

tickersDF.index.rename('ticker', inplace=True)
tickersDF.drop(columns=['Symbol'], inplace=True)


# # Sort Data

table=pd.DataFrame()

ticker_index = []
retry_ticker = []
count = 0

for p in tickers:
#     print(p)
    try:
        data=si.get_stats(p)
        data.index=data["Attribute"]
        data=data.drop(labels="Attribute",axis=1)
        raw_table=data.T
        raw_table['current_price'] = round(si.get_live_price(p),2)
        table=table.append(raw_table)   #Table having Data about the company
        ticker_index.append(p)
    except:
        count = count+1
        print('Bad Ticker {}: {}'.format(count, p))
        retry_ticker.append(p)

if len(retry_ticker) > 0:     
    time.sleep(60*20)
    count = 0

    for p in retry_ticker:
    #     print(p)
        try:
            data=si.get_stats(p)
            data.index=data["Attribute"]
            data=data.drop(labels="Attribute",axis=1)
            raw_table=data.T
            raw_table['current_price'] = round(si.get_live_price(p),2)
            table=table.append(raw_table)   #Table having Data about the company
            ticker_index.append(p)
            time.sleep(10)
        except:
            count = count+1
            print('Bad Ticker 2nd attempt {}: {}'.format(count, p))
            time.sleep(60*5)
    
table.index=ticker_index
table1 = table[ratio_stat]


time.sleep(60*20)


table=pd.DataFrame()

tickers = ticker_index.copy()
new_index = []
retry_ticker = []
count = 0

for p in tickers:
#     print(p)
    try:
        extra_ratio=si.get_stats_valuation(p)
        extra_ratio = extra_ratio.iloc[:,0:2]
        extra_ratio.index=extra_ratio['Unnamed: 0']
        extra_ratio=extra_ratio.drop(labels='Unnamed: 0',axis=1)
        new_table=extra_ratio.T
        table=table.append(new_table)  #Table having Data about the company
        new_index.append(p)
        time.sleep(10)
    except:
        count = count+1
        print('Bad Ticker {}: {}'.format(count, p))
        retry_ticker.append(p)
        time.sleep(60*5)
        
if len(retry_ticker) > 0:     
    time.sleep(60*20)
    count = 0

    for p in retry_ticker:
    #     print(p)
        try:
            data=si.get_stats(p)
            data.index=data["Attribute"]
            data=data.drop(labels="Attribute",axis=1)
            raw_table=data.T
            raw_table['current_price'] = round(si.get_live_price(p),2)
            table=table.append(raw_table)   #Table having Data about the company
            new_index.append(p)
            time.sleep(10)
        except:
            count = count+1
            print('Bad Ticker 2nd attempt {}: {}'.format(count, p))
            time.sleep(60*5)
        
table.index=new_index
table2 = table[ratio_valuation_function]


final=pd.concat([table2,table1],axis=1)


final.to_csv('../ProjectDatasets/final_recommendations_int.csv', index=True, index_label='ticker')
print(final.shape)


# # Evaluations


final['Trailing P/E'] = pd.to_numeric(final['Trailing P/E'], errors='coerce')
final['Price/Book (mrq)'] = pd.to_numeric(final['Price/Book (mrq)'], errors='coerce')


# low_valuations
final = final[(final['Trailing P/E'].astype(float)<40) & (final['Price/Book (mrq)'].astype(float) < 15)].copy()

# earning_power
final = final[final['Diluted EPS (ttm)'].astype(float) > 4].copy()

# equity_to_debt
final = final[(final['Total Debt/Equity (mrq)'].astype(float)< 75 )].copy() # Filter for Debt to Equity
final = final[(final['Return on Equity (ttm)'] > str(20) )].copy() # Filter for ROE

# insider_owned
final = final[final['% Held by Insiders 1']>str(.07)].copy()


FINAL = pd.concat([tickersDF,final], axis=1, join='inner')
FINAL.sort_values(by=['current_price'], inplace=True)


FINAL.head()


FINAL.to_csv('../ProjectDatasets/final_recommendations.csv', index=True, index_label='ticker')


FINAL.shape


stop = timeit.default_timer()

print('Time (hrs): ', ((stop - start)/60)/60)  

