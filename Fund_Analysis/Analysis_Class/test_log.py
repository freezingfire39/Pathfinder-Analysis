import os,sys
import numpy as np
import pandas as pd
import datetime
from airflow.exceptions import AirflowException
from pathlib import Path
home = str(Path.home())
import pytz
from itertools import islice
import subprocess
import logging
logging.basicConfig(
      # Log file path
    filemode='a',  # 'a' means append (add to the existing file), 'w' would overwrite the file each time
    level=logging.INFO,  # Logging level set to ERROR
    format='%(asctime)s - %(levelname)s - %(message)s',  # Includes timestamp, log level, and message
    datefmt='%Y-%m-%d %H:%M:%S',  # Timestamp format
    handlers=[
        logging.FileHandler(home + '/Desktop/info.log'),
        logging.StreamHandler
    ]
)
logger = logging.Logger("test")
def get_files_from_folders(dir):
    files = []
    for item in os.listdir(dir):
        # print(item)
        files.append(item)
    files.sort()
    print (f"total file count: {len(files)}, from folder: {dir}")
    return files
def readBackground(symbol_file_path):
    print ("start reading file path:", symbol_file_path)
    try:
        background_csv = pd.read_csv(symbol_file_path + '/Background.csv')
    except:
        print ("fail to read background.csv file. skip this file")
        return None
    try:
        type = background_csv['基金类型'].iloc[0]
        return type
        # print ("type:", type)
        # if "货币型" in type:
        #     return 1
        # elif "债券型" in type:
        #     return 2
        # elif "指数型" in type or "QDII" in type:
        #     return 3
        # else:# "混合型"
        #     return 4
    except:
        # logging.error("Faild to read file path: %s",symbol_file_path)
        return ""
def main(files):
    all_type = []
    for file in files:
        symbol_file_path = input_file_path + "/" + file
        type = readBackground(symbol_file_path)
        if type == None:
            continue
        if type in all_type:
            pass
        else:
            all_type.append(type)
            info_log = "add type: " + str(type) + ", symbol:" + str(file)
            logger.info(info_log)
            logger.info("add type: " + str(type))
            logger.info(", symbol:" + str(file))
    pass
if __name__ == '__main__':
    input_file_path = home + '/Desktop/output_china'

    try:
        files = get_files_from_folders(input_file_path)
        main(files)
    except Exception as e:
        raise AirflowException("fail to run at error ", e)