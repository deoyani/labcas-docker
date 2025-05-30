FROM apache/airflow:2.6.3

USER root
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

ARG GITHUB_TOKEN
RUN git clone https://${GITHUB_TOKEN}@github.com/jpl-labcas/publish.git /opt/publish

RUN if [ -f /opt/publish/setup.py ]; then \
      pip install /opt/publish; \
    elif [ -f /opt/publish/publish ]; then \
      chmod +x /opt/publish/publish && ln -s /opt/publish/publish /usr/local/bin/publish; \
    fi

USER airflow
RUN pip install --no-cache-dir pandas openpyxl docker
