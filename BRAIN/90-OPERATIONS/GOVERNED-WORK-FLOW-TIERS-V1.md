# High-Performance Governed Work Flow — v1

**Owner:** Shawn Vibert, Human Director  
**Status:** implementation proposal; not yet canonical  
**Baseline:** `main` at `576b67aafd7f7eea2bf393c7f15f334fbca4950f` (2026-10-21)  
**Purpose:** preserve protection while removing avoidable paperwork friction and keeping work flowing.

## Executive decision

Use blast-radius tiers, not one uniform ceremony for every change. Automated tests and specification checks remain responsible for checking the work itself. Paperwork gates check only the evidence/independence contract and must be fast, legible, and proportionate.

**Hard boundary:** this change does not directly alter branch-protection / ruleset Required-check settings. That is the Human Director's governor action. The candidate unified gate must be tested and proven first; only then present the exact before/after Required-check names for Shawn's one settings change. Never disable protection early.

## Three tiers

### Tier A — high consequence; full strength
Examples: governance and law, authority/security/privacy, CI/workflow files, gate machinery, production deploy paths, database migrations/production data, mass deletion or destructive transforms, irreversible behavior, and changes that alter what another gate accepts.

Requirements:
- Relevant functional/spec/security tests pass.
- A different seat's independent scorecard is pinned to the exact current head SHA and is at least 9.5/10 (AAA), with honest gaps stated.
- Evidence links resolve and state what they prove.
- Independent review and all required protocol gates pass.
- Runtime/production proof is required when the change claims production behavior.
- Any new commit invalidates head-bound evidence and requires re-score/re-verify. Unrelated changes should not silently invalidate a scorecard if the scored diff and its dependency context are unchanged; the gate must make this decision explicit and auditable, never silently reuse a stale pin.

### Tier B — ordinary work; one paperwork gate
Examples: ordinary application behavior, non-security bug fixes, non-governance documentation, and bounded features.

Requirements:
- Functional tests and relevant specification checks still run; they inspect the work.
- One unified evidence gate checks both: (a) a different seat's scorecard for the exact current head, and (b) evidence links that actually resolve.
- The unified gate emits one actionable verdict and one remediation path. It does not require two separate paperwork check names to express the same missing receipt/evidence problem.
- Review and substantive required checks remain independent; combining paperwork does not weaken code correctness or authorization.

### Tier C — mechanical content; use the content door
Examples: Smart Note filings, note captures, index regeneration, and pure data-only changes whose accepted write path already validates them.

Requirements:
- Do not route note filings through a mega-PR merely to satisfy code-merge paperwork.
- Use the canonical Smart Note/content sync path, which must validate schema, identity/collision, provenance, and generated projections.
- Machine-generated indexes must pass their determinism/freshness checks.
- Spot-verify after landing and record the sample, coverage, and result.
- No scorecard ceremony for a pure mechanical filing. If a content change also changes law, code, a workflow, security, or destructive behavior, it is not Tier C; classify it at the higher tier.
- The content door must be the only supported road for routine note filings; do not invent a second competing note write path.

## Classification rules

Classification is based on the full changed-file set and risk, not title alone. Highest-risk match wins:
1. Tier A if any changed path or semantic purpose touches governance/law/authority, security/privacy, workflow/CI/gate code, production deployment, migrations, permissions, deletion at scale, or gate acceptance behavior.
2. Tier C only if every changed artifact is a recognized mechanical content/data/index artifact and no Tier A or ordinary executable behavior is present.
3. Tier B otherwise.
4. Unknown path/purpose or ambiguous mixed changes are escalated to Tier A until reviewed. The classifier may recommend a tier, but cannot authorize a protected action.

## One unified paperwork gate

The candidate gate must:
- Read the current PR body, current head SHA, PR author seat, changed paths, review/scorecard comments, and evidence URLs from live GitHub state.
- Validate the different-seat rule and exact-head binding using the same canonical matcher as the existing consensus gate; no duplicated regex implementation.
- Validate evidence links with bounded timeouts, clear status, and safe handling of redirects/HEAD-rejecting hosts.
- Enforce the Tier A score threshold; do not infer a score from prose unrelated to the reviewed SHA.
- Return a single machine-readable verdict plus a plain-language summary:
  - `PASS`
  - `BLOCKED — SCORECARD_MISSING`
  - `BLOCKED — WRONG_SEAT`
  - `BLOCKED — STALE_HEAD`
  - `BLOCKED — SCORE_BELOW_TIER_A_THRESHOLD`
  - `BLOCKED — EVIDENCE_MISSING`
  - `BLOCKED — EVIDENCE_UNRESOLVED`
  - `BLOCKED — AMBIGUOUS_TIER`
  - `ERROR — VERIFICATION_UNAVAILABLE`
- Every blocked verdict must include the exact missing fact and one action that cures it. Network/API outage must say verification unavailable, not mislabel the work as low quality.
- Keep substantive tests, security scans, schema checks, and spec checks separate. A green paperwork gate is not a quality verdict.

## Stale scorecards and changed commits

