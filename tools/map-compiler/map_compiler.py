#!/usr/bin/env python3
"""Living Map compiler v1 — the map stops being a document, becomes a measurement.

Each probe measures one slice of live state and returns:
    {status: green|amber|red|unknown, evidence: str, measured_at: ISO-UTC}

Rules (non-negotiable):
  - A probe that cannot measure returns status `unknown` with loud evidence.
    Never silent. Never fake green.
  - Judgments stay human; measurements are mechanical.
  - Exit code is 0 even when everything is red — a red measurement is data,
    not a crash. A traceback means the compiler itself broke (loud failure).

Environment:
  GH_TOKEN        GitHub token for API reads (required for feeds/bridge/dock/capture).
  SUPABASE_URL    Optional. SUPABASE_KEY optional.
                  Without a service-role/authenticated key, row counts are
                  unmeasurable (anon role is RLS-locked) -> probe reports unknown.

Usage:
  python3 map_compiler.py [--out HUB/MAP-STATE.json]
"""

import argparse
import base64
import datetime
import json
import os
import sys
import urllib.request
import urllib.error

OWNER = "SoulSchoolAcademy"
REPO = "NayaPOWER"
API = "https://api.github.com"
HUB_HOST = "https://nayanet.live"

EXPECTED_FEEDS = [
    "feed", "today", "lists", "spaces", "reports", "library",
    "connect", "ledger", "connections", "mail", "settings", "manifest",
]

# room path -> (seed markers, loader markers)
ROOMS = {
    "hub/": (["OFFICIAL_NOTES"], ["NayaPowerRuntime", "HUB/FEEDS"]),
    "hub/today": (["__fixtures"], ["NayaPowerRuntime", "today()"]),
    "hub/lists": (["ListAdapter", "SEED_"], ["NayaPowerRuntime", "lists()"]),
    "hub/spaces": (["SEED_SPACES"], ["NayaPowerRuntime", "spaces()"]),
    "hub/mail": (["demo:true", "THREADS"], ["NayaPowerRuntime", "smartMail"]),
    "hub/reports": (["RAW_MD"], ["NayaPowerRuntime", "smartReports"]),
    "hub/ledger": (["demoStream", "simLive"], ["NayaPowerRuntime", "smartLedger"]),
    "hub/library": (["CANON_BLOCKS"], ["NayaPowerRuntime", "intelligentLibrary"]),
    "hub/connections": (["NayaPeople", "PACK"], ["NayaPowerRuntime", "smartConnections"]),
}

DOCK_PRS = [2676, 2678, 2679, 2680, 2686]
CAPTURE_WORKFLOW = "nayanet-agent-capture.yml"

# Tables verified to exist via the live OpenAPI spec (47 paths, pulled 2026-10-15).
KNOWN_TABLES = [
    "nayanet_intelligent_blocks",
    "nayanet_intelligence_index",
    "nayanet_smart_ledger",
    "members",
    "smart_note_artifacts",
    "smart_note_events",
    "smart_note_receipts",
    "v7_smart_note_transactions",
]
# The database holds 22 tables total (12,026 rows, verified via Management API
# 2026-10-15); the remaining 14 table names are not inventoried here.


