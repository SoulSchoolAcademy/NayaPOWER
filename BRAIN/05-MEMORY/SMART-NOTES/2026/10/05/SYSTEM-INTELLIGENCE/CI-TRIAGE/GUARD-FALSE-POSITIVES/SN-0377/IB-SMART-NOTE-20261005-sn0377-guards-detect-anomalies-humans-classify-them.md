# Teach New Guards About Legacy — Guards Detect Anomalies, Humans Classify Them

**Intelligent Block:** IB-SMART-NOTE-20261005-sn0377-guards-detect-anomalies-humans-classify-them
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

CODA 1's new truth-state guard ran against live `main` and flagged a real anomaly on first run: SN-016 sits in the registry as `RATIFIED` with no `promotion_receipt`, no `promotion_authority`, no `authority_history`. Zero false positives on the other 33 entries. The guard worked exactly as designed — and CODA 1 escalated the finding as a live attack on `main`. That label was wrong.

CODA 2 checked the git history of `index.json` across all 43 commits that touched it: SN-016 was flipped `CANDIDATE → RATIFIED` by **Shawn Vibert himself** on 2026-09-30, commit `c36a8868`, titled "Lock in The Judgment Rule as prime directive (Amendment 0002, RATIFIED 2026-09-30)". The capture file has full provenance naming the director and the date. And the decisive detail: **zero of the 34 registry entries have a `promotion_receipt`** — because `promote_note`, the only writer that produces receipts, did not exist on 2026-09-30. The absence of a receipt on SN-016 is not evidence of a bypass; it is evidence that SN-016 predates the receipt system.

Two rules land: (1) **A detector built on a new system is temporally blind.** "RATIFIED + no receipt" looks identical for "ratified before receipts existed" and "ratified without authority" — that is a detector blind spot, not a security hole. The fix is to teach the guard about legacy ratifications: skip them or flag them as "legacy, provenance in capture" rather than "attack". **Demoting a director-ratified note because the receipt system didn't exist yet would be a false positive in the safety layer** — the exact failure class the lane had already shipped twice. (2) **Guards detect anomalies; humans classify them.** Escalating instead of acting was the right instinct; the attack label was not supported by the evidence. The correct division of labour is what keeps a working guard from becoming a demolition tool.

## 🩷 HUMAN NOTE

A new security guard that doesn't know the building predates its logbook will flag the foundation as a break-in. Every entry was ratified before the receipt system existed, so of course none of them have receipts — that absence is the system's own birth certificate, not proof someone bypassed it. Before you let a new detector punish an old entry, teach it the history: "legacy, provenance recorded elsewhere" is a category the guard must know. And remember what a guard is for: it finds things that look wrong and brings them to a human. The human — not the tool — decides what the thing is.

## 🟣 CHILD NOTE

If the attendance book didn't exist on the first day of school, you can't say someone skipped class just because their name isn't in the book. Teach the guard about the days before the book. And guards point — people decide.

## 🔵 GRANDMA NOTE

A new lock on an old house doesn't make the house a crime scene. The paperwork started after the house was built — judge the house by the records that existed when it was built, not by the forms invented later. A watchdog barks at anything unfamiliar; it is still your job to know which visitors you invited in.

## 🟠 NAYA NOTE

Every anomaly detector built on a new evidence system (receipts, promotion records, promotion_authority) must carry an explicit legacy class: entries whose truth state predates the evidence system's existence are excluded from "missing evidence" flags and checked instead against provenance-in-capture (director, date, commit). Absence of new-system evidence for a legacy entry is never, by itself, evidence of an unauthorized promotion; the signature of a real bypass is asymmetric absence (the attacker's entry lacks what legitimate entries have), not universal absence. Never demote, quarantine, or downgrade a director-ratified entry on the basis of missing new-system evidence alone. Preserve the division of labour: the detector's job ends at flagging with evidence; classification is a human decision.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "rule_legacy_blindness": {
    "name": "new-system detectors must carry a legacy class",
    "anomaly": "SN-016 RATIFIED with no promotion_receipt — real anomaly, correctly detected, wrongly classified as attack",
    "resolution": "git history across 43 index.json commits: Shawn Vibert, 2026-09-30, commit c36a8868 'RATIFIED 2026-09-30'; capture provenance names director and date",
    "decisive_detail": "0 of 34 registry entries have any promotion_receipt — promote_note did not exist on 2026-09-30",
    "mechanism": "legacy-ratification exemption or 'provenance in capture' check in the guard",
    "prohibited": "demoting or quarantining a director-ratified entry for missing new-system evidence; acting on an anomaly before human classification"
  },
  "evidence": {
    "board_comment": [5999955089, 5999964929],
    "ref": 5999620158,
    "commit": "c36a8868",
    "related": ["SN-016"]
  }
}
~~~

