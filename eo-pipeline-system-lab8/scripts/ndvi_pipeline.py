# -*- coding: utf-8 -*-
import os
import rasterio
import numpy as np

print("--- Zadanie 5: Obliczanie wskaznika NDVI ---")

b04_path = "assets/bands/B04_10m.tif"
b08_path = "assets/bands/B08_10m.tif"

if not os.path.exists(b04_path) or not os.path.exists(b08_path):
    print("Blad: Brak plikow wejsciowych w assets/bands/! Uruchom create_sample_bands.py")
    exit()

# Otwieramy pasma i wczytujemy dane jako typ float, zeby dzielenie dzialalo prawidlowo
with rasterio.open(b04_path) as red_src:
    red = red_src.read(1).astype(float)

with rasterio.open(b08_path) as nir_src:
    nir = nir_src.read(1).astype(float)

# Wzor na NDVI: (NIR - RED) / (NIR + RED)
# Dodajemy mala wartosc 1e-6, zeby uniknac bledu dzielenia przez zero (tzw. epsilon)
ndvi = (nir - red) / (nir + red + 1e-6)

print("Zakonczono obliczenia NDVI.")
print(" NDVI MIN:", ndvi.min())
print(" NDVI MAX:", ndvi.max())

# Tworzymy folder na wyniki i zapisujemy tablice NumPy (.npy)
os.makedirs("results/ndvi", exist_ok=True)
np.save("results/ndvi/ndvi.npy", ndvi)
print("Zapisano plik tablicy: results/ndvi/ndvi.npy")
