# RECORD — MAIL WRITE-PATH ROUND (2026-11-13, ~02:31–02:50Z)

Maker seat, alone, no subagents. Brief: `BRIEF-MAIL-WRITE-PATH-20261112.md` (checked 9/9).
Branch: `mail/write-path-20261112`. Work dir: `team-nitro/mail-write-path-20261112/`.

## DONE — what done looks like, met

Three sends, each through the gated path and no other way, each proven by its
`scheduled_messages` row read first-hand: status `fired` AND
`result.delivered_to` containing `mail:<recipient-alias>`. Zero sends outside
the gated path. Zero reads of any citizen mail. Count = 3 sends, 3 rows,
3 proofs.

## THE THREE PROOFS (read first-hand, service-key read, poll pattern from `fire-test-sync-engine.py`)

| # | Send | Row id | fire_at | fired_at | delivered_to | attempts |
|---|------|--------|---------|----------|--------------|----------|
| 1 | Convergence piece → resolve | `44cf8d0f-30a0-47df-b710-01f4928a8b4c` | 2026-11-13T02:36:21Z | 2026-11-13T02:37:15.062Z | `['mail:resolve']` | 1 |
| 2 | Power's reply → naya-power (verbatim) | `f6c4ad97-3c53-47fd-bd14-9678f8e11b9c` | 2026-11-13T02:36:22Z | 2026-11-13T02:37:15.168Z | `['mail:naya-power']` | 1 |
| 3 | Fresh catch-up digest → naya-power + resolve | `20089854-d75a-4771-857e-fb69dabd586a` | 2026-11-13T02:36:22Z | 2026-11-13T02:37:15.274Z | `['mail:naya-power', 'mail:resolve']` | 1 |

All three fired on the first attempt, ~53 s after fire_at, on the worker's
next minute tick. Subjects (read back from the rows): "Converging on PI —
one record, one shared statement" · "Your four questions, answered — two
reverters, not one" · "Catch-up digest — runs 198-205: the sisters, the five
decisions, the walk, the mail path". Owner on all three rows: `naya-power`.
Proof log: `proof-log.json` (read-back of the three rows, in the work dir).

## STEP 1 — GROUND (first-hand, nothing carried on trust)

- **RPC contract read first-hand** from `~/workspace/membership/004_scheduler_rpcs.sql`:
  `sched_create(p_token, p_kind, p_subject, p_body, p_recipients jsonb,
  p_fire_at timestamptz, p_recur jsonb)` RETURNS uuid, SECURITY DEFINER.
  Validates: owner session token (owner_alias forced from the session, never
  caller text); kind in post/mail/message/reminder/announcement; fire_at not
  more than 2 min in the past; recipients a JSON object; recur freq in
  once/daily/weekly/monthly. **Matches `schedule_row`'s call shape exactly.
  No divergence — no STOP.**
- **CORRECTION (my first probe failed on it, named so the next seat doesn't
  repeat it):** `delivered_to` is NOT a top-level column — selecting it
  returns HTTP 400 `42703 column scheduled_messages.delivered_to does not
  exist`. It lives inside the `result` jsonb (`result.delivered_to`), as the
  worker writes it (`sync-engine-worker.js` line 210) and as
  `fire-test-sync-engine.py` reads it. The brief's shorthand "delivered_to"
  means `result.delivered_to`. All proofs above use that field.
- **Live baseline re-read first-hand** (`step1-baseline.py`, output
  `step1-baseline.out`): latest 10 rows; newest `bb30a19c-…` fired
  00:09:15Z → `mail:verifyroutetest20261110` — matches the back-end record
  exactly (next three `7d0a0643`, `e269c49d`, `c81f5f71` also match; the
  record's fifth, `871af11d`, is sixth here — `2a60d9e7` shares its fire
  time; all five named rows present, all fired). Engine last fired
  00:09:15Z, ~2.5 h before scheduling: nothing had been due since 00:08Z,
  and the engine fires ~1 min after fire_at whenever a row is due. The
  three rows firing at 02:37:15Z prove liveness behaviorally — no STOP.
- **Worker claim semantics read first-hand** from `sync-engine-worker.js`:
  kind `mail` iterates `recipients.thread_aliases`, delivers
  `mail:<alias>` per alias, per-channel idempotency (already-delivered
  channels skipped), `recur once` → terminal `fired`. A two-alias mail row
  delivers both — send 3's single row is correct.
