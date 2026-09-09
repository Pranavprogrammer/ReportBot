import sqlite3
from datetime import datetime
from .config import DB_PATH

def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                started_at TEXT NOT NULL,
                finished_at TEXT,
                status TEXT NOT NULL,
                files_processed INTEGER DEFAULT 0,
                rows_processed INTEGER DEFAULT 0,
                valid_rows INTEGER DEFAULT 0,
                quarantined_rows INTEGER DEFAULT 0,
                report_file TEXT,
                email_sent INTEGER DEFAULT 0,
                error_message TEXT
            )
        """)
        conn.commit()

def start_run():
    with connect() as conn:
        cur = conn.execute(
            "INSERT INTO runs (started_at, status) VALUES (?, ?)",
            (datetime.now().isoformat(timespec="seconds"), "RUNNING")
        )
        conn.commit()
        return cur.lastrowid

def finish_run(run_id, **values):
    values["finished_at"] = datetime.now().isoformat(timespec="seconds")
    fields = ", ".join(f"{k}=?" for k in values)
    params = list(values.values()) + [run_id]
    with connect() as conn:
        conn.execute(f"UPDATE runs SET {fields} WHERE id=?", params)
        conn.commit()

def get_runs(limit=20):
    with connect() as conn:
        rows = conn.execute(
            "SELECT * FROM runs ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
    return [dict(r) for r in rows]

def get_summary():
    with connect() as conn:
        total = conn.execute("SELECT COUNT(*) FROM runs").fetchone()[0]
        success = conn.execute("SELECT COUNT(*) FROM runs WHERE status='SUCCESS'").fetchone()[0]
        last = conn.execute("SELECT * FROM runs ORDER BY id DESC LIMIT 1").fetchone()
        processed = conn.execute("SELECT COALESCE(SUM(rows_processed),0) FROM runs").fetchone()[0]
    return {
        "total_runs": total,
        "successful_runs": success,
        "rows_processed": processed,
        "last_run": dict(last) if last else None
    }
