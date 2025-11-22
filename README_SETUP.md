# ✅ Setup Complete!

Everything has been automatically set up for you! Here's what was done:

## ✅ What Was Installed

1. **PostgreSQL 14** - Database server installed and running
2. **Python Backend** - Virtual environment created, all dependencies installed
3. **Node.js Frontend** - All dependencies installed
4. **Database** - Created `forecast_db` with:
   - 4 default sources (Polymarket, Kalshi, Metaculus, Public Model)
   - 2 sample events

## 🚀 How to Start the Application

### Option 1: Start Everything at Once (Recommended)

```bash
./start.sh
```

This will start both backend and frontend servers. Press `Ctrl+C` to stop both.

### Option 2: Start Separately (Better for Development)

**Terminal 1 - Backend:**
```bash
./start-backend.sh
```

**Terminal 2 - Frontend:**
```bash
./start-frontend.sh
```

### Option 3: Manual Start

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

## 🌐 Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📋 What You Can Do Now

1. **View the App**: Open http://localhost:3000 in your browser
2. **Test the API**: Visit http://localhost:8000/docs to see all available endpoints
3. **Check Database**: 
   ```bash
   export PATH="/opt/homebrew/opt/postgresql@14/bin:$PATH"
   psql forecast_db -c "SELECT * FROM events;"
   ```

## 🔧 Useful Commands

### Start/Stop PostgreSQL
```bash
brew services start postgresql@14   # Start
brew services stop postgresql@14    # Stop
brew services restart postgresql@14 # Restart
```

### Database Commands
```bash
export PATH="/opt/homebrew/opt/postgresql@14/bin:$PATH"
psql forecast_db                    # Connect to database
psql forecast_db -c "SELECT * FROM sources;"  # Query sources
psql forecast_db -c "SELECT * FROM events;"   # Query events
```

### Reset Database (if needed)
```bash
cd backend
source venv/bin/activate
python scripts/init_db.py
```

### Start Data Ingestion Worker (Optional)
```bash
cd backend
source venv/bin/activate
python scripts/scheduler.py
```

This will fetch data from prediction markets every 15 minutes.

## 📝 Configuration Files

- `backend/.env` - Backend configuration (database URL, API keys)
- `frontend/.env.local` - Frontend configuration (API URL)

## 🎯 Next Steps

1. **Add Real Events**: Update the sample events with actual market IDs from:
   - Polymarket: https://polymarket.com
   - Kalshi: https://kalshi.com
   - Metaculus: https://www.metaculus.com

2. **Train Source Weights**: Once you have resolved events with historical data:
   ```bash
   cd ml
   jupyter notebook
   # Open weight_learning.ipynb and run all cells
   ```

3. **Add API Keys** (optional): If you want to use authenticated APIs, add keys to `backend/.env`

## 🆘 Troubleshooting

### PostgreSQL Not Running
```bash
brew services start postgresql@14
```

### Port Already in Use
If port 8000 or 3000 is already in use, you can change them:
- Backend: `uvicorn app.main:app --reload --port 8001`
- Frontend: `npm run dev -- -p 3001`

### Database Connection Error
Check that PostgreSQL is running:
```bash
brew services list | grep postgresql
```

If not running:
```bash
brew services start postgresql@14
```

## 📚 Additional Resources

- See `SETUP_GUIDE.md` for detailed setup instructions
- See `QUICKSTART.md` for quick reference
- See `README.md` for full project documentation

---

**Everything is ready to go! Just run `./start.sh` to start the application!** 🚀

