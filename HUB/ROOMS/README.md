# 🔱 NayaNET Intelligent Hub — Room System

**Status:** FUNCTIONAL SPECIFICATION V1 — proposed canonical subordinate contract  
**Authority:** Shawn Vibert, Human Director  
**Parent contracts:** `HUB/PROJECT-INTELLIGENCE.md` + `HUB/DESIGN-CONTRACT.md`  
**Implementation owner:** Issue #1270  
**Coordination:** Issue #554

## The idea

The Hub is not one giant dashboard. It is **eleven intelligent environments inside one living system**.

Each room is a masterpiece with its own purpose, visual identity, signature interaction and real causal function — while sharing one shell, one intelligence substrate, one truth model and one Naya.

A person should feel that they are entering a different instrument, not opening another recolored card page.

## The 11 primary rooms

| Room | Human metaphor | Core question | Signature experience |
|---|---|---|---|
| Smart Feed | **The game** | What is happening now? | Live intelligence stream |
| Your Intelligence Today | **The highlight reel** | What mattered today? | Beautiful daily story / snapshot |
| Your Reports | **The film room** | What does it mean over time? | Synthesis, trends, decisions |
| Intelligent Library | **The vault** | What do we know? | Searchable intelligence archive |
| Smart Connect | **The portal bay** | How can people/systems connect? | Governed doors into one intelligence |
| Smart Ledger | **The black box / proof room** | What happened and what proves it? | Receipts, authority, evidence, outcomes |
| Your Connections | **The constellation** | Who/what am I connected to? | Governed relationship map |
| Smart Lists | **The mission table** | What am I tracking or organizing? | Living collections powered by intelligence |
| Smart Mail | **The signal room** | What communication matters? | Intelligent message triage and action |
| Smart Spaces | **The worlds** | What context am I inside? | Context environments for projects/people/life |
| Settings | **The control deck** | How should NayaNET work for me? | Identity, privacy, preferences, trust, system controls |

## Universal capabilities — not extra primary rooms

These should be available throughout the Hub:

- **Search Intelligence** — global retrieval with provenance.
- **Ask Naya** — interpretation in current context.
- **Smart Note / Capture** — capture from anywhere; not required to occupy a permanent primary rail slot.
- **Save / Favorite / Add to List** — organize canonical intelligence.
- **Inspect Source / Evidence** — trust and provenance.
- **Space context** — current context is visible and switchable.
- **Truth state** — LOADING / EMPTY / READY / BLOCKED / UNAUTHORIZED / NOT_VERIFIED / VERIFIED / ERROR / OFFLINE / UNKNOWN / DISABLED.

### IA reconciliation note

Open PR #1278 currently adds **Smart Notes** and **System** as primary rail rooms, producing 13 rooms. The canonical product model remains 11 primary rooms until deliberately changed.

Recommended placement:
- **Smart Notes** = universal capture capability + optional focused capture view.
- **System** = advanced diagnostics / status under Settings or another explicitly secondary surface.

Do not silently expand the primary rail.

## Room design grammar

Every room gets a unique composition, but every room must answer in the first few seconds:

1. **Where am I?**
2. **What matters here?**
3. **What can I do next?**

Each room specifies:
- human promise;
- signature visual concept;
- information hierarchy;
- primary instrument;
- controls;
- data/runtime owner;
- cross-room handoffs;
- states;
- mobile behavior;
- evidence/authority boundary;
- acceptance proof.

## Cross-room flow

The rooms are not isolated apps.

```
SMART FEED  → raw/current flow
     ↓
TODAY       → daily highlights
     ↓
REPORTS     → cross-time meaning
     ↓
LIBRARY     → durable retrieval

CONNECT     → channels into the intelligence
CONNECTIONS → governed relationships created/observed through those channels
SPACES      → context boundary for people + intelligence + activity
MAIL        → communications entering/leaving those contexts
LISTS       → human-curated/actionable organization

LEDGER      → proof layer beneath all consequential activity
SETTINGS    → human control over identity/privacy/preferences/runtime relationship
```

Every room may hand an object to another room without copying canonical truth. Example: Feed item → Add to List; Mail → Capture Smart Note; Today highlight → Open in Feed; Report insight → Open evidence in Ledger; Connection → Open shared Space.

## Experience law

**One shell. Eleven masterpieces. One Naya. One governed intelligence substrate.**

The room spec may change layout. It may not create a second brain, second authority system, second ledger, or second canonical data store.

## Read order

1. `ROOM-FUNCTIONAL-CONTRACT-V1.md`
2. the relevant room spec
3. `ROOMS-MACHINE-V1.json`
4. parent Hub build/design contracts
5. current runtime evidence

## Exactly one next action

Use these room contracts to reconcile the app foundation and then implement **Your Intelligence Today** first as the full end-to-end exemplar: identity → canonical retrieval → highlights → provenance → Naya interpretation → actions → honest refusal/error states.
