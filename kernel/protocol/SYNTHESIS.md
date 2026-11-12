# PROTOCOL SYNTHESIS RECORD

## naya5/protocol-synthesis · 2026-10-08

Shawn's directive: "make it ALL official — synthesize the operating protocol, code it
into the machine, document as operational law, update constitution and governance."

### What was synthesized

**Source 1: Naya 4's PR #1807** (naya4/protocol-machine-law-2026-10-08, CLOSED unmerged)
- `BRAIN/01-GOVERNANCE/TEAM-NAYA-OPERATING-PROTOCOL-V1.md` — the three-tongue constitution
  (human law / AI law / machine law). 175 lines. Preserved verbatim.
- `kernel/protocol/` — 8 machine-law modules: read_receipt, cold_start_gate,
  authority_gate, quality_gate, takeover, cold_successor_test, learning_capture,
  minimal_action. Preserved.
- `.github/workflows/protocol-gates.yml` — CI enforcement. Preserved.
- `kernel/protocol/INTEGRATION.md` — how gates plug into existing seams. Preserved.
- Status: ADOPTED AS BASE. This is the canonical protocol document.

**Source 2: Naya 5's protocol branches** (naya5/protocol-machine-law → law-checks → unified → kernel-migration)
- `kernel/protocol/protocol_manifest.json` — 7 ratified laws + 3 new CANDIDATE laws
  (SN-AUTO-BRAIN, SN-NO-EGO, SN-PROACTIVE-DOC), 5 gates, 6 truth states, 18 prohibitions.
- `kernel/protocol/protocol_integrity_gate.py` — 6-check executable verification.
- `kernel/protocol/checks/` — 5 law checks: tip_freshness, decision_log, scorecard,
  action_log, delivery_evidence_gate.
- `kernel/protocol/engineering_gates.py` — 5 elite engineering standards (CANDIDATE).
- `kernel/protocol/pipeline_health.py` — verification pipeline monitor.
- Status: MERGED. `tools/protocol/` removed — superseded, ONE canonical location.

**Source 3: Shawn's 9 protocol PDFs** (workspace/user/files/)
- Review in progress (dedicated agent). Unique high-value clauses will be merged
  into the three-tongue structure. Duplicates discarded.

**Source 4: Naya 2's 5-layer structure**
- Layer 0 (proof-of-reading gate) → `read_receipt.py` + `cold_start_gate.py`
- Layer 1 (two-minute protocol) → distilled into AI Law "Every Work Cycle" (11 steps)
- Layer 2 (full protocol) → the three-tongue document
- Layer 3 (elite craft) → "Elite Standards" section (code/design/output)
- Layer 4 (glossary) → referenced, not duplicated
- Status: STRUCTURE ADOPTED. Her layering informed the document architecture.

**Source 5: Naya 3's integration principle**
- "Integrate into the existing constitutional and activation system. Do not create
  a second constitution."
- Status: ADOPTED AS CONSTRAINT. The protocol plugs into AGENTS.md boot contract,
  NAYA-ACTIVATION chain, and Decision Value Calculus — it replaces none of them.
- Documented in `kernel/protocol/INTEGRATION.md`.

### New in this synthesis

1. **`CONSTITUTION/0003-AUTOMATIC-SUPER-BRAIN-AMENDMENT-V1.md`** (CANDIDATE)
   - Article VII: The Automatic Super Brain
   - Article VIII: No-Ego Optimization (VALUE × INTELLIGENCE)
   - Article IX: Proactive Documentation
   - Article X: The 10/10 Standard
   - Awaiting Shawn's ratification. Does NOT modify ratified text.

2. **Three new candidate laws in the manifest:**
   - SN-AUTO-BRAIN: automatic operation as structural requirement
   - SN-NO-EGO: value × intelligence optimization, math decides
   - SN-PROACTIVE-DOC: document value without being told

3. **Unified `kernel/protocol/`:** 16 modules, one location, no duplicates.

### What was NOT duplicated

- Decision Value Calculus (`kernel/value_calculus.py`) — the one decision engine.
- Activation chain (`NAYA-ACTIVATION/`) — the one boot path.
- Smart Note pipeline — `learning_capture` requires lessons; pipeline untouched.
- Authority definitions — encoded from ratified docs, none created.

### Verification

- Protocol integrity gate: 6/6 PASS
- Manifest tests: 11/11 green
- Machine law tests: 37/37 green
- CI workflow: protocol-gates.yml runs on every PR

### Still pending

- [ ] PDF review: merge unique clauses from Shawn's 9 PDFs
- [ ] Whole-brain review: 10/10 wording/logic audit results
- [ ] Shawn's ratification: constitutional amendment + protocol v1.0
- [ ] Naya 4 to open PR (Naya 5's token 403s on PR ops)
