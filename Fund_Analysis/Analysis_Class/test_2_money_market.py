import pandas as pd
import Analysis_class
import yfinance as yf
import numpy as np
import sys
from pathlib import Path
home = str(Path.home())

def main(symbol_file_path,symbol,search_file_path):
    #asset_type='stock_'
    #asset_type='bond_'
    asset_type='money_market_'
    #asset_type='overseas_'

    input_file_path=symbol_file_path+'Fund_2.csv'
    background_file_path=symbol_file_path+'Background.csv'
    rank_file_path=asset_type+''
    return_rank_file_path=search_file_path+asset_type+'return_rank.csv'
    cagr_rank_file_path=search_file_path+asset_type+'CAGR_rank.csv'  ##return_rank_csv
    Trading_days = 250
    trading_days=250
    save_file_path=symbol_file_path+'sample_feature.csv'
    # Ticker = "000001"
    Ticker = symbol
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


    sales_fee = df_background['托管费率'].iloc[0].split("%")[0]
    sales_fee = float(sales_fee )/100

    df_target_2['net_return']=df_target_2['return']-(custody_fee+management_fee+sales_fee)/Trading_days

    df_target_2['累计净值'] =(1+df_target_2['return']).cumprod()



    df_test_4 = df_target_2['申购状态'].resample('D')
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

    
    df_test_4 = df_target_2['赎回状态'].resample('D')
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
    

    df_target_2['CAGR'] = 0

    df_target_2['CAGR'].iloc[-1] = (df_target_2['累计净值'].iloc[-1])**(1/(len(df_target_2)/trading_days))

    df_target_2['annual_return'] = (1+df_target_2['return']).rolling(window=trading_days).apply(np.prod, raw=True)-1

    rank_file = pd.read_csv(return_rank_file_path).set_index('Unnamed: 0')
    if df_target_2['annual_return'].iloc[-1] > 0.02:

        new_row = {'ticker': Ticker, 'value': df_target_2['annual_return'].iloc[-1]}
        rank_file.loc[len(rank_file)] = new_row
        rank_file.to_csv(return_rank_file_path)

    rank_file = pd.read_csv(cagr_rank_file_path).set_index('Unnamed: 0')
    new_row = {'ticker': Ticker, 'value': df_target_2['CAGR'].iloc[-1]}
    rank_file.loc[len(rank_file)] = new_row
    rank_file.to_csv(cagr_rank_file_path)

    #df_target['fee_gap'] = df_target['net_return']-df_target['return']

    df_target_2.to_csv(save_file_path)
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
