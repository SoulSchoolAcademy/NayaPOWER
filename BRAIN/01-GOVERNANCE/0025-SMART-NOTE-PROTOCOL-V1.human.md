# The Smart Note Protocol — V1 ULTIMATE (human tongue)

*The single canonical home for everything about Smart Notes. Ordered by Shawn Vibert, 2026-10-21. This text merges two drafts — Resolve's 0025 (PR #2850) and Nitro's recommendations draft of the same day — each scorecarded by the other seat's evidence, keeping what scored and curing what didn't. SN-0810 remains the worked example. If any other document's Smart Note procedure disagrees with this one, this one governs.*

## 1. What a Smart Note is

A Smart Note is how intelligence enters NayaNET and stays: one idea, lesson, decision, or discovery, told completely — so a human gets it in seconds, a child and a grandma get it too, and a machine can file, find, speak, and share it without guessing. It is the unit the whole hive learns in. A note that isn't in the Hub doesn't exist for the hive, no matter where it was written.

## 2. How it flows — Sender → Bridge → Receiver

The author writes the note and lands it on GitHub **main — the only door**. The bridge (an automatic sync) scans main's tree, reads each new or changed note, derives its category from its filing path, files it into the Hub's table, mints its share page and card art, enqueues its voice, and refreshes the Hub. The receiver — any human opening the Hub — sees the card in the feed, taps through to the note's own page, listens in Naya's voice, and shares it onward.

## 3. The laws

1. **One note, one truth.** One canonical note per idea, at one canonical path. Corrections edit the note; they never fork it. (The same note filed twice under two categories is a defect, not a backup.)
2. **Category from the path.** The category is *structural*: the bridge derives it from the filing path's TOPIC segment. TOPIC is chosen by what the note is **about** — never by what kind of note it is. No topic segment, no landing.
3. **The Viral Law.** The headline is the greatest-possible hook for a human reader — crafted, scored, rewritten until a busy stranger would tap it. IDs, kinds, and topics are small print. A label is not a title.
4. **Nine sections, in order.** Each section translates the same truth for a different reader; each may be short; none may be absent.
5. **The filename is the ID.** The file is named by its full IB identifier — that name is what the share page and card art are minted from. Any other filename = a note that half-exists.
6. **Main is the only door.** Local files, branches, PRs, and chat messages are drafts and handoffs, not notes.
7. **The author follows it through.** Four verifications, run personally by the author, before the word "done" is spoken (§7).
8. **Voice at publish.** Rendering starts at landing — nutshell first — never at a reader's click.
9. **Never announce a ghost.** No completion claim without the four verifications. A stalled note is reported as stalled, with the failing step named.
10. **The intelligence is counted.** Every note is a tracked unit (§8): totals, per category, per author, per day/week/month/year, filed-vs-visible, voiced — computed, never hand-typed.
11. **Every landing is an Intelligent Event.** Notification, Today's Intel nutshell, activity-feed entry with a Smart Link (§9). A silent landing has only half-arrived.
12. **Distill, don't dump.** The Hub's surfaced intelligence is distilled essence on a daily/weekly/monthly/yearly rhythm (§10). Raw volume buries the intelligence it claims to share.

## 4. Viralize — category, headline, ultimate hook

A note is authored in this order: **category → topic headline → ultimate hook → the nine sections.** Shawn calls this discipline **viralize**: every note is made to be read, not merely filed. The hook is scored honestly before landing — *would a busy stranger tap this?* — and rewritten until the answer is yes (target: 9+ on the stranger-tap test). The subheadline carries the plain-English promise of what the reader gets.

