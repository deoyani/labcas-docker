#!/bin/bash

# Set Solr data directory within the container
SOLR_DATA_DIR=/tmp/labcas/solr/data

# Solr server URL
SOLR_SERVER_URL=https://localhost:8984

# Ensure the Solr data directory exists
mkdir -p $SOLR_DATA_DIR

# Copy JSON files using relative paths
cp /tmp/labcas/sample_data/dataset_solr.json $SOLR_DATA_DIR/
cp /tmp/labcas/sample_data/file_solr.json $SOLR_DATA_DIR/
cp /tmp/labcas/sample_data/collection_solr.json $SOLR_DATA_DIR/

# Post JSON files to respective Solr cores
curl -k "$SOLR_SERVER_URL/solr/datasets/update?commit=true" --data-binary @$SOLR_DATA_DIR/dataset_solr.json -H "Content-type:application/json"
curl -k "$SOLR_SERVER_URL/solr/files/update?commit=true" --data-binary @$SOLR_DATA_DIR/file_solr.json -H "Content-type:application/json"
curl -k "$SOLR_SERVER_URL/solr/collections/update?commit=true" --data-binary @$SOLR_DATA_DIR/collection_solr.json -H "Content-type:application/json"
