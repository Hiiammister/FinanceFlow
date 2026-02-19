from datetime import datetime
from dateutil.relativedelta import relativedelta

from core.reports import month_totals, category_totals
from core.budgets import list_budgets

def prev_month(month: str) -> str:
    dt = datetime.strptime(month + "-01", "%Y-%m-%d")
    prev = dt - relativedelta(months=1)
    return prev.strftime("%Y-%m")

def budget_gaps(month: str):
    budgets = list_budgets(month)
    spent_by_cat = {x["category"]: x["amount"] for x in category_totals(month)}

    gaps = []
    for b in budgets:
        spent = float(spent_by_cat.get(b["category"], 0.0))
        budget = float(b["budget_amount"])
        gap = spent - budget
        gaps.append({
            "category": b["category"],
            "budget": budget,
            "spent": spent,
            "gap": gap
        })

    # biggest overruns first
    gaps.sort(key=lambda x: x["gap"], reverse=True)
    return gaps

def trend_vs_last_month(month: str):
    pm = prev_month(month)
    cur = {x["category"]: x["amount"] for x in category_totals(month)}
    prev = {x["category"]: x["amount"] for x in category_totals(pm)}

    all_cats = set(cur) | set(prev)
    trends = []
    for c in all_cats:
        delta = float(cur.get(c, 0.0)) - float(prev.get(c, 0.0))
        trends.append({"category": c, "delta_amount": delta})

    trends.sort(key=lambda x: abs(x["delta_amount"]), reverse=True)
    return trends

def insights_payload(month: str):
    totals = month_totals(month)
    top_cats = category_totals(month)[:8]
    gaps = budget_gaps(month)[:8]
    trends = trend_vs_last_month(month)[:10]
    return {
        "month": month,
        "totals": totals,
        "top_categories": top_cats,
        "budget_gaps": gaps,
        "trend_vs_last_month": trends
    }
