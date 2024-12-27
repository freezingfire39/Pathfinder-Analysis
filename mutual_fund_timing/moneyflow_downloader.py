import tushare as ts
pro = ts.pro_api('84be1015becc0b9dbbab507552c328cbf447bc02cbd29cfa09029bc6')


df = pro.moneyflow_mkt_dc(start_date='20240901', end_date='20240930')

df_2 = pro.moneyflow_ind_ths(start_date='20240901', end_date='20240930')

for ticker in df_2['ts_code']:
    df_temp = df_2[df_2['ts_code']==ticker]
    df_temp.to_csv(df_2['industry'][0]+'.csv')
    break


df.to_csv('index_money_flow.csv')


