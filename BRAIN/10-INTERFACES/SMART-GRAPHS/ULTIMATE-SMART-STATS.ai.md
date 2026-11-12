# Ultimate Smart Stats — Builder's Spec (AI language)

**Status:** CANDIDATE spec v1 · **Date:** 2026-10-22
**Human analysis of record:** Nitro, *The Living Data System* (2026-10-22, `~/workspace/user/files/LIVING-DATA-SYSTEM-2026-10-22.md`) — block names, data taxonomy, and display laws are hers and canonical; this spec EXTENDS that file with build contracts and does not restate it.
**Extends:** `BRAIN/10-INTERFACES/SMART-GRAPHS/SMART-GRAPHS-SPEC.ai.md` (grammar G1–G7 + output contract in force) · **Governing law:** SN-0822 (living-data law) · **Pairs with:** `DESIGN-BLOCKS/` canon, Composition Law (SN-1790), Factory standard-feature contracts.
**First landing:** Nu's flagship Reports build (Nitro's lane) — §8.

---

## 0. The frame — one universal app, many front doors (Shawn, 2026-10-22, standing doctrine)

ONE ultimate app; each "app" is a **front door** (entrance + main-page focus) into the same interconnected system. Doors: `personal` (intelligence today) · `smart-lists` · `business` · `booking` (wired to Calendar) · `product` · `events` · `community` · `profile` · `menu` (services; ours = NayaPOWER monthly/quarterly/yearly/lifetime) · `sign-up` (email/follow/Connect) · `dashboard` (= the Living Data System).

Consequences for builders:

1. **The Dashboard is one door AND the blocks live inside every door by default.** Data displayed beautifully is a default property of the app, not a page you visit. Every door inherits the §2 blocks; the door's configuration declares which blocks *lead* on its home (e.g. Personal leads Pulse Strip + Insight Feed; Business leads Journey Funnel + Pulse Strip; Community leads Faces Board). Non-leading blocks remain present per the door config — a door may demote a block below the fold, never delete the grammar.
2. **Simplicity law.** Presentation is simplified-beautiful for an average person / child / grandma: simple in presentation, never shallow in substance; full depth is one tap away (the ↗ contract). Mechanically: headline value + micro-sentence on the surface (SN-0822); evidence, history, and tables live behind the tap. A block whose surface requires expertise to read fails this law.
3. **Personal / Business / Space are door configurations** (cover + leading blocks + §4.2 additions) of the one base — not separate apps, not separate codebases. All "per-template" language in this spec means per-door configuration.

## 1. Tokens (exact)

### 1.1 Obsidian stack

| Token | Value | Job |
|---|---|---|
| `--bg-0` | `#0B0D12` | Page ground |
| `--bg-1` | `#12151D` | Sunken wells (streak wells, stream rows, table stripes) |
| `--bg-2` | `#171B25` | Card surface (default block body) |
| `--bg-3` | `#252B39` | Raised surface, hover, chips, inputs |

### 1.2 Spectrum jobs (semantic — a color is a job, never decoration)

| Token | Value | Job |
|---|---|---|
| `--alive` | `#55e39a` | emerald — alive / healthy / on-target |
| `--extra` | `#e8b64c` | gold — extraordinary / opportunity |
| `--alarm` | `#ff5a6e` | red — alarm / leak / failure |
| `--sig` | `#a06bff` | scored purple — signature; headline series; "you" (canonical per tokens.css unification 2026-10-09) |
| `--sig-soft` | `#9d75ff` | purple — ambient signature (gradients, ghost marks) |
| `--human` | `#d86cff` | magenta — human / people / social |
| `--know` | `#55b9ee` | sapphire — knowledge / learning / information |

Series order (G3, unchanged): purple → sapphire → emerald → gold → magenta; max 5, remainder aggregates to "Other". Purple opens every composition (Nitro Display Law 2).

### 1.3 Type & depth

