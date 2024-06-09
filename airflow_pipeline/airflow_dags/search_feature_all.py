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
    'search_feature_all', default_args=default_args,
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
    cmd = "git -C ~/Desktop/Pathfinder-Analysis checkout main"
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


python_op_201 = BashOperator(
    task_id='search_symbol_iterator_0-200',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '0 200'
)
python_op_202 = BashOperator(
    task_id='search_symbol_iterator_200-400',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '200 400'
)
python_op_203 = BashOperator(
    task_id='search_symbol_iterator_400-600',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '400 600'
)
python_op_204 = BashOperator(
    task_id='search_symbol_iterator_600-800',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '600 800'
)
python_op_205 = BashOperator(
    task_id='search_symbol_iterator_800-1000',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '800 1000'
)
python_op_206 = BashOperator(
    task_id='search_symbol_iterator_1000-1200',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '1000 1200'
)
python_op_207 = BashOperator(
    task_id='search_symbol_iterator_1200-1400',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '1200 1400'
)
python_op_208 = BashOperator(
    task_id='search_symbol_iterator_1400-1600',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '1400 1600'
)
python_op_209 = BashOperator(
    task_id='search_symbol_iterator_1600-1800',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '1600 1800'
)
python_op_210 = BashOperator(
    task_id='search_symbol_iterator_1800-2000',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '1800 2000'
)

python_op_211 = BashOperator(
    task_id='search_symbol_iterator_2000-2200',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '2000 2200'
)
python_op_212 = BashOperator(
    task_id='search_symbol_iterator_2200-2400',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '2200 2400'
)
python_op_213 = BashOperator(
    task_id='search_symbol_iterator_2400-2600',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '2400 2600'
)
python_op_214 = BashOperator(
    task_id='search_symbol_iterator_2600-2800',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '2600 2800'
)
python_op_215 = BashOperator(
    task_id='search_symbol_iterator_2800-3000',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '2800 3000'
)
python_op_216 = BashOperator(
    task_id='search_symbol_iterator_3000-3200',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '3000 3200'
)
python_op_217 = BashOperator(
    task_id='search_symbol_iterator_3200-3400',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '3200 3400'
)
python_op_218 = BashOperator(
    task_id='search_symbol_iterator_3400-3600',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '3400 3600'
)
python_op_219 = BashOperator(
    task_id='search_symbol_iterator_3600-3800',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '3600 3800'
)
python_op_220 = BashOperator(
    task_id='search_symbol_iterator_3800-4000',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '3800 4000'
)
python_op_221 = BashOperator(
    task_id='search_symbol_iterator_4000-4200',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '4000 4200'
)
python_op_222 = BashOperator(
    task_id='search_symbol_iterator_4200-4400',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '4200 4400'
)
python_op_223 = BashOperator(
    task_id='search_symbol_iterator_4400-4600',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '4400 4600'
)
python_op_224 = BashOperator(
    task_id='search_symbol_iterator_4600-4800',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '4600 4800'
)
python_op_225 = BashOperator(
    task_id='search_symbol_iterator_4800 5000',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '4800 5000'
)
python_op_226 = BashOperator(
    task_id='search_symbol_iterator_5000-5200',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '5000 5200'
)
python_op_227 = BashOperator(
    task_id='search_symbol_iterator_5200-5400',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '5200 5400'
)
python_op_228 = BashOperator(
    task_id='search_symbol_iterator_5400-5600',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '5400 5600'
)
python_op_229 = BashOperator(
    task_id='search_symbol_iterator_5400-5800',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '5600 5800'
)
python_op_230 = BashOperator(
    task_id='search_symbol_iterator_5800-6000',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '5800 6000'
)

python_op_231 = BashOperator(
    task_id='search_symbol_iterator_6000-6200',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '6000 6200'
)
python_op_232 = BashOperator(
    task_id='search_symbol_iterator_6200-6400',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '6200 6400'
)
python_op_233 = BashOperator(
    task_id='search_symbol_iterator_6400-6600',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '6400 6600'
)
python_op_234 = BashOperator(
    task_id='search_symbol_iterator_6600-6800',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '6600 6800'
)
python_op_235 = BashOperator(
    task_id='search_symbol_iterator_6800-7000',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '6800 7000'
)
python_op_236 = BashOperator(
    task_id='search_symbol_iterator_7000-7200',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '7000 7200'
)
python_op_237 = BashOperator(
    task_id='search_symbol_iterator_7200-7400',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '7200 7400'
)
python_op_238 = BashOperator(
    task_id='search_symbol_iterator_7400-7600',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '7400 7600'
)
python_op_239 = BashOperator(
    task_id='search_symbol_iterator_7600-7800',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '7600 7800'
)
python_op_240 = BashOperator(
    task_id='search_symbol_iterator_7800-8000',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '7800 8000'
)

