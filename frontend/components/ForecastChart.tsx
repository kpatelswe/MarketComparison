'use client'

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { useMemo } from 'react'

interface ForecastPoint {
  timestamp: string
  probability: number
  source_name: string
}

interface Consensus {
  probability: number
}

interface ForecastChartProps {
  forecasts: ForecastPoint[]
  consensus: Consensus | null
}

export default function ForecastChart({ forecasts, consensus }: ForecastChartProps) {
  const chartData = useMemo(() => {
    // Group forecasts by timestamp and source
    const dataMap = new Map<string, Record<string, number | string>>()
    
    forecasts.forEach((forecast) => {
      const timestamp = new Date(forecast.timestamp).toISOString()
      if (!dataMap.has(timestamp)) {
        dataMap.set(timestamp, { timestamp })
      }
      dataMap.get(timestamp)![forecast.source_name] = forecast.probability * 100
    })

    // Add consensus if available
    if (consensus) {
      dataMap.forEach((data) => {
        data['Consensus'] = consensus.probability * 100
      })
    }

    return Array.from(dataMap.values()).sort((a, b) => 
      new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()
    )
  }, [forecasts, consensus])

  // Get unique source names
  const sources = useMemo(() => {
    const sourceSet = new Set<string>()
    forecasts.forEach((f) => sourceSet.add(f.source_name))
    if (consensus) {
      sourceSet.add('Consensus')
    }
    return Array.from(sourceSet)
  }, [forecasts, consensus])

  const colors = [
    '#3b82f6', // blue
    '#10b981', // green
    '#f59e0b', // amber
    '#ef4444', // red
    '#8b5cf6', // purple
    '#ec4899', // pink
  ]

  if (chartData.length === 0) {
    return (
      <div className="h-64 flex items-center justify-center text-gray-500">
        No forecast data available
      </div>
    )
  }

  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart data={chartData}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis
          dataKey="timestamp"
          tickFormatter={(value) => {
            const date = new Date(value)
            return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
          }}
        />
        <YAxis
          domain={[0, 100]}
          tickFormatter={(value) => `${value}%`}
        />
        <Tooltip
          formatter={(value: number) => `${value.toFixed(1)}%`}
          labelFormatter={(label) => {
            const date = new Date(label)
            return date.toLocaleString()
          }}
        />
        <Legend />
        {sources.map((source, index) => (
          <Line
            key={source}
            type="monotone"
            dataKey={source}
            stroke={source === 'Consensus' ? '#8b5cf6' : colors[index % colors.length]}
            strokeWidth={source === 'Consensus' ? 3 : 2}
            strokeDasharray={source === 'Consensus' ? '5 5' : '0'}
            dot={false}
            activeDot={{ r: 4 }}
          />
        ))}
      </LineChart>
    </ResponsiveContainer>
  )
}

