# -*- coding: utf-8 -*-
import os
import numpy as np
import rasterio
import matplotlib.pyplot as plt
from rasterio.transform import from_origin

print("--- Zadanie Praktyczne P1: Porownanie Dwoch Obserwacji (Chmury) ---")

os.makedirs("results/ndvi_comparison", exist_ok=True)
os.makedirs("reports", exist_ok=True)

width, height = 300, 300
transform = from_origin(19.0, 51.0, 10, 10)
profile = {"driver": "GTiff", "height": height, "width": width, "count": 1, "dtype": "float32", "crs": "EPSG:4326", "transform": transform}

# 1. Tworzenie dwoch zestawow danych: Bez chmur oraz Z chmurami
# Obserwacja A (czyste niebo)
red_A = np.random.normal(1200, 200, (height, width)).astype('float32')
nir_A = np.random.normal(2600, 400, (height, width)).astype('float32')
ndvi_A = (nir_A - red_A) / (nir_A + red_A + 1e-6)

# Obserwacja B (zaklocona chmurami - chmury maja b. wysokie odbicie w Red i niskie/srednie NDVI)
red_B = np.random.normal(1200, 200, (height, width)).astype('float32')
nir_B = np.random.normal(2600, 400, (height, width)).astype('float32')
# Nakladamy sztuczna wielka chmure w srodku macierzy (indeksy 50 do 200)
red_B[50:200, 50:200] = 9000.0  
nir_B[50:200, 50:200] = 9200.0
ndvi_B = (nir_B - red_B) / (nir_B + red_B + 1e-6)

# Mapy graficzne
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.imshow(ndvi_A, cmap='YlGn', vmin=-1, vmax=1)
plt.title("Obserwacja A (Niskie zachmurzenie)")
plt.colorbar()

plt.subplot(1, 2, 2)
plt.imshow(ndvi_B, cmap='YlGn', vmin=-1, vmax=1)
plt.title("Obserwacja B (Wysokie zachmurzenie)")
plt.colorbar()

plt.savefig("results/ndvi_comparison/ndvi_cloud_comparison.png")
plt.close()

# Generujemy osobne pojedyncze pliki wymagane przez instrukcje
plt.imshow(ndvi_A, cmap='YlGn', vmin=-1, vmax=1)
plt.savefig("results/ndvi_comparison/low_cloud_observation_ndvi_map.png")
plt.close()

plt.imshow(ndvi_B, cmap='YlGn', vmin=-1, vmax=1)
plt.savefig("results/ndvi_comparison/high_cloud_observation_ndvi_map.png")
plt.close()

# Zliczanie statystyk
high_veg_A = np.sum(ndvi_A > 0.5)
high_veg_B = np.sum(ndvi_B > 0.5)

with open("reports/multi_observation_ndvi_comparison.txt", "w") as f:
    f.write("POROWNANIE JAKOSCI NDVI DLA DWOCH OBSERWACJI\n")
    f.write("=============================================\n\n")
    f.write(f"OBSERWACJA A (Czysta): Srednie NDVI = {ndvi_A.mean():.4f}, Piksele bujnej roslinnosci = {high_veg_A}\n")
    f.write(f"OBSERWACJA B (Chmury): Srednie NDVI = {ndvi_B.mean():.4f}, Piksele bujnej roslinnosci = {high_veg_B}\n\n")
    f.write("WNIOSKI ANALITYCZNE:\n")
    f.write(" - Chmury drastycznie zaburzaja wskaznik roslinnosci, sprowadzajac jego wartosc w okolice zera (0.01).\n")
    f.write(" - Obserwacja B wykazuje falszywy zanik powierzchni zielonych z powodu przesloniecia terenu chmura.\n")
    f.write(" - Do operacyjnego monitorowania oraz trenowania modeli AI nalezy BEZWZGLEDNIE wybrac Obserwacje A.\n")

print("Zapisano pliki porownawcze w: results/ndvi_comparison/ oraz reports/multi_observation_ndvi_comparison.txt")
