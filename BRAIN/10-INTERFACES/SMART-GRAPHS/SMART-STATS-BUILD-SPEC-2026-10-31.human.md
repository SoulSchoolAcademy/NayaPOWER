# SMART STATS — The Build Spec (v3, 2026-10-31)

**For:** Shawn · **From:** Naya Resolve · **Status:** build-ready; base spec CANDIDATE → this addendum carries today's rulings and asks ratification by landing
**Base (not repeated here):** `ULTIMATE-SMART-STATS.human.md` / `.ai.md` / `ultimate-smart-stats.machine.json` (2026-10-22) — the 8 blocks, the Smart Graphs instruments, the tokens, SN-0822's law: *magnitude + shape + direction + a human sentence — or it doesn't ship.*
**Companion:** `smart-stats-build-2026-10-31.machine.json` (the value table + matrix + placement as data)

---

## In a nutshell

Smart Stats is one engine, not 26 dashboards. One ledger of events, one value table, one chart matrix, eight blocks — and every page in the network pulls the same blocks, fed by its own world's slice of the same ledger. The Dashboard is the signature piece: the door whose whole focus is the system itself. Every other door inherits it. A page with no stats on it is a page that hasn't been built yet.

## 1 · The data spine — one ledger, every conversion knows its mother

Every number anywhere in NayaNET is computed from one event stream. An event is: **actor · kind · world · source · timestamp**. Nothing is stored as a guess; aggregates are always derived, so any number on any page can be traced to the events that made it.

- **Attribution is a field, not a report.** A join records which invite (and whose) brought it. A click records which link, in which world. A sale records the product and its creator. Until an event kind carries its source, its insights stay honest aggregates — never invented breakdowns.
- **Provenance rides every surface.** Each stats surface states its own truth in one line: *Ledger synced · N of M sources live.* A source that isn't wired renders the honest frame — "not tracked yet" — never a plausible number.
- **The tick rule (Living Data guard).** Every animation, breath, and river movement is a real ledger event arriving. Motion that isn't an event is a liar that breathes, and it fails the gate.

## 2 · THE VALUE TABLE — one table, one place (locked 2026-10-31)

This table is the single source for what an action is worth — Dashboard score, Smart Ledger, and canon (SN-1905) all read from here. *(Delta vs SN-1905 as filed: sale 50 → 100, per Shawn's derivation and Nitro's best-option answer, seconded by Resolve on the math — strict ladder, no ties, hardest-to-fake signal carries the crown. Invites, saves, membership added as first-class rows. A canon amendment note is owed so the Smart Note and this table never disagree again.)*

| Action | Points | Rule |
|---|---|---|
| Birth (base) | **75** | Once, at joining. The foundation, not a bonus. |
| Like / love | 1 | Wired: pending |
| Comment | 3 | Wired: pending |
| Save | 5 | Newly wired (server-persisted) |
| Share (inside NayaNET) | 5 | Wired: pending |
| Share (external) | 10 | Wired: pending |
| Invite sent | **25** | First invite per person only, through the system — cannot be farmed |
| Post created | 25 | Live |
| Smart Note created | 35 | Live |
| Membership created | **40** | Once. Stepping onto the stage, not paying rent — the leaderboard can't be bought monthly |
| Join (an invite becomes a member) | **50** | Send 25 + join 50 = **75 = exactly one birth.** Bringing a person into the world is worth one birth. |
| Sale | **100** | Real money moving — the hardest signal to fake, so it safely carries the highest value. The crown of the table. |

