# DESIGN BRIEF — 04 · REPORTS: one area, stats as a view inside it

**Pair:** `/rooms/reports` (SURVIVOR, kept whole) + `/personal#reports` (stats harvested in as a view; the page then goes)
**PI item:** `reports-merge-20261026` (owner Nitro, in motion)
**Order in build sequence:** 4 of 7

## The law that shapes this merge (director, 2026-10-26 — general)
**ONE AREA:** one page does not mean everything crammed onto one scroll. One AREA holds everything relevant to each other, with BUTTONS opening views within that one area. Never a thousand top-level pages of the same thing done wrong, never one endless scroll pretending to be unity. Stats becomes a button/view inside Reports — not a section dumped onto the library page.

## Contract read
Design Contract + Master Contract (canonical links in the Toolkit §3). The briefer read the Design Toolkit in full — `BRAIN/10-INTERFACES/NAYA-DESIGN-TOOLKIT.md` at main tip `57866113ca22c48c1580db8489ca8e35b88d6682`, blob `9bf8e446`, 6,546B — and this brief is written to its §4 template. The builder states their own contract read in the build pass before code (Toolkit §1.1).

## Factory / approved-page study notes
- **Nitro's rendered study** (board #3066, comment 6406326834; `reports-study/STUDY.md`, 1280+390, 0px overflow, on Nitro's box): rooms/reports is the REPORTS side — "Your intelligence, collected across time. Each report — one beautiful board." **6 daily reports**, DAILY/WEEKLY/MONTHLY/YEARLY tabs, search, day cards, READ / VIEW / COPY LINK / MD download — missing only the stats. personal#reports is the STATS side — counts first (wall posts, messages, invites, people, today, last 7 days), busiest day, mix, trend, people-in-report, honest empties — but stats WITHOUT reports to read.
- **Factory inventory status (named gap):** the Smart Factory inventory (404 pieces) and the design-language extraction are on Nitro's box, moving to GitHub under PR #3075 — **unreachable from the briefer's seat**. The builder maps harvested elements to Factory pieces at build time or names the gap on the board.

## Measured facts (briefer's byte probes, 2026-10-26 ~02:31Z; saved under `hidden_files/merge-briefs/probes/`)
- `/rooms/reports`: 200, **211,699B** (byte-identical to the audit), viewport PRESENT (quote-agnostic), title "Reports — NayaNET Intelligent Hub". Strings verified in served bytes: `DAILY`, `WEEKLY`, `MONTHLY`, `YEARLY`, `COPY LINK`, `download`, and the hero line `Your intelligence, collected`.
- `/personal` flagship template (602,710B): the stats section's strings verified in bytes: `busiest`, `trend`, `wall posts` (counts/mix/trend/people per the study). The stats live as a section of the shared flagship template — see the template warning in Brief 01; it applies here in full.

## Harvest inventory (element — source — proof)
- **The reports library, kept whole** — period tabs (DAILY/WEEKLY/MONTHLY/YEARLY), search, day cards, READ/VIEW/COPY LINK/MD-download actions, the "one beautiful board" presentation — source: `/rooms/reports` — proof: [live bytes: strings above] + [rendered study 6406326834]. Edit-only: the room is the authority.
- **The stats set, harvested as a view** — counts (wall posts, messages, invites, people, today, last 7 days), busiest day, mix, trend, people-in-report, WITH its honest-empty states — source: `/personal#reports` — proof: [live bytes: strings above] + [rendered study]. The honest empties are part of the harvest: a stat with no data says so, in the same plain words.
- **The view-switch pattern** — a STATS button inside the room opening the stats view, in the room's own tab/button language (the period tabs are the in-page precedent) — source: `/rooms/reports` period tabs — proof: [live bytes] + [rendered study]. No new navigation idiom is invented for this.

## What dies / what survives / what is harvested from the loser
- **Dies:** `/personal#reports` as a page. After the harvest lands and is proven, the personal Reports tab opens the ONE area (`/rooms/reports`).
- **Survives:** `/rooms/reports`, whole, as the one Reports area.
- **Harvested from the loser:** the full stats set (above) as a button/view within the room, **on the same records**. Nothing else — the personal side has no reports to read, and that absence is exactly what dies.

## Shared-records / wiring requirement
- Stats are computed from the SAME records the reports are built from — no second stats store, no divergent counts. The stats view shows stats **on the report/period in view** (the study's shape: "a stats button inside reports that shows stats on the report").
- Template-surgery warning (as Brief 01): the loser is a section of the shared flagship template serving Personal / Business / Space / Dashboard. Removing it must be proven against all flagship faces rendered after the edit.

## Scorer + verifier
- **Builder:** Naya Nitro. **Scorer + verifier:** Naya Resolve — rendered review at the real address (phone AND laptop) + scorecard, different seat from the builder. The scorecard posts under Resolve's seat identity; if the formal different-login prong needs a distinct GitHub login, that is named at scoring time, never assumed.
- **Deploy:** on the director's tap, after the scorecard.

## Proof required before announcement
Rendered review still owed — this brief rests on byte probes + the cited rendered study; **no rendered proof of the merged area exists yet**. Required: (1) staged render phone + laptop, 0px overflow measured; (2) SIGNED-IN citizen view — real reports readable/downloadable AND the stats view showing real stats on the same records (one screenshot of each is not a reconciliation: counts in the stats view must match the records the reports show); (3) personal Reports tab landing on the one area; flagship faces rendered intact post-surgery; (4) different-seat scorecard ≥ 9.0.

## Land bar
**9.0 or better**, with link + verification + reconciled counts.

## The lesson this brief carries
Stats without the thing they describe is a dashboard to nowhere. Numbers belong inside the area they measure — close enough to check against the thing itself.
