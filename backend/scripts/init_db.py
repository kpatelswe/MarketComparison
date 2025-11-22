"""
Initialize database with default sources and sample events.
Run this script after setting up your database.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine, Base
from app.models import Source, Event
from datetime import datetime, timedelta

# Create tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    # Create default sources
    sources = [
        Source(
            name="polymarket",
            display_name="Polymarket",
            weight=1.0,
            is_active=True
        ),
        Source(
            name="kalshi",
            display_name="Kalshi",
            weight=1.0,
            is_active=True
        ),
        Source(
            name="metaculus",
            display_name="Metaculus",
            weight=1.0,
            is_active=True
        ),
        Source(
            name="public_model",
            display_name="Public Model",
            weight=1.0,
            is_active=True
        ),
    ]
    
    for source in sources:
        existing = db.query(Source).filter(Source.name == source.name).first()
        if not existing:
            db.add(source)
            print(f"Created source: {source.display_name}")
        else:
            print(f"Source already exists: {source.display_name}")
    
    db.commit()
    
    # Create sample events (you'll need to update these with actual IDs from your sources)
    sample_events = [
        Event(
            title="2024 US Presidential Election - Democratic Win",
            description="Will the Democratic candidate win the 2024 US Presidential Election?",
            category="politics",
            resolution_date=datetime(2024, 11, 5),
            resolved=False,
            polymarket_id="example-market-id-1",
            kalshi_id="EXAMPLE-1",
            metaculus_id=12345,
            public_model_id="election-2024"
        ),
        Event(
            title="Bitcoin Price Above $100k by End of 2024",
            description="Will Bitcoin price exceed $100,000 USD by December 31, 2024?",
            category="economics",
            resolution_date=datetime(2024, 12, 31),
            resolved=False,
            polymarket_id="example-market-id-2",
            kalshi_id="EXAMPLE-2",
            metaculus_id=12346,
            public_model_id="btc-100k"
        ),
    ]
    
    for event in sample_events:
        existing = db.query(Event).filter(Event.title == event.title).first()
        if not existing:
            db.add(event)
            print(f"Created event: {event.title}")
        else:
            print(f"Event already exists: {event.title}")
    
    db.commit()
    print("\nDatabase initialized successfully!")
    print("\nNote: Update the sample events with actual market IDs from your sources.")
    
except Exception as e:
    db.rollback()
    print(f"Error initializing database: {e}")
    raise
finally:
    db.close()

