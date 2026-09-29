create table public.nayanet_team_activity (
  event_id text primary key,
  effective_at timestamptz not null,
  session_id text not null,
  claim_id text not null,
  action_id text not null,
  decision_id text not null,
  authority_id text not null,
  actor_id uuid not null,
  run_id text not null,
  subject text not null,
  summary text not null,
  evidence jsonb not null default '[]'::jsonb,
  next_action text not null,
  successor text not null,
  execution_receipt_id uuid,
  created_at timestamptz not null default now(),
  constraint nayanet_team_activity_evidence_array check (jsonb_typeof(evidence)='array')
);
create unique index nayanet_team_activity_receipt_uq on public.nayanet_team_activity(execution_receipt_id) where execution_receipt_id is not null;
alter table public.nayanet_team_activity enable row level security;
create or replace function public.nayanet_record_team_activity(
  p_event_id text,p_effective_at timestamptz,p_session_id text,p_claim_id text,p_action_id text,
  p_decision_id text,p_authority_id text,p_actor_id uuid,p_run_id text,p_subject text,p_summary text,
  p_evidence jsonb,p_next_action text,p_successor text,p_execution_receipt_id uuid default null
) returns jsonb language plpgsql security definer set search_path=public
as $$
declare v_user uuid := auth.uid(); v_created_at timestamptz; v_event_id text;
begin
 if v_user is null then raise exception 'AUTH_REQUIRED'; end if;
 if p_actor_id <> v_user then raise exception 'ACTOR_BINDING_MISMATCH'; end if;
 if coalesce(length(trim(p_event_id)),0)=0 or coalesce(length(trim(p_session_id)),0)=0 or coalesce(length(trim(p_claim_id)),0)=0
 or coalesce(length(trim(p_action_id)),0)=0 or coalesce(length(trim(p_decision_id)),0)=0 or coalesce(length(trim(p_authority_id)),0)=0
 or coalesce(length(trim(p_run_id)),0)=0 or coalesce(length(trim(p_next_action)),0)=0 or coalesce(length(trim(p_successor)),0)=0
 then raise exception 'ACTIVITY_BINDING_INCOMPLETE'; end if;
 insert into public.nayanet_team_activity(event_id,effective_at,session_id,claim_id,action_id,decision_id,authority_id,actor_id,run_id,subject,summary,evidence,next_action,successor,execution_receipt_id)
 values(p_event_id,p_effective_at,p_session_id,p_claim_id,p_action_id,p_decision_id,p_authority_id,p_actor_id,p_run_id,p_subject,p_summary,p_evidence,p_next_action,p_successor,p_execution_receipt_id)
 on conflict(event_id) do nothing returning event_id,created_at into v_event_id,v_created_at;
 if v_event_id is null then select event_id,created_at into v_event_id,v_created_at from public.nayanet_team_activity where event_id=p_event_id;
 return jsonb_build_object('status','REPLAY','event_id',v_event_id,'created_at',v_created_at); end if;
 return jsonb_build_object('status','CREATED','event_id',v_event_id,'created_at',v_created_at);
end; $$;
revoke all on public.nayanet_team_activity from anon,authenticated;
grant execute on function public.nayanet_record_team_activity(text,timestamptz,text,text,text,text,text,uuid,text,text,text,jsonb,text,text,uuid) to authenticated;
