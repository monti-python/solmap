"""PVGIS API client — fetches solar irradiance data from the EU Commission."""

import httpx

from app.core.config import settings


async def fetch_pvgis_annual_data(
    lat: float,
    lon: float,
    tilt: float | None = None,
    aspect: float = 0,  # 0 = south
) -> dict:
    """
    Query the PVGIS hourly/annual radiation endpoint.

    Returns the raw PVGIS JSON response.
    Raises httpx.HTTPStatusError on non-2xx responses.
    """
    params: dict = {
        "lat": lat,
        "lon": lon,
        "outputformat": "json",
        "browser": 0,
        "userhorizon": "",
        "usehorizon": 1,
        "aspect": aspect,
        "pvtechchoice": "crystSi",
        "mountingplace": "building",
        "loss": settings.default_system_losses * 100,  # PVGIS expects percent
        "peakpower": 1,  # normalise to 1 kWp; we scale later
    }

    if tilt is not None:
        params["angle"] = tilt
    else:
        params["optimalangles"] = 1

    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.get(
            f"{settings.pvgis_base_url}/PVcalc",
            params=params,
        )
        response.raise_for_status()
        return response.json()


def parse_pvgis_response(data: dict) -> tuple[float, float]:
    """
    Extract annual yield (kWh/kWp) and optimal tilt from a PVGIS JSON response.

    Returns:
        (annual_yield_kwh_per_kwp, optimal_tilt_deg)
    """
    outputs = data["outputs"]
    annual_yield = outputs["totals"]["fixed"]["E_y"]  # kWh/kWp/year
    optimal_tilt = data["inputs"]["mounting_system"]["fixed"].get("slope", {}).get("value", 35)
    return float(annual_yield), float(optimal_tilt)
