# SN-0962 — When CI Logs Are Walled, Declare PROVEN-UNKNOWN and Repro Locally at the Exact Pinned Head

- **Intelligent Block:** IB-SMART-NOTE-20261011-sn0962-when-ci-logs-are-walled-repro-locally-at-exact-head
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE (Team Naya engineering knowledge)
- **Captured:** 2026-10-11
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
- **Provenance:** night-shift-2026-10-10, worker t0042-browser-1825-log (tick t0042) — receipt `receipts/t0042-browser-1825-log.md` (score 6): "failing test names now PROVEN-UNKNOWN via both API (t0042-c) and browser… named the cheapest remaining route (local repro at exact head bytes)"; worker t0052-a (tick t0052) — receipt `receipts/t0052-a.md` (score 8): executed the route at pinned head 9a9954bc8886 (head unmoved during run): 5 failed / 1051 passed / 11 skipped, all 5 attributed; morning-flags.md #9 (2026-10-11 01:04 PDT).

## IN A NUTSHELL

PR #1825's failing tests were unknowable all night: the GitHub API gave workflow-level status only, and the job logs sat behind a sign-in wall. After ~10 timed-out browser attempts and an API dead end, worker t0042-browser-1825-log did the intelligent thing: it **declared the failing test names PROVEN-UNKNOWN** (honest unknown, not a guess) and named the cheapest remaining route — a local repro of the exact CI step at the exact pinned head bytes, fetched over the git protocol (zero REST quota). Worker t0052-a executed it: fetched `refs/pull/1825/head` at pinned `9a9954bc8886`, confirmed the head didn't move during the run, ran bare `python -m pytest -q`, and closed the 4-tick unknown in one pass — all 5 failures exactly attributed (324 unregistered candidate notes trip the drift guard 1→324 and drop the SN-0632–SN-0959 guards; 3 stale SN-0359 artifacts that vanish on rebase). The doctrine: when the logs are walled, stop probing the wall — declare PROVEN-UNKNOWN, then take the cheapest route that can actually prove the answer. The local repro also catches environment confounds for free (the same run is where SN-0960's /tmp-full phantom failures were found).

## HUMAN NOTE

It's like the mechanic's computer refusing to show the error codes — the screen is locked, the manual is behind glass. You could keep poking at the locked screen for an hour (ten timed-out attempts), or you can open the hood yourself and look at the engine. The engine is right there: the exact commit bytes are fetchable for free, and running the exact test command locally shows you everything the locked screen was hiding. Honest "I can't see it" beats a confident guess — and opening the hood beats staring at the locked screen.

## CHILD NOTE

Imagine your teacher won't show you which questions you got wrong — the paper is locked in a drawer. You can keep asking for the paper, or you can just take the test again yourself at your desk and see which questions are hard. That's what the worker did: couldn't see the answers, so they re-did the work locally and found all five tricky questions by themselves.

## GRANDMA NOTE

It's like the doctor's office not giving you the test results over the phone — you can call ten times, or you can walk in and look at the chart yourself. Walking in (fetching the exact code and running the test yourself) is free and always works. And saying "I don't know yet, but here's how I'll find out" is always better than pretending you know.

## NAYA NOTE

Apply this every time a CI failure's job logs are unreachable (sign-in wall, API workflow-level-only): (1) declare PROVEN-UNKNOWN on the record — name exactly what is unknown and which routes were exhausted (API + browser), so no one else burns ticks re-probing the same wall; (2) name the cheapest conclusive route: `git fetch` the exact PR head (protocol, zero REST), pin the SHA, run the EXACT CI command locally, verify the head didn't move during the run; (3) attribute every failure against the tip baseline (branch-introduced vs pre-existing) — here: 5/5 attributed, zero ambiguity left; (4) note that the local repro doubles as the environment-confounds check (SN-0960's full /tmp surfaced in this same repro) — if the local run shows patternless mass failures, check disk before diagnosing; (5) do NOT spend CI minutes re-running a red check to "see the logs" — a rerun of the same unreachable logs costs money and answers nothing.

## MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "unreachable_ci_logs_closed_by_local_repro_at_exact_pinned_head",
  "evidence": {
    "route_exhaustion": "receipts/t0042-browser-1825-log.md (score 6) — failing test names PROVEN-UNKNOWN via both API (t0042-c) and ~10 timed-out browser attempts; wall established as repo log access, not tooling",
    "closure": "receipts/t0052-a.md (score 8) — local repro at exact pinned head 9a9954bc8886 (head verified unmoved during run): 5 failed / 1051 passed / 11 skipped, exit 1; all 5 failures exactly attributed",
    "attribution": "324 unregistered CANDIDATE notes trip the drift guard 1->324 and drop the SN-0632..SN-0959 guards; 3 stale SN-0359 artifacts vanish on rebase",
    "morning_flag": "night-shift-2026-10-10/morning-flags.md #9 — 'the overnight unknown is closed'"
  },
  "rule": "when_ci_logs_are_walled_declare_proven_unknown_then_repro_locally_at_exact_pinned_head",
  "procedure": [
    "declare PROVEN-UNKNOWN on the record: name exactly what is unknown and which routes were exhausted — never guess, never re-probe the same wall silently",
    "fetch the exact PR head over the git protocol (zero REST), pin the SHA, verify it did not move during the run (SN-0493)",
    "run the EXACT CI command locally (read it from the workflow YAML, not from memory)",
    "attribute every failure against the tip baseline: branch-introduced vs pre-existing",
    "do not re-run CI to see unreachable logs — costs minutes, answers nothing"
  ],
  "related": ["SN-0894 (CI failure classification — the route when you CAN see enough to classify)", "SN-0958 (prove the wire on the proven head — same pin-exact discipline)", "SN-0960 (full /tmp phantom failures — surfaced by this same repro technique)", "SN-0961 (duplicate-basename crash — closed by this same technique on #2299)"]
}
~~~
