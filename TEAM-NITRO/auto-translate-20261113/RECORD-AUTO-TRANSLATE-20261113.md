# RECORD — AUTO-TRANSLATE: pages speak your language, and you can see what to do
## Area #41 · 2026-11-13 · Fresh maker (second maker) · Captain: Naya Nitro Narzan · Owner seat: Wren (BUILD)

**Branch:** `personal/auto-translate-20261113` (parent `5b1a8ccc1`, the Personal
complete tip).
**Staged link:** https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/personal-page-complete-20261113/personal-complete.html&ref=personal/auto-translate-20261113&cb=<FINAL COMMIT SHA — see §7>
**Built file:** `TEAM-NITRO/personal-page-complete-20261113/personal-complete.html`
— **1,621,175 B, sha256 `28ca21fa376ddaeb7a8a51f935407e7465bff68fd79d3d99b03958b83c8e4403`**,
23,547 lines.
**Work dir:** `team-nitro/auto-translate-20261113/` (this round's files; the
filed copies live under `TEAM-NITRO/auto-translate-20261113/` in the repo).

## §0 — An honest note: I am the second maker

The first maker built this round 16:45–17:26Z and died 17:30:24Z on a runtime
transport failure (sqlx pool timeout) — not a task failure. I started fresh
from her work dir at 17:31Z. What I found, first-hand, and what I did about
it:

- **Found built, not run.** Her build script had run (worktree file sha
  `59e420a8…`, 1,616,265 B — NOT the base `4872414a…`), the grown dictionary
  (167 keys/language), the Translate module and the staging worker were all
  in place. Part 1 was proven at 390 (`verify-a-390.json`, 17:23Z). Part 2
  and Part 3 were UNPROVEN, and there was no record, no scorecard, no
  staged link, no branch.
- **Her verification scripts were stale and could never have passed.** Her
  `verify-b.py` / `verify-local.py` click `.mw-tr-src`, `.mw-tr-showorig`,
  `.mw-tr-back` and read `.mw-tr-err` / `.mw-tr-picker` — none of those
  classes exist in the module she built. The module's real classes are
  `.mw-tr-pick` > `.mw-tr-lang`, `.mw-tr-view` + `.mw-tr-label`,
  `.mw-tr-orig`, `.mw-tr-view.mw-tr-fail`. I wrote `verify2.py` against the
  real classes and re-proved Part 2 from scratch. Her `verify-a.py` (Part 1)
  was sound; I re-ran it at all three widths on the rebuilt file.
- **Her Part 1 proof already showed the gap.** `verify-a-390.json` records
  `trBtns: 0` — I confirmed first-hand this is CORRECT on a fresh load (the
  wall holds only the "No posts yet" empty-state card, zero
  `article.intel-board`), not a defect. The Translate tap attaches when a
  card exists.
- **Two real defects she had not found.** (1) The wall repaint kills an
  in-flight Translate tap (§4). (2) The three drawer worlds had no icon
  twins, so the no-words step "find your world" could not tell them apart
  (§5). I fixed both in the round, rebuilt from the pristine base twice,
  and re-verified everything below.
