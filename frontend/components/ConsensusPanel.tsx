'use client'

interface Consensus {
  probability: number
  disagreement: number
  disagreement_label: string
  confidence_interval_lower: number
  confidence_interval_upper: number
  source_count: number
}

interface ConsensusPanelProps {
  consensus: Consensus
}

export default function ConsensusPanel({ consensus }: ConsensusPanelProps) {
  const formatPercent = (value: number) => `${(value * 100).toFixed(1)}%`
  const margin = (consensus.confidence_interval_upper - consensus.confidence_interval_lower) / 2

  const getDisagreementColor = (label: string) => {
    switch (label) {
      case 'Low':
        return 'bg-green-100 text-green-800'
      case 'Medium':
        return 'bg-yellow-100 text-yellow-800'
      case 'High':
        return 'bg-red-100 text-red-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h3 className="text-xl font-semibold mb-4">Consensus Probability</h3>
      
      <div className="space-y-4">
        {/* Main Consensus Value */}
        <div className="text-center p-6 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-lg text-white">
          <div className="text-sm opacity-90 mb-2">Consensus</div>
          <div className="text-5xl font-bold">{formatPercent(consensus.probability)}</div>
          <div className="text-sm opacity-90 mt-2">
            ± {formatPercent(margin)} (90% CI)
          </div>
        </div>

        {/* Confidence Interval */}
        <div className="bg-gray-50 rounded-lg p-4">
          <div className="text-sm text-gray-600 mb-2">Confidence Interval (90%)</div>
          <div className="flex items-center justify-between">
            <span className="text-lg font-semibold">
              {formatPercent(consensus.confidence_interval_lower)}
            </span>
            <span className="text-gray-400">→</span>
            <span className="text-lg font-semibold">
              {formatPercent(consensus.confidence_interval_upper)}
            </span>
          </div>
        </div>

        {/* Disagreement Score */}
        <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
          <div>
            <div className="text-sm text-gray-600 mb-1">Disagreement</div>
            <div className="text-lg font-semibold">
              {formatPercent(consensus.disagreement)}
            </div>
          </div>
          <div>
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${getDisagreementColor(consensus.disagreement_label)}`}>
              {consensus.disagreement_label}
            </span>
          </div>
        </div>

        {/* Source Count */}
        <div className="text-sm text-gray-600 text-center">
          Aggregated from {consensus.source_count} source{consensus.source_count !== 1 ? 's' : ''}
        </div>
      </div>
    </div>
  )
}

