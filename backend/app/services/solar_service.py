"""Solar potential calculations and financial modelling."""

import math

from app.core.config import settings
from app.models.solar import FinancialMetrics, LocationInfo, SolarMetrics, SolarResponse
from app.services.pvgis_client import fetch_pvgis_annual_data, parse_pvgis_response

# Panel power density (kWp/m²) at Standard Test Conditions (1 kW/m² irradiance)
# For monocrystalline panels: power_density = efficiency × 1 kW/m² STC → kWp/m²
PANEL_POWER_DENSITY_KWP_M2 = settings.default_panel_efficiency  # e.g. 0.20 kWp/m²


async def calculate_solar_potential(
    lat: float,
    lon: float,
    area_m2: float = 20.0,
    tilt: float | None = None,
) -> SolarResponse:
    """
    Full pipeline: PVGIS data → solar metrics → financial model.
    """
    pvgis_data = await fetch_pvgis_annual_data(lat, lon, tilt=tilt)
    annual_yield_per_kwp, optimal_tilt = parse_pvgis_response(pvgis_data)

    # Approximate annual in-plane irradiance from PVGIS yield by reversing the
    # system loss factor.  PVGIS already applies some internal losses, so this
    # is an estimate; the authoritative value would come from a separate PVGIS
    # radiation endpoint.
    irradiance = annual_yield_per_kwp / (1 - settings.default_system_losses)

    peak_power_kwp = area_m2 * PANEL_POWER_DENSITY_KWP_M2
    annual_yield_kwh = peak_power_kwp * annual_yield_per_kwp

    solar = SolarMetrics(
        annual_irradiance_kwh_m2=round(irradiance, 1),
        optimal_tilt_deg=round(optimal_tilt, 1),
        peak_power_kwp=round(peak_power_kwp, 2),
        annual_yield_kwh=round(annual_yield_kwh, 1),
    )

    financials = _compute_financials(solar)

    return SolarResponse(
        location=LocationInfo(lat=lat, lon=lon),
        solar=solar,
        financials=financials,
    )


def _compute_financials(solar: SolarMetrics) -> FinancialMetrics:
    """Compute financial return metrics for a given solar system."""
    cost = solar.peak_power_kwp * settings.default_cost_per_kwp_eur
    annual_savings = solar.annual_yield_kwh * settings.default_electricity_price_eur
    payback = cost / annual_savings if annual_savings > 0 else float("inf")
    npv = _npv(
        cost=cost,
        annual_benefit=annual_savings,
        years=20,
        discount_rate=settings.discount_rate,
    )
    co2_offset = solar.annual_yield_kwh * settings.default_co2_intensity_kg_kwh

    return FinancialMetrics(
        system_cost_eur=round(cost, 0),
        annual_savings_eur=round(annual_savings, 0),
        payback_years=round(payback, 1),
        npv_20yr_eur=round(npv, 0),
        co2_offset_kg_yr=round(co2_offset, 0),
    )


def _npv(cost: float, annual_benefit: float, years: int, discount_rate: float) -> float:
    """Calculate net present value of a solar investment."""
    pv_benefits = sum(
        annual_benefit / math.pow(1 + discount_rate, t) for t in range(1, years + 1)
    )
    return pv_benefits - cost
