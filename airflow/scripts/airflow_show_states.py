#!/usr/bin/env python3
import sys
import subprocess

import json

def main():
    if len(sys.argv) != 3:
        print("Usage: airflow_show_states.py <dag_id> <run_id>")
        sys.exit(1)
    dag_id = sys.argv[1]
    run_id = sys.argv[2]

    # Step 1: List DAG runs and find execution_date for run_id
    list_runs_cmd = [
        "docker-compose",
        "exec",
        "airflow",
        "airflow",
        "dags",
        "list-runs",
        "-d",
        dag_id,
        "--output",
        "json"
    ]
    try:
        list_runs_result = subprocess.run(list_runs_cmd, check=True, capture_output=True, text=True)
        runs = json.loads(list_runs_result.stdout)
    except Exception as e:
        print(f"Error listing DAG runs: {e}", file=sys.stderr)
        sys.exit(1)

    execution_date = None
    for run in runs:
        if run.get("run_id") == run_id:
            execution_date = run.get("execution_date")
            break

    if not execution_date:
        print(f"Run ID {run_id} not found for DAG {dag_id}", file=sys.stderr)
        sys.exit(1)

    # Step 2: Use execution_date to get task states
    states_cmd = [
        "docker-compose",
        "exec",
        "airflow",
        "airflow",
        "tasks",
        "states-for-dag-run",
        dag_id,
        execution_date
    ]
    try:
        result = subprocess.run(states_cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}", file=sys.stderr)
        print(e.stderr, file=sys.stderr)
        sys.exit(e.returncode)

if __name__ == "__main__":
    main()