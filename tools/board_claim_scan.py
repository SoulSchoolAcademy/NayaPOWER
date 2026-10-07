"""Board claim scan — one-repair-per-class as muscle memory.

WHY THIS EXISTS
---------------
Duplicate work is the defect coordinated overlap exists to prevent. The
2026-10-02 #1315 incident (byte-identical duplicate repair of #1312) and the
2026-10-01 SN-018 double-claim both happened because a seat built without
scanning what was already claimed. The standing prose ("list open PRs before
opening a repair") is correct but unenforced — prose doesn't run.

This tool runs the check mechanically. Before building ANYTHING (repair PR,
feature, Smart Note, law), run it:

    python3 tools/board_claim_scan.py --work "repair: brain index drift on main"

It scans (1) open PRs and (2) the live team board's recent comments for
existing claims on the same work, and verdicts:

    CLEAR      — no conflicting claim found; build.
    COLLISION  — an open PR or board claim covers this work; STOP, coordinate
                 on the board, and either stand down or consolidate.

Exit codes: 0 = CLEAR, 2 = COLLISION, 3 = environment failure (could not
fetch; do not treat as clear — UNKNOWN != PASS).

Matching is keyword-based and deliberately recall-biased: a false positive
costs a minute of reading; a missed duplicate costs a second PR, a renumber,
or a reverted merge. Weak matches are listed as advisories, not collisions.

Stdlib only. Fetches via ~/workspace/naya/bin/gh-api when available, else
accept --prs-json / --board-json for offline testing.
"""

import argparse
import json
import re
import subprocess
import sys

REPO = "SoulSchoolAcademy/NayaPOWER"
GH_API = "/home/hatch/workspace/naya/bin/gh-api"

STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "to", "in", "on", "for", "with",
    "pr", "issue", "merge", "merged", "open", "closed", "fix", "feat",
    "docs", "repair", "build", "new", "from", "this", "that", "is",
}

# Coordination chatter, not work identifiers: shared "claim"/"board"/"scan"
# proves nothing about the SAME work being claimed.
DOMAIN_STOPWORDS = {
    "claim", "claimed", "board", "scan", "scanning", "collision", "seat",
    "lane", "team", "naya", "coda", "shawn", "sign", "receipt",
}


def tokens(text):
    words = re.findall(r"[a-z0-9]+", text.lower())
    # Keep hyphenated compounds whole too: "full-auto-merge-v1" is far more
    # distinctive than {full, auto} once "merge" is stopworded out.
    compounds = re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)+", text.lower())
    kept = [w for w in words if w not in STOPWORDS and w not in DOMAIN_STOPWORDS]
    toks = {w for w in kept if len(w) > 2}
    # Version tokens: "v9" is short but highly distinctive.
    toks.update(w for w in kept if re.fullmatch(r"v\d+", w))
    toks.update(c for c in compounds if len(c) > 4)
    # Adjacent bigrams of kept tokens: "ask naya v9" survives even though
    # "naya" alone is domain chatter.
    toks.update(f"{a} {b}" for a, b in zip(kept, kept[1:]) if len(a) > 1 and len(b) > 1)
    return toks


def gh_api(method, path):
    out = subprocess.run(
        ["sh", "-c", 'exec "$0" "$@"', GH_API, method, path],
        capture_output=True, text=True, timeout=60,
    )
    if out.returncode != 0:
        raise RuntimeError(f"gh-api {method} {path} failed: {(out.stderr or out.stdout)[:200]}")
    return json.loads(out.stdout)


def fetch_open_prs():
    """Read all open PR pages within a bounded budget; never truncate to CLEAR."""
    items = []
    seen = set()
    for page in range(1, 11):
        data = gh_api("GET", f"/repos/{REPO}/pulls?state=open&per_page=100&page={page}")
        if not isinstance(data, list) or len(data) > 100:
            raise RuntimeError("PR_COVERAGE: malformed PR page")
        for p in data:
            if (not isinstance(p, dict) or type(p.get("number")) is not int
                    or not isinstance(p.get("title"), str)
                    or not isinstance(p.get("head"), dict)
                    or not isinstance(p["head"].get("ref"), str)):
                raise RuntimeError("PR_COVERAGE: malformed PR")
            if p["number"] in seen:
                raise RuntimeError("PR_COVERAGE: duplicate PR; retry scan")
            seen.add(p["number"])
            items.append({
                "kind": "pr",
                "id": p["number"],
                "title": p["title"],
                "ref": p["head"]["ref"],
                "text": f"{p['title']} {p['head']['ref']}",
            })
        if len(data) < 100:
            return items
    raise RuntimeError("PR_PAGINATION_LIMIT: no terminal page within 1000 PRs; cannot declare CLEAR")


