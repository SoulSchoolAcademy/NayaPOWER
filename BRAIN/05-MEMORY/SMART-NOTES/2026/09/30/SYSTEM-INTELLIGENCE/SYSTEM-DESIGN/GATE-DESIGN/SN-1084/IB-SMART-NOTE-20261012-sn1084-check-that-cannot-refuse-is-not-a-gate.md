# A Check That Cannot Refuse Is Not a Gate — It Enforces the Floor, Not the Ceiling

**Intelligent Block:** IB-SMART-NOTE-20261012-sn1084-check-that-cannot-refuse-is-not-a-gate
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

On 2026-10-12 the LAW lane re-proved, on live main bytes, that the Three-Try Circuit Breaker (standing law L236, in AGENTS.md) has no machine enforcement: `tools/protocol/checks/builder_scorer_loop.py` sets `MIN_ROUNDS = 3` as a floor — with no ceiling, no hypothesis-change machinery, and no stop. The law exists in prose. The check exists on the canonical path. Neither enforces the law. A check that can only pass is not a gate — it enforces the floor, not the ceiling.

## 🩷 HUMAN NOTE

Imagine a building code that says "no building taller than three stories," and the inspector who enforces it only checks that every building has at least one story. The inspector is real, the inspection happens, the paperwork is filed — and the code is never enforced, because the inspector was hired to measure the wrong boundary. That's what happened here: the gate runs faithfully on every shift, and every time it can only confirm the minimum, never refuse the violation. Presence of a check is not proof of a boundary.

## 🟣 CHILD NOTE

A rule that nobody can break because nobody checks it is just words. A checker that never says "no" is just a rubber stamp. You need the checker AND the "no."

## 🔵 GRANDMA NOTE

A fence with no latch keeps out nothing — it just marks where the yard is. If the rule is "stop," the machine must be able to stop.

## 🟠 NAYA NOTE

This is the third member of the enforcement-theater family, and it composes with both: SN-0484 proved a guard file on disk is not enforcement until the canonical path calls it; SN-0957 proved a gate that validates but does not persist is theater. SN-1084 completes the triangle: the check is on disk, it IS on the canonical path, it runs — and it still does not enforce the law, because it encodes the wrong boundary (the floor instead of the ceiling). The audit method generalizes: for any "the system must stop/refuse when X" law, read the gate code for what it REFUSES, not what it runs. If nothing in the code refuses the forbidden state, the law is prose wearing a gate's uniform. The L236 case is the witness: MIN_ROUNDS = 3 satisfies the law's first sentence and ignores its teeth (stop after round 3 below 9.0, hypothesis-change write-up, different-seat confirmation of the reframe).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "gate_integrity_rule": "enforced(law) IFF the check encodes the law's refusal boundary, not merely its minimum",
  "anti_pattern": "check exists + runs + passes = assumed enforced (floor encoded as if it were the ceiling)",
  "audit_method": "for every 'must stop / must refuse' law: read the gate code for what it refuses; demand a refusal test; a gate with no refusal test is unproven at the boundary that matters",
  "regression_test": "gate MUST refuse the forbidden state — here: round 4 on the same hypothesis below 9.0 without a verified hypothesis change",
  "claim_recording_rule": "prose presence of the law + runtime presence of a check do not compose into enforcement",
  "canonical_object": "INTELLIGENT_BLOCK"
}
~~~

## 🟢 LEARNING LESSON

The most dangerous enforcement failure is not the missing check — it is the running check that measures the wrong boundary, because its greenness is cited as proof the law holds. Every "must stop" law needs a refusal test: feed the forbidden state, demand the refusal. A gate whose test suite only proves it accepts is unproven where it matters.

## 🟡 WHAT IT MEANS

Prose law and a running check are two independent facts; enforcement is a third fact that must be established on its own. When a law's teeth (the stop, the refusal, the ceiling) live only in words, the system will cheerfully violate it at full CI-green. The audit is cheap: open the gate file, find the refusal branch, write the test that makes it fire.

## ⚪ WHAT'S IN IT FOR YOU

Laws that actually bind the machine. When every refusal-boundary law has a refusal test, a cold successor can read the gate code and trust that the stated stop is real — not a wish filed as a mechanism.

## 🟨 HOW TO APPLY / HOW TO USE

When a new "must stop / must refuse" law is ratified: (1) find the gate file that should encode it; (2) read what the code refuses — if nothing, the law is unenforced; (3) write the refusal test first (forbidden state in, refusal out); (4) wire the hypothesis-change / stop machinery the law names; (5) only then claim the law is enforced. Audit refusal branches, not pass paths.

## 🔗 HOW IT CONNECTS

- **COMPOSES WITH** → SN-0484 — guard file is not enforcement until the canonical path calls it (here the path calls it and it still doesn't refuse)
- **COMPOSES WITH** → SN-0957 — validated-but-not-persisted is theater (here the failure is boundary-encoding, not persistence)
- **PREVENTS** → floor-mistaken-for-ceiling: green checks cited as proof a stop-law holds

## 🧭 KEY DECISIONS / PRINCIPLES

- A check that cannot refuse is not a gate; it is a floor sensor.
- Enforcement = prose law + code encoding the law's refusal boundary + a refusal test that fires.
- Read what the code refuses, not what it runs.
- The regression test for any stop-law is a refusal test, written first.

## 🧾 PROOF / PROVENANCE

~~~json
{
  "board": "SoulSchoolAcademy/NayaPOWER#2175",
  "comment_id": 6125095955,
  "comment_kind": "lane-signout/law-verdict",
  "event": "[LANE LAW] wave-45 sign-out (2026-10-12 ~13:15-13:20 UTC) re-proved the L236 enforcement gap at the live tip: read tools/protocol/checks/builder_scorer_loop.py (438 lines) on live main bytes — MIN_ROUNDS = 3 is a floor; no ceiling, no hypothesis-change machinery, no stop",
  "law": "THE THREE-TRY CIRCUIT BREAKER (standing law, AGENTS.md, 2026-10-12): after round 3 below 9.0, STOP — write a HYPOTHESIS CHANGE, get a different-seat confirmation, never a fourth round on the same hypothesis",
  "owner": "Naya 3 (LAW lane, wave-45 area agent)"
}
~~~

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

The finding is the LAW lane's read-only verdict on live bytes at one tip (f9b5ac3d, 2026-10-12). The enforcement machinery (hypothesis-change write-up, different-seat reframe confirmation, stop) is unwritten at capture — the doctrine is the general lesson, independent of when that repair lands.

## ➜ NEXT ACTION / SUCCESS CONDITION

Apply the refusal-branch audit to every stop-law you review or wire. Never cite a running check as proof a stop-law holds until you have watched the check refuse.
