Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-23
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

Before writing stall-cap-check.py, t1421-lane4 (Naya Mason, 2026-10-23 07:41 PDT) scanned hidden_files/bin/ for an existing detector — found header-check.py (the four-line-header checker, already covering a nearby principle), saw the overlap, and pivoted to a principle with no existing check (the stall-receipt cap). Thirty seconds of `ls` before designing; the seat named it as the run's win and the root cause of the win: "the brief's 'prefer a ratified one' plus 30 seconds of ls before designing." The seat's own correction, now in the lane journal: duplicate instruments reading the same bytes through different parsing produce conflicting verdicts and split the ENFORCED count — one canonical instrument per rule. "Always scan bin/ for an existing detector before building" is now the first step of VIOLATION briefs. The lesson: the first action of any instrument-building brief is an existing-instrument scan; a second checker for a covered principle is motion, not progress.

## 🩷 HUMAN NOTE

Shawn — before building the new rule-break detector, the seat did something smart and cheap: it looked at the toolbox first. There was already a checker for the header rule, so instead of building a second one, it picked a rule with no checker at all — the stall cap. Thirty seconds of looking saved a duplicate. The lesson is now written into the lane journal: before you build any new instrument, check whether one already exists. Two checkers for the same rule will eventually disagree with each other, and then nobody knows which one is right. One rule, one checker — and looking first is always cheaper than building twice.

## 🟣 CHILD NOTE

Imagine you need a screwdriver, and you run straight to the store to buy one — but there was already a screwdriver in the toolbox at home. Now you have two screwdrivers, and one of them is a slightly different size, so sometimes they disagree about which screw fits. The smart move: open the toolbox FIRST, look inside, and only go to the store if the tool you need isn't there. That's what the seat did — thirty seconds of looking in the toolbox before building anything.

## 🔵 GRANDMA NOTE

Honey, it's the old rule: look before you leap. The seat was about to build a brand-new checker, but first it peeked into the toolbox — and found a checker already there for a nearby rule. So it built for a rule that had no checker instead. Now the team's journal says: always peek in the toolbox first. Two tools doing the same job will quarrel eventually, and a quarrel between checkers is worse than no checker at all.

## 🟠 NAYA NOTE

This is instrument-design hygiene at the cheapest possible price point. The t1421 seat's scan found header-check.py (four-line header, a nearby principle) and pivoted to the uncovered stall-receipt cap — avoiding a duplicate that would have read the same bytes through different parsing and produced conflicting verdicts, splitting the ENFORCED count the law self-audit tracks. The mechanism is divergence risk: two instruments for one rule rot separately, and their disagreement is indistinguishable from a real violation signal. The decision this changes is the first action of every VIOLATION brief: scan hidden_files/bin/ and name the overlap result before any design. The enforcement is the brief-filing check — a VIOLATION brief that builds without naming its existing-instrument scan result fails filing. Carry: this composes with SN-1877 (build the watcher) — first check whether the watcher exists, then build only what is missing.

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn-1878-scan-bin-before-building-detector",
  "lesson": "The first action of any instrument-building brief is an existing-instrument scan. Before writing stall-cap-check.py, t1421-lane4 (Naya Mason, 2026-10-23 07:41 PDT) scanned hidden_files/bin/ for an existing detector, found header-check.py (the four-line-header checker, a nearby principle), saw the overlap, and pivoted to a principle with no existing check (the stall-receipt cap). Thirty seconds of ls before designing; the seat named it as the run's win and the root cause of the win. Duplicate instruments reading the same bytes through different parsing produce conflicting verdicts and split the ENFORCED count — one canonical instrument per rule. 'Always scan bin/ for an existing detector before building' is now the first step of VIOLATION briefs in the lane journal. A second checker for a covered principle is motion, not progress.",
  "applies_when": ["instrument", "design", "instrument-design", "violation", "brief", "governance", "rule-enforcement", "tooling", "duplication"],
  "enforcement": "VIOLATION briefs carry an explicit first step: scan hidden_files/bin/ for an existing detector and name the overlap-check result in the brief; a brief that builds without naming the scan result fails the brief-filing check. The lane journal holds the step; the t1421 receipt (line 43, 56) is the worked example.",
  "evidence": ["hidden_files/learning-events-2026-10-23-15.md ([INTELLIGENT] event: seat corrected its own design process, 2026-10-23 15:00 PDT hour)", "hidden_files/twelve-lane-receipts/t1421-lane4.md (lines 7, 43, 56: bin/ scan, header-check.py overlap found, pivot to uncovered principle; lane-journal step)", "hidden_files/bin/header-check.py (the existing instrument found)", "hidden_files/bin/stall-cap-check.py (the instrument built instead)"]
}
```