python_op_241 = BashOperator(
    task_id='search_symbol_iterator_8000-8200',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '8000 8200'
)
python_op_242 = BashOperator(
    task_id='search_symbol_iterator_8200-8400',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '8200 8400'
)
python_op_243 = BashOperator(
    task_id='search_symbol_iterator_8400-8600',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '8400 8600'
)
python_op_244 = BashOperator(
    task_id='search_symbol_iterator_8600-8800',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '8600 8800'
)
python_op_245 = BashOperator(
    task_id='search_symbol_iterator_8800-9000',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '8800 9000'
)
python_op_246 = BashOperator(
    task_id='search_symbol_iterator_9000-9200',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '9000 9200'
)
python_op_247 = BashOperator(
    task_id='search_symbol_iterator_9200-9400',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '9200 9400'
)
python_op_248 = BashOperator(
    task_id='search_symbol_iterator_9400-9600',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '9400 9600'
)
python_op_249 = BashOperator(
    task_id='search_symbol_iterator_9600-9800',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '9600 9800'
)
python_op_250 = BashOperator(
    task_id='search_symbol_iterator_9800-10000',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '9800 10000'
)
python_op_251 = BashOperator(
    task_id='search_symbol_iterator_10000-10200',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '10000 10200'
)
python_op_252 = BashOperator(
    task_id='search_symbol_iterator_10200-10400',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '10200 10400'
)
python_op_253 = BashOperator(
    task_id='search_symbol_iterator_10400-10600',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '10400 10600'
)
python_op_254 = BashOperator(
    task_id='search_symbol_iterator_10600-10800',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '10600 10800'
)
python_op_255 = BashOperator(
    task_id='search_symbol_iterator_10800-11000',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '10800 11000'
)
python_op_256 = BashOperator(
    task_id='search_symbol_iterator_11000-11200',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '11000 11200'
)
python_op_257 = BashOperator(
    task_id='search_symbol_iterator_11200-11400',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '11200 11400'
)
python_op_258 = BashOperator(
    task_id='search_symbol_iterator_11400-11600',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '11400 11600'
)
python_op_259 = BashOperator(
    task_id='search_symbol_iterator_11600-11800',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '11600 11800'
)
python_op_260 = BashOperator(
    task_id='search_symbol_iterator_11800-12000',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '11800 12000'
)
python_op_261 = BashOperator(
    task_id='search_symbol_iterator_12000-12200',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '12000 12200'
)
python_op_262 = BashOperator(
    task_id='search_symbol_iterator_12200-12400',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '12200 12400'
)
python_op_263 = BashOperator(
    task_id='search_symbol_iterator_12400-12600',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '12400 12600'
)
python_op_264 = BashOperator(
    task_id='search_symbol_iterator_12600-12800',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '12600 12800'
)
python_op_265 = BashOperator(
    task_id='search_symbol_iterator_12800-13000',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '12800 13000'
)
python_op_266 = BashOperator(
    task_id='search_symbol_iterator_13000-13200',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '13000 13200'
)
python_op_267 = BashOperator(
    task_id='search_symbol_iterator_13200-13400',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '13200 13400'
)
python_op_268 = BashOperator(
    task_id='search_symbol_iterator_13400-13600',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '13400 13600'
)
python_op_269 = BashOperator(
    task_id='search_symbol_iterator_13600-13800',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '13600 13800'
)
python_op_270 = BashOperator(
    task_id='search_symbol_iterator_13800-14000',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '13800 14000'
)

