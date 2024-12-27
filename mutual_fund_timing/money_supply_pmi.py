import tushare as ts
pro = ts.pro_api('84be1015becc0b9dbbab507552c328cbf447bc02cbd29cfa09029bc6')

#获取单日全部股票数据
df = pro.cn_pmi(start_m='201901', end_m='202411')
df = df.iloc[::-1]
df.set_index('MONTH',inplace=True)
df.index = pd.to_datetime(df.index,format='%Y%m')

print (df.head(20))
df = df.resample('M').last()

#### import os, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import investpy
import yfinance as yf
import pywt

copper_future_1 = pro.fut_daily(ts_code='IH.CFX', start_date='20190115', end_date='20241215').set_index('trade_date')
copper_future_2 = pro.fut_daily(ts_code='IF.CFX', start_date='20190115', end_date='20241215').set_index('trade_date')

copper_future_1 = copper_future_1.iloc[::-1]
copper_future_2 = copper_future_2.iloc[::-1]

copper_future_1.index = pd.to_datetime(copper_future_1.index)
copper_future_2.index = pd.to_datetime(copper_future_2.index)

copper_future_1 = copper_future_1.resample('M').last()

copper_future_1['return'] = copper_future_1['close'].pct_change()
copper_future_2['return'] = copper_future_2['close'].pct_change()

copper_future_1['return_2'] = copper_future_1['open']/copper_future_1['close'].shift(1)-1

df_drop=[]
for i in copper_future_1.index:
    if i not in df.index:
        df_drop.append(i)
copper_future_1 = copper_future_1.drop(df_drop, axis=0)

df_drop=[]
for i in df.index:
    if i not in copper_future_1.index:
        df_drop.append(i)
df = df.drop(df_drop, axis=0)

copper_future_1['gap'] = df['PMI020400'].pct_change()

copper_future_1['gap'] = copper_future_1['gap'].cumsum()
copper_future_1['gap'].plot()
#copper_future_1.dropna(inplace=True)

print (copper_future_1)




df_drop=[]
for i in copper_future_1.index:
    if i not in copper_future_2.index:
        df_drop.append(i)
copper_future_1 = copper_future_1.drop(df_drop, axis=0)

df_drop=[]
for i in copper_future_2.index:
    if i not in copper_future_1.index:
        df_drop.append(i)
copper_future_2 = copper_future_2.drop(df_drop, axis=0)
copper_future_1.fillna(method='ffill',inplace=True)
print (copper_future_1)
print (copper_future_2)
copper_future_2['zscore'] = (copper_future_1['gap'] - copper_future_1['gap'].rolling(10).mean())/copper_future_1['gap'].rolling(10).std(ddof=0)




copper_future_2['trade'] = 0
copper_future_2['trade'] = copper_future_2['trade'].astype('float64')
for i in range(len(copper_future_2)):
    if i<1:
        continue
        #if df_return['zscore'][i-1]>=1.2:
        #    df_return['trade'][i]=-1
    #if copper_future_2['return'][i-1]<-0.03:
    #    copper_future_2['trade'][i:i+2]=1
    
    #elif copper_future_2['zscore'][i-1]>=1.3:
    #    copper_future_2['trade'][i:i+3]=-1
    
    if copper_future_2['zscore'][i-1]<=-1.4 and copper_future_2['zscore'][i-1]>=-2.:
        copper_future_2['trade'][i:i+1]=1
    

    elif copper_future_2['zscore'][i-1]>=1.4 and copper_future_2['zscore'][i-1]<=2.:
        copper_future_2['trade'][i:i+1]=-1
    elif copper_future_2['zscore'][i-1]<=1.4 and copper_future_2['zscore'][i-1]>=0.6:
        copper_future_2['trade'][i:i+1]=-1
    

    elif copper_future_2['zscore'][i-1]>=-1.4 and copper_future_2['zscore'][i-1]<=-0.6:
        copper_future_2['trade'][i:i+1]=1


    elif copper_future_2['zscore'][i-1]<=-0 and copper_future_2['zscore'][i-1]>=-0.6:
        copper_future_2['trade'][i:i+1]=-1
    

    elif copper_future_2['zscore'][i-1]>=0 and copper_future_2['zscore'][i-1]<=0.6:
        copper_future_2['trade'][i:i+1]=1

    if copper_future_2['zscore'][i-1]>=2.:
        copper_future_2['trade'][i:i+1]=1
    

    elif copper_future_2['zscore'][i-1]<=-2.:
        copper_future_2['trade'][i:i+1]=-1
    #elif copper_future_2['zscore'][i-1]<=0.2 and copper_future_2['zscore'][i-1]>=-0.2:
    #    copper_future_2['trade'][i:]=0





copper_future_2['full_return'] = copper_future_2['trade']*(copper_future_1['return'])
import pyfolio_master as pf
#df_trade = pd.to_numeric(df_trade, errors='coerce')
copper_future_2.index = pd.to_datetime(copper_future_2.index)
pf.create_full_tear_sheet(copper_future_2['full_return'])
print (copper_future_2)
    
if copper_future_2['zscore'][-1]<=-0.7:
    print (2)
    
elif copper_future_2['zscore'][-1]<=-0.2 and copper_future_2['zscore'][-1]>=-0.7:
    print (1)
elif copper_future_2['zscore'][-1]>=0.4 and copper_future_2['zscore'][-1]<=1.4:
    print (-1)

