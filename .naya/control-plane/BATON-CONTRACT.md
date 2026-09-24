# NayaPOWER — Current Naya Baton Contract

**Status:** CANONICAL OPERATING CONTRACT  
**Path:** `.naya/control-plane/BATON.json`  
**Purpose:** Make the current Naya handoff a machine-readable, evidence-bound continuation object.

## Core law

**Every substantive Naya execution must leave one complete baton for the next Naya.**

The baton is not a second project state machine. It is the canonical continuation boundary that binds the current operational state to the current intelligence, evidence, authority, and one executable successor action.

## Baton contract

The baton binds:

1. **CURRENT STATE** — where NayaPOWER is now.
2. **CURRENT INTELLIGENCE** — the canonical intelligence needed to understand the present boundary.
3. **PROVEN / UNKNOWN** — evidence-backed truth and explicit uncertainty.
4. **ACTIVE BLOCK** — the current governed unit of work.
5. **ONE NEXT ACTION** — exactly one authorized executable action.
6. **EVIDENCE** — receipts/proofs supporting the state and claims.
7. **SUCCESSOR PROMPT** — directly executable continuation instructions.
8. **PLAYBACK POINTER** — where the successor can reconstruct relevant history and evolution.

## Authority relationship

The baton does not outrank the sources it references.

- Live Git identity outranks recorded identity.
- `.naya/control-plane/STATE.json` owns canonical operational current state.
- `.naya/control-plane/BLOCKS.json` owns the active block and single next action.
- `.naya/control-plane/MAP.json` owns mission/system/authority navigation.
- `.naya/control-plane/PROOF.json` owns proof-state/evidence rules and proof claims.
- The baton owns the **continuation contract**: the coherent handoff assembled from those authorities.
- Runtime/database state owns transactional runtime facts where explicitly applicable.
- Execution receipts and evidence artifacts support claims.
- Historical memory and conversation context cannot override canonical sources.

## Required baton fields

`identity`, `generated_at`, `source_of_truth`, `current_state`, `current_intelligence`, `truth`, `active_block`, `next_action`, `evidence`, `successor_prompt`, and `playback`.

The top-level `identity` is the canonical repository identity and must equal `repository`.

The top-level `evidence` is a non-empty list of read-only pointers to existing canonical proof sources; it does not promote a source or replace its claim state.

`source_snapshot.live_head` identifies the source commit used to derive the BATON projection, not necessarily the later commit that stores the BATON artifact. Freshness validation requires that source commit to remain an ancestor of live HEAD with no unaccounted source-surface changes after it.

## One-next-action law

The baton MUST expose exactly one executable next action. A vague instruction such as “continue” is invalid.

The action must state:

- objective;
- source of truth;
- execution;
- acceptance;
- verification;
- successor requirement.

## Truth law

The baton must distinguish:

- PROVEN / VERIFIED
- IMPLEMENTED
- UNKNOWN
- FAILED
- BLOCKED
- STALE

No assertion becomes proof merely because it appears in the baton.

## Playback law

The baton points to the current applicable intelligence first and preserves lineage/history separately.

**Default retrieval:** latest applicable canonical state.  
**Playback:** reconstruct prior states, decisions, corrections, evidence, and handoffs when required.

New intelligence must not silently erase historical intelligence.

## Continuation law

A substantive execution is incomplete for handoff until:

`CURRENT STATE → NEXT ACTION → EXECUTE → VERIFY → RECORD → UPDATE BATON → SUCCESSOR`

The baton is therefore the bridge between Naya sessions.

## Automation target

The first implementation may assemble the baton from existing canonical control-plane sources.

The mature runtime must automatically refresh it after every meaningful state-changing Naya execution and make it consumable by a cold successor.

## Acceptance

A cold Naya must be able to:

1. load the baton;
2. resolve its referenced canonical sources;
3. understand current state;
4. distinguish proof from unknown;
5. understand the active block;
6. execute the one next action when authorized;
7. verify the outcome;
8. update the baton;
9. leave the next successor with a new baton.

**No conversational archaeology. No competing next-action state machine. No hidden human reconstruction.**

## Operating slogan

**TAG → YOU'RE IT → EXECUTE → VERIFY → RECORD → UPDATE → PASS THE BATON.**
