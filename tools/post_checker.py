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

SHA_RE = re.compile(
    r"(?:@\s*|\b(?:sha|commit|tree|tip|head|ref)\s*[:=]?\s*)"
    r"([0-9a-f]{7,40})\b",
    re.IGNORECASE)
REF_RE = re.compile(r"#\d{3,5}(?!\d)")
SCORE_RE = re.compile(r"(\d+(?:\.\d+)?)\s*/\s*10")

# Score-meaning words match on word boundaries only: "relationships" must
# not count as "ships", "meaningless" must not count as "meaning".
# Hyphen-joined words do not count either: "held-out" is not "held".
# The guard covers ASCII hyphen and Unicode dashes (U+2010–U+2015).
MEANING_RE = re.compile(
    r"(?<![\-\u2010-\u2015])\b(why not 10|why it is not|meaning|ships|"
    r"one more pass|rework|backwards|held|blocked|verified)"
    r"\b(?![\-\u2010-\u2015])", re.IGNORECASE)


def _labeled(body, field):
    """True when `field` heads a labeled line: `FIELD: ...`, `**FIELD:**`,
    `**FIELD -> WHY:**`, `FIELD - ...`, `CONNECTS TO: ...`. Unlabeled prose
    never counts — a paragraph that merely *mentions* every field word is
    not a field, and neither is a prose sentence that starts with a field
    word plus a clause (`WHO are we to judge this: nobody.` is prose, not
    a WHO field: only the separator, an `-> ...` suffix, or a `TO`
    suffix may intervene between the field word and the separator."""
    pat = re.compile(
        r"(?im)^\s*(?:[-—–*•>]+\s*)?(?:\*\*)?" + re.escape(field)
        + r"\b(?:\s*(?:\*\*)?\s*[:\-–]|\s+(?:->|→)\s*[^:\n]*[:\-–]"
        + r"|\s+TO\s*(?:\*\*)?\s*[:\-–])")
    return bool(pat.search(body))


def _stem_present(body, stem):
    """EVENT question stems match as a word prefix ('falsif' catches
    'falsified'). Deliberate: EVENT questions are stems, not labels —
    unlike PULSE/RECEIPT fields, which are label-anchored above."""
    return bool(re.search(r"(?i)\b" + re.escape(stem) + r"\w*", body))


# The three leads sign with the family name: Naya Clarity Narzan, etc.
# Their agents sign "Naya <Leader> <Name>" — no Narzan. That asymmetry is
# deliberate: it ends the name confusion between lead and agent for good.
# Identity resolution lives in _candidate_from_text / check_identity:
# signature lines only, mentions never bind.


def _strip_markers(line):
    """Strip leading bullets/dashes/quotes/markdown so a signature line
    like `**[Naya 5] ...` or `— Naya Delta` reads as `Naya 5 ...`."""
    return re.sub(r"^[\s>•\-—–*\[\]]+", "", line.strip())


def _candidate_from_text(text, roster):
    """Classify the name a signature line starts with, or None.

    Returns (kind, name): kind is 'lead' (full `Naya <Leader> Narzan`),
    'agent' (`Naya <Leader> <CapitalizedName>`), 'roster' (a roster seat),
    'leader_malformed' (a `Naya <Leader>` prefix with a non-conforming
    continuation — lowercase name, or no Narzan/agent name at all), or
    'bare' (`Naya <Name>` with no leader prefix).

    The leader-prefix branch runs FIRST, before the roster loop: a
    `Naya <Leader>` prefix must never fall through to the roster match,
    or a bare lead plus one punctuation mark (`WHO: Naya Clarity.`)
    would pass as a roster seat."""
    text = text.lstrip()
    m = re.match(r"Naya\s+(Clarity|Verity|Resolve)(?![A-Za-z])", text)
    if m:
        rest = text[m.end():].strip()
        if not rest:
            return ("leader_malformed", f"Naya {m.group(1)}")
        # The continuation is the immediate next token: a punctuation-
        # only token ("," after "Naya Clarity, Naya Mu") is NOT a name —
        # it is the bare-lead case, never an agent named "Naya".
        nxt = rest.split()[0].strip(".,;:·—–)]}*|!?\"'")
        if not nxt:
            return ("leader_malformed", f"Naya {m.group(1)}")
        if nxt == "Narzan":
            return ("lead", f"Naya {m.group(1)} Narzan")
        if re.fullmatch(r"[A-Z][a-zA-Z\-]*", nxt):
            return ("agent", f"Naya {m.group(1)} {nxt}")
        return ("leader_malformed", f"Naya {m.group(1)} {nxt}")
    for seat in roster:
        if re.match(re.escape(seat) + r"(?![A-Za-z])", text):
            return ("roster", seat)
    m = re.match(r"Naya\s+[A-Z][a-zA-Z\-]*", text)
    if m:
        return ("bare", m.group(0))
    return None


