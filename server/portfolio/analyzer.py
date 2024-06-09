import json
import numpy as np
class Analyzer:

    def __init__(self, portfolio):
        self.portfolio = portfolio
        self.returns = self.portfolio.returns

    def rolling_sharpe(self, risk_free_rate=0.0, window=120):
        returns = self.returns.copy()
        returns['rolling_SR'] = returns['return'].rolling(window).apply(lambda x: (x.mean() - risk_free_rate) / x.std(),
                                                                        raw=True)
        comment=""
        if returns['rolling_SR'][-1] < (returns['return'].mean() / returns['return'].std()) - 0.1:
            comment = "This fund's has performed below its historical average in the last 6 months."
        elif returns['rolling_SR'][-1] > (returns['return'].mean() / returns['return'].std()) + 0.1:
            comment = "This fund's has performed below its historical average in the last 6 months."
        else:
            comment = "This fund's has performed inline with its historical average in the last 6 months."

        sr = returns["rolling_SR"]
        return self._to_json(sr), comment

    def sharpe(self, risk_free_rate=0.0):
        returns = self.returns.copy()
        sharpe_ratio = (returns['return'].mean() - risk_free_rate) / returns.std()
        return sharpe_ratio


    def rolling_volatility(self, rolling_vol_window=120):
        returns = self.returns.copy()
        comment = ""
        rv = returns['return'].rolling(rolling_vol_window).std() \
            * np.sqrt(250)
        rv_json = self._to_json(rv)
        return rv_json, comment


    def max_drawdown(self):
        returns = self.returns.copy()
        cumulative_returns = (1 + returns['return']).cumprod()
        max_cumulative_returns = cumulative_returns.cummax()
        drawdown = (cumulative_returns - max_cumulative_returns) / max_cumulative_returns
        drawdown_json = self._to_json(drawdown)

        return drawdown_json


    def _to_json(self, series):
        df = series.to_frame()
        df.reset_index(inplace=True)
        df_json = df.to_json(orient='records', date_format='iso')
        return df_json






