-- Intelligent Graph Relationship V2 persistence hardening.
-- Additive only. Extends the existing canonical relationship table; no second graph store.
-- Historical V1 edges remain epistemically unchanged and are backfilled only with conservative defaults.

alter table public.nayanet_brain_relationships
  add column if not exists status text not null default 'ACTIVE',
  add column if not exists visibility text not null default 'PRIVATE',
  add column if not exists evidence_refs jsonb not null default '[]'::jsonb,
  add column if not exists observed_at timestamptz,
  add column if not exists valid_from timestamptz,
  add column if not exists valid_until timestamptz,
  add column if not exists supersedes_relationship_id uuid references public.nayanet_brain_relationships(relationship_id),
  add column if not exists consent_ref text,
  add column if not exists applicability jsonb not null default '{"state":"UNKNOWN","task_classes":[],"limitations":["LEGACY_V1_UNCLASSIFIED"]}'::jsonb,
  add column if not exists reason_codes jsonb not null default '["LEGACY_V1_EDGE"]'::jsonb;

update public.nayanet_brain_relationships
set observed_at = coalesce(observed_at, created_at),
    valid_from = coalesce(valid_from, created_at)
where observed_at is null or valid_from is null;

alter table public.nayanet_brain_relationships
  alter column observed_at set not null,
  alter column valid_from set not null;

alter table public.nayanet_brain_relationships
  drop constraint if exists nayanet_brain_relationships_status_v2_chk,
  add constraint nayanet_brain_relationships_status_v2_chk
    check (status in ('ACTIVE','REVOKED','SUPERSEDED','INVALIDATED')),

  drop constraint if exists nayanet_brain_relationships_visibility_v2_chk,
  add constraint nayanet_brain_relationships_visibility_v2_chk
    check (visibility in ('PRIVATE','DERIVED_SHARED','PUBLIC_DERIVED')),

  drop constraint if exists nayanet_brain_relationships_temporal_v2_chk,
  add constraint nayanet_brain_relationships_temporal_v2_chk
    check (valid_until is null or valid_from <= valid_until),

  drop constraint if exists nayanet_brain_relationships_supersession_v2_chk,
  add constraint nayanet_brain_relationships_supersession_v2_chk
    check (supersedes_relationship_id is null or supersedes_relationship_id <> relationship_id),

  drop constraint if exists nayanet_brain_relationships_visibility_consent_v2_chk,
  add constraint nayanet_brain_relationships_visibility_consent_v2_chk
    check (visibility <> 'DERIVED_SHARED' or consent_ref is not null),

  drop constraint if exists nayanet_brain_relationships_evidence_refs_v2_chk,
  add constraint nayanet_brain_relationships_evidence_refs_v2_chk
    check (jsonb_typeof(evidence_refs) = 'array'),

  drop constraint if exists nayanet_brain_relationships_applicability_v2_chk,
  add constraint nayanet_brain_relationships_applicability_v2_chk
    check (
      jsonb_typeof(applicability) = 'object'
      and applicability ? 'state'
      and applicability ? 'task_classes'
      and applicability ? 'limitations'
      and applicability->>'state' in ('APPLICABLE','NOT_APPLICABLE','UNKNOWN')
      and jsonb_typeof(applicability->'task_classes') = 'array'
      and jsonb_typeof(applicability->'limitations') = 'array'
    ),

  drop constraint if exists nayanet_brain_relationships_reason_codes_v2_chk,
  add constraint nayanet_brain_relationships_reason_codes_v2_chk
    check (jsonb_typeof(reason_codes) = 'array' and jsonb_array_length(reason_codes) > 0);

create index if not exists nayanet_relationship_owner_status_time_v2_idx
  on public.nayanet_brain_relationships(owner_id,status,valid_from,valid_until);

create index if not exists nayanet_relationship_supersession_v2_idx
  on public.nayanet_brain_relationships(owner_id,supersedes_relationship_id)
  where supersedes_relationship_id is not null;

comment on column public.nayanet_brain_relationships.visibility is
  'Graph V2 visibility. PRIVATE by default. DERIVED_SHARED requires consent_ref.';
comment on column public.nayanet_brain_relationships.applicability is
  'Task applicability metadata. UNKNOWN remains UNKNOWN; retrieval does not imply applicability.';
comment on column public.nayanet_brain_relationships.supersedes_relationship_id is
  'Optional exact prior relationship superseded by this edge. Never deletes historical provenance.';

-- Deliberately no UPDATE to epistemic_state.
-- Migration does not promote historical V1 edges, create authority, widen RLS, or claim live runtime support.
