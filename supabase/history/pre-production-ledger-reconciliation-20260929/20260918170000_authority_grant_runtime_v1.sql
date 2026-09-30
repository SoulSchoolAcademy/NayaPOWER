-- Naya Authority Grant Runtime V1
-- Implements the smallest authoritative grant representation without creating a new identity system.

create table if not exists public.nayanet_authority_grants (
  grant_id uuid primary key default gen_random_uuid(),
  issuer_id uuid not null references auth.users(id) on delete restrict,
  subject_id uuid not null references auth.users(id) on delete restrict,
  source_event_id text not null,
  mission_id text not null,
  scope jsonb not null default '{}'::jsonb,
  actions jsonb not null default '[]'::jsonb,
  constraints jsonb not null default '{}'::jsonb,
  issued_at timestamptz not null default now(),
  expires_at timestamptz,
  status text not null default 'ACTIVE' check (status in ('ISSUED','ACTIVE','EXPIRED','REVOKED','INVALID')),
  revoked_at timestamptz,
  evidence jsonb not null default '{}'::jsonb,
  parent_authority jsonb,
  schema_version text not null default '1.0.0',
  created_at timestamptz not null default now(),
  check (jsonb_typeof(scope) = 'object'),
  check (jsonb_typeof(actions) = 'array' and jsonb_array_length(actions) > 0),
  check (expires_at is null or expires_at > issued_at),
  check ((status = 'REVOKED') = (revoked_at is not null))
);

create index if not exists nayanet_authority_grants_subject_idx on public.nayanet_authority_grants(subject_id, status, expires_at);
create index if not exists nayanet_authority_grants_issuer_idx on public.nayanet_authority_grants(issuer_id, created_at desc);
create unique index if not exists nayanet_authority_grants_source_event_key on public.nayanet_authority_grants(issuer_id, source_event_id);

alter table public.nayanet_authority_grants enable row level security;
create policy "authority grants visible to issuer or subject" on public.nayanet_authority_grants for select to authenticated using ((select auth.uid()) = issuer_id or (select auth.uid()) = subject_id);
create policy "authority grants insertable only by authenticated issuer" on public.nayanet_authority_grants for insert to authenticated with check ((select auth.uid()) = issuer_id);
create policy "authority grants revocable only by issuer" on public.nayanet_authority_grants for update to authenticated using ((select auth.uid()) = issuer_id) with check ((select auth.uid()) = issuer_id);

create or replace function public.nayanet_authority_grant_immutable_guard()
returns trigger language plpgsql set search_path = '' as $$
begin
  if new.grant_id <> old.grant_id or new.issuer_id <> old.issuer_id or new.subject_id <> old.subject_id or new.source_event_id <> old.source_event_id or new.mission_id <> old.mission_id or new.scope <> old.scope or new.actions <> old.actions or new.constraints <> old.constraints or new.issued_at <> old.issued_at or new.expires_at is distinct from old.expires_at or new.parent_authority is distinct from old.parent_authority or new.schema_version <> old.schema_version or new.created_at <> old.created_at then
    raise exception 'AUTHORITY_GRANT_IMMUTABLE';
  end if;
  if new.status <> old.status and not (old.status in ('ISSUED','ACTIVE') and new.status = 'REVOKED') then raise exception 'AUTHORITY_GRANT_STATUS_IMMUTABLE'; end if;
  if new.status = 'REVOKED' and new.revoked_at is null then raise exception 'AUTHORITY_GRANT_REVOKED_AT_REQUIRED'; end if;
  if new.status <> 'REVOKED' and new.revoked_at is not null then raise exception 'AUTHORITY_GRANT_REVOKED_AT_FORBIDDEN'; end if;
  if new.evidence <> old.evidence and new.status <> 'REVOKED' then raise exception 'AUTHORITY_GRANT_EVIDENCE_IMMUTABLE'; end if;
  return new;
end;
$$;
drop trigger if exists nayanet_authority_grant_immutable on public.nayanet_authority_grants;
create trigger nayanet_authority_grant_immutable before update on public.nayanet_authority_grants for each row execute function public.nayanet_authority_grant_immutable_guard();

create or replace function public.nayanet_issue_authority_grant(p_subject_id uuid,p_source_event_id text,p_mission_id text,p_scope jsonb,p_actions jsonb,p_constraints jsonb default '{}'::jsonb,p_expires_at timestamptz default null,p_evidence jsonb default '{}'::jsonb,p_parent_authority jsonb default null)
returns public.nayanet_authority_grants language plpgsql set search_path = '' as $$
declare v public.nayanet_authority_grants;
begin
  if (select auth.uid()) is null then raise exception 'AUTH_REQUIRED'; end if;
  if p_subject_id is null or p_source_event_id is null or btrim(p_source_event_id) = '' then raise exception 'AUTHORITY_GRANT_REQUIRED_FIELDS'; end if;
  if p_mission_id is null or btrim(p_mission_id) = '' then raise exception 'AUTHORITY_GRANT_MISSION_REQUIRED'; end if;
  if jsonb_typeof(p_scope) <> 'object' then raise exception 'AUTHORITY_GRANT_SCOPE_INVALID'; end if;
  if jsonb_typeof(p_actions) <> 'array' or jsonb_array_length(p_actions) = 0 then raise exception 'AUTHORITY_GRANT_ACTIONS_REQUIRED'; end if;
  if p_expires_at is not null and p_expires_at <= clock_timestamp() then raise exception 'AUTHORITY_GRANT_EXPIRES_IN_PAST'; end if;
  insert into public.nayanet_authority_grants(issuer_id,subject_id,source_event_id,mission_id,scope,actions,constraints,issued_at,expires_at,status,evidence,parent_authority)
  values ((select auth.uid()),p_subject_id,p_source_event_id,p_mission_id,p_scope,p_actions,coalesce(p_constraints,'{}'::jsonb),clock_timestamp(),p_expires_at,'ACTIVE',coalesce(p_evidence,'{}'::jsonb),p_parent_authority)
  returning * into v;
  return v;
