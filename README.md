Enerlytics.ai — Global Renewable Investment Intelligence Platform
==================================================================

Enerlytics.ai is an AI-driven renewable energy intelligence platform designed to evaluate and discover high-potential locations for utility-scale renewable energy investments worldwide.

The platform combines global meteorological datasets, machine learning models and financial investment analytics to estimate renewable energy production and evaluate the financial feasibility of large-scale solar, wind and battery storage projects.

Enerlytics.ai enables developers, investors and energy analysts to analyze renewable potential at any geographic coordinate and identify optimal locations for future energy infrastructure.

Project Objectives
------------------

The primary objective of Enerlytics.ai is to build a scalable AI platform capable of evaluating renewable energy investment opportunities across the globe.

The project focuses on the following goals:

- Build a global geographic grid for renewable resource scanning
- Collect and process global weather datasets relevant to renewable energy production
- Train machine learning models to estimate solar and wind energy generation potential
- Calculate financial investment metrics such as ROI and Levelized Cost of Energy (LCOE)
- Rank potential renewable investment locations using AI-based scoring models
- Provide an interactive dashboard to analyze renewable investment opportunities

Run Locally
-----------

Prerequisites:

- Python 3.11+
- pip

1) Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2) Install dependencies:

```bash
pip install -r requirements.txt
```

3) Create environment file:

```bash
cp .env.example .env
```

4) Start the API:

```bash
uvicorn enerlytics_ai.app.main:app --app-dir src --reload
```

The API will be available at:

- `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`

API Quick Check
---------------

Health check:

```bash
curl http://127.0.0.1:8000/health
```

Analyze endpoint example:

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/analyze-site" \
  -H "Content-Type: application/json" \
  -d '{"latitude":41.0082,"longitude":28.9784}'
```

Historical endpoint example (Turkey, monthly series by year range):

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/historical-solar" \
  -H "Content-Type: application/json" \
  -d '{"latitude":41.0082,"longitude":28.9784,"start_year":2015,"end_year":2024}'
```

Historical response includes:

- `monthly_series`: month-by-month GHI values
- `annual_summary`: year-by-year total and average GHI

Expected response shape:

```json
{
  "data_source": "NASA POWER",
  "annual_energy_kwh": 0.0,
  "estimated_lcoe": 0.0,
  "summary": "Estimated annual production is ... kWh with an LCOE of ... USD/kWh."
}
```

Project Structure
-----------------

```text
enerlytics.ai/
  src/enerlytics_ai/    # application source code
  configs/              # environment and deployment configs
  pipelines/            # data/ML pipeline definitions
  analysis/             # notebooks, figures, reports
  tests/unit/           # fast isolated tests
  tests/integration/    # service-level tests
  docs/                 # project documentation
  scripts/              # automation and utility scripts
  data/                 # raw and processed datasets
```

License
-------

This project is licensed under the MIT License.

MIT License allows reuse, modification and distribution with proper attribution.

Author
------

Hüseyin Küçükoğul

Data Scientist  
Co-Founder & CEO — RemmeyAI
