# OPERATING CODE V2 — MUST TRACKING
*Workstream 2 (Compile the Law, Phase 1) — Operation Flow Like Water, 2026-10-10.*
*Source of truth: `BRAIN/01-GOVERNANCE/0008-OPERATING-CODE-V2.{ai,human}.md` + `0008-operating-code-v2.machine.json` (RATIFIED 2026-10-10 by Shawn).*

## Why this file exists

Every "MUST", "NEVER", "always", "required", "no … without", "no exceptions" in V2 is listed below with its enforcement status. The rule that governs this file: **no phantom enforcement claims survive** — anything that claims mechanical enforcement must point at code and tests, or be flagged.

Statuses:
- **engine-exists** — code + tests enforce it today (named).
- **engine-planned** — no engine yet; the owning workstream is named.
- **relabeled-aspirational** — no engine and none honestly possible; a proposed honest rewording is given. Ratified V2 text is NOT edited here — constitutional text changes need Shawn. Proposed rewordings are listed as proposed amendments at the bottom.

## Canonical spot — why here, not in machine.json

This tracking lives as a standalone `.md` beside the three ratified tongues, deliberately NOT inside `0008-operating-code-v2.machine.json`:
1. `machine.json` is ratified constitutional text. This workstream is forbidden from editing ratified V2 text (amendments need Shawn).
2. Tracking entries are audit evidence with prose justifications — a poor fit for the machine schema, and editing the schema risks breaking its consumers and the encoding audit.
3. The doc-completeness gate treats this as a single-form governance artifact (warning-level, non-blocking); it is evidence, not a law, so it does not take the law triple.

## DOMAIN 1 — DECISION

| # | V2 § | Claim (exact) | Status | Engine / owner / proposal |
|---|------|---------------|--------|--------------------------|
| 1 | 1.1 | "Every significant decision follows five steps. No exceptions. No shortcuts." | engine-exists | `kernel/scorecard_law.py` — `run_scorecard()` executes ENUMERATE→SCORE→GATE→DECIDE→RECEIPT in order; `validate_receipt()` re-derives all five. Tests: `tests/test_scorecard_law.py`. |
| 2 | 1.1 | "List every real option. Not two. All of them." | engine-exists | Structural: ≥2 options, unique non-empty ids (`ENUMERATE_TOO_FEW_OPTIONS`, `ENUMERATE_MISSING_ID`, `ENUMERATE_DUPLICATE_ID`). Honest limit: no engine can know the *real* option space — completeness of enumeration remains seat judgment. |
| 3 | 1.1 | "Score each honestly… Authentic scores only — inflated scores destroy the mechanism." | engine-exists | Structural: all six V2 dimensions, numeric 0–10, every option (`SCORE_MISSING_DIMENSION`, `SCORE_NON_NUMERIC_DIMENSION`, `SCORE_DIMENSION_OUT_OF_RANGE`). Honest limit: the *honesty* of the values is seat judgment — the engine enforces the shape, not the belief. |
| 4 | 1.1 | "A gate failure kills the option regardless of score." | engine-exists | Gates assessed before decide; failures recorded in `killed_by_gate` with the failed gate named (`GATE_FAILED`). Tests prove a 60/60 scorer loses to a gate failure. |
| 5 | 1.1 | "Highest valid score wins. Act without asking." | engine-exists | Max total among gate-passers wins. Honest limit: an exact tie is NO_DECISION (`DECIDE_NO_CLEAR_WINNER`) — uncertainty is decided by more scoring, not a coin flip (V2 §1.2). |
| 6 | 1.1 | "RECEIPT — Written and posted. No receipt, no action." | engine-exists | `build_receipt()` / `validate_receipt()`; `RECEIPT_NOT_POSTED` refuses unposted receipts. The merge gate's P8 refuses any merge without a posted receipt id. |
| 7 | 1.2 | "When unsure what to do, do NOT queue it for Shawn. Run the calculator. The math decides." | relabeled-aspirational | No runtime gate can force a seat to run the engine. Proposed honest wording: "Standing behavioral rule; compliance is verified in activation exams and lane scorecards, not by a runtime gate." |
| 8 | 1.3 | "A score never grants permission. Gates run before scores are read." | engine-exists | Gates are assessed before `decide` runs; `_check_authority()` forces `NEEDS_AUTHORITY` when any human-only gate is attested, regardless of score (`AUTHORITY_HUMAN_ONLY_GATE`). |
| 9 | 1.4 | "Unchanged human-only gates" (constitutional ratification, production dispatch/DB, credentials/money, destructive/irreversible) | engine-exists | `HUMAN_ONLY_GATES` in `kernel/scorecard_law.py`; `PROTECTED_PATH_PREFIXES` + human-only flags in `tools/auto_merge_gate.py`. Tests cover both. |

