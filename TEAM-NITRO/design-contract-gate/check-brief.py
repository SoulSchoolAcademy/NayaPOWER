#!/usr/bin/env python3
"""check-brief.py — THE BRIEF CHECKER (the lock-in machine).

Usage: python3 check-brief.py <brief.md> [more briefs...]

A brief that fails this checker does not go out, ever. Run it before
dispatching any seat: a FAIL means the brief is incomplete and the
captain fixes it — the checker never auto-fixes a brief, it reports.

What it checks (each is a named section in the output):
  1. DONE FIRST — done defined BEFORE the work: exact element, exact
     change, exact measurement, and what must NOT be there.
  2. HARVEST SOURCES — every component names its harvest source; every
     named path must exist on disk.
  3. LAWS L1-L7 — tonight's laws, each named or referenced with its test.
  4. DESIGN-CONTRACT GATE — checks (a)-(i) named, plus human checks H1-H5.
  5. ANTI-REPEAT LIST — the six known failure modes, as prohibitions.
  6. FIVE GATES — the five gates, named or referenced via template §0.
  7. VERIFICATION PLAN — Playwright (or real browser) at desktop 1440 +
     phone 390 + true 360, zero overflow, zero console errors, named
     no-regressions.
  8. SHOULD THIS EXIST — the brief names the host page the work
     attaches to and what it does not duplicate; a standalone page
     fails outright (the minus-ten law, 2026-11-10).

Rules of the checker itself (the lock-in law):
  - Plain Python, stdlib only. No dependencies.
  - Checks are text-pattern based (section headings + key phrases),
    tolerant of wording — it fails on ABSENCE, not on phrasing. A brief
    that carries the substance in its own words passes.
  - Output is one line per check (CHECK <name>: PASS|FAIL — <evidence>)
    plus a final OVERALL: PASS|FAIL. Exit 0 on PASS, 1 on FAIL,
    2 on usage error (missing file / no args).

Sources: THE-SUPERCHARGER-BLUEPRINT-20261109.md §3A ("a brief checker.
A brief missing a required section FAILS before it is sent") and
DESIGN-BRIEF-TEMPLATE.md §2A (tonight's laws L1-L7). Style copied from
design-contract-gate/check-gate.py (plain functions, one line per
finding, exit codes).
"""

import os
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------- helpers

class Result:
    def __init__(self, number, name):
        self.number = number
        self.name = name
        self.passed = True
        self.evidence = []

    def fail(self, evidence):
        self.passed = False
        self.evidence.append(evidence)

    def ok(self, evidence):
        self.evidence.append(evidence)


def sections(text):
    """Split markdown into (heading, body) pairs by ATX headings.
    Text before the first heading is the preamble, heading ''."""
    parts = re.split(r"(?m)^(#{1,6}\s+.*)$", text)
    out = [("", parts[0])]
    for i in range(1, len(parts) - 1, 2):
        out.append((parts[i].strip(), parts[i + 1] if i + 1 < len(parts) else ""))
    return out


def body_lines(text):
    """All non-heading lines (headings would fake verb matches like
    'The fix' counting as a change verb)."""
    return [ln for ln in text.splitlines()
            if not re.match(r"\s*#{1,6}\s", ln)]


# ---------------------------------------------------------------- check 1

CHANGE_VERBS = re.compile(
    r"\b(remove|removes|removed|move|moves|moved|rebuild|rebuilds|"
    r"replace|replaces|delete|deletes|cut|cuts|apply|applies|double|"
    r"doubles|add|adds)\b"
    r"|gets its own"
    r"|break (it|them|this) into",
    re.I)

