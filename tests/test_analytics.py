import pandas as pd
from reportbot.analytics import calculate_metrics

def test_metrics():
    df = pd.DataFrame([
        {"date":"2026-09-01","product":"A","quantity":2,"price":100,"region":"North","order_id":"1","revenue":200},
        {"date":"2026-09-02","product":"B","quantity":1,"price":300,"region":"South","order_id":"2","revenue":300},
    ])
    m = calculate_metrics(df)
    assert m["total_revenue"] == 500
    assert m["orders"] == 2
    assert m["aov"] == 250
