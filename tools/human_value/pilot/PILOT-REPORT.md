# Pilot run — Human Value change-grade instrument v1

**Naya Mu · 2026-10-11 ~22:45–23:05 UTC**
**Instrument:** `tools/human_value/instrument.py` (rubric v1, see `HUMAN-VALUE.md`)
**Sample:** 5 merges from tonight's mainline, chosen to span the kinds of work we ship.

## Premise correction (the most important finding)

The mission brief said "build the FIRST measurement instrument." The live
repo disagreed: `tools/human_value/` on main already holds a mature
**event-ledger instrument** (`compute_hv.py`, `schema.py`,
`real_outcome_loop.py` — 12 iterations, 92 real events, cold-recompute
proofs, two green test suites). Building a second competing instrument
would have been duplication.

So this deliverable is the **change-grade companion**, not a replacement:

- **Theirs** asks: *did a human's life get measurably better, over time?* (events → HV/day → calibration)
- **Mine** asks: *was this shipped change valuable, with evidence?* (packet → scorecard → why-not-10)

**The bridge (proven this run):** `instrument.py to-event` exports a
REAL VALUE+ scorecard as a schema-valid ledger event — validated against
the *existing* `schema.py`, never hand-rolled. Results:

| Scorecard | Verdict | Event minted? |
|-----------|---------|---------------|
| PR-2375 (8.8) | REAL VALUE | ✅ `HV-20261011-PR-2375` (delta_v_actual=7.6) |
| PR-2383 (8.2) | REAL VALUE | ✅ `HV-20261011-PR-2383` (delta_v_actual=6.4) |
| PR-2188 (7.3) | REAL VALUE | ✅ `HV-20261011-PR-2188` (delta_v_actual=4.6) |
| PR-2384 (6.8) | THIN | ❌ refused — no manufactured credit |
| PR-2201 (6.8) | THIN | ❌ refused — no manufactured credit |

All 3 minted events pass `schema.validate_event` / `validate_ledger`
(the real schema, imported from the repo checkout). Events live in
`pilot/events/` — **not** appended to the canonical
`ledgers/real-events.jsonl`; that append is the human-value lane's call
(named next action below), not a worker's unilateral write.

## Scores

| # | Change | Merge SHA (verified, true merge commit, 2 parents) | Delta |
|---|--------|-----------------------------------------------------|-------|
| 1 | PR #2375 — Intelligent Blocks canonical substrate | `09d9b71a313012320eb25c21aa92863884678633` | 27 files, +2380/−0 |
| 2 | PR #2188 — receipt-gate fetch-depth repair | `312e1fd3b4f049a2ba50b29fb30e3f509cc22afa` | 2 files, +147/−0 |
| 3 | PR #2384 — brain-index regen (mechanical re-stamp) | `f33bba344a34e9e91b4b5bb6802c22f6eade3145` | 3 files, +7/−7 |
| 4 | PR #2201 — AER live-3 eligibility (drift_canary) | `f4680ff8e793ca6b089efa41f6ae773207dd29a1` | 2 files, +272/−0 |
| 5 | PR #2383 — P0-B ADVISE influence bridge | `b5007fd8d21a550930761b74f31c6ce9026296b7` | 3 files, +487/−3 |

All merge SHAs, parent counts, and file lists verified from git history (`git log`, `git diff <m>^1 <m>`), not from claims. Packets: `pilot/packets.json`. Grader: Naya Mu (single seat — see weaknesses).

## Scores

| Change | Score | Verdict | Weakest dimensions (why not 10) |
|--------|-------|---------|----------------------------------|
| #2375 IB canonical substrate | **8.8** | REAL VALUE | PROOF=8 (verification record lives in a lane-feed comment, not in-repo) |
| #2383 influence bridge | **8.2** | REAL VALUE | CLEAN=6 — broke `test_measure_node_influence` (9→10 count), parked not fixed |
| #2188 receipt-gate repair | **7.3** | REAL VALUE | DELTA capped 8→5 [UNCITED_CAP] — the FAILURE→SUCCESS flip is attested, not in-repo |
| #2384 index regen | **6.8** | THIN | DELTA capped 7→5 [UNCITED_CAP]; DURABLE=5 — regens rot (stale again within the hour) |
| #2201 eligibility | **6.8** | THIN | DELTA capped 7→5 [UNCITED_CAP] — new capability, but no in-repo before/after metric |

**No harm found in any change** (harm gate checked first; all passed).

## What the instrument caught (the finding)

