import pandas as pd
import Analysis_class_portfolio as Analysis_class
import yfinance as yf
import numpy as np


asset_type='stock_'
#asset_type='bond_'
#asset_type='money_market_'
#asset_type='overseas_'


input_file_path=''  ##ticker_information fund_1
background_file_path='Background.csv'
return_rank_file_path=asset_type+'return_rank.csv'
cagr_rank_file_path=asset_type+'CAGR_rank.csv'  ##return_rank_csv
rank_file_path=''+asset_type  ##all other filter csv
comp_file_path='index_comps.csv'
comp_file_path_2='industry_comps.csv'
save_file_path='sample_feature.csv'
Ticker = "Port_1"
Trading_days = 250
trading_days=250

print (Ticker)



import json
import pandas as pd
from pandas.io.json import json_normalize
data = json.load(open(input_file_path+'response.json'))
df = json_normalize(data['portfolio'], max_level=2)
return_list = df['returns'].to_list()
data = json_normalize(return_list)
data = data.transpose()
df2 = pd.json_normalize(data.iloc[:, 0])
df2['date'] = pd.to_datetime(df2['date']).dt.date
df_target = df2.set_index('date')

df_target.index = pd.to_datetime(df_target.index)
df_target['return'] = df_target['value']


rolling_sharpe_df = pd.DataFrame(index=df_target.index,columns=['rolling_SR_comments','excess_return_comments', 'alpha_comments','beta_comments','upside_capture_comments','downside_capture_comments','index_comments','sector_comments','volatility_comments','drawdown_amount_comments', 'drawdown_duration_comments', 'return_comments','return_corr_comments','return_benchmark_comments', 'alpha_benchmark_comments','beta_benchmark_comments','upside_benchmark_comments','downside_benchmark_comments','excess_sharpe_benchmark_comments','sr_benchmark_comments','drawdown_duration_benchmark_comments','drawdown_amount_benchmark_comments','volatility_benchmark_comments'])
rolling_sharpe_df.to_csv('comments.csv')








df_target['annual_return'] = (1+df_target['return']).rolling(window=trading_days).apply(np.prod, raw=True)-1





##calculate net return

index_comps = pd.read_csv(comp_file_path).set_index('Date')
industry_comps = pd.read_csv(comp_file_path_2).set_index('Date')
index_comps.index = pd.to_datetime(index_comps.index)
industry_comps.index = pd.to_datetime(industry_comps.index)






comp_3_name,comp_4_name, df_target = Analysis_class.corr_analysis(df_target,industry_comps,Ticker,rank_file_path, rank_file_path,input_file_path=input_file_path)


comp_1_name,comp_2_name, df_target = Analysis_class.corr_analysis(df_target,index_comps,Ticker,rank_file_path, rank_file_path,input_file_path=input_file_path)


df_target['rolling_mean'] = df_target['return'].rolling(trading_days).mean()
df_target['comp_mean'] = index_comps[comp_1_name].rolling(trading_days).mean()


df_target['comp_1'] = index_comps[comp_1_name]
df_target['excess_return']=df_target['return']-df_target['comp_1'].pct_change()


df_target = Analysis_class.rolling_sharpe(df_target,rank_file_path = rank_file_path, input_file_path = input_file_path,asset_type=asset_type, security_code = Ticker)

df_target = Analysis_class.return_analysis(df_target,input_file_path = input_file_path,rank_file_path = rank_file_path,asset_type=asset_type )


df_target = Analysis_class.max_drawdown_analysis(df_target,rank_file_path = rank_file_path, security_code = Ticker,input_file_path=input_file_path)

if comp_1_name in industry_comps:
    df_target = Analysis_class.alpha_beta_analysis(df_target, industry_comps[comp_1_name],rank_file_path = rank_file_path,input_file_path = input_file_path, security_code = Ticker)
else:
    df_target = Analysis_class.alpha_beta_analysis(df_target, index_comps[comp_1_name],rank_file_path = rank_file_path,input_file_path = input_file_path, security_code = Ticker)


df_target['累计净值'] = (1+df_target['return']).cumprod()

df1 = df_target[['累计净值', 'comp_1']]

# Resample to month end and calculate the monthly percent change

df_rets_monthly = df1.resample('M').last().pct_change().dropna()

df_target = Analysis_class.market_capture_ratio(df_rets_monthly, df_target, rank_file_path = rank_file_path, input_file_path = input_file_path,security_code = Ticker)

print (df_target)

if comp_1_name in industry_comps:
    df_target = Analysis_class.rolling_volatility(df_target, industry_comps[comp_1_name],rank_file_path = rank_file_path,input_file_path = input_file_path, security_code = Ticker)
else:
    df_target = Analysis_class.rolling_volatility(df_target, index_comps[comp_1_name],rank_file_path = rank_file_path,input_file_path = input_file_path, security_code = Ticker)

df_target = Analysis_class.plot_drawdown_underwater(df_target)

Analysis_class.create_interesting_times_tear_sheet(df_target['return'])
Analysis_class.create_interesting_times_tear_sheet(df_target['return'], benchmark_rets=df_target['comp_1'].pct_change())




df_target.to_csv(save_file_path)
#Analysis_class.rolling_volatility(df_target, index_comps[comp_1_name])