- **Anon read re-verified blind:** `read-mail.py 60` → 0 rows, empty output,
  exit 0. The privacy fix stays blind, left blind.
- **Branch head verified first-hand:** `git ls-remote origin
  mail/write-path-20261112` → `091961ba4149628191d143c5eccd2c0e5251109c`
  ("hub: SN-01773 baked card title carries the hook headline (was a body
  sentence) — naya-power, gap-d43"); `git fetch` + `rev-parse FETCH_HEAD`
  confirms the same SHA. The brief's "from main head 091961ba" is the
  pre-created branch head, not main's head — my first reading was wrong,
  resolved by the fetch. No divergence.

## STEP 2 — COMPOSE (sources, no invention)

- **Send 1** (`send1-body.txt`, 1,847 B): from (a) the convergence draft
  (`SN-XXXX-converge-with-nitro-and-power-DRAFT.md` — dual purpose, bridge,
  three seats' marks) + (b) the APPROVED one-record design (Shawn 19:38:41Z
  Nov 11: Box is the one record, PI is the face, Factory is the hands, Hub
  is the eyes — corroborated verbatim in `BRIEF-SMART-HUB-REBUILD-20261112.md`
  §6 and `SMART-HUB-BRIDGE-DESIGN-20261111.md`) + (c) the captain's
  one-record proposal as his piece. No source disputes the approved
  wording — no STOP, nothing improvised. Carries the APPROVED design, not
  the recommendation.
- **Send 2** (`send2-body.txt`, 6,686 B): `mail-to-power-revert-answers.txt`
  copied byte-for-byte (`cmp` VERBATIM-IDENTICAL at stage time, re-verified
  after scheduling: still identical). No edits. The guard-fired note was NOT
  sent separately — its substance folds into send 3 as a status item.
- **Send 3** (`send3-body.txt`, 5,853 B): composed fresh in the round from
  the run files + `~/MEMORY.md` + `~/memory/2026-11-13.md`, in the shape of
  `run172-mail-digest.txt`. Coverage: runs 198–205; SN-2692–2741 filings;
  the captain's five decisions 00:47Z; twelve sisters + masters charter +
  activation order 02:14Z + 12-minutes-per-minute rate; walk fixes
  (new-account bug fixed, bug-verify-v4 67/0, end-probe-v2 200/0,
  question-page fix on staging); clone checker PASS 9/10; live-feed fall
  992→877; mail incident + this path; guard-fired status. **No stale digest
  body re-sent** — no run198–205 digest file exists (only run170 + run172);
  the stale bodies in `run198-mail.py` and the run199–202 resends were never
  read for content. **Adjudication, named:** one daily-log line says
  "SN-2722–2732 filed run 204", but the brief's coverage list says
  2722–2731 and the numbering-law entry holds SN-2732 unfiled (a hole,
  never taken). The digest follows the brief: 2722–2731, SN-2732 named as
  still unfiled.
- **Human checks H1–H5** (attested with evidence): H1 the words are true —
  every number above traces to a named first-hand source in this record.
  H2 the recipients are right — resolve / naya-power / naya-power+resolve,
  per the brief. H3 nothing private is in it — no citizen mail content, no
  secrets, no token; bodies contain only the named sources. H4 the proof
  row is named — the three row ids in the table above. H5 the bounds hold —
  three sends, gated path only, no fourth send.

## STEP 3 — SCHEDULE (gated path only)

Driver `send-gated.py` reuses the scheduler's own helpers
(`get_service_key` --from-mgmt, memory only; `mint_session` /
`drop_session`; `sb` POST to `/rest/v1/rpc/sched_create`) with the exact
RPC shape: `p_token, p_kind 'mail', p_subject, p_body, p_recipients
{"thread_aliases": [...]}`, `p_fire_at`, `p_recur {"freq":"once"}`. One
short-lived owner session for the run, dropped at the end. One row per
send, in order. Output `send-gated.out` + `schedule-log.json` (read back:
3 rows, subjects, aliases, byte counts match the body files).
No `send-mail-helper.py`. No direct `smart_mail_messages` write of any
kind. No new send mechanism, no page build, no new table. No key from
Shawn, no tap from him. Nothing secret printed, logged, or stored.

## STEP 4 — WAIT

Worker's next minute tick claimed all three rows; all fired 02:37:15Z
(~53 s after fire_at). No row waited past 10 minutes; no named failure.

