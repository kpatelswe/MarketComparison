import httpx
from typing import List, Dict, Optional
from datetime import datetime
import os

POLYMARKET_API_BASE = "https://clob.polymarket.com"

async def fetch_polymarket_markets(event_ids: Optional[List[str]] = None) -> List[Dict]:
    """
    Fetch market data from Polymarket API.
    For MVP, we'll use their public market endpoints.
    """
    try:
        async with httpx.AsyncClient() as client:
            # Polymarket GraphQL endpoint
            url = "https://data-api.polymarket.com/events"
            
            response = await client.get(url, timeout=30.0)
            response.raise_for_status()
            
            data = response.json()
            
            # Parse markets from response
            markets = []
            if isinstance(data, list):
                for market in data:
                    if market.get("active"):
                        markets.append({
                            "id": market.get("id"),
                            "title": market.get("question"),
                            "probability": market.get("probability", 0.5),  # May need to calculate from prices
                            "timestamp": datetime.utcnow(),
                            "raw_data": market
                        })
            
            return markets
            
    except Exception as e:
        print(f"Error fetching Polymarket data: {e}")
        return []

async def fetch_polymarket_probability(market_id: str) -> Optional[float]:
    """
    Fetch current probability for a specific Polymarket market.
    Uses condition_id, market_slug, or question_id to find the market.
    """
    try:
        async with httpx.AsyncClient() as client:
            # Fetch markets list and find the one matching our ID
            url = f"{POLYMARKET_API_BASE}/markets?active=true&limit=100"
            response = await client.get(url, timeout=30.0)
            response.raise_for_status()
            
            data = response.json()
            markets = data.get("data", []) if isinstance(data, dict) else data
            
            # Find the market by condition_id, market_slug, or question_id
            market = None
            for m in markets:
                if (m.get("condition_id") == market_id or 
                    m.get("market_slug") == market_id or 
                    m.get("question_id") == market_id or
                    str(m.get("condition_id")) == str(market_id) or
                    str(m.get("market_slug")) == str(market_id)):
                    market = m
                    break
            
            if market:
                # Try to get order book data for probability
                condition_id = market.get("condition_id")
                if condition_id:
                    try:
                        # Get order book to calculate probability from prices
                        orderbook_url = f"{POLYMARKET_API_BASE}/book?token_id={condition_id}"
                        book_resp = await client.get(orderbook_url, timeout=10.0)
                        if book_resp.status_code == 200:
                            book_data = book_resp.json()
                            # Calculate from order book bids/asks
                            if "bids" in book_data and "asks" in book_data:
                                bids = book_data["bids"]
                                asks = book_data["asks"]
                                if bids and asks:
                                    # Use mid price
                                    best_bid = float(bids[0][0]) if bids else 0.5
                                    best_ask = float(asks[0][0]) if asks else 0.5
                                    probability = (best_bid + best_ask) / 2
                                    return probability
                    except:
                        pass
                
                # Fallback: use market's outcomes if available
                if "outcomes" in market:
                    outcomes = market["outcomes"]
                    if len(outcomes) >= 2:
                        yes_price = outcomes[0].get("price", 0.5)
                        no_price = outcomes[1].get("price", 0.5)
                        probability = yes_price / (yes_price + no_price) if (yes_price + no_price) > 0 else 0.5
                        return probability
                
                # Last resort: return 0.5 if market found but no price data
                return 0.5
            
            return None
            
    except Exception as e:
        print(f"Error fetching Polymarket probability for {market_id}: {e}")
        return None

