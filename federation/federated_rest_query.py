import json
import requests
with open("contracts/providers_registry.json", "r") as f:
	providers = json.load(f)
all_results = []
for provider in providers:
	provider_name = provider["name"]
	provider_url = provider["url"]
	response = requests.get(f"{provider_url}/observations")
	data = response.json()
	for row in data:
		row["provider"] = provider_name
		all_results.append(row)
print("TOTAL RECORDS:", len(all_results))
for row in all_results:
	print(row)
