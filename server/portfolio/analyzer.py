import json
import numpy as np
import pandas as pd
import os

from portfolio.analysis_methods import PortfolioAnalysis


class Analyzer:

    def __init__(self, portfolio, rank_file_path, comments_output_path):
        self.portfolio = portfolio
        self.returns = self.portfolio.returns
        self.rank_file_path = rank_file_path
        self.comments_output_path = comments_output_path
        self.trading_days = 250
    def history(self):
        returns = self.portfolio.returns["return"]
        returns.index = returns.index.date
        return self._to_json(returns)

    # def rolling_sharpe(self, risk_free_rate=0.0, window=120): # transaction fee -> net return
    #     returns = self.returns.copy()
    #     returns['rolling_SR'] = returns['return'].rolling(window).apply(lambda x: (x.mean() - risk_free_rate) / x.std(),
    #                                                                     raw=True)
    #     comment=""
    #     if returns['rolling_SR'][-1] < (returns['return'].mean() / returns['return'].std()) - 0.1:
    #         comment = "This fund's has performed below its historical average in the last 6 months."
    #     elif returns['rolling_SR'][-1] > (returns['return'].mean() / returns['return'].std()) + 0.1:
    #         comment = "This fund's has performed below its historical average in the last 6 months."
    #     else:
    #         comment = "This fund's has performed inline with its historical average in the last 6 months."
    #
    #     sr = returns["rolling_SR"]
    #     return self._to_json(sr, "rolling_SR"), comment
    #
    # def sharpe(self, risk_free_rate=0.0):
    #     returns = self.returns.copy()
    #     sharpe_ratio = (returns['return'].mean() - risk_free_rate) / returns.std()
    #     return sharpe_ratio
    #
    #
    # def rolling_volatility(self, rolling_vol_window=120):
    #     returns = self.returns.copy()
    #     comment = ""
    #     rv = returns['return'].rolling(rolling_vol_window).std() \
    #         * np.sqrt(250)
    #     rv_json = self._to_json(rv)
    #     return rv_json, comment
    #
    #
    # def max_drawdown(self):
    #     returns = self.returns.copy()
    #     cumulative_returns = (1 + returns['return']).cumprod()
    #     max_cumulative_returns = cumulative_returns.cummax()
    #     drawdown = (cumulative_returns - max_cumulative_returns) / max_cumulative_returns
    #     drawdown_json = self._to_json(drawdown)
    #
    #     return drawdown_json, ""

    def analyze(self):
        comp_file_path = 'index_comps.csv'
        comp_file_path_2 = 'industry_comps.csv'
        comp_file_path = os.path.join(self.rank_file_path, comp_file_path)
        comp_file_path_2 = os.path.join(self.rank_file_path, comp_file_path_2)
        index_comps = pd.read_csv(comp_file_path).set_index('Date')
        industry_comps = pd.read_csv(comp_file_path_2).set_index('Date')
        index_comps.index = pd.to_datetime(index_comps.index)
        industry_comps.index = pd.to_datetime(industry_comps.index)
        self.rank_file_path = self.rank_file_path + "stock_"
        pa = PortfolioAnalysis(self.rank_file_path, self.comments_output_path)
        ticker = "Sample"
        df_target = self.portfolio.returns
        trading_days = 250
        rolling_sharpe_df = pd.DataFrame(index=df_target.index,
                                         columns=['rolling_SR_comments', 'excess_return_comments', 'alpha_comments',
                                                  'beta_comments', 'upside_capture_comments',
                                                  'downside_capture_comments', 'index_comments', 'sector_comments',
                                                  'volatility_comments', 'drawdown_amount_comments',
                                                  'drawdown_duration_comments', 'return_comments',
                                                  'return_corr_comments', 'return_benchmark_comments',
                                                  'alpha_benchmark_comments', 'beta_benchmark_comments',
                                                  'upside_benchmark_comments', 'downside_benchmark_comments',
                                                  'excess_sharpe_benchmark_comments', 'sr_benchmark_comments',
                                                  'drawdown_duration_benchmark_comments',
                                                  'drawdown_amount_benchmark_comments',
                                                  'volatility_benchmark_comments'])
        rolling_sharpe_df.to_csv(self.comments_output_path + 'comments.csv')

        df_target['annual_return'] = (1 + df_target['return']).rolling(window=trading_days).apply(np.prod, raw=True) - 1

        comp_3_name, comp_4_name, df_target = pa.corr_analysis(df_target, industry_comps, ticker,
                                                                           self.rank_file_path, self.rank_file_path,
                                                                           input_file_path=self.comments_output_path)

        comp_1_name, comp_2_name, df_target = pa.corr_analysis(df_target, index_comps, ticker,
                                                                           self.rank_file_path, self.rank_file_path,
                                                                           input_file_path=self.comments_output_path)

        df_target['rolling_mean'] = df_target['return'].rolling(self.trading_days).mean()
        df_target['comp_mean'] = index_comps[comp_1_name].rolling(self.trading_days).mean()

        df_target['comp_1'] = index_comps[comp_1_name]
        df_target['excess_return'] = df_target['return'] - df_target['comp_1'].pct_change()

        df_target = pa.rolling_sharpe(df_target, rank_file_path=self.rank_file_path,
                                      input_file_path=self.comments_output_path, security_code=ticker)

        df_target = pa.return_analysis(df_target)

        df_target = pa.max_drawdown_analysis(df_target, rank_file_path=self.rank_file_path, security_code=ticker,
                                                         input_file_path=self.comments_output_path)

        if comp_1_name in industry_comps:
            df_target = pa.alpha_beta_analysis(df_target, industry_comps[comp_1_name],
                                                           rank_file_path=self.rank_file_path,
                                                           input_file_path=self.comments_output_path, security_code=ticker)
        else:
            df_target = pa.alpha_beta_analysis(df_target, index_comps[comp_1_name],
                                                           rank_file_path=self.rank_file_path,
                                                           input_file_path=self.comments_output_path, security_code=ticker)

        df_target['累计净值'] = (1 + df_target['return']).cumprod()

        df1 = df_target[['累计净值', 'comp_1']]

        # Resample to month end and calculate the monthly percent change

        df_rets_monthly = df1.resample('M').last().pct_change().dropna()

        df_target = pa.market_capture_ratio(df_rets_monthly, df_target, rank_file_path=self.rank_file_path,
                                                        input_file_path=self.comments_output_path, security_code=ticker)


        if comp_1_name in industry_comps:
            df_target = pa.rolling_volatility(df_target, industry_comps[comp_1_name],
                                                          rank_file_path=self.rank_file_path,
                                                          input_file_path=self.comments_output_path, security_code=ticker)
        else:
            df_target = pa.rolling_volatility(df_target, index_comps[comp_1_name],
                                                          rank_file_path=self.rank_file_path,
                                                          input_file_path=self.comments_output_path, security_code=ticker)
        return df_target




    def _to_json(self, series, col="return"):
        df = series.to_frame()
        df.dropna(inplace=True)
        df.reset_index(inplace=True)
        df.rename(columns={col:"value"}, inplace=True)
        df_json = df.to_dict(orient='records')
        return df_json

