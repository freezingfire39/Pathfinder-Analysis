import pandas as pd

input_path = '/home/app/Desktop/output_search/'
output_path = '/home/app/Desktop/output_search/'
stock_list=[]
rank_csv_1 = pd.read_csv(input_path+'overseas_drawdown_amount_rank.csv').set_index('Unnamed: 0')
rank_csv_2 = pd.read_csv(input_path+'overseas_return_rank.csv').set_index('Unnamed: 0')

df = pd.DataFrame(columns = rank_csv_2.columns)

for i in range(len(rank_csv_2)):
    ticker = rank_csv_2['ticker'][i]
    if ticker in rank_csv_1['ticker'].values:
        df = df.append(rank_csv_2.iloc[i], ignore_index=True)

df.to_csv(output_path+"overseas_return_drawdown_amount.csv", sep=',',index=False)

