# MAXESS / NAYA — SOURCE & MEMORY MAP

## Purpose
This file prevents source confusion by separating **governance, active engineering state, approved baselines, durable memory, and historical evidence**.

It is a map, not a competing source of product law.

## Current repository roles

### Canonical project brain

- `SoulSchoolAcademy/MaxRESULTS`
- `main` = governance/reference branch.
- `maxess-results-v21-working` = current active Results engineering branch.

### Governance / operating authority

- `START-HERE.md` — entry and cold-start law.
- `docs/REPOSITORY-MAP.md` — navigation, categories, authority, and current state.
- `NAYA-OS.md` — governing Naya/Nitro operating laws.
- `docs/NAYA-NITRO-MODE.md` — execution protocol.
- `docs/NAYA-EXECUTIVE-PLAN.md` — North Star and executive operating objective.
- `docs/NAYA-EXECUTION-PROMPT-TEMPLATE.md` — reusable execution contract.
- `docs/NAYA-SMART-NOTES-SYSTEM.md` — memory rules.

### Product authority

- `docs/MAXESS-RESULTS-PRODUCT-SPEC.md` — current consolidated Results requirements.
- `docs/NAYA-MAXESS-OPERATING-MANUAL.md` — practical Results operating rules.
- Task-specific design directives, when explicitly identified by the current user/task.

### Runtime data authority

`window.MAXESS_RESULT` is the authoritative runtime result object for the Results experience.

### Deployment authority

`docs/DEPLOYMENT-CONTRACT.md` defines GitHub → Groove → public verification. GitHub state is never proof of live publication.

### Release authority

`docs/RELEASE-CHECKLIST.md` defines the release gate. A release is not complete merely because code exists or source QA passes.

## State model

Use these states explicitly:

**WORKING** → actively being developed; not automatically approved.

**VERIFIED** → applicable engineering/behavior QA passed.

**HUMAN REVIEW REQUIRED** → human visual/product judgment remains.

**APPROVED BASELINE** → explicitly approved by the human/product authority.

**LIVE VERIFIED** → public target has been fetched and parity/visual QA passed.

**HISTORICAL** → preserved evidence, not active authority.

No file becomes authoritative merely because it is newer, larger, committed, or named “final.”

## Fresh Section 01 state

The current Section 01 build is a fresh working build. There is **no human-approved production baseline for the full Section 01 experience yet**.

The user has explicitly protected the existing **Orb visual/behavior system** as the element to preserve while the rest of Section 01 remains open to improvement.

Therefore:

- Orb = **PROTECTED WORKING DESIGN ELEMENT**.
- Surrounding Section 01 presentation = **OPEN FOR REFINEMENT**.
- Full Section 01 = **WORKING / NOT APPROVED**.
- Live/public parity = **NOT VERIFIED unless separately tested**.

Do not use stale “authoritative V21 renderer” wording from older delivery artifacts as a reason to freeze the rest of the design. If such wording appears in a supplied artifact, treat it as historical/contextual until reconciled with current human requirements.

## Memory architecture

### Naya Note / Smart Note

**Naya Note = Smart Note = durable Naya memory.**

The durable memory system is defined by `docs/NAYA-SMART-NOTES-SYSTEM.md` and stored under `docs/smart-notes/`.

The memory system must support retrieval by:

- date;
- category;
- title/topic;
- keywords;
- aliases/synonyms;
- related concepts;
- project/feature scope;
- natural-language meaning.

It must not depend on exact phrasing from the original conversation.

### Learning log

`docs/NAYA-NITRO-LEARNING-LOG.md` is the compact running record of durable execution-system lessons. It is not a replacement for the structured Smart Note system.

### Governance promotion

A Smart Note records learning/context. When a lesson becomes a true governing rule, promote it deliberately into the appropriate governance/product document and cross-reference the originating note.

## Historical knowledge

The original `SoulSchoolAcademy/maxess` repository remains historical reference material unless explicitly requested or deliberately migrated.

Historical source classes include:

- old governance documents;
- prior Results specifications;
- old execution directives;
- previous HTML renderers;
- generated fragments;
- old scripts;
- prior deployment artifacts;
- old Smart Notes.

Do not blindly copy historical authority into the active path.

## Migration rule

The clean repository should converge toward:

```text
ONE governance system
+ ONE current product specification per product
+ ONE explicit active engineering path
+ ONE approved baseline when approved
+ ONE runtime data authority
+ ONE deployment/release contract
+ ONE durable Smart Note memory system
+ historical evidence clearly marked as historical
+ deterministic QA/guardrails
```

Avoid:

```text
competing FINAL files
competing source-of-truth documents
duplicate memory systems
mystery loaders
unclassified experiments
stale claims of authority
```

## Legacy-reference rule

When an old document conflicts with the current explicit human requirement or current governance, do not silently choose the old rule. Surface the conflict, determine the current rule, update the appropriate authority, and preserve the historical evidence as historical.
