# ProStackHub_ReportBot — Automated Sales Analytics Pipeline

> Internship Task 5 — ReportBot

ReportBot is a Python automation project that turns incoming sales CSV files into validated analytics, professional PDF reports, email-ready reports, and SQLite-based run history.

## ✨ Features

- CSV ingestion from `data/incoming/`
- Schema/type validation
- Quarantine malformed rows with error logs
- Pandas analytics:
  - daily revenue
  - weekly/monthly analysis
  - top products
  - regional breakdown
  - MoM growth
  - AOV
  - annualized CLV proxy
- Professional PDF generation with ReportLab
- SMTP email delivery with retry logic
- Daily 9:00 AM scheduler
- SQLite pipeline monitoring
- `--status` CLI
- Clean responsive FastAPI dashboard
- PDF download from the dashboard
- `/health` endpoint for deployment monitoring

## 🧱 Architecture

```text
CSV files
   ↓
Validation + quarantine
   ↓
Pandas analytics
   ↓
SQLite run logging
   ↓
ReportLab PDF
   ↓
SMTP email
   ↓
Dashboard + health API
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for the technical write-up.

## 🚀 Run locally in VS Code

### 1. Create/activate a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Install packages

```bash
pip install -r requirements.txt
```

### 3. Start the web app

```bash
uvicorn app:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

### 4. Run the pipeline manually

The repository includes a sample CSV.

```bash
python scripts/run_pipeline.py
```

Then refresh the dashboard. A PDF appears in `data/reports/`.

### 5. Check pipeline health

```bash
python scripts/status.py --status
```

## 📧 Email setup

Email sending is intentionally disabled by default.

Copy `.env.example` to `.env` and configure environment variables before enabling SMTP. Never commit real passwords or app passwords to GitHub.

For Gmail, use an App Password rather than your normal account password.

## ⏰ Scheduling

The application starts a background scheduler and runs daily at 09:00 by default.

For production deployments, configure the hosting environment so the service remains running. A platform cron/job can also call the pipeline command when scheduled execution is required.

## 🌐 Deployment

This project is designed to deploy cleanly on Render or another Python web-service platform.

Typical Render settings:

- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn app:app --host 0.0.0.0 --port $PORT`

Set the email variables as environment variables if email delivery is enabled.

## 📦 Submission checklist

- [x] Public GitHub repository
- [x] Clean README.md
- [x] ARCHITECTURE.md
- [x] Deployable FastAPI application
- [x] PDF report generation
- [x] Automation/scheduling
- [x] SQLite monitoring
- [x] 3-minute walkthrough video to record
- [x] LinkedIn project post to publish

## 🎤 40-second interview explanation

“ReportBot is an automated sales analytics pipeline I built in Python. It takes incoming sales CSV files, validates their schema and data types, quarantines invalid rows, and uses Pandas to calculate revenue, AOV, product performance, regional performance and growth. It then generates a professional PDF report using ReportLab, can email the report through SMTP with retry logic, and stores pipeline execution history in SQLite. I also built a FastAPI dashboard to upload data, run the pipeline and download reports.”

## 🛠️ Tech stack

Python • FastAPI • Pandas • ReportLab • SQLite • SMTP • Schedule • HTML/CSS/JavaScript • Chart.js

## 📁 Project structure

```text
ProStackHub_ReportBot/
├── app.py
├── reportbot/
│   ├── analytics.py
│   ├── config.py
│   ├── database.py
│   ├── emailer.py
│   ├── pipeline.py
│   ├── report.py
│   ├── scheduler.py
│   └── validation.py
├── scripts/
├── data/
│   ├── incoming/
│   ├── quarantine/
│   └── reports/
├── static/
├── templates/
├── tests/
├── ARCHITECTURE.md
├── requirements.txt
├── Procfile
└── runtime.txt
```
