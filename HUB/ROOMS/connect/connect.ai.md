# Smart Connect — Builder Spec (AI)

**Status:** PROPOSED. **Route:** `hub/connect`. **Accent:** teal. **Build order:** 4.

## Shell contract

Sidebar + Naya rail unchanged; center swaps. Sidebar placement of Connect itself is an open team decision (canonical rail slot vs. special feature block above Settings) — build the room route-independent so either placement works.

## Component tree

1. `ConnectHero` — "CONNECT YOUR INTELLIGENCE" + ownership line.
2. `DoorGallery` — nine `DoorPortal` objects from the canonical registry: jewel icon, name, one-line capability, `FourLightStatus`.
3. `DoorPortal` detail (expand) — what it can do / what LAW permits / CONFIGURE / VERIFY actions.
4. `ConsentCenter` — grant rows: what, with whom, lineage, toggle, revoke.
5. `SharePreview` (arrives from other rooms) — what/with whom/reversible + Confirm/Cancel.
6. `RoadmapBoard` — non-registry ideas, explicitly marked PROPOSED.

## Data bindings

- Doors ← `BRAIN/10-INTERFACES/0002-SMART-DOOR-REGISTRY-V1.json` + live status probes (connected/authenticated/authorized/healthy).
- Grants ← consent store with lineage. Statuses re-probed on room entry and on demand ("Re-check").

## States

- Per-door: the four lights independently true/false/unknown. `unknown` renders as UNKNOWN, never assumed.
- `verify_running`: progress with real checks. `revoked`: instant UI update + Ledger receipt.

## Interactions

- CONNECT → real connection flow → CONFIGURE → VERIFY (four lights light up as each passes).
- Toggle grant → immediate effect + receipt. Revoke → immediate + receipt + ripple notice.
- Share preview Confirm → share executes → Ledger receipt; Cancel → nothing happens, no trace.
- "Which door do I need?" → Naya recommends from described need.

## Design tokens

Teal flow accents; portals as physical jewel-objects with depth; four-light status as a distinct component (never a single "connected" badge).

## Acceptance

Doors mirror registry exactly; four lights independently truthful; revoke is instant and receipted; no dead buttons; 9.0+.
