# PROTOCOL KERNEL MIGRATION
## tools/protocol/ → kernel/protocol/ — 2026-10-08

### Decision
`kernel/protocol/` is the canonical home for machine law. Protocol-as-law is foundational infrastructure, not a utility. All machine-law implementations converge here.

### Sources merged
1. **Naya 4's `naya4/protocol-machine-law-2026-10-08`** (BASE): kernel/protocol/ structure, agent-focused gates, read receipts, takeover rules.
2. **Naya 5's `naya5/protocol-unified`** (MIGRATED IN): protocol manifest, protocol integrity gate, 5 law checks, manifest tests.

### Migration decisions

| Item | Decision | Rationale |
|------|----------|-----------|
| `protocol_manifest.json` | Migrated to `kernel/protocol/` | Single source of truth for laws as data |
| My `cold_start_gate.py` | Renamed to `protocol_integrity_gate.py` | Hers tests the AGENT, mine tests the LAW. Different subjects, clear names. |
| Her `cold_start_gate.py` | Kept as-is | Canonical agent boot gate, integrated with read_receipt |
| Her `quality_gate.py` | Kept as-is | Validates scorecard structure (dataclass) |
| My `checks/quality_gate.py` | Renamed to `checks/delivery_evidence_gate.py` | Validates delivery pipeline (dict-based). Different from hers, no conflict. |
| My 4 other checks | Migrated to `kernel/protocol/checks/` unchanged | tip_freshness, decision_log, scorecard, action_log — no equivalents in hers |
| Tests | Hers kept, mine adapted | Her tests cover her modules. My manifest tests adapted to new paths as `test_protocol_manifest_integrity.py`. |
| `tools/protocol/` | Superseded | Do not use. All content now in `kernel/protocol/`. |

### Name resolution summary
- `cold_start_gate.py` (hers): Tests whether an AGENT can begin work. Requires read receipt, identity, authority knowledge.
- `protocol_integrity_gate.py` (mine, renamed): Tests whether the PROTOCOL is valid. Manifest well-formed, tip resolvable, law IDs unique.
- `quality_gate.py` (hers): Validates SCORECARD structure. Weighted dimensions, 9.0 floor.
- `checks/delivery_evidence_gate.py` (mine, renamed): Validates DELIVERY record. Build + verification evidence present, gates passing.

### Tests
- Her test suite: covers kernel/protocol modules (read_receipt, authority_gate, quality_gate, cold_start, cold_successor, takeover)
- My adapted tests: `test_protocol_manifest_integrity.py` covers manifest + integrity gate at new paths
- No duplicate test coverage. No conflicts.

### What was dropped
Nothing. All content from both implementations preserved. `tools/protocol/` is superseded but its content lives on in `kernel/protocol/`.
