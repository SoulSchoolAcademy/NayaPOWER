# 06 — Engineering + Verification Map

## 1. Current package topology

### Source
- `2026 09 08 452 NayaNET Hub.html`
- `nayanet-intelligent-feed-v6.js`

### Deployment workflow
- `.github/workflows/deploy-current-nayanet-hub.yml`

### Runtime
- `https://nayanet-v7-intelligent-hub.nayanet.workers.dev/`

### Smart Link
- `https://nayanet-v7-intelligent-hub.nayanet.workers.dev/intelligence/nayanet-intelligent-feeds`

The workflow copies the exact HTML snapshot to `release/assets/index.html`, copies the feed JS, creates a Cloudflare Worker wrapper, deploys, then curls root/Smart Link/feed and checks source markers. This is source/artifact/runtime verification, but it is not a substitute for visual independent inspection. 

## 2. HTML responsibilities

The audited HTML currently contains:
- global CSS
- shell markup
- page-state markup
- ecosystem links
- feature-report links
- local storage state
- page navigation
- Smart Note creation and rendering
- report generation
- GitHub verification
- mail draft behavior
- settings behavior
- multiple intelligence enhancement layers
- multiple feed mutation/normalization layers

This is functionally rich but architecturally overloaded.

## 3. JavaScript responsibilities

### Base inline application script
Owns:
- navigation
- note persistence
- type inference
- note rendering
- metrics
- reports
- evidence
- settings
- mail
- GitHub verification
- local discovery block

### `nayanet-intelligent-feed-v6.js`
Owns a renderer/normalization pass over `#homeIntelligentBlocks`.

Its stated intent is `TRUE LEGACY BOARD RECONSTRUCTION` and it:
- removes rejected renderer IDs/selectors
- converts grids/columns/rows to vertical flow
- removes code/debug artifacts
- applies a luminous intelligence spine
- standardizes typography and surfaces
- supports reduced motion
- repeatedly restores the target every animation frame

### Inline V7 intelligence layers
The HTML contains multiple later layers for:
- login welcome
- ecosystem menu
- right-rail removal
- feed mirror
- intelligence search
- library
- lists/groups
- engagement
- Today surface
- presentation refinement
- feed excellence
- canonical authority correction

This is the central engineering lesson: too many scripts mutate the same DOM. The rebuild must consolidate the final intended behavior into a single state/render architecture.

## 4. Current local storage map

| Key | Meaning |
|---|---|
| `nayanet_v7_live_notes` | Smart Note event array |
| `nayanet_v7_live_settings` | five operating booleans |
| `nayanet_v7_mail_drafts` | locally preserved mail drafts |
| `nayanet_v7_alias` | local NayaNET alias |
| `nayanet_v7_surgical_v1` | integrated intelligence state: favorites, lists, groups, engagement, profile/referral, feedback |
| `nayanet_intelligent_blocks_v2` | feed/blocks favorite/save/rating/comment state |
| `nayanet_intelligent_feed_actions_v1` | feed engagement state |
| `nayanet_ambassador_url` | local ambassador URL used by share layer |
| `nayanet_v7_referral` | referral value used by sharing |

## 5. APIs / network calls actually present

### GitHub verification
`GET https://api.github.com/repos/SoulSchoolAcademy/NayaPOWER`

Purpose: verify repository doorway and default branch.

### No production Naya call
The static package contains no actual remote Naya reasoning request in the audited application logic.

### No production mail call
No outbound mail API is called by Smart Mail.

### No secure discovery endpoint
People discovery is intentionally blocked.

## 6. Data boundaries

### Browser-local
Notes, settings, drafts, engagement, lists, groups, feedback and referral state are browser-local.

### Remote read-only
GitHub verification is a remote read.

### Remote deployment
GitHub Actions + Cloudflare Worker deployment is remote infrastructure, not application intelligence storage.

## 7. Renderer contract

The future renderer should accept a canonical block object rather than scrape the DOM.

