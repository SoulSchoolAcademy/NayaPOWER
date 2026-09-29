create table if not exists public.learning_evidence (
  id uuid primary key default gen_random_uuid(),
  member_id uuid not null references auth.users(id) on delete cascade,
  target_id text not null,
  level text not null,
  provenance text not null,
  status text not null default 'CANDIDATE',
  claim text not null,
  observed_value jsonb not null default 'null',
  verification_method text not null,
  source_event_id text,
  created_at timestamptz not null default now(),
  expires_at timestamptz
);
create index if not exists learning_evidence_member_target_idx on public.learning_evidence(member_id,target_id,created_at desc);
alter table public.learning_evidence enable row level security;
drop policy if exists learning_evidence_owner on public.learning_evidence;
create policy learning_evidence_owner on public.learning_evidence for all to authenticated using (member_id=auth.uid()) with check (member_id=auth.uid());

create table if not exists public.nayanet_value_receipts (
  receipt_id uuid primary key default gen_random_uuid(),
  owner_id uuid not null references auth.users(id) on delete cascade,
  event_id text not null,
  outcome_id text not null,
  item_id text not null,
  verified_value numeric,
  resources jsonb not null default '{}',
  dimensions jsonb not null default '{}',
  profile jsonb not null default '{}',
  mvpa numeric,
  verification_state text not null,
  evidence_refs jsonb not null default '[]',
  created_at timestamptz not null default now(),
  unique(owner_id,event_id,outcome_id,item_id)
);
alter table public.nayanet_value_receipts enable row level security;
drop policy if exists nayanet_value_receipt_owner on public.nayanet_value_receipts;
create policy nayanet_value_receipt_owner on public.nayanet_value_receipts for all to authenticated using (owner_id=auth.uid()) with check (owner_id=auth.uid());

create or replace function public.nayanet_validate_authority_grant(
  p_grant_id uuid, p_action text, p_target text
) returns jsonb language plpgsql security definer set search_path='' as $$
declare g public.nayanet_authority_grants; uid uuid := auth.uid();
begin
  if uid is null then return jsonb_build_object('status','BLOCKED','reason','AUTH_REQUIRED'); end if;
  select * into g from public.nayanet_authority_grants
   where grant_id=p_grant_id and subject_id=uid;
  if not found then return jsonb_build_object('status','BLOCKED','reason','GRANT_NOT_FOUND_OR_NOT_OWNED'); end if;
  if g.status='REVOKED' then return jsonb_build_object('status','BLOCKED','reason','GRANT_REVOKED'); end if;
  if g.status<>'ACTIVE' then return jsonb_build_object('status','BLOCKED','reason','GRANT_NOT_ACTIVE'); end if;
  if g.expires_at is not null and g.expires_at <= clock_timestamp()
    then return jsonb_build_object('status','BLOCKED','reason','GRANT_EXPIRED'); end if;
  if not (g.actions ? p_action) then return jsonb_build_object('status','BLOCKED','reason','ACTION_OUT_OF_SCOPE'); end if;
  if coalesce(g.scope->>'target','')<>p_target and coalesce(g.scope->>'project_id','')<>p_target
    then return jsonb_build_object('status','BLOCKED','reason','TARGET_OUT_OF_SCOPE'); end if;
  return jsonb_build_object('status','AUTHORIZED','grant_id',g.grant_id,'issuer_id',g.issuer_id,'subject_id',g.subject_id,'mission_id',g.mission_id,'scope',g.scope,'actions',g.actions,'constraints',g.constraints,'source_event_id',g.source_event_id);
end;
$$;
revoke all on function public.nayanet_validate_authority_grant(uuid,text,text) from public,anon;
grant execute on function public.nayanet_validate_authority_grant(uuid,text,text) to authenticated;

create or replace function public.nayanet_retrieve_intelligent_block(p_block_id uuid)
returns public.nayanet_intelligent_blocks
language plpgsql security invoker set search_path=public as $$
declare b public.nayanet_intelligent_blocks;
begin
  select * into b from public.nayanet_intelligent_blocks
   where block_id=p_block_id and owner_id=auth.uid()
     and status not in ('DELETED','SUPERSEDED');
  if not found then raise exception 'INTELLIGENT_BLOCK_NOT_FOUND_OR_NOT_OWNED'; end if;
  return b;
end;
$$;
revoke all on function public.nayanet_retrieve_intelligent_block(uuid) from public,anon;
grant execute on function public.nayanet_retrieve_intelligent_block(uuid) to authenticated;
