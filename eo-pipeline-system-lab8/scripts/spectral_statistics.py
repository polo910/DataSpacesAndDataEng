# -*- coding: utf-8 -*-
import os
import rasterio
import numpy as np

print("--- Zadanie 4: Statystyki spektralne ---")

RASTER_FILES = {
    "B04_10m": "assets/bands/B04_10m.tif",
    "B08_10m": "assets/bands/B08_10m.tif"
}

os.makedirs("reports", exist_ok=True)

with open("reports/spectral_statistics.txt", "w") as f:
    f.write("STATYSTYKI SPEKTRALNE PASM\n")
    f.write("==========================\n\n")
    
    for name, path in RASTER_FILES.items():
        print("-" * 40)
        print("Analiza pasma:", name)
        f.write("Pasmo: " + name + " (" + path + ")\n")
        
        if os.path.exists(path):
            with rasterio.open(path) as src:
                # Wczytujemy pierwsza warstwe jako macierz numpy
                band = src.read(1)
                
                # Obliczamy podstawowe statystyki przy uzyciu numpy
                v_min = np.min(band)
                v_max = np.max(band)
                v_mean = np.mean(band)
                v_std = np.std(band)
                
                # Wyswietlamy w konsoli
                print(" MIN:", v_min)
                print(" MAX:", v_max)
                print(" MEAN (Srednia):", v_mean)
                print(" STD (Odchylenie):", v_std)
                
                # Zapisujemy do pliku tekstowego
                f.write(" MIN: " + str(v_min) + "\n")
                f.write(" MAX: " + str(v_max) + "\n")
                f.write(" MEAN: " + str(v_mean) + "\n")
                f.write(" STD: " + str(v_std) + "\n\n")
        else:
            print(" Brak pliku rastra! Wygeneruj najpierw sztuczne pasma.")
            f.write(" Stan: Brak pliku\n\n")
            
    # Odpowiedzi na pytania interpretacyjne z instrukcji laboratoriow
    f.write("INTERPRETACJA INZYNIERSKA:\n")
    f.write("1. Ktore pasmo zawiera wieksze wartosci srednie?\n")
    f.write("   Odp: Pasmo B08 (Near Infrared / Bliska podczerwien) ma znacznie wyzsza srednia niz B04 (Red).\n")
    f.write("2. Dlaczego roslinnosc moze zachowywac sie inaczej w obu pasmach?\n")
    f.write("   Odp: Zdrowa roslinnosc silnie pochlania swiatlo czerwone (B04) do fotosyntezy, a odbija podczerwien (B08).\n")
    f.write("3. Dlaczego te roznice sa wazne dla obliczania wskaznika NDVI?\n")
    f.write("   Odp: Poniewaz kontrast miedzy silnym odbiciem w podczerwieni a pochlanianiem w czerwieni pozwala jednoznacznie wykryc roslinnosc zywa.\n")

print("\nRaport statystyk zapisany w: reports/spectral_statistics.txt")
