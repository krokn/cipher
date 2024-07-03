from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone
from src.api.routers import all_routers
from src.utils.generate_levels import update_levels

app = FastAPI(
    title="Шифр",
)
scheduler = AsyncIOScheduler(timezone=timezone('Europe/Moscow'))

scheduler.add_job(update_levels, CronTrigger(hour=12, minute=18))

@app.on_event("startup")
async def startup_event():
    print("Starting up...")
    scheduler.start()

@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down...")
    scheduler.shutdown()


for router in all_routers:
    app.include_router(router)