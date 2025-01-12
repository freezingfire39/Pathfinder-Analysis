df = pro.opt_basic(exchange='SSE', fields='ts_code,name,exercise_type,list_date,delist_date')

df['delist_date'] = df['delist_date'].astype('float64')

df = df[df['delist_date']>20250000]

df = df[df['name'].str.contains("华泰柏瑞沪深")]

df_call = df[df['name'].str.contains("认购")]

df_put =  df[df['name'].str.contains("认沽")]
print (df_call)

df_2 = pro.opt_daily(ts_code=df_call['ts_code'].iloc[0], start_date='20240101',end_date='20241216').set_index('trade_date')
df_2 = df_2.iloc[::-1]
df_2.index = pd.to_datetime(df_2.index)

df_2['return'] = df_2['close'].pct_change()

print (df_2)
df_3 = pro.opt_daily(ts_code=df_put['ts_code'].iloc[0], start_date='20240101',end_date='20241216').set_index('trade_date')
df_3 = df_3.iloc[::-1]
df_3.index = pd.to_datetime(df_3.index)

df_3['return'] = df_3['close'].pct_change()

for ticker in df_call['ts_code']:
    df_temp = pro.opt_daily(ts_code=ticker, start_date='20240101',end_date='20241216').set_index('trade_date')
    df_temp = df_temp.iloc[::-1]
    df_temp.index = pd.to_datetime(df_temp.index)
    if len(df_temp) < 10:
        pass

    else:
        df_2['oi']+=df_temp['oi']
        df_2['return']+=df_temp['close'].pct_change()


for ticker in df_put['ts_code']:
    df_temp = pro.opt_daily(ts_code=ticker, start_date='20240101',end_date='20241216').set_index('trade_date')
    df_temp = df_temp.iloc[::-1]
    df_temp.index = pd.to_datetime(df_temp.index)
    if len(df_temp) < 10:
        pass

    else:
        df_3['oi']+=df_temp['oi']
        df_3['return']+=df_temp['close'].pct_change()

print (df_2)
print (df_3)




copper_future_1 = pro.fut_daily(ts_code='IH.CFX', start_date='20190115', end_date='20241217').set_index('trade_date')
copper_future_2 = pro.fut_daily(ts_code='IF.CFX', start_date='20190115', end_date='20241217').set_index('trade_date')

copper_future_1 = copper_future_1.iloc[::-1]
copper_future_2 = copper_future_2.iloc[::-1]

copper_future_1.index = pd.to_datetime(copper_future_1.index)
copper_future_2.index = pd.to_datetime(copper_future_2.index)


copper_future_1['return'] = copper_future_1['close'].pct_change()


df_drop=[]
for i in copper_future_1.index:
    if i not in df_2.index:
        df_drop.append(i)
copper_future_1 = copper_future_1.drop(df_drop, axis=0)


copper_future_1['gap'] = (df_2['oi']-df_3['oi']).pct_change()

copper_future_1['gap'] = copper_future_1['gap'].cumsum()
copper_future_1['gap'].plot()
#copper_future_1.dropna(inplace=True)

copper_future_2['zscore'] = (copper_future_1['gap'] - copper_future_1['gap'].rolling(3).mean())/copper_future_1['gap'].rolling(3).std(ddof=0)

copper_future_2['trade'] = 0
copper_future_2['trade'] = copper_future_2['trade'].astype('float64')
for i in range(len(copper_future_2)):
    if i<1:
        continue
        #if df_return['zscore'][i-1]>=1.2:
        #    df_return['trade'][i]=-1
    #if copper_future_2['return'][i-1]<-0.03:
    #    copper_future_2['trade'][i:i+2]=1
    
    #elif copper_future_2['zscore'][i-1]>=1.3:
    #    copper_future_2['trade'][i:i+3]=-1
    
    if copper_future_2['zscore'][i-1]<=-0.8 and copper_future_2['zscore'][i-1]>=-2.:
        copper_future_2['trade'][i:i+1]=1
    

    elif copper_future_2['zscore'][i-1]>=0.8 and copper_future_2['zscore'][i-1]<=2.:
        copper_future_2['trade'][i:i+1]=-1
    elif copper_future_2['zscore'][i-1]<=0.8 and copper_future_2['zscore'][i-1]>=0.:
        copper_future_2['trade'][i:i+1]=1
    

    elif copper_future_2['zscore'][i-1]>=-0.8 and copper_future_2['zscore'][i-1]<=-0.:
        copper_future_2['trade'][i:i+1]=-1


    #elif copper_future_2['zscore'][i-1]<=0.2 and copper_future_2['zscore'][i-1]>=-0.2:
    #    copper_future_2['trade'][i:]=0
copper_future_2['full_return'] = copper_future_2['trade']*(copper_future_1['return'])
import pyfolio_master as pf
#df_trade = pd.to_numeric(df_trade, errors='coerce')
copper_future_2.index = pd.to_datetime(copper_future_2.index)
pf.create_full_tear_sheet(copper_future_2['full_return'])
print (copper_future_2)
    
if copper_future_2['zscore'][-1]<=-0.7:
    print (2)
    
elif copper_future_2['zscore'][-1]<=-0.2 and copper_future_2['zscore'][-1]>=-0.7:
    print (1)
elif copper_future_2['zscore'][-1]>=0.4 and copper_future_2['zscore'][-1]<=1.4:
    print (-1)
