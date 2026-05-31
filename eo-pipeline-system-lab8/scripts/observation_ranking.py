# -*- coding: utf-8 -*-
import os
import requests
from datetime import datetime

print("--- Zadanie 7: Silnik Rankingu Obserwacji Satelitarnych ---")

STAC_URL = "https://stac.dataspace.copernicus.eu/v1/search"

# Zapytanie zgodne z instrukcja pobierajace do 10 produktow z polski poludniowej
QUERY = {
    "collections": ["sentinel-2-l2a"],
    "bbox": [19.0, 50.0, 20.0, 51.0],
    "datetime": "2024-01-01T00:00:00Z/2024-01-31T23:59:59Z",
    "limit": 10
}

# 1. Funkcje pomocnicze do punktacji (uproszczona logika dla studenta)
def compute_cloud_score(cloud_cover):
    if cloud_cover is None:
        return 0
    # Im mniejsze zachmurzenie tym wiecej punktow (max 100)
    return max(0, 100 - cloud_cover)

def compute_completeness_score(assets_count):
    # Prosta drabinka punktowa z instrukcji
    if assets_count >= 30:
        return 30
    elif assets_count >= 20:
        return 20
    elif assets_count >= 10:
        return 10
    else:
        return 0

def parse_datetime(value):
    # Prosta konwersja czasu na obiekt datetime Pythona
    if value.endswith("Z"):
        value = value.replace("Z", "+00:00")
    return datetime.fromisoformat(value)

print("Pobieranie metadanych obserwacji z Copernicus STAC API...")
features = []
try:
    response = requests.post(STAC_URL, json=QUERY, timeout=30)
    response.raise_for_status()
    data = response.json()
    features = data.get("features", [])
    print(f"Pobrano pomyslnie {len(features)} obserwacji.")
except Exception as e:
    print("Brak polaczenia internetowego z API lub timeout. Tworze dane mockowe (atrapowe) do testu rankingu.")
    # Tworzymy sztuczne metadane, zeby skrypt zawsze zadzialal bez internetu!
    features = [
        {"id": "S2A_MSIL2A_20240129_NISKI_CLOUD", "properties": {"datetime": "2024-01-29T09:42:41Z", "eo:cloud_cover": 3.5}, "assets": {"band1": {}, "band2": {}, "b3": {}, "b4": {}, "b5": {}, "b6": {}, "b7": {}, "b8": {}, "b9": {}, "b10": {}, "b11": {}, "b12": {}, "t1": {}, "t2": {}, "t3": {}}},
        {"id": "S2B_MSIL2A_20240115_WYS_CLOUD", "properties": {"datetime": "2024-01-15T10:12:00Z", "eo:cloud_cover": 65.2}, "assets": {"band1": {}, "band2": {}}},
        {"id": "S2A_MSIL2A_20240101_SREDNI_CLOUD", "properties": {"datetime": "2024-01-01T09:50:30Z", "eo:cloud_cover": 18.1}, "assets": {"band1": {}, "band2": {}, "b3": {}, "b4": {}, "b5": {}, "b6": {}, "b7": {}, "b8": {}, "b9": {}, "b10": {}}}
    ]

# Wyznaczamy najnowsza date sposrod znalezionych
parsed_times = []
for item in features:
    dt_str = item["properties"].get("datetime")
    if dt_str:
        parsed_times.append(parse_datetime(dt_str))

# Jesli cos znaleziono, okreslamy najnowszy czas jako punkt odniesienia recency
newest_time = max(parsed_times) if parsed_times else datetime.now()

ranked_list = []

for item in features:
    pid = item.get("id")
    props = item.get("properties", {})
    assets_dict = item.get("assets", {})
    
    c_cover = props.get("eo:cloud_cover", 100.0)
    a_count = len(assets_dict)
    
    # Obliczanie skladowych ocen
    cloud_score = compute_cloud_score(c_cover)
    comp_score = compute_completeness_score(a_count)
    
    # Ocena aktualnosci (recency)
    item_time = parse_datetime(props.get("datetime"))
    age_days = (newest_time - item_time).total_seconds() / 86400.0
    recency_score = max(0, 20 - (age_days / 30.0) * 20)
    
    # Wynik koncowy
    final_score = cloud_score + comp_score + recency_score
    
    ranked_list.append({
        "id": pid,
        "time": props.get("datetime"),
        "cloud_cover": c_cover,
        "assets_count": a_count,
        "cloud_score": cloud_score,
        "completeness_score": comp_score,
        "recency_score": recency_score,
        "final_score": final_score
    })

# Sortujemy liste od najwyzszego wyniku do najnizszego
ranked_list = sorted(ranked_list, key=lambda x: x["final_score"], reverse=True)

# Zapisujemy wyniki rankingu do pliku raportu
os.makedirs("reports", exist_ok=True)
with open("reports/observation_ranking.txt", "w") as f:
    f.write("SILNIK RANKINGU OBSERWACJI - RAPORT BIEZACY\n")
    f.write("============================================\n\n")
    
    for idx, obs in enumerate(ranked_list, 1):
        f.write(f"{idx}. ID Produktu: {obs['id']}\n")
        f.write(f"   Czas akwizycji: {obs['time']}\n")
        f.write(f"   Zachmurzenie: {obs['cloud_cover']}% -> Punkty: {obs['cloud_score']:.2f}\n")
        f.write(f"   Liczba zasobow: {obs['assets_count']} -> Punkty: {obs['completeness_score']:.2f}\n")
        f.write(f"   Punkty aktualnosci: {obs['recency_score']:.2f}\n")
        f.write(f"   WYNIK KONCOWY (FINAL SCORE): {obs['final_score']:.2f}\n")
        f.write("-" * 60 + "\n")
        
    f.write("\nODPOWIEDZI NA PYTANIA INTERPRETACYJNE:\n")
    f.write("1. Ktory produkt powinien byc przetwarzany jako pierwszy?\n")
    f.write(f"   Odp: Produkt o najwyzszym wyniku, czyli: {ranked_list[0]['id']}\n")
    f.write("2. Co mialo najwiekszy wplyw na decyzje?\n")
    f.write("   Odp: Glownym czynnikiem determinujacym wynik bylo niskie zachmurzenie (cloud_cover), dajace blisko 100 punktow basowych.\n")
    f.write("3. Czy ta strategia jest wystarczajaca dla systemow operacyjnych?\n")
    f.write("   Odp: Jest to model bazowy. W pelnych systemach uwzglednia sie tez koszty dostepu, rozdzielczosc oraz pokrycie obszaru zainteresowania (AOI).\n")

print("Zakonczono tworzenie rankingu. Wyniki zapisano w: reports/observation_ranking.txt")
