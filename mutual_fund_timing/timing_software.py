import seaborn as sns
copper_future_1 = pd.read_csv('asset_combined.csv').set_index('date')
copper_future_1.index = pd.to_datetime(copper_future_1.index)
#copper_future_1['Sum']=copper_future_1[copper_future_1.columns].sum(axis=1)

print (copper_future_1)

copper_future_2 = pd.read_csv('aggre_return.csv').set_index('date')
copper_future_2.index = pd.to_datetime(copper_future_2.index)
#copper_future_2.dropna(inplace=True)
copper_future_2['mean'] = copper_future_2[copper_future_2.columns].mean(axis=1)

a = copper_future_1.index.to_series().reindex(copper_future_2.index).bfill().ffill()



copper_future_3 = copper_future_2 .groupby(a).sum()
print (copper_future_2)

copper_future_1 = copper_future_1.pct_change()

df_drop=[]
for i in copper_future_1.index:
    if i not in copper_future_3.index:
        df_drop.append(i)
copper_future_1 = copper_future_1.drop(df_drop, axis=0)

df_drop=[]
for i in copper_future_3.index:
    if i not in copper_future_1.index:
        df_drop.append(i)
copper_future_3 = copper_future_3.drop(df_drop, axis=0)

copper_future_1['zscore'] = (copper_future_1['信息传输、软件和信息技术服务业']  - copper_future_1['信息传输、软件和信息技术服务业'].rolling(5).mean())/copper_future_1['信息传输、软件和信息技术服务业'].rolling(5).std(ddof=0)
copper_future_1['trade'] = 0
copper_future_1['trade'] = copper_future_1['trade'].astype('float64')

for i in range(len(copper_future_1)):
    if i<1:
        continue

    if copper_future_1['zscore'][i-1]>=0.:
        copper_future_1['trade'][i:i+1]=1


print (copper_future_1)
copper_future_1['full_return'] = copper_future_1['trade']*copper_future_3['信息传输、软件和信息技术服务业']
import pyfolio_master as pf
#df_trade = pd.to_numeric(df_trade, errors='coerce')

pf.create_full_tear_sheet(copper_future_1['full_return'])
