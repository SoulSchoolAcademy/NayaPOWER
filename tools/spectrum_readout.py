#!/usr/bin/env python3
"""Spectrum readout — the hive's rung distribution on the -9..+9 Intelligence Hierarchy.

Every sign-out carries a mandatory spectrum line, e.g. "Spectrum +7" or
"Spectrum -4". The hive could not see its own rung distribution. This tool
parses venue comments (or a cached JSON array of comment objects) and emits the
distribution: per-rung counts, N, mean, per-seat breakdown, and the time window.

Parsing contract (fail-closed):
- Fenced code blocks and blockquoted lines are stripped before matching —
  format examples and quoted scores never count. Corrections restate inline,
  never in quotes, so last-wins still holds on the stripped body.
- Unicode dashes (U+2212, U+2013, U+2014) normalize to hyphen first.
- One score per comment: the LAST "Spectrum <int>" match wins, so a CORRECTION
  post that restates the old score then the new one counts the new one.
- "Spectrum 8/10" and "Spectrum 8.5" do not count (fraction/ratio guard);
  a trailing sentence period ("Spectrum +7.") still counts.
- A comment with no parseable spectrum line is unscored, never zero-filled.
- A score outside [-9, +9] is excluded and counted as out-of-range, never clamped.
- A live-mode API failure raises and exits non-zero; no partial readout is
  emitted silently.

Usage:
  python3 tools/spectrum_readout.py --comments-file comments.json [--json]
  python3 tools/spectrum_readout.py --issue 2537 --pages 5 [--json]
  comments.json is a JSON array of objects with at least "id", "body",
  "created_at", and "user" ({"login": ...}).

Output (human): a readable table. Output (--json): the same data as JSON.
"""

import argparse
import json
import re
import subprocess
import sys

REPO = "SoulSchoolAcademy/NayaPOWER"
GH_API = ["gh-api"]  # resolved from PATH; override via --gh-api

SPECTRUM_RE = re.compile(
    r"(?<![-\w])Spectrum\s*:?\s*(?:\(?[Cc]orrected\)?:?\s*)?"
    r"(\(\s*[+-]?\d{1,2}\s*\)|[+-]?\d{1,2})(?![/\d])(?!\.[0-9])(?!-\d)(?!\s*-\s*\d)(?!\w)",
    re.IGNORECASE)
# A 3+-digit "spectrum" number is out of range, not "no line" (audit precision).
SPECTRUM_BIG_RE = re.compile(r"(?<![-\w])Spectrum\s*:?\s*[+-]?\d{3,}", re.IGNORECASE)

# Seat markers seen in the wild (first match in order wins):
#   **Seat:** Naya Resolve Narzan · **Lane:** build        (night-shift runs)
#   **WHO:** Naya Resolve Narzan · lane verify               (verify sign-outs)
#   # PULSE — [Naya Resolve · BUILD] ...                     (pulse headers)
#   **[Naya Mechanic] sign-out — WAVE 173 ...                 (wave sign-outs)
# A seat name is "Naya <word>" (up to three words) on ONE line — never
# trailing prose, never the next line.
NAME = r"Naya [A-Za-z0-9]+(?:[^\S\n]+[A-Za-z0-9]+){0,2}"
# Combined header: [Naya Resolve · BUILD] carries seat AND lane in one bracket.
HEADER_SEAT_LANE_RE = re.compile(r"\[(%s)\s*·\s*([A-Za-z]+)\]" % NAME)
SEAT_PATTERNS = [
    re.compile(r"\*\*Seat:\*\*\s*(%s)" % NAME),
    re.compile(r"\*\*WHO:\*\*\s*(%s)" % NAME),
    re.compile(r"^#\s+[^\n]*\[(%s)\s*[·\]]" % NAME, re.M),
    re.compile(r"^\*?\*?\[(%s)\]" % NAME, re.M),
]
LANE_PATTERNS = [
    re.compile(r"\*\*Lane:\*\*\s*([A-Za-z]+)"),
    re.compile(r"·\s*lane\s+([A-Za-z]+)", re.IGNORECASE),
    re.compile(r"\[LANE\s+([A-Za-z]+)\]"),
]

