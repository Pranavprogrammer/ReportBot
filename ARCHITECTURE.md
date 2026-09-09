# ARCHITECTURE.md

## 1. Project goal

ReportBot automates a recurring sales-reporting workflow:

**Ingest → Validate → Analyze → Generate PDF → Email → Monitor**

The design separates validation, analytics, reporting, email delivery and persistence so each part can be tested and maintained independently.

## 2. Component architecture

```text
                         ┌──────────────────────┐
                         │ FastAPI Web Dashboard │
                         └──────────┬───────────┘
                                    │
                     Upload / Run / Download / Health
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    Pipeline Service  │
                         └──────────┬───────────┘
                                    │
          ┌─────────────────────────┼─────────────────────────┐
          ▼                         ▼                         ▼
 ┌────────────────┐       ┌────────────────┐        ┌────────────────┐
 │ CSV Validation │       │ Pandas Metrics │        │ SQLite Logging │
 └───────┬────────┘       └───────┬────────┘        └────────────────┘
         │                         │
         ▼                         ▼
 ┌────────────────┐       ┌────────────────┐
 │  Quarantine    │       │ ReportLab PDF  │
 └────────────────┘       └───────┬────────┘
                                  ▼
                         ┌────────────────┐
                         │ SMTP + Retry   │
                         └────────────────┘
```

## 3. Data flow

1. A CSV is placed in `data/incoming/` or uploaded from the dashboard.
2. `validation.py` checks required columns and converts dates/numbers.
3. Invalid rows are written to `data/quarantine/`.
4. Valid rows are passed to `analytics.py`.
5. `analytics.py` calculates business metrics.
6. Metrics are saved to `data/latest_metrics.json` for the dashboard.
7. `report.py` creates a PDF in `data/reports/`.
8. `emailer.py` sends the PDF when SMTP is enabled.
9. `database.py` stores every run, including success/failure, row counts and report name.
10. `scheduler.py` triggers the same pipeline every day at 09:00.

## 4. Key design decisions

### Separation of concerns
The pipeline is divided into small modules rather than one large script. This makes it easier to test validation and analytics independently.

### Quarantine instead of silent deletion
Malformed rows are preserved in an error CSV so the user can inspect what went wrong.

### SQLite for run history
SQLite is lightweight, requires no external database server, and is suitable for a portfolio automation project.

### Email disabled by default
The project never sends email unexpectedly. SMTP is enabled only through environment variables.

### Dashboard over a raw CLI
The dashboard makes the project easier to demonstrate during an internship review while the CLI remains available for automation and health checks.

## 5. Failure handling

- Missing CSV → pipeline fails with a clear message.
- Missing required column → validation raises an error.
- Invalid row → row is quarantined and processing continues.
- PDF generation failure → run is marked FAILED.
- Email failure → SMTP retry is attempted up to three times.
- Every pipeline exception is stored in SQLite.

## 6. Deployment considerations

The FastAPI app can be deployed as a Python web service. The service exposes `/health` for health monitoring.

The scheduler is implemented in-process for local/self-hosted execution. For a production environment where the web process can sleep or restart, use the hosting provider's cron/job facility to invoke the pipeline command at 09:00. This keeps scheduled execution independent from HTTP traffic.

## 7. Security

- No secrets are hard-coded.
- Email credentials are environment variables.
- `.env` should remain local and should never be committed.
- Uploaded filenames are reduced to their basename before saving.
