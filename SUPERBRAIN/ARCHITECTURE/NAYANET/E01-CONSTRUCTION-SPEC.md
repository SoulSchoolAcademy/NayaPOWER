# 🔱 NAYANET — E01 CONSTRUCTION SPECIFICATION

**Status:** CANONICAL E01 CONSTRUCTION AUTHORITY
**Date:** 2026-08-30
**Version:** 1.0

## Mission

Build the first room of NayaNET as a complete, extraordinary static-first experience:

**WELCOME → NAYA PRESENCE → FREE NAYANET IDENTITY → SMART NAME / SMART LINK → PERSONAL INTELLIGENT HOME → NEXT ACTION**

E01 must feel like receiving the keys to an extraordinary intelligence machine:

> **Here you go. Drive.**

It is not a dashboard, sales page, fake AI, fake account system, or miniature version of the entire network.

## 1. Human journey

### Arrival
The visitor immediately sees Naya, the Living Sun, a concise promise, and one dominant action: **Create My NayaNET**.

### Identity
The visitor enters only a name for the static experience. The browser creates a local identity representation. The UI clearly explains that this is a local/static identity preview until durable account infrastructure is connected.

### Reveal
The experience transforms from welcome into a personal intelligent home. The user receives a Smart Name and Smart Link representation and sees the Toolbox/Command Station.

### Choice
Naya presents two high-value next paths: **Start the Five-Day Challenge** and **Experience Naya Power**. Secondary destinations explain the future Hub, Superbrain, Collective and Network without pretending those services are live.

### Continuity
The name and E01 progress persist locally when browser storage is available. No secret or sensitive credential is stored.

## 2. Screen architecture

### Stage A — The Arrival Field
- full-width deep-space canvas;
- subtle radial energy field;
- NayaNET wordmark/identity;
- Living Sun centered in the visual hierarchy;
- Naya greeting;
- one-sentence value proposition;
- primary CTA;
- tiny trust statement: no email required to begin.

### Stage B — Identity Gate
- focused name input;
- example Smart Name preview;
- live Smart Link preview;
- validation;
- one action: **Enter NayaNET**;
- accessible error/help state.

### Stage C — Welcome Home
- personalized greeting;
- Smart Name badge;
- Smart Link card with copy affordance;
- Naya presence;
- command station arranged as meaningful orbital/tool nodes rather than generic metric cards;
- Five-Day Challenge and Naya Power highlighted as primary destinations.

### Stage D — Naya Guidance
Naya explains the two strongest next actions in plain language and recommends one based on whether the user is new or returning.

### Stage E — Future Horizon
A restrained glimpse of the larger network: Superbrain, Collective, Connect, Smart Mail and Daily Intelligence. Future capabilities are visibly labeled as future/not yet connected.

## 3. Living Sun specification

The Sun is an actual interaction/state primitive.

Layers:
1. Ambient field
2. Outer orbital ring
3. Energy ring
4. Intelligence ring
5. Core
6. Naya presence

States:
- RESTING: slow breathing;
- ATTENTION: increased luminosity;
- LISTENING: receiving/opening ring motion;
- THINKING: directional orbit;
- SPEAKING: synchronized calm pulse;
- PLAYING: controlled playback ring;
- SUCCESS: outward completion wave;
- WARNING: semantic caution state + text;
- ERROR: clear error state + recovery;
- DISCONNECTED: muted state + truthful explanation.

Every state has an accessible text label. `prefers-reduced-motion` disables decorative movement while preserving state communication.

## 4. Interaction contract

Every primary control has a deterministic result.

- Create My NayaNET → validate → create local identity → success → Home.
- Meet Naya → Naya panel opens and Sun enters SPEAKING/ATTENTION.
- Sun → state changes and feedback; never decorative-only.
- Smart Link copy → copies if permitted; otherwise displays manual-copy fallback.
- Five-Day Challenge → opens E05 destination if present; otherwise opens a truthful continuation panel.
- Naya Power → opens E02 destination if present; otherwise shows activation explanation.
- Future tool → opens a clear future-state panel; never a dead button.
- Reset local identity → confirmation → clears local E01 state.

