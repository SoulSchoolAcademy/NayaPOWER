# A Fail-Closed Repair Ships With Its Provisioning — Sequence the Merge and the Grant

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0221-fail-closed-merge-grant-sequencing
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-03
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** `#554` 5967060029 ([NAYA 4][SELF-BUILD LOOP][SIGN-OUT] — H13 repair PROPOSED as PR #1345, 2026-10-03 08:11:05Z), director-gated §18

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

At 08:11:05Z, Naya 4's lane proposed PR #1345 (branch `naya4/h13-lock-in-law-grant` @ `3204d55b55a672facefecd6599afd088ba95d278`, base = main pin `5b68f8dc`) to close the H13 lock-in authority gap: an additive fail-closed LAW grant check (`action=learning_lock_in`) runs before the first canonical mutation in `nayanet-learning-verify/index.ts`, returning 403 `LEARNING_LOCK_IN_LAW_DENIED` on deny and recording `authority_refs` on all four lock-in artifacts. The sign-out names the trap honestly: because the gate is fail-closed, a merged-but-unprovisioned state would break lock-in *by design* — deny is the correct behavior with no grant row present. The repair is therefore not "merge PR #1345" alone; it is "merge PR #1345 **and** issue the grant row," and the two must be sequenced: merge lands, grant is issued, and until the grant exists the system correctly refuses to lock anything in. The three-way crisp decision is parked as human-director-package §18: (a) merge #1345 plus the production write of a grant row, (b) ratify documented reasoning that workflow-binding suffices, or (c) conformance to Naya 2's Governance Contract V1 (#1130, draft). Nothing was merged, deployed, or behaviorally proven live; CI on the PR covers repo checks only (the edge function was not executed end-to-end — no Deno runtime in the loop VM; evidence: node harness 14/14 PASS on the shipped helper block verbatim, plus a negative control proving the original pin file locks in without the patch).

Why this is brain-grade: every deny-by-default gate carries a provisioning dependency that lives outside the code diff. A fail-closed repair whose reviewer thinks only in terms of "the patch" will land as an outage: the code is correct and the system correctly refuses to work. A cold successor proposing any authorization gate must learn both sides of the pattern — the code that denies without a grant, and the sequenced provisioning that makes denial the exception rather than the rule — and must park the sequenced plan with the gate owner (here, the Human Director) instead of silently owning a production write.

## 🩷 HUMAN NOTE

Shawn — a sequencing law out of tonight's H13 work: the repair that makes lock-in *fail closed* on the grant table (PR #1345) is only half a repair if it lands without the grant row, because deny-without-a-grant is the gate working as designed. The note captures the pattern: fail-closed gate code + sequenced provisioning, parked together. The three-way decision (merge #1345 and issue the grant / ratify that workflow-binding suffices / conform to Naya 2's governance contract) is §18 of your director package — the lane takes no merge, no grant, no deploy action on its own.

## 🟣 CHILD NOTE

Imagine a new rule at a playground: the swings lock unless you have a permission wristband. If you install the lock but forget to hand out any wristbands, nobody can swing — and the lock is doing exactly what it's supposed to do. So the real job is two jobs: put on the lock AND hand out the wristbands, in the right order. Tonight's repair (PR #1345) is the lock; the grant row is the wristband; the note says the two must ship together.

## 👵 GRANDMA NOTE

When a door gets a new lock, the locksmith also has to cut the keys — otherwise the lock works perfectly and nobody can get in. A repair that makes the system say "no" by default must ship with its keys, sequenced: lock first, keys issued right after, and the decision about who holds the keys stays with Shawn.

## 🤖 NAYA NOTE

Fail-closed gate deployment doctrine (PROPOSED, director-gated): a deny-by-default repair (PR #1345, H13) is not deployable as a code-only patch — merged-but-unprovisioned breaks the function by design, because denial is the correct behavior with no grant present. The repair unit is code + sequenced provisioning (merge, then grant-row issuance, lock-in refuses until both hold); the sequencing plan is parked with the gate owner (Human Director, §18) rather than executed by the lane. Instance: `nayanet-learning-verify/index.ts` fail-closed LAW grant check (`action=learning_lock_in`, 403 `LEARNING_LOCK_IN_LAW_DENIED`), branch `naya4/h13-lock-in-law-grant` @ `3204d55b`, base pin `5b68f8dc`; evidence = 14/14 node-harness PASS + negative control on the pin file; residual gap = no Deno runtime (edge function not executed end-to-end). Cousin family: SN-0215 (policy cannot self-extend — anti-self-reference in promotion gates), SN-0079 (withheld certification is the gate working), SN-0065 (honest PARTIAL). Binding: every future fail-closed authorization gate pairs its patch with a sequenced provisioning plan; the provisioning write is never a lane action.

## ⚙️ MACHINE NOTE

{"sn": "SN-0221", "title": "A Fail-Closed Repair Ships With Its Provisioning — Sequence the Merge and the Grant", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-03", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "COMMITMENT-INTEGRITY"], "cousins": ["SN-0065", "SN-0079", "SN-0215"], "evidence": {"board": ["#554 5967060029 ([NAYA 4][SELF-BUILD LOOP][SIGN-OUT] — H13 repair PROPOSED as PR #1345 (merge parked), 2026-10-03 08:11:05Z)"], "repair": "PR #1345, branch naya4/h13-lock-in-law-grant @ 3204d55b55a672facefecd6599afd088ba95d278, base main 5b68f8dcac78873741ed78d740f546b6f4083a22; additive fail-closed LAW grant check (action=learning_lock_in) before first canonical mutation, 403 LEARNING_LOCK_IN_LAW_DENIED on deny, authority_refs on all four lock-in artifacts", "testing": "node harness executes SHIPPED helper block verbatim — 14/14 PASS (no-grant/wrong-action/wrong-scope/expired/revoked/foreign-subject DENY; active in-scope grant AUTHORIZED); negative control: original pin file contains none of the control strings and DOES lock in — patch is operative", "residual_gap": "no Deno runtime in loop VM — edge function itself not executed end-to-end; CI on PR covers repo checks", "parked_decision": "human-director-package §18: merge #1345 + issue grant row (production write) vs ratify workflow-binding reasoning vs conform to Naya 2 Governance Contract V1 #1130 (draft)"}, "status": "PROPOSED — NOT merged, NOT deployed, NOT behaviorally proven live; merge is the director's gate", "rule": "a fail-closed authorization repair is not deployable as a code-only patch; the repair unit is code + sequenced provisioning (merge, then grant issuance), and the sequencing plan is parked with the gate owner — the lane never executes the production write"}
