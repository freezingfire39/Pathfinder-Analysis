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
import logging4

logger = logging4.Logger(name="MyLogger")
formatter = '[[time]] - [[name]] - [[level_name]] - [[msg]]'
# add/del channel
# logger.add_channel(filename='log.txt', level=logging4.WARNING)
# logger.add_channel(filename=sys.stdout, level=logging4.ERROR, formatter=formatter)
logger.add_channel(filename=home + '/Desktop/info.log', level=logging4.INFO, formatter=formatter)
logger.add_channel(filename=home + '/Desktop/error.log', level=logging4.ERROR, formatter=formatter)
# logger.del_channel(filename='log2.txt')
def readBackground(symbol_file_path):
    print ("start reading file path:", symbol_file_path)
    symbols = symbol_file_path.split("/")
    try:
        background_csv = pd.read_csv(symbol_file_path + '/Background.csv')
    except:
        print ("fail to read background.csv file. skip this file")
        return 0
    if symbols[-1] == "003816":
        return 22
    try:
        type = background_csv['基金类型'].iloc[0]
        print ("type:", type)
        logger.info("read " + symbol_file_path + ", background type is:" + type)
        test1_array = ['混合型-灵活', '混合型-偏股', '指数型-股票', '股票型', '混合型-偏债', '混合型-绝对收益', '混合型-平衡',
                       'FOF-稳健型', 'FOF-进取型', 'FOF-均衡型']
        test2_array = ['货币型-普通货币']
        test22_array = ['货币型-浮动净值']
        test3_array = ['债券型-混合二级', '债券型-长债', '债券型-混合一级', '债券型-中短债', '指数型-固收']
        test33_array = ['QDII-纯债', 'QDII-混合债']
        test4_array = ['QDII-普通股票', '指数型-海外股票', '指数型-其他', 'QDII-混合偏股', 'QDII-混合灵活', 'QDII-商品',
                       'QDII-混合平衡', 'QDII-REITs', '商品', 'QDII-FOF']
        if type in test1_array:
            return 1
        elif type in test2_array:
            return 2
        elif type in test22_array:
            return 22
        elif type in test3_array:
            return 3
        elif type in test33_array:
            return 33
        elif type in test4_array:
            return 4
        else:
            logger.error("symbol:" + symbol_file_path + ", type not define:" + type)
            return 0
    except:
        error_log = "Faild to read file path: "+ str(symbol_file_path)
        logger.error(error_log)
        return 0
def readDays(symbol_file_path):
    print ("shortfunds check, start reading file path:", symbol_file_path)
    symbols = symbol_file_path.split("/")
    try:

        background_csv = pd.read_csv(symbol_file_path + '/Background.csv')
        # only need to check Fund 1, fund 2 is money order will skip
        fund1_csv = pd.read_csv(symbol_file_path + '/Fund_1.csv')
    except:
        print ("fail to read background.csv or Fund_1.csv file. skip this file")
        return 0
    try:
        type = background_csv['基金类型'].iloc[0]
        print("type:", type)
        logger.info("read " + symbol_file_path + ", background type is:" + type)
        money_order_array = ['货币型-普通货币','货币型-浮动净值']
        if type in money_order_array:
            # skip all money order
            print("skip money order for shortfunds check.")
            return 0
        fund1_csv = fund1_csv.sort_values(by='净值日期')
        fund1_csv['净值日期'] = pd.to_datetime(fund1_csv['净值日期'])
        first_date = fund1_csv['净值日期'].iloc[0]
        last_date = fund1_csv['净值日期'].iloc[-1]
        difference_days = (last_date - first_date).days
        logger.info(symbol_file_path + ", difference in days:" + str(difference_days))
        if difference_days <= 250:
            return 1
    except Exception as e:
        print()
        return 0
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
        logger.info("trigger: " + script_path + " " + params)
    else:
        print (f"Error in running the script. Return code: {result.returncode}, script: {script_path} {params} ")
        logger.error("fail to trigger: " + script_path + " " + params)
# 混合型-灵活, 混合型-偏股, 指数型-股票, 股票型, 混合型-偏债, 混合型-绝对收益, 混合型-平衡, FOF-稳健型, FOF-进取型, FOF-均衡型
# return 1 run test.py
def trigger_test(formatted_number):
    trigger_python_script(home + '/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/test.py',formatted_number)
    pass
# 货币型-普通货币
# return 2 test_2_money_market
def trigger_test_2_money_market(formatted_number):
    trigger_python_script(home + '/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/test_2_money_market.py', formatted_number)
    pass
# 003816, 货币型-浮动净值: test_2_money_market_2
def trigger_test_2_money_market_2(formatted_number):
    trigger_python_script(home + '/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/test_2_money_market_2.py', formatted_number)
    pass
# 债券型-混合二级, 债券型-长债, 债券型-混合一级, 债券型-中短债, 指数型-固收, QDII-纯债, QDII-混合债
# return 3 test_3_bonds
def trigger_test_3_bonds(formatted_number):
    trigger_python_script(home + '/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/test_3_bonds.py', formatted_number)
    pass
# test_3_bonds_2: QDII-纯债, QDII-混合债
def trigger_test_3_bonds_2(formatted_number):
    trigger_python_script(home + '/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/test_3_bonds_2.py', formatted_number)
    pass
# QDII-普通股票, 指数型-海外股票, 指数型-其他, QDII-混合偏股, QDII-混合灵活, QDII-商品, QDII-混合平衡, QDII-REITs, 商品, QDII-FOF
# return 4 run test_4_overseas
def trigger_test_4_overseas(formatted_number):
    trigger_python_script(home + '/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/test_4_overseas.py', formatted_number)
    pass
def trigger_test_shortfunds(formatted_number):
    trigger_python_script(home + '/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/test_shortfunds.py', formatted_number)
    pass
def main(start_symbol, end_symbol, input_file_path, files):
    # iterator from [start_symbol to end_symbol]
    # read Background.csv column 基金类型
    # for i in range(start_symbol, (end_symbol+1)):
    #     formatted_number = f"{i:06}"  # Formats the number as a string with leading zeros up to 6 digits
    for file in files[int(start_symbol): int(end_symbol)]:
        # print(formatted_number)
        # symbol_file_path = input_file_path + "/" + formatted_number
        symbol_file_path = input_file_path + "/" + file
        shortType = readDays(symbol_file_path)
        if shortType == 1:
            trigger_test_shortfunds(file)
            continue
        type = readBackground(symbol_file_path)
        print("type number:", type)
        if type == 1:
            trigger_test(file)
        elif type == 2:
            trigger_test_2_money_market(file)
        elif type == 22:
            trigger_test_2_money_market_2(file)
        elif type == 3:
            trigger_test_3_bonds(file)
        elif type == 33:
            trigger_test_3_bonds_2(file)
        elif type == 4:
            trigger_test_4_overseas(file)
        else: # type == 0
            continue

def get_files_from_folders(dir):
    files = []
    for item in os.listdir(dir):
        # print(item)
        files.append(item)
    files.sort()
    print (f"total file count: {len(files)}, from folder: {dir}")
    return files
if __name__ == '__main__':
    input_file_path = home + '/Desktop/output_china'
    # output_file_path = home + '/Desktop/output_china'
    try:
        start_symbol = int(sys.argv[1])
        end_symbol = int(sys.argv[2])
        files = get_files_from_folders(input_file_path)
        main(start_symbol, end_symbol, input_file_path, files)
    except Exception as e:
        raise Exception("fail to run at error ", e)