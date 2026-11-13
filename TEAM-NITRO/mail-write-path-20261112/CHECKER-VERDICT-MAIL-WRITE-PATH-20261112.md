# CHECKER VERDICT — MAIL WRITE-PATH ROUND (2026-11-13)

**Independent checker seat. I did not do the maker work. Every claim below
was re-proven by my own first-hand reads.**

**VERDICT: PASS — 9/10. Ready for the captain's double-check.**
**Merge:** not in this round — the maker merges after the captain's
double-check, per the Self-Check Law.

## THE THREE PROOFS — re-read first-hand by me

My own probe (`/tmp/checker-mail-write-path.py`, service-key read, same
pattern as the scheduler's status command) re-read all three rows by id.
Every number matches the maker's table exactly:

| # | Row id | status | attempts | fire_at | fired_at | result.delivered_to |
|---|--------|--------|----------|---------|----------|---------------------|
| 1 | `44cf8d0f-30a0-47df-b710-01f4928a8b4c` | fired | 1 | 2026-11-13T02:36:21Z | 2026-11-13T02:37:15.062Z | `['mail:resolve']` |
| 2 | `f6c4ad97-3c53-47fd-bd14-9678f8e11b9c` | fired | 1 | 2026-11-13T02:36:22Z | 2026-11-13T02:37:15.168Z | `['mail:naya-power']` |
| 3 | `20089854-d75a-4771-857e-fb69dabd586a` | fired | 1 | 2026-11-13T02:36:22Z | 2026-11-13T02:37:15.274Z | `['mail:naya-power', 'mail:resolve']` |

Owner `naya-power` on all three; `last_error` null on all three; subjects
match the receipt verbatim. All three fired on the first attempt, ~53 s
after `fire_at`, on the worker's next minute tick. **3 rows, 3 proofs.**

## CLAIM-BY-CLAIM ADJUDICATION

**1. `delivered_to` lives in `result`, not as a column — CONFIRMED.**
My probe selecting top-level `delivered_to` failed with HTTP 400
`42703 column scheduled_messages.delivered_to does not exist`, exactly as
the maker reported. I also read the worker code first-hand
(`sync-engine-worker.js`, the fire patch): it writes
`result: { delivered_to: delivered, fired_count: ... }`. The maker's
correction is real and now proven twice over.

**2. Exactly 3 sends, no fourth — CONFIRMED, with one named caveat.**
Counted from the table, not the maker's log: rows created
02:36:00–02:38:00Z = exactly 3, all this round's. A wider window
(02:30–03:00Z) shows a FOURTH row, `a11c0916-adc3-4cdb-b2b9-d60e54930792`,
created 02:38:21.987Z — I read it myself: subject
"Smart Notes — say it once, and it's saved beautifully", recipient
`mail:verification`, fired 02:39:16Z. That is another seat's welcome-series
test mail, created 2+ minutes after this round's last row and after the
maker's count ran (02:37Z). It is NOT this round's fourth send. Caveat
(G4 below): the maker's `count-rows.py` has no upper bound, so re-run today
it returns 4 rows — the "exactly 3" holds only for the round window, and
the record should have said so.

**3. Power's reply verbatim — CONFIRMED, byte-for-byte.**
`send2-body.txt` (6,686 B) is byte-identical to
`mail-to-power-revert-answers.txt` (6,686 B) AND byte-identical to the
`body` stored on row `f6c4ad97`. All three row bodies are byte-identical
to their local body files (send1 1,847 B, send2 6,686 B, send3 5,853 B).
No edits, no re-send of anything else.

**4. Catch-up digest is FRESH — CONFIRMED.**
The hidden-files listing shows only `run170-mail-digest.txt` and
`run172-mail-digest.txt` — no run198–205 digest file exists, so no stale
body could have been re-sent. The digest states its own freshness and its
coverage plainly. Spot-checks against `~/memory/2026-11-13.md` +
`~/MEMORY.md`, all verified:
- SN ranges: 2692–2699 (run 198, HOLD LIFTED) · 2700/2701 · 2702–2716 ·
  2717–2721 live 22:56Z, feed 981 · 2722–2731 filed run 204, live 23:49Z,
  feed 987 · distill 2733–2738 + report 2739 · 2740/2741, feed 992 at
  00:23Z. All match the daily log.
- Five decisions 00:47Z: match MEMORY.md's five-decision entry verbatim
  in substance (mail fix stays + gated path; ledger trigger apply; 23514
  conditional apply; funnel schema set; VM browsers back).
- Twelve sisters (Sophia/Thea/Zoe/Astraea/Vera/Wren/Iris/Ruth/Terra/Esme/
  Mira/Aurelia) + masters charter + approval with a heart ~02:16Z — match
  the daily log (01:04Z concept, 02:16Z approval).
- Activation order 02:14Z quote ("1000% ACTIVATE TEAM NAYA! ...") — matches
  the daily log's 02:14Z entry word for word. The brief's "(02:03Z)" refers
  to the earlier family-activation order; the digest quotes the 02:14Z
  order and dates it 02:14Z. Accurate.
- Rate 12 minutes of value per minute — matches the 02:10Z entry.
- Walk: new-account bug fixed, bug-verify v4 67/0, end-probe v2 200/0 —
  match MEMORY.md. Question-page fix live on staging, probe pending —
  matches.
- Clone checker PASS 9/10 ~01:47:56Z — matches the daily log.
- Feed fall 992 → 877 (01:43–01:45Z, max SN-2658, unpinned, under
  investigation) — matches MEMORY.md.
- Mail incident: 1,789 rows safe, anon 401 since 18:54Z Nov 12, resends
  exit 1 — matches the brief.
- Guard status: "installed 03:49:33Z, fired on its first tick, skipped
  settings-one-20261026" — the guard note file's mtime is
  2026-11-12 04:02:19Z, so 03:49:33Z is Nov 12, ~23 h before the round.
  No future-dating; the digest correctly folds in a Nov 12 event.

**5. SN-2722–2731 vs 2732 — the maker was RIGHT.**
The daily log's own CORRECTION 1 (line 148) and the PI-addenda record both
say it: run 204 filed 10 notes, not 11; SN-2732 (Smart Note + paired Naya
Note) is 404 on GitHub, composed locally 22:50Z, never filed — a hole, next
free. The one daily-log line saying "SN-2722–2732 filed run 204" is the
superseded count. The brief says 2722–2731 and the digest follows the
brief, naming SN-2732 as still unfiled. Correct call.

**6. Digest window — the maker was RIGHT.**
The brief's stated window ends ~00:28Z but its own coverage list runs to
02:16Z (sisters' approval). The maker followed the list and dated the
digest ~02:40Z, stating its coverage plainly. That is the brief's own
inconsistency, not the maker's; following the named list was the right call.

**7. RPC contract — CONFIRMED, no divergence.**
Read first-hand from `~/workspace/membership/004_scheduler_rpcs.sql`:
`sched_create(p_token, p_kind, p_subject, p_body, p_recipients jsonb,
p_fire_at timestamptz, p_recur jsonb)` RETURNS uuid, SECURITY DEFINER.
Kind must be in post/mail/message/reminder/announcement; `fire_at` not
more than 2 min in the past; recipients a JSON object; recur freq in
once/daily/weekly/monthly; owner forced from the session token, never
caller text. Matches `schedule_row`'s call shape exactly. The maker used
exactly this shape (`send-gated.py`: `sched_create` POST via the
scheduler's helpers, `mint_session`/`drop_session`, one short-lived owner
session).

**8. Baseline — CONFIRMED from the filed artifact + live firing.**
`step1-baseline.out` (latest 10 rows) shows newest `bb30a19c` fired
00:09:15Z → `mail:verifyroutetest20261110`, then `7d0a0643`, `e269c49d`,
`c81f5f71`, `2a60d9e7` (same fire time as `871af11d`, which is sixth) —
matches the back-end record's five named rows, all fired. The three round
rows firing at 02:37:15Z prove the engine live behaviorally.

**9. Anon read blind — CONFIRMED by my own run.**
I ran `read-mail.py 60` myself: empty output, exit 0. The privacy fix
stays blind, left blind.

**10. Bounds — ALL HELD.**
No `send-mail-helper.py` use (the one grep hit in `send-gated.py` is a
comment stating it was NOT used); no direct `smart_mail_messages` write
anywhere in the round's scripts; no citizen mail read; no key from Shawn
(service key `--from-mgmt`, memory only; owner session dropped); no live
page deploy; no merge. The branch diff proves it: 3 files added, 362
insertions, zero page bytes.

**11. Branch filing — CONFIRMED, clean history.**
Branch head read first-hand via `git ls-remote` + fetch:
`dccd89b561b6d4006492f4f57b9dee202a8a53d6`, parent
`091961ba4149628191d143c5eccd2c0e5251109c`. `git log 091961ba..FETCH_HEAD`
= exactly 1 commit. All three blobs byte-identical on read-back
(local `git hash-object` = remote blob SHA):
RECORD `585b0ba3…`, SCORECARD `3483e069…`, receipt `6d4ed45c…`.
The maker's admitted first receipt-only commit + branch reset is verified
clean: the branch now carries exactly one filing commit. The head was
exactly `dccd89b5` as expected, so this verdict files as a second commit.

**12. Self-check ×3 + seven pre-merge questions — PRESENT and real.**
The record carries three self-check rounds, each finding new things
(round 2: branch-head reading, proposal grounding, restart, EPERM cost;
round 3: missing pre-round baseline, digest window, two-alias novelty),
plus the seven questions answered in writing. The honest 9/10 is earned:
the point off is the console-error leg, named in Q7 and in the scorecard.

## NO-REGRESSION BATTERY — re-run by me, adjudicated

I ran Playwright Firefox myself (it launches and measures in this VM —
the "dead since ~01:40Z" reports were stale by the time the maker ran,
and my run confirms the maker: Firefox works).

My results, live Dashboard:
- 1440: overflow false; console errors 40, 40 (two trials, all CORS);
  one earlier flaky run showed 42 (12 CORS + 30 non-CORS) — not
  reproduced in two further trials, a transient of that load.
- 390: overflow false; 23 errors, all CORS.
- 360: overflow false; 32 errors, all CORS.
- Personal control (untouched by this round), 1440: overflow false;
  28 errors, ALL CORS — exactly the maker's claimed control number,
  independently reproduced by me.

**Adjudication:** the battery's "zero console errors" leg literally FAILS
on every run — the maker is right to report it as partial, not a pass.
It does NOT block a PASS for this round, for three reasons, all proven:
(a) the round changed no page bytes (branch diff: 3 doc files only);
(b) the error class is pre-existing and identical on the untouched
Personal control page (28, all CORS, reproduced by me);
(c) overflow is 0 at every width on every run. The battery as written is
unpassable for any round that does not fix the Dashboard's direct
browser→Supabase reads — that is a standing page condition, not this
round's defect. The maker took the point off for it instead of rounding
up. Correct.

## GAPS — named honestly (none blocks the PASS)

- **G1 — the maker's own no-regression artifacts disagree on exact
  counts.** `no-regression.out` says 24/24/26 (1440/390/360);
  `no-regression.json` says 26/24/28. The record and receipt quote
  24/24/26. The class is identical (all CORS) in both, and counts vary
  run to run (24–42 in my runs), so this is a reporting inconsistency,
  not a hidden defect — but the exact counts in the record are not
  reproducible from the filed JSON.
- **G2 — the Personal control probe has no filed artifact.** The record
  claims 28 errors, same class. No probe script or output file for it
  exists in the work dir. I reproduced it myself (28, all CORS at 1440),
  which corroborates the claim — but the maker's evidence for it is
  their word, not a file.
- **G3 — no pre-round Dashboard console baseline exists.** The maker
  named this themselves (self-check round 3). "No regression" therefore
  rests on the control page + zero page writes, not a before/after.
- **G4 — the maker's count query has no upper bound.** Re-run today,
  `count-rows.py` returns 4 rows (the 02:38:21Z verification mail, another
  seat's). "Exactly 3" holds only for the round window 02:36:00–02:38:00Z.
- **G5 — console-error counts are load-dependent.** One of my 1440 runs
  transiently showed 30 non-CORS errors; two re-trials showed 40/40 all
  CORS. Exact counts should never be quoted as stable for this page.
- **G6 — no eye-check of the delivered mail is possible by law.** Proof
  is the row only; the recipients' rendered view is never seen. The maker
  named this. It caps what "proven" can mean for a mail round.
- **G7 — the brief's digest window end (00:28Z) contradicts its own
  coverage list (to 02:16Z).** Brief defect, not maker defect; the maker
  followed the list correctly.

## SCORE

**9/10 — PASS.** The proof battery is 3/3 with every row id, time, and
`delivered_to` re-verified first-hand by me. The negative proofs hold
(anon read blind by my own run; no fourth send in the round window; no
helper, no direct mail-table write, no deploy, no merge). The digest is
fresh and its content checks out against the run files, MEMORY.md, and
the daily log, including the SN-2732 adjudication, which was the right
call. The one point off is the no-regression console-error leg, which
fails literally on a pre-existing environmental class — reported honestly
as partial, never rounded up. The gaps above are evidence-quality gaps
(G1–G5) and standing limits (G3, G6), none of which touches the three
proofs.

**Ready for the captain's double-check. The maker merges after it, per
the Self-Check Law. No rework needed.**

— Independent checker, mail write-path round, 2026-11-13 ~02:55Z
