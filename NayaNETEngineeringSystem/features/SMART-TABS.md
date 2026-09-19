# Smart Tabs

## WHAT

Smart Tabs are the persistent quick-access navigation layer of NayaNET. They sit across the top of the Intelligent Hub / Smart Feed and provide one-tap access to destinations, topics, projects, categories, saved retrievals, and intelligence views.

**Smart Notes remember it. Smart Lists organize what I keep. Smart Tabs get me there now. Smart Feed shows me the intelligence.**

Smart Tabs are a navigation/retrieval layer, not a new intelligence store.

## WHY

As intelligence accumulates, navigation becomes a scaling problem. Smart Tabs let a human keep frequently used destinations and retrieval intents immediately accessible without duplicating Smart Notes or creating a parallel classification database.

## HUMAN EXPERIENCE

A clean horizontal bar runs across the top of the Intelligent Hub.

Examples:

`ALL  •  AI  •  PROJECTS  •  BUSINESS  •  LEARNING  •  IDEAS  •  NAYA POWER`

The bar is horizontally scrollable when needed. Tapping a tab immediately navigates to its destination or applies its retrieval intent.

A human can create, rename, edit, reorder, favorite/pin, and remove tabs. The human-friendly label is separate from the machine target.

## TAB TYPES

Initial conceptual target types:

- `url`
- `topic`
- `query`
- `category`
- `route`

The implementation should use the smallest set that fits the existing retrieval/navigation architecture.

### URL tab

`Google → https://google.com`

### Intelligence tab

`AI → topic/query/keywords → existing retrieval → permission filter → results`

### Project tab

`MY PROJECT → existing project/topic/retrieval target → authorized results`

## CORE OBJECT CONTRACT

```json
{
  "id": "stable-id",
  "label": "AI",
  "type": "topic",
  "target": {
    "query": "AI",
    "topic": "AI",
    "keywords": ["artificial intelligence", "AI"]
  },
  "scope": "personal",
  "favorite": true,
  "priority": 1,
  "position": 1,
  "created_at": "...",
  "updated_at": "...",
  "created_by": "human"
}
```

The key invariant is:

**LABEL ≠ TARGET**

## FRONT END

The top-level Smart Tabs bar must:

- remain visually accessible near the top of the Hub;
- support horizontal scrolling;
- provide immediate click/tap navigation;
- support add/edit/remove/reorder;
- make the selected state obvious;
- avoid motion that steals focus or changes selection unexpectedly;
- remain usable on desktop and mobile;
- preserve accessibility and readable labels.

If auto-motion is ever used, interaction immediately gives control to the human.

**Motion introduces choices. Human interaction owns the choices.**

## BACK END

Smart Tabs are persistent user configuration. They should reuse existing navigation, search, retrieval, topic, category, project, and permission primitives.

Do not create Smart Tab-specific intelligence indexes when an existing canonical retrieval primitive can answer the same request.

## DATA

The canonical Smart Tab record must contain a stable identifier, human label, target type, target definition, owner/scope, ordering, preference state, provenance/creator, and timestamps sufficient to reconstruct the user's navigation configuration.

The exact physical storage is implementation-dependent and must be established from the live repository/runtime before migration work.

## RETRIEVAL

For intelligence tabs:

`SMART TAB → TARGET → EXISTING RETRIEVAL → AUTHORITY / VISIBILITY FILTER → PRESENT`

Never:

`SMART TAB → PRESENT → CHECK PERMISSIONS`

A tab cannot grant access. A public-looking label cannot make private intelligence public. Popularity or repeated use is not verification of truth.

## CONNECTIONS

```text
SEARCH → DISCOVER → SAVE AS SMART TAB → REUSE
SMART TAB → SMART FEED QUERY STATE → RESULTS
SMART TAB → SELECT RESULTS → SMART LIST
SMART TAB → AUTHORIZED RESULTS → SMART SHARE / SMART SPACE / SMART MAIL
```

