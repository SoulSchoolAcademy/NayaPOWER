# NAYA NOTE — P1 CANONICAL WRITE COVERAGE

**Status:** VERIFIED
**Project:** `PRJ-NAYAPOWER-SUPERBRAIN`
**Verified main:** `9aefe57a71bd6425681bb435d70417ad33832198`
**Authoritative Gate:** run `32909426069`, job `98000403862`
**Protected GREEN:** `0f82325a82ed37b5b3a3d097599025369c03a1ed`

## What was learned
The first universal canonical-write pass should not start by migrating code blindly. The correct first move is a machine-readable inventory that distinguishes real event writers from derived/audit producers and deliberately refuses to call an ambiguous case canonical.

The repository audit scans production Python under `.naya/memory` and `.naya/runtime`. The authoritative gate observed 7 relevant findings: A/canonical=1, B/safe migration=0, C/adapter=0, D/derived/audit=6, E/unresolved=0, detected bypasses=0.

The real canonical event-producing caller found was `.naya/memory/emit_daily_intelligence.py`, which imports and invokes `create_or_replay` from the canonical event store. The six D findings are derived/audit producers, not canonical event writers.

## Important boundary
A GREEN static audit is **not** proof of semantic universal adoption. The audit is intentionally conservative but can still miss dynamic or indirect persistence paths. Therefore the system must strengthen detection before claiming the entire production architecture is universally canonical.

## Reusable engineering lesson
**Inventory → classify → prove → migrate → enforce.**
Never infer universal adoption from a partial search. A deliberate direct event-write fixture must fail, and the authoritative gate must observe the guard.

A second lesson was proven by the follow-up gate: the human-readable Next Execution is also a machine interface. Changing its canonical headings broke the contract parser; restoring the exact machine-recognized headings repaired the system without weakening the validator.

## Evidence
The authoritative main gate completed every substantive step GREEN on the exact current main SHA, including fresh-checkout restoration, canonical memory, duplicate/entity audit, relationship graph, regression, continuity, PROJECT/Next Execution/paired representations/learning, Prompt Architect, intelligence, derived index, retrieval baseline, health, Daily CIS, continuity receipt, and artifact upload.

## Next
Harden the coverage audit against dynamic/indirect writers and explicitly enumerate production event-producing semantics. Only migrate callers if a real B/C/E case is discovered.
