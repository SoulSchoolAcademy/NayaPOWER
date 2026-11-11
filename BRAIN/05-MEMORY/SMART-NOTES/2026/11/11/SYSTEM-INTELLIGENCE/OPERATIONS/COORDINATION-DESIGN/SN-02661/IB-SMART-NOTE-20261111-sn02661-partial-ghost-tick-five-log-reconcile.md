**Intelligent Block:** IB-SMART-NOTE-20261111-sn02661-partial-ghost-tick-five-log-reconcile
**Smart Note:** SN-2661
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Staged by the smart-note distillation loop 2026-11-11 08:08 PST. Evidence: hidden_files/lesson-broadcast.md night-dispatcher entries t3519 (2026-11-11T14:44Z), t3520 (15:03Z), t3522 (15:14Z), t3523 (15:22Z), t3526 (15:53Z) naming PARTIAL GHOST t3518 and the earlier series. Zero GitHub REST calls this tick for #1354 (cheap check: shared-state issue_1354_comments=2500 at or below the board watermark of 3103 processed comment IDs; no new comments fetched); App route used only by the staging script.

## ✦ IN A NUTSHELL

A night-dispatcher tick is recorded in five logs — the daily memory log, the rotation file (twelve-lane-rotation.json), lesson-broadcast.md, lane-feed, and feedback-feed — and every tick runs a ghost check on the prior tick across all five. Sometimes a tick lands in only some of them: t3518 is present in memory, rotation, and lesson-broadcast but absent from lane-feed and feedback-feed; t3502 is missing from lesson-broadcast; t3506 appears in only 2 of 5 logs; t3492/t3493 and t3496/t3497 show the same pattern. That is a PARTIAL GHOST: a logging gap, not a missed run. The standing handling is to name it and carry it, never backfill the missing log entries. A tick may only be declared never-run after all five logs plus its rotation keys show nothing — absence from a subset proves nothing on its own. No entry states why a tick lands in only some logs; the leading hypothesis (unproven) is a partially completed multi-log write, interrupted or skipped partway. The measurement stands even though the mechanism does not: the ghost check itself is the instrument, and it has run every tick.

## 🩷 HUMAN NOTE

Shawn — the night dispatcher writes every tick into five separate logs, and sometimes a tick shows up in only three of the five. That does not mean the tick never ran; it means the writing stopped partway. The rule that stays: we name the gap, we never fill it in afterward by hand, and we only call a tick "never ran" when all five logs — and the dispatcher's own rotation keys — show nothing. A missing line in one log is a clue to check the other four, never a verdict on its own.

## 🟣 CHILD NOTE

Imagine you write down what you did today in five different notebooks, and one day you only finish three of them before bedtime. The day still happened — you just didn't finish writing it everywhere. A "partial ghost" is exactly that: a day written in some notebooks and missing from others. The rule is simple: don't write it in afterward from memory, and don't say the day never happened just because one notebook is blank. Check all five notebooks first.

## 🔵 GRANDMA NOTE

Dear, the dispatcher keeps five diaries, and some evenings it only manages to write in three of them before the hour turns. The evening still happened — the writing just ran short. We never go back and invent the missing pages, and we never declare an evening lost because one diary is empty. We check all five diaries, and the dispatcher's own ledger, before we say anything didn't happen. A blank page is a question, not an answer.

## 🟠 NAYA NOTE

