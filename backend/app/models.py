from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Source(Base):
    __tablename__ = "sources"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)  # e.g., "polymarket", "kalshi", "metaculus"
    display_name = Column(String)  # e.g., "Polymarket"
    api_endpoint = Column(String, nullable=True)
    weight = Column(Float, default=1.0)  # Learned weight for consensus
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    forecasts = relationship("Forecast", back_populates="source")

class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    category = Column(String)  # e.g., "sports", "politics", "economics"
    resolution_date = Column(DateTime(timezone=True), nullable=True)
    resolved = Column(Boolean, default=False)
    outcome = Column(String, nullable=True)  # "YES" or "NO" or other
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    forecasts = relationship("Forecast", back_populates="event")
    
    # Source-specific event IDs
    polymarket_id = Column(String, nullable=True)
    kalshi_id = Column(String, nullable=True)
    metaculus_id = Column(String, nullable=True)
    public_model_id = Column(String, nullable=True)

class Forecast(Base):
    __tablename__ = "forecasts"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), index=True)
    source_id = Column(Integer, ForeignKey("sources.id"), index=True)
    probability = Column(Float)  # Probability value (0.0 to 1.0)
    timestamp = Column(DateTime(timezone=True), index=True, server_default=func.now())
    raw_data = Column(Text, nullable=True)  # Store raw API response for debugging
    
    event = relationship("Event", back_populates="forecasts")
    source = relationship("Source", back_populates="forecasts")

class Consensus(Base):
    __tablename__ = "consensus"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), index=True, unique=True)
    probability = Column(Float)  # Weighted consensus probability
    disagreement = Column(Float)  # Standard deviation across sources
    disagreement_label = Column(String)  # "Low", "Medium", "High"
    confidence_interval_lower = Column(Float)  # 90% CI lower bound
    confidence_interval_upper = Column(Float)  # 90% CI upper bound
    timestamp = Column(DateTime(timezone=True), index=True, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    event = relationship("Event")

