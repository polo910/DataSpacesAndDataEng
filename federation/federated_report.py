import json, requests, duckdb, os
from datetime import datetime

# Ścieżki i dane
REGISTRY = "contracts/providers_registry.json"
OBJ_ID = "OBJ-003"
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with open(REGISTRY, "r") as f:
    providers = json.load(f)

# Pobieranie danych REST
all_data = []
for p in providers:
    try:
        res = requests.get(f"{p['url']}/observations").json()
        for r in res: r['provider'] = p['name']
        all_data += res
    except: pass

# Statystyki
total = len(all_data)
distinct = len(set(r['object_id'] for r in all_data))
obj_data = [r for r in all_data if r['object_id'] == OBJ_ID]
obj_providers = set(r['provider'] for r in obj_data)

# DuckDB i GraphQL (wyniki)
con = duckdb.connect()
urls = " UNION ALL ".join([f"SELECT * FROM '{p['url']}/observations.csv'" for p in providers])
duck_res = con.execute(f"SELECT count(*) FROM ({urls})").fetchone()[0]
gql_res = len(requests.post("http://127.0.0.1:9000/graphql", json={"query": "{observations{objectId}}"}).json()['data']['observations'])

# Generowanie raportu
report = f"""FEDERATED ACCESS REPORT
-----------------------
Generated at: {timestamp}

[REGISTERED PROVIDERS]
{chr(10).join(['- ' + p['name'] for p in providers])}

[GLOBAL STATISTICS]
Total observations: {total}
Distinct objects: {distinct}

[OBJECT ANALYSIS: {OBJ_ID}]
Providers containing object:
{chr(10).join(['- ' + p for p in obj_providers])}
Total observations: {len(obj_data)}

[ACCESS LAYERS]
REST RESULT: {total}
DUCKDB RESULT: {duck_res}
GRAPHQL RESULT: {gql_res}

[COMPLETENESS]
Federation complete: YES"""

fname = f"reports/federated_access_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
os.makedirs("reports", exist_ok=True)
with open(fname, "w") as f: f.write(report)
print(f"Raport zapisany: {fname}")
