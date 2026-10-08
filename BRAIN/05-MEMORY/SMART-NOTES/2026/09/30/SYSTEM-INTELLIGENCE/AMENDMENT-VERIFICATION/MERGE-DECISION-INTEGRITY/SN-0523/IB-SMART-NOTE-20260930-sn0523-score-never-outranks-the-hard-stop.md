# Score Never Outranks the Hard Stop

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0523-score-never-outranks-the-hard-stop
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6030360603 ([NAYA][P0 GATE 2 SIGN-OUT] — PR #1685, exact head `00f3be968fde42fb20348be5033a622055dc9267`, 2026-10-07T03:35:36Z) — SoulSchoolAcademy.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Gate 2's sign-out was as green as it gets: 9.8/10, focused verifier 31/31, Node gate 12/12, and all four GitHub CI workflows SUCCESS on the exact head. And the auto-merge verdict was **DENY / HUMAN-ONLY** — because the branch touched `.github/workflows/`, which FULL-AUTO-MERGE-V1 §4 classifies as a protected path that may never be auto-merged. The score was honest (the missing 0.2: not merged, not deployed, not production-proven), and the verdict was computed *independently of the score*. The seat also refused to reinterpret Shawn's conditional instruction as authority to bypass the protected-path rule. The standing lesson for the cold successor: **scores measure readiness; they never grant authority.** A hard stop holds at 9.8 exactly as at 4.2 — and the moment a high score tempts you to relax a boundary is the moment the boundary matters most.

## 🩷 HUMAN NOTE

Shawn, here's one I'm proud of the seat for. Gate 2 came back at 9.8 out of 10 — everything green, every test passing — and she still refused to auto-merge, because the branch touches the workflows directory, which your merge law marks as protected. She also didn't let a conditional instruction from you become an excuse to bypass it. The point: a great score is a measurement, not a permission slip. The boundaries hold no matter how good the number looks.

## 👶 CHILD NOTE

Imagine you get 98 out of 100 on a test — amazing! But there's a rule: "no one goes into the kitchen without asking Mom." Your 98 doesn't change the rule. You still ask Mom. Scores tell you how well you did; rules tell you what's allowed. Those are two different things, and a big score never beats a rule.

## 👵 GRANDMA NOTE

Dear, there's a difference between being ready and being permitted. The machine proved itself thoroughly — 98% excellent — but the rule said that particular kind of change always needs a human's explicit word. And she honored the rule anyway, even though it was tempting to let the excellent score do the talking. That discipline is what makes a system trustworthy: the limits hold even when everything is going well.

## 🧠 NAYA NOTE

Cold successor: compute the score and the authority verdict as **two separate outputs** — never let the score number flow into the merge/authority decision. Before any score-gated automation runs, enumerate the hard stops (protected paths, authority boundaries, Director gates) and check them first; if any fires, the score is informational only. A conditional instruction from Shawn ("merge if green") is not a bypass of a standing protected-path rule — treat it as satisfying the green condition, not as overriding the boundary. When the score is highest, re-check the boundaries with extra care: that is when the temptation to skip them is strongest.

## 🤖 MACHINE NOTE

```json
{
  "sn": "SN-0523",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-06",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/AMENDMENT-VERIFICATION/MERGE-DECISION-INTEGRITY",
  "doctrine": "A score measures readiness; it never grants authority. A protected-path hard stop holds at 9.8 exactly as at 4.2.",
  "evidence": [
    "#1354 comment 6030360603 (Gate 2 sign-out: 9.8/10, all CI green, AUTO-MERGE = DENY / HUMAN-ONLY on .github/workflows/ protected path, FULL-AUTO-MERGE-V1 §4)",
    "#1354 comment 6030360603 (seat refused to reinterpret Shawn's conditional instruction as authority to bypass the protected-path rule)"
  ],
  "falsifiers": [
    "A 9+ scorecard receipt triggering an auto-merge on a protected path",
    "A conditional director instruction treated as authority to bypass a standing rule",
    "Score and merge-verdict computed as one number instead of two independent verdicts"
  ],
  "applies_to": "merge decisions, promotion gates, any score-gated automation"
}
```
