# ACTION 08 — TWO-USER ADVERSARIAL PRODUCTION PROOF

## MISSION

Prove the real authenticated Communication + Organization lifecycle at the current human-facing runtime.

## REQUIRED ACTORS

- **A:** legitimate authenticated human session.
- **B:** distinct legitimate authenticated human session.
- **C:** unrelated authenticated human for denial testing where available.

## EXACT PROOF

A:
1. authenticate
2. create shared Space
3. observe Space event

B:
4. authenticate
5. discover Space
6. JOIN
7. reload
8. verify membership

A/B:
9. explicitly save each other as Connections
10. verify provenance
11. add Connection to Smart List
12. reload
13. remove from List
14. verify Connection remains
15. establish valid authority
16. send Smart Mail
17. B verifies receipt
18. inspect cognition/Ledger lineage
19. replay identical idempotency key
20. verify no duplicate

Revocation:
21. leave/revoke
22. retry Mail
23. verify server-side relationship denial

C:
24. attempt protected Space/Connection/List/Mail operations
25. verify denial and no private-data leakage

## EVIDENCE

Capture:
- exact authenticated actor IDs without exposing secrets
- timestamps
- deployed route
- source/deployment marker
- Space ID
- membership ID
- Connection ID
- List ID
- message ID
- receipt ID
- cognition event ID
- Ledger event ID
- replay result
- denial/error result
- screenshots or runtime evidence where available

## HARD RULES

No synthetic-user final proof. No database-only substitute. No UI-only success. No authority bypass. No privacy weakening.

## FAILURE LAW

Observed failure → exact boundary → source/runtime truth → root cause → smallest fix → same proof rerun → evidence update.

## REQUIRED REPORT

DONE / PROOF / NOT PROVEN / DECISION / BLOCKERS / NEXT.

NEXT must be a complete cold-start master execution directive.
