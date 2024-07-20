import pandas as pd
from pathlib import Path
home = str(Path.home())
def main(asset_type,path):
    # asset_type='stock_'
    # #asset_type='bond_'
    # #asset_type='money_market_'
    # #asset_type='overseas_'

    path = path + asset_type

    rolling_sharpe_df = pd.DataFrame(columns=['ticker','value'])
    rolling_sharpe_df['ticker']=rolling_sharpe_df['ticker'].astype(str)



    rolling_sharpe_df.to_csv(path+'rolling_sharpe_benchmark.csv')
    rolling_sharpe_df.to_csv(path+'excess_sharpe_benchmark.csv')
    rolling_sharpe_df.to_csv(path+'drawdown_duration_benchmark.csv')
    rolling_sharpe_df.to_csv(path+'drawdown_amount_benchmark.csv')
    rolling_sharpe_df.to_csv(path+'return_benchmark.csv')
    rolling_sharpe_df.to_csv(path+'CAGR_benchmark.csv')
    rolling_sharpe_df.to_csv(path+'upside_capture_benchmark.csv')
    rolling_sharpe_df.to_csv(path+'downside_capture_benchmark.csv')
    rolling_sharpe_df.to_csv(path+'alpha_benchmark.csv')
    rolling_sharpe_df.to_csv(path+'positive_beta_benchmark.csv')
    rolling_sharpe_df.to_csv(path+'negative_beta_benchmark.csv')
    rolling_sharpe_df.to_csv(path+'volatility_benchmark.csv')


    ##index


if __name__ == '__main__':
    input_file_path = home + '/Desktop/output_china'
    # output_file_path = home + '/Desktop/output_china'
    try:
        asset_type='stock_'
        path = home + '/Desktop/output_search/'
        main(asset_type, path)
        asset_type='bond_'
        main(asset_type, path)
        asset_type='money_market_'
        main(asset_type, path)
        asset_type='overseas_'
        main(asset_type, path)
    except Exception as e:
        raise AirflowException("fail to run at error ", e)
