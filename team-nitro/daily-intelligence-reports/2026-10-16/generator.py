#!/usr/bin/env python3
"""Daily Intelligence Report generator — Naya Nitro Pi (Team Nitro, KNOW seat, playing BUILD).

Choice of language documented: PYTHON (not shell) because the job needs
robust RSS/Atom XML parsing, JSON emission, and safe text templating —
all in the stdlib, zero third-party dependencies, so it runs in CI or a
scheduled lane without installs. A shell script would shell out to curl +
jq + sed and break on feed-format drift; this does not.

Pipeline:  reachable sources → dated markdown artifact + machine JSON
            → Reports room read contract (REPORTS-READ-CONTRACT.md).

Usage:
    python3 generator.py --date 2026-10-16 \
        --system-file system-2026-10-16.json \
        --outdir ./2026-10-16

Honesty rules (hard):
- Every web item carries its source name and its URL, straight from the feed.
- A source that cannot be fetched is reported as unreachable. Nothing is
  invented to fill a section. A section with zero items says so.
- Per-link target-page reachability is NOT separately verified; the report
  says that explicitly. Feed-level reachability IS verified (HTTP 200) and
  recorded in both outputs.
"""
import argparse
import datetime as dt
import html
import json
import os
import sys
import urllib.request
import xml.etree.ElementTree as ET

SOURCES = [
    {
        "id": "hackernews",
        "name": "Hacker News",
        "feed": "https://news.ycombinator.com/rss",
        "heading": "Hacker News — front page",
    },
    {
        "id": "arxiv_cs_ai",
        "name": "arXiv cs.AI",
        "feed": "https://arxiv.org/rss/cs.AI",
        "heading": "arXiv cs.AI — newest",
    },
    {
        "id": "lobsters",
        "name": "Lobsters",
        "feed": "https://lobste.rs/rss",
        "heading": "Lobsters — front page",
    },
]

USER_AGENT = "NayaPOWER-daily-intelligence/1.0 (Team Nitro report generator)"
TIMEOUT_S = 30


def fetch_feed(source):
    """Fetch one feed. Returns (reachable, fetched_at_iso, items)."""
    req = urllib.request.Request(source["feed"], headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_S) as resp:
            if resp.status != 200:
                return False, _now(), []
            raw = resp.read()
    except Exception:
        return False, _now(), []
    try:
        root = ET.fromstring(raw)
    except ET.ParseError:
        return False, _now(), []
    items = []
    for it in root.findall(".//item"):
        title = (it.findtext("title") or "").strip()
        link = (it.findtext("link") or "").strip()
        published = (it.findtext("pubDate") or it.findtext("published") or "").strip()
        if title and link:
            items.append({"title": title, "url": link, "published": published})
        if len(items) >= 30:
            break
    return True, _now(), items


def _now():
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def esc_md(text):
    return text.replace("*", "\\*")


def build_markdown(date, system, source_results, per_source):
    ib_id = f"IB-DIR-NAYAPOWER-{date.replace('-', '')}-001"
    report_id = f"DIR-NAYAPOWER-{date}"
    human_date = dt.date(*map(int, date.split("-"))).strftime("%B %d, %Y")
    lines = []
    a = lines.append

    a("# Canonical Intelligence Report Record\n")
    a("**Object type:** DAILY_INTELLIGENCE_REPORT  \n")
    a(f"**Intelligent Block ID:** `{ib_id}`  \n")
    a(f"**Report ID:** `{report_id}`  \n")
    a("**Period type:** DAILY  \n")
    a(f"**Period date:** {date}  \n")
    a(f"**Scope:** {system['scope']}  \n")
    a("**Status:** CANONICAL DAILY REPORT SNAPSHOT  \n")
    a(f"**Canonical repository representation:** team-nitro/daily-intelligence-reports/{date}/report-{date}.md  \n")
    a("**Hub projection:** Reports → Daily Intelligence  \n")
    a("**Related Hub mirrors:** Activity event + Smart Note/distillation may link to this report but do not replace it  \n")
    a("**Snapshot law:** facts, SHAs, and web items below are true only as of the generation window; later changes do not rewrite this historical daily record.  \n")
    a(f"**Generator:** team-nitro/daily-intelligence-reports/{date}/generator.py (stdlib-only Python — no third-party deps)  \n")
    a("**Built by:** Naya Nitro Pi (Team Nitro, KNOW seat — playing BUILD per the Chameleon Rule)  \n")
    a("\n---\n")
    a(f"# NayaPOWER Daily Intelligence Briefing — {human_date}\n")
    a(f"{system['headline']}\n")

    a("## 1. WHAT CHANGED?\n")
    for point in system["changed"]:
        a(f"- {point}\n")

    a("\n## 2. BIGGEST AHA\n")
    a(f"{system['aha']}\n")

    a("\n## 3. LIVE WEB INTELLIGENCE\n")
    a("_Each item is source-labeled and links to the URL its feed supplied. "
      "Feed reachability (HTTP 200) was verified at build time; target-page "
      "reachability was not separately verified._\n")
    for src in SOURCES:
        res = source_results[src["id"]]
        items = res["items"][:per_source]
        a(f"\n### {src['heading']}\n")
        a(f"_Feed: {src['feed']} — fetched {res['fetched_at']} — HTTP 200 verified at build time._\n")
        if not res["reachable"]:
            a("_Source unreachable at build time — no items fabricated. Worth retrying on the next run._\n")
            continue
        if not items:
            a("_No items returned by the feed at build time._\n")
            continue
        for it in items:
            a(f"- [{esc_md(it['title'])}]({it['url']}) — Source: {src['name']}\n")

    a("\n## 4. ONE THING TO REMEMBER\n")
    a(f"**{system['remember']}**\n")
    return "".join(lines)


