# LabCAS Docker Environment

This repository provides a Dockerized setup for LabCAS (Laboratory Catalog and Archive System) at JPL. It includes a `Dockerfile` and a `build_labcas.sh` script for automating the process of building and running the LabCAS environment, complete with LDAP configuration, Apache, and backend services.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Advanced Usage](#advanced-usage)
- [Contributing](#contributing)
- [License](#license)

## Overview

This project automates the deployment of the LabCAS environment using Docker. The Docker image contains all necessary dependencies, including OpenJDK, Apache, LDAP, and the LabCAS backend. The `build_labcas.sh` script simplifies the build and run process, handling LDAP initialization, Apache setup, and backend service execution.

## Prerequisites

Before you begin, ensure you have the following installed:

- [Docker](https://docs.docker.com/get-docker/)
- [Git](https://git-scm.com/)
- [Bash](https://www.gnu.org/software/bash/) (for running the provided script)
- A valid LabCAS username and password for accessing the resources

## Setup

Run the helper script to install Docker, Docker Compose, and Python dependencies:

```bash
./setup_dependencies.sh
```

### Access to Private GitHub Repositories

The Airflow and publish containers require access to the private
`jpl-labcas/publish` repository. Set a personal access token in the
`GITHUB_TOKEN` environment variable before building or pulling the
images:

```bash
export GITHUB_TOKEN=<your_token>
```

If your token also allows access to GitHub Container Registry, log in so
the `publish` image can be pulled:

```bash
echo "$GITHUB_TOKEN" | docker login ghcr.io -u <github_username> --password-stdin
```

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/labcas-docker.git
   cd labcas-docker
    ```
2. **Configure Credentials**

   You will need your LabCAS username and password for authentication. These can be configured directly in the `build_labcas.sh` script or passed as environment variables.

## Usage

To build and run the LabCAS Docker environment, simply run:

```bash
docker-compose up --build
```

Make sure the `GITHUB_TOKEN` variable is set in your environment so that the
private `publish` repository can be cloned during the build.

If you have already run previous builds and re-running, recommend shutting down previous environments first:

```bash
docker-compose down
docker-compose up --build
```

This script will:

1. Build the Docker image across the `Dockerfiles` in subdirectories labcas-ui, labcas-backend, and ldap.
2. Run the Docker container with the necessary environment variables.
3. Initialize the LDAP configuration.
4. Start the Apache server.
5. Launch the LabCAS backend services.

## Important Notes and Troubleshooting

### Docker Container Error
If you get an error that a previous Docker container still exists, run the following command to remove the container:
```bash
docker rm [9c*** container ID]
```

### CORS Issue
You might encounter CORS issues because the LabCAS backend web service is currently hosted on port 8444 while the UI is on port 80. A future release will resolve this by changing the UI to port 443 and set up a reverse proxy on the LabCAS backend.

For continued testing, if you’re using a MacBook, you can bypass CORS issues by running Chrome without CORS checks using the following command:
```bash
open -na "Google Chrome" --args --disable-web-security --user-data-dir="/tmp/chrome_dev"
```

### Disabling Certificate Checks (Temporary)
Because the SSL certificates are not yet set up, please follow the steps below to disable certificate checks for the LabCAS backend service:
1.	Open Chrome as described in step 4 (with --disable-web-security).
2.	Navigate to: https://3.80.56.196:8444/labcas-backend-data-access-api/auth
3.	Click “Proceed to [your_ip_address]” to bypass the certificate warning.

## Configuration

### Configuration Change: ui/environment.cfg
Please update the following file: ui/environment.cfg. Replace ip_address_placeholder with the actual IP address of your server. If you are running this locally on a MacBook, you can use localhost as the IP address:
```bash
ip_address_placeholder -> localhost (or your server IP)
```

### Environment Variables

You can configure the following environment variables to customize your setup:

- `LDAP_ADMIN_USERNAME`: The LDAP admin username (default: `admin`)
- `LDAP_ADMIN_PASSWORD`: The LDAP admin password (default: `secret`)
- `LDAP_ROOT`: The LDAP root domain (default: `dc=labcas,dc=jpl,dc=nasa,dc=gov`)
- `HOST_PORT_HTTP`: The host port to map to container's port 80 (default: `80`)
- `HOST_PORT_HTTPS`: The host port to map to container's port 8444 (default: `8444`)

### Script Configuration

To modify the build and run process, you can edit the `build_labcas.sh` script. The following variables are available:

- `IMAGE_NAME`: The name of the Docker image to build (default: `labcas_debug_image`)
- `CONTAINER_NAME`: The name of the Docker container to run (default: `labcas_debug_instance`)

## Contributing

Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.

## License

The project is licensed under the Apache version 2 license.

## Airflow and Publish Integration

This setup includes optional services for running Apache Airflow and the LabCAS `publish` tool. The `airflow` container executes DAGs stored in `./airflow/dags` and mounts `./airflow/scripts` for helper scripts. A simple example DAG `parse_and_publish` parses an Excel file and then invokes the `publish` command to push metadata to the LabCAS backend.

The Airflow service now runs with `LocalExecutor` and a PostgreSQL database, enabling Docker-based tasks to run properly and ensuring logs are captured for troubleshooting. A new `postgres` container is included in the compose file and Airflow connects to it using the `AIRFLOW__DATABASE__SQL_ALCHEMY_CONN` environment variable.

The `publish` container is built from `ghcr.io/jpl-labcas/publish` and communicates with the backend service on the internal Docker network.

To start all services, run:

```bash
docker-compose up --build
```

Airflow will be available on port `8081` and can be used to orchestrate metadata publishing workflows.

### Building and Running `labcas-publish`

The publishing tool can also be executed on its own.  A container image is
provided in the private registry and can be built locally with

```bash
docker buildx create --name labcas --use               # one time
docker buildx build --tag labcas-publish:latest \
  --file docker/Dockerfile --load .
```

To run the container you must supply a few environment variables and mount the
metadata and data directories:

```bash
docker container run --rm \
  --env consortium=EDRN \
  --env collection=MyCollection \
  --env solr=https://host.docker.internal:8984/solr \
  --volume $HOST_METADATA_PATH:/mnt/metadata:ro \
  --volume $HOST_DATA_PATH:/mnt/data \
  labcas-publish
```

Supported variables are shown below with their defaults:

| Variable            | Purpose                                             | Default                                   |
|---------------------|-----------------------------------------------------|-------------------------------------------|
| `solr`              | URL to LabCAS Solr                                  | `https://host.docker.internal:8984/solr` |
| `consortium`        | Science organization (EDRN, MCL, or NIST)           | `EDRN`                                    |
| `collection`        | Name of the collection to publish                   | *(none)*                                  |
| `collection_subset` | Single dataset within the collection                | *(optional)*                              |
| `publish_id`        | Publication ID to re-use                            | *(optional)*                              |
| `steps`             | Comma-separated publication steps                   | `headers,hash,crawl,updown,compare,publish,thumbnails` |

Two volumes must be provided: the metadata configuration directory mounted to
`/mnt/metadata` (read-only is fine) and the LabCAS data directory mounted to
`/mnt/data` with write access.

When using `docker-compose`, define the above variables in your shell
environment or an `.env` file so that the `publish` service receives the
correct configuration.

### Testing the `parse_and_publish` DAG

1. Place the Excel file you want to ingest at `./data/input.xlsx`.
2. Export `HOST_DATA_PATH` with the absolute path to the project `data` directory so Airflow can mount it when running Docker tasks:

   ```bash
   export HOST_DATA_PATH=$(pwd)/data
   ```

3. Adjust credentials for the publish tool in `shared-config/publish/publish.cfg` if necessary. This file is mounted into the publish container using `docker-compose.override.yml`.
4. Start the environment with `docker-compose up --build`.

   Ensure the `GITHUB_TOKEN` environment variable is exported so the
   `publish` image can be built.

5. Trigger the DAG from the Airflow UI or run the following command:

   ```bash
   docker exec airflow airflow dags trigger parse_and_publish
   ```

Task logs for the publish step will be available in the Airflow interface and in `./airflow/logs` on the host.

### Viewing Logs

Each container writes its output to Docker's logging system. If a workflow fails or a service does not start correctly, you can inspect the logs with `docker logs`:

```bash
# Example: view Airflow logs
docker logs airflow

# Example: view publish container logs
docker logs labcas-publish
```

Airflow task logs are persisted to the `airflow/logs` directory on the host, so you can also browse those files directly.
