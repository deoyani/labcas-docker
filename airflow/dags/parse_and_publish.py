from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

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

    publish_task = DockerOperator(
        task_id="publish_metadata",
        image="labcas-docker-publish:latest",
        api_version="auto",
        auto_remove=True,
        command="",
        environment={
            "steps": "publish"
        },
        mounts=[Mount(source="/Users/david/Documents/Projects/Labcas/labcas-docker/data", target="/data", type="bind")],
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
    )

    parse_task >> publish_task
