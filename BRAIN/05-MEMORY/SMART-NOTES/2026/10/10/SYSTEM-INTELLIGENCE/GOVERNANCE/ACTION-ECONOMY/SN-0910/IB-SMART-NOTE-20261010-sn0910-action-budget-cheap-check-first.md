# SN-0910 — The Action Budget: Resource Discipline Means Single Reader, Cheap-Check-First, Stand-Down

> **CORRECTION (Naya 4, 2026-10-10):** the "~2,500 actions/month ≈ 83/day" figure as a generic action budget is **obsolete**. Shawn's researched correction (2026-10-10) established the ~2,500 figure refers to **GitHub Actions minutes**, not generic tool calls or cron runs. The operational discipline below — single reader, cheap-check-first, stand-down on 403, git protocol preferred — stands unchanged as good resource hygiene regardless of which meter is scarce. The original uncorrected text is preserved below for provenance.

- **Intelligent Block:** IB-SMART-NOTE-20261010-sn0910-action-budget-cheap-check-first
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE (Team Naya operational knowledge)
- **Captured:** 2026-10-10
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
- **Provenance:** Shawn's standing constraint 2026-10-10 (~09:00 PDT): ~2,500 actions/month, ~83/day TOTAL across all workers and jobs. Naya 4's budget-rebuild coordination, #1354 comment 6099520994 (2026-10-10 16:09:57Z).

## IN A NUTSHELL

The team has a hard budget: ~2,500 actions/month ≈ 83/day TOTAL across every worker and scheduled job. Shawn's words: "make every action matter... every thing costs time money attention." The trigger was real: on 2026-10-10 the team burned 5,000 GitHub API calls in one morning and hit the free Muse weekly limit, forcing everything onto paid tokens.

The architecture that makes the budget survivable:

1. **One reader.** The director pass is the SINGLE GitHub reader (every 30m). It writes `shared-state.json` — main tip, comment count, area flags, stand-down flag. Every other worker reads disk, never the API.
2. **Cheap-check-first.** Every worker body starts by reading shared state. If nothing changed since its watermark, the run is complete and it reports nothing. A correct "nothing changed" is a perfect run.
3. **Stand-down on 403.** Any 403 → set `stand_down=true` in shared-state.json (with reason + until-timestamp one hour out), then STOP. Never hammer a closed door. Endpoint-specific permanent blocks (like the #1354 comment cap) are recorded without a global stand-down — judgment, not a reflex.
4. **Cheapest path.** Git protocol (`ls-remote`, `fetch`) for repo state — zero REST quota. REST only for what the protocol cannot do: comments, check runs, merges, PR metadata.
5. **Cadence split.** Watchers fast + cheap (30m, 1–3 calls when quiet); area drivers deep (6h execution runs). Idle ticks cost almost nothing; the waste was per-tick behavior, not tick count.

This design was adopted by both lanes: Naya 2's lanes already run cheap-check-first + stand-down + single reader. The shared-state.json file is the coordination point; every lane honors its `stand_down` flag.

Durable rule: **a finite action budget is not managed by slowing down — it is managed by never re-reading what one reader already read. One writer of shared state, cheap-check-first everywhere, stop on any 403.**

## HUMAN NOTE

It's like a household with a strict electricity budget: you don't dim the lights all day — you wire one meter, teach everyone to check the meter before turning anything on, and kill everything instantly if the grid says stop. Checking the meter costs nothing; flipping every switch to see what's on is what blows the budget. A quiet house with the meter checked is a perfect day.

## CHILD NOTE

You only have a few coins to spend each day, and everything you do costs a coin. So one person reads the important stuff and writes it on the board for everyone — the rest just check the board. If the board says nothing changed, you're done and you saved your coins. And if a door says "stop," you stop — you never keep knocking.

## GRANDMA NOTE

It's plain thrift: when the household budget is fixed, you don't have five people going to the store to check the same price. One person checks, writes it on the kitchen board, and everybody reads the board. If the board says nothing's changed, that's a perfect errand — it cost nothing. And if the store's door is shut, you don't keep rattling it.

## NAYA NOTE

Cold successor: the standing constraint is ~2,500 actions/month (≈83/day) across the whole team. Operationalize it this way: (1) exactly one scheduled reader (the director pass) touches the GitHub API on a fixed cadence and writes `~/workspace/goals/bring-naya-to-life/hidden_files/shared-state.json`; (2) every other worker's first step is reading shared-state.json and comparing against its watermark — no change = run complete, report nothing; (3) on ANY GitHub 403, set `stand_down=true` with reason and a one-hour `stand_down_until_utc`, then exit immediately — never retry, never probe; (4) distinguish permanent endpoint blocks (e.g., the #1354 comment cap) from rate limits: record the former as state (`issue_1354_comments_disabled`), stand down only for the latter; (5) prefer git protocol for all repo state (tips, trees, files, PR heads) — REST only for comments, check runs, merges, PR metadata. Every worker body carries this budget law verbatim.

## MACHINE NOTE
```json
{
  "intelligent_block": "IB-SMART-NOTE-20261010-sn0910-action-budget-cheap-check-first",
  "sn": "SN-0910",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-10",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "GOVERNANCE",
  "subcategory": "ACTION-ECONOMY",
  "lesson_type": "DOCTRINE",
  "evidence": {
    "constraint": "Shawn 2026-10-10 ~09:00 PDT: ~2,500 actions/month, ~83/day TOTAL",
    "trigger": "5,000 GitHub API calls burned in one morning 2026-10-10; free Muse weekly limit 100% used, on paid tokens",
    "design": "#1354 comment 6099520994 (2026-10-10 16:09:57Z) — single reader, cheap-check-first, stand-down, cheapest-path, cadence split",
    "adoption": "Naya 2 lanes confirmed same law, relay comment 6099728568",
    "state": "shared-state.json carries stand_down / stand_down_reason / stand_down_until_utc / issue_1354_comments_disabled"
  },
  "rules": [
    "one reader writes shared-state.json; everyone else reads disk",
    "cheap-check-first: no change since watermark = run complete, report nothing",
    "any 403 -> stand_down=true, stop immediately, never hammer",
    "permanent endpoint blocks are recorded state, not global stand-down",
    "git protocol for repo state (free); REST only for comments/checks/merges"
  ]
}
```
