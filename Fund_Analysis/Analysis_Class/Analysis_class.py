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
import seaborn
from matplotlib.ticker import FuncFormatter
import utils
import statsmodels.api as sm
from statsmodels import regression

def rolling_sharpe(returns, rank_file_path,input_file_path,security_code,asset_type,risk_free_rate=0.0, window=250):

    returns['rolling_SR'] = returns['return'].rolling(window).apply(lambda x: (x.mean() - risk_free_rate) / x.std(), raw = True)
    
    comment_csv = pd.read_csv(input_file_path+'comments.csv').set_index('净值日期')
    if returns['rolling_SR'].iloc[-1] < (returns['return'].mean()/returns['return'].std())-0.1:
        #print ("This fund's has performed below its historical average in the last 6 months.")
        #print ("本基金最近一年的夏普指数低于其历史平均水平，意味着策略的近期表现有所下降。")
        comment_csv.at[comment_csv.index[-1],'rolling_SR_comments']  = "本基金最近一年的夏普指数低于其历史平均水平，意味着策略的近期表现有所下降。"
        comment_csv.to_csv(input_file_path+'comments.csv')
    elif returns['rolling_SR'].iloc[-1] > (returns['return'].mean()/returns['return'].std())+0.1:
        #print ("This fund's has performed below its historical average in the last 6 months.")
        #print ("本基金最近一年的夏普指数高于其历史平均水平，意味着策略的近期表现有所上升。")
        comment_csv.at[comment_csv.index[-1],'rolling_SR_comments']   = "本基金最近一年的夏普指数高于其历史平均水平，意味着策略的近期表现有所上升。"
        comment_csv.to_csv(input_file_path+'comments.csv')
    else:
        #print ("This fund's has performed inline with its historical average in the last 6 months.")
        comment_csv.at[comment_csv.index[-1],'rolling_SR_comments']  = "本基金最近一年的夏普指数与其历史平均水平基本一致，意味着策略的近期表现没有很大的变化。"
        comment_csv.to_csv(input_file_path+'comments.csv')
        #print ("本基金最近一年的夏普指数与其历史平均水平基本一致，意味着策略的近期表现没有很大的变化。")
        
    rank_file = pd.read_csv(rank_file_path+'rolling_sharpe_rank.csv').set_index('Unnamed: 0')
    if returns['rolling_SR'][-1] > 0.8:

        new_row = {'ticker': security_code, 'value': returns['rolling_SR'][-1]}
        rank_file.loc[len(rank_file)] = new_row
        #rank_file['ticker'] = rank_file['ticker'].apply('="{}"'.format)
        rank_file.to_csv(rank_file_path+'rolling_sharpe_rank.csv')
    returns['excess_return'].fillna(method='ffill',inplace=True)
    returns['excess_SR'] = returns['excess_return'].rolling(window).apply(lambda x: (x.mean() - risk_free_rate) / x.std(), raw = True)


    comment_csv = pd.read_csv(input_file_path+'comments.csv').set_index('净值日期')
    if returns['excess_SR'].iloc[-1] < (returns['excess_return'].mean()/returns['excess_return'].std())-0.1:
        #print ("This fund's has performed below its historical average in the last 6 months.")
        #print ("本基金最近一年的夏普指数低于其历史平均水平，意味着策略的近期表现有所下降。")
        comment_csv.at[comment_csv.index[-1],'excess_return_comments']  = "本基金最近一年的基本表现弱于对标的基准指数"+returns['benchmark_name'][-1]
        print (comment_csv)
        comment_csv.to_csv(input_file_path+'comments.csv')
    elif returns['rolling_SR'].iloc[-1] > (returns['return'].mean()/returns['return'].std())+0.1:
        #print ("This fund's has performed below its historical average in the last 6 months.")
        #print ("本基金最近一年的夏普指数高于其历史平均水平，意味着策略的近期表现有所上升。")
        comment_csv.at[comment_csv.index[-1],'excess_return_comments']  = "本基金最近一年的基本表现强于对标的基准指数"+returns['benchmark_name'][-1]
        print (comment_csv)
        comment_csv.to_csv(input_file_path+'comments.csv')
    else:
        #print ("This fund's has performed inline with its historical average in the last 6 months.")
        comment_csv.at[comment_csv.index[-1],'excess_return_comments']  = "本基金最近一年的基本表现持平对标的基准指数"+returns['benchmark_name'][-1]
        print (comment_csv)

        comment_csv.to_csv(input_file_path+'comments.csv')
        #print ("本基金最近一年的夏普指数与其历史平均水平基本一致，意味着策略的近期表现没有很大的变化。")


    
    if asset_type=='bond_':
    
        if returns['return'].corr(returns['comp_1'])>0.8:
            if returns['excess_SR'][-1]>0.2:
                print ('This fund has adopted similar strategy to 10 year treasury bond but it has generated stronger return recently.')
            elif returns['excess_SR'][-1]<-0.2:
                print ('This fund has adopted similar strategy to 10 year treasury bond but it has generated weaker return recently.')
            else:
                print ('This fund has adopted similar strategy to 10 year treasury bond and its performance is also similar.')

        else:
            if returns['excess_SR'][-1]>0.2:
                print ('This fund has adopted different strategy to 10 year treasury bond but it has generated stronger return recently.')
            elif returns['excess_SR'][-1]<-0.2:
                print ('This fund has adopted different strategy to 10 year treasury bond but it has generated weaker return recently.')
            else:
                print ('This fund has adopted different strategy to 10 year treasury bond but its performance is similar.')
    return returns


def plot_drawdown_periods(returns, top=10, ax=None, **kwargs):
    """
    Plots cumulative returns highlighting top drawdown periods.

    Parameters
    ----------
    returns : pd.Series
        Daily returns of the strategy, noncumulative.
         - See full explanation in tears.create_full_tear_sheet.
    top : int, optional
        Amount of top drawdowns periods to plot (default 10).
    ax : matplotlib.Axes, optional
        Axes upon which to plot.
    **kwargs, optional
        Passed to plotting function.

    Returns
    -------
    ax : matplotlib.Axes
        The axes that were plotted on.
    """

    if ax is None:
        ax = plt.gca()

    y_axis_formatter = FuncFormatter(utils.two_dec_places)
    ax.yaxis.set_major_formatter(FuncFormatter(y_axis_formatter))

    df_cum_rets = ep.cum_returns(returns, starting_value=1.0)
    df_drawdowns = timeseries.gen_drawdown_table(returns, top=top)

    df_cum_rets.plot(ax=ax, **kwargs)

    lim = ax.get_ylim()
    colors = sns.cubehelix_palette(len(df_drawdowns))[::-1]
    for i, (peak, recovery) in df_drawdowns[
            ['Peak date', 'Recovery date']].iterrows():
        if pd.isnull(recovery):
            recovery = returns.index[-1]
        ax.fill_between((peak, recovery),
                        lim[0],
                        lim[1],
                        alpha=.4,
                        color=colors[i])
    ax.set_ylim(lim)
    ax.set_title('Top %i drawdown periods' % top)
    ax.set_ylabel('Cumulative returns')
    ax.legend(['Portfolio'], loc='upper left',
              frameon=True, framealpha=0.5)
    ax.set_xlabel('')
    return ax


def plot_drawdown_underwater(returns, ax=None, **kwargs):
    """
    Plots how far underwaterr returns are over time, or plots current
    drawdown vs. date.

    Parameters
    ----------
    returns : pd.Series
        Daily returns of the strategy, noncumulative.
         - See full explanation in tears.create_full_tear_sheet.
    ax : matplotlib.Axes, optional
        Axes upon which to plot.
    **kwargs, optional
        Passed to plotting function.

    Returns
    -------
    ax : matplotlib.Axes
        The axes that were plotted on.
    """

    if ax is None:
        ax = plt.gca()

    y_axis_formatter = FuncFormatter(utils.percentage)
    ax.yaxis.set_major_formatter(FuncFormatter(y_axis_formatter))

    df_cum_rets = ep.cum_returns(returns['return'], starting_value=1.0)
    running_max = np.maximum.accumulate(df_cum_rets)
    underwater = -100 * ((running_max - df_cum_rets) / running_max)
    (underwater).plot(ax=ax, kind='area', color='coral', alpha=0.7, **kwargs)
    ax.set_ylabel('Drawdown')
    ax.set_title('Underwater plot')
    ax.set_xlabel('')
    return ax

def get_max_drawdown_underwater(underwater):
    """
    Determines peak, valley, and recovery dates given an 'underwater'
    DataFrame.

    An underwater DataFrame is a DataFrame that has precomputed
    rolling drawdown.

    Parameters
    ----------
    underwater : pd.Series
       Underwater returns (rolling drawdown) of a strategy.

    Returns
    -------
    peak : datetime
        The maximum drawdown's peak.
    valley : datetime
        The maximum drawdown's valley.
    recovery : datetime
        The maximum drawdown's recovery.
    """

    valley = underwater.idxmin()  # end of the period
    # Find first 0
    peak = underwater[:valley][underwater[:valley] == 0].index[-1]
    # Find last 0
    try:
        recovery = underwater[valley:][underwater[valley:] == 0].index[0]
    except IndexError:
        recovery = np.nan  # drawdown not recovered
    return peak, valley, recovery


