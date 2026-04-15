#!/bin/bash
for file in providers/*/observations.csv
do
    echo "Dostawca: $file"
    cut -d',' -f1 "$file" | sort | uniq -c
done
