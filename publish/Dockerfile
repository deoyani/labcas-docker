# Build the publish tool locally instead of pulling the upstream image.
# This Dockerfile should be updated with the actual build steps for the publish tool.

FROM python:3.10-slim

ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y git gcc libglib2.0-dev libxml2-dev libxslt1-dev libjpeg-dev zlib1g-dev libopenjp2-7-dev libtiff-dev && rm -rf /var/lib/apt/lists/*

# clone the Publish repo (token optional for private repos)
RUN git clone https://$GITHUB_TOKEN@github.com/jpl-labcas/publish.git /opt/publish
WORKDIR /opt/publish

# install Publish and its deps
RUN if [ -f setup.py ]; then pip install . ; \
    elif [ -f requirements.txt ]; then pip install -r requirements.txt ; fi

ENTRYPOINT ["/usr/local/bin/python3"]
CMD ["publishing_pipeline.py"]