def get_max_drawdown(returns):
    """
    Determines the maximum drawdown of a strategy.

    Parameters
    ----------
    returns : pd.Series
        Daily returns of the strategy, noncumulative.
        - See full explanation in :func:`~pyfolio.timeseries.cum_returns`.

    Returns
    -------
    float
        Maximum drawdown.

    Note
    -----
    See https://en.wikipedia.org/wiki/Drawdown_(economics) for more details.
    """

    returns = returns.copy()
    df_cum = cum_returns(returns['return'], 1.0)
    running_max = np.maximum.accumulate(df_cum)
    underwater = df_cum / running_max - 1
    return get_max_drawdown_underwater(underwater)


def get_top_drawdowns(returns, top=10):
    """
    Finds top drawdowns, sorted by drawdown amount.

    Parameters
    ----------
    returns : pd.Series
        Daily returns of the strategy, noncumulative.
         - See full explanation in tears.create_full_tear_sheet.
    top : int, optional
        The amount of top drawdowns to find (default 10).

    Returns
    -------
    drawdowns : list
        List of drawdown peaks, valleys, and recoveries. See get_max_drawdown.
    """

    returns = returns.copy()
    df_cum = ep.cum_returns(returns['return'], 1.0)
    running_max = np.maximum.accumulate(df_cum)
    underwater = df_cum / running_max - 1

    drawdowns = []
    for _ in range(top):
        peak, valley, recovery = get_max_drawdown_underwater(underwater)
        # Slice out draw-down period
        if not pd.isnull(recovery):
            underwater.drop(underwater[peak: recovery].index[1:-1],
                            inplace=True)
        else:
            # drawdown has not ended yet
            underwater = underwater.loc[:peak]

        drawdowns.append((peak, valley, recovery))
        if ((len(returns) == 0)
                or (len(underwater) == 0)
                or (np.min(underwater) == 0)):
            break

    return drawdowns


def gen_drawdown_table(returns, rank_file_path,security_code,input_file_path,top=10):
    """
    Places top drawdowns in a table.

    Parameters
    ----------
    returns : pd.Series
        Daily returns of the strategy, noncumulative.
         - See full explanation in tears.create_full_tear_sheet.
    top : int, optional
        The amount of top drawdowns to find (default 10).

    Returns
    -------
    df_drawdowns : pd.DataFrame
        Information about top drawdowns.
    """

    df_cum = ep.cum_returns(returns['return'], 1.0)
    drawdown_periods = get_top_drawdowns(returns, top=top)
    df_drawdowns = pd.DataFrame(index=list(range(top)),
                                columns=['Net drawdown in %',
                                         'Peak date',
                                         'Valley date',
                                         'Recovery date',
                                         'Duration'])

    for i, (peak, valley, recovery) in enumerate(drawdown_periods):
        if pd.isnull(recovery):
            df_drawdowns.loc[i, 'Duration'] = np.nan
        else:
            df_drawdowns.loc[i, 'Duration'] = len(pd.date_range(peak,
                                                                recovery,
                                                                freq='B'))
        df_drawdowns.loc[i, 'Peak date'] = (peak.to_pydatetime()
                                            .strftime('%Y-%m-%d'))
        df_drawdowns.loc[i, 'Valley date'] = (valley.to_pydatetime()
                                              .strftime('%Y-%m-%d'))
        if isinstance(recovery, float):
            df_drawdowns.loc[i, 'Recovery date'] = recovery
        else:
            df_drawdowns.loc[i, 'Recovery date'] = (recovery.to_pydatetime()
                                                    .strftime('%Y-%m-%d'))
        df_drawdowns.loc[i, 'Net drawdown in %'] = (
            (df_cum.loc[peak] - df_cum.loc[valley]) / df_cum.loc[peak]) * 100

    df_drawdowns['Peak date'] = pd.to_datetime(df_drawdowns['Peak date'])
    df_drawdowns['Valley date'] = pd.to_datetime(df_drawdowns['Valley date'])
    df_drawdowns['Recovery date'] = pd.to_datetime(
        df_drawdowns['Recovery date'])
    df_drawdowns.to_csv('drawdown.csv')
    returns['drawdown_duration'] = 0
    returns['drawdown_amount'] = 0
    returns['drawdown_duration'] = returns['drawdown_duration'].astype(int)
    returns['drawdown_amount'] = returns['drawdown_amount'].astype(int)
    print (df_drawdowns['Duration'].max())
    returns['drawdown_duration'].iloc[-1] = df_drawdowns['Duration'].max()
    returns['drawdown_amount'].iloc[-1] = df_drawdowns['Net drawdown in %'].max()


    comment_csv = pd.read_csv(input_file_path+'comments.csv').set_index('净值日期')
    
    print (returns.tail(10))
    if df_drawdowns['Duration'].mean()>400:
        comment_csv.at[comment_csv.index[-1],'drawdown_duration_comments']  = "本基金的回撤时间大于类似产品的平均，意味着在亏损的时候会需要更多的时间回到原点。"
        comment_csv.to_csv(input_file_path+'comments.csv')
        #print ("compare to industry average, this security has longer drawdowns")
        #print ("本基金的回撤时间大于类似产品的平均，意味着在亏损的时候会需要更多的时间回到原点。")
    elif df_drawdowns['Duration'].mean()<300:
        comment_csv.at[comment_csv.index[-1],'drawdown_duration_comments']  = "本基金的回撤时间小于类似产品的平均，意味着在亏损的时候会需要更少的时间回到原点。"
        comment_csv.to_csv(input_file_path+'comments.csv')
        #print ("compare to industry average, this security has shorter drawdowns")
        #print ("本基金的回撤时间小于类似产品的平均，意味着在亏损的时候会需要更少的时间回到原点。")
    else:
        comment_csv.at[comment_csv.index[-1],'drawdown_duration_comments']  = "本基金的回撤时间与类似产品的平均基本一致。"
        comment_csv.to_csv(input_file_path+'comments.csv')
        #print ("This security's drawdown duration is inline with industry average")
        #print ("本基金的回撤时间与类似产品的平均基本一致。")

    if returns['drawdown_amount'][-1]>0.3:
        comment_csv.at[comment_csv.index[-1],'drawdown_amount_comments']  = "本基金的最大回撤大于类似产品的平均，意味着在最坏情况的亏损的时候会相对更高。"
        comment_csv.to_csv(input_file_path+'comments.csv')
        #print ("compare to industry average, this security has longer drawdowns")
        #print ("本基金的回撤时间大于类似产品的平均，意味着在亏损的时候会需要更多的时间回到原点。")
    elif returns['drawdown_amount'][-1]<0.2:
        comment_csv.at[comment_csv.index[-1],'drawdown_amount_comments']  = "本基金的最大回撤小于类似产品的平均，意味着在最坏情况的亏损的时候会相对更低。"
        comment_csv.to_csv(input_file_path+'comments.csv')
        #print ("compare to industry average, this security has shorter drawdowns")
        #print ("本基金的回撤时间小于类似产品的平均，意味着在亏损的时候会需要更少的时间回到原点。")
    else:
        comment_csv.at[comment_csv.index[-1],'drawdown_amount_comments']  = "本基金的最大回撤与类似产品的平均一致。"
        comment_csv.to_csv(input_file_path+'comments.csv')
        #print ("This security's drawdown duration is inline with industry average")
        #print ("本基金的回撤时间与类似产品的平均基本一致。")
    
    rank_file = pd.read_csv(rank_file_path+'drawdown_duration_rank.csv').set_index('Unnamed: 0')
    if returns['drawdown_duration'].iloc[-1] < 300:

        new_row = {'ticker': security_code, 'value': returns['drawdown_duration'][-1]}
        rank_file.loc[len(rank_file)] = new_row
        #rank_file['ticker'] = rank_file['ticker'].apply('="{}"'.format)
        rank_file.to_csv(rank_file_path+'drawdown_duration_rank.csv')
        
    rank_file = pd.read_csv(rank_file_path+'drawdown_amount_rank.csv').set_index('Unnamed: 0')
    if returns['drawdown_amount'].iloc[-1] < 0.2:

        new_row = {'ticker': security_code, 'value': returns['drawdown_amount'][-1]}
        rank_file.loc[len(rank_file)] = new_row
        #rank_file['ticker'] = rank_file['ticker'].apply('="{}"'.format)
        rank_file.to_csv(rank_file_path+'drawdown_amount_rank.csv')
        
    return returns
    
def max_drawdown_analysis(returns, rank_file_path,security_code,input_file_path):
    returns = gen_drawdown_table(returns, rank_file_path,security_code,input_file_path)
    plot_drawdown_underwater(returns)
    return returns
    

