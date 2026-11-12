# RECORD — Walk END SLIDE 10/10 + the New-Account Fix (Team Nitro, maker seat)
Captain: Naya Nitro Narzan. Maker: Walk end-slide maker seat (re-dispatch —
the first maker was killed by a runtime restart ~22:52Z; this round started
fresh from the brief and inherited the first maker's staged bytes + probes).
Staged link: https://naya-walk-beginning-staging.nayapower.workers.dev/
Branch: `walk/end-slide-10-20261112` (from `walk/s2-box-pages-20261112`,
tip `dbc2f7be`).
Work dir: `~/workspace/team-nitro/walk/end-slide-10-20261112/`
Base dir: `~/workspace/team-nitro/walk-s2-box-pages-20261112/` (the S2 files;
edit, never rebuild).

## The order (one line)
Shawn 22:25Z: the end slide is not 10/10 — make it 10/10 (bullseye §1 A–H).
Shawn 22:36Z, top priority, before the rebuild: a new citizen CANNOT create
a new account from a browser that already holds a profile — he entered
"Mike", the certificate came up "Shawn" + his old profile (cert Nº 000149),
NO alias field, and Enter jumped to the end. "It shouldn't remember me...
they should be able to make a new account."

## The bug — root causes (three, all in the staged files)
Found by reproducing it in a returning-browser context (Playwright
persistent profile) and reading the code — the first maker's repro
(`bug-repro.py`, 18/0, 22:40Z) showed the certificate painting the old name
"Bug Owner", cert Nº 000183, "This Smart Name is yours — welcome back.",
NO alias field, Enter jumping to the end slide.
1. **The walk ingest poisoned the stored name (walk).** The walk stored any
   `?name=` against the stored alias — a lone `?name=Mike` (his URL read
   `identity.html?name=M`) overwrote the stored name while the alias stayed
   the old citizen's. Fix (pair rule): a `?name=` is stored ONLY together
   with its `?alias=`; the identity page always hands off the pair.
2. **The identity restore was ungated (identity).** Loading the certificate
   silently restored the stored profile whatever `?name=` said. Fix: the
   restore runs ONLY when `?name=` matches the stored name, or there is no
   `?name=`; a `?name=` naming another identity stays composing (alias
   field open, empty); a `?name=` naming another identity this browser
   already knows switches to that one and restores IT.
3. **The heal poisoned the singleton the other way round (identity — found
   by THIS maker, reading the heal in the typed-alias path).** The registry
   heal wrote the certified name into `nayanet_smart_name` whenever it
   differed — including when the certified identity was ANOTHER one (typing
   bugowner9 while stored as mike8). The entry page jumps back in on the
   stored pair, so it would have jumped into the wrong name. The v3 probe
   never asserted the singleton after typing another alias, so it passed
   with this live. Fix (identity v3, the heal gate): the singleton name is
   healed ONLY when the certified alias IS the stored alias; the remembered
   identities list heals with the correct pair either way.
Plus: the registry truth heals a poisoned stored name + the identities list
on restore; the re-entering owner hands off the CERTIFIED name (registry
truth), never a passed `?name=`; a new claim ADDS to
`nayanet_smart_identities` (max 8), never replaces; the entry page lists
every identity on the device as its own Jump back in ("Also on this
device:").
The live `shawnvibe` row was never touched — the old-profile leg uses test
profiles as the stand-in, named honestly here.

## §1 coverage (A–H) — all verified by the end probe, 200/0
- **A — their world, presented:** three page cards (Personal, Business,
  Space) carrying THEIR typed page titles + one line of THEIR own words +
  the Smart Link address; each a real click to the real created page.
  1440: Five's Garden / Green Box Farm / The Garden Room (words: "I am a
  gardener from the valley..." / "I grow vegetables..." / "A garden room
  for growers..."). 390: Six's Table / Seed & Supper / Supper Club. The
  Personal title is TYPED on the names page this round (the first maker's
  probes left it blank, so the card fell back to the alias — the probe gap
  this maker closed). Card clicks land on the created pages (1440 all
  three; 390 Business).
- **B — Smart Link as a real object:** the chip shows `nayanet.app/<alias>`
  with a working Copy — real click, clipboard reads
  `https://nayanet.app/joinus?ref=<alias>`, label flips to "Copied ✓"
  (1440/390/360). The line names identity, smart name, ambassador link,
  tracking, paid every Wednesday.
- **C — five doors in his order:** Dashboard FIRST and lit as recommended
  first ("Get your Smart Link — recommended first"), then Personal,
  Business, Space, Hub — order asserted at all three widths. Every door
  carries the typed title and lands on the real page/Hub for THIS citizen
  (Dashboard to the live Dashboard; Personal/Business/Space to the created
  pages; Hub to the staging Hub listing all three pages). "Choose your
  package" stays AFTER the product (below the deal board); the footer line
  stays true ("See the whole product first, then choose your package —
  then back to the Hub, where all your pages live.").
- **D — Collective Agreement board:** AFTER the world, BEFORE pricing.
  "Here's the deal." — all 12 terms asserted by text at all widths: the
  agreement · we don't sell your data · NO ads · not reading your mail ·
  not reading your instant messages · not even keeping them · auto-
  distillation default a WEEK, bump to a day or a month, never kept more
  than a month max · BUT you can SAVE anything, saved ones locked to you
  in your Smart Box.
- **E — Naya speaks:** the play button speaks the congratulations + the
  deal (the Voice Memos closing script), proven by real click: state
  `playing`, live speech, "Naya is speaking — the congratulations, and
  the deal."; second tap pauses ("Paused. Tap play to hear it again.").
  HONEST BOUNDARY: the live voice path is speechSynthesis; the real-voice
  recording is a later step, named as owed, never faked.
- **F — quote-glow fix:** "Congratulations, you're hired." reads single.
  Computed text-shadow is now `rgba(0,0,0,0.85) 0px 2px 6px,
  rgba(0,0,0,0.9) 0px 1px 0px` — the 18px purple blur glow is gone; the
  text stays verbatim. Eye-checked single at 1440/390/360.
- **G — widths 1440/390/360, zero overflow, zero console errors:**
  overflow 0 at every step and width; staged-origin console errors 0;
  pageerrors 0. One-screen fit measured: congratulations + link + all
  five doors above the fold on phone (390×844: last door bottom 784 ≤ 844;
  360×800: 676 ≤ 800; 1440: 800 ≤ 900).
- **H — no regression:** re-proven by the fresh-alias full walks, not
  assumed — ten questions (all ten filled at 1440; Skip Q1/Q10 at 390,
  storing nothing) · names page (slugs follow live; personal address is
  the alias itself) · building page (done + three real links) · Hub door
  (lands + lists the pages) · pricing button (after the agreement) ·
  entry dial (name-only, one input) · alias-only certificate · returning-
  citizen choice (Jump back in + new-account line + other identities).

## Verification — probe runs (Playwright Firefox on the VM, from the LOGIN page)
- **Bug repro (first maker):** `bug-repro.py`, 18/0 — the bug reproduced
  exactly as Shawn described it.
- **Bug verify v3 (this maker, re-dispatch):** `bug-verify-v3.py`,
  **63 PASS / 1 FAIL**. The 1 fail was a PROBE artifact, not the product:
  the v2→v3 transform left the hardcoded expectation "Mike7" (v2's alias)
  while the probe typed v3's alias mike8 — the page correctly echoed
  "Mike8". Fixed in v4 (expectation + check name).
- **Bug verify v4 (identity v3, heal gate):** `bug-verify-v4.py`,
  **67 PASS / 0 FAIL, exit 0** (`bug-verify-results-v4.json`). Fresh
  aliases healwalk2 / bugowner10 / mike9 / bugfresh3; fresh profiles.
  Leg 0: the heal still works on the restore path (poisoned "Mike" →
  registry truth "Heal Walker", cert Nº 000190, stored name + list healed).
  Leg (a): Mike walks fresh — certificate composing, alias open, claims
  mike9, Q1–Q10, end slide with his Smart Link + world cards + agreement
  board; Box 1/1, project 1, 3 pages read back; old profile's Box/project
  still exactly one. Leg (b): the heal gate — typing bugowner10 certifies
  as Bug Owner (cert Nº 000191) AND the stored pair stays mike9/Mike, the
  list holds both correct pairs, the CURRENT Jump back in carries the
  stored pair (`/hub?name=Mike&alias=mike9`), Jump back in as Bug Owner
  lands on Bug Owner's Hub listing his pages; `?name=Zara` (brand new)
  stays composing. Leg (c): fresh-browser regression clean.
- **End probe v2:** `end-probe-v2.py`, **200 PASS / 0 FAIL, exit 0**
  (`end-results-v2.json`). 1440 full leg (endwalk5), 390 fresh leg
  (endwalk6), 360 seeded spot checks (endwalk5's stored state). Console
  errors are scoped by origin: staged origins 0 at all widths. The 1440
  leg carries a live-dashboard direct-load adjudication (see below).
- **Live-dashboard adjudication:** the v1 probe's one fail was a console
  error on the LIVE Dashboard after the Dashboard-door click (unpkg
  supabase-js blocked for a MIME-type mismatch). In v2 the door click
  produced ZERO live-origin errors (`door-live=[]`) — the unpkg error did
  NOT reproduce. The direct load of the live Dashboard showed that page's
  OWN errors instead: CORS blocks on its `smart_mail_threads` fetch
  (to_alias=flagship-personal) — the standing mail incident, not the walk,
  and not seen via the door click. Named honestly: the v1 error's root
  cause is unproven (transient or changed); it is a live-page asset error,
  out of this round's scope, and it did not reproduce.
- **Independent read-backs (not the probe):** served `/welcome` sha
  `16da2b97…` = filed walk sha; served `/identity.html` sha `55fdffa8…` =
  filed identity sha (the heal-gate comment is in the served bytes);
  served `/` sha `51b42b87…` = filed welcome sha (all curl-verified after
  the redeploy, deployment `a11843905af24961925401a5710b7e1d`). Box for
  mike9/endwalk5 read back via `/api/welcome/box` — all ten answers word
  for word, page names with typed titles, exactly one Box + one project +
  three pages each.
- **Diffs vs S2 (filed base):** walk 175 lines (world cards + deal board +
  Naya speaks + quote-glow + ingest pair rule + one-screen tightening);
  identity 76 lines (restore gated + heal + certified-name handoff +
  heal gate + rememberIdentity); welcome 46 lines (other-identities
  jump-back-in). S2 base shas: walk `efaec98f…` (3,329,959 B), identity
  `84c2b29a…` (306,162 B), welcome `506a0f82…` (623,558 B).

## Self-checks (three rounds, each finding NEW things)
- **Round 1** (eye-check of the v3 screenshots + reading the heal):
  F1 — THE HEAL GATE (real defect, not a probe gap): the heal wrote the
  certified name against the stored alias even when the certified identity
  was another one. Fix: gate the singleton heal on the certified alias
  BEING the stored alias; the list still heals with the correct pair.
  Re-proven by bug-verify-v4 (67/0, the gate assertions are new).
  F2 — the Personal-title probe gap: no probe ever typed a Personal title,
  so the Personal card/door was only proven on the alias fallback. Fix:
  the end probe now fills `#name-personal` (Five's Garden / Six's Table)
  and asserts it on card + door + Box read-back. Re-proven by end-probe-v2
  (200/0). F3 — the stale "Mike7" probe expectation (v2 leftover): fixed
  to "Mike9" and renamed honestly ("echoes the typed alias").
- **Round 2** (eye-check of the end-probe 1440/390 cards + deal): no new
  defects. The world cards read as designed parts (purple/green/gold top
  edges, elevated, same board grammar as the names page); the deal board
  is gold-edged and fully readable; "Choose your package" sits lit purple
  below it; the footer line is true. Noted, NOT a defect: the walk's
  corner-gem frame ornaments overlap the "Your world" heading when it is
  scrolled to the exact top edge — pre-existing frame behavior on every
  step (S2), not this round's; the brief does not cover the frame.
- **Round 3** (eye-check of the 360 slide + 390 deal; brief-line coverage;
  design-contract gate): no new defects. 360 fits one screen with the Copy
  button showing "Copied ✓" and the paused-speak status visible; the 390
  deal board reads whole. §1 A–H all mapped to passing checks (see
  coverage above); gate (a)–(i) + H1–H5 + L1–L7 recorded below.

## Design-contract gate (a)–(i) + H1–H5 + L1–L7 (PASS/N/A with the measurement)
- (a) zero white/light backgrounds — PASS: obsidian throughout; the deal
  board and world cards are obsidian with colored top edges; screenshots
  at 1440/390/360 show no light background.
- (b) every element raised/elevated — PASS: world cards + deal board +
  doors elevated with rims + glow (purple/green/gold); hover light-up is
  the same board grammar as the names page (cards lift + glow on hover;
  doors light on hover/focus — the lit states are visible in the
  screenshots).
- (c) gauges/numbers alive — N/A: this round adds no gauges/numbers. The
  certificate number (000190/000191) is a live registry number, not a
  gauge.
- (d) no text-in-image, no pasted document — PASS: Naya's portrait is a
  photo with no pasted text; congratulations + deal + cards are live text.
- (e) no bare text blocks — PASS: every line lives in a board, card, chip
  or door; no wall of bare text (screenshots).
- (f) stranger test — PASS: the end probe walked cold from the LOGIN page
  at 1440/390, 200/0; the bug verify walked the returning-browser paths
  cold, 67/0.
- (g) perfect words — PASS: the deal board's words are Shawn's Collective
  Agreement, crafted in his voice; the congratulations is verbatim; the
  world cards carry the citizen's own words, never invented.
- (h) title + subtitle + nutshell — PASS: every card carries label + title
  + words + address; the deal board carries title + subtitle + five
  nutshell points; the Smart Link chip carries the link + its line.
- (i) Naya speaks, faces alternate — PASS: her portrait + play button +
  voice on the end slide; the citizen's words on the cards and pages.
- H1 stranger test — PASS: cold walks, 200/0 + 67/0.
- H2 perfect-words — PASS: deal terms verbatim to his dictation; card
  words are the citizen's own, read back word for word.
- H3 face quality — PASS: Naya's portrait crisp at 1440 and 390
  (screenshots `end-slide-1440.png`, `end-slide-390.png`); no distortion.
- H4 test in his head — PASS: finish → world cards → click → your page,
  your words (card + door click-throughs at 1440 + 390).
- H5 one ultimate ten — PASS: one walk, one Box, one project, three pages,
  one Hub, one end slide; the deal board is the one closing board, the
  heal gate adds no second path.
- L1 stranger — PASS (cold walks). L2 perfect words — PASS (deal verbatim,
  cards the citizen's words). L3 title+subtitle+nutshell — PASS (cards +
  deal board). L4 Naya speaks, faces alternate — PASS (her portrait/voice;
  citizen's words on the pages). L5 test in his head — PASS (stranger
  finds their world without instruction). L6 smart-note format — PASS
  (created pages carry the citizen's words in order — read-backs).
  L7 one ultimate ten — PASS (one end slide, one deal board, one link chip,
  five doors; nothing doubles).

## Six anti-repeat items (brief §5, verbatim)
1. Never report done from scroll-0 checks alone. — Kept: verification
   walked the whole flow at 1440/390/360, scrolled steps, building → end →
   Hub → pages; the deal board + cards were eye-checked scrolled, not just
   at scroll 0.
2. Never claim without a live measurement. — Kept: every claim above
   carries a check, a sha, or a screenshot.
3. Never paste dictation verbatim. — Kept: the deal board's words are
   crafted from his Collective Agreement dictation in his voice, not
   pasted; the congratulations is verbatim because it IS his line.
4. Never use the word 'blockchain'. — Kept (0 occurrences in the work).
5. Never invent a component when the harvested one exists. — Kept: world
   cards harvest the names-page boards + building-page cards; the deal
   board harvests the same board grammar; the doors are the walk's own.
6. Never present work without a live link. — Kept: staged link above,
   live and curl-verified to the filed shas.

## The seven pre-merge questions (in writing)
NOTE: no merge in this round — staged only, per the brief. The maker does
NOT merge; the staged work waits for the captain's double-check + Shawn's
eye + his tap. These answers are the law's record.
1. Did I check my own work three times? YES — round 1 (the heal gate, the
   Personal-title probe gap, the stale Mike7 expectation), round 2 (eye-
   check of the 1440/390 cards + deal, no new defects), round 3 (eye-check
   of the 360 slide + 390 deal, brief-line coverage, design-contract gate).
   Each round found NEW things in round 1; rounds 2–3 confirmed clean.
2. Is it 9 or better by my own honest score? YES — honest **9**. The
   staged site is 10 on its evidence (200/0 + 67/0, read-backs, shas); the
   round scores 9 because the v1 live-dashboard error's root cause is
   unproven (it did not reproduce, so it is adjudicated, not explained),
   Speak is wiring-proven not voice-proven, and the Box/pages live-table
   writes still wait for the server-side key.
3. What could this break? The staged worker ONLY
   (`naya-walk-beginning-staging`) + the branch. Nothing live touched: no
   live nayanet worker, no live walk, no pricing, no auto-delete, no
   install veil. The deploy changes only the staged walk/identity/welcome
   (the identity v3 heal gate is the only change since the v2 bytes the
   first maker deployed). Rollback: redeploy the previous worker.js
   (filed blob on the S2 branch, deployment `3c5a257c-0f11-4163-aae1-
   19ca1803fe07` for the S2 worker; the v2 identity bytes are the filed
   S2 blob `3760825e…`).
4. Are the automatic checks green? YES — bug-verify-v4: 67 pass / 0 fail,
   exit 0; end-probe-v2: 200 pass / 0 fail, exit 0; served bytes
   curl-verified to the filed shas; the rebuilt worker embeds the new
   identity (grep-verified + served-sha-verified); the WELCOME_ASSETS KV
   binding survived the redeploy (re-checked after the PUT).
5. Does it follow the ultimate objectives? YES, five gates: right (a new
   citizen can actually join from a shared browser; the end slide shows
   THEIR world and THE deal); truly needed (Shawn ordered both, the bug
   first); mine to do (staged only, my round); now (the round is the
   vehicle; the heal gate was the wise fix, not a shortcut); provable
   (67/0 + 200/0 + read-backs + shas).
6. Did I prove it with real measurements? YES — live bytes (curl shas),
   rendered pages (screenshots 1440/390/360), real clicks (probe
   click-throughs on every card + door + Copy + play), independent
   read-backs (Box/project/pages/Hub via API + curl).
7. Is there anything in here not ten out of ten that I'm knowingly leaving?
   YES, named: (a) Box/pages live-table writes wait for the server-side
   key — KV-fallback reported in every completion response, never hidden;
   (b) Naya's real-voice recording is owed (speechSynthesis wiring only);
   (c) the v1 live-dashboard unpkg error did not reproduce — adjudicated
   as a live-page asset error, root cause unproven; (d) the live splice is
   his hand; (e) the walk's corner-gem frame overlaps headings at exact
   scroll-top (pre-existing, all steps, cosmetic); (f) the composing
   certificate echoes the typed alias pretty-printed ("Mike9") while the
   citizen has not yet claimed — S2 behavior, kept, not redesigned here.

## Filed blobs (branch `walk/end-slide-10-20261112`, verified by read-back)
Commit 1: `891580ba311ff3bec6c012948ca932bbd6751b56` — "End slide 10/10 +
new-account fix (identity v3 heal gate)". Parent: S2 tip `dbc2f7be`.
- `walk-beginning-fixed.html` — sha `16da2b97…`, 3,342,188 B, blob
  `be2883d4dd0d1feaeb84d4b25c718628ba3399e4`
- `identity-fixed.html` — sha `55fdffa8…`, 310,455 B, blob
  `6197fc1d39ece90cc7ddc06e837765a3aad46ba8`
- `welcome-staged.html` — sha `51b42b87…`, 626,198 B, blob
  `3974d813adb76bef3268279ed9a49c622200f0ab`
- `build-beginning-staging-worker.py` — sha `3fd40fa9…`, blob
  `16da99cbe89d75c58f5104155a533e4fa59dcc4e`
- `walk-beginning-staging-worker.js` — sha `05dbc26c…`, 4,316,482 B, blob
  `96cf5e671c8ce4c8ae22ee493733f06b9a4565f2`
- Probes + results + transforms + screenshots in
  `TEAM-NITRO/walk/end-slide-10-20261112/` (32 files total in commit 1;
  key blobs: `bug-verify-v4.py` `9f61616a…`, `bug-verify-results-v4.json`
  `735198c2…`, `end-probe-v2.py` `0c633cdf…`, `end-results-v2.json`
  `471648a3…`, `bug-verify-v3.py` `d71fe717…`, `bug-verify-results.json`
  `3c3360ac…`).
- Deployed: `a11843905af24961925401a5710b7e1d` (identity v3 PUT 23:38:15Z).
  Served `/welcome` sha `16da2b97…` = filed walk sha; served
  `/identity.html` sha `55fdffa8…` = filed identity sha; served `/` sha
  `51b42b87…` = filed welcome sha (curl-verified after the PUT).
- Commit 2 (this RECORD + SCORECARD + the filing script) follows below.

## NOT-DONE (named, never hidden)
No merge, no PR, no live deploy — staged only, waits for the captain's
double-check (returning-browser path first) + Shawn's eye + his tap · live
splice (his hand) · Box/pages live-table writes (server-side key, his hand)
· Naya's real-voice recording (later step) · the walk's LIVE identity still
carries the old certificate (surgical splice, his hand) · install veil (his
call) · auto-delete machine · the v1 unpkg error's root cause (unproven,
did not reproduce) · cleanup of the test identities (see below).

## Test identities to clean up (with the standing cleanup list)
This round claimed (registry rows + KV `complete_<alias>` keys + Box/project
rows): endwalk3, endwalk4, endwalk5, endwalk6, bugowner7, bugowner8,
bugowner9, bugowner10, healwalk1, healwalk2, mike7, mike8, mike9,
bugfresh1, bugfresh2, bugfresh3 (certs Nº 000183–000191). Delete rows +
keys together, maker + checker + re-checker + captain agreeing the list
first — never by one seat alone. The live `shawnvibe` row is NOT test data
and is never touched.