## STEP 5 — PROVE

`prove-sends.py` polled each row by id until `fired`, then checked
`result.delivered_to` — the table above is the read-back. All three
proven, attempts = 1 each, no retries, no doubles.

## VERIFICATION PLAN — full run

- **Proof battery: 3/3 PASS.** 3 rows, 3 proofs, every row id + fire time
  + delivered_to in the table above.
- **No-regression battery: PARTIAL — overflow PASS, console-error leg NOT
  clean (named, not hidden).** Playwright Firefox ran (the VM browsers
  were reported dead since ~01:40Z; Firefox launched and measured fine
  this round). Live Dashboard `https://nayanet.app/dashboard` HTTP 200,
  1,817,928 B; overflow_x = false at 1440, 390, and 360. Console errors:
  24 / 24 / 26 — ALL one class: Firefox CORS blocks on the Dashboard's own
  direct Supabase REST reads (`smart_mail_threads`, `smart_notes`,
  `smart_links`, `smart_link_daily_stats`, `invites`,
  `smart_link_dimension_stats`; "CORS request did not succeed", status
  null). **Control:** live Personal, which this round never touched,
  shows the SAME class — 28 console errors, same tables, overflow false.
  The class is a standing environmental condition of the live pages'
  direct browser→Supabase reads in this VM's browser, present identically
  on an untouched control page. This round changed no page bytes (no
  deploy, no page write), so no regression is attributable to it — but the
  battery as written ("zero console errors") does not pass literally, and
  the round does not claim it does. Full output: `no-regression.json`.
- **Negative proofs: PASS.**
  - Anon read blind: `read-mail.py 60` → 0 rows (re-verified, left blind).
  - No direct `smart_mail_messages` write: none exists — the only writes
    this round are the 3 `sched_create` RPC calls (named in Step 3) plus
    the round's own work-dir files. No `send-mail-helper.py` call.
  - No fourth send: `count-rows.py` counted from the table — exactly 3
    rows created in the round window (02:36:00Z→), all three this round's,
    all `fired` (output `count-rows.out`).

## BOUNDS — all held

