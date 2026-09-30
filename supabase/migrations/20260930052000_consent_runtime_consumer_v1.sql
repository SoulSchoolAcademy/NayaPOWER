-- P4 — Consent runtime consumer: the missing live reader for the consent seam.
--
-- PROPOSED / SOURCE-ONLY. Not applied to production. Not merged. Opened-but-unmerged PR.
--
-- Context (H10-1, report: workspace/h10-1-verification.md; design: P4-consent-consumer-design):
-- migration 20260930022500 created the consent/revocation schema but no runtime
-- consumer — post-promotion the schema exists while every read path trusts
-- point-in-time stamps instead of LIVE participation. This migration supplies the
-- one consumer every current read path must call:
--   public.nayanet_consent_is_active(p_owner_id uuid) -> boolean
-- and hardens the collective_wisdom read policy (R2) to require live
-- participation, not row status alone. The graph selector read path (R1) must
-- call the same function per edge owner at read time — wired in PR #1125
-- (naya/know-v2-selector-gates), not here.
--
-- Ordering: runs strictly AFTER 20260930022500 (consent schema) and
-- 20260930040000 (R1 writer). No production object is modified: the
-- superseded objects below were created by an UNAPPLIED pending migration.
--
-- Constitutional basis: Art. XI (PRIVATE BY DEFAULT; SHARED BY CHOICE;
-- COLLECTIVE BY CONSENT), Art. V.4 (revocation must prevent further
-- consequential use), Art. XIV (fail closed on authority/consent uncertainty).

-- =========================================================================
-- 1. The live-consent consumer.
--    TRUE  iff the owner holds >= 1 participation row with
--          status='active' AND consent_state='explicit'.
--    FALSE otherwise: no row, revoked, pending, NULL owner, or ANY query
--    error. UNKNOWN -> FALSE. Fail closed, always (Art. XIV).
-- =========================================================================

create or replace function public.nayanet_consent_is_active(p_owner_id uuid)
returns boolean
language plpgsql
security definer
set search_path = ''
as $$
declare
  v_ok boolean := false;
begin
  if p_owner_id is null then
    return false;
  end if;
  begin
    select exists(
      select 1
      from public.nayanet_smart_connect_participation
      where member_id = p_owner_id
        and status = 'active'
        and consent_state = 'explicit'
    ) into v_ok;
  exception
    when others then
      -- Any failure of the consent check is a denial, never a bypass.
      return false;
  end;
  return coalesce(v_ok, false);
end;
$$;

comment on function public.nayanet_consent_is_active(uuid) is
  'P4 consent runtime consumer. Live explicit-consent check. TRUE iff owner has >= 1 '
  'participation row (status=active AND consent_state=explicit). FALSE on every other '
  'state and on any error — fail closed (Art. XIV). Every cross-owner read path '
  '(graph selector R1, collective_wisdom RLS R2, future Spaces/connectors R3) must '
  'call this per owner at read time. PROPOSED — not applied to production.';

-- Least privilege: callable by the runtime paths that need it; not by the public.
revoke all on function public.nayanet_consent_is_active(uuid) from public, anon;
grant execute on function public.nayanet_consent_is_active(uuid) to authenticated, service_role;

-- =========================================================================
-- 2. Harden the collective_wisdom read path (R2).
--    The pending policy from 20260930022500 trusted the row's status alone:
--      using (status='ACTIVE' or owner_id = auth.uid())
--    A row can be ACTIVE while the owner's participation is revoked (direct
--    write, missed revocation path). Require LIVE participation for
--    non-owners. Owners always read their own rows.
-- =========================================================================

-- The authenticated read policy below can only fire if the role holds the
-- table privilege: RLS is evaluated AFTER the GRANT check. Without this
-- grant every authenticated read fails with "permission denied for table"
-- before any policy runs (proven by executing the verify script: P2 failed
-- at the grant check, not the policy). The security_invoker feed view does
-- not bypass this — the invoker still needs the base-table privilege.
grant select on public.nayanet_collective_wisdom to authenticated;

drop policy if exists nayanet_collective_wisdom_safe_read
  on public.nayanet_collective_wisdom;

create policy nayanet_collective_wisdom_safe_read
  on public.nayanet_collective_wisdom
  for select to authenticated
  using (
    (status = 'ACTIVE' and public.nayanet_consent_is_active(owner_id))
    or owner_id = auth.uid()
  );

comment on policy nayanet_collective_wisdom_safe_read
  on public.nayanet_collective_wisdom is
  'P4: read requires LIVE explicit participation for non-owners (not row status '
  'alone). Owners always read their own rows. PROPOSED — not applied to production.';
