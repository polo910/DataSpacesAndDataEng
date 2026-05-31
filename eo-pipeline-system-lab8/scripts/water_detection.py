# -*- coding: utf-8 -*-
import os
import numpy as np
import matplotlib.pyplot as plt

print("--- Zadanie Praktyczne P2: Detekcja Zbiornikow Wodnych ---")

ndvi_path = "results/ndvi/ndvi.npy"

if not os.path.exists(ndvi_path):
    print("Blad: Brak pliku bazowego ndvi.npy! Uruchom najpierw: ndvi_pipeline.py")
    exit()

ndvi = np.load(ndvi_path)

# Regula detekcji: woda ma ujemne wartosci NDVI (NDVI < 0)
water_mask = ndvi < 0

water_pixels = int(np.sum(water_mask))
non_water_pixels = int(np.sum(~water_mask))
total = int(ndvi.size)
water_percentage = (water_pixels / total) * 100

print(f" Wykryto {water_pixels} pikseli wody, co stanowi {water_percentage:.2f}% obszaru.")

# Zapisujemy tablice logiczna w formacie numpy
np.save("results/ndvi/water_mask.npy", water_mask)

# Tworzymy rysunek maski binarnej (czarno-bialy lub niebieski)
plt.figure(figsize=(7, 6))
plt.imshow(water_mask, cmap='Blues')
plt.title("Maska Binarna Wykrytej Wody (NDVI < 0)")
plt.colorbar(label="0: Lad, 1: Woda")
plt.savefig("results/ndvi/water_mask.png")
plt.close()

# Raport tekstowy
os.makedirs("reports", exist_ok=True)
with open("reports/water_detection.txt", "w") as f:
    f.write("TEMATYCZNY RAPORT DETEKCJI WODY POWIERZCHNIOWEJ\n")
    f.write("===============================================\n\n")
    f.write(f"Regula klasyfikacji binarnej: NDVI < 0\n")
    f.write(f"Statystyki pikseli:\n")
    f.write(f" - Piksele sklasyfikowane jako woda: {water_pixels}\n")
    f.write(f" - Piksele sklasyfikowane jako lad: {non_water_pixels}\n")
    f.write(f" - Procentowa zawartosc wody na zdjęciu: {water_percentage:.2f}%\n\n")
    f.write("INTERPRETACJA INZYNIERSKA:\n")
    f.write(" Prog progowania NDVI < 0 jest prosta i skuteczna metoda wstepnej segmentacji zbiornikow wodnych.\n")
    f.write(" Nalezy jednak pamietac, ze gleboki cien gorski lub dachy niektorych budynkow moga rowniez dawac wynik ujemny.\n")
    f.write(" Produkt ten stanowi idealne wejscie (maske warunkowa) dla algorytmow klasyfikacji maszynowej AI.\n")

print("Zapisano wyniki detekcji wody: results/ndvi/water_mask.png oraz reports/water_detection.txt")
