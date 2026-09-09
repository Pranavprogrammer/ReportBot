from pathlib import Path
import pandas as pd
from .config import QUARANTINE_DIR

REQUIRED_COLUMNS = ["date", "product", "quantity", "price", "region", "order_id"]

def validate_csv(path: Path):
    df = pd.read_csv(path)
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"{path.name}: missing required columns: {', '.join(missing)}")

    work = df.copy()
    work["_row_number"] = range(2, len(work) + 2)

    work["date_parsed"] = pd.to_datetime(work["date"], errors="coerce")
    work["quantity_num"] = pd.to_numeric(work["quantity"], errors="coerce")
    work["price_num"] = pd.to_numeric(work["price"], errors="coerce")

    invalid = (
        work["date_parsed"].isna()
        | work["quantity_num"].isna()
        | (work["quantity_num"] <= 0)
        | work["price_num"].isna()
        | (work["price_num"] < 0)
        | work["product"].isna()
        | work["region"].isna()
        | work["order_id"].isna()
    )

    bad = work[invalid].copy()
    good = work[~invalid].copy()

    if not bad.empty:
        QUARANTINE_DIR.mkdir(parents=True, exist_ok=True)
        bad["error"] = "Invalid date/quantity/price or missing required value"
        bad.to_csv(QUARANTINE_DIR / f"{path.stem}_errors.csv", index=False)

    good["date"] = good["date_parsed"].dt.strftime("%Y-%m-%d")
    good["quantity"] = good["quantity_num"]
    good["price"] = good["price_num"]
    good["revenue"] = good["quantity"] * good["price"]

    return good[["date", "product", "quantity", "price", "region", "order_id", "revenue"]], len(df), len(bad)
