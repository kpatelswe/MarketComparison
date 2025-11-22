# Quick Start Guide

Get the Consensus Forecast Aggregator running in 5 minutes.

## Step 1: Database Setup

```bash
# Install PostgreSQL (if not already installed)
# macOS: brew install postgresql
# Ubuntu: sudo apt-get install postgresql

# Create database
createdb forecast_db
```

## Step 2: Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your DATABASE_URL

# Initialize database
python scripts/init_db.py
```

## Step 3: Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local (optional, defaults to localhost:8000)
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
```

## Step 4: Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Terminal 3 - Data Ingestion (optional, for live data):**
```bash
cd backend
source venv/bin/activate
python -m app.workers.ingestion_worker
```

## Step 5: Access the App

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Adding Events

You can add events via the API or directly in the database. Update the sample events created by `init_db.py` with actual market IDs from:
- Polymarket: Find market IDs from their website
- Kalshi: Use their API or website to find event tickers
- Metaculus: Use question IDs from metaculus.com
- Public Models: Use appropriate identifiers

## Training Weights

Once you have resolved events in your database:

```bash
cd ml
jupyter notebook
# Open weight_learning.ipynb and run all cells
```

## Troubleshooting

**Database connection errors:**
- Check your `DATABASE_URL` in `backend/.env`
- Ensure PostgreSQL is running: `pg_isready`

**API errors:**
- Check that backend is running on port 8000
- Verify CORS settings in `backend/app/main.py`

**Frontend not loading:**
- Check that `NEXT_PUBLIC_API_URL` matches your backend URL
- Check browser console for errors

**No forecast data:**
- Ensure ingestion worker is running
- Check that events have valid source IDs
- Verify API keys are set (if required)

