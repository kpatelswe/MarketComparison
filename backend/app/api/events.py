from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from app.database import get_db
from app.models import Event, Forecast, Source
from pydantic import BaseModel

router = APIRouter()

class EventResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    category: str
    resolution_date: Optional[datetime]
    resolved: bool
    outcome: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class ForecastPoint(BaseModel):
    timestamp: datetime
    probability: float
    source_name: str

class EventForecastsResponse(BaseModel):
    event_id: int
    event_title: str
    forecasts: List[ForecastPoint]

@router.get("/", response_model=List[EventResponse])
async def list_events(
    category: Optional[str] = None,
    resolved: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """List all events, optionally filtered by category or resolution status"""
    query = db.query(Event)
    
    if category:
        query = query.filter(Event.category == category)
    if resolved is not None:
        query = query.filter(Event.resolved == resolved)
    
    events = query.order_by(Event.created_at.desc()).all()
    return events

@router.get("/{event_id}", response_model=EventResponse)
async def get_event(event_id: int, db: Session = Depends(get_db)):
    """Get a specific event by ID"""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.get("/{event_id}/forecasts", response_model=EventForecastsResponse)
async def get_event_forecasts(
    event_id: int,
    hours: Optional[int] = 24,  # Default to last 24 hours
    db: Session = Depends(get_db)
):
    """Get forecast time-series for an event"""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Get forecasts from the last N hours
    cutoff_time = datetime.utcnow() - timedelta(hours=hours)
    
    forecasts = db.query(Forecast).filter(
        Forecast.event_id == event_id,
        Forecast.timestamp >= cutoff_time
    ).order_by(Forecast.timestamp.asc()).all()
    
    # Group by source and format
    forecast_points = []
    for forecast in forecasts:
        source = db.query(Source).filter(Source.id == forecast.source_id).first()
        forecast_points.append(ForecastPoint(
            timestamp=forecast.timestamp,
            probability=forecast.probability,
            source_name=source.display_name if source else "Unknown"
        ))
    
    return EventForecastsResponse(
        event_id=event_id,
        event_title=event.title,
        forecasts=forecast_points
    )

