# NayaNET Intelligent Hub — Canonical Architecture Map

**Status:** CANONICAL ARCHITECTURE BOUNDARY — 2026-09-22
**Repository:** SoulSchoolAcademy/NayaPOWER
**Application boundary:** `NAYANET/HUB/`
**Production runtime target:** `https://sparkling-shape-7ae5.smartnetpodcast.workers.dev`
**Authority:** GitHub `main` → canonical Hub build → exact artifact → Cloudflare Worker → live runtime

## Architecture law

`NAYANET/HUB/` is the **only implementation boundary for the NayaNET Intelligent Hub**.

Everything required to build, run, test, and present the Hub belongs under this boundary, except genuinely shared NayaPOWER platform/control-plane infrastructure.

No Hub feature may have a second mutable implementation elsewhere in the repository.

Historical artifacts may remain outside the boundary for provenance, but they are not executable production authority.

## Canonical application tree

```
NayaPOWER/
├── NAYANET/
│   └── HUB/                              # THE APPLICATION
│       ├── index.html                    # canonical human-facing shell/reference entry
│       ├── package.json                  # Hub build contract
│       ├── package-lock.json
│       ├── vite.config.ts
│       ├── tsconfig.json
│       ├── wrangler.jsonc                # Worker contract
│       ├── worker.js                     # canonical Worker entry
│       ├── public/                       # browser-served assets
│       │   ├── NAYANET/
│       │   │   └── name-first-auth-adapter.js
│       │   ├── assistant-runtime.js
│       │   ├── hub-completeness.js
│       │   ├── smart-feed.js
│       │   ├── smart-tabs.js
│       │   ├── nayanet-interface-command-station.js
│       │   └── intelligence/
│       │       └── pis-feed.json         # generated projection, never authority
│       ├── src/
│       │   ├── main.tsx                  # application bootstrap
│       │   ├── app/                      # shell, routing, feature surfaces
│       │   ├── identity/                 # identity/session boundary
│       │   ├── intelligence/             # intelligence objects and presentation
│       │   ├── data/                     # retrieval/projection adapters
│       │   ├── config/                   # Hub configuration
│       │   ├── baseline/                 # protected reference only
│       │   └── styles/                   # one owned visual system
│       ├── scripts/                      # Hub-only tooling
│       ├── contracts/                    # Hub contracts
│       ├── tests/                        # Hub acceptance/integration/unit tests
│       ├── features/                     # feature specifications
│       ├── docs/                         # current engineering documentation
│       └── ARCHITECTURE-MAP.md
│
├── .naya/                                # NayaPOWER control plane
│   ├── control-plane/                    # state, baton, authorization, proof
│   ├── runtime/                          # governed execution substrate
│   ├── governance/                      # policy/constitutional controls
│   ├── contracts/                        # cross-system contracts
│   ├── intelligence/                    # canonical intelligence schemas
│   ├── learning/                        # learning state/contracts
│   ├── memory/                          # durable Naya memory
│   ├── project-intelligence/            # project cognition
│   ├── handoffs/                        # successor continuity
│   └── tests/                            # control-plane tests
│
├── supabase/                             # managed persistence/server boundary
│   ├── functions/
│   └── migrations/
├── NAYANET/EXECUTION-BRIDGE/             # shared transport/integration
├── scripts/                              # shared platform tooling only
└── .github/workflows/                    # CI/CD/governance orchestration
```

## Hub feature tree

```
HUB
├── Shell
│   ├── Identity
│   ├── Top Bar
│   ├── Search / Talk to Naya
│   ├── Navigation
│   └── Responsive / Mobile
├── Intelligence
│   ├── Intelligence Today
│   ├── Smart Feed
│   │   ├── Collective
│   │   ├── Personal
│   │   └── Activity
│   ├── Intelligent Blocks
│   ├── Universal Search
│   └── Intelligence Library
├── Capture
│   └── Smart Notes
├── Connect
│   ├── Smart Share
│   ├── Smart Lists
│   ├── Smart Spaces
│   ├── Connections
│   └── Smart Mail
├── Understand
│   ├── Reports
│   ├── Smart Ledger
│   ├── Evidence
│   └── Activity
├── Learn
│   ├── Dream
│   └── Adaptive Learning
├── Use
│   └── Naya Play
└── Settings
    └── Identity / privacy / preferences
```

The feature tree is one application, not separate applications. One intelligence object may project into multiple surfaces without creating a second source of truth.

## Causal contract

`HUMAN → HUB → GOVERNED CAPABILITY → NAYAPOWER → PERSISTENCE → RETRIEVAL → HUB → EVIDENCE → CONTINUATION`

A selector, route, component, or successful HTTP response is not by itself proof of this chain.

## Audit findings that must be repaired

### GAP-001 — Production does not currently build the Hub application

The current canonical Cloudflare workflow manually assembles `dist/` from the Hub HTML plus Hub-specific files that live outside the Hub:

- root `assistant-runtime.js`
- root `hub-completeness.js`
- root `smart-feed.js`
- root `smart-tabs.js`
- root `identity.html`
- `NAYANET/name-first-auth-adapter.js`

