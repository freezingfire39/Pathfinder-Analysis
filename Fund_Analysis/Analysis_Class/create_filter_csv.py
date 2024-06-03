import pandas as pd
from pathlib import Path
home = str(Path.home())

asset_type='stock_'
#asset_type='bond_'
#asset_type='money_market_'
#asset_type='overseas_'



path = home + '/Desktop/output_search/' + asset_type

rolling_sharpe_df = pd.DataFrame(columns=['ticker','value'])
rolling_sharpe_df['ticker']=rolling_sharpe_df['ticker'].astype(str)

#technical
rolling_sharpe_df.to_csv(path+'rolling_sharpe_rank.csv')
rolling_sharpe_df.to_csv(path+'drawdown_duration_rank.csv')
rolling_sharpe_df.to_csv(path+'drawdown_amount_rank.csv')
rolling_sharpe_df.to_csv(path+'return_rank.csv')
rolling_sharpe_df.to_csv(path+'CAGR_rank.csv')
rolling_sharpe_df.to_csv(path+'upside_capture_rank.csv')
rolling_sharpe_df.to_csv(path+'downside_capture_rank.csv')
rolling_sharpe_df.to_csv(path+'alpha_rank.csv')
rolling_sharpe_df.to_csv(path+'positive_beta_rank.csv')
rolling_sharpe_df.to_csv(path+'negative_beta_rank.csv')
rolling_sharpe_df.to_csv(path+'volatility_rank.csv')


##index
rolling_sharpe_df.to_csv(path+'A50.csv')
rolling_sharpe_df.to_csv(path+'Shenzhen100.csv')
rolling_sharpe_df.to_csv(path+'Chuangye50.csv')
rolling_sharpe_df.to_csv(path+'Hushen300.csv')
rolling_sharpe_df.to_csv(path+'Zhongzheng500.csv')
rolling_sharpe_df.to_csv(path+'Zhongzheng1000.csv')
rolling_sharpe_df.to_csv(path+'Kechuang50.csv')
rolling_sharpe_df.to_csv(path+'Hangseng.csv')


##Sector
rolling_sharpe_df.to_csv(path+'Finance.csv')
rolling_sharpe_df.to_csv(path+'Pharmaceutical.csv')
rolling_sharpe_df.to_csv(path+'Healthcare.csv')
rolling_sharpe_df.to_csv(path+'FoodBeverage.csv')
rolling_sharpe_df.to_csv(path+'Energy.csv')
rolling_sharpe_df.to_csv(path+'Semiconductor.csv')
rolling_sharpe_df.to_csv(path+'Software.csv')
rolling_sharpe_df.to_csv(path+'Military.csv')
rolling_sharpe_df.to_csv(path+'Chemicals.csv')
rolling_sharpe_df.to_csv(path+'Manufacturing.csv')
rolling_sharpe_df.to_csv(path+'Metal.csv')
rolling_sharpe_df.to_csv(path+'Agriculture.csv')
rolling_sharpe_df.to_csv(path+'Infrastructure.csv')
rolling_sharpe_df.to_csv(path+'Environmental.csv')

