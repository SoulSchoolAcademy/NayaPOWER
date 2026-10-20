# 0030 — THE VALUE-ONLY BRAIN (AI tongue)

Canonical design + behavior spec for NayaPOWER's GitHub brain. Source: Shawn's command 2026-10-20 ~23:55Z; evidence: reservoir census 2026-10-20 + Nitro's Completion Doctrine report (2026-10-20, the doctrine's enforcement record: 620 of 662 items each blocked by exactly one named gap — 325 failing CI / 208 conflicts / 77 unfinished drafts / 9 collisions; head CI 582 failing vs 80 passing; board ceremony measured at 85% of 701 comments); governing directive 6304093518 + escalation 6304214219 + convergence ruling (main seat, ~23:59Z). Human tongue: `0030-VALUE-ONLY-BRAIN-V1.human.md`. Machine tongue: `0030-value-only-brain-v1.machine.json`.

## PROBLEM REGISTER (P1–P14) → SOLUTION REGISTER (S1–S14)

| # | Problem (measured) | Solution (mechanism, not prose) | Owner | Falsifier / metric |
|---|---|---|---|---|
| P1 | Creation parallel+free, finishing serial → reservoir (662 open; 25/day in, 7/day out) | Creation freeze until open <100; permanent WIP cap 5 open PRs/lane; creation budget = merges last week + 2 | Director/dispatcher | Open count prints nightly; freeze re-engages automatically at ≥100 |
| P2 | Starts without purpose/duplicate check/owner | PURPOSE TEST mandatory pre-start (value? for whom? completable? scored?) + search-before-open (repo + PR heads + commit graph) | Every seat | Dock refuses review on duplicates; spot audits |
| P3 | Parallel duplicate versions never reconciled | One canonical seam rule: search lanes before authoring; supersede-close duplicates the same shift | Authors + dock | Duplicate pairs counted nightly → target 0 |
| P4 | Task lists auto-file follow-ups; filing counted as work | Filing ≠ work; completion is the only list metric; follow-ups require purpose test | Dispatcher | Queue OPEN count trend (365→393/day was the symptom) |
| P5 | Title/hook duplication (SN-0805 first title reused an existing hook) | Title scan before naming (existing titles/hooks registry = repo title grep over BRAIN + Hub); viral bar: hook in first breath, clarity, friend test | Authors | Duplicate-title scan in nightly report → 0 |
| P6 | Meter measured reporting (312 reports, 46 finishes; sign-out compliance 1.0) | Headline metrics replaced: merged / closed / scores-moved / reservoir count. Opened & comment counts never reported as achievement | Reporting lanes | Nightly report format audit |
| P7 | Dead work ownerless; 472 untouched ≥7d, no alarm | Expiry machinery (Nitro drain rule, adopted): every surviving item carries exactly ONE named gap + owner; owner fixes the gap or closes the item **by 2026-10-27**; anything undispositioned after that date is closed as abandoned. Untouched 7d → listed; closed at weekly distillation sweep thereafter. Reservoir counted every 30 min by the director pass, trend recorded | Merge dock + director | Untouched-≥7d count nightly → trend to 0; open count <100 by the deadline and held there |
| P8 | Rules as prose (WIP cap never enforced) | Every standing rule must name its gate/checker; a rule without machinery is filed as PROPOSED-WISH and carries no authority | Governance | Rule registry audit: rule → gate mapping complete |
| P9 | Self-merge breaches ×4 + signature≠seat (shared login) | Merge bar: 9.5 exact-head scorecard + different-seat review + green gates; L565 (login≠seat proof via seat-tagged review + declared seat); L569: unsatisfiable legs escalate to Shawn's ruleset gate — NEVER lane workarounds; bypass scoping = Shawn's human decision (open) | Merge dock + Shawn (gate) | Any merge lacking pins = breach post within one relay pass |
| P10 | Claims as truth ("ratified" without pins; fabricated quotes) | NO-WORD RATIFICATION: status claims require scorecard pins; L451: quotes attributed to Shawn require his bytes; violations VOID on adjudication | Main seat adjudication | Claim audit on board samples |
| P11 | Instruments stale (scorecard parser zeros ×3 days; brain-index drift → Kernel Tests RED hours) | Freshness law: every check names basis SHA (L572); post-commit check is authority; index regen atomic with projection (register-and-restamp in one transaction); instrument self-test in nightly report | KNOW/index lane | Kernel Tests green at tip; instrument self-test prints nightly |
| P12 | Projections land unregistered (11–13 IB pages missing from registry) | Register-on-commit inside the projection transaction — a projection that cannot register does not land | Projection lane | Registry-vs-tree diff nightly → 0 |
| P13 | Comment flood (600+/13h) taxes attention | §5 discipline: venue posts only for claim/complete/block/handoff/receipt + wins/lessons; hourly consolidation by dispatcher; posts-per-fold becomes a health metric | Dispatcher + all seats | Posts/day and posts-per-finish print nightly |
| P14 | Reports restate state; "what finished?" unasked | COMPLETED-ONLY REPORTING LAW: reports carry only completed work scored >9; silence over restatement | All reporting lanes | Report audit vs law |

## BEHAVIOR SPEC (per seat, per cycle)

1. DECLARE the Oath of Honor. ACTIVATE from current brain state (tip + distilled state, never stale cache).
2. PURPOSE TEST before any start. Fail = do not start.
3. SEARCH before creating (notes, rules, titles, PRs, branches). Build on or cite the existing artifact.
4. WORK inside WIP cap. One lane, one receipt; last-second deconfliction re-fetch before any venue post or merge.
5. FINISH with proof: scorecard at exact head + independent witness (different seat) + sabotage-tested verification + clickable evidence link.
6. REPORT completions only. Board = wins, completions, blockers, handoffs, receipts, lessons.
7. CLOSE your own dead work same-shift, reason on the page. Closing is honorable; rotting is not.
8. LEARN mechanically: lesson → rule/gate/habit change, or it is noise. A lesson counts only when a future decision changes.
9. RUN THE EIGHT VARIABLES every cycle: synergize, optimize, organize, maximize, equalize, distill, lessons, intelligence→value. Continuous, not occasional.
10. SCORE honestly: <9 does not ship, does not stay, does not get reported as value. Aim 10; floor 9 (exclusive) for reporting; merge bar 9.5.

## NIGHTLY PRINTOUT (mandatory fields)

open_pr_count · median_age_days · untouched_ge_7d · created_today · merged_today · closed_today · created_to_finished_ratio · registry_diff · duplicate_titles · posts_per_finish · kernel_tests_at_tip · scoreboard (learning / human_value / production).

## RELATIONSHIP TO EXISTING LAW

Implements and unifies: the Completion Law (SN-0805/SN-0806), the AI-waste ruling (SN-0807), the Flow Test, the Purpose Test, Completed-Only Reporting, L565/L568/L569/L571/L572, the Eight Variables. Where this spec and an older prose rule conflict, this spec governs until the older rule gains machinery or is retired. Human gates unchanged (production, credentials/money, destructive actions, ruleset/App permissions, constitutional ratification — Shawn's).
