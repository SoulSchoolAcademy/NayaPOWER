"""Improved graphs, single derivation.
One function feeds wall header, Reports, mix, Today, 14-day trend, streak,
and the ambassador series, so four renderings cannot drift."""
from datetime import date, timedelta

def series(days):
    """days: list of {date: 'YYYY-MM-DD', posts, messages, invites, clicks, signups, sales}."""
    by_date = {d["date"]: d for d in days}
    out = []
    today = date.today()
    for i in range(13, -1, -1):
        d = (today - timedelta(days=i)).isoformat()
        row = by_date.get(d, {})
        out.append({"date": d, "posts": row.get("posts", 0), "messages": row.get("messages", 0),
                    "invites": row.get("invites", 0), "clicks": row.get("clicks", 0),
                    "signups": row.get("signups", 0), "sales": row.get("sales", 0)})
    return out

def streak(days):
    s = series(days)
    n = 0
    for row in reversed(s):
        total = row["posts"] + row["messages"] + row["invites"] + row["clicks"]
        if total > 0:
            n += 1
        else:
            break
    return n

def totals(days):
    s = series(days)
    keys = ["posts", "messages", "invites", "clicks", "signups", "sales"]
    return {k: sum(r[k] for r in s) for k in keys}
