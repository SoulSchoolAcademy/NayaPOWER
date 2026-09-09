# 07 — Rebuild + Acceptance Contract

## Mission

Rebuild the NayaNET Intelligent Hub from verified understanding, not from accumulated patches.

The old product is the evidence base. The new implementation is a clean expression of the proven intent and preserved functionality.

## Phase 0 — Lock authority

Before coding:

- Select exactly one current Hub source.
- Archive historical snapshots explicitly.
- Select exactly one feed renderer.
- Select exactly one persistence contract.
- Select exactly one route/state model.
- Record all external destinations from the Page Map.

**BLOCKER:** the current repository contains a source-authority discrepancy. Resolve it first.

## Phase 1 — Build the shell

Acceptance:
- desktop left sidebar works.
- no desktop right sidebar.
- mobile has no left sidebar.
- mobile bottom nav works.
- topbar works.
- ecosystem links all work.
- feature report links all work.
- active state is correct after every navigation.

## Phase 2 — Build the intelligence model

Acceptance:
- one event = one canonical identity.
- Human meaning is preserved exactly.
- Naya output is clearly separated from Human input.
- Machine evidence is clearly separated from semantic intelligence.
- Feed is a projection, not a second memory store.
- verification state is explicit.

## Phase 3 — Build Smart Notes

Acceptance:
- capture works.
- type classification works or is explicitly user-editable.
- persistence works.
- reload preserves notes.
- search works.
- category filters work.
- time filters work.
- note opens into the same canonical event, not a duplicate object.

## Phase 4 — Build Intelligent Feed

Acceptance:
- no two-column board renderer.
- no random horizontal cards.
- no code/debug artifacts.
- no competing renderer.
- no repeated DOM mutation loop.
- every board is a single coherent intelligence object.
- sequence supports:
  WISDOM → HUMAN → CHILD → GRANDMA → NAYA → MACHINE → WEAVER → LESSON / MEANING / ACTION.
- feed answers current-state questions.
- feed is chronological/current-state-first.

## Phase 5 — Build retrieval

Acceptance:
- global intelligence search works.
- Smart Notes search works.
- result has source ID/provenance.
- result can locate the original event.
- search does not silently invent semantic answers.

## Phase 6 — Build Naya connection

Acceptance:
- real authenticated Naya adapter exists.
- request/response is traceable.
- Naya response is attached to the correct event.
- machine receipt exists.
- pending/blocked/failed states are visible.
- no response is fabricated when the service is unavailable.

## Phase 7 — Build Daily Intelligence

Acceptance:
- report is source-backed.
- no fake activity fills empty periods.
- report distinguishes observed facts from interpretation.
- report carries forward learning and next action.

## Phase 8 — Build Collective

Acceptance:
- private by default.
- explicit consent required.
- de-identification boundary exists.
- collective view never exposes raw private notes.
- opt-out persists.

## Phase 9 — Build Smart Mail

Acceptance:
- compose works.
- drafts persist.
- send only becomes SENT after actual transport receipt.
- failed/pending states remain truthful.
- inbox/sent/drafts/rooms/groups/lists are real states, not decorative tabs.

## Phase 10 — Build Settings

Acceptance:
- each setting has defined effect.
- setting persistence is proven.
- reset works.
- settings do not exist merely to look configurable.

## Phase 11 — Visual excellence

Acceptance:
- premium black/obsidian/purple/white/gold system.
- cinematic editorial intelligence.
- strong hierarchy.
- no generic SaaS cards.
- no glassmorphism overload.
- no clutter.
- no competing visual centers.
- all controls feel intentional.
- desktop and mobile both feel designed, not merely collapsed.

## Phase 12 — Verification

### Source
- exact current source file identified.
- source markers present.

### Artifact
- build contains exact source.
- assets resolve.

### Deployment
- expected worker/version deployed.

### Runtime
- exact public URL returns expected artifact.
- Smart Link returns expected artifact.
- feed asset returns expected renderer.

### Visual
- browser observation confirms page.
- no right sidebar.
- no garbage/debug.
- correct boards.
- correct links.

### Interaction
Test every critical action:
- Home
- Smart Notes
- Reports
- Intelligence Library
- Collective
- Evidence
- Connections
- Smart Mail
- Settings
- ecosystem links
- feature reports
- create note
- search
- filters
- feed engagement
- verify GitHub
- compose mail
- settings save/reset
- collective toggle

### Persistence
- create note → reload → note remains.
- setting → reload → setting remains.
- draft → reload → draft remains.
- engagement → reload → state remains.

### Responsive
- desktop.
- tablet.
- mobile.
- narrow mobile.
- keyboard/focus.
- reduced motion.

## Completion standard

A Hub task is complete only when:

**SOURCE → BUILD → DEPLOY → RUNTIME → OBSERVATION → INTERACTION → PERSISTENCE → MOBILE → NO REGRESSION**

is proven.

A successful GitHub commit is not a successful product release.

A successful workflow is not visual proof.

A source marker is not proof that the correct DOM is visible.

## AAA scorecard

### A — Architecture
- one source
- one state model
- one renderer
- one persistence boundary
- explicit adapters

### A — Application
- all pages work
- all buttons work
- all links work
- all data transitions are understandable
- no dead ends

### A — Assurance
- runtime verified
- evidence preserved
- regressions tested
- truth states explicit
- no fabricated intelligence

## Final build principle

**Learn from every failed patch. Preserve what was proven. Remove what created ambiguity. Rebuild the system so the next Naya has to reason less, guess less, and verify more.**
