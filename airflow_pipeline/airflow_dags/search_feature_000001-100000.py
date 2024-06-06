import datetime
import airflow
import logging
import time
from airflow import DAG
from airflow.models import Variable
from datetime import datetime, timedelta
import subprocess
from airflow.exceptions import AirflowException
from airflow.utils.state import State
import sys
import os
from pathlib import Path
import pendulum
home = str(Path.home())
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
import io
import pytz

local_tz = pendulum.timezone("America/New_York")# New York timezone
ny_tz = pytz.timezone("America/New_York")
def localize_ny_tz(d):
    return ny_tz.fromutc(d)
default_args = {
    'owner': 'app',
    'depends_on_past': False,
    # 'start_date': airflow.utils.dates.days_ago(1),
    # 'start_date': datetime(year=2024, month=4, day=23, hour=0, minute=0, tzinfo=local_tz),
    'email': ['None'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0
}

dag = DAG(
    'search_feature_000001-100000', default_args=default_args,
    user_defined_filters= {'localtz': localize_ny_tz}
    # catchup=False
    # schedule_interval='0 0 * * *'
    # schedule_interval=timedelta(days=1)
)


def configure_this_dags_run_properties(**ctx):
    # Check Variable if we need set to back-fill if so, create Dag config file for this dag run. Once complete Update Variable.
    pass

def print_msg(msg, **ctx):
    print (msg)
    logging.info("%s" %msg)

def pass_op(**ctx):
    pass

def python_script(script_name, params, **ctx):
    logging.info("script name is-%s-" % script_name)
    logging.info("Now Invoke Python Script %s" % script_name)
    # xcom_search_external_bucket = ""
    # xcom_item_attribute_partition_epoch = ""
    # try:
    #     task_instance = ctx['task_instance']
    #     xcom_item_attribute_partition_epoch = task_instance.xcom_pull(task_ids='startup_create_cluster', key='xcom_item_attribute_partition_epoch')
    #     logging.info ("xcom_item_attribute_partition_epoch pull from = " + xcom_item_attribute_partition_epoch)
    # except Exception as e:
    #     logging.info("fail to read xcom_search_external_bucket and xcom_item_attribute_partition_epoch")

    cmd = ''
    filePath = ''
    # input = params.split(' ')
    now = datetime.now(tz=local_tz)
    logging.info("now time:" + str(now))
    logging.info("current timestamp:" + str(now.timestamp()))
    cmd = ("python %s %s" % (script_name, params))
    logging.info("trigger cmd: " + cmd)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.STDOUT, shell=True)

    for line in io.TextIOWrapper(p.stdout, encoding="utf-8"):
        logging.info(line)
        if 'AirflowException' in line or 'Error' in line:
            sys.exit('fail at running this script: {}, line: {}'.format(script_name, line))
    # task_instance = ctx['task_instance']
    # task_instance.xcom_push(key='xcom_item_attribute_partition_epoch', value=xcom_item_attribute_partition_epoch)

def python_script_background(script_name, params, **ctx):
    logging.info("script name is-%s-" % script_name)
    logging.info("Now Invoke Python Script %s" % script_name)
    cmd = ("python %s/%s %s" % ("/home/app/Desktop/scripts",script_name, params))
    code = os.system(cmd)
    if code == 0:
        print("success run: " + cmd)
    else:
        print("fail run: " + cmd)
        sys.exit('fail at running this script: {}, cmd: {}'.format(script_name, cmd))

def delay_op(time_delay, **ctx):
    logging.info("delay time: " + time_delay)
    time.sleep(float(time_delay))

def download_ops_scripts(**ctx):
    pass

def initialize_configuration(**ctx):
    # check out and download the latest git repo
    cmd = "git -C ~/Desktop/Pathfinder-Analysis checkout Analysis-Class"
    os.system(cmd)
    cmd = "git -C ~/Desktop/Pathfinder-Analysis pull"
    os.system(cmd)
    print("git pull succeed")
    now = datetime.now(tz=local_tz)
    logging.info("now NY time:")
    logging.info(now)
    logging.info(now.timestamp())

python_op_0 = PythonOperator(
    task_id='initialize_configuration',
    python_callable=initialize_configuration,
    provide_context=True,
    trigger_rule='all_success',
    op_kwargs={},
    dag=dag)

python_op_1 = PythonOperator(
    task_id='task_completed',
    python_callable=pass_op,
    provide_context=True,
    trigger_rule='all_success',
    op_kwargs={},
    dag=dag
)


python_op_2 = BashOperator(
    task_id='search_symbol_iterator_000001-010000',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '000001 010000'
)
python_op_21 = BashOperator(
    task_id='search_symbol_iterator_010001-020000',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '000001 010000'
)
python_op_22 = BashOperator(
    task_id='search_symbol_iterator_020001-030000',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '000001 010000'
)
python_op_23 = BashOperator(
    task_id='search_symbol_iterator_030001-040000',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '000001 010000'
)
python_op_24 = BashOperator(
    task_id='search_symbol_iterator_040001-050000',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '000001 010000'
)
python_op_25 = BashOperator(
    task_id='search_symbol_iterator_050001-060000',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '000001 010000'
)
python_op_26 = BashOperator(
    task_id='search_symbol_iterator_060001-070000',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '000001 010000'
)
python_op_27 = BashOperator(
    task_id='search_symbol_iterator_070001-080000',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '000001 010000'
)
python_op_28 = BashOperator(
    task_id='search_symbol_iterator_080001-090000',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '000001 010000'
)
python_op_29 = BashOperator(
    task_id='search_symbol_iterator_090001-100000',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '000001 010000'
)
python_op_2.set_upstream(python_op_0)
python_op_21.set_upstream(python_op_0)
python_op_22.set_upstream(python_op_0)
python_op_23.set_upstream(python_op_0)
python_op_24.set_upstream(python_op_0)
python_op_25.set_upstream(python_op_0)
python_op_26.set_upstream(python_op_0)
python_op_27.set_upstream(python_op_0)
python_op_28.set_upstream(python_op_0)
python_op_29.set_upstream(python_op_0)

python_op_1.set_upstream(python_op_2)
python_op_1.set_upstream(python_op_21)
python_op_1.set_upstream(python_op_22)
python_op_1.set_upstream(python_op_23)
python_op_1.set_upstream(python_op_24)
python_op_1.set_upstream(python_op_25)
python_op_1.set_upstream(python_op_26)
python_op_1.set_upstream(python_op_27)
python_op_1.set_upstream(python_op_28)
python_op_1.set_upstream(python_op_29)
