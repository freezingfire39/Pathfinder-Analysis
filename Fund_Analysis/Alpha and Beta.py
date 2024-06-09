#
from scipy import stats
from sklearn.linear_model import LinearRegression

df_target['alpha'] = 0
df_target['alpha'] = df_target['alpha'].astype('float64')
df_target['beta'] = 0
df_target['beta'] = df_target['beta'].astype('float64')

df_drop=[]
for i in df_target.index:
    if i not in comp_2.index:
        df_drop.append(i)
df_target = df_target.drop(df_drop, axis=0)


df_drop=[]
for i in comp_2.index:
    if i not in df_target.index:
        df_drop.append(i)
comp_2 = comp_2.drop(df_drop, axis=0)
comp_2['return'] = comp_2['Close'].pct_change()
for i in range(len(df_target)):
    if i<90:
        continue
    df_temp_1 = df_target.iloc[i-90:i]
    df_temp_2 = comp_2.iloc[i-90:i]
    #print (df_temp_1)
    (beta, alpha) = stats.linregress(df_temp_2['return'], df_temp_1['return'])[0:2]
    df_target['alpha'][i]=alpha
    df_target['beta'][i]=beta
df_target['alpha'].plot()
print (df_target)