PERIODS = OrderedDict()
# Dotcom bubble
PERIODS['Dotcom'] = (pd.Timestamp('20000310'), pd.Timestamp('20000910'))

# Lehmann Brothers
PERIODS['Lehman'] = (pd.Timestamp('20080801'), pd.Timestamp('20081001'))

# 9/11
PERIODS['9/11'] = (pd.Timestamp('20010911'), pd.Timestamp('20011011'))

# 05/08/11  US down grade and European Debt Crisis 2011
PERIODS[
    'US downgrade/European Debt Crisis'] = (pd.Timestamp('20110805'),
                                            pd.Timestamp('20110905'))

# 16/03/11  Fukushima melt down 2011
PERIODS['Fukushima'] = (pd.Timestamp('20110316'), pd.Timestamp('20110416'))

# 01/08/03  US Housing Bubble 2003
PERIODS['US Housing'] = (
    pd.Timestamp('20030108'), pd.Timestamp('20030208'))

# 06/09/12  EZB IR Event 2012
PERIODS['EZB IR Event'] = (
    pd.Timestamp('20120910'), pd.Timestamp('20121010'))

# August 2007, March and September of 2008, Q1 & Q2 2009,
PERIODS['Aug07'] = (pd.Timestamp('20070801'), pd.Timestamp('20070901'))
PERIODS['Mar08'] = (pd.Timestamp('20080301'), pd.Timestamp('20080401'))
PERIODS['Sept08'] = (pd.Timestamp('20080901'), pd.Timestamp('20081001'))
PERIODS['2009Q1'] = (pd.Timestamp('20090101'), pd.Timestamp('20090301'))
PERIODS['2009Q2'] = (pd.Timestamp('20090301'), pd.Timestamp('20090601'))

# Flash Crash (May 6, 2010 + 1 week post),
PERIODS['Flash Crash'] = (
    pd.Timestamp('20100505'), pd.Timestamp('20100510'))

# April and October 2014).
PERIODS['Apr14'] = (pd.Timestamp('20140401'), pd.Timestamp('20140501'))
PERIODS['Oct14'] = (pd.Timestamp('20141001'), pd.Timestamp('20141101'))

# Market down-turn in August/Sept 2015
PERIODS['Fall2015'] = (pd.Timestamp('20150815'), pd.Timestamp('20150930'))

# Market regimes
PERIODS['Low Volatility Bull Market'] = (pd.Timestamp('20050101'),
                                         pd.Timestamp('20070801'))

PERIODS['GFC Crash'] = (pd.Timestamp('20070801'),
                        pd.Timestamp('20090401'))

PERIODS['Recovery'] = (pd.Timestamp('20090401'),
                       pd.Timestamp('20130101'))

PERIODS['New Normal'] = (pd.Timestamp('20130101'),
                         pd.Timestamp('today'))
                         
##China Stock Crash
PERIODS['New Normal'] = (pd.Timestamp('20070201'),
                         pd.Timestamp('20071101'))
PERIODS['2015 Crash'] = (pd.Timestamp('20150601'),
                         pd.Timestamp('20160201'))
PERIODS['2023 Crash'] = (pd.Timestamp('20231201'),
                         pd.Timestamp('20240222'))
                         
PERIODS['Covid'] = (pd.Timestamp('20191201'),
                         pd.Timestamp('20200601'))

def print_table(table,
                name=None,
                float_format=None,
                formatters=None,
                header_rows=None):
    """
    Pretty print a pandas DataFrame.

    Uses HTML output if running inside Jupyter Notebook, otherwise
    formatted text output.

    Parameters
    ----------
    table : pandas.Series or pandas.DataFrame
        Table to pretty-print.
    name : str, optional
        Table name to display in upper left corner.
    float_format : function, optional
        Formatter to use for displaying table elements, passed as the
        `float_format` arg to pd.Dataframe.to_html.
        E.g. `'{0:.2%}'.format` for displaying 100 as '100.00%'.
    formatters : list or dict, optional
        Formatters to use by column, passed as the `formatters` arg to
        pd.Dataframe.to_html.
    header_rows : dict, optional
        Extra rows to display at the top of the table.
    """

    if isinstance(table, pd.Series):
        table = pd.DataFrame(table)

    if name is not None:
        table.columns.name = name

    html = table.to_html(float_format=float_format, formatters=formatters)

    if header_rows is not None:
        # Count the number of columns for the text to span
        n_cols = html.split('<thead>')[1].split('</thead>')[0].count('<th>')

        # Generate the HTML for the extra rows
        rows = ''
        for name, value in header_rows.items():
            rows += ('\n    <tr style="text-align: right;"><th>%s</th>' +
                     '<td colspan=%d>%s</td></tr>') % (name, n_cols, value)

        # Inject the new HTML
        html = html.replace('<thead>', '<thead>' + rows)

    display(HTML(html))


def standardize_data(x):
    """
    Standardize an array with mean and standard deviation.

    Parameters
    ----------
    x : np.array
        Array to standardize.

    Returns
    -------
    np.array
        Standardized array.
    """

    return (x - np.mean(x)) / np.std(x)

def extract_interesting_date_ranges(returns, periods=None):
    """
    Extracts returns based on interesting events. See
    gen_date_range_interesting.

    Parameters
    ----------
    returns : pd.Series
        Daily returns of the strategy, noncumulative.
         - See full explanation in tears.create_full_tear_sheet.

    Returns
    -------
    ranges : OrderedDict
        Date ranges, with returns, of all valid events.
    """
    if periods is None:
        periods = PERIODS
    returns_dupe = returns.copy()
    returns_dupe.index = returns_dupe.index.map(pd.Timestamp)
    ranges = OrderedDict()
    for name, (start, end) in periods.items():
        try:
            period = returns_dupe.loc[start:end]
            if len(period) == 0:
                continue
            ranges[name] = period
        except BaseException:
            continue

    return ranges
def create_interesting_times_tear_sheet(returns, benchmark_rets=None,
                                        periods=None, legend_loc='best',
                                        return_fig=False):
    """
    Generate a number of returns plots around interesting points in time,
    like the flash crash and 9/11.

    Plots: returns around the dotcom bubble burst, Lehmann Brothers' failure,
    9/11, US downgrade and EU debt crisis, Fukushima meltdown, US housing
    bubble burst, EZB IR, Great Recession (August 2007, March and September
    of 2008, Q1 & Q2 2009), flash crash, April and October 2014.

    benchmark_rets must be passed, as it is meaningless to analyze performance
    during interesting times without some benchmark to refer to.

    Parameters
    ----------
    returns : pd.Series
        Daily returns of the strategy, noncumulative.
         - See full explanation in create_full_tear_sheet.
    benchmark_rets : pd.Series
        Daily noncumulative returns of the benchmark.
         - This is in the same style as returns.
    periods: dict or OrderedDict, optional
        historical event dates that may have had significant
        impact on markets
    legend_loc : plt.legend_loc, optional
         The legend's location.
    return_fig : boolean, optional
        If True, returns the figure that was plotted on.
    """

    rets_interesting = extract_interesting_date_ranges(
        returns, periods)

    if not rets_interesting:
        warnings.warn('Passed returns do not overlap with any'
                      'interesting times.', UserWarning)
        return

    print_table(pd.DataFrame(rets_interesting)
                      .describe().transpose()
                      .loc[:, ['mean', 'min', 'max']] * 100,
                      name='Stress Events',
                      float_format='{0:.2f}%'.format)

    if benchmark_rets is not None:
        returns = utils.clip_returns_to_benchmark(returns, benchmark_rets)

        bmark_interesting = extract_interesting_date_ranges(
            benchmark_rets, periods)

    num_plots = len(rets_interesting)
    # 2 plots, 1 row; 3 plots, 2 rows; 4 plots, 2 rows; etc.
    num_rows = int((num_plots + 1) / 2.0)
    fig = plt.figure(figsize=(14, num_rows * 6.0))
    gs = gridspec.GridSpec(num_rows, 2, wspace=0.5, hspace=0.5)

    for i, (name, rets_period) in enumerate(rets_interesting.items()):
        # i=0 -> 0, i=1 -> 0, i=2 -> 1 ;; i=0 -> 0, i=1 -> 1, i=2 -> 0
        ax = plt.subplot(gs[int(i / 2.0), i % 2])

        ep.cum_returns(rets_period).plot(
            ax=ax, color='forestgreen', label='algo', alpha=0.7, lw=2)

        if benchmark_rets is not None:
            ep.cum_returns(bmark_interesting[name]).plot(
                ax=ax, color='gray', label='benchmark', alpha=0.6)
            ax.legend(['Algo',
                       'benchmark'],
                      loc=legend_loc, frameon=True, framealpha=0.5)
        else:
            ax.legend(['Algo'],
                      loc=legend_loc, frameon=True, framealpha=0.5)

        ax.set_title(name)
        ax.set_ylabel('Returns')
        ax.set_xlabel('')

    if return_fig:
        return fig
    
def event_analysis(returns):
    create_interesting_times_tear_sheet(returns)
    
    
