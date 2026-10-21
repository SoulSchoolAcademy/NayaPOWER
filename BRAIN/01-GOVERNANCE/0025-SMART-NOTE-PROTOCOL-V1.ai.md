# The Smart Note Protocol — V1 ULTIMATE (AI tongue)

Canonical procedure. Merges Resolve's 0025 draft (PR #2850) with Nitro's 2026-10-21 recommendations draft, scorecarded against live evidence; Shawn's rulings of 2026-10-21 govern all conflicts. Worked example: SN-0810. If another document's procedure disagrees, this one governs; file the conflict as a defect.

## Definitions
- Smart Note: the unit of living intelligence in NayaNET; a nine-section document (§Sections), filed in the brain, synced to Supabase `hub_smart_notes`, rendered in the Hub.
- Terminal states: `VERIFIED_LIVE` (all four verifications true) or `STALLED:<failing-step>`. "Done" == VERIFIED_LIVE. Written / committed / PR open / landing requested / on main unverified are NOT done.

## Identifiers, category, filing
- ID: SN-####. Claim scan BEFORE writing: (a) main tree, (b) open PR heads/staging trees, (c) board tail, (d) the corpus for the IDEA itself (dedupe — one note, one truth; corrections edit, never fork). First claim stands; never reuse a number. A scan executed against unpadded patterns misses zero-padded filings (`SN-01773`) — scan both forms.
- IB id: `IB-SMART-NOTE-YYYYMMDD-sn####-<slug>`; filename == IB id + `.md`, exactly. Any other filename = no share page, no card art.
- Path: `BRAIN/05-MEMORY/SMART-NOTES/YYYY/MM/DD/<TOPIC>/<theme>/SN-####/<IB id>.md`.
- Category is STRUCTURAL: the bridge derives it from the path TOPIC segment (`topic_for_path`). TOPIC = the note's SUBJECT from the existing taxonomy, never its kind. `**Category:**` line inside the note == path TOPIC. One canonical spelling per category (case-sensitive); variants are defects.
- UNCATEGORIZED is the bridge's render for a topic-less/malformed filing: a protocol violation; the note is not done even if visible; the author re-files under the true path. If no subtopic fits, create one deliberately (named for the true domain) and record it in the NAYA section.

## Viralize + the block standard
- Authoring order fixed: category → topic headline → ultimate hook → nine sections.
- Hook: the greatest-possible human hook; self-scored on the stranger-tap test ("would a busy stranger tap this?"); target ≥9; rewrite until yes. Kind/ID/topic labels are forbidden as titles. Subheadline = the plain-English promise.
- Deliverable = a one-minute Intelligent Block: skim (Nutshell + headings carry the whole), listen (play, real voice), full read. Distillation standard: essence in the simplest, clearest, most concise words that keep the truth whole. Presentation: elevated boards, big clear text.
- Feed surfacing is BY CATEGORY via Smart Tabs — never one undifferentiated stream.

## Sections — canonical spellings, in order, none absent
`IN A NUTSHELL`, `THE HUMAN VERSION`, `FOR A CHILD`, `FOR GRANDMA`, `FOR NAYA`, `FOR THE MACHINE`, `WHAT IT ALL MEANS`, `WHAT'S IN IT FOR YOU`, `HOW IT APPLIES`. Ingest minimum: non-empty NUTSHELL or HUMAN VERSION — below that the bridge silently cannot ingest. Nutshell stands alone. MACHINE section = parseable JSON with the note id + operative values. Metadata header: `**ID:**`, `**Created:**`, `**Category:**`.