- Body **18px**, line-height 1.5. Headline numerals 40–56px, weight 700, `tabular-nums`, `#F5F7FB` (G4: the number is the hero). Secondary `rgba(245,247,251,.62)`; tertiary `rgba(245,247,251,.40)`.
- Jewel 3D depth per block: `box-shadow: 0 1px 0 rgba(255,255,255,.05) inset, 0 -12px 24px rgba(0,0,0,.35) inset, 0 18px 40px rgba(0,0,0,.45)`; top highlight `border-top: 1px solid rgba(255,255,255,.07)`; radius 20px blocks / 13px chips.
- Glow (G2): `drop-shadow(0 0 12px <job at 45%>)` on the data element only, intensity scales with value/state — never the whole card.
- Motion: entry `--ease: cubic-bezier(.16,.84,.22,1)`; snap `--snap: cubic-bezier(.32,.72,0,1)`. `prefers-reduced-motion` → fully lit static (Nitro Display Law 3): no count-up, no pulse, final values rendered — never broken, never blank.

---

## 2. The 8 canonical blocks (Nitro's names — binding contracts)

Each block is an Intelligent Block: canonical name, data contract over the §4 taxonomy, an underlying Smart Graphs instrument binding (the rendering engine — do not fork it), alive behaviors, and the five truth states (`live · sample · loading · empty · error`, G6). Every block satisfies **SN-0822: magnitude + shape + direction + a human sentence — or it doesn't ship.** Every block carries the Smart Graphs envelope (title · sub-line · visualization · foot row with source honesty + save/share/PDF/send actions) unless noted as an atom.

### 2.1 Pulse Strip
- **Harvest:** KPI anatomy (Xintra Projects, Trackify Analytics, Preadmin Admin).
- **Contract:** `{items: [{metric_id, label, value, unit, delta_pct, period_label, spark: points[≥2], sentence}]}` — 3–4 items.
- **Binding:** each item = `living-counter` + `delta-chip` + `spark-trace` (atoms, §3). The ↗ corner arrow (Trackify) marks the tap-to-detail route.
- **Sentence rule (refinement of SN-0822, see §7.2):** `sentence` is a micro-read, ≤6 words, on Home ("Invites are converting well"); the full sentence lives in the Insight Feed.
- **Alive:** values count up on entry; sparklines draw; on live tick, changed values tween in place (tabular width reserved — no layout shift).

### 2.2 Trend Panel
- **Harvest:** bar+line combo (Xintra Audience/Project Statistics).
- **Contract:** `{bars: [{label, value}], line: [{label, value}], bar_metric, line_metric, periods: [today, 7d, 30d, all]}` — bars = volume, line = the rate that rides on it.
- **Binding:** NEW instrument `combo-stage` (jewel-pillar bars + SVG line) — the one chart form the Smart Graphs canon lacks; minted by this spec for this block.
- **Alive:** bars rise in sequence, line draws after; period tab switches re-animate from the same data contract (all blocks on the page re-frame together — Display Law 5).

### 2.3 Mix Donut
- **Harvest:** donut with a heart (Xintra Follow On Device, Preadmin Subscriptions, Trackify Time Allocation).
- **Contract:** `{segments: [{label, value, metric_id}], total}` ≤5 + Other, spectrum order.
- **Binding:** composition instrument (static sibling of `spectrum-flow`); center total = `living-counter`.
- **Alive:** sweep-in on entry; center counts up; legend rows carry count **and** share % and delta; segment hover isolates and shows its value in the center.

### 2.4 Journey Funnel
- **Harvest:** funnels (Preadmin Deals tapered stages; Recruitment stage pills).
- **Contract:** `{stages: [{label, value, metric_id}]}` ordered ≥2; conversion computed between consecutive stages and overall.
- **Binding:** NEW block form `funnel-descent` (descending jewel bands, width ∝ value).
- **Alive:** stages rise in sequence; conversion % counts; leak rule — stage-over-stage drop > 40% (per-journey `leak_threshold` override allowed) → that joint glows `--alarm` and generates an Insight Feed candidate (§6).

### 2.5 Faces Board
- **Harvest:** people-first (Xintra Suggestions/Requests, Preadmin Clock-In/Out, Sales Performance).
- **Contract:** `{people: [{person_id, name, avatar_ref|initials, presence: live|recent|away, fact, action: message}]}` — newest + most active, default 5.
- **Binding:** list composition over `mini-orb` presence marks (existing orbs family); avatar = jewel initial disc when no photo (never a broken image).
- **Alive:** `live` presence carries the breathing pulse dot; new arrivals prepend with slide; `fact` is one datum in words ("Joined Tue · 14 posts"), never a raw metric name.
- **Template note:** Business worlds relabel the board **Customers** (Nitro Part 4) — same block, same contract.

