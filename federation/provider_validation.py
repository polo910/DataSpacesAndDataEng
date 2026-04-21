import json
import requests
with open("contracts/providers_registry.json", "r") as f:
	providers = json.load(f)
with open("contracts/observation_schema.json", "r") as f:
	contract = json.load(f)
required_fields = contract["required_fields"]
for provider in providers:
	provider_name = provider["name"]
	provider_url = provider["url"]
	try:
		response = requests.get(f"{provider_url}/observations", timeout=2)
		data = response.json()
		if len(data) == 0:
			print(provider_name, ": EMPTY DATASET")
			continue
		missing = [field for field in required_fields if field not in data[0]]
		if missing:
			print(provider_name, ": VIOLATION")
			print("Missing fields:", missing)
		else:
			print(provider_name, ": OK")
	except Exception:
		print(provider_name, ": UNAVAILABLE")
