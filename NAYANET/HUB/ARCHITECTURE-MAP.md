# NayaNET Hub — Canonical Architecture

## Purpose

NAYANET/HUB is the only current human-facing Hub application boundary.
The Hub exists to turn a person's captured intelligence into something they can see, understand, connect, use, verify, preserve, and carry forward.
The current NAYANET/HUB/index.html source is the visual quality reference. It defines the quality bar for interaction, visual hierarchy, Smart Feed presentation, icon quality, spacing, depth, responsiveness, and polish — not a ceiling. Future work must improve the experience without creating a second Hub.

## Non-negotiable architecture

One source → one app boundary → one build → one artifact → one runtime.

- Human-facing source: NAYANET/HUB/index.html
- Runtime assets: NAYANET/HUB/public/
- Application source: NAYANET/HUB/src/
- Contracts: NAYANET/HUB/contracts/
- Feature specifications and integration boundaries: NAYANET/HUB/features/
- Verification: NAYANET/HUB/tests/ and NAYANET/HUB/scripts/
- Build output: NAYANET/HUB/dist/ (generated, never source)
- Cloudflare entry: NAYANET/HUB/worker.js
- Cloudflare configuration: NAYANET/HUB/wrangler.jsonc
- Managed persistence: Supabase, treated as the canonical data/service layer rather than a mirrored filesystem tree.

No Hub build step may reach upward into the repository for Hub-specific browser/runtime/build files.

## 10/10 tree

```text
NAYANET/HUB/
├── app/
│   ├── shell/
│   ├── navigation/
│   ├── routing/
│   └── state/
├── features/
│   ├── intelligence/
│   │   ├── today/
│   │   ├── smart-feed/
│   │   │   ├── personal/
│   │   │   ├── collective/
│   │   │   └── activity/
│   │   ├── search/
│   │   └── library/
│   ├── capture/smart-notes/
│   ├── connect/
│   │   ├── smart-share/
│   │   ├── smart-lists/
│   │   ├── smart-spaces/
│   │   ├── contacts/
│   │   └── smart-mail/
│   ├── understand/
│   │   ├── reports/
│   │   ├── smart-ledger/
│   │   ├── evidence/
│   │   └── activity/
│   ├── learn/
│   │   ├── dream/
│   │   └── adaptive-learning/
│   ├── play/naya-play/
│   └── settings/
├── identity/
├── intelligence/
│   ├── models/
│   ├── projections/
│   ├── retrieval/
│   └── permissions/
├── services/
│   ├── naya/
│   ├── supabase/
│   ├── persistence/
│   ├── activity/
│   └── ledger/
├── contracts/
├── data/
├── public/
├── styles/
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── acceptance/
│   └── parity/
├── scripts/
├── docs/
├── index.html
├── identity.html
├── package.json
├── package-lock.json
├── vite.config.ts
├── wrangler.jsonc
├── worker.js
└── ARCHITECTURE-MAP.md
```

### Current implementation rule

The tree above is the product architecture. Existing src/* remains the implementation lane until a feature is actually migrated. Do not create duplicate top-level implementations just to make directory names match the diagram.
The correct evolution is: existing canonical implementation → feature-owned modules → shared contracts/services → verified retirement of old code.

## Causal data model

```text
HUMAN → HUB UI → GOVERNED CAPABILITY → NAYAPOWER / GOVERNANCE → CANONICAL SERVICE + SUPABASE → RECEIPT / EVIDENCE / LEARNING → RETRIEVAL → HUB PROJECTION → HUMAN UNDERSTANDING / ACTION → ACTIVITY + SMART LEDGER
```

Supabase is persistence and governed service infrastructure, not a copy of the filesystem and not a second Hub implementation.

## Visual quality contract

The current index.html establishes the minimum quality bar for:
- physical, tactile buttons with depth and responsive motion;
- restrained black/white/deep-purple visual system;
- clear hierarchy and generous spatial rhythm;
- intelligent blocks that make information easier to understand;
- Smart Feed modes that feel like one intelligence system, not three separate products;
- high-quality iconography and semantic visual cues;
- responsive desktop/mobile behavior;
- persistent mission/context surfaces;
- meaningful empty, loading, blocked, and verified states;
- no fake success and no fabricated intelligence.

Future visual work should improve this baseline rather than flatten, replace, or regress it.

## Retirement rule

The following are not current Hub implementations and must not return as deployable sources:
- NAYANET/E02-INTELLIGENT-HUB
- NAYANET/E02-INTELLIGENT-HUB-AAA
- NAYANET/E02-INTELLIGENT-HUB-CLOUDFLARE
- NAYANET/E03-INTELLIGENT-HUB

Historical evidence may live in governance/activity records, but historical Hub code is not an implementation authority.

## Release contract

A release is valid only when:
1. NAYANET/HUB builds without reading Hub-specific files from parent directories.
2. dist/ is generated from that build and contains the canonical runtime assets.
3. The Cloudflare Worker deploys the generated dist/ from the Hub configuration.
4. The live root serves the exact built index.html bytes.
5. The live runtime assets correspond to the same source commit.
6. Browser acceptance proves the canonical shell, Smart Feed modes, mission bar, feature surfaces, and responsive states.
7. A release receipt records source commit, artifact hash, Worker, and verification result.

Unknown is not success. Blocked is not pass.