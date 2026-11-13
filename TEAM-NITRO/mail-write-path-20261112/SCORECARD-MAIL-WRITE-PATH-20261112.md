# SCORECARD — MAIL WRITE-PATH ROUND

**Honest score: 9/10.**

## Why it is not a 10

1. The no-regression battery's console-error leg does not pass literally:
   24 / 24 / 26 console errors at 1440 / 390 / 360. Every one is the same
   pre-existing CORS class on the live pages' direct browser→Supabase
   reads, present identically (28) on the untouched Personal control page,
   and this round changed no page bytes — but the battery as written says
   "zero console errors", and the round does not claim a clean battery.
2. No pre-round Dashboard console baseline exists, so "no regression"
   rests on the control page + zero page writes, not a before/after.
3. The recipients' rendered mail view is never eye-checked — by law, proof
   is the scheduled_messages row only. That is the design, not a defect,
   but it caps what "proven" can mean for a mail round.
4. The digest's SN range needed mid-round adjudication (2722–2731 vs one
   daily-log line's 2722–2732); the brief was followed and the call is
   named in the record.
5. Step 1's engine-liveness evidence was a 2.5-hour-old fired row plus the
   behavioral proof of the three rows firing — not a fresh row at Step 1.

## 10 things loved

1. The gated path used exactly as harvested — scheduler + worker, no new mechanism.
2. The sched_create RPC contract read first-hand from its migration; shape matched, no divergence.
3. The live baseline re-read first-hand and matched the carried back-end record row for row.
4. The anon read re-verified blind (0 rows) and left blind.
5. Send 2 byte-identical verbatim, verified twice by cmp.
6. All three rows fired on the first attempt, ~53 s after fire_at, delivered_to exact.
7. Row count from the table = 3 — no fourth send, counted, not logged.
8. Playwright Firefox actually ran — overflow 0 at 1440/390/360.
9. The CORS class characterized with a control page instead of hidden.
10. No secrets printed, logged, or stored; the owner session minted for the run was dropped.

## 10 things not loved

1. The console-error leg (above) — the round's only non-pass.
2. The brief's "delivered_to" shorthand invited a real 400 on my first probe.
3. The brief's "from main head 091961ba" wording misled my first reading of the branch head.
4. "The captain's one-record proposal" has no single canonical file to point at.
5. The digest window in the brief ends 00:28Z but the coverage list runs to 02:16Z.
6. EPERM flake discipline slowed every file write (all read back, none lost).
7. A service restart mid-probe (nothing lost, but a reminder the ground moves).
8. The 2.5 h engine-idle gap at Step 1 needed behavioral proof.
9. No prior two-alias mail row existed in the baseline for send 3 to compare against.
10. The round's proof is row-only by law — the human eye never sees the delivered mail.

## 10 things to make it 10x better

1. A standing pre-round console baseline for the Dashboard (or a fix to its direct Supabase reads) — another round's job, named here.
2. One line in the brief template: delivered_to lives in result, not as a column.
3. One line in the brief template: branch head, not main head.
4. A canonical file for the captain's one-record proposal.
5. Digest coverage windows stated as the task's list, not a stale end time.
6. Keep the control-page probe as the standard move whenever a battery leg fails.
7. Keep every write read-back verified under the EPERM flake (done this round).
8. Keep outputs on disk before reporting (done — the restart cost nothing).
9. For two-recipient sends, keep the single-row shape (proven this round).
10. Keep the score honest when a leg is partial — never round a partial up to a pass.

## 10 solutions applied right now

1. The column correction is written in the record, not just fixed in the probe.
2. The branch-head correction is written in the record.
3. The SN-range adjudication is written in the record.
4. The console-error leg is reported as partial, not as a pass.
5. The digest states its coverage window plainly (~02:40Z).
6. The receipt carries the full row read-back.
7. The schedule/proof/count/no-regression logs are kept in the work dir.
8. The control-page probe is filed as evidence (Personal, 28 errors, same class).
9. Nothing is claimed from a send call — only from row reads.
10. The score is 9, not 10 — the point off is the console-error leg, named above.

## Verdict

The round's own deliverable is complete: 3 sends, 3 rows, 3 proofs, every
bound held. The point off is the verification battery's console-error leg,
which fails literally on a pre-existing environmental class the round did
not cause and cannot fix inside its bounds. 9/10 — file, do not rework,
captain double-checks before any merge.
