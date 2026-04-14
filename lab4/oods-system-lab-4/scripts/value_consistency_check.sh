#!/bin/bash

duckdb -c "
SELECT object_id, MIN(temperature), MAX(temperature)
FROM read_csv_auto('providers/*/observations.csv')
GROUP BY object_id;
"
