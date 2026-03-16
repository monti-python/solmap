import { describe, it, expect, vi, beforeEach } from 'vitest'
import { fetchSolarPotential } from '../services/solarApi'
import type { SolarResponse } from '../services/types'

const mockResponse: SolarResponse = {
  location: { lat: 47.37, lon: 8.54 },
  solar: {
    annual_irradiance_kwh_m2: 1200,
    optimal_tilt_deg: 35,
    peak_power_kwp: 4,
    annual_yield_kwh: 4000,
  },
  financials: {
    system_cost_eur: 6000,
    annual_savings_eur: 1200,
    payback_years: 5,
    npv_20yr_eur: 15000,
    co2_offset_kg_yr: 720,
  },
}

beforeEach(() => {
  vi.restoreAllMocks()
})

describe('fetchSolarPotential', () => {
  it('builds the correct URL and returns data', async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(mockResponse),
    })
    vi.stubGlobal('fetch', fetchMock)

    const result = await fetchSolarPotential({ lat: 47.37, lon: 8.54, area_m2: 20 })

    expect(fetchMock).toHaveBeenCalledOnce()
    const calledUrl = fetchMock.mock.calls[0][0] as string
    expect(calledUrl).toContain('lat=47.37')
    expect(calledUrl).toContain('lon=8.54')
    expect(calledUrl).toContain('area_m2=20')
    expect(result).toEqual(mockResponse)
  })

  it('omits optional params when not provided', async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(mockResponse),
    })
    vi.stubGlobal('fetch', fetchMock)

    await fetchSolarPotential({ lat: 41.38, lon: 2.17 })

    const calledUrl = fetchMock.mock.calls[0][0] as string
    expect(calledUrl).not.toContain('area_m2')
    expect(calledUrl).not.toContain('tilt')
  })

  it('throws on non-ok response', async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: false,
      status: 422,
      text: () => Promise.resolve('Validation error'),
    })
    vi.stubGlobal('fetch', fetchMock)

    await expect(fetchSolarPotential({ lat: 47.37, lon: 8.54 })).rejects.toThrow('API error 422')
  })
})
