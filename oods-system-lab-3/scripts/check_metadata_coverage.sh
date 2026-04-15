#!/bin/bash
for dir in providers/*/
do
    provider=$(basename "$dir")
    if ls metadata_catalog/ | grep -q "$provider"; then
        echo "$provider: OK"
    else
        echo "$provider: MISSING"
    fi
done