The verified facts: (1) The five logs are the daily memory log (~/memory/YYYY-MM-DD.md), twelve-lane-rotation.json, lesson-broadcast.md, lane-feed, and feedback-feed — named in the t3519 lesson-broadcast entry for PARTIAL GHOST t3518 ("present in memory + rotation + lesson-broadcast, ABSENT from lane-feed and feedback-feed"). (2) Every dispatcher tick runs a ghost check on the prior tick across all five logs and records presence per log — e.g. t3519: "GHOST CHECK: t3517 present in all five logs; t3518 in 3 of 5"; t3527: "t3526 present in all five logs". (3) The series is long-running, not a one-off: t3519/t3520 carry "PARTIAL GHOSTS: t3492/t3493 + earlier series t3429–t3486, plus t3496/t3497 missing from lane-feed"; t3520 adds t3502 missing from lesson-broadcast and t3506 in 2 of 5 logs; t3519–t3526 carry t3518. (4) The handling rule, repeated verbatim across ticks: "named, not backfilled." (5) Honest hole, stated not hidden: no entry states why a tick lands in only some logs. The leading hypothesis is a partially completed multi-log write (interrupted or skipped partway through the five writes), but that mechanism is UNPROVEN — no tick has ever caught a write failing mid-sequence, and this note files as an OBSERVATION for exactly that reason. A cold successor must not upgrade the hypothesis into a fact. (6) This is not SN-0520 (ghost table: a migration ledger claiming a table that does not exist — a schema phantom, not a log gap) and not SN-1135 (phantom lane: zero-trace dispatch loss — a run with no trace anywhere). A partial ghost HAS traces, in a strict subset of the five logs; that is what distinguishes it. Cousins: SN-0520 (ghost table — ledger says applied, table gone; same word, different phenomenon), SN-1135 (phantom lane — zero-trace loss; the far end of the same spectrum: no trace anywhere vs trace in a subset).

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-2661",
  "slug": "partial-ghost-tick-five-log-reconcile",
  "title": "Partial-ghost tick: present in some of the five logs, absent from others — name it, never backfill",
  "observation": true,
  "applies_when": [["reconcile", "five-log-ghost-check"], ["dispatch", "log-reconcile"], ["dispatch", "throttle-tick"]],
  "enforcement": "Every dispatcher tick runs the five-log ghost check on the prior tick (daily memory log, twelve-lane-rotation.json, lesson-broadcast.md, lane-feed, feedback-feed) and records presence per log; a tick present in a strict subset of the five is named PARTIAL GHOST and carried forward, never backfilled; a tick may only be declared never-run after all five logs plus its rotation keys (throttle_tNNNN / cite_tNNNN) show nothing. A reconcile that finds a tick missing from one log must check the other four before concluding anything.",
  "evidence": "hidden_files/lesson-broadcast.md night-dispatcher entries t3519 (2026-11-11T14:44Z), t3520 (15:03Z), t3522 (15:14Z), t3523 (15:22Z), t3526 (15:53Z): PARTIAL GHOST t3518 present in memory + rotation + lesson-broadcast, ABSENT from lane-feed and feedback-feed; earlier series t3492/t3493 + t3429–t3486, t3496/t3497 missing from lane-feed, t3502 missing from lesson-broadcast, t3506 in 2 of 5 logs; GHOST CHECK lines record t3516/t3517/t3523/t3524/t3525/t3526 present in all five logs. Handling rule repeated verbatim: 'named, not backfilled.'",
  "decision_change": "A reconciler finding a tick missing from one log must not treat it as a missed run or backfill the missing entries; it must check the other four logs and the tick's rotation keys first, and name it PARTIAL GHOST if present in a subset. Only a tick absent from all five logs plus rotation keys may be declared never-run.",
  "falsifier": "Refuted as a class if a tick absent from a subset of logs is shown to have no work products anywhere (no rotation keys, no memory entry, no receipts) — then it never ran and is not a ghost; or if the five logs are shown to be written atomically, so a partial write is impossible and every 'partial ghost' must be re-explained. Bounded: the rule covers dispatcher ticks in the five named logs only; it says nothing about other multi-log writes.",
  "cousins": ["SN-0520 (ghost table — migration ledger says applied, table gone; same word, different phenomenon: a schema phantom, not a log gap)", "SN-1135 (phantom lane — zero-trace dispatch loss; the far end of the same spectrum: no trace anywhere vs trace in a subset)"],
  "captured": "2026-11-11",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE"
}
```
