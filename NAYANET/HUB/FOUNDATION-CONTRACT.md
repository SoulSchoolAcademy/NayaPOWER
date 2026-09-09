# NayaNET Intelligent Hub — Canonical Source + Design Token + Foundation Contract

**Status:** FOUNDATION CONTRACT — FORWARD AUTHORITY
**Version:** 1.0
**North Star:** INTELLIGENCE MADE VISIBLE.
**Mission:** CAPTURE → DISTILL → ORGANIZE → REMEMBER → FIND → COMPOUND.

## 1. Authority

This contract is the implementation boundary for the new NayaNET Intelligent Hub. Historical Hub files remain reference-only and are not imported or executed by the new application. Vercel is excluded. The established Cloudflare Worker `aged-art-7c12` is the current production destination, subject to independent runtime verification on release.

## 2. Canonical source boundary

All new Hub application source belongs under:

`NAYANET/HUB/`

No runtime source may be sourced from historical Hub HTML/JS. No second application, renderer, shell, navigation authority, or Smart Feed renderer may compete with this application.

## 3. Exact source tree

```text
NAYANET/HUB/
├── FOUNDATION-CONTRACT.md
├── package.json
├── tsconfig.json
├── vite.config.ts
├── index.html
├── src/
│   ├── main.tsx
│   ├── app/
│   │   ├── App.tsx
│   │   ├── routes.ts
│   │   └── AppShell.tsx
│   ├── components/
│   │   ├── shell/
│   │   ├── navigation/
│   │   ├── intelligence/
│   │   ├── controls/
│   │   └── surfaces/
│   ├── intelligence/
│   │   ├── types.ts
│   │   ├── event.ts
│   │   ├── block.ts
│   │   └── feed.ts
│   ├── identity/
│   │   ├── types.ts
│   │   └── session.ts
│   ├── data/
│   │   ├── repositories/
│   │   └── adapters/
│   ├── navigation/
│   │   └── navigation.ts
│   ├── styles/
│   │   ├── tokens.css
│   │   ├── globals.css
│   │   └── responsive.css
│   ├── assets/
│   └── verification/
│       └── contracts/
└── public/
    └── assets/
```

The tree defines ownership; folders are not permission to create competing implementations. A component has one owner and one rendering authority.

## 4. Application entry

`NAYANET/HUB/index.html` is the document entry point.

`NAYANET/HUB/src/main.tsx` is the sole JavaScript application entry point.

`src/app/App.tsx` owns application composition.

`src/app/AppShell.tsx` owns the permanent shell. Room components render inside the shell; rooms do not create alternate shells.

## 5. Component ownership

**AppShell:** identity context, top system context, desktop left navigation, mobile navigation, workspace outlet, system/status layer.

**Navigation:** one route registry and one navigation presentation. No room defines its own global navigation.

**Intelligence:** Intelligent Event normalization, Smart Feed lenses, and the single Intelligent Block renderer.

**Controls:** canonical buttons, search/Ask Naya, lens control, filters, utility actions.

**Surfaces:** room surfaces, intelligence objects, notes, evidence, metrics, communication and system surfaces. All inherit the same material/design tokens.

## 6. Data/model ownership

Source-of-truth models live in `src/intelligence`, `src/identity`, and `src/data`. Presentation components may consume models but may not redefine them.

Persistence belongs behind repository interfaces. UI state is not authoritative persistence.

## 7. Routing contract

| Route | Purpose |
|---|---|
| `/` | Home / orientation chamber |
| `/feed` | Smart Feed |
| `/notes` | Smart Notes |
| `/today` | Intelligence Today |
| `/reports` | Reports |
| `/library` | Intelligence Library |
| `/collective` | Collective Intelligence |
| `/evidence` | Evidence |
| `/connections` | Connections |
| `/mail` | Smart Mail |
| `/space` | Smart Space |
| `/settings` | Settings |

Navigation must support direct entry, refresh, browser back/forward, and unknown-route handling without creating alternate application roots.

## 8. Identity/session interface

The application consumes an identity context with:

```text
user_id
session_id
display_name
smart_name
smart_alias
permissions
privacy_state
```

