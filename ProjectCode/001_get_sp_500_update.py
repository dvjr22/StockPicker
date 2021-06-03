#!/usr/bin/env python
# coding: utf-8

import pandas as pd


url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
file_scp_500 = '../ProjectDatasets/sp_500_info.csv'
file_scp_symbol = '../ProjectDatasets/sp_500_symbols.csv'

table = pd.read_html(url)
df = table[0]

df['Symbol'] = df['Symbol'].str.replace(r'\.', '-')

df.to_csv(file_scp_500)
df.to_csv(file_scp_symbol, columns=['Symbol'],index=False,header=True)

