import httpx
from typing import List, Dict, Optional
from datetime import datetime
import os

KALSHI_API_BASE = "https://trading-api.kalshi.com/trade-api/v2"

async def fetch_kalshi_markets(event_ids: Optional[List[str]] = None) -> List[Dict]:
    """
    Fetch market data from Kalshi API.
    Note: Kalshi requires authentication for most endpoints.
    For MVP, we'll use public market data if available.
    """
    try:
        # Kalshi requires API credentials
        api_key = os.getenv("KALSHI_API_KEY")
        api_secret = os.getenv("KALSHI_API_SECRET")
        
        if not api_key or not api_secret:
            print("Kalshi API credentials not configured")
            return []
        
        async with httpx.AsyncClient() as client:
            # Kalshi authentication endpoint
            auth_url = f"{KALSHI_API_BASE}/portfolio/balance"
            
            headers = {
                "Authorization": f"Bearer {api_key}:{api_secret}"
            }
            
            # For MVP, we'll use a simplified approach
            # In production, you'd need to properly authenticate and fetch markets
            markets_url = f"{KALSHI_API_BASE}/markets"
            
            response = await client.get(markets_url, headers=headers, timeout=30.0)
            
            if response.status_code == 200:
                data = response.json()
                markets = []
                
                if "markets" in data:
                    for market in data["markets"]:
                        if market.get("status") == "open":
                            markets.append({
                                "id": market.get("event_ticker"),
                                "title": market.get("title"),
                                "probability": market.get("yes_bid", 0.5),  # Use bid price as proxy
                                "timestamp": datetime.utcnow(),
                                "raw_data": market
                            })
                
                return markets
            else:
                print(f"Kalshi API error: {response.status_code}")
                return []
            
    except Exception as e:
        print(f"Error fetching Kalshi data: {e}")
        return []

async def fetch_kalshi_probability(market_id: str) -> Optional[float]:
    """
    Fetch current probability for a specific Kalshi market.
    """
    try:
        api_key = os.getenv("KALSHI_API_KEY")
        api_secret = os.getenv("KALSHI_API_SECRET")
        
        if not api_key or not api_secret:
            return None
        
        async with httpx.AsyncClient() as client:
            url = f"{KALSHI_API_BASE}/markets/{market_id}"
            headers = {
                "Authorization": f"Bearer {api_key}:{api_secret}"
            }
            
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract probability from market data
            if "yes_bid" in data and "yes_ask" in data:
                # Use mid price
                yes_bid = data["yes_bid"]
                yes_ask = data["yes_ask"]
                probability = (yes_bid + yes_ask) / 2
                return probability / 100.0  # Kalshi uses 0-100 scale
            
            return None
            
    except Exception as e:
        print(f"Error fetching Kalshi probability for {market_id}: {e}")
        return None

