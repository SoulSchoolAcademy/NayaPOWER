# WIRE RECEIPT — directive status-promotion mechanism

**Seat:** Naya 2 · build lane · night shift 2026-10-11
**Stacks on:** PR #2225 (register) → PR #2289 (sync gate). This adds the third piece: the honest flipper.
**Plain words:** the register knew every directive's status but had no honest way to change one. Now it does.

## The gap (why this exists)

The machine-readable directive register (58 directives) is the authority for *what* each directive is,
and the sync gate keeps *references* honest. But the `status` field could only move by hand-editing JSON —
silent, evidence-free, unaudited. Tonight's wire lane named the gap exactly:
"per-directive status promotion (NOT_STARTED→ENFORCED) has no flipping mechanism."
A status that can be hand-edited is a claim, not a fact.

## What was built (one PR, additive only — zero changes to register data)

- **`tools/directive_register_promote.py`** — the promotion authority. The ONLY honest path
  NOT_STARTED → BUILDING → BUILT_AS_CODE → ENFORCED (the register's own taxonomy, one step, never back).
  Skip-level jumps and demotions are refused. Evidence is mandatory per target:
  BUILDING needs the sign-in comment; BUILT_AS_CODE / ENFORCED need the PR + sign-out comment.
  Same-status re-runs are idempotent no-ops. Every promotion appends one JSONL record to
  `BRAIN/01-GOVERNANCE/directive-register-audit.log`
  (directive_id, from, to, evidence_pr, evidence_comment, actor, UTC timestamp,
  sha256 of the pre-write register bytes).
- **`tools/directive_register_status_check.py`** — the CI gate. Every status change between base and HEAD
  must have a matching audit record in the same PR; every audit record must match a real change;
  audit from/to must equal the actual old/new statuses; malformed audit lines fail; an unloadable
  register fails closed. The initial-registration PR (no register at base) is validated, not blocked.
- **`.github/workflows/directive-register-status.yml`** — runs the gate + the test suite on any PR
  touching the register, the audit log, or the mechanism itself.
- **`tools/tests/test_directive_register_promote.py`** — 20 tests, incl. negative controls
  (skip-level, demotion, phantom id, missing/malformed evidence, corrupt register, silent hand-edit,
  orphan audit, audit mismatch, malformed audit line) and a dry-run dogfood test against the live register.

## Proof (build-lane standard)

- 20/20 tests green on the branch (see test run below).
- Negative controls verified: each refusal path returns the documented exit code and writes nothing.
- Dogfood: `promote --id D8 --to BUILDING --dry-run` against the live 58-directive register → clean,
  exit 0, zero writes.
- Fail-closed: corrupt register → exit 2 via the register authority; never a silent pass.

## Failure modes (honest)

- **Register written, audit append failed** → exit 3, and the exact recovery line is printed
  (append it manually, commit both files). The status gate would flag the drift at review time anyway.
- **Evidence existence is format-validated, not network-verified.** The tool checks that the PR number
  and comment id are positive integers; it does not call the GitHub API. Existence is the reviewer's
  job — the audit record links straight to both, one click each. A CI-side existence check was
  deliberately not added (API dependency + rate limits for zero extra honesty: the link IS the proof).
- **Statuses are still stale for tonight's shipped work.** This PR builds the flipper; it does NOT
  batch-promote other seats' directives. D55–D65 (built and mostly wired tonight) stay NOT_STARTED
  in the register until their owning seats promote them through this tool with their own evidence.
  That is the point of the mechanism: the owner asserts, the audit proves, the gate enforces.

## Operating path now protected

The directive register's status lifecycle — trigger: any PR touching
`BRAIN/01-GOVERNANCE/directive-register.json` or the audit log; block: `directive-register-status` red.
Defect class: silent/evidence-free status edits (the stale-status class).

## What this does NOT claim

- Not merged (merge lane / Shawn's triggers own the queue; this stacks on #2289).
- Not a verdict on any directive's completion — the mechanism records claims, seats make them.
- Not a replacement for the sync gate (#2289) — that guards references, this guards statuses.
