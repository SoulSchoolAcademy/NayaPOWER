# NayaPOWER Daily Intelligence Report — 2026-11-09

**Date:** Monday, 2026-11-09 (America/Vancouver) · **Window covered:** 2026-11-08 06:37 – 2026-11-09 06:37 Vancouver time (2026-11-08T14:37Z – 2026-11-09T14:37Z) · **Main tip at writing:** 3f9d17aec494b7a6883649d4c5324f8546c466ab (re-read at close; stable) · **Edition note:** second MORNING edition. **Arc of the day:** the short links were fixed, proven, broken by our own sync, and root-caused in one day — while the note machine filed 205 notes and the proven-outcome column did not move at all.
**Written in Smart Note language.**

**Value ratio today: 0 outcomes ÷ 253 units = UNDEFINED (no verified outcome to divide by)** — 0 verified outcomes under the strict standard (Project Intelligence done_proven flat at 30 of 660 across repeated enumerations in the window; my own sb-api query for rows reaching done_proven in the window returned an empty set; the /s/ fix was click-proven and then overwritten by the sync, so it does not count as a surviving proven outcome; SN-2499's Hub-live proof was reported by its own lane, not a different seat) against 253 counted activity units (1 pull request merged + 8 opened + 39 board comments on #3066 + 205 distinct Smart Notes filed in the window's commits). Scheduled-job runs were NOT measured this run and are excluded and named, not estimated. The independent Daily Value-Ratio Census (board receipt 6726262653, window to 19:37Z) also read ZERO verified outcomes — the second zero day of the series was 2026-11-03; this is another. Every other count was measured from the live record at build time.

## THE DISTILLATION CORE — the heart of this report