### 2.6 Insight Feed
- **Harvest:** Trackify AI Insights "Recommendations" — the most intelligent pattern in the 29.
- **Contract:** `{insights: [{id, job: alarm|extra|alive, sentence, evidence: {metric_id, value, delta_chip}, action: {label, target}, ts}]}` — feed-ordered by job urgency then recency.
- **Binding:** composed of `insight-card` atoms (§3) in a `pulse-stream` frame (existing stream behavior).
- **Placement rule:** Home shows top 3; a feed with an `alarm` item pins that item directly under the Pulse Strip (Composition §5.4). Full feed is one tap from Home.
- **Contract rule:** `action.target` must resolve to a real route/block — a dead button fails the block.
- **Generation:** §6.

### 2.7 Heat & Streaks
- **Harvest:** heat grid (mining severity calendar, Preadmin Leads heatmap) + streaks (Trackify Habit Tracker).
- **Contract:** `{cells: [{x, y, value}], x_labels, y_labels, streaks: [{label, days, state: active_today|pending_today|broken}]}`.
- **Binding:** NEW block form `heat-grid` + streak wells (`living-counter` in a `--bg-1` well with flame mark; the check control fills with the block's color when today's unit completes).
- **Alive:** cells bloom in a wave on entry; top-decile cells glow; a completed streak check ignites (color fill + count tween) without reload.

### 2.8 Health Gauge
- **Harvest:** single-score gauge (Preadmin Attendance semicircle, NPS semicircle).
- **Contract:** `{score_100, ingredients: [{label, value_100}]}` — ingredients fixed by Nitro Part 3: response time, activity, growth, completeness (weights are per-door config, declared in the block's sub-line — an unexplained score fails SN-0822's sentence clause).
- **Binding:** `orbit-dial` instrument, /100 scale (see §7.1 for the scale split: vitality /100 here; judgment scores remain /10 on orbit-dial elsewhere).
- **Alive:** arc sweeps to value on entry; score counts; crossing below the door's health floor re-jobs the arc to `--alarm` and generates an Insight Feed candidate.

### 2.9 Reserved / supporting
- **Radar** (`balance-radar`): Hub-level only — balance across a person's worlds / across dimensions. Never inside a single app's Reports (Nitro Part 3).
- **Constellation** (existing instrument): network structure views (Spaces/Hub) — distinct question from radar (§7.3).
- **Ranked-bar list** (`rank-board` atom): inside blocks (top pages, top products, top contributors) — name + spectrum bar + value.
- **Segmented bar** (`segmented-bar` atom): composition snapshot without a chart (Preadmin Employee Status pattern).

---

## 3. Atoms (supporting pieces — not standalone blocks)

| Atom | Contract | Rule |
|---|---|---|
| `delta-chip` | `{delta_pct\|delta_abs, direction, job}` | job: ≥0 → `alive`; <0 → `alarm`; inverse metrics (refunds, bounce, backlog) invert; \|delta\| ≥ metric's `extraordinary_threshold` → `extra`. Flips color live on job change |
| `spark-trace` | `{points[≥2], job}` | hand-rolled SVG polyline, no axes; draws on entry; last point pulses; <2 points → atom omitted (never a fake line) |
| `insight-card` | `{job, sentence, evidence, action}` | the Insight Feed atom; anatomy fixed by §6 |
| `rank-board` | `{rows[{label, value, sub?}]}` | bar ∝ value/max in row's job color |
| `segmented-bar` | `{segments[{label, value}]}` | single bar, spectrum segments, big numbers under |

Existing canon instruments bound above (do not re-author): `living-counter`, `pulse-orb`, `jewel-pillar`, `spectrum-flow`, `constellation`, `pulse-rings`, `orbit-dial` (SMART-GRAPHS specimens), `nl-table` (exact-value lookup — never a hero), `state-badge`.

---

## 4. Data taxonomy (Nitro's — canonical; this section adds IDs + color jobs)

### 4.1 Universal core (every smart app, from minute one, from its own tables)

