import { useState, useCallback } from 'react'
import Map, { Marker, NavigationControl } from 'react-map-gl'
import 'mapbox-gl/dist/mapbox-gl.css'
import { useSolarQuery } from '../hooks/useSolarQuery'
import { ResultsPanel } from '../components/ResultsPanel'
import styles from './MapPage.module.css'

const MAPBOX_TOKEN = import.meta.env.VITE_MAPBOX_TOKEN as string

export default function MapPage() {
  const [marker, setMarker] = useState<{ lat: number; lon: number } | null>(null)
  const [areaM2, setAreaM2] = useState<number>(20)
  const { data, loading, error, query } = useSolarQuery()

  const handleMapClick = useCallback(
    (evt: { lngLat: { lat: number; lng: number } }) => {
      const { lat, lng: lon } = evt.lngLat
      setMarker({ lat, lon })
      query(lat, lon, areaM2)
    },
    [areaM2, query],
  )

  return (
    <div className={styles.page}>
      <header className={styles.header}>
        <h1>solmap ☀️</h1>
        <p>Click anywhere on the map to assess solar potential</p>
        <label className={styles.areaLabel}>
          Roof area (m²):
          <input
            type="number"
            min={1}
            max={500}
            value={areaM2}
            onChange={(e) => setAreaM2(Number(e.target.value))}
            className={styles.areaInput}
          />
        </label>
      </header>

      <div className={styles.mapContainer}>
        <Map
          mapboxAccessToken={MAPBOX_TOKEN}
          initialViewState={{ longitude: 8.54, latitude: 47.37, zoom: 5 }}
          style={{ width: '100%', height: '100%' }}
          mapStyle="mapbox://styles/mapbox/satellite-streets-v12"
          onClick={handleMapClick}
          cursor="crosshair"
        >
          <NavigationControl position="top-right" />
          {marker && (
            <Marker longitude={marker.lon} latitude={marker.lat} color="#f59e0b" />
          )}
        </Map>

        {(loading || data || error) && (
          <div className={styles.overlay}>
            {loading && <p className={styles.status}>Fetching solar data…</p>}
            {error && <p className={styles.error}>{error}</p>}
            {data && <ResultsPanel data={data} />}
          </div>
        )}
      </div>
    </div>
  )
}