DONE_SIGNALS = {
    "exact element": [
        re.compile(r"exact element", re.I),
        re.compile(r"each of the", re.I),
        re.compile(r"every button", re.I),
        re.compile(r"each item", re.I),
        re.compile(r"inner block", re.I),
        re.compile(r"three parts", re.I),
        re.compile(r"the element", re.I),
        re.compile(r"`\.[a-z][\w-]*`"),
    ],
    "exact change": [
        re.compile(r"exact change", re.I),
        re.compile(r"exact behavior", re.I),
        CHANGE_VERBS,
    ],
    "exact measurement": [
        re.compile(r"exact measurement", re.I),
        re.compile(r"\bmeasure\b", re.I),
        re.compile(r"2×"),
        re.compile(r"\d+\s*px"),
        re.compile(r"zero overflow", re.I),
        re.compile(r"count\s*=", re.I),
    ],
    "what must NOT be there": [
        re.compile(r"must not be there", re.I),
        re.compile(r"no wall of text", re.I),
        re.compile(r"\bdo NOT\b"),
        re.compile(r"\bdo not\b", re.I),
        re.compile(r"\bnever\b", re.I),
        re.compile(r"scope boundary", re.I),
    ],
}


def _signals_in(scope, signals):
    """Return the list of signal names NOT found in scope text."""
    missing = []
    for name, patterns in signals.items():
        if not any(p.search(scope) for p in patterns):
            missing.append(name)
    return missing


def check_1_done_first(text):
    r = Result(1, "DONE FIRST")
    done_section = None
    for heading, body in sections(text):
        if re.search(r"done", heading, re.I) and re.search(
                r"first|defined|§6", heading, re.I):
            done_section = body
            break
    if done_section is not None:
        missing = _signals_in(done_section, DONE_SIGNALS)
        if missing:
            r.fail("done section present but missing: " + ", ".join(missing))
        else:
            r.ok("done section names element + change + measurement + "
                 "must-not-be-there")
        return r
    # No dedicated done section: the four signals must be carried across
    # the brief (work sections + rules + verify), change verbs read from
    # body lines only so a heading like 'The fix' cannot fake a change.
    scope = "\n".join(body_lines(text))
    missing = _signals_in(scope, DONE_SIGNALS)
    if missing:
        r.fail("no done section; distributed done-definition missing: "
               + ", ".join(missing))
    else:
        r.ok("no dedicated done section, but element + change + "
             "measurement + must-not-be-there are all carried across "
             "the brief")
    return r


# ---------------------------------------------------------------- check 2

PATH_RE = re.compile(r"(~/[^\s`\"'\)\],;]+|/home/hatch/[^\s`\"'\)\],;]+"
                     r"|workspace/[^\s`\"'\)\],;]+)")
CUTS_MOVES_ONLY = re.compile(
    r"deletions \+ moves only|no new copy|no new buttons", re.I)
ARTIFACT_SOURCE = re.compile(
    r"artifact\s+`[a-z][\w-]*`|the v\d+ artifact|artifact is at v\d+"
    r"|work on .{0,40}artifact", re.I)


def _named_paths(text):
    found = []
    for m in PATH_RE.finditer(text):
        p = m.group(1).rstrip(".,:;")
        found.append(p)
    return sorted(set(found))


def _resolve(path_str):
    if path_str.startswith("~"):
        return Path(os.path.expanduser(path_str))
    if path_str.startswith("/"):
        return Path(path_str)
    return Path.home() / path_str  # workspace/... from home


def check_2_harvest(text):
    r = Result(2, "HARVEST SOURCES")
    missing_paths = [p for p in _named_paths(text)
                     if not _resolve(p).is_file()]
    if missing_paths:
        r.fail("named harvest path does not exist: "
               + ", ".join(missing_paths))
    if CUTS_MOVES_ONLY.search(text):
        # A cuts/moves-only brief builds nothing new: the page itself is
        # the source. It must name the artifact and at least one real
        # file (its activation reads count).
        if not ARTIFACT_SOURCE.search(text):
            r.fail("cuts/moves-only brief names no artifact source "
                   "(the page itself is the harvest source — name it)")
        elif not _named_paths(text):
            r.fail("cuts/moves-only brief names no file path at all")
        elif not missing_paths:
            r.ok("cuts/moves-only: artifact named, %d file path(s) exist"
                 % len(_named_paths(text)))
        return r
    # A build brief must carry a harvest section with real source lines.
    harvest_body = None
    for heading, body in sections(text):
        if re.search(r"harvest", heading, re.I):
            harvest_body = body
            break
    if harvest_body is None:
        r.fail("no harvest section (build brief — every component must "
               "name its harvest source)")
        return r
    source_lines = [ln for ln in harvest_body.splitlines()
                    if ln.strip() and re.search(
                        r"~/|/home/hatch|artifact|hub|piece index|"
                        r"harvested from|`\.[a-z]", ln, re.I)]
    if not source_lines:
        r.fail("harvest section present but names no source")
    elif not missing_paths:
        r.ok("harvest section names %d source(s); all named paths exist"
             % len(source_lines))
    return r


