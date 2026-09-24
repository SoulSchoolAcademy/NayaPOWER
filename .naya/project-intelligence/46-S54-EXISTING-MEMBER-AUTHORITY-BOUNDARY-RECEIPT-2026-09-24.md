# System 54 — Existing-Member Authority Boundary Receipt

**Date:** 2026-09-24  
**Status:** BLOCKED  
**Causal boundary:** existing member → authority grant → `intelligence_commit`

## Exact target

- Learning evidence: `1112073e-08ee-407e-a47a-8b65b845f57b`
- Current learning status: `ACTIVE`
- Required action: `intelligence_commit`
- Required proof after authorization: canonical cognition event → intelligence index → provenance → no duplicate destination → receipt/cognition lineage → fresh retrieval.

## What was repaired

- PR #587 merged: `fix(intelligence): bind commit path to authority grants`.
- PR #588 merged: `fix(intelligence): reconcile execution authorization overload`.
- PR #589 merged: `fix(migration): remove UTF-8 BOM`.
- Production migration `wire_authority_grant_into_intelligence_commit_v1` applied successfully.
- Production migration `reconcile_execution_authorization_cognition_overload_v1` applied successfully after the BOM repair.
- `nayanet-compound-intelligence` deployed as version 37 with JWT verification enabled.
- Production inspection confirms the 7-argument `p_execution_authorization` cognition receipt boundary exists and enforces authority, actor, permission, and governance state.
- Focused execution-authorization tests: 3/3 PASS.
- Hub identity regression suite: 15/15 PASS.

## Why execution is blocked

Read-only production inspection found **zero authority grants** for the existing member and therefore zero currently usable grants. The existing candidate cannot truthfully be promoted until a legitimate authenticated owner session issues an in-scope grant.

No owner identity was impersonated. No grant was fabricated. No production Intelligent Block was created merely to make the proof green.

## Success criterion

`legitimate owner session → minimum scoped authority grant → intelligence_commit → canonical event → index → provenance → receipt → fresh retrieval`, independently reconstructed from production evidence.

## Exact verification method

1. Establish the real owner session through the governed identity boundary.
2. Issue the minimum scoped `intelligence_commit` grant.
3. Execute only learning evidence `1112073e-08ee-407e-a47a-8b65b845f57b` through the canonical commit path.
4. Independently query production for the event, index projection, provenance, duplicate destinations, receipt lineage, and fresh owner-scoped retrieval.
5. Record the resulting IDs and outcome before any promotion to VERIFIED/WISDOM.

## Next Naya

Do not retry the candidate until the owner session and valid grant exist. The repository/runtime authority seam is now repaired; the remaining boundary is legitimate owner authorization.
