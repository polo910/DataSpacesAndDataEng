# -*- coding: utf-8 -*-
import os
import numpy as np
import rasterio
from rasterio.transform import from_origin

print("--- Tworzenie sztucznych danych satelitarnych ---")

# Upewniamy sie, ze folder istnieje
os.makedirs("assets/bands", exist_ok=True)

width = 300
height = 300

# Dowolne transformacje i profile wymagane przez rasterio
transform = from_origin(19.0, 51.0, 10, 10)

# Generujemy losowe macierze pikseli (normalny rozklad) imitujace pasma Red i NIR
# Red (Kanal 4) - srednia 1200, NIR (Kanal 8) - srednia 2500
red = np.random.normal(1200, 250, (height, width)).astype('float32')
nir = np.random.normal(2500, 500, (height, width)).astype('float32')

profile = {
    "driver": "GTiff",
    "height": height,
    "width": width,
    "count": 1,
    "dtype": "float32",
    "crs": "EPSG:4326",
    "transform": transform
}

# Zapisujemy plik B04 (Czerwony)
with rasterio.open("assets/bands/B04_10m.tif", "w", **profile) as dst:
    dst.write(red, 1)

# Zapisujemy plik B08 (Podczerwien)
with rasterio.open("assets/bands/B08_10m.tif", "w", **profile) as dst:
    dst.write(nir, 1)

print("Sukces! Utworzono pliki:")
print(" - assets/bands/B04_10m.tif")
print(" - assets/bands/B08_10m.tif")