# Content that must never contribute a score: fenced code blocks (format
# examples) and inline code spans (format mentions), and blockquoted lines
# (quoting someone else's score). Stripped before matching. Fences are split,
# not regex-matched, so an UNCLOSED fence quarantines everything after it —
# the alternating-segment rule puts odd segments inside fences, and a trailing
# unclosed segment is odd by construction. Corrections restate inline, never
# in quotes — last-wins still holds on the stripped body.
QUOTE_RE = re.compile(r"(?m)^\s*>.*$")
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")


def strip_code(body):
    # Split on UNESCAPED fences only: GitHub renders "\```" literally, so an
    # escaped marker must not quarantine the text after it.
    parts = re.split(r"(?<!\\)```", body)
    body = "".join(parts[0::2])
    return INLINE_CODE_RE.sub("", body)

# Unicode dashes normalize to ASCII hyphen before matching (phone-typed
# sign-outs); otherwise a real score is silently dropped as unscored.
DASHES = {"\u2212": "-", "\u2013": "-", "\u2014": "-"}

MIN_RUNG, MAX_RUNG = -9, 9


def parse_comment(comment):
    """Parse one comment dict. Returns a result dict (never raises on content)."""
    body = comment.get("body") or ""
    for dash, hyphen in DASHES.items():
        body = body.replace(dash, hyphen)
    body = QUOTE_RE.sub("", strip_code(body))
    result = {
        "id": comment.get("id"),
        "created_at": comment.get("created_at"),
        "author": (comment.get("user") or {}).get("login"),
        "score": None,
        "seat": None,
        "lane": None,
        "excluded": None,
    }
    hm = HEADER_SEAT_LANE_RE.search(body)
    if hm:
        result["seat"] = hm.group(1).strip()
        result["lane"] = hm.group(2).strip().lower()
    else:
        for pat in SEAT_PATTERNS:
            m = pat.search(body)
            if m:
                result["seat"] = m.group(1).strip() or None
                break
    if result["lane"] is None:
        for pat in LANE_PATTERNS:
            m = pat.search(body)
            if m:
                result["lane"] = m.group(1).strip().lower() or None
                break
    matches = SPECTRUM_RE.findall(body)
    if not matches:
        if SPECTRUM_BIG_RE.search(body):
            result["excluded"] = "out_of_range"
        else:
            result["excluded"] = "no_spectrum_line"
        return result
    # findall captures the number group only — int() cannot fail; no dead branch.
    # findall returns the group; strip any surrounding parens whitespace first.
    raw = matches[-1].strip().strip("()").strip()  # last match wins
    score = int(raw)
    if score < MIN_RUNG or score > MAX_RUNG:
        result["excluded"] = "out_of_range"
        return result
    result["score"] = score
    return result


def aggregate(parsed):
    scored = [p for p in parsed if p["score"] is not None]
    distribution = {}
    for p in scored:
        distribution[p["score"]] = distribution.get(p["score"], 0) + 1
    seats = {}
    for p in scored:
        key = p["seat"] or "unknown"
        s = seats.setdefault(key, {"n": 0, "total": 0})
        s["n"] += 1
        s["total"] += p["score"]
    for s in seats.values():
        s["mean"] = round(s["total"] / s["n"], 2)
        del s["total"]
    excluded = {}
    for p in parsed:
        if p["excluded"]:
            excluded[p["excluded"]] = excluded.get(p["excluded"], 0) + 1
    scores = [p["score"] for p in scored]
    scored_times = [p["created_at"] for p in scored if p.get("created_at")]
    audit = [{"id": p["id"], "score": p["score"], "excluded": p["excluded"],
              "seat": p["seat"], "lane": p["lane"]} for p in parsed]
    return {
        "comments_scanned": len(parsed),
        "comments_scored": len(scored),
        "comments_unscored": len(parsed) - len(scored),
        "excluded": excluded,
        "distribution": dict(sorted(distribution.items())),
        "mean": round(sum(scores) / len(scores), 2) if scores else None,
        "min": min(scores) if scores else None,
        "max": max(scores) if scores else None,
        "by_seat": dict(sorted(seats.items())),
        "window_oldest": min(scored_times) if scored_times else None,
        "window_newest": max(scored_times) if scored_times else None,
        "window_scope": "scored comments",
        "parsed": audit,
    }


