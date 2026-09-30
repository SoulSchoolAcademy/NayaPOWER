-- Preserve Graph V2 temporal integrity while keeping canonical producers compatible.
-- A newly persisted relationship is observed and becomes valid at insertion time.
-- This does not relax NOT NULL, temporal, evidence, visibility, consent, or epistemic constraints.

alter table public.nayanet_brain_relationships
  alter column observed_at set default now(),
  alter column valid_from set default now();
