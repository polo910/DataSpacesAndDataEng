#!/bin/bash
for file in ../providers/*/observations.csv
do
    count=$(wc -l < "$file")
    folder=$(basename "$(dirname "$file")")
    echo "$folder: $count"
done
