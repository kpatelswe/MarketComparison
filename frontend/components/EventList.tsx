'use client'

interface Event {
  id: number
  title: string
  category: string
  resolved: boolean
}

interface EventListProps {
  events: Event[]
  selectedEvent: Event | null
  onSelectEvent: (event: Event) => void
}

export default function EventList({ events, selectedEvent, onSelectEvent }: EventListProps) {
  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-xl font-semibold mb-4">Events</h2>
      <div className="space-y-2">
        {events.length === 0 ? (
          <p className="text-gray-500">No events available</p>
        ) : (
          events.map((event) => (
            <button
              key={event.id}
              onClick={() => onSelectEvent(event)}
              className={`w-full text-left p-3 rounded-lg transition-colors ${
                selectedEvent?.id === event.id
                  ? 'bg-blue-100 border-2 border-blue-500'
                  : 'bg-gray-50 hover:bg-gray-100 border-2 border-transparent'
              }`}
            >
              <div className="font-medium text-gray-900">{event.title}</div>
              <div className="text-sm text-gray-500 mt-1">
                {event.category} • {event.resolved ? 'Resolved' : 'Active'}
              </div>
            </button>
          ))
        )}
      </div>
    </div>
  )
}

