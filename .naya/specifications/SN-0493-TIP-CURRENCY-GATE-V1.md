# SN-0493 Tip-Currency Gate — Spec

**Law:** SN-0493 (ratified) — "a decision computed on tip T is inadmissible
after the tip moves; re-verify tip currency at action time."

**Incident:** 2026-10-06 — Naya 2's merge decision for PR #1661 was computed
on a tip that PR #1660 had already moved 3 minutes earlier. Perfect decision,
dead world.

## What this enforces

Before any consequential action (merge, deploy, promotion, grant issuance),
the decision record's `base_tip_sha` is compared against the live tip.
Moved → BLOCK. Missing/malformed base tip → FAIL CLOSED. Unresolvable
live tip → FAIL CLOSED.

## Files

- `scripts/gate-tip-currency.py` — the gate (stdlib only).
- `.naya/specifications/SN-0493-TIP-CURRENCY-GATE-V1.md` — this spec.

## Checks

| ID | Name | Fail mode |
|----|------|-----------|
| T1 | Base tip present, 40-hex | FAIL CLOSED (missing/malformed) |
| T2 | Live tip resolvable | FAIL CLOSED (unresolvable) |
| T3 | base_tip_sha == live tip | BLOCKED (moved; re-verify + re-stamp) |

Base-tip field aliases: `base_tip_sha`, `main_tip_sha`, `decided_on_tip`,
`tip_sha`, `basis_commit`, `verified_main_tip_sha` (also one envelope
level down: `decision.*`, `receipt.*`, `state.*`).

Live-tip resolution order: `--live-tip` override → `git ls-remote` →
local git (`main`/`origin/main`/`HEAD`) → GitHub API (`GITHUB_TOKEN`).

Exit codes: 0 = currency verified, may proceed. 1 = BLOCKED (fail closed).
2 = usage/input error.

## Usage

```bash
# at decision time: stamp the record with the current tip
python3 scripts/gate-tip-currency.py --stamp decision.json

# at action time: verify currency before acting
python3 scripts/gate-tip-currency.py decision.json || exit 1

# falsifier battery
python3 scripts/gate-tip-currency.py --self-test
```

## Relationship to existing gates

- `tools/auto_merge_gate.py` P4/P10 already enforces tip currency for the
  auto-merge path. This gate generalizes SN-0493 to ALL consequential
  actions and to decision records that never pass through the auto-merge
  receipt (issue-comment decisions, grant issuances, promotions, deploys).
- Follows the drift-tripwire pattern: runnable `--check`-style script,
  exit-code contract, CI-suitable, stdlib only.

## Honest limits

- The gate checks that the decision was re-verified against the CURRENT
  tip; it cannot check that the re-verification was THOROUGH. Re-stamping
  without re-reading is a human-discipline gap, not a machine-checkable one.
- Live-tip resolution needs network, git, or a token; with none available
  it fails closed (correct) but blocks legitimate offline work — use
  `--live-tip` explicitly in that case.

## Score

8.5/10 — gate built, self-test 7/7 green, incident replay verified,
fail-closed on all unknowns. −1.5: not yet wired into CI, and re-stamp
discipline is unenforced by machine.
