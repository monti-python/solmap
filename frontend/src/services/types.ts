/** Solar API response types mirroring backend Pydantic schemas. */

export interface LocationInfo {
  lat: number
  lon: number
  address?: string
}

export interface SolarMetrics {
  annual_irradiance_kwh_m2: number
  optimal_tilt_deg: number
  peak_power_kwp: number
  annual_yield_kwh: number
}

export interface FinancialMetrics {
  system_cost_eur: number
  annual_savings_eur: number
  payback_years: number
  npv_20yr_eur: number
  co2_offset_kg_yr: number
}

export interface SolarResponse {
  location: LocationInfo
  solar: SolarMetrics
  financials: FinancialMetrics
}
