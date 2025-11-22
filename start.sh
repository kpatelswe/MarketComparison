#!/bin/bash

# Consensus Forecast Aggregator - Start Script
# Starts both backend and frontend servers

set -e

echo "🚀 Starting Consensus Forecast Aggregator..."
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Add PostgreSQL to PATH
export PATH="/opt/homebrew/opt/postgresql@14/bin:$PATH"

# Check if PostgreSQL is running
if ! pg_isready -h localhost > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠${NC} PostgreSQL is not running. Starting it..."
    brew services start postgresql@14
    sleep 2
fi

# Check if backend venv exists
if [ ! -d "backend/venv" ]; then
    echo -e "${YELLOW}⚠${NC} Backend virtual environment not found. Run ./setup.sh first."
    exit 1
fi

echo "📦 Starting Backend Server..."
echo "   Backend will be available at: http://localhost:8000"
echo "   API Docs will be available at: http://localhost:8000/docs"
echo ""
echo "🎨 Starting Frontend Server..."
echo "   Frontend will be available at: http://localhost:3000"
echo ""
echo -e "${GREEN}✓${NC} Both servers are starting..."
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""
echo "========================================"
echo ""

# Start backend in background
cd backend
source venv/bin/activate
uvicorn app.main:app --reload > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Start frontend in background
cd frontend
npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

# Wait for servers to start
echo "Waiting for servers to start..."
sleep 5

# Check if servers are running
if ps -p $BACKEND_PID > /dev/null && ps -p $FRONTEND_PID > /dev/null; then
    echo -e "${GREEN}✓${NC} Both servers started successfully!"
    echo ""
    echo "📝 Logs:"
    echo "   Backend:  tail -f backend.log"
    echo "   Frontend: tail -f frontend.log"
    echo ""
    echo "🌐 Access the app:"
    echo "   Frontend: http://localhost:3000"
    echo "   Backend:  http://localhost:8000"
    echo "   API Docs: http://localhost:8000/docs"
    echo ""
    echo "Press Ctrl+C to stop servers..."
    
    # Trap Ctrl+C and kill both servers
    trap "echo ''; echo 'Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT
    
    # Wait for user to stop
    wait
else
    echo -e "${YELLOW}⚠${NC} Servers may have failed to start. Check logs:"
    echo "   tail backend.log"
    echo "   tail frontend.log"
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
    exit 1
fi

