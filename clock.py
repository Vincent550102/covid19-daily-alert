from apscheduler.schedulers.blocking import BlockingScheduler
import json
from main import external


sched = BlockingScheduler()


@sched.scheduled_job('interval', seconds=15)
def timed_job():
    external()

# @sched.scheduled_job('cron', day_of_week='mon-sun', hour=2)
# def scheduled_job():
#     try:
#         db = json.load(open('DataBase/DataBase.json', encoding='utf-8'))
#     except:
#         db = json.loads("{}")
#     alert_all(db)

sched.start()
