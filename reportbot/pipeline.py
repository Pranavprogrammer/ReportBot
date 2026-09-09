import json
from datetime import datetime
from pathlib import Path
import pandas as pd

from .config import INCOMING_DIR, REPORTS_DIR, METRICS_PATH
from .database import start_run, finish_run
from .validation import validate_csv
from .analytics import calculate_metrics
from .report import build_pdf
from .emailer import send_with_retry

def run_pipeline():
    run_id = start_run()
    started = datetime.now()
    try:
        csv_files = sorted(INCOMING_DIR.glob("*.csv"))
        if not csv_files:
            raise RuntimeError("No CSV files found in data/incoming.")

        frames = []
        total_rows = 0
        quarantined = 0

        for path in csv_files:
            good, rows, bad = validate_csv(path)
            total_rows += rows
            quarantined += bad
            if not good.empty:
                frames.append(good)

        if not frames:
            raise RuntimeError("No valid rows were available after validation.")

        df = pd.concat(frames, ignore_index=True)
        metrics = calculate_metrics(df)
        METRICS_PATH.write_text(json.dumps(metrics, indent=2))

        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        report_name = f"sales_report_{datetime.now():%Y%m%d_%H%M%S}.pdf"
        report_path = REPORTS_DIR / report_name
        build_pdf(metrics, report_path)

        email_sent, email_message = send_with_retry(report_path, metrics)
        finish_run(
            run_id,
            status="SUCCESS",
            files_processed=len(csv_files),
            rows_processed=total_rows,
            valid_rows=len(df),
            quarantined_rows=quarantined,
            report_file=report_name,
            email_sent=int(email_sent),
            error_message=None
        )

        return {
            "files_processed": len(csv_files),
            "rows_processed": total_rows,
            "valid_rows": len(df),
            "quarantined_rows": quarantined,
            "report_file": report_name,
            "email_message": email_message,
            "duration_seconds": round((datetime.now() - started).total_seconds(), 2),
            "metrics": metrics
        }
    except Exception as exc:
        finish_run(run_id, status="FAILED", error_message=str(exc))
        raise