def now_iso():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def gh_get(path, token):
    req = urllib.request.Request(
        API + path,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "User-Agent": "living-map-compiler/1.0",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.load(resp), None
    except urllib.error.HTTPError as e:
        try:
            detail = json.loads(e.read().decode("utf-8") or "{}")
        except Exception:
            detail = {}
        return None, {"http_status": e.code, **detail}
    except Exception as e:  # network failure etc.
        return None, {"error": str(e)}


def fetch_text(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": "living-map-compiler/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def probe_supabase_tables(cfg):
    """Row counts need an authenticated/service key. Anon is RLS-locked (42501).
    Without one, OpenAPI can still confirm table existence — counts stay unknown."""
    lns = []
    url = cfg.get("supabase_url", "").rstrip("/")
    key = cfg.get("supabase_key", "")
    baseline = ("Last verified baseline (2026-10-15, Management API): 22 tables, "
                "12,026 rows — NOT re-measured this run.")
    if not url:
        return {
            "status": "unknown",
            "evidence": ("measurement unavailable: no SUPABASE_URL in this environment. "
                         + baseline + " Row counts require an authenticated key "
                         "(anon role is RLS-locked, 42501) — loud unknown, not fake green."),
            "measured_at": now_iso(),
        }
    # 1. OpenAPI: which known tables are exposed?
    try:
        spec = json.loads(fetch_text(url + "/rest/v1/"))
        paths = spec.get("paths", {})
        present = [t for t in KNOWN_TABLES if f"/{t}" in paths]
        lns.append(f"OpenAPI reachable; {len(present)}/{len(KNOWN_TABLES)} known tables exposed")
    except Exception as e:
        return {"status": "unknown",
                "evidence": (f"measurement unavailable: OpenAPI unreachable ({e}). "
                             + baseline + " An authenticated key is required "
                             "(anon role is RLS-locked, 42501) — loud unknown, not fake green."),
                "measured_at": now_iso()}
    # 2. Row counts — only with a key.
    if not key:
        return {"status": "unknown",
                "evidence": ("; ".join(lns) + ". Row counts unavailable: no SUPABASE_KEY "
                             "(anon role is RLS-locked, 42501). " + baseline
                             + " — loud unknown, not fake green"),
                "measured_at": now_iso()}
    counts = {}
    failures = 0
    for t in present:
        try:
            # exact count via HEAD with Prefer: count=exact (no body transferred)
            req = urllib.request.Request(
                f"{url}/rest/v1/{t}?select=*",
                method="HEAD",
                headers={"apikey": key, "Authorization": f"Bearer {key}",
                         "Prefer": "count=exact"},
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                cr = resp.headers.get("Content-Range", "")
            counts[t] = cr.split("/")[-1] if "/" in cr else "?"
        except Exception as e:
            failures += 1
            counts[t] = f"unreadable ({e})"
    if failures == len(present):
        return {"status": "unknown",
                "evidence": f"tables exposed but unreadable with provided key ({failures}/{len(present)} failed)",
                "measured_at": now_iso()}
    total = sum(int(v) for v in counts.values() if str(v).isdigit())
    status = "green" if failures == 0 else "amber"
    return {"status": status,
            "evidence": f"{len(present)} tables exposed; row counts: {counts}; readable total ~{total}",
            "measured_at": now_iso()}


def probe_feeds(cfg):
    """Each expected HUB/FEEDS/<name>.json on main: exists? fresh? valid? how many items?"""
    token = cfg.get("gh_token", "")
    if not token:
        return {"status": "unknown", "evidence": "measurement unavailable: no GH_TOKEN",
                "measured_at": now_iso()}
    live, missing = [], []
    for name in EXPECTED_FEEDS:
        path = f"HUB/FEEDS/{name}.json"
        data, err = gh_get(f"/repos/{OWNER}/{REPO}/contents/{path}?ref=main", token)
        if err or not data:
            missing.append(name)
            continue
        try:
            raw = base64.b64decode(data["content"])
            obj = json.loads(raw)
            items = len(obj) if isinstance(obj, (list, dict)) else 1
        except Exception as e:
            missing.append(f"{name} (invalid JSON: {e})")
            continue
        # last-commit age
        commits, cerr = gh_get(
            f"/repos/{OWNER}/{REPO}/commits?path={path}&sha=main&per_page=1", token)
        age = "?"
        if commits:
            try:
                dt = datetime.datetime.fromisoformat(
                    commits[0]["commit"]["committer"]["date"].replace("Z", "+00:00"))
                age = str(datetime.datetime.now(datetime.timezone.utc) - dt).split(".")[0]
            except Exception:
                pass
        live.append(f"{name} ({items} items, {age} old)")
    parts = []
    if live: parts.append(f"live: {', '.join(live)}")
    if missing: parts.append(f"missing/invalid: {', '.join(missing)}")
    evidence = "; ".join(parts) if parts else "no feed data"
    if missing and not live:
        status = "red"
    elif missing:
        status = "amber"
    else:
        status = "green"
    return {"status": status, "evidence": evidence, "measured_at": now_iso()}


def probe_bridge(cfg):
    """PR #2679 state + whether bridge code exists in the repo on main."""
    token = cfg.get("gh_token", "")
    if not token:
        return {"status": "unknown", "evidence": "measurement unavailable: no GH_TOKEN",
                "measured_at": now_iso()}
    pr, err = gh_get(f"/repos/{OWNER}/{REPO}/pulls/2679", token)
    pr_state = f"{pr['state']}" if pr else f"unreadable ({err})"
    # bridge code presence: look for the runtime marker in likely locations
    candidates = ["HUB/bridge.js", "HUB/naya-runtime.js", "hub/bridge.js"]
    found = []
    for cpath in candidates:
        data, err = gh_get(f"/repos/{OWNER}/{REPO}/contents/{cpath}?ref=main", token)
        if data and not err:
            found.append(cpath)
    if pr and pr["state"] == "open":
        status, note = "amber", "PR open, unmerged"
    elif pr and pr.get("merged"):
        status, note = ("green" if found else "amber"), "PR merged"
    else:
        status, note = "red", f"PR state: {pr_state}"
    evidence = (f"PR #2679 {pr_state} ({note}); bridge code in repo: "
                + (", ".join(found) if found else "not found at checked paths"))
    return {"status": status, "evidence": evidence, "measured_at": now_iso()}


def probe_rooms(cfg):
    """Fetch the DEPLOYED pages and grep: seed markers vs loader markers."""
    results = {}
    for path, (seeds, loaders) in ROOMS.items():
        url = f"{HUB_HOST}/{path}"
        try:
            text = fetch_text(url)
        except Exception as e:
            results[path] = f"unknown (fetch failed: {e})"
            continue
        seed_hits = [m for m in seeds if m in text]
        loader_hits = [m for m in loaders if m in text]
        if loader_hits and not seed_hits:
            results[path] = "loading"
        elif seed_hits and not loader_hits:
            results[path] = f"seeds ({', '.join(seed_hits)})"
        elif seed_hits and loader_hits:
            results[path] = f"mixed (seeds: {', '.join(seed_hits)}; loaders: {', '.join(loader_hits)})"
        else:
            results[path] = "unknown (no markers matched)"
    n = len(results)
    n_seed = sum(1 for v in results.values() if v.startswith("seeds"))
    n_load = sum(1 for v in results.values() if v == "loading")
    n_unk = sum(1 for v in results.values() if v.startswith("unknown"))
    detail = "; ".join(f"{p}: {v}" for p, v in results.items())
    if n_unk == n:
        status = "unknown"
    elif n_load == n:
        status = "green"
    elif n_seed == n:
        status = "red"
    else:
        status = "amber"
    return {"status": status,
            "evidence": f"{n_seed}/{n} on seeds, {n_load}/{n} loading, {n_unk}/{n} unknown — {detail}",
            "measured_at": now_iso()}


def probe_capture(cfg):
    """Latest runs of the capture workflow: status + age. Is the pump running?"""
    token = cfg.get("gh_token", "")
    if not token:
        return {"status": "unknown", "evidence": "measurement unavailable: no GH_TOKEN",
                "measured_at": now_iso()}
    runs, err = gh_get(
        f"/repos/{OWNER}/{REPO}/actions/workflows/{CAPTURE_WORKFLOW}/runs?per_page=5", token)
    if err or not runs or not runs.get("workflow_runs"):
        return {"status": "unknown",
                "evidence": f"measurement unavailable: workflow runs unreadable ({err})",
                "measured_at": now_iso()}
    wr = runs["workflow_runs"]
    latest = wr[0]
    try:
        dt = datetime.datetime.fromisoformat(
            latest["created_at"].replace("Z", "+00:00"))
        age = str(datetime.datetime.now(datetime.timezone.utc) - dt).split(".")[0]
    except Exception:
        age = "?"
    recent_success = any(r.get("conclusion") == "success" for r in wr)
    recent_failure = any(r.get("conclusion") == "failure" for r in wr)
    # pump = scheduled runs (not just manual dispatches)
    scheduled = [r for r in wr if r.get("event") == "schedule"]
    evidence = (f"latest run {latest.get('status')}/{latest.get('conclusion')} "
                f"({age} old, event={latest.get('event')}); "
                f"{len(scheduled)}/5 recent runs scheduled; "
                f"recent success: {recent_success}, recent failure: {recent_failure}")
    if latest.get("conclusion") == "success" and scheduled:
        status = "green"
    elif recent_success:
        status = "amber"  # works when triggered, no pump
    elif recent_failure:
        status = "red"
    else:
        status = "unknown"
    return {"status": status, "evidence": evidence, "measured_at": now_iso()}


def dock_pr_status(pr_state, merged, ci_state):
    """Honesty-critical dock PR state mapping (pure function, regression-tested).

    merged              -> green   (the planned work landed)
    open (any CI state) -> amber   (in flight: waiting on review/merge, or needs work)
    closed, not merged  -> red     (rejected/abandoned — never green, even with green CI)
    anything else       -> unknown (loud unknown, never silent green)
    """
    if merged:
        return "green"
    if pr_state == "open":
        # amber whether CI is green (waiting on review/merge) or not (needs work)
        return "amber"
    if pr_state == "closed":
        # closed WITHOUT merge: the planned work did not land.
        # Never green — a rejected/abandoned dock item is a red flag,
        # not a quiet pass.
        return "red"
    return "unknown"


def probe_dock(cfg):
    """States + CI of the dock PRs."""
    token = cfg.get("gh_token", "")
    if not token:
        return {"status": "unknown", "evidence": "measurement unavailable: no GH_TOKEN",
                "measured_at": now_iso()}
    rows = []
    worst = "green"
    order = {"red": 3, "amber": 2, "unknown": 2, "green": 0}
    for num in DOCK_PRS:
        pr, err = gh_get(f"/repos/{OWNER}/{REPO}/pulls/{num}", token)
        if err or not pr:
            rows.append(f"#{num}: unreadable")
            worst = "unknown" if worst == "green" else worst
            continue
        sha = pr["head"]["sha"]
        ci, _ = gh_get(f"/repos/{OWNER}/{REPO}/commits/{sha}/check-runs", token)
        checks = (ci.get("check_runs") if ci else []) or []
        concl = {c.get("conclusion") for c in checks}
        if not checks:
            ci_state = "no checks"
        elif concl == {"success"}:
            ci_state = "green"
        elif "failure" in concl:
            ci_state = "failing"
        else:
            ci_state = "pending"
        state = pr["state"]
        merged = bool(pr.get("merged"))
        ps = dock_pr_status(state, merged, ci_state)
        if order[ps] > order[worst]:
            worst = ps
        rows.append(f"#{num} {state}{' (merged)' if merged else ''} (CI {ci_state})")
    return {"status": worst, "evidence": "; ".join(rows), "measured_at": now_iso()}


PROBES = {
    "supabase_tables": probe_supabase_tables,
    "feeds": probe_feeds,
    "bridge": probe_bridge,
    "rooms": probe_rooms,
    "capture": probe_capture,
    "dock": probe_dock,
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="HUB/MAP-STATE.json")
    args = ap.parse_args()

    cfg = {
        "gh_token": os.environ.get("GH_TOKEN", ""),
        "supabase_url": os.environ.get("SUPABASE_URL", ""),
        "supabase_key": os.environ.get("SUPABASE_KEY", ""),
    }

    probes = {}
    for name, fn in PROBES.items():
        try:
            probes[name] = fn(cfg)
        except Exception as e:  # the compiler broke — loud
            probes[name] = {"status": "unknown",
                            "evidence": f"COMPILER ERROR in probe '{name}': {e}",
                            "measured_at": now_iso()}
        # schema-guard every probe result
        p = probes[name]
        assert p["status"] in ("green", "amber", "red", "unknown"), f"bad status in {name}"
        for k in ("status", "evidence", "measured_at"):
            assert k in p, f"missing {k} in {name}"

    summary = {"green": 0, "amber": 0, "red": 0, "unknown": 0}
    for p in probes.values():
        summary[p["status"]] += 1

    state = {"measured_at": now_iso(), "probes": probes, "summary": summary}

    out_path = args.out
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(state, f, indent=2)
        f.write("\n")

    # Loud console report — staleness must be visible, not silent.
    print(f"Living Map compiled at {state['measured_at']} -> {out_path}")
    for name, p in probes.items():
        print(f"  [{p['status'].upper():7}] {name}: {p['evidence'][:160]}")
    print(f"  summary: {summary}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
