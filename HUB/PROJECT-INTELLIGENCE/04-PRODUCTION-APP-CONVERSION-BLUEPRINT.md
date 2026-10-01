# 04 — Production App Conversion Blueprint

## Objective

Turn the current HTML concept into a maintainable production application **without losing the approved visual quality**.

Do not port the 843 KB file line-for-line. Extract its design system, information architecture, interaction semantics and useful behavior into clean components.

## 1. Preserve before rebuilding

Before implementation changes:

1. capture reference screenshots of Welcome, Identity and Hub;
2. capture hover/selected/pressed/focus states of key controls;
3. record desktop/tablet/mobile reference views;
4. inventory every left-rail destination;
5. inventory top ecosystem links;
6. inventory nine boards;
7. inventory all actions and runtime dependencies;
8. classify each item KEEP / IMPROVE / REPLACE / REMOVE;
9. record why;
10. define proof for replacements.

This creates a no-regression baseline.

## 2. Application architecture

Framework choice is secondary to preserving the existing canonical application seam. Do not create a parallel product if a canonical app owner already exists.

Recommended component responsibilities:

```
App
├─ Router
├─ DesignSystemProvider
├─ RuntimeProvider
├─ IdentityProvider
├─ AppShell
│  ├─ LeftRail
│  │  └─ NavButton
│  ├─ TopSystemBar
│  ├─ IntelligenceSearch
│  ├─ FeedModeTabs
│  ├─ MainWorkspace
│  └─ NayaCompanion
├─ Welcome
├─ Identity
└─ HubRoom
   ├─ RoomHeader
   ├─ IntelligenceBoard
   │  ├─ BoardJewel
   │  ├─ TruthState
   │  ├─ Nutshell
   │  ├─ IntelligenceLayer
   │  └─ ActionBar
   └─ RoomSpecificContent
```

## 3. Design-system primitives

Create reusable primitives instead of page-specific glow hacks:

- `PowerButton`;
- `NavButton`;
- `IntelligenceBoard`;
- `IntelligenceJewel`;
- `TruthBadge`;
- `EnergyPath / Progress`;
- `IdentityPortal`;
- `StatusIndicator`;
- `IntelligenceLayer`;
- `NayaPresence`.

All derive from shared tokens.

## 4. Data/runtime architecture

UI components never own canonical intelligence.

Use adapters/services that expose governed application operations, for example:

- current identity/session;
- search intelligence;
- load feed;
- load current intelligence;
- capture Smart Note;
- load reports;
- list library intelligence;
- list Smart Doors / connection state;
- load Ledger;
- list Connections;
- load/send Smart Mail;
- list Spaces;
- inspect settings/runtime state.

Every method must return explicit loading/empty/error/blocked/unknown states.

## 5. Navigation registry

Use one canonical machine-readable room registry.

The same registry should drive:

- left rail;
- route labels;
- theme color;
- icon identity;
- access/state handling;
- analytics/telemetry labels;
- tests.

Do not hand-code room names in five places.

Production name: **Smart Connect**, not Smart Share.

## 6. Migration sequence

### Phase A — baseline and tokens
- freeze reference screenshots;
- lock design tokens;
- lock room registry;
- lock route map.

### Phase B — App Shell
- router;
- left rail;
- top system bar;
- search;
- Naya companion boundary;
- responsive shell.

### Phase C — onboarding
- Welcome;
- Identity;
- successful transition into Hub;
- remove duplicate onboarding/auth experience.

### Phase D — first real room
Migrate **Your Intelligence Today** end-to-end because it forces identity, retrieval, truth state, current intelligence, interpretation and next actions to compose.

### Phase E — core retrieval rooms
- Smart Feed;
- Intelligent Library;
- Reports.

### Phase F — governed capability rooms
- Smart Connect / Smart Doors;
- Ledger;
- Connections;
- Mail;
- Spaces;
- Settings.

### Phase G — full board/action migration
Migrate the nine-board living-intelligence experience and real action paths.

## 7. Visual-regression law

A refactor cannot be called an improvement from source cleanliness alone.

For each milestone compare:

- composition;
- object depth;
- border/light precision;
- semantic spectrum;
- button tactility;
- icon craft;
- typography;
- hierarchy;
- readability;
- motion;
- responsive behavior.

If the clean app looks flatter/cheaper, the milestone FAILS.

## 8. Functional truth law

For every visible control define:

`CONTROL → INTENT → AUTHORITY → RUNTIME OPERATION → OBSERVATION → UI STATE → RECEIPT/EVIDENCE WHERE REQUIRED`

No dead controls.

If a capability is not implemented:
- do not fake it;
- show explicit unavailable/coming/blocked state as appropriate.

## 9. Testing stack

Minimum:

- component/unit tests;
- route tests;
- runtime-adapter contract tests;
- negative authority tests;
- loading/empty/error/blocked tests;
- keyboard/focus tests;
- reduced-motion tests;
- responsive visual snapshots;
- visual-regression screenshots;
- browser end-to-end journeys;
- production/runtime evidence where consequential.

## 10. Performance

Living depth must come from disciplined composition rather than uncontrolled DOM/CSS/animation weight.

Prefer:
- GPU-friendly transforms/opacity;
- bounded glow layers;
- lazy noncritical content;
- paginated/virtualized large feeds;
- image optimization;
- no permanent MutationObserver patchwork;
- no unnecessary polling;
- no layout-thrashing animation.

## 11. Stop conditions

Stop and reconcile before continuing if:

- current main moved materially;
- another PR establishes a canonical app owner;
- implementation starts duplicating intelligence or authority;
- Smart Connect diverges from the Smart Door contract;
- visual quality regresses below the approved baseline;
- identity routing becomes ambiguous;
- a test requires fabricating success;
- the production boundary cannot be observed.

## 12. Definition of complete

The Hub is production-ready only when the clean component architecture and the premium living interface are the **same product**, and a real human journey proves:

**IDENTIFY → ENTER → UNDERSTAND → FIND → ACT → OBSERVE → VERIFY → RETURN → CONTINUE**
