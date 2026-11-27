# Auto Organizer — Proof Results

Engine: `../auto-organizer.js` (v1.0.0-20261126, with the evidence threshold added after run 2).
Spec: `../THE-AUTO-ORGANIZER-ALGORITHM.md`.
Runner: `run-proof.cjs` (Node, read-only Supabase via `sb-api`; overrides and learned rules live in memory in Node, in `localStorage` in the browser).
Corpus: the first 200 rows of `hub_smart_notes` (the table holds 1,000+ rows — the count query is limit-capped at 1,000; the proof is a 200-row sample, not the whole table).

## Run 1 — 2026-11-26 21:52:57–21:53:00 MST (before keyword cleanup)

`organizeAll()` over 200 rows: 0.264s.

| Subcategory | Count |
|---|---|
| General (home) | 114 |
| Technology & Gadgets | 32 |
| History, Science & Learning | 16 |
| Music | 15 |
| Reading & Literature | 8 |
| Fitness & Working Out | 7 |
| Podcasts & Audio | 3 |
| Writing & Storytelling | 2 |
| Photography & Videography | 2 |
| Travel & Exploration | 1 |

By source: keywords 86, home 114. By confidence: low 86, none 114.

**Finding:** the big buckets were all single-word noise — technology 32 all on "smart" alone (the system's own "smart note" boilerplate), music 15 mostly on "instrument" (12, meaning a tool, not music), history 16 mostly on "learning" (12, Naya's "learn in a minute" phrasing), fitness 7 all on "running" (the system running). The engine worked mechanically; the distribution on internal system notes was noisy.

## Keyword cleanup (evidence-driven, after run 1)

Removed 8 bare words the system's own daily language hijacks: `smart`, `instrument`, `instruments`, `performance`, `performer`, `learning`, `language`, `running`. Phrases kept: `smart home`, `playing instruments`, `language learning`. (Also already excluded from the start: `pc`, `mobile`, `tv`, `ai` as bare keys.)

## Run 2 — 2026-11-26 21:53:50–21:53:53 MST (after cleanup, before threshold)

| Subcategory | Count |
|---|---|
| General (home) | 173 |
| Reading & Literature | 8 |
| Podcasts & Audio | 4 |
| History, Science & Learning | 4 |
| Travel & Exploration | 2 |
| Writing & Storytelling | 2 |
| Photography & Videography | 2 |
| Cooking & Baking | 1 |
| DIY & Woodworking | 1 |
| Technology & Gadgets | 1 |
| Music | 1 |
| Fitness & Working Out | 1 |

By source: home 173, keywords 27. By confidence: none 173, low 27.

## Hand-check of run 2's 27 placements — every one read against its title and nutshell

**1 correct out of 27:**

- ✅ "Viral Factory: 100 Videos With No Camera, No Crew, No Excuses" → Photography & Videography, on `video` — the note is literally about making 9:16 videos. Correct.

**26 wrong — all single-word metaphor or passing mention:**

- "The Bounded Red Team Assignment Model" → Podcasts & Audio (`audio`) — about red-team assignments, not podcasts.
- "No Dashes in Domains" → Travel & Exploration (`travel`) — about domain slugs.
- "A Deployed URL Is Not the Deployed Product" → History (`history`) — about proving deployment currency.
- "The PDF Test" → Cooking & Baking (`recipe`) — about dataviz specs; "recipe" is a passing word.
- "Novelty Gets Its Own Score Axis" → DIY & Woodworking (`craft`) — about interface design; "craft" means craftsmanship.
- "Test the feedback path, not just the buttons" → Podcasts & Audio (`audio`) — about a Play button test, not audio content.
- "The Authorization Window Race" → Reading & Literature (`reading`) — about deploy authorization; "reading" = reading a response.
- "Building Fresh, Not on a False Memory" → Podcasts & Audio (`audio`) — about Naya Voice integration engineering, not podcasts.
- "Restraint Surgery — Elegance Is Subtraction" → Technology & Gadgets (`tech`) — about design composition.
- "After a PR-body PATCH, verify from the PATCH response itself" → Reading & Literature (`reading`) — engineering.
- "The Ingestion Bar" → Reading & Literature (`writing`) — about transferring his brain into the system.
- "Capture without a receipt check leaks intelligence into chat history" → History (`history`) — about capture; "history" is chat history.
- "Occupancy Scans Must Cover Merged PRs" → Reading & Literature (`books`) — about PRs; "books" is bookkeeping.
- "Teach New Guards About Legacy" → History (`history`) — about truth-state guards.
- "Live Bytes Beat Every Story" → Writing & Storytelling (`story`, `stories`) — the note is about verification, using "story" as a metaphor for reports.
- "Never Delete What You Don't Understand" → History (`history`) — "Records are history", metaphorical.
- "The Agreement Page Feel" → Music (`listening`) — about a page's feel.
- "Ledger APPLIED Is a Claim, Not a Proof" → Reading & Literature (`reading`) — engineering.
- "A local preflight verifier's green is bounded by its execution surface" → Reading & Literature (`reading`) — engineering.
- "Tune to Intent, Not to Words" → Reading & Literature (`reading`) — about dictation transcription.
- "A Regression That Only Greps for Presence Is Not a Guard" → Fitness & Working Out (`strength`) — engineering; "strength" is a passing word.
- "Design Contract v1.1" → Writing & Storytelling (`story`) — about contract amendments.
- "The Factory — The Reusable-Parts Law" → Travel & Exploration (`travel`) — about cloning pages.
- "The Mail Key Never Moved" → Podcasts & Audio (`audio`) — about a mail key; "audio" is a voice-call mention.
- "A Gate Must Declare Its Coverage Before Its Verdict" → Reading & Literature (`reading`) — engineering.
- "A Verification Packet Is a Photograph" → Photography & Videography (`photograph`) — the note USES a photograph as a metaphor for a packet; the subject is verification, not photography.