def linreg(x,y):
    x = sm.add_constant(x)
    model = regression.linear_model.OLS(y,x).fit()

    # We are removing the constant
    x = x[:, 1]
    return model.params[0], model.params[1]

def alpha_beta_analysis(returns, comp, security_code,rank_file_path,input_file_path, window=250):

    returns['alpha'] = 0
    returns['alpha'] = returns['alpha'].astype('float64')
    returns['beta'] = 0
    returns['beta'] = returns['beta'].astype('float64')
    comp.dropna(inplace=True)
    returns_2 = returns.copy()
    df_drop=[]
    for i in returns_2.index:
        if i not in comp.index:
            df_drop.append(i)
    returns_2 = returns_2.drop(df_drop, axis=0)


    df_drop=[]
    for i in comp.index:
        if i not in returns.index:
            df_drop.append(i)
    comp = comp.drop(df_drop, axis=0)
    comp = comp.pct_change()

    for i in range(len(returns_2)):
        if i<window:
            pass
        else:
        
            df_temp_1 = returns_2.iloc[i-window:i]
            df_temp_2 = comp.iloc[i-window:i]

            X = df_temp_1['return'][1:].values
            Y = df_temp_2[1:].values
            alpha, beta = linreg(X,Y)
            returns_2['alpha'][i]=alpha
            returns_2['beta'][i]=beta
            

    returns['alpha'] = returns_2['alpha']
    returns['beta'] = returns_2['beta']

    comment_csv = pd.read_csv(input_file_path+'comments.csv').set_index('净值日期')
    
    if returns['alpha'][-1]>0.1:
        #print ("This fund has outperformed the benchmark")
        comment_csv.at[comment_csv.index[-1],'alpha_comments']  = "本基金对比基准指数取得了较明显的超额收益。"
        comment_csv.to_csv(input_file_path+'comments.csv')
        #print ("本基金对比基准指数取得了较明显的超额收益")
    elif returns['alpha'][-1]<-0.1:
        comment_csv.at[comment_csv.index[-1],'alpha_comments']  = "本基金对比基准指数有较明显的超额亏损。"
        comment_csv.to_csv(input_file_path+'comments.csv')
        #print ("This fund has outperformed the benchmark")
        #print ("本基金对比基准指数有较明显的超额亏损")
    else:
        print ("This fund has not outperformed the benchmark")
        comment_csv.at[comment_csv.index[-1],'alpha_comments']  = "本基金回报对比指数基本一致。"
        comment_csv.to_csv(input_file_path+'comments.csv')
        #print ("本基金回报对比指数基本一致")
    if returns['beta'][-1]>1.2:
        comment_csv.at[comment_csv.index[-1],'beta_comments']  = "本基金对比基准指数有更高的波动率。"
        comment_csv.to_csv(input_file_path+'comments.csv')
        #print ("This fund is considerably more volatile than the benchmark")
        #print ("本基金对比基准指数有更高的波动率")
    elif returns['beta'][-1]<-1.2:
        comment_csv.at[comment_csv.index[-1],'beta_comments']  = "本基金对比基准指数有较低的波动率。"
        comment_csv.to_csv(input_file_path+'comments.csv')
        #print ("This fund is considerably less volatile than the market")
        #print ("本基金对比基准指数有较低的波动率")
    else:
        comment_csv.at[comment_csv.index[-1],'beta_comments']  = "本基金对比基准指数的波动率基本一致。"
        comment_csv.to_csv(input_file_path+'comments.csv')
        #print ("This fund's volatilty is in line with benchmark")
        #print ("本基金对比基准指数的波动率基本一致)
    rank_file = pd.read_csv(rank_file_path+'alpha_rank.csv').set_index('Unnamed: 0')
    if returns['alpha'][-1] > 0.1:

        new_row = {'ticker': security_code, 'value': returns['alpha'][-1]}
        rank_file.loc[len(rank_file)] = new_row
        #rank_file['ticker'] = rank_file['ticker'].apply('="{}"'.format)
        rank_file.to_csv(rank_file_path+'alpha_rank.csv')
        
    rank_file = pd.read_csv(rank_file_path+'positive_beta_rank.csv').set_index('Unnamed: 0')
    if returns['beta'][-1] > 1.5:

        new_row = {'ticker': security_code, 'value': returns['beta'][-1]}
        rank_file.loc[len(rank_file)] = new_row
        #rank_file['ticker'] = rank_file['ticker'].apply('="{}"'.format)
        rank_file.to_csv(rank_file_path+'positive_beta_rank.csv')
        
    rank_file = pd.read_csv(rank_file_path+'negative_beta_rank.csv').set_index('Unnamed: 0')
    if returns['beta'][-1] < 0.:

        new_row = {'ticker': security_code, 'value': returns['beta'][-1]}
        rank_file.loc[len(rank_file)] = new_row
        #rank_file['ticker'] = rank_file['ticker'].apply('="{}"'.format)
        rank_file.to_csv(rank_file_path+'negative_beta_rank.csv')
    
    
    return returns

