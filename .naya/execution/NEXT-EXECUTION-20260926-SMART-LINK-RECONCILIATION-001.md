# 🔱 NEXT P0 — SMART-LINK-RECONCILIATION-001

## MISSION
Reconcile the existing live generic Smart Link implementation and both existing Smart Link machine schemas against the newer canonical narrow Smart Link law.

## PROVEN CURRENT TRUTH
- `.naya/runtime/smart_ledger_engine.py` has a live `generate_smart_link(target_type,...)` function accepting `smart_note`, `ledger_event`, `value_event`, and `collective_intelligence`.
- `.naya/runtime/smart_ledger_engine.py:192` emits a `ledger_event` Smart Link in the vertical slice.
- `.naya/runtime/test_smart_ledger_engine.py` explicitly tests `ledger_event` Smart Links.
- `.naya/contracts/SMART-LINK-CONTRACT.json` is the primary broad machine schema.
- `.naya/contracts/schemas/SMART-LINK-CONTRACT.json` is a second, independently-shaped Smart Link schema and adds `verification_receipt`.
- `.naya/control-plane/RELATIONSHIP-INDEX.json` references both.
- Newer canonical Smart Link law defines Smart Link narrowly around the canonical Smart Note link.

## REQUIRED RECONCILIATION
1. Inspect callers and historical introduction of `generate_smart_link`.
2. Determine which outputs are true Smart Links versus merely generic references/projections.
3. Establish one canonical machine owner and one semantic owner.
4. Decide the disposition of the existing generic runtime function: retire, re-scope, or explicitly rename/classify it without inventing a second Smart Link concept.
5. Decide the disposition of `.naya/contracts/schemas/SMART-LINK-CONTRACT.json`: canonical, supporting schema, historical, or merge candidate.
6. Preserve dedicated Ledger Event and Value Event nouns/schemas.
7. Do not silently break live tests or vertical-slice behavior.
8. Do not create a replacement Smart Link contract.
9. Do not touch constitutional authority.

## ACCEPTANCE
- Every existing Smart Link implementation/schema has one explicit owner/disposition.
- No live code remains semantically mislabeled as Smart Link without a deliberate compatibility decision.
- No duplicate canonical Smart Link schema remains unexplained.
- A migration, retirement, or compatibility path is evidenced before deleting/changing live behavior.
- Affected tests are updated and executed where runtime permits.
- Registry/topology/receipt records what changed, evidence, truth status, remaining holes, and exactly one successor.

## STOP
If a migration would alter externally relied-on behavior without sufficient evidence, stop that mutation and record UNKNOWN/BLOCKED while continuing any safe dependency mapping.

## CONTINUITY
BLOCKS = one next action; EP-001 = execution rules; BATON = continuation projection. Issue #554 is communication only.
