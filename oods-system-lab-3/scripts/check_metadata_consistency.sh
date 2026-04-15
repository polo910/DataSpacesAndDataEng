#!/bin/bash
for path in $(grep -o "providers/[^/ ]*/observations.csv" metadata_catalog/*.json)
do
    if [ -f "$path" ]; then
        echo "$path: EXISTS"
    else
        echo "$path: NOT FOUND"
    fi
done
