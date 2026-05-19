import os
import requests

STAC_URL = "https://stac.dataspace.copernicus.eu/v1/search"

# Zapytanie z poprawnym formatem daty i czasu (ISO 8601 z separatorami)
QUERY = {
    "collections": ["sentinel-2-l2a"],
    "bbox": [19.0, 50.0, 20.0, 51.0],
    "datetime": "2024-01-01T00:00:00Z/2024-01-31T23:59:59Z",
    "query": {
        "eo:cloud_cover": {
            "lt": 20
        }
    },
    "limit": 1
}

# Spójne mapowanie z oryginalnym rozszerzeniem .jp2 (obsługiwanym przez rasterio)
OUTPUT_PATHS = {
    "thumbnail": "assets/thumbnails/thumbnail.jpg",
    "TCI_10m": "assets/visual/visual.jp2",
    "B04_10m": "assets/bands/B04_10m.jp2",
    "B08_10m": "assets/bands/B08_10m.jp2"
}

def is_http_url(url):
    return (
        url.startswith("http://")
        or url.startswith("https://")
    )

def download_file(url, output_path):
    # Jeśli URL to ścieżka lokalna Copernicus (/eodata/...), zamieniamy ją na pełny adres URL
    if url.startswith("/eodata/"):
        url = "https://download.dataspace.copernicus.eu" + url

    if not is_http_url(url):
        print(
            "SKIPPED NON-HTTP ASSET:",
            url
        )
        return False

    # Tworzenie struktury katalogów na dysku, jeśli nie istnieją
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    response = requests.get(
        url,
        timeout=120
    )
    response.raise_for_status()
    with open(output_path, "wb") as f:
        f.write(response.content)
    return True

# Wysłanie zapytania do API STAC
response = requests.post(
    STAC_URL,
    json=QUERY
)
data = response.json()
item = data["features"][0]
assets = item["assets"]

print(
    "AVAILABLE ASSETS:"
)
for asset_name in assets:
    print(
        asset_name
    )

print("\n--- STARTING DOWNLOAD PROCESS ---")

downloaded_count = 0
skipped_count = 0
failed_count = 0

# Pobieranie wybranych zasobów zdefiniowanych w OUTPUT_PATHS
for asset_name, output_path in OUTPUT_PATHS.items():
    if asset_name in assets:
        asset_url = assets[asset_name].get("href")
        print(f"Downloading {asset_name}...")
        try:
            success = download_file(asset_url, output_path)
            if success:
                print(f"SUCCESS: Saved to {output_path}")
                downloaded_count += 1
            else:
                skipped_count += 1
        except Exception as e:
            print(f"FAILED to download {asset_name}: {e}")
            failed_count += 1
    else:
        print(f"Asset '{asset_name}' not found in API response. Skipping.")
        skipped_count += 1

# Generowanie krótkiego raportu podsumowującego
print("\n" + "="*30)
print("       DOWNLOAD REPORT       ")
print("="*30)
print(f"Successfully downloaded: {downloaded_count}")
print(f"Skipped assets:          {skipped_count}")
print(f"Failed downloads:        {failed_count}")
print(f"Total processed:         {downloaded_count + skipped_count + failed_count}")
print("="*30)
