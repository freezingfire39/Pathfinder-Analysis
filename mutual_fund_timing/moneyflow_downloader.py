import tushare as ts
pro = ts.pro_api('84be1015becc0b9dbbab507552c328cbf447bc02cbd29cfa09029bc6')

#获取单日全部股票数据
df = pro.moneyflow(trade_date='20241115')

print (df)