## DOMAIN 2 — COMMUNICATION

| # | V2 § | Claim (exact) | Status | Engine / owner / proposal |
|---|------|---------------|--------|--------------------------|
| 10 | 2.1 | "Never send jargon without the translation." | engine-planned | Owner: Workstream 8 — gate console (Operation Flow Like Water). Behavioral until the console ships. |
| 11 | 2.2 | "Speak in meaning, not identifiers." | engine-planned | Owner: Workstream 8 — gate console. |
| 12 | 2.3 | "Milestones only… Silence beats a useless send." | engine-planned | Owner: Workstream 8 — gate console. |
| 13 | 2.4 | "Every execution reply ends with the next action." | engine-planned | Owner: Workstream 8 — gate console. |
| 14 | 2.5 | "Never make him hunt." (link + value + 1-2-3 steps) | engine-planned | Owner: Workstream 8 — gate console. |

## DOMAIN 3 — EXECUTION

| # | V2 § | Claim (exact) | Status | Engine / owner / proposal |
|---|------|---------------|--------|--------------------------|
| 15 | 3.1 | Score → holes → fill → re-score → ship. "Three rounds, not two hundred." | engine-exists | `tools/score_fill_ship.py` — `evaluate_shipment()`; `SHIP_ROUNDS_EXCEEDED` fires past 3 rounds without reaching 10. Tests: `tests/test_score_fill_ship.py`. |
| 16 | 3.2 | "Nothing below 9.0 ships. Nothing below 9.0 reaches Shawn." | engine-exists | `SHIP_FLOOR = 9.0`; `SHIP_BELOW_FLOOR` refuses. The "reaches Shawn" send-path half is engine-planned (Workstream 8 — gate console). |
| 17 | 3.3 | "Score the experience, not the code." | engine-exists (partial) | No engine can score lived experience. What IS mechanical: independent verification is enforced (`SHIP_SELF_VERIFIED`). Experience scoring itself is attested by the independent verifier — noted honestly, not claimed as machine-scored. |
| 18 | 3.4 | "Never build a second mechanism for one decision." | relabeled-aspirational | Design discipline. This workstream honored it: the V2 §5.2 gate was built by *extending* `tools/auto_merge_gate.py`, not by writing a second gate. Proposed honest wording: "Design discipline; enforced in code review and lane ownership, not by a runtime gate." |
| 19 | 3.5 | "Smart Apps: solve once, freeze, never rebuild." | engine-planned | Owner: Workstream 9 — first true Smart App (Operation Flow Like Water). |
| 20 | 3.8 | "No one scores their own work. Ever. Verification is independent or it doesn't count." | engine-exists | `SHIP_SELF_VERIFIED` refuses scorer==verifier in `tools/score_fill_ship.py`; merge-gate receipts carry `decided_by` and a posted comment id so an independent seat can re-derive the decision. |

## DOMAIN 4 — LEARNING

| # | V2 § | Claim (exact) | Status | Engine / owner / proposal |
|---|------|---------------|--------|--------------------------|
| 21 | 4.1 | "If it's valuable, it gets captured — always, no asking." | relabeled-aspirational | The capture pipeline (`.naya/capture/`) exists, but "always" cannot be a machine guarantee. Proposed honest wording: "Capture discipline; a lost valuable is the failure, verified in review — 'always' is the standard, not a machine guarantee." |
| 22 | 4.2 | "Every Smart Note and every significant change gets an automatic check: all forms present? All locations covered? If not, flagged and filled immediately." | engine-exists (partial) | `tools/doc_completeness_check.py` + `doc-completeness-gate.yml` run on changed files in CI (forms check). Honest limit: only *changed* files are gated (pre-existing debt is tracked, not blocking); the "all locations" half (repo/doctrine/lessons/checklist/memory) is not fully mechanical — remainder is engine-planned (Workstream 7 — learning loop closure). |
| 23 | 4.3 | "Bake it in… inherited at activation. Zero ramp-up." | engine-planned | Owner: Workstream 6 — cold activation proof (+ activation hardening). |

## DOMAIN 5 — AUTHORITY

