create or replace function public.nayanet_record_team_activity(
  p_event_id text,p_effective_at timestamptz,p_session_id text,p_claim_id text,p_action_id text,
  p_decision_id text,p_authority_id text,p_actor_id uuid,p_run_id text,p_subject text,p_summary text,
  p_evidence jsonb,p_next_action text,p_successor text,p_execution_receipt_id uuid default null
) returns jsonb language plpgsql security definer set search_path=public
as $$
declare v_user uuid := auth.uid(); v_created_at timestamptz; v_event_id text; v_receipt_user uuid; v_receipt_status text;
begin
 if v_user is null then raise exception 'AUTH_REQUIRED'; end if;
 if p_actor_id <> v_user then raise exception 'ACTOR_BINDING_MISMATCH'; end if;
 if p_execution_receipt_id is null then raise exception 'EXECUTION_RECEIPT_REQUIRED'; end if;
 select user_id,status into v_receipt_user,v_receipt_status from public.nayanet_execution_receipts where id=p_execution_receipt_id;
 if v_receipt_user is null then raise exception 'EXECUTION_RECEIPT_NOT_FOUND'; end if;
 if v_receipt_user <> v_user then raise exception 'EXECUTION_RECEIPT_OWNER_MISMATCH'; end if;
 if v_receipt_status not in ('VERIFIED','EXECUTED','SUCCESS') then raise exception 'EXECUTION_NOT_COMPLETED'; end if;
 if coalesce(length(trim(p_event_id)),0)=0 or coalesce(length(trim(p_session_id)),0)=0 or coalesce(length(trim(p_claim_id)),0)=0
 or coalesce(length(trim(p_action_id)),0)=0 or coalesce(length(trim(p_decision_id)),0)=0 or coalesce(length(trim(p_authority_id)),0)=0
 or coalesce(length(trim(p_run_id)),0)=0 or coalesce(length(trim(p_next_action)),0)=0 or coalesce(length(trim(p_successor)),0)=0
 then raise exception 'ACTIVITY_BINDING_INCOMPLETE'; end if;
 insert into public.nayanet_team_activity(event_id,effective_at,session_id,claim_id,action_id,decision_id,authority_id,actor_id,run_id,subject,summary,evidence,next_action,successor,execution_receipt_id)
 values(p_event_id,p_effective_at,p_session_id,p_claim_id,p_action_id,p_decision_id,p_authority_id,p_actor_id,p_run_id,p_subject,p_summary,p_evidence,p_next_action,p_successor,p_execution_receipt_id)
 on conflict(event_id) do nothing returning event_id,created_at into v_event_id,v_created_at;
 if v_event_id is null then select event_id,created_at into v_event_id,v_created_at from public.nayanet_team_activity where event_id=p_event_id; return jsonb_build_object('status','REPLAY','event_id',v_event_id,'created_at',v_created_at); end if;
 return jsonb_build_object('status','CREATED','event_id',v_event_id,'created_at',v_created_at);
end; $$;
