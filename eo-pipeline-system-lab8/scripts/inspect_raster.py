# -*- coding: utf-8 -*-
import os
import rasterio

print("--- Zadanie 3: Inspekcja danych rastrowych ---")

# Lista plikow do sprawdzenia
RASTER_FILES = [
    "assets/bands/B04_10m.tif",
    "assets/bands/B08_10m.tif"
]

os.makedirs("reports", exist_ok=True)

# Otwieramy plik raportu do zapisu
with open("reports/raster_inspection.txt", "w") as f:
    f.write("RAPORT INSPEKCJI RASTROW\n")
    f.write("=========================\n\n")
    
    for path in RASTER_FILES:
        f.write("Sciezka pliku: " + path + "\n")
        print("-" * 40)
        print("Plik: " + path)
        
        if os.path.exists(path):
            with rasterio.open(path) as src:
                # Pobieramy metadane rastra
                w = src.width
                h = src.height
                bands = src.count
                crs = str(src.crs)
                bounds = str(src.bounds)
                
                # Wypisujemy na ekran
                print(" Szerokosc:", w)
                print(" Wysokosc:", h)
                print(" Liczba pasm:", bands)
                print(" CRS (Uklad wspolrzednych):", crs)
                print(" Granice (Bounds):", bounds)
                
                # Zapisujemy do pliku
                f.write(" Szerokosc: " + str(w) + "\n")
                f.write(" Wysokosc: " + str(h) + "\n")
                f.write(" Liczba pasm: " + str(bands) + "\n")
                f.write(" CRS: " + crs + "\n")
                f.write(" Granice: " + bounds + "\n\n")
        else:
            print(" Plik NIE istnieje! Uruchom najpierw: create_sample_bands.py")
            f.write(" Stan: Plik nie znaleziony w przestrzeni roboczej\n\n")

print("\nRaport zapisany w: reports/raster_inspection.txt")
