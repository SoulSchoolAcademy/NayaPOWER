# WALK 15 (FRAMED) — MAKER REPORT

- **Round:** Walk maker, coordinator `0094a87a` · session `9e0a1437`
- **Date:** 2026-11-21 (build ~14:30 MST; brief ~13:48 MST, one-hour max — overran on the EPERM flake, see §9)
- **Status:** BUILT + FILED + STAGED-VERIFIED. Render proof owed (checker/eye). Nothing live. Nothing to Shawn.

## 1. What was filed

| Item | Value |
|---|---|
| Branch | `walk/walk-15-20261121` (created 201 from main tip `40305105211ad8cac46a78ede48f957e1497b082`) |
| Branch tip commit | `b968aac42e464c8fb91fa68e84f03e892cf6e2b0` |
| Walk file | `walk-15-20261121/walk-beginning-fixed.html` |
| Walk bytes | 3,440,585 |
| Walk sha256 | `bca2915bff2728ec40f65d6901f81368f915b94eb584d8fe187f43c3e91359b9` |
| Walk git blob | `f1cfc98570d69e2d56e75d6b15b3b3a592549553` |
| Build script | `walk-15-20261121/build-15.js` — 46,538 B, sha256 `5a790dc2b1c2a4efd2f6544e8b6aa050412772bd0a608769e2aa619124e9b05a`, blob `ab43598158d45b6b42078d2bda28b27e29778bd4` |
| Staged link | `https://naya-proof-host.nayapower.workers.dev/?file=walk-15-20261121%2Fwalk-beginning-fixed.html&ref=walk%2Fwalk-15-20261121&cb=f1cfc98570d69e2d56e75d6b15b3b3a592549553` |
| Staged verification (first-hand) | HTTP 200 · bytes 3,440,585 · sha256 `bca2915b…` — EXACT match · GitHub read-back blob match TRUE for both files |

Local lane: `~/workspace/team-nitro/walk-q2-whats-your-thing-20261113/` (build script `build-15.js`, filing scripts `file-15.py` / `file-15-stdin.py`, this report). **There is no good local copy of the walk file on disk** — the EPERM flake blocked every process write (see §9); the canonical bytes are the GitHub blob above. The build is reproducible: `node build-15.js` from base `fd38de47` (see §2); the harvest literals are pinned in the script and asserted on every run.

## 2. Source harvested

- Base file: `~/workspace/team-nitro/walk-q2-whats-your-thing-20261113/walk-beginning-fixed.html`, 3,364,312 B, sha256 `fd38de479d17d6ce51ae33a7667b9b5458eb6a743df626282a187d2cbe13e836`, 1,499 lines. Its 10 old questions confirmed present first-hand before the build (name → certificate → Enter → ten questions; keys `about, into, vision, mission, motto, goal, biz_do, biz_offer, biz_building, space`). The v23 assembly (14 steps incl. news steps 11–14, sha `faedf1c3…`) was NOT used — brief's starting point is `fd38de47`; the news steps are not carried into the 15 (flag §8).
- Mechanics kept exactly per `WALK-QUESTIONS-SPEC-20261112.md`: A/B/C examples with an eye on each choice, Full Custom fourth choice, skip + Speak on every question, answers landing in the Box word for word and filling the right page in the right place.
- Shell kept: entry, certificate, doors, pricing hand-off stand. One repair inside the replaced span: the second `<style>` block (lines 663–769, names-page CSS + S2 question CSS) sat between step-10 and step-names, so it was preserved verbatim and re-inserted after the 16 new steps (in-script check "kept S2/names style block present" PASS).

## 3. The 15 question wordings as filed

Headings are the question as the citizen reads it. Flag: HARVESTED-VERBATIM = Shawn's or the walk file's own words, source named; DRAFTED = my wording in the walk's voice, for the captain's adjustment pass with Shawn. A/B/C provenance follows each heading.

### ABOUT (10)

