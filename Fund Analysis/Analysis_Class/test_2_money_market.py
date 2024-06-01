import pandas as pd
import Analysis_class
import yfinance as yf
import numpy as np


rank_file_path=''
Trading_days = 250
trading_days=250





df_target_2 =pd.read_csv('Fund_2.csv')


df_target_2['7日年化收益率（%）'] = df_target_2['7日年化收益率（%）'].str.rstrip('%').astype('float') / 100.0

df_target_2['return'] = (df_target_2['7日年化收益率（%）']+1)**(1/trading_days)-1
print (df_target_2['return'])




##calculate net return
df_background = pd.read_csv('Background.csv')
print (df_background)
management_fee = df_background['管理费率'].iloc[0].split("%")[0]


management_fee = float(management_fee)/100
print (management_fee)
custody_fee = df_background['托管费率'].iloc[0].split("%")[0]
custody_fee = float(custody_fee)/100


sales_fee = df_background['销售服务费率'].iloc[0].split("%")[0]
sales_fee = float(sales_fee )/100

df_target_2['net_return']=df_target_2['return']-(custody_fee+management_fee+sales_fee)/Trading_days

#df_target['fee_gap'] = df_target['net_return']-df_target['return']

df_target_2.to_csv('sample_feature.csv')
#Analysis_class.rolling_volatility(df_target, index_comps[comp_1_name])



