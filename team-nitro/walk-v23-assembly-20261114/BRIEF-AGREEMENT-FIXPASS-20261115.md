# BRIEF — AGREEMENT FIX PASS (fix round → fix pass, 2026-11-15)

**Status:** brief for a focused fix pass. The fix round is NOT WHOLE — coordinator verdict NOT WHOLE, 12/14 pass, 2 fail. This pass fixes exactly those two fails and touches nothing else.

**Due:** 2026-11-15T05:30Z · **Owner:** captain
**One List item:** `agreement-v4-naya-voice-portraits` — stays dispatched; this fix pass is its continuation, not a new item.
**Coordinator:** to be dispatched on this brief (check-brief 9/9 required before dispatch). The captain dispatches — the brief-writer does not.

## The order behind it

The fix round completed with 12 of 14 items passing and all six no-regression guards passing. The two fails are small and named, each one named thing, not a general unravelling. This pass closes them both in one round, on the same page, and the page then comes to Shawn whole.

## DONE FIRST — what done looks like, defined before the work

The exact element is the agreement step on the walk's /welcome page — board 58 and the portraits on the §4 run and in the eye notes, on the fix-round file. The exact change is: board 58's first paragraph is split so no board anywhere exceeds 4 sentences, and the b02 ×11 eye-note repeat is broken while faces are put into the §4 run from the remaining face-library pictures. The exact measurement is: every board 1–4 sentences, proven by a sentence count, not a paragraph count; no single portrait file illustrates more than 2 eye notes; the §4 run carries faces on at least every third board; no two adjacent boards share the same portrait. What must NOT be there: no board over 4 sentences, no portrait illustrating more than 2 eye notes, no 40-board faceless run, no changed Official word, no new defect in any of the 12 passes or 6 guards.

## Base file

The base file for this pass is the fix round's filed file — the build the checker checked, nothing else. This pass is an edit to the base file, never a fresh build. File `~/workspace/team-nitro/walk-v23-assembly-20261114/walk-beginning-fixed.html`, 3,493,483 B, sha256 `7553d76bf2067d60838ec94894d4952acd2a1a8772802727f845f01a79d60af2`, served at `https://naya-walk-beginning-staging.nayapower.workers.dev/welcome` (worker `naya-walk-beginning-staging`). New branch: `agreement/fix-round-20261115-fixpass`. (The round's maker record names no git branch — the round deployed in-memory to the staging worker — so this branch name is the new one.) Records of the round just completed: `~/workspace/team-nitro/walk-v23-assembly-20261114/MAKER-RECORD-AGREEMENT-FIX-ROUND-20261115.md` and `~/workspace/team-nitro/walk-v23-assembly-20261114/CHECKER-RECORD-AGREEMENT-FIX-ROUND-20261115.md`. The round brief: `~/workspace/team-nitro/walk-v23-assembly-20261114/BRIEF-AGREEMENT-FIX-ROUND-20261115.md`. The deliverable is an edit to the base file: edit this file, never rebuild. The fix pass edits THIS file — it does not start a new worker, it does not touch the live site. Nothing goes live on this pass. Staging only, until Shawn's tap.

## Where it lives

The agreement lives on the walk's /welcome page — the staged worker's welcome step, the agreement step of the walk, before the world reveal and before pricing. It does not duplicate the walk's ten questions, the end/world reveal, or the pricing page — the agreement is its own step, and this pass changes only the agreement step. It does not duplicate the Personal, Business, or Space pages, and it does not rebuild the feed, the Dashboard, or the Hub. This pass is not a standalone page — it lives on the walk's /welcome page, and it duplicates nothing.

## Words source (the ONLY words source)

`~/workspace/team-nitro/walk-v23-assembly-20261114/COLLECTIVE-AGREEMENT-OFFICIAL-20261115.md` — the Official, 2,124 words, $25 (never $20), cancel line ends "That's the fair way to do it.", Q5 in Shawn's words, "I'm not an LLM" present, last line "nayanet.app — enter.". The Official is the words source. No other text file is a words source. If a line in the Official conflicts with a line on the v4 build, the Official wins. **The fix pass must not change one word of the Official on the page** — splitting a board moves sentences between boards; it never rewrites, drops, or adds a word.

## ITEM 1 RULING — carried in this brief so the next maker does not re-fight it

