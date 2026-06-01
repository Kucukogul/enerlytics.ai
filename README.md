# Enerlytics.ai

AI platform for predicting renewable energy investment opportunities in Turkiye.

Combines meteorological data, machine learning and financial analytics to estimate solar energy potential and evaluate project feasibility at any location in Turkiye.

---

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn enerlytics_ai.app.main:app --app-dir src --reload
```

API → `http://127.0.0.1:8000` · Docs → `http://127.0.0.1:8000/docs`

---

## Quick Start

```bash
# Site analysis
curl -X POST "http://127.0.0.1:8000/api/v1/analyze-site" \
  -H "Content-Type: application/json" \
  -d '{"latitude": 39.9208, "longitude": 32.8541}'

# Historical solar data
curl -X POST "http://127.0.0.1:8000/api/v1/historical-solar" \
  -H "Content-Type: application/json" \
  -d '{"latitude": 39.9208, "longitude": 32.8541, "start_year": 2015, "end_year": 2024}'
```

---

## Structure

```
enerlytics.ai/
│
├── src/enerlytics_ai/
│   ├── api/
│   │   └── routes.py                        # API route definitions
│   ├── app/
│   │   ├── main.py                          # FastAPI app entry point
│   │   └── config.py                        # app configuration
│   ├── models/
│   │   ├── energy_model.py                  # solar energy estimation model
│   │   └── lcoe_model.py                    # LCOE financial model
│   ├── services/
│   │   ├── pvgis_data_service.py            # PVGIS API integration
│   │   ├── solar_data_service.py            # solar data fetching & caching
│   │   └── solar_model_service.py           # model inference service
│   └── utils/
│       ├── constants.py                     # shared constants
│       └── helpers.py                       # utility functions
│
├── pipelines/
│   ├── province_scan.py                     # scans all 81 TR provinces
│   └── scoring.py                           # investment scoring logic
│
├── analysis/
│   ├── notebooks/
│   │   ├── 01_eda.ipynb                     # exploratory data analysis
│   │   └── 02_turkiye_geneli_eda.ipynb      # Turkiye-wide solar EDA
│   └── outputs/
│       ├── monthly_stats.csv
│       ├── tr81_monthly_risk_band.csv
│       └── tr81_province_ranking.csv        # province investment ranking
│
├── data/
│   ├── raw/pvgis/                           # raw PVGIS API responses
│   └── processed/                           # cleaned province datasets
│
├── scripts/
│   └── fetch_pvgis_81_seriescalc.py         # data collection script
│
└── tests/
    ├── unit/
    │   └── test_scoring.py
    └── integration/
        └── test_province_pipeline.py
```

---

**Author:** Huseyin Kucukogul · MIT License