Identity authority is backend/authentication-derived. Browser storage may cache non-authoritative continuity only. The Hub must never treat arbitrary local state as the identity database.

## 9. Intelligent Event schema

```text
IntelligentEvent {
  event_id
  user_id
  created_at
  updated_at
  source { type, id?, label? }
  human_input { raw, captured_at }
  context { topic?, tags?, location?, related_event_ids? }
  naya_interpretation { observation?, interpretation?, recommendation?, uncertainty? }
  machine_evidence { items[], verification_state }
  weaver_synthesis { summary?, relationships? }
  lesson { text?, retained? }
  meaning { text?, significance? }
  action { text?, status?, due_at? }
  relationships { event_ids[], connection_ids[], space_ids[] }
  privacy { visibility, consent_state }
  trust { level, evidence_ids[] }
  status
}
```

`human_input` is immutable historical source. Derived fields are explicitly derived. Missing layers remain absent; no renderer fabricates them.

## 10. Intelligent Block contract

The single canonical renderer receives one Intelligent Event and produces one intelligent object. Its progressive structure is:

`IDENTITY → NUTSHELL → PERSPECTIVES → WEAVER → LESSON → MEANING → ACTION`

Perspectives may include `WISDOM`, `HUMAN`, `CHILD`, `GRANDMA`, `NAYA`, `MACHINE`, and `WEAVER`. Layer presence is data-driven. The renderer never invents missing intelligence.

The visual object uses one coherent material surface and intelligence spine; perspectives are not rendered as a generic card wall.

## 11. Smart Feed contract

Smart Feed is one renderer with three lenses:

- **PERSONAL** — intelligence the user owns or is permitted to see personally.
- **COLLECTIVE** — consented shared intelligence within the user's permitted collective boundary.
- **ACTIVITY** — network activity relevant to the user's intelligence context, including events such as Smart Space requests and other meaningful changes.

The lenses are views over the same intelligence graph, not separate feeds or data stores.

Feed ordering is derived from relevance, recency, importance, unfinished action, relationship, learning value, newness, trust, and user intent. The first vertical slice may use deterministic local fixtures, but must preserve the production data contract and clearly mark fixture status.

## 12. Design tokens

### Typography

- UI/system: `Inter, ui-sans-serif, system-ui, sans-serif`
- Display emphasis: same family with weight variation; no decorative display dependency.
- Body: 15–17px, readable line height 1.45–1.65.
- Labels: 11–13px, tracked uppercase only where semantic hierarchy requires it.
- Primary headings: 28–42px desktop; responsive reduction without loss of hierarchy.

### Spacing

Base unit: 4px.

Canonical scale: `4, 8, 12, 16, 20, 24, 32, 40, 48, 64`.

### Radii

- control: 10px
- surface: 18px
- major intelligence object: 26–30px
- pill: 999px

Radii must communicate hierarchy, not decoration.

### Semantic colors

- Obsidian base: `#07070A`
- Obsidian surface: `#0D0D12`
- Elevated surface: `#13131B`
- Purple intelligence: `#875CFF`
- Human magenta: `#FF4FD8`
- Machine sapphire: `#4D8DFF`
- Verified green: `#55E39A`
- Significance gold: `#E8C766`
- Primary text: `#FFFFFF`
- Secondary text: `#B8B8C7`
- Quiet text: `#777789`
- Structural border: `rgba(255,255,255,.10)`
- Focus: `#B89CFF`

Semantic colors must not become rainbow decoration.

### Borders / illumination / depth

Major surfaces use restrained structural borders, a subtle top/edge highlight, controlled radial illumination, and deep shadow. Glow is reserved for focus/intelligence/state. No glassmorphism.

### Button states

Canonical button families: `PRIMARY`, `SECONDARY`, `UTILITY`, `INTELLIGENCE_ACTION`, `STATE`.

Every family defines: `default`, `hover`, `focus`, `active`, `disabled`, `loading`, `success`.

Buttons communicate hierarchy through size, weight, spacing, materiality and state first; color is supporting semantics.

### Surface families