def fetch_comments(issue, pages, gh_api_cmd):
    """Fetch the LAST `pages` pages (100/page) of issue comments. Raises on failure."""
    meta = subprocess.run(
        gh_api_cmd + ["GET", f"/repos/{REPO}/issues/{issue}"],
        capture_output=True, text=True, check=False,
    )
    if meta.returncode != 0:
        raise RuntimeError(f"issue metadata fetch failed: {meta.stderr.strip()}")
    total = json.loads(meta.stdout)["comments"]
    last_page = (total + 99) // 100
    first_page = max(1, last_page - pages + 1)
    comments = []
    for page in range(first_page, last_page + 1):
        r = subprocess.run(
            gh_api_cmd + ["GET", f"/repos/{REPO}/issues/{issue}/comments?per_page=100&page={page}"],
            capture_output=True, text=True, check=False,
        )
        if r.returncode != 0:
            raise RuntimeError(f"comments page {page} fetch failed: {r.stderr.strip()}")
        batch = json.loads(r.stdout)
        if not isinstance(batch, list):
            raise RuntimeError(f"comments page {page} returned non-list payload")
        comments.extend(batch)
    return comments, {"issue": issue, "pages": pages, "total_comments": total,
                      "pages_read": [first_page, last_page]}


def render_human(data, source):
    lines = []
    lines.append("SPECTRUM READOUT — hive rung distribution (-9..+9)")
    if source["issue"] == "file":
        n = source['total_comments']
        lines.append(f"source: comments file ({n} comment{'s' if n != 1 else ''})")
    else:
        lines.append(f"source: issue #{source['issue']} comments, pages {source['pages_read'][0]}..{source['pages_read'][1]} of {source['total_comments']}")
    if data["window_oldest"] is None:
        lines.append("window (scored): n/a (no scored comments)")
    else:
        lines.append(f"window (scored): {data['window_oldest']} .. {data['window_newest']}")
    lines.append(f"scored: {data['comments_scored']} / scanned: {data['comments_scanned']} (unscored: {data['comments_unscored']})")
    if data["excluded"]:
        lines.append("excluded: " + ", ".join(f"{k}={v}" for k, v in sorted(data["excluded"].items())))
    lines.append("")
    lines.append("rung  count")
    for rung, count in data["distribution"].items():
        bar = "#" * count
        lines.append(f"{rung:+4d}  {count:5d}  {bar}")
    lines.append("")
    if data["mean"] is None:
        lines.append("mean n/a  min n/a  max n/a  (no scored comments)")
    else:
        lines.append(f"mean {data['mean']}  min {data['min']}  max {data['max']}")
    lines.append("")
    lines.append("by seat:")
    for seat, s in data["by_seat"].items():
        lines.append(f"  {seat}: n={s['n']} mean={s['mean']}")
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Spectrum readout: the hive's rung distribution.")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--comments-file", help="JSON array of comment objects (offline mode)")
    src.add_argument("--issue", type=int, help="issue number for live mode")
    ap.add_argument("--pages", type=int, default=5, help="pages of 100 to read from the tail (live mode)")
    ap.add_argument("--json", action="store_true", dest="as_json", help="emit machine JSON")
    ap.add_argument("--gh-api", default="gh-api", help="gh-api executable")
    args = ap.parse_args(argv)

    if args.comments_file:
        with open(args.comments_file) as f:
            comments = json.load(f)
        source = {"issue": "file", "pages_read": [0, 0], "total_comments": len(comments)}
    else:
        comments, source = fetch_comments(args.issue, args.pages, [args.gh_api])

    if not isinstance(comments, list):
        raise SystemExit("comments payload is not a list — refusing to emit a readout")
    if any(not isinstance(c, dict) for c in comments):
        raise SystemExit("comments payload has non-object items — refusing to emit a readout")

    parsed = [parse_comment(c) for c in comments]
    data = aggregate(parsed)

    if args.as_json:
        print(json.dumps({"source": source, "readout": data}, indent=2))
    else:
        print(render_human(data, source))
    return 0


if __name__ == "__main__":
    sys.exit(main())
