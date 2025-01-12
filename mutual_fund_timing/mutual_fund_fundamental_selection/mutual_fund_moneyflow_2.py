import tushare as ts
import tushare as ts
pro = ts.pro_api('84be1015becc0b9dbbab507552c328cbf447bc02cbd29cfa09029bc6')



df_3 = pro.fund_portfolio(ts_code='001753.OF')

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

df['total_revenue'] = 0
df['total_revenue'] = df['total_revenue'].astype('float64')

df['total_profit'] = 0
df['total_profit'] = df['total_profit'].astype('float64')


df_2 = pro.moneyflow(ts_code=df['symbol'].iloc[0], start_date='20240115', end_date='20241215')
df_2.set_index('trade_date',inplace=True)
df_2.index = pd.to_datetime(df_2.index)


df_4 = pro.moneyflow_mkt_dc(start_date='20240101', end_date='20241230')
df_4.set_index('trade_date',inplace=True)
df_4.index = pd.to_datetime(df_4.index)


print (df_4)

for symbol in df['symbol']:

    if symbol == df['symbol'].iloc[0]:
        pass
    


    df_temp = pro.moneyflow(ts_code=symbol, start_date='20240115', end_date='20241215')
    df_temp.set_index('trade_date',inplace=True)
    df_temp.index = pd.to_datetime(df_temp.index)

    

    df_2['net_mf_amount']+=df_temp['net_mf_amount']


df_trade = pro.fund_nav(ts_code='001753.OF', start_date='20180101', end_date='20241229')
print (df_trade)
df_trade = df_trade.iloc[::-1]
df_trade.set_index('nav_date',inplace=True)
df_trade.index = pd.to_datetime(df_trade.index)
df_trade['return'] = df_trade['accum_nav'].pct_change()
print (df_trade)



df_2.dropna(inplace=True)
df.dropna(inplace=True)

df_drop=[]
for i in df_trade.index:
    if i not in df_2.index:
        df_drop.append(i)
df_trade = df_trade.drop(df_drop, axis=0)

df_drop=[]
for i in df_trade.index:
    if i not in df_4.index:
        df_drop.append(i)
df_trade = df_trade.drop(df_drop, axis=0)

df_drop=[]
for i in df_2.index:
    if i not in df_trade.index:
        df_drop.append(i)
df_2 = df_2.drop(df_drop, axis=0)

df_drop=[]
for i in df_4.index:
    if i not in df_trade.index:
        df_drop.append(i)
df_4 = df_4.drop(df_drop, axis=0)


df_trade['gap'] = df_2['net_mf_amount'].pct_change()-df_4['net_amount'].pct_change()


df_trade['zscore_3'] =(df_trade['gap'] - df_trade['gap'].rolling(10).mean())/df_trade['gap'].rolling(10).std(ddof=0)




df_trade['trade'] = 0
df_trade['trade'] = df_trade['trade'].astype('float64')
for i in range(len(df_trade)):
    if i<1:
        continue


    if df_trade['zscore_3'][i-1]<=-0.1 and df_trade['zscore_3'][i-1]>=-0.6:
        df_trade['trade'][i:i+1]=1

    elif df_trade['zscore_3'][i-1]>=0.1 and df_trade['zscore_3'][i-1]<=0.6:
        df_trade['trade'][i:i+1]=-1


    if df_trade['zscore_3'][i-1]>=0.6:
        df_trade['trade'][i:i+1]=1

    elif df_trade['zscore_3'][i-1]<=-0.6:
        df_trade['trade'][i:i+1]=-1

df_trade['full_return'] = df_trade['trade']*df_trade['return']
import pyfolio_master as pf
print (df_trade)
#df_trade = pd.to_numeric(df_trade, errors='coerce')

pf.create_full_tear_sheet(df_trade['full_return'])




    









    






