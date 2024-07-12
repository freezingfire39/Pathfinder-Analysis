import os, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


df_test_1 = pd.read_csv('sample_feature_000552_bond.csv').set_index('净值日期')
df_test_1.index = pd.to_datetime(df_test_1.index)

df_test_2 = pd.read_csv('sample_feature_000415_bond.csv').set_index('净值日期')
df_test_2.index = pd.to_datetime(df_test_2.index)


df_test_3 = pd.read_csv('sample_feature_001309_stock.csv').set_index('净值日期')
df_test_3.index = pd.to_datetime(df_test_3.index)

df_test_4 = pd.read_csv('sample_feature_160719_gold.csv').set_index('净值日期')
df_test_4.index = pd.to_datetime(df_test_4.index)

df_test_1 = df_test_1['累计净值'].resample('D').last()
df_test_1 = df_test_1.to_frame()
df_test_1.reset_index(inplace=True)
from pandas.tseries.offsets import BDay
isBusinessDay = BDay().onOffset
match_series = pd.to_datetime(df_test_1['净值日期']).map(isBusinessDay)
df_test_1 = df_test_1[match_series]
df_test_1.set_index('净值日期',inplace=True)
df_test_1 = df_test_1.fillna(method='ffill')

df_test_1['return'] = df_test_1['累计净值'].pct_change()



df_test_2 = df_test_2['累计净值'].resample('D').last()
df_test_2 = df_test_2.to_frame()
df_test_2.reset_index(inplace=True)
from pandas.tseries.offsets import BDay
isBusinessDay = BDay().onOffset
match_series = pd.to_datetime(df_test_2['净值日期']).map(isBusinessDay)
df_test_2 = df_test_2[match_series]
df_test_2.set_index('净值日期',inplace=True)
df_test_2 = df_test_2.fillna(method='ffill')

df_test_2['return'] = df_test_2['累计净值'].pct_change()

df_test_3 = df_test_3['累计净值'].resample('D').last()
df_test_3 = df_test_3.to_frame()
df_test_3.reset_index(inplace=True)
from pandas.tseries.offsets import BDay
isBusinessDay = BDay().onOffset
match_series = pd.to_datetime(df_test_3['净值日期']).map(isBusinessDay)
df_test_3 = df_test_3[match_series]
df_test_3.set_index('净值日期',inplace=True)
df_test_3 = df_test_3.fillna(method='ffill')

df_test_3['return'] = df_test_3['累计净值'].pct_change()


df_test_4 = df_test_4['累计净值'].resample('D').last()
df_test_4 = df_test_4.to_frame()
df_test_4.reset_index(inplace=True)
from pandas.tseries.offsets import BDay
isBusinessDay = BDay().onOffset
match_series = pd.to_datetime(df_test_4['净值日期']).map(isBusinessDay)
df_test_4 = df_test_4[match_series]
df_test_4.set_index('净值日期',inplace=True)
df_test_4 = df_test_4.fillna(method='ffill')

df_test_4['return'] = df_test_4['累计净值'].pct_change()


df_asset = pd.read_csv('Asset.csv')

df_asset = df_asset.iloc[::-1]
df_asset.set_index('日期',inplace=True)
df_asset.index = pd.to_datetime(df_asset.index)
df_asset = df_asset.replace('---',0)
df_asset['期末净资产（亿元）'] = df_asset['期末净资产（亿元）'].apply(float)
df_asset['期间申购（亿份）'] = df_asset['期间申购（亿份）'].apply(float)
df_asset['期间赎回（亿份）'] = df_asset['期间赎回（亿份）'].apply(float)



df_asset['asset_change'] = df_asset['期末净资产（亿元）'].pct_change()
df_asset['asset_change_2'] = df_asset['期间申购（亿份）']-df_asset['期间申购（亿份）'].shift(1)
df_asset['asset_change_3'] = df_asset['期间赎回（亿份）']-df_asset['期间赎回（亿份）'].shift(1)
df_asset.replace([np.inf, -np.inf], np.nan, inplace=True)
df_asset.dropna(inplace=True)
(df_asset['期间申购（亿份）']-df_asset['期间赎回（亿份）']).cumsum().plot()




df_drop=[]
for i in df_test_1.index:
    if i not in df_test_2.index:
        df_drop.append(i)
df_test_1 = df_test_1.drop(df_drop, axis=0)

df_drop=[]
for i in df_test_1.index:
    if i not in df_test_4.index:
        df_drop.append(i)
df_test_1 = df_test_1.drop(df_drop, axis=0)


df_drop=[]
for i in df_test_1.index:
    if i not in df_test_3.index:
        df_drop.append(i)
df_test_1 = df_test_1.drop(df_drop, axis=0)


df_drop=[]
for i in df_test_2.index:
    if i not in df_test_1.index:
        df_drop.append(i)
df_test_2 = df_test_2.drop(df_drop, axis=0)

df_drop=[]
for i in df_test_3.index:
    if i not in df_test_1.index:
        df_drop.append(i)
df_test_3 = df_test_3.drop(df_drop, axis=0)

df_drop=[]
for i in df_test_4.index:
    if i not in df_test_1.index:
        df_drop.append(i)
df_test_4 = df_test_4.drop(df_drop, axis=0)



df_test = pd.DataFrame()








df_test['return'] = (df_test_1['return']+df_test_2['return'])/2

df_test['return_2'] = (df_test_3['return']+df_test_4['return'])/2


df_test['return'] = df_test['return']*0.9+df_test['return_2']*0.1


df_test['zscore'] = (df_asset['asset_change']  - df_asset['asset_change'].rolling(5).mean())/df_asset['asset_change'].rolling(5).std(ddof=0)
print (df_test)
df_test['trade'] = 0
df_test['trade'] = df_test['trade'].astype('float64')
for i in range(len(df_test)):
    if i<1:
        continue

    df_test['trade'][i:i+1]=1



df_test['full_return'] = df_test['trade']*df_test['return']
import pyfolio_master as pf
#df_trade = pd.to_numeric(df_trade, errors='coerce')

pf.create_full_tear_sheet(df_test['full_return'])
