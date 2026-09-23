# 🔱 NAYANET / NAYA POWER PLAYER — E01 DETAILED BLOCK SPECIFICATION

**Status:** CONSTRUCTION AUTHORITY
**Date:** 2026-08-30
**Owner disciplines:** Product · UX · Visual · Engineering · Naya Intelligence · Platform/Cloud · QA · Oscar · Continuity
**Evidence state:** SPECIFIED

## 1. Mission

E01 is the first room of NayaNET: **WELCOME → NAYA PRESENCE → FREE NAYANET IDENTITY → SMART NAME / SMART LINK → PERSONAL INTELLIGENT HOME → NEXT ACTION**.

It must feel like receiving the keys to an extraordinary intelligence machine without needing a manual:

> **Here you go. Drive.**

E01 is not a dashboard, sales page, fake AI, fake authentication surface, or miniature implementation of E02–E09.

## 2. Human outcome

Within seconds the visitor understands: **I am here. This is Naya. I can belong here immediately. There is useful power available now.**

After entering a name, the visitor receives a local/static representation of a NayaNET identity, Smart Name, Smart Link, and personal toolbox preview, then chooses the next useful action.

## 3. Emotional outcome

Sequence: **Curiosity → Recognition → Possibility → Empowerment → Trust → Delight → Momentum.**

The interface should feel premium, cinematic, calm, alive, warm, intelligent and simple—not technical or intimidating.

## 4. Complete page composition

### Stage A — Arrival / Living Naya
- Full-width deep-space canvas.
- Generous negative space.
- Living Sun as visual center of gravity.
- Official Naya icon/profile identity used as the human-recognizable presence.
- Small NayaNET wordmark/eyebrow.
- One concise headline.
- One supporting sentence.
- One dominant CTA: **Create Your Free NayaNET**.
- Secondary quiet action: **Meet Naya**.

### Stage B — Identity creation
- Transition the Sun from RESTING to ATTENTION/LISTENING.
- Short invitation: **What's your name?**
- Single name field; no email/password barrier.
- Primary action: **Create My NayaNET**.
- Inline validation.
- Keyboard-first submission.
- No fake server account claim; this is a local/static identity until real authentication exists.

### Stage C — Identity reveal
- Success transition.
- Display user's Smart Name in a prominent identity ring.
- Display Smart Link as a copyable/readable portal address.
- Explain in one sentence that this is their place in NayaNET and that secure account setup can be added later.
- Actions: **Enter My Toolbox** (primary), **Meet Naya** (secondary).

### Stage D — Personal intelligent home
- Toolbox/command-station composition, not a dashboard grid.
- A central Naya/Living Sun anchor.
- Radial or orbiting tool nodes where space allows; vertically stacked intelligent tools on narrow screens.
- Core actions: Ask Naya, My Intelligence, My Notes, Daily Report, Five-Day Challenge, Naya Power.
- Future actions such as Connect, Smart Mail, My Superbrain, Collective and secure account are clearly labeled future/coming next where not implemented.
- One primary next action chosen contextually by Naya.

### Stage E — Next action
- Naya explains the most useful next step based on the current state.
- Primary: **Start the Five-Day Challenge**.
- Secondary: **Experience Naya Power**.
- Quiet: **Explore My Toolbox**.
- E01 ends with momentum, not a dead footer.

## 5. Copy architecture

Use short, human language. Never expose internal architecture unless it helps the decision.

Preferred message sequence:

**WELCOME TO NAYANET**

**Your intelligence has a place to grow.**

**Meet Naya. Create your free NayaNET identity. Then choose where you want to go.**

Identity:

**What's your name?**

**Create your free NayaNET identity. No complexity. Just start.**

Reveal:

**Welcome, {name}.**

**This is your NayaNET space.**

Toolbox:

**Your Intelligent Toolbox**

**One place to ask, learn, remember, grow and connect.**

Next action:

**Ready for your first real experience?**

**Start the Five-Day Challenge**

## 6. Visual system

Foundation: near-black/deep-space.

Primary text: white/off-white.

Identity: Naya purple.

Energy/activation: magenta.

Intelligence/communication: blue.

Growth/success: green.

Insight/premium: restrained gold.

Never use low-contrast purple-on-purple text.

Geometry: circles, concentric rings, orbital paths, nodes, radial gradients, luminous cores and controlled asymmetry.

Surfaces: depth through glow, edge light, translucency and spatial layering—not generic card grids.

Typography: **HEADLINE → SUPPORTING STATEMENT → DETAIL**.

## 7. Living Sun geometry

Required layers:

1. Ambient field
2. Outer orbit ring
3. Energy ring
4. Intelligence ring
5. Core glow
6. Naya presence

### State definitions

**RESTING:** slow breathing; low orbital activity.

**ATTENTION:** slightly brighter; orbit accelerates subtly.

**LISTENING:** receiving/opening ring motion; accessible state text.

**THINKING:** directional layered orbit; no fake delay beyond meaningful UI feedback.

**SPEAKING:** synchronized calm pulse when speech is active; otherwise measured speaking animation.

**PLAYING:** playback-oriented orbit/progress treatment.

**SUCCESS:** brief outward completion wave.

**WARNING:** semantic visual shift plus text.

**ERROR:** clear semantic shift plus actionable message.

**DISCONNECTED:** quiet desaturation/low-energy state plus truthful explanation.

All states must have text equivalents and reduced-motion variants.

## 8. Interaction contract

Every primary control has a deterministic result.