end;
$$;
grant execute on function public.nayanet_issue_authority_grant(uuid,text,text,jsonb,jsonb,jsonb,timestamptz,jsonb,jsonb) to authenticated;
revoke execute on function public.nayanet_issue_authority_grant(uuid,text,text,jsonb,jsonb,jsonb,timestamptz,jsonb,jsonb) from anon, public;

create or replace function public.nayanet_revoke_authority_grant(p_grant_id uuid,p_evidence jsonb default '{}'::jsonb)
returns public.nayanet_authority_grants language plpgsql set search_path = '' as $$
declare v public.nayanet_authority_grants;
begin
  if (select auth.uid()) is null then raise exception 'AUTH_REQUIRED'; end if;
  update public.nayanet_authority_grants set status='REVOKED',revoked_at=clock_timestamp(),evidence=evidence || jsonb_build_object('revocation',coalesce(p_evidence,'{}'::jsonb)) where grant_id=p_grant_id and issuer_id=(select auth.uid()) and status in ('ISSUED','ACTIVE');
  if not found then raise exception 'AUTHORITY_GRANT_NOT_REVOCABLE'; end if;
  select * into v from public.nayanet_authority_grants where grant_id=p_grant_id;
  return v;
end;
$$;
grant execute on function public.nayanet_revoke_authority_grant(uuid,jsonb) to authenticated;
revoke execute on function public.nayanet_revoke_authority_grant(uuid,jsonb) from anon, public;

create or replace function public.nayanet_validate_authority_grant(p_grant_id uuid,p_action text,p_target text)
returns jsonb language plpgsql set search_path = '' as $$
declare g public.nayanet_authority_grants; uid uuid; reason text := 'AUTHORIZED';
begin
  uid := (select auth.uid());
  if uid is null then return jsonb_build_object('status','BLOCKED','reason','AUTH_REQUIRED'); end if;
  select * into g from public.nayanet_authority_grants where grant_id=p_grant_id and (issuer_id=uid or subject_id=uid);
  if not found then return jsonb_build_object('status','BLOCKED','reason','GRANT_NOT_FOUND_OR_NOT_OWNED','grant_id',p_grant_id); end if;
  if g.subject_id <> uid then return jsonb_build_object('status','BLOCKED','reason','WRONG_SUBJECT','grant_id',g.grant_id); end if;
  if g.status='REVOKED' then return jsonb_build_object('status','BLOCKED','reason','GRANT_REVOKED','grant_id',g.grant_id,'source_event_id',g.source_event_id); end if;
  if g.status in ('INVALID','ISSUED') then return jsonb_build_object('status','BLOCKED','reason','GRANT_NOT_ACTIVE','grant_id',g.grant_id,'source_event_id',g.source_event_id); end if;
  if g.expires_at is not null and g.expires_at <= clock_timestamp() then return jsonb_build_object('status','BLOCKED','reason','GRANT_EXPIRED','grant_id',g.grant_id,'source_event_id',g.source_event_id,'expires_at',g.expires_at); end if;
  if not (g.actions ? p_action) then reason := 'ACTION_OUT_OF_SCOPE'; elsif not (coalesce(g.scope->>'target','')=p_target or coalesce(g.scope->>'project_id','')=p_target) then reason := 'TARGET_OUT_OF_SCOPE'; end if;
  if reason='AUTHORIZED' then return jsonb_build_object('status','AUTHORIZED','reason','VALID_IN_SCOPE_GRANT','grant_id',g.grant_id,'issuer_id',g.issuer_id,'subject_id',g.subject_id,'mission_id',g.mission_id,'scope',g.scope,'actions',g.actions,'constraints',g.constraints,'issued_at',g.issued_at,'expires_at',g.expires_at,'grant_status','ACTIVE','revoked_at',g.revoked_at,'evidence',g.evidence,'source_event_id',g.source_event_id); end if;
  return jsonb_build_object('status','BLOCKED','reason',reason,'grant_id',g.grant_id,'issuer_id',g.issuer_id,'subject_id',g.subject_id,'grant_status',g.status,'expires_at',g.expires_at,'revoked_at',g.revoked_at,'source_event_id',g.source_event_id);
end;
$$;
grant execute on function public.nayanet_validate_authority_grant(uuid,text,text) to authenticated;
revoke execute on function public.nayanet_validate_authority_grant(uuid,text,text) from anon, public;

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
