"""
Scheduler script to run ingestion worker periodically.
Run this as a background process or cron job.
"""
import asyncio
import time
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.workers.ingestion_worker import ingest_forecasts

async def main():
    scheduler = AsyncIOScheduler()
    
    # Run ingestion every 15 minutes
    scheduler.add_job(
        ingest_forecasts,
        'interval',
        minutes=15,
        id='ingestion_job',
        replace_existing=True
    )
    
    scheduler.start()
    print("Scheduler started. Ingestion will run every 15 minutes.")
    
    try:
        # Keep the script running
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("Scheduler stopped.")

if __name__ == "__main__":
    asyncio.run(main())

