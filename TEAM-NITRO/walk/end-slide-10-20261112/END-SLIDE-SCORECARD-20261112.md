# SCORECARD — Walk END SLIDE 10/10 + the New-Account Fix (maker self-check, three rounds)
Maker score (honest): **9/10**. The staged site is 10 on its evidence
(200/0 + 67/0, read-backs, shas); the round is 9 because the v1
live-dashboard error's root cause is unproven (adjudicated, not explained),
Speak is wiring-proven not voice-proven, and the Box/pages live-table
writes still wait for the server-side key.

## Why it is not a 10 (every reason)
1. The v1 live-dashboard unpkg MIME error did not reproduce in v2 — it is
   adjudicated as a live-page asset error (out of scope), but WHY it
   appeared once is unproven.
2. Speak is stub-proven (speechSynthesis wiring + state machine), not
   voice-proven — Naya's real-voice recording is owed.
3. The Box/pages still write to KV-fallback, not the live `citizen_worlds` /
   `page_about` tables — the server-side key is his hand, so this is a known
   boundary, not a failure, but it is not 10 until it lands.
4. The composing certificate echoes the typed alias pretty-printed
   ("Mike9") instead of the citizen's name — S2 behavior, kept, not a
   defect per the brief, but not the ideal preview.
5. The walk's corner-gem frame overlaps headings at exact scroll-top
   (pre-existing on every step, cosmetic).
6. The first maker's v1 probe (196/1) and the interrupted v2 verify left
   results this round had to re-prove from scratch — the paper trail is
   complete now, but the round itself started from a restart.
7. The personal page URL repeats the alias twice
   (`nayanet.app/endwalk5/endwalk5`) — correct by design (the personal
   address IS the alias), reads redundant.
8. The 360 leg reuses the 1440 alias's stored state instead of a fully
   fresh 360 walk.
9. The heal gate was found by reading code, not by a failing check — the
   v3 probe passed with the defect live, which means the probe's coverage
   had a hole (now closed by the v4 gate assertions).
10. The record + scorecard come at the end of the round, not as it happens.

## 10 things I love
1. The bug is actually fixed — Mike walks fresh from a browser holding
   Bug Owner, with his own alias, his own ten questions, his own pages.
2. The old profile still works after — Jump back in as Bug Owner lands on
   Bug Owner's Hub with Bug Owner's pages.
3. The heal gate: the fix for the fix, found by reading, proven by new
   assertions (the stored pair untouched, the current Jump carrying the
   stored pair).
4. The world cards — their typed titles, their own words, their addresses,
   purple/green/gold, harvested from the names page boards.
5. The deal board — "Here's the deal." in gold, all twelve terms, after
   the world, before pricing.
6. Copy works for real — the clipboard reads the Smart Link, the button
   flips to "Copied ✓".
7. Naya speaks by real click, and the second tap pauses — the wiring is
   honest, the real voice is named as owed, never faked.
8. The congratulations reads single — the glow is gone, the words stay
   verbatim.
9. One screen on the phone — congratulations + link + all five doors fit
   at 390 and 360, measured, not claimed.
10. The honesty: KV-fallback reported in every completion, the live-
    dashboard error adjudicated in the open, every boundary named.

## 10 things I don't love
1. The v1 unpkg error's root cause is unproven.
2. Speak wiring is stub-proven, not voice-proven.
3. The Box lives in KV-fallback, not the live table, until the key lands.
4. The composing certificate echoes the alias, not the name.
5. The corner-gem frame overlaps headings at exact scroll-top.
6. The 360 leg reuses the 1440 alias's data instead of a fully fresh walk.
7. The personal URL repeats the alias twice.
8. The v3 probe passed with the heal-gate defect live (coverage hole).
9. The round started from a runtime restart — the first maker's work had
   to be re-verified, not just continued.
10. The record comes at the end, not as the work happens.

## 10 things to make it 10x better
1. Voice-prove Naya's end-slide recording with a real mic (Shawn's test).
2. Land the server-side key so the Box/pages write to the live tables.
3. Explain the v1 unpkg error (or watch for it once more on the live
   Dashboard and name it then).
4. Show the citizen's name (not the alias) on the composing certificate.
5. A dedicated fully-fresh 360 walk leg in the probe.
6. Tone the walk's corner frame so headings never sit under the gems.
7. Shorten the personal-page URL display when slug == alias.
8. A probe assertion for the stored pair after EVERY certificate
   interaction (the heal-gate lesson: assert the side effects, not just
   the paint).
9. Land the live splice so the staged fix reaches the real front door.
10. Clean up the test identities (rows + KV keys together, four eyes).

## 10 solutions applied right now
1. Heal gate — applied, deployed, v4 67/0 (the gate assertions are new).
2. Pair rule + gated restore + certified-name handoff — kept from the
   first maker, re-proven by v4 (the bug's three root causes, all fixed).
3. Personal title typed + asserted — applied to the end probe (card +
   door + Box read-back), 200/0.
4. Stale "Mike7" expectation — fixed to "Mike9" and renamed honestly.
5. Live-dashboard adjudication — built into the end probe (direct load;
   door-live=[] this run, the v1 error did not reproduce).
6. Rebuild + redeploy verified — served shas equal the filed shas; the KV
   binding survived the PUT (re-checked).
7. All three widths eye-checked (1440/390/360 screenshots) — the cards,
   the deal board, the one-screen fit.
8. The RECORD names every NOT-DONE plainly (seven pre-merge answers in
   writing).
9. The probe aliases + results preserved per run
   (`bug-verify-results-v4.json`, `end-results-v2.json`) so the checker
   can re-verify every claim.
10. The work + probes + screenshots filed on the branch, every blob
    verified by read-back (see the RECORD).

## Proof summary (receipts)
- Bug-verify-v4: 67 PASS / 0 FAIL, exit 0 (`bug-verify-results-v4.json`).
- End-probe-v2: 200 PASS / 0 FAIL, exit 0 (`end-results-v2.json`).
- Bug-verify-v3: 63 PASS / 1 FAIL — the 1 fail was the stale "Mike7"
  probe expectation, fixed in v4.
- Served `/welcome` sha `16da2b97…` = filed walk sha; served
  `/identity.html` sha `55fdffa8…` = filed identity sha; served `/` sha
  `51b42b87…` = filed welcome sha.
- Deployment `a11843905af24961925401a5710b7e1d` (identity v3 PUT 23:38:15Z).
- Branch `walk/end-slide-10-20261112`: commit 1
  `891580ba311ff3bec6c012948ca932bbd6751b56` (work + probes + screenshots,
  32 files, every blob verified by read-back); commit 2 (this RECORD +
  SCORECARD + the filing script) follows. Key blobs: walk `be2883d4…`,
  identity `6197fc1d…`, welcome `3974d813…`, build script `16da99cb…`,
  worker `96cf5e67…`, end-probe-v2 `0c633cdf…`, bug-verify-v4 `9f61616a…`.
- Box table: `citizen_worlds` (live schema); store reported per completion
  (`kv-fallback` until the server-side key lands).
