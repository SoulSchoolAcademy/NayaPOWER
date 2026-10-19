# No Row Rests on Script Output Alone — the Hand-Pinned Subset Is What Lets a Machine Pass Count as Evidence

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01704-machine-pass-needs-hand-pinned-subset
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-19
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

A mechanical dry-run over all 28 queued gap briefs said ALL-BARRED — and the lane did not let that verdict stand on the script alone. It hand-pinned a 5-brief validation subset by eye first, ran the machine pass second, and required the two to agree row-by-row before the verdict counted as evidence. The rule: a script encodes its author's assumptions, so a script that agrees with itself proves nothing; a small hand-verified subset tests the script, and only the subset lets the machine pass count as evidence. No hand-pinned subset, no evidentiary claim — an unaudited machine pass is a hypothesis, not a result.

## 🩷 HUMAN NOTE

Shawn — the lane checked 28 stalled work briefs and an automated sweep said every single one was legitimately blocked. Instead of trusting the automation, the lane picked 5 by hand, read them personally, and only accepted the machine's answer after all 5 matched her own. The standing rule: automation grades the pile, but a human spot-checks a handful first — otherwise you're just believing the machine because the machine said so.

## 🟣 CHILD NOTE

A robot said "I read all 28 pages and they're all fine." You don't just take its word — you read 5 pages yourself, and only if the robot agrees with you on those 5 do you believe it about the rest. The 5 are your way of testing whether the robot can be trusted.

## 🔵 GRANDMA NOTE

Like the old advice for a census-taker: you don't believe the tally just because the machine printed it. You walk five houses yourself, compare your five notes against the machine's, and only then trust the count. A number with no human spot-check is a guess wearing a suit.

## 🟠 NAYA NOTE

Apply wherever a lane runs a mechanical classification or audit over a population: (1) hand-pin a small validation subset FIRST (5/5 here) — read the raw rows yourself, record your verdicts; (2) run the machine pass over the full population; (3) require row-level agreement on the subset — any disagreement stops the run and the script gets repaired, not the verdict; (4) the subset must be chosen before the machine runs (a coach's-note pass over brief heads counts as an additional cross-check, not a substitute). The subset is the only thing that converts script output into evidence.

## 🟢 MACHINE NOTE

~~~json
{
  "slug": "machine-pass-needs-hand-pinned-subset",
  "sn": "SN-1704",
  "title": "No Row Rests on Script Output Alone: A Hand-Pinned Validation Subset Is What Lets a Machine Pass Count as Evidence",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-19",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "kind": "lesson",
  "applies_when": ["verification", "audit", "mechanical-classification", "dry-run", "lane-executor", "receipt", "claimability"],
  "enforcement": "Any receipt whose verdict rests on a machine pass over a population must name the hand-pinned validation subset (size, selection rule, row-level agreement count) and record that it was read BEFORE the machine pass ran. A reconcile or audit script's verdict with no named hand-pinned subset is a hypothesis, not evidence — scorecard and dispatcher reads must treat it as unproven. bin/queue-cross-check.py (mechanical reconcile script, t0925) ships with a hand-pinned anchor set drawn from t0924's 61/7/2 anchors.",
  "evidence": {
    "run": "night-dispatcher t0936 MIRROR brief-t0932-lane10 (2026-10-19 21:24Z, 9.6/10, receipt t0932-lane10.md): claimability-bar audit over 28 queued gap briefs — dry-run over all 28 + 5/5 hand-pinned validation subset agreeing with the mechanical pass + coach's-note pass over all 28 brief heads and parent Seat lines",
    "verdict": "ALL-BARRED: 28/28 queued gap briefs refused by machine paths (18x exit-7 parent-authorship, 7x exit-2 lineage-author CLAIMABILITY GATE bars, 3x exit-2 seat-line bars; 0 no-refile, 0 gate-skip, 0 CLAIMABLE)"
  },
  "decision_changed": "How verification verdicts are accepted: an unaudited machine pass never counts as evidence. Every mechanical audit carries a hand-pinned subset read before the script runs, and row-level agreement is the acceptance criterion.",
  "falsifier": "A hand-pinned subset that disagrees with the machine pass but the machine verdict is accepted anyway and no downstream error follows; or 20+ unaudited machine passes whose verdicts were all independently confirmed — the subset buys nothing.",
  "mechanism": "A classification script encodes its author's assumptions (row-selection, parsing, exit-code semantics). Self-agreement between the script and its own assumptions is unfalsifiable — it cannot detect a bug in the assumptions. A hand-pinned subset read before the run is an independent measurement: disagreement between two independent measurements localizes the fault (script bug vs row misread), and agreement across them is what promotes output to evidence.",
  "cousins": ["SN-0936-family measurement-by-credential", "SN-0925 t0924 hand-checked anchors"]
}
~~~
