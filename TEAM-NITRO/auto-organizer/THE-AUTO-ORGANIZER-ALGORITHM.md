# THE AUTO ORGANIZER ALGORITHM

**Shawn's order, voice call 2026-11-26 ~21:35–21:43 MST ("Okay, so let's get her done").**
His words, kept verbatim:

> "write an algorithm that using like just simple logic even categorization even as simple as a library, you should be able to auto organize these feeds where it just like it makes sense that these things would go together and they would be categorized that way. So intelligence should always be looking at a way to organize things intelligently and I'm pretty sure you can just make it so it's automatic where it just knows how to categorize it because it looks oh this goes with this, let's put those together, right?"

> "our smart notes even the posts and even our what we put in the whole system sort of works that way. Where it just auto organizes itself. Even our contacts, even our smart note lists, our even our own notes. Everything the whole system just auto organizes with intelligence and you can choose to always change those categories or move one thing from another but our system goes out of its way to try to organize things for you in the most intelligent way. Like by default."

> "auto organizer is sort of auto match kind of work together one's doing organizing, one's doing matching. They're a little bit different, right? But they work together... in sync with the Smart Vault or the Nanonode because you want everything to be organized and to be matched up properly within it, right? So then the system, they all work together."

> "we're taking like basically gigs of memory and turning it into active intelligence that is auto-organizing becoming a nano node that is a smart vault or memory system. For the users to store their digital assets and intelligence."

## In a nutshell

Every new thing — smart note, post, contact, list, or the citizen's own note — is a book arriving at the library. The Organizer reads its cover and its first page, looks at the words on the shelves, and puts the book on the shelf where the most words match. The citizen can always move a book to another shelf, and the move always wins — and the Organizer remembers which words taught it, so the next similar book goes to the right shelf the first time. Then it hands the placed book to Smart Match, which pairs it with the right people. All of it happens inside the Smart Vault / Nano Node, by default, in seconds.

## The simple logic (the whole algorithm, in plain words)

1. **Read the cover and the first page.** For a note: its topics (if it has any), title, nutshell, and the first ~1,200 characters of its body. For a post: title + body. For a contact: name, alias, about, and shared interests. For a list: its name and its items' titles. That text is the haystack.
2. **Score every shelf.** Each of the 25 subcategories has a list of words (below). A word found in the haystack scores: a long phrase (over 12 characters) = 3, a phrase with a space = 2, a single word = 1. Most points wins. Every subcategory scores independently; a word can count on more than one shelf.
3. **The citizen's own labels win ties.** If the item's topics name a subcategory outright, that is a direct hit (+10). If the item's topics name a major category, only that major's shelves are scored. If the citizen's Q14 picks include a subcategory, it gets +2 — their declared interest breaks ties.
4. **A move teaches.** When the citizen moves an item, the move is recorded and the item's two strongest words gain +2 toward the new shelf for future items. A later move of the same item retracts its old lesson. Lessons cap at 50, oldest first.
5. **The citizen's move always wins.** An override is checked before any scoring. Nothing outranks it.
6. **A single word is not evidence — the threshold.** A placement needs REAL evidence: total score ≥ 3, or one real phrase hit (weight ≥ 2). Below that, the item lands at home — the major the item already named, else the citizen's first picked interest, else General — with confidence "none" and the reason written on it, plus the best-scoring subcategory recorded as a SUGGESTION the citizen can confirm or move. The system suggests; it does not fake. (Measured, proof run 2, 2026-11-26 21:53 MST: hand-checking 27 score-1 placements on real notes found 26 wrong — metaphor or passing mention: "reading" the response, "story" as metaphor, "travel" in passing. After the threshold, run 3 placed 0 of 200 real notes and suggested on 27 — the honest shape for a corpus of system notes.)
7. **The category is never guessed separately.** Each subcategory belongs to exactly one major category, so the major is derived from the winning subcategory. One decision, not two.
8. **Hand it to Match.** The placement goes to Smart Match as `{itemId, type, category, subcategory, keywords, owner, reasons}`. The Organizer does NOT compute match percentages — Match owns that, through the privacy gate, with reasons attached.

## What it is built on (harvested, not invented)

