# -*- coding: utf-8 -*-
"""
insert comments later
"""

import pandas as pd

url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
file_scp_500 = 'Data/sp_500_info.csv'
file_scp_symbol = "Data/sp_500_symbols.csv"

table = pd.read_html(url)
df = table[0]
df.to_csv(file_scp_500)
df.to_csv(file_scp_symbol, columns=['Symbol'],index=False,header=False)

df.head()

print('done')