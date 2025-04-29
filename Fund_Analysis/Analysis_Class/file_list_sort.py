import os
import pandas as pd

stock_list=[]
bond_list=[]
money_market_list=[]
overseas_list=[]
others_list=[]
missing_list=[]

target_filename = 'Background.csv'

root_folder = '/home/app/Desktop/output_china'
for root, dirs, files in os.walk(root_folder):
    if target_filename in files:
        file_path = os.path.join(root, target_filename)
        df = pd.read_csv(file_path)
        strategy = df['基金类型'].iloc[0]
        ticker = df['基金代码'].iloc[0]
        ticker = ticker.split('（')[0]
        if strategy == '债券型-混合二级' or '债券型-长债' or '债券型-混合一级' or '债券型-中短债' or '指数型-固收' or 'QDII-纯债' or 'QDII-混合债':
            bond_list.append(ticker)

        elif strategy == '混合型-灵活' or '混合型-偏股' or '指数型-股票' or '股票型' or '混合型-偏债' or '混合型-绝对收益' or '混合型-平衡' or 'FOF-稳健型' or 'FOF-进取型' or 'FOF-均衡型':
            stock_list.append(ticker)

        elif strategy == '货币型-普通货币' or '货币型-浮动净值':
            money_market_list.append(ticker)
        elif strategy == 'QDII-普通股票' or '指数型-海外股票' or '指数型-其他' or 'QDII-混合偏股' or 'QDII-混合灵活' or 'QDII-商品' or 'QDII-混合平衡' or 'QDII-REITs' or '商品' or 'QDII-FOF':
            overseas_list.append(ticker)
        else:
            others_list.append(ticker)

    else:
        missing_list.append(dirs)



print (stock_list)
print (bond_list)
print (money_market_list)
print (overseas_list)
print (others_list)
print (missing_list)
