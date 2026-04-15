#!/bin/bash

count=0

for file in ../providers/*/observations.csv
do
    grep "$1" "$file"
    c=$(grep -c "$1" "$file")
    count=$((count + c))
done

echo "Total matches: $count"
