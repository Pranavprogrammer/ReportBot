import threading
import schedule
import time
from .config import SCHEDULE_HOUR, SCHEDULE_MINUTE
from .pipeline import run_pipeline

_started = False

def scheduled_job():
    try:
        run_pipeline()
    except Exception as exc:
        print(f"[ReportBot scheduler] {exc}")

def start_scheduler():
    global _started
    if _started:
        return
    _started = True
    schedule.every().day.at(f"{SCHEDULE_HOUR:02d}:{SCHEDULE_MINUTE:02d}").do(scheduled_job)

    def loop():
        while True:
            schedule.run_pending()
            time.sleep(30)

    threading.Thread(target=loop, daemon=True).start()
