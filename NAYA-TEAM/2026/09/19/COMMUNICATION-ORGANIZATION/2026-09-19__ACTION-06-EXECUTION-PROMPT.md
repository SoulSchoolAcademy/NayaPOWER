# ACTION 06 — SMART LIST + SMART MAIL RELATIONSHIP BINDING

## MISSION

Make Smart List a true organization projection over canonical identity/Connection state and make Smart Mail re-evaluate relationship eligibility at send time without replacing the existing authority-grant boundary.

## EXECUTION

1. Inventory live tables/functions/indexes/RLS matching List, Favorite, Saved, Collection, Group and person organization.
2. Inspect all available GitHub source/spec references.
3. Reconcile any existing List primitive before creating storage.
4. If absent, create the smallest owner-scoped List + List-member model.
5. List membership must reference canonical member/Connection identity and must not copy profile data.
6. Add/remove must be idempotent and reload-persistent.
7. Removing a List entry must not revoke the underlying Connection.
8. Inspect `nayanet-smart-mail` v12 and `nayanet_send_smart_mail_authorized`.
9. Define the exact relationship eligibility predicate.
10. Enforce that predicate server-side at send time.
11. Keep `nayanet_validate_authority_grant` mandatory.
12. Test relationship denial and authority denial separately.
13. Test replay/idempotency.
14. Record all evidence in Team Naya.
15. Update Smart List, Smart Mail, Job 04 and the master directive.

## HARD RULES

No Hub redesign. No authority bypass. No duplicate identity. No UI-only authorization. No claim of verified Mail until the relationship gate is proven.

## REQUIRED REPORT

DONE / PROOF / NOT PROVEN / DECISION / BLOCKERS / NEXT.

NEXT must be a complete cold-start successor directive.
