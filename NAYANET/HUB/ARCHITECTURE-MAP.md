# NayaNET Hub — Canonical AAA Architecture

## North Star

NAYANET/HUB is the single human-facing Hub implementation boundary.

The product chain is:

Human → NayaPOWER governance → Naya → Superbrain → Intelligent Event → Intelligent Block → Smart Feed → Smart Doors → governed capabilities → persistence/index → retrieval → verification → learning → compounding → Superbrain.

The Hub makes this enormous system simple, beautiful, obvious, private, and actionable. The current index.html is the visual quality floor/reference, not the architecture or ceiling.

## Canonical Hub tree

```
NAYANET/HUB/
├── app/
│   ├── App.tsx
│   ├── main.tsx
│   ├── shell/
│   │   └── AppShell.tsx
│   └── routing/
│       ├── HubRouter.tsx
│       └── routes.ts
├── features/
│   ├── capture/
│   │   └── smart-notes/
│   ├── intelligence/
│   │   └── reports/
│   ├── connect/
│   │   ├── smart-share/
│   │   ├── smart-lists/
│   │   ├── smart-spaces/
│   │   ├── smart-mail/
│   │   └── contacts/
│   ├── proof/
│   ├── learn/
│   │   └── dream/
│   ├── naya/
│   │   └── play/
│   └── system/
│       └── settings/
├── identity/
├── intelligence/
│   ├── retrieval/
│   ├── SmartFeedBoard.tsx
│   ├── cognition.ts
│   ├── actionPersistenceBridge.ts
│   ├── compoundIntelligence.ts
│   └── types.ts
├── services/
│   └── config/
├── styles/
├── public/
├── scripts/
├── docs/
├── index.html
├── package.json
├── package-lock.json
├── tsconfig.json
├── vite.config.ts
├── wrangler.jsonc
├── worker.js
└── ARCHITECTURE-MAP.md
```

## Ownership rules

- Human-facing product capabilities live under features/.
- App shell and navigation live under app/.
- Identity is isolated under identity/.
- Canonical event, Intelligent Block, Smart Feed, cognition, learning, and retrieval logic live under intelligence/.
- Runtime/config adapters live under services/.
- Visual implementation lives under styles/ and must have one intentional authority.
- public/ contains runtime assets only.
- scripts/ contains deterministic build and verification machinery.
- docs/ contains contracts, evidence, and retained historical knowledge; it is not an implementation authority.

## Canonical intelligence object

One occurrence becomes one Intelligent Event and one canonical Intelligent Block representation. Human, Naya, and machine perspectives are projections of that object rather than separate representations.

The object carries, as applicable:

SOURCE · IDENTITY · TIME · OWNER · AUTHORITY · TRUTH · PROVENANCE · CONTEXT · HUMAN MEANING · NAYA INTERPRETATION · MACHINE REPRESENTATION · LESSON · VALUE · ACTION · EVIDENCE · LIFECYCLE · INTEGRITY · PRIVACY · CONSENT · RELATIONSHIPS.

Human questions are:

What happened? What does it mean? Why does it matter? What can I do with it?

Machine questions are:

What is the event? Who owns it? What authority exists? What is proven? What is uncertain? What happened next?

## Smart Door grammar

Every consequential capability follows the same governed grammar:

SELECT/CAPTURE → AUTHORIZE → CREATE OR ACT → PERSIST → INDEX → PROJECT → EVIDENCE/RECEIPT → LEARN → COMPOUND.

Examples include Smart Note, Smart Share, Smart Mail, Smart Space, and Smart List.

## Release boundary

One source → one app boundary → one build → one artifact → one runtime.

Supabase is persistence/index and governed service infrastructure, not a second Hub tree.

Historical E02/E03 Hub generations are retired and are not deployable implementation authorities.

Unknown is not success. Blocked is not pass. No retry without new information.
