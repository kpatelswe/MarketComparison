import numpy as np
from typing import List, Dict, Tuple
from sqlalchemy.orm import Session
from app.models import Forecast, Source, Event, Consensus
from datetime import datetime

def calculate_consensus(
    db: Session,
    event_id: int,
    forecasts: List[Forecast] = None
) -> Dict:
    """
    Calculate consensus probability, disagreement, and confidence interval
    for a given event.
    """
    if forecasts is None:
        # Get latest forecasts from all sources for this event
        forecasts = db.query(Forecast).filter(
            Forecast.event_id == event_id
        ).order_by(Forecast.timestamp.desc()).all()
    
    if not forecasts:
        return None
    
    # Group by source and get latest probability per source
    source_probs = {}
    source_weights = {}
    
    for forecast in forecasts:
        source_id = forecast.source_id
        if source_id not in source_probs or forecast.timestamp > source_probs[source_id][1]:
            source_probs[source_id] = (forecast.probability, forecast.timestamp)
    
    # Get weights for each source
    for source_id, (prob, ts) in source_probs.items():
        source = db.query(Source).filter(Source.id == source_id).first()
        if source and source.is_active:
            source_weights[source_id] = source.weight
            source_probs[source_id] = prob
    
    if not source_probs:
        return None
    
    # Extract probabilities and weights
    probabilities = list(source_probs.values())
    weights = [source_weights.get(sid, 1.0) for sid in source_probs.keys()]
    
    # Normalize weights
    total_weight = sum(weights)
    if total_weight == 0:
        weights = [1.0 / len(weights)] * len(weights)
    else:
        weights = [w / total_weight for w in weights]
    
    # Calculate weighted average (consensus)
    consensus_prob = sum(p * w for p, w in zip(probabilities, weights))
    
    # Calculate disagreement (standard deviation)
    disagreement = np.std(probabilities)
    
    # Classify disagreement
    if disagreement < 0.05:
        disagreement_label = "Low"
    elif disagreement < 0.15:
        disagreement_label = "Medium"
    else:
        disagreement_label = "High"
    
    # Calculate confidence interval using bootstrap method
    ci_lower, ci_upper = calculate_confidence_interval(probabilities, weights)
    
    return {
        "probability": consensus_prob,
        "disagreement": disagreement,
        "disagreement_label": disagreement_label,
        "confidence_interval_lower": ci_lower,
        "confidence_interval_upper": ci_upper,
        "source_count": len(probabilities),
        "timestamp": datetime.utcnow()
    }

def calculate_confidence_interval(
    probabilities: List[float],
    weights: List[float],
    confidence: float = 0.90,
    n_bootstrap: int = 1000
) -> Tuple[float, float]:
    """
    Calculate confidence interval using bootstrap method.
    """
    if len(probabilities) < 2:
        # If only one source, use a simple uncertainty estimate
        return max(0.0, probabilities[0] - 0.05), min(1.0, probabilities[0] + 0.05)
    
    bootstrap_samples = []
    for _ in range(n_bootstrap):
        # Resample with replacement
        indices = np.random.choice(len(probabilities), size=len(probabilities), replace=True)
        resampled_probs = [probabilities[i] for i in indices]
        resampled_weights = [weights[i] for i in indices]
        
        # Normalize weights
        total = sum(resampled_weights)
        if total > 0:
            resampled_weights = [w / total for w in resampled_weights]
        
        # Calculate weighted average
        sample_consensus = sum(p * w for p, w in zip(resampled_probs, resampled_weights))
        bootstrap_samples.append(sample_consensus)
    
    # Calculate percentiles
    alpha = 1 - confidence
    lower_percentile = (alpha / 2) * 100
    upper_percentile = (1 - alpha / 2) * 100
    
    ci_lower = np.percentile(bootstrap_samples, lower_percentile)
    ci_upper = np.percentile(bootstrap_samples, upper_percentile)
    
    return float(ci_lower), float(ci_upper)

def update_consensus(db: Session, event_id: int):
    """Update consensus record for an event"""
    consensus_data = calculate_consensus(db, event_id)
    
    if not consensus_data:
        return None
    
    # Update or create consensus record
    existing = db.query(Consensus).filter(Consensus.event_id == event_id).first()
    
    if existing:
        existing.probability = consensus_data["probability"]
        existing.disagreement = consensus_data["disagreement"]
        existing.disagreement_label = consensus_data["disagreement_label"]
        existing.confidence_interval_lower = consensus_data["confidence_interval_lower"]
        existing.confidence_interval_upper = consensus_data["confidence_interval_upper"]
        existing.updated_at = datetime.utcnow()
    else:
        consensus = Consensus(
            event_id=event_id,
            probability=consensus_data["probability"],
            disagreement=consensus_data["disagreement"],
            disagreement_label=consensus_data["disagreement_label"],
            confidence_interval_lower=consensus_data["confidence_interval_lower"],
            confidence_interval_upper=consensus_data["confidence_interval_upper"]
        )
        db.add(consensus)
    
    db.commit()
    return consensus_data

