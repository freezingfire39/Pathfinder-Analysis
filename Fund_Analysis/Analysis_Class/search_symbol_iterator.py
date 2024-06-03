import os,sys
import numpy as np
import pandas as pd
import datetime
from airflow.exceptions import AirflowException
from pathlib import Path
home = str(Path.home())
import pytz

def readBackground(symbol_file_path):
    print ("start reading file path:", symbol_file_path)
    try:
        background_csv = pd.read_csv(symbol_file_path + '/Background.csv')
    except:
        print ("fail to read background.csv file. skip this file")
        return 0
    type = background_csv['基金类型'].iloc[0]
    print ("type:", type)

def main(start_symbol, end_symbol, input_file_path):
    # iterator from [start_symbol to end_symbol]
    # read Background.csv column 基金类型
    # 货币型(test_2_money_market)，债券型(test_3_bonds)， 指数型 - 海外股票 / QDII(test_4_overseas), else (test.py)
    for i in range(start_symbol, (end_symbol+1)):
        formatted_number = f"{i:06}"  # Formats the number as a string with leading zeros up to 6 digits
        # print(formatted_number)
        symbol_file_path = input_file_path + "/" + formatted_number
        # print (symbol_file_path)
        readBackground(symbol_file_path)


if __name__ == '__main__':
    input_file_path = home + '/Desktop/output_china'
    # output_file_path = home + '/Desktop/output_china'
    try:
        start_symbol = int(sys.argv[1])
        end_symbol = int(sys.argv[2])
        main(start_symbol, end_symbol, input_file_path)
    except Exception as e:
        raise AirflowException("fail to run at error ", e)