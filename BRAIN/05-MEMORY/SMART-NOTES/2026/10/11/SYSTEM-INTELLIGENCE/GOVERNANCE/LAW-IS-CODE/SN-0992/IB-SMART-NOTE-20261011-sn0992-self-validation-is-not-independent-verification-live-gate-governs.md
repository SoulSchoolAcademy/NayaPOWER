# Self-Validation Is Not Independent Verification — When Law and Runtime Disagree, the Live Gate Governs

**Intelligent Block:** IB-SMART-NOTE-20261011-sn0992-self-validation-is-not-independent-verification-live-gate-governs
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #2175 comment 6110478046 (2026-10-11 15:15Z — "Merge bottleneck: exact law/runtime mismatch + root-cause repair required") and #2175 comment 6110411823 (2026-10-11 15:08Z — Naya source-audit handoff); corroborated by #2175 comment 6110554566 (12-Laws director's reference: "Triple self-review is a quality discipline and does not itself constitute the *independent verification* required for governed work products").

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The director's standing rule for the merge bottleneck is real and valuable: a missing outside validator must not cause indefinite waiting, so quality is primarily the builder's responsibility — three explicit cycles of honest assessment → gap discovery → upgrade → re-score, target 10/10, minimum 9/10, real evidence, no inflated scores. **But that is self-validation, not independent verification**, and the 2026-10-11 review proved the system has an exact law/runtime mismatch: `BRAIN/01-GOVERNANCE/OPERATING-LAW.md`/`.json` LAW-A03 requires validation by a different seat; `tools/protocol/checks/merge_authority.py` fails closed without an `independent_validator`; `tools/check_merge_consensus.py` requires a cross-seat `[NAYA M · REVIEW] APPROVED` receipt plus an exact-head scorecard, and does not accept a three-round self-validation receipt. A self-validation fallback is policy; the live gate is code — and a rule that isn't enforced by code isn't a rule (FOLLOW THE CODE OR DON'T CODE). The attempted gate edit was **blocked by platform safety checks**, so the fallback is NOT implemented — recording it as implemented would be the breach. **Until law and runtime are reconciled in code with acceptance tests, honor the actual live gate rather than bypassing it.** And the fallback must never be labeled "independent verification" — self-review 3x is useful draft quality control, not an independent verifier or human permission.

## 🩷 HUMAN NOTE

Shawn — the director's answer to the merge bottleneck is right as far as it goes: builders must validate their own work hard (three honest rounds, 9/10 minimum, real evidence) instead of waiting forever for an outside reviewer. But that doesn't replace independent verification — the live merge gate still requires a different seat's sign-off, and a policy document saying "self-review is enough for now" doesn't change what the code enforces. We tried to change the gate code to match the policy and the platform blocked the edit — so the fallback is *not* in effect, no matter what any document says. The rule: the live code wins until new code with passing tests lands. Never call self-review "independent verification."

## 🟣 CHILD NOTE

Imagine two rule books for a game. One says "any player can check their own answers." The other — the one the referee actually follows — says "someone else must check your answers." You can't play by the first book while the referee uses the second. And if you tried to hand the referee a new rule book but he refused to take it, you don't get to say "he accepted it." You play by the rules he's actually using until he really takes the new book.

## 👵 GRANDMA NOTE

A building had two rule lists: the suggestion box said residents could approve their own renovations, but the locked front door only opened for the building manager's key. Someone wrote a note saying "the suggestion box is now the rule" — but the door still needed the manager's key, and the locksmith refused to change the lock. The note on the box didn't open the door. The door that is really there is the rule that matters — until someone actually changes the lock.

## 💜 NAYA NOTE

Future Naya: whenever policy (a doc, a directive, a fallback procedure) conflicts with a live gate (the code that actually enforces), **the live gate governs** — always. The reconciliation path is: (1) write the fallback as code with a canonical receipt schema, exact-head binding, protected-action exclusions, and regression/negative-control proof; (2) land it; (3) only then does the policy take effect. A gate edit blocked by platform safety is not a partial implementation — it is a non-implementation, and recording it as implemented is the failure mode. And keep the labels honest forever: three honest self-validation rounds (target 10, floor 9) is builder quality discipline; *independent verification* means a distinct seat's receipt on the exact head. Never relabel one as the other — the label is what the gate checks.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-0992",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-11",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "LAW-IS-CODE"],
  "cousins": ["SN-0972", "SN-0781", "SN-0120", "SN-0932", "SN-0580", "SN-0994"],
  "rule": "When policy and a live gate disagree, the live gate governs until a reconciling code change with acceptance tests lands. A three-round self-validation receipt (target 10/10, minimum 9/10, real evidence) is builder quality discipline, never independent verification; a gate edit blocked by platform safety checks is not implemented — do not record or relabel it as such.",
  "anti_rule": "Treating a policy fallback as effective while the live gate still requires cross-seat receipts; labeling self-validation receipts 'independent verification'; recording a blocked gate edit as an implemented change.",
  "evidence": {
    "bottleneck_review": "#2175 comment 6110478046 (2026-10-11 15:15Z) — exact law/runtime mismatch: OPERATING-LAW.md/.json LAW-A03 requires different-seat validation; merge_authority.py fails closed without independent_validator; check_merge_consensus.py requires cross-seat [NAYA M · REVIEW] APPROVED + exact-head scorecard; attempted gate edit blocked by platform safety checks — fallback NOT implemented",
    "source_audit": "#2175 comment 6110411823 (2026-10-11 15:08Z) — self-review 3x is useful draft quality control, not an independent verifier or human permission; archived #1354 still hardcoded in cold_start_gate (law/boot discrepancy)",
    "director_reference": "#2175 comment 6110554566 (2026-10-11 15:23Z) — 'Triple self-review is a quality discipline and does not itself constitute the independent verification required for governed work products and specific merge/release gates'",
    "fallback_acceptance_tests": "exactly three ordered rounds, each with honest findings + named upgrade/no-change justification + distinct evidence; receipt bound to exact current head and author seat; final score >= 9.0; final exact-head suite green; zero critical defects; Value Calculus receipt; zero objections — stale head, missing round, fake/missing evidence, self-labelled independent reviewer, score < 9, red tests, protected actions all fail closed"
  },
  "authority": "observed field review — Naya 4 distillation, CANDIDATE (auto-capture, not ratified)"
}
```
