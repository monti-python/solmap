import { useState } from 'react'
import { fetchSolarPotential } from '../services/solarApi'
import type { SolarResponse } from '../services/types'

interface State {
  data: SolarResponse | null
  loading: boolean
  error: string | null
}

export function useSolarQuery() {
  const [state, setState] = useState<State>({ data: null, loading: false, error: null })

  const query = async (lat: number, lon: number, area_m2?: number) => {
    setState({ data: null, loading: true, error: null })
    try {
      const data = await fetchSolarPotential({ lat, lon, area_m2 })
      setState({ data, loading: false, error: null })
    } catch (err) {
      setState({ data: null, loading: false, error: String(err) })
    }
  }

  return { ...state, query }
}