The Official contains "governed by the applicable published agreements" (×1) and "the intended default is seven days" (×1) — verified first-hand by the maker and by the checker, each grepping the Official file itself. The round brief demanded both Official-verbatim AND a 0-grep on those phrases; both cannot hold. The brief's own words-source rule decides it: "If a line in the Official conflicts with a line on the v4 build, the Official wins." The two phrases are Shawn's ratified Official words — they survived his 01:57Z read-through line edits. **The fix-pass maker must NOT delete or alter them.** If the checker flags them again, the coordinator rules PASS on the same ground and flags them for Shawn, not the maker. The v4-only hedged forms ("Our planned privacy standard", "until the full retention system is implemented and independently verified") still read 0 — that half of the grep stands and is unchanged.

## THE ROUND VERDICT THIS PASS ANSWERS (read first)

Coordinator verdict: NOT WHOLE, 12/14 pass, 2 fail. The checker (Vera) verified the served bytes twice (3,493,483 B, sha `7553d76b…`, byte-exact both fetches) and walked the whole flow from the login page, by eye, phone first then desktop, at true viewports 360×800, 390×844, 1440×900, 1920×1080, at scroll 0 AND scrolled, zero console errors. **Passes (12):** items 2 (hook screen), 4 (one button), 5 (white text), 7 (signing bigger at all widths, 1.6–1.8×), 8 (eyes open 14/14), 9 (eyes jewelry-level), 10 (corner gems inside), 11 (360px overflow gone at true 360px), 12 (wax seal), 13 (founders line verbatim), 14 (keep-reading 82 clicks / 83 boards). All six no-regression guards pass. **Fails (2):** item 3 (board 58 carries 6 sentences) and item 6 (78 of 83 boards carry no portrait; the §4 run has no face at all; /agmt-b02.jpg illustrates eleven different §4 eye notes). Item 1 failed only on the hedged-grep clause — the verbatim half passed — and is settled by the ITEM 1 RULING above, not by a fix.

## THE FIXES — two, in one pass

### 1. BOARD 58 — THREE-SENTENCE LAW

One board carries 6 sentences. Board 58 (QUESTION 4 · 23 OF 42) reads: first paragraph alone holds 4 sentences ("I know what you might be thinking. "What's the catch?" "Is this a scam?" Those are fair questions.") + 1 + 1. The maker counted `<p>`s (3), not sentences — the brief's rule is sentences, and the checker counted sentences on all 83 boards, twice, and found this one board over 4. Fix: split that board's first paragraph so NO board anywhere exceeds 4 sentences. The split is at sentence boundaries, never mid-sentence, and moves sentences between boards — it never rewrites, drops, or adds a word (see Words source above). **Count sentences, never `<p>` elements:** a paragraph can hold four sentences, and a board can hold several paragraphs. **Proof:** Vera re-counts ALL 83 boards sentence by sentence (never by `<p>` count) — every board 1–4 sentences. The keep-reading behaviour follows the new board count (one board per click, in order, to the end); the progress gems track the new count.

### 2. PORTRAITS — VISIBLY DIFFERENT

78 of 83 boards carry no portrait; the §4 run (boards 37–77) has no face at all; and /agmt-b02.jpg illustrates ELEVEN different §4 eye notes (12 occurrences in the served file: 1 board portrait + 11 notes). A reader opening several §4 notes sees the same portrait eleven times. Fix, in two parts: (a) break the b02 ×11 eye-note repeat — rotate the note photos through the face library, or drop the photo from the notes; the maker's call, scorecarded in the maker record (ten loves / ten don't-loves / how to make it ten times better, with the choice and its reason written down); (b) put faces into the §4 run from the remaining face-library pictures. The section-board-only structure is arithmetically forced — 15 pictures, 83 boards, so a portrait on every board would force repeats — but a 40-board faceless run and one portrait eleven times are fixable defects, not forced ones. Seven distinct face-library pictures are still unused (the round used eight: top flank, five section boards, summary, signing); the maker draws on those seven first, and any reuse of an already-used picture on a §4 board must still satisfy the measurement below. Naya_Profile_black_full.jpg is byte-identical to Naya_Profile_2.jpg — never used twice. Sisters' faces are never Naya's voice. **Proof:** no single portrait file illustrates more than 2 eye notes; the §4 run carries faces on at least every third board; no two adjacent boards share the same portrait. The checker opens every changed portrait full-size and confirms no two adjacent boards read as the same portrait.

## NO-REGRESSION GUARDS — all 12 round passes + 6 guards must still hold

