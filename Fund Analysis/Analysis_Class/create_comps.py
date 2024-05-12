import pandas as pd
import matplotlib.pyplot as plt
import empyrical as ep
import numpy as np
import pandas as pd
import scipy as sp
import scipy.stats as stats
from sklearn import linear_model
import matplotlib.gridspec as gridspec
from collections import OrderedDict
from IPython.display import display, HTML
from sklearn.linear_model import LinearRegression
import yfinance as yf
from datetime import datetime


start = datetime(2010, 1, 1)
symbols_list = ['510050.SS', '159901.SZ', '159949.SZ', '510300.SS', '510500.SS', '512100.SS', '588000.SS', '510900.SS']

#array to store prices
symbols=[]
for ticker in symbols_list:
    r = yf.download(ticker, start=start, end="2024-05-05")
    # add a symbol column
    r['Symbol'] = ticker
    symbols.append(r)
# concatenate into df
df = pd.concat(symbols)
df = df.reset_index()
df = df[['Date', 'Close', 'Symbol']]
df.head()
df_pivot=df.pivot('Date','Symbol','Close').reset_index()
df_pivot.set_index('Date',inplace=True)
df_pivot.index = pd.to_datetime(df_pivot.index)
df_pivot.to_csv("index_comps.csv")


symbols_list = ['510230.SS', '512010.SS', '512170.SS', '515170.SS', '512480.SS', '515230.SS', '512660.SS', '516220.SS','516800.SS',"512400.SS","159825.SZ","516950.SS","516070.SS"]
#array to store prices
symbols=[]

#array to store prices
symbols=[]
for ticker in symbols_list:
    r = yf.download(ticker, start=start, end="2024-05-05")
    # add a symbol column
    r['Symbol'] = ticker
    symbols.append(r)
# concatenate into df
df = pd.concat(symbols)
df = df.reset_index()
df = df[['Date', 'Close', 'Symbol']]
df.head()
df_pivot=df.pivot('Date','Symbol','Close').reset_index()


df_pivot.set_index('Date',inplace=True)
df_pivot.index = pd.to_datetime(df_pivot.index)

df_pivot.to_csv("industry_comps.csv")
