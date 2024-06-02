import pandas as pd
import Analysis_class
import yfinance as yf
import numpy as np





#asset_type='stock_'
#asset_type='bond_'
asset_type='money_market_'
#asset_type='overseas_'

input_file_path='Fund_2.csv'
background_file_path='Background.csv'
rank_file_path=asset_type+''
return_rank_file_path=asset_type+'return_rank.csv'
Trading_days = 250
trading_days=250
save_file_path='sample_feature.csv'

df_target_2 =pd.read_csv(input_file_path)


df_target_2['7日年化收益率（%）'] = df_target_2['7日年化收益率（%）'].str.rstrip('%').astype('float') / 100.0

df_target_2['return'] = (df_target_2['7日年化收益率（%）']+1)**(1/trading_days)-1
print (df_target_2['return'])




##calculate net return
df_background = pd.read_csv(background_file_path)
print (df_background)
management_fee = df_background['管理费率'].iloc[0].split("%")[0]


management_fee = float(management_fee)/100
print (management_fee)
custody_fee = df_background['托管费率'].iloc[0].split("%")[0]
custody_fee = float(custody_fee)/100


sales_fee = df_background['销售服务费率'].iloc[0].split("%")[0]
sales_fee = float(sales_fee )/100

df_target_2['net_return']=df_target_2['return']-(custody_fee+management_fee+sales_fee)/Trading_days

df_target_2['累计净值'] =(1+df_target_2['return']).cumprod()


df_target_2['CAGR'] = 0

df_target_2['CAGR'][-1] = (df_target_2['累计净值'][-1])**(1/(len(df_target)/trading_days))

rank_file = pd.read_csv(return_rank_file_path).set_index('Unnamed: 0')
if df_target['annual_return'][-1] > 1.3:

    new_row = {'ticker': Ticker, 'value': df_target['annual_return'][-1]}
    rank_file.loc[len(rank_file)] = new_row
    rank_file.to_csv(return_rank_file_path)



#df_target['fee_gap'] = df_target['net_return']-df_target['return']

df_target_2.to_csv(save_file_path)
#Analysis_class.rolling_volatility(df_target, index_comps[comp_1_name])



