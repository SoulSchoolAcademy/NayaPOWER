# PROTOCOL UNIFICATION — Merge Decisions
## naya5/protocol-unified · 2026-10-08

### What was merged

**Source 1: naya5/protocol-machine-law** (a3458903)
- protocol_manifest.json (7 laws, 5 gates, 6 truth states, 18 prohibitions)
- cold_start_gate.py (6-check boot verification)
- tests/test_protocol_machine_law.py (11 tests)
- Status: SUPERSEDED — all content preserved in the unified branch

**Source 2: naya5/protocol-law-checks** (71205d3c)
- Everything from Source 1, PLUS:
- tools/protocol/checks/ (5 executable law checks: tip_freshness, quality_gate, decision_log, scorecard, action_log)
- tests/test_protocol_law_checks.py (34 tests)
- Status: BASE — the unified branch is built on this (superset)

**Source 3: Naya 3's prototype** (not locatable)
- Described as: JSON contract, Python validator, 13 tests
- Status: PENDING — not found in #1354 comments (searched pages 11-13). When located, reconcile into this branch. The manifest structure is designed to accommodate additional validators.

### What was taken from each

From machine-law: The manifest structure, cold-start gate design, "readiness not authority" principle.
From law-checks: All 5 executable checks, both test suites, the checks/__init__.py shared pattern.
From Naya 3 (pending): To be integrated when prototype is located.

### What was dropped and why

- Nothing dropped from the Naya 5 branches. law-checks was already a superset of machine-law.
- The machine-law branch remains for history but is superseded.
- No competing implementations remain in the Naya 5 lane.

### Test results

- Cold-start gate: 6/6 PASS
- Manifest validation: 7 laws (unique IDs), 5 gates (Shawn's word required), 6 truth states (distinct rules), 18 prohibitions
- Law checks: 5 modules import cleanly
- Test suites: test_protocol_machine_law.py (11 tests) + test_protocol_law_checks.py (34 tests) = 45 tests

### Single source of truth

**Branch naya5/protocol-unified is the ONE machine-law implementation.**

All future protocol-as-code work builds on this branch. No competing branches.
When Naya 3's prototype is located, it merges HERE — not as a separate branch.
