#!/bin/bash
res1=$(./scripts/search_distributed.sh OBJ-003 | tail -n 1)
res2=$(./scripts/search_federated.sh OBJ-003 | wc -l)
echo "Dist: $res1, Fed: $res2"
