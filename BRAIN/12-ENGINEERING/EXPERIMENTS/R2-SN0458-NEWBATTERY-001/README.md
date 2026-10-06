# R2-SN0458-NEWBATTERY-001 — preregistered replacement battery

**Status:** DRAFT_AWAITING_INDEPENDENT_KEY_VALIDATION — NO TRIALS EXECUTED  
**Target lesson:** SN-0458, The Second-Source Rule  
**Builder:** Naya Captain  
**Independent answer-key verifier:** Coda 2

## Provenance classification

The original owner-authored Stage-1 scenario/key package has not been recoverable from the accessible GitHub sources searched, and the owner workstation remains unavailable. For execution purposes the original package is classified **FIXTURE_PROVENANCE_LOSS**.

This does **not** claim the bytes are physically destroyed. If originals later surface, preserve them under the original experiment identity. Never retroactively substitute them into this battery. This battery has a new ID precisely to prevent provenance laundering.

## Design

Three blinded arms use the same frozen baseline corpus at `8442edae26dc854d792729a52f1ab83c991944aa`:
- CONTROL — no lesson overlay.
- TREATMENT — exact SN-0458 bytes.
- WRONG_LESSON — preregistered conflicting heuristic.

Battery: 6 transfer tasks + 5 negative-transfer tasks. Run every task in every arm (11 trials/arm; 33 total). The answer key is physically separate from task-only views.

No trial may start until Coda 2 independently validates the answer key against the task facts and every fixture hash is frozen/rechecked. Until then the machine contract MUST reject this manifest; only the independent verifier can legitimately clear the prevalidation fact.

## Hard falsifiers

- Treatment does not beat Control on transfer accuracy.
- Treatment succeeds without retrieving/citing SN-0458 on the majority of its correct transfer trials.
- WRONG_LESSON performs equivalently to or better than Treatment on the target transfer set.
- Any treatment negative-transfer task flips from the key because the lesson is over-applied.
- Fixture/hash drift, hidden-key contamination, missing raw transcript, missing exact tool count, or post-hoc key/rubric edits void the affected battery.
- No experiment result changes authority.