_EXPLICIT_SIG_RE = re.compile(
    r"(?i)(?:WHO\b\s*(?:\*\*)?\s*[:\-–]|Signed\s+by\b|By\b\s*(?:[:\-–]|Naya\b))")
_SIG_PREFIX_RE = re.compile(
    r"(?i)(?:WHO|Signed(?:\s+by)?|By)\b\s*(?:\*\*)?\s*[:\-–]?\s*\**")


def _verdict_for(kind, name):
    """Map a candidate kind to check_identity's (ok, detail)."""
    if kind == "lead":
        return True, f"signed: lead {name}"
    if kind == "agent":
        return True, f"signed: leader agent {name}"
    if kind == "roster":
        return True, f"signed: {name}"
    if kind == "leader_malformed":
        if name in (f"Naya {lead}" for lead in
                    ("Clarity", "Verity", "Resolve")):
            return False, (f"incomplete identity '{name}' — leads sign "
                           f"with the family name: '{name} Narzan'")
        return False, (f"malformed agent identity '{name}' — agent names "
                       "are capitalized: "
                       "'Naya <Clarity|Verity|Resolve> <Name>'")
    return False, (f"incomplete identity '{name}' — "
                   "Shawn's naming law needs the leader prefix: "
                   "'Naya <Clarity|Verity|Resolve> <Name>'")


def check_identity(body, roster=ROSTER):
    """Roster seats and leader-prefixed agents only. Returns (ok, detail).

    The signer is resolved from an explicit signature line ONLY: a
    `WHO:`-labeled line, a `Signed:`/`By:` line, or a line that STARTS
    with the name (after markers). A name merely *mentioned* in the body
    never signs the post — a post signed 'Naya Alpha' that thanks
    'Naya Verity Narzan' is signed by Naya Alpha.

    Two-pass scan: explicit signature lines (`WHO:`/`Signed by`/`By:`)
    take precedence over bare name-leading lines in ANY order — a
    mention line above the WHO line must not steal the signature.
    When an explicit signature line exists, it IS the signature claim:
    bare lines never override it, and an explicit line with no
    resolvable name leaves identity unbound."""
    lines = [_strip_markers(line) for line in body.splitlines()]
    explicit_seen = False
    for text in lines:
        if not _EXPLICIT_SIG_RE.match(text):
            continue
        explicit_seen = True
        m = _SIG_PREFIX_RE.match(text)
        cand = _candidate_from_text(text[m.end():], roster) if m else None
        if cand is not None:
            return _verdict_for(*cand)
    if explicit_seen:
        return False, ("explicit signature line present but no roster "
                       "seat name found — identity unbound")
    for text in lines:
        cand = _candidate_from_text(text, roster)
        if cand is None:
            continue
        return _verdict_for(*cand)
    return False, "no roster seat name found — identity unbound"


def check_evidence(body):
    """An anchored SHA, a PR/issue ref, or a run id — or it didn't happen.

    A bare hex word is NOT evidence: 'deadbeef' in prose proves nothing.
    A SHA counts only with an anchor — `@ <sha>`, `sha: <sha>`,
    `commit <sha>`, `tip <sha>`, `head <sha>`, `tree <sha>`,
    `ref <sha>` — or a `#NNNN` ref."""
    hits = SHA_RE.findall(body) + REF_RE.findall(body)
    if hits:
        return True, f"evidence anchors: {hits[:3]}"
    return False, "no anchored SHA, PR/issue ref, or run id found"


def check_score(body):
    """A score with meaning, not a bare number.

    Meaning words match on word boundaries: 'relationships' is not
    'ships', 'meaningless' is not 'meaning'."""
    m = SCORE_RE.search(body)
    if not m:
        return False, "no X/10 score found"
    if MEANING_RE.search(body):
        return True, f"score {m.group(0).strip()} with meaning"
    return False, f"score {m.group(0).strip()} present but meaning unstated"


def check_level(body, level):
    """Required fields for the post's level.

    PULSE/RECEIPT fields must head labeled lines (`FIELD: ...`) —
    unlabeled prose that mentions every field word fails. EVENT
    questions are stems matched as word prefixes."""
    if level == "PULSE":
        missing = [f for f in PULSE_FIELDS if not _labeled(body, f)]
    elif level == "RECEIPT":
        missing = [f for f in RECEIPT_FIELDS if not _labeled(body, f)]
    elif level == "EVENT":
        missing = [q for q in EVENT_QUESTIONS if not _stem_present(body, q)]
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