It then deploys that assembled artifact.

**Consequence:** the live Worker is not presently a transparent deployment of the application tree under `NAYANET/HUB/src/`. This is the primary source/runtime ambiguity.

### GAP-002 — The Hub build itself reaches outside its boundary

`NAYANET/HUB/package.json` currently copies Hub-specific build/runtime assets from:

- `../../scripts/build-smart-feed-projection.py`
- `../../scripts/nayanet-cognitive-engine.js`
- `../../assistant-runtime.js`
- `../../smart-feed.js`
- `../../smart-tabs.js`
- `../name-first-auth-adapter.js`
- `../../identity.html`

A canonical application must be buildable from its own boundary plus explicitly declared shared packages/interfaces.

### GAP-003 — Mutable duplicate browser runtimes exist

Both root and Hub-public copies exist for the main browser runtime assets. They are not all byte-identical:

- `assistant-runtime.js`: different blobs
- `hub-completeness.js`: different blobs
- `smart-feed.js`: different blobs
- `smart-tabs.js`: same blob
- name-first adapter: Hub-public and root copies both exist

This is a direct single-source-of-truth violation.

### GAP-004 — Historical Hub implementations are mixed with the active application

The repository still contains substantial historical/competing Hub surfaces, including:

- `NAYANET/E02-INTELLIGENT-HUB/`
- `NAYANET/E02-INTELLIGENT-HUB-AAA/`
- `NAYANET/E02-INTELLIGENT-HUB-CLOUDFLARE/`
- `NAYANET/E03-INTELLIGENT-HUB/`
- dated root Hub HTML/JS artifacts
- historical Smart Feed implementations
- `NAYANET/HUB/src/baseline/HubBaselineApp.tsx`

These can be retained as provenance, but production authority must be machine-unambiguous.

### GAP-005 — Visual reference and application authority are mixed

The protected visual baseline is a reference. The operational Hub is the application.

Correct relationship:

**PROTECTED REFERENCE → ONE IMPLEMENTED HUB → ONE BUILD → ONE ARTIFACT → ONE RUNTIME**

The reference must not silently become a second production application.

### GAP-006 — CI/CD ownership is too fragmented

The repository currently contains 32 workflow files. Many are legitimate NayaPOWER proofs, but production Hub release authority must be singular.

Verification workflows may prove individual contracts. Only one release workflow may publish the Hub.

## Elite release chain

```
GitHub main
   ↓
NAYANET/HUB source
   ↓
Hub dependency + type + build validation
   ↓
deterministic artifact
   ↓
release manifest
   ├── source commit SHA
   ├── source entry/blob SHA
   ├── build identity
   ├── artifact SHA
   ├── Worker name
   └── release timestamp
   ↓
Cloudflare Worker: sparkling-shape-7ae5
   ↓
exact live artifact parity
   ↓
browser rendering
   ↓
human interaction
   ↓
causal consequence
   ↓
evidence / ledger / activity
```

No hidden source assembly is allowed between these stages.

## Enforcement invariants

CI must fail when:

1. A production Hub implementation exists outside `NAYANET/HUB/`.
2. The release workflow imports Hub-specific source from outside `NAYANET/HUB/`.
3. A second Hub HTML entry becomes deployable.
4. The release artifact cannot be mapped to one Git commit.
5. Source and artifact identities disagree.
6. A historical Hub surface becomes the production entrypoint.
7. A feature creates a second intelligence/persistence authority.
8. A Smart Door bypasses the governed capability boundary.
9. Navigation/selector success is treated as causal production proof.

## Refactoring law

Do **not** redesign the accepted product merely to clean the repository.

First consolidate ownership. Then progressively refactor internals while preserving the accepted visual language and proven behavior.

Required sequence:

**1. Internalize Hub-specific runtime/build assets → 2. make Hub build self-contained → 3. make one release consume only Hub → 4. explicitly retire/mark competing production surfaces → 5. enforce the boundary in CI → 6. prove exact artifact/runtime parity → 7. continue feature completion.**

## Cold-engineer test

A new engineer should be able to answer without conversation archaeology:

- **Where is the Hub?** `NAYANET/HUB/`
- **Where is its source?** `NAYANET/HUB/src/` plus its canonical entry.
- **Where are browser runtime assets?** `NAYANET/HUB/public/`
- **Where are Hub tests?** `NAYANET/HUB/tests/`
- **Where are Hub contracts?** `NAYANET/HUB/contracts/`
- **What builds it?** `NAYANET/HUB/package.json`
- **What deploys it?** one canonical release workflow.
- **Where does it run?** `sparkling-shape-7ae5`
- **Where is governance?** `.naya/`
- **Where is managed persistence?** `supabase/`
- **How is release identity proven?** Git source SHA → artifact SHA → live runtime → browser evidence.
- **What is historical?** everything outside the implementation boundary that is explicitly classified non-authoritative.

**Final law: ONE BRAIN. ONE HUB. ONE BUILD. ONE ARTIFACT. ONE RUNTIME. ONE CURRENT STATE. ONE NEXT ACTION.**
