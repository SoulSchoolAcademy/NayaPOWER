# A Falsifier Battery Must Prove Its Subject Exists — Preflight Hard-RED Before the Battery Runs

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1571-falsifier-battery-subject-existence-preflight
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-17
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** t0703-lane8 learning event, hidden_files/learning-events-2026-10-17-12.md (CANDIDATE 567, appended to CORE-PRINCIPLES.md 2026-10-17); RED-first battery 15/15, sha-pinned

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

t0703-lane8 built a RED-first falsifier battery for the claim-liveness tripwire (`phantom_claim_detector.py`) — and the battery's own pre-detector run exposed a trap: 2 of 12 checks "passed" on a battery whose subject didn't exist yet, because a **missing detector exits 2 — the same exit code as a caught failure**. The battery's pass criteria could not distinguish absence from failure; without a preflight it would have certified a nonexistent detector as passing. The repair: every falsifier battery opens with a **subject-existence preflight** — a hard RED on a missing subject, executed before the battery runs, so the RED is honest. The final battery went 15/15 only because the preflight made the RED real first.

Why this is brain-grade: a falsifier battery that can be tricked by nothing-at-all certifies nothing. The exit-2 coincidence is the generic mechanism — any guard whose miss signal collides with its failure signal has this hole, and the only fix that closes it lives in the battery's own runner, not in the detector being tested.

## 🩷 HUMAN NOTE

Shawn — a new gate-building rule, caught by a real build this morning. A seat built a test battery meant to prove a detector works by showing it catches red plants. But the battery had a hole: when the detector didn't exist at all, the "missing" signal (exit code 2) was identical to the "caught it" signal — so the battery cheerfully reported 2 of 12 passing on a subject that wasn't there. The fix is a preflight: before the battery runs, it checks the subject exists, and if it doesn't, it fails hard and loud instead of grading an empty room. Every future falsifier battery must open with this preflight, or its pass is uncertified.

## 🟣 CHILD NOTE

Imagine a teacher giving a fire drill and grading the fire alarm — but there's no fire alarm installed, and "no alarm" sounds exactly the same as "alarm worked." The teacher would give an A to an empty wall. The fix: before the drill starts, the teacher taps the wall and asks, "Is there actually an alarm here?" If there's no alarm, the drill is a failure — not a pass. You can't grade a test on a student who never walked in.

## 👵 GRANDMA NOTE

Like testing whether a smoke detector works by holding a candle under it — but you test the wrong ceiling, where no detector was ever mounted, and "no beep" counts as "beeped correctly." You'd leave the house believing it was protected. The honest procedure: first confirm the detector is actually on that ceiling. Only then strike the match. Absence and success must never sound the same.

## 🧠 NAYA NOTE

Cold successor: (1) Every falsifier battery you build or adopt opens with a subject-existence preflight — assert the subject exists (file present, import resolvable, hook registered) and hard-RED (exit 2, loud) when it doesn't, BEFORE any pass/fail grading. (2) The preflight must itself be RED-first tested: a pre-detector run against a deliberately missing subject must show hard-RED, not a passing battery — that run is the proof the preflight is wired. (3) Scope: this is mandatory for every battery whose miss/failure signals can coincide (exit codes, empty-result sets, timeouts). If your battery's failure signal is provably distinguishable from subject-absence, the preflight is redundant — name that proof, don't skip it by feeling. (4) The 15/15 battery that proved this: t0703-lane8, `phantom_claim_detector.py`, sha-pinned RED-first battery — read its runner as the template.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-1571",
  "title": "A Falsifier Battery Must Prove Its Subject Exists — Preflight Hard-RED Before the Battery Runs",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-17",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "CI-TRIAGE", "RED-CLASSIFICATION"],
  "cousins": ["SN-0233", "SN-0443"],
  "applies_when": ["gate", "falsifier-battery", "red-first"],
  "enforcement": "RED-first battery convention: the battery runner executes a subject-existence preflight before any grading; a missing subject produces a hard RED (exit 2, loud) rather than a passing battery; the preflight is asserted by the battery's own pre-detector run against a deliberately missing subject (t0703-lane8: 15/15, sha-pinned; the pre-detector run must show hard-RED before the battery runs)",
  "evidence": {
    "event": "t0703-lane8 learning event (CANDIDATE 567) in hidden_files/learning-events-2026-10-17-12.md; appended to CORE-PRINCIPLES.md as CANDIDATE 567 on 2026-10-17",
    "coincidence": "pre-detector run showed 2/12 'passing' on a nonexistent subject — a missing detector exits 2, identical to a caught failure; without the preflight the battery would have certified a nonexistent detector",
    "artifact": "phantom_claim_detector.py — read-only scanner built with the RED-first battery (15/15, sha-pinned)"
  },
  "doctrine": {
    "decision_change": "whenever a falsifier battery is designed, built, or adopted, the design must include a subject-existence preflight that runs before the battery; a battery reporting PASS without a preflight is uncertified and must not enter any lane's process",
    "falsifiability": "if a battery's failure signal is provably distinguishable from subject-absence (no exit-code / empty-result / timeout coincidence), the preflight is redundant — the rule is scoped to batteries whose miss signal collides with the failure signal",
    "mechanism": "exit-2 coincidence: the absent subject produces the same signal as the caught failure, so pass criteria cannot distinguish 'nothing to test' from 'test passed'; the hard-RED preflight breaks the coincidence by making absence a loud failure before grading begins"
  },
  "rule": "every falsifier battery opens with a subject-existence preflight that hard-REDs on a missing subject before any grading — the preflight is itself proven by a pre-detector run against a deliberately missing subject that shows hard-RED, never a passing battery"
}
```
