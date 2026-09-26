# 🔱 SMART-LINK-ENFORCEMENT-002 — EXECUTABLE SUCCESSOR BATON

**MISSION:** Mechanically enforce the canonical Smart Link law at the repository boundary.

**NORTH STAR:** Nayas do not lose memory. Intelligence remains provenance-bound, correctly named, retrievable, applicable, verifiable, and inheritable.

## REQUIRED READ ORDER

1. .naya/control-plane/BLOCKS.json
2. .naya/control-plane/BATON.json
3. .naya/control-plane/STATE.json
4. .naya/control-plane/PROOF.json
5. .naya/contracts/CONTRACT-REGISTRY-V1.md
6. .naya/contracts/CONTRACT-TOPOLOGY-RECONCILIATION-V1.md
7. .naya/codex/NAYA-LINK-IDENTITY-AND-EVIDENCE-CONTRACT-V1.md
8. .naya/contracts/SMART-LINK-CONTRACT.json
9. .naya/tests/test_smart_link_identity_contract.py
10. .github/workflows/verify-smart-link-identity.yml

## CURRENT VERIFIED FRONTIER

SMART-LINK-RECONCILIATION-001 is verified for its runtime/schema scope.

Evidence:
- generate_smart_link was re-scoped to generate_reference.
- The vertical slice now exposes reference, not smart_link.
- The canonical machine owner is .naya/contracts/SMART-LINK-CONTRACT.json.
- The duplicate schema is a supporting $ref alias.
- Ledger Event and Value Event remain distinct nouns.
- Runtime compatibility tests: 6/6 PASS.
- Smart Link identity tests: 4 PASS.
- JSON schema files parse successfully.
- Constitutional authority was not changed.

## EXECUTE NOW

1. Inspect the existing Smart Link identity test and workflow.
2. Verify that .naya/contracts/SMART-LINK-CONTRACT.json is actually loaded by the test.
3. Verify the schema rejects:
   - target_type=ledger_event;
   - Hub runtime URLs;
   - GitHub commit/evidence URLs;
   - wrong Smart Note path shapes.
4. Verify the schema accepts a canonical GitHub Smart Note URL.
5. Verify the application-level identity test still rejects wrong-IB URLs.
6. Run the complete affected Smart Link test and the Smart Ledger compatibility test in a clean worktree.
7. Inspect the resulting diff and confirm no second Smart Link contract was created.
8. Confirm no live generate_smart_link implementation/caller remains.
9. Update the canonical registry with the enforcement result.
10. Update topology/receipt evidence.
11. Update BLOCKS so there is exactly one next action.
12. Update BATON with the same single successor.
13. Post [NAYA][UPDATE] to Issue #554.
14. Post [NAYA][SIGN-OUT] only after the durable receipt and exactly one successor exist.

## HARD STOPS

- Do not create another Smart Link contract.
- Do not restore generic target types under the Smart Link noun.
- Do not relabel Hub Deep Links or Evidence Links as Smart Links.
- Do not change constitutional authority.
- Do not delete live behavior without evidence.
- UNKNOWN/BLOCKED is never PASS.
- If CI or an external boundary is unavailable, record the exact blocker and continue every safe independent verification.

## ACCEPTANCE

PASS only when:
- canonical schema is mechanically exercised;
- canonical Smart Note URL passes;
- Hub/runtime/evidence URLs fail;
- wrong target types fail;
- application-level IB identity correspondence remains enforced;
- affected tests pass;
- registry/topology/control-plane evidence is current;
- Issue #554 has UPDATE and SIGN-OUT;
- exactly one executable successor is left.

## CONTINUATION

After verification, do not merely state the next action.

Write the complete next execution prompt into the repository, update BLOCKS/BATON, communicate it on Issue #554, and execute it immediately when authorized.

**YOU ARE IT. EXECUTE → VERIFY → PRESERVE → COMMUNICATE → HANDOFF → CONTINUE.**
