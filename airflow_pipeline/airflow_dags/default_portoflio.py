from airflow import DAG
from airflow.decorators import task

DATA_DATE = '{{ data_interval_end }}'
DJANGO_URL = 'localhost:8000'
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

@task(task_id='pull', templates_dict={"date": DATA_DATE, "url": DJANGO_URL, "body": BODY, "output": OUTPUT_FOLDER})
def pull_result(**kwargs):
    date = kwargs['date']
    url = kwargs['url']
    body = kwargs['body']
    output = kwargs['output']
    import requests
    import json
    import os
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
    default_args=default_args,
) as dag:
    pull_default = pull_result()

    pull_default