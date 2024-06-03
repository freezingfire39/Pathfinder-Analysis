
security_1 = '512170'
security_2 = '515170'
security_3 = '512660'
security_4 = '516800'
security_5 = "512400"

df_port_1 = nasdaqdatalink.get_table('DY/EMPRIA', security=security_1)
df_port_1  = df_port_1 .iloc[::-1]
df_port_1 .set_index('date',inplace=True)
df_port_1 .index = pd.to_datetime(df_port_1 .index)


df_port_2 = nasdaqdatalink.get_table('DY/EMPRIA', security=security_2)
df_port_2 = df_port_2.iloc[::-1]
df_port_2.set_index('date',inplace=True)
df_port_2.index = pd.to_datetime(df_port_2.index)

df_port_3 = nasdaqdatalink.get_table('DY/EMPRIA', security=security_3)
df_port_3 = df_port_3.iloc[::-1]
df_port_3.set_index('date',inplace=True)
df_port_3.index = pd.to_datetime(df_port_3.index)

df_port_4 = nasdaqdatalink.get_table('DY/EMPRIA', security=security_4)
df_port_4 = df_port_4.iloc[::-1]
df_port_4.set_index('date',inplace=True)
df_port_4.index = pd.to_datetime(df_port_4.index)

df_port_5 = nasdaqdatalink.get_table('DY/EMPRIA', security=security_5)
df_port_5 = df_port_5.iloc[::-1]
df_port_5.set_index('date',inplace=True)
df_port_5.index = pd.to_datetime(df_port_5.index)

df_target['port_1_return'] = df_port_1['close'].pct_change()
df_target['port_2_return'] = df_port_2['close'].pct_change()

df_target['port_1_close'] = df_port_1['close']
df_target['port_2_close'] = df_port_2['close']
df_target['port_3_close'] = df_port_3['close']
df_target['port_4_close'] = df_port_4['close']
df_target['port_5_close'] = df_port_5['close']
returns = df_target[['return','port_1_return','port_2_return']]

cov_matrix = returns.cov()

cov_matrix
weights = np.array([.25, .45, .3])

# Set an initial investment level
initial_investment = 1000000
avg_rets = returns.mean()

# Calculate mean returns for portfolio overall,
# using dot product to
# normalize individual means against investment weights
 # https://en.wikipedia.org/wiki/Dot_product#:~:targetText=In%20mathematics%2C%20the%20dot%20product,and%20returns%20a%20single%20number.
port_mean = avg_rets.dot(weights)

# Calculate portfolio standard deviation
port_stdev = np.sqrt(weights.T.dot(cov_matrix).dot(weights))

# Calculate mean of investment
mean_investment = (1+port_mean) * initial_investment

# Calculate standard deviation of investmnet
stdev_investment = initial_investment * port_stdev
conf_level1 = 0.05

# Using SciPy ppf method to generate values for the
# inverse cumulative distribution function to a normal distribution
# Plugging in the mean, standard deviation of our portfolio
# as calculated above
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.norm.html
from scipy.stats import norm
cutoff1 = norm.ppf(conf_level1, mean_investment, stdev_investment)
var_1d1 = initial_investment - cutoff1
var_array = []
num_days = int(15)
for x in range(1, num_days+1):
    var_array.append(np.round(var_1d1 * np.sqrt(x),2))
    print(str(x) + " day VaR @ 95% confidence: " + str(np.round(var_1d1 * np.sqrt(x),2)))

# Build plot
plt.xlabel("Day #")
plt.ylabel("Max portfolio loss (USD)")
plt.title("Max portfolio loss (VaR) over 15-day period")
plt.plot(var_array, "r")