| Metric ID | Meaning | Color job |
|---|---|---|
| `views` | page/app views | `--sig` |
| `visitors` | unique visitors | `--sig` |
| `posts` | posts published into the app | `--human` |
| `messages_received` / `messages_replied` | conversation volume + replies | `--human` |
| `response_time_median` | median first-response (inverse) | `--alive` (alarm when over promise) |
| `connections` | followers/members total | `--human` |
| `invites_sent` → `invites_opened` → `invites_joined` | the invite journey (feeds Journey Funnel) | `--sig` |
| `content_published` | notes/pages/items published | `--know` |
| `voice_plays` | plays of spoken content | `--know` |
| `saves` / `shares` | kept / spread counts | `--know` / `--human` |
| `activity_heat` | per-day intensity (feeds Heat & Streaks) | block hue |
| `streaks[]` | named streaks (active days, posting, response) | `--extra` while growing |
| `health_score` | computed /100 (feeds Health Gauge) | score-driven |

### 4.2 Per-door additions (door configurations of the one base)

- **Smart Personal:** `profile_views`, `note_reach` (plays/saves/shares per note), `connection_growth_rate`, `top_connections` (Faces Board source).
- **Smart Business:** `leads`, `deals_funnel[]` + `deals_value` (Journey Funnel), `orders`, `revenue` (where commerce exists), `repeat_customer_rate`, `response_vs_promise`, `top_customers` (Faces Board → "Customers").
- **Smart Space:** `member_growth`, `joins` (invite funnel), `posts_per_member`, `top_contributors`, `event_rsvps` (where events exist).

### 4.3 Hub rollup (every world a person owns)
`total_reach`, `total_activity`, `per_app_health[]` (Health Gauge × worlds), and the `balance-radar` across worlds. NayaNET's own team gauges (dock, queue, alignment) render through the same blocks — the system eats its own cooking.

### 4.4 Color-job layer (my addition over Nitro's taxonomy)
Every metric carries the job color in §4.1–4.2 so any source — native or plugged in later — arrives pre-colored by meaning. Domain groupings for tabs/filters: Attention (views/visitors/reach/shares), People (connections/posts/messages/faces), Performance (invites/deals/conversion), Money (orders/revenue — Business), Learning (notes/plays/saves/streaks). Groupings organize; they never re-color.

---

## 5. Composition rules (Composition Law applied)

1. **Cover first.** Reports opens with world chrome: identity, live state (pulse dot + "updated Xs ago"), period switch. No banners; install lives in Settings.
2. **Home light.** Above the fold (phone): chrome + Pulse Strip + top of Trend Panel. Max the 8 canonical blocks per Reports home; detail (full feed, full tables via `nl-table`, per-metric history) is one tap per block — the ↗ is the contract.
3. **Standing order:** Pulse Strip → Insight pin (only when an alarm insight exists) → Trend Panel → Mix Donut + Journey Funnel → Heat & Streaks + Health Gauge → Faces Board → Insight Feed. Urgency reorders *within* the Insight Feed, never the skeleton (Display Law 7: one system in every app).
4. **Period is global.** Today / 7d / 30d / All re-frames every block together from the same contracts (Display Law 5).
5. **"+ Add Block."** Owners may add supporting atoms (rank-board, segmented-bar) and rearrange within the skeleton; they may not introduce a new visual design. Personalization = which blocks + which data (Display Law 7).
6. **Honest sparse states** (Display Law 4): a new app renders all applicable blocks in `empty` state with the copy pattern "Your story starts now — here's your first week taking shape." Fixtures posing as life are a contract failure.
7. **Blocks in every door (§0.1).** The §5.3 standing order governs the Dashboard door's full Reports home. Other doors compose a *subset in the same relative order* per their door configuration, with the door's lead blocks promoted — the grammar, order logic, and block contracts never change between doors.
8. **Simplicity law (§0.2).** Surface = value + shape + micro-sentence; depth (history, evidence, `nl-table`) is one tap away on every block, in every door. If a surface needs a manual, the surface is wrong.

---

## 6. Insight Feed generation contract

