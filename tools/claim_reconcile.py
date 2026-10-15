"""Claim reconciler — the machine that catches the next #2597.

THE INCIDENT THIS EXISTS FOR
----------------------------
#2597: a merge intent claimed "green CI" while the Team gate was RED.
A human caught the overstatement. This tool makes the MACHINE catch it.

USAGE
-----
  python3 tools/claim_reconcile.py --pr 2568 --claim-file intent.txt
  python3 tools/claim_reconcile.py --pr 2568 --claim-file intent.txt \
      --require-claims        # the CI gate: silence is BLIND, not clean
  python3 tools/claim_reconcile.py --pr 2568 --claim-file intent.txt \
      --pr-json pr.json --checks-json checks.json     # offline, deterministic

WHAT IT CHECKS (evidence, not trust)
------------------------------------
1. SHA FRESHNESS: if the claim cites a commit SHA, it must equal the PR's
   live head SHA. A "green CI" claim from an older head is STALE (exit 2).
2. BROAD CLAIMS ("green CI", "all checks green"): every check with a
   completed run at the exact head must conclude success. One red/failed
   run = CONFLICT (exit 1) — the #2597 shape.
3. NAMED CLAIMS ("Team gate green"): the named check's LATEST run at the
   head must be success. "Latest" is by started_at — not completed_at —
   because #2552 showed a success and a failure 3s apart, and completed_at
   ordering lets a cherry-picked green win (wave-179 finding). Matching is
   EXACT canonical equality (NFKC + confusable fold + case/separator
   collapse): a homograph name never matches the real check, and a
   substring-only name ("gate" vs "Team gate") is AMBIGUOUS and fails
   closed — never silently bound to the wrong check.
4. BLIND = FAIL CLOSED: if the API cannot be reached or the evidence is
   missing, exit 3. UNKNOWN is not PASS.
5. SILENCE = BLIND (with --require-claims, used by the CI gate): a merge
   intent carrying no adjudicable claims — no broad-green, no named gate,
   no cited SHA — exits 3. A "/merge" with nothing to check is ambiguous,
   not clean.

Exit codes: 0 = reconciled | 1 = CONFLICT | 2 = STALE | 3 = BLIND
Stdlib only. CI-runnable: auth via GITHUB_TOKEN/GH_TOKEN env; offline via
--pr-json / --checks-json fixtures.

WHAT THIS DOES NOT CLAIM (D32)
------------------------------
- It adjudicates CLAIM TEXT, not intent: only claims it can parse.
- It reads the latest 100 check-runs; PRs beyond that are out of scope.
- The confusable table is a curated high-value set (Cyrillic, Greek,
  fullwidth, diacritics) — not the full UTS-39 table. A novel homoglyph
  that survives the fold still fails closed as "no such check"; it can
  never match the wrong check.
- Two checks whose names canonicalize identically collapse in latest_runs
  (latest started_at wins). Check names come from repo workflows, not PR
  bodies, so a PR author cannot plant a homograph check name — but an
  external check app could, and the tool would judge the later-started one.
- A green run proves the machines ran green, not WHAT they verified.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import unicodedata
import urllib.request

REPO = "SoulSchoolAcademy/NayaPOWER"
API = "https://api.github.com"

EXIT_OK = 0
EXIT_CONFLICT = 1
EXIT_STALE = 2
EXIT_BLIND = 3

BROAD_GREEN = re.compile(
    r"\b(green\s+ci|ci\s+(is\s+)?green|all\s+checks\s+(are\s+)?green|"
    r"checks\s+(are\s+)?all\s+green|ci\s+green\s+at|full\s+ci\s+green)\b",
    re.IGNORECASE,
)
SHA_RE = re.compile(r"\b[0-9a-f]{40}\b")
# Unicode-letter name classes: a homograph name must still PARSE (so the
# strict matcher can bind it to the real check) -- parsing wide, matching
# strict. The NAMED_GREEN form captures "<Name> gate|check green"; the name
# is re-joined with the literal so "Team gate green" names the check
# "Team gate" exactly.
NAMED_GREEN = re.compile(
    r"([^\W\d_][\w][\w \-/]{1,48}?)\s+"
    r"(gate|check)\s+(?:is\s+|came\s+back\s+)?green\b",
    re.IGNORECASE,
)
# "Team review: green", "Receipt gate — green"
NAMED_GREEN_COLON = re.compile(
    r"^[\s>*\-]*([^\W\d_][\w][\w \-/]{1,48}?)\s*[:\u2013\u2014-]\s*green\b",
    re.IGNORECASE | re.MULTILINE,
)

GREEN_WORDS = {"green", "passing", "pass", "success", "successful"}


# High-value Latin lookalikes -> ASCII. Not the full UTS-39 table: anything
# the fold does not catch fails closed as "no such check" (never matches
# wrongly), so the table only needs to cover the common attack surface.
_CONFUSABLES = {
    # Cyrillic
    "а": "a", "с": "c", "е": "e", "і": "i", "ј": "j", "о": "o", "р": "p",
    "ѕ": "s", "х": "x", "у": "y", "һ": "h", "ԝ": "w", "ԛ": "q", "ԁ": "d",
    "ԍ": "g", "ԋ": "n", "ԏ": "t", "ԑ": "e", "ԓ": "l", "ԟ": "y",
    "А": "a", "В": "b", "С": "c", "Е": "e", "Н": "h", "І": "i",
    "Ј": "j", "К": "k", "М": "m", "О": "o", "Р": "p", "Ѕ": "s",
    "Т": "t", "Х": "x", "Ү": "y",
    # Greek
    "α": "a", "β": "b", "ε": "e", "ι": "i", "κ": "k", "ν": "v",
    "ο": "o", "ρ": "p", "τ": "t", "υ": "u", "χ": "x", "ζ": "z",
    "η": "n", "μ": "m", "ω": "w", "Α": "a", "Β": "b", "Ε": "e",
    "Η": "h", "Ι": "i", "Κ": "k", "Μ": "m", "Ν": "n", "Ο": "o",
    "Ρ": "p", "Τ": "t", "Υ": "y", "Χ": "x", "Ζ": "z",
}


def canonical(name: str) -> str:
    """Homograph-resistant normalization. NFKC (fullwidth -> ASCII),
    confusable fold (Cyrillic/Greek lookalikes -> Latin), diacritic strip,
    then case/separator collapse. Two names are equal only if they say the
    same thing through the same letters -- lookalikes never match."""
    s = unicodedata.normalize("NFKC", name)
    s = "".join(_CONFUSABLES.get(ch, ch) for ch in s)
    s = "".join(ch for ch in unicodedata.normalize("NFKD", s)
                if not unicodedata.combining(ch))
    s = s.lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def norm(name: str) -> str:
    return canonical(name)


def match_check(want: str, runs: dict) -> tuple:
    """Named-claim resolution. Exact canonical equality matches; anything
    less (substring-only) is AMBIGUOUS and fails closed -- "gate" must never
    silently match "gatekeeper" while "Team gate" is red."""
    exact = [(k, r) for k, r in runs.items() if k == want]
    if len(exact) == 1:
        return exact[0][1], "exact"
    if len(exact) > 1:
        return None, "ambiguous"
    partial = [(k, r) for k, r in runs.items() if want in k or k in want]
    if partial:
        return None, "ambiguous"
    return None, "none"


def api_get(path: str) -> dict:
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    req = urllib.request.Request(API + path)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:  # noqa: BLE001 - blindness is a verdict, not a traceback
        raise RuntimeError(f"BLIND: GET {path} failed: {type(e).__name__}: {e}")


def parse_claim(text: str) -> dict:
    cited = sorted(set(SHA_RE.findall(text)))
    named = set()
    for m in NAMED_GREEN.finditer(text):
        # re-join the literal: "Team gate green" names check "Team gate"
        named.add(canonical(m.group(1) + " " + m.group(2)))
    for m in NAMED_GREEN_COLON.finditer(text):
        candidate = canonical(m.group(1))
        if candidate not in GREEN_WORDS and len(candidate) > 2:
            named.add(candidate)
    return {
        "broad_green": bool(BROAD_GREEN.search(text)),
        "cited_shas": cited,
        "named_green": sorted(named),
    }


def latest_runs(checks: list) -> dict:
    """Latest completed run per check name. Latest = by started_at.
    Wave-179 lesson: #2552 had success+failure 3s apart; completed_at
    ordering lets a cherry-picked green win. started_at is the order
    the machines actually ran."""
    best: dict[str, dict] = {}
    for run in checks:
        name = run.get("name", "")
        status = run.get("status")
        started = run.get("started_at") or ""
        key = norm(name)
        cur = best.get(key)
        if cur is None or started > (cur.get("started_at") or ""):
            if status == "completed":
                best[key] = run
            elif cur is None:
                best[key] = run  # keep in-progress record if nothing completed
    return best


def reconcile(claim_text: str, pr: dict, checks: list) -> dict:
    claim = parse_claim(claim_text)
    head = (pr.get("head") or {}).get("sha", "")
    verdict = {"pr": pr.get("number"), "head_sha": head,
               "claim": claim, "findings": [], "verdict": "RECONCILED"}
    blind = not head or not checks

    # 1. SHA freshness
    for sha in claim["cited_shas"]:
        if sha != head:
            verdict["findings"].append(
                {"kind": "STALE",
                 "detail": f"claim cites {sha[:12]}... but PR head is {head[:12]}...",
                 "cited": sha, "head": head})
            verdict["verdict"] = "STALE"

    if blind:
        verdict["findings"].append(
            {"kind": "BLIND", "detail": "missing head SHA or check-runs; cannot adjudicate"})
        verdict["verdict"] = "BLIND"
        return verdict

    runs = latest_runs(checks)

    def run_evidence(run: dict) -> dict:
        return {"name": run.get("name"), "run_id": run.get("id"),
                "conclusion": run.get("conclusion"), "status": run.get("status"),
                "head_sha": run.get("head_sha"), "started_at": run.get("started_at"),
                "html_url": run.get("html_url")}

    # 2. Broad claims
    if claim["broad_green"]:
        bad = []
        for key, run in sorted(runs.items()):
            if run.get("status") != "completed" or run.get("conclusion") != "success":
                bad.append(run_evidence(run))
        if bad:
            verdict["findings"].append(
                {"kind": "CONFLICT",
                 "detail": "claimed 'green CI' but these checks are not green at the head",
                 "checks": bad})
            verdict["verdict"] = "CONFLICT"

    # 3. Named claims — exact canonical match only; homograph games fail closed
    for want in claim["named_green"]:
        match, kind = match_check(want, runs)
        if kind == "ambiguous":
            verdict["findings"].append(
                {"kind": "CONFLICT", "match": "ambiguous",
                 "detail": f"claimed '{want}' green but the name matches no "
                           "check exactly -- refusing a partial match",
                 "want": want})
            verdict["verdict"] = "CONFLICT"
        elif match is None:
            verdict["findings"].append(
                {"kind": "CONFLICT", "match": "none",
                 "detail": f"claimed '{want}' green but no such check ran at the head",
                 "want": want})
            verdict["verdict"] = "CONFLICT"
        elif match.get("status") != "completed" or match.get("conclusion") != "success":
            verdict["findings"].append(
                {"kind": "CONFLICT", "match": "exact",
                 "detail": f"claimed '{want}' green but live run is "
                           f"{match.get('status')}/{match.get('conclusion')}",
                 "check": run_evidence(match)})
            verdict["verdict"] = "CONFLICT"

    if verdict["verdict"] == "RECONCILED":
        verdict["evidence"] = {
            "checks_seen": len(runs),
            "green": sum(1 for r in runs.values()
                         if r.get("status") == "completed" and r.get("conclusion") == "success"),
        }
    return verdict


def main() -> int:
    ap = argparse.ArgumentParser(description="Reconcile CI claims against live check-run evidence.")
    ap.add_argument("--pr", type=int, required=True)
    ap.add_argument("--claim-file", required=True)
    ap.add_argument("--pr-json", help="offline PR fixture")
    ap.add_argument("--checks-json", help="offline check-runs fixture")
    ap.add_argument("--require-claims", action="store_true",
                    help="fail BLIND when the claim text carries no adjudicable "
                         "claims (the CI gate passes this; silence is not clean)")
    ap.add_argument("--out", help="write verdict JSON here")
    args = ap.parse_args()

    try:
        with open(args.claim_file, encoding="utf-8") as f:
            claim_text = f.read()
    except OSError as e:
        print(json.dumps({"verdict": "BLIND", "detail": f"cannot read claim file: {e}"}))
        return EXIT_BLIND

    try:
        if args.pr_json:
            with open(args.pr_json, encoding="utf-8") as f:
                pr = json.load(f)
        else:
            pr = api_get(f"/repos/{REPO}/pulls/{args.pr}")
        if args.checks_json:
            with open(args.checks_json, encoding="utf-8") as f:
                checks_payload = json.load(f)
        else:
            head = (pr.get("head") or {}).get("sha", "")
            if not head:
                raise RuntimeError("BLIND: PR has no head SHA")
            checks_payload = api_get(
                f"/repos/{REPO}/commits/{head}/check-runs?per_page=100")
        checks = checks_payload.get("check_runs", checks_payload if isinstance(checks_payload, list) else [])
    except RuntimeError as e:
        print(json.dumps({"verdict": "BLIND", "detail": str(e)}))
        return EXIT_BLIND

    verdict = reconcile(claim_text, pr, checks)

    # Fail-closed on silence: a merge intent carrying no adjudicable claims
    # is ambiguous, not clean. --require-claims (used by the CI gate) turns
    # that into BLIND.
    c = verdict["claim"]
    adjudicable = c["broad_green"] or c["cited_shas"] or c["named_green"]
    if args.require_claims and not adjudicable and verdict["verdict"] == "RECONCILED":
        verdict["verdict"] = "BLIND"
        verdict["findings"].append(
            {"kind": "BLIND",
             "detail": "merge intent carried no adjudicable claims "
                       "(no broad-green, no named gate, no cited SHA) -- "
                       "refusing to pass on silence"})

    out = json.dumps(verdict, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(out + "\n")
    print(out)
    return {"RECONCILED": EXIT_OK, "CONFLICT": EXIT_CONFLICT,
            "STALE": EXIT_STALE, "BLIND": EXIT_BLIND}[verdict["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
