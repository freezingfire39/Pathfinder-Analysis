import pandas as pd
import Analysis_class
import yfinance as yf
import numpy as np


rank_file_path=''
Ticker = "000001"
Trading_days = 250
trading_days=250

print (Ticker)


df_target = pd.read_csv('Fund_1.csv')
df_target_2 =pd.read_csv('Fund_2.csv')


df_target_2['7日年化收益率（%）'] = df_target_2['7日年化收益率（%）'].str.rstrip('%').astype('float') / 100.0

df_target_2['return'] = (df_target_2['7日年化收益率（%）']+1)**(1/trading_days)-1
print (df_target_2['return'])


df_target = df_target.iloc[::-1]
risk_free_rate=0.0
df_target.set_index('净值日期',inplace=True)
df_target.index = pd.to_datetime(df_target.index)
df_target['return'] = df_target['累计净值'].pct_change()

df_target['annual_return'] = (1+df_target['return']).rolling(window=trading_days).apply(np.prod, raw=True)
rank_file = pd.read_csv(rank_file_path+'return_rank.csv').set_index('Unnamed: 0')
if df_target['annual_return'][-1] > 1.3:

    new_row = {'ticker': Ticker, 'value': df_target['annual_return'][-1]}
    rank_file.loc[len(rank_file)] = new_row
    rank_file.to_csv(rank_file_path+'return_rank.csv')


##calculate net return
df_background = pd.read_csv('Background.csv')
print (df_background)
management_fee = df_background['管理费率'].iloc[0].split("%")[0]


management_fee = float(management_fee)/100
print (management_fee)
custody_fee = df_background['托管费率'].iloc[0].split("%")[0]
custody_fee = float(custody_fee)/100

df_target['net_return']=df_target['return']-(custody_fee+management_fee)/Trading_days

#df_target['fee_gap'] = df_target['net_return']-df_target['return']




index_comps = pd.read_csv('index_comps.csv').set_index('Date')
industry_comps = pd.read_csv('industry_comps.csv').set_index('Date')
index_comps.index = pd.to_datetime(index_comps.index)
industry_comps.index = pd.to_datetime(industry_comps.index)


comp_1_name,comp_2_name, df_target = Analysis_class.corr_analysis(df_target,industry_comps,Ticker,rank_file_path, rank_file_path)



comp_3_name,comp_4_name, df_target = Analysis_class.corr_analysis(df_target,index_comps,Ticker,rank_file_path, rank_file_path)





df_target['rolling_mean'] = df_target['return'].rolling(trading_days).mean()
df_target['comp_mean'] = industry_comps[comp_1_name].rolling(trading_days).mean()

df_target = Analysis_class.rolling_sharpe(df_target,rank_file_path = rank_file_path, security_code = Ticker)

df_target = Analysis_class.max_drawdown_analysis(df_target,rank_file_path = rank_file_path, security_code = Ticker)

if comp_1_name in industry_comps:
    df_target = Analysis_class.alpha_beta_analysis(df_target, industry_comps[comp_1_name],rank_file_path = rank_file_path, security_code = Ticker)
else:
    df_target = Analysis_class.alpha_beta_analysis(df_target, index_comps[comp_1_name],rank_file_path = rank_file_path, security_code = Ticker)



df_target['comp_1'] = industry_comps[comp_1_name]
df1 = df_target[['累计净值', 'comp_1']]

# Resample to month end and calculate the monthly percent change
df_rets_monthly = df1.resample('M').last().pct_change().dropna()
df_target = Analysis_class.market_capture_ratio(df_rets_monthly, df_target, rank_file_path = rank_file_path, security_code = Ticker)

print (df_target)

if comp_1_name in industry_comps:
    df_target = Analysis_class.rolling_volatility(df_target, industry_comps[comp_1_name],rank_file_path = rank_file_path, security_code = Ticker)
else:
    df_target = Analysis_class.rolling_volatility(df_target, index_comps[comp_1_name],rank_file_path = rank_file_path, security_code = Ticker)

df_target = Analysis_class.plot_drawdown_underwater(df_target)

Analysis_class.create_interesting_times_tear_sheet(df_target['return'])
Analysis_class.create_interesting_times_tear_sheet(df_target['return'], benchmark_rets=df_target['comp_1'].pct_change())




df_target.to_csv('sample_feature.csv')
#Analysis_class.rolling_volatility(df_target, index_comps[comp_1_name])