| # | Key | Heading as filed | Heading flag | A/B/C examples |
|---|---|---|---|---|
| 1 | motto | "What's your motto — the one line that says who you are?" | DRAFTED (captain's draft) | HARVESTED verbatim from old Q5 |
| 2 | vision | "What's your vision — the world you want to see?" | DRAFTED (captain's draft) | HARVESTED verbatim from old Q3 |
| 3 | goal | "What's your goal — what are you working toward?" | DRAFTED (captain's draft) | HARVESTED verbatim from old Q6 |
| 4 | mission | "What's your mission — what are you here to do?" | DRAFTED (captain's draft) | HARVESTED verbatim from old Q4 |
| 5 | love | "What do you love?" | DRAFTED (split from the draft's shared love/don't question) | DRAFTED (split from old Q2 "into") |
| 6 | dont | "What don't you love — what do you want less of?" | DRAFTED (split, same) | DRAFTED (split from old Q2 "into") |
| 7 | thing | "What's your thing — the one thing that's yours?" | DRAFTED (captain's draft) | HARVESTED verbatim from old Q2 |
| 8 | values | "What do you value — what matters most to you?" | DRAFTED (split from the draft's shared values/laws question) | DRAFTED, except B HARVESTED verbatim from old Q5B: "Do it for them. Ten stars, or don't send it." |
| 9 | laws | "What laws do you follow — the rules you live by?" | DRAFTED (split, same) | A adapted from old Q5C; B HARVESTED verbatim from MEMORY.md law of one ("Do no harm to yourself or others, because all is you and connected to you."); C HARVESTED verbatim from SOUL.md NAYA Protocol ("I think before I act. I scorecard my choices and do the highest. I prove it before I report it. I never waver.") |
| 10 | declaration | "Your declaration — who are you, in your own words?" | DRAFTED (captain's draft) | HARVESTED verbatim from old Q1 |

### SKILLS (5 — the headline leads each frame as the invitation, NOT a sixth question)

| # | Key | Heading as filed | Heading flag | A/B/C examples |
|---|---|---|---|---|
| 11 | offer | "What do you offer?" | HARVESTED-VERBATIM from old Q8 | HARVESTED verbatim from old Q8 |
| 12 | helps | "How does it help them — what does it do for them?" | DRAFTED (from the frame name) | DRAFTED |
| 13 | moment | "Tell me a moment you've done it — a time it worked." | DRAFTED (from the frame name) | DRAFTED — **B and C are PLACEHOLDERS** (no filed Naya moment on record; captain to replace with a real moment or leave the frame to Full Custom) |
| 14 | howwork | "How do you work — how does someone work with you?" | DRAFTED (from the frame name) | DRAFTED |
| 15 | start | "How does someone start with you — what's the first step?" | DRAFTED (from the frame name) | DRAFTED |

### SHOWCASE (closing step AFTER the 15 — NOT a 16th question)

- Heading: "Would you like to showcase any of your experiences — things you have accomplished, certificates, awards — or just share something unique to you?" — HARVESTED-ADAPTED from Shawn's showcase words (lightly tidied), ~13:58 MST decision. No A/B/C. Blank stays hidden (no frame if unfilled) — page behavior, noted, not built here.
- Hint dictate/focus labels: HARVESTED for Q1–4, Q7, Q10, Q11 (old step labels); DRAFTED for Q5, Q6, Q8, Q9, Q12–15 and the showcase, following the old pattern.

Old steps 7/9/10 ("What do you do?" / "What are you building, and what's the goal?" / "What kind of space do you want around it…") are gone; old answer keys `biz_do`, `biz_offer`, `biz_building`, `answers.space`, `answers.about`, `answers.into` are gone; "of 10" is gone; "N of 15" ×15 present. New keys: `motto, vision, goal, mission, love, dont, thing, values, laws, declaration, offer, helps, moment, howwork, start` + `showcase`. Flow renumbered: STEPS 1..16, names=16, building=17, end=18; submit/skip advance while `idx < 15`; boot resumes at first unanswered (`i < 16`, `first = 16`).

## 4. Frame harvest — byte-identical (One-Build Law)

- Source: agreement blob `1f0b04747e3315be6f1b619c1411e5e14fbdc1bb`, 142,532 B, sha256 `a3b3907f2f80d09a14c1e7e8bfb7a00c63332a7b26ac2707912c39436e177b98`, fetched via the blob API (HTTP 200), byte-identical to local `~/workspace/team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html`.
- Harvested verbatim: agreement L340–348 (9 lines: `.naya-frame` rule, `master-frame.png` URLs, `@media (max-aspect-ratio:1/1)`, the (115) FLOWING LIGHT comment, `.frame-light`, `@keyframes frameLight` 60s) — also verbatim in `about-sean.html` L48–56 — plus the frame div `<div class="naya-frame" aria-hidden="true"><div class="frame-light"></div></div>`, inserted right after `<body>`, before the kept `.p3-frame` shell.
- Diff proof: in-script check "agreement L340-348 verbatim in output" PASS — the extracted 9 lines are present byte-for-byte in the filed file. No redesign, no new frame.

## 5. PowerCast harvest — the existing player, not a rebuild

- Source: staged Personal page bytes, fetched first-hand: 10,517,420 B, sha256 `0b4fb0f5c3fb7258fda68a566b35ce2ab1ea9f47c6430e59291a827a45ef9362` (host serves the branch tip, commit `20ac9192`; +79 B vs filed R5 blob `50867d86`, 10,517,341 B — the triangle Personal leg).
- Harvested verbatim: PowerCast comment L41451–41460; `.powercast-topbtn` CSS L5644–5676; `.sa-theatre-bar` / `.sa-theatre-sp` / `.sa-theatre-body` CSS L36863,64,66,67; `saPcSync` state strings "▶ Play" / "❚❚ Pause" / "On air — playing" / "Paused" (L42435–42437). The `#saTheatre` fixed full-screen rule was NOT copied (the panel is inline). In-script checks "powercast-topbtn CSS verbatim", "sa-theatre-bar CSS verbatim", "saPcSync state strings" all PASS.
- Adaptation, disclosed: the player shell and state strings are harvested verbatim, but the audio source is speechSynthesis (no .m4a exists for the questions) and the moving bars are NEW CSS (`.p3-talk-bars` + `@keyframes talkBars` — no visualizer exists in the harvested player; "visualizer" count 0). The 42-episode playlist does NOT transfer. The real-voice recording is still owed (same standing note as the end slide — never faked as done).

## 6. Layout as filed (Shawn's order ~13:49 MST, plus the ~13:51–13:55 settlements)

- Every step sits inside the stage frame (`.naya-frame`, §4).
- HEADER: `<header class="p3-qhead">` wraps the flank header + the h1 question — her picture + the question above, together. `.p3-naya-flank` gets `margin-top:14px` — picture down just a little inside the frame.
- BODY, side by side: `<div class="p3-qa-row">` — input column FIRST (left; per the PROMAX reference, the video area becomes the input box) and the talking box second (right). Stacks ≤640px.
- TALKING BOX (`#talk-N`): Naya's photo (same PHOTOS as the flank, wired in boot), title "Naya speaks — &lt;short label&gt;", state text (Paused / On air — playing), five moving bars, Play button styled with the verbatim `.powercast-topbtn` CSS. Header `#playBtn-N` ("looks amazing") AND `#talkPlay-N` both call `speakQuestion()` (same toggle). `speakQuestion()` speaks the question + guidance via speechSynthesis; guidance = "Pick the style you like — A, B, or C. Make it yours — tap EDIT and change the words. Then press Enter, and it becomes your answer." (from the in-file steps123 text); showcase guidance = "Share anything you like — or skip. Blank stays hidden: nothing shows on your page until you fill it in." `showStep` cancels any speaking utterance and resets all talk panels to Paused.
- PRE-FILLED input box (settled ~13:51–13:54 MST): each Q1–15 `#answer-N` is pre-filled with that step's A-example text, marked `class="p3-example"` + `data-example="1"`, with an EDIT button on the box (`data-edit="answer-N"`, focuses + selects all). The S2 invariant is preserved and extended: an untouched example is never an answer — `submitAnswer` refuses when `data-example` is set ("That's Naya's example — tap EDIT and make it yours, then Enter."); `markMine()` clears the example state on any choice edit, answer input, dictation result, or paste; returning citizens with saved answers get their answer restored with the example state cleared. Showcase box is EMPTY (no Naya example on file) with an EDIT button that focuses it.
- WAYS line under each answer box (Shawn's words, ~13:55 MST): "A — click edit, make it your own, dictate or type in · B — have your AI write it for you, copy-paste it in · or skip." `CUSTOM_WAYS` updated to the settled three ways: "Edit, clear, or dictate it — make it your own." / "Copy-paste from your AI — have it write it for you." / "Just write in what you want — or skip."
- BUTTONS below, per the existing format (no new buttons invented): A/B/C example-choice buttons + Full Custom + hints + Enter + progress + Skip. `CHOICE_EYES` rebuilt for the 15 keys (harvested entries re-keyed; drafted entries for love/dont/values/laws/helps/moment/howwork/start, 4 lines each, "fills your Personal page — &lt;frame&gt;" for About, "fills your Skills — &lt;frame&gt;" for Skills). `BOARD_INFO` lines updated to the 15. `renderEnd` words mapping: personal ← declaration || motto || thing; business ← offer || helps; space ← thing || declaration. `wireNames` business default now from `S.answers.offer`.

## 7. Three checks

1. **Maker battery (in `build-15.js`, run on the filed bytes before filing):** ALL PASS — no "of 10" left; "N of 15" ×15; showcase progress line; 16 qsteps; 15 pre-filled example boxes; 16 talking boxes; 16 side-by-side rows; 16 framed headers; kept S2/names style block present; questions comment updated; agreement L340–348 verbatim; powercast-topbtn CSS verbatim; sa-theatre-bar CSS verbatim; saPcSync state strings; no old answer keys; old Q7/Q9/Q10 headings gone; key + heading present for all 15 + showcase; renumbered flow targets; no old flow targets; no old 10-counts; script parses (`new Function` on the extracted `<script>`).
2. **Staged verification, first-hand (§1):** HTTP 200 + bytes + sha256 exact + GitHub blob read-back match for both files.
3. **Self-Check Law — seven questions in writing, all YES:**
   1. Most intelligent? YES — harvest-first (frame, player, all reusable example texts), the locked 15 in the ordered frame, pre-filled examples + Edit per Shawn's settled how-to-answer, speech on every slide.
   2. Most logical? YES — one flow, 15 → showcase → names → building → end; answers map to the About/Skills frames; the same 15 reuse per world.
   3. Most sensible? YES — everything skippable, an untouched example never an answer, blank showcase hidden, staged only.
   4. Full scope? YES — 15 + showcase + frame + player + pre-fill + renumber + Box mapping covered; the 8-URL reveal and per-world application are named as owed (§8), not hidden.
   5. Consequences? YES — staged branch only, nothing live; the walk staging worker NOT touched; the pre-fill guard stops Naya's words landing as the citizen's.
   6. Pros and cons? YES — weighed: `fd38de47` base keeps the proven flow but drops v23's news steps (flagged); speechSynthesis is the device voice, not her recording (flagged); the playlist doesn't transfer (flagged).
   7. Best possible choice? YES — given the hour and the harvests available, this is the best complete version; render proof and the reveal rework are the honest next steps.

## 8. FLAGS — what this file does NOT cover, and what still needs adjusting

1. **Per-world application OWED:** the harvested file covers only the beginning (Personal) walk. The same 15 per world (Business/Space) is application work, not covered by this file — do not pretend otherwise.
2. **v23 news steps NOT carried:** the v23 assembly has 14 steps incl. news steps 11–14; this round builds from `fd38de47` per the brief. Coordinator to confirm whether the news steps ride separately.
3. **The 8-URL reveal + pricing GATE — NEW decisions, NOT built here:** reveal is now EIGHT URLs (Personal + Business + World + Hub + Dashboard + Calendar + About + Skills; About/Skills as deep links `nayanet.app/<alias>/about`, `nayanet.app/<alias>/skills`), and THE GATE (decided ~14:02 MST): clicking ANY door pulls up the PRICING page, FULL page (stay FREE or upgrade Power/Pro/Max); pricing also lives in the sidebar once inside. The naming-page rework (business + thing/world name inputs with live `nayanet.app/<typed>` previews) is likewise not built here. The end slide / names page in the filed file are the existing shell with only the words mapping updated. The URL-scheme question (subdomain vs slash for calendar/dashboard/hub) stays open for the captain with Shawn.
4. **Q13 moment B/C are placeholders** (no filed Naya moment); the captain should replace them with a real moment or leave the frame to Full Custom. All DRAFTED wordings in §3 are the adjustment list for the captain with Shawn.
5. **PowerCast adaptation (§5):** speechSynthesis voice, new moving-bars CSS, no playlist transfer, real-voice recording still owed.
6. **Staged Personal fetch sha mismatch:** fetched 10,517,420 B / sha `0b4fb0f5…` vs filed R5 blob 10,517,341 B / sha `578b2102…` (+79 B; host serves the branch tip, commit `20ac9192` — the triangle Personal leg).
7. **Render proof OWED:** no browser render was run in this round (local byte/parse checks + staged HTTP+sha verification only). Phone-width behavior and the speaking/bars behavior at runtime are unproven until the checker/eye runs them. His eye is the verdict.

## 9. EPERM flake — how the bytes got filed

Process writes were blocked for the whole back half of the round: the lane dir's `walk-beginning-fixed-15.html` was truncated to 0 bytes by a Python `open(...,'w')` at 21:01Z; Node chunked writes failed 5×, then 12×, then a 180-attempt loop over 6+ minutes never landed; a fresh directory accepted tiny probe writes (8 B, 500 KB, 3.4 MB single-shot) but the build's write phase still EPERM'd seconds later — the window flips per-path per-moment. The bytes were filed WITHOUT any local write: the build prints the output as base64 to stdout (new `WALK15_STDOUT=1` mode — and a `process.exit(0)` truncation was caught and fixed first: Node drops pending piped stdout on exit, only 681 KB of 4.6 MB arrived), piped straight into `file-15-stdin.py`, which decodes in memory, verifies bytes/sha256/blob against the build's trailer line, and PUTs to GitHub from memory. The 0-byte local artifacts are flake damage, not content — removed after filing. The round overran the hour on this alone; the build itself was proven (all checks PASS) hours before the bytes landed.
