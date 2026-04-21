#!/bin/bash

echo "A:"
duckdb -c "DESCRIBE SELECT * FROM 'providers/satellite_A/observations.csv';"

echo "B:"
duckdb -c "DESCRIBE SELECT * FROM 'providers/satellite_B/observations.csv';"

echo "G:"
duckdb -c "DESCRIBE SELECT * FROM 'providers/ground_station/observations.csv';"
