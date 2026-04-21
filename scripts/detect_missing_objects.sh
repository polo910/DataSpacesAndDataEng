#!/bin/bash

for obj in $(duckdb -c "SELECT DISTINCT object_id FROM read_csv_auto('providers/*/observations.csv');")
do
  echo -n "$obj missing in: "

  duckdb -c "SELECT COUNT(*) FROM 'providers/satellite_A/observations.csv' WHERE object_id='$obj';" | grep -q 0 && echo -n "satellite_A "
  duckdb -c "SELECT COUNT(*) FROM 'providers/satellite_B/observations.csv' WHERE object_id='$obj';" | grep -q 0 && echo -n "satellite_B "
  duckdb -c "SELECT COUNT(*) FROM 'providers/ground_station/observations.csv' WHERE object_id='$obj';" | grep -q 0 && echo -n "ground_station "

  echo ""
done
