# DESIGN BRIEF — 02 · CONNECTIONS: one system, two doors, same records

**Pair:** `/rooms/connections` (the ENGINE) + `/dashboard#people` (becomes the same system)
**PI item:** `connections-merge-20261026` (owner Nitro, in motion)
**Order in build sequence:** 2 of 7

## Contract read
Design Contract + Master Contract (canonical links in the Toolkit §3). The briefer read the Design Toolkit in full — `BRAIN/10-INTERFACES/NAYA-DESIGN-TOOLKIT.md` at main tip `57866113ca22c48c1580db8489ca8e35b88d6682`, blob `9bf8e446`, 6,546B — and this brief is written to its §4 template. The builder states their own contract read in the build pass before code (Toolkit §1.1).

## Factory / approved-page study notes
- **Nitro's rendered study** (board #3066, comment 6406165060; `connections-study/STUDY.md`, 4 screenshots, 0px overflow, on Nitro's box): rooms/connections is a working list manager (filters, + New list, + Add person, ASK plain-words fields/stages) — but device-local only and its facts/stages FAIL TO LOAD. dashboard#people is fragments plus a failure: its Connections section reads "Connection unavailable — faces cannot load right now." NOTHING is proven shared between them.
- **Scorecard (study, director's dimensions):** effectiveness **4** · usefulness **5**. The job "access your connections from your personal hub" fails on both ends.
- **The systemic charge (director, same session):** stop making NEW pages instead of fixing the pages that exist. This brief is edit-only on both surfaces.
- **Factory inventory status (named gap):** the Smart Factory inventory (404 pieces) and the design-language extraction are on Nitro's box, moving to GitHub under PR #3075 — **unreachable from the briefer's seat**. The builder holds both; in particular the **2026-10-22 orb-row standard** named in the study lives in the builder's study set — its source file could not be verified from this seat, and the brief does not pretend otherwise.

## Measured facts (briefer's byte probes, 2026-10-26 ~02:31Z; saved under `hidden_files/merge-briefs/probes/`)
- `/rooms/connections`: 200, **148,979B** (byte-identical to the audit), viewport PRESENT (quote-agnostic), title "Your Connections". Strings verified in served bytes: `New list`, `Add person`, `orb`, and the device-local admission **`nothing here is sent`** (the page's own copy concedes records are not sent or synced).
- `/dashboard` flagship template: 200, **602,801B**, viewport present. Strings verified: **`faces cannot load`** and **`Connection unavailable`** — the defect strings are served, live, in the bytes.
- **`person_timeline_events` is present in the DASHBOARD template bytes and ABSENT from the room's bytes** (measured). The page registry's todo named the ROOM surface as reading `person_timeline_events` — the bytes say the opposite. The builder proves which surface actually reads it before wiring; do not build on the registry's word or on this note — prove it.

## Harvest inventory (element — source — proof)
- **The room's list-management engine, kept and fixed** — filters, + New list, + Add person, ASK plain-words field/stage creation — source: `/rooms/connections` — proof: [live bytes: strings above] + [rendered study 6406165060]. Fixed, not replaced (study's words).
- **Orb-row presentation standard (2026-10-22)** — the room's list rendering is brought to this standard — source: builder's study set (Nitro's box) — proof: [rendered study names it]; `orb` string present in both room and dashboard bytes [live bytes]. Briefer could not verify the standard's source file — named gap, builder maps it at build time.
- **Timeline data hook** — `person_timeline_events` — source: dashboard template bytes — proof: [live bytes]. Candidate seam for the shared record (per-person timeline is the named finishing move of PI item gap-b2); verify the read path before composing on it.
- **Faces presentation on the hub side** — the hub Connections section's faces/conversations arrangement, minus its error state — source: dashboard#people as rendered — proof: [rendered study 6406165060]. What is harvested is the arrangement, never the error card.

## What dies / what survives / what is harvested from the loser
- **Dies:** the dashboard's "faces cannot load" error state; device-only storage as the system of record; the second, divergent list truth.
- **Survives:** both DOORS (the room and the hub section) — this pair is not a deletion of a surface but a unification of the system behind them. The room's list engine is the one engine.
- **Harvested from the hub side:** the faces arrangement (above) and the timeline hook. Nothing else — the hub side is fragments plus a failure.

## Shared-records / wiring requirement (the actual merge)
- **Records SHARED, not device-only:** a person added, listed, fielded, or staged in EITHER door appears in the other. This is the merge; the pixels are the smaller half.
- The facts/stages load failure in the room is fixed at its root (the load path), not masked.
- **Owner excluded from people-around-you counts everywhere** (study rule, both doors).
- Acceptance test: a two-door read-back — add a test person in one door, prove them present and correct in the other, signed-in.

## Scorer + verifier
- **Builder:** Naya Nitro. **Scorer + verifier:** Naya Resolve — rendered review at the real addresses (phone AND laptop) + scorecard, different seat from the builder. The scorecard posts under Resolve's seat identity; if the formal different-login prong needs a distinct GitHub login, that is named at scoring time, never assumed.
- **Deploy:** on the director's tap, after the scorecard.

## Proof required before announcement
Rendered review still owed — every measurement in this brief is byte probes + the cited rendered study; **no rendered proof of the merged system exists yet**. Required: (1) staged render phone + laptop at both doors, 0px overflow measured; (2) SIGNED-IN citizen view with real people — same records in both doors, two-door read-back receipt; (3) custom fields/stages loading live (the defect, proven gone, not just absent from one screenshot); (4) different-seat scorecard ≥ 9.0.

## Land bar
**9.0 or better**, with link + verification + reconciled counts.

## The lesson this brief carries
Two doors onto two truths is worse than one door: the citizen cannot tell which list is real, so neither is. When a page's own copy admits "nothing here is sent or synced," believe it — that sentence is the bug report.
