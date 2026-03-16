"""Application settings loaded from environment variables."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "solmap"
    debug: bool = False

    # PVGIS base URL (EU Commission open API)
    pvgis_base_url: str = "https://re.jrc.ec.europa.eu/api/v5_2"

    # Electricity price defaults (EUR/kWh)
    default_electricity_price_eur: float = 0.30  # Swiss average

    # PV system defaults
    default_panel_efficiency: float = 0.20   # 20 % monocrystalline
    default_system_losses: float = 0.14      # wiring, inverter, soiling
    default_cost_per_kwp_eur: float = 1500   # installed cost EUR/kWp
    default_lifetime_years: int = 25
    discount_rate: float = 0.03              # 3 % real discount rate

    # CO₂ grid intensity (kg CO₂/kWh) — Swiss grid (low due to hydro/nuclear)
    default_co2_intensity_kg_kwh: float = 0.18


settings = Settings()
