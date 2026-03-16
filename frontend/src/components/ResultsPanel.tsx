import type { SolarResponse } from '../services/types'
import styles from './ResultsPanel.module.css'

// Average CO₂ per short-haul flight (economy, ~2 h): ~120 kg per passenger
// Source: ICAO Carbon Emissions Calculator (2024)
const CO2_PER_FLIGHT_KG = 120

interface Props {
  data: SolarResponse
}

export function ResultsPanel({ data }: Props) {
  const { solar, financials } = data

  return (
    <div className={styles.panel}>
      <h2>Solar Potential</h2>

      <section>
        <h3>☀️ Solar Metrics</h3>
        <dl>
          <dt>Annual irradiance</dt>
          <dd>{solar.annual_irradiance_kwh_m2.toLocaleString()} kWh/m²</dd>
          <dt>Optimal tilt</dt>
          <dd>{solar.optimal_tilt_deg}°</dd>
          <dt>System size</dt>
          <dd>{solar.peak_power_kwp} kWp</dd>
          <dt>Annual yield</dt>
          <dd>{solar.annual_yield_kwh.toLocaleString()} kWh</dd>
        </dl>
      </section>

      <section>
        <h3>💶 Financial Return</h3>
        <dl>
          <dt>System cost</dt>
          <dd>€{financials.system_cost_eur.toLocaleString()}</dd>
          <dt>Annual savings</dt>
          <dd>€{financials.annual_savings_eur.toLocaleString()}</dd>
          <dt>Payback period</dt>
          <dd>{financials.payback_years} years</dd>
          <dt>20-year NPV</dt>
          <dd>€{financials.npv_20yr_eur.toLocaleString()}</dd>
        </dl>
      </section>

      <section>
        <h3>🌿 CO₂ Impact</h3>
        <p>
          <strong>{financials.co2_offset_kg_yr.toLocaleString()} kg</strong> of CO₂ offset per year
          <br />
          ≈ {(financials.co2_offset_kg_yr / CO2_PER_FLIGHT_KG).toFixed(1)} flights Madrid–Zurich avoided
        </p>
      </section>
    </div>
  )
}
