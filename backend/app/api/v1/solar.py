"""Solar potential API endpoints."""

from fastapi import APIRouter, HTTPException, Query

from app.services.solar_service import calculate_solar_potential

router = APIRouter(prefix="/solar", tags=["solar"])


@router.get("", summary="Get solar potential for a location")
async def get_solar_potential(
    lat: float = Query(..., ge=-90, le=90, description="Latitude (WGS84)"),
    lon: float = Query(..., ge=-180, le=180, description="Longitude (WGS84)"),
    area_m2: float = Query(20.0, gt=0, description="Available rooftop area in m²"),
    tilt: float | None = Query(None, ge=0, le=90, description="Panel tilt in degrees"),
):
    """
    Returns solar irradiance, estimated annual yield, and financial metrics
    for the given location and rooftop configuration.
    """
    try:
        return await calculate_solar_potential(lat=lat, lon=lon, area_m2=area_m2, tilt=tilt)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Upstream data error: {exc}") from exc
