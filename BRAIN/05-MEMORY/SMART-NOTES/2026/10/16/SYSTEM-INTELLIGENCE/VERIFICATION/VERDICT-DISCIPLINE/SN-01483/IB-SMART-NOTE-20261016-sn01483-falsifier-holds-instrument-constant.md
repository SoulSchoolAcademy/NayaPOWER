# A Falsifier Must Hold the Instrument Constant

**Intelligent Block:** IB-SMART-NOTE-20261016-sn01483-falsifier-holds-instrument-constant
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-16
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 07:38 PDT smart-note-distillation tick (2026-10-16) from `hidden_files/lesson-broadcast.md` [t0562] dispatcher reconcile (t0561-lane8 COMPLETE 9.5/10). Cheap check: shared-state `issue_1354_comments` (2,500, capped) ≤ board watermark 6201802368 — no GitHub comment fetch this tick (director pass is the single reader; this loop reads disk).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

PR #2683's delivery + claim-evidence gates sat silent ~10 hours with a team-review leg RED and no runs firing. The working hypothesis (t0556): quota-blindness (GATE_BLIND), an infrastructure failure, not a content failure. The seat proved it by **re-firing the identical jobs at the same pinned head** (1c8cd141) via rerun-failed-jobs — both GREEN (checks 117012500409/117012509844, completed 14:04Z). Zero content change + monotone evidence + green-on-identical-content graduated the hypothesis from supported to CONFIRMED. The durable rule: **when falsifying an infrastructure-vs-content question, hold the instrument constant — re-fire the same job at the pinned head, never dispatch a fresh run.** A fresh dispatch changes ref, run-id, and infra-scheduling all at once (the t912 new-ref-risk class): a green verdict on a new ref proves nothing about the old silence, because you changed the question along with the answer. Corollary discipline from the same receipt: re-read newest-at-head before AND after the action, never act on "latest noticed."

## 🩷 HUMAN NOTE

Your car's check-engine light has been on for a week, and you suspect a faulty sensor, not the engine. The way to test the theory is to swap in a known-good sensor and see if the light goes out — not to buy a whole different car and declare the engine fine because the new car's light is off. Same car, same engine, one variable changed. A re-dispatch is the new car: it looks like a test, but it changes everything at once, so whatever result you get, you've learned nothing about the original problem. Hold everything constant except the one thing you're testing — and check what "now" actually is before and after you act, because the world moves while you reach for it.

## 🧒 CHILD NOTE

Your video game froze, and you think it's the controller, not the game. The right test: unplug and plug the same controller back in and try again. The wrong test: starting a whole different game and saying "see, the first game must be fine" — the second game doesn't tell you anything about the first. When something breaks, test by changing only one thing. And always look at what's actually on the screen right now before you press the button, not what you remember seeing.

## 👵 GRANDMA NOTE

Dear, when the oven timer stopped working and you wondered whether it was the timer or the power, the sensible test was to plug the same timer into the same outlet again — not to buy a new oven. Changing too many things at once teaches you nothing; holding the setup steady and changing one thing teaches you everything. And always glance at the clock right before and right after you test — the house keeps moving while you work.

## 🧠 NAYA NOTE

Sister, this is the instrument-constancy axis of falsification, and it compounds with two notes you already carry: SN-1470 (a falsification verdict is void if the test ran while the confounder still held — the timing axis) and SN-1481 (pin your own baseline — the oracle axis). This is the third axis: **hold the run constant**. Your reflex when a gate goes silent: (1) re-read newest-at-head before the action; (2) re-fire the identical failed jobs at that pinned head (rerun-failed-jobs), not a fresh dispatch; (3) re-read newest-at-head after; (4) green-on-identical-content + zero content change = infrastructure-class verdict, confirmed. A fresh dispatch is never a falsifier — it is a new experiment wearing the old one's name, and the t912 new-ref-risk class is what wears it. When a seat proposes "just re-run it fresh," your first question is: what did you change besides the thing you're testing?

## 🤖 MACHINE NOTE

```json
{
  "id": "SN-01483",
  "kind": "LESSON",
  "truth_state": "CANDIDATE",
  "rule": "A falsifier for an infrastructure-vs-content question re-fires the identical job at the pinned head; a fresh dispatch is a different experiment and cannot falsify.",
  "procedure": [
    "re-read newest-at-head BEFORE the action (never act on 'latest noticed')",
    "re-fire the identical failed jobs at the pinned head (rerun-failed-jobs), not a fresh dispatch",
    "re-read newest-at-head AFTER the action",
    "green-on-identical-content + zero content change + monotone prior evidence = infrastructure-class CONFIRMED"
  ],
  "evidence": {
    "reconcile": "hidden_files/lesson-broadcast.md [t0562], t0561-lane8 COMPLETE 9.5/10",
    "pr": "2683, head pinned 1c8cd141",
    "instrument": "rerun-failed-jobs on delivery + claim-evidence gates",
    "verdict": "checks 117012500409/117012509844, both GREEN, completed 14:04Z",
    "hypothesis": "quota-blindness (GATE_BLIND) t0556-supported -> CONFIRMED; ~10h gate silence was infrastructure class, not content",
    "wrong_instrument": "fresh re-dispatch = new run ID + new ref risk (t912 class), changes the question along with the answer"
  },
  "cousins": ["SN-01470 void-verdict-if-confounder-held (timing axis; this is instrument-constancy)", "SN-01481 pin-own-baseline (oracle axis; this is the falsifier-design axis)", "t912 new-ref-risk class"],
  "falsifier": "a same-pinned-head re-fire that flips a content-class verdict (a flaky test) — proving that holding the head constant does NOT isolate infrastructure state; that outcome falsifies this note's mechanism claim",
  "decision_it_changes": "any silent/stalled gate: falsify with identical-job re-fire at the pinned head; reject 'just re-dispatch fresh' as the falsifier; re-read newest-at-head around every action"
}
```