Smart Tabs and Smart Lists remain distinct:

- **Smart Tabs = where I want to go now.**
- **Smart Lists = what I intentionally keep together.**

## INTELLIGENCE / LEARNING

Smart Tab creation and repeated use may provide signals about navigation intent, recurring subjects, active projects, and changing priorities. Those signals are behavioral evidence, not facts or authority.

Observed behavior must remain distinct from inferred preference.

## AUTHORITY / PRIVACY

Smart Tabs inherit the current user's authorization and object-level visibility rules. They must never bypass RLS, sharing scope, revocation, or consent boundaries.

**Private by default • Shared by choice • Collective by consent • Public by decision.**

## FAILURE MODES

- broken URL or route
- invalid target definition
- retrieval target returns no authorized results
- stale project/topic reference
- unauthorized target
- duplicate tab identity/configuration
- ordering conflict
- persistence failure
- cross-user leakage
- selected state inconsistent with destination

Failures must produce a concrete diagnosis and changed repair before rerun; equivalent retries without new information are not acceptable.

## TESTS

Minimum acceptance path:

1. authenticated user creates a Smart Tab;
2. tab persists after reload/session return;
3. tab appears in the top navigation bar;
4. tab navigates to its configured destination or retrieval view;
5. intelligence tab uses existing retrieval semantics;
6. authorization/visibility is enforced before presentation;
7. user can edit, reorder, favorite, and remove the tab;
8. second user cannot see or manipulate the first user's private tab configuration;
9. deleting a tab does not delete the underlying intelligence;
10. source/build/deployed runtime behavior agrees.

## OBSERVABILITY

Every substantive Smart Tabs engineering session must record:

- actor/session;
- local timestamp;
- exact feature/sub-feature worked;
- work performed;
- files/runtime objects changed;
- tests and evidence;
- current completion state;
- blockers/questions;
- what remains;
- exactly one continuation action.

This record belongs in the Team Naya activity system and the feature's project activity projection. Activity is a projection of canonical events; it is not a second truth store.

## DEPLOYMENT

Smart Tabs must be mapped from source → build → deployed runtime. A source-only component or prototype is not production verification.

## VERIFICATION

Status vocabulary:

- `DEFINED` — contract exists.
- `IMPLEMENTED` — source implementation exists.
- `TESTED` — required tests pass in the applicable environment.
- `LIVE VERIFIED` — authenticated deployed behavior and persistence are observed.
- `INDEPENDENTLY VERIFIED` — verification evidence is independently reproduced where required.
- `UNKNOWN` / `BLOCKED` — evidence is insufficient or an execution boundary prevents proof.

## CURRENT STATE

**DEFINED — implementation mapping required.**

The canonical Smart Tabs source note is `.naya/2026-09-11-NAYAPOWER-09-SMART-TABS-SMART-NOTE.md`. It defines persistent top-of-Hub navigation, URL and intelligence targets, ordering/editing, reuse of existing retrieval, permission filtering, and the distinction from Smart Lists and Smart Feed.

## GAPS

1. Inspect the current Hub source and determine the correct top-level navigation insertion point.
2. Inspect existing routing/retrieval primitives before creating any storage or API.
3. Determine whether a canonical Smart Tab store already exists in the repository/runtime.
4. Implement the smallest persistent Smart Tab layer if it does not exist.
5. Connect intelligence tabs to existing retrieval rather than a duplicate index.
6. Add authenticated owner-isolation tests.
7. Prove source/build/deployed-runtime parity.
8. Add day/month/year activity navigation and feature completion reporting to the human-facing activity projection.

## NEXT ACTION

**Map Smart Tabs against the live Hub source and existing retrieval/navigation primitives, then implement the smallest production path for the persistent top-of-page tab bar without creating a duplicate intelligence store. Record the complete session in the dated Team Naya activity system and update this feature's completion checklist/evidence.**
