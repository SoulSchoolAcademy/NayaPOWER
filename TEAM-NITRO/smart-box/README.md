# smart-box — module home

The Smart Box system lives here: one shape for everything (the intelligent
block), one gate that permits (`may_share`), one function that organizes,
one key that plugs in, one bridge that connects the boxes into NayaNET.

- `block.py` — the shape + the converter (real smart notes and Smart Box
  entries → blocks).
- `gate.py` — `may_share(block, actor, action)` → ALLOW / DENY.
- `test_smart_box.py` — the round-trip check + the 10-case gate matrix.
- `THE-SMART-BOX-BLUEPRINT-20261109.md` lives in `~/workspace/team-nitro/`
  (the spec for all five pieces).

The store is GitHub + Supabase + Cloudflare — already built. The vault is a
namespace, not a new building. No new database. No new app.
