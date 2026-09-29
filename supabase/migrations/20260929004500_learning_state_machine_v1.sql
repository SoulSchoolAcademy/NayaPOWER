-- NayaPOWER learning lifecycle V1
-- Preserve legacy learning_evidence.status for compatibility while making
-- verification and measured effect explicit, orthogonal, and mechanically enforced.

alter table public.learning_evidence
  add column if not exists verification_state text,
  add column if not exists effect_state text;

-- Fail-closed backfill: only rows carrying the full bounded causal proof signature
-- become VERIFIED / OUTCOME_VERIFIED. Mere ACTIVE status is not enough.
update public.learning_evidence
set
  verification_state = case
    when status = 'ACTIVE'
      and provenance = 'VERIFICATION'
      and verification_method ilike 'Independent causal-learning runtime verification:%'
      and observed_value #>> '{behavioral_delta,changed}' = 'true'
      and observed_value #>> '{outcome_delta,provenance_preserved}' = '1'
      then 'VERIFIED'
    else 'CANDIDATE'
  end,
  effect_state = case
    when status = 'ACTIVE'
      and provenance = 'VERIFICATION'
      and verification_method ilike 'Independent causal-learning runtime verification:%'
      and observed_value #>> '{behavioral_delta,changed}' = 'true'
      and observed_value #>> '{outcome_delta,provenance_preserved}' = '1'
      then 'OUTCOME_VERIFIED'
    when observed_value #>> '{behavioral_delta,changed}' = 'true'
      then 'INFLUENCED'
    else 'UNMEASURED'
  end
where verification_state is null or effect_state is null;

alter table public.learning_evidence
  alter column verification_state set default 'CANDIDATE',
  alter column verification_state set not null,
  alter column effect_state set default 'UNMEASURED',
  alter column effect_state set not null;

do $$
begin
  if not exists (
    select 1 from pg_constraint
    where conname = 'learning_evidence_verification_state_check'
      and conrelid = 'public.learning_evidence'::regclass
  ) then
    alter table public.learning_evidence
      add constraint learning_evidence_verification_state_check
      check (verification_state in ('CANDIDATE','VERIFIED','REJECTED','CONTRADICTED','SUPERSEDED'));
  end if;

  if not exists (
    select 1 from pg_constraint
    where conname = 'learning_evidence_effect_state_check'
      and conrelid = 'public.learning_evidence'::regclass
  ) then
    alter table public.learning_evidence
      add constraint learning_evidence_effect_state_check
      check (effect_state in ('UNMEASURED','INFLUENCED','OUTCOME_VERIFIED'));
  end if;
end
$$;

create table if not exists public.nayanet_learning_state_transitions (
  transition_id uuid primary key default gen_random_uuid(),
  learning_id uuid not null references public.learning_evidence(id) on delete cascade,
  member_id uuid not null references auth.users(id) on delete cascade,
  dimension text not null check (dimension in ('VERIFICATION','EFFECT')),
  from_state text,
  to_state text not null,
  reason text not null,
  evidence jsonb not null default '{}'::jsonb,
  actor_ref text not null default 'database-trigger',
  created_at timestamptz not null default now()
);

create index if not exists nayanet_learning_state_transitions_learning_idx
  on public.nayanet_learning_state_transitions(learning_id, created_at);

alter table public.nayanet_learning_state_transitions enable row level security;

drop policy if exists nayanet_learning_state_transitions_owner_read
  on public.nayanet_learning_state_transitions;
create policy nayanet_learning_state_transitions_owner_read
  on public.nayanet_learning_state_transitions
  for select
  using (auth.uid() = member_id);

grant select on public.nayanet_learning_state_transitions to authenticated;
revoke insert, update, delete on public.nayanet_learning_state_transitions from authenticated, anon;

insert into public.nayanet_learning_state_transitions
  (learning_id, member_id, dimension, from_state, to_state, reason, evidence, actor_ref)
select
  id,
  member_id,
  'VERIFICATION',
  null,
  verification_state,
  'MIGRATION_BASELINE',
  jsonb_build_object('legacy_status', status, 'provenance', provenance),
  'migration'
from public.learning_evidence
where not exists (
  select 1 from public.nayanet_learning_state_transitions t
  where t.learning_id = learning_evidence.id and t.dimension = 'VERIFICATION'
);

insert into public.nayanet_learning_state_transitions
  (learning_id, member_id, dimension, from_state, to_state, reason, evidence, actor_ref)
select
  id,
  member_id,
  'EFFECT',
  null,
  effect_state,
  'MIGRATION_BASELINE',
  jsonb_build_object('legacy_status', status, 'provenance', provenance),
  'migration'
from public.learning_evidence
where not exists (
  select 1 from public.nayanet_learning_state_transitions t
  where t.learning_id = learning_evidence.id and t.dimension = 'EFFECT'
);

