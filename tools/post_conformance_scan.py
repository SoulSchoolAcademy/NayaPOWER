"""Post-conformance scan — advisory measurement for the Team Feed Standard.

Reads recent comments on a team feed issue, runs tools/post_checker.py
against the posts that DECLARE a level (PULSE / RECEIPT / EVENT), and
reports the conformance rate. Posts that declare no level are NOT judged:
prose is prose; only a post that presents itself for grading is graded
(the orchid-wasp guard — a metric that flags everything measures nothing).

Advisory only: exit 0 always, no comments posted, no writes of any kind.
The scan produces a measurement; enforcement ramps are a separate,
human decision. Designed for a scheduled CI job (job summary + artifact).

Usage:
    GITHUB_TOKEN=... python tools/post_conformance_scan.py \
        --repo SoulSchoolAcademy/NayaPOWER --issue 2537 --max-comments 100
"""

import json
import os
import re
import sys
import urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from post_checker import check_post  # noqa: E402

LEVELS = ("PULSE", "RECEIPT", "EVENT")

# A post declares its level with a bracket tag or a labeled line near the top.
_LEVEL_RE = re.compile(
    r"(?:^|\s)\[(PULSE|RECEIPT|EVENT)\]"
    r"|^(?:level|post-level)\s*[:\-–]\s*(PULSE|RECEIPT|EVENT)\b",
    re.IGNORECASE | re.MULTILINE,
)


def detect_level(body, head_lines=15):
    """Return the declared level, or None when the post declares none.

    Only the first `head_lines` non-empty lines are considered: a level
    declared at the bottom of a long post is not a declaration, it is
    an accident. Case-insensitive.
    """
    head = "\n".join(
        line for line in body.splitlines() if line.strip()
    ).split("\n")
    head = "\n".join(head[:head_lines])
    m = _LEVEL_RE.search(head)
    if not m:
        return None
    return (m.group(1) or m.group(2)).upper()


def fetch_comments(repo, issue, token, max_comments=100):
    """Newest-first comment list (id, user, body) from the issue API.

    Read-only. Pages oldest-first from the API and keeps the newest
    `max_comments` by id.
    """
    comments = []
    page = 1
    while len(comments) < max_comments + 100:
        url = (f"https://api.github.com/repos/{repo}/issues/{issue}/comments"
               f"?per_page=100&page={page}")
        req = urllib.request.Request(
            url,
            headers={"Authorization": f"Bearer {token}",
                     "Accept": "application/vnd.github+json",
                     "User-Agent": "naya-post-conformance-scan"},
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            batch = json.load(resp)
        if not batch:
            break
        comments.extend(batch)
        if len(batch) < 100:
            break
        page += 1
        if page > 10:
            break
    comments.sort(key=lambda c: c["id"])
    return comments[-max_comments:]


def scan(comments):
    """Run the checker over declared-level posts. Returns the report dict."""
    graded = []
    skipped = 0
    for c in comments:
        body = c.get("body") or ""
        level = detect_level(body)
        if level is None:
            skipped += 1
            continue
        verdict, findings = check_post(body, level=level)
        graded.append({
            "comment_id": c["id"],
            "author": (c.get("user") or {}).get("login"),
            "level": level,
            "verdict": verdict,
            "findings": [
                {"check": name, "ok": ok, "detail": detail}
                for name, ok, detail in findings
            ],
        })
    passes = sum(1 for g in graded if g["verdict"] == "PASS")
    return {
        "scanned": len(comments),
        "graded": len(graded),
        "skipped_undeclared": skipped,
        "passed": passes,
        "flagged": len(graded) - passes,
        "conformance_rate": (passes / len(graded) if graded else None),
        "posts": graded,
    }


def render_markdown(report, repo, issue):
    """Human summary for the CI job summary."""
    lines = [
        "# Post-conformance scan (advisory)",
        "",
        f"Feed: `{repo}#{issue}` — {report['scanned']} recent comments scanned.",
        "",
        f"- Graded (declared a level): **{report['graded']}**",
        f"- Skipped (no level declared — prose, not judged): "
        f"{report['skipped_undeclared']}",
        f"- PASS: **{report['passed']}** / FLAG: **{report['flagged']}**",
    ]
    if report["conformance_rate"] is None:
        lines.append("- Conformance rate: n/a (no graded posts in window)")
    else:
        lines.append(
            f"- Conformance rate: **{report['conformance_rate']:.0%}** "
            f"of graded posts")
    lines.append("")
    lines.append("Advisory only: this scan never fails, never posts, never "
                 "writes. It measures; enforcement ramps are human decisions.")
    if report["flagged"]:
        lines.append("")
        lines.append("## Flagged posts")
        for g in report["posts"]:
            if g["verdict"] != "PASS":
                bad = "; ".join(
                    f"{f['check']}: {f['detail']}"
                    for f in g["findings"] if not f["ok"])
                lines.append(
                    f"- comment {g['comment_id']} ({g['author']}, "
                    f"{g['level']}): {bad}")
    return "\n".join(lines) + "\n"


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(
        description="Advisory conformance scan for the Team Feed Standard.")
    ap.add_argument("--repo", default="SoulSchoolAcademy/NayaPOWER")
    ap.add_argument("--issue", default="2537")
    ap.add_argument("--max-comments", type=int, default=100)
    ap.add_argument("--out", default="post-conformance-report.json")
    args = ap.parse_args(argv)

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("GITHUB_TOKEN not set — cannot read feed comments.",
              file=sys.stderr)
        return 0  # advisory: missing credential is not a failure

    comments = fetch_comments(args.repo, args.issue, token,
                              max_comments=args.max_comments)
    report = scan(comments)
    report["repo"] = args.repo
    report["issue"] = args.issue
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
    print(render_markdown(report, args.repo, args.issue))
    return 0  # advisory: the scan never fails


if __name__ == "__main__":
    sys.exit(main())
