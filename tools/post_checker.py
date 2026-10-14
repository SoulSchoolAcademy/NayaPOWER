"""Post checker — the comm standard's teeth (Naya 5, 2026-10-14).

Mechanizes the reconciled Team Communication Standard: a board post is
checked against its level's required fields, roster identity, evidence,
score meaning, and next-owner. It FLAGS missing pieces; it does not
reject — enforcement ramps from advisory to gating.

Levels: PULSE (8 fields), RECEIPT (7 fields), EVENT (8 questions).
"""

import re

ROSTER = ["Naya Alpha", "Naya Beta", "Naya Gamma", "Naya Delta",
          "Naya Epsilon", "Naya Zeta", "Naya Eta", "Naya Theta",
          "Naya Iota", "Naya Kappa", "Naya Lambda", "Naya Mu",
          "Naya 1", "Naya 2", "Naya 3", "Naya 4", "Naya 5",
          "Naya Verity", "Naya Resolve", "Naya Clarity"]

PULSE_FIELDS = ["WHO", "MISSION", "STATUS", "TRUTH", "SCORE", "BLOCKER",
                "NEXT", "SOURCE"]
RECEIPT_FIELDS = ["WHO", "NUTSHELL", "WHAT", "EVIDENCE", "SCORE",
                  "CONNECTS", "NEEDS"]
EVENT_QUESTIONS = ["discover", "evidence", "wrong", "falsif",
                   "updated", "behavior", "verifier", "successor"]

SHA_RE = re.compile(r"\b[0-9a-f]{7,40}\b")
REF_RE = re.compile(r"#\d{3,5}")
SCORE_RE = re.compile(r"(\d+(?:\.\d+)?)\s*/\s*10")


def _has(body, *needles):
    low = body.lower()
    return [n for n in needles if n.lower() not in low]


LEADERS = ["Naya Clarity", "Naya Verity", "Naya Resolve"]

# The three leads sign with the family name: Naya Clarity Narzan, etc.
# Their agents sign "Naya <Leader> <Name>" — no Narzan. That asymmetry is
# deliberate: it ends the name confusion between lead and agent for good.
LEAD_FULL = ["Naya Clarity Narzan", "Naya Verity Narzan",
             "Naya Resolve Narzan"]

# Shawn's naming law (2026-10-14): a leader's agent signs
# "Naya <Leader> <Name>" — the given name becomes the last name.
# A bare "Naya <Name>" is incomplete, not wrong: it needs its leader prefix.
AGENT_RE = re.compile(r"\bNaya\s+(Clarity|Verity|Resolve)\s+[A-Z][a-zA-Z\-]*\b")
BARE_NAYA_RE = re.compile(r"\bNaya\s+[A-Z][a-zA-Z\-]*\b")


def check_identity(body, roster=ROSTER):
    """Roster seats and leader-prefixed agents only. Returns (ok, detail)."""
    for lead in LEAD_FULL:
        if lead.lower() in body.lower():
            return True, f"signed: lead {lead}"
    m = AGENT_RE.search(body)
    if m:
        return True, f"signed: leader agent {m.group(0)}"
    for seat in roster:
        if seat.lower() in body.lower():
            return True, f"signed: {seat}"
    bare = BARE_NAYA_RE.search(body)
    if bare:
        return False, (f"incomplete identity '{bare.group(0)}' — "
                       "Shawn's naming law needs the leader prefix: "
                       "'Naya <Clarity|Verity|Resolve> <Name>'")
    return False, "no roster seat name found — identity unbound"


def check_evidence(body):
    """A SHA, a PR/issue ref, or a run id — or it didn't happen."""
    hits = SHA_RE.findall(body) + REF_RE.findall(body)
    if hits:
        return True, f"evidence anchors: {hits[:3]}"
    return False, "no SHA, PR/issue ref, or run id found"


def check_score(body):
    """A score with meaning, not a bare number."""
    m = SCORE_RE.search(body)
    if not m:
        return False, "no X/10 score found"
    low = body.lower()
    meaning = any(w in low for w in
                  ["why not 10", "why it is not", "meaning", "ships",
                   "one more pass", "rework", "backwards", "held",
                   "blocked", "verified"])
    if meaning:
        return True, f"score {m.group(0).strip()} with meaning"
    return False, f"score {m.group(0).strip()} present but meaning unstated"


def check_level(body, level):
    """Required fields for the post's level."""
    if level == "PULSE":
        missing = _has(body, *PULSE_FIELDS)
    elif level == "RECEIPT":
        missing = _has(body, *RECEIPT_FIELDS)
    elif level == "EVENT":
        missing = _has(body, *EVENT_QUESTIONS)
    else:
        return False, f"unknown level {level!r}"
    if missing:
        return False, f"missing {level} fields: {missing}"
    return True, f"all {level} fields present"


def check_post(body, level="RECEIPT", roster=ROSTER):
    """Full check. Returns (verdict, findings).

    verdict: "PASS" or "FLAG". findings: list of (check, ok, detail).
    """
    findings = []
    for name, fn in [("identity", lambda b: check_identity(b, roster)),
                     ("level", lambda b: check_level(b, level)),
                     ("evidence", check_evidence),
                     ("score", check_score)]:
        ok, detail = fn(body)
        findings.append((name, ok, detail))
    verdict = "PASS" if all(ok for _, ok, _ in findings) else "FLAG"
    return verdict, findings


def describe(verdict_findings):
    """One-line human rendering."""
    verdict, findings = verdict_findings
    bad = [f"{n}: {d}" for n, ok, d in findings if not ok]
    if verdict == "PASS":
        return "PASS — identity, fields, evidence, and score meaning present"
    return "FLAG — " + "; ".join(bad)


def main(argv=None):
    """CLI: check a board post file (or stdin) against the standard.

    Exit 0 on PASS, 1 on FLAG — wired for pre-post self-checks and CI.
    """
    import argparse
    import sys
    ap = argparse.ArgumentParser(
        description="Check a team board post against the Team Feed Standard.")
    ap.add_argument("file", nargs="?",
                    help="Post text file (default: read stdin)")
    ap.add_argument("--level", default="RECEIPT",
                    choices=["PULSE", "RECEIPT", "EVENT"],
                    help="Post level to check against")
    args = ap.parse_args(argv)
    body = open(args.file, encoding="utf-8").read() if args.file \
        else sys.stdin.read()
    verdict, findings = check_post(body, level=args.level)
    print(describe((verdict, findings)))
    for name, ok, detail in findings:
        if not ok:
            print(f"  ! {name}: {detail}")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    import sys
    raise SystemExit(main())
