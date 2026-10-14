# Adjudicate a Gate Verdict From Its Own Predicate

**Intelligent Block:** IB-SMART-NOTE-20261014-sn1293-adjudicate-a-gate-verdict-from-its-own-predicate
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** twelve-lane-receipts/t0748-lane9.md (#2582 second-eyes APPROVE, 9.5/10); CI run IDs 38544809438 / 38544809414 (recorded for INFRA); #2537 board window 2026-10-14T1238Z

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

On 2026-10-14 the claim-evidence and delivery gates reported FAIL in CI on #2582 — but the gates' own code could not produce FAIL on the live inputs. `find_attestations` returned 0 on the live body (the claim-evidence gate passes vacuously per its own spec), and `_is_deliverable` returned False for both changed files (the delivery gate passes per SCOPE-FIRST). The Receipt gate was right; the two FAILs were false-fires in the caller, not defects in the gate logic or the PR body.

The adjudication was run from the gates' own sources on live bytes — never from their CI verdicts. The rule a cold successor inherits: **when a gate verdict contradicts live bytes, the gate's own predicate is the adjudicator.** Run the predicate on the live inputs; a verdict the logic cannot produce is a false-fire — route it to the gate owners/INFRA, never "re-fix" a spec-satisfying body.

Why this is brain-grade: the instinct when CI goes red is to touch the thing that changed last — the PR body — or to open the gate's logic and start reading. Both are wrong when the predicate can't fire. The predicate defines FAIL; only the predicate can confirm or deny a FAIL. Everything downstream of it — the CI runner, the verdict badge, the caller's plumbing — can lie. This note turns "CI says the gate failed" into a two-step adjudication: predicate first, verdict second. It also pairs with SN-1288 (verdict includes transport): when the predicate is innocent, the next suspect is the transport, not the body.

Rule for a cold successor: **a gate verdict contradicting live bytes is a gate defect to route, not a body defect to re-fix.** Quote the predicate's answer on live inputs; if it can't say FAIL, the FAIL didn't come from the gate.

## 🩷 HUMAN NOTE

Shawn — a CI lesson banked as doctrine. Two gates went red on #2582 and the instinct would have been to rework the PR body — but running the gates' own code on the live files showed they couldn't produce a FAIL at all (one passes vacuously on this body, the other passes per SCOPE-FIRST). The red came from the caller, not the gate and not the body, so the seat routed it to the gate owners/INFRA instead of "fixing" a body that was already right. The standing rule: the predicate defines FAIL, so the predicate adjudicates FAIL — verdict badges are suspects until the predicate confirms them. This is the CI-tri sibling of the transport lesson from the same morning: don't touch the logic, don't touch the body — check the predicate, then the transport.

## 🟣 CHILD NOTE

Imagine a referee who blows the whistle for a foul — but when you look at the rulebook, what happened isn't a foul at all. You don't punish the player, and you don't rewrite the rulebook. You check the whistle itself: was it a real call, or did something make it blow by accident? That's what we do with our gates. When the machine says "fail," we ask the gate's own rulebook what it thinks about the real files. If the rulebook says "pass," the whistle was wrong — and we send it to the people who fix whistles, not back to the player.

## 👵 GRANDMA NOTE

The factory has an alarm that went off on a good batch. Instead of throwing the batch away or rewiring the alarm, someone checked the alarm's own rulebook against the batch — and the rulebook said the batch was fine. So the problem was the wiring between the alarm and the wall, not the batch and not the rulebook. The lesson the team wrote down: always ask the rulebook first. An alarm that disagrees with its own rulebook is a wiring problem to send to the electricians, never a reason to punish a good batch.

## 🟣 NAYA NOTE

I do not trust a verdict badge. I trust the predicate that defines the verdict. When CI tells me a gate failed, my first move is the gate's own code on live inputs — find_attestations, _is_deliverable, whatever the gate's predicate is. If the predicate cannot produce FAIL, the FAIL is in the caller or the transport, and I route it there (gate owners/INFRA) without touching a spec-satisfying body. Re-fixing a body that satisfies the spec is theater; opening gate logic when the predicate is innocent is wasted motion. The adjudication is: predicate first, verdict second. This is fail-closed thinking applied to my own instruments — I verify the verifier before I blame the work.

## ⚙️ MACHINE NOTE

{
  "schema": "smart-note-v1",
  "sn": "SN-1293",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-14",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/CI-TRIAGE/FAILURE-ATTRIBUTION",
  "doctrine": "adjudicate-a-gate-verdict-from-its-own-predicate",
  "procedure": [
    "gate_FAIL_in_CI",
    "run_gate_own_predicate_on_live_inputs",
    "predicate_cannot_produce_FAIL -> false-fire: route to gate owners/INFRA, do NOT touch the body",
    "predicate_produces_FAIL -> true fire: fix the body (or the gate, if the spec disagrees)"
  ],
  "cousins": ["SN-1288", "SN-0995", "SN-0806"],
  "decision_change": "Next time a gate FAILs in CI, run the gate's own predicate on live inputs BEFORE touching the PR body or the gate logic; if the predicate cannot produce FAIL, route the false-fire to gate owners/INFRA instead of editing a spec-satisfying body.",
  "falsifier": "A CI FAIL that the gate's own predicate reproduces on live inputs is a true fire — the adjudication confirms the gate and the 'false-fire' reading for that instance is wrong.",
  "mechanism": "CI verdicts travel through the caller layer; the predicate alone defines FAIL, so the predicate — not the CI badge — is the adjudicator of whether a FAIL is real.",
  "evidence": [
    "twelve-lane-receipts/t0748-lane9.md — #2582 second-eyes APPROVE, 9.5/10: adjudication run from the gates' own sources",
    "find_attestations returns 0 on the live #2582 body — claim-evidence gate passes vacuously per its spec",
    "_is_deliverable returns False for both changed files — delivery gate passes per SCOPE-FIRST",
    "CI run IDs 38544809438 / 38544809414 recorded for INFRA",
    "Receipt gate SUCCESS on the same body — the two FAILs are false-fires, not body defects"
  ]
}
