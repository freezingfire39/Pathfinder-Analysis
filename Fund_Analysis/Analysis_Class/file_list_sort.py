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
        print (root)
        print (dirs)
        print (files)
        df = pd.read_csv(file_path)
        strategy = df['基金类型'].iloc[0]
        ticker = df['基金代码'].iloc[0]
        ticker = ticker.split('（')[0]
        if strategy in ['债券型-混合二级', '债券型-长债', '债券型-混合一级', '债券型-中短债', '指数型-固收', 'QDII-纯债', 'QDII-混合债']:
            bond_list.append(ticker)

        elif strategy in ['混合型-灵活', '混合型-偏股', '指数型-股票', '股票型', '混合型-偏债', '混合型-绝对收益', '混合型-平衡', 'FOF-稳健型', 'FOF-进取型', 'FOF-均衡型']:
            stock_list.append(ticker)

        elif strategy in ['货币型-普通货币', '货币型-浮动净值']:
            money_market_list.append(ticker)
        elif strategy in ['QDII-普通股票', '指数型-海外股票', '指数型-其他', 'QDII-混合偏股', 'QDII-混合灵活', 'QDII-商品', 'QDII-混合平衡', 'QDII-REITs', '商品', 'QDII-FOF']:
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
