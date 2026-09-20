# NAYA POWER — SMART NOTE / INTELLIGENT BLOCK DATA CONTRACT V1

DATE: 2026-09-12
STATUS: CANONICAL DATA CONTRACT V1
NUMBER: 42
AUTHORITY: SUBORDINATE TO #40 AND GOVERNANCE

## PURPOSE
Define the canonical information object that can become a Smart Note, Intelligent Block, and feed item without losing provenance, meaning, privacy, or verification.

## 1. CANONICAL OBJECT

A Smart Note is one intelligence event containing, where applicable:
- event identity;
- source identity;
- timestamp;
- author/actor;
- mission/context;
- verification state;
- privacy/publication state;
- In a Nutshell;
- Human Note;
- Child View;
- Grabber View;
- Naya Note;
- Machine Note;
- Adapter Learning;
- What It Means;
- What's In It For You;
- provenance;
- related events;
- actions;
- Space relationships;
- reaction/rating/comment state.

## 2. REQUIRED SEMANTIC LAYERS

IN A NUTSHELL = fastest truthful comprehension.
HUMAN NOTE = human-originated meaning/context.
CHILD VIEW = simplest understandable explanation.
GRABBER VIEW = compelling entry point without deception.
NAYA NOTE = intelligent interpretation/recommendation.
MACHINE NOTE = machine-readable execution/state detail.
ADAPTER LEARNING = what the system learned or adapted.
WHAT IT MEANS = significance.
WHAT'S IN IT FOR YOU = practical value/application.

These layers are semantic contracts, not merely visual tabs.

## 3. TRUTH

Every factual assertion that matters must retain source/provenance and verification classification. UNKNOWN is valid. Historical proof cannot silently become current proof.

## 4. IDENTITY

Every object has a stable event/intelligence identity. Rendering in multiple feeds must not clone the intelligence object into independent truths.

## 5. PRIVACY

Publication state is explicit: PRIVATE, SHAREABLE, PUBLIC. Personal content cannot enter Collective without an authorized publication transition.

## 6. ACTIONS

Collective: Create Space, Favorite, Save, Share, Rate This Intel, Love, Like, Comment.
Personal: Favorite, Save, Share, Make Public.
Activity: inspect, open source, continue action, verify, record where authorized.

## 7. VERSIONING

The object may evolve through verified events. Consumers should tolerate additive fields and preserve unknown fields rather than destructively rewriting intelligence.

## 8. QUALITY GATE

A valid Intelligent Block must be understandable without opening Machine Note, traceable to a source/event, privacy-correct, state-correct, and actionable when an action is available.


## 9. CANONICAL REPOSITORY LOCATION + LIFECYCLE

Effective 2026-09-19, the single canonical human-facing repository collection for Smart Notes is:

`SMART-NOTES/YYYY/MM/DD/SN-YYYYMMDD-<slug>.md`

A Smart Note has one stable intelligence identity and one canonical human-facing repository home. It may have governed runtime representations elsewhere, but those representations are projections/runtime state and must preserve the same identity, provenance, privacy, and verification state.

The canonical lifecycle is:

**CREATE → CANONICALIZE → PERSIST → VERIFY → INDEX → LEARN → RETRIEVE → REPLAY/APPLY → VERIFY OUTCOME → COMPOUND**

### Runtime separation

- `SMART-NOTES/YYYY/MM/DD/` = canonical human-readable intelligence corpus.
- `.naya/memory/` and other runtime paths = machine-readable events, indexes, receipts, validators, and implementation state.
- Supabase / managed persistence = governed durable runtime persistence.
- Intelligence Index / Intelligent Blocks / reports / learning evidence / Dream replay = derived or projected intelligence that must retain canonical provenance.
- Intelligent Hub = human-facing projection/action surface, never a competing source of truth.

### Cold-Naya rule

Every Naya must read this contract and the canonical Activity Feed before creating a Smart Note. New canonical Smart Notes must use the `SMART-NOTES/YYYY/MM/DD/` convention. If an existing artifact is found elsewhere, classify it before moving, copying, deleting, or treating it as canonical.

**One Smart Note = one stable identity = one canonical human-facing home.**
