# 🔱 Naya Power — Cloudflare Application Execution Directive

**STATUS:** CANONICAL PRODUCT / BUILD LOCK
**DATE:** 2026-08-30
**REPOSITORY:** `SoulSchoolAcademy/NayaPOWER`
**CURRENT HEAD AT LOCK:** `7df2ebea51102ed43f32a635e8d9b6c9fbcbd6e2`

## Mission

Build the real Naya Power customer application for Cloudflare as an app-like intelligence environment, not a generic SaaS dashboard and not a conventional sales page.

## North Star

> **SEE NAYA → LISTEN → ASK → EXPERIENCE → UNDERSTAND → FIVE-DAY CHALLENGE → ACTIVATE**

A human should open the application and immediately understand that NayaPOWER is different because they can experience Naya rather than merely read claims about her.

## Product lock

The product is **Naya Power Player**, the customer-facing experiential layer of NayaPOWER.

The Player must include:

- premium persistent application shell;
- Shawn + Naya opening Powercast;
- Living Sun as the central interaction surface;
- Living Sun states: idle, listening, thinking, speaking, teaching, Powercast;
- selectable Powercasts inside the Player;
- Ask Naya with text input;
- voice-first response presentation where technically available;
- dictation/microphone where technically available;
- intentional text reveal rather than text-dominant UX;
- playable Five-Day Challenge;
- intelligence ecosystem exploration;
- clear activation path into Intelligent Hub.

## Experience law

The interface must feel:

**alive · premium · intelligent · simple · immersive · fast · trustworthy · app-like**

Use the strongest lessons from Pro Max Player and MAXIS E01–E09, but evolve them from media-player UX into intelligence-player UX.

## Cloudflare architecture lock

Use **Cloudflare Workers Static Assets** for the application deployment substrate.

```text
GitHub
  ↓ canonical source
Cloudflare Worker
  ├── static Naya Power Player assets
  └── edge API
```

The deployment artifact should remain intentionally simple. Do not add infrastructure complexity unless the product requires it.

**GitHub Actions is intentionally paused. Do not retry, dispatch, or troubleshoot it.**

## Intelligent Hub boundary

The Intelligent Hub is the control plane for sovereign Superbrain connections. Its canonical law is:

> **CONNECT THE SUPERBRAIN. DO NOT ABSORB THE SUPERBRAIN.**

The Player may expose the Hub experience, but it MUST NOT fake provider/runtime capabilities.

The Hub must preserve:

- least-privilege provider access;
- explicit capability grants;
- connection consent separate from contribution consent;
- human approval before wisdom publication;
- minimum-necessary contribution intake;
- privacy/quality gates;
- identity-free Collective Intelligence Events;
- revocation;
- canonical Note Event authority.

A GitHub fork is not a synchronization mechanism. A pasted personal GitHub password/token is not the normal connection path.

## Truth boundary

Always distinguish:

`DESIGNED → IMPLEMENTED → TESTED → VERIFIED → DEPLOYED → PRODUCTION-PROVEN`

Never claim live Superbrain grounding, production GitHub App connection, canonical event publication, or production LLM capability until executable evidence exists.

## Build order

### P0 — Player
1. application shell;
2. Living Sun;
3. Powercast;
4. Ask Naya;
5. Five-Day Challenge;
6. ecosystem;
7. activation CTA;
8. Cloudflare deployment proof.

### P1 — Intelligent Hub runtime
1. production GitHub App adapter;
2. selected Superbrain resource binding;
3. durable connection/consent state;
4. wisdom contribution flow;
5. value extraction/generalization;
6. privacy/quality gate;
7. Collective Intelligence Event publication;
8. Intelligence Feed retrieval;
9. revocation and correction/supersession.

### P2 — Production intelligence
1. authenticated user/session layer;
2. authorized Naya runtime/LLM;
3. canonical event-store integration;
4. production observability;
5. end-to-end runtime proof.

## Verification law

For every substantive build:

**BUILD → VIEW → WHY IS THIS NOT A 10? → REPAIR → VERIFY → DOCUMENT → COMPOUND**

Minimum browser targets:

`320, 360, 375, 390, 414, 480, 600, 768, 900, 1024, 1280`

Verify:

- `/`;
- `/api/health`;
- `/api/config`;
- `/api/ask`;
- invalid input handling;
- voice capability fallback;
- Five-Day Challenge persistence;
- Hub truth states;
- mobile experience;
- no unsupported capability is represented as live.

## Delivery standard

The Cloudflare application package must be self-contained and handoff-ready:

- complete source;
- Cloudflare configuration;
- Worker/API;
- complete UI;
- test harness;
- deployment instructions;
- architecture documentation;
- execution directive;
- explicit verified/unverified capability list.

## Protected architecture

- Human owns the destination; Naya helps navigate reality.
- Canonical Note Event remains the memory authority.
- Vectors and projections are derived, never authoritative.
- The Running Feed is orientation, not a competing memory store.
- Collective intelligence receives reusable wisdom, not private life.
- IMPLEMENTED ≠ TESTED ≠ VERIFIED ≠ RUNTIME-PROVEN ≠ PRODUCTION-PROVEN.

## Success condition

A real human can open the Cloudflare application, experience Naya, receive useful grounded information, progress through the first activation journey, understand the sovereignty/privacy model, and know exactly what to do next.

## Final operating command

**READ → UNDERSTAND → LEAD → BUILD → VERIFY → REPAIR → DOCUMENT → PACKAGE → PASS THE TORCH.**
