#!/bin/bash

d=$(./search_distributed.sh "$1" | grep "Total matches" | awk '{print $3}')
f=$(./search_federated.sh "$1" | grep "Total matches" | awk '{print $3}')

echo "Distributed: $d"
echo "Federated: $f"

if [ "$d" -eq "$f" ]; then
    echo "Consistency: YES"
else
    echo "Consistency: NO"
fi