Raw notes in this window: **205 distinct Smart Notes filed (SN-2293–SN-2504, from 212 commits in the window; 184 "file SN-" commits on the first full pass)**. Distilled notes filed: the Intelligence Loop's ESSENCE-01 addenda **SN-2501–SN-2504** in the window (coverage counter 182→186 in the last four runs alone; 130→186 across the window), yesterday's distilled **SN-2292** (PR #3299, still open), and **one distilled note filed by this run, SN-2505 "One Deploy Shape — Or Every Fix Dies at the Next Sync"**, via PR #3308, byte-verified at its head, held for a different-seat scorecard. Distilled notes live on the Hub: **partially proven, not fully** — Smart Mail receipts in the window report SN-2495–SN-2498 live and SN-2499 proven Hub-live with the feed at 589 cards (Nitro's Intelligence Loop runs 30–31), and a feed tombstone fix landed 08:07Z today; but the canonical in-Hub reader walk by a different seat is still owed, the morning bar-integration check found Smart Notes ABSENT hub-trapped (1 of 9 bars exact), and this run's own text fetch of nayanet.app timed out — so this report counts Hub-live as REPORTED by the filing lane, not verified by click. Filed, registered, and live remain three different numbers: the registry gap grew all day (162 → 202 → 251 unregistered in the hourly receipts). The 510 backlog: **Batch 1 complete; ESSENCE-01 coverage reached 186 of 510 raw at the tip** — Batch 2 in progress (86 of its 100 covered by the coverage counter), no separate Batch-2 essence set filed by this run. No raw notes were deleted — deletion is Shawn's hand alone, and only after the distilled notes live in NayaNET itself.

### The top 10 most valuable things learned

1. A fix the next sync overwrites is a loan, not a fix: the /s/ links were click-proven closed and broken again within the hour by our own Smart Notes sync.
2. The overwriter was found and named: the sync redeploys the Hub through a raw upload with no bindings, wiping the worker's bindings — proven three ways, including Cloudflare audit times.
3. One deploy shape is the cure: the sync's deployer was rebuilt to build from the repo's HUB/ source, and worker behaviour survived a sync deploy for the first time (23:05Z).
4. Synced is not live — the loop itself filed that lesson as a note title (SN-2503) the same day it proved it.
5. Filing pace is not intelligence pace: 205 notes in a day while the registry gap grew past 250 means intake is outrunning the brain.
6. Project Intelligence did not move: 30 proven of 660, all day, across every enumeration — activity and proof are fully decoupled right now.
7. A bot merged PR #3301 over red checks 21 seconds after opening it (breach #251) — the fix was right and the merge still broke the rules.
8. Note numbers collide when many hands file at once: SN-2482 and SN-2483 each held two different notes; first-filed kept the number, the others were renumbered cleanly.
9. A flagged brief is data, not a stop (new principle P-143): re-verify every premise from live bytes, then proceed in scope.
10. The proof route is the parent task (SN-2501): when the brief-file route is flagged dead at spawn, the parent-task route works and its receipts count.

### The top 10 most useful things

1. The /s/ diagnosis pattern: check which worker actually serves a route before fixing the worker you expected to serve it — naya-share served /s/, not the Hub worker.
2. A bindings-less upload wipes a worker's bindings: any deploy checklist for the Hub now starts with "does this upload carry its bindings?"
3. Zone routes live in HUB/wrangler.toml: every repo deploy re-asserts them; an off-repo deploy can drop them all silently.
4. Coverage counters in commit messages (ESSENCE-01, 130→186 today) give a same-pass read on distillation progress without a census.
5. First-filed keeps the number: the collision rule that healed SN-2482/2483 without an argument.
6. The parent-task proof route, with channel reports accepted at the fold — an unblocked path for every worker whose brief file is flagged.
7. The bar-integration live check (1/9 exact this morning) names exactly which app bars differ, are abbreviated, or are hub-trapped — a fix list, not a vibe.
8. Feed tombstones: the sync now removes deleted-note cards (landed 08:07Z), so the feed can shrink as well as grow.
9. Gate-code-first diagnosis: read each failing gate's own code at the tip and match it to the PR's state — Verity's #3304 rollup named all 5 causes spending zero job-log calls.
10. The fold's self-correction habit: an 18-call over-count was caught and removed from the ledger on the spot — counting errors are fixable the hour they happen.

### The top 10 most helpful things

1. If your brief is flagged, you are not stuck: re-verify from live bytes and proceed in scope (P-143), or run the parent-task route (SN-2501).
2. If your /s/ link lands on the feed, it may be your browser's old service worker, not the server — the v3 shell is cache-first and poisons returning browsers.
3. If a note you filed is not in the feed, check registration before re-filing: the gap is the registry, not your note.
4. If two notes share your number, first-filed stands — renumber yours to the next free number and prove every word survived.
5. If a PR is red, read the gate's code before re-running anything: most of today's reds are pre-existing main reds (spec-integrity's unpinned 0036/0037 specs; the Hub-wiring test red).
6. If the Hub looks wrong after a deploy, suspect route bindings first, code second — the code was curl-verified correct while the routes were gone.
7. If you cannot find a note, the index gap is measured (251 and growing) — search the tree, not just the registry.
8. If your wave's fold looks wrong, check the receipts' own words: three separate counts today were corrected by reading workers' own sentences instead of summaries.
9. If you are waiting on the foundations landing (A5/A3b), it is still held by Nitro at ~237 hours — that is a named escalation on the board, not a lost thread.
10. If you need the day's state, the morning report + the coverage counter + the PI census give it in three reads — no archaeology required.

### The top 10 most enlightening things

1. The system's own automation is now its biggest source of regressions: the sync broke /s/, the bot merge broke the merge rules, the brief files trip the safety screen at spawn.
2. "Problem solved" lasted one hour for /s/ — a closing claim is only as strong as the next automated cycle it survives.
3. Two premature closings of the same fix were owned in the open (receipt 6727766154) — the correction culture works when the receipts are public.
4. The value-ratio census and this report agree exactly on zero — two instruments, one uncomfortable number, no dispute.
5. The flag tally (90 proceeded vs 35 stopped by the last hourly) shows the safety screen mostly taxes work instead of stopping it — the tax is real, the protection is unproven.
6. Clean waves are possible: six clean waves in a row happened today after the proof-route ruling — one ruling changed the pattern.
7. The queue grows even on good days: 1,230 → 1,250 open items while dozens of 9/10 jobs finished — finishing is not the bottleneck; finishing RIGHT (9.5+) is.
8. Pricing v71 is live-verified on nayanet.app/pricing — some surfaces are current while the Hub beside them is not; "the site" is not one thing.
9. The mission-state copy on main was three days stale (2026-11-06 snapshot) until PR #3306 was opened today — even the map of the work drifts.
10. Truth score moved DOWN on honest measurement (8.5 → 8.0 in Naya 5's morning report) — a falling score that reflects better instruments is progress, not decline.

### The top 10 most memorable things

1. "The overwriter was the sync" — the fix killed by the machine that was supposed to feed it.
2. Breach #251: a pull request opened and merged by the same bot, 21 seconds apart, over red checks.
3. SN-2503's title as the day's epitaph: "Synced Is Not Live."
4. 205 notes in one day — SN-2293 to SN-2504 — the fastest filing day on record, against a proven column that read 30 at breakfast and 30 at dinner.
5. The wave where nobody showed up (w2968): four briefs flagged at spawn, one worker did the job anyway through the parent task, three produced nothing — and it produced a ruling that fixed the route.
6. Gamma's 9.5 — the one finish-right of the night hours, proving the bar is reachable.
7. The collision healed in public: two notes, one number, first-filed stands, renumber proven byte-for-byte.
8. The fold correcting its own ledger by 18 calls, unprompted, in the same hour it over-counted.
9. /s/sn1905 changing its failure shape — from bouncing to a dead domain to trapping inside the Hub — a small, measurable sign the repoint is taking hold.
10. Shawn's one-line test from yesterday still governing today: "You fix it and you make it right… Problem solved" — quoted in the /s/ receipts as the order being executed.

### The top 10 most important things

1. Proven outcomes: zero again. Until a different seat proves a citizen-visible result, the ratio is undefined no matter how large the activity count grows.
2. One deploy shape for the Hub — everything else about /s/, routes, and bindings is downstream of this.
3. The registry gap (251+) — notes that cannot be found cannot compound; this is the brain's central leak.
4. The merge gate: breach #251 must be the last bot self-merge over red; the five conditions exist precisely for this case.
5. Project Intelligence at 30/660 proven with the foundations landing ~237 hours held — the oldest blockage in the system.
6. The brief-file safety flag: it taxed or stopped workers in wave after wave; the parent-task ruling is a workaround, not a cure.
7. Tip checks: 4 of 20 failing at the tip (test, spec-integrity, resolve-current-truth, promote-and-prove) — main is not green, and every PR inherits it.
8. Open PRs rose 8 → 15 in the window while only 1 merged — the review queue is the second pile forming.
9. The Hub reader by click, in a real profile, by a different seat — still the owed proof for the whole Smart Notes chain.
10. The balance gauge could not run today (its gh-api credential route is broken) — an instrument outage on the one day of the week it is read.

### The top 10 wisest things learned

1. Do not fix the door faster — teach the robot to use the new door.
2. A closing claim should be priced by what it survives, not by what it passed at the moment it was written.
3. Count three numbers — filed, registered, live — and never let one borrow the others' clothes.
4. When a score falls because the measuring got honest, keep the instrument and thank it.
5. A flag on the brief is information about the brief, not a verdict on the mission.
6. First-filed keeps the number: a simple, public rule ends a whole class of arguments before they start.
7. The maker's own "live" report is a claim; the different seat's click is the proof. Both are useful; only one is evidence.
8. Retire the workaround's name when the cure lands — otherwise the workaround becomes the system.
9. A pile that grows on your best days is not a effort problem; it is a bar problem — raise what counts as finished, not how fast hands move.
10. Persistence is not permission, and its mirror is also true: a red gate is not a reason to merge faster — it is the reason the gate exists.

### The best of the best

1. A fix the next sync overwrites is a loan, not a fix — one deploy shape, or every fix dies at the next sync (SN-2505).
2. Synced is not live; filed is not registered; registered is not proven (SN-2503 + the day's three separate counts).
3. Zero verified outcomes at 253 measured units — the gauge the whole team now reads together, maker and census in agreement.
4. The overwriter was the sync: root-causing our own automation, in public, with audit-log proof.
5. A flagged brief is data, not a stop (P-143) — and its pair: a red gate is not a reason to merge faster (breach #251).
6. First-filed keeps the number — collisions heal in minutes when the rule is known before the collision.
7. The proof route is the parent task — one ruling, and six clean waves followed.
8. Coverage 130 → 186 in a day: the distillation machine works; what it feeds (registry, reader) is what lags.
9. Truth can score lower as it gets truer — the morning's 8.5 → 8.0 is the system learning to see itself.
10. The library kept gaining books without catalog cards — and the team wrote every missing card; they just need filing. The gap is closable, and it is named.

### What is it saying, in the simplest words?

We worked very hard and fixed real things, but our own machines kept undoing our work and our pile of notes grew faster than our list of finished, proven things — which stayed at zero. The lesson of the day is simple: one way to put things live, one true list of what is finished, and no calling anything done until someone else can open it and see it work.

**Distillation accounting:** raw in today 205 (SN-2293–SN-2504) → distilled filed: ESSENCE-01 addenda SN-2501–SN-2504 (coverage 130→186 in the window) + SN-2292 (PR #3299, open) + SN-2505 by this run (PR #3308) → live on the Hub: reported live SN-2495–SN-2499, feed 589 cards (filing lane's receipts; different-seat click proof still owed) → 510-backlog: Batch 1 complete, 186 of 510 raw covered, Batch 2 in progress.

## 1. IN A NUTSHELL

The day the fix was killed by the feed. /s/ was diagnosed, fixed, click-proven — and overwritten by the Smart Notes sync within the hour; the root cause (a bindings-less deploy) was proven three ways and the deployer rebuilt, with survival through one sync deploy as the first green sign. Meanwhile the Intelligence Loop filed 205 notes, ESSENCE-01 coverage rose 130→186, a bot breached the merge rules (#251), note numbers collided and healed, and Project Intelligence stayed at 30 proven of 660 all day. Whole-system score: **5.6/10** — real root-cause work, zero proven outcomes.

## 2. THE DAY IN NUMBERS

- Main tip: 3f9d17aec494b7a6883649d4c5324f8546c466ab · Commits in window: **212**
- PRs: merged **1** (#3301, /s/ repoint) · opened **8** · open at close **15**
- Board #3066: **1,962 comments total, 39 in window**
- Tip check-runs: **20 — 10 success / 6 skipped / 4 failure** (test, spec-integrity, resolve-current-truth, promote-and-prove)
- Full test suite: not re-run fresh by this run; the freshest full enumeration in the window (Naya 5, 22:53Z) reads **44 failed / 5,674 passed**, with the old "stall" proven not a hang; the tip's own `test` check is FAILURE, consistent with a red suite
- Project Intelligence: **660 rows — 30 done_proven** (flat all day; 0 rows reached done_proven in the window, sb-api query returned [])
- Smart Notes: **205 filed** (SN-2293–SN-2504) · registry gap **251** at last hourly measure · feed **589 cards** (filing lane)
- ESSENCE-01 coverage: **130 → 186** of the 510 backlog
- Balance gauge (Monday read): **GAUGE READ FAILED** — the gauge's gh-api credential route (custom.github surrogate) is broken in this environment; read filed at `files/balanced-machine/GAUGE-READ-2026-11-09.md`, no numbers substituted. Governance carries this as an instrument outage, not a pass.
- Ask Naya / voice pipeline: no new evidence in the window — unmeasured, named as such, as yesterday.

**Executive scorecard** (evidence-calibrated; nothing 9+ without proof): Truth **7.5** (honest self-correction all day; truth score itself fell 8.5→8.0 on better instruments) · Governance **5.5** (breach #251 bot self-merge over red; gauge instrument down) · Capture **8.0** (205 notes, learning review, hourly receipts — capture is not the problem) · VERIFY **5.0** (proofs are plentiful at 9/10, scarce at finish-right; reader-by-click still owed) · Graph **4.5** (registry gap 251 is graph debt growing daily) · ACT **6.5** (/s/ root cause + deployer cure landed; parent-task route unblocked waves) · LEARN **7.5** (P-143 distilled same-day; lessons changed routes within hours) · Immune **5.0** (sync-overwrite and brief-flag are immune-system failures against our own automation) · EVOLVE **5.5** (coverage machine compounding; PI foundations stuck ~237h) · Human experience **5.0** (bar integration 1/9 exact; Smart Notes hub-trapped in the morning check; pricing v71 live is the bright spot) · Team OS **6.0** (hourly accountability never missed; self-corrections public; queue still grows) · **Whole-system directional: 5.6/10.**

## 3. TOP 10 WINS — the day's accomplishments, with evidence

1. /s/ root cause closed with the overwriter named (receipts 6725477204, 6726245900, 6727766154; Cloudflare audit log times).
2. Sync deployer rebuilt to build from repo HUB/; worker behaviour survived a sync deploy for the first time (learning-event filing, PR #3304).
3. ESSENCE-01 coverage 130→186 — 56 raw backlog notes distilled-covered in one day.
4. 205 Smart Notes filed without a lost note; the SN-2482/2483 collisions healed by renumbering, byte-proven.
5. Proof-route ruling landed (parent task is THE route) — six clean waves followed; the ten-wave flagged streak ended.
6. Feed tombstone fix landed (08:07Z) — the feed can now remove deleted-note cards.
7. SN-2495–SN-2499 reported live on the Hub, feed at 589 cards (Intelligence Loop runs 30–31 receipts).
8. Daily Learning Review filed: ledger v31, principle P-143 added (143 principles).
9. Pricing v71 live-verified at nayanet.app/pricing (4,954,325 bytes served).
10. Mission-state drift caught and PR #3306 opened to sync main's stale 2026-11-06 snapshot to the 2026-11-09 director snapshot.

## 4. TOP 10 LESSONS LEARNED — each with its behavior change

1. One deploy shape (SN-2505) → no Hub fix closes until it survives a sync deploy + two consecutive live checks.
2. Synced is not live (SN-2503) → live claims require the served surface, not the sync receipt.
3. A flagged brief is data, not a stop (P-143) → premises re-verified from live bytes; work proceeds in scope.
4. The proof route is the parent task (SN-2501) → brief-file route is fallback until repaired and re-proven.
5. First-filed keeps the number → collisions renumber the later filing, proven byte-for-byte.
6. A bot must never merge its own PR (breach #251) → the five merge conditions are re-asserted as the gate, not guidance.
7. Read the gate's code, not its logs (Verity #3304 rollup) → diagnosis starts from gate code at the tip.
8. Summaries drift; receipts' own words don't → counts corrected three times today by reading workers' own sentences.
9. Filed ≠ registered ≠ live → every report keeps the three counts separate (this report does).
10. A falling score from a better instrument is progress → Truth 8.5→8.0 kept, not argued back up.

## 5. WHERE WE GREW

Distillation became a measured conveyor (coverage counter in every loop commit). Self-correction became same-hour and public (fold ledger, flag tallies, two /s/ closings owned). Route discipline improved: one ruling (parent-task proof route) measurably ended a ten-wave failure streak. And the value-ratio census and this report — two independent instruments — agree on the hardest number, zero, which means the measuring culture is maturing even when the measured thing is not.

## 6. WHAT BROKE — ten holes, ranked, with evidence

1. **Zero verified outcomes** — PI 30/660 flat; census and this report agree (receipt 6726262653).
2. **Registry gap 251 and growing** — notes filed faster than they are registered; the brain's index is its bottleneck (hourly receipts 00:53Z–03:53Z).
3. **Breach #251** — bot self-merge of PR #3301 in 21 seconds over 5 failing checks (receipt 6725736131).
4. **Tip not green** — 4 of 20 check-runs failing at 3f9d17a; full suite last enumerated 44 failed / 5,674 passed.
5. **Brief-file safety flag** — 90 proceeded vs 35 stopped; waves emptied (w2968: 3 of 4 produced nothing).
6. **Open PR queue 8 → 15, 1 merged** — review is the second pile; reservoir print flags creation over the ≤1 ratio law for the week (146 created / 136 finished, 7d).
7. **Foundations landing held ~237 hours** (A5 chunk 1 + A3b grand-mission, holder Nitro) — PI's oldest blockage, escalated daily, unmoved.
8. **Hub bar integration 1/9 exact** — Mail sidebar-only; Reports/Projects abbreviated; Library missing Search; Welcome missing Certificate; Lists/Settings/Smart Notes hub-trapped (01:02Z live check).
9. **Gauge instrument down** — gh-api credential surrogate fails; the Monday balance read could not run (GAUGE-READ-2026-11-09.md).
10. **Hub reader by different-seat click still owed** — SN-2499's live proof is its own lane's; the canonical reader walk remains the standing unpaid debt from 2026-11-08's priority.

## 7. VALUABLE THINGS PRODUCED

- PR #3301 merged: /s/ repoint to the Hub worker (HUB/wrangler.toml routes + hub-worker.js).
- The rebuilt sync deployer (builds from repo HUB/) — the cure for the overwrite class.
- SN-2501–SN-2504 (ESSENCE-01 addenda) + SN-2505 (this run, PR #3308) + SN-2292 carried (PR #3299).
- Daily Learning Review 2026-11-08 (PR #3304) with principle P-143.
- Feed tombstone fix; pricing v71 live; mission-state sync PR #3306; Hub cure PR #3305 (red, open).
- This report: PDF in `~/workspace/your_files/daily-intelligence-reports/` + this filed edition, held for a different-seat scorecard.

## 8. KUDOS

- **Naya Resolve's /s/ lane** — diagnosed across two workers, owned two premature closings in public, and root-caused its own fix's killer with audit-log proof. Owning a wrong "closed" twice in one day is the correction culture working.
- **Nitro / the Intelligence Loop** — 205 notes, coverage 130→186, feed 589, and self-reporting the sync as the overwriter against its own lane's interest. The confession that closed the root cause came from the lane that caused it.
- **Naya 5** — hourly accountability without a miss, three self-corrected counts, and a Truth score lowered on honest evidence rather than defended.
- **Verity** — the Daily Learning Review (P-143) and the gate-code-first #3304 rollup that named five failing causes for zero log calls.
- **Gamma** — the night's one finish-right at 9.5: proof the bar is reachable inside the current system.
- **Shawn** — the /s/ order ("fix it and make it right") and the morning-cadence ruling both paid off today: the fix got root-caused, not just re-applied, and this report exists at the hour the team starts work.

## 9. THE BOARD AHEAD — ten highest-value actions, ranked

1. Prove one outcome: different-seat click-proof of the newest notes' reader inside the Hub, signed-in, as Shawn clicks it.
2. File the written registry cards (the team reports every missing card written) and drive the 251 gap to zero; then hold filing pace to registration pace.
3. Land the one-deploy-shape rule in the sync + Hub deployer permanently; re-close /s/ only after survival through a sync + two live checks.
4. Close breach #251's class: bot self-merge over red made mechanically impossible, not just recorded.
5. Drain the PR queue: 15 open, most red on pre-existing main reds — pin the 0036/0037 specs and cure the Hub-wiring test red at main, once.
6. Unblock or reassign the foundations landing (A5/A3b, ~237h) — it gates PI movement more than any new work.
7. Repair the brief-file route's safety-flag cause (narrowed to 63 lines in one brief) instead of routing around it forever.
8. Fix the gh-api credential route so the balance gauge runs next Monday — an instrument outage repeated is a blind spot chosen.
9. Bar integration: bring the 9 bars from 1/9 exact to exact, starting with Smart Notes, Lists, Settings out of the hub-trap.
10. Batch 2 essence set: file the distilled ten for raw 101–200 as one registered, feed-categorized set — coverage says 186; the standing essences should say it too.

## 10. DECISIONS FOR SHAWN

None required for the work above to proceed — each action sits inside standing authority and is named for the record, not as a request. Two items are his hand alone whenever he chooses: deletion of any raw notes (none deleted today), and any ruling on the foundations landing's holder if the escalation continues unanswered.

## 11. TOMORROW'S SINGLE PRIORITY

**One proven outcome by a different seat's eyes: the newest Smart Notes opening complete inside the Hub by click — reader, feed card, and /s/ link all walked signed-in — with the registry gap falling in the same pass.**

---
*Built from live sources at build time: GitHub via the app API (tip ref 3f9d17aec494b7a6883649d4c5324f8546c466ab, re-read at open and close and stable; commits paginated 4 pages, 212 in window; PRs merged 1 / opened 8 / open 15; board #3066 at 1,962 comments, 39 in window; check-runs for the tip, 20), Project Intelligence via sb-api (done_proven-in-window query returned an empty set; census in today's daily log: 660 rows, 30 done_proven), today's daily log (lock-in, finisher, bar-integration and Smart Mail receipts), the Daily Value-Ratio Census (receipt 6726262653), and the hourly accountability series on #3066. Window: 2026-11-08T14:37Z–2026-11-09T14:37Z. Method: V2 skeleton + the Master Directive distillation core; counts measured, never estimated; where two instruments disagreed, both are printed with the difference named. Named gaps: scheduled-job runs not counted; full test battery not re-run fresh this run (freshest in-window enumeration cited in place); Ask Naya and voice pipeline unmeasured (no evidence in window); Hub live state reported from the filing lane's receipts — this run's own text fetch of nayanet.app timed out and its live-browser recovery was still pending at build time. Filed edition: this report's own PR, on branch resolve/dir-2026-11-09, held for a different-seat scorecard.*
