
%matplotlib inline
fig = plt.figure(figsize=(15, 7))
ax1 = fig.add_subplot(1, 1, 1)

import nasdaqdatalink
nasdaqdatalink.ApiConfig.api_key = 'znxYqt7DpE3soUMDRfGE'
security = '510500' ##target name
df_target = nasdaqdatalink.get_table('DY/EMPRIA', security=security)
df_target = df_target.iloc[::-1]
df_target.set_index('date',inplace=True)
df_target.index = pd.to_datetime(df_target.index)
print (df_target)

df_target['return'] = df_target['close'].pct_change()
df_target['return'].hist(bins=50, ax=ax1)
ax1.set_xlabel('Return')
ax1.set_ylabel('Sample')
ax1.set_title('Return distribution')
plt.show()
comp_1 = yf.download(comp_1_name, start=start, end="2024-04-05") ##chuangye50
comp_2 = yf.download(comp_2_name , start=start, end="2024-04-05")
df_target['gap_1'] = df_target['return']-comp_1['Close'].pct_change()
df_target['gap_2'] = df_target['return']-comp_2['Close'].pct_change()

fig = plt.figure(figsize=(15, 7))
ax1 = fig.add_subplot(1, 1, 1)
df_target['return'] = df_target['close'].pct_change()
df_target['gap_2'].hist(bins=50, ax=ax1)
ax1.set_xlabel('Return')
ax1.set_ylabel('Sample')
ax1.set_title('Return distribution')
plt.show()
