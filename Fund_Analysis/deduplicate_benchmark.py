import pandas as pd
from pathlib import Path
home = str(Path.home())
def main(asset_type,path):
    # asset_type='stock_'
    # #asset_type='bond_'
    # #asset_type='money_market_'
    # #asset_type='overseas_'

    path = path + asset_type



    benchmark_file_list = [path+'rolling_sharpe_benchmark.csv', ath+'excess_sharpe_benchmark.csv',
        path+'drawdown_duration_benchmark.csv', path+'drawdown_amount_benchmark.csv', path+'return_benchmark.csv', path+'CAGR_benchmark.csv', path+'upside_capture_benchmark.csv', path+'downside_capture_benchmark.csv', path+'alpha_benchmark.csv', path+'positive_beta_benchmark.csv', path+'negative_beta_benchmark.csv', path+'volatility_benchmark.csv']

    for file in benchmark_file_list:
    

        df_nasdaq_1h_early_return = pd.read_csv(file).set_index('Unnamed: 0')


        df_nasdaq_1h_early_return = df_nasdaq_1h_early_return[~df_nasdaq_1h_early_return['ticker'].duplicated(keep='first')]

        df_nasdaq_1h_early_return.to_csv(file)


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
