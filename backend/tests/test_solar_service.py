"""Tests for solar financial calculations (no network calls)."""

import pytest

from app.models.solar import SolarMetrics
from app.services.solar_service import _compute_financials, _npv


class TestNPV:
    def test_zero_cost_positive_benefit(self):
        result = _npv(cost=0, annual_benefit=1000, years=20, discount_rate=0.03)
        assert result > 0

    def test_high_cost_negative_npv(self):
        result = _npv(cost=1_000_000, annual_benefit=100, years=20, discount_rate=0.03)
        assert result < 0

    def test_breakeven(self):
        """NPV ≈ 0 when cost equals undiscounted sum of benefits."""
        result = _npv(cost=20_000, annual_benefit=1000, years=20, discount_rate=0.0)
        assert abs(result) < 1e-6

    def test_discount_reduces_npv(self):
        npv_nodiscount = _npv(cost=10_000, annual_benefit=1000, years=20, discount_rate=0.0)
        npv_discounted = _npv(cost=10_000, annual_benefit=1000, years=20, discount_rate=0.05)
        assert npv_nodiscount > npv_discounted


class TestComputeFinancials:
    @pytest.fixture
    def sample_solar(self) -> SolarMetrics:
        return SolarMetrics(
            annual_irradiance_kwh_m2=1300.0,
            optimal_tilt_deg=35.0,
            peak_power_kwp=5.0,
            annual_yield_kwh=5000.0,
        )

    def test_system_cost_proportional_to_kwp(self, sample_solar):
        from app.core.config import settings

        result = _compute_financials(sample_solar)
        expected_cost = sample_solar.peak_power_kwp * settings.default_cost_per_kwp_eur
        assert result.system_cost_eur == round(expected_cost, 0)

    def test_annual_savings_positive(self, sample_solar):
        result = _compute_financials(sample_solar)
        assert result.annual_savings_eur > 0

    def test_payback_reasonable(self, sample_solar):
        result = _compute_financials(sample_solar)
        # For European residential solar, payback should be between 3 and 20 years
        assert 3 <= result.payback_years <= 20

    def test_co2_offset_positive(self, sample_solar):
        result = _compute_financials(sample_solar)
        assert result.co2_offset_kg_yr > 0

    def test_zero_yield_infinite_payback(self):
        solar = SolarMetrics(
            annual_irradiance_kwh_m2=0.0,
            optimal_tilt_deg=0.0,
            peak_power_kwp=5.0,
            annual_yield_kwh=0.0,
        )
        result = _compute_financials(solar)
        assert result.payback_years == float("inf")
        assert result.annual_savings_eur == 0
