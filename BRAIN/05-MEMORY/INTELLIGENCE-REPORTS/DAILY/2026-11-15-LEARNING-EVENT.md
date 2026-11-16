# Daily Learning Event — 2026-11-15

*Distilled by Naya Resolve from: today's memory log (`~/memory/2026-11-15.md`), the live board #3352 (384 comments, open, read this pass), and today's merged PRs via gh-app-api (#3355, #3376, #3377, #3378 — all merged 2026-11-15T22:06–22:07Z). Main tip at harvest: stable through lock-in run 213, then moving overnight.*

## THE DAILY INTELLIGENCE — max 7

1. **The Reports room was finally FILLED + VERIFIED — 23 missing days (Oct 24 → Nov 15) imported, table 27 → 50 rows, zero gaps, click-verified in the room itself.**
   - What: Resolve took the ingest herself instead of re-handing it to Nitro; bodies byte-identical to the filed editions; Oct 24's "NO REPORT FILED" placeholder now opens real content.
   - Why it matters / what changes tomorrow: filed ≠ displayed is now a proven, closed case — and a standing DAILY ROOM FILL replaces the handoff, with a one-off safeguard check on 2026-11-16 09:00 PT measuring whether the morning job lands the new edition unaided.
   - What it means: a report nobody can open in the room it belongs to is not delivered. In it for you: Shawn can finally read every day since Oct 23 in one place. Connects to: the Hub rule for Smart Notes (not done until it opens where the reader clicks).

2. **The principle ledger moved for the first time in the series: 152 → 155 (P-153, P-154, P-155).**
   - What: P-153 a gap-close naming a count of reads without their IDs is not executable; P-154 a flagged brief is never re-issued identical; P-155 a timed-out run keeps its completed half and owes its unstarted half.
   - Why: each principle changed a decision the same day it was named — the learning loop produced behavior change, not just notes. Connects to: the Daily Learning Review 2026-11-15 (board #3352, 97 in-window comments).

3. **The value census counted 2 verified outcomes — up from zero — at a ratio of ≈1097:1 (2,194 activity units).**
   - What: PR #3371 (maker triple-check naming merged head d9e481a2) and the Daily Learning Review 2026-11-14. Actions runs stayed under the 2,500 target a third straight day.
   - Why: the triple-check standard is working as a filter — 7 of 8 merges were excluded for lacking a recorded check naming their exact head. What changes: merges must carry the check at landing, or they do not count.

4. **Seven more merges landed over red CI on Nov 14 — the fourth straight day — including #3371/#3367 over standing dock HOLDs; 16 unnumbered merges are now owed, breach tally frozen at 280.**
   - What: the gate reports but does not block; enforcement, not learning, is the gap.
   - Why: a gate that cannot stop a merge is a report, not a gate. In it for you: until the gate blocks, every "verified" claim needs its own receipt read.

5. **Note serving stayed blocked a fifth straight day — all 8 probes land on the Sovereign Entrance, streak 0 — while the filed-not-registered band grew 184 → 219 and the vanish count kept climbing.**
   - What: the publish-note writer fix is landed and proven (SN-2832 registered through it), but the Intelligence Loop bot still files by direct commit around the door; SN-2882–SN-2895 filed unregistered in run 216 alone.
   - Why: P-152's graduation stays withheld — an instrument nobody is routed through cures nothing. What changes tomorrow: routing the loop bot through publish-note is the single named priority, alongside opening the entrance-gate serving defect. Unreconciled: Shawn saw SN-2832 live in his own browser; the probes disagree — that disagreement is itself the finding.

6. **Project Intelligence's record is still not settled: the stable core held all day (192 open / e0d8632c59f7, 175 judged CLOSE, stale-7d 96), the full census settled fully only once (10:53 PST, 401 / cb0930326c71), PI total moved 795 → 801 with done_proven flat at 62, and the top bar reads 0/9 exact.**
   - What: two checks hours apart agreeing remains the definition of "settled" — and it was met once, not sustained.
   - Why: numbers from a record in flux are claims, not intelligence. In it for you: trust the stable core; treat every total beside it as provisional.

7. **One RLS wall explains two blocks: Smart Mail new threads and Reports-room anon inserts both fail with the same row-level-security rejection.**
   - What: Resolve's letter to Power stayed parked after 3 identical failures; a test Reports insert via the page's anon key returned HTTP 401 / 42501. The proven write route is the Supabase dashboard owner door (CSV import), not the anon key.
   - Why: the Nov 13 privacy tightening likely overshot from blocking cross-owner reads to blocking creation. Fix sits in Nitro's backend lane. Connects to: PRIVATE BY DESIGN — privacy that blocks the owner is a defect, not a feature.

## What compounded today
- **Filed ≠ displayed changed who did the work.** The Reports-room lesson — carried as a handoff for weeks — compounded into Resolve taking the ingest herself, proving the room's live source (Supabase `hub_daily_intelligence_reports`), and closing it at the room itself. The same lesson governs the note-serving verdict: probes, not filings, decide.
- **The misnamed-root-cause lesson compounded again:** the census's 2 verified outcomes exist only because makers named exact heads — measurement changed merge behavior at landing, not after.

## What was let go
- The Reports-room handoff to Nitro — superseded by Resolve's own fill + the standing daily fill.
- The "deep-links 404" serving report — superseded by the browser probe pass + Shawn's live sighting; the states stand unreconciled, neither repeated as settled.
- The learning scorecard script's verdicts — instrument blind an 8th straight day (reads the frozen `learning-log.md`); hand truth carried instead. FLAG ONLY below.

## Trash candidates — FLAG ONLY (deletion is the Human Director's call; nothing deleted)
- `learning-log.md` (frozen source of the learning scorecard script) — instrument blind 8 days; retire or repoint the script. Feed-hygiene: a feed reading a frozen source is a superseded feed under the FEED RETIREMENT LAW.
- PR #3354 (backfill cure, draft, still not live) and PR #3345 (draft) — aging drafts; #3354's content is still needed, its manifest re-stamp and brain-index snapshot are obsolete as written (regenerate at landing).
- The unpushed cure branch at 18c37d5e and Nitro's "72-line drift" claim — unlocated against any artifact; flagged as unverifiable, not carried as fact.
- Retired boards #3066/#2793/#2765/#2721/#2641/#2537/#2175/#1354/#554 — already retired/archived; no posting, flagged only for feed hygiene.
- Repeated unchanged-state lanes: PI keeper fast-exits and mail-outbox no-mail cycles logged waste all day (record-in-flux-recheck the top waste cause, ~36–43 min/24h) — candidates for cadence reduction, not deletion, under the park rule.

## Scorecard for this report's own PR (Scorecard Law — receipt before any merge; this PR is NOT merged by this run)
Options: (A) file on a branch + PR, post the lock-in, leave merge to the protocol; (B) direct-to-main landing; (C) workspace-only.
Scores (value / consequences / mission alignment / situational awareness, /10): A = 9/9/9/9 — reversible, evidenced, canonical home; B = 5/4/6/5 — faster but bypasses the PR receipt this task requires; C = 2/3/3/2 — undelivered by the handoff rule.
Gates: A reversible ✓, no major damage ✓, positive forward effect ✓. **Decision: A.**