The fix pass touches nothing else. Vera sweeps all of these on the new served bytes; a fail on any one fails the pass:

- **Official words verbatim** (sentence/word-level, zero board words outside the Official, zero Official board-words missing) — the two phrases in the ITEM 1 RULING above stand as Official words.
- **Hook screen** — one photo at the top, "Hi, I'm Naya" beside it, no big portrait inside the board, no "THE ROYAL MANUSCRIPT" / "THE HOOK · WHAT IT IS" labels, title "The Collective Agreement", five jump pills flush to the top, hook text verbatim.
- **One button only** — "Keep reading ◆" remains; WHAT'S NEXT? visible 0.
- **White text, never gray** — every text on the agreement page white on obsidian (section-kind labels in their designed tone colours, as before).
- **Signing bigger at ALL widths** — ~1.6–1.8× the board picture at 360, 390, 1440, and 1920.
- **Eyes open 14/14** — every eye opens on tap 1 and closes on tap 2, note top visible right below its eye.
- **Eyes jewelry-level** — faceted cabochons, never flat dots.
- **Corner gems fully inside viewport** — all four gems whole at every width.
- **360px overflow gone at TRUE 360px** — Playwright, scrollWidth = innerWidth, hook + fully unfolded, at 360, 390, 1440, 1920.
- **Wax seal, not a ring** — deep-red wax blob with gold N, stamps on agree, holds, then the world reveals with the 5 doors.
- **Founders line verbatim** — "The first 1,000 founders get half price, and double points once a thousand founders join."
- **"bonus" = 0 in the whole file** — and "blockchain" = 0.
- **Keep-reading** — one board per click, in order, through the whole re-split letter (82 clicks / 83 boards before this pass; the count follows the new board count after the split).
- **The end** — ONLY signing picture + "I agree — show me my world ◆" + "The Collective Agreement — between NayaNET and you. Welcome aboard."
- **Skip never signs** — no seal, "You skipped the agreement…" + "Read the agreement" link, same 5 doors.
- **Plain-text view** — whole letter in order, ends exactly "nayanet.app — enter."
- **Jump pills 5/5** — THE PROMISE / WHAT WE DO / HOW IT WORKS / YOU'RE HIRED / HOW YOU GET PAID, each landing on its board.
- **Agree via Enter** — seal stamps, world reveals with all 5 doors (Dashboard, Personal, Business, Space, Hub).
- **No flat dots** anywhere on the agreement page.

## HARVEST, NEVER INVENT — the parts this pass takes

- Portraits: the face library (`~/workspace/team-nitro/walk-v23-assembly-20261114/NAYA-FACE-LIBRARY.md`) — 15 distinct pictures, harvested verbatim, never remade. The Warm portraits differ most and are the first pick. The seven still-unused pictures are the first draw for the §4 run.
- Board portraits, jump pills, progress gems, board orbs, eyes, seal, corner gems: the fix-round file's own parts — they PASSED the checker. Keep them; do not remake them. The fix pass changes which portrait file sits where and how board 58 splits — it invents no new component.
- Anything new must prove in writing that it cannot be harvested, before it is made, and be made in the exact same format as the harvested ones.

## THE LAW THAT GOVERNS THIS PASS

- **§0 FIVE GATES** before every consequential action: Gate 1 — is it right? Gate 2 — is it what they truly need? Gate 3 — is it mine to do? Gate 4 — is now the time? Gate 5 — can I prove it? Any gate no → stop, say why, propose the wise path.
- **The highest-level canon** (`~/workspace/team-nitro/THE-HIGHEST-LEVEL-DESIGN.md`): ten checks — real object, touchable · jewelry, not dots · elevated, never flat (obsidian never gray; hover lights in own colour) · colour speaks (own colour per thing; gold only for the active one) · alive numbers · nutshell first (2–3 sentences a board, no repeating, no filler) · motion that means something · active intelligence · harvest, never invent · proven by eye. A fail blocks the deploy. The canon's nutshell check IS fix 1 of this brief.
- **The sense check:** the user sees the PAGE, not the diff. Before anything reaches his eyes: is it logical? Is it sensible? Is it intelligent? Am I doubling up? Does it make sense on the page he will look at? A reader opening several §4 notes and seeing the same portrait eleven times fails the sense check even if every board portrait is distinct.
- **Verify from the login page,** whole flow, phone first + desktop, by eye — his eye is the final gate. A checker passing a mechanism's presence is not the visual fact.
- **The goal of the plan:** do the highest level of work all the way through, thinking it through using the highest level of intelligence and logic to get there, being creative, innovative, and going out of our way to produce useful, powerful, beautifully presented, intelligent interfaces for intelligence to operate in, live in, and compound in.