**The score formula** (what the Dashboard gauge computes, and what any page's Pulse Strip shows for its world):

```
SCORE = 75
      + 25·posts + 35·notes + 5·saves
      + 25·invites_sent + 50·joins + 40·membership(0 or 1) + 100·sales
      + 1·likes + 3·comments + 5·shares + 10·external_shares
```
Unwired rows count 0 today **and the page says so** — the pending-values note on the live Dashboard ("invites · membership · levels — values await Shawn's ruling") is now CLOSED by this table; the page's next pass replaces it with the values themselves.

**The guard rows.** Law of One / no-harm: harm earns zero. Continuous harm drives points negative and functionality fades toward none. Cross-account farming is detected and those accounts go down together. The anti-farm rule on invites (first-per-person, in-system only) is part of the table, not a footnote.

**Levels.** The ladder stands. The display law changes: never show a bare distance. Always human terms — *"725 to go — about 21 days at your pace"* — where pace is the trailing 7-day average of earned points per day. (Stars six through nine remain unnamed — Shawn's to name.)

## 3 · THE MATRIX — when × what × where (locked by Shawn)

Every stats surface in the network is a view into one three-axis matrix. The axes never change; only the slice does.

- **WHEN:** Live · Hour · 7 days · 30 days · All time
- **WHAT:** Activity · Engagement · Points (with drill-down) · Growth · Money — **each category owns one spectrum color**, network-wide, forever. A color means the same thing on every page.
- **WHERE:** This world (the default) · Pages · Rooms · Smart Link

**The resting state IS everything.** There is no "Everything" button and no Mix view — the unfiltered state is the whole picture; the axes only narrow it. Glossy buttons carry live numbers inside them; a button whose number isn't real yet says so on its face.

## 4 · The blocks — the parts, and the grammar inside them

The eight canonical blocks (contracts in the base AI spec) are the only stats parts that exist. Builders import them; nobody redraws them.

**Pulse Strip · Trend Panel · Mix Donut · Journey Funnel · Faces Board · Insight Feed · Heat & Streaks · Health Gauge**

Inside the blocks, each source speaks its own visual grammar (the Living Data language):
**creating = steps · notes = constellation · likes = ripples · shares = branches · invites = funnel · sales = climb · membership = a closing ring · the River = all currents in one flow.**

The narrator (Insight Feed, "Naya reads it back") turns the numbers into meaning on every surface that carries it — including bad news, said beautifully, or the panel is decoration and gets cut.

## 5 · The placement matrix — which parts lead on which door (the family law)

Build to what it **should** be, never what it is. Before any build starts, the builder names the siblings: the parts it shares with its family and the doors it must resemble. A piece that doesn't fit its family is no piece.

| Door | Leads with | Also carries |
|---|---|---|
| **Dashboard** (the signature piece) | All eight — it IS the system, fully expressed | The River · the narrator · the full matrix |
| **Personal** | Pulse Strip · Faces Board · Insight Feed | Trend Panel |
| **Business** | Trend Panel · Journey Funnel (leads→deals) · Mix Donut (money) | Pulse Strip · Insight Feed |
| **Space** | Faces Board · Heat & Streaks · Journey Funnel (the invite journey) | Pulse Strip · membership ring |
| **Reports** | Insight Feed as letters · Health Gauge | Dashboard ⇄ Reports cross-buttons, both ways |
| **Project Intelligence** | Health Gauge (filled vs proven as a living graph) · Trend Panel | Pulse Strip |
| **Smart Lists** | Pulse Strip (mini) | — grows by import, never by invention |
| **Every other door** | **Pulse Strip at minimum** — score + momentum + one mini trend, fed by that world's ledger | Blocks added by import as the door matures |

## 6 · The gate — stats checks that run as code, not eyeballs

A stats surface ships only when every check passes, with evidence (screenshot + measurements) attached:

1. **Obsidian check** — computed background is the obsidian token; white text; no white background anywhere in the surface.
2. **Spectrum walk** — no color repeats adjacently in any pill/button row; each WHAT category renders in its own locked color.
3. **Reconciliation test** — the displayed score equals the value-table formula applied to the displayed counts. (The 175 test: 75 + 4×25 + 0×35 = 175, or the build fails.)
4. **Honesty test** — every unwired metric renders its honest frame; a fabricated or SAMPLE value outside a labeled specimen fails the build.
5. **SN-0822 test** — every number carries magnitude + shape + direction + a human sentence, in its block or on its tap-through.
6. **Family test** — every block on the page is byte-identical to the Factory part (import, not copy); the builder's sibling list is attached.
7. **No dead chrome** — no SOON pills, no disabled axes pretending; a dark axis is labeled with why, or it isn't rendered.
8. **Motion truth** — every animated element is driven by a ledger event kind that exists in the spine.

## 7 · Build order (from today's live state)

1. **Close the values on the live Dashboard** — replace the "await ruling" note with this table's values (invites 25/50, membership 40, sale 100); the counts already exist.
2. **Pulse Strip transplant** — onto Personal, Business, Space, verbatim from the Dashboard's blocks, fed by each world's slice. (This is fix #3 of today's four-page scorecard.)
3. **Attribution capture** — joins, clicks, sales record their source at write time.
4. **Gate checks 1–8 into the design gate** — so every future build is held by code.
5. **Per-door lead blocks** per §5, in lane order.
6. **Reports letters** fed by the Insight Feed; PI's filled-vs-proven becomes a living graph (Vitality Law).

## 8 · What's still open (named, not hidden)

- Stars six through nine: unnamed — Shawn's to name.
- The canon amendment note aligning SN-1905's filed table with §2 (sale 100) — owed by the lane, no decision needed.
- Phone-width density for the full Dashboard expression — unmeasured in Resolve's tooling; measured check owed at first gate run.
- Ask Naya "Tell me my stats" — the voice briefing rides this same spine (one word can note it, smart-note it, or mail it); spec'd in Nitro's briefing, built on this table when the spine lands.

— Naya Resolve, 2026-10-31
