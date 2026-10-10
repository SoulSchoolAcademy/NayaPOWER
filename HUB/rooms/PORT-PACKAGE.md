# Room Port Package — Naya 4 → one-app convergence

**Status:** CANDIDATE · offered to #1270 / #1278 lanes · not a parallel app.
**Source:** branch `naya4/hub-rooms-v1`, `HUB/rooms/.src/` (commit `35856721`).
**Law:** `HUB/SMART-APP-10-10-EXECUTION-LAW.md` §23 (one-app convergence).

## Role of this package

`naya4/hub-rooms-v1` injected furnished rooms into the `smart-feed.html` monolith.
That technique is **retired as a production path** — the monolith is a laboratory
(31 script blocks, `MutationObserver` globally shimmed to no-op at line 5, repeated
repair/boot families). Per the convergence law, the production vehicle is #1278's
modular architecture.

What survives as portable value:

1. **Ten room modules** (`HUB/rooms/.src/rooms/*.js`) — self-contained render
   functions with real interaction logic, proven in live Chrome 152.
2. **The room store + action contract** (`HUB/rooms/.src/core.js`) — receipts,
   hash chain, prefs, export/erase, action dispatch.
3. **Five integration defects** the live browser found that unit tests could not
   (below) — transfer them as regression tests for the modular app.
4. **The live-browser QA driver** (`HUB/rooms/.src/qa/cdp-qa.js`) — CDP-based,
   all rooms clicked, interactions executed, screenshots reviewed.

## What each room brings (proven behaviors)

| Room | Portable logic |
|---|---|
| reports | Narrative synthesis from real counts + receipts; Day/Week/Month/Year ranges that change the synthesis, not just the filter |
| library | Search + facet + time filters over intelligence objects; inline inspect |
| connect | 10-door grid, two-step scope review → confirm, per-door CAN/CANNOT, "connection ≠ permission" |
| ledger | Hash-linked receipt chain, verify (CHAIN VALID), export |
| connections | Add/remove governed relationship records, scope display, per-connection receipts |
| lists | Saved/favorite/loved/top-rated/collections, canonical lanes |
| mail | Honest empty state, notification pref, no fake mailbox |
| spaces | Six context spaces with privacy tiers, note counts, custom-space creation |
| settings | Identity, runtime boundary, privacy, export/erase, reduce motion |
| notes | Runtime-first capture, honest local fallback, file-to-space |

## Adapter surface the rooms need

The rooms currently read a local store (`NayaHub.d`). For the modular app, the
**one canonical runtime adapter** should expose (names illustrative):

- `getReceipts() / addReceipt(action, detail) / verifyLedger()` — hash-linked chain
- `getSpaces() / createSpace(name)` — context environments
- `getConnections() / addConnection() / removeConnection()` — governed relationships
- `getCollections() / saveToCollection(ref)` — lists over canonical objects
- `listIntelligenceObjects()` — for reports/library synthesis (NOT DOM scrape)
- `searchIntelligence(query)` — governed retrieval with provenance (§21.4: never DOM text)
- `getDoors()` — canonical Smart Door registry state (reconciled; §21.5)
- `getRuntimeState()` — honest per-room state for the §21 state model

Local persistence is a prototype fallback, never the canonical truth (§15 DO NOT).

## Transfer tests — five defects the browser caught

These are architecture-agnostic. The modular app must prove each one closed:

1. **Duplicate definitions.** The monolith defined some rooms twice; hoisting made
   the stub live. Test: every room route renders the furnished module, not a stub.
2. **Router bypass.** `render()` routed two rooms through placeholder stubs while
   the real modules sat dead. Test: no room function is unreachable dead code.
3. **Cross-closure scope.** Room code lived in a different closure than the router
   → ReferenceError on click. Test: click every room, assert zero unhandled rejections.
4. **Deep-linking.** Nav clicks never updated the address bar. Test: click →
   address bar shows `#/hub/<room>`; fresh load of the URL renders the room;
   back/forward works.
5. **Stale labels.** "Smart Share" survived in three places after the rename.
   Test: canonical names asserted in exactly one source (link registry / room map).

## What NOT to port

- The monolith-injection build technique (`build.py` replacing functions inside
  `smart-feed.html`). It was scaffolding, not architecture.
- Hardcoded door lists (bind `getDoors()` to the reconciled canonical registry).
- DOM-scraped library search (bind `searchIntelligence()`).
- `localStorage` as source of truth (prototype fallback only).

## Verification standard for the port

Per the execution law §11/§22: code tests + browser interaction + persistence
reread + negative/refusal proof + responsive/device + a11y + independent D1–D8.
A room is not "ported" because its route renders — it is ported when its
ORIENTATION → STATE → INTELLIGENCE → ACTION → PROOF chain works end to end.
