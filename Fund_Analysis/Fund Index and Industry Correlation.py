#search_result = investpy.search_quotes(text='Blackrock', products=['funds'],
#                                       countries=['united states'], n_results=1)
import investpy
import pandas as pd
import pyfolio as pf
import yfinance as yf
#print (search_result)
df = investpy.get_funds_list(country="China")
print(len(df))
print (df)
nasdaqdatalink.ApiConfig.api_key = 'znxYqt7DpE3soUMDRfGE'
security = '510500' ##target name
df_target = nasdaqdatalink.get_table('DY/EMPRIA', security=security)
df_target = df_target.iloc[::-1]
df_target.set_index('date',inplace=True)
df_target.index = pd.to_datetime(df_target.index)

#index_etf_1 = yf.download("510050.SS", start="2021-06-01", end="2023-11-15") ##A50
#index_etf_2 = yf.download("159901.SZ", start="2021-06-01", end="2023-11-15") ##Shenzhen100
#index_etf_3 = yf.download("159949.SZ", start="2021-06-01", end="2023-11-15") ##chuangye50
#index_etf_4 = yf.download("510300.SS", start="2021-06-01", end="2023-11-15") ##husheng300
#index_etf_5 = yf.download("510500.SS", start="2021-06-01", end="2023-11-15") ##zhongzheng500
#index_etf_6 = yf.download("512100.SS", start="2021-06-01", end="2023-11-15") ##zhongzheng1000
#index_etf_7 = yf.download("588000.SS", start="2021-06-01", end="2023-11-15") ##kechuang50
#index_etf_8 = yf.download("510900.SS", start="2021-06-01", end="2023-11-15") ##HangSeng
start = datetime(2017, 1, 1)
symbols_list = ['510050.SS', '159901.SZ', '159949.SZ', '510300.SS', '510500.SS', '512100.SS', '588000.SS', '510900.SS']
#array to store prices
symbols=[]

#array to store prices
symbols=[]
for ticker in symbols_list:
    r = yf.download(ticker, start=start, end="2024-04-05")
    # add a symbol column
    r['Symbol'] = ticker
    symbols.append(r)
# concatenate into df
df = pd.concat(symbols)
df = df.reset_index()
df = df[['Date', 'Close', 'Symbol']]
df.head()
df_pivot=df.pivot('Date','Symbol','Close').reset_index()


df_pivot.set_index('Date',inplace=True)
df_pivot.index = pd.to_datetime(df_pivot.index)

df_pivot.head()
df_pivot[security] = df_target['close']





print (df_pivot)



corr_df = df_pivot.corr(method='pearson')
#reset symbol as index (rather than 0-X)
corr_df.head().reset_index()
#del corr_df.index.name
corr_df.head(10)

plt.figure(figsize=(13, 8))
seaborn.heatmap(corr_df, annot=True, cmap='RdYlGn')
plt.figure()
df_new = corr_df[security].drop(corr_df[security].idxmax())
comp_1_name = df_new.idxmax()

#index_etf_1 = yf.download("510230.SS", start="2021-06-01", end="2023-11-15") ##finance
#index_etf_2 = yf.download("512010.SS", start="2021-06-01", end="2023-11-15") ##Pharmaceutical
#index_etf_3 = yf.download("512170.SS", start="2021-06-01", end="2023-11-15") ##healthcare
#index_etf_4 = yf.download("515170.SS", start="2021-06-01", end="2023-11-15") ##food&bev
#index_etf_5 = yf.download("516160.SS", start="2021-06-01", end="2023-11-15") ##new energy
#index_etf_6 = yf.download("512480.SS", start="2021-06-01", end="2023-11-15") ##semiconductor
#index_etf_7 = yf.download("515230.SS", start="2021-06-01", end="2023-11-15") ##software
#index_etf_8 = yf.download("512660.SS", start="2021-06-01", end="2023-11-15") ##military
#index_etf_9 = yf.download("516220.SS", start="2021-06-01", end="2023-11-15") ##chemistry
#index_etf_10 = yf.download("516800.SS", start="2021-06-01", end="2023-11-15") ##manufacturing
#index_etf_11 = yf.download("512400.SS", start="2021-06-01", end="2023-11-15") ##metal
#index_etf_12 = yf.download("159825.SZ", start="2021-06-01", end="2023-11-15") ##agriculture
#index_etf_13 = yf.download("516950.SS", start="2021-06-01", end="2023-11-15") ##infrastructure
#index_etf_14 = yf.download("516070.SS", start="2021-06-01", end="2023-11-15") ##environmental

start = datetime(2017, 1, 1)
symbols_list = ['510230.SS', '512010.SS', '512170.SS', '515170.SS', '512480.SS', '515230.SS', '512660.SS', '516220.SS','516800.SS',"512400.SS","159825.SZ","516950.SS","516070.SS"]
#array to store prices
symbols=[]

#array to store prices
symbols=[]
for ticker in symbols_list:
    r = yf.download(ticker, start=start, end="2024-04-05")
    # add a symbol column
    r['Symbol'] = ticker
    symbols.append(r)
# concatenate into df
df = pd.concat(symbols)
df = df.reset_index()
df = df[['Date', 'Close', 'Symbol']]
df.head()
df_pivot=df.pivot('Date','Symbol','Close').reset_index()


df_pivot.set_index('Date',inplace=True)
df_pivot.index = pd.to_datetime(df_pivot.index)

df_pivot.head()
df_pivot[security] = df_target['close']

corr_df = df_pivot.corr(method='pearson')
#reset symbol as index (rather than 0-X)
corr_df.head().reset_index()
#del corr_df.index.name
corr_df.head(10)

plt.figure(figsize=(13, 8))
seaborn.heatmap(corr_df, annot=True, cmap='RdYlGn')
plt.figure()

