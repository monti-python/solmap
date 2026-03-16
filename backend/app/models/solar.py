"""Pydantic schemas for the solar API."""

from pydantic import BaseModel, Field


class LocationInfo(BaseModel):
    lat: float
    lon: float
    address: str | None = None


class SolarMetrics(BaseModel):
    annual_irradiance_kwh_m2: float = Field(description="Annual in-plane irradiance kWh/m²")
    optimal_tilt_deg: float = Field(description="Optimal panel tilt angle in degrees")
    peak_power_kwp: float = Field(description="Installed peak power in kWp")
    annual_yield_kwh: float = Field(description="Estimated annual energy yield in kWh")


class FinancialMetrics(BaseModel):
    system_cost_eur: float = Field(description="Estimated total installed system cost in EUR")
    annual_savings_eur: float = Field(description="Estimated annual electricity savings in EUR")
    payback_years: float = Field(description="Simple payback period in years")
    npv_20yr_eur: float = Field(description="Net present value over 20 years in EUR")
    co2_offset_kg_yr: float = Field(description="Annual CO₂ offset in kg")


class SolarResponse(BaseModel):
    location: LocationInfo
    solar: SolarMetrics
    financials: FinancialMetrics


class SolarRequest(BaseModel):
    lat: float = Field(ge=-90, le=90, description="Latitude in decimal degrees (WGS84)")
    lon: float = Field(ge=-180, le=180, description="Longitude in decimal degrees (WGS84)")
    area_m2: float = Field(default=20.0, gt=0, description="Available rooftop area in m²")
    tilt: float | None = Field(
        default=None, ge=0, le=90, description="Panel tilt in degrees (None = use optimal)"
    )
