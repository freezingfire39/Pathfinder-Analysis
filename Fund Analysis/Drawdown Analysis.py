import pyfolio as pf
import pandas as pd

wealth_index = 1000*(1+df_target['return']).cumprod()
previous_peaks = wealth_index.cummax()
drawdown = (wealth_index-previous_peaks)/previous_peaks
drawdown.plot()
pf.show_worst_drawdown_periods(df_target['return'])
