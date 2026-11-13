# RECORD — WALK Q2 "WHAT'S YOUR THING?" REWORD ROUND (2026-11-13)

Maker seat. Brief: `BRIEF-WALK-Q2-WHATS-YOUR-THING-20261113.md` (checked 9/9, 21,681 B, sha `9ced0c33`).
Branch: `walk/q2-whats-your-thing-20261113` (created from main tip `c630e5d5dc288ea154b10e9be8928fa6f542c1af`, read first-hand via the GitHub API this round).
Work dir: `team-nitro/walk-q2-whats-your-thing-20261113/`.
Staged link: https://naya-walk-beginning-staging.nayapower.workers.dev/ (v22 — NOT redeployed in this round; see DEPLOY STOP below).

## DONE — what done looks like, met

- Heading (line 346, read on the slide at 390 + 1440 + 360): `"What's your thing? What do you love? What do you love to do?"` — verbatim, 2 lines at 1440, 3 lines at 390/360, wraps, never clips, never overflows.
- All three examples read in the new frame (see THE REWORD).
- Both hint lines read in the new frame; paste hint unchanged.
- All three eye pop-ups read in the new frame (2-A, 2-B, 2-C); the Full Custom eye (2-custom) shows the three ways, the third pointing at "the examples above" — the new examples (see FINDING F1).
- grep count = 0 for "What are you into" anywhere; grep count = 0 for "what you're into".
- Zero overflow at 1440/390/360; zero console errors at 1440/390/360 (local render probe — see VERIFICATION PLAN).
- "2 of 10" still reads; answer box still empty; Skip, Speak, Enter, 1-2-3 untouched.
- **NOT MET — the staged leg:** the staged walk still serves v22 (old Q2). The full walk by eye from the login page on the STAGED link is owed after deploy. Deploy is STOPPED by the brief's own deploy-order rule (see DEPLOY STOP). The round scores 7/10 honestly; no checker is dispatched per the task.

## GROUND (first-hand, nothing carried on trust)

