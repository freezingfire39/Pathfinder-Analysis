from datetime import datetime
import pendulum
from airflow import DAG
from airflow.decorators import task

DJANGO_URL = '127.0.0.1:8000'
BODY = {"weights":[{"symbol":"000552", "weight": 0.35},
                        {"symbol":"000415", "weight":0.35},
                        {"symbol":"001309", "weight":0.15},
                        {"symbol":"002258", "weight":0.15}
                        ],"amount": 1e6}
OUTPUT_FOLDER = "/home/app/Desktop/default_portfolio/"

default_args = {
    'owner': 'zgao',
    'depends_on_past': False,
    'retries': 3
}
local_tz = pendulum.timezone("America/New_York")# New York timezone

@task(task_id='pull', templates_dict={ "url": DJANGO_URL, "body": BODY, "output": OUTPUT_FOLDER})
def pull_result(**kwargs):
    import requests
    import json
    import os
    import datetime
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    url = kwargs['url']
    body = kwargs['body']
    output = kwargs['output']
    full_url = url + "/api/v1/py/custom/portfolio/"
    response = requests.post(full_url, json=body)
    response.raise_for_status()
    result = response.json()
    filename = os.path.join(output, f"{date}.json")
    with open(filename, "w") as file:
        json.dump(result, file, indent=4)

with DAG(
    dag_id='default_portoflio',
    schedule="0 10 * * 1-5" ,
    start_date=datetime(2020, 1, 1, tzinfo=local_tz),
    catchup=False,
    default_args=default_args,
) as dag:
    pull_default = pull_result()

    pull_default