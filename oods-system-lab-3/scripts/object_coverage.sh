#!/bin/bash
all_objects=$(cat providers/*/observations.csv | cut -d',' -f1 | sort | uniq)
for obj in $all_objects
do
    count=$(grep -l "$obj" providers/*/observations.csv | wc -l)
    echo "Object $obj in $count providers"
done