- **A commit was filed mid-round, not by me.** At 17:50:32Z, while I was
  verifying, branch `personal/auto-translate-20261113` appeared on the
  remote as one commit `5bd5b35f7` ("Auto-Translate (Area #41)..."), holding
  my 18:00-rebuild file minus the drawer fix and NO record/scorecard/proof.
  Its message claims verifications that had not been run at 17:50
  ("translations read back whole; honest failure; no-words 5-step pass at
  390 and 1440") and "icon twin for every text-only chrome control" — the
  drawer worlds had none. Parallel files appeared in the work dir at the
  same time (`nowords-390/1440-*.png` 17:49–17:50, `proof-390-translated.png`
  17:39) from a hand I cannot identify; no script or JSON came with them,
  so I rely on none of them. This filing REPLACES that interim commit with
  one truthful commit (same parent `5b1a8ccc1`, same branch): the page below
  plus the record, scorecard, proof, sources and evidence. Nothing in this
  record rests on the interim commit or the parallel files.

## §1 — The five gates (applied to this round)

1. **Is it right?** Yes. A citizen who reads no English gets the page in
   their language and can work it from the objects alone; their own words
   are never replaced, never stored as a translation, never auto-translated
   in bulk. No harm surface: no new vendor, no key, no live touch.
2. **Is it what they truly need?** Yes — the bullseye: a citizen who reads
   no English opens Personal, the page speaks their language, and they can
   see what everything is and how to work it from the objects alone.
3. **Is it mine to do?** Yes. Staged only, on the brief's branch, inside
   the brief's scope. The one protected-adjacent act — force-updating the
   branch ref to replace the interim commit — is the brief's own filing
   instruction ("file the branch, one commit"), and the replacement removes
   false verification claims rather than adding any.
4. **Is now the time?** Yes. Base verified unmoved at every rebuild; the
   worker binding proven live before any edit; verification complete before
   filing.
5. **Can I prove it?** Yes — every claim below carries a sha, a line
   number, a count, a JSON file or a screenshot, all read first-hand in
   this round.

## §2 — Base verification + the state I found the worktree in

- **Base (brief §Base files):**
  `/home/hatch/workspace/personal-complete-wt/TEAM-NITRO/personal-page-complete-20261113/personal-complete.html`
  — 1,555,404 B, sha256
  `4872414a1d428a940a4e12ac31c419f999843a2fde072a9ac91d09b42051c666`.
  Re-verified by `sha256sum` before EACH rebuild (three times); the base
  assertion inside `build-auto-translate.py` also passed each time. The
  parent commit `5b1a8ccc1` (full
  `5b1a8ccc1d5b59bd4d2b49f2c80e83a46c695159`) did not move during the round;
  its blob IS the base sha. The worktree branch moved once — the 17:50Z
  interim commit (§0) — the base never did.
- **State found (17:31Z):** worktree file sha
  `59e420a88ac864ad141dc4ba8c00c128ecb0afad8bbae042f1104b6f3360cf23`,
  1,616,265 B — the first maker's build HAD run (build script's base-sha
  assertion would have refused a re-run, correctly). Markers present:
  `id="mw-translate"` + `id="mw-translate-css"`, 167 keys/language in
  `MW_I18N`, `data-mw-tr` 89 occurrences (line count; 112 by string count).
  I did NOT re-run her build on that file. I restored the pristine base
  from `5b1a8ccc1` and rebuilt from source twice (§3).
- **Rebuild 1 (repaint fix, §4):** 1,620,745 B, sha
  `13530a2f76fc1bab277978f70fe438dc9fad80e5bffbea7720417c947d4520b8`.
- **Rebuild 2 — FINAL (repaint fix + drawer gems, §5):** 1,621,175 B, sha
  `28ca21fa376ddaeb7a8a51f935407e7465bff68fd79d3d99b03958b83c8e4403`,
  23,547 lines. `data-mw-tr` 114 occurrences (112 markup + 2 from the
  substring `data-mw-tr-key` inside the translate module), `data-mw-ph` 5.
  Every number in §4–§6 below was measured on this final file.

## §3 — Step 0: the translation machine, proven live

- **Bindings (read first-hand):**
  `python3 ~/workspace/project-intelligence/cf-worker.py get-bindings
  b5e2a51b3e883f7722287c5f51b1196b naya-auto-translate-staging` → HTTP 200,
  `[{"name":"AI","project":"<catalog>","type":"ai"}]`. The AI binding IS
  live on the deployed staging worker. No stop condition triggered.
- **Script read-back:** `get-script` for the same worker → HTTP 200,
  3,521 B (multipart envelope; local source 3,337 B, sha
  `32b5647d1eb110a991a7033ec1314e10f277c04727cde5420be7d6373fb8988d`),
  envelope contains `env.AI.run` + `m2m100` — the deployed bytes are this
  round's worker (`naya-auto-translate-staging-worker.js`).