def market_capture_ratio(returns, returns_daily, security_code, rank_file_path,input_file_path,rolling_window=250):
    """
    Function to calculate the upside and downside capture for a given set of returns.
    The function is set up so that the investment's returns are in the first column of the dataframe
    and the index returns are the second column.
    :param returns: pd.DataFrame of asset class returns
    :return: pd.DataFrame of market capture results
    """

    # initialize an empty dataframe to store the results
    df_mkt_capture = pd.DataFrame()

    # 1) Upside capture ratio
    # a) Isolate positive periods of the index
    up_market = returns[returns.iloc[:, -1] >= 0]

    # b) Geometrically link the returns
    up_linked_rets = ((1 + up_market).product(axis=0)) - 1

    # c) Calculate the ratio, multiply by 100 and round to 2 decimals to show in percent
    up_ratio = (up_linked_rets / up_linked_rets.iloc[-1] * 100).round(2)

    # 2) Downside capture ratio
    # a) Isolate negative periods of the index
    down_market = returns[returns.iloc[:, -1] < 0]

    # b) Geometrically link the returns
    down_linked_rets = ((1 + down_market).product(axis=0)) - 1

    # c) Calculate the ratio, multiply by 100 and round to 2 decimals to show in percent
    down_ratio = (down_linked_rets / down_linked_rets.iloc[-1] * 100).round(2)

    # 3) Combine to produce our final dataframe
    df_mkt_capture = pd.concat([up_ratio, down_ratio], axis=1)
    print (df_mkt_capture)
    comment_csv = pd.read_csv(input_file_path+'comments.csv').set_index('净值日期')
    df_mkt_capture.columns = ['Upside Capture', 'Downside Capture']
    if df_mkt_capture['Upside Capture'][0]>1 and df_mkt_capture['Downside Capture'][0]>1:
        if df_mkt_capture['Upside Capture'][0]-df_mkt_capture['Downside Capture'][0]>0:
            comment_csv.at[comment_csv.index[-1],'upside_capture_comments']  = "本基金在基准指数上行和下行的时候能经历了更大的波动，但在上行的时候取得的超额收益大于下行时候的超额亏损，表现整体高于了基准指数。"
            comment_csv.to_csv(input_file_path+'comments.csv')
            #print ("This fund moves more than the index. However, it is able to generate more gains in a up market than loss in a down market, makes it a better choice than the index. ")
            #print ("本基金在基准指数上行和下行的时候能经历了更大的波动，但在上行的时候取得的超额收益大于下行时候的超额亏损，表现整体高于了基准指数。")
        else:
            comment_csv.at[comment_csv.index[-1],'upside_capture_comments']  = "本基金在基准指数上行和下行的时候能经历了更大的波动，但在上行的时候取得的超额收益小于下行时候的超额亏损，表现整体弱于基准指数。"
            comment_csv.to_csv(input_file_path+'comments.csv')
            #print ("This fund moves more than the index, but it suffers more loss in a down market than gains in a up market, make the index a better choice. ")
            #print ("本基金在基准指数上行和下行的时候能经历了更大的波动，但在上行的时候取得的超额收益小于下行时候的超额亏损，表现整体弱于基准指数。")
    elif df_mkt_capture['Upside Capture'][0]>1 and df_mkt_capture['Downside Capture'][0]<1:
        comment_csv.at[comment_csv.index[-1],'upside_capture_comments']  = "本基金在基准指数上行的时候取得了更高的超额收益，但在基金指数下行的时候经历了较低的亏损，表现显著高于了基准指数。"
        comment_csv.to_csv(input_file_path+'comments.csv')
        #print ("This fund makes more money in a up market and loses less money in a down market. ")
        #print ("本基金在基准指数上行的时候取得了更高的超额收益，但在基金指数下行的时候经历了较低的亏损，表现显著高于了基准指数。")
    elif df_mkt_capture['Upside Capture'][0]<1 and df_mkt_capture['Downside Capture'][0]>1:
        comment_csv.at[comment_csv.index[-1],'upside_capture_comments']  = "本基金在基准指数上行的时候取得了更低的超额收益，但在基金指数下行的时候经历了更大的亏损，表现显著低于了基准指数。"
        comment_csv.to_csv(input_file_path+'comments.csv')
        #print ("This fund makes less money in a up market and loses more money in a down market. ")
        #print ("本基金在基准指数上行的时候取得了更低的超额收益，但在基金指数下行的时候经历了更大的亏损，表现显著低于了基准指数。")
    else:
        if df_mkt_capture['Upside Capture'][0]-df_mkt_capture['Downside Capture'][0]>0:
            comment_csv.at[comment_csv.index[-1],'upside_capture_comments']  = "本基金在基准指数上行和下行的时候能经历了更小的波动，但在上行的时候取得的超额收益大于下行时候的超额亏损，表现整体优于基准指数。"
            comment_csv.to_csv(input_file_path+'comments.csv')
            #print ("This fund moves less than the index. However, it is able to generate more gains in a up market than loss in a down market, makes it a better choice than the index.")
            #print ("本基金在基准指数上行和下行的时候能经历了更小的波动，但在上行的时候取得的超额收益大于下行时候的超额亏损，表现整体优于基准指数。")
        else:
            comment_csv.at[comment_csv.index[-1],'upside_capture_comments']  = "本基金在基准指数上行和下行的时候能经历了更小的波动，但在上行的时候取得的超额收益小于下行时候的超额亏损，表现整体弱于基准指数。"
            comment_csv.to_csv(input_file_path+'comments.csv')
            #print ("This fund moves less than the index, but it suffers more loss in a down market than gains in a up market, make the index a better choice. ")
            #print ("本基金在基准指数上行和下行的时候能经历了更小的波动，但在上行的时候取得的超额收益小于下行时候的超额亏损，表现整体弱于基准指数。")
    
    returns_daily['Upside_Capture_mean']=0
    returns_daily['Downside_Capture_mean']=0
    returns_daily['Upside_Capture']=0
    returns_daily['Downside_Capture']=0
    
    returns_daily['Upside_Capture_mean'] = df_mkt_capture['Upside Capture'][0]
    returns_daily['Downside_Capture_mean'] = df_mkt_capture['Downside Capture'][0]
    returns_daily_2 = returns_daily[['累计净值', 'comp_1']].pct_change()
    for i in range(len(returns_daily_2)):
        if i < rolling_window:
            pass
        returns_temp = returns_daily_2.iloc[i-rolling_window:i]
        up_market = returns_temp[returns_temp.iloc[:, -1] >= 0]

        # b) Geometrically link the returns
        up_linked_rets = ((1 + up_market).product(axis=0)) - 1

        # c) Calculate the ratio, multiply by 100 and round to 2 decimals to show in percent
        up_ratio = (up_linked_rets / up_linked_rets.iloc[-1] * 100).round(2)

        # 2) Downside capture ratio
        # a) Isolate negative periods of the index
        down_market = returns_temp[returns_temp.iloc[:, -1] < 0]

        # b) Geometrically link the returns
        down_linked_rets = ((1 + down_market).product(axis=0)) - 1

        # c) Calculate the ratio, multiply by 100 and round to 2 decimals to show in percent
        down_ratio = (down_linked_rets / down_linked_rets.iloc[-1] * 100).round(2)

        # 3) Combine to produce our final dataframe
        df_mkt_capture = pd.concat([up_ratio, down_ratio], axis=1)
        df_mkt_capture.columns = ['Upside Capture', 'Downside Capture']
        returns_daily['Upside_Capture'].iloc[i] = df_mkt_capture['Upside Capture'].iloc[0]
        returns_daily['Downside_Capture'].iloc[i] = df_mkt_capture['Downside Capture'].iloc[0]
    
    rank_file = pd.read_csv(rank_file_path+'upside_capture_rank.csv').set_index('Unnamed: 0')
    if returns_daily['Upside_Capture'][-1] > 30:

        new_row = {'ticker': security_code, 'value': returns_daily['Upside_Capture'][-1]}
        rank_file.loc[len(rank_file)] = new_row
        #rank_file['ticker'] = rank_file['ticker'].apply('="{}"'.format)
        rank_file.to_csv(rank_file_path+'upside_capture_rank.csv')
    
    
    rank_file = pd.read_csv(rank_file_path+'downside_capture_rank.csv').set_index('Unnamed: 0')
    if returns_daily['Downside_Capture'][-1] < 15:

        new_row = {'ticker': security_code, 'value': returns_daily['Downside_Capture'][-1]}
        rank_file.loc[len(rank_file)] = new_row
        #rank_file['ticker'] = rank_file['ticker'].apply('="{}"'.format)
        rank_file.to_csv(rank_file_path+'downside_capture_rank.csv')
            
    return returns_daily


