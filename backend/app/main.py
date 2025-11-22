from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import events, consensus, sources
from app.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Consensus Forecast Aggregator API",
    description="API for aggregating prediction market forecasts",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(events.router, prefix="/api/events", tags=["events"])
app.include_router(consensus.router, prefix="/api/consensus", tags=["consensus"])
app.include_router(sources.router, prefix="/api/sources", tags=["sources"])

@app.get("/")
async def root():
    return {"message": "Consensus Forecast Aggregator API"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

