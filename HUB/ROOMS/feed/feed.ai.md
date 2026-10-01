# Smart Feed — Builder Spec (AI)

**Status:** PROPOSED. **Route:** `hub/feed`. **Accent:** gold/orange (sparingly: unread markers, active tab rail, LED). **Build order:** hardened throughout.

## Shell contract

Sidebar unchanged. Naya rail unchanged. Center swaps. Route `hub/feed` must not reload shell. Feed is the default landing room after Identity.

## Component tree

1. `FeedHeader` — "SMART FEED," live LED, "Catch me up" button.
2. `ModeTabs` — COLLECTIVE | PERSONAL | ACTIVITY, default Collective, `?mode=` param, session-persistent.
3. `FilterPills` — All / Mentions / Milestones / Naya insights / Unread.
4. `Stream` — virtualized list of `IntelligentBlock` cards ("In a Nutshell" form): identity jewel, title, Naya's one-line read, truth seal, provenance footer, jewel action row.
5. `EmptyState` per mode — honest copy per mode ("No collective activity shared with you yet.").

## Data bindings

- Collective ← network intelligence service (consent-filtered view).
- Personal ← private intelligence store.
- Activity ← operational truth log (RECEIVED/AUTHORIZED/EXECUTED/VERIFIED).
- Each card binds: `block_id`, `truth_state`, `source`, `timestamps`, `naya_read`.

## States

- `live` / `catching_up` (LED amber, "syncing…") / `offline` (LED red, cached with "as of <time>").
- `loading`: skeleton cards. `empty`: per-mode honest copy. `error`: retry with the error stated.

## Interactions

- Mode tab → full re-query of that mode's source; stream replaces; URL param updates.
- Love → recorded to the block's engagement record; jewel fills; undo available.
- Save → list picker modal → pointer added; toast.
- Share → Connect share preview → consent → Ledger receipt.
- Ask Naya → Naya panel with block context.
- Card tap (non-button) → expands "In a Nutshell" → full board (perspective layers).
- "Catch me up" → Naya narrates unread since last visit (real items only).

## Design tokens

- Accent gold/orange reserved for: unread/new energy, active tab rail, LED live state. Never body text (law).
- Cards: obsidian elevated surface, jewel icon with contained depth, truth seal chip.
- Type: title 23px, body 15px (pending Shawn's ruling), micro 11.5px floor.

## Acceptance

Mode switch re-queries (not filters); no cross-mode leakage; stream virtualized ≥500 items; offline shows cached-with-stamp; every action has a verifiable consequence; 9.0+.
