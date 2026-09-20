# JOB 02 — SMART TABS
## Mission
Make Smart Tabs the persistent navigation layer into the real NayaNET retrieval system.

## Job
Implement the smallest production Smart Tab path using the existing Hub navigation design and existing retrieval primitives.

## Contract
A tab has stable identity, label, target type, target, scope, favorite, priority, position, timestamps, and creator/owner. LABEL ≠ TARGET.

Supported target types may include URL, topic, query, category, or route, but use the smallest set actually required by existing production retrieval.

## Build
- Map the current Hub tab/navigation regions.
- Reuse Smart Feed/retrieval/navigation primitives.
- Establish one canonical persistence owner; do not invent a parallel intelligence store.
- Authenticated CRUD: create, rename, edit target, reorder, favorite/pin, remove.
- Persist and reload.
- Apply owner isolation.
- Clicking a tab must resolve target → existing retrieval → authority/visibility filter → presentation.
- Deleting a tab must never delete the intelligence it points to.
- Preserve the canonical visual design and responsive behavior.
- Prove Cloudflare source/build/runtime parity.

## Acceptance
A real user can create a tab, reload, click it, reach the intended retrieval state, reorder/favorite/remove it, and another user cannot see or mutate it. The tab is navigation, not an access grant and not an intelligence record.

## Dependency
Use Smart Feed's actual retrieval surface; coordinate rather than inventing a new retrieval API.

## Handoff
Update Smart Tabs report/checklist/activity and leave the next integration action for Feed navigation continuity.
