import type { SolarResponse } from './types'

const API_BASE = '/api/v1'

export interface SolarQueryParams {
  lat: number
  lon: number
  area_m2?: number
  tilt?: number
}

export async function fetchSolarPotential(params: SolarQueryParams): Promise<SolarResponse> {
  const url = new URL(API_BASE + '/solar', window.location.origin)
  url.searchParams.set('lat', String(params.lat))
  url.searchParams.set('lon', String(params.lon))
  if (params.area_m2 !== undefined) url.searchParams.set('area_m2', String(params.area_m2))
  if (params.tilt !== undefined) url.searchParams.set('tilt', String(params.tilt))

  const res = await fetch(url.toString())
  if (!res.ok) {
    const detail = await res.text()
    throw new Error(`API error ${res.status}: ${detail}`)
  }
  return res.json() as Promise<SolarResponse>
}
