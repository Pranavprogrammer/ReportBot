import pandas as pd

def calculate_metrics(df: pd.DataFrame):
    if df.empty:
        return {
            "total_revenue": 0,
            "orders": 0,
            "aov": 0,
            "mom_growth": 0,
            "clv": 0,
            "top_products": [],
            "regional": [],
            "daily_revenue": []
        }

    orders = int(df["order_id"].nunique())
    revenue = float(df["revenue"].sum())
    aov = revenue / orders if orders else 0

    dates = pd.to_datetime(df["date"])
    monthly = df.assign(month=dates.dt.to_period("M")).groupby("month")["revenue"].sum().sort_index()
    if len(monthly) >= 2 and monthly.iloc[-2] != 0:
        mom = float((monthly.iloc[-1] - monthly.iloc[-2]) / monthly.iloc[-2] * 100)
    else:
        mom = 0.0

    customer_proxy = orders
    clv = aov * 12  # simple portfolio-friendly annualized proxy

    top = (
        df.groupby("product")["revenue"].sum()
        .sort_values(ascending=False).head(5)
        .reset_index()
    )
    top_products = [{"product": r["product"], "revenue": round(float(r["revenue"]), 2)}
                    for _, r in top.iterrows()]

    regional = (
        df.groupby("region")["revenue"].sum()
        .sort_values(ascending=False).reset_index()
    )
    regional_data = [{"region": r["region"], "revenue": round(float(r["revenue"]), 2)}
                     for _, r in regional.iterrows()]

    daily = (
        df.groupby("date")["revenue"].sum().reset_index().sort_values("date")
    )
    daily_data = [{"date": r["date"], "revenue": round(float(r["revenue"]), 2)}
                  for _, r in daily.iterrows()]

    return {
        "total_revenue": round(revenue, 2),
        "orders": orders,
        "aov": round(aov, 2),
        "mom_growth": round(mom, 2),
        "clv": round(clv, 2),
        "top_products": top_products,
        "regional": regional_data,
        "daily_revenue": daily_data
    }
