"""
Add sample forecast data for demonstration purposes.
This creates realistic forecast time-series data for the sample events.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models import Event, Source, Forecast
from datetime import datetime, timedelta
import random

db = SessionLocal()

try:
    # Get events and sources
    events = db.query(Event).all()
    sources = db.query(Source).filter(Source.is_active == True).all()
    
    if not events:
        print("No events found. Please run init_db.py first.")
        sys.exit(1)
    
    if not sources:
        print("No sources found. Please run init_db.py first.")
        sys.exit(1)
    
    print(f"Adding sample forecast data for {len(events)} events...")
    
    for event in events:
        print(f"\nProcessing event: {event.title}")
        
        # Check if forecasts already exist
        existing = db.query(Forecast).filter(Forecast.event_id == event.id).first()
        if existing:
            print(f"  Forecasts already exist for this event. Skipping...")
            continue
        
        # Create forecast data for the last 7 days (168 hours)
        # Generate realistic probability time-series
        base_probability = random.uniform(0.3, 0.7)  # Base probability between 30-70%
        
        for source in sources:
            # Each source has slightly different probabilities (simulating disagreement)
            source_adjustment = random.uniform(-0.15, 0.15)
            source_base = max(0.1, min(0.9, base_probability + source_adjustment))
            
            # Generate time-series data (one data point per 6 hours for 7 days = 28 points)
            for i in range(28):
                # Create timestamp (going back in time)
                hours_ago = (28 - i) * 6
                timestamp = datetime.utcnow() - timedelta(hours=hours_ago)
                
                # Add some realistic variation (trending up/down slightly with noise)
                trend = i * 0.002  # Small trend over time
                noise = random.uniform(-0.05, 0.05)  # Random noise
                
                probability = max(0.05, min(0.95, source_base + trend + noise))
                
                # Create forecast record
                forecast = Forecast(
                    event_id=event.id,
                    source_id=source.id,
                    probability=round(probability, 4),
                    timestamp=timestamp,
                    raw_data=None
                )
                db.add(forecast)
        
        print(f"  Added forecast data from {len(sources)} sources")
        print(f"  Generated {28} time points per source ({28 * len(sources)} total forecasts)")
    
    db.commit()
    print("\n✅ Sample forecast data added successfully!")
    print("\nNote: This is sample data for demonstration. For real data, run:")
    print("  python scripts/scheduler.py")
    print("  or")
    print("  python -m app.workers.ingestion_worker")
    
except Exception as e:
    db.rollback()
    print(f"Error adding sample forecasts: {e}")
    import traceback
    traceback.print_exc()
    raise
finally:
    db.close()

