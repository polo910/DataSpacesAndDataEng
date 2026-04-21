#!/bin/bash

FULL=$(duckdb -c "SELECT COUNT(*) FROM read_csv_auto('providers/*/observations.csv');")
FED=$(duckdb -c "SELECT COUNT(*) FROM read_csv_auto(['providers/satellite_A/observations.csv','providers/satellite_B/observations.csv']);")

if [ "$FULL" -eq "$FED" ]; then
  echo "COMPLETE"
else
  echo "INCOMPLETE"
fi
