# smart-box — module home

The Smart Box system lives here: one shape for everything (the intelligent
block), one gate that permits (`may_share`), one function that organizes,
one key that plugs in, one bridge that connects the boxes into NayaNET.

- `block.py` — the shape + the converter (real smart notes and Smart Box
  entries → blocks) + `organize(thing)` (piece 3: LOOK → TAG → FILE →
  LINK) + `complete_where` (the map's Supabase half).
- `gate.py` — `may_share(block, actor, action)` → ALLOW / DENY +
  `KeyRegistry` (piece 4: mint / check / revoke, proven per call).
- `bridge.py` — piece 5: `carry` (a block box → box, gate-checked,
  zero loss, duplicate refused) + `build_space_from_note` (one click;
  the second click finds the space).
- `syncbox.py` — the sickness's root in the box: the sync working
  memory + the bake step captured (`capture_sync_state`) and rebuilt
  byte-identical (`rebuild_from_box`).
- `box/` — the box record itself: the sync state + heartbeat verbatim
  + `manifest.json` (sha256 of every piece, bake recorded by hash).
- `test_smart_box.py` — the round-trip check + the 10-case gate matrix
  + organize (whole 2,086-entry store) + key lifecycle + bridge +
  map completion + recovery demo: 82/82, exit 0, zero stderr.
- `THE-SMART-BOX-BLUEPRINT-20261109.md` lives in `~/workspace/team-nitro/`
  (the spec for all five pieces).

The store is GitHub + Supabase + Cloudflare — already built. The vault is a
namespace, not a new building. No new database. No new app.