| Piece | Source (harvested byte-for-byte in logic) |
|---|---|
| Keyword scoring, weights 3/2/1, most-hits-wins, home-cluster default | `intelClusterOf` in the Hub (`hub-unified-20261124/r20/hub-live-R12-BASE.html`, smartTabStrip area) and its server twin `team-nitro/public-blog-seo-20261112/hub-worker-intel-today.js:451` |
| Tabs are the Organizer's face: All + system tabs + per-topic tabs + human tabs | `smartTabStrip` in the same Hub file (line ~7925) |
| Override storage: device-local JSON, in-memory fallback | Human-tabs pattern, `localStorage['nayanet.feed.smartTabs.v1']` |
| Move UI: a `.tab-menu` panel of `.mi` items, outside-click/Escape dismisses | Category picker `openCategoryPicker` in the same Hub file |
| Tab colours: Gematria by first letter; pill flow | `GEMATRIA_NUM` / `PILL_FLOW` in the same Hub file (untouched) |

**One hardening over the harvested pattern:** keywords match on word boundaries, not raw substrings. The harvested `indexOf` would let the 2-letter key "ai" match "said", "again", "training", and "tv" match "active". Same weights, same scoring — safer matching. Do not "fix" it back to `indexOf`.

## The shelves (settled taxonomy)

6 major categories, 25 subcategories — his list, web 2026-11-26 ~18:49 MST. Keyword lists are built ONLY from his two word lists (that structured list + the first-10 list, chat 2026-11-26 ~18:44 MST): label words + description words + their plurals.

- **Entertainment & Media:** Music · Movies & Television · Gaming · Reading & Literature · Podcasts & Audio
- **Food & Drink:** Cooking & Baking · Dining Out & Food Culture · Coffee, Tea & Craft Beverages
- **Health, Fitness & Sports:** Fitness & Working Out · Spectator Sports · Recreational & Team Sports · Mental Health & Mindfulness
- **Outdoors & Travel:** Travel & Exploration · Hiking & Nature · Gardening & Houseplants · Pets & Animals
- **Arts, Crafts & Making:** Visual Arts · Photography & Videography · Fiber & Textile Arts · Writing & Storytelling · DIY & Woodworking
- **Lifestyle, Tech & Knowledge:** Fashion & Personal Style · Home Decor & Interior Design · Technology & Gadgets · History, Science & Learning

The full keyword list per subcategory lives in `auto-organizer.js` (`TAXONOMY`). Every keyword traces to a word in his lists.

**Words deliberately left out, with measured reasons (proof run 1, 200 real notes, 2026-11-26 21:52 MST):**
- `pc` and `mobile` (from "Video Games & Gaming (console, PC, mobile, online competitive)"): as bare substrings they would file every phone/tech note under Gaming. `console` and `online competitive` carry that shelf instead.
- `tv` and `ai` as bare keys: 2-letter substrings match inside ordinary words ("active", "said"). Only the phrases `ai tools` and `pc building` are kept.
- `smart` (Technology & Gadgets): run 1 placed 32 notes there, ALL on the single word "smart" — the system's own "smart note" boilerplate in every nutshell. Removed; `smart home` (phrase) stays.
- `instrument`, `instruments`, `performance`, `performer` (Music): run 1 placed 15 notes there, 12 on "instrument" — system notes use "instrument" to mean a tool/means, and "performance" to mean system performance, not music. Removed; `playing instruments` (phrase) stays.
- `learning`, `language` (History, Science & Learning): run 1 placed 16 notes there, 12 on "learning" — Naya's own "learn in a minute" phrasing. Removed; `language learning` (phrase) stays.
- `running` (Fitness & Working Out): run 1 placed 7 notes there, ALL on "running" — system notes use "running" to mean the system running, not the exercise. Removed; `working out`, `workout`, `strength`, `yoga`, `pilates`, `home workouts`, `swimming` stay.

After those removals (run 2), placements on the same 200 notes are driven only by distinctive words — see `proof/PROOF-RESULTS.md`. The lesson, kept as law: **a keyword that the system's own daily language uses is not a keyword.** Measure every keyword against the real corpus before trusting it.

