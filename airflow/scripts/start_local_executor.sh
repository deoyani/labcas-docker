#!/usr/bin/env bash
set -e
airflow db upgrade
# create admin user if not exists
if ! airflow users list | grep -q "^admin\b"; then
  airflow users create --username admin --password admin --firstname Air --lastname Flow --role Admin --email admin@example.com
fi
# start scheduler in background
airflow scheduler &
# start webserver
exec airflow webserver
