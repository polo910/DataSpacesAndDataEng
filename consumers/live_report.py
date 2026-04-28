import requests
import json
import os
from datetime import datetime

BROKER_URL = "http://127.0.0.1:7000/events"
CONTRACT_PATH = "../contracts/event_schema.json"
REGISTRY_PATH = "../contracts/providers_registry.json"
SELECTED_OBJ = "OBJ-003"

def create_report():
    try:
        events = requests.get(BROKER_URL).json()
        with open(CONTRACT_PATH, "r") as f:
            fields = json.load(f)["required_fields"]
        with open(REGISTRY_PATH, "r") as f:
            expected = [p["name"] for p in json.load(f)]

        # Przetwarzanie
        valid = [e for e in events if all(f in e for f in fields)]
        invalid_cnt = len(events) - len(valid)
        active = sorted(set(e["provider"] for e in valid))
        missing = sorted(set(expected) - set(active))
        
        counts = {}
        for e in valid:
            counts[e["provider"]] = counts.get(e["provider"], 0) + 1
            
        distinct_objs = len(set(e["object_id"] for e in valid))
        sel_count = sum(1 for e in valid if e["object_id"] == SELECTED_OBJ)

        # Składanie raportu
        now = datetime.now()
        report = f"""REAL-TIME FEDERATION REPORT
---------------------------
Generated at: {now.strftime("%Y-%m-%d %H:%M:%S")}

[STREAM STATUS]
Total events: {len(events)}
Valid events: {len(valid)}
Invalid events: {invalid_cnt}

[PROVIDERS]
Active providers:
{chr(10).join('- ' + p for p in active) if active else "- none"}
Missing providers:
{chr(10).join('- ' + p for p in missing) if missing else "- none"}

[PER-PROVIDER COUNTS]
{chr(10).join(f"{k}: {v}" for k, v in counts.items())}

[OBJECT STATISTICS]
Distinct objects: {distinct_objs}
{SELECTED_OBJ} observations: {sel_count}

[FEDERATION STATUS]
COMPLETE: {"YES" if not missing else "NO"}
"""
        # Zapis do pliku
        os.makedirs("reports", exist_ok=True)
        filename = f"reports/stream_report_{now.strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, "w") as f:
            f.write(report)
        print(f"Report saved to {filename}")

    except Exception as e:
        print(f"Failed to generate report: {e}")

if __name__ == "__main__":
    create_report()
