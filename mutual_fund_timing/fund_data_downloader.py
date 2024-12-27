import tushare as ts
pro = ts.pro_api('84be1015becc0b9dbbab507552c328cbf447bc02cbd29cfa09029bc6')
df = pro.fund_basic(market='E')

for ticker in df['ts_code']:
    print (ticker)

    df_2 = pro.fund_manager(ts_code=ticker)
    df_3 = pro.fund_portfolio(ts_code=ticker)

    df_2.to_csv('manager_info.csv')
    df_3.to_csv('holdings_info.csv')
    break


