# BRIEF — AUTO-TRANSLATE SETTINGS-PANEL FIX (Area #41, 2026-11-13)
## Captain: Naya Nitro Narzan · Owner seat: Wrena (BUILD) · Base: the auto-translate staged bytes

## Bullseye (one line)
The Settings panel speaks Spanish, French and German like the rest of the chrome — every label in it changes when the language changes, with nothing left in English.

## Why this round exists
The auto-translate round (maker 9/10, checker PASS) proved the tabs, rail, + menu, bottom bar and note translation — but the captain's double-check caught the Settings panel still reading English after a switch to Spanish. The brief named the Settings rows explicitly as part of "the whole chrome" ("every label on the page carries a translation"). The checker's probe set never opened the Settings panel, so the gap slipped through. This round closes it. Nothing else changes.

## Done first — defined before the work

**Exact element:** the staged Personal complete page at branch `personal/auto-translate-20261113`, tip `f9242820df009ce0270b2e4ad93cd5cbe98a170c` (1,621,175 B, sha `28ca21fa376ddaeb7a8a51f935407e7465bff68fd79d3d99b03958b83c8e4403`) — specifically its Settings panel: the "Your Preferences" heading, the "Notifications" heading, every Settings row label and sub (Deep black, Notifications, Smart Tabs drift, Motion & glow, Auto-refresh, Public profile, and any other row the panel holds), and the language picker labels themselves.