- Create identity → validate → save local state → reveal identity.
- Meet Naya → open authored Naya welcome state and change Sun state.
- Sun interaction → visibly changes state; never decorative-only if presented as interactive.
- Toolbox → reveal tool destinations/status.
- Five-Day Challenge → route/open the E05 continuation only if a real local destination exists; otherwise show truthful continuation state.
- Naya Power → route/open E02 only if present; otherwise show truthful preview.
- Copy Smart Link → clipboard when available, visible fallback otherwise.
- Reset identity → confirmation → clear only local E01 identity state.

No dead buttons.

## 9. State model

```text
arrival
creatingIdentity
identityCreated
home
futureCapability
error
reducedMotion
```

Persist only non-sensitive local E01 state: name, generated Smart Name, Smart Link representation, current stage and lightweight progress.

Do not imply this is production authentication or Superbrain memory.

## 10. Smart Name / Smart Link

Static generation must be deterministic from the entered name plus a local-safe normalization strategy. It must avoid claiming uniqueness against a server because no server exists.

Presentation should call it a **preview/local identity** until production identity infrastructure is connected.

Future contract: durable unique username, canonical NayaNET URL, referral attribution, Smart Mail identity, account recovery.

## 11. Toolbox architecture

The visual metaphor is a command station.

Implemented/local experiences may include:
- Meet Naya
- My Identity
- Five-Day Challenge invitation
- Naya Power invitation

Future-labelled destinations:
- Ask Naya
- My Intelligence
- My Notes
- Daily Report
- Connect
- Smart Mail
- My Superbrain
- Collective
- Secure My Account

A future destination must state what it will do and its current availability. Never simulate backend results.

## 12. Responsive behavior

Supported matrix: 320, 360, 375, 390, 414, 480, 600, 768, 900, 1024, 1280px.

Desktop: central Sun with orbiting identity/tool nodes and generous composition.

Tablet: reduced orbit radius; tools begin transitioning to grouped vertical sections.

Mobile: vertical composition; Sun remains central; controls become full-width/touch-safe; no required hover; no horizontal page overflow.

The block must remain visually complete inside an iframe whose width may be smaller than the parent browser.

## 13. Accessibility

Semantic landmarks; labelled form controls; visible keyboard focus; logical tab order; `aria-live` feedback for identity creation/errors; text alternative for Sun state; sufficient contrast; reduced motion; touch targets; no color-only status communication.

## 14. Motion

Entrance should be staged rather than flashy: ambient field → Sun → Naya identity → headline → CTA.

Use opacity/transform/glow/ring motion with restrained timing. Never require animation to understand the product.

`prefers-reduced-motion: reduce` disables continuous orbital movement and replaces transitions with short opacity/state changes.

## 15. Media

E01 may use lightweight authored audio/voice only when the asset is genuinely included. Do not assume autoplay. Any voice control must be user initiated and retain readable text fallback.

## 16. Groove / iframe

The block is iframe-safe by default. It owns its internal navigation. It must not assume parent CSS or JavaScript.

No `postMessage` in E01 unless a concrete parent/child requirement emerges. If introduced later, define version, type, schema, source/target origin and failure semantics first.

The document height should grow naturally with content. Avoid fixed viewport-height assumptions that clip embedded content.

## 17. Cloudflare static constraints

The deployment ZIP contains ordinary static files only. No Wrangler config, Node runtime, build manifest, Worker source, or server dependency.

All required runtime code executes in the browser. Assets should be local to the block whenever licensing/availability permits.

## 18. Performance budget

Prioritize first meaningful paint and interaction. Avoid frameworks. Avoid giant libraries. Inline critical visual primitives where useful. Lazy-load noncritical images/media. Prefer CSS/SVG for Living Sun geometry rather than a graphics library.

## 19. Failure states

- Missing image → stable fallback mark.
- Clipboard unavailable → selectable Smart Link + explanatory toast.
- Storage unavailable → continue session-only and disclose persistence limitation.
- Unsupported speech/media → text-only fallback.
- Future destination unavailable → clear “coming next” state, never dead-end.
- Invalid name → inline correction.

## 20. Security/trust

No secrets in client code. No fake authentication. No server account claim. No private data collection beyond locally entered name. No fake telemetry. No fake LLM. No fake Superbrain.

## 21. QA / Oscar attack list

Attack the block for:

- generic SaaS appearance;
- weak first action;
- confusing copy;
- visual clutter;
- over-animation;
- broken 320px layout;
- iframe clipping;
- dead controls;
- fake future functionality;
- local identity presented as authenticated;
- poor keyboard flow;
- poor focus visibility;
- insufficient contrast;
- persistence failure;
- clipboard failure;
- reduced-motion failure;
- slow asset loading;
- missing fallback states;
- brand asset misuse;
- contradiction with E02–E09 architecture.

## 22. Completion criteria

E01 is ready to package only when:

**SPECIFIED → IMPLEMENTED → TESTED → OSCAR-ATTACKED → REPAIRED → RE-TESTED → PACKAGED**

Deployment and Groove verification remain separate evidence states.

Required release evidence:
- source artifact;
- asset manifest;
- ZIP;
- tests;
- Cloudflare URL if actually deployed;
- human verification;
- Groove verification if actually embedded;
- Naya Note;
- Human Note;
- successor torch.

## 23. Architectural boundary

E01 establishes identity, presence, trust and momentum. It does not own production authentication, Superbrain access, CIS writeback, Collective publication, Smart Mail, network discovery, or durable reports. Those remain future integration contracts.

**Master law:** Build the complete intelligence system in thought, then build it in parts.