**Known collisions (shared words, documented, not hidden):** `journaling` scores in Reading & Literature, Writing & Storytelling, AND Mental Health & Mindfulness. `writing` scores in Reading & Literature and Writing & Storytelling. `film` scores in Movies & Television and Photography & Videography. `gardening` / `camping` score in Hiking & Nature and Gardening & Houseplants. `organizing` scores in Home Decor & Interior Design — so a note about the Auto Organizer itself will lean that way on that word alone. `learning` scores in History, Science & Learning — and Naya's own "learn in a minute" phrasing contains it, so system notes lean that way on that word alone. Ties break by taxonomy order, then citizen picks, then learned rules. A placement with score 1–2 never places at all now (step 6) — it becomes a suggestion, so the citizen sees why and confirms or moves it.

## The topics level (ready, not invented)

The output shape is `{category, subcategory, topic: null, topicReady: true}`. `TOPICS` starts empty. `setTopics(list)` loads it the moment he gives the list; it validates that every topic names a real subcategory and rejects the list otherwise. **The topics list is his call — the captain's six-area proposal (identity and memory; work and business; spaces and worlds; projects and creation; connections and matches; learning and growth) is a CANDIDATE, not a ruling. Nothing about topics is invented.**

## Where it lives in the code

- **Engine:** `TEAM-NITRO/auto-organizer/auto-organizer.js` — dependency-free, runs in the browser and in Node. Exports `organize`, `organizeAll`, `moveItem`, `clearOverride`, `matchInput`, `setTopics`, `TAXONOMY`, `learnedRules`, `overrides`.
- **Face:** the Hub's Smart Tabs (`smartTabStrip`). At note-load time the feed calls `organize(item, ctx)` and stores the result on the note as `note.organizer = {category, subcategory, topic, confidence, reasons, source}`. The tab strip then shows the item under its category tab. **The Hub file itself is NOT touched by this build** — Hub R20 owns that file (one lane, one round); the Hub lane includes the engine next, by loading this file before `smartTabStrip` and calling `organize()` at load.
- **Placement is computed on read, not stored in the database.** `hub_smart_notes` has no category column (verified 2026-11-26: columns are author, child_note, created_at, github_path, grandma_note, how_it_applies, human_note, ib_id, id, machine_note, naya_note, note_created, nutshell, source, title, what_it_means, whats_in_it_for_you). No schema change is needed or made. The only stored piece is the citizen's override (device-local, like human tabs) — the Vault record carries the override when the sync path exists (open item, not invented).
- **Proof:** `TEAM-NITRO/auto-organizer/proof/` — `run-proof.mjs` (Node proof on real Supabase data), `proof.html` (staged in-browser proof), `PROOF-RESULTS.md` (timestamps + numbers).

## How it works with Smart Match and the Vault (the three systems, in sync)

1. A smart note enters the intelligence system → **Smart Vault** (it is saved there from day one).
2. **Auto Organizer** places it — category, subcategory, reasons — on read, by default, in seconds.
3. **Smart Match** takes the placement (`matchInput`) and pairs the item with the right people, through the privacy gate, with reasons attached. Organizer places; Match pairs. Different jobs, one flow.
4. **Smart Lists** carry it, organized through the Organizer — the tabs are the Organizer's face.
5. Everything happens inside the citizen's Nano Node — their Smart Vault — so it is organized AND matched properly within it, and it travels with them from Personal into Business and Space.

## What is still open

1. **Topics list** — his call. The engine is ready; the list is not invented.
2. **Smart Match endpoint** — the `matchInput` handoff object is defined and proven; the Match percentage itself is Match's job, and its note-surface endpoint decision is still open. The proof shows the handoff, never a faked match %.
3. **Hub inclusion** — the engine is filed and proven on staging; the Hub lane (R20, running) includes it next by loading the file and calling `organize()` at note-load time. Not forced into the R20 file while that round runs.
4. **Cross-device overrides** — overrides are device-local today (same as human tabs). A Vault-synced override record is the follow-on, not invented here.
5. **Keyword collisions** (above) — the tie-breaks hold; a learned-rule pass over real citizen data will sharpen them over time. The engine learns from moves, so this improves with use.
6. **Vocabulary growth from moves** — a moved item with no matched keywords teaches nothing yet (there are no keywords to teach). The follow-on: learn the moved item's most distinctive words as new keywords for its shelf — driven by real citizen moves, never invented here.
