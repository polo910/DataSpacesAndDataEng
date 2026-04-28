import requests
import time
import json

# Adresy i pliki
BROKER_URL = "http://127.0.0.1:7000/events"
CONTRACT_PATH = "../contracts/event_schema.json"
REGISTRY_PATH = "../contracts/providers_registry.json"
SELECTED_OBJ = "OBJ-003"

# Progi dla zadania Task P5
TEMP_THRESHOLD = 25.0
VELOCITY_THRESHOLD = 100.0

while True:
    try:
        # Pobieranie danych [cite: 84, 156]
        response = requests.get(BROKER_URL)
        events = response.json()
        
        # Wczytywanie kontraktów [cite: 136, 314]
        with open(CONTRACT_PATH, "r") as f:
            required_fields = json.load(f)["required_fields"]
        with open(REGISTRY_PATH, "r") as f:
            expected_providers = [p["name"] for p in json.load(f)]

        valid_events = []
        invalid_count = 0

        for e in events:
            # Walidacja kontraktu (Task 10) [cite: 316, 336]
            if all(field in e for field in required_fields):
                valid_events.append(e)
                
                # ALERT P4: Detekcja konkretnego obiektu [cite: 382]
                if e["object_id"] == SELECTED_OBJ:
                    print(f"!!! ALERT: {e['object_id']} observed by {e['provider']} at {e['timestamp']} !!!")

                # ALERT P5: Przekroczenie progów [cite: 383]
                if e["temperature"] > TEMP_THRESHOLD:
                    print(f"WARNING: High Temp! Provider: {e['provider']}, Value: {e['temperature']}")
                if e["velocity"] > VELOCITY_THRESHOLD:
                    print(f"WARNING: High Velocity! Provider: {e['provider']}, Value: {e['velocity']}")
            else:
                invalid_count += 1

        # Statystyki (Task 7, 8) [cite: 243, 270]
        print(f"\n[SUMMARY] Total events: {len(events)} | Valid: {len(valid_events)} | Invalid: {invalid_count}")
        
        if valid_events:
            per_provider = {}
            for e in valid_events:
                p = e["provider"]
                per_provider[p] = per_provider.get(p, 0) + 1
            
            print(f"PER-PROVIDER: {per_provider}")
            print(f"DISTINCT OBJECTS: {len(set(e['object_id'] for e in valid_events))}")

        # Analiza kompletności (Task 9) [cite: 298, 299]
        active_providers = set(e["provider"] for e in valid_events)
        missing_providers = sorted(set(expected_providers) - active_providers)
        
        print(f"MISSING PROVIDERS: {missing_providers if missing_providers else 'none'}")
        print(f"FEDERATION COMPLETE: {'YES' if not missing_providers else 'NO'}")
        print("-" * 50)

    except Exception as e:
        print(f"ERROR: {e}")

    time.sleep(3) # Polling (Task 7) [cite: 39, 242]
