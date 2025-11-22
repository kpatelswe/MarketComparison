from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Event, Consensus
from app.services.consensus_calculator import calculate_consensus
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

router = APIRouter()

class ConsensusResponse(BaseModel):
    event_id: int
    event_title: str
    probability: float
    disagreement: float
    disagreement_label: str
    confidence_interval_lower: float
    confidence_interval_upper: float
    source_count: int
    timestamp: datetime

@router.get("/{event_id}", response_model=ConsensusResponse)
async def get_consensus(event_id: int, db: Session = Depends(get_db)):
    """Get current consensus probability for an event"""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Get consensus from database or calculate on the fly
    consensus_record = db.query(Consensus).filter(Consensus.event_id == event_id).first()
    
    if consensus_record:
        return ConsensusResponse(
            event_id=event_id,
            event_title=event.title,
            probability=consensus_record.probability,
            disagreement=consensus_record.disagreement,
            disagreement_label=consensus_record.disagreement_label,
            confidence_interval_lower=consensus_record.confidence_interval_lower,
            confidence_interval_upper=consensus_record.confidence_interval_upper,
            source_count=0,  # Could add this to Consensus model
            timestamp=consensus_record.updated_at or consensus_record.timestamp
        )
    else:
        # Calculate on the fly
        consensus_data = calculate_consensus(db, event_id)
        if not consensus_data:
            raise HTTPException(status_code=404, detail="No forecasts available for this event")
        
        return ConsensusResponse(
            event_id=event_id,
            event_title=event.title,
            **consensus_data
        )