create or replace function public.nayanet_guard_learning_state_transition()
returns trigger
language plpgsql
security definer
set search_path = ''
as $$
declare
  v_behavior_changed boolean := coalesce(new.observed_value #>> '{behavioral_delta,changed}', 'false') = 'true';
  v_outcome_delta text := coalesce(new.observed_value #>> '{outcome_delta,provenance_preserved}', '0');
begin
  if old.verification_state is distinct from new.verification_state then
    if not (
      (old.verification_state = 'CANDIDATE' and new.verification_state in ('VERIFIED','REJECTED','CONTRADICTED')) or
      (old.verification_state = 'VERIFIED' and new.verification_state in ('CONTRADICTED','SUPERSEDED')) or
      (old.verification_state = 'CONTRADICTED' and new.verification_state in ('VERIFIED','REJECTED','SUPERSEDED'))
    ) then
      raise exception 'INVALID_LEARNING_VERIFICATION_TRANSITION:%->%', old.verification_state, new.verification_state;
    end if;

    if new.verification_state = 'VERIFIED' and not (
      new.status = 'ACTIVE'
      and new.provenance = 'VERIFICATION'
      and v_behavior_changed
    ) then
      raise exception 'VERIFIED_LEARNING_REQUIRES_ACTIVE_INDEPENDENT_BEHAVIOR_EVIDENCE';
    end if;

    if new.verification_state = 'REJECTED'
      and nullif(trim(coalesce(new.observed_value->>'rejection_reason','')), '') is null then
      raise exception 'REJECTED_LEARNING_REQUIRES_REASON';
    end if;

    if new.verification_state = 'SUPERSEDED'
      and nullif(trim(coalesce(new.observed_value->>'superseded_by_learning_id','')), '') is null then
      raise exception 'SUPERSEDED_LEARNING_REQUIRES_REPLACEMENT';
    end if;
  end if;

  if old.effect_state is distinct from new.effect_state then
    if not (
      (old.effect_state = 'UNMEASURED' and new.effect_state = 'INFLUENCED') or
      (old.effect_state = 'INFLUENCED' and new.effect_state = 'OUTCOME_VERIFIED')
    ) then
      raise exception 'INVALID_LEARNING_EFFECT_TRANSITION:%->%', old.effect_state, new.effect_state;
    end if;

    if new.effect_state = 'INFLUENCED' and not v_behavior_changed then
      raise exception 'INFLUENCED_LEARNING_REQUIRES_MEASURED_BEHAVIOR_CHANGE';
    end if;

    if new.effect_state = 'OUTCOME_VERIFIED' and not (
      new.verification_state = 'VERIFIED'
      and v_behavior_changed
      and v_outcome_delta in ('1','1.0')
      and new.provenance = 'VERIFICATION'
    ) then
      raise exception 'OUTCOME_VERIFIED_REQUIRES_VERIFIED_POSITIVE_MEASURED_OUTCOME';
    end if;
  end if;

  return new;
end
$$;

drop trigger if exists nayanet_guard_learning_state_transition
  on public.learning_evidence;
create trigger nayanet_guard_learning_state_transition
before update of verification_state, effect_state on public.learning_evidence
for each row execute function public.nayanet_guard_learning_state_transition();

create or replace function public.nayanet_record_learning_state_transition()
returns trigger
language plpgsql
security definer
set search_path = ''
as $$
declare
  v_actor text := coalesce(
    nullif(current_setting('request.jwt.claim.sub', true), ''),
    current_user
  );
  v_evidence jsonb := jsonb_build_object(
    'source_event_id', new.source_event_id,
    'verification_method', new.verification_method,
    'legacy_status', new.status,
    'provenance', new.provenance
  );
begin
  if tg_op = 'INSERT' then
    insert into public.nayanet_learning_state_transitions
      (learning_id, member_id, dimension, from_state, to_state, reason, evidence, actor_ref)
    values
      (new.id, new.member_id, 'VERIFICATION', null, new.verification_state, 'LEARNING_CREATED', v_evidence, v_actor),
      (new.id, new.member_id, 'EFFECT', null, new.effect_state, 'LEARNING_CREATED', v_evidence, v_actor);
    return new;
  end if;

  if old.verification_state is distinct from new.verification_state then
    insert into public.nayanet_learning_state_transitions
      (learning_id, member_id, dimension, from_state, to_state, reason, evidence, actor_ref)
    values (
      new.id, new.member_id, 'VERIFICATION', old.verification_state, new.verification_state,
      'VERIFICATION_STATE_TRANSITION', v_evidence, v_actor
    );
  end if;

  if old.effect_state is distinct from new.effect_state then
    insert into public.nayanet_learning_state_transitions
      (learning_id, member_id, dimension, from_state, to_state, reason, evidence, actor_ref)
    values (
      new.id, new.member_id, 'EFFECT', old.effect_state, new.effect_state,
      'EFFECT_STATE_TRANSITION', v_evidence, v_actor
    );
  end if;

  return new;
end
$$;

drop trigger if exists nayanet_record_learning_state_transition
  on public.learning_evidence;
create trigger nayanet_record_learning_state_transition
after insert or update of verification_state, effect_state on public.learning_evidence
for each row execute function public.nayanet_record_learning_state_transition();
