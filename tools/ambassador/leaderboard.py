"""Ambassador leaderboard derivation. Alias only, never real identity.
Honest empty state: no events -> empty list, never fabricated ranks."""
def leaderboard(events, links=None):
    totals = {}
    for e in events:
        a = e.get("alias")
        if not a:
            continue
        t = totals.setdefault(a, {"alias": a, "clicks": 0, "signups": 0, "sales": 0, "share": 0.0})
        kind = e.get("kind")
        if kind == "click":
            t["clicks"] += 1
        elif kind == "signup":
            t["signups"] += 1
        elif kind == "sale":
            t["share"] += max(0.0, float(e.get("net", 0)) * 0.5)
            t["sales"] += 1
    rows = sorted(totals.values(), key=lambda r: (-r["share"], -r["signups"], -r["clicks"], r["alias"]))
    for i, r in enumerate(rows, 1):
        r["rank"] = i
    return rows

def my_row(alias, events):
    rows = leaderboard(events)
    for r in rows:
        if r["alias"] == alias:
            return r
    return {"alias": alias, "clicks": 0, "signups": 0, "sales": 0, "share": 0.0, "rank": None}