def corr_analysis(returns,comp, security_code, rank_file_path, rank_file_path_2,input_file_path):
    security_code = str(security_code)
    
    comp[security_code] = returns['累计净值']
    corr_df = comp.corr(method='pearson')
    print (corr_df)
    #reset symbol as index (rather than 0-X)

    corr_df_2=corr_df.drop([security_code],axis=1)
    
    corr_df.head().reset_index()
    plt.figure(figsize=(13, 8))
    seaborn.heatmap(corr_df, annot=True, cmap='RdYlGn')
    plt.figure()
    corr_df = corr_df[security_code].drop(corr_df[security_code].idxmax())
    print (corr_df)
    comp_1_name = corr_df.idxmax()
    comp_2_name = corr_df.idxmin()

    if "510050.SS" in comp.columns:
        returns['index_peers']=0
        returns['index_peers'].iloc[-1] = corr_df_2.columns[np.argsort(-1*corr_df_2.tail(1).values,axis=1)[:, :3]]

        
    else:
        returns['industry_peers']=0
        returns['industry_peers'].iloc[-1] = corr_df_2.columns[np.argsort(-1*corr_df_2.tail(1).values,axis=1)[:, :3]]
        
    comment_csv = pd.read_csv(input_file_path+'comments.csv').set_index('净值日期')
    returns['positive_comp'] = 0
    returns['negative_comp'] = 0
    returns['benchmark_name'] = 0
    returns['positive_comp'] = returns['positive_comp'].astype(str)
    returns['negative_comp'] = returns['negative_comp'].astype(str)
    returns['benchmark_name'] = returns['benchmark_name'].astype(str)
    returns['benchmark_name_2'] = 0
    returns['benchmark_name_2'] = returns['benchmark_name_2'].astype(str)
    if corr_df[comp_1_name] > 0.9:
        ##save comp_1_name
        if comp_1_name=="510050.SS":
            returns.at[returns.index[-1],'benchmark_name'] = 'A50'
            comment_csv.at[comment_csv.index[-1],'index_comments']  = "本基金与A50有较强的相关性。"
            comment_csv.to_csv(input_file_path+'comments.csv')
            
            
            #print ("This etf correlates with A50")
            #print ("本基金与中证50（大盘股）有较强的相关性。")
            rank_file = pd.read_csv(rank_file_path_2+'A50.csv').set_index('Unnamed: 0')
            if corr_df[comp_1_name] > 0.9 and comp_1_name in comp.columns:

                new_row = {'ticker': security_code, 'value': corr_df[comp_1_name]}
                rank_file.loc[len(rank_file)] = new_row
                #rank_file['ticker'] = rank_file['ticker'].apply('="{}"'.format)
                rank_file.to_csv(rank_file_path_2+'A50.csv')
                
        elif comp_1_name=="159901.SZ":
            returns.at[returns.index[-1],'benchmark_name'] = '深圳100（深A大盘股）'
            comment_csv.at[comment_csv.index[-1],'index_comments']  = "本基金与深圳100（深A大盘股）有较强的相关性。"
            comment_csv.to_csv(input_file_path+'comments.csv')
            
            #print ("This etf correlates with Shenzhen 100")
            #print ("本基金与深圳100（深A大盘股）有较强的相关性。")
            rank_file = pd.read_csv(rank_file_path_2+'Shenzhen100.csv').set_index('Unnamed: 0')
            if corr_df[comp_1_name] > 0.9 and comp_1_name in comp.columns:

                new_row = {'ticker': security_code, 'value': corr_df[comp_1_name]}
                rank_file.loc[len(rank_file)] = new_row
                #rank_file['ticker'] = rank_file['ticker'].apply('="{}"'.format)
                rank_file.to_csv(rank_file_path_2+'Shenzhen100.csv')
            
            
        elif comp_1_name=="159949.SZ":
            #print ("This etf correlates with Chuangye 50")
            returns.at[returns.index[-1],'benchmark_name'] = '创业板'
            comment_csv.at[comment_csv.index[-1],'index_comments']  = "本基金与创业板有较强的相关性。"
            comment_csv.to_csv(input_file_path+'comments.csv')
            
            rank_file = pd.read_csv(rank_file_path_2+'Chuangye50.csv').set_index('Unnamed: 0')
            if corr_df[comp_1_name] > 0.9 and comp_1_name in comp.columns:

                new_row = {'ticker': security_code, 'value': corr_df[comp_1_name]}
                rank_file.loc[len(rank_file)] = new_row
                #rank_file['ticker'] = rank_file['ticker'].apply('="{}"'.format)
                rank_file.to_csv(rank_file_path_2+'Chuangye50.csv')
                
            #print ("本基金与创业板有较强的相关性。")
        elif comp_1_name=="510300.SS":
            #print ("This etf correlates with Hushen 300")
            returns.at[returns.index[-1],'benchmark_name'] = '沪深300'
            comment_csv.at[comment_csv.index[-1],'index_comments']  = "本基金与沪深300有较强的相关性。"
            comment_csv.to_csv(input_file_path+'comments.csv')
            rank_file = pd.read_csv(rank_file_path_2+'Hushen300.csv').set_index('Unnamed: 0')
            if corr_df[comp_1_name] > 0.9 and comp_1_name in comp.columns:

                new_row = {'ticker': security_code, 'value': corr_df[comp_1_name]}
                rank_file.loc[len(rank_file)] = new_row
                #rank_file['ticker'] = rank_file['ticker'].apply('="{}"'.format)
                rank_file.to_csv(rank_file_path_2+'Hushen300.csv')
            
            #print ("本基金与沪深300有较强的相关性。")
        elif comp_1_name=="510500.SS":
            #print ("This etf correlates with Zhongzheng 500")
            returns.at[returns.index[-1],'benchmark_name'] = '中证500（中盘股）'
            comment_csv.at[comment_csv.index[-1],'index_comments']  = "本基金与中证500（中盘股）有较强的相关性。"
            comment_csv.to_csv(input_file_path+'comments.csv')
            
            rank_file = pd.read_csv(rank_file_path_2+'Zhongzheng500.csv').set_index('Unnamed: 0')
            if corr_df[comp_1_name] > 0.9 and comp_1_name in comp.columns:

                new_row = {'ticker': security_code, 'value': corr_df[comp_1_name]}
                rank_file.loc[len(rank_file)] = new_row
                #rank_file['ticker'] = rank_file['ticker'].apply('="{}"'.format)
                rank_file.to_csv(rank_file_path_2+'Zhongzheng500.csv')
            
            #print ("本基金与中证500（中盘股）有较强的相关性。")
        elif comp_1_name=="512100.SS":
            #print ("This etf correlates with Zhongzheng 1000")
            returns.at[returns.index[-1],'benchmark_name'] = '中证1000（小盘股）'
            comment_csv.at[comment_csv.index[-1],'index_comments']  = "本基金与中证1000（小盘股）有较强的相关性。"
            comment_csv.to_csv(input_file_path+'comments.csv')
            rank_file = pd.read_csv(rank_file_path_2+'Zhongzheng1000.csv').set_index('Unnamed: 0')
            if corr_df[comp_1_name] > 0.9 and comp_1_name in comp.columns:

                new_row = {'ticker': security_code, 'value': corr_df[comp_1_name]}
                rank_file.loc[len(rank_file)] = new_row
                #rank_file['ticker'] = rank_file['ticker'].apply('="{}"'.format)
                rank_file.to_csv(rank_file_path_2+'Zhongzheng1000.csv')
            
            #print ("本基金与中证1000（小盘股）有较强的相关性。")
        elif comp_1_name=="588000.SS":
            #print ("This etf correlates with Kechuang 50")
            returns.at[returns.index[-1],'benchmark_name'] = '科创板'
            comment_csv.at[comment_csv.index[-1],'index_comments']  = "本基金与科创板有较强的相关性。"
            comment_csv.to_csv(input_file_path+'comments.csv')
            rank_file = pd.read_csv(rank_file_path_2+'Kechuang50.csv').set_index('Unnamed: 0')
            if corr_df[comp_1_name] > 0.9 and comp_1_name in comp.columns:

                new_row = {'ticker': security_code, 'value': corr_df[comp_1_name]}
                rank_file.loc[len(rank_file)] = new_row
                #rank_file['ticker'] = rank_file['ticker'].apply('="{}"'.format)
                rank_file.to_csv(rank_file_path_2+'Kechuang50.csv')
            
            #print ("本基金与科创板有较强的相关性。")
        elif comp_1_name=="510900.SS":
            print ("This etf correlates with Hang Seng Index")
            #print ("本基金与香港恒生指数有较强的相关性。")
            returns.at[returns.index[-1],'benchmark_name'] = '香港恒生指数'
            comment_csv.at[comment_csv.index[-1],'index_comments']  = "本基金与香港恒生指数有较强的相关性。"
            comment_csv.to_csv(input_file_path+'comments.csv')
            
            rank_file = pd.read_csv(rank_file_path_2+'Hangseng.csv').set_index('Unnamed: 0')
            if corr_df[comp_1_name] > 0.9 and comp_1_name in comp.columns:

                new_row = {'ticker': security_code, 'value': corr_df[comp_1_name]}
                rank_file.loc[len(rank_file)] = new_row
                #rank_file['ticker'] = rank_file['ticker'].apply('="{}"'.format)
                rank_file.to_csv(rank_file_path_2+'Hangseng.csv')
            
            
        elif comp_1_name=="510230.SS":
            #print ("This etf correlates with Finance Sector")
            #print ("本基金与金融板块有较强的相关性。")
            returns.at[returns.index[-1],'benchmark_name_2'] = '金融板块'
            comment_csv.at[comment_csv.index[-1],'industry_comments']  = "本基金与金融板块有较强的相关性。"
            comment_csv.to_csv(input_file_path+'comments.csv')
            
            rank_file = pd.read_csv(rank_file_path_2+'Finance.csv').set_index('Unnamed: 0')
            if corr_df[comp_1_name] > 0.9 and comp_1_name in comp.columns:

                new_row = {'ticker': security_code, 'value': corr_df[comp_1_name]}
                rank_file.loc[len(rank_file)] = new_row
                #rank_file['ticker'] = rank_file['ticker'].apply('="{}"'.format)
                rank_file.to_csv(rank_file_path_2+'Finance.csv')
            
            
        elif comp_1_name=="512010.SS":
            print ("This etf correlates with Pharmaceutical Sector")
            #print ("本基金与医药板块有较强的相关性。")
            returns.at[returns.index[-1],'benchmark_name_2'] = '医药板块'
            comment_csv.at[comment_csv.index[-1],'industry_comments']  = "本基金与医药板块有较强的相关性。"
            comment_csv.to_csv(input_file_path+'comments.csv')
            
            rank_file = pd.read_csv(rank_file_path_2+'Pharmaceutical.csv').set_index('Unnamed: 0')
            if corr_df[comp_1_name] > 0.9 and comp_1_name in comp.columns:

                new_row = {'ticker': security_code, 'value': corr_df[comp_1_name]}
                rank_file.loc[len(rank_file)] = new_row
                #rank_file['ticker'] = rank_file['ticker'].apply('="{}"'.format)
                rank_file.to_csv(rank_file_path_2+'Pharmaceutical.csv')
                
        elif comp_1_name=="512170.SS":
            #print ("This etf correlates with Healthcare Sector")
            #print ("本基金与医疗板块有较强的相关性。")
            returns.at[returns.index[-1],'benchmark_name_2'] = '医疗板块'
            comment_csv.at[comment_csv.index[-1],'industry_comments']  = "本基金与医疗板块有较强的相关性。"
            comment_csv.to_csv(input_file_path+'comments.csv')
            rank_file = pd.read_csv(rank_file_path_2+'Healthcare.csv').set_index('Unnamed: 0')
            if corr_df[comp_1_name] > 0.9 and comp_1_name in comp.columns:

                new_row = {'ticker': security_code, 'value': corr_df[comp_1_name]}
                rank_file.loc[len(rank_file)] = new_row
                #rank_file['ticker'] = rank_file['ticker'].apply('="{}"'.format)
                rank_file.to_csv(rank_file_path_2+'Healthcare.csv')
                
        elif comp_1_name=="515170.SS":
            #print ("This etf correlates with Food & Beverage Sector")
            #print ("本基金与食品饮料板块有较强的相关性。")
            returns.at[returns.index[-1],'benchmark_name_2'] = '食品饮料板块'
            comment_csv.at[comment_csv.index[-1],'industry_comments']  = "本基金与食品饮料板块有较强的相关性。"
            comment_csv.to_csv(input_file_path+'comments.csv')
            rank_file = pd.read_csv(rank_file_path_2+'FoodBeverage.csv').set_index('Unnamed: 0')
            if corr_df[comp_1_name] > 0.9 and comp_1_name in comp.columns:

                new_row = {'ticker': security_code, 'value': corr_df[comp_1_name]}
                rank_file.loc[len(rank_file)] = new_row
                #rank_file['ticker'] = rank_file['ticker'].apply('="{}"'.format)
                rank_file.to_csv(rank_file_path_2+'FoodBeverage.csv')
            
            
        elif comp_1_name=="516160.SS":
            #print ("This etf correlates with Energy Sector")
            #print ("本基金与能源板块有较强的相关性。")
            returns.at[returns.index[-1],'benchmark_name_2'] = '能源板块'
            comment_csv.at[comment_csv.index[-1],'industry_comments']  = "本基金与能源板块有较强的相关性。"
            comment_csv.to_csv(input_file_path+'comments.csv')
            rank_file = pd.read_csv(rank_file_path_2+'Energy.csv').set_index('Unnamed: 0')
            if corr_df[comp_1_name] > 0.9 and comp_1_name in comp.columns:

                new_row = {'ticker': security_code, 'value': corr_df[comp_1_name]}
                rank_file.loc[len(rank_file)] = new_row
                #rank_file['ticker'] = rank_file['ticker'].apply('="{}"'.format)
                rank_file.to_csv(rank_file_path_2+'Energy.csv')
            
            
        elif comp_1_name=="512480.SS":
            #print ("This etf correlates with Semiconductor")
            #print ("本基金与半导体板块有较强的相关性。")
            returns.at[returns.index[-1],'benchmark_name_2'] = '半导体板块'
            comment_csv.at[comment_csv.index[-1],'industry_comments']  = "本基金与半导体板块有较强的相关性。"
            comment_csv.to_csv(input_file_path+'comments.csv')
            rank_file = pd.read_csv(rank_file_path_2+'Semiconductor.csv').set_index('Unnamed: 0')
            if corr_df[comp_1_name] > 0.9 and comp_1_name in comp.columns:

                new_row = {'ticker': security_code, 'value': corr_df[comp_1_name]}
                rank_file.loc[len(rank_file)] = new_row
                #rank_file['ticker'] = rank_file['ticker'].apply('="{}"'.format)
                rank_file.to_csv(rank_file_path_2+'Semiconductor.csv')
            
        elif comp_1_name=="515230.SS":
            #print ("This etf correlates with Software")
            #print ("本基金与软件板块有较强的相关性。")
            returns.at[returns.index[-1],'benchmark_name_2'] = '软件板块'
            comment_csv.at[comment_csv.index[-1],'industry_comments']  = "本基金与软件板块有较强的相关性。"
            comment_csv.to_csv(input_file_path+'comments.csv')
            rank_file = pd.read_csv(rank_file_path_2+'Software.csv').set_index('Unnamed: 0')
            if corr_df[comp_1_name] > 0.9 and comp_1_name in comp.columns:

                new_row = {'ticker': security_code, 'value': corr_df[comp_1_name]}
                rank_file.loc[len(rank_file)] = new_row
                #rank_file['ticker'] = rank_file['ticker'].apply('="{}"'.format)
                rank_file.to_csv(rank_file_path_2+'Software.csv')
            
            
        elif comp_1_name=="512660.SS":
            #print ("This etf correlates with Military")
            #print ("本基金与军工板块有较强的相关性。")
            returns.at[returns.index[-1],'benchmark_name_2'] = '军工板块'
            comment_csv.at[comment_csv.index[-1],'industry_comments']  = "本基金与军工板块有较强的相关性。"
            comment_csv.to_csv(input_file_path+'comments.csv')
            rank_file = pd.read_csv(rank_file_path_2+'Military.csv').set_index('Unnamed: 0')
            if corr_df[comp_1_name] > 0.9 and comp_1_name in comp.columns:

                new_row = {'ticker': security_code, 'value': corr_df[comp_1_name]}
                rank_file.loc[len(rank_file)] = new_row
                #rank_file['ticker'] = rank_file['ticker'].apply('="{}"'.format)
                rank_file.to_csv(rank_file_path_2+'Military.csv')
            
        elif comp_1_name=="516220.SS":
            #print ("This etf correlates with Chemicals")
            #print ("本基金与化工板块有较强的相关性。")
            returns.at[returns.index[-1],'benchmark_name_2'] = '化工板块'
            comment_csv.at[comment_csv.index[-1],'industry_comments']  = "本基金与化工板块有较强的相关性。"
            comment_csv.to_csv(input_file_path+'comments.csv')
            rank_file = pd.read_csv(rank_file_path_2+'Chemicals.csv').set_index('Unnamed: 0')
            if corr_df[comp_1_name] > 0.9 and comp_1_name in comp.columns:

                new_row = {'ticker': security_code, 'value': corr_df[comp_1_name]}
                rank_file.loc[len(rank_file)] = new_row
                #rank_file['ticker'] = rank_file['ticker'].apply('="{}"'.format)
                rank_file.to_csv(rank_file_path_2+'Chemicals.csv')
            
            
        elif comp_1_name=="516800.SS":
            #print ("This etf correlates with Manufacturing")
            #print ("本基金与制造业板块有较强的相关性。")
            returns.at[returns.index[-1],'benchmark_name_2'] = '制造业板块'
            comment_csv.at[comment_csv.index[-1],'industry_comments']  = "本基金与制造业板块有较强的相关性。"
            comment_csv.to_csv(input_file_path+'comments.csv')
            rank_file = pd.read_csv(rank_file_path_2+'Manufacturing.csv').set_index('Unnamed: 0')
            if corr_df[comp_1_name] > 0.9 and comp_1_name in comp.columns:

                new_row = {'ticker': security_code, 'value': corr_df[comp_1_name]}
                rank_file.loc[len(rank_file)] = new_row
                #rank_file['ticker'] = rank_file['ticker'].apply('="{}"'.format)
                rank_file.to_csv(rank_file_path_2+'Manufacturing.csv')
                
            
        elif comp_1_name=="512400.SS":
            #print ("This etf correlates with Metal")
            #print ("本基金与有色金属板块有较强的相关性。")
            returns.at[returns.index[-1],'benchmark_name_2'] = '有色金属板块'
            comment_csv.at[comment_csv.index[-1],'industry_comments']  = "本基金与有色金属板块有较强的相关性。"
            comment_csv.to_csv(input_file_path+'comments.csv')
            rank_file = pd.read_csv(rank_file_path_2+'Metal.csv').set_index('Unnamed: 0')
            if corr_df[comp_1_name] > 0.9 and comp_1_name in comp.columns:

                new_row = {'ticker': security_code, 'value': corr_df[comp_1_name]}
                rank_file.loc[len(rank_file)] = new_row
                #rank_file['ticker'] = rank_file['ticker'].apply('="{}"'.format)
                rank_file.to_csv(rank_file_path_2+'Metal.csv')
            
            
        elif comp_1_name=="159825.SZ":
            #print ("This etf correlates with Agriculture")
            #print ("本基金与农业板块有较强的相关性。")
            returns.at[returns.index[-1],'benchmark_name_2'] = '农业板块'
            comment_csv.at[comment_csv.index[-1],'industry_comments']  = "本基金与农业板块有较强的相关性。"
            comment_csv.to_csv(input_file_path+'comments.csv')
            rank_file = pd.read_csv(rank_file_path_2+'Agriculture.csv').set_index('Unnamed: 0')
            if corr_df[comp_1_name] > 0.9 and comp_1_name in comp.columns:

                new_row = {'ticker': security_code, 'value': corr_df[comp_1_name]}
                rank_file.loc[len(rank_file)] = new_row
                #rank_file['ticker'] = rank_file['ticker'].apply('="{}"'.format)
                rank_file.to_csv(rank_file_path_2+'Agriculture.csv')
                
                
        elif comp_1_name=="516950.SS":
            #print ("This etf correlates with Infrastructure")
            returns.at[returns.index[-1],'benchmark_name_2'] = '基建板块'
            comment_csv.at[comment_csv.index[-1],'industry_comments']  = "本基金与基建板块有较强的相关性。"
            comment_csv.to_csv(input_file_path+'comments.csv')
            #print ("本基金与基建板块有较强的相关性。")
            rank_file = pd.read_csv(rank_file_path_2+'Infrastructure.csv').set_index('Unnamed: 0')
            if corr_df[comp_1_name] > 0.9 and comp_1_name in comp.columns:

                new_row = {'ticker': security_code, 'value': corr_df[comp_1_name]}
                rank_file.loc[len(rank_file)] = new_row
                #rank_file['ticker'] = rank_file['ticker'].apply('="{}"'.format)
                rank_file.to_csv(rank_file_path_2+'Infrastructure.csv')
            
        elif comp_1_name=="516070.SS":
            #print ("This etf correlates with Environmental")
            returns.at[returns.index[-1],'benchmark_name_2'] = '环保板块'
            comment_csv.at[comment_csv.index[-1],'industry_comments']  = "本基金与环保板块有较强的相关性。"
            comment_csv.to_csv(input_file_path+'comments.csv')
            #print ("本基金与环保板块有较强的相关性。")
            rank_file = pd.read_csv(rank_file_path_2+'Environmental.csv').set_index('Unnamed: 0')
            if corr_df[comp_1_name] > 0.9 and comp_1_name in comp.columns:

                new_row = {'ticker': security_code, 'value': corr_df[comp_1_name]}
                rank_file.loc[len(rank_file)] = new_row
                #rank_file['ticker'] = rank_file['ticker'].apply('="{}"'.format)
                rank_file.to_csv(rank_file_path_2+'Environmental.csv')
            
            
    if corr_df[comp_2_name] < -0.9:
        ##save comp_2_name
        if comp_1_name=="510050.SS":
            print ("This etf negatively correlates with A50")
            #print ("本基金与中证50（大盘股）有较强的负相关性。")
        elif comp_1_name=="159901.SZ":
            print ("This etf negatively correlates with Shenzhen 100")
            #print ("本基金与深圳100（深A大盘股）有较强的负相关性。")
        elif comp_1_name=="159949.SZ":
            print ("This etf negatively correlates with Chuangye 50")
            #print ("本基金与创业板有较强的负相关性。")
        elif comp_1_name=="510500.SS":
            print ("This etf negatively correlates with Hushen 300")
            #print ("本基金与沪深300有较强的负相关性。")
        elif comp_1_name=="512100.SS":
            print ("This etf negatively correlates with Zhongzheng 500")
            #print ("本基金与中证500（中盘股）有较强的负相关性。")
        elif comp_1_name=="512100.SS":
            print ("This etf negatively correlates with Zhongzheng 1000")
            #print ("本基金与中证1000（小盘股）有较强的负相关性。")
        elif comp_1_name=="512100.SS":
            print ("This etf negatively correlates with Kechuang 50")
            #print ("本基金与科创板有较强的负相关性。")
        elif comp_1_name=="510900.SS":
            print ("This etf negatively correlates with Hang Seng Index")
            #print ("本基金与香港恒生指数有较强的负相关性。")
            
        elif comp_1_name=="510230.SS":
            print ("This etf negatively correlates with Finance Sector")
            #print ("本基金与金融板块有较强的负相关性。")
        elif comp_1_name=="512010.SS":
            print ("This etf negatively correlates with Pharmaceutical Sector")
            #print ("本基金与医药板块有较强的负相关性。")
        elif comp_1_name=="512170.SS":
            print ("This etf negatively correlates with Healthcare Sector")
            #print ("本基金与医疗板块有较强的负相关性。")
        elif comp_1_name=="515170.SS":
            print ("This etf negatively correlates with Food & Beverage Sector")
            #print ("本基金与食品饮料板块有较强的负相关性。")
        elif comp_1_name=="516160.SS":
            print ("This etf negatively correlates with Energy Sector")
            #print ("本基金与能源板块有较强的负相关性。")
        elif comp_1_name=="512480.SS":
            print ("This etf negatively correlates with Semiconductor")
            #print ("本基金与半导体板块有较强的负相关性。")
        elif comp_1_name=="515230.SS":
            print ("This etf negatively correlates with Software")
            #print ("本基金与软件板块有较强的相关性。")
        elif comp_1_name=="512660.SS":
            print ("This etf negatively correlates with Military")
            #print ("本基金与军工板块有较强的负相关性。")
        elif comp_1_name=="516220.SS":
            print ("This etf negatively correlates with Chemicals")
            #print ("本基金与化工板块有较强的负相关性。")
        elif comp_1_name=="516800.SS":
            print ("This etf negatively correlates with Manufacturing")
            #print ("本基金与制造业板块有较强的负相关性。")
        elif comp_1_name=="512400.SS":
            print ("This etf negatively correlates with Metal")
            #print ("本基金与有色金属板块有较强的负相关性。")
        elif comp_1_name=="159825.SZ":
            print ("This etf negatively correlates with Agriculture")
            #print ("本基金与农业板块有较强的负相关性。")
        elif comp_1_name=="516950.SS":
            print ("This etf negatively correlates with Infrastructure")
            #print ("本基金与基建板块有较强的负相关性。")
        elif comp_1_name=="516070.SS":
            print ("This etf negatively correlates with Environmental")
            #print ("本基金与环保板块有较强的负相关性。")
        
    else:
        print ("No clear correlation")
        #print ("本基金投资风格较多元。")
    returns['positive_comp'][-1] = comp_1_name
    returns['negative_comp'][-1] = comp_2_name
    print (returns['negative_comp'][-1])
    #print (returns['negative_comp'][-1])

    
    return comp_1_name,comp_2_name, returns
        