## LAWS L1–L7 — tonight's laws, each named with its test

- **L1 — stranger test:** a cold stranger with no prior knowledge reads the agreement and gets it — who we are, what you're agreeing to, why it's awesome — from the boards alone.
- **L2 — perfect-words law:** the words are perfect words — word-perfect, grammar-perfect, read aloud like a friend talking; his words are input, the build carries them verbatim, never softened.
- **L3 — title+subtitle+nutshell:** every board carries title+subtitle+nutshell — the title says it, the nutshell says it once, the board never repeats the title.
- **L4 — Naya speaks, faces alternate:** Naya speaks in first person throughout, and faces alternate — a different picture of her on every board, never the same one twice.
- **L5 — test in his head:** the test in his head — he reads it as a human, not a checklist: does it feel real, warm, inviting, solid, logical, sensible?
- **L6 — ## note format:** the records file in `##` sections — maker record and checker record both in `##` format, each claim with its evidence.
- **L7 — one ultimate ten:** one ultimate ten — the page is scored as one thing, and it is not done until it is a ten, not a collection of passed parts.

## DESIGN-CONTRACT GATE (a)–(i) + human checks H1–H5

The design-contract gate, checks (a)–(i), all named: (a) zero white/light backgrounds — obsidian, never gray; (b) every element raised/elevated — no flat boxes, no flat buttons; (c) gauges/numbers alive — the day's numbers live, never dead; (d) no text-in-image; (e) no bare text blocks; (f) no look-alike — harvested parts, never remade look-alikes; (g) `##` format; (h) no dictation-blunt phrases; (i) title+subtitle+nutshell + faces alternate. Human checks H1–H5, attested with evidence in the handoff: (H1) cold-stranger read — a stranger gets it from the boards alone; (H2) read-aloud — it sounds like a friend laying it out straight, not a form; (H3) thumb test at phone width — every button reachable, no stretch; (H4) skim test — the boards alone carry the whole agreement; (H5) first-glance eye test — it looks great the moment you land on it, nothing less than great.

## ANTI-REPEAT LIST — the six known failure modes, as prohibitions

- Never paste dictation verbatim — his words are input, the build carries the sense in plain words, never a pasted transcript.
- Never use the word 'blockchain' — it does not belong in the agreement or the build.
- Never invent a component when the harvested one exists — harvest-first, always.
- Never report done from scroll-0 checks alone — every check runs at scroll 0 AND scrolled, phone first, then desktop.
- Never claim without a live measurement — live bytes and live readings, never claims.
- Never present work without a live link — no link = not done; the staged link goes to Shawn with the verdict.

## VERIFICATION PLAN (maker → checker → captain)

- **Maker** builds on the base file, checks three times, answers the seven self-check questions in writing (Self-Check Law), files a maker record with bytes + sha256 + URL + the item-by-item proof (sentence counts for ALL 83 boards — counted by sentences, never by `<p>` count — plus the portrait audit: eye-note photo counts per file, §4 board faces, adjacent-board comparison).
- **Checker (Vera)** does a FOCUSED re-check of fixes 1 + 2 only (sentence count of all 83 boards + portrait audit), plus a no-regression sweep of the 12 passes + 6 guards listed above. Verifies by EYE, phone first then desktop, walking the whole flow from the login page: Playwright at desktop 1440 + phone 390 + true 360, zero overflow, zero console errors. Every check runs at phone width first, then desktop, at scroll 0 AND scrolled. Checker files a checker record with a verdict per fix — PASS or FAIL, no partial credit. A fail on any fix fails the pass.
- **Captain** double-checks from the login page, phone + desktop, before anything reaches Shawn. Nothing merges, nothing goes live — staging only, until Shawn's tap.

## DONE LINE

Done = both fixes PASS by eye (maker ×3 + checker + captain double-check), every board 1–4 sentences by sentence count, no portrait file illustrating more than 2 eye notes, faces on at least every third board of the §4 run, no two adjacent boards sharing the same portrait, the Official words verbatim and untouched, and every no-regression guard still holding. Done is the staged link in front of Shawn's eyes — nothing less.
