#!/bin/bash

REPORT_FILE="../reports/data_space_report.txt"
QUERY="OBJ-003"

echo "DATA SPACE REPORT" > "$REPORT_FILE"

# Total datasets
echo "Total datasets: $(ls ../providers/*/observations.csv 2>/dev/null | wc -l)" | tee -a "$REPORT_FILE"

# Total records
total=0
for f in ../providers/*/observations.csv; do
    [ -f "$f" ] && total=$((total + $(wc -l < "$f")))
done
echo "Total records: $total" | tee -a "$REPORT_FILE"

# Objects found for query OBJ-003 (distributed)
dist=$(./search_distributed.sh "$QUERY" | grep "Total matches" | awk '{print $3}')
# Objects found for query OBJ-003 (federated)
fed=$(./search_federated.sh "$QUERY" | grep "Total matches" | awk '{print $3}')

echo "Objects found for query $QUERY: $dist" | tee -a "$REPORT_FILE"
echo "Consistency check: $( [ "$dist" -eq "$fed" ] && echo YES || echo NO )" | tee -a "$REPORT_FILE"

echo "Report saved to $REPORT_FILE"
