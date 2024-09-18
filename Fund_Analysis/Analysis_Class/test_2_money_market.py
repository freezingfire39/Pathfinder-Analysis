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

    df_target_2 = df_target_2.iloc[::-1]

    df_target_2.set_index('净值日期',inplace=True)
    df_target_2.index = pd.to_datetime(df_target_2.index)
    df_target_2['7日年化收益率（%）'] = df_target_2['7日年化收益率（%）'].str.rstrip('%').astype('float') / 100.0

    df_target_2['return'] = (df_target_2['7日年化收益率（%）']+1)**(1/trading_days)-1


    rolling_sharpe_df = pd.DataFrame(index=df_target_2.index,columns=['rolling_SR_comments','excess_return_comments', 'alpha_comments','beta_comments','upside_capture_comments','downside_capture_comments','index_comments','sector_comments','volatility_comments','drawdown_amount_comments', 'drawdown_duration_comments', 'return_comments','return_corr_comments','return_benchmark_comments', 'alpha_benchmark_comments','beta_benchmark_comments','upside_benchmark_comments','downside_benchmark_comments','excess_sharpe_benchmark_comments','sr_benchmark_comments','drawdown_duration_benchmark_comments','drawdown_amount_benchmark_comments','volatility_benchmark_comments'])
    rolling_sharpe_df.to_csv(symbol_file_path+'comments.csv')

    ##calculate net return
    df_background = pd.read_csv(background_file_path)

    management_fee = df_background['管理费率'].iloc[0].split("%")[0]


    management_fee = float(management_fee)/100

    custody_fee = df_background['托管费率'].iloc[0].split("%")[0]
    custody_fee = float(custody_fee)/100


    sales_fee = df_background['托管费率'].iloc[0].split("%")[0]
    sales_fee = float(sales_fee )/100

    df_target_2['net_return']=df_target_2['return']-(custody_fee+management_fee+sales_fee)/Trading_days

    df_target_2['cum_return'] = (1+df_target_2['return']).cumprod()-1
    df_target_2['cum_net_return'] = (1+df_target_2['net_return']).cumprod()-1

    df_target_2['累计净值'] =(1+df_target_2['return']).cumprod()



    rolling_sharpe_df = pd.DataFrame(index=df_target_2.index,columns=['rolling_SR_comments','excess_return_comments', 'alpha_comments','beta_comments','upside_capture_comments','downside_capture_comments','index_comments','sector_comments','volatility_comments','drawdown_amount_comments', 'drawdown_duration_comments','return_benchmark_comments', 'alpha_benchmark_comments','beta_benchmark_comments','upside_benchmark_comments','downside_benchmark_comments','excess_sharpe_benchmark_comments','sr_benchmark_comments','drawdown_duration_benchmark_comments','drawdown_amount_benchmark_comments','volatility_benchmark_comments'])
    rolling_sharpe_df.to_csv('comments.csv')

    
    df_test_4 = df_target_2['申购状态'].resample('D')
    df_test_4 = df_test_4.fillna(method='ffill')

    df_test_1 = df_test_4[df_test_4.str.contains("暂停申购")]
    df_test_2 = df_test_4[df_test_4.str.contains("开放申购")]
    
    df_target_2['purchase_comments']=0
    df_target_2['purchase_days']=0
    df_target_2['purchase_days_2']=0
    if len(df_test_1)==0:
        df_target.at[df_target.index[-1],'purchase_comments']  = "本基金一直都是开放认购。"
    
    
    #print ("This fund is always open for investment")
    elif len(df_test_2)==0:
        df_target_2.at[df_target.index[-1],'purchase_comments']  = "本基金尚未开放认购。"
    else:
        if df_target_2['申购状态'][-1]=="开放申购":
            df_target_2.at[df_target_2.index[-1],'purchase_comments']  = "本基金目前开放认购。"
        #print ("open for purchase")
        else:
            df_target_2.at[df_target_2.index[-1],'purchase_comments']  = "本基金目前不开放认购。"
        #print ("not open for purchase")

        close_days = df_test_1.index[-1]-df_test_2.index[-1]

        df_target_2.at[df_target_2.index[-1],'purchase_days']  = "本基金距离上次开放申购已经过去了"+str(close_days)+"天。"
        df_test_2 = df_test_2.to_frame()
        df_test_2['flag']=1
        df_test_5 = df_test_2['flag'].resample('Y').sum()
        df_target_2.at[df_target_2.index[-1],'purchase_days_2']  = "本基金每年约有"+str(df_test_5.mean())+"天开放认购"

    df_target_2['excess_SR']=0
    df_test_4 = df_target_2['赎回状态'].resample('D')
    df_test_4 = df_test_4.fillna(method='ffill')

    df_test_1 = df_test_4[df_test_4.str.contains("暂停赎回")]
    df_test_2 = df_test_4[df_test_4.str.contains("开放赎回")]
    df_target_2['redeem_comments']=0
    df_target_2['redeem_days']=0
    df_target_2['redeem_days_2']=0
    if len(df_test_1)==0:
        df_target_2.at[df_target_2.index[-1],'purchase_comments']  = "本基金一直都是开放赎回。"
    
    
    #print ("This fund is always open for investment")
    elif len(df_test_2)==0:
        df_target_2.at[df_target.index[-1],'purchase_comments']  = "本基金尚未开放赎回。"
    else:
        if df_target_2['申购状态'][-1]=="开放申购":
            df_target_2.at[df_target.index[-1],'purchase_comments']  = "本基金目前开放赎回。"
        #print ("open for purchase")
        else:
            df_target_2.at[df_target.index[-1],'purchase_comments']  = "本基金目前不开放赎回。"
        #print ("not open for purchase")

        close_days = df_test_1.index[-1]-df_test_2.index[-1]

        df_target_2.at[df_target_2.index[-1],'purchase_days']  = "本基金距离上次开放赎回已经过去了"+int(close_days)+"天。"
        df_test_2 = df_test_2.to_frame()
        df_test_2['flag']=1
        df_test_5 = df_test_2['flag'].resample('Y').sum()
        df_target_2.at[df_target_2.index[-1],'purchase_days_2']  = "本基金每年约有"+int(df_test_5.mean())+"天开放赎回"
    

    df_target_2['CAGR'] = 0

    df_target_2['CAGR'].iloc[-1] = (df_target_2['累计净值'].iloc[-1])**(1/(len(df_target_2)/trading_days))

    df_target_2['annual_return'] = (1+df_target_2['return']).rolling(window=trading_days).apply(np.prod, raw=True)-1



    rank_file = pd.read_csv(search_file_path+asset_type+'return_benchmark.csv').set_index('Unnamed: 0')
    new_row = {'ticker': Ticker, 'value': df_target_2['annual_return'][-1]}
    rank_file.loc[len(rank_file)] = new_row
    #rank_file['ticker'] = rank_file['ticker'].apply('="{}"'.format)
    rank_file.to_csv(search_file_path+asset_type+'return_benchmark.csv')
    



    df_target_2['benchmark_name']=0
    df_target_2.at[df_target_2.index[-1],'benchmark_name']  = "货币基金平均收益"
    df_target_2['fund_name']=0
    df_target_2.at[df_target_2.index[-1],'fund_name']  = str(df_background['基金简称'][0])


    rank_file = pd.read_csv(return_rank_file_path).set_index('Unnamed: 0')
    if df_target_2['annual_return'][-1] > 0.01:

        new_row = {'ticker': Ticker, 'value': df_target_2['annual_return'][-1],'name': df_target_2['fund_name'][-1], 'sharpe_ratio': "不适用", 'return': df_target_2['return'][-1]}
        rank_file.loc[len(rank_file)] = new_row
        rank_file.to_csv(return_rank_file_path)
        
    rank_file = pd.read_csv(cagr_rank_file_path).set_index('Unnamed: 0')
    new_row = {'ticker': Ticker, 'value': df_target_2['CAGR'][-1],'name': df_target_2['fund_name'][-1], 'sharpe_ratio': "不适用", 'return': df_target_2['return'][-1]}
    rank_file.loc[len(rank_file)] = new_row
    rank_file.to_csv(cagr_rank_file_path)

    #df_target['fee_gap'] = df_target['net_return']-df_target['return']
    df_target_2 = Analysis_class.return_analysis(df_target_2,input_file_path = symbol_file_path,rank_file_path = search_file_path+asset_type, asset_type=asset_type)
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
