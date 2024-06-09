import os,sys
import numpy as np
import pandas as pd
import datetime
from airflow.exceptions import AirflowException
from pathlib import Path
home = str(Path.home())
import pytz
import subprocess
import logging
logging.basicConfig(
    filename=home + '/Desktop/error.log',  # Log file path
    filemode='a',  # 'a' means append (add to the existing file), 'w' would overwrite the file each time
    level=logging.ERROR,  # Logging level set to ERROR
    format='%(asctime)s - %(levelname)s - %(message)s',  # Includes timestamp, log level, and message
    datefmt='%Y-%m-%d %H:%M:%S'  # Timestamp format
)

def readBackground(symbol_file_path):
    print ("start reading file path:", symbol_file_path)
    try:
        background_csv = pd.read_csv(symbol_file_path + '/Background.csv')
    except:
        print ("fail to read background.csv file. skip this file")
        return 0
    try:
        type = background_csv['基金类型'].iloc[0]
        print ("type:", type)
        if "货币型" in type:
            return 1
        elif "债券型" in type:
            return 2
        elif "指数型" in type or "QDII" in type:
            return 3
        else:# "混合型"
            return 4
    except:
        logging.error("Faild to read file path: %s",symbol_file_path)
        return 0

def trigger_python_script(script_path, params):
    print ("trigger: " + script_path + " " + params)
    result = subprocess.run(['python', script_path, params], text=True, capture_output=True)
    print("Standard Output:")
    print(result.stdout)
    print("Standard Error:")
    print(result.stderr)
    if result.returncode == 0:
        print ("job succeed, " + script_path + " " + params)
    else:
        print (f"Error in running the script. Return code: {result.returncode}, script: {script_path} {params} ")

# "货币型"  1 test_2_money_market
def trigger_test_2_money_market(formatted_number):
    trigger_python_script(home + '/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/test_2_money_market.py', formatted_number)
    pass
# "债券型" 2 test_3_bonds
def trigger_test_3_bonds(formatted_number):
    trigger_python_script(home + '/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/test_3_bonds.py', formatted_number)
    pass
# "指数型" or "QDII" 3 run test_4_overseas
def trigger_test_4_overseas(formatted_number):
    trigger_python_script(home + '/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/test_4_overseas.py', formatted_number)
    pass
# "混合型" 4 run test.py
def trigger_test(formatted_number):
    trigger_python_script(home + '/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/test.py',formatted_number)
    pass
def main(start_symbol, end_symbol, input_file_path):
    # iterator from [start_symbol to end_symbol]
    # read Background.csv column 基金类型
    # 货币型(test_2_money_market)，债券型(test_3_bonds)， 指数型 - 海外股票 / QDII(test_4_overseas), else (test.py)
    for i in range(start_symbol, (end_symbol+1)):
        formatted_number = f"{i:06}"  # Formats the number as a string with leading zeros up to 6 digits
        # print(formatted_number)
        symbol_file_path = input_file_path + "/" + formatted_number
        # print (symbol_file_path)
        type = readBackground(symbol_file_path)
        print("type number:", type)
        if type == 0:
            continue
        elif type == 1:
            trigger_test_2_money_market(formatted_number)
        elif type == 2:
            trigger_test_3_bonds(formatted_number)
        elif type == 3:
            trigger_test_4_overseas(formatted_number)
        else:
            trigger_test(formatted_number)


if __name__ == '__main__':
    input_file_path = home + '/Desktop/output_china'
    # output_file_path = home + '/Desktop/output_china'
    try:
        start_symbol = int(sys.argv[1])
        end_symbol = int(sys.argv[2])
        main(start_symbol, end_symbol, input_file_path)
    except Exception as e:
        raise AirflowException("fail to run at error ", e)