The finished note is a **one-minute Intelligent Block** with three first-class reading paths: **skim** it (the Nutshell and headings carry the whole), **listen** to it (play — Naya's real voice), or **read** it fully. It is presented beautifully — elevated boards, big clear text — and it is **distilled**: the essence in the most simple, clear, concise words that keep the truth whole.

## 5. Categorization — structural, mandatory, no exceptions

The canonical path is part of the note's correctness, not bookkeeping:

`BRAIN/05-MEMORY/SMART-NOTES/YYYY/MM/DD/<TOPIC>/<theme>/SN-####/IB-SMART-NOTE-YYYYMMDD-sn####-<slug>.md`

- TOPIC comes from the brain's existing taxonomy, chosen for the note's subject. The `**Category:**` line inside the note must match the path.
- **"UNCATEGORIZED" is forbidden.** It is what the bridge renders when a filing has no topic to derive from — a malformed filing, 100% preventable at the moment of filing. A note rendered UNCATEGORIZED is not done, even if visible; its author re-files it under its true path.
- One canonical spelling per category, everywhere (case-sensitive): variant spellings (`system` vs `SYSTEM`) silently split the counts and the tabs.
- If no existing subtopic fits, create one deliberately — named for the note's true domain — and record the creation in the note's NAYA section.
- The feed obeys the same law: notes surface **by category under Smart Tabs**, never as one endless river. The category is the note's address in the Hub, not just its folder.

## 6. The nine sections — in order, none missing

**IN A NUTSHELL / THE HUMAN VERSION / FOR A CHILD / FOR GRANDMA / FOR NAYA / FOR THE MACHINE / WHAT IT ALL MEANS / WHAT'S IN IT FOR YOU / HOW IT APPLIES.**

This is not ceremony: the bridge requires a non-empty Nutshell or Human section to ingest a note at all — a missing core section makes the note invisible, silently. The Nutshell must stand alone. The Machine section must be executable truth (parseable values), not prose about the idea.

## 7. The procedure — the triple-A pass

- **Step 0 — Declare and dedupe.** Name the idea; scan the corpus for it first — duplicates die here (Law 1). Claim the next free number in your sequence (scan main's tree + open claims; first claim stands; never reuse).
- **Step 1 — Category.** Choose the TOPIC by subject (§5). This decides the path, the tab, and the counts.
- **Step 2 — The hook.** Viralize (§4): headline as the ultimate hook, scored; subheadline as the plain promise.
- **Step 3 — The nine sections.** All nine, in order (§6).
- **Step 4 — Metadata, filename, path.** `**ID:**`, `**Created:**`, `**Category:**` (== path TOPIC). Filename == full IB id. Path == the canonical template.
- **Step 5 — Three scorecard passes.** Hook, truth, completeness — scored separately; nothing ships below 9 on any pass.
- **Step 6 — Land on main.** Direct write (Smart Notes folder, standing approval) or a PR the dock merges. Either way the author watches it arrive — a request handed to another lane is a handoff, not a landing.
- **Step 7 — Voice.** Confirm the render enqueued at landing, nutshell chunks first.
- **Step 8 — The four verifications.** (1) The file is on main — read the tree, not a receipt. (2) The card renders in the Hub feed. (3) `nayanet.live/s/<id>` answers 200. (4) The share image answers 200. All four true = **VERIFIED_LIVE**. Anything less = **STALLED:<failing-step>**, named and still owned by the author. Any later byte edit to the note restarts Step 8.

## 8. Tracking — the intelligence is counted

What isn't tracked isn't managed. The Smart Ledger and the data dashboard show, computed from the brain's tree and the live feed — never hand-typed, never estimated: **totals** (how many Smart Notes exist), **by category** (the shape of what we know), **by author** (each person's and each Naya's contribution, visible to them), **by time** (day/week/month/year — the compounding made visible), **filed vs visible** (any gap is a defect list with names on it — invisible notes found by arithmetic, not by accident), and **voiced** (how many carry Naya's real voice). The census at this protocol's writing: 639 files, 619 unique notes — and visible taxonomy drift (one topic holding 593 files beside three variant spellings), which is why §5's spelling law is a tracking law too.

## 9. The Intelligent Event — everyone is notified

Every verified landing announces itself in three places: (1) **a notification in the Hub**; (2) **Today's Intel** — the note's nutshell in the daily intelligence play, linked to the whole; (3) **the activity feed** — an entry (what the intelligence is, whose it is, when it happened) carrying a **Smart Link** to the full Intelligent Block. Nayas and humans alike are notified of the intelligence, where it lives, and when it happened.

*Honest state at V1: the feed card is live; the Today's Intel nutshell and the activity-feed event are owed wiring (Today's Intel still renders fixed fixtures) — tracked build work under this protocol, never claimed working until all three surfaces verify live for a real note.*

## 10. Distillation events — essence in, ore archived

