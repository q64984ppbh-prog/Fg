from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from data.config import db
import pytz

MSK_TZ = pytz.timezone("Europe/Moscow")

async def reset_day_amount():
    await db.admin.reset_amount("ProfitDay")
    await db.admin.reset_amount("Amount_Replenishment_Day")

async def reset_week_amount():
    await db.admin.reset_amount("ProfitWeek")
def start_scheduler():
    scheduler = AsyncIOScheduler(timezone=MSK_TZ)

    scheduler.add_job(reset_day_amount, CronTrigger(hour=0, minute=0, second=0))
    scheduler.add_job(reset_week_amount, CronTrigger(day_of_week="mon", hour=0, minute=0, second=0))

    scheduler.start()
    print("планировшик запущен")
