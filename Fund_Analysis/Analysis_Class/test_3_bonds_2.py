import pandas as pd
import Analysis_class
import yfinance as yf
import numpy as np

import sys
from pathlib import Path
home = str(Path.home())

def main(symbol_file_path,symbol,search_file_path):

    #asset_type='stock_'
    asset_type='bond_'
    #asset_type='money_market_'
    #asset_type='overseas_'

    input_file_path=symbol_file_path+'Fund_1.csv'  ##ticker_information fund_1
    background_file_path=symbol_file_path+'Background.csv'
    return_rank_file_path=search_file_path+asset_type+'return_rank.csv'  ##return_rank_csv
    rank_file_path=search_file_path+asset_type
    cagr_rank_file_path=search_file_path+asset_type+'CAGR_rank.csv'   ##all other filter csv
    save_file_path=symbol_file_path+'sample_feature.csv'


    # Ticker = "000001"
    Ticker = symbol
    Trading_days = 250
    trading_days=250

    print (Ticker)


    df_target = pd.read_csv(input_file_path)




    df_target = df_target.iloc[::-1]
    risk_free_rate=0.0
    df_target.set_index('净值日期',inplace=True)
    df_target.index = pd.to_datetime(df_target.index)
        df_test_4 = df_target['申购状态'].resample('D')
    df_test_4 = df_test_4.fillna(method='ffill')
    print (df_test_4)
    df_test_1 = df_test_4[df_test_4.str.contains("暂停申购")]
    df_test_2 = df_test_4[df_test_4.str.contains("开放申购")]
    if len(df_test_1)==0:
        print ("This fund is always open for investment")
    elif len(df_test_2)==0:
        print ("This fund is not open to invest yet")
    else:
        if df_target['申购状态'][-1]=="开放申购":
            print ("open for purchase")
        else:
            print ("not open for purchase")

        close_days = df_test_1.index[-1]-df_test_2.index[-1]
        print (close_days) ##how many days since it is open
        df_test_2 = df_test_2.to_frame()
        df_test_2['flag']=1
        df_test_5 = df_test_2['flag'].resample('Y').sum()
        print (int(df_test_5.mean()))  ##how many days in a year

    
    df_test_4 = df_target['赎回状态'].resample('D')
    df_test_4 = df_test_4.fillna(method='ffill')
    print (df_test_4)
    df_test_1 = df_test_4[df_test_4.str.contains("暂停赎回")]
    df_test_2 = df_test_4[df_test_4.str.contains("开放赎回")]
    if len(df_test_1)==0:
        print ("This fund is always open for redemption")
    elif len(df_test_2)==0:
        print ("This fund is not open to redemption yet")
    else:
        if df_target['申购状态'][-1]=="开放赎回":
            print ("open for redemption")
        else:
            print ("not open for redemption")

        close_days = df_test_1.index[-1]-df_test_2.index[-1]
        print (close_days) ##how many days since it is open
        df_test_2 = df_test_2.to_frame()
        df_test_2['flag']=1
        df_test_5 = df_test_2['flag'].resample('Y').sum()
        print (int(df_test_5.mean()))  ##how many days in a year


    df_target = df_target['累计净值'].resample('D').last()
    df_target = df_target.to_frame()
    df_target.reset_index(inplace=True)
    from pandas.tseries.offsets import BDay
    isBusinessDay = BDay().onOffset
    match_series = pd.to_datetime(df_target['净值日期']).map(isBusinessDay)
    df_target = df_target[match_series]
    df_target.set_index('净值日期',inplace=True)
    df_target = df_target.fillna(method='ffill')





    
    df_target['return'] = df_target['累计净值'].pct_change()

    df_target['annual_return'] = (1+df_target['return']).rolling(window=trading_days).apply(np.prod, raw=True)-1
    rank_file = pd.read_csv(return_rank_file_path).set_index('Unnamed: 0')
    if df_target['annual_return'][-1] > 0.05:

        new_row = {'ticker': Ticker, 'value': df_target['annual_return'][-1]}
        rank_file.loc[len(rank_file)] = new_row
        rank_file.to_csv(return_rank_file_path)






    df_target['CAGR'] = 0

    df_target['CAGR'].iloc[-1] = (df_target['累计净值'].iloc[-1]/df_target['累计净值'].iloc[0])**(1/(len(df_target)/trading_days))


    rank_file = pd.read_csv(cagr_rank_file_path).set_index('Unnamed: 0')
    new_row = {'ticker': Ticker, 'value': df_target['CAGR'][-1]}
    rank_file.loc[len(rank_file)] = new_row
    rank_file.to_csv(cagr_rank_file_path)

    ##calculate net return
    df_background = pd.read_csv(background_file_path)
    print (df_background)
    management_fee = df_background['管理费率'].iloc[0].split("%")[0]


    management_fee = float(management_fee)/100
    print (management_fee)
    custody_fee = df_background['托管费率'].iloc[0].split("%")[0]
    custody_fee = float(custody_fee)/100

    df_target['net_return']=df_target['return']-(custody_fee+management_fee)/Trading_days

    #df_target['fee_gap'] = df_target['net_return']-df_target['return']




    index_comps = yf.download("TLT", start="2000-01-01", end="2024-10-16")
    print (index_comps)
    df_target['comp_1'] =index_comps['Close'].pct_change()
    index_comps = index_comps['Close']

    index_comps.index = pd.to_datetime(index_comps.index)



    df_target['excess_return']=df_target['return']-df_target['comp_1']






    df_target['rolling_mean'] = df_target['return'].rolling(trading_days).mean()
    df_target['comp_mean'] = index_comps.rolling(trading_days).mean()

    df_target = Analysis_class.rolling_sharpe(df_target,rank_file_path = rank_file_path, security_code = Ticker, asset_type = asset_type)

    df_target = Analysis_class.max_drawdown_analysis(df_target,rank_file_path = rank_file_path, security_code = Ticker)


    df_target = Analysis_class.alpha_beta_analysis(df_target, index_comps,rank_file_path = rank_file_path, security_code = Ticker)



    df_target['comp_1'] = index_comps
    df1 = df_target[['累计净值', 'comp_1']]
    print (df1)

    # Resample to month end and calculate the monthly percent change
    df_rets_monthly = df1.resample('M').last().pct_change().dropna()

    df_target = Analysis_class.market_capture_ratio(df_rets_monthly, df_target, rank_file_path = rank_file_path, security_code = Ticker)

    print (df_target)


    df_target = Analysis_class.rolling_volatility(df_target, index_comps,rank_file_path = rank_file_path, security_code = Ticker)


    df_target = Analysis_class.plot_drawdown_underwater(df_target)

    Analysis_class.create_interesting_times_tear_sheet(df_target['return'])
    Analysis_class.create_interesting_times_tear_sheet(df_target['return'], benchmark_rets=df_target['comp_1'].pct_change())




    df_target.to_csv(save_file_path)
    #Analysis_class.rolling_volatility(df_target, index_comps[comp_1_name])

if __name__ == '__main__':
    file_path = home + '/Desktop/output_china/' # for daily download file
    search_file_path = home + '/Desktop/output_search/'
    try:
        symbol = sys.argv[1]
        symbol_file_path = file_path + symbol + "/"
        main(symbol_file_path, symbol,search_file_path)
    except Exception as e:
        error_message = f"Failed to run at error: {str(e)}"
        raise Exception(error_message)(e)