The Hub does not receive the raw pile. Filed notes are ore: their intelligence is real, but no human reads hundreds of them. The living intelligence is **distilled on a rhythm** — daily (the day's notes → the day's essence), weekly, monthly, yearly, each level keeping only what the level below proved matters — toward a target shape of **roughly 50–100 essence blocks per scope**, in the wisest form, the fewest words, the smallest data that keep the truth whole.

Guard rules: **we never delete a lesson that matters** (distillation is compression, not disposal; raw notes stay archived in the brain); **distill, don't dump** (raw volume into the Hub violates this protocol like an uncategorized filing); **it is a habit with named owners, not a project.**

## 11. Voice — play means Naya's real voice

Pressing play reads the note in Naya's real cloned voice, never the robotic fallback. The player first looks for the note's baked narration; Law 8 puts the bake at publish so the real voice is there from the first play. A reader's first click may wait briefly while rendering finishes; no click ever *starts* a bake. If play falls back to the robot voice, the bake didn't happen — a defect to fix, not a setting to accept.

## 12. Failure modes — what NOT to do, and why

| Failure | What actually happens | The cure |
|---|---|---|
| Request a landing and assume it | The note never arrives; the hive believes a ghost (SN-1771) | Law 7 — the author verifies, personally |
| File without a TOPIC segment | The card renders UNCATEGORIZED (SN-1773/1774 pattern) | Law 2 — the path is part of correctness |
| File the same note twice | Two homes, split counts, confused tabs (SN-1773's two filings) | Law 1 — one note, one truth; dedupe at Step 0 |
| Title the note with its kind or label | Nobody taps it; the intelligence dies unread | Law 3 — hook first; labels are small print |
| Name the file anything but the IB id | No share page, no card art — a note that half-exists | Law 5 |
| Skip or empty a core section | The bridge cannot ingest the note; silence | Law 4 — the parser requires Nutshell/Human |
| Announce "done" at creation | A false report; trust in every later report drops | Law 9 + SN-0812 |
| Edit a landed note and walk away | The card may change or vanish unobserved | Re-run Step 8 after any edit |
| Claim the sync's timing as guaranteed | Documented cadence ≠ observed behavior (SN-0812: no card >7 min after a canonical bot landing) | Verify live (§7 Step 8); the streamline is owed work, not a promise |

*Pipeline honest state (root-caused 2026-10-21): the bridge is an identity-blind tree scan by construction — when a landed note doesn't appear, the cause is a run that didn't complete or a file that isn't on main, never the carrier's identity. The documented ≈5-minute cadence is nevertheless UNVERIFIED by observation; until the streamline (machinery in the repo, push-triggered run, reconciler + heartbeat) lands and is acceptance-proven, the author's Step 8 is the only reliable detector, and no seat states a note "will appear in seconds" as a fact.*

## 13. Roles

- **Any human** can say "smart note this" about anything, any time.
- **The author** (any Naya seat) owns the note end-to-end: dedupe, category, hook, sections, filing, landing, voice, the four verifications, the link delivered.
- **The bridge lane** (Nitro) owns the sync, the share assets, the rebake, and bake-on-publish. The bridge is machinery: it owes the author nothing and forgives nothing — feed it exactly right.
- **A different seat** verifies quality at the bar for protocol-level changes; routine notes are verified by their author's four checks.
- **Shawn's word in the moment** outranks this protocol — and the protocol is updated the same day to match it.
- **Every other Naya** learns the protocol from this document. No seat should ever have to ask how a Smart Note works.

## 14. The standing rulings carried by this protocol

- Done = visible in the Hub feed, four verifications, link as proof (Shawn, 2026-10-21; Nitro R5).
- Viralize: category → topic headline → ultimate hook; the greatest-possible hook is mandatory (Shawn, 2026-10-21).
- Categorization is structural and mandatory; UNCATEGORIZED is a malformed filing, never a category (Shawn + bridge mechanics, 2026-10-21).
- Tracking: the intelligence is counted, computed, six ways (Shawn, 2026-10-21).
- The Intelligent Event: notification + Today's Intel nutshell + activity Smart Link (Shawn, 2026-10-21).
- Distillation events: essence surfaces, ore archived, nothing that matters ever deleted (Shawn, 2026-10-21).
- Amendments land by PR through the scored process — the protocol about finishing things must itself always be finished: merged, verified, announced (Nitro, R8).
