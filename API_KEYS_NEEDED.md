# API Keys Needed for Real-Time Data

## What We Need API Keys For:

### 1. **Kalshi** (Recommended)
- **Why**: Kalshi requires authentication for most API endpoints
- **How to get**: Sign up at https://kalshi.com/trade-api/
- **What you need**: 
  - `KALSHI_API_KEY` 
  - `KALSHI_API_SECRET`
- **Add to**: `backend/.env`

### 2. **Metaculus** (Optional but Recommended)
- **Why**: Metaculus API may require authentication for some endpoints
- **How to get**: Contact Metaculus API support or check their documentation
- **What you need**:
  - `METACULUS_API_KEY` (if available)
- **Add to**: `backend/.env`

### 3. **Polymarket** (Currently Working WITHOUT Key)
- **Status**: ✅ We can fetch public market data without API key
- **Note**: Some endpoints may require authentication for premium features

## Setup Instructions:

### If you have Kalshi API keys:

1. Edit `backend/.env`:
   ```bash
   KALSHI_API_KEY=your_key_here
   KALSHI_API_SECRET=your_secret_here
   ```

2. The ingestion worker will automatically use them when available

### If you have Metaculus API key:

1. Edit `backend/.env`:
   ```bash
   METACULUS_API_KEY=your_key_here
   ```

## Current Status:

- ✅ **Polymarket**: Working (no key needed for public data)
- ⚠️ **Kalshi**: Needs API keys for real-time data
- ⚠️ **Metaculus**: May need API key, or can try public endpoints
- ✅ **Public Models**: Can scrape Economist and other public sources

## What We're Doing Now:

Right now we're using **Polymarket's public API** which works without keys. We're finding CURRENT 2024/2025 markets and fetching real-time order book data.

If you provide Kalshi keys, we can add that as a second source for each event to get multi-source consensus!

