def market_capture_ratio(returns):
    """
    Function to calculate the upside and downside capture for a given set of returns.
    The function is set up so that the investment's returns are in the first column of the dataframe
    and the index returns are the second column.
    :param returns: pd.DataFrame of asset class returns
    :return: pd.DataFrame of market capture results
    """

    # initialize an empty dataframe to store the results
    df_mkt_capture = pd.DataFrame()

    # 1) Upside capture ratio
    # a) Isolate positive periods of the index
    up_market = returns[returns.iloc[:, -1] >= 0]

    # b) Geometrically link the returns
    up_linked_rets = ((1 + up_market).product(axis=0)) - 1

    # c) Calculate the ratio, multiply by 100 and round to 2 decimals to show in percent
    up_ratio = (up_linked_rets / up_linked_rets.iloc[-1] * 100).round(2)

    # 2) Downside capture ratio
    # a) Isolate negative periods of the index
    down_market = returns[returns.iloc[:, -1] < 0]

    # b) Geometrically link the returns
    down_linked_rets = ((1 + down_market).product(axis=0)) - 1

    # c) Calculate the ratio, multiply by 100 and round to 2 decimals to show in percent
    down_ratio = (down_linked_rets / down_linked_rets.iloc[-1] * 100).round(2)

    # 3) Combine to produce our final dataframe
    df_mkt_capture = pd.concat([up_ratio, down_ratio], axis=1)

    df_mkt_capture.columns = ['Upside Capture', 'Downside Capture']

    return df_mkt_capture

df_target['comp_1'] = comp_2['Close']
print (df_target)
# Keep only the adjusted close columns
df1 = df_target[['close', 'comp_1']]

# Resample to month end and calculate the monthly percent change
df_rets_monthly = df1.resample('M').last().pct_change().dropna()

# Calculate the market capture ratios
df_mkt_capture = market_capture_ratio(df_rets_monthly)

print(df_mkt_capture)
