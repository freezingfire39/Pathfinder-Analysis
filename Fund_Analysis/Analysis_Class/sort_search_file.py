import os,sys
import numpy as np
import pandas as pd
import datetime
# from airflow.exceptions import AirflowException
from pathlib import Path
home = str(Path.home())
import pytz
from itertools import islice
import subprocess
def get_all_files(input_file_path):
    print("input file path:", input_file_path)
    csv_files = []
    for filename in os.listdir(input_file_path):
        if filename.endswith('.csv') and 'benchmark' not in filename:
            csv_files.append(filename)
    return csv_files
def main(input_file_path):
    csv_files = get_all_files(input_file_path)
    for filename in csv_files:
        filepath = os.path.join(input_file_path, filename)
        df = pd.read_csv(filepath)
        if 'drawdown_duration' in filename or 'drawdown_amount' in filename or 'volatility' in filename:
            # sorting ascending
            sorted_df = df.sort_values(by='value', ascending=True)
        else:
            # sorting decending
            sorted_df = df.sort_values(by='value', ascending=False)
        sorted_df.to_csv(filepath, index=False)
if __name__ == '__main__':
    input_file_path = home + '/Desktop/output_search'
    # output_file_path = home + '/Desktop/output_china'
    try:
        main(input_file_path)
    except Exception as e:
        raise Exception("fail to run at error ", e)