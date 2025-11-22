'use client'

import { useEffect, useState } from 'react'
import EventList from '@/components/EventList'
import ForecastChart from '@/components/ForecastChart'
import ConsensusPanel from '@/components/ConsensusPanel'
import axios from 'axios'

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface Event {
  id: number
  title: string
  description?: string
  category: string
  resolved: boolean
}

interface ForecastPoint {
  timestamp: string
  probability: number
  source_name: string
}

interface Consensus {
  probability: number
  disagreement: number
  disagreement_label: string
  confidence_interval_lower: number
  confidence_interval_upper: number
  source_count: number
}

export default function Home() {
  const [events, setEvents] = useState<Event[]>([])
  const [selectedEvent, setSelectedEvent] = useState<Event | null>(null)
  const [forecasts, setForecasts] = useState<ForecastPoint[]>([])
  const [consensus, setConsensus] = useState<Consensus | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchEvents()
  }, [])

  useEffect(() => {
    if (selectedEvent) {
      fetchForecasts(selectedEvent.id)
      fetchConsensus(selectedEvent.id)
    }
  }, [selectedEvent])

  const fetchEvents = async () => {
    try {
      const response = await axios.get(`${API_BASE}/api/events?resolved=false`)
      setEvents(response.data)
      if (response.data.length > 0 && !selectedEvent) {
        setSelectedEvent(response.data[0])
      }
      setLoading(false)
    } catch (error) {
      console.error('Error fetching events:', error)
      setLoading(false)
    }
  }

  const fetchForecasts = async (eventId: number) => {
    try {
      const response = await axios.get(`${API_BASE}/api/events/${eventId}/forecasts?hours=168`) // Last week
      setForecasts(response.data.forecasts)
    } catch (error) {
      console.error('Error fetching forecasts:', error)
    }
  }

  const fetchConsensus = async (eventId: number) => {
    try {
      const response = await axios.get(`${API_BASE}/api/consensus/${eventId}`)
      setConsensus(response.data)
    } catch (error) {
      console.error('Error fetching consensus:', error)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">Loading...</div>
      </div>
    )
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="max-w-7xl mx-auto">
        <header className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Consensus Forecast Aggregator
          </h1>
          <p className="text-gray-600">
            Aggregate probabilities from multiple prediction markets
          </p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Event List */}
          <div className="lg:col-span-1">
            <EventList
              events={events}
              selectedEvent={selectedEvent}
              onSelectEvent={setSelectedEvent}
            />
          </div>

          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {selectedEvent && (
              <>
                <div className="bg-white rounded-lg shadow-lg p-6">
                  <h2 className="text-2xl font-semibold mb-4">
                    {selectedEvent.title}
                  </h2>
                  {selectedEvent.description && (
                    <p className="text-gray-600 mb-4">{selectedEvent.description}</p>
                  )}
                </div>

                {/* Consensus Panel */}
                {consensus && (
                  <ConsensusPanel consensus={consensus} />
                )}

                {/* Forecast Chart */}
                <div className="bg-white rounded-lg shadow-lg p-6">
                  <h3 className="text-xl font-semibold mb-4">Forecast Curves</h3>
                  <ForecastChart forecasts={forecasts} consensus={consensus} />
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </main>
  )
}

