import tushare as ts
import pandas as pd
from datetime import datetime
import pendulum
from airflow import DAG
from airflow.decorators import task


default_args = {
    'owner': 'zgao',
    'depends_on_past': False,
    'retries': 3
}
local_tz = pendulum.timezone("America/New_York")# New York timezone

@task(task_id='timing')
def timing():
    pro = ts.pro_api('84be1015becc0b9dbbab507552c328cbf447bc02cbd29cfa09029bc6')

    df = pro.moneyflow_mkt_dc(start_date='20190115', end_date='20251215').set_index('trade_date')
    df = df.iloc[::-1]
    df.index = pd.to_datetime(df.index)

    print(df.head(20))

    df_2 = pro.index_daily(ts_code='399300.SZ', start_date='20190115', end_date='20251215').set_index('trade_date')
    df_2 = df_2.iloc[::-1]
    df_2.index = pd.to_datetime(df_2.index)

    print(df_2)

    df_drop = []
    for i in df.index:
        if i not in df_2.index:
            df_drop.append(i)
    df = df.drop(df_drop, axis=0)

    df_drop = []
    for i in df_2.index:
        if i not in df.index:
            df_drop.append(i)
    df_2 = df_2.drop(df_drop, axis=0)

    df['gap'] = (df['buy_elg_amount_rate'] - df['net_amount_rate'])

    df['gap'].plot()

    df['zscore'] = (df['gap'] - df['gap'].rolling(10).mean()) / df['gap'].rolling(10).std(ddof=0)

    df['trade'] = 0
    df['trade'] = df['trade'].astype('float64')
    for i in range(len(df)):
        if i < 1:
            continue

        if df['zscore'][i - 2] <= -0.8 and df['zscore'][i - 2] >= -2.6:
            df['trade'][i:i + 1] = 1


        elif df['zscore'][i - 2] >= 0.8 and df['zscore'][i - 2] <= 2.6:
            df['trade'][i:i + 2] = -1

    df['full_return'] = df['trade'] * (df_2['open'].pct_change())
    df.to_csv("/home/app/Desktop/default_portfolio/timing.csv")

with DAG(
    dag_id='timing_portfolio',
    start_date=datetime(2020, 1, 1, tzinfo=local_tz),
    catchup=False,
    default_args=default_args,
) as dag:
    timing = timing()

    timing
