#!/bin/bash

duckdb -c "
SELECT object_id, COUNT(DISTINCT filename)
FROM read_csv_auto('providers/*/observations.csv', filename=true)
GROUP BY object_id;
"