**Exact change:** every label in the Settings panel is added to `MW_I18N` in Spanish, French and German, marked with `data-mw-tr` where the `mwApplyLang` pattern reaches, and extended through the `byId` map where it does not. Proper names never translate (Naya, NayaNET, a citizen's alias). Icons never translate. The language picker in Settings stays the one picker — no second picker is built. The mechanism is the round's own proven dictionary; this is data + marking for one panel, not a new design.

**Proof (the maker proves all of this, first-hand, on the staged bytes):**
1. Inventory the Settings panel first-hand from the staged file — every heading, every row label, every sub — and list them in the record before editing.
2. Switch to Spanish, open the Settings panel, and show every label changed (screenshot at 390). Repeat for French and German (screenshots at 390). Zero English labels left in the panel in any of the three languages, except proper names.
3. Grep the staged bytes for Settings-panel labels without a translation marker — zero left — and record the count before and after.
4. Regression: the switch still works on the tabs, rail, + menu and bottom bar (the checker's green set), and a note Translate tap still works end to end with the original one tap away.
5. Add the credit line owed to the first maker in the record, by name: her dictionary preserve-step regex fix (DE values leaking into es/fr) and the Unicode-aware icon regex (`\p{L}` not `\w`, line 20436) are real, in the build, verified first-hand by the second maker.

**Exact measurement:** the Settings-panel inventory is counted before the fix (every heading, row label and sub listed in the record) and after (zero English labels left in the panel in es/fr/de except proper names); grep count of Settings-panel labels without a translation marker = 0; zero overflow at 390/1440/360, zero console errors.

**Must NOT:**
- No live touch, no merge, no PR. Staged only, on a new branch from the auto-translate tip.
- No change to the Settings gear's open/close behaviour (unproven quirk — leave it; the corrections round owns it if it is real).
- No change to the welcome sentence or the world names (proper names / citizen's own words — correctly untranslated).
- No new vendor, key, framework, or picker. No blanket auto-translation on load.
- No change to the drawer links, the chat tap, or the fail view — those are the round's named gaps, not this fix.

## Possibility proof (why this is buildable)
The mechanism is proven and live on the staged bytes: `MW_I18N` holds 167 keys per language, `mwApplyLang` rewrites marked elements, the picker persists. The Settings rows are plain markup (`os-setrow-main` blocks, 22 of them, 2 currently marked) — the same marking pattern the round already applied 114 times. The staging worker and its Workers AI binding are untouched by this fix.

## Harvest sources

- The round's own build script: `~/workspace/team-nitro/auto-translate-20261113/build-auto-translate.py` — the grown dictionary and the marking pattern are harvested from it, verbatim.
- The grown dictionary: `~/workspace/team-nitro/auto-translate-20261113/dict-final.json` — 167 keys per language, the source for the new Settings keys.
- The staged bytes the fix edits: `~/workspace/team-nitro/auto-translate-20261113/captain-staged-check.html` — the captain's first-hand copy of the tip, sha `28ca21fa376ddaeb7a8a51f935407e7465bff68fd79d3d99b03958b83c8e4403`.
- The chrome inventory that names Settings rows in scope: `~/workspace/team-nitro/auto-translate-20261113/CHROME-INVENTORY-20261113.md`.

## Files
- Captain verdict this fix answers: `~/workspace/team-nitro/auto-translate-20261113/CAPTAIN-VERDICT-AUTO-TRANSLATE-20261113.md`
- Brief the fix completes: `~/workspace/team-nitro/auto-translate-20261113/BRIEF-AUTO-TRANSLATE-20261113.md`
- Base staged bytes (captain's copy): `~/workspace/team-nitro/auto-translate-20261113/captain-staged-check.html`

## §0 — The five gates (the Wise One manifesto — run before every consequential action)

- **Gate 1 — Is it right?** Yes: a citizen who picks Spanish should read the whole page in Spanish, including the panel where they picked it. Leaving it English is the half-done shape.
- **Gate 2 — Is it what they truly need?** Yes: the brief promised every label; the Settings panel is where a citizen meets the language choice itself.
- **Gate 3 — Is it mine to do?** Yes: the captain's double-check sends a below-9 round back in; the fix is staged only, no live touch, no merge, no money, no credentials.
- **Gate 4 — Is now the time?** Yes: the corrections round is held behind this landing, so the fix unblocks the queue rather than adding to it.
- **Gate 5 — Can I prove it?** Yes: switch to es/fr/de, open the panel, every label changed, screenshots at 390; grep the staged bytes for unmarked Settings labels — zero left.

## Design-contract gate (a)–(i) + human checks H1–H5

- **(a)** zero white/light backgrounds — the fix adds words, not backgrounds; the Settings panel keeps its obsidian boards.
- **(b)** every element raised/elevated — no new elements; the existing rows keep their elevation.
- **(c)** gauges/numbers alive — the points pill keeps its living number; the fix touches labels only.
- **(d)** no text-in-image — no new images.
- **(e)** no bare text blocks — the panel rows are boards with icons and labels, as built.
- **(f)** no look-alike — the dictionary IS the page's own `MW_I18N`; nothing is remade to look like it.
- **(g)** `##` format — this brief and the record use `##` sections.
- **(h)** no dictation-blunt phrases — no new public copy is invented; the dictionary holds the page's own words in three languages.
- **(i)** title+subtitle+nutshell + faces alternate — not applicable to a settings panel; the note page keeps its shape.
- **Human checks H1–H5:** H1 stranger test (a Spanish speaker opens Settings and reads it) · H2 perfect-words law · H3 face quality (the panel's icons unchanged) · H4 test in his head · H5 one ultimate ten — attested with evidence in the handoff.

## Anti-repeat list (the six known failure modes — as prohibitions)

- never paste dictation verbatim — take the meaning, craft the words.
- never use the word 'blockchain'.
- never invent a component when the harvested one exists — harvest, don't invent.
- never report done from scroll-0 checks alone — scroll 0 AND scrolled, at every width.
- never claim without a live measurement — live bytes, never with claims; receipt before report.
- never present work without a live link — no link = not done.

## Verification plan

**Method:** Playwright (or real browser), fresh profile per width — phone 390 FIRST, then desktop 1440, then true 360. **Zero overflow** at scroll 0 AND scrolled; **zero console errors**; zero page errors. **Named no-regressions:** the tabs, rail, + menu and bottom bar still switch (the checker's green set); a note Translate tap still works end to end with the original one tap away; the pill still settles live; the language choice still persists across reload.

**Settings proof:** switch the picker to Spanish, open the Settings panel — every heading, row label and sub reads Spanish (screenshot at 390). Repeat for French and German. Grep the staged bytes for Settings-panel labels without a translation marker — zero left. The checker re-runs this battery on the staged bytes, not the local file alone.

**Staged link:** the proof-host staged link for the fix branch, same bytes as local (sha re-verified at round end).

## Should this exist — host page + no duplicate

**Host page: the Personal page — the citizen's world.** This work lives on Personal and its Settings panel; it attaches to Personal, it does not duplicate it. **No new page is built** — Personal IS the template every page clones from, so what lands here rides the clone to Business and Space. It duplicates nothing: the dictionary is grown, not replaced; the mechanism is the round's own proven one.

## Edit, don't create — base file, no fresh build

**The base file is** the Personal complete page on branch `personal/auto-translate-20261113`, tip `f9242820df009ce0270b2e4ad93cd5cbe98a170c` (1,621,175 B, sha `28ca21fa376ddaeb7a8a51f935407e7465bff68fd79d3d99b03958b83c8e4403`) — edited in place through the round's own build shape, filed as its own commit on a new branch from that tip. **Edit this file** — never rebuild it. No new file is created except the round's own record + scorecard + proof updates in the work dir, which are the round's evidence, not a page.
