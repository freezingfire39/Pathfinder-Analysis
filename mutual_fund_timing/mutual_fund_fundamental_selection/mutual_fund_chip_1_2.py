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




df_2 = pro.cyq_chips(ts_code=df['symbol'].iloc[0], start_date='20180801', end_date='20241208') ##end date today's date, start_date 5 month minus
df_2.set_index('trade_date',inplace=True)
df_2.index = pd.to_datetime(df_2.index)
df_2 = df_2.resample("D").sum()

print (df_2)

for symbol in df['symbol']:

    if symbol == df['symbol'].iloc[0]:
        pass
    
    df_temp = pro.moneyflow_ths(ts_code=symbol, start_date='20241101', end_date='20241201') ##end date today's date, start date one month minus


    df['last_month_flow'] += df_temp['net_amount'].sum()

    df_temp = pro.cyq_chips(ts_code=symbol, start_date='20180801', end_date='20241208') ##end date today's date, start_date 5 month minus
    df_temp.set_index('trade_date',inplace=True)
    df_temp.index = pd.to_datetime(df_temp.index)
    df_temp = df_temp.resample("D").sum()





    df_2['percent']+=df_temp['percent']



df_trade = pro.fund_nav(ts_code='501060.SH', start_date='20180101', end_date='20241229')
print (df_trade)
df_trade = df_trade.iloc[::-1]
df_trade.set_index('ann_date',inplace=True)
df_trade.index = pd.to_datetime(df_trade.index)

df_trade['return'] = df_trade['accum_nav'].pct_change()
print (df_trade)

df_2.dropna(inplace=True)

df_drop=[]
for i in df_trade.index:
    if i not in df_2.index:
        df_drop.append(i)
df_trade = df_trade.drop(df_drop, axis=0)

df_drop=[]
for i in df_2.index:
    if i not in df_trade.index:
        df_drop.append(i)
df_2 = df_2.drop(df_drop, axis=0)




df_trade['gap'] = df_2['percent']


df_trade['zscore_3'] =(df_trade['gap'] - df_trade['gap'].rolling(5).mean())/df_trade['gap'].rolling(5).std(ddof=0)




df_trade['trade'] = 0
df_trade['trade'] = df_trade['trade'].astype('float64')
for i in range(len(df_trade)):
    if i<1:
        continue


    if df_trade['zscore_3'][i-1]<=-0.5 and df_trade['zscore_3'][i-1]>=-1.6:
        df_trade['trade'][i:i+1]=1

    elif df_trade['zscore_3'][i-1]>=0.5 and df_trade['zscore_3'][i-1]<=1.6:
        df_trade['trade'][i:i+1]=-1

    if df_trade['zscore_3'][i-1]>=1.6:
        df_trade['trade'][i:i+1]=-1

    elif df_trade['zscore_3'][i-1]<=-1.6:
        df_trade['trade'][i:i+1]=1


df_trade['full_return'] = df_trade['trade']*df_trade['return']
import pyfolio_master as pf
print (df_trade)
#df_trade = pd.to_numeric(df_trade, errors='coerce')

pf.create_full_tear_sheet(df_trade['full_return'])




    









    






