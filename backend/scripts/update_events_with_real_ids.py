"""
Update events with real market IDs from APIs and fetch actual data.
This script finds real markets and updates the database.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
import httpx
from app.database import SessionLocal
from app.models import Event, Source, Forecast
from datetime import datetime
from app.services.ingestion import polymarket, metaculus, public_model
from app.services.consensus_calculator import update_consensus

async def find_and_update_real_markets():
    """Find real markets and update events"""
    db = SessionLocal()
    
    try:
        print("Searching for real markets from APIs...\n")
        
        # Get events
        events = db.query(Event).filter(Event.resolved == False).all()
        sources = db.query(Source).filter(Source.is_active == True).all()
        source_map = {source.name: source for source in sources}
        
        # Try to find real Polymarket markets
        print("Fetching Polymarket markets...")
        try:
            async with httpx.AsyncClient() as client:
                # Try Polymarket's markets endpoint
                url = "https://clob.polymarket.com/markets?active=true&limit=20"
                response = await client.get(url, timeout=10.0)
                if response.status_code == 200:
                    data = response.json()
                    markets = data.get("data", []) if isinstance(data, dict) else data
                    if isinstance(markets, list) and len(markets) > 0:
                        print(f"  Found {len(markets)} Polymarket markets")
                        # Use first few active markets
                        active_markets = [m for m in markets if m.get('active') and not m.get('closed')][:2]
                        for i, event in enumerate(events[:2]):
                            if i < len(active_markets):
                                market = active_markets[i]
                                # Use condition_id or market_slug as identifier
                                market_id = market.get('condition_id') or market.get('market_slug') or market.get('question_id', '')
                                if market_id:
                                    event.polymarket_id = str(market_id)
                                    question = market.get('question', '')[:50]
                                    print(f"  Updated event '{event.title}' with Polymarket ID: {market_id[:40]}")
                                    print(f"    Market: {question}")
        except Exception as e:
            print(f"  Error fetching Polymarket: {e}")
            import traceback
            traceback.print_exc()
        
        # Try to find real Metaculus questions
        print("\nFetching Metaculus questions...")
        try:
            async with httpx.AsyncClient() as client:
                url = "https://www.metaculus.com/api/questions/?status=open&limit=10"
                response = await client.get(url, timeout=10.0)
                if response.status_code == 200:
                    data = response.json()
                    if 'results' in data and len(data['results']) > 0:
                        questions = data['results']
                        print(f"  Found {len(questions)} Metaculus questions")
                        for i, event in enumerate(events[:2]):
                            if i < len(questions):
                                q = questions[i]
                                event.metaculus_id = str(q.get('id'))
                                print(f"  Updated event '{event.title}' with Metaculus ID: {q.get('id')}")
        except Exception as e:
            print(f"  Error fetching Metaculus: {e}")
        
        db.commit()
        print("\n✅ Events updated with real market IDs")
        
        # Now fetch actual forecast data
        print("\n" + "="*50)
        print("Fetching real forecast data from APIs...")
        print("="*50 + "\n")
        
        for event in events:
            print(f"\nProcessing: {event.title}")
            
            # Fetch from Polymarket
            if event.polymarket_id and "polymarket" in source_map:
                print(f"  Fetching from Polymarket (ID: {event.polymarket_id})...")
                try:
                    prob = await polymarket.fetch_polymarket_probability(event.polymarket_id)
                    if prob is not None:
                        forecast = Forecast(
                            event_id=event.id,
                            source_id=source_map["polymarket"].id,
                            probability=prob,
                            timestamp=datetime.utcnow()
                        )
                        db.add(forecast)
                        print(f"    ✓ Polymarket: {prob:.2%}")
                    else:
                        print(f"    ✗ Could not fetch Polymarket data")
                except Exception as e:
                    print(f"    ✗ Error: {e}")
            
            # Fetch from Metaculus
            if event.metaculus_id and "metaculus" in source_map:
                print(f"  Fetching from Metaculus (ID: {event.metaculus_id})...")
                try:
                    prob = await metaculus.fetch_metaculus_probability(int(event.metaculus_id))
                    if prob is not None:
                        forecast = Forecast(
                            event_id=event.id,
                            source_id=source_map["metaculus"].id,
                            probability=prob,
                            timestamp=datetime.utcnow()
                        )
                        db.add(forecast)
                        print(f"    ✓ Metaculus: {prob:.2%}")
                    else:
                        print(f"    ✗ Could not fetch Metaculus data")
                except Exception as e:
                    print(f"    ✗ Error: {e}")
            
            # Update consensus
            try:
                update_consensus(db, event.id)
                print(f"  ✓ Consensus calculated")
            except Exception as e:
                print(f"  ✗ Consensus error: {e}")
        
        db.commit()
        print("\n" + "="*50)
        print("✅ Real forecast data fetched and saved!")
        print("="*50)
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(find_and_update_real_markets())

