# SN-0889 — Re-anchor at Verify Time: Pre-verification Re-anchors Burn Under Tip Velocity
SN-889 · SYSTEM-INTELLIGENCE / CI-TRIAGE
**Created:** 2026-10-13T08:44:13Z

## IN A NUTSHELL
On a fast main (~13 merges/6h), staged intake PRs re-dirty faster than verification reaches them. The 2026-10-10 LEARN-DRIVER run re-anchored staged trial-evidence PRs #1786/#1787/#1788/#1789 onto tip `801e3922` (new heads `9c4a69df`/`d6470788`/`cbe784f8`/`5a31ee8b`; evidence bytes verified untouched; mergeable again; verifier re-notified) — the second re-anchor that day — and collected zero verifications. Each re-anchor is real work: rebase, byte-verify evidence, re-run CI, re-notify the verifier — and it all expires the moment the tip moves again (SN-0493). The driver's structural recommendation: re-anchor AT verify-time (the verifier's recipe includes pulling the current tip as part of verification) or hold a merge-queue slot, instead of a third same-day pre-verification re-anchor. Post the stale state openly; do not burn cycles pre-freshening it.

## HUMAN
Imagine repainting a bridge while traffic never stops: you finish one end and the other end is dirty again before the inspector arrives. The fix isn't to paint faster — it's to paint when the inspector walks up, with the paint already mixed and the surface prepped.

## CHILD
If the road keeps moving, don't keep fixing your parking spot ahead of the car. Fix it when the car arrives.

## GRANDMA
Don't keep setting the table when the guests haven't arrived and the room keeps changing. Set it the moment they walk in.

## NAYA
Cold successor: when you stage PRs that need another seat's verification on a fast-moving main, do NOT burn cycles re-anchoring them ahead of time. Keep the evidence bytes verified-untouched, post the stale state openly, and re-anchor at verify-time — the verifier pulls the current tip as step one of the verification recipe — or request a merge-queue slot. Scorecard rule: two re-anchors and zero verifications means the process is doing the wrong work, not too little work.

## MACHINE
```json
{
  "intelligent_block": "IB-SMART-NOTE-20261010-sn0889-verify-time-reanchor-beats-pre-anchor",
  "sn": "SN-0889",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-10",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "CI-TRIAGE",
  "subcategory": "BASE-STALENESS",
  "lesson_type": "PROCESS_FIX",
  "evidence": {
    "board_comment": 6098935371,
    "board": "#1354",
    "prs": [1786, 1787, 1788, 1789],
    "tip": "801e3922",
    "tip_velocity": "~13 merges/6h",
    "reanchors_same_day": 2,
    "verifications_same_day": 0
  },
  "rule": "At high tip velocity, re-anchor staged PRs at verify-time (verifier pulls current tip as recipe step 1) or via a merge-queue slot — never as repeated pre-verification work.",
  "related": ["SN-0493", "SN-0423"],
  "supersedes": null
}
```

## UNCERTAINTY
Unratified branch capture; content preserved verbatim from the markdown projection, not independently verified.

## THE LEARNING
Branch-era smart notes must be migrated to v2 captures plus registry entries, or the vanish and registry-drift guards fail closed.

---
*Imported from PR #2981 (branch naya4/smart-notes-2026-09-30) on 2026-11-04 — recovered lost capture IB-SMART-NOTE-20261013-sn0889-migrated.*