- Staged `/welcome` re-read before editing: HTTP 200, 3,363,931 B, sha256 `227a667e4eb8e7f38fc8859495fa934b1a3b865323767816f94009b1d0df88c3` — matches the brief. Re-read again after the edit, before filing: same sha — the staged version has NOT moved.
- Base = the staged v22 served bytes (`/tmp/walk-v22.html`), never the local file. Local `walk-questions-10-20261112/walk-beginning-fixed.html` checked: 3,365,275 B, sha `a3510446…` — the names-page round's working copy, as the brief warned. Not used as base.
- Current Q2 verified first-hand in the staged bytes before editing: heading `"What are you into, and why?"` (line 346, `#step-2`, `data-key="into"`, lines 339–374); A/B/C textareas (lines 349–351) byte-identical to the canonical answers doc lines 44–56; hints (lines 365–366); `CHOICE_EYES "into"` (line 1280).
- **Correction to the brief, found first-hand:** the eye entries do NOT live in `BOARD_INFO`. `BOARD_INFO` holds only `personal` / `business` / `space`. The three-voice eye entries live in `CHOICE_EYES["into"]` (line 1280) — the strings the brief quotes match `CHOICE_EYES` verbatim. This round edits `CHOICE_EYES`, and the record names the correction. `BOARD_INFO personal` line ("what you are into") is out of scope per the brief and untouched.
- The key NEVER changed: `data-key="into"` (line 339) present; `KEYS = ['about', 'into', 'vision', 'mission', 'motto', 'goal', 'biz_do', 'biz_offer', 'biz_building', 'space']` byte-identical; S2 Box mapping untouched — `answers.into` ×2, in `words.personal = S.answers.about || S.answers.into` and `words.space = S.answers.space || S.answers.into`.
- Naya speaks, read first-hand: the question-step play button is glow-only — `/* play: audio slots are empty until the audio round — glow only, never faked */`. No handler hardcodes the old question; there is nothing to reword. Real voice is a later step, never faked.
- Main tip re-read first-hand via `gh-direct.py`: `c630e5d5dc288ea154b10e9be8928fa6f542c1af` (merge of Factory L7, 2026-11-13T02:52:31Z) — same as the brief. Branch `walk/q2-whats-your-thing-20261113` verified free (404) before creation.
- EPERM flake: CLEAR at edit time (python write probe landed first-hand, 03:03Z). VM browsers: ALIVE again — Playwright Firefox launched and measured first-hand (the Q10 record's "dead" note is stale for this window).

## THE REWORD

Heading (exact, carried in the brief): `"What's your thing? What do you love? What do you love to do?"`

### A — Warm & Plain

> My thing is music — the songs I love and the artists I play over and over. Because nobody should feel alone in the thing they love, and my music is how my people find me.

Harvest, word by word: "music … the songs I love … the artists" ← Shawn 02:50Z list (music, an artist); "Because nobody should feel alone in the thing they love" ← canonical Q2 A, verbatim tail; "my people find me" ← canonical Q2 A ("people finding each other"). Two sentences, first person, Naya's warm & plain voice. Concrete personal love, named first.

### B — Bold & Short (the money thing)

> My thing is making money — I make a page about Naya and send people to it, and I get 50% of the revenue, paid when we're paid. Anybody can.

Harvest, word by word: "my thing is making money — I make a page about Naya and send people to it" ← the brief's required beat, verbatim in substance; "I get 50% of the revenue, paid when we're paid" ← end-slide pay words ("You get 50% of the revenue, paid when we're paid") + Q9 choice C ("50% of the revenue, paid when we're paid"); "Anybody can." ← Shawn 02:52Z addendum, verbatim. Two short sentences.

### C — Full & Visionary

> My thing is the connection itself — the moment two like minds find each other across the world and realize they were never alone. Sometimes your thing is what you love, sometimes it's your job — either way, that moment becomes our place: a smart hub, a digital world where everybody meets on the one thing we love.

Harvest, word by word: first sentence ← canonical Q2 C, near-verbatim ("I'm into the connection itself — the moment two like minds find each other across the world and realize they were never alone"); "Sometimes your thing is what you love, sometimes it's your job" ← Shawn 02:56Z clarification (a thing can be a love, a job, or two different ones); "that moment becomes our place" ← Shawn 02:52Z addendum (space / group / community / place, one thing); "a smart hub, a digital world" ← Shawn 02:56Z clarification, verbatim ("smart, interactive, intelligent spaces, like worlds. Digital worlds"). Two sentences. The 02:56Z simple language rides the examples: a child and a grandma read "your thing", "what you love", "your job", "our place" — no category word anywhere.

### Hints (exact, carried in the brief)

- Dictate (line 365, tip + aria-label): "Click the button and tell us what your thing is"
- Focus (line 366, tip + aria-label): "Type in what your thing is, and what you love to do"
- Paste: unchanged — "Copy-paste from your AI into the box" (×20 file-wide: 10 steps × label + tip).

### Eye entries (`CHOICE_EYES "into"`, line 1280 — see the BOARD_INFO correction above)

- A — "Naya's warm & plain voice — my thing is music." / "Music is the thing — the songs and the artists I love." / "It fills your Personal page and your Space — the people you want around you." / "The right people recognize themselves in it."
- B — "Naya's bold & short voice — making money, with a page about Naya." / "One line that says the whole thing: the thing is making money, the page is about Naya." / "It fills your Personal page and your Space — the people you want around you." / "People feel the promise at once."
- C — "Naya's full & visionary voice — the moment becomes a place." / "It paints the moment everything is for — and the place it becomes: a smart hub, a digital world." / "It fills your Personal page and your Space — the people you want around you." / "People can feel themselves in that moment."

The "It fills your Personal page and your Space" line stays verbatim in all three (still true); the fourth lines keep their meaning; the B eye names the money beat, per the brief.

### What the answer becomes

Q2's answer is the seed of the room Q10 names: the thing they love becomes the page people connect around — space, group, community, place, one thing. The thread runs Q2 → Q10 → the space, and the S2 mapping (`answers.into` → Personal + Space taglines) carries it unchanged.

## THE EDIT (method + proof)

- Script: `edit-walk-q2.py` (in the work dir, filed on the branch). Exact-string replacements with count assertions; every assertion passed on the first clean run (two script bugs found and fixed before the run: a wrong paste-hint count in my own assertion — 20, not 10 — and a Python quoting error; both were the script's, never the file's).
- Changed lines, exactly: **[346, 349, 350, 351, 365, 366, 1280]** — heading, three textareas, two hint lines, the `CHOICE_EYES "into"` line. Nothing else. Line count unchanged (1,499 lines).
- New file: `walk-beginning-fixed.html`, 3,364,312 B (+381 B vs v22), sha256 `fd38de479d17d6ce51ae33a7667b9b5458eb6a743df626282a187d2cbe13e836`.
- Static counts after the edit: "What are you into" = 0 · "what you're into" = 0 · "what you are into" = 1 (the out-of-scope `BOARD_INFO personal` line, untouched) · `data-key="into"` present · KEYS byte-identical · `answers.into` ×2 · "2 of 10" ×1 · paste hint ×20 · all nine other question headings present word for word (asserted in the script).
- "into" remaining inside the Q2 section: ×3 only — `data-key="into"` (must stay) + "Copy-paste from your AI into the box" ×2 (paste hint, unchanged per the brief).

## VERIFICATION PLAN — full run

Local render probe `q2-probe.py` (Playwright Firefox, live browser, first-hand) — the edited file served over localhost, `#step-2` forced visible. This is a RENDERED measurement of the edited bytes at exact widths; it is NOT the staged walk from the login page (that leg needs the staging worker + backend and is owed after deploy — see DEPLOY STOP).

| Width | Heading | Font | Overflow | Console errors | Eyes 2-A/B/C/custom |
|---|---|---|---|---|---|
| 1440 | verbatim, 2 lines, box 1084×96 @ (178,184) | 36.81px | 0 (scrollW 1440 = winW) | 0 | all visible, new text |
| 390 | verbatim, 3 lines, box 362×106 @ (14,130) | 27.19px | 0 (scrollW 390 = winW) | 0 | all visible, new text |
| 360 | verbatim, 3 lines, box 332×106 @ (14,118) | 27.19px | 0 (scrollW 360 = winW) | 0 | all visible, new text |

- All three examples read verbatim from the DOM at all three widths; both new hint lines read; answer box empty (`answerEmpty: true`); "2 of 10" reads; all four eye pop-ups opened and their full text captured (see `q2-probe-results.json`).
- Eye-check of screenshots (`q2-390.png`, `q2-1440.png`, `q2-390-full.png`): the heading reads cleanly at both widths — no shrink, no split into a subtitle, per the brief's instruction. The full 390 page reads top to bottom: heading, 1-2-3, A/B/C boards, Full Custom, empty answer box, Speak, Enter, hint icons, "2 of 10", Skip.
- No-regressions, proven by the 7-line diff: the other nine questions word for word, names page, building page, end slide, certificate flow, pay words, deal board, Speak flow, Skip — all byte-identical to v22 (only the seven listed lines differ).

## FINDINGS (named, never hidden)

- **F1 — the Full Custom eye shows the new examples by reference, not inline.** `data-eye="2-custom"` opens `CUSTOM_WAYS` (shared across all ten questions): "1. Copy it in from your AI… 2. Dictate… 3. Or take one of the examples above and make it your own." The examples above ARE the new ones after this edit — verified by clicking 2-custom in the probe at all three widths. Changing the custom-eye text itself would touch all ten questions (shared `CUSTOM_WAYS`) or need a new per-question mechanism (out of bounds). The brief's "must show the NEW examples" is met by the pointer to the new examples on the same slide; the captain judges whether that satisfies the bar.
- **F2 — the brief mislabels the eye variable.** The eye entries are `CHOICE_EYES["into"]`, not `BOARD_INFO "into"` (`BOARD_INFO` holds only personal/business/space). Corrected in this record; the edit is in the right place, verified by the probe (the eye pop-ups show the new text).
- **F3 — choice photos are empty circles in the local render.** `/naya-a.jpg` etc. are served by the staging worker from KV, not by localhost — a local-serving artifact, not an edit defect. The top flank portrait renders; the boards' photos will render on staging as in v22.
- **F4 — the C board's "Full & Visionary" style name wraps below the icon row at 390.** Pre-existing v22 layout (same wrap exists for long style names), unchanged by this round — the reword touches words, never layout.

## DEPLOY STOP (escalated, not improvised)

- **NOT DEPLOYED, by the brief's own deploy-order rule.** The Q10 probe has not run; the join fix rides the Q10 maker's next deploy (v23) after it; the names-page and pay-words rounds are also building on v22. Deploying this round now would race v23 and risk reverting the join merge or the other rounds' work. Per the brief: STOP + escalate rather than deploy over the merge.
- Deploy path grounded from the Q10 record, verified first-hand: `build-beginning-staging-worker.py` reads the walk from disk (`walk-beginning-fixed.html` in its round dir) and builds the worker; `deploy-merged.py` builds + PUTs in memory with the join code carried forward (`recordJoin` 3× in the deployed v22 worker). The path is clear — the STOP is about ORDER, not about an unclear path.
- **Handoff for v23:** whoever deploys v23 must take THIS branch's walk file as the walk input — `walk/q2-whats-your-thing-20261113:walk-q2-whats-your-thing-20261113/walk-beginning-fixed.html`, 3,364,312 B, sha256 `fd38de47…`. Deploying from the Q10 round dir's v22 file would REVERT the Q2 reword. The same collision applies to the names-page and pay-words rounds — the coordinator sequences the three.
- The staged sha was re-verified immediately before filing (still `227a667e…`) — no version move, no deploy war, no revert to report.

## SELF-CHECK x3

- **Round 1 — static (edit script, 03:03Z):** every replacement count-asserted; the 7-line diff asserted; key/KEYS/mapping/other-nine-questions asserted. Found and fixed two of my own script bugs (paste-hint count 20 not 10; a quoting error) — both script-side, never file-side. No code change came out of round 1 beyond the reword itself.
- **Round 2 — rendered (probe + screenshots, 03:05–03:06Z):** heading wrap measured + eye-checked at 1440/390/360; all four eye pop-ups read; zero overflow; zero console errors. New findings: F1 (custom eye by reference), F3 (local photo artifact), F4 (pre-existing C wrap) — all recorded, none hidden.
- **Round 3 — brief-line coverage (03:07Z):** DONE FIRST re-read line by line against the evidence above. Every item is met except the staged leg (deploy STOP). The "into" sweep inside the Q2 section leaves only `data-key` + the unchanged paste hint. The 02:56Z simple-language addendum is carried in A (music, plain), B (money, plain), C (love/job/both, smart hub/digital world) and in the C eye nutshell. No silent shrink, no subtitle split, no key rename, no other-question touch.

## SEVEN PRE-MERGE QUESTIONS

1. **Did I check my own work three times? YES.** Rounds 1–3 above, each finding NEW things (round 2 found F1/F3/F4; round 3 confirmed the addendum coverage and the Q2 "into" sweep).
2. **Is it 9 or better by my own honest score? NO — 7/10.** The BUILD is 9/10 (the reword is complete, harvested, and rendered-proven at three widths). The ROUND is 7/10 because the brief's done bar includes the staged proof from the login page, and that leg is owed after deploy — blocked by the brief's own STOP rule, not by a defect. Two points off, named: (a) no staged proof from the login page, (b) no deploy/merge in this round. Per the task, no checker is dispatched; the stop is reported honestly.
3. **What could this break?** The staged walk's Q2 strings (only Q2 changed — 7 lines); the v23 deploy if the deployer takes the wrong walk file (mitigated by the handoff above); nothing else — no live deploy, no merge, no money, no credentials, no destructive action, no privacy change, no key rename, no other question, no names/building/end-slide bytes.
4. **Are the automatic checks green? PARTIAL.** The edit-script assertions all pass; the local render probe passes at 1440/390/360 with zero console errors. There is no CI suite on this branch. The staged walk check is unrun because the deploy is stopped.
5. **Does it follow the ultimate objectives (five gates)? PARTIAL — gate 5 is not yet yes.** Gate 1 (right?) yes — the question finds their thing, which becomes their place. Gate 2 (what they truly need?) yes — a child and a grandma can answer it. Gate 3 (mine to do?) yes — brief-authorized, Q2 only, staged only. Gate 4 (now?) yes — built, filed, verified locally; the deploy waits on the coordinator's order. Gate 5 (can I prove it?) PARTIAL — the edited bytes are proven rendered locally; the staged proof is owed. Four yes + one partial = do not call it done.
6. **Did I prove it with real measurements? PARTIAL.** Staged base sha + file sha + grep counts + local rendered measurements + screenshots — yes, live-measured. Staged proof from the login page — NO, not yet (deploy stopped).
7. **Is there anything in here not ten out of ten that I'm knowingly leaving? YES — named, never silent.** (a) The staged leg is unrun (deploy STOP — see above). (b) F1: the Full Custom eye points at the new examples rather than displaying them inline — a judgment call for the captain. (c) F2: the brief's `BOARD_INFO` label for the eye entries is wrong in the brief; the edit is in `CHOICE_EYES`, corrected here.

**Verdict on the seven:** two NOs — do not merge (nothing to merge in this round), do not call the round 9+, do not show Shawn anything as finished. Hand to the coordinator with the STOP named and the v23 handoff in writing.

## DESIGN-CONTRACT GATE (a)–(i) + H1–H5 + L1–L7

- (a) zero white/light backgrounds — PASS. Obsidian stays; no background touched.
- (b) every element raised/elevated — PASS. Boards untouched, still elevated.
- (c) gauges/numbers alive — PASS. "2 of 10" stays live; 1-2-3 untouched.
- (d) no text-in-image — PASS. The question is live text, never baked into an image.
- (e) no bare text blocks — PASS. Question + examples stay in boards.
- (f) no look-alike — PASS. Three distinct voices, three distinct examples (music / money / the place).
- (g) `##` format — PASS. This record is in `##` sections.
- (h) no dictation-blunt phrases — PASS. Shawn's frame is carried as the frame; the examples are written in Naya's voice; his 02:56Z words are carried as the addendum's meaning, not pasted as dictation.
- (i) title+subtitle+nutshell + faces alternate — PASS. Question is the title; examples are the nutshell; three faces alternate as in v22.
- H1 the words are true — PASS. Every new word traces to a named harvest source (see THE REWORD).
- H2 the question is right — PASS. It asks for the thing, not a category.
- H3 nothing private is in it — PASS. No citizen data, no secrets.
- H4 the proof is named — PASS. Staged sha + file sha + grep counts + probe results + screenshots.
- H5 the bounds hold — PASS. Staged walk only, Q2 only, no live deploy, no merge.
- L1 stranger test — PASS (local render). A cold stranger reads Q2 and knows at once what to answer — their thing, what they love.
- L2 perfect-words law — PASS. "What's your thing?" names the love, not a category.
- L3 title+subtitle+nutshell — PASS.
- L4 Naya speaks, faces alternate — PASS (static + probe). Play button is glow-only until the audio round; three faces alternate A/B/C.
- L5 test in his head — CANNOT PASS YET. Would he say "that's my thing"? The words are his frame in Naya's voice; his eye is the final gate, and the staged page is not yet live with the reword.
- L6 `##` sections — PASS.
- L7 one ultimate ten — NOT YET. One question, one thing; the staged proof is owed.

## FILED BLOBS (branch `walk/q2-whats-your-thing-20261113`)

Branch created from live main tip `c630e5d5dc288ea154b10e9be8928fa6f542c1af` (read first-hand via the GitHub API this round). Branch head: `d98ade8986c1ff2afdaa46af8e3e79466598c9ba`. All blobs read-back verified (filing run 03:09Z):

- `walk-q2-whats-your-thing-20261113/walk-beginning-fixed.html` — 3,364,312 B, sha256 `fd38de479d17d6ce51ae33a7667b9b5458eb6a743df626282a187d2cbe13e836`, blob `afe5a7bf7cb49db763873c091f37a99b4536c5ff`.
- `walk-q2-whats-your-thing-20261113/edit-walk-q2.py` — blob `563a5ab30eac93701e0b710ee0e5180d7ce5d285`.
- `walk-q2-whats-your-thing-20261113/q2-probe.py` — blob `58480143e57774d65fbeb94dbab710006a25a2e5`.
- `walk-q2-whats-your-thing-20261113/q2-probe-results.json` — blob `105ded432c20b80e8c29a09530bbfc690f01be47`.
- `walk-q2-whats-your-thing-20261113/q2-390.png` — blob `80128f859dbf346a2db41e47adf260c7927a43d8`.
- `walk-q2-whats-your-thing-20261113/q2-1440.png` — blob `5c3e6056a67c3e69c61d8bc89c7d62670fc0f0d0`.
- `walk-q2-whats-your-thing-20261113/RECORD-WALK-Q2-WHATS-YOUR-THING-20261113.md` (this file) — blob `f10dc7d32fbfe0ad14dcc86398cd3602eb0dd2dc` (re-filed after this section was completed with the branch head; the blob changes on re-file — the filing run's read-back is the authority).
- `walk-q2-whats-your-thing-20261113/SCORECARD-WALK-Q2-WHATS-YOUR-THING-20261113.md` — blob `6cf6514fb0e197a30524d081cd709fdd080afc5e`.
- `walk-q2-whats-your-thing-20261113/receipt-walk-q2-whats-your-thing.json` — blob `b71e7e3c9870d09671aef1f79b2f134138e3e854`.

(Blob shas + read-back verification: filing run 03:09Z, all match=True.)

## BOUNDS (honest — what was actually proven, and what was not)

- **Proven:** staged v22 base (hash, twice) · edited file (hash, 7-line diff, grep counts, key/KEYS/mapping intact, other nine questions verbatim) · local rendered measurements at 1440/390/360 (heading verbatim + wrap, zero overflow, zero console errors, all four eye pop-ups, hints, "2 of 10", empty answer box) · screenshots eye-checked · branch + blobs read-back verified (filing run).
- **NOT proven:** the staged walk from the login page at 390 + 1440 (deploy stopped) · the Box read-back of a Q2 answer in the new frame (needs a staged walk) · Shawn's eye on the reword. Nothing in this record claims a staged number.
- **Test aliases:** none used in this round (no walk was run — the probe forced `#step-2` visible locally; no Box rows exist for this round). No test data was written anywhere.