# ---------------------------------------------------------------- check 3

LAWS = [
    ("L1", "stranger test", [re.compile(r"stranger test", re.I)]),
    ("L2", "perfect-words law", [re.compile(r"perfect-words", re.I),
                                 re.compile(r"perfect words", re.I),
                                 re.compile(r"his words are input", re.I)]),
    ("L3", "title+subtitle+nutshell",
     [re.compile(r"title.{0,12}subtitle.{0,12}nutshell", re.I | re.S),
      re.compile(r"title\+subtitle\+nutshell", re.I)]),
    ("L4", "Naya speaks, faces alternate",
     [re.compile(r"faces alternate", re.I),
      re.compile(r"naya speaks", re.I)]),
    ("L5", "test in his head", [re.compile(r"test in his head", re.I)]),
    ("L6", "## note format", [re.compile(r"`##`", re.I),
                               re.compile(r"## sections", re.I)]),
    ("L7", "one ultimate ten", [re.compile(r"one ultimate ten", re.I)]),
]
LAW_RANGE = re.compile(r"L1\s*[–\-]\s*L7")
LAW_REF = re.compile(r"§2A|template", re.I)


def check_3_laws(text):
    r = Result(3, "LAWS L1–L7")
    referenced = bool(LAW_RANGE.search(text) and LAW_REF.search(text))
    missing = []
    for law_id, law_name, patterns in LAWS:
        if any(p.search(text) for p in patterns):
            r.ok("%s %s — named" % (law_id, law_name))
        elif referenced:
            r.ok("%s %s — referenced via L1–L7 + §2A/template"
                 % (law_id, law_name))
        else:
            missing.append("%s (%s)" % (law_id, law_name))
    if missing:
        r.fail("missing laws: " + "; ".join(missing))
    return r


# ---------------------------------------------------------------- check 4

GATE_LETTERS = [
    ("(a)", "zero white/light backgrounds",
     [re.compile(r"\(a\)"), re.compile(r"zero white", re.I)]),
    ("(b)", "every element raised/elevated",
     [re.compile(r"\(b\)"), re.compile(r"\braised\b", re.I),
      re.compile(r"\belevated\b", re.I)]),
    ("(c)", "gauges/numbers alive",
     [re.compile(r"\(c\)"), re.compile(r"gauges", re.I),
      re.compile(r"numbers alive", re.I)]),
    ("(d)", "no text-in-image",
     [re.compile(r"\(d\)"), re.compile(r"text-in-image", re.I)]),
    ("(e)", "no bare text blocks",
     [re.compile(r"\(e\)"), re.compile(r"bare text", re.I)]),
    ("(f)", "no look-alike",
     [re.compile(r"\(f\)"), re.compile(r"look-alike", re.I)]),
    ("(g)", "## format",
     [re.compile(r"\(g\)"), re.compile(r"##.{0,20}format", re.I | re.S)]),
    ("(h)", "no dictation-blunt phrases",
     [re.compile(r"\(h\)"), re.compile(r"dictation-blunt", re.I),
      re.compile(r"banned blunt", re.I)]),
    ("(i)", "title+subtitle+nutshell + faces alternate",
     [re.compile(r"\(i\)"), re.compile(r"faces alternate", re.I)]),
]
GATE_RANGE = re.compile(r"\(a\)\s*[–\-]\s*\(i\)")
GATE_MENTION = re.compile(r"design-contract gate|design contract gate|"
                          r"THE DESIGN CONTRACT", re.I)
