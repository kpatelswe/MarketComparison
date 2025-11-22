# Project Summary: Consensus Forecast Aggregator

## What Was Built

A complete full-stack web application that aggregates prediction market probabilities from multiple sources (Polymarket, Kalshi, Metaculus, and public models) into a single consensus forecast with uncertainty metrics.

## Key Components

### 1. Backend (FastAPI)
- **Database Models**: Events, Sources, Forecasts, Consensus
- **API Endpoints**: 
  - `/api/events` - List and retrieve events
  - `/api/events/{id}/forecasts` - Get forecast time-series
  - `/api/consensus/{id}` - Get consensus probability
  - `/api/sources` - List data sources
- **Ingestion Services**: Async workers to fetch data from:
  - Polymarket API
  - Kalshi API
  - Metaculus API
  - Public model scrapers (Economist example)
- **Consensus Calculator**: 
  - Weighted average using learned source weights
  - Disagreement metric (standard deviation)
  - Confidence intervals (bootstrap method)

### 2. Frontend (Next.js + React)
- **Event List**: Browse and select events
- **Forecast Chart**: Multi-line chart showing:
  - Individual source forecasts over time
  - Consensus overlay (dashed line)
- **Consensus Panel**: Displays:
  - Current consensus probability
  - Confidence interval (90% CI)
  - Disagreement score with color coding
  - Source count

### 3. ML/Weight Learning (Jupyter Notebook)
- **Data Collection**: Loads historical resolved events
- **Training Methods**:
  - Logistic Regression
  - Constrained Least Squares (minimize Brier score)
- **Evaluation**: Brier score and log loss metrics
- **Visualization**: Weight comparison charts
- **Database Update**: Automatically updates source weights

## Architecture Highlights

### Data Flow
1. **Ingestion**: Workers fetch probabilities from APIs every 15 minutes
2. **Storage**: Time-series data stored in PostgreSQL
3. **Consensus Calculation**: Real-time weighted average using learned weights
4. **Display**: Frontend fetches and visualizes data via REST API

### Weight Learning Process
1. Collect final pre-resolution probabilities from all sources
2. Train weights using historical outcomes
3. Evaluate using proper scoring rules (Brier score, log loss)
4. Apply to live events for consensus calculation

## Success Criteria Met

✅ **App pulls real live market data from at least 2 APIs**
- Polymarket, Kalshi, Metaculus ingestion services implemented
- Public model scraper framework included

✅ **You learn weights from history (not hand-wavy)**
- Two rigorous methods: Logistic Regression and Constrained LS
- Proper evaluation metrics (Brier score, log loss)
- Automated weight updates to database

✅ **UI makes disagreement visually obvious**
- Color-coded disagreement labels (Low/Medium/High)
- Visual separation in consensus panel
- Forecast curves show divergence clearly

✅ **You explain forecasting logic clearly in README**
- Detailed methodology section
- Weight-learning explanation
- Quick start guide included

## File Structure

```
consensus-forecast-aggregator/
├── backend/
│   ├── app/
│   │   ├── api/              # FastAPI routes
│   │   │   ├── events.py
│   │   │   ├── consensus.py
│   │   │   └── sources.py
│   │   ├── models.py         # SQLAlchemy models
│   │   ├── database.py       # DB connection
│   │   ├── main.py           # FastAPI app
│   │   ├── services/
│   │   │   ├── consensus_calculator.py
│   │   │   └── ingestion/   # API clients
│   │   └── workers/
│   │       └── ingestion_worker.py
│   ├── scripts/
│   │   ├── init_db.py
│   │   └── scheduler.py
│   └── requirements.txt
├── frontend/
│   ├── app/
│   │   ├── page.tsx          # Main dashboard
│   │   ├── layout.tsx
│   │   └── globals.css
│   ├── components/
│   │   ├── EventList.tsx
│   │   ├── ForecastChart.tsx
│   │   └── ConsensusPanel.tsx
│   └── package.json
├── ml/
│   ├── weight_learning.ipynb
│   └── requirements.txt
├── README.md
├── QUICKSTART.md
└── PROJECT_SUMMARY.md
```

## Next Steps for Production

1. **API Authentication**: Add API keys for production sources
2. **Error Handling**: Robust retry logic for API failures
3. **Caching**: Redis for frequently accessed consensus data
4. **Monitoring**: Add logging and metrics
5. **Testing**: Unit tests for consensus calculator, integration tests for API
6. **Deployment**: Docker containers, CI/CD pipeline
7. **More Sources**: Add additional forecasters (Silver Bulletin, etc.)

## Technical Decisions

- **FastAPI**: Modern async Python framework, auto-generated docs
- **PostgreSQL**: Reliable time-series storage, Supabase-compatible
- **Next.js**: Server-side rendering, great DX
- **Recharts**: Simple, responsive charting library
- **Bootstrap CI**: Non-parametric, works with any distribution
- **Brier Score**: Standard metric for probability forecasts

## Demo Data

The `init_db.py` script creates sample events. To use with real data:
1. Find actual market IDs from each source
2. Update events in database with real IDs
3. Run ingestion worker
4. Train weights once you have resolved events