```text
IntelligentBlock {
  id
  title
  type
  createdAt
  updatedAt
  source
  visibility
  verification
  human
  child
  grandma
  naya
  machine
  weaver
  lesson
  meaning
  action
  tags[]
  engagement
  provenance
}
```

The renderer should be pure wherever possible:

`canonical state → deterministic DOM`

Actions should mutate state and request a rerender/update, not mutate arbitrary DOM from unrelated scripts.

## 8. State architecture target

```text
Canonical Event Store
        ↓
Application State / Selectors
        ↓
Page State
        ↓
Single Renderer
        ↓
DOM
```

Not:

```text
HTML
 + inline script A
 + inline script B
 + feed JS
 + overlay C
 + overlay D
 + mutation observer
 + interval
 + animation frame loop
```

The latter is the current failure pattern that makes source intent difficult to reconcile with visible runtime.

## 9. Deployment verification contract

Every Hub release must verify, in order:

1. **SOURCE** — exact file selected.
2. **BUILD ARTIFACT** — packaged bytes and required markers.
3. **DEPLOYMENT** — deployment succeeds.
4. **PUBLIC RUNTIME** — exact public URL serves the expected artifact.
5. **ASSET RUNTIME** — imported JS asset is the expected version.
6. **DOM OBSERVATION** — independent browser observation confirms visible structure.
7. **INTERACTION TEST** — critical controls behave correctly.
8. **PERSISTENCE TEST** — state survives reload where intended.
9. **MOBILE TEST** — responsive contract is verified.
10. **NO-REGRESSION TEST** — no right sidebar, debug artifact, broken link or duplicate renderer has returned.

## 10. Required release evidence

A release is not production-proven until there is evidence for:
- exact source path
- exact artifact path
- exact deployment identifier
- exact public URL
- exact observed runtime content
- critical DOM markers
- critical click results
- local persistence result
- mobile result

## 11. Source-authority correction

The repository continuity document says `NAYANETHUBONE.html` is authoritative, while the current deploy workflow packages `2026 09 08 452 NayaNET Hub.html`.

This must be resolved before rebuilding. The future contract should name exactly one file as current Hub source, and all deployment workflows should consume only that source.

## 12. Runtime architecture target

Recommended reconstruction:

```text
Canonical Hub Source
   ↓
Single Data Model
   ↓
Single Router / Page State
   ↓
Single Intelligence Store Adapter
   ↓
Single Feed Renderer
   ↓
Single Interaction Controller
   ↓
Persistence Adapter
   ↓
Optional Naya / Backend adapters
   ↓
Verification + receipts
```

External services should be adapters, not hidden DOM scripts.

## 13. Persistence target

The local static package can remain a fallback/dev adapter, but production should use a canonical authenticated store.

The adapter boundary should make it possible to swap:
- localStorage
- authenticated API
- Supabase/Postgres
- Naya Power / Superbrain event pipeline

without rewriting the visual renderer.

## 14. Naya adapter target

```text
Hub Action
  ↓
Naya Adapter
  ↓
Authenticated Superbrain / Naya Power
  ↓
Naya response + receipt
  ↓
Canonical event enrichment
  ↓
Feed projection
```

The adapter must return explicit status such as `pending`, `verified`, `blocked`, `failed`, rather than leaving the UI to infer truth.

## 15. Mail adapter target

```text
Compose
  ↓
Validate
  ↓
Communication Adapter
  ↓
Transport
  ↓
Receipt
  ↓
Sent / Draft / Failed state
```

A pending local draft must never be rendered as a sent message.

## 16. Search adapter target

Search should query canonical intelligence state/index, then return records with provenance.

The UI should know:
- why a result matched
- source event ID
- current state
- privacy
- verification
- destination on open

## 17. Engineering quality gates

- No duplicate renderer for same target.
- No mutation observer used as a substitute for correct architecture.
- No setInterval/animation-frame loop used to fight another renderer.
- No hidden source authority.
- No source file with misleading historical name used as current without lock.
- No feature may claim server persistence when it is local only.
- No user-visible debug/code artifact.
