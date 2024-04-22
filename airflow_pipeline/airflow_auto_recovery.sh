#!/usr/bin/env bash
# run airflow auto check and restart if airflow is down
# add to crons job: */15 * * * * bash /home/app/Desktop/machine_learning/airflow_pipeline/airflow_auto_recovery.sh
set -e
echo "run airflow auto recovery shell scripts"
echo "airflow-webserver pid="
if pgrep -f airflow-webserver
then
    echo "regular check succeed, airflow web server is running"
else
    echo "regular check fail, start running airflow job"
    nohup airflow webserver -p 8080 &> /home/app/Desktop/airflow_nohup.out &
fi

echo "sleep for 10 seconds"
sleep 10
echo "airflow scheduler pid="
if pgrep -f 'airflow scheduler'
then
    echo "regular check succeed, airflow scheduler is running"
else
    echo "regular check fail, start running airflow scheduler"
    nohup airflow scheduler &> /home/app/Desktop/airflow_nohup.out &
fi
