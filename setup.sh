#!/bin/bash

# Consensus Forecast Aggregator - Setup Script
# This script will set up everything needed to run the project

set -e  # Exit on error

echo "🚀 Consensus Forecast Aggregator - Setup"
echo "========================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check prerequisites
echo "📋 Checking prerequisites..."

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓${NC} Python found: $PYTHON_VERSION"
else
    echo -e "${RED}✗${NC} Python 3 not found. Please install Python 3.10+"
    exit 1
fi

# Check Node.js
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✓${NC} Node.js found: $NODE_VERSION"
else
    echo -e "${RED}✗${NC} Node.js not found. Please install Node.js 18+"
    exit 1
fi

# Check PostgreSQL
if command -v psql &> /dev/null; then
    echo -e "${GREEN}✓${NC} PostgreSQL found"
    POSTGRES_INSTALLED=true
else
    echo -e "${YELLOW}⚠${NC} PostgreSQL not found"
    echo "   Install PostgreSQL:"
    echo "   macOS: brew install postgresql@14"
    echo "   Ubuntu: sudo apt-get install postgresql"
    POSTGRES_INSTALLED=false
fi

echo ""
echo "📦 Setting up Backend..."
echo "-----------------------"

cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}✓${NC} Virtual environment created"
else
    echo -e "${GREEN}✓${NC} Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo -e "${GREEN}✓${NC} Python dependencies installed"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cat > .env << EOF
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/forecast_db

# API Keys (optional - only needed if using authenticated APIs)
# POLYMARKET_API_KEY=your_key_here
# KALSHI_API_KEY=your_key_here
# KALSHI_API_SECRET=your_secret_here
# METACULUS_API_KEY=your_key_here
EOF
    echo -e "${GREEN}✓${NC} .env file created"
    echo -e "${YELLOW}⚠${NC} Please edit backend/.env with your database credentials"
else
    echo -e "${GREEN}✓${NC} .env file already exists"
fi

deactivate
cd ..

echo ""
echo "🎨 Setting up Frontend..."
echo "------------------------"

cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm install
    echo -e "${GREEN}✓${NC} Node.js dependencies installed"
else
    echo -e "${GREEN}✓${NC} Node.js dependencies already installed"
fi

# Create .env.local if it doesn't exist
if [ ! -f ".env.local" ]; then
    echo "Creating .env.local file..."
    echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
    echo -e "${GREEN}✓${NC} .env.local file created"
else
    echo -e "${GREEN}✓${NC} .env.local file already exists"
fi

cd ..

echo ""
echo "🗄️  Database Setup"
echo "-----------------"

if [ "$POSTGRES_INSTALLED" = true ]; then
    echo "To set up the database, run these commands:"
    echo ""
    echo "  1. Create database:"
    echo "     createdb forecast_db"
    echo ""
    echo "  2. Update DATABASE_URL in backend/.env with your credentials"
    echo ""
    echo "  3. Initialize database:"
    echo "     cd backend"
    echo "     source venv/bin/activate"
    echo "     python scripts/init_db.py"
    echo ""
else
    echo -e "${YELLOW}⚠${NC} PostgreSQL is not installed. Please install it first."
    echo ""
    echo "After installing PostgreSQL:"
    echo "  1. Create database: createdb forecast_db"
    echo "  2. Update DATABASE_URL in backend/.env"
    echo "  3. Run: cd backend && source venv/bin/activate && python scripts/init_db.py"
fi

echo ""
echo "✅ Setup Complete!"
echo ""
echo "📝 Next Steps:"
echo "=============="
echo ""
echo "1. Set up PostgreSQL database (if not done already)"
echo "2. Update backend/.env with your DATABASE_URL"
echo "3. Initialize database:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python scripts/init_db.py"
echo ""
echo "4. Start the backend (Terminal 1):"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   uvicorn app.main:app --reload"
echo ""
echo "5. Start the frontend (Terminal 2):"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "6. (Optional) Start data ingestion (Terminal 3):"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python scripts/scheduler.py"
echo ""
echo "🌐 Access the app:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""