**General sample (5 of 173), all correctly General:** "The Future Is Now — Active Intelligence, Always Learning" · "The standing directive supersedes the roster" · "The Nonstop Loop — NayaPOWER Operating Code" · "RESOURCE-CONSTRAINED EXECUTION LAW (proposed)" · "Two sign-outs were posted for the same 13:01 PDT brain-drive tick". All system notes with no interest content. Correct.

**Verdict of the hand-check:** a single generic word is NOT evidence. 26 of 27 score-1 placements were wrong. That is what forced the threshold.

## The threshold (added after run 2)

A placement now needs REAL evidence: total score ≥ 3, or one real phrase hit (weight ≥ 2). Below that, the item goes home with the best subcategory recorded as a **suggestion** the citizen can confirm or move. The system suggests; it does not fake.

## Run 3 (final) — 2026-11-26 21:57:18–21:57:24 MST

- Rows pulled: 200. `organizeAll()` over 200 rows: 1.8s (21:57:22.344 → 21:57:24.128). Whole proof end to end: 5.8s.
- **Distribution: General 200, placements 0, suggestions 27** (the same 27 as run 2's placements, now suggestions, not placements). By source: home 200. By confidence: none 200.
- Suggestions by subcategory: Reading & Literature 8, Podcasts & Audio 4, History, Science & Learning 4, Travel & Exploration 2, Writing & Storytelling 2, Photography & Videography 2, Cooking & Baking 1, DIY & Woodworking 1, Technology & Gadgets 1, Music 1, Fitness & Working Out 1.

That is the honest shape for a corpus of internal system notes: nothing in them belongs in an interest category, and the engine no longer pretends otherwise.

## Live items (run 3, same timestamps — all placed in under a second)

1. **New smart note "Sourdough on Sunday — what the slow rise taught me"** — 21:57:24.230 MST → **Food & Drink / Cooking & Baking**, score 5, medium, keywords `cooking`, `baking`, `home cooking`, `recipe`. Match handoff: `{itemId: live-note-1, type: note, category: Food & Drink, subcategory: Cooking & Baking, keywords: [cooking, baking, home cooking, recipe], owner: null}`.
2. **Post "Sunrise on the Elk Trail — five quiet miles before the town woke up"** — 21:57:24.241 MST → **Outdoors & Travel / Hiking & Nature**, score 7, high, keywords `hiking`, `trail walking`, `trail`, `birding`. Match handoff included.
3. **Contact Mara Ellison** (violin, community orchestra, never misses a concert, teaches piano; interests concerts, playing instruments) — 21:57:24.242 MST → **Entertainment & Media / Music**, score 5, medium, keywords `concert`, `concerts`, `playing instruments`. Match handoff included.

## User move overrides (run 3)

- 21:57:24.312 MST — the citizen moves the trail post to **Travel & Exploration**. Re-organize returns **override, score 10, high** — the override wins.
- Learned rule taught by that move: `travel-exploration` keywords `trail walking`, `hiking`, taughtBy `live-post-1`, at 2026-11-27T04:57:24Z.

## Learning test (run 3)

- 21:57:24.317 MST — second similar post: "Morning trail walking on the ridge, then a road trip home" → **Outdoors & Travel / Travel & Exploration**, score 5, medium, reasons `road trip`, `trip`, `learned:trail walking`. **Without the rule, Hiking would win 4–3.** The move taught the engine; the next similar post lands right the first time. PROOF END 21:57:24.317 MST.

## Browser proof (staged page)

`proof.html` runs the same five live items in a real browser and lets the citizen type their own item and watch where it lands. Verified in Chromium 159 headless, 2026-11-26 ~22:01 MST: all five cards render exactly as the Node proof — note Cooking & Baking score 5, post Hiking & Nature score 7, contact Music score 5, move override Travel & Exploration score 10, learning post Travel & Exploration score 5 with `learned:trail walking`. The page carries an **inlined copy** of `auto-organizer.js` v1.0.0-20261126 (threshold build) so it works standalone on the proof host — if the engine changes, re-inline from `../auto-organizer.js` and re-verify the five cards. The page clears its own demo overrides on every load so yesterday's moves never change today's proof.

## What the proof proves, and what it does not

- **Proves:** the engine places real items with real evidence (3/3 live items, correct), the override always wins, a move teaches the next similar item, the match handoff carries category + keywords + reasons for Smart Match, and — after the threshold — it does not fake placements on a corpus where nothing belongs in a category (0/200 placed, 27 suggested).
- **Does not prove:** placement accuracy on real citizen content (the corpus is system notes; citizen posts/notes use life language, where the keywords are meant to fire). That is the next measurement, once real citizen items run through it.
- **Known limitation:** a real citizen post that uses none of the taxonomy's words ("Made sourdough today, the starter finally worked" — no `cooking`/`baking`/`recipe`) scores 0 and goes home. The vocabulary grows only from citizen moves today, and a moved item with no matched keywords teaches nothing yet (open item 6 in the spec).
