# Consensus Forecast Aggregator for Prediction Markets

A web application that aggregates probabilities for real-world events from multiple forecasting communities and markets (Polymarket, Kalshi, Metaculus, and public models) and outputs a single consensus probability with uncertainty and disagreement metrics.

## Overview

Different communities price the same event differently. This app:
- Ingests probabilities over time from multiple sources
- Normalizes and aligns all probabilities to a shared timeline
- Learns source reliability weights from historical resolved events
- Combines current probabilities into a consensus probability with uncertainty metrics

## Features

### A) Forecast Curves
- Line chart per source (Polymarket, Kalshi, Metaculus, Public Model)
- Consensus line overlay

### B) Consensus Probability
- Weighted average of sources
- Current value display (e.g., "Consensus: 64% YES")

### C) Disagreement Score
- Standard deviation across sources
- Labeled as: Low / Medium / High disagreement

### D) Confidence Interval
- Bootstrap method for uncertainty estimation
- Output format: "Consensus 64% ± 6% (90% CI)"

## Weight-Learning Methodology

The system uses historical resolved events to learn optimal weights:

1. **Data Collection**: For each past event, collect final pre-resolution probabilities (within 24 hours of resolution) from each source
2. **Training**: Use one of two methods:
   - **Logistic Regression**: Treats source probabilities as features and learns coefficients that minimize log loss
   - **Constrained Least Squares**: Directly optimizes weights to minimize Brier score with constraints (weights sum to 1, all non-negative)
3. **Evaluation**: Compare methods using Brier score and log loss metrics
4. **Application**: Apply learned weights to live events for consensus calculation

### Why This Works

- **Brier Score**: Measures calibration - how well-calibrated are the probabilities? Lower is better (0 = perfect, 1 = worst)
- **Log Loss**: Penalizes confident wrong predictions more heavily
- **Historical Performance**: Sources that were more accurate in the past get higher weights
- **Data-Driven**: No arbitrary assumptions - weights emerge from actual performance data

This approach ensures weights are data-driven rather than arbitrary, improving forecast accuracy over simple averaging.

## Tech Stack

- **Backend**: FastAPI + async workers
- **Database**: PostgreSQL (Supabase-compatible)
- **Frontend**: Next.js + Tailwind CSS + Recharts
- **ML/Stats**: Python (sklearn, numpy, pandas)
- **Data Ingestion**: Scheduled cron jobs / background workers

## Project Structure

```
├── backend/           # FastAPI backend
│   ├── app/
│   │   ├── api/      # API routes
│   │   ├── models/   # Database models
│   │   ├── services/ # Business logic
│   │   └── workers/  # Background jobs
│   └── requirements.txt
├── frontend/         # Next.js frontend
│   ├── app/         # Next.js app directory
│   ├── components/  # React components
│   └── package.json
├── ml/              # ML notebooks and scripts
│   ├── weight_learning.ipynb
│   └── requirements.txt
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL database (or Supabase)

### Installation

1. **Clone and setup**:
```bash
git clone <repository-url>
cd consensus-forecast-aggregator
```

2. **Backend Setup**:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Frontend Setup**:
```bash
cd frontend
npm install
```

4. **ML Environment**:
```bash
cd ml
pip install -r requirements.txt
jupyter notebook
```

### Database Setup

1. Create a PostgreSQL database:
```bash
createdb forecast_db
```

2. Configure database connection in `backend/.env`:
```bash
cp backend/.env.example backend/.env
# Edit backend/.env with your database credentials
```

3. Initialize database with default sources:
```bash
cd backend
python scripts/init_db.py
```

### Configuration

Create `.env` files:

**Backend** (`backend/.env`):
- `DATABASE_URL` - PostgreSQL connection string
- `POLYMARKET_API_KEY` - Optional, for Polymarket API
- `KALSHI_API_KEY` / `KALSHI_API_SECRET` - Optional, for Kalshi API
- `METACULUS_API_KEY` - Optional, for Metaculus API

**Frontend** (`frontend/.env.local`):
- `NEXT_PUBLIC_API_URL` - Backend API URL (default: http://localhost:8000)

### Running the Application

1. **Start the backend**:
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```
Backend will be available at http://localhost:8000

2. **Start the frontend**:
```bash
cd frontend
npm run dev
```
Frontend will be available at http://localhost:3000

3. **Run data ingestion** (in a separate terminal):
```bash
cd backend
source venv/bin/activate
python -m app.workers.ingestion_worker
```

4. **Or use the scheduler** (runs ingestion every 15 minutes):
```bash
cd backend
source venv/bin/activate
python scripts/scheduler.py
```

### Training Weights

After you have some resolved events in your database:

```bash
cd ml
jupyter notebook
# Open weight_learning.ipynb and run all cells
```

This will:
- Load historical resolved events
- Train weights using logistic regression and constrained least squares
- Compare methods and select the best
- Update source weights in the database

## API Endpoints

- `GET /api/events` - List all tracked events
- `GET /api/events/{event_id}/forecasts` - Get forecast time-series for an event
- `GET /api/events/{event_id}/consensus` - Get current consensus probability
- `GET /api/sources` - List all data sources
- `POST /api/weights/train` - Retrain weight model

## Success Criteria

✅ App pulls real live market data from at least 2 APIs  
✅ You learn weights from history (not hand-wavy)  
✅ UI makes disagreement visually obvious  
✅ You explain forecasting logic clearly in README  

## License

MIT

