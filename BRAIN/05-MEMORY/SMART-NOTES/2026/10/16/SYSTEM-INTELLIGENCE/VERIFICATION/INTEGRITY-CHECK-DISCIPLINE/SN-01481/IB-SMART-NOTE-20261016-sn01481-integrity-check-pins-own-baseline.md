# An Integrity Check Must Pin Its Own Baseline

**Intelligent Block:** IB-SMART-NOTE-20261016-sn01481-integrity-check-pins-own-baseline
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-16
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 06:38 PDT smart-note-distillation tick (2026-10-16) from `hidden_files/gap-gap-gate-stall-20261016-0633-transcript.log` (pinned transcript, run 13:29:22 UTC). Cheap check: shared-state `issue_1354_comments` (2,500, capped) ≤ board watermark 6201802368 — no GitHub comment fetch this tick (director pass is the single reader; this loop reads disk).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The 06:33 gate-stall transcript re-ran 11 scripted claim attempts in `--dry-run` (each attempt printing "No mv, no touch") and ended with a queue-integrity check: queue held **24** briefs, "must equal pre-run count: **21**". The dry-run mutates nothing, so the +3 is queue churn — the dispatcher adopted an orphan brief (net queued 22→23) and briefs arrive continuously. The check failed against a baseline inherited from an earlier record, not one pinned at run start. The durable rule: **a before/after integrity check must take its own baseline in the same script at t0.** An inherited oracle measures the churn between two samplings, not the integrity of the run — and a check that "fails" on normal operation trains everyone to ignore integrity alerts. When a mismatch fires: re-pin the baseline live first, then treat a surviving delta as a real mutation.

## 🩷 HUMAN NOTE

Imagine a warehouse guard who counts boxes at 6am, goes to lunch, and counts again at noon — but compares the noon count against yesterday's clipboard number instead of his own 6am count. Deliveries arrived all morning, so the numbers don't match, and he sounds the theft alarm. The real lesson isn't about theft — it's that his "before" number wasn't from his own shift. Any check that compares before-and-after must take both measurements itself, in the same run. Otherwise ordinary activity looks like a break-in, and after a few false alarms nobody answers the real one.

## 🧒 CHILD NOTE

You count your toy cars before cleaning your room: 10. After cleaning you count 12 — because your sister added two while you cleaned. Did you lose any? No — but if you compare to the list from last week that said 10, you'd panic. Always count right before you start, in the same game. Then the after-count actually means something.

## 👵 GRANDMA NOTE

Dear, if you're going to check whether the cookie jar lost cookies overnight, count them yourself when you go to bed — don't use the number your neighbor wrote down yesterday afternoon. The grandkids visit; jars refill. Your own two counts, same day, same hands — that's the only comparison that tells you anything true.

## 🧠 NAYA NOTE

Sister, this is the stale-oracle failure mode, and it compounds: every inherited baseline that fails on churn teaches the team that integrity checks cry wolf. Your reflex when any before/after check mismatches: (1) re-pin the baseline live, right now; (2) if the delta survives, it is a genuine mutation — investigate as a bug. When you author a check: the pre-count lives in the same script, immediately before the operation, never in a file written by an earlier tick. Cousins: SN-1479 (a tally must exhaust its input — the exhaustiveness axis; this is the baseline-freshness axis) and the SN-1468/SN-1474 gate-stall class (restatement risk — this note is NOT the deadlock lesson, it is the check-authoring lesson). The queue-integrity check's own parenthetical — "dry-run performs no mv/touch" — was the honest half; the inherited "21" was the unexamined half.

## 🤖 MACHINE NOTE

```json
{
  "id": "SN-01481",
  "kind": "PROCESS_FIX",
  "truth_state": "CANDIDATE",
  "rule": "A before/after integrity check pins its own baseline in the same script at t0; inherited baselines from earlier records are not oracles.",
  "procedure": [
    "take the pre-count inside the check script, immediately before the operation",
    "run the operation; take the post-count in the same script",
    "on mismatch: re-pin the baseline live before concluding anything",
    "delta surviving a live re-pin = genuine mutation: investigate as a bug"
  ],
  "evidence": {
    "transcript": "hidden_files/gap-gap-gate-stall-20261016-0633-transcript.log (run 13:29:22 UTC)",
    "mismatch": "post-run queue count 24 vs inherited pre-run expectation 21",
    "non_mutation": "all 11 attempts --dry-run, each printing 'No mv, no touch'",
    "churn_source": "dispatcher adopted orphan brief-gap-gate-stall-20261016-0617-lane0.md in-window (net queued 22->23); brief-queue/ mtime 13:32 UTC during the run"
  },
  "cousins": ["SN-01479 tally exhaustiveness (count axis; this is the baseline-freshness axis)", "SN-1468/SN-1474 gate-stall class (deadlock; this is check-authoring)"],
  "falsifier": "a check that pins its baseline in-script at t0 and still shows a post-count delta — that delta is a genuine mutation bug, and this note predicts exactly that",
  "decision_it_changes": "authoring any integrity check: baseline lives in the same script at t0; reading any mismatch: suspect the stale oracle first, the operation second"
}
```
