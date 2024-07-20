import pandas as pd


stock_list=[]
rank_csv_1 = pd.read_csv('/Users/yiluntong/Downloads/output_search/bond_rolling_sharpe_rank.csv').set_index('Unnamed: 0')
rank_csv_2 = pd.read_csv('/Users/yiluntong/Downloads/output_search/bond_return_rank.csv').set_index('Unnamed: 0')
for ticker in rank_csv_1['ticker']:
    if ticker in rank_csv_2['ticker'].values:
        stock_list.append(ticker)

df = pd.DataFrame(data={"col1": stock_list})
df.to_csv("top_bond.csv", sep=',',index=False)