def fetch_board_tail(board, pages=2):
    """Read the newest pages*100 comments, refusing an incomplete snapshot.

    GitHub's issue-comment endpoint orders by ascending ID, so pages 1..2
    are the oldest comments, not the tail. Counts locate the final window;
    a changed count requires a fresh scan rather than a false CLEAR.
    """
    if type(pages) is not int or pages < 1:
        raise ValueError("pages must be a positive integer")
    issue_path = f"/repos/{REPO}/issues/{board}"

    def comment_count():
        issue = gh_api("GET", issue_path)
        count = issue.get("comments") if isinstance(issue, dict) else None
        if type(count) is not int or count < 0:
            raise RuntimeError("BOARD_COMMENT_COUNT: missing or invalid count")
        return count

    count = comment_count()
    first_page = max(0, count - pages * 100) // 100 + 1
    last_page = (count + 99) // 100
    items = []
    for page in range(first_page, last_page + 1):
        data = gh_api(
            "GET",
            f"/repos/{REPO}/issues/{board}/comments?per_page=100&page={page}",
        )
        expected = min(100, count - (page - 1) * 100)
        if not isinstance(data, list) or len(data) != expected:
            raise RuntimeError("BOARD_COVERAGE: incomplete comment page; retry scan")
        for c in data:
            if (not isinstance(c, dict) or type(c.get("id")) is not int
                    or not isinstance(c.get("body"), str)):
                raise RuntimeError("BOARD_COVERAGE: malformed comment")
            if items and c["id"] <= items[-1]["id"]:
                raise RuntimeError("BOARD_COVERAGE: duplicate or unordered comments")
            items.append(
                {
                    "kind": "board",
                    "id": c["id"],
                    "title": c["body"][:80].replace("\n", " "),
                    "ref": "",
                    "text": c["body"][:2000],
                }
            )
    if comment_count() != count:
        raise RuntimeError("BOARD_CHANGED: comment count moved; retry scan")
    return items[-pages * 100:]


def scan(work, candidates):
    work_toks = tokens(work)
    collisions = []
    advisories = []
    for cand in candidates:
        cand_toks = tokens(cand["text"])
        shared = work_toks & cand_toks
        shared_compounds = {t for t in shared if "-" in t}
        shared_bigrams = {t for t in shared if " " in t}
        shared_unigrams = shared - shared_compounds - shared_bigrams
        # A bigram carrying a version token ("ask v9") is as identifying as a
        # compound — versioned workstreams are the unit of duplication.
        versioned_bigrams = {t for t in shared_bigrams if re.search(r"v\d+", t)}
        # Collision: a shared compound identifier (PR-1444, SN-0296,
        # full-auto-merge-v1), a versioned bigram, >= 2 shared bigram phrases,
        # or >= 4 shared distinctive unigrams. A single generic bigram
        # ("hub rooms") is topical, not identical work -> advisory.
        # Generic coordination vocabulary alone never collides.
        if shared_compounds or versioned_bigrams or len(shared_bigrams) >= 2 or len(shared_unigrams) >= 4:
            collisions.append((cand, sorted(shared)))
        elif len(shared) >= 2:
            advisories.append((cand, sorted(shared)))
    return collisions, advisories


def main(argv):
    ap = argparse.ArgumentParser(description="Scan for existing claims before building.")
    ap.add_argument("--work", required=True, help="Description of the work you intend to build.")
    ap.add_argument("--board", default="1354", help="Team board issue number.")
    ap.add_argument("--prs-json", help="Offline: JSON file with open-PR list.")
    ap.add_argument("--board-json", help="Offline: JSON file with board comments.")
    args = ap.parse_args(argv)

    try:
        if args.prs_json:
            prs = json.load(open(args.prs_json))
        else:
            prs = fetch_open_prs()
        if args.board_json:
            board = json.load(open(args.board_json))
        else:
            board = fetch_board_tail(args.board)
    except Exception as exc:  # noqa: BLE001 — environment failure is a verdict
        print(f"ENVIRONMENT FAILURE: {exc} — could not scan; do NOT treat as clear.")
        return 3

    candidates = prs + board
    collisions, advisories = scan(args.work, candidates)

    print(f"work: {args.work}")
    print(f"scanned: {len(prs)} open PRs, {len(board)} board comments")
    if collisions:
        print("VERDICT: COLLISION — do not build; coordinate first.")
        for cand, shared in collisions:
            print(f"  - [{cand['kind']} {cand['id']}] {cand['title'][:100]} (shared: {', '.join(shared)})")
        return 2
    print("VERDICT: CLEAR — no conflicting claim found.")
    if advisories:
        print("advisories (weak matches, review before building):")
        for cand, shared in advisories[:5]:
            print(f"  - [{cand['kind']} {cand['id']}] {cand['title'][:100]} (shared: {', '.join(shared)})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
