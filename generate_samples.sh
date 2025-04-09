#!/bin/bash
# This script generates 1000 sample patients for California in various formats
# and zips them up by type in the ./samples/ subdirectory

../synthes/run_synthea -p 1000 California \
  --exporter.csv.export=true

mkdir -p samples

for type in csv
do
  zip -jr samples/synthea_sample_data_${type}_california_latest.zip output/${type}/
done
