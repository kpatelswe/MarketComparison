# 🚀 Quick Setup Guide

This guide will help you set up the Consensus Forecast Aggregator from scratch.

## ✅ Prerequisites Check

Run the setup script to check and install everything:

```bash
./setup.sh
```

The script will:
- ✅ Check Python 3, Node.js, and PostgreSQL
- ✅ Set up Python virtual environment
- ✅ Install all Python dependencies
- ✅ Install all Node.js dependencies
- ✅ Create `.env` configuration files

## 📋 Step-by-Step Setup

### Step 1: Install PostgreSQL (if not installed)

**macOS (using Homebrew):**
```bash
brew install postgresql@14
brew services start postgresql@14
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
```

**Windows:**
Download and install from https://www.postgresql.org/download/windows/

### Step 2: Create Database

```bash
createdb forecast_db
```

Or if you have a different PostgreSQL setup:
```bash
psql -U postgres -c "CREATE DATABASE forecast_db;"
```

### Step 3: Configure Database Connection

Edit `backend/.env` with your database credentials:

```bash
# For default local setup (username: postgres, no password)
DATABASE_URL=postgresql://postgres@localhost:5432/forecast_db

# Or if you have a password
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/forecast_db

# Or for a custom user
DATABASE_URL=postgresql://youruser:yourpassword@localhost:5432/forecast_db
```

### Step 4: Initialize Database

```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python scripts/init_db.py
```

This will:
- Create all database tables
- Add default sources (Polymarket, Kalshi, Metaculus, Public Model)
- Add sample events

### Step 5: Start the Application

**Terminal 1 - Backend Server:**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

Backend will run at: http://localhost:8000  
API Documentation: http://localhost:8000/docs

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Frontend will run at: http://localhost:3000

**Terminal 3 - Data Ingestion (Optional):**
```bash
cd backend
source venv/bin/activate
python scripts/scheduler.py
```

This will fetch data from prediction markets every 15 minutes.

## 🎯 Verify Everything Works

1. **Check Backend:**
   - Open http://localhost:8000/docs
   - You should see the API documentation
   - Try `GET /api/events` - should return empty array or sample events

2. **Check Frontend:**
   - Open http://localhost:3000
   - You should see the application interface
   - If events exist, they should be listed

3. **Check Database:**
   ```bash
   psql forecast_db -c "SELECT * FROM sources;"
   psql forecast_db -c "SELECT * FROM events;"
   ```

## 🔧 Troubleshooting

### Database Connection Errors

**Error: `could not connect to server`**
- Make sure PostgreSQL is running:
  - macOS: `brew services list` (should show postgresql@14 as started)
  - Linux: `sudo systemctl status postgresql`
- Check connection string in `backend/.env`

**Error: `database does not exist`**
- Create the database: `createdb forecast_db`

**Error: `password authentication failed`**
- Update `DATABASE_URL` in `backend/.env` with correct credentials
- Or create a user: `psql -U postgres -c "CREATE USER youruser WITH PASSWORD 'yourpassword';"`

### Backend Won't Start

**Error: `ModuleNotFoundError`**
- Make sure virtual environment is activated: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`

**Error: `Address already in use`**
- Port 8000 is already in use
- Change port: `uvicorn app.main:app --reload --port 8001`
- Update frontend `.env.local`: `NEXT_PUBLIC_API_URL=http://localhost:8001`

### Frontend Won't Start

**Error: `Cannot find module`**
- Make sure you're in the frontend directory
- Reinstall: `npm install`

**Error: `Port 3000 is already in use`**
- Change port: `npm run dev -- -p 3001`

### No Data Showing

- Make sure database is initialized: `python scripts/init_db.py`
- Check that events exist: `psql forecast_db -c "SELECT * FROM events;"`
- Start the data ingestion worker: `python scripts/scheduler.py`

## 📝 Next Steps

1. **Add Real Events:**
   - Update sample events in the database with actual market IDs
   - Or add new events via the API

2. **Configure API Keys (Optional):**
   - Edit `backend/.env` to add API keys for authenticated APIs
   - Currently, most APIs work without keys

3. **Train Source Weights:**
   - Once you have resolved events with historical data:
   ```bash
   cd ml
   jupyter notebook
   # Open weight_learning.ipynb and run all cells
   ```

4. **Deploy:**
   - Backend: Deploy to Heroku, Railway, or similar
   - Frontend: Deploy to Vercel, Netlify, or similar

## 🆘 Getting Help

- Check the [README.md](README.md) for detailed documentation
- Check the [QUICKSTART.md](QUICKSTART.md) for quick reference
- Review API documentation at http://localhost:8000/docs

## 📚 Useful Commands

```bash
# Backend
cd backend
source venv/bin/activate
python scripts/init_db.py           # Initialize/reset database
uvicorn app.main:app --reload       # Start backend server
python scripts/scheduler.py         # Start data ingestion

# Frontend
cd frontend
npm install                         # Install dependencies
npm run dev                         # Start development server
npm run build                       # Build for production
npm run lint                        # Run linter

# Database
psql forecast_db                    # Connect to database
psql forecast_db -c "SELECT * FROM events;"  # Query events
createdb forecast_db                # Create database
dropdb forecast_db                  # Drop database (careful!)
```

