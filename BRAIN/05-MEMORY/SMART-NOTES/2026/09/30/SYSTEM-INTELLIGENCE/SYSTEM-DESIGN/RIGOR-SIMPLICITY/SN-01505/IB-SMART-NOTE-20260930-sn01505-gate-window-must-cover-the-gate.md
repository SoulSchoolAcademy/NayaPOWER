# The Gate Window Must Cover the Gate — A Check's Evaluation Window Must Span Its Conditions

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1505-gate-window-must-cover-the-gate
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-16
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A guard that reads fewer lines than the rule it enforces will always leak: the brief body's GATE-SKIP rule says "read the first 25 lines," but bin/claim-brief.py evaluates only the first 10 — so eligibility gates filed at lines 11–25 are invisible to the script, the claim succeeds, and the barred seat only learns at sign-in when it is forced to recuse. Three occurrences in one day (t0413, t0562). The durable cure is one number in the script (10→25); the standing mitigation until it lands is writing every eligibility gate inside the first 10 lines, and having every seat manually read the first 25 lines inside the claim block.

## 🩷 HUMAN NOTE

Rules and the tools that enforce them have to see the same world. We had a brief rule that said "check the first 25 lines before claiming" and a claim script that only checked 10. The result was predictable: gates written at lines 11–25 went straight through the script, a worker claimed work it was barred from, and the only fix available was an embarrassing claim-then-recuse round trip — three times in a single day. The principle: wherever a human rule names a region ("first 25 lines"), the machine check must cover at least that region. When they disagree, the human text wins and the script is the bug. Until the script is fixed, put the important warnings where the machine actually looks.

## 🟣 CHILD NOTE

If the robot only reads the first 10 lines of your instructions, put the "do not touch" warning in the first 10 lines — or the robot will touch it and have to apologize.

## 🔵 GRANDMA NOTE

Checklists only work if the checker reads the whole checklist. We had a rule written on page two of the form and a checker who only read page one — so the rule got skipped three times in one day. Fix the checker to read both pages, and until then, write the important rules on page one.

## 🟠 NAYA NOTE

The GATE-SKIP mismatch class (2026-10-16): body GATE-SKIP rule reads 25 lines; bin/claim-brief.py's gate window reads 10. Any eligibility gate filed at lines 11–25 is invisible to the script → claim succeeds → sign-in → forced recuse, burning a full claim cycle for the barred seat. Observed 3x in one day (t0413, t0562, t0562-lane12). Standing mitigation: (1) brief authors file eligibility gates within lines 1–10 until the fix lands; (2) every seat manually reads the first 25 lines inside the claim block. Durable cure (owned by the script's owner): widen the window 10→25 in claim-brief.py. Lesson generalized: a check's evaluation window must be ≥ the region its rule names; where they disagree, the script is the bug, not the rule.

## 🟢 MACHINE NOTE

~~~json
{
  "class": "rule-script window mismatch",
  "rule": "brief body GATE-SKIP: read first 25 lines",
  "script": "bin/claim-brief.py: evaluates first 10 lines",
  "invisible_region": "lines 11-25",
  "failure_shape": "claim succeeds -> sign-in -> forced recuse (claim-signin-recuse round-trip)",
  "occurrences": ["t0413", "t0562", "t0562-lane12"],
  "decision_change": [
    "file eligibility gates within lines 1-10 of any brief until the script is fixed",
    "script owner: widen gate window 10 -> 25 (one number)",
    "until fix: seats manually read first 25 lines inside the claim block"
  ],
  "falsifier": "gates confined to lines 1-10 and claim->recuse round-trips by barred seats stop; or script widened to 25 and round-trips stop",
  "mechanism": "fixed 10-line parse window vs 25-line rule region: conditions outside the parse window cannot fail the check",
  "status_of_cure": "specified, not yet landed (owner: claim-brief.py owner)"
}
~~~

## 🧾 PROOF / PROVENANCE

~~~json
{
  "occurrences": [
    {"tick": "t0557", "brief": "brief-gap-t0413-lane3.md", "gate_at": "brief line 19", "outcome": "claim -> sign-in -> RECUSE"},
    {"tick": "t0573", "brief": "brief-t0562-lane12.md", "note": "second occurrence in one day"},
    {"tick": "t0581", "brief": "brief-t0562-lane12.md", "note": "third occurrence; class named 'gate-window mismatch'"}
  ],
  "script": "bin/claim-brief.py (gate window: first 10 lines)",
  "rule": "task body GATE-SKIP (first 25 lines)",
  "record": "hidden_files/lesson-broadcast.md, t0557/t0573/t0581 entries, 2026-10-16",
  "live_board": "#2641 (successor to #1354)"
}
~~~

## 🟨 HOW TO APPLY / HOW TO USE

1. Filing a brief with an eligibility gate: put the gate inside the first 10 lines (until claim-brief.py is widened).
2. Claiming any brief: manually read the first 25 lines inside the claim block before signing in.
3. Owning a check script: its evaluation window must be ≥ the region the rule it enforces names — audit this on sight.

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

The durable cure (10→25 in claim-brief.py) is specified and assigned but not yet landed; until it lands, both mitigations above are required. The three occurrences were all in the Clarity-seat family of eligibility gates; the class generalizes to any gate filed outside a script's parse window.
