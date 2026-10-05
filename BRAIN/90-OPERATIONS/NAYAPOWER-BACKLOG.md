# NayaPOWER Shared Backlog

> **The single shared to-do / ideas list for all Naya seats** (Naya 1, Naya 2, Naya 3, Naya 4, Codex).
> Anything we plan to add, any idea worth considering, any concept under evaluation lives here —
> in one place, visible to every seat, with a clear status.

## How to add items

1. Open a PR that edits **this file** (never edit on `main` directly).
2. Add the item under the right section with the one-line format below.
3. A seat owner moves items through the lifecycle by PR.

## Status lifecycle

```
IDEA → CONSIDERING → QUEUED → IN-PROGRESS → DONE / DROPPED
```

| Status       | Meaning                                              |
|--------------|------------------------------------------------------|
| IDEA         | Raw concept. Not evaluated yet.                      |
| CONSIDERING  | Under active evaluation. Has an owner asking questions. |
| QUEUED       | Accepted. Ready to build when a lane picks it up.    |
| IN-PROGRESS  | A lane is actively building it (link the PR/branch). |
| DONE         | Landed on `main` and verified.                       |
| DROPPED      | Evaluated and deliberately not pursued (record why). |

## Item format

```markdown
- [ ] **Title** — what it is, in one line.
  Why: one line on the value.
  `source: <tag>` · `status: QUEUED`
```

---

## Queued

Ready to build. A lane may claim any item by moving it to IN-PROGRESS with a branch/PR link.

- [ ] **Disjoint held-out audit for promoted learning** — prove promoted intelligence generalizes, not memorizes.
  Why: honest anti-contamination discipline; gains must survive benchmark-disjoint evaluation.
  `source: rsi-scorecard-2026-10-05` · `status: QUEUED`

- [ ] **Formal verification contracts (SEVerA-style)** — first-order-logic I/O contracts with rejection sampler + verified fallback.
  Why: mathematical proof of zero violations beats empirical proof alone; the highest verification bar found.
  `source: rsi-scorecard-2026-10-05` · `status: QUEUED`

- [ ] **Retrieval-time hash re-verification** — re-check content hash at every retrieval against the capture hash (Merkle ledger).
  Why: closes the tamper-evidence loop; we hash at capture, now prove bytes are identical at use.
  `source: rsi-scorecard-2026-10-05` · `status: QUEUED`

- [ ] **Noise bands + cost-aware acceptance gates** — replace binary pass/fail promotion with noise-aware confidence and cost budgets.
  Why: fewer false passes, fewer false rejections; promotion decisions become statistically honest.
  `source: rsi-scorecard-2026-10-05` · `status: QUEUED`

- [ ] **Contrastive fault localization for repairs** — pair successful/failed trajectories, attribute recurring defects to one bounded module, evolve only that module.
  Why: repairs hit the exact broken component — faster, smaller, safer fixes.
  `source: rsi-scorecard-2026-10-05` · `status: QUEUED`

- [ ] **Canonical discovery/trajectory tree receipts** — every important experiment retains decision points, branches, actions, observations, costs, evaluator results, failures, and provenance.
  Why: the raw material Dream-style replay needs; no replay without retained trees.
  `source: naya3-rsi-analysis-2026-10-05` · `status: QUEUED`

- [ ] **Dream-style offline replay worlds** — turn historical discovery trees into cheap replay simulators; evaluate candidate exploration policies offline at near-zero cost before spending real online calls. Must stay off the live request path.
  Why: Dream-RSI's best idea; tests new ideas against history for free before risking real execution.
  `source: naya3-rsi-analysis-2026-10-05` · `status: QUEUED`

- [ ] **Candidate archive + shadow/canary promotion with auto-rollback** — keep diverse promising candidates (preserve stepping stones); promote winners through replay → test → independent verification → shadow/canary → production, with automatic rollback on degradation.
  Why: never lose a good idea; promotions self-heal if they degrade.
  `source: naya3-rsi-analysis-2026-10-05` · `status: QUEUED`

---

## Considering

Under evaluation. Has an open question or a gate before it can be queued.

- [ ] **Production parity promotion (a3ce52dc)** — promote exact current main through the governed production path.
  Why: the first real RED; everything downstream (graph proof, compounding proof) waits on it.
  `source: naya1-briefing-2026-10-05` · `status: CONSIDERING` · `gate: Shawn's explicit word`

- [ ] **Hub rooms completion** — finish the canonical Hub application (11 rooms) and close the deployed-surface gap.
  Why: the brain is ahead of the deployed organism; the cockpit must catch up after proof closure.
  `source: naya1-briefing-2026-10-05` · `status: CONSIDERING`

- [ ] **Ask Naya v9 real-phone test** — PR #1453 stays HOLD pending Shawn's real-phone test.
  Why: Scorecard Law said don't merge before the test; the test is the gate.
  `source: scorecard-law-2026-10-05` · `status: CONSIDERING` · `gate: real-phone test`

- [ ] **PowerCast deployment** — v5.16 candidate; deploy when the proof lane clears.
  Why: finished work waiting on the brain-proof priority, not on readiness.
  `source: lane-status-2026-10-05` · `status: CONSIDERING`

---

## Ideas

Raw concepts. Not evaluated. Add freely; promote to Considering with a PR when there's a real question to answer.

- [ ] **EVOLVE/DREAM Governed Experiment Campaign V1** — one bounded campaign contract combining NayaPOWER governance + Dream replay efficiency + ModularRSI contrastive attribution + AlphaEvolve/DGM candidate diversity. Not a new subsystem; a laboratory inside the brain.
  Why: Naya 3's recommended next major architectural enhancement after production parity.
  `source: naya3-rsi-analysis-2026-10-05` · `status: IDEA`

- [ ] **Negative-transfer refusal proof** — demonstrate the brain refusing to apply intelligence where it doesn't belong.
  Why: retrieval without refusal is not intelligence; phase 4 of the 10/10 path.
  `source: naya1-briefing-2026-10-05` · `status: IDEA`

- [ ] **Authority non-inheritance proof** — cold successor inherits knowledge but never authority.
  Why: one of NayaPOWER's defining properties; phase 5 of the 10/10 path.
  `source: naya1-briefing-2026-10-05` · `status: IDEA`

- [ ] **Durable human-value measurement** — measure fewer errors, less rework, faster correct decisions, lower cognitive burden.
  Why: graduation from technically intelligent to actually valuable; phase 6 of the 10/10 path.
  `source: naya1-briefing-2026-10-05` · `status: IDEA`

---

## Done

Landed and verified. Newest first.

- [x] **Shared backlog + automated activity feed created** — this file and the 15-min activity feed publisher.
  `source: shawn-directive-2026-10-05` · `status: DONE` · `2026-10-05`
