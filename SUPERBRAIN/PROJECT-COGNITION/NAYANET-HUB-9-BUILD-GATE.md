# NayaNET Hub 9 — Build Completion Gate

## Purpose
This gate defines when Hub 9 is **finished being set up**. It deliberately separates build/setup completion from later public runtime verification.

## Phase A — Source reconstruction

- [ ] Identify the single current Hub 9 source artifact.
- [ ] Inventory HTML structure, pages, navigation, feed containers, event handlers, persistence stores, and injected/additive scripts.
- [ ] Identify duplicate or historical feed authorities.
- [ ] Identify every localStorage key and classify it as UI preference, user content, engagement, cache, or cognition.
- [ ] Identify current source-of-truth boundaries.
- [ ] Preserve known-good behavior before making changes.

## Phase B — Cognitive operating mechanism

The Hub must implement:

`ENTER → LOAD → ORIENT → VERIFY → DECIDE → ACT → OBSERVE → RECORD → LEARN → HAND OFF`

Required state:

- situation
- current action
- history/result
- objective
- confidence + basis
- what matters
- self-challenge/evaluation
- next action
- result
- change
- evidence
- known-good baseline
- unknowns/blockers
- successor handoff

## Phase C — Persistence

- [ ] Cognition state is versioned.
- [ ] State updates are revision-checked.
- [ ] Stale writes cannot silently overwrite newer state.
- [ ] State and execution receipt form one logical transition where possible.
- [ ] Failure leaves a truthful recoverable state.
- [ ] Successor can restore state without prior conversation history.

## Phase D — Intelligence experience

The Hub must make the protocol useful, not merely visible.

A user/Naya should be able to answer immediately:

1. What is happening?
2. What are we doing?
3. What already happened?
4. What are we trying to accomplish?
5. How confident are we, and why?
6. What matters most?
7. What should we challenge?
8. What is the highest-value next action?
9. What happened after acting?
10. What changed?
11. What should carry forward?

## Phase E — Presentation AAA pass

- [ ] Black is the reading environment.
- [ ] White is the primary information color.
- [ ] Spectral color identifies meaning/perspective rather than decorating text.
- [ ] The nutshell is visually dominant.
- [ ] Perspective boards are distinct and easy to scan.
- [ ] Primary action buttons are obvious and large enough.
- [ ] No duplicated feed authorities.
- [ ] No contradictory labels.
- [ ] No decorative control without a useful function.
- [ ] No white-on-white, black-on-black, or low-contrast critical information.
- [ ] Mobile is intentionally designed, not merely squeezed.

## Phase F — Truth and failure gates

The Hub must never represent:

- local persistence as server proof;
- demo intelligence as real Naya interpretation;
- a blocked capability as success;
- an intended deployment as a verified deployment;
- an unobserved outcome as a completed action.

Failure transition:

`STOP → RECORD FAILURE → PRESERVE KNOWN-GOOD → UPDATE UNKNOWN/FAILED STATE → CAPTURE LEARNING → DEFINE NEXT ACTION → HANDOFF`

## Phase G — Cold handoff

**Naya A**

- enters with current state;
- performs one meaningful action;
- records expected result;
- observes actual result;
- attaches evidence;
- persists revision;
- captures learning;
- writes exact next action;
- exits.

**Naya B**

- enters with no conversation history;
- loads the durable state;
- identifies the prior result and evidence;
- identifies remaining work;
- identifies exact next action;
- cannot overwrite a newer revision with stale state.

## Phase H — Release proof (later)

Only after A–G pass:

`SOURCE → BUILD ARTIFACT → DEPLOYMENT → EXACT PUBLIC HUB 9 URL → INDEPENDENT OBSERVATION`

A setup/build pass is **not** a runtime pass. Runtime is the final release-proof stage.

## Completion rule

Hub 9 is **BUILD-READY** only when every required setup gate A–G is evidenced. It becomes **RELEASE-VERIFIED** only after Phase H is independently observed.