Privacy fix STAYS · gated path only · exactly three sends, in order · no
direct mail-table write · no citizen mail read · no key/tap from Shawn ·
no live page deploy · no merge (branch filing only; merge waits for the
captain's double-check) · no new mechanism/table/page · five gates run
before the first schedule and again before each send (all five yes each
time; the gates are in the scorecard). EPERM flake: every file write
verified by read-back; no 0-byte file called a result (all work-dir files
listed with sizes below; the one service restart mid-probe lost nothing —
outputs were on disk).

## WORK-DIR FILES (all verified by read-back, non-zero)

`send1-body.txt` 1,847 B · `send2-body.txt` 6,686 B (verbatim) ·
`send3-body.txt` 5,853 B · `send-gated.py` + `send-gated.out` +
`schedule-log.json` · `prove-sends.py` + `prove-sends.out` +
`proof-log.json` · `step1-baseline.py` + `step1-baseline.out` ·
`count-rows.py` + `count-rows.out` · `no-regression.py` +
`no-regression.out` + `no-regression.json` · record, scorecard, receipt
(this file, its companions).

## SELF-CHECK ×3 (in writing, before reporting)

**Round 1 — why it is not a 10:** (1) the no-regression console-error leg
does not pass literally (24/24/26), even though the class is pre-existing
and characterized with a control page; (2) the Step 1 engine-idle gap
(2.5 h since the last fired row) needed behavioral proof rather than a
fresh row at Step 1; (3) the digest's SN range needed mid-round
adjudication (2722–2731 vs 2732); (4) no eye-check of the delivered mail
in Smart Mail is possible by law (proof is the row only) — the recipients'
rendered view is never seen; (5) the brief's "delivered_to" shorthand
invites the column mistake my first probe made.
**Round 2 — new findings:** (6) the branch-head wording ("from main head
091961ba") misleads — it is the pre-created branch head, and my first
reading was wrong until the fetch proved it; (7) "the captain's
one-record proposal" has no single canonical file — it is grounded across
three briefs plus the bridge design doc, not one proposal document;
(8) the service restarted mid-probe once (nothing lost, outputs on disk);
(9) EPERM discipline cost time on every write (all verified by read-back).
**Round 3 — new findings:** (10) the no-regression battery has no
pre-round Dashboard console baseline, so "no regression" rests on the
Personal control + zero page writes, not a before/after; (11) the digest
covers items past the brief's stated window end (00:28Z) — activation
order 02:14Z, sisters' approval 02:16Z — because the task's coverage list
names them; the digest dates itself ~02:40Z and states its coverage
plainly; (12) the two-alias row shape (send 3) is proven by the worker
code + the fired row, but no prior two-alias mail row existed in the
baseline to compare against — the proof stands on its own row.
**10 things loved:** the gated path used exactly as harvested, no new
mechanism · RPC contract read first-hand from the migration · baseline
re-read first-hand and matched · anon read re-verified blind · send 2
byte-identical verbatim, verified twice · all three rows fired first
attempt, ~53 s, delivered_to exact · row count from the table = 3, no
fourth send · Playwright battery actually ran — overflow 0 at all widths
· the CORS class characterized with a control page, not hidden · no
secrets printed, logged, or stored; the owner session dropped.
**10 to make it 10x (solutions applied now where the round owns them):**
the column correction is written in this record (not just fixed in the
probe) · the branch-head correction is written here · the SN-range
adjudication is written here · the console-error leg is reported as
partial, not rounded up · the digest states its coverage window plainly ·
the receipt carries the full read-back · the schedule/proof logs are kept
in the work dir · the control-page probe is filed as evidence ·
nothing is claimed from a send call — only from row reads · the score
below is honest, not rounded.

## SEVEN PRE-MERGE QUESTIONS (in writing; merge waits for the captain's double-check)

1. **Checked my own work three times?** Yes — the three rounds above;
   each round found new things (round 2: branch-head reading, proposal
   grounding, restart, EPERM cost; round 3: missing pre-round baseline,
   digest window, two-alias novelty).
2. **Is it 9 or better by my own honest score?** Yes — 9/10 (scorecard).
   The point off is the console-error leg, named in Q7.
3. **What could this break?** The only live writes are the 3
   `scheduled_messages` rows (now terminal `fired`); one short-lived owner
   session (dropped). No page bytes, no schema, no grant, no mail reads.
   A double-delivery is impossible by construction (atomic claim,
   per-channel idempotency) and disproven by the row reads (attempts = 1,
   delivered_to exact, row count = 3). Nothing else is touched.
4. **Are the automatic checks green?** The round's own checks: proof
   battery 3/3 green; negative proofs green; overflow green. The
   console-error leg is NOT green (24/24/26, pre-existing class, control
   page identical) — it is reported as a partial, not merged over
   silently. No page-build checker applies to this round (no page file).
5. **Does it follow the ultimate objectives?** Yes — the five gates,
   answered honestly before the first schedule and before each send: right
   (gated path, privacy preserved) · truly needed (mail held since runs
   198, sisters owed the convergence + reply + catch-up) · mine to do
   (the brief authorizes exactly these three sends) · now (engine live,
   baseline current) · provable (row read-back). All five yes.
6. **Did I prove it with real measurements?** Yes — row reads first-hand
   (ids, fire/fired times, delivered_to), row-count query from the table,
   anon-read 0 rows, Playwright measurements at three widths, curl 200 +
   1,817,928 B. No claim rests on a send call returning.
7. **Anything not ten out of ten knowingly left?** Yes, named: (a) the
   no-regression console-error leg (pre-existing CORS class, control page
   identical, round changed no page bytes); (b) the SN-2722–2731 vs 2732
   adjudication (brief followed); (c) no pre-round Dashboard console
   baseline exists; (d) the recipients' rendered mail view is never
   eye-checked (by law — proof is the row only). Nothing is left silently.

## FILING

Filed to branch `mail/write-path-20261112` in ONE commit (parent
`091961ba`, verified first-hand before filing), head-guarded, read-back
verified per file (remote blob SHA = local `git hash-object` for each of
the three files; branch head re-read after filing — the resulting head
SHA is in the maker's report to the captain, and is re-derivable from the
branch at any time). Filing method: GitHub git-data API (blobs + tree +
commit + ref update) via `gh-direct.py`, token in memory only — a first
contents-API PUT created one receipt-only commit by mistake and was reset
off the branch (ref force-reset to `091961ba`, verified) before this
single filing commit, so the branch carries exactly one filing commit.
No merge — the captain double-checks, then the maker merges under the
Self-Check Law.
