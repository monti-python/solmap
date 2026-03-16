# solmap 🌞🗺️

**Solar potential mapping for Europe — AI-powered, financially actionable.**

solmap lets homeowners, municipalities, and investors instantly assess the solar energy potential of any rooftop in Europe. Enter an address, get an interactive 3D view of annual irradiance, a panel layout recommendation, and a financial return projection — all in your browser.

---

## Why solmap?

Switzerland and Spain receive vastly different sunlight, yet both countries have aggressive net-zero targets and growing solar incentive programs. Existing tools are either US-centric (Google Sunroof), enterprise-only, or require manual data uploads. solmap fills the gap with a **free, open-data, European-first** experience that anyone can use in under 60 seconds.

---

## Market Research

### Competitive Landscape

| Product | Strengths | Weaknesses |
|---|---|---|
| **Google Project Sunroof** | Excellent UX, wide US coverage | US-only, closed data, no financial detail |
| **PVGIS (EU Commission)** | Free, authoritative EU data | Technical interface, no 3D, no finance |
| **Solargis** | Professional-grade irradiance data | Paid API, no consumer UI |
| **Helioscope / Aurora Solar** | Installer workflow, shade analysis | B2B only, expensive, US-centric |
| **In-Sun-Ity (CH)** | Swiss-focused | Limited coverage, no open API |

### Differentiators

1. **European-first open data** — built on PVGIS, Copernicus, and OpenStreetMap, free to use.
2. **3D rooftop analysis** — uses OpenStreetMap building footprints + elevation models for shade simulation.
3. **AI yield prediction** — ML model trained on historical Swiss/Spanish weather patterns.
4. **Instant financial snapshot** — net present value, payback period, and CO₂ offset in one click.
5. **Open API** — developers and municipalities can query any location programmatically.

### Target Markets

- **Switzerland** — high electricity prices (CHF 0.30/kWh+), strong federal and cantonal subsidies, affluent homeowners.
- **Spain** — Europe's highest irradiance, booming self-consumption market post 2019 Royal Decree.
- **Germany / Austria / Benelux** — expansion phase 2.

---

## Architecture

```
solmap/
├── backend/          # Python / FastAPI — data pipeline & AI inference
│   ├── app/
│   │   ├── api/      # REST endpoints
│   │   ├── core/     # Config, logging, security
│   │   ├── models/   # Pydantic schemas & SQLModel DB models
│   │   ├── services/ # Solar calculations, PVGIS client, AI model
│   │   └── main.py
│   ├── tests/
│   ├── pyproject.toml
│   └── Dockerfile
├── frontend/         # React + TypeScript + Mapbox GL JS
│   ├── src/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── pages/
│   │   └── services/
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

### Data Sources

| Source | Data | License |
|---|---|---|
| [PVGIS](https://re.jrc.ec.europa.eu/pvg_tools/) | Solar irradiance, PV yield | CC BY 4.0 |
| [OpenStreetMap](https://www.openstreetmap.org/) | Building footprints, roads | ODbL |
| [Copernicus DEM](https://spacedata.copernicus.eu/) | Elevation / terrain | Free for public use |
| [OpenWeatherMap](https://openweathermap.org/) | Real-time weather | Free tier |

---

## Quickstart

### Prerequisites

- Docker & Docker Compose ≥ 2.0
- Node.js ≥ 20 (for local frontend dev)
- Python ≥ 3.11 (for local backend dev)

### Run with Docker Compose

```bash
git clone https://github.com/monti-python/solmap.git
cd solmap
cp .env.example .env          # add your Mapbox token
docker compose up --build
```

Frontend: http://localhost:5173  
Backend API: http://localhost:8000  
API docs: http://localhost:8000/docs

### Backend (local dev)

```bash
cd backend
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

### Frontend (local dev)

```bash
cd frontend
npm install
npm run dev
```

---

## API Reference

### `GET /api/v1/solar`

Returns solar potential for a given location.

**Query parameters**

| Param | Type | Description |
|---|---|---|
| `lat` | float | Latitude (WGS84) |
| `lon` | float | Longitude (WGS84) |
| `area_m2` | float | Available roof area in m² (optional, default 20) |
| `tilt` | float | Panel tilt in degrees (optional, default optimal) |

**Example**

```bash
curl "http://localhost:8000/api/v1/solar?lat=47.3769&lon=8.5417&area_m2=30"
```

**Response**

```json
{
  "location": { "lat": 47.3769, "lon": 8.5417, "address": "Zurich, Switzerland" },
  "solar": {
    "annual_irradiance_kwh_m2": 1287,
    "optimal_tilt_deg": 35,
    "peak_power_kwp": 5.4,
    "annual_yield_kwh": 5230
  },
  "financials": {
    "system_cost_eur": 8100,
    "annual_savings_eur": 1569,
    "payback_years": 5.2,
    "npv_20yr_eur": 23400,
    "co2_offset_kg_yr": 940
  }
}
```

---

## Roadmap

### v0.1 — MVP (current)
- [x] Project scaffolding & architecture
- [ ] PVGIS API integration
- [ ] Basic REST API (`/api/v1/solar`)
- [ ] Interactive map (Mapbox) with location search
- [ ] Financial calculator widget

### v0.2 — 3D & AI
- [ ] OpenStreetMap building extrusion (3D rooftop view)
- [ ] Shade simulation using elevation model
- [ ] ML yield correction model (Swiss + Spanish weather data)

### v0.3 — Product
- [ ] User accounts & saved projects
- [ ] PDF report export
- [ ] Installer marketplace integration
- [ ] Open API with rate-limited free tier

---

## Contributing

Pull requests welcome! Please open an issue first to discuss what you'd like to change.

## License

[MIT](LICENSE)

