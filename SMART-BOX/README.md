# SMART-BOX — the REAL Smart Box (live surface)

**Live:** https://nayanet.app/smartbox · **Worker:** `naya-smart-box` · **Route:** `nayanet.app/smartbox*`

Shawn opened the Box and got "a box of the number one in it" — a directory
listing, not a usable box. His order (2026-11-06 01:58Z): a REAL box where you
can actually access it efficiently and effectively, get everything you need
from it, store everything that matters in it — FOR BUILDING IN IT.

## What this is

A live, usable surface on nayanet.app — not the working files. The working
files (harvest scripts + store) live at `~/workspace/nitro-smart-box/` and
remain the canonical harvest source. This directory holds the live surface:

- `app/index.html` — the Box page (search, feed, linked view, add form, build-in-it)
- `worker.js` — the `naya-smart-box` worker (serves the page + `/smartbox/data` + `/smartbox/add`)
- `data/entries.jsonl` — dated snapshot of the canonical store (see `data/meta.json`)
- `data/meta.json` — harvest stamp: harvested_at + sha256 + count

## How it works

- **Access:** search by topic, date, or his exact words — timed, times shown.
- **Get what you need:** auto-organized feed (feed.py scoring: recency + value +
  topic + connection) + the linked view (PI, Factory, build, Mail, Lists).
- **Store:** `POST /smartbox/add` → Cloudflare KV, one key per entry
  (`entry:SB-XXXX`, counter `meta:next_id` from SB-2087), immediate read-back.
- **Build in it:** the page states the four steps (find → add to your build →
  open Factory/PI → build and put it back).

## Honest limits (on the page too)

- KV adds are NOT the canonical record. A reconcile job (KV → canonical
  store + Smart Note filing) is owed; until it exists, added entries are
  labelled "added via the Box — pending filing" and a re-harvest would lose
  them. KV is eventually consistent (~60 s).
- Snapshot freshness has no owner yet: a scheduled harvest → KV refresh job
  is owed. The snapshot stamp + sha256 are on the page footer.
- Entry IDs are positional and shift as sources grow — cite the source,
  never the ID alone.
- The ten-section Smart Note format has no fields in the harvested store, so
  the page renders entries faithfully from what the harvest holds and never
  invents sections. Full ten-section reading lives in the filed Smart Note:
  4 of the 5 featured entries link to one (SB-2079 → SN-2089, SB-2007 →
  SN-2077, SB-1954 → SN-2084, SB-1941 → the filed Act draft, not a Smart
  Note); SB-0021 has no filed note yet. The linked notes were filed before
  the no-machine ruling, so each still carries a Machine Note section, and
  before the GOLD/RED layers — per-entry GOLD/RED on the page are quoted
  from the entry's own words where the entry supports them (SB-2007 has no
  RED layer, SB-1941 has neither). The full 2,086-entry link backfill is
  owed as the reconcile job, not this surface.

## Fix pass 2026-11-06 (PR #3237, same branch — Verifier defects D1/D3/D5/D4 + design law)

- D1: footer/code/entry links wrap (`overflow-wrap:anywhere`) — no sideways scroll on a 390px phone.
- D3: SB-1941 date corrected `55:07Z` → `00:55:07Z` (source memory/2026-11-06.md:179 heading; harvest dropped the `00:`) — fixed in the canonical store, the snapshot, and KV.
- D5: sub-millisecond searches display `<1 ms`, never `0.0 ms`.
- D4: after an add, the page polls `/smartbox/data` until the entry lands in the shared store, then refreshes the counts line itself; the copy no longer says "at once" for the shared store.
- Design law: links + per-entry GOLD/RED above (4 of 2,086 entries linked so far).

## Deploy

Worker PUT (multipart, metadata mandatory) + route + KV namespace, per the
Scout's ordered steps in `~/workspace/team-nitro/smart-box-real/SCOUT-FINDINGS.md`.
Freeze point: `worker.js` + `app/index.html` as committed on this branch.
Never merge your own PR — merges are Shawn's hand.
