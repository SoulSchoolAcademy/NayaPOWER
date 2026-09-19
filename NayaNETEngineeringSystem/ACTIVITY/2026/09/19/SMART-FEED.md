# Smart Feed — Activity — 2026-09-19

FEATURE: Smart Feed
STATE: DEFINED — runtime product closure not proven

## CURRENT REPORT
The contract requires Activity, Personal, and Collective streams with authorized retrieval, provenance, pagination, actions, and privacy. Underlying event/intelligence primitives exist, but the complete human-facing Feed contract has not been proven end-to-end.

## TODO
- [ ] Map live Hub Feed source and deployed route.
- [ ] Map canonical activity projection/event source.
- [ ] Map Personal and Collective retrieval.
- [ ] Prove permission filtering before presentation.
- [ ] Prove pagination and duplicate prevention.
- [ ] Prove source drill-down and action persistence.
- [ ] Prove source/build/runtime parity.

## NEXT
Audit the deployed Hub Smart Feed against its three-stream contract and classify each stream REAL, PARTIAL, DEMO, or MISSING with evidence.