`ROOM_SURFACE`, `INTELLIGENCE_OBJECT`, `NOTE_SURFACE`, `EVIDENCE_SURFACE`, `METRIC_SURFACE`, `COMMUNICATION_SURFACE`, `SYSTEM_SURFACE`.

## 13. Desktop shell contract

Desktop composition is:

`TOP SYSTEM CONTEXT + QUIET LEFT NAVIGATION + FULL INTELLIGENCE WORKSPACE + SYSTEM/STATUS LAYER`.

There is no permanent right sidebar. The workspace receives the dominant visual width. Existing proven button/board design DNA is preserved through extraction and tokenization rather than invented anew.

## 14. Mobile shell contract

Mobile is an intentional composition, not compressed desktop:

`COMPACT TOP CONTEXT + INTELLIGENCE WORKSPACE + INTENTIONAL BOTTOM NAVIGATION`.

No permanent left or right sidebar. Primary intelligence, Ask Naya, capture and action remain dominant. Touch targets and progressive disclosure are explicit.

## 15. Cloudflare production contract

Production target: Cloudflare only.

Current established Worker destination: `aged-art-7c12.nayanet.workers.dev`.

The new release mechanism must package `NAYANET/HUB/` into an immutable artifact and deploy it to the established Worker architecture. The application source remains in `NAYANET/HUB/`; Cloudflare is deployment/runtime, not source authority.

Release chain:

`SOURCE → STATIC ANALYSIS → CONTRACT TESTS → BUILD → ARTIFACT INSPECTION → CLOUDFLARE DEPLOY → EXACT PUBLIC URL → HTTP OBSERVATION → DOM/ASSET CHECK → VISUAL CHECK → INTERACTION CHECK → MOBILE CHECK → RELEASE LOCK`

No Vercel deployment is permitted.

## 16. Verification gates

A stage cannot advance until its gate passes:

1. **Source gate:** one canonical source boundary; no historical imports; no competing renderer.
2. **Contract gate:** models, routes, identity and visual tokens conform to this contract.
3. **Build gate:** clean build; static analysis; no broken imports.
4. **Artifact gate:** generated artifact inspected and traced back to source.
5. **Deployment gate:** exact Cloudflare Worker receives the artifact.
6. **Runtime gate:** exact public URL independently observed.
7. **Interaction gate:** navigation, controls, feed lens and key actions work.
8. **Persistence gate:** authoritative persistence is tested where applicable.
9. **Responsive gate:** desktop/tablet/mobile/small mobile checked.
10. **Accessibility gate:** keyboard, focus, labels, contrast, reduced motion and target sizing checked.
11. **Visual gate:** actual public screen compared against intended design system.
12. **Lock gate:** evidence and release identity recorded in the project activity feed.

## 17. First buildable vertical slice

The first slice is intentionally narrow but production-shaped:

`AUTHENTICATED IDENTITY CONTEXT → APP SHELL → HOME → ASK NAYA/SEARCH ENTRANCE → FEED LENS CONTROL → ONE REALISTIC INTELLIGENT EVENT → ONE CANONICAL INTELLIGENT BLOCK → DESKTOP + MOBILE → CLOUDFLARE DEPLOY → INDEPENDENT VERIFICATION`

It must prove the architecture before additional rooms are built. It must include no fake secondary rooms, no legacy renderer, no right sidebar, and no second feed implementation.

## 18. Explicitly protected

- Historical files remain untouched as reference.
- Vercel remains excluded.
- No permanent right sidebar.
- No competing shell/navigation/feed/block renderers.
- Human source remains distinct from Naya-derived intelligence and Machine evidence.
- Privacy boundaries remain explicit.
- Proven button/board/material design DNA is preserved and elevated rather than reinvented.
- Source-to-runtime integrity must be independently proven.
- No fake intelligence.

## 19. Execution law

`DEFINE → INSPECT → EXTRACT → RECONCILE → PRESERVE → ELEVATE → BUILD`

No implementation begins outside this boundary. Once implementation begins, each vertical slice follows:

`DEFINE → BUILD → LOOK → CLICK → TEST → PERSIST → MOBILE → VERIFY → LOCK → NEXT`.
