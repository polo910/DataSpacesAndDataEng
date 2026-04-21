#!/bin/bash

OUT=reports/query_report.txt

echo "REPORT" > $OUT
date >> $OUT

echo "TOTAL:" >> $OUT
duckdb -c "SELECT COUNT(*) FROM read_csv_auto('providers/*/observations.csv');" >> $OUT

echo "OBJ-003:" >> $OUT
duckdb -c "SELECT COUNT(*) FROM read_csv_auto('providers/*/observations.csv') WHERE object_id='OBJ-003';" >> $OUT
