# Waste Meter — Spec v1 (2026-10-10)

**One sentence:** The waste meter makes invisible AI effort visible, so the team can stop spending it.

## What "waste" means here (the operational definition)

**Waste = any unit of machine or human effort that did not advance a merged, verified outcome.**

Three shapes, in plain words:

1. **Rework** — doing the same unit of work twice. A pull request that needed 9 commits to land did roughly 8 more units of work than a clean one-commit landing. A force-push rewrites history someone may already have reviewed.
2. **Waiting** — work that sits idle. An open PR untouched for days is effort frozen: the author moved on, the reviewer never came, the value never shipped.
3. **Redo** — work that undoes earlier work. A reverted merge means the original effort plus the revert effort both produced nothing. A CI re-run re-spends machine time because the first attempt failed or flaked.

What we do NOT call waste: careful review, honest failed experiments that taught something, or slow work that was genuinely hard. The meter counts events; humans judge whether an event was wasteful. The meter's job is visibility, not verdicts.

## What we meter now (v1 proxies)

Every figure cites its source. Anything we had to guess is labeled **estimate**.

| # | Proxy | Plain words | Source | Honest limit |
|---|-------|-------------|--------|--------------|
| 1 | Commits per merged PR (mean, median, max) | How many tries it took to land each change | PR timeline API (`committed` events) | Counts commits, not their size; a 1-line fix-up and a rewrite both count as 1 |
| 2 | Force-pushes (branch rewrites) | How often history was rewritten mid-review | PR timeline API (`head_ref_force_pushed`) | Can't tell a trivial rebase from a real rewrite |
| 3 | PR cycle time (created → merged, median/mean hours) | How long a change took from "ready to look at" to "landed" | PR list API (`created_at`, `merged_at`) | Includes legitimate review and wait-for-CI time; it's the full loop, not first-green latency |
| 4 | CI re-runs (extra attempts beyond the first) | How many times the machines had to redo a run | Actions runs API (`run_attempt`) | Wall-clock minutes include queue time; labeled as run time, not pure compute |
| 5 | Reverted merges | Changes that got landed and then un-landed | Search API, merged PRs titled "Revert …" | Misses reverts done by direct push; misses partial rollbacks |
| 6 | Stalled PRs (open, untouched > 72h) | Work sitting frozen, waiting on someone | PR list API (`state=open`, `updated_at`) | "Untouched" means no GitHub event; a lane may be working locally |
| 7 | Smart Notes staged per builder-day | Useful output reaching the board per active lane per day | #1354 comments (`since=`), keyword match on staged-note posts | Counts posts, not quality; a quiet lane may be doing deep work |

## What we do NOT meter yet (aspirational — needs instrumentation)

- **Token / compute spend per decision.** The single most valuable number (cost per shipped outcome) has **no data source today**: the GitHub API exposes no token usage, and local agent run logs don't record tokens. Marked as follow-up: needs instrumentation at the agent-runtime layer before it can be real. We will not fake it.
- Human attention minutes (review time, context-switch cost).
- Opportunity cost of stalled work.

## How to read the readout

`python3 tools/waste_meter.py --days 7` prints a plain-words markdown report:

- **In a nutshell** — the one-paragraph story of the week.
- **The numbers** — each proxy with its figure and its source.
- **Where the waste went** — the proxies ranked by wasted events, in plain words.
- **What we can't see yet** — the honest gaps, so nobody mistakes the meter for the whole truth.

Re-run cadence: weekly baseline, posted to #1354 with the raw JSON archived under the goal's `hidden_files/`. Week-over-week deltas are the point — a single week is a snapshot, the trend is the signal.

## Non-goals

- The meter never touches `.github/workflows/`, production, credentials, or anything destructive. Read-only on GitHub except the lane's own branch/PR.
- The meter never scores people. It scores the system's waste so the system can improve.
- No invented numbers. Ever. A missing source is reported as missing, not filled in.
