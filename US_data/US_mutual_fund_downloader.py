import yfinance as yf
import pandas as pd

Ticker_df = pd.read_csv('tickers.csv')


for tickers in Ticker_df['Ticker']:
    df_data = yf.download(tickers,start="2010-01-01",end="2024-01-01")
    df_data.to_csv(tickers+"_return.csv")
    ticker = yf.Ticker(tickers)
    df_dividend = ticker.actions
    df_dividend.to_csv(tickers+"_dividend.csv")
    df_info = pd.json_normalize(ticker.info)
    df_info.to_csv(tickers+"_info.csv")
