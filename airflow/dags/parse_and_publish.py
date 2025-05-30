from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount
import logging

with DAG(
    dag_id="parse_and_publish",
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:

    parse_task = BashOperator(
        task_id="parse_excel",
        bash_command="set -euxo pipefail; ls -al /data; python /opt/airflow/scripts/parse_excel.py /data/input.xlsx /data/output.json; cat /data/output.json",
    )

    publish_task = DockerOperator(
        task_id="publish_metadata",
        image="labcas-docker-publish:latest",
        api_version="auto",
        auto_remove=True,
        command="",
        environment={
            "steps": "publish",
            "LOG_LEVEL": "DEBUG",
        },
        mounts=[Mount(source="/data", target="/data", type="bind")],
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
    )

    parse_task >> publish_task
