import httpx
from typing import List, Dict, Optional
from datetime import datetime
import os

METACULUS_API_BASE = "https://www.metaculus.com/api"

async def fetch_metaculus_questions(event_ids: Optional[List[int]] = None) -> List[Dict]:
    """
    Fetch questions/forecasts from Metaculus API.
    """
    try:
        async with httpx.AsyncClient() as client:
            # Metaculus public API endpoint
            url = f"{METACULUS_API_BASE}/questions/"
            
            params = {
                "status": "open",
                "limit": 100
            }
            
            if event_ids:
                params["ids"] = ",".join(map(str, event_ids))
            
            response = await client.get(url, params=params, timeout=30.0)
            response.raise_for_status()
            
            data = response.json()
            
            questions = []
            if "results" in data:
                for question in data["results"]:
                    # Get community prediction (median or mean)
                    community_prediction = question.get("community_prediction", 0.5)
                    
                    questions.append({
                        "id": question.get("id"),
                        "title": question.get("title"),
                        "probability": community_prediction,
                        "timestamp": datetime.utcnow(),
                        "raw_data": question
                    })
            
            return questions
            
    except Exception as e:
        print(f"Error fetching Metaculus data: {e}")
        return []

async def fetch_metaculus_probability(question_id: int) -> Optional[float]:
    """
    Fetch current probability for a specific Metaculus question.
    """
    try:
        async with httpx.AsyncClient() as client:
            url = f"{METACULUS_API_BASE}/questions/{question_id}/"
            
            response = await client.get(url, timeout=30.0)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract community prediction
            community_prediction = data.get("community_prediction", 0.5)
            
            # Metaculus predictions are typically 0-1 scale already
            return float(community_prediction)
            
    except Exception as e:
        print(f"Error fetching Metaculus probability for {question_id}: {e}")
        return None

