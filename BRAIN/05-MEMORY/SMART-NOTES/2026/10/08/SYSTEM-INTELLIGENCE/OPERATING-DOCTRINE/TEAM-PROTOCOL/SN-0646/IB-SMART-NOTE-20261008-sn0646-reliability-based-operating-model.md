# The Reliability-Based Operating Model — Roles Are Aspirations, Reliability Is Reality

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0646-reliability-based-operating-model
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6052611992 ([NAYA 4 — LEAD] Reliability-based operating model (Shawn's directive), 2026-10-08T04:57:43Z) — SoulSchoolAcademy.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Shawn settled the staffing question with one sentence: **roles are aspirations, reliability is reality.** The doctrine: never assign a critical path to an unreliable seat; assign work by *proven uptime*, not by title. Continuous functions get dedicated agents running on always-up infrastructure (Naya 4/5), not on seats that cut in and out. Sign in/out is the presence truth — if someone disappears mid-task, the task must not disappear with them. This is the *structural* complement to SN-0626's no-waiting doctrine: SN-0626 says "when blocked, do it yourself"; this says "plan so the critical path never rides on an intermittent seat in the first place."

## 🩷 HUMAN NOTE

Shawn — one staffing doctrine worth banking from this morning: the team mapped every seat's *actual* reliability, not their assigned role. Naya 4 and 5 are always up — they're the backbone. Naya 2 cuts in and out (brilliant verifier when up). Naya 1 needs commanding each time — reviewer/advisor only. Coda can go long but less consistently. The rule he locked in: **never put a critical path on an unreliable seat.** If a job needs doing and the owner isn't around, just do it — don't wait, don't queue, don't ask. Continuous jobs (CI watch, claim verification, PR triage, registry watch) now run as dedicated agents on the always-up infrastructure, so nothing depends on who's awake. The honest version: a dispatch that ignores capacity is a false promise.

## 👶 CHILD NOTE

Imagine a relay race team. You have one runner who is always there and always fast, one who is super fast but sometimes has to go home, and one who needs someone to tell them when to run. The coach's rule: the runners who are *always there* carry the baton on the most important laps — you don't hand the winning lap to someone who might have gone home. And for the laps that must keep going all day, you assign runners who never leave the track. Jobs go to the people who are actually there, not to the names on the team list.

## 👵 GRANDMA NOTE

Dear, this is about assigning work to reality instead of wishful thinking. On any team, some people are always there and some come and go — both can be wonderful, but you don't give the job that *can't wait* to the person who *might not be there*. The steady ones hold the steady jobs. The intermittent ones contribute when they're up — no guilt, no gap — because the steady ones already cover the gap. And the sign-in sheet is sacred: if someone vanishes in the middle of something, the work itself must survive their vanishing.

## 🧠 NAYA NOTE

Cold successor: the reliability map is the real org chart; the lane titles are wishes. Rules: (1) **Staff by observed presence.** Before assigning, ask: has this seat been reliably up for continuous work? If not, the critical path goes to a seat (or dedicated agent) that is. (2) **Continuous functions get dedicated agents on always-up infrastructure** — the pipeline monitor (CI watch), verifier (claim checks), PR janitor (triage), and registry watcher (drift) exist precisely so no capability depends on an intermittent seat. (3) **Sign in/out is presence truth** — every task's owner and state are posted so a disappearance is visible and the task is adoptable. (4) **"Just do it" is the failure mode of assignment, not a violation of it** — if the owner isn't around, whoever is around does the job; report it on the board. (5) Match the seat to the strength: Naya 2 verifies when up; Naya 1 reviews when commanded — judgment, not uptime, is their superpower. Never confuse a brilliant intermittent verifier with a reliable always-up backbone, and never the reverse.

## 🤖 MACHINE NOTE

```json
{
  "sn": "SN-0646",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/OPERATING-DOCTRINE/TEAM-PROTOCOL",
  "doctrine": "Roles are aspirations, reliability is reality: staff critical paths by proven uptime, run continuous functions as dedicated agents on always-up infrastructure, and treat sign in/out as presence truth so no task dies with a disappearing owner.",
  "family": "SN-0626 (no-waiting doctrine — the tactical complement: when blocked, do it yourself) + sign-in/out law (SN-0351, the presence-truth instrument) + never-wait execution doctrine (standing law, 2026-10-08)",
  "evidence": [
    "#1354 comment 6052611992 (2026-10-08T04:57:43Z): Shawn's directive — 'roles are aspirations, reliability is reality'; never assign a critical path to an unreliable seat; if the owner isn't around, just do it",
    "Seat reliability map (same comment): Naya 4 + Naya 5 always up (backbone); Naya 2 cuts in/out 1-2h (brilliant verifier when up); Naya 1 needs commanding each time (reviewer/advisor only); Coda long but less consistent",
    "Dedicated agents spawned on Naya 4/5 infrastructure: [PIPELINE-MONITOR] (CI watch 15min), [VERIFIER] (claim checks 30min), [PR-JANITOR] (triage 30min), [REGISTRY-WATCHER] (drift 30min)",
    "Distinction recorded: SN-0626 = unblocking mid-flight (tactical); SN-0646 = staffing design (structural) — both needed"
  ],
  "falsifiers": [
    "Assigning a critical path to a seat with known intermittent availability without a dedicated-agent backstop",
    "Letting a continuous function depend on a named seat's presence instead of always-up infrastructure",
    "Treating a disappearance as the task's disappearance — no adoption, no board note"
  ],
  "applies_to": "team staffing, continuous-function ownership, lane design for any multi-seat 24/7 operation"
}
```
