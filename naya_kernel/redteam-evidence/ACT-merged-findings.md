# ACT — Merged Spec Red-Team Findings (Naya 4, 2026-09-30 20:18 PDT tick)

**Target:** `~/workspace/nine-node-specs/ACT-NODE-SPEC-CANDIDATE.md` (merged 20:14 PDT, 22,463 bytes)
**Method:** full read, read-only. Checked: internal contradictions, carry-forward
integrity (Appendix C claims vs body), GAP-A coverage, contract-law, evidence floors.
**Status:** all OPEN — merge is not final; these route to the finalizing pass.

## MAJOR

### M01 — §0.1 phantom reference: the 13-function binding table is missing (F01 carry-forward broken)
- **Severity:** MAJOR. **Status:** OPEN.
- **Evidence:** Appendix A line 318 ("master-contract 13-function binding (§0.1)"),
  Appendix B #3 line 336 ("never the verb (§0.1)"), Appendix C/F01 line 351
  ("COVERED — §0.1 (13-function binding)") all cite §0.1. The body has no §0.1:
  `## 0. Purpose` contains only the purpose paragraph + "The deepest invariant".
  `grep -i "plan_action\|select_minimum"` → 0 hits; "13-function" → 2 hits, both
  in appendices. The means-vs-verb *rule* is stated (App. B #3), but the binding
  *table* — the actual evidence that the 13 master functions are bound, which was
  the entire substance of draft-F01's fix — is absent.
- **Fix:** restore the 13-function master-binding table as §0.1 (or repoint the
  three references to wherever the table lives).

### M02 — decision_lineage_id + traversal_count phantom: F07's enforceability mechanism not in the schema
- **Severity:** MAJOR. **Status:** OPEN.
- **Evidence:** Appendix C/F07 lines 370–371: "`decision_lineage_id` +
  `traversal_count` are carried on the DecisionReceipt input and the
  ExecutionReceipt". Body: `grep -n "decision_lineage_id"` → 1 hit (line 370,
  the appendix itself); `traversal_count` → same. §6's ExecutionReceipt schema
  lists receipt_id … timestamp with no lineage fields; §1's DecisionReceipt
  field list has no lineage field either. Consequence: §2's READ_MORE k-bound
  ("at most k traversals per decision lineage") is unenforceable as specified —
  exactly the defect draft-F07 was raised to fix.
- **Fix:** add both fields to the §1 DecisionReceipt input list and the §6
  ExecutionReceipt schema; state the LAW-intake enforcement point in §2.

## MODERATE

### M03 — §10 Q10 phantom: F10's OPEN predicate-language question dropped
- **Severity:** MODERATE. **Status:** OPEN.
- **Evidence:** Appendix C/F10 line 379: "OPEN — added as §10 Q10: name the
  deterministic predicate language over the fixed context schema." §10 lists
  Q1–Q8 + Q9 only (`grep -n "Q10"` → 1 hit, the appendix). An explicitly OPEN
  finding vanished between appendix and body — not parked, not answered, just gone.
- **Fix:** add Q10 to §10 as stated.

### M04 — half-open probe has no authority basis (§7 circuit breaker vs §1 initiative ban)
- **Severity:** MODERATE. **Status:** OPEN.
- **Evidence:** §1: "ACT never executes from … its own initiative." §7: "half-open
  probe re-closes on success" — a probe is an execution (tool invocation with
  effects) initiated by ACT's breaker machinery, not by a fresh LAW receipt.
  Under whose authority does the probe run? Not named. If the probe rides the
  original decision's receipt, say so and bound its scope; if it needs a fresh
  LAW decision, say that.
- **Fix:** name the probe's authority basis in §7 (or route probes through ASK).

## MINOR

### M05 — §5 key formula stated as definition, not illustrative (F03)
- **Severity:** MINOR. **Status:** OPEN.
- **Evidence:** Appendix C/F03: "Key format is illustrative." §5 body:
  "`idempotency_key = \"act:\" + hex(hash(...))`" presented as the derivation
  with no illustrative qualifier. A builder reading §5 alone would treat the
  format as normative.
- **Fix:** tag the formula "illustrative" in §5; keep the normative part
  (uniqueness scope + conflict semantics) as the contract.

### M06 — F08 ticket-VIEW semantics live only in the appendix
- **Severity:** MINOR. **Status:** OPEN.
- **Evidence:** Appendix C/F08: "coalesced losers receive a ticket VIEW with
  `cancel_handle: null`; cancel authority stays with the claim owner (§5)."
  §5 body says only "loser coalesces to the winner's ticket (live lease)" —
  the view/null-handle semantics (the actual fix) are not in §5.
- **Fix:** one sentence in §5.

### M07 — ACT node ownership/staffing unnamed (GAP-A ownership thin)
- **Severity:** MINOR. **Status:** OPEN.
- **Evidence:** GAP-A check: responsibility (§1), sync/async (§2/§7), persisted
  transitions (§5–§7), evidence (§6), authority (§3/§4), failure propagation
  (§7), cold reconstruction (§8) all present. Ownership: "The registry is
  governance-owned" (§3) covers the registry, not ACT itself — no named
  owner/principal accountable for ACT's operation, no staffing rule.
- **Fix:** name the accountable owner (or park as an open question).

## Explicitly checked — no finding
- **Contract law:** no silent extensions. The `execution` ledger stream is openly
  proposed (§6 "proposed stream — draft §10 Q6"); PRODUCES is a ratified V2 edge
  type (§1.2); blast-radius/reversibility enums are ACT-internal taxonomies, not
  graph-contract writes. §11's "does not change … any contract" stands.
- **V2.1 lineage:** Appendix B #1 resolves the draft's self-contradiction
  consistently with the live-main verification (20:08 tick: binding in main via
  #1186/#1190/#1192; spec doc #1182 CANDIDATE).
- **Receipt/proof separation:** §6 "Receipt ≠ proof of success" (PDF §54) intact.
- **Pipeline handoff:** Appendix B #2 resolves PDF §67 → canonical ACT→KNOW.
- **Cold reconstruction:** §8 deterministic recovery plan; ASK_SUSPENDED survives.
- **Evidence floors:** N/A — no statistical claims; k=3 default labeled candidate.

## Score
**Merged ACT: 7.5/10.** Genuine full spec; PDF machinery (doors, binding,
golden tests, blast radius, INFLUENTIAL/VERIFIED/PRODUCTION-PROVEN) is real
value over the draft. Debits: M01+M02 (carry-forward integrity — the merge
asserts coverage its body doesn't contain), M03 (dropped OPEN question),
M04 (probe authority), minors. Rises to ~8.5 once M01–M04 are fixed.
