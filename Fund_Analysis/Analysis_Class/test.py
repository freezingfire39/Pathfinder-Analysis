import pandas as pd
import Analysis_class
import yfinance as yf
import numpy as np
import sys
from pathlib import Path
home = str(Path.home())

def main(symbol_file_path,symbol,search_file_path):
    asset_type='stock_'
    #asset_type='bond_'
    #asset_type='money_market_'
    #asset_type='overseas_'


    input_file_path=symbol_file_path + 'Fund_1.csv'  ##ticker_information fund_1
    background_file_path=symbol_file_path + 'Background.csv'
    return_rank_file_path=search_file_path+asset_type+'return_rank.csv'
    cagr_rank_file_path=search_file_path+asset_type+'CAGR_rank.csv'  ##return_rank_csv
    rank_file_path=search_file_path+asset_type  ##all other filter csv
    comp_file_path=search_file_path+'index_comps.csv'
    comp_file_path_2=search_file_path+'industry_comps.csv'
    save_file_path=symbol_file_path +'sample_feature.csv'
    # Ticker = "000001"
    Ticker = symbol
    Trading_days = 250
    trading_days=250



    df_target = pd.read_csv(input_file_path)


    df_target = df_target.iloc[::-1]
    risk_free_rate=0.0
    df_target.set_index('净值日期',inplace=True)
    df_target.index = pd.to_datetime(df_target.index)





    rolling_sharpe_df = pd.DataFrame(index=df_target.index,columns=['rolling_SR_comments','excess_return_comments', 'alpha_comments','beta_comments','upside_capture_comments','downside_capture_comments','index_comments','sector_comments','volatility_comments','drawdown_amount_comments', 'drawdown_duration_comments','return_comments','return_corr_comments','return_benchmark_comments', 'alpha_benchmark_comments','beta_benchmark_comments','upside_benchmark_comments','downside_benchmark_comments','excess_sharpe_benchmark_comments','sr_benchmark_comments','drawdown_duration_benchmark_comments','drawdown_amount_benchmark_comments','volatility_benchmark_comments'])
    rolling_sharpe_df.to_csv(symbol_file_path + 'comments.csv')


    df_test_4 = df_target['申购状态'].resample('D')
    df_test_4 = df_test_4.fillna(method='ffill')
    df_test_1 = df_test_4[df_test_4.str.contains("暂停申购")]
    df_test_2 = df_test_4[df_test_4.str.contains("开放申购")]
    
    df_target['purchase_comments']=0
    df_target['purchase_days']=0
    df_target['purchase_days_2']=0
    if len(df_test_1)==0:
        df_target.at[df_target.index[-1],'purchase_comments']  = "本基金一直都是开放认购。"
    
    
    #print ("This fund is always open for investment")
    elif len(df_test_2)==0:
        df_target.at[df_target.index[-1],'purchase_comments']  = "本基金尚未开放认购。"
    else:
        if df_target['申购状态'][-1]=="开放申购":
            df_target.at[df_target.index[-1],'purchase_comments']  = "本基金目前开放认购。"
        #print ("open for purchase")
        else:
            df_target.at[df_target.index[-1],'purchase_comments']  = "本基金目前不开放认购。"
        #print ("not open for purchase")

        close_days = df_test_1.index[-1]-df_test_2.index[-1]

        df_target.at[df_target.index[-1],'purchase_days']  = "本基金距离上次开放申购已经过去了"+str(close_days)+"天。"
        df_test_2 = df_test_2.to_frame()
        df_test_2['flag']=1
        df_test_5 = df_test_2['flag'].resample('Y').sum()
        df_target.at[df_target.index[-1],'purchase_days_2']  = "本基金每年约有"+str(df_test_5.mean())+"天开放认购"

    
    df_test_4 = df_target['赎回状态'].resample('D')
    df_test_4 = df_test_4.fillna(method='ffill')
    df_test_1 = df_test_4[df_test_4.str.contains("暂停赎回")]
    df_test_2 = df_test_4[df_test_4.str.contains("开放赎回")]
    df_target['redeem_comments']=0
    df_target['redeem_days']=0
    df_target['redeem_days_2']=0
    if len(df_test_1)==0:
        df_target.at[df_target.index[-1],'purchase_comments']  = "本基金一直都是开放赎回。"
    
    
    #print ("This fund is always open for investment")
    elif len(df_test_2)==0:
        df_target.at[df_target.index[-1],'purchase_comments']  = "本基金尚未开放赎回。"
    else:
        if df_target['申购状态'][-1]=="开放申购":
            df_target.at[df_target.index[-1],'purchase_comments']  = "本基金目前开放赎回。"
        #print ("open for purchase")
        else:
            df_target.at[df_target.index[-1],'purchase_comments']  = "本基金目前不开放赎回。"
        #print ("not open for purchase")

        close_days = df_test_1.index[-1]-df_test_2.index[-1]

        df_target.at[df_target.index[-1],'purchase_days']  = "本基金距离上次开放赎回已经过去了"+str(close_days)+"天。"
        df_test_2 = df_test_2.to_frame()
        df_test_2['flag']=1
        df_test_5 = df_test_2['flag'].resample('Y').sum()
        df_target.at[df_target.index[-1],'purchase_days_2']  = "本基金每年约有"+str(df_test_5.mean())+"天开放赎回"

    
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
    df_target['cum_return'] = (1+df_target['return']).cumprod()-1

    df_target['annual_return'] = (1+df_target['return']).rolling(window=trading_days).apply(np.prod, raw=True)-1



    df_target['CAGR'] = 0

    df_target['CAGR'].iloc[-1] = (df_target['累计净值'].iloc[-1]/df_target['累计净值'].iloc[0])**(1/(len(df_target)/trading_days))



    rank_file = pd.read_csv(search_file_path+asset_type+'return_benchmark.csv').set_index('Unnamed: 0')
    new_row = {'ticker': Ticker, 'value': df_target['annual_return'][-1]}
    rank_file.loc[len(rank_file)] = new_row
    #rank_file['ticker'] = rank_file['ticker'].apply('="{}"'.format)
    rank_file.to_csv(search_file_path+asset_type+'return_benchmark.csv')

    




    ##calculate net return
    df_background = pd.read_csv(background_file_path)
    management_fee = df_background['管理费率'].iloc[0].split("%")[0]


    management_fee = float(management_fee)/100
    custody_fee = df_background['托管费率'].iloc[0].split("%")[0]
    custody_fee = float(custody_fee)/100

    df_target['net_return']=df_target['return']-(custody_fee+management_fee)/Trading_days
    df_target['cum_net_return'] = (1+df_target['net_return']).cumprod()-1

    #df_target['fee_gap'] = df_target['net_return']-df_target['return']

    df_target['fund_name']=0
    df_target.at[df_target.index[-1],'fund_name']  = str(df_background['基金简称'][0])


    index_comps = pd.read_csv(comp_file_path).set_index('Date')
    industry_comps = pd.read_csv(comp_file_path_2).set_index('Date')
    index_comps.index = pd.to_datetime(index_comps.index)
    industry_comps.index = pd.to_datetime(industry_comps.index)






    comp_3_name,comp_4_name, df_target = Analysis_class.corr_analysis(df_target,industry_comps,Ticker,rank_file_path=rank_file_path,rank_file_path_2 = rank_file_path,input_file_path = symbol_file_path)

    comp_1_name,comp_2_name, df_target = Analysis_class.corr_analysis(df_target,index_comps,Ticker,rank_file_path=rank_file_path, rank_file_path_2 = rank_file_path,input_file_path = symbol_file_path)

    df_target['comp_1'] = index_comps[comp_1_name]
    df_target['comp_1'] = df_target['comp_1'].fillna(method='ffill')
    df_target['excess_return']=df_target['return']-df_target['comp_1'].pct_change()

    df_target['rolling_mean'] = df_target['return'].rolling(trading_days).mean()
    df_target['comp_mean'] = index_comps[comp_1_name].rolling(trading_days).mean()

    df_target = Analysis_class.rolling_sharpe(df_target,rank_file_path = rank_file_path, input_file_path = symbol_file_path, asset_type=asset_type, security_code = Ticker)

    rank_file = pd.read_csv(return_rank_file_path).set_index('Unnamed: 0')
    if df_target['annual_return'][-1] > 0.05:

        new_row = {'ticker': Ticker, 'value': df_target['annual_return'][-1],'name': df_target['fund_name'][-1], 'sharpe_ratio': df_target['rolling_SR'][-1], 'return': df_target['return'][-1]}
        rank_file.loc[len(rank_file)] = new_row
        rank_file.to_csv(return_rank_file_path)
        
    rank_file = pd.read_csv(cagr_rank_file_path).set_index('Unnamed: 0')
    new_row = {'ticker': Ticker, 'value': df_target['CAGR'][-1],'name': df_target['fund_name'][-1], 'sharpe_ratio': df_target['rolling_SR'][-1], 'return': df_target['return'][-1]}
    rank_file.loc[len(rank_file)] = new_row
    rank_file.to_csv(cagr_rank_file_path)






    
    df_target = Analysis_class.return_analysis(df_target,input_file_path = symbol_file_path,rank_file_path = rank_file_path, asset_type=asset_type,security_code = Ticker)

    df_target = Analysis_class.max_drawdown_analysis(df_target,rank_file_path = rank_file_path, input_file_path = symbol_file_path, security_code = Ticker)

    if comp_1_name in industry_comps:
        df_target = Analysis_class.alpha_beta_analysis(df_target, df_target['comp_1'].pct_change(),rank_file_path = rank_file_path, input_file_path = symbol_file_path,security_code = Ticker)
    else:
        df_target = Analysis_class.alpha_beta_analysis(df_target, df_target['comp_1'].pct_change(),rank_file_path = rank_file_path, input_file_path = symbol_file_path,security_code = Ticker)


    df1 = df_target[['累计净值', 'comp_1']]

    # Resample to month end and calculate the monthly percent change
    df_rets_monthly = df1.resample('M').last().pct_change().dropna()

    df_target = Analysis_class.market_capture_ratio(df_rets_monthly, df_target, rank_file_path = rank_file_path, input_file_path = symbol_file_path,security_code = Ticker)


    if comp_1_name in industry_comps:
        df_target = Analysis_class.rolling_volatility(df_target, df_target['comp_1'].pct_change(),rank_file_path = rank_file_path, input_file_path = symbol_file_path,security_code = Ticker)
    else:
        df_target = Analysis_class.rolling_volatility(df_target, df_target['comp_1'].pct_change(),rank_file_path = rank_file_path, input_file_path = symbol_file_path,security_code = Ticker)

    df_target = Analysis_class.plot_drawdown_underwater(df_target)

    df_target = Analysis_class.return_forecast(df_target, index_comps[comp_1_name],asset_type=asset_type)

    Analysis_class.event_analysis(df_target['return'], benchmark_rets=df_target['comp_1'].pct_change())

    df_target.drop(['index_peers','industry_peers'],axis=1,inplace=True)
    df_target.replace([np.inf, -np.inf], np.nan, inplace=True)
    df_target.fillna(method='ffill',inplace=True)
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

