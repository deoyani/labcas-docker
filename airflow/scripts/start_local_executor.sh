#!/usr/bin/env bash
set -e
airflow db upgrade
# create admin user if not exists

airflow users create \
  --username admin \
  --password admin \
  --firstname Air \
  --lastname Flow \
  --role Admin \
  --email admin@example.com \
  --skip-if-exists

# start scheduler in background
airflow scheduler &
# start webserver
exec airflow webserver