1. **Inputs:** deltas vs prior window; threshold crossings (per-metric `alarm_threshold`, `extraordinary_threshold`); Journey Funnel leak joints; Health Gauge floor crossings; cross-domain lag correlation (e.g. Attention delta at t−2d vs Money/Activity delta at t); streak breaks and streak milestones; unanswered-message aging vs `response_time_median` promise.
2. **Card anatomy (fixed):** `sentence` (plain words; names the cause only when evidence supports it — correlation is labeled as correlation) + `evidence` (the metric rendered as value + `delta-chip`) + `action` (button → the block/route where the fix lives). Model sentence: *"3 invites opened, none joined — send the nudge."*
3. **Jobs:** `alarm` = loss/leak/failure needing action · `extra` = extraordinary gain or closing opportunity · `alive` = a working pattern worth protecting — **max 1 `alive` card surfaced at a time** (praise is rationed so it stays meaningful).
4. **Cadence:** regenerate on period change, on any alarm crossing, and on stream events aging past promise; a dismissed card does not repeat within the same window.
5. **Voice:** Smart Note human language; no metric IDs in sentences (say "fewer people are finishing the invite," not "stage-3 conversion decay").

---

## 7. Disagreements with Nitro — explicit, with reasons

1. **Scale split (Health Gauge).** Nitro's gauge is /100 — adopted for *vitality* (a computed percentage of response/activity/growth/completeness). NayaNET *judgment* scores (Calculator, scorecards) remain /10 on the same `orbit-dial` instrument. Rationale: one dial, two meanings would corrupt both; the scale is declared in the block's sub-line so the reader always knows which they're seeing.
2. **Pulse Strip sentence length.** SN-0822 (hers) requires a sentence per number; the Composition Law requires a light home. Resolution: micro-sentence ≤6 words on the Strip; full sentence + evidence + action in the Insight Feed. The law ships; the strip stays glanceable. If Nu's prototype shows the micro-sentences reading as clutter in practice, the fallback is sentence-on-first-item-only — decided by the prototype, not by taste.
3. **Constellation retained.** Nitro reserves radar for Hub balance (adopted). The canon's `constellation` instrument answers a different question (connection structure, e.g. a Space's member graph) and remains available; radar = balance across dimensions, constellation = structure of connections. No duplication: different data contracts (`{dimensions[]}` vs `{nodes[], edges[]}`).
4. **Plug-in order.** My first draft led with external connectors; Nitro's native-first model is adopted (§8): the app's own tables are source zero. Connectors (social accounts etc.) attach as additional sources feeding the *same* metric IDs — the block never changes shape when a source is added (her Part 4, adopted verbatim as the plug-in law).

---

## 8. Plug-in model & landing

**Source zero (native):** every Factory app instruments its own Supabase tables for the §4.1 core at build time — the blocks are born reading them; a fresh app shows honest sparse states, never fixtures.

**Plugged-in sources:** a connector declares `{auth_kind, metric_ids[], refresh: stream|poll|manual, identity: {name, mark}}`. Its fields map to taxonomy metric IDs by the connector's declared map only — unmapped data is dropped, never guessed (UNKNOWN ≠ PASS). Added sources deepen existing blocks (extra series/rows); zero mapped metrics = connect fails with an honest error. Until a source's first successful sync its contributions render `sample`-labeled; a failed sync errors only its own contributions, with remedy text; data older than 2× the refresh interval shows exact age in `--extra` in the sub-line.

**Create-a-world:** a world with no external source is valid — manual/native metrics (a project, a classroom, a habit) are first-class sources.

**Landing order:**
1. **Nu's flagship Reports build (Nitro's lane, in flight)** — first landing: Pulse Strip + Trend Panel + Mix Donut + Insight Feed sentences; Journey Funnel / Health Gauge / Heat & Streaks ride items 3–10 of `TEN-STAR-SCORECARD-2026-10-22.md`.
2. Blocks minted as official Factory pieces (`DESIGN-BLOCKS/blocks/graphs/`, named + dual-labeled) → standard feature of the one base, inherited by every door (per-block exact-predicate Factory contracts are the follow-on artifact, written against Nu's proven prototype — Nitro's named honest gap).
3. Hub rooms' stats surfaces adopt the same blocks (Reports room first, Mirror item B8); Hub rollup + `balance-radar` land with the rollup.

## 9. Honesty boundaries

- This spec does not claim connector coverage exists for any external source; coverage ships per-connector.
- Health-score weights are per-door config and must be declared in-block; an undeclared-weight score must not render.
- The specimen (`specimen-ultimate-dashboard.html`) uses sample data, labeled SAMPLE on the page, per G6.
