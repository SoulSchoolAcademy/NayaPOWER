# WIRE RECEIPT — Machine-Readable Directive Register

**Wired:** 2026-10-11 · Naya 2 wire lane · PR: naya2/wire-directive-register (stacked on PR #2225)
**Mechanism:** `BRAIN/01-GOVERNANCE/directive-register.json` — the single machine source of truth
for the 58 master directives D8–D65 (built by PR #2225: JSON + 10 self-tests + self-check CI).
**Status before wiring:** CODE-ONLY — nothing in any operating path consumed the register.

## What was wired

1. `tools/directive_register.py` — the importable authority. Fail-closed loader:
   missing/corrupt/misshapen register, duplicate ids, or missing keys raise
   `DirectiveRegisterError`; unknown-id lookup raises `UnknownDirectiveError`.
   No defaults, no synthesized metadata — a caller that cannot load the register
   must refuse to certify.
2. `tools/directive_register_sync.py` — the sync scanner. Every `D<n>` token in a
   changed governance document must resolve against the register:
   D1–D7 out of scope (meta-governance, excluded per Shawn's scoping);
   D8–D65 must exist in the register; anything above D65 is a violation (register it first).
   Corrupt register → exit 2 (fail-closed), never a silent pass.
3. `.github/workflows/directive-register-sync.yml` — the enforcement gate.

## Operating path now protected

**The PR merge path for governance documents.**
Trigger: any PR changing `BRAIN/01-GOVERNANCE/**` (or the scanner/loader itself).
Block: the `directive-register-sync` check goes red → the PR cannot merge.
This enforces the D35 stale-publication class at the exact point where stale
directive references would enter the tree: a phantom or mistyped directive
number outside the registered set is caught before merge, with a file:line witness.

## Proof the wiring works (2026-10-11, this run)

Local (mechanism):
- Live fire on the real tree: 42 governance docs scanned → 0 violations,
  11 out-of-scope refs (D1–D7), 58 register entries. Clean, honestly reported.
- Negative control: fixture doc referencing an unregistered directive number →
  1 violation naming file:line, exit 1. The scanner blocks.
- Sabotage: missing register → exit 2; malformed register → exit 2 FAIL-CLOSED.
  The gate refuses rather than passing blind.
- Test suite: 24/24 green (`test_directive_register.py` + `test_directive_register_sync.py`),
  including negative controls for corrupt/missing/duplicate register states.

Live path (enforcement) — independently re-verified 2026-10-11 ~06:00Z:
- **Wiring defect found:** both gate workflows shipped with a Python-style
  `"""` docstring above the YAML document — a parse error. Every historical
  run of both workflows concluded failure with zero jobs: the "gate" never
  executed on any PR. Fixed (docstring → comments, verified with
  yaml.safe_load). Second defect: the test steps ran `python3 -m pytest` on a
  bare setup-python image (`No module named pytest`) — added an explicit
  pip install step to both workflows.
- **Gate green on clean tree:** run 38116175188 (Directive Register Sync,
  pull_request) → success; run 38116175184 (Directive Register Check) → success.
- **Gate RED on real violation:** temporary commit citing an unregistered
  directive number (above the D65 ceiling) in
  `BRAIN/01-GOVERNANCE/__WIRE_TEST_VIOLATION__.md` → run 38116336113 failed at
  step "Validate directive references in changed governance docs". Reverted
  immediately after; tree clean.
- Brain-index drift on this branch (REAL-TREE, 12th occurrence class) re-stamped
  at basis f2c614a5 (merge-base with live main 57e935c1); `test` check green.

## How to verify it is still connected

1. Open any PR touching `BRAIN/01-GOVERNANCE/` and add a line referencing an
   unregistered directive number (e.g. one above D65) — the
   `directive-register-sync` check must go red naming the file and line.
2. `python3 tools/directive_register_sync.py --repo . --all` must exit 0 on a
   healthy tree and exit 2 if `directive-register.json` is corrupted.
3. `python3 -c "from tools.directive_register import load_register; load_register()"`
   must return 58 entries; any downstream gate importing this module inherits
   the fail-closed contract.

## Failure mode if the wiring breaks

If the workflow file is deleted or the `paths` filter narrowed, governance PRs
stop being reference-checked: phantom directive numbers can merge silently and
the register decays into a document again. Detection: the receipt's check #1
above goes unanswered (no check run on a governance PR). The scanner and loader
remain usable as library code regardless.

## Remains unwired

- The register's per-directive `status` field (NOT_STARTED → ENFORCED) is still
  honesty-accounting maintained by build lanes; no mechanism yet flips a status
  on verified enforcement (that promotion needs its own wire + evidence rule).
- Downstream gates (D32 scanner, merge-queue fairness scanner) still carry their
  own directive metadata; adopting `tools/directive_register.py` as their source
  is offered, not yet done — a future wire run can take it without duplicating
  this mechanism.
