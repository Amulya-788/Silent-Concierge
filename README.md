# Silent Concierge — Luxury Retail Edge Clienteling Engine

**Silent Concierge** is an edge-first luxury retail clienteling and backroom RFID curation engine designed for high-jewelry and couture maisons (modeled on Christian Dior / LVMH Paris–Bengaluru boutique operations).

## 1. Core Architectural Pillars

### Ephemeral BLE & 24-Hour Appointment Privacy Gate (Zero-PII at Rest)

* **GDPR Vault Locked (`LOCKED_AT_REST`)**: Client purchase vectors reside encrypted at the edge with zero personally identifiable information (PII), style DNA, or archive history exposed on the Sales Associate terminal.

* **Doorway BLE Handshake (`LAYER_1_DOORWAY_BLE`)**: Triggered when a client's Apple Wallet PassKit token wakes via ceiling iBeacon (`DIOR-BLR-DOOR01`), temporarily unlocking the client dossier, sister-boutique handoff note, and verified sizing for the active session.

* **24-Hour Pre-Arrival Token (`TOMORROW_24H_APPOINTMENT_KEY`)**: Grants temporary pre-arrival access for scheduled private salon appointments.

### Size-Delta Gift Filtering

High-net-worth clients frequently purchase gifts for family or associates that distort standard collaborative filtering models. Silent Concierge compares every historical transaction against the client's verified `core_rtw_size` and `core_shoe_size` (plus `gift_receipt_flag` for leather goods and high jewelry), stripping out gift transactions before computing the client's personal Style DNA.

### Luxury Consumer Psychology & Sqrt-Weighted Euclidean Matching

Within each product category (`Ready-to-Wear`, `Handbags`, `Shoes`, `Jewelry`), the engine extracts the modal frequency across six aesthetic dimensions and median price spend, then ranks local backroom RFID inventory using a domain-locked `MinMaxScaler` and square-root-weighted Euclidean distance:

* **Material Tier (30%)**: Prioritizes textile and exotic skin hierarchy (cashmere, crocodile, silk-wool).

* **Logo Prominence (20%)**: Separates quiet-luxury purists (`1/5`) from monogram collectors (`5/5`).

* **Detail Complexity (15%)**: Balances architectural tailoring against high-craft embellishment.

* **Silhouette Length (10%)**, **Color Palette (10%)**, **Shine Index (10%)**, and **Base Price (5%)**.

* **Exact Size & Discovery Ranking**: Filters backroom RFID stock strictly to the client's verified size and surfaces **new unowned style codes first** ahead of archive replenishment pieces.

## 2. Quick Start

```
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt

# Verify the edge backend and regenerate synced CSVs + edge_live_state.json
python appy.py

# Launch the Sales Associate Clienteling UI
streamlit run Sales_Associate_UI.py

```

## 3. Repository Structure

```text
Silent-Concierge/
├── appy.py                         # Core in-memory Edge Engine (<5 ms scan latency & Euclidean recommender)
├── Sales_Associate_UI.py           # Streamlit Sales Associate iPad UI (Christian Dior / LVMH styling)
├── requirements.txt                # Python dependencies (streamlit, pandas, numpy)
├── README.md                       # Architecture & quick-start guide
└── data/                           # Relational CSV databases & runtime sync packet
    ├── master_product_catalog.csv  # Table 1: Paris Master PIM Catalog (12 luxury templates + SVG URIs)
    ├── vip_global_history.csv      # Table 2: Global Cloud CRM History (2,500 VIP transactions + gift flags)
    ├── local_rfid_inventory.csv    # Table 3: Bengaluru Backroom RFID Stock (60 physical units)
    └── edge_live_state.json        # Auto-generated at runtime on scan (do not edit manually)
```