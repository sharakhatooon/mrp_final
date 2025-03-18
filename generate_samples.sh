#!/bin/bash
# This script generates 10000 sample patients for California in various formats
# and zips them up by type in the ./samples/ subdirectory

../synthes/run_synthea -p 10000 --state "California" \
  --exporter.ccda.export=true \
  --exporter.fhir.export=true \
  --exporter.fhir_stu3.export=true \
  --exporter.fhir_dstu2.export=true \
  --exporter.csv.export=true

mkdir -p samples

for type in ccda fhir fhir_stu3 fhir_dstu2 csv
do
  zip -jr samples/synthea_sample_data_${type}_california_latest.zip output/${type}/
done
