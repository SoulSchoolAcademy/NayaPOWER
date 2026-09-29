alter table public.nayanet_execution_receipts
  add column if not exists authority_grant_id uuid references public.nayanet_authority_grants(grant_id) on delete restrict,
  add column if not exists authority_issuer_id uuid references auth.users(id) on delete restrict,
  add column if not exists authority_scope jsonb,
  add column if not exists authority_actions jsonb,
  add column if not exists authority_constraints jsonb,
  add column if not exists authority_status_at_execution text,
  add column if not exists authority_source_event_id text,
  add column if not exists authority_validated_at timestamptz;

create index if not exists nayanet_execution_receipts_authority_grant_idx on public.nayanet_execution_receipts(authority_grant_id);

alter table public.nayanet_execution_receipts
  drop constraint if exists nayanet_execution_receipts_authority_status_check;
alter table public.nayanet_execution_receipts
  add constraint nayanet_execution_receipts_authority_status_check
  check (authority_status_at_execution is null or authority_status_at_execution in ('ACTIVE','EXPIRED','REVOKED','INVALID'));

create or replace function public.nayanet_authority_grant_immutable_guard()
returns trigger
language plpgsql
set search_path = ''
as $$
begin
  if new.grant_id <> old.grant_id
     or new.issuer_id <> old.issuer_id
     or new.subject_id <> old.subject_id
     or new.source_event_id <> old.source_event_id
     or new.mission_id <> old.mission_id
     or new.scope <> old.scope
     or new.actions <> old.actions
     or new.constraints <> old.constraints
     or new.issued_at <> old.issued_at
     or new.expires_at is distinct from old.expires_at
     or new.parent_authority is distinct from old.parent_authority
     or new.schema_version <> old.schema_version
     or new.created_at <> old.created_at
  then
    raise exception 'AUTHORITY_GRANT_IMMUTABLE';
  end if;
  if new.status <> old.status and not (old.status in ('ISSUED','ACTIVE') and new.status = 'REVOKED') then
    raise exception 'AUTHORITY_GRANT_STATUS_IMMUTABLE';
  end if;
  if new.status = 'REVOKED' and new.revoked_at is null then
    raise exception 'AUTHORITY_GRANT_REVOKED_AT_REQUIRED';
  end if;
  if new.status <> 'REVOKED' and new.revoked_at is not null then
    raise exception 'AUTHORITY_GRANT_REVOKED_AT_FORBIDDEN';
  end if;
  if new.evidence <> old.evidence and new.status <> 'REVOKED' then
    raise exception 'AUTHORITY_GRANT_EVIDENCE_IMMUTABLE';
  end if;
  return new;
end;
$$;

create or replace function public.nayanet_validate_authority_grant(
  p_grant_id uuid,
  p_action text,
  p_target text
)
returns jsonb
language plpgsql
set search_path = ''
as $$
declare g public.nayanet_authority_grants; uid uuid; reason text := 'AUTHORIZED';
begin
  uid := (select auth.uid());
  if uid is null then return jsonb_build_object('status','BLOCKED','reason','AUTH_REQUIRED'); end if;
  select * into g from public.nayanet_authority_grants where grant_id = p_grant_id and (issuer_id = uid or subject_id = uid);
  if not found then return jsonb_build_object('status','BLOCKED','reason','GRANT_NOT_FOUND_OR_NOT_OWNED','grant_id',p_grant_id); end if;
  if g.subject_id <> uid then return jsonb_build_object('status','BLOCKED','reason','WRONG_SUBJECT','grant_id',g.grant_id); end if;
  if g.status = 'REVOKED' then return jsonb_build_object('status','BLOCKED','reason','GRANT_REVOKED','grant_id',g.grant_id,'source_event_id',g.source_event_id); end if;
  if g.status in ('INVALID','ISSUED') then return jsonb_build_object('status','BLOCKED','reason','GRANT_NOT_ACTIVE','grant_id',g.grant_id,'source_event_id',g.source_event_id); end if;
  if g.expires_at is not null and g.expires_at <= clock_timestamp() then return jsonb_build_object('status','BLOCKED','reason','GRANT_EXPIRED','grant_id',g.grant_id,'source_event_id',g.source_event_id,'expires_at',g.expires_at); end if;
  if not (g.actions ? p_action) then reason := 'ACTION_OUT_OF_SCOPE';
  elsif not (coalesce(g.scope->>'target','') = p_target or coalesce(g.scope->>'project_id','') = p_target) then reason := 'TARGET_OUT_OF_SCOPE';
  end if;
  if reason = 'AUTHORIZED' then
    return jsonb_build_object('status','AUTHORIZED','reason','VALID_IN_SCOPE_GRANT','grant_id',g.grant_id,'issuer_id',g.issuer_id,'subject_id',g.subject_id,'mission_id',g.mission_id,'scope',g.scope,'actions',g.actions,'constraints',g.constraints,'issued_at',g.issued_at,'expires_at',g.expires_at,'grant_status','ACTIVE','revoked_at',g.revoked_at,'evidence',g.evidence,'source_event_id',g.source_event_id);
  end if;
  return jsonb_build_object('status','BLOCKED','reason',reason,'grant_id',g.grant_id,'issuer_id',g.issuer_id,'subject_id',g.subject_id,'grant_status',g.status,'expires_at',g.expires_at,'revoked_at',g.revoked_at,'source_event_id',g.source_event_id);
end;
$$;
