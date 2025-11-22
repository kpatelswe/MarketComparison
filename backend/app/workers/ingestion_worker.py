import asyncio
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Event, Forecast, Source
from app.services.ingestion import polymarket, kalshi, metaculus, public_model
from app.services.consensus_calculator import update_consensus

async def ingest_forecasts():
    """
    Main ingestion function that fetches forecasts from all sources
    and stores them in the database.
    """
    db = SessionLocal()
    
    try:
        # Get all active events
        events = db.query(Event).filter(Event.resolved == False).all()
        
        # Get all active sources
        sources = db.query(Source).filter(Source.is_active == True).all()
        
        source_map = {source.name: source for source in sources}
        
        for event in events:
            # Fetch from Polymarket
            if event.polymarket_id and "polymarket" in source_map:
                prob = await polymarket.fetch_polymarket_probability(event.polymarket_id)
                if prob is not None:
                    save_forecast(db, event.id, source_map["polymarket"].id, prob, "polymarket")
            
            # Fetch from Kalshi
            if event.kalshi_id and "kalshi" in source_map:
                prob = await kalshi.fetch_kalshi_probability(event.kalshi_id)
                if prob is not None:
                    save_forecast(db, event.id, source_map["kalshi"].id, prob, "kalshi")
            
            # Fetch from Metaculus
            if event.metaculus_id and "metaculus" in source_map:
                prob = await metaculus.fetch_metaculus_probability(int(event.metaculus_id))
                if prob is not None:
                    save_forecast(db, event.id, source_map["metaculus"].id, prob, "metaculus")
            
            # Fetch from public model
            if event.public_model_id and "public_model" in source_map:
                prob = await public_model.fetch_public_model_probability(event.public_model_id)
                if prob is not None:
                    save_forecast(db, event.id, source_map["public_model"].id, prob, "public_model")
            
            # Update consensus after ingesting all sources
            update_consensus(db, event.id)
        
        db.commit()
        print(f"Ingestion completed at {datetime.utcnow()}")
        
    except Exception as e:
        db.rollback()
        print(f"Error in ingestion: {e}")
        raise
    finally:
        db.close()

def save_forecast(db: Session, event_id: int, source_id: int, probability: float, source_name: str):
    """Save a forecast to the database"""
    forecast = Forecast(
        event_id=event_id,
        source_id=source_id,
        probability=probability,
        timestamp=datetime.utcnow()
    )
    db.add(forecast)
    print(f"Saved forecast: {source_name} -> {probability:.2%} for event {event_id}")

if __name__ == "__main__":
    # Run ingestion
    asyncio.run(ingest_forecasts())