| # | V2 § | Claim (exact) | Status | Engine / owner / proposal |
|---|------|---------------|--------|--------------------------|
| 24 | 5.1 | Human-only gates "(never crossed)" — production dispatch/DB, workflows, credentials/money, destructive/irreversible, constitutional ratification, authority/consent/security | engine-exists | `tools/auto_merge_gate.py`: `PROTECTED_PATH_PREFIXES` + five human-only flags, any attested/missing → refused. `kernel/scorecard_law.py`: `HUMAN_ONLY_GATES`. Tests: `tests/test_auto_merge_gate_v2.py`, `tests/test_scorecard_law.py`. |
| 25 | 5.2 | Auto-merge grant: "tests green on live-verified bytes, no conflicts, branch current, intent posted, revertable in one commit, scorecard receipt posted. No receipt, no merge." | engine-exists | `tools/auto_merge_gate.py` — `V2_GRANT_CLAUSES` maps each of the six clauses to enforced preconditions (P1/P2, P3, P4/H2, P5, P7, P8/H1/H4). V2 receipts (engine `SCORECARD-LAW-V2`) validated by `kernel/scorecard_law.validate_receipt` — one receipt mechanism, not two (V2 §7.11). |
| 26 | 5.5 | "Jurisdiction follows the trigger chain… his call before the merge, not after." | engine-exists (partial) | The human-only flags refuse the merge before it happens. Honest limit: tracing a *trigger chain* (which workflow a path change fires) is seat judgment at PR time — noted, not claimed as machine-traced. |

## DOMAIN 7 — DESIGN

| # | V2 § | Claim (exact) | Status | Engine / owner / proposal |
|---|------|---------------|--------|--------------------------|
| 27 | 7.3 | "Decorative effects MUST NOT compete with readable intelligence." | engine-exists (partial) | `design-gate.yml` runs a real gate on every PR (self-test + fixtures, failure propagates). Honest limit: aesthetic judgment remains seat/human — the gate enforces its fixture-verified predicates, not taste. |
| 28 | 7.4 | "You may not replace it with something cleaner-but-generic." | engine-exists (partial) | Same gate, same honest limit. |
| 29 | 7.9 | "Never build from memory and wait for correction." | relabeled-aspirational | Builder discipline. Proposed honest wording: "Spec-first discipline; verified by spec-first receipts in the lane, not by a runtime gate." |
| 30 | 7.10 | "Score the rendered experience… Verify before claiming." | engine-planned | Owner: design-gate extension / Workstream 8 — gate console. |
| 31 | 7.11 | ".md placement… Never workspace-only." | relabeled-aspirational | Placement discipline. Proposed honest wording: "Placement discipline; checked in PR review, not by a runtime gate." |
| 32 | 7.12 | Design 10/10 checklist — "Before any design ships" | engine-planned | Owner: design-gate extension (Workstream 8 — gate console). |

## AMENDMENT PATH + SUPREME LAW

| # | V2 § | Claim (exact) | Status | Engine / owner / proposal |
|---|------|---------------|--------|--------------------------|
| 33 | Amend | "Amendments come through Shawn's authority only." | engine-exists | `tools/amendment_loader.py` (landed on main via PR #2129, Workstream 3) — validates amendment records against the V2 Amendment Path: required fields, structural validity, Shawn's authorization marker; fail closed with named refusal reasons (`MISSING_AUTHORIZATION`, `BAD_AUTHORITY`, `BAD_AUTHORIZATION_REF`, …). Validator only — never amends, never flips ratification status. Tests: `tests/test_amendment_loader.py` (46 green). |
| 34 | §0 | "The Law of One governs everything below… No exceptions." | relabeled-aspirational | Constitutional supremacy principle, not a mechanical rule. No rewording proposed — it reads correctly as a principle. Enforcement is by seat judgment under the Judgment Rule, not by code; no mechanical enforcement is claimed. |

## Open honesty notes (not amendments — facts for the record)

1. **Two canons → unify.** `BRAIN/01-GOVERNANCE/OPERATING-LAW.md` / `.json` (45 laws, claims CANONICAL piece-by-piece ratification) sat beside V2 (7 domains, ratified 2026-10-10). As of 2026-10-10 ~08:09 PDT Shawn ordered DISTILL TO ONE: V2 + 45-law merged into a single canonical operating law (essence kept, duplication dropped, better version wins); Workstream 10 owns the unified text, only Shawn marks RATIFIED. No entry above claims V2 mechanically overrides the 45-law canon in the interim.
2. **Engine coverage after this workstream:** of 34 tracked claims, 18 are engine-exists (11 fully, 7 partial with honest limits named), 9 are engine-planned with named owners, 7 are relabeled-aspirational with proposed honest rewordings. Zero phantom enforcement claims.

## Proposed amendments (for Shawn — NOT applied)

The relabeled-aspirational rows above carry proposed honest rewordings (#7, #18, #21, #29, #31). They are proposals only. Ratified V2 text was not touched by this workstream.
