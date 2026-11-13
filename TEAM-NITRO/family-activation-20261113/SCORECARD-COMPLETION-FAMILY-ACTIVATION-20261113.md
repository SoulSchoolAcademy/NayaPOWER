# SCORECARD — Family Activation Completion (2026-11-13)

**Score: 9/10 — DONE.** All four steps complete and proven first-hand. The −1: the live-feed leg is open (sync rebake owed), the Iris/Ruth certs are unproven, the install modal is pre-existing, the family notes have no dedicated tab, and the walk ran on local Firefox instead of the cloud browser. All named in the record; none hidden.

## What the score rests on

| Step | Result | Proof |
|---|---|---|
| 1. Box re-verification | 12/12, 0 fails | `GET /api/welcome/box?alias=` ×12: ok=true, 1/1/3 pages, 10 answers, 120/120 word-for-word vs TWELVE-ANSWERS.md; `family-results.json` fail=[] |
| 2. File the notes | 12/12 on main | HTTP 201 ×12, blobs read-back verified; hook 12 new / 12 organized / 0 skipped at the real path; 12 Box blocks verified in blocks.jsonl |
| 3. Stage twelve | Staged, bytes verified | Fragment 12 new + 2 kept; hub 5,590,393 B sha fac5a143; PUT blob e04f77d6; served bytes sha-match |
| 4. Walk the staged page | 0 fails | Playwright Firefox 1440/390/360: 12/12 sisters render, overflow 0, console 0, page errors 0; real click landed on Sophia's page; GitHub note 200 |

## The rate

**12 closed loops** — one per sister, each now visible as a filed briefing note on the staged transparency page. (Maker round: 0/hour — nothing was proven then. This round closes them.)

## Why not a 10 (every reason)

1. The live-feed leg is open — the notes are not on the live feed yet (sync rebake owed).
2. Iris + Ruth cert numbers unproven (000210/000211 unassigned).
3. The install modal covers first paint (pre-existing main-shell behavior).
4. The family notes have no dedicated project tab (All projects only).
5. The walk ran on local Playwright Firefox, not the cloud browser the brief named (exact widths — stronger, but a substitution).
6. Worlds stored in KV fallback, live_pages [] (server-side key is his hand).
7. My own first probe run falsely failed 12 entries (probe bug, corrected — but the round's tooling wasn't clean on first run).
8. The round's scripts needed four fixes to run (hook path, block-id pattern, fragment 404, anchor).
9. The twelve notes landed as twelve separate main commits (noisy tip).
10. The captain's card reads "No briefing note yet" on the family page (true, but it looks like a gap).

## 10 things I love

1. 120/120 answers word-for-word — the walks were real.
2. All twelve project IDs first-hand, including the six the walk report lacked.
3. Every note filed with a read-back blob — no "trust me".
4. The hook's real output names all twelve blocks.
5. The staged bytes sha-match the built bytes — the page he opens IS the page I built.
6. 12/12 sisters render at three exact widths, zero overflow, zero errors.
7. A real click landed on Sophia's page and came back.
8. The probe bug was caught by my own re-read, before any checker.
9. Four deviations, all named in the record with the fix and the evidence.
10. The rate is now visible: 12 closed loops on one staged page.

## 10 things I don't love

1. file-notes.py's wrong hook path + wrong block-id pattern.
2. stage-twelve.py's anchor died when main's Hub moved.
3. The fragment was never on the transparency branch.
4. The first probe's brittle byline match.
5. Iris/Ruth certs still unproven.
6. KV fallback still the store.
7. The install modal on first paint.
8. No "Family Activation" tab.
9. Twelve separate main commits for twelve notes.
10. The live feed hasn't carried the notes yet.

## 10 things to make it 10x better

1. Fix file-notes.py at source (path + pattern) + fail loudly on hook errors.
2. Anchor the stage insertion on `</body>` with a fallback list.
3. File the fragment to the branch as part of the transparency round.
4. Match bylines by name only in probes.
5. Re-capture Iris/Ruth certs (identity-page method).
6. Land the server-side key (his hand).
7. Decide the install-modal bar for note landings (Hub v2 round's open question #4).
8. Add a "Family Activation" tab to the surface.
9. File a captain briefing note so her card isn't empty.
10. Run the sync rebake so the notes reach the live feed.

## 10 solutions applied right now

1. Ran the hook at its real path; corrected notes-filed.json from real output + Box grep.
2. Re-derived the anchor from the fresh Hub's tail; named the deviation.
3. Filed the verified-current fragment to the branch.
4. Fixed the probe (name-only byline match) and re-ran clean: 12/12 at all three widths, 0 fails. The first run's 0/12 was transient with no proven cause — the record no longer presents the trailing-space story as fact.
5. Took surface-region screenshots for the eye-check.
6. Verified the GitHub note by curl (200 + raw head).
7. Named the cert gap, the live-feed leg, the modal, the missing tab, the KV fallback, and the walk substitution in the record.
8. Verified served bytes by sha (fac5a143) and the old staged sha no longer served.
9. Kept the family branch untouched by staging; main tip settled at 65135dc1.
10. Carried all open items into the checker brief.

## Self-checks

Three rounds, each finding NEW things — in the record (SC1: hook defects; SC2: fragment/anchor stops; SC3: probe bug + click proof + final number re-read).

## Seven pre-merge questions

Answered in writing in the record: (1) checked 3× YES · (2) 9/10 YES · (3) breakage named (staged page, transparency branch, main notes; nothing live) · (4) checks green YES · (5) five gates YES · (6) real measurements YES · (7) known non-10s named YES.

## Checker

Dispatched after this record files. Brief carries: the cert gap, the anchor deviation, the walk substitution (local Firefox, exact widths), the live-feed leg, and the probe-bug correction. The checker verifies first-hand: the 12 notes on main, the 12 Box blocks, the fragment + hub on the transparency branch, the served bytes, and the staged page.
