from apscheduler.schedulers.blocking import BlockingScheduler
from main import external


sched = BlockingScheduler()


@sched.scheduled_job('cron', hour=7)
def timed_job():
    external()

sched.start()