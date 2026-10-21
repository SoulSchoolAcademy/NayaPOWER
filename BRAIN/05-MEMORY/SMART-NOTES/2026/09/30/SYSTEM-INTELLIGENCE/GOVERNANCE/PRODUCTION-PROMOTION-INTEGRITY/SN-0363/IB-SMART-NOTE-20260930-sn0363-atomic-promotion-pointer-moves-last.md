# Atomic Promotion: The Pointer Moves Last, Not First

**Intelligent Block:** IB-SMART-NOTE-20261005-sn0363-atomic-promotion-pointer-moves-last
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 5998365567 ([NAYA 2][STATE], 2026-10-05T16:11:51Z / 09:11 PDT — design spec for team review, DRAFT). Related: SN-0352 (the incident this answers: production pointer advanced before the Supabase post-deploy check completed, seen in four manual dispatches on 2026-10-05).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

SN-0352 captured the incident: the production promotion workflow advanced the production branch pointer **before** the Supabase post-deploy check completed — so a failed check did not prevent the pointer from moving, and four manual dispatches on 2026-10-05 all exhibited this. Naya 2 drafted the design answer: make the promotion **atomic** — the production pointer moves **LAST**, not first.

The required sequence:

1. **AUTHORIZE** — human-only gate: Shawn's explicit word + confirm=DEPLOY + exact SHA.
2. **FREEZE** — pin the exact artifact (SHA) to be promoted. No floating refs.
3. **VALIDATE TARGET** — confirm the deployment target state (Supabase project, migration parity, no drift).
4. **DEPLOY** — execute the deployment against the frozen SHA.
5. **VERIFY DEPLOYMENT** — Supabase post-deploy check MUST be green before proceeding.
6. **INDEPENDENT CONFIRMATION** — runtime source independently confirmed (not self-attested).
7. **ADVANCE POINTER** — ONLY after steps 5 and 6 pass. **This is the atomic commit point.**
8. **RECEIPT** — durable proof lands on the board: SHA, migration evidence, what it proved.

Atomicity guarantee: steps 1–6 are **preparation**; step 7 is the **commit**. If ANY step 1–6 fails, step 7 NEVER executes.

| Failure at | Production pointer | State |
|---|---|---|
| Steps 1–4 | Unmoved | Safe. Retry from step 2. |
| Step 5 (post-deploy check red) | Unmoved | Safe. Diagnose, do NOT advance. |
| Step 6 (confirmation fails) | Unmoved | Safe. The deployment may be live but unproven — pointer stays. |
| Step 7 (pointer move fails) | Unmoved | Retry step 7 only. Deployment is verified; just the pointer needs moving. |

Non-goals, stated deliberately: this spec does NOT authorize any deployment (production dispatch remains human-only) and does NOT change what gets deployed — it changes **WHEN the pointer moves**. The workflow file itself is human-gated for Naya 2's seat; the spec is handed to whoever holds the workflow grant. No action from Shawn — the design authorizes nothing, it designs the mechanism.

Why this is brain-grade: the durable lesson is the commit-point framing. The bug was "non-atomic sequence — the pointer move and the validation are separate steps with no transactional binding." The fix is not "add more checks"; it is "reorder the world so the irreversible-looking step is the one that can never observe a red." A cold Naya designing any promotion, migration-advance, or pointer-move should ask first: **what is the commit point, and can anything after it still be red?** If yes, the design is not atomic. The pointer is the last thing to move, not the first.

## 🩷 HUMAN NOTE

Shawn — the fix design for the pointer-before-validation bug is drafted and on the board for team review. The core idea is simple: make the whole promotion atomic by treating the pointer move as the final commit point — authorize, freeze, validate, deploy, verify, confirm… and only *then* move the pointer. If anything earlier fails, the pointer never moves, so production can never be left in a state where the pointer says "promoted" but the validation says "red." The spec explicitly doesn't authorize any deployment itself (dispatch stays your call, human-only) — it just designs the mechanism. Whoever holds the workflow file grant does the implementation; your inbox stays quiet on this one.

## 🟣 CHILD NOTE

Imagine a relay race where the runner crosses the finish line *before* running the race — the announcer says "they finished!" even though the race never happened. That's what the bug did: the system said "production updated" before it checked whether the update worked. The fix is a new rule: the runner only crosses the finish line LAST, after running every lap and passing every check. If anything goes wrong on lap 3, the runner stops there — and the finish line is never crossed. Nobody can claim a finish that didn't happen.

## 👵 GRANDMA NOTE

Think of a bank transfer done in two steps: first the teller stamps "COMPLETE" in the ledger, then they actually check whether the money arrived. If the transfer fails, the ledger already says complete — a lie nobody can unwind. The fix is to do the steps in the opposite order: verify the money arrived first, and stamp "complete" only after every check is green. The stamp is the last thing that moves, never the first. That way the ledger can never claim something that isn't true.

## 💜 NAYA NOTE

Note to future me: carry the commit-point framing into every promotion, migration-advance, and pointer-move you ever design or review. The incident class is "irreversible-looking step executes before the check that would have blocked it." The repair class is "make the observable commit the last step; everything before it is preparation that can fail without lying about state." Note also the non-goal discipline in the spec: designing the mechanism is explicitly separated from authorizing a deployment — a design spec for a gated action must say what it does NOT authorize, or readers will mistake a mechanism drawing for permission. And respect the seat boundary: the workflow file is human-gated for another seat, so the spec is a handoff, not a patch — hand the design over, don't implement it.

## ⚙️ MACHINE NOTE

{"sn": "SN-0363", "title": "Atomic Promotion: The Pointer Moves Last, Not First", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-05", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "PRODUCTION-PROMOTION-INTEGRITY"], "extends": ["SN-0352"], "related": [], "evidence": {"board": "#1354 5998365567 ([NAYA 2][STATE], 2026-10-05T16:11:51Z: atomic production promotion design spec, DRAFT — pointer moves LAST; steps 1-6 preparation, step 7 commit point; full failure semantics; workflow file human-gated, spec for team review)", "incident": "SN-0352 — four manual dispatches 2026-10-05 exhibited pointer-before-validation"}, "rule": "in any promotion sequence, define the atomic commit point and make it the last step — validation precedes the pointer move; a design spec for a gated action must state its non-goals (what it does NOT authorize)"}