def rolling_volatility(returns, comp, rank_file_path,security_code,input_file_path,rolling_vol_window=250):
    """
    Determines the rolling volatility of a strategy.

    Parameters
    ----------
    returns : pd.Series
        Daily returns of the strategy, noncumulative.
         - See full explanation in tears.create_full_tear_sheet.
    rolling_vol_window : int
        Length of rolling window, in days, over which to compute.

    Returns
    -------
    pd.Series
        Rolling volatility.
    """

    comp = comp.pct_change()

    returns['vol'] = returns['return'].rolling(rolling_vol_window).std() \
        * np.sqrt(250)
    returns['excess_vol'] = returns['excess_return'].rolling(rolling_vol_window).std() \
        * np.sqrt(250)
    returns['comp_vol'] = comp.rolling(rolling_vol_window).std() \
        * np.sqrt(250)
    comment_csv = pd.read_csv(input_file_path+'comments.csv').set_index('净值日期')
    if returns['vol'].mean() > 1.2*returns['comp_vol'].mean():
        comment_csv.at[comment_csv.index[-1],'volatility_comments']  = "本基金的波动率显著高于基准指数。"
        comment_csv.to_csv(input_file_path+'comments.csv')
        
        #print ('The fund is more volatile than index.')
        #print ("本基金的波动率显著高于基准指数。")
    elif returns['vol'].mean() < 0.8*returns['comp_vol'].mean():
        comment_csv.at[comment_csv.index[-1],'volatility_comments']  = "本基金的波动率显著低于基准指数。"
        comment_csv.to_csv(input_file_path+'comments.csv')
        #print ('The fund is less volatile than index.')
        #print ("本基金的波动率显著低于基准指数。")
    else:
        comment_csv.at[comment_csv.index[-1],'volatility_comments']  = "本基金的波动率与基准指数基本一致。"
        comment_csv.to_csv(input_file_path+'comments.csv')
        #print ('The fund has similar volatility to the index. ')
        #print ("本基金的波动率与基准指数基本一致。")
    comment_csv = pd.read_csv(input_file_path+'comments.csv').set_index('净值日期')
    if returns['vol'][-1]>1.2*returns['vol'].mean():
        comment_csv.at[comment_csv.index[-1],'volatility_comments']  += "本基金的波动率近期有明显上升。"
        comment_csv.to_csv(input_file_path+'comments.csv')
        #print ('The fund has become more volatile recently')
        #print ("本基金的波动率近期有明显上升。")
    elif returns['vol'][-1]<0.8*returns['vol'].mean():
        comment_csv.at[comment_csv.index[-1],'volatility_comments']  += "本基金的波动率近期有明显下降。"
        comment_csv.to_csv(input_file_path+'comments.csv')
        #print ('The fund has become less volatile recently')
        #print ("本基金的波动率近期有明显下降。")
    else:
        comment_csv.at[comment_csv.index[-1],'volatility_comments']  += "本基金的波动率近期较为稳定。"
        comment_csv.to_csv(input_file_path+'comments.csv')
        #print ('The volatility has been consistent recently')
        #print ("本基金的波动率近期较为稳定。")
    
    rank_file = pd.read_csv(rank_file_path+'volatility_rank.csv').set_index('Unnamed: 0')
    if returns['vol'][-1] < 0.1:

        new_row = {'ticker': security_code, 'value': returns['vol'][-1]}
        rank_file.loc[len(rank_file)] = new_row
        #rank_file['ticker'] = rank_file['ticker'].apply('="{}"'.format)
        rank_file.to_csv(rank_file_path+'volatility_rank.csv')
        
        
    return returns


