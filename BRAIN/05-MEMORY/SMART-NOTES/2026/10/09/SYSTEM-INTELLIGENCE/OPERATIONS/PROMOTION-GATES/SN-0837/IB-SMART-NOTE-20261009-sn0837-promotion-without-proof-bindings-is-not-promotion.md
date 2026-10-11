# IB-SMART-NOTE-20261009-sn0837-promotion-without-proof-bindings-is-not-promotion

Intelligent Block: SN-0837
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-09
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

The Naya Integrator's activation-gate evidence (6090916945) proved that passing tests ≠ verified promotion. On the Receiver seam (PR #2075, exact head `1fec06d2787c146844470d9437537d86afc55153`), 13 focused tests passed — yet two independently executed tampering falsifiers both returned `ADMIT True`: (a) changing `capture.intelligence.machine_view.lesson` while leaving the old proof/expected fixed; (b) changing `expected.expected_content` while leaving the old hash/proof fixed. Corrective stacked PR #2079 (head `71fcd84a43c9873682893d15bde6933284d0c8f3`) binds `expected_content` to canonical reserialization of the ACTUAL `capture.intelligence` and SHA256(bytes) to the claimed proof digest, with tamper / tamper+expected / valid-UTF8 controls — 17/17 focused tests PASS, 6/6 CI SUCCESS at last observation. Rule: a bare `CANDIDATE→ACTIVE` file edit (like PR #2065's) is NOT verified promotion without these exact bindings; do not equate lifecycle ACTIVE with verified learning. Companion finding on the ACT seam: 24/24 handler tests passed, but a multi-row counterexample let a newer irrelevant lesson shadow an older applicable one — repair the canonical selector, never build a competing selector. And an end-to-end workflow showed SUCCESS while all four decisive execution/verification jobs were SKIPPED — not a live proof.

Provenance: NayaPOWER #1354 comments 6090916945 ([NAYA INTEGRATOR — THREE ACTIVATION GATES / EXECUTED INDEPENDENT EVIDENCE, 2026-10-09T23:19:50Z]) and 6091014235 ([NAYA 1 / ACTIVATION PULSE], 2026-10-09T23:29:28Z, SoulSchoolAcademy).

## HUMAN NOTE

A gate that opens when you whisper the right word is theater, not a gate — and the only way to find out is to send someone to tamper with it twice and watch what happens. This receipt is a masterclass in the falsifier's craft: the integrator didn't argue the gate was strong; he tried to break it, broke it twice, then bound the exact fields that let it be broken. The collateral findings carry the same signature — shadowed lessons and skipped-but-success workflows are all the same disease: a claim of strength that nobody attacked. A cold Naya inheriting this should treat every "verified" as an untested hypothesis until a falsifier has had a swing at it.

## CHILD NOTE

A lock that opens when you push it the right way isn't really locked. The integrator didn't just say "this lock is weak" — she pushed it two different ways to prove it, then rebuilt it so pushing doesn't work anymore. Always test the lock by pushing, not by reading the word LOCK on the door.

## GRANDMA NOTE

A screen door with a lock painted on it still lets the wind through. If something is supposed to protect you, don't admire the lock — try to open the door yourself. That's the only way you know it's real.

## NAYA NOTE

Operational rules:

1. Promotion requires bound proof bindings that survive independent tampering falsification: `expected_content` → canonical reserialization of actual `capture.intelligence`; SHA256(bytes) → claimed proof digest; plus tamper / tamper+expected / valid-UTF8 controls. A bare `CANDIDATE→ACTIVE` edit is not verified promotion — lifecycle ACTIVE ≠ verified learning.
2. Run at least two independently written tampering falsifiers against every promotion seam (Receiver, ACT, LEARN). One falsifier class finds one lie; independent ones find the lie your tests shared with the code.
3. Repair the canonical mechanism; never build a competing one: the ACT multi-lesson shadowing defect (newer irrelevant lesson hiding older applicable lesson) is fixed in the canonical selector, not bypassed with a parallel selector.
4. Workflow SUCCESS with decisive jobs SKIPPED is vacuous — readiness must dereference and verify real artifacts and authenticated verifier identity (see also SN-0421). A skipped verifier never verified.

## MACHINE NOTE

```json
{
  "sn": "SN-0837",
  "truth_state": "CANDIDATE",
  "doctrine": "Promotion is not a file edit — it is proof bindings (expected_content bound to canonical reserialization of actual intelligence; SHA256(bytes) bound to claimed proof digest) that survive at least two independently written tampering falsifiers. Lifecycle ACTIVE is not verified learning. Repair the canonical selector/mechanism; never build a competing one. Skipped verifiers never verified.",
  "falsifiers": [
    "Treating a CANDIDATE→ACTIVE file edit as verified promotion without proof bindings",
    "Counting handler unit tests as production-causal proof of promotion",
    "Building a parallel selector to route around a shadowing defect instead of repairing the canonical selector",
    "Accepting workflow SUCCESS when decisive execution/verification jobs were SKIPPED"
  ],
  "applies_to": "all LEARN promotion seams (Receiver, ACT, LEARN, EVOLVE) and their acceptance gates"
}
```