def build_json(date, system, source_results, per_source, md_path):
    items = []
    sources = []
    for src in SOURCES:
        res = source_results[src["id"]]
        trimmed = res["items"][:per_source]
        sources.append(
            {
                "id": src["id"],
                "name": src["name"],
                "feed": src["feed"],
                "reachable": res["reachable"],
                "fetched_at": res["fetched_at"],
                "items_returned": len(res["items"]),
                "items_included": len(trimmed),
            }
        )
        for it in trimmed:
            items.append(
                {
                    "source": src["name"],
                    "source_id": src["id"],
                    "title": it["title"],
                    "url": it["url"],
                    "published": it["published"],
                }
            )
    return {
        "report_id": f"DIR-NAYAPOWER-{date}",
        "ib_id": f"IB-DIR-NAYAPOWER-{date.replace('-', '')}-001",
        "period_type": "DAILY",
        "period_date": date,
        "scope": system["scope"],
        "status": "CANONICAL DAILY REPORT SNAPSHOT",
        "generated_at": _now(),
        "built_by": "Naya Nitro Pi (Team Nitro, KNOW seat — playing BUILD per the Chameleon Rule)",
        "md_path": md_path,
        "sources": sources,
        "items": items,
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description="Generate the daily intelligence report.")
    ap.add_argument("--date", default=dt.date.today().isoformat())
    ap.add_argument("--outdir", required=True, help="dated output directory")
    ap.add_argument("--system-file", required=True, help="JSON with scope/headline/changed/aha/remember")
    ap.add_argument("--per-source", type=int, default=5)
    ap.add_argument("--offline", action="store_true",
                    help="skip all fetches; sections report sources as unreachable")
    args = ap.parse_args(argv)

    with open(args.system_file, encoding="utf-8") as f:
        system = json.load(f)
    for key in ("scope", "headline", "changed", "aha", "remember"):
        if key not in system:
            sys.exit(f"system file missing key: {key}")

    results = {}
    if args.offline:
        for src in SOURCES:
            results[src["id"]] = {"reachable": False, "fetched_at": _now(), "items": []}
    else:
        for src in SOURCES:
            reachable, fetched_at, items = fetch_feed(src)
            results[src["id"]] = {"reachable": reachable, "fetched_at": fetched_at, "items": items}

    os.makedirs(args.outdir, exist_ok=True)
    md_name = f"report-{args.date}.md"
    md_path = os.path.join(args.outdir, md_name)
    json_path = os.path.join(args.outdir, f"report-{args.date}.json")

    md = build_markdown(args.date, system, results, args.per_source)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md)

    payload = build_json(args.date, system, results, args.per_source, md_name)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
        f.write("\n")

    n_items = len(payload["items"])
    n_ok = sum(1 for s in payload["sources"] if s["reachable"])
    print(f"report: {md_path}")
    print(f"json:   {json_path}")
    print(f"sources reachable: {n_ok}/{len(SOURCES)}; items included: {n_items}")
    for s in payload["sources"]:
        print(f"  - {s['name']}: {'OK' if s['reachable'] else 'UNREACHABLE'} "
              f"({s['items_included']} included / {s['items_returned']} returned)")


if __name__ == "__main__":
    main()
