import tushare as ts
import tushare as ts
pro = ts.pro_api('84be1015becc0b9dbbab507552c328cbf447bc02cbd29cfa09029bc6')



df_3 = pro.fund_portfolio(ts_code='501060.SH')

df_3 = df_3.sort_values(by=['amount'])

df = df_3.tail(20)


df['last_month_flow'] = 0
df['last_month_flow'] = df['last_month_flow'].astype('float64')

df['last_quarter_revenue'] = 0
df['last_quarter_revenue'] = df['last_quarter_revenue'].astype('float64')

df['this_quarter_revenue'] = 0
df['this_quarter_revenue'] = df['this_quarter_revenue'].astype('float64')

df['last_quarter_profit'] = 0
df['last_quarter_profit'] = df['last_quarter_profit'].astype('float64')

df['this_quarter_profit'] = 0
df['this_quarter_profit'] = df['this_quarter_profit'].astype('float64')




df_2 = pro.income(ts_code=df['symbol'].iloc[0], start_date='20220801', end_date='20241208', fields='total_profit,total_revenue,f_ann_date') ##end date today's date, start_date 5 month minus
df_2.set_index('f_ann_date',inplace=True)
df_2.index = pd.to_datetime(df_2.index)
df_2 = df_temp.resample("Q").last()

print (df_2)

for symbol in df['symbol']:

    if symbol == df['symbol'].iloc[0]:
        pass
    
    df_temp = pro.moneyflow_ths(ts_code=symbol, start_date='20241101', end_date='20241201') ##end date today's date, start date one month minus


    df['last_month_flow'] += df_temp['net_amount'].sum()

    df_temp = pro.income(ts_code=symbol, start_date='20220801', end_date='20241208', fields='total_profit,total_revenue,f_ann_date') ##end date today's date, start_date 5 month minus
    df_temp.set_index('f_ann_date',inplace=True)
    df_temp.index = pd.to_datetime(df_temp.index)
    df_temp = df_temp.resample("Q").last()

    
    df['last_quarter_revenue']+=df_temp['total_revenue'][1]
    df['this_quarter_revenue']+=df_temp['total_revenue'][0]
    
    df['last_quarter_profit']+=df_temp['total_profit'][1]
    df['this_quarter_profit']+=df_temp['total_profit'][0]


    df_2['total_revenue']+=df_temp['total_revenue']
    df_2['total_profit']+=df_temp['total_profit']
    print (df_2)


    
    df.to_csv('fundamental.csv')
    df_2.to_csv('fundamental_all.csv')
    break



    






