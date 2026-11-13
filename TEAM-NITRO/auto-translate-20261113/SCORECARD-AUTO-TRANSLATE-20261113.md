# SCORECARD — AUTO-TRANSLATE (Area #41, 2026-11-13)
## Fresh maker (second maker) · Captain: Naya Nitro Narzan

**Built file sha:** `28ca21fa376ddaeb7a8a51f935407e7465bff68fd79d3d99b03958b83c8e4403`
(1,621,175 B, 23,547 lines) · **Branch:** `personal/auto-translate-20261113`
· **Honest score: 9 / 10**

## Why it is not a 10

Two things are named-but-undone, and one of them is visible on the page:
the drawer navigation links beyond the three worlds are still text-only
(Your Reports, Intel Today, Smart Factory, memberships, About Us, White
Paper — reachable chrome with no icon twin), and the chat-message
Translate tap is built but has never been exercised against a live chat
message. A 10 needs both closed. The pill reading "0" on `file://` is NOT
a deduction — it is the known live-fetch stop, proven not a regression.

## 10 things I love

1. The dictionary is the page's own machine, grown — 17 keys to 167, same
   `MW_I18N` + `mwApplyLang`, no framework, no vendor, no key.
2. First visit speaks your language with no tap — `navigator.language`,
   one line of arithmetic, es-ES → es, ja-JP → en.
3. The Translate tap asks what language the note is in — never silently
   assumes English. That is the honest shape of the whole round.
4. A 3-sentence note comes back whole — all three sentences, in order,
   title + subtitle + nutshell carried. The segmentation order in the
   brief was right and the proof shows it.
5. The original is always one tap away, and the card's own words are never
   touched — the translation is a view below, labelled, collapsible.
6. Failure is honest: "Translation unavailable — the original is here",
   no invented words, original intact.
7. The repaint fix — state by card key, not by node. A tap that used to
   die silently now survives the wall rebuilding under it. That is the
   kind of fix that never shows and always matters.
8. The drawer gems: three lit jewels — blue, green, gold — and a stranger
   who reads nothing can tell the worlds apart by colour + position.
9. The no-words screenshots: with every word hidden, the page is still
   obviously a world — cover, gems, tabs, plus, rail. The visual language
   was already mostly there; the round finished it.
10. The proof is real: every claim has a sha, a line, a count, a JSON, a
    screenshot — and the two defects this round found were found by
    measurement, not by opinion.

## 10 things I don't love

1. The drawer navigation links are still text-only — the one visible
   place the "no text-only control" rule does not reach.
2. The chat-message Translate tap is built but unproven live.
3. The fail view vanishes after 6 seconds — a citizen who looks away
   misses the reason. Honest, but brief.
4. The first maker's verification scripts shipped with wrong class names
   and could never have passed — the round nearly reported them as done.
5. The interim commit's message claimed verifications that had not been
   run. A claim in a commit message is still a claim.
6. The pill reads "0" on `file://` — correct behaviour, but it will keep
   being misread as a regression until the staged proof is the default
   view.
7. The wall repaint still destroys and rebuilds every card node — the
   translate module now survives it, but the repaint itself is a sledgehammer.
8. The dictionary holds three languages, not any language — "for all
   people, in all countries" is still three countries' worth of chrome.
9. The Naya feed stays skeleton on `file://`, so its Translate path was
   proven on a synthetic card, not a live Naya note.
10. The translation takes ~12 seconds for three segments (sequential
    Workers AI calls) — fine for one tap, slow enough to notice.

## 10 things to make it 10x better

1. Twin every drawer link, not just the three worlds — finish the rule.
2. Prove the chat-message tap against a live chat message.
3. Keep the fail view until dismissed — or at least 30 seconds.
4. Parallelise the segment calls (one request, segments in one body) and
   cache by (text, source, target) so a re-tap is instant.
5. Add the next three chrome languages as data (Portuguese, Arabic with
   the RTL flip, Mandarin) — the mechanism is ready.
6. Land the picked language in the Smart Box record so every page reads
   it — the Box fork, closed.
7. Wire the Hub toggle to this mechanism so the dead switch comes alive.
8. Make the wall painter preserve card nodes across repaints instead of
   `innerHTML` — the translate fix becomes unnecessary.
9. Show the translation's confidence or a "report a bad translation"
   tap — citizens correct the machine, the dictionary learns.
10. Auto-detect the source language on tap (Workers AI language ID) with
    the picker as the override — the tap becomes one tap, not two.

## 10 solutions to apply right now

1. File this round with the drawer-world twins in (done — §12b).
2. Keep the repaint-resilience state-by-key in the module (done — it is
   the difference between a tap that works and a tap that dies).
3. Keep `verify2.py` as the Part 2 script of record — the stale-selector
   scripts are superseded and must not be re-run as proof.
4. Note the 6-second fail window in the record so the next verifier polls
   fast (done — §4).
5. Stage under the amended commit and verify staged bytes == local by sha
   before anything is shown (in progress — §7).
6. Replace the interim commit's message with the truthful one (the filing
   does this).
7. Name the Box write, RTL, Hub toggle and drawer-links follow-ons in the
   record with owners (done — §10).
8. Do not fold the Personal corrections round into this branch (kept
   separate, per the brief).
9. Do not claim the chat path or the Naya live path until a live message /
   live note proves them (named in the record, not claimed).
10. Re-run the whole battery (verify-a ×3, verify2, repaint ×2, nowords
    ×2) on any future rebuild of this file before filing — the battery is
    the gate, not the build script's exit code.

## The honest score

**9 / 10.** The bullseye is hit: a citizen who reads no English opens
their Personal page, the page speaks their language, and they can work it
from the objects alone — proven at 390, 1440 and 360, in es/fr/de, with
real translations read back whole and a no-words flow that completes.
The point off is the two named gaps (drawer navigation links, chat tap
unproven live). Nothing in the score is a guess: every deduction names a
thing on the page you can go and look at.
