#!/bin/bash
{
    echo "DATA SPACE HEALTH REPORT"
    echo "Total datasets: $(ls providers/*/observations.csv | wc -l)"
    echo "Orphan datasets: $(./scripts/detect_orphan_data.sh | wc -l)"
} > reports/data_space_health.txt