def plot_drawdown_underwater(returns):
    """
    Plots how far underwaterr returns are over time, or plots current
    drawdown vs. date.

    Parameters
    ----------
    returns : pd.Series
        Daily returns of the strategy, noncumulative.
         - See full explanation in tears.create_full_tear_sheet.
    ax : matplotlib.Axes, optional
        Axes upon which to plot.
    **kwargs, optional
        Passed to plotting function.

    Returns
    -------
    ax : matplotlib.Axes
        The axes that were plotted on.
    """

    #if ax is None:
    #    ax = plt.gca()

    #y_axis_formatter = FuncFormatter(utils.percentage)
    #ax.yaxis.set_major_formatter(FuncFormatter(y_axis_formatter))
    returns['underwater']=0
    returns['underwater'] = returns['underwater'].astype('float64')
    df_cum_rets = ep.cum_returns(returns['return'], starting_value=1.0)
    running_max = np.maximum.accumulate(df_cum_rets)
    returns['underwater'] = -100 * ((running_max - df_cum_rets) / running_max)
    #(returns['underwater']).plot(ax=ax, kind='area', color='coral', alpha=0.7, **kwargs)
    #ax.set_ylabel('Drawdown')
    #ax.set_title('Underwater plot')
    #ax.set_xlabel('')
    return returns