- **Live test translation (curl, before any edit):**
  `POST https://naya-auto-translate-staging.nayapower.workers.dev/translate`
  `{"segments":["El sol sale sobre la ciudad."],"source_lang":"es","target_lang":"en"}`
  → HTTP 200,
  `{"ok":true,"source_lang":"es","target_lang":"en","segments":["The sun rises over the city."],"translated_text":"The sun rises over the city."}`.
  Real translation, no key, no new vendor — Workers AI
  `@cf/meta/m2m100-1.2b` on the platform already used.
- **Box fork (grounded first-hand):** zero occurrences of `preferences` in
  the built page; the picked language lives only in localStorage
  `mw.set.lang` (`mwGet`/`mwPut`, built-file lines 19950–19951; read line
  20415; write line 20527). There is no citizen-preferences record on the
  page to write to. The Box write is a named follow-on, never claimed.

## §4 — Part 1 + Part 2: the chrome speaks, the words translate

### The build
`build-auto-translate.py` (work dir, edited only to add §12b drawer gems;
the translate module `mw-translate.js` edited for §4's repaint fix).
Shape: base-sha assertion → span-replace the language block with
`mw-lang-block.js` + `dict-final.json` → 18 numbered edit sections →
inject `mw-translate.css` + `mw-translate.js` before `</body>`.
Final built markers: `MW_I18N` line 20407 (167 keys in es/fr/de);
`mwBrowserLang`/`mwLangCode`/`mwApplyLang` grown in place; translate CSS
line 23194 (`<style id="mw-translate-css">`), module line 23225
(`<script id="mw-translate">`), endpoint line 23239
(`https://naya-auto-translate-staging.nayapower.workers.dev/translate`);
drawer gems lines 4821–4823.

### Chrome inventory (first maker's count, adopted after spot-checks)
`CHROME-INVENTORY-20261113.md` + `inv-keys.json` + `inv-tr-keys.json`:
165 keys (158 chrome + 'In a nutshell' + 'open' + 6 creator/chat keys);
the grown dictionary holds **167 keys per language** (es/fr/de), covering
every inventoried key in all three languages, zero fallbacks to English
except proper names. Corrections to the brief found first-hand and kept:
the dictionary held 18 entries / 17 distinct keys, not 12; the visible
row is 8 buttons but the `byId` map names 11 (statsbtn + intelbtn are dead
ids, settingsbtn is the gear, icon-only per R20); NO numbered guide-steps
block exists on the page (0 hits for 'Step 1/2/3', '1-2-3') — none was
invented; the bottom bar was already icon-only. Out of inventory, named
(not silent): the inner rooms, the Smart Access course pane + PowerCast
player, the wall meta line (plural templates), chat send-status lines,
the owner's tagline, the hidden old plus menu.

### Part 1 proof — language switching (re-run by me on the FINAL file)
`verify-a.py` at 390, 1440, 360 → `verify-a-{390,1440,360}.json`:
- **Page errors: [] at all three widths. Overflow: 0 at scroll 0 AND
  scrolled at all three widths** (sw == iw: 390/390, 1440/1440, 360/360).
- **Console errors: 60 / 42 / 56 — every one Supabase** (`console_non_supabase:
  []` at all three widths). The count varies run to run (42–60); all are
  the known environmental failed-external-fetch set, never page errors.
- **Language switch (all widths):** picker es → `msgbtn` "✉️ Mensaje",
  `skillsbtn` "⭐ Habilidades", `tabPublic` "🌍 Feed inteligente público",
  `feedline` "MATCH → ORGANIZAR → CONECTAR", `railHead` "La gente a tu
  alrededor"; fr → "✉️ Message" / "⭐ Compétences" / "🌍 Fil intelligent
  public"; de → "✉️ Nachricht" / "⭐ Fähigkeiten" / "🌍 Öffentlicher
  Smart-Feed". `documentElement.lang` follows the pick; the pick persists
  across reload (`stored: "de"` after reload).
- **First visit:** locale es-ES → page picks es with no tap (`stored:
  null` — no pick stored, the default is the browser's); locale ja-JP →
  falls back to en, no banner, no error.
- **No-regressions green set (all widths):** tabs `✦ Personal` /
  `🌍 Public smart feed` / `✦ Naya Notes` (icon twins on all three);
  rail 20 cards; + menu 5 items; bottom-bar segs
  `plus/mail/activity/spaces/eco` with translated aria-labels;
  wallCards 1 (the "No posts yet" empty-state card — the only card on a
  fresh load); **pill "0"** — see the honest note below, it is NOT a
  regression.
- **Pill note (honest):** on `file://` the points pill reads `…` → `0`
  because the live points fetch cannot run (the same environmental fetch
  stop behind the Supabase console errors). The Personal-complete record
  proves the pill resolves to live 25 on a staged/live session; the pill
  is untouched by this round (no points-round lines edited — the build
  script never touches `#pointscount` except the `pts` label's
  `data-mw-tr`). The staged verification (§7) re-checks the pill on the
  served bytes.

### Part 2 proof — Translate taps (re-proven by me on the FINAL file)
`verify2.py` → `verify-b2-390.json` (390; the brief's first width).
Console 54, all Supabase (`console_non_supabase: []`); page errors [];
overflow 390/390.
- **es → en, multi-sentence (the segmentation proof):** 3-sentence Spanish
  stub ("El sol sale sobre la ciudad y todo se llena de luz. Caminamos
  juntos por el mercado, probando el pan y hablando del futuro. La vida es
  mejor cuando se comparte.") → view labelled "🌐 Translated from Spanish",
  nutshell reads in full: "The sun rises over the city and everything is
  filled with light. We walked through the market together, tasting the
  bread and talking about the future. Life is better when it is shared."
  **All three sentences present, none dropped.** Title + subtitle +
  nutshell carried (L3). Picker offered all four native names
  (English/Español/Français/Deutsch) with the question "What language is
  this note in?" — source never assumed. Screenshot
  `proof-390-translated-es.png`.
- **fr → en:** "🌐 Translated from French" — "The morning is quiet and
  the city is slowly waking up. We drank coffee and watched the river
  pass." **de → en:** "🌐 Translated from German" — "The evening is quiet
  and the lights of the city are reflected in the river. We go home
  slowly and think about tomorrow."
- **en → es / fr / de** (page language = target each time): "🌐 Traducido
  del inglés" / "🌐 Traduit de l'anglais" / "🌐 Übersetzt aus dem
  Englischen" — the garden note translated whole into each language, the
  Translate UI itself in the picked language ("Mostrar original" /
  "Afficher l'original" / "Original zeigen").
- **Original one tap away:** "Show original" → view collapses
  (`collapsed: true`, button reads "Show translation", original nutshell
  intact underneath, "IN A NUTSHELL El sol sale sobre la ciudad…");
  "Show translation" → the view returns with its label. The card's own
  content is never removed or rewritten — the translation is a view below
  it. Nothing is stored as the note.
- **Naya-card attach (labelled synthetic):** the live Naya feed stays
  skeleton on `file://`, so the scan path was proven with a faithful
  `.ph-card` (h3 + meta p + body p) inserted into `#mwFeedNaya` — it got
  its Translate button (`naya_tr_btns: 1`). The wall path is proven on
  real stub cards through the page's own `fcStubInsert`.
- **Honest failure:** with the worker host route-aborted, the tap shows
  "Translation unavailable — the original is here" (seen, `failure_seen:
  true`), no invented view, original intact, page errors []. (The fail
  view self-removes after 6 s — the first run missed it by polling at 8–9 s;
  the proof polls every 500 ms.) Screenshot `proof-390-failure.png`.
- **Fresh-load zero is correct:** `tr_btns_fresh_load: 0`,
  `wall_cards_fresh: 0` — there are no notes to translate until one
  exists; the button appears the moment a card does (`tr_btns_after_stub:
  1`).

### The repaint defect — found, fixed, proven (fresh-maker fix #1)
- **Found:** the first Translate tap in a fresh page died intermittently
  (verify2 run 1: `es_picker: null`; the isolated failure run: picker
  `False` at +1000 ms). Polling at 100 ms intervals reproduced it:
  picker present at +100 ms, gone by +200 ms. A MutationObserver log on
  `#os-wall-list` showed the cause at +717 ms after the tap: the wall
  painter (`mwPaintWallPosts`, built-file line ~8627) rebuilt the list
  with `list.innerHTML` — stub card removed, "No posts yet" card
  re-inserted, stub re-inserted as a FRESH node. The picker (and any
  finished view) died with the old node. The repaint fires once after
  load, when the live rows land (~12–14 s), and on every tab switch and
  filter change — a citizen tapping Translate in that window lost the tap
  silently.
- **Fixed** in `mw-translate.js` (no page-mechanism change — the painter
  is the page's own, out of scope to rewrite): translate state is kept by
  CARD KEY, not by node (`pendingPick` for an open picker, `doneViews`
  for a finished translation, `inFlight` while a fetch runs; key = the
  stub id, else a hash of the card's own words; `cardKey`/`findCard`/
  `mountView`, lines 23263–23300). `attachRow` re-mounts an open picker or
  a finished view onto the fresh node; `run()` stores the result by key
  BEFORE mounting and mounts on the live node resolved by key, so a
  repaint mid-fetch still lands the view. A restored view never yanks the
  scroll (`doScroll: false` on restore).
- **Proven:** `verify-repaint.py` → `verify-repaint-390.json`: natural
  post-load repaint at 9,914 ms after the stub; the es→en view mounted on
  the live node at +12.5 s and stayed (no gaps in 50 polls after first
  sighting). `verify-repaint2.py` → `verify-repaint2-390.json`:
  FORCED repaint (`window.mwPaintWallPosts(window.MW_WALL_POSTS||[])`)
  while the picker was open → picker re-appeared on the fresh node
  (`picker_after_forced_repaint: true`); translation completed; a SECOND
  forced repaint → the finished view survived byte-identical
  (`view_after_second_repaint` == `view_after_translate`). Page errors []
  in both. Screenshots `proof-390-repaint-view.png`,
  `proof-390-repaint-picker.png`, `proof-390-repaint-view2.png`.

## §5 — Part 3: the visual language — the no-words test

### The drawer-gem defect — found, fixed (fresh-maker fix #2)
- **Found:** the brief's step 2 ("find your world by the three gems")
  could not pass as built. The three worlds live in the left drawer
  (`#os-drawer`, opened by the icon-only `spaces` seg), but their links
  were bare text — no icon, no marker; `--rc` only shows on hover. With
  words hidden the three rows were three identical dark boards.
- **Fixed** in the build script (§12b, three `rep()`s, count-asserted):
  each world link carries the tab twin's own span
  (`<span class="os-jewel os-jewel-sm" style="--jc:<its --rc>">✦</span>`)
  in the colour the page already assigns that world in this drawer —
  Personal `#3fb8ff`, Business `#2fe89e`, Space `#ffbf3d` (built-file
  lines 4821–4823). The other drawer links stay text-only — navigation,
  not one of the five no-words steps; named here as a gap, not claimed.
  The inventory's "no new icon twins for drawer labels" line is corrected
  by this fix for the three worlds, which ARE reachable chrome.

### The test
`verify3.py` → `verify-nowords-{390,1440}.json`. Hiding method: a style
rule makes all text transparent EXCEPT the icon twins (`.os-jewel`),
the + menu icon spans (`.fc-pi-ico`) and the bottom bar
(`#naya-notif-bar`, whose SVGs use `currentColor`). Emoji (💬✉️🌍⭐🔊🎥)
render in full colour regardless of `color`, so they stay visible; only
word-glyphs vanish. Layout untouched (no font-size/display change).
Page errors [] and overflow 0 at both widths; console 42/42, all Supabase.

| Step | 390 tap target (x, y, w×h) | 1440 tap target (x, y, w×h) | Result |
|---|---|---|---|
| 1 ENTER — land, know you're in | cover (0,0,390×420) visible; 8 hero buttons as shapes (110×46); pill (185,414,30×26) | cover (0,0,1440×464); hero buttons 147×49; pill (397,307,30×26) | PASS — landing IS entering; the orb + row + pill read as shapes |
| 2 FIND YOUR WORLD — three gems | `spaces` seg (232,786,50×48) → drawer opens; worlds at (14,103/160/217,272×49), jewels 23×23 at x=27: Personal `#3fb8ff`, Business `#2fe89e`, Space `#ffbf3d` | `spaces` seg (787,778,66×56); same three rows + jewels | PASS — colour + position tell the worlds apart; drawer closes via backdrop |
| 3 READ THE FEED — tabs | Public tab (138,384,114×75), 🌍 jewel `#3fb8ff` → `aria-selected: true`, active | Public tab (379,396,343×51), 🌍 jewel | PASS |
| 4 MAKE A POST — + menu | `plus` seg (46,786,50×48) → menu, 5 items with icons ✎/✎/✦/💬/✉️ (202×48 each); item 0 (9,527) → composer visible (hint 302×69, input 302×89), menu closed | `plus` seg (487,778,66×56); items at x=419; composer 660×89 | PASS |
| 5 TALK TO SOMEONE — rail | rail card (16,331,356×181); Chat button (29,464,78×35), 💬 icon → chat panel opens (`#fcChat` 358×339, flex, visible) | rail card (1096,332,318×181); Chat (1109,465,69×35) → chat 380×339 | PASS |

Screenshots (all words hidden, icons lit): `proof-{390,1440}-nowords-1-enter.png`,
`-2-worlds.png`, `-3-feed.png`, `-4-plusmenu.png`, `-4-composer.png`,
`-5-talk.png`. The 390 `-2-worlds` shot is the proof of fix #2: three
elevated boards, each with a lit jewel — blue, green, gold.
Honest limits: the orb's class did not match my probe selector (`orb:
null` in both JSONs) — the cover itself is the enter proof and the
screenshots show it; the orb selector is a probe gap, not a page gap.
The world links were NOT followed (they navigate to nayanet.app) — the
step's proof is the drawer open with the three jewelled rows, recorded.

### Lists room (no-regression, brief's green set)
Clicking the Lists entry opens the room: `#lists.ph-sec.os-view.on`
visible ("📋 Smart Lists"), input `#os-list-input` + Add button visible,
page errors []. Probed first-hand (`/tmp/pw-lists.py`).

## §6 — DONE definition (brief §Done first, checked)

- **Exact element:** the staged Personal complete page — chrome, feed
  cards, language picker. DONE — all of it carries the grown dictionary
  and the Translate tap.
- **Exact change (1)** dictionary grown 17 → 167 keys/language, whole
  chrome, through `MW_I18N` + `mwApplyLang`, no new framework. DONE.
- **(2)** first visit reads `navigator.language`, nearest held language
  or English; the Settings pick rules and persists. DONE (es-ES → es,
  ja-JP → en, reload persistence, all widths).
- **(3)** every note/message carries a Translate tap: real translation,
  labelled source + target, original one tap away, never replaced, never
  stored. DONE (wall + Naya scan paths; chat-message path built the same
  way — its tap is attached by `scan()` on `#fcChat .fc-chat-msg`; not
  exercised live in this round because no chat messages exist on a fresh
  load — named, not claimed).
- **(4)** every text-only chrome control in the five-step flow has an icon
  twin harvested from the page's own set. DONE for the flow (tabs, rail
  buttons, + menu, bottom bar, drawer worlds). NOT done for the other
  drawer navigation links — named gap in §5, follow-on.
- **Exact measurement:** dictionary 167/167/167 keys, zero fallbacks
  except proper names; language switch at 390/1440/360 with zero page
  errors; Translate tap real for es/fr/de notes and en into es/fr/de;
  multi-sentence note whole (3/3 sentences); honest failure; no-words
  five steps at 390 + 1440. DONE.
- **What must NOT be there:** no new framework/vendor/key — none. No
  silent replacement — none (views only, labelled). No blanket
  auto-translation — none (on tap only). No invented language — none
  (viewer picks the source). No Ask Naya touched — untouched. No Hub
  toggle rewired — untouched. No live touch — none. No new page — none.
  RTL — not claimed (named follow-on). Personal corrections round NOT
  folded in — not touched (cover top, points pill, side rail as the
  corrections round defines them are queued behind this round).
- **Design-contract gate (a)–(i):** (a) no new backgrounds — the
  translation view and picker are obsidian boards; (b) elevated — both
  are elevated boards/buttons, never flat text; (c) counts alive — 167
  keys, 20 rail cards, pill number untouched; (d) no text-in-image — no
  new images; (e) no bare text blocks — the translated note is a labelled
  board with its original one tap away; (f) no look-alike — the dictionary
  IS `MW_I18N`, the icons ARE the page's own set, the machine IS Workers
  AI on the platform already used; (g) `##` format — this record; (h) no
  dictation-blunt phrases — no new public copy invented; (i)
  title+subtitle+nutshell + faces alternate — the translation carries all
  three; chrome, words and pictures are the faces. Human checks H1–H5:
  H1 stranger test — the no-words test (§5); H2 perfect-words — the
  translation is the note's own words in another language; H3 face
  quality — the twins are the network's own jewels/emoji/SVGs; H4 test in
  his head — a citizen in any country opens the page and works it; H5 one
  ultimate ten — the page speaking your language AND working with no words
  at all, together, on the same page.

## §7 — Staging + filing

- **Staged link:** https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/personal-page-complete-20261113/personal-complete.html&ref=personal/auto-translate-20261113&cb=eeb5db00814b8bd3d12f16edc25b8ecf7e4ab791
- **Staged bytes vs local:** curl of the staged link → HTTP 200,
  1,621,175 B, sha256 `28ca21fa376ddaeb7a8a51f935407e7465bff68fd79d3d99b03958b83c8e4403`
  — BYTE-IDENTICAL to the local final file. Markers present on staged
  bytes: `mw-translate` 2, `os-jewel os-jewel-sm` 32.
- **Staged verification** (`verify-staged.py` → `verify-staged.json`,
  390, on the served bytes): page errors []; console 60, all Supabase
  (`console_non_supabase: []`); overflow 0 at scroll 0 AND scrolled;
  green set — tabs `✦ Personal / 🌍 Public smart feed / ✦ Naya Notes`,
  rail 20 cards, + menu 5 items, wall empty-state (0 real cards — the
  live collective did not load in this session either), pill "0" (same
  fetch stop as local; base pill is also "0" in the identical environment
  — proven not a regression, §4); language switch on staged bytes — es:
  `msgbtn` "✉️ Mensaje", `tabPublic` "🌍 Feed inteligente público";
  live translation tap on staged bytes — Spanish stub → "🌐 Translated
  from Spanish / The sun rises over the city and everything is filled
  with light. We walked through the market together." with "Show
  original". Screenshot `proof-staged-390-translated.png`.
- **Filing:** branch `personal/auto-translate-20261113`, ONE commit,
  parent `5b1a8ccc1`, via `gh-direct.py` (one API write at a time; blobs
  via process substitution, never staged to disk). Read-back verified
  (ref + commit + page blob re-read after the force-update; raw page at
  the filed commit re-downloaded: sha `28ca21fa…`, 1,621,175 B). Contents:
  the built page + `TEAM-NITRO/auto-translate-20261113/` (brief,
  inventory, build script, translate module + CSS, language block,
  dictionary, worker + meta, record, scorecard, proof, verify scripts +
  JSONs, key screenshots). The interim commit `5bd5b35f7` is replaced by
  this filing (§0).

## §8 — Three self-checks (each found NEW things)

1. **The build itself** — inventory counted before each edit; diff
   confined to the named regions (language span, 18 edit sections, drawer
   gems §12b, module injection); base sha asserted before every rebuild.
   NEW findings: the stale-selector scripts (replaced, §0); the repaint
   defect (fixed, §4); the drawer-gem defect (fixed, §5); the interim
   commit with false claims (replaced, §0/§7). The diff was re-read after
   each rebuild (line numbers in §4).
2. **The browser + curl proof** — new evidence at every width and every
   language: verify-a ×3, verify2, repaint ×2, nowords ×2, Lists probe,
   worker curl + bindings read. NEW findings: the first-tap flake is a
   repaint, not a click miss (proven by the 100 ms poll + mutation log);
   the fail view self-removes after 6 s (first runs missed it by polling
   too late); the pill "0" on `file://` is the fetch stop, not a
   regression (proven by the base's own behaviour + the Personal record).
3. **The proof itself** — re-read the diff, re-ran the samples, confirmed
   the base did not move mid-round (parent `5b1a8ccc1` unmoved; base sha
   `4872414a…` asserted at all three rebuilds). NEW findings: the worktree
   branch DID move mid-round (interim commit, §0) — the base did not; the
   parallel files in the work dir are unverifiable (no script/JSON) and
   are relied on for nothing; the chat-message translate path is built
   but unexercised live (§6) — named, not claimed.

## §9 — Seven pre-merge answers (in writing)

1. **Three self-checks done?** Yes — §8, each finding new things.
2. **Honest 9+?** Score 9 — see `SCORECARD-AUTO-TRANSLATE-20261113.md`.
   Deduction: the drawer navigation links beyond the three worlds are
   still text-only, and the chat-message translate path is built but
   unexercised live.
3. **Blast radius named?** Staged Personal page only. The Hub shell, the
   walk worker and live are untouched except by the named follow-ons (Box
   write, RTL, Hub toggle inheritance). No main change except this branch
   filing. No mail.
4. **Checks green?** Language proof + translation proof + no-words proof,
   all green on the final file; every exception named (pill "0" on
   `file://`, Naya attach synthetic, chat path unexercised, drawer
   navigation links text-only).
5. **Five gates?** Yes, with evidence (§1).
6. **Real proof?** Live bytes, shas, line numbers, counts, browser
   measurements and screenshots, all read first-hand in this round (§3–§5,
   §7).
7. **No silent known defects?** None silent — every gap, fork and
   not-yet-verified store read is named in this record (§0, §4 pill note,
   §5 limits, §6).

## §10 — Follow-ons (named, not silent)

- **Box write:** the picked language has no preferences record to land
  in (§3). Needs a citizen-preferences record design (owner: Box seat).
- **RTL:** content translates into right-to-left languages through the
  machine; the chrome direction flip is a named follow-on.
- **Hub toggle:** the Hub's "Language + auto-translate" toggle stays a
  dead switch; the Hub inherits the Personal mechanism as a follow-on for
  the Hub seat.
- **Drawer navigation links:** the non-world drawer links (Your Reports,
  Intel Today, Smart Factory, memberships, About Us, White Paper) are
  still text-only — twin them in a follow-on.
- **Chat-message translate tap:** built (`scan()` attaches it to
  `#fcChat .fc-chat-msg`) but unexercised live — needs a live chat
  message to prove against.
- **More chrome languages:** data-only follow-on (one dictionary object +
  one select option per language, no code change).
