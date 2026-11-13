# BRIEF — AUTO-TRANSLATE CARD-LABELS FIX (Area #41, 2026-11-13)
## Captain: Naya Nitro Narzan · Owner seat: Wrena (BUILD) · Base: the auto-translate Settings-fix staged bytes

## Bullseye (one line)
The note cards speak Spanish, French and German like the rest of the chrome — the Intelligent Block's fixed labels change when the language changes, with nothing left in English except proper names and the citizen's own words.

## Why this round exists
The Settings-panel fix passed its double-check 10/10 — the panel speaks all three languages. But the captain's eye check on that same pass caught visible English chrome outside the panel, on every note card in Spanish mode: the Intelligent Block's fixed labels ("IN A NUTSHELL", "＋ CREATE SPACE", "★ FAVORITE", "ADD TO THE INTELLIGENCE", "ADD INTEL", "ONE INTELLIGENCE · MANY VIEWS · ONE IDENTITY", "TRUST: SOURCE / INTERPRETATION SEPARATED"). The captain confirmed them in the staged bytes first-hand: visible template strings, unmarked, not in `MW_I18N`. The brief's Part 1 promised "every label on the page" and the inventory's scope line names "feed cards" — these are the page's own words, not the citizen's, and not proper names. Same miss class as the Settings panel, found the same way. This round closes it. Nothing else changes.

## Done first — defined before the work

**Exact element:** the staged Personal complete page at branch `personal/auto-translate-settings-fix-20261113`, tip `3d8f9651e54fd90ea92d640dbbe93323e448b529` (1,639,171 B, sha `d91945f6b883dff7311c320802b62ab7d0ac0fffa756a48c36e867f6fc44f3e4`) — specifically the note cards' fixed Intelligent Block labels: "IN A NUTSHELL" (the block heading), "＋ CREATE SPACE", "★ FAVORITE", "ADD TO THE INTELLIGENCE", "ADD INTEL", "ONE INTELLIGENCE · MANY VIEWS · ONE IDENTITY", "TRUST: SOURCE / INTERPRETATION SEPARATED", and any other fixed card label the maker's first-hand inventory finds.

