from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount
import os
import logging

# Host path for the data directory. Defaults to '/data' if the environment
# variable is not set. This allows running the DAG without creating a global
# '/data' directory on the host by specifying HOST_DATA_PATH=<project>/data
# when starting Airflow.

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

    host_data = os.environ.get("HOST_DATA_PATH", os.path.abspath("/data"))

    basic_auth_user = os.getenv("BASIC_AUTH_USER", "dliu")
    basic_auth_pass = os.getenv("BASIC_AUTH_PASS", "secret")

    publish_task = DockerOperator(
        task_id="publish_metadata",
        image="labcas-docker-publish:latest",
        api_version="auto",
        auto_remove=True,
        command="",
        environment={
            "steps": "publish",
            "LOG_LEVEL": "DEBUG",
            "LABCAS_API_URL": "https://labcas-backend:8444/labcas-backend-data-access-api",
            "SOLR_URL": "https://localhost:8984",
            "COLLECTION": "test_collection",
            "BASIC_AUTH_USER": basic_auth_user,
            "BASIC_AUTH_PASS": basic_auth_pass,
        },
        mounts=[Mount(source=host_data, target="/data", type="bind")],
        docker_url="unix://var/run/docker.sock",
        network_mode="labcas-docker_default",
        tty=True,
    )

    parse_task >> publish_task
