# Federated EO Data Space for National Flood Monitoring

A lightweight, searchable Earth Observation (EO) resource catalogue designed for the **National Flood Monitoring Agency**. This system serves as a Federated Data Space that integrates satellite imagery, thematic products, and operational services from multiple independent providers (ESA, Copernicus EMS, and CLMS) into a unified dashboard to support emergency response and early warning activities during flood crises.

Developed as a mini-project for the **Data Spaces and Federated Data Engineering** course at **AGH University of Krakow**.

---

## 🌊 Project Overview & Architecture

During a flood emergency, operators face critical questions regarding flood extent, current observations, and resource selection under extreme conditions (e.g., heavy cloud cover or night-time operations). This project addresses these needs by creating an interconnected **Metadata Repository** and **Searchable Inventory** that unifies diverse EO assets into a common description framework while strictly preserving data provenance.

### Federated EO Resources Included:
1. **Sentinel-1 IW VV+VH (ESA / Copernicus):** Raw Synthetic Aperture Radar (SAR) imagery. Weather-independent (penetrates clouds) and operational at night, making it the primary asset for active flood detection during severe storms.
2. **Sentinel-2 (ESA / Copernicus):** High-resolution multispectral optical imagery. Ideal for post-flood damage grading and precise extent assessment under clear skies.
3. **CEMS Early Warning - GloFAS/EFAS (Copernicus EMS):** River discharge forecasts and hydrological models used for pre-flood risk analysis and early warnings.
4. **CLMS Bio-geophysical - Soil Moisture (Copernicus Land):** Grid models representing soil saturation levels, crucial for anticipating flash-flood risks from incoming rainfall.

---

## 🛠️ Technology Stack
- **Backend/Frontend:** Python 3.10+ & Streamlit (for building the reactive web interface and data container)
- **Data Management:** Pandas DataFrame (for dynamic filtering, tabular comparison, and metadata handling)

---

## 📁 Repository Structure

```text
federated-eo-data-space/
│
├── app.py               # Main application script containing the data container & UI logic
├── requirements.txt     # Python package dependencies
└── README.md            # Project documentation and deployment guide

```

---

## 🚀 Deployment & Local Installation

Follow these steps to set up a virtual environment and run the Federated Data Space application locally:

### 1. Clone the Repository

```bash
git clone [https://github.com/YOUR_GITHUB_USERNAME/federated-eo-data-space.git](https://github.com/YOUR_GITHUB_USERNAME/federated-eo-data-space.git)
cd federated-eo-data-space

```

### 2. Set Up a Virtual Environment (`venv`)

#### On Windows (Command Prompt / PowerShell):

```bash
python -m venv env
.\env\Scripts\activate

```

#### On macOS / Linux:

```bash
python3 -m venv env
source env/bin/activate

```

*Once activated, your terminal prompt will show `(env)`.*

### 3. Install Dependencies

Ensure your environment is active and install the required libraries:

```bash
pip install -r requirements.txt

```

### 4. Launch the Federated Data Space

Run the Streamlit application:

```bash
streamlit run app.py

```

The application will automatically open in your default browser at `http://localhost:8501`.

---

## 🎛️ Operational Features Demonstrated in the Video

The application directly fulfills all minimum operational and architectural requirements defined by the project specification:

* **Resource Browsing & Comparison:** A unified, tabular view allows rapid side-by-side comparison of sensor types, constraints, and operational roles.
* **Dynamic Situational Filtering:** The sidebar allows operators to check boxes like `Praca w nocy` or `Pełne zachmurzenie` to immediately filter down to resilient assets (e.g., hiding Sentinel-2 when cloud cover prevents optical observation).
* **Provenance & Direct Access:** Information about resource origin is fully preserved, and the system dynamically generates secure, direct URL hyperlinks to the original provider data stores or API endpoints.

---

## 📝 License & Academic Honesty

This project was implemented independently as individual laboratory coursework. All data structures, design decisions, and architectural features represent the author's own work in exploring the European Earth Observation ecosystem.