## Pipeline (Sender → Bridge → Receiver)
1. SENDER: the note file on GitHub `main` — the ONLY door. Local files, branches, open PRs are invisible downstream.
2. BRIDGE: the sync scans main's tree (identity-blind by construction), detects by blob SHA, derives category from path, parses (refuses below ingest minimum), upserts to Supabase `dahisasgpfvziswqvmvm` / `hub_smart_notes`, mints share assets via `naya-share` (routes /s/* and /share-img/*), enqueues voice at publish (nutshell chunks first, then remaining layers), rebakes the Hub when ≥1 note syncs.
3. RECEIVER: feed card (by category tab), own page /s/sn####, share image, play in the real voice.
4. HONEST STATE (root-caused 2026-10-21): the documented ≈5-min cadence is NOT confirmed by observation (SN-0812, bot-landed canonical 18:21:52Z → no card, no rebake >7 min). Treat cadence as UNVERIFIED. The streamline (machinery committed to repo under tools/smart-notes-sync/, push-triggered workflow on the SMART-NOTES path, scheduled reconciler + visible heartbeat, acceptance proof timing both doors) is designed and owed; secrets placement is a human-gate packet. Until it is acceptance-proven, no seat states appearance timing as fact, and the author's verification is the only reliable detector.
5. REGISTRY NOTE: `.naya/memory/smart-notes/index.json` is reconciled by its own cure lane; the Hub feed does not read it. Registry lag never blocks visibility and never excuses a missing landing.

## Landing doors (author drives until landed)
- Door A — direct write to main via the App/bypass identity (standing approval covers the Smart Notes folder). The main-seat gh identity has NO bypass (direct ref PATCH = 422). Request the carry ON the board naming the exact built commit + branch; FOLLOW UP until the ref moves. An unanswered request is not a landing (SN-1771).
- Door B — dock-merged PR through the full scored process.
After a Door-A landing, close the record PR as superseded; never merge a stale registry regen from it.

## Verification — author, personally, in order (all four = VERIFIED_LIVE)
1. Tree: the file exists at its exact path on main (contents API / tree read — never a push receipt).
2. Feed: the note's OWN entry in the live baked feed array (IB id + title) — a textual mention inside another note does not count.
3. Page: GET nayanet.live/s/sn#### == 200.
4. Share image: GET the note's share image == 200.
Any byte edit after verification restarts this sequence. Deliver to Shawn = the feed link + the own-page link.

## Tracking (the intelligence ledger)
Countable in the Smart Ledger / dashboard along: total; per category; per author (human or seat); per day/week/month/year; filed-vs-visible delta (tree count vs live feed count — nonzero = a defect list, each item named); voiced count. All stats COMPUTED from tree + live feed at read time; hand-entered numbers are violations. Census at V1: 639 files / 619 unique SN ids / 16 filing days; taxonomy drift present (593 files under one topic beside variant spellings) — normalization is owed work under this protocol.

## The Intelligent Event (mandatory outputs of a verified landing)
(1) Hub notification; (2) the note's NUTSHELL in Today's Intel, linked; (3) activity-feed entry (what/whose/when) with a Smart Link to /s/sn####. State at V1: feed card LIVE; Intel nutshell + activity event NOT wired (Today's Intel renders fixed fixtures, 2026-10-21 room audit) — owed build work; never claim the event layer works until all three verify live for a real note.

## Distillation events (standing rhythm)
Raw filed notes are ORE; surfaced intelligence is DISTILLED ESSENCE. Cadence daily/weekly/monthly/yearly, each level distilling the level below; target ≤ ~50–100 essence blocks per scope. NEVER delete a lesson that matters — distillation compresses and surfaces; raw notes stay archived in the brain. Dumping raw volume into the Hub violates this protocol like an uncategorized filing. Recurring habit with named owners, not a project.

## Failure modes (observed; prevention named)
request-assumed landing → ghost note (verify personally) · topic-less path → UNCATEGORIZED render (path is correctness) · duplicate filing → split counts/tabs (dedupe at Step 0; edit, never fork) · label-as-title → unread note (viralize) · non-IB filename → no share page/art (filename == IB id) · empty core section → silent ingest refusal (nine complete sections) · done-at-creation → false report (terminal states only) · edit-and-walk-away → silent card change/vanish (re-verify) · guaranteed-timing claims → falsified by observation (honest state, §Pipeline.4) · unpadded scan patterns → missed zero-padded filings (scan both forms).

## Roles
Author (any seat): end-to-end owner. Bridge lane (Nitro): sync, share assets, rebake, bake-on-publish. Different seat: quality verification for protocol-level changes. Shawn: any human may order a note with "smart note this"; his word in the moment outranks this protocol, which is updated the same day to match.
