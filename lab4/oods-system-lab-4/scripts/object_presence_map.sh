#!/bin/bash

echo "OBJECT A B G"

duckdb -c "
SELECT DISTINCT object_id FROM read_csv_auto('providers/*/observations.csv');
" | while read obj
do
  A=$(duckdb -c "SELECT COUNT(*) FROM 'providers/satellite_A/observations.csv' WHERE object_id='$obj';")
  B=$(duckdb -c "SELECT COUNT(*) FROM 'providers/satellite_B/observations.csv' WHERE object_id='$obj';")
  G=$(duckdb -c "SELECT COUNT(*) FROM 'providers/ground_station/observations.csv' WHERE object_id='$obj';")

  [ "$A" -gt 0 ] && A="X" || A="-"
  [ "$B" -gt 0 ] && B="X" || B="-"
  [ "$G" -gt 0 ] && G="X" || G="-"

  echo "$obj $A $B $G"
done
