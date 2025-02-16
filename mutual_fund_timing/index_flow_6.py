import tushare as ts
pro = ts.pro_api('84be1015becc0b9dbbab507552c328cbf447bc02cbd29cfa09029bc6')

#获取单日全部股票数据

output_file_path=''


df = pro.moneyflow_mkt_dc(start_date='20190115', end_date='20250215').set_index('trade_date')
df = df.iloc[::-1]
df.index = pd.to_datetime(df.index)

print (df.head(20))



#### import os, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import investpy


df['gap'] = (df['buy_lg_amount_rate']-df['buy_elg_amount_rate'])

#df['gap'] = df['gap'].cumsum()

df['gap'].plot()


df['zscore'] = (df['gap'] - df['gap'].rolling(10).mean())/df['gap'].rolling(10).std(ddof=0)


df['trade'] = 0
df['trade'] = df['trade'].astype('float64')
for i in range(len(df)):
    if i<1:
        continue

    
    if df['zscore'][i-1]<=-0.8 and df['zscore'][i-1]>=-2.6:
        df['trade'][i:i+1]=1
    

    elif df['zscore'][i-1]>=0.8 and df['zscore'][i-1]<=2.6:
        df['trade'][i:i+1]=-1
    elif df['zscore'][i-1]<=0.8 and df['zscore'][i-1]>=0.:
        df['trade'][i:i+1]=1
    

    elif df['zscore'][i-1]>=-0.8 and df['zscore'][i-1]<=-0.:
        df['trade'][i:i+1]=-1


df['full_return'] = df['trade']*(df['close_sh'].pct_change())
import pyfolio_master as pf
#df_trade = pd.to_numeric(df_trade, errors='coerce')
df.index = pd.to_datetime(df.index)
pf.create_full_tear_sheet(df['full_return'])
print (df.tail(30))