A scorecard binds to the exact tree it evaluated. A changed head normally requires a fresh scorecard. To avoid pointless churn for unrelated changes, a future optimization may permit reuse only if:
- the scorecard includes a machine-readable diff fingerprint and dependency scope;
- the changed commit is proven outside that scope;
- the independent verifier reruns the required impact analysis; and
- the resulting reuse decision is recorded against the new head.

Until that optimization exists, exact-head pinning remains strict. Do not pretend the previous SHA equals the new SHA.

## Balance gauge — equalization dial

Measure each gate weekly and per 100 PRs, separated by tier:
- **Friction rate:** paperwork-only blocks / PRs entering that gate.
- **Substance yield:** real defects caught / total gate blocks.
- **Form-tax ratio:** paperwork-only blocks / real defects caught (report undefined if zero defects).
- **Median cure time:** first block to accepted receipt/evidence.
- **Rework count:** number of receipt/body edits per PR.
- **False-block rate:** gate rejects work that satisfies its own stated contract.
- **Escape rate:** independently confirmed defects that passed relevant checks.
- **Flow time:** open to merged, plus time spent waiting on gates.
- **Tier drift:** classifier disagreements and post-merge reclassifications.
- **Content-door health:** accepted/rejected note filings, schema/collision failures, and post-landing spot-check failures.

Targets:
- 100% of failures name one concrete cure.
- Zero accepted stale scorecards.
- Zero security or protected-authority bypasses.
- Reduce duplicate paperwork check failures to zero after migration.
- Reduce median paperwork cure time and form-tax ratio without increasing escape rate.
- Review tiering when paperwork-only blocks exceed real defects caught for two consecutive review windows; adjust thresholds based on counted evidence, not pressure to make red green.

## Rollout sequence

1. Snapshot the current main SHA, open PR list, branch protection/rulesets, workflow names, and check names.
2. Audit every open PR by Tier A/B/C, real blockers, stale/conflicting branches, and whether it belongs on the content door. Mark unknowns as unknown; do not invent check states.
3. Add tests for tier classification, receipt matching, exact-head staleness, link failures, error messages, and tier-specific requirements.
4. Implement the unified gate alongside existing gates. Do not remove the old checks or change Required-check settings yet.
5. Run full protocol and regression checks, adversarial fixtures, and a shadow comparison on the live PR set. Compare both old gates and the unified verdict.
6. Require a distinct-seat scorecard for the gate change itself. Resolve any disagreement before migration.
7. Confirm the new unified check is consistently present and green where expected. Confirm Tier C content-door tests and post-landing spot checks.
8. Present Shawn the exact Required-check change: retain all substantive quality/security checks, replace the two paperwork-only required contexts with the one proven unified context for Tier A/B, and preserve Tier C's machine content checks. Do not perform the governor's click on his behalf.
9. After Shawn changes protection settings, verify the actual ruleset/branch protection state, run a harmless test PR through all three tiers, and confirm no deadlock or bypass.
10. Monitor the equalization dial, publish REACT evidence, and tune only from observed numbers.

## Wider system: GitHub → Supabase → Hub

### GitHub
- One canonical queue and dependency graph; stop creating discretionary PRs while the queue is above its agreed ceiling.
- One task owner, one acceptance contract, one source of truth, and distinct builder/scorer/verifier seats.
- No duplicate implementation or competing calculators.
- Required checks are classified as substantive-quality, security/authority, or paperwork; never conflate them.
- Report stale head, missing evidence, and actual test failure as distinct states.

### Supabase
- Inspect and classify every relevant table, policy, trigger, function, migration, and production path before changing anything.
- Preserve authorization, RLS, tenant boundaries, provenance, idempotency, and rollback.
- Change one table/path at a time: baseline → migration → focused tests → RLS/negative tests → integration verification → rollback check → record → next table.
- No bulk policy weakening. A security control that blocks a legitimate flow is repaired at the narrowest root cause while unauthorized paths remain denied.
- Production dispatch/deploy and credential changes remain protected actions.

### Hub
- Treat Hub as a projection, never the source of truth.
- Every room/action must resolve to a canonical contract and have a real end-to-end behavior, visible state, failure state, and recovery path.
- Separate content ingestion from application deploys: a routine note landing must not trigger an unnecessary full Hub deployment unless the deployed application artifact actually changed.
- Verify one complete user journey per increment; test persistence and readback, not just the UI.
- Measure user-visible completion, latency, failure/retry rate, and stale projection rate.

## Definition of success

This design is successful only when:
- substantive quality checks remain intact;
- Tier A retains full independent proof and risk controls;
- Tier B has one legible paperwork gate instead of two overlapping blockers;
- Tier C content uses its canonical validated door without scorecard ceremony;
- every red has one explicit cure;
- stale evidence cannot pass;
- no protected settings are changed without Shawn;
- the queue becomes smaller through valid completion, not artificial closure;
- GitHub, Supabase, and Hub flow is measured end to end; and
- the balance gauge shows less paperwork friction without a rise in escaped defects.

**No false green. No paperwork deadlock. Maximum responsible flow.**