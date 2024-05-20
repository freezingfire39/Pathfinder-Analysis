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

def rolling_sharpe(returns, risk_free_rate=0.0, window=60):

    returns['rolling_SR'] = returns['return'].rolling(window).apply(lambda x: (x.mean() - risk_free_rate) / x.std(), raw = True)
    returns['rolling_SR'].plot()
    if returns['rolling_SR'][-1] < (returns['return'].mean()/returns['return'].std())-0.1:
        print ("This fund's has performed below its historical average in the last 6 months.")
    elif returns['rolling_SR'][-1] > (returns['return'].mean()/returns['return'].std())+0.1:
        print ("This fund's has performed below its historical average in the last 6 months.")
    else:
        print ("This fund's has performed inline with its historical average in the last 6 months.")
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


def gen_drawdown_table(returns, top=10):
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
    
    returns['drawdown_duration'] = 0
    returns['drawdown_amount'] = 0
    returns['drawdown_duration'] = returns['drawdown_duration'].astype(int)
    returns['drawdown_amount'] = returns['drawdown_amount'].astype(int)
    print (df_drawdowns['Duration'].max())
    returns['drawdown_duration'][-1] = df_drawdowns['Duration'].max()
    returns['drawdown_amount'][-1] = df_drawdowns['Net drawdown in %'].max()
    print (returns.tail(10))
    if df_drawdowns['Duration'].mean()>300:
        print ("compare to industry average, this security has longer drawdowns")

    return returns
    
def max_drawdown_analysis(returns):
    returns = gen_drawdown_table(returns)
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

def alpha_beta_analysis(returns, comp, window=90):

    returns['alpha'] = 0
    returns['alpha'] = returns['alpha'].astype('float64')
    returns['beta'] = 0
    returns['beta'] = returns['beta'].astype('float64')
    comp.dropna(inplace=True)
    df_drop=[]
    for i in returns.index:
        if i not in comp.index:
            df_drop.append(i)
    returns = returns.drop(df_drop, axis=0)


    df_drop=[]
    for i in comp.index:
        if i not in returns.index:
            df_drop.append(i)
    comp = comp.drop(df_drop, axis=0)
    comp = comp.pct_change()

    for i in range(len(returns)):
        if i<window:
            pass
        else:
        
            df_temp_1 = returns.iloc[i-window:i]
            df_temp_2 = comp.iloc[i-window:i]

            (beta, alpha) = stats.linregress(df_temp_2, df_temp_1['return'])[0:2]
            returns['alpha'][i]=alpha
            returns['beta'][i]=beta
            
    returns['alpha'].plot()
    returns['beta'].plot()
    
    if returns['alpha'][-1]>0.1:
        print ("This fund has outperformed the benchmark")
    else:
        print ("This fund has not outperformed the benchmark")
    
    
    return returns

def market_capture_ratio(returns, returns_daily, rolling_window=90):
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

    df_mkt_capture.columns = ['Upside Capture', 'Downside Capture']
    if df_mkt_capture['Upside Capture'][0]>1 and df_mkt_capture['Downside Capture'][0]>1:
        if df_mkt_capture['Upside Capture'][0]-df_mkt_capture['Upside Capture'][0]>0:
            print ("This fund moves more than the index. However, it is able to generate more gains in a up market than loss in a down market, makes it a better choice than the index. ")
        else:
            print ("This fund moves more than the index, but it suffers more loss in a down market than gains in a up market, make the index a better choice. ")
    elif df_mkt_capture['Upside Capture'][0]>1 and df_mkt_capture['Downside Capture'][0]<1:
        print ("This fund makes more money in a up market and loses less money in a down market. ")
    elif df_mkt_capture['Upside Capture'][0]<1 and df_mkt_capture['Downside Capture'][0]>1:
        print ("This fund makes less money in a up market and loses more money in a down market. ")
    else:
        if df_mkt_capture['Upside Capture'][0]-df_mkt_capture['Upside Capture'][0]>0:
            print ("This fund moves less than the index. However, it is able to generate more gains in a up market than loss in a down market, makes it a better choice than the index.")
        else:
            print ("This fund moves less than the index, but it suffers more loss in a down market than gains in a up market, make the index a better choice. ")
    
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
        returns_daily['Upside_Capture'][i] = df_mkt_capture['Upside Capture'][0]
        returns_daily['Downside_Capture'][i] = df_mkt_capture['Downside Capture'][0]
    
    
    
    
    
    return returns_daily