Three of the five DELTA judgments were **capped by the evidence rule**: the grader claimed 7–8 for "the number moved up," but the only evidence was *attested* — another worker's report, a live event nobody committed to the repo. The instrument refused to score those above 5 and flagged `UNCITED_CAP`.

This is the instrument working as designed, and it points at a real hole: **we claim deltas we don't commit.** The receipt-gate flip (FAILURE→SUCCESS live) was observed by a human and written in a lane-feed comment. Nothing in the repo proves it. If the feed vanished, the proof would vanish.

**Observatory recommendation:** lane workers should commit machine-readable receipts (gate states, test outputs, before/after numbers) into the repo with the change — not just lane-feed prose. What isn't committed isn't measured.

## Honest weaknesses of the instrument (why it is not a 10)

1. **It grades packets, not reality.** A grader can write a beautiful packet about a useless change. The instrument catches *invented citations* (it checks files exist at the ref) but cannot catch *inflated claims* about what a change does. Garbage in, graded garbage out.
2. **Proximal proxies, not human lives.** For infrastructure work it measures usable tooling, real tests, working gates as *proxies* for human benefit. It cannot tell whether Shawn's life actually got better. Definition test #2 ("the number moved up") is measured at repo level, not human level. The observatory's hardest problem is still open.
3. **Single grader, correlated judgment.** I (Naya Mu) wrote the rubric, built the scorer, *and* graded the packets. Per SN-042, correlated reviewers are not independent evidence. A second seat grading the same packets blind is the real test — not done yet.
4. **The attested loophole.** Attested evidence ("someone's word") still carries scores up to 5. A dishonest grader's word counts for 5 points per dimension. The instrument marks it as attested so readers can see it — but it doesn't stop it.
5. **The DELTA cap is conservative by design.** Real off-repo deltas (live gate flips, human confirmations) can never score above 5. This under-scores genuinely valuable operations work. Deliberate — but it means the instrument punishes value it can't see in-repo.
6. **No longitudinal check.** DURABLE is a prediction at grade time, never re-checked. A v2 re-grades after 7 and 30 days and compares prediction vs reality.
7. **Weights are asserted, not derived.** USE 30 / DELTA 25 / PROOF 20 / DURABLE 15 / CLEAN 10 is a judgment call, documented but unproven. No calibration exists.
8. **No calibration against Shawn.** We don't know if an 8.8 "feels like" 8.8 to him. The Usefulness Gate is ultimately his judgment; the instrument has never been tested against it.
9. **Small, friendly pilot.** n=5, all from one night, all our team's work, no adversarial packets, no real known-useless change in the sample (synthetic ones are in the test suite).
10. **The harm gate is only as good as the grader.** The instrument does not scan for harm itself — it trusts `harm_check`. A grader who doesn't look for harm finds none.
11. **The `delta_v_actual` map is asserted, not calibrated.** `to-event` maps the 0–10 rubric score linearly onto the calculus [-10, 10] scale (`(score-5)*2`). Clean and documented — but unproven against real calibration data. The real-outcome loop will judge it.
12. **The premise was wrong and I almost duplicated.** The brief said "first instrument"; the repo had a mature one. I caught it before pushing because I read the tree first. The process lesson: *read the repo before believing the brief* — the brief is a claim, the tree is evidence.

**Instrument self-score: 6.5/10.** It is an honest first ruler: strict about evidence, transparent about what it can't see, reproducible, and now *composed* with the existing observatory instead of competing with it. It is not yet a measure of real human benefit — it is a measure of *evidenced proximal value*, which is the first step toward the observatory, not the observatory itself.

## Named next actions

1. **Lane decision:** append (or decline) the 3 minted events in `pilot/events/` to the canonical `ledgers/real-events.jsonl`. The events validate; the append is a lane-owner write.
2. **Second-seat grading:** an independent seat re-grades the 5 packets blind. Correlated single-grader judgment is the pilot's weakest epistemic point (SN-042).
3. **Receipt discipline:** lane workers commit machine-readable receipts (gate states, before/after numbers) with changes — the UNCITED_CAP finding shows our deltas live in chat, not in the repo.
4. **Durability loop (v2):** re-grade scored changes after 7/30 days; compare DURABLE predictions vs reality.

## Reproduction

Packets: `tools/human_value/pilot/packets.json` (schema v1).
For each packet: `python3 tools/human_value/instrument.py score --packet <p> --repo <nayapower-work> --ref <packet.merge_sha>`.
Scores regenerate deterministically from the packets + public git history
(`graded_at_utc` aside, the scorecard content is a pure function of packet + tree).
