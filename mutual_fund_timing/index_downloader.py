import tushare as ts
pro = ts.pro_api('84be1015becc0b9dbbab507552c328cbf447bc02cbd29cfa09029bc6')

ticker_list = ['000001.SH', '000300.SH', '000905.SH', '399001.SZ', '399005.SZ', '399006.SZ', '399016.SZ', '399300.SZ']

for ticker in ticker_list:
    df = pro.index_dailybasic(ts_code = ticker, start_date='20240901', end_date='20240930', fields='trade_date,turnover_rate,pe,pb')

    df_temp.to_csv(ticker+'.csv')
    break