def corr_analysis(returns,comp, security_code):
    comp[security_code] = returns['累计净值']
    corr_df = comp.corr(method='pearson')
    corr_df_2=corr_df.drop([security_code],axis=1)
    if "510050.SS" in comp.columns:
        returns['index_peers']=0
        returns['index_peers'][-1] = corr_df_2.columns[np.argsort(-1*corr_df_2.tail(1).values,axis=1)[:, :3]]
    else:
        returns['industry_peers']=0
        returns['industry_peers'][-1] = corr_df_2.columns[np.argsort(-1*corr_df_2.tail(1).values,axis=1)[:, :3]]
    #reset symbol as index (rather than 0-X)
    corr_df.head().reset_index()
    plt.figure(figsize=(13, 8))
    seaborn.heatmap(corr_df, annot=True, cmap='RdYlGn')
    plt.figure()
    corr_df = corr_df[security_code].drop(corr_df[security_code].idxmax())
    print (corr_df)

    comp_1_name = corr_df.idxmax()
    comp_2_name = corr_df.idxmin()
    returns['positive_comp'] = 0
    returns['negative_comp'] = 0
    returns['positive_comp'] = returns['positive_comp'].astype(str)
    returns['negative_comp'] = returns['negative_comp'].astype(str)
    if corr_df[comp_1_name] > 0.8:
        ##save comp_1_name
        if comp_1_name=="510050.SS":
            print ("This etf correlates with A50")
        elif comp_1_name=="159901.SZ":
            print ("This etf correlates with Shenzhen 100")
        elif comp_1_name=="159949.SZ":
            print ("This etf correlates with Chuangye 50")
        elif comp_1_name=="510300.SS":
            print ("This etf correlates with Hushen 300")
        elif comp_1_name=="510500.SS":
            print ("This etf correlates with Zhongzheng 500")
        elif comp_1_name=="512100.SS":
            print ("This etf correlates with Zhongzheng 1000")
        elif comp_1_name=="588000.SS":
            print ("This etf correlates with Kechuang 50")
        elif comp_1_name=="510900.SS":
            print ("This etf correlates with Hang Seng Index")
            
        elif comp_1_name=="510230.SS":
            print ("This etf correlates with Finance Sector")
        elif comp_1_name=="512010.SS":
            print ("This etf correlates with Pharmaceutical Sector")
        elif comp_1_name=="512170.SS":
            print ("This etf correlates with Healthcare Sector")
        elif comp_1_name=="515170.SS":
            print ("This etf correlates with Food & Beverage Sector")
        elif comp_1_name=="516160.SS":
            print ("This etf correlates with Energy Sector")
        elif comp_1_name=="512480.SS":
            print ("This etf correlates with Semiconductor")
        elif comp_1_name=="515230.SS":
            print ("This etf correlates with Software")
        elif comp_1_name=="512660.SS":
            print ("This etf correlates with Military")
        elif comp_1_name=="516220.SS":
            print ("This etf correlates with Chemicals")
        elif comp_1_name=="516800.SS":
            print ("This etf correlates with Manufacturing")
        elif comp_1_name=="512400.SS":
            print ("This etf correlates with Metal")
        elif comp_1_name=="159825.SZ":
            print ("This etf correlates with Agriculture")
        elif comp_1_name=="516950.SS":
            print ("This etf correlates with Infrastructure")
        elif comp_1_name=="516070.SS":
            print ("This etf correlates with Environmental")
    if corr_df[comp_2_name] < -0.8:
        ##save comp_2_name
        if comp_1_name=="510050.SS":
            print ("This etf negatively correlates with A50")
        elif comp_1_name=="159901.SZ":
            print ("This etf negatively correlates with Shenzhen 100")
        elif comp_1_name=="159949.SZ":
            print ("This etf negatively correlates with Chuangye 50")
        elif comp_1_name=="510500.SS":
            print ("This etf negatively correlates with Hushen 300")
        elif comp_1_name=="512100.SS":
            print ("This etf negatively correlates with Zhongzheng 500")
        elif comp_1_name=="512100.SS":
            print ("This etf negatively correlates with Zhongzheng 1000")
        elif comp_1_name=="512100.SS":
            print ("This etf negatively correlates with Kechuang 50")
        elif comp_1_name=="510900.SS":
            print ("This etf negatively correlates with Hang Seng Index")
            
        elif comp_1_name=="510230.SS":
            print ("This etf negatively correlates with Finance Sector")
        elif comp_1_name=="512010.SS":
            print ("This etf negatively correlates with Pharmaceutical Sector")
        elif comp_1_name=="512170.SS":
            print ("This etf negatively correlates with Healthcare Sector")
        elif comp_1_name=="515170.SS":
            print ("This etf negatively correlates with Food & Beverage Sector")
        elif comp_1_name=="516160.SS":
            print ("This etf negatively correlates with Energy Sector")
        elif comp_1_name=="512480.SS":
            print ("This etf negatively correlates with Semiconductor")
        elif comp_1_name=="515230.SS":
            print ("This etf negatively correlates with Software")
        elif comp_1_name=="512660.SS":
            print ("This etf negatively correlates with Military")
        elif comp_1_name=="516220.SS":
            print ("This etf negatively correlates with Chemicals")
        elif comp_1_name=="516800.SS":
            print ("This etf negatively correlates with Manufacturing")
        elif comp_1_name=="512400.SS":
            print ("This etf negatively correlates with Metal")
        elif comp_1_name=="159825.SZ":
            print ("This etf negatively correlates with Agriculture")
        elif comp_1_name=="516950.SS":
            print ("This etf negatively correlates with Infrastructure")
        elif comp_1_name=="516070.SS":
            print ("This etf negatively correlates with Environmental")
        
    else:
        print ("No clear correlation")
    returns['positive_comp'][-1] = comp_1_name
    returns['negative_comp'][-1] = comp_2_name
    print (returns['negative_comp'][-1])
    #print (returns['negative_comp'][-1])

    
    return comp_1_name,comp_2_name, returns
        



def rolling_volatility(returns, comp, rolling_vol_window=90):
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
    
    df_drop=[]
    for i in returns.index:
        if i not in comp.index:
            df_drop.append(i)
    returns = returns.drop(df_drop, axis=0)


    df_drop=[]
    for i in comp.index:
        if i not in returns.index:
            df_drop.append(i)
    comp = comp.drop(df_drop, axis=0)
    comp = comp.pct_change()
    returns['vol'] = returns['return'].rolling(rolling_vol_window).std() \
        * np.sqrt(250)
    returns['comp_vol'] = comp.rolling(rolling_vol_window).std() \
        * np.sqrt(250)
    if returns['vol'].mean() > 1.2*returns['comp_vol'].mean():
        print ('The fund is more volatile than index.')
    elif returns['vol'].mean() < 0.8*returns['comp_vol'].mean():
        print ('The fund is less volatile than index.')
    else:
        print ('The fund has similar volatility to the index. ')
        
    if returns['vol'][-1]>1.2*returns['vol'].mean():
        print ('The fund has become more volatile recently')
    elif returns['vol'][-1]<0.8*returns['vol'].mean():
        print ('The fund has become less volatile recently')
    else:
        print ('The volatility has been consistent recently')
    

    return returns
