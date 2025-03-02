import tushare as ts
pro = ts.pro_api('84be1015becc0b9dbbab507552c328cbf447bc02cbd29cfa09029bc6')

#获取单日全部股票数据

output_file_path=''


df = pro.moneyflow_mkt_dc(start_date='20190115', end_date='20250215').set_index('trade_date')
df = df.iloc[::-1]
df.index = pd.to_datetime(df.index)

print (df.head(20))

df_2 = pro.index_daily(ts_code='399300.SZ', start_date='20190115', end_date='20250215').set_index('trade_date')
df_2 = df_2.iloc[::-1]
df_2.index = pd.to_datetime(df_2.index)

print (df_2)

df_drop=[]
for i in df.index:
    if i not in df_2.index:
        df_drop.append(i)
df = df.drop(df_drop, axis=0)

df_drop=[]
for i in df_2.index:
    if i not in df.index:
        df_drop.append(i)
df_2 = df_2.drop(df_drop, axis=0)



#### import os, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import investpy


df['gap'] = (df['net_amount_rate'].pct_change())

#df['gap'] = df['gap'].cumsum()

from scipy.signal import qspline1d, qspline1d_eval
df['gap_3']=0
df['gap_3'] = df['gap_3'].astype('float64')
time_step = 1

from scipy.signal import butter, sosfilt, hilbert, lfilter
def butter_bandpass(lowcut,highcut,fs,order=8):
    nyq = 0.5*fs
    low = lowcut/nyq
    high = highcut/nyq

    b,a = butter(order, [low, high], btype='band')
    return b,a

def butter_bandpass_filter(data,lowcut,highcut,fs,order=8):
    b,a = butter_bandpass(lowcut,highcut,fs,order=order)
    return lfilter(b,a,data)

from scipy.signal import qspline1d, qspline1d_eval,sosfiltfilt

from scipy import fftpack

for i in range(len(df['gap'])):
    if i <30:
        continue


    
    
    df_temp = df['gap'][i-30:i]
    sos = butter(4, 0.125, output='sos')
    data_bp8 = hilbert(df_temp)
    data_bp2 = butter_bandpass_filter(df_temp,500,2000,20000,2)

    df['gap_3'][i] = data_bp8[-1]
    
    
    



df['zscore'] = (df['gap_3'] - df['gap_3'].rolling(10).mean())/df['gap_3'].rolling(10).std(ddof=0)


df['trade'] = 0
df['trade'] = df['trade'].astype('float64')
for i in range(len(df)):
    if i<1:
        continue

    
    if df['zscore'][i-2]<=-0.8 and df['zscore'][i-2]>=-1.8:
        df['trade'][i:i+1]=-1
    

    elif df['zscore'][i-2]>=0.8 and df['zscore'][i-2]<=1.8:
        df['trade'][i:i+1]=1

    elif df['zscore'][i-2]<=0.8 and df['zscore'][i-2]>=0.1:
        df['trade'][i:i+1]=-1
    

    elif df['zscore'][i-2]>=-0.8 and df['zscore'][i-2]<=-0.1:
        df['trade'][i:i+1]=1

    if df['zscore'][i-2]>=1.8:
        df['trade'][i:i+1]=-1
    

    elif df['zscore'][i-2]<=-1.8:
        df['trade'][i:i+1]=1

df['full_return'] = df['trade']*(df_2['open'].pct_change())

import pyfolio_master as pf
#df_trade = pd.to_numeric(df_trade, errors='coerce')
df.index = pd.to_datetime(df.index)
pf.create_full_tear_sheet(df['full_return'])
print (df.tail(30))


