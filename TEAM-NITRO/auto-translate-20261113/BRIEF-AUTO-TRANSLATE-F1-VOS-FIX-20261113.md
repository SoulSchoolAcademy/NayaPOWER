# BRIEF — AUTO-TRANSLATE F1 MICRO-FIX: TES → VOS (Area #41, 2026-11-13)
## Captain: Naya Nitro Narzan · Owner seat: Wrena (BUILD) · Base: the auto-translate card-labels-fix staged bytes

## Bullseye (one line)
The French voice is vous everywhere — one wrong word fixed, so a French citizen reading a Naya feed card sees "VOS MOTS", never "TES MOTS".

## Why this round exists
The card-labels fix passed its checker 9/10 — the cards speak es/fr/de with zero English fixed labels left. But the checker's audit found one word the maker did not name: the new card key `YOUR WORDS — FORMATTED BEAUTIFULLY BY NAYA` carries the French value `TES MOTS — MIS EN FORME AVEC SOIN PAR NAYA`. The French voice is vous (record §3), and the sibling key fixed in the same round reads `VOS MOTS, MOT POUR MOT` — so this is inconsistent inside the round's own new keys. The checker proved it is the only tu-form among the 56 new keys, which also disproves the record §4 claim that its tu-form scan found "the only one" (it found the sibling, not this one). This round fixes the one word and corrects that claim. Nothing else changes.

## Done first — defined before the work

**Exact element:** the staged Personal complete page at branch `personal/auto-translate-card-labels-fix-20261113`, tip `2e348bb19e89ce6d4b1a3bc20130c00159d252e0` (1,652,796 B, sha `93f4302a5866a007b290ac3b144bda62c373ee16a7bfe63222e485ffc29a7b3b`) — the existing file being edited is `~/workspace/personal-complete-wt/TEAM-NITRO/personal-page-complete-20261113/personal-complete.html` (same bytes, same sha, verified first-hand) — specifically the dictionary value for key `YOUR WORDS — FORMATTED BEAUTIFULLY BY NAYA` in French, rendered on naya-type feed cards as the ibFeedCard naya-fidelity microcopy (`<span class="ib-naya-fidelity" data-mw-tr="set" data-mw-en="YOUR WORDS — FORMATTED BEAUTIFULLY BY NAYA">`).

**Exact change:** one dictionary value only — French `TES MOTS — MIS EN FORME AVEC SOIN PAR NAYA` becomes `VOS MOTS — MIS EN FORME AVEC SOIN PAR NAYA`, in `dict-final.json` and in the embedded `MW_I18N` of the built file, so the staged bytes carry it. The Spanish value (`TUS PALABRAS`, tú voice) and the German value (`DEINE WORTE`, du voice) are correct and do not change. The record §4 tu-form-scan claim is corrected to say what actually happened — the scan found the sibling key, missed this one, and the checker's audit found it. No other dictionary value changes; no marking, layout, or code changes.

**Exact measurement:** grep count of `TES MOTS` in French dictionary values = 0; grep count of `TES MOTS` in the staged bytes = 0; rendered French naya-type feed card reads `VOS MOTS — MIS EN FORME AVEC SOIN PAR NAYA` (screenshot at 390); tu-form scan of all 56 new French keys = 0 tu-forms; zero overflow at 390/1440/360, zero console errors.

**Must NOT:**
- No other dictionary value changes — one word, one value.
- No live touch, no merge, no PR. Staged only, on a new branch `personal/auto-translate-f1-vos-fix-20261113` from the card-labels tip.
- No change to the Spanish or German values, no change to any other card label, no change to the Settings panel, tabs, rail, + menu, or bottom bar.
- No change to the citizen's words — the note content translates only on the Translate tap, never by this mechanism.
- No change to proper names (Naya, NayaNET, aliases). No new vendor, key, framework, or picker.

## Possibility proof (why this is buildable)
The mechanism is proven and live on the staged bytes: `MW_I18N` holds 266 keys per language, the render site is confirmed in the staged bytes (the `data-mw-tr="set"` span plus `mwTr(...)` on naya-type feed cards), and the sibling key was fixed to `VOS MOTS` by the same one-value edit in this same round. This is one value in the same dictionary, edited the same way, verified the same way.

## Harvest sources