HUMAN_CHECKS = re.compile(r"H1\s*[–\-]\s*H5|human checks", re.I)


def check_4_gate(text):
    r = Result(4, "DESIGN-CONTRACT GATE (a)–(i) + H1–H5")
    if not GATE_MENTION.search(text):
        r.fail("no design-contract gate section named")
        return r
    ranged = bool(GATE_RANGE.search(text))
    missing = []
    for letter, name, patterns in GATE_LETTERS:
        if ranged or any(p.search(text) for p in patterns):
            r.ok("%s %s — %s" % (letter, name,
                                 "referenced via (a)–(i)" if ranged
                                 else "named"))
        else:
            missing.append("%s (%s)" % (letter, name))
    if missing:
        r.fail("missing gate checks: " + "; ".join(missing))
    if HUMAN_CHECKS.search(text):
        r.ok("human checks H1–H5 named")
    else:
        r.fail("human checks H1–H5 not named (attested with evidence "
               "in the handoff)")
    return r


# ---------------------------------------------------------------- check 5

ANTI_REPEAT = [
    ("never paste dictation verbatim",
     [re.compile(r"never paste.{0,40}verbatim", re.I | re.S),
      re.compile(r"verbatim.{0,20}v49", re.I)]),
    ("never use the word 'blockchain'",
     [re.compile(r"never.{0,30}blockchain", re.I | re.S)]),
    ("never invent a component when the harvested one exists",
     [re.compile(r"never invent", re.I),
      re.compile(r"harvest,? don't invent", re.I),
      re.compile(r"harvest-first", re.I)]),
    ("never report done from scroll-0 checks alone",
     [re.compile(r"scroll[ -]?0.{0,30}(alone|AND scrolled)", re.I | re.S)]),
    ("never claim without a live measurement",
     [re.compile(r"never claim without", re.I),
      re.compile(r"live measurement", re.I),
      re.compile(r"live bytes.{0,60}never with claims", re.I | re.S)]),
    ("never present work without a live link",
     [re.compile(r"never present.{0,40}live link", re.I | re.S),
      re.compile(r"link,? don't preview", re.I),
      re.compile(r"no link = not done", re.I)]),
]


def check_5_anti_repeat(text):
    r = Result(5, "ANTI-REPEAT LIST")
    missing = []
    for name, patterns in ANTI_REPEAT:
        if any(p.search(text) for p in patterns):
            r.ok(name + " — present")
        else:
            missing.append(name)
    if missing:
        r.fail("missing anti-repeat items: " + "; ".join(missing))
    return r


# ---------------------------------------------------------------- check 6

FIVE_GATES = [
    ("Gate 1 — is it right?", [re.compile(r"is it right", re.I)]),
    ("Gate 2 — is it what they truly need?",
     [re.compile(r"truly need", re.I)]),
    ("Gate 3 — is it mine to do?", [re.compile(r"mine to do", re.I)]),
    ("Gate 4 — is now the time?", [re.compile(r"now the time", re.I)]),
    ("Gate 5 — can I prove it?", [re.compile(r"can i prove it", re.I)]),
]
GATES_REF = re.compile(r"five gates", re.I)
GATES_REF_CONTEXT = re.compile(r"§0|before every consequential action|"
                               r"template|wise one|manifesto", re.I)


def check_6_five_gates(text):
    r = Result(6, "FIVE GATES")
    referenced = bool(GATES_REF.search(text)
                      and GATES_REF_CONTEXT.search(text))
    missing = []
    for name, patterns in FIVE_GATES:
        if any(p.search(text) for p in patterns):
            r.ok(name + " — named")
        elif referenced:
            r.ok(name + " — referenced via 'five gates' + template §0")
        else:
            missing.append(name)
    if missing:
        r.fail("missing gates: " + "; ".join(missing))
    return r


