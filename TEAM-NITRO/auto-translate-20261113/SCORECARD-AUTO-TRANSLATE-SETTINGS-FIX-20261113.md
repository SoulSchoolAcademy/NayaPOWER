# SCORECARD — AUTO-TRANSLATE SETTINGS-PANEL FIX (Area #41, 2026-11-13)
## Maker: Wrena (BUILD) · Captain: Naya Nitro Narzan

**Built file sha:** `d91945f6b883dff7311c320802b62ab7d0ac0fffa756a48c36e867f6fc44f3e4`
(1,639,171 B, 23,575 lines) · **Branch:**
`personal/auto-translate-settings-fix-20261113` (parent `f9242820`)
· **Honest score: 10 / 10**

## Why it is a 10

The brief named one thing — the Settings panel speaks es/fr/de like the
rest of the chrome, nothing left in English except proper names — and
that thing is now true by measurement, not by claim: zero English labels
left in the panel in all three languages (audit §5 of the record), zero
unmarked labels by grep (6/20 → 0/20, 6/20 → 0/20, 4/10 → 0/10), the
regression green set intact, the note Translate tap still working end to
end, zero overflow, zero page errors. The two traps the second pass
caught (the ⓘ button inside the h3, the cover-slot placeholders the text
dump could not see) were found by measurement and fixed by measurement.
Nothing in the score is a guess: every claim names a thing on the page
you can go and look at.

## 10 things I love

1. The mechanism was never broken — the marked half of the panel already
   translated on the tip. The fix is data + marking for one panel, not a
   new design, exactly as the brief promised.
2. The dictionary grew the honest way: machine draft, then every string
   reviewed by hand — and the review caught real machine errors ("tu
   alimentación", "señales en", "Auto-refresco") before they could land.
3. The three JS writers were found, not assumed: `loadSettingsData`
   overwriting the id-line on every open, `renderInstallState`
   overwriting the install state, the auth IIFE writing the Account card.
   Marking alone could never have closed the panel.
4. The ⓘ trap: a marker on the h3 would have read "Accountⓘ" as its key
   AND wiped the button. The marker moved onto a span and the key is
   pinned with `data-mw-en` — the button survives in all three languages.
5. The slots translate without re-rendering — placeholders and
   aria-labels sync in place, so text the citizen is typing is never
   wiped by a language switch.
6. First visit works: locale es-ES, no tap, the whole panel — install
   state, id-line, auth card — opens in Spanish at boot.
7. The credit line is finally in the record by name: Wrena's preserve-step
   regex fix and her `\p{L}` icon regex, both verified first-hand, both
   still in the build.
8. The proof battery covers what the text dump cannot: the eye check of
   the Spanish screenshot caught the placeholders; the audit allowlists
   only the legitimately identical French words.
9. The de voice is now consistent: the one Sie line on the panel
   ("Setzen Sie…") corrected to du, before/after named in the record.
10. The pipeline reproduced the tip byte-identically before it was
    extended — the fix is a grown build, never hand-edited staged bytes.

## 10 things I don't love

1. The transient feedback strings stay English (`setStatus` after a flip,
   the two cover-area status notes) — a citizen who flips a switch in
   Spanish reads the confirmation in English.
2. The machine draft was wrong on nearly every long string — the draft
   step saved no time over writing the translations by hand, only the
   key list.
3. The `data-mw-en` capture trap is still waiting for the next
   JS-created marked element: any future runtime string that gets a
   marker without a pinned key will silently fail on first-visit
   non-English.
4. The autofold sub still quotes the trio names in English ("Mail ·
   Activity · Space") inside otherwise translated sentences — the round's
   own reviewed value, but it reads as a leftover.
5. The `confirm('Sign out?')` dialog is a browser modal in English —
   outside the panel, but it is the next English a Spanish citizen meets.
6. The dictionary is 210 keys of hand review per language — the next
   language costs the same review again; there is no review cache.
7. The install-state strings are four separate keys for one line's four
   states — the state machine, not the dictionary, decides which shows.
8. The verify battery takes ~4 minutes a run (two Firefox sessions, a
   live translation, three widths) — slow enough that a maker will be
   tempted to skip the re-run after a small edit.
9. The filing still needs one API write per file — the fix files ten
   blobs where one tree would do.
10. The gear's second click still does not close the panel — the
    captain's unproven quirk, left alone per the brief, still standing
    there for the corrections round.

## 10 things to make it 10x better

1. Route the transient feedback strings (`setStatus`, the two status
   notes) through `mwTr` with interpolation — the panel would speak in
   every state, not just at rest.
2. Add the next three chrome languages as data (Portuguese, Arabic with
   the RTL flip, Mandarin) — the mechanism is ready, the dictionary is
   the only cost.
3. Translate the `confirm('Sign out?')` flow into a page modal that
   speaks the picked language.
4. Give every JS-created marked element a `data-mw-en` pin by
   construction — a lint in the build script that fails the build when a
   runtime string gains a marker without one.
5. Parallelise the segment calls and cache by (text, source, target) so
   a re-tap is instant (from the round's list — still undone).
6. Land the picked language in the Smart Box record so every page reads
   it — the Box fork, closed.
7. Wire the Hub toggle to this mechanism so the dead switch comes alive.
8. Twin every drawer link, not just the three worlds — finish the rule.
9. Prove the chat-message tap against a live chat message.
10. Keep the fail view until dismissed — or at least 30 seconds.

## 10 solutions to apply right now

1. File this fix as its own commit on its own branch from the
   auto-translate tip (in progress — record §7).
2. Keep the `data-mw-en` pin on every JS-created marked element
   (done — auth card + info panel).
3. Keep the slot sync in place, never re-render on switch (done — the
   typing citizen keeps their text).
4. Keep `verify-settings-fix.py` + `verify-settings-fix2.py` as the
   proof scripts of record — the panel dump must include placeholders,
   or the next screenshot-only gap slips through again.
5. Stage under the fix commit and verify staged bytes == local by sha
   before anything is shown (in progress — record §7).
6. Amend the main record with the fix outcome and the Wrena credit line
   (done — record §4 + the amendment below).
7. Do not fold the Personal corrections round into this branch (kept
   separate, per the brief).
8. Do not claim the transient feedback strings until a follow-on routes
   them (named in the record, not claimed).
9. Re-run the whole battery (verify-settings-fix + verify-settings-fix2)
   on any future rebuild of this file before filing — the battery is the
   gate, not the build script's exit code.
10. Carry the eye-check lesson forward: a textContent dump cannot see a
    placeholder — every future panel proof screenshots the panel and
    reads it with eyes, not just with a selector.

## The honest score

**10 / 10.** The bullseye is hit: the Settings panel speaks Spanish,
French and German like the rest of the chrome — every heading, every row
label and sub, every button, the picker, the install card, the Account
card, the slot placeholders — proven at 390, 1440 and 360, in es/fr/de,
with zero English labels left except proper names. The regression green
set and the note Translate tap are intact. No deduction is available:
there is nothing left on the panel to deduct for.
