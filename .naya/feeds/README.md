# Specialty-feed lifecycle registry — #2244 requirement 2

Machine form of #2244 §2: *"reuse existing feeds when they fit; create a new
focused feed only for a material project/problem that needs its own persistent
discussion. Keep it open while unresolved/ongoing; close with a resolution
receipt and canonical Smart Note link."*

## What it is

`tools/feed_lifecycle.py` — a fail-closed registry of specialty feeds with an
enforced lifecycle:

```
OPEN → RESOLVED → CLOSED        (focused feeds)
OPEN (forever)                  (standing feeds — protected)
```

The nine standing feeds (#1865–#1873, from the ratified Team Naya Operating
Protocol) are seeded by `init` and **cannot be resolved, closed, or reopened**
— closing a standing feed would contradict ratified law, so the tool refuses.

## Rules (all enforced, all tested)

| Rule | Enforcement |
|---|---|
| Focused feed needs a material justification | `create` rejects justifications < 40 chars |
| Focused feeds split from a standing feed | `create` rejects unknown / non-standing / non-OPEN parents |
| One feed per material problem | `create` is idempotent on (title, parent) while OPEN |
| Close with a resolution receipt + Smart Note link | `resolve` requires outcome (≥20 chars), `SN-NNNN` id, and an http(s) link |
| No skipping the receipt | `OPEN → CLOSED` is illegal; `close` needs RESOLVED |
| Standing feeds stay open | `resolve`/`close`/`reopen` on `feed-1865`…`feed-1873` → `StandingFeedProtectedError` |
| Regressions are honest | `reopen` (RESOLVED → OPEN) keeps the prior receipt in `resolution_history` |
| Corrupt state fails closed | missing/wrong-schema/duplicate-id registry → named error, never a default |

Learning events (PR #2296's envelope) attach via `link-event`. `match` resolves
a feed by id, issue number (`1868` / `#1868`), or issue URL — the seam the
envelope's SHARED gate ("requires the specialty-feed URL") can consult.

## Store

`~/workspace/goals/nayapower-10-10-completion-drive/hidden_files/feed-registry.json`
— runtime state, created by `init` (`--root` overrides the directory; the test
suite uses a temp dir). Like the #2296 event ledger it lives outside `BRAIN/`,
so it adds **zero brain-index drift**. The registry records claims; it does not
verify Smart Notes exist — that belongs to a live verifier.

## CLI

```
feed_lifecycle.py init
feed_lifecycle.py create --title T --owner O --justification J --parent feed-1868 [--issue N]
feed_lifecycle.py link-issue --feed F --issue N
feed_lifecycle.py resolve --feed F --outcome O --smart-note-id SN-1234 --smart-note-link URL [--evidence E ...]
feed_lifecycle.py close --feed F
feed_lifecycle.py reopen --feed F --reason R
feed_lifecycle.py link-event --feed F --event EVT-ID
feed_lifecycle.py get --feed F | list [--status S] [--kind K] | match QUERY
```

Refusals exit 2 with `FEED_LIFECYCLE_REFUSED: <ErrorName>: <reason>` on stderr.

## What this does NOT claim

- Not a GitHub issue creator — the venue is created by a seat; the registry links it.
- Not a notification mechanism (that's #2303) and not the learning-event envelope (that's #2296).
- A RESOLVED feed is not a verified lesson — `BEHAVIORALLY_VERIFIED` lives in the envelope, not here.
- No ratified-law edits. Purely additive.
