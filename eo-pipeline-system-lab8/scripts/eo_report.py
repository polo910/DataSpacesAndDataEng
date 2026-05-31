# -*- coding: utf-8 -*-
import os
import numpy as np
import rasterio

print("--- Zadanie 8: Zbiorczy Raport Przetwarzania EO ---")

REPORT_FILE = "reports/eo_processing_report.txt"
os.makedirs("reports", exist_ok=True)

# Definiujemy sprawdzane pliki projektu
ASSET_PATHS = {
    "Miniatura (thumbnail)": "assets/thumbnails/thumbnail.jpg",
    "Pasmo Czerwone (B04)": "assets/bands/B04_10m.tif",
    "Pasmo Podczerwieni (B08)": "assets/bands/B08_10m.tif",
    "Macierz NumPy NDVI (.npy)": "results/ndvi/ndvi.npy",
    "Wizualizacja Mapy NDVI (.png)": "results/ndvi/ndvi_map.png"
}

print("Budowanie pelnego zestawienia inzynierskiego...")

with open(REPORT_FILE, "w") as f:
    f.write("====================================================\n")
    f.write("   ZBIORCZY OPERACYJNY RAPORT PRZETWARZANIA SYSTEMU EO\n")
    f.write("====================================================\n\n")
    
    # Sekcja 1: Status plikow wynikowych
    f.write("1. STATUS GENEROWANYCH ZASOBOW ARTEFAKTOW:\n")
    for name, path in ASSET_PATHS.items():
        if os.path.exists(path):
            f.write(f" - [DOSTEPNY] {name} -> Sciezka: {path}\n")
        else:
            f.write(f" - [BRAK]    {name} (Uruchom odpowiedni skrypt pipeline!)\n")
            
    # Sekcja 2: Statystyki rastrów
    f.write("\n2. METADANE GEOPRZESTRZENNE PASM WEJSCIOWYCH:\n")
    test_band = "assets/bands/B04_10m.tif"
    if os.path.exists(test_band):
        with rasterio.open(test_band) as src:
            f.write(f" - Rozdzielczosc/Wymiary: {src.width} x {src.height} px\n")
            f.write(f" - System odniesienia CRS: {src.crs}\n")
            f.write(f" - Wspolrzedne graniczne: {src.bounds}\n")
    else:
        f.write(" - Brak plikow wejsciowych pasm do zbadania metadanych.\n")
        
    # Sekcja 3: Statystyki NDVI
    f.write("\n3. STATYSTYKI ANALITYCZNE PRODUKTU NDVI:\n")
    npy_path = "results/ndvi/ndvi.npy"
    if os.path.exists(npy_path):
        ndvi = np.load(npy_path)
        f.write(f" - Minimum NDVI: {ndvi.min():.4f}\n")
        f.write(f" - Maksimum NDVI: {ndvi.max():.4f}\n")
        f.write(f" - Srednia arytmetyczna: {ndvi.mean():.4f}\n")
        
        # Ocena dominacji
        high_veg = np.sum(ndvi > 0.5)
        pct_veg = (high_veg / ndvi.size) * 100
        f.write(f" - Udzial wysokiej roslinnosci: {pct_veg:.2f}%\n")
        f.write("\n Ocena Środowiskowa: ")
        if pct_veg > 30:
            f.write("Wykryto wysoka dominacje szaty roslinnej na badanym obszarze.\n")
        else:
            f.write("Obszar o przewadze terenu zurbanizowanego, nieuzytkow lub cieków wodnych.\n")
    else:
        f.write(" - Brak pliku ndvi.npy do wyznaczenia statystyk zbiorczych.\n")
        
    # Sekcja 4: Podsumowanie Rankingu
    f.write("\n4. SKROCONE WYNIKI RANKINGU METADANYCH STAC:\n")
    ranking_txt = "reports/observation_ranking.txt"
    if os.path.exists(ranking_txt):
        with open(ranking_txt, "r") as rf:
            lines = rf.readlines()
            # Przepisujemy pierwsze 15 linii rankingu, zeby nie przepelnic raportu glosnego
            for line in lines[:12]:
                f.write("   " + line)
    else:
        f.write(" - Brak wczesniejszego pliku rankingu metadanych.\n")

print("Zapisano glowny zbiorczy raport: reports/eo_processing_report.txt")
