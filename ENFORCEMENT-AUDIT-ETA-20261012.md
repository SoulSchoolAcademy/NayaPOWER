# Enforcement Audit — Decision Engine consolidation (Naya Eta, 2026-10-12 00:13Z)

Mission: post-consolidation enforcement audit (Grand TODO P0).
Shawn 2026-10-11 22:34Z: competing DecisionEngine implementations CONSOLIDATE
into ONE ultimate decision engine.

## Verdict

**Main tip is RED on the one-engine enforcement gate.** The consolidation
build reported "complete" at ~22:43Z exists only as the unmerged branch
`naya5/decision-engine-consolidation` (server tip `8de2ac1659`). It was never
opened as a PR and never merged. The live tip `665098e3f0` still defines TWO
engines, and the machine-law gate that CI runs fails.

**The merge path is proven clean.** Three-way merge of the consolidation
branch onto the live tip: zero conflicts, enforcement check PASS, 182/182
decision tests PASS. Whatever lane takes the merge, the groundwork is verified.

## Receipts (all from source reads, pristine worktrees at exact SHAs)

### 1. Tip re-resolution (SN-0493)
- Dispatcher-confirmed tip at 00:09Z: `665098e3f00c9aa6f63907360b8500891704071c`
- Re-resolved at action time via API
  (`gh-api GET /repos/SoulSchoolAcademy/NayaPOWER/git/refs/heads/main`):
  `665098e3f00c9aa6f63907360b8500891704071c` — MATCH.

### 2. Enforcement check at the live tip: FAIL (exit 1)
Command: `python3 tools/check_no_competing_engine.py`
(command run in pristine worktree at 665098e3f0, 2026-10-12 00:14Z)
```
FAIL: competing decision/scoring engine detected in kernel/:
  kernel/decision_principle.py:218: class DecisionEngine — defines competing engine 'DecisionEngine'
```
Exactly ONE hit; the AST check sees only real definitions (no grep
false-positives). This check is wired into CI:
`.github/workflows/protocol-gates.yml:66`
(`python3 tools/check_no_competing_engine.py --root .`), so main is
currently red on this gate.

### 3. Consolidation branch state
- Branch `naya5/decision-engine-consolidation`, server tip `8de2ac1659`
  (pushed; base `1b6f72defa`, ~9h behind live main).
- No PR exists for it; not an ancestor of main.
- What it does: folds the two-phase architecture (Phase 1 hard-gate
  partition + Phase 2 argmax over admissible only), disqualification-as-
  exclusion, unknown-defers law, consented+mitigated residual risk, honest
  outputs (ACT/ABSTAIN/ASK/REFUSE/READ_MORE) into `kernel/value_calculus.py`
  (`decide()` + `partition_candidates()`); renames the old second engine
  `DecisionEngine` → `PrincipleOracle` (explicit non-authoritative test-role
  oracle).
- Enforcement check on the branch: `OK: one decision engine (kernel/value_calculus.py), one boot path` (exit 0).
- `kernel/value_calculus.py` has NO runtime import of
  `kernel/decision_principle.py` (mentions are docstring/comment only);
  `kernel/decision_principle.py` imports stdlib only
  (`dataclasses`, `typing`, `math`, `random`) — the oracle shares zero code
  with the canonical engine: genuinely independent.
- At the live tip, `kernel/decision_principle.py` is already imported only by
  `tests/test_decision_principle.py` — nothing in production wires it. The
  failure is pure **policy lag**: the written law (AST name check) still sees
  a class named `DecisionEngine`; the consolidation renames it away.

### 4. Test evidence (command + scope; PATH included ~/workspace/bin/python shim)
Main tip (665098e3f0) — 7 decision/calculus files:
```
python3 -m pytest tests/test_decision_principle.py tests/test_value_calculus.py \
  tests/test_decision_discipline.py tests/test_decision_value_smart_ledger_v2_1.py \
  tests/test_act_value_calculus_wiring.py tests/test_worker_learning_decision.py \
  tests/test_value_calculus_graph_binding.py -q
→ 164 passed in 1.07s
```
Consolidation branch (8de2ac1659) — same 7 + `tests/test_decision_consolidation.py`:
```
→ 182 passed in 1.09s
```
Merged tree (conflict-free three-way merge of consolidation onto 665098e3f0,
verified in scratch worktree):
```
→ enforcement check PASS (exit 0); 182 passed in 1.40s
```

### 5. Count correction (D32 anti-cascade)
The consolidation commit message claims "2,110 cross-verification scenarios".
Grounded from source: the committed test suite exercises **210** —
`dp.scenario_battery()` = 10 + `dp.random_scenarios(seed=42/1337, count=100)`
= 200. All 210 agree (`agreed: True`, verified live). No larger battery
exists anywhere in the repo (searched *.py/*.md for "2110"/"2,110"). The
2,110 number has no provenance — use 210.

## What this does NOT claim
- Does NOT claim the consolidation is safe to merge on the builder's word
  alone — merge still needs the delegated-merge conditions (independent
  validation by a different seat, intent + scorecard posted on the team feed,
  no team objection). This audit verified the build and the merge path; it
  is not that validation.
- Does NOT claim the full repo suite is green — scope was the decision
  engine + the one-engine gate, per this lane's mandate.
- Does NOT claim the 2,110→210 correction invalidates the consolidation —
  210 independently agreeing scenarios is itself strong evidence; the issue
  is the number's provenance, not the result.

## Next highest-value move (for the lane that picks it up)
1. Open the PR from `naya5/decision-engine-consolidation` (target: main;
   Naya 4 opens PRs).
2. Different-seat independent validation of the 18 consolidation tests +
   the 210-scenario agreement, fresh eyes on the value_calculus additions.
3. Post intent + scorecard on the team feed (#2154), wait for no-objection.
4. Merge. The rehearsal here proves it lands conflict-free and flips the
   protocol-gates check from FAIL to PASS at the live tip.