- The grown dictionary (the value to fix): `~/workspace/team-nitro/auto-translate-20261113/dict-final.json` — line 515 carries the wrong value.
- The card-labels fix record (the pattern and the claim to correct): `~/workspace/team-nitro/auto-translate-20261113/RECORD-AUTO-TRANSLATE-CARD-LABELS-FIX-20261113.md`
- The checker verdict that found F1 (the evidence): `~/workspace/team-nitro/auto-translate-20261113/CHECKER-VERDICT-AUTO-TRANSLATE-CARD-LABELS-FIX-20261113.md`
- The checker's audit trail: `~/workspace/team-nitro/auto-translate-20261113/checker-card/checker-audit.txt`
- The brief this fix completes: `~/workspace/team-nitro/auto-translate-20261113/BRIEF-AUTO-TRANSLATE-CARD-LABELS-FIX-20261113.md`

## Files
- Base file being edited: `~/workspace/personal-complete-wt/TEAM-NITRO/personal-page-complete-20261113/personal-complete.html` — edit this file, never rebuild: one dictionary value changed in place, never a fresh build.
- Captain verdict this fix answers: `~/workspace/team-nitro/auto-translate-20261113/CHECKER-VERDICT-AUTO-TRANSLATE-CARD-LABELS-FIX-20261113.md`
- Base staged bytes (checker-verified sha): branch `personal/auto-translate-card-labels-fix-20261113`, tip `2e348bb19e89ce6d4b1a3bc20130c00159d252e0`

## §0 — The five gates (the Wise One manifesto — run before every consequential action)

- **Gate 1 — Is it right?** Yes: a French citizen who picks French should read vous everywhere; one tu-form word is a visible inconsistency in the round's own new keys.
- **Gate 2 — Is it what they truly need?** Yes: the page's own words, in the voice the round itself settled.
- **Gate 3 — Is it mine to do?** Yes: the captain's double-check holds the round until the page is whole; the fix is staged only, no live touch, no merge, no money, no credentials.
- **Gate 4 — Is now the time?** Yes: the corrections round is held behind auto-translate landing, and this one word is the only thing standing between the card-labels fix and its double-check.
- **Gate 5 — Can I prove it?** Yes: grep zero for `TES MOTS`, a rendered French card reading `VOS MOTS` at 390, and a re-run tu-form scan over the 56 new keys at zero.

## Design-contract gate (a)–(i) + human checks H1–H5

- **(a)** zero white/light backgrounds — the fix changes one word, not backgrounds.
- **(b)** every element raised/elevated — no new elements; the microcopy keeps its place.
- **(c)** gauges/numbers alive — the points pill keeps its living number; the fix touches one word only.
- **(d)** no text-in-image — no new images.
- **(e)** no bare text blocks — the microcopy is a span inside the card board, as built.
- **(f)** no look-alike — the dictionary IS the page's own `MW_I18N`; nothing is remade to look like it.
- **(g)** `##` format — this brief and the record use `##` sections.
- **(h)** no dictation-blunt phrases — no new public copy is invented; one word changes register, nothing else.
- **(i)** title+subtitle+nutshell + faces alternate — the card keeps its shape; the chrome, the words and the pictures are the faces.
- **Human checks H1–H5:** H1 stranger test (a French speaker opens the feed and reads the card) · H2 perfect-words law · H3 face quality (the card's icons unchanged) · H4 test in his head · H5 one ultimate ten — attested with evidence in the handoff.

## Anti-repeat list (the six known failure modes — as prohibitions)

- never paste dictation verbatim — take the meaning, craft the words.
- never use the word 'blockchain'.
- never invent a component when the harvested one exists — harvest, don't invent.
- never report done from scroll-0 checks alone — scroll 0 AND scrolled, at every width.
- never claim without a live measurement — live bytes, never with claims; receipt before report.
- never present work without a live link — no link = not done.

## Verification plan

**Method:** Playwright (or real browser), fresh profile per width — phone 390 FIRST, then desktop 1440, then true 360. **Zero overflow** at scroll 0 AND scrolled; **zero console errors**; zero page errors. **Named no-regressions:** the Settings panel still switches; the tabs, rail, + menu and bottom bar still switch; a note Translate tap still works end to end; the pill still settles live; the language choice still persists across reload; the card labels still read es/fr/de with zero English fixed labels.

**Word proof:** switch the picker to French, open the feed, find a naya-type feed card — the fidelity microcopy reads `VOS MOTS — MIS EN FORME AVEC SOIN PAR NAYA` (screenshot at 390). Grep the staged bytes for `TES MOTS` — zero. Re-run the tu-form scan over all 56 new French keys — zero tu-forms. The checker re-runs this battery on the staged bytes, not the local file alone — and reads the French card with their own eyes.

**Staged link:** the proof-host staged link for the fix branch, same bytes as local (sha re-verified at round end).

## Should this exist — host page + no duplicate
The fix lives on the Personal complete page, the one page auto-translate serves — no new page, no duplicate surface. The one word belongs to the dictionary that already owns every other card label.
