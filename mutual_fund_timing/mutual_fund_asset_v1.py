import os, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


df_test_1 = pd.read_csv('sample_feature.csv').set_index('净值日期')
df_test_1.index = pd.to_datetime(df_test_1.index)




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


df_test = pd.DataFrame()

df_test['return'] = df_test_1['return'].resample('3M').sum()

df_drop=[]
for i in df_test.index:
    if i not in df_asset.index:
        df_drop.append(i)
df_test = df_test.drop(df_drop, axis=0)

df_drop=[]
for i in df_asset.index:
    if i not in df_test.index:
        df_drop.append(i)
df_asset = df_asset.drop(df_drop, axis=0)



df_test['zscore'] = (df_asset['asset_change']  - df_asset['asset_change'].rolling(5).mean())/df_asset['asset_change'].rolling(5).std(ddof=0)
print (df_test)
df_test['trade'] = 0
df_test['trade'] = df_test['trade'].astype('float64')
for i in range(len(df_test)):
    if i<1:
        continue

    if df_test['zscore'][i-1]>=0.2:
        df_test['trade'][i:i+1]=1



df_test['full_return'] = df_test['trade']*df_test['return']
import pyfolio_master as pf
#df_trade = pd.to_numeric(df_trade, errors='coerce')

pf.create_full_tear_sheet(df_test['full_return'])
