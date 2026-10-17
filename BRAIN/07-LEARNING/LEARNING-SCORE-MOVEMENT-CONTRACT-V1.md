# Learning Score-Movement Contract v1

**Status:** RATIFIED OPERATIONAL CONTRACT — 2026-10-09  
**Authority:** Naya 1 operational ratification, under the Human Director's explicit instruction to make the learning score contract official. The Human Director remains final consequential authority.  
**Canonical coordination record:** [Team Naya #1354](https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1354#issuecomment-6086218713)  
**Learning execution owner:** Naya 4, [Learning team feed #1865](https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1865)  
**Scope:** LEARNING score only. Do not substitute this ladder for other area scorecards.

## Prime rules

1. **“Smart Note this” is user value approval and authorization to capture.** Do not place an authorized capture in a discretionary value-review queue.
2. **Capture authorization does not disable machine law.** Schema, authentication, authority, provenance, integrity, consent/scope, and safety checks remain automatic and fail closed.
3. **Capture/activation, observed behavior change, and cold successor reuse are distinct milestones.** Never report one as another.
4. **UNKNOWN/BLOCKED is not PASS. STORED is not LEARNED. RETRIEVED is not UNDERSTOOD. IMPLEMENTED is not VERIFIED.**
5. **A builder cannot verify their own result.** Verification requires a different seat using independent evidence or replay.
6. **Activity has zero score weight.** Note counts, candidate counts, PRs, comments, test counts, and “building” statuses do not move the score.
7. **No skipped rungs, no averaged-away weakness.** Each threshold is cumulative and earned on exact evidence.
8. **One canonical pipeline.** No parallel capture, receipt, registry, or resolver authority may be introduced to make a demo pass.

## The 5.0 → 10.0 ladder

All evidence must be tied to an exact tested main SHA, named task, raw outcome, canonical receipt/run, and verifier. The scorer records both the evidence and any remaining unknown.

| Score | Capability proved | Minimum acceptance evidence |
|---:|---|---|
| **5.0** | Captured — baseline | Canonical Smart Note transactions persist with valid schema, truth state, and receipt. Capture volume has no further score weight. |
| **5.5** | Retrievable by intent | Three cold queries retrieve the applicable lesson without Smart Note ID hints; query, result, and relevance are recorded. |
| **6.0** | Falsifiable | 100% of the defined scored lesson set has a substantive falsifier; machine check plus a 10% substance sample. |
| **6.5** | Applied | Three real decision receipts show lesson → changed decision → counterfactual, independently checked. |
| **7.0** | Independently verified | Five lesson claims are confirmed by a different seat using independent evidence, not author restatement. |
| **7.5** | Legitimate promotion | At least one real, non-test lesson passes the actual promotion gate with a receipt and no bypass/override. |
| **8.0** | Machine-enforced | Three lessons are executable laws/gates, each with lawful acceptance and unlawful rejection demonstrated in CI or runtime. |
| **8.5** | Holds over time | Three closed loops pass a preregistered recurrence check of at least seven days. A recurrence removes that loop from the count until repaired and retested. |
| **9.0** | Cold successor reuse | One zero-warm-context successor retrieves by intent, applies the lesson to a real task, and produces an independently verified behavior delta. A plausible WRONG_LESSON control must not improve the outcome. |
| **9.5** | Replicated compounding | The full capture → persist → receipt/link → cold retrieve → apply → observe → verify → successor-reuse loop repeats across at least three distinct lessons, with independent verification and no synthetic substitute for production-path evidence. |
| **10.0** | Self-sustaining learning | All 9.5 criteria hold; at least three full loops in the trailing 30 days originate without Shawn prompting the correction; Naya 1 and the Human Director explicitly confirm. |

## Required score receipt

Every score assignment or change must record:

- score before and after, with the exact rung being claimed;
- exact repository main SHA and runtime/CI run identifiers;
- named lesson and task, CONTROL/TREATMENT/WRONG_LESSON definition where causal learning is claimed;
- raw outcomes, canonical capture receipt, Smart Link, cold-retrieval result, and behavior delta as applicable;
- builder seat and distinct verifier seat;
- evidence URL(s), verdict, remaining UNKNOWN/BLOCKED items, and next weakest point.

If the rung's minimum evidence is absent, retain the existing score and state the precise missing evidence. Do not round, infer, or award partial credit for activity.

## Immediate application to the current state

The authoritative LEARNING score remains **5.0** until the next rung is evidenced. Read-only inspection of the connected Supabase project found the two latest GitHub projection receipts failed with `GITHUB_COMMIT_FAILED:403`; the related canonical transaction rows were `completed`. That means capture transaction completion is not proof of a verified GitHub projection or cold retrieval.

The next operational target is therefore to close the projection seam and prove cold retrieval by intent. The score contract does not block capture: user-authorized capture proceeds immediately through the canonical path, with automated guards intact. Score movement waits for the relevant evidence.

## Owners and separation of duties

- **Naya 4 / Learning lead:** coordinates one closure path, tracks the owner → deliverable → different-seat verifier table, and reports score evidence.
- **Instant-activation builder (#1713):** repairs the canonical capture/projection seam and supplies branch/PR/head plus negative controls.
- **E2E pipeline owner (#1741):** runs a real authorized capture through persisted bytes, `PROJECTION_VERIFIED`, generated Smart Link, and cold retrieval.
- **Experiment owner (#1602):** runs the preregistered CONTROL/TREATMENT/WRONG_LESSON test and cold successor B/C only after real retrieval is available.
- **Independent verifier:** must not be the builder; independently replays the exact evidence.
- **Human Director:** final consequential authority.

These are coordinated responsibilities, not parallel pipelines. Every sign-out reports actual changes, evidence, score delta (or explicitly zero), first broken link, and one next action.

## Ratification and change control

This v1 is the single operational ladder. Amend it only by a versioned, explicit decision that replaces the full mapping; do not keep competing active rubrics. Ratification of the contract does not itself raise the score or prove the learning loop.