python_op_271 = BashOperator(
    task_id='search_symbol_iterator_14000-14200',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '14000 14200'
)
python_op_272 = BashOperator(
    task_id='search_symbol_iterator_14200-14400',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '14200 14400'
)
python_op_273 = BashOperator(
    task_id='search_symbol_iterator_14400-14600',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '14400 14600'
)
python_op_274 = BashOperator(
    task_id='search_symbol_iterator_14600-14800',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '14600 14800'
)
python_op_275 = BashOperator(
    task_id='search_symbol_iterator_14800-15000',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '14800 15000'
)
python_op_276 = BashOperator(
    task_id='search_symbol_iterator_15000-15200',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '15000 15200'
)
python_op_277 = BashOperator(
    task_id='search_symbol_iterator_15200-15400',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '15200 15400'
)
python_op_278 = BashOperator(
    task_id='search_symbol_iterator_15400-15600',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '15400 15600'
)
python_op_279 = BashOperator(
    task_id='search_symbol_iterator_15600-15800',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '15600 15800'
)
python_op_280 = BashOperator(
    task_id='search_symbol_iterator_15800-16000',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '15800 16000'
)
python_op_281 = BashOperator(
    task_id='search_symbol_iterator_16000-16200',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '16000 16200'
)
python_op_282 = BashOperator(
    task_id='search_symbol_iterator_16200-16400',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '16200 16400'
)
python_op_283 = BashOperator(
    task_id='search_symbol_iterator_16400-16600',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '16400 16600'
)
python_op_284 = BashOperator(
    task_id='search_symbol_iterator_16600-16800',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '16600 16800'
)
python_op_285 = BashOperator(
    task_id='search_symbol_iterator_16800-17000',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '16800 17000'
)
python_op_286 = BashOperator(
    task_id='search_symbol_iterator_17000-17200',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '17000 17200'
)
python_op_287 = BashOperator(
    task_id='search_symbol_iterator_17200-17400',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '17200 17400'
)
python_op_288 = BashOperator(
    task_id='search_symbol_iterator_17400-17600',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '17400 17600'
)
python_op_289 = BashOperator(
    task_id='search_symbol_iterator_17600-17800',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '17600 17800'
)
python_op_290 = BashOperator(
    task_id='search_symbol_iterator_17800-18000',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '17800 18000'
)
python_op_291 = BashOperator(
    task_id='search_symbol_iterator_18000-18200',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '18000 18200'
)
python_op_292 = BashOperator(
    task_id='search_symbol_iterator_18200-18400',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '18200 18400'
)
python_op_293 = BashOperator(
    task_id='search_symbol_iterator_18400-18600',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '18400 18600'
)
python_op_294 = BashOperator(
    task_id='search_symbol_iterator_18600-18800',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '18600 18800'
)
python_op_295 = BashOperator(
    task_id='search_symbol_iterator_18800-19000',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '18800 19000'
)
python_op_296 = BashOperator(
    task_id='search_symbol_iterator_19000-19200',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '19000 19200'
)
python_op_297 = BashOperator(
    task_id='search_symbol_iterator_19200-19400',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '19200 19400'
)
python_op_298 = BashOperator(
    task_id='search_symbol_iterator_19400-19600',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '19400 19600'
)
python_op_299 = BashOperator(
    task_id='search_symbol_iterator_19600-19800',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '19600 19800'
)
python_op_300 = BashOperator(
    task_id='search_symbol_iterator_19800-20000',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '19800 20000'
)
python_op_301 = BashOperator(
    task_id='search_symbol_iterator_20000-20200',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '20000 200'
)
python_op_302 = BashOperator(
    task_id='search_symbol_iterator_20200-20400',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '20200 20400'
)
python_op_303 = BashOperator(
    task_id='search_symbol_iterator_20400-20600',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '20400 20600'
)
python_op_304 = BashOperator(
    task_id='search_symbol_iterator_20600-20800',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '20600 20800'
)
python_op_305 = BashOperator(
    task_id='search_symbol_iterator_20800-201000',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '20800 21000'
)
python_op_306 = BashOperator(
    task_id='search_symbol_iterator_21000-21200',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '21000 21200'
)
python_op_307 = BashOperator(
    task_id='search_symbol_iterator_21200-21400',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '21200 21400'
)
python_op_308 = BashOperator(
    task_id='search_symbol_iterator_21400-21600',
    trigger_rule='all_success',
    dag=dag,
    bash_command='python /home/app/Desktop/Pathfinder-Analysis/Fund_Analysis/Analysis_Class/search_symbol_iterator.py '
                 '21400 21600'
)

python_op_0 >> python_op_201 >> python_op_202 >> python_op_203 >> python_op_204 >> python_op_205 >> python_op_206 \
>> python_op_207 >> python_op_208 >> python_op_209 >> python_op_210 >> python_op_211 >> python_op_212 >> python_op_213 \
>> python_op_214 >> python_op_215 >> python_op_216 >> python_op_217 >> python_op_218 >> python_op_219 >> python_op_220\
>> python_op_221 >> python_op_222 >> python_op_223 >> python_op_224 >> python_op_225 >> python_op_226 >> python_op_227 \
>> python_op_228 >> python_op_229 >> python_op_230 >> python_op_231 >> python_op_232 >> python_op_233 >> python_op_234 \
>> python_op_235 >> python_op_236 >> python_op_237 >> python_op_238 >> python_op_239 >> python_op_240 >> python_op_241 \
>> python_op_242 >> python_op_243 >> python_op_244 >> python_op_245 >> python_op_246 >> python_op_247 >> python_op_248 \
>> python_op_249 >> python_op_250 >> python_op_251 >> python_op_252 >> python_op_253 >> python_op_254 >> python_op_255 \
>> python_op_256 >> python_op_257 >> python_op_258 >> python_op_259 >> python_op_260 >> python_op_261 >> python_op_262 \
>> python_op_263 >> python_op_264 >> python_op_265 >> python_op_266 >> python_op_267 >> python_op_268 >> python_op_269 \
>> python_op_270 >> python_op_271 >> python_op_272 >> python_op_273 >> python_op_274 >> python_op_275 >> python_op_276 \
>> python_op_277 >> python_op_278 >> python_op_279 >> python_op_280 >> python_op_281 >> python_op_282 >> python_op_283 \
>> python_op_284 >> python_op_285 >> python_op_286 >> python_op_287 >> python_op_288 >> python_op_289 >> python_op_290 \
>> python_op_291 >> python_op_292 >> python_op_293 >> python_op_294 >> python_op_295 >> python_op_296 >> python_op_297 \
>> python_op_298 >> python_op_299 >> python_op_300 >> python_op_301 >> python_op_302 >> python_op_303 >> python_op_304 \
>> python_op_305 >> python_op_306 >> python_op_307 >> python_op_308 \
>> python_op_1



