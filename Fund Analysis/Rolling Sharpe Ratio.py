risk_free_rate=0.0
df_target['rolling_SR'] = df_target['return'].rolling(60).apply(lambda x: (x.mean() - risk_free_rate) / x.std(), raw = True)
df_target['rolling_SR'].plot()