## 5. Static-first engineering

Required artifact:

```text
E01/
  index.html
  e01.css
  e01.js
  README.md
  assets/
  data/
```

No Node runtime, build system, Wrangler, framework, server, database, or API is required for the baseline experience.

The block must be independently deployable and embeddable.

CSS and JS are namespaced. No parent DOM assumptions. No cross-frame messaging in E01 unless a real requirement is later approved.

## 6. Data/state

Local state may contain only non-sensitive E01 experience data:

- display name;
- generated Smart Name representation;
- generated Smart Link representation;
- first-visit/returning state;
- completed E01 milestones.

The static block must never claim that this local state is a production authenticated account or Superbrain.

## 7. Smart identity model

For E01 demonstration purposes, the visitor's name is transformed into a normalized Smart Name representation. The Smart Link is presented as the future persistent NayaNET identity URL concept.

Example presentation:

`Shawn` → `shawn.nayanet`

The exact production routing/domain remains a future platform decision and must not be falsely represented as provisioned.

## 8. Visual direction

Foundation: near-black/deep-space.

Primary type: white.

Identity: Naya purple.

Energy: magenta.

Intelligence: electric blue.

Growth: green.

Insight: gold/yellow.

Use circles, concentric rings, orbital paths, nodes, radial gradients, luminous cores, glass/depth surfaces, and restrained motion. Avoid generic SaaS card grids.

Official Naya assets are the preferred identity references. Use the locked assets supplied in `03A-OFFICIAL-NAYA-BRAND-ASSET-LOCK.md`; do not invent substitute Naya portraits.

## 9. Mobile

Mobile is a first-class composition. The order remains:

**Naya → action → value → choices.**

No hover-dependent interaction. Minimum comfortable touch targets. No horizontal overflow. Sun scales without losing its geometry. Sections remain vertically composable for Groove.

## 10. Groove

E01 is designed to be hosted at a stable Cloudflare URL and embedded into Groove using an iframe after independent deployment.

The block must not depend on parent-page JavaScript. Navigation stays inside E01 by default. Future `postMessage` communication requires a versioned, origin-validated contract.

The artifact must tolerate narrow iframe widths and variable heights.

## 11. Failure design

Asset failure → preserve layout and use identity fallback.

Storage failure → continue in current session and explain persistence limitation.

Clipboard failure → show the Smart Link for manual copying.

Media/speech failure → retain text experience.

Future service unavailable → truthful unavailable/future state.

Unknown route → purposeful continuation, never blank/dead state.

## 12. Accessibility

Semantic HTML, keyboard navigation, visible focus, labels, logical headings, live regions where state changes, sufficient contrast, reduced motion, non-color state communication, accessible Sun status, and touch-safe controls.

## 13. Performance

No dependencies. Critical CSS/JS local. Lazy-load optional imagery/media. Avoid layout shifts. Keep animation inexpensive. The first meaningful interaction must work before secondary assets finish loading.

## 14. Acceptance criteria

E01 passes only when:

- first viewport is immediately understandable;
- official Naya identity is represented correctly;
- Living Sun communicates state;
- name creation works;
- Smart Name/Link are generated and usable as local representations;
- Home transformation works;
- every visible control has a meaningful outcome;
- future functionality is truthful;
- mobile works at 320–1280px;
- keyboard and reduced-motion behavior work;
- storage and clipboard failure paths work;
- no secrets exist in client files;
- ZIP contains only static deployable material;
- Cloudflare static upload succeeds;
- deployed URL is human-tested;
- Groove iframe is separately verified.

## 15. Evidence ladder

Record separately:

**SPECIFIED → IMPLEMENTED → TESTED → DEPLOYED → HUMAN-VERIFIED → GROOVE-VERIFIED → FROZEN**

No state may be claimed without evidence.

## 16. Next blocks

E01 ends by making the next door obvious:

E02 Power → E03 Powercast → E04 Ask → E05 Challenge → E06 Hub → E07 Superbrain → E08 Collective/Network → E09 Activation.

E01 must not absorb these blocks; it must establish the identity and momentum that make them desirable.
