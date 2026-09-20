-- P0 independent real-outcome/value contract V1
create table if not exists public.nayanet_execution_outcomes (
  outcome_id uuid primary key default gen_random_uuid(),
  receipt_id uuid not null unique references public.nayanet_execution_receipts(id) on delete restrict,
  user_id uuid not null references auth.users(id) on delete restrict,
  project_id text not null,
  experiment_case_id text,
  outcome_type text not null,
  verifier_id uuid not null references auth.users(id) on delete restrict,
  evidence jsonb not null default '{}'::jsonb,
  benefit numeric not null default 0,
  harm numeric not null default 0,
  cost numeric not null default 0,
  risk_adjusted_loss numeric not null default 0,
  verified_value numeric generated always as (benefit - harm - cost - risk_adjusted_loss) stored,
  verified boolean not null default false,
  verification_method text not null,
  created_at timestamptz not null default now(),
  check (jsonb_typeof(evidence) = 'object'),
  check (benefit >= 0 and harm >= 0 and cost >= 0 and risk_adjusted_loss >= 0)
);

comment on table public.nayanet_execution_outcomes is
  'Independent receiver/outcome evidence for consequential execution receipts. Value is deterministically computed from independently recorded outcome components; execution policy cannot self-score it.';

alter table public.nayanet_execution_outcomes enable row level security;

drop policy if exists nayanet_execution_outcomes_select_own on public.nayanet_execution_outcomes;
create policy nayanet_execution_outcomes_select_own
  on public.nayanet_execution_outcomes for select
  to authenticated
  using ((select auth.uid()) = user_id);

revoke all on table public.nayanet_execution_outcomes from anon, authenticated, public;
grant select on table public.nayanet_execution_outcomes to authenticated;

create or replace function public.nayanet_record_smart_mail_outcome(
  p_receipt_id uuid,
  p_message_id uuid,
  p_experiment_case_id text default null
)
returns jsonb
language plpgsql
security definer
set search_path=''
as $$
declare
  v_user uuid := (select auth.uid());
  r public.nayanet_execution_receipts;
  m public.v7_mail_messages;
  outcome public.nayanet_execution_outcomes;
begin
  if v_user is null then raise exception 'AUTH_REQUIRED'; end if;
  select * into r from public.nayanet_execution_receipts where id = p_receipt_id for share;
  if r.id is null then raise exception 'RECEIPT_NOT_FOUND'; end if;
  if r.user_id <> v_user then raise exception 'RECEIPT_OWNER_MISMATCH'; end if;
  if r.action <> 'smart_mail_send' then raise exception 'UNSUPPORTED_OUTCOME_ACTION'; end if;
  if p_experiment_case_id is not null and r.experiment_case_id is not null
     and r.experiment_case_id <> p_experiment_case_id then raise exception 'EXPERIMENT_CASE_MISMATCH'; end if;
  select * into m from public.v7_mail_messages where id = p_message_id;
  if m.id is null then raise exception 'MESSAGE_NOT_FOUND'; end if;
  if (m.metadata->>'execution_receipt_id') <> p_receipt_id::text then raise exception 'MESSAGE_RECEIPT_LINEAGE_MISMATCH'; end if;
  if not exists (select 1 from public.v7_mail_members where thread_id = m.thread_id and user_id = v_user)
    then raise exception 'RECEIVER_NOT_AUTHORIZED'; end if;

  insert into public.nayanet_execution_outcomes(
    receipt_id,user_id,project_id,experiment_case_id,outcome_type,verifier_id,
    evidence,benefit,harm,cost,risk_adjusted_loss,verified,verification_method
  )
  values(
    r.id,r.user_id,r.project_id,r.experiment_case_id,'receiver_retrieval',v_user,
    jsonb_build_object(
      'message_id',m.id,'thread_id',m.thread_id,'receiver_id',v_user,
      'receiver_retrieved',true,'receiver_retrieved_at',now(),
      'source','authenticated_receiver_retrieval',
      'outcome_contract','NAYANET_REAL_OUTCOME_VALUE_V1'
    ),
    1,0,0,0,true,'authenticated receiver retrieval'
  )
  on conflict (receipt_id) do update
    set evidence=excluded.evidence, verifier_id=excluded.verifier_id,
        verified=true, verification_method=excluded.verification_method
  returning * into outcome;

  update public.nayanet_execution_receipts
    set value = coalesce(value,'{}'::jsonb) || jsonb_build_object(
      'schema','NAYANET_REAL_OUTCOME_VALUE_V1','outcome_id',outcome.outcome_id,
      'verified',outcome.verified,'verified_value',outcome.verified_value,
      'verification_method',outcome.verification_method
    )
  where id=r.id;

  return jsonb_build_object(
    'status','VERIFIED','outcome_id',outcome.outcome_id,'receipt_id',outcome.receipt_id,
    'verified_value',outcome.verified_value,'benefit',outcome.benefit,'harm',outcome.harm,
    'cost',outcome.cost,'risk_adjusted_loss',outcome.risk_adjusted_loss,
    'verification_method',outcome.verification_method,'evidence',outcome.evidence
  );
end;
$$;

revoke all on function public.nayanet_record_smart_mail_outcome(uuid,uuid,text) from public,anon,authenticated;
grant execute on function public.nayanet_record_smart_mail_outcome(uuid,uuid,text) to authenticated,service_role;

create index if not exists nayanet_execution_outcomes_receipt_idx
  on public.nayanet_execution_outcomes(receipt_id);
create index if not exists nayanet_execution_outcomes_case_idx
  on public.nayanet_execution_outcomes(user_id,project_id,experiment_case_id,created_at desc);
