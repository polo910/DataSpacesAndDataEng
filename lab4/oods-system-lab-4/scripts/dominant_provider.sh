#!/bin/bash

echo "satellite_A:"
duckdb -c "SELECT COUNT(*) FROM 'providers/satellite_A/observations.csv';"

echo "satellite_B:"
duckdb -c "SELECT COUNT(*) FROM 'providers/satellite_B/observations.csv';"

echo "ground_station:"
duckdb -c "SELECT COUNT(*) FROM 'providers/ground_station/observations.csv';"
