import pandas as pd
from core.db import get_conn

def df_transactions_for_month(month: str) -> pd.DataFrame:
    conn = get_conn()
    rows = conn.execute("""
        SELECT * FROM transactions
        WHERE substr(date, 1, 7) = ?
        ORDER BY date ASC
    """, (month,)).fetchall()
    conn.close()
    return pd.DataFrame([dict(r) for r in rows])

def month_totals(month: str):
    df = df_transactions_for_month(month)
    if df.empty:
        return {"income": 0.0, "expense": 0.0, "net": 0.0}

    income = float(df[df["type"] == "income"]["amount"].sum())
    expense = float(df[df["type"] == "expense"]["amount"].sum())
    return {"income": income, "expense": expense, "net": income - expense}

def category_totals(month: str):
    df = df_transactions_for_month(month)
    if df.empty:
        return []

    exp = df[df["type"] == "expense"]
    if exp.empty:
        return []

    grouped = exp.groupby("category")["amount"].sum().sort_values(ascending=False)
    return [{"category": k, "amount": float(v)} for k, v in grouped.items()]
