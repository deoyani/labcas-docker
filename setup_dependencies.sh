#!/usr/bin/env bash
set -eux

apt-get update
apt-get install -y docker.io docker-compose python3-pip

pip3 install --no-cache-dir pyyaml pandas openpyxl

docker --version
docker-compose --version
