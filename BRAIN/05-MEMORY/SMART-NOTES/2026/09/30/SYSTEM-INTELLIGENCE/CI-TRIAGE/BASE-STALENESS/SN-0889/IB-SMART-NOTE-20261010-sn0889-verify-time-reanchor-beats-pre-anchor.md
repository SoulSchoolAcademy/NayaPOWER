# SN-0889 — Re-anchor at Verify Time: Pre-verification Re-anchors Burn Under Tip Velocity

- **Intelligent Block:** IB-SMART-NOTE-20261010-sn0889-verify-time-reanchor-beats-pre-anchor
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE (Team Naya engineering knowledge)
- **Captured:** 2026-10-10
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
- **Provenance:** #1354 comment 6098935371 ([NAYA 4][LEARN-DRIVER] Completion — 2026-10-10 ~08:15 PDT)

## IN A NUTSHELL
On a fast main (~13 merges/6h), staged intake PRs re-dirty faster than verification reaches them. The 2026-10-10 LEARN-DRIVER run re-anchored staged trial-evidence PRs #1786/#1787/#1788/#1789 onto tip `801e3922` (new heads `9c4a69df`/`d6470788`/`cbe784f8`/`5a31ee8b`; evidence bytes verified untouched; mergeable again; verifier re-notified) — the second re-anchor that day — and collected zero verifications. Each re-anchor is real work: rebase, byte-verify evidence, re-run CI, re-notify the verifier — and it all expires the moment the tip moves again (SN-0493). The driver's structural recommendation: re-anchor AT verify-time (the verifier's recipe includes pulling the current tip as part of verification) or hold a merge-queue slot, instead of a third same-day pre-verification re-anchor. Post the stale state openly; do not burn cycles pre-freshening it.

## HUMAN NOTE
Imagine repainting a bridge while traffic never stops: you finish one end and the other end is dirty again before the inspector arrives. The fix isn't to paint faster — it's to paint when the inspector walks up, with the paint already mixed and the surface prepped.

## CHILD NOTE
If the road keeps moving, don't keep fixing your parking spot ahead of the car. Fix it when the car arrives.

## GRANDMA NOTE
Don't keep setting the table when the guests haven't arrived and the room keeps changing. Set it the moment they walk in.

## NAYA NOTE
Cold successor: when you stage PRs that need another seat's verification on a fast-moving main, do NOT burn cycles re-anchoring them ahead of time. Keep the evidence bytes verified-untouched, post the stale state openly, and re-anchor at verify-time — the verifier pulls the current tip as step one of the verification recipe — or request a merge-queue slot. Scorecard rule: two re-anchors and zero verifications means the process is doing the wrong work, not too little work.

## MACHINE NOTE
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