**Exact change:** every fixed card label is added to `MW_I18N` in Spanish, French and German, marked with `data-mw-tr` where the `mwApplyLang` pattern reaches, and extended through the `byId` map or the card renderers where it does not — including labels written by the JS card builders, not just static markup. Proper names never translate (Naya, NayaNET, a citizen's alias). The citizen's own words never translate by this mechanism (they translate only on the Translate tap, Part 2). Icons never translate. The language picker in Settings stays the one picker — no second picker is built. The mechanism is the round's own proven dictionary; this is data + marking for one surface, not a new design.

**Exact measurement:** the card-label inventory is counted before the fix (every fixed label listed in the record) and after (zero English fixed labels left on a rendered card in es/fr/de except proper names); grep count of unmarked fixed card labels = 0; zero overflow at 390/1440/360, zero console errors.

**Must NOT:**
- No live touch, no merge, no PR. Staged only, on a new branch from the Settings-fix tip.
- No change to the citizen's words — the note content translates only on the Translate tap, never by this mechanism.
- No change to proper names (Naya, NayaNET, aliases, membership names, page names).
- No change to the Settings panel, the drawer links, the chat tap, or the fail view — those are other rounds' scope, not this fix.
- No change to the gear / panel dismissal behaviour (the corrections round owns it).
- No new vendor, key, framework, or picker. No blanket auto-translation on load.

## Possibility proof (why this is buildable)
The mechanism is proven and live on the staged bytes: `MW_I18N` holds 210 keys per language, `mwApplyLang` rewrites marked elements, the Settings fix proved the same pattern reaches JS-written strings (`loadSettingsData`, `renderInstallState`, the auth IIFE, the cover-slot renderer). The card labels are plain template strings in the card builders — the same marking pattern the round already applied 153 times. The staging worker and its Workers AI binding are untouched by this fix.

## Harvest sources

- The Settings-fix record (the pattern for JS-written strings): `~/workspace/team-nitro/auto-translate-20261113/RECORD-AUTO-TRANSLATE-SETTINGS-FIX-20261113.md`
- The round's own build script: `~/workspace/team-nitro/auto-translate-20261113/build-auto-translate.py` — the grown dictionary and the marking pattern are harvested from it, verbatim.
- The grown dictionary: `~/workspace/team-nitro/auto-translate-20261113/dict-final.json` — 210 keys per language, the source for the new card keys.
- The staged bytes the fix edits: `~/workspace/team-nitro/auto-translate-20261113/captain-fix-staged-check.html` — the captain's first-hand copy of the tip, sha `d91945f6b883dff7311c320802b62ab7d0ac0fffa756a48c36e867f6fc44f3e4`.
- The chrome inventory that names feed cards in scope: `~/workspace/team-nitro/auto-translate-20261113/CHROME-INVENTORY-20261113.md`.

## Files
- Captain verdict this fix answers: `~/workspace/team-nitro/auto-translate-20261113/CAPTAIN-VERDICT-AUTO-TRANSLATE-SETTINGS-FIX-20261113.md`
- Brief the fix completes: `~/workspace/team-nitro/auto-translate-20261113/BRIEF-AUTO-TRANSLATE-20261113.md`
- Base staged bytes (captain's copy): `~/workspace/team-nitro/auto-translate-20261113/captain-fix-staged-check.html`

## §0 — The five gates (the Wise One manifesto — run before every consequential action)

- **Gate 1 — Is it right?** Yes: a citizen who picks Spanish should read the whole page in Spanish, including the headings on every note card. Leaving them English is the half-done shape.
- **Gate 2 — Is it what they truly need?** Yes: the brief promised every label; the card headings are the most-seen labels on the page.
- **Gate 3 — Is it mine to do?** Yes: the captain's double-check holds the round until the page is whole; the fix is staged only, no live touch, no merge, no money, no credentials.
- **Gate 4 — Is now the time?** Yes: the corrections round is held behind auto-translate landing, so the fix unblocks the queue rather than adding to it.
- **Gate 5 — Can I prove it?** Yes: switch to es/fr/de, open the feed, every card heading changed, screenshots at 390; grep the staged bytes for unmarked fixed card labels — zero left.

## Design-contract gate (a)–(i) + human checks H1–H5

- **(a)** zero white/light backgrounds — the fix adds words, not backgrounds; the cards keep their obsidian boards.
- **(b)** every element raised/elevated — no new elements; the existing card labels keep their elevation.
- **(c)** gauges/numbers alive — the points pill keeps its living number; the fix touches labels only.
- **(d)** no text-in-image — no new images.
- **(e)** no bare text blocks — the card labels are headings inside boards, as built.
- **(f)** no look-alike — the dictionary IS the page's own `MW_I18N`; nothing is remade to look like it.
- **(g)** `##` format — this brief and the record use `##` sections.
- **(h)** no dictation-blunt phrases — no new public copy is invented; the dictionary holds the page's own words in three languages.
- **(i)** title+subtitle+nutshell + faces alternate — the card keeps its shape: title + subtitle + nutshell in the picked language; the chrome, the words and the pictures are the faces.
- **Human checks H1–H5:** H1 stranger test (a Spanish speaker opens the feed and reads the cards) · H2 perfect-words law · H3 face quality (the card's icons unchanged) · H4 test in his head · H5 one ultimate ten — attested with evidence in the handoff.

## Anti-repeat list (the six known failure modes — as prohibitions)

- never paste dictation verbatim — take the meaning, craft the words.
- never use the word 'blockchain'.
- never invent a component when the harvested one exists — harvest, don't invent.
- never report done from scroll-0 checks alone — scroll 0 AND scrolled, at every width.
- never claim without a live measurement — live bytes, never with claims; receipt before report.
- never present work without a live link — no link = not done.

## Verification plan

**Method:** Playwright (or real browser), fresh profile per width — phone 390 FIRST, then desktop 1440, then true 360. **Zero overflow** at scroll 0 AND scrolled; **zero console errors**; zero page errors. **Named no-regressions:** the Settings panel still switches (the fix round's green set); the tabs, rail, + menu and bottom bar still switch; a note Translate tap still works end to end with the original one tap away; the pill still settles live; the language choice still persists across reload.

**Card proof:** switch the picker to Spanish, open the feed — every fixed card label reads Spanish on a rendered card (screenshot at 390). Repeat for French and German. Grep the staged bytes for fixed card labels without a translation marker — zero left. The checker re-runs this battery on the staged bytes, not the local file alone — and opens the feed themselves in all three languages, reading the card headings with their own eyes (the last two checkers' lesson, applied).

**Staged link:** the proof-host staged link for the fix branch, same bytes as local (sha re-verified at round end).

## Should this exist — host page + no duplicate

**Host page: the Personal page — the citizen's world.** This work lives on Personal and its note cards; it attaches to Personal, it does not duplicate it. **No new page is built** — Personal IS the template every page clones from, so what lands here rides the clone to Business and Space. It duplicates nothing: the dictionary is grown, not replaced; the mechanism is the round's own proven one.

## Edit, don't create — base file, no fresh build

**The base file is** the Personal complete page on branch `personal/auto-translate-settings-fix-20261113`, tip `3d8f9651e54fd90ea92d640dbbe93323e448b529` (1,639,171 B, sha `d91945f6b883dff7311c320802b62ab7d0ac0fffa756a48c36e867f6fc44f3e4`) — edited in place through the round's own build shape, filed as its own commit on a new branch from that tip. **Edit this file** — never rebuild it. No new file is created except the round's own record + scorecard + proof updates in the work dir, which are the round's evidence, not a page.
