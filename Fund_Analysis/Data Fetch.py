import nasdaqdatalink
nasdaqdatalink.ApiConfig.api_key = 'znxYqt7DpE3soUMDRfGE'
security = '510500' ##target name
df_target = nasdaqdatalink.get_table('DY/EMPRIA', security=security)
df_target = df_target.iloc[::-1]
df_target.set_index('date',inplace=True)
df_target.index = pd.to_datetime(df_target.index)
print (df_target)
df_target_2 = nasdaqdatalink.get_table('DY/EMMONA', security='000010')
print (df_target_2)
df_target_3 = nasdaqdatalink.get_table('DY/EMNAVA', security=security)
print (df_target_3)
df_target_4 = nasdaqdatalink.get_table('DY/EMNAVADJA', security=security)
print (df_target_4)
