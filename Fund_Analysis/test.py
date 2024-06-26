import pandas as pd
import Analysis_class
import yfinance as yf

trading_days=250

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


index_comps = pd.read_csv('index_comps.csv').set_index('Date')
industry_comps = pd.read_csv('industry_comps.csv').set_index('Date')
index_comps.index = pd.to_datetime(index_comps.index)
industry_comps.index = pd.to_datetime(industry_comps.index)


comp_1_name,comp_2_name = Analysis_class.corr_analysis(df_target['累计净值'],industry_comps,"000001")


Analysis_class.rolling_sharpe(df_target)

Analysis_class.max_drawdown_analysis(df_target['return'])

try:
    Analysis_class.alpha_beta_analysis(df_target, industry_comps[comp_1_name])
except:
    Analysis_class.alpha_beta_analysis(df_target, index_comps[comp_1_name])



df_target['comp_1'] = industry_comps[comp_1_name]
df1 = df_target[['累计净值', 'comp_1']]

# Resample to month end and calculate the monthly percent change
df_rets_monthly = df1.resample('M').last().pct_change().dropna()
Analysis_class.market_capture_ratio(df_rets_monthly)

try:
    Analysis_class.rolling_volatility(df_target, industry_comps[comp_1_name])
except:
    Analysis_class.rolling_volatility(df_target, index_comps[comp_1_name])

