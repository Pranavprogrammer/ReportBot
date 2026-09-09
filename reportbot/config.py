import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
INCOMING_DIR = DATA_DIR / "incoming"
REPORTS_DIR = DATA_DIR / "reports"
QUARANTINE_DIR = DATA_DIR / "quarantine"
DB_PATH = DATA_DIR / "reportbot.db"
METRICS_PATH = DATA_DIR / "latest_metrics.json"

SENDER_EMAIL = os.getenv("REPORTBOT_SENDER_EMAIL", "")
SENDER_PASSWORD = os.getenv("REPORTBOT_SENDER_PASSWORD", "")
RECIPIENT_EMAIL = os.getenv("REPORTBOT_RECIPIENT_EMAIL", "")
SMTP_HOST = os.getenv("REPORTBOT_SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("REPORTBOT_SMTP_PORT", "587"))
SEND_EMAIL = os.getenv("REPORTBOT_SEND_EMAIL", "false").lower() == "true"

SCHEDULE_HOUR = int(os.getenv("REPORTBOT_SCHEDULE_HOUR", "9"))
SCHEDULE_MINUTE = int(os.getenv("REPORTBOT_SCHEDULE_MINUTE", "0"))
TIMEZONE = os.getenv("REPORTBOT_TIMEZONE", "Asia/Kolkata")
