-- Harden trigger-only functions identified by the production security advisor.
-- These functions are invoked by table triggers, not direct client RPC calls.
-- Preserve trigger behavior while removing unnecessary direct execution surface.

alter function public.nayanet_checkpoint_receipts_immutable()
  set search_path = '';

revoke execute on function public.nayanet_checkpoint_receipts_immutable()
  from public, anon, authenticated;

revoke execute on function public.nayanet_require_explicit_smart_connect_consent()
  from public, anon, authenticated;
