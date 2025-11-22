from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Source
from pydantic import BaseModel

router = APIRouter()

class SourceResponse(BaseModel):
    id: int
    name: str
    display_name: str
    weight: float
    is_active: bool
    
    class Config:
        from_attributes = True

@router.get("/", response_model=List[SourceResponse])
async def list_sources(db: Session = Depends(get_db)):
    """List all data sources"""
    sources = db.query(Source).all()
    return sources

@router.get("/{source_id}", response_model=SourceResponse)
async def get_source(source_id: int, db: Session = Depends(get_db)):
    """Get a specific source by ID"""
    source = db.query(Source).filter(Source.id == source_id).first()
    if not source:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Source not found")
    return source