# ---------------------------------------------------------------- check 7

VERIFY_ITEMS = [
    ("method: Playwright (or real browser)",
     [re.compile(r"playwright", re.I),
      re.compile(r"real browser", re.I)]),
    ("desktop 1440", [re.compile(r"1440")]),
    ("phone 390", [re.compile(r"390")]),
    ("true 360", [re.compile(r"360")]),
    ("zero overflow", [re.compile(r"zero overflow", re.I)]),
    ("zero console errors", [re.compile(r"zero console errors", re.I)]),
    ("named no-regressions", [re.compile(r"no[- ]regressions?", re.I)]),
]


def check_7_verification(text):
    r = Result(7, "VERIFICATION PLAN")
    missing = []
    for name, patterns in VERIFY_ITEMS:
        if any(p.search(text) for p in patterns):
            r.ok(name + " — present")
        else:
            missing.append(name)
    if missing:
        r.fail("missing verification items: " + "; ".join(missing))
    return r


# ---------------------------------------------------------------- check 8

HOST_SIGNALS = [
    re.compile(r"host page", re.I),
    re.compile(r"where it lives", re.I),
    re.compile(r"lives on", re.I),
    re.compile(r"attaches to", re.I),
    re.compile(r"entry point", re.I),
    re.compile(r"does not duplicate", re.I),
    re.compile(r"not a duplicate", re.I),
    re.compile(r"duplicates nothing", re.I),
    re.compile(r"no new page", re.I),
]
STANDALONE = re.compile(r"standalone page", re.I)
NOT_STANDALONE = re.compile(r"not a standalone|never a standalone",
                            re.I)


def check_8_should_exist(text):
    """Gate 1 made mechanical: a build that is not a page itself must
    name the host page it attaches to; a new page must name the page
    it does not duplicate. The Factory one-click flow passed checks
    1-7 and was a minus-ten because nobody asked this — a standalone
    page duplicating the Factory, wired to nothing, two blocks doing
    nothing. A brief that builds a standalone page fails here, full
    stop."""
    r = Result(8, "SHOULD THIS EXIST — HOST PAGE + NO DUPLICATE")
    if STANDALONE.search(text) and not NOT_STANDALONE.search(text):
        r.fail("brief builds a standalone page — name the host page "
               "it lives on instead (a flow not wired into its page "
               "is waste)")
        return r
    if not any(p.search(text) for p in HOST_SIGNALS):
        r.fail("no host page / where-it-lives statement — every build "
               "names the page it attaches to and what it does not "
               "duplicate")
    else:
        r.ok("host page + no-duplicate named")
    return r


# ---------------------------------------------------------------- main

CHECKS = [check_1_done_first, check_2_harvest, check_3_laws,
          check_4_gate, check_5_anti_repeat, check_6_five_gates,
          check_7_verification, check_8_should_exist]


def check_brief(path):
    text = Path(path).read_text(encoding="utf-8", errors="ignore")
    print("=" * 72)
    print("BRIEF CHECK: %s" % path)
    print("=" * 72)
    results = [fn(text) for fn in CHECKS]
    for res in results:
        verdict = "PASS" if res.passed else "FAIL"
        print("\nCHECK %d %s — %s" % (res.number, res.name, verdict))
        for ev in res.evidence:
            print("      - " + ev)
    overall = all(res.passed for res in results)
    print("\nOVERALL: %s — %s" % ("PASS" if overall else "FAIL", path))
    return overall


def main(argv):
    args = list(argv[1:])
    if not args:
        print("usage: check-brief.py <brief.md> [more briefs...]")
        return 2
    overall_fail = False
    for fname in args:
        if not Path(fname).is_file():
            print("ERROR: file not found: %s" % fname)
            overall_fail = True
            continue
        if not check_brief(fname):
            overall_fail = True
    return 1 if overall_fail else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
