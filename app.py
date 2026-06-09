import streamlit as st
import pandas as pd

# 1. Twój "kontener" z datasetami i ich cechami technicznymi
eo_database = [
    {
        "Nazwa zasobu": "Sentinel-1 IW VV+VH",
        "Dostawca": "ESA / Copernicus",
        "Typ danych": "Surowe zobrazowanie radarowe (SAR)",
        "Działa w nocy": "Tak",
        "Odporny na chmury": "Tak",
        "Rola operacyjna": "Wykrywanie powodzi (Flood detection)",
        "Link / API": "https://browser.dataspace.copernicus.eu/"
    },
    {
        "Nazwa zasobu": "Sentinel-2 (Optyczny)",
        "Dostawca": "ESA / Copernicus",
        "Typ danych": "Zobrazowanie optyczne (Multispectral)",
        "Działa w nocy": "Nie",
        "Odporny na chmury": "Nie",
        "Rola operacyjna": "Ocena zasięgu i strat (Flood extent / Grading)",
        "Link / API": "https://browser.dataspace.copernicus.eu/"
    },
    {
        "Nazwa zasobu": "CEMS Early Warning - GloFAS/EFAS",
        "Dostawca": "Copernicus EMS",
        "Typ danych": "Prognozy i modele hydrologiczne",
        "Działa w nocy": "Tak",
        "Odporny na chmury": "Tak",
        "Rola operacyjna": "Wczesne ostrzeganie (Early Warning)",
        "Link / API": "https://emergency.copernicus.eu/"
    },
    {
        "Nazwa zasobu": "CLMS Bio-geophysical - Soil Moisture",
        "Dostawca": "Copernicus Land (CLMS)",
        "Typ danych": "Model wilgotności gleby (Grid)",
        "Działa w nocy": "Tak",
        "Odporny na chmury": "Tak",
        "Rola operacyjna": "Analiza ryzyka (Pre-flood analysis)",
        "Link / API": "https://land.copernicus.eu/"
    }
]

# Konwersja do DataFrame (żeby Streamlit ładnie to wyświetlił w tabeli)
df = pd.DataFrame(eo_database)

# 2. Interfejs aplikacji
st.set_page_config(page_title="Federated EO Data Space", layout="wide")
st.title("🌊 Krajowy System Monitorowania Powodzi - Federated Data Space")
st.write("Uproszczony katalog zasobów Earth Observation wspierający zarządzanie kryzysowe.")

st.divider()

# 3. Panel boczny z filtrami (Użytkownik klika, co potrzebuje w danym momencie)
st.sidebar.header("🎛️ Filtry sytuacji operacyjnej")

filter_night = st.sidebar.checkbox("Praca w nocy (Night operations)")
filter_clouds = st.sidebar.checkbox("Pełne zachmurzenie (Cloudy conditions)")

# Logika filtrowania bazy danych
filtered_df = df.copy()

if filter_night:
    filtered_df = filtered_df[filtered_df["Działa w nocy"] == "Tak"]

if filter_clouds:
    filtered_df = filtered_df[filtered_df["Odporny na chmury"] == "Tak"]

# 4. Wyświetlanie wyników
st.subheader("📋 Dostępne i rekomendowane zasoby danych:")
if not filtered_df.empty:
    # Wyświetlamy jako ładną, interaktywną tabelę
    st.dataframe(filtered_df, use_container_width=True)
    
    # Dodatkowe ułatwienie: szczegółowy podgląd wybranego elementu
    st.write("---")
    st.subheader("🔍 Szczegóły i bezpośredni dostęp")
    selected_resource = st.selectbox("Wybierz zasób z listy, aby uzyskać link dostępu:", filtered_df["Nazwa zasobu"])
    
    row = filtered_df[filtered_df["Nazwa zasobu"] == selected_resource].iloc[0]
    st.info(f"**Opis zastosowania:** {row['Rola operacyjna']}\n\n🔗 **Punkt dostępu (URL/API):** [{row['Link / API']}]({row['Link / API']})")
else:
    st.error("Brak zasobów spełniających wybrane kryteria! Zmień ustawienia filtrów.")
