"""Integration tests for the FastAPI solar endpoint (no real network calls)."""

from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

MOCK_PVGIS_RESPONSE = {
    "inputs": {
        "mounting_system": {
            "fixed": {
                "slope": {"value": 35},
                "azimuth": {"value": 0},
            }
        }
    },
    "outputs": {
        "totals": {
            "fixed": {
                "E_y": 970.0,   # kWh/kWp/year
            }
        }
    },
}


class TestHealthEndpoint:
    def test_health_returns_ok(self):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["service"] == "solmap"


class TestSolarEndpoint:
    @patch(
        "app.services.solar_service.fetch_pvgis_annual_data",
        new_callable=AsyncMock,
        return_value=MOCK_PVGIS_RESPONSE,
    )
    def test_returns_200_with_valid_params(self, _mock):
        response = client.get("/api/v1/solar?lat=47.37&lon=8.54&area_m2=25")
        assert response.status_code == 200

    @patch(
        "app.services.solar_service.fetch_pvgis_annual_data",
        new_callable=AsyncMock,
        return_value=MOCK_PVGIS_RESPONSE,
    )
    def test_response_has_expected_keys(self, _mock):
        response = client.get("/api/v1/solar?lat=47.37&lon=8.54")
        data = response.json()
        assert "location" in data
        assert "solar" in data
        assert "financials" in data

    @patch(
        "app.services.solar_service.fetch_pvgis_annual_data",
        new_callable=AsyncMock,
        return_value=MOCK_PVGIS_RESPONSE,
    )
    def test_location_echoes_input(self, _mock):
        response = client.get("/api/v1/solar?lat=41.38&lon=2.17")
        data = response.json()
        assert abs(data["location"]["lat"] - 41.38) < 1e-6
        assert abs(data["location"]["lon"] - 2.17) < 1e-6

    @patch(
        "app.services.solar_service.fetch_pvgis_annual_data",
        new_callable=AsyncMock,
        return_value=MOCK_PVGIS_RESPONSE,
    )
    def test_solar_metrics_positive(self, _mock):
        response = client.get("/api/v1/solar?lat=47.37&lon=8.54&area_m2=30")
        data = response.json()["solar"]
        assert data["annual_irradiance_kwh_m2"] > 0
        assert data["peak_power_kwp"] > 0
        assert data["annual_yield_kwh"] > 0

    @patch(
        "app.services.solar_service.fetch_pvgis_annual_data",
        new_callable=AsyncMock,
        return_value=MOCK_PVGIS_RESPONSE,
    )
    def test_larger_area_gives_higher_yield(self, _mock):
        r_small = client.get("/api/v1/solar?lat=47.37&lon=8.54&area_m2=10")
        r_large = client.get("/api/v1/solar?lat=47.37&lon=8.54&area_m2=40")
        yield_small = r_small.json()["solar"]["annual_yield_kwh"]
        yield_large = r_large.json()["solar"]["annual_yield_kwh"]
        assert yield_large > yield_small

    def test_invalid_lat_returns_422(self):
        response = client.get("/api/v1/solar?lat=999&lon=8.54")
        assert response.status_code == 422

    def test_invalid_lon_returns_422(self):
        response = client.get("/api/v1/solar?lat=47.37&lon=999")
        assert response.status_code == 422

    def test_missing_lat_returns_422(self):
        response = client.get("/api/v1/solar?lon=8.54")
        assert response.status_code == 422

    @patch(
        "app.services.solar_service.fetch_pvgis_annual_data",
        new_callable=AsyncMock,
        side_effect=RuntimeError("upstream timeout"),
    )
    def test_upstream_error_returns_502(self, _mock):
        response = client.get("/api/v1/solar?lat=47.37&lon=8.54")
        assert response.status_code == 502
