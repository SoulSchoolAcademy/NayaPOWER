# Team Naya — SECURITY DEFINER Anonymous Execution Hardening

**Date:** 2026-09-19
**Repository:** SoulSchoolAcademy/NayaPOWER
**Observed main HEAD before this record:** ece4963ec9944b98be93b072d5d87691f47ebc38

## WHAT I INSPECTED

Live Supabase security advisors and PostgreSQL function privileges were inspected.

The live SECURITY DEFINER inventory identified four functions callable by `anon`:
- `public.nayanet_index_intelligence_row()`
- `public.v7_create_smart_note(...)` — both overloads
- `public.v7_update_profile_settings(jsonb)`
- `public.verify_smart_note(uuid)`

The same inventory confirmed authenticated execution remained available for the governed functions.

## WHAT I EXECUTED

Applied migration `revoke_anon_security_definer_execution_20260919` to revoke `EXECUTE` from `anon` for those SECURITY DEFINER entry points.

No function was removed and no authenticated execution boundary was weakened.

## WHY

These functions are authenticated/owner-scoped operations or internal indexing/verification paths. Anonymous execution of exposed SECURITY DEFINER functions creates an unnecessary privilege boundary.

This hardening preserves the law:

**authenticated authority must be independently bound; SECURITY DEFINER must not turn an anonymous caller into an authorized actor.**

## PROOF STATUS

Migration application returned **success**.

A fresh advisor recheck is still required to establish the post-migration lint state.

## IMPORTANT UNKNOWN

This action does not prove the complete SECURITY DEFINER audit. The remaining authenticated SECURITY DEFINER functions require per-function caller, auth.uid binding, owner binding, mutation scope, returned-data, positive-test and negative-test review.

## PROTECTED

- existing authenticated paths
- existing SECURITY DEFINER functions
- Smart Mail auth.uid boundary
- canonical control-plane authority
- no alternate deployment lane
- no product-data rewrite

## NEXT

The canonical P0 control-plane next action remains the authorized Assistant-lane test identity / authenticated lifecycle proof. In parallel, continue the systematic SECURITY DEFINER review and verify this migration's advisor result before changing additional functions.

**SUCCESSOR:** Fresh Naya: re-resolve live main HEAD, consume this receipt, re-run the security advisor, then inspect the remaining authenticated SECURITY DEFINER functions against auth.uid/owner/mutation/data-return boundaries. Do not revoke legitimate authenticated functions blindly.
