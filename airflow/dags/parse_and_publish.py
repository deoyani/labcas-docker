from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="parse_and_publish",
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:

    parse_task = BashOperator(
        task_id="parse_excel",
        bash_command="python /opt/airflow/scripts/parse_excel.py /data/input.xlsx /data/output.json",
    )

    publish_task = BashOperator(
        task_id="publish_metadata",
        bash_command="publish /data/output.json --backend-url https://labcas-backend:8444",
    )

    parse_task >> publish_task
