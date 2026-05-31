# -*- coding: utf-8 -*-
import os
import numpy as np
import matplotlib.pyplot as plt

print("--- Zadanie 6: Wizualizacja i analiza NDVI ---")

ndvi_path = "results/ndvi/ndvi.npy"

if not os.path.exists(ndvi_path):
    print("Blad: Brak pliku npy! Uruchom najpierw ndvi_pipeline.py")
    exit()

# Wczytujemy tablice numpy wygenerowana w poprzednim kroku
ndvi = np.load(ndvi_path)

# Obliczamy statystyki pikseli
n_min = float(ndvi.min())
n_max = float(ndvi.max())
n_mean = float(ndvi.mean())

# Zliczamy piksele spelniajace kryteria (np.sum traktuje True jako 1, a False jako 0)
high_veg = int(np.sum(ndvi > 0.5))
low_ndvi = int(np.sum(ndvi < 0))
total_pixels = int(ndvi.size)

# Procenty
high_veg_pct = (high_veg / total_pixels) * 100
low_ndvi_pct = (low_ndvi / total_pixels) * 100

print("NDVI VISUALIZATION")
print("=" * 50)
print("NDVI MIN:", n_min)
print("NDVI MAX:", n_max)
print("NDVI MEAN:", n_mean)
print("WYSOKA ROSLINNOSC (NDVI > 0.5):", high_veg, f"({high_veg_pct:.2f}%)")
print("NISKIE NDVI / WODA (NDVI < 0):", low_ndvi, f"({low_ndvi_pct:.2f}%)")

# Generujemy mape graficzna za pomoca Matplotlib
plt.figure(figsize=(8, 6))
# Uzywamy mapy kolorow 'YlGn' (Yellow-Green), ktora idealnie pasuje do roslinnosci
plt.imshow(ndvi, cmap='YlGn', vmin=-1, vmax=1)
plt.colorbar(label='Wartosc Wskaznika NDVI')
plt.title('Mapa Wskaznika NDVI (Symulacja Satelitarna)')

# Zapisujemy wykres do pliku graficznego
plt.savefig("results/ndvi/ndvi_map.png")
plt.close()
print("Zapisano obraz mapy: results/ndvi/ndvi_map.png")

# Zapisujemy raport analizy tekstowej
os.makedirs("reports", exist_ok=True)
with open("reports/ndvi_analysis.txt", "w") as f:
    f.write("RAPORT ANALIZY WSKAZNIKA NDVI\n")
    f.write("==============================\n\n")
    f.write("Plik zrodlowy tablicy: " + ndvi_path + "\n")
    f.write("Wygenerowana mapa: results/ndvi/ndvi_map.png\n\n")
    f.write("Statystyki zbioru pikseli:\n")
    f.write(" - Minimalne NDVI: " + str(n_min) + "\n")
    f.write(" - Maksymalne NDVI: " + str(n_max) + "\n")
    f.write(" - Srednie NDVI: " + str(n_mean) + "\n")
    f.write(" - Liczba pikseli gstej roslinnosci (NDVI > 0.5): " + str(high_veg) + f" ({high_veg_pct:.2f}%)\n")
    f.write(" - Liczba pikseli niskiego NDVI (NDVI < 0): " + str(low_ndvi) + f" ({low_ndvi_pct:.2f}%)\n\n")
    f.write("INTERPRETACJA INZYNIERSKA:\n")
    f.write(" Obszary o wysokim wskazniku NDVI (>0.5) reprezentuja zdrowa, gęstą roślinność (lasy, pola uprawne).\n")
    f.write(" Obszary o ujemnym NDVI reprezentuja akweny wodne lub glebokie cienie terenowe.\n")
    f.write(" Brak bezposredniego wplywu zachmurzenia (cloud contamination), poniewaz dane wejsciowe byly syntetyczne.\n")

print("Zapisano raport tekstowy: reports/ndvi_analysis.txt")
