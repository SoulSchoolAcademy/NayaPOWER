-- Live filing: project_ops tables (Seat 1, TABLES) — Supabase filing round 2026-11-21
-- Source: FIRST-HAND live read of project supabase-red-cable (dahisasgpfvziswqvmvm)
--   via Supabase Management API POST /projects/dahisasgpfvziswqvmvm/database/query
--   (pg_catalog + pg_get_constraintdef / pg_get_indexdef / pg_get_triggerdef / pg_get_viewdef),
--   read 2026-11-21. READ-ONLY against live: no live writes, no schema/RLS/policy changes.
-- Laws named: THE-NAYA-DESIGN-LAWS.md FIRST, then THE-PLAYBOOK.md, DESIGN-INTELLIGENCE-REPORT.md,
--   THE-ULTIMATE-ORIENTATION.md, THE-SET-ORIENTATION.md, THE-ANATOMY-OF-A-SMART-APP-PAGE.md,
--   THE-HEART-OF-THE-MACHINE.md, THE-OFFICIAL-PARTS.md, THE-ARMY-TRAINING.md, the One-Build Law,
--   the Eleven Laws, the Inventory Law.
-- These objects had NO source in any repo migration (verified against the fixed analyzer:
-- 71 migration CREATE TABLEs + 2 migration CREATE VIEWs, 195 files, 0 failures).
-- Idempotent: CREATE TABLE IF NOT EXISTS / CREATE INDEX IF NOT EXISTS / CREATE POLICY guarded
-- by DO blocks; safe to replay on a DB that already has these objects.
-- NOTE: trigger functions referenced below are filed by Seat 2 (FUNCTIONS) where live-only;
--   this file creates the tables + trigger attachments only.
-- NOTE (Seat 7 reorder, 2026-11-21 — SEAT-6-DECISION B8–B9): the projects
--   section below now precedes project_intel_items (it was L279–L341):
--   project_intel_items / work_items FK to projects, which did not exist yet at
--   those points (42P01). projects references only itself (self-FK parent_id,
--   re-checked first-hand), so the move is cycle-free. Every statement in the
--   moved section is byte-identical; order only.
-- NOTE (Seat 6 fix, 2026-11-21 — SEAT-5-DECISION finding): the two trigger blocks
--   below (trg_items_state_changed, trg_items_transition_log) now guard on
--   to_regproc('public.items_state_changed' / 'public.items_transition_log') IS NOT NULL,
--   so on a fresh apply — where 190008 (which defines both functions) has not run yet —
--   the blocks skip cleanly instead of erroring 42883 and halting the chain.
--   190008 creates both triggers itself (guarded), so they still land at the end
--   of the chain. The two CREATE TRIGGER statements are byte-identical; nothing
--   else in this file changed.

-- ---------------------------------------------------------------------------
-- Table: public.projects (6 columns, live)
create table if not exists public."projects" (
  "id" uuid default gen_random_uuid() not null,
  "owner_alias" text not null,
  "name" text not null,
  "motto" text,
  "created_at" timestamp with time zone default now() not null,
  "parent_id" uuid,
  constraint "projects_motto_bounded" CHECK ((char_length(COALESCE(motto, ''::text)) <= 300)),
  constraint "projects_name_bounded" CHECK ((char_length(name) <= 120)),
  constraint "projects_name_nonempty" CHECK ((char_length(btrim(name)) > 0)),
  constraint "projects_parent_id_fkey" FOREIGN KEY (parent_id) REFERENCES projects(id) ON DELETE SET NULL,
  constraint "projects_pkey" PRIMARY KEY (id)
);

create index if not exists projects_owner_idx ON public.projects USING btree (owner_alias, created_at DESC);
create index if not exists projects_parent_idx ON public.projects USING btree (parent_id, created_at);

alter table public."projects" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,anon=arwdDxtm/postgres,authenticated=arwdDxtm/postgres,service_role=arwdDxtm/postgres}

do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='projects' and policyname='projects_del_anon') then
    create policy "projects_del_anon" on public."projects" as permissive for delete to anon using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='projects' and policyname='projects_del_authenticated') then
    create policy "projects_del_authenticated" on public."projects" as permissive for delete to authenticated using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='projects' and policyname='projects_ins_anon') then
    create policy "projects_ins_anon" on public."projects" as permissive for insert to anon with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='projects' and policyname='projects_ins_authenticated') then
    create policy "projects_ins_authenticated" on public."projects" as permissive for insert to authenticated with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='projects' and policyname='projects_sel_anon') then
    create policy "projects_sel_anon" on public."projects" as permissive for select to anon using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='projects' and policyname='projects_sel_authenticated') then
    create policy "projects_sel_authenticated" on public."projects" as permissive for select to authenticated using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='projects' and policyname='projects_upd_anon') then
    create policy "projects_upd_anon" on public."projects" as permissive for update to anon using (true) with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='projects' and policyname='projects_upd_authenticated') then
    create policy "projects_upd_authenticated" on public."projects" as permissive for update to authenticated using (true) with check (true);
  end if;
end $$;

-- ---------------------------------------------------------------------------
-- Table: public.project_intel_items (20 columns, live)
create table if not exists public."project_intel_items" (
  "id" uuid default gen_random_uuid() not null,
  "project_id" uuid not null,
  "item_key" text not null,
  "title" text not null,
  "state" text not null,
  "detail" text,
  "evidence_url" text,
  "sort" integer default 0 not null,
  "updated_at" timestamp with time zone default now() not null,
  "owner_seat" text,
  "next_action" text,
  "blocker" jsonb,
  "maker_seat" text,
  "prover_seat" text,
  "last_actor_seat" text,
  "note_refs" text[] default '{}'::text[] not null,
  "notes" jsonb default '[]'::jsonb not null,
  "parent_item_id" uuid,
  "state_changed_at" timestamp with time zone,
  "created_at" timestamp with time zone,
  constraint "project_intel_items_key_bounded" CHECK ((char_length(item_key) <= 200)),
  constraint "project_intel_items_key_nonempty" CHECK ((char_length(btrim(item_key)) > 0)),
  constraint "project_intel_items_state_valid" CHECK ((state = ANY (ARRAY['done-proven'::text, 'in-motion'::text, 'blocked'::text, 'queued'::text, 'needs-his-hands'::text, 'summary'::text, 'claimed'::text, 'in_progress'::text, 'verifying'::text, 'done_proven'::text, 'needs_shawn'::text]))),
  constraint "project_intel_items_title_bounded" CHECK ((char_length(title) <= 500)),
  constraint "project_intel_items_parent_item_id_fkey" FOREIGN KEY (parent_item_id) REFERENCES project_intel_items(id) ON DELETE SET NULL,
  constraint "project_intel_items_project_id_fkey" FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
  constraint "project_intel_items_pkey" PRIMARY KEY (id),
  constraint "project_intel_items_unique" UNIQUE (project_id, item_key)
);

create index if not exists project_intel_items_project_idx ON public.project_intel_items USING btree (project_id, sort);

alter table public."project_intel_items" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,anon=arwdDxtm/postgres,authenticated=arwdDxtm/postgres,service_role=arwdDxtm/postgres}

do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='project_intel_items' and policyname='project_intel_items_del_anon') then
    create policy "project_intel_items_del_anon" on public."project_intel_items" as permissive for delete to anon using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='project_intel_items' and policyname='project_intel_items_del_authenticated') then
    create policy "project_intel_items_del_authenticated" on public."project_intel_items" as permissive for delete to authenticated using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='project_intel_items' and policyname='project_intel_items_ins_anon') then
    create policy "project_intel_items_ins_anon" on public."project_intel_items" as permissive for insert to anon with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='project_intel_items' and policyname='project_intel_items_ins_authenticated') then
    create policy "project_intel_items_ins_authenticated" on public."project_intel_items" as permissive for insert to authenticated with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='project_intel_items' and policyname='project_intel_items_sel_anon') then
    create policy "project_intel_items_sel_anon" on public."project_intel_items" as permissive for select to anon using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='project_intel_items' and policyname='project_intel_items_sel_authenticated') then
    create policy "project_intel_items_sel_authenticated" on public."project_intel_items" as permissive for select to authenticated using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='project_intel_items' and policyname='project_intel_items_upd_anon') then
    create policy "project_intel_items_upd_anon" on public."project_intel_items" as permissive for update to anon using (true) with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='project_intel_items' and policyname='project_intel_items_upd_authenticated') then
    create policy "project_intel_items_upd_authenticated" on public."project_intel_items" as permissive for update to authenticated using (true) with check (true);
  end if;
end $$;

-- trigger trg_items_state_changed on project_intel_items
do $$ begin
  if to_regproc('public.items_state_changed') is not null and not exists (select 1 from pg_trigger where tgname='trg_items_state_changed' and tgrelid='public."project_intel_items"'::regclass) then
    CREATE TRIGGER trg_items_state_changed BEFORE UPDATE ON public.project_intel_items FOR EACH ROW EXECUTE FUNCTION items_state_changed();
  end if;
end $$;
-- trigger trg_items_transition_log on project_intel_items
do $$ begin
  if to_regproc('public.items_transition_log') is not null and not exists (select 1 from pg_trigger where tgname='trg_items_transition_log' and tgrelid='public."project_intel_items"'::regclass) then
    CREATE TRIGGER trg_items_transition_log AFTER INSERT OR UPDATE OF state ON public.project_intel_items FOR EACH ROW EXECUTE FUNCTION items_transition_log();
  end if;
end $$;

-- ---------------------------------------------------------------------------
-- Table: public.work_items (23 columns, live)
create table if not exists public."work_items" (
  "id" uuid default gen_random_uuid() not null,
  "project_id" uuid not null,
  "parent_item_id" uuid,
  "item_key" text not null,
  "title" text not null,
  "detail" text,
  "state" text default 'queued'::text not null,
  "owner_seat" text,
  "next_action" text,
  "blocker" jsonb,
  "priority" integer,
  "evidence_url" text,
  "maker_seat" text,
  "prover_seat" text,
  "last_actor_seat" text,
  "cost_units" numeric,
  "note_refs" text[] default '{}'::text[] not null,
  "notes" jsonb default '[]'::jsonb not null,
  "created_at" timestamp with time zone default now() not null,
  "updated_at" timestamp with time zone default now() not null,
  "state_changed_at" timestamp with time zone default now() not null,
  "claimed_at" timestamp with time zone,
  "acceptance_criteria" jsonb default '[]'::jsonb not null,
  constraint "work_items_blocked_law" CHECK (((state <> 'blocked'::text) OR ((blocker IS NOT NULL) AND (blocker ? 'what'::text) AND (blocker ? 'owner'::text) AND (blocker ? 'since'::text) AND (blocker ? 'clearing_action'::text)))),
  constraint "work_items_done_proven_law" CHECK (((state <> 'done_proven'::text) OR ((evidence_url IS NOT NULL) AND (prover_seat IS NOT NULL) AND ((maker_seat IS NULL) OR (prover_seat <> maker_seat))))),
  constraint "work_items_state_check" CHECK ((state = ANY (ARRAY['queued'::text, 'claimed'::text, 'in_progress'::text, 'verifying'::text, 'done_proven'::text, 'blocked'::text, 'needs_shawn'::text, 'done-proven'::text, 'in-motion'::text, 'needs-his-hands'::text]))),
  constraint "work_items_state_valid" CHECK ((state = ANY (ARRAY['queued'::text, 'claimed'::text, 'in_progress'::text, 'verifying'::text, 'blocked'::text, 'needs_shawn'::text, 'done_proven'::text]))),
  constraint "work_items_title_nonempty" CHECK ((char_length(btrim(title)) > 0)),
  constraint "work_items_parent_item_id_fkey" FOREIGN KEY (parent_item_id) REFERENCES work_items(id) ON DELETE SET NULL,
  constraint "work_items_project_id_fkey" FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
  constraint "work_items_pkey" PRIMARY KEY (id),
  constraint "work_items_project_key" UNIQUE (project_id, item_key)
);

alter table public."work_items" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,anon=arwdDxtm/postgres,authenticated=arwdDxtm/postgres,service_role=arwdDxtm/postgres}

do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='work_items' and policyname='work_items_del_anon') then
    create policy "work_items_del_anon" on public."work_items" as permissive for delete to anon using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='work_items' and policyname='work_items_del_authenticated') then
    create policy "work_items_del_authenticated" on public."work_items" as permissive for delete to authenticated using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='work_items' and policyname='work_items_ins_anon') then
    create policy "work_items_ins_anon" on public."work_items" as permissive for insert to anon with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='work_items' and policyname='work_items_ins_authenticated') then
    create policy "work_items_ins_authenticated" on public."work_items" as permissive for insert to authenticated with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='work_items' and policyname='work_items_sel_anon') then
    create policy "work_items_sel_anon" on public."work_items" as permissive for select to anon using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='work_items' and policyname='work_items_sel_authenticated') then
    create policy "work_items_sel_authenticated" on public."work_items" as permissive for select to authenticated using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='work_items' and policyname='work_items_upd_anon') then
    create policy "work_items_upd_anon" on public."work_items" as permissive for update to anon using (true) with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='work_items' and policyname='work_items_upd_authenticated') then
    create policy "work_items_upd_authenticated" on public."work_items" as permissive for update to authenticated using (true) with check (true);
  end if;
end $$;

-- trigger trg_work_items_state_changed on work_items
do $$ begin
  if not exists (select 1 from pg_trigger where tgname='trg_work_items_state_changed' and tgrelid='public."work_items"'::regclass) then
    CREATE TRIGGER trg_work_items_state_changed BEFORE UPDATE ON public.work_items FOR EACH ROW EXECUTE FUNCTION work_items_state_changed();
  end if;
end $$;
-- trigger trg_work_items_transition_log on work_items
do $$ begin
  if not exists (select 1 from pg_trigger where tgname='trg_work_items_transition_log' and tgrelid='public."work_items"'::regclass) then
    CREATE TRIGGER trg_work_items_transition_log AFTER INSERT OR UPDATE OF state ON public.work_items FOR EACH ROW EXECUTE FUNCTION work_items_transition_log();
  end if;
end $$;
-- trigger work_items_packet_law_trg on work_items
do $$ begin
  if not exists (select 1 from pg_trigger where tgname='work_items_packet_law_trg' and tgrelid='public."work_items"'::regclass) then
    CREATE CONSTRAINT TRIGGER work_items_packet_law_trg AFTER INSERT OR UPDATE OF state ON public.work_items DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION work_items_packet_law();
  end if;
end $$;

-- ---------------------------------------------------------------------------
-- Table: public.work_transitions (9 columns, live)
create table if not exists public."work_transitions" (
  "id" uuid default gen_random_uuid() not null,
  "item_id" uuid,
  "item_key" text,
  "project_id" uuid,
  "from_state" text,
  "to_state" text,
  "actor_seat" text,
  "proof_url" text,
  "at" timestamp with time zone default now() not null,
  constraint "work_transitions_pkey" PRIMARY KEY (id)
);

create index if not exists work_transitions_at_idx ON public.work_transitions USING btree (at);
create index if not exists work_transitions_item_idx ON public.work_transitions USING btree (item_id);

alter table public."work_transitions" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,anon=arwdDxtm/postgres,authenticated=arwdDxtm/postgres,service_role=arwdDxtm/postgres}

do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='work_transitions' and policyname='work_transitions_del_anon') then
    create policy "work_transitions_del_anon" on public."work_transitions" as permissive for delete to anon using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='work_transitions' and policyname='work_transitions_del_authenticated') then
    create policy "work_transitions_del_authenticated" on public."work_transitions" as permissive for delete to authenticated using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='work_transitions' and policyname='work_transitions_ins_anon') then
    create policy "work_transitions_ins_anon" on public."work_transitions" as permissive for insert to anon with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='work_transitions' and policyname='work_transitions_ins_authenticated') then
    create policy "work_transitions_ins_authenticated" on public."work_transitions" as permissive for insert to authenticated with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='work_transitions' and policyname='work_transitions_sel_anon') then
    create policy "work_transitions_sel_anon" on public."work_transitions" as permissive for select to anon using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='work_transitions' and policyname='work_transitions_sel_authenticated') then
    create policy "work_transitions_sel_authenticated" on public."work_transitions" as permissive for select to authenticated using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='work_transitions' and policyname='work_transitions_upd_anon') then
    create policy "work_transitions_upd_anon" on public."work_transitions" as permissive for update to anon using (true) with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='work_transitions' and policyname='work_transitions_upd_authenticated') then
    create policy "work_transitions_upd_authenticated" on public."work_transitions" as permissive for update to authenticated using (true) with check (true);
  end if;
end $$;

-- ---------------------------------------------------------------------------
-- Table: public.project_members (6 columns, live)
create table if not exists public."project_members" (
  "id" uuid default gen_random_uuid() not null,
  "project_id" uuid not null,
  "member_ref" text not null,
  "member_label" text,
  "added_by" text,
  "created_at" timestamp with time zone default now() not null,
  constraint "project_members_label_bounded" CHECK ((char_length(COALESCE(member_label, ''::text)) <= 300)),
  constraint "project_members_ref_bounded" CHECK ((char_length(member_ref) <= 200)),
  constraint "project_members_ref_nonempty" CHECK ((char_length(btrim(member_ref)) > 0)),
  constraint "project_members_project_id_fkey" FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
  constraint "project_members_pkey" PRIMARY KEY (id),
  constraint "project_members_unique" UNIQUE (project_id, member_ref)
);

create index if not exists project_members_project_idx ON public.project_members USING btree (project_id, created_at);
create index if not exists project_members_ref_idx ON public.project_members USING btree (member_ref, created_at DESC);

alter table public."project_members" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,anon=arwdDxtm/postgres,authenticated=arwdDxtm/postgres,service_role=arwdDxtm/postgres}

do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='project_members' and policyname='project_members_del_anon') then
    create policy "project_members_del_anon" on public."project_members" as permissive for delete to anon using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='project_members' and policyname='project_members_del_authenticated') then
    create policy "project_members_del_authenticated" on public."project_members" as permissive for delete to authenticated using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='project_members' and policyname='project_members_ins_anon') then
    create policy "project_members_ins_anon" on public."project_members" as permissive for insert to anon with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='project_members' and policyname='project_members_ins_authenticated') then
    create policy "project_members_ins_authenticated" on public."project_members" as permissive for insert to authenticated with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='project_members' and policyname='project_members_sel_anon') then
    create policy "project_members_sel_anon" on public."project_members" as permissive for select to anon using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='project_members' and policyname='project_members_sel_authenticated') then
    create policy "project_members_sel_authenticated" on public."project_members" as permissive for select to authenticated using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='project_members' and policyname='project_members_upd_anon') then
    create policy "project_members_upd_anon" on public."project_members" as permissive for update to anon using (true) with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='project_members' and policyname='project_members_upd_authenticated') then
    create policy "project_members_upd_authenticated" on public."project_members" as permissive for update to authenticated using (true) with check (true);
  end if;
end $$;

-- ---------------------------------------------------------------------------
-- Table: public.build_queue (7 columns, live)
create table if not exists public."build_queue" (
  "id" uuid default gen_random_uuid() not null,
  "contract" jsonb not null,
  "status" text default 'pending'::text,
  "result_url" text,
  "receipt" jsonb,
  "created_at" timestamp with time zone default now(),
  "updated_at" timestamp with time zone default now(),
  constraint "build_queue_status_check" CHECK ((status = ANY (ARRAY['pending'::text, 'building'::text, 'done'::text, 'failed'::text]))),
  constraint "build_queue_pkey" PRIMARY KEY (id)
);

alter table public."build_queue" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,anon=arwm/postgres,service_role=arwdDxtm/postgres}

do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='build_queue' and policyname='pass2_anon_insert_build_queue') then
    create policy "pass2_anon_insert_build_queue" on public."build_queue" as permissive for insert to anon with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='build_queue' and policyname='pass2_anon_select_build_queue') then
    create policy "pass2_anon_select_build_queue" on public."build_queue" as permissive for select to anon using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='build_queue' and policyname='pass2_anon_update_build_queue') then
    create policy "pass2_anon_update_build_queue" on public."build_queue" as permissive for update to anon using (true) with check (true);
  end if;
end $$;

-- ---------------------------------------------------------------------------
-- Table: public.queue_packets (10 columns, live)
create table if not exists public."queue_packets" (
  "id" uuid default gen_random_uuid() not null,
  "item_id" uuid,
  "item_key" text not null,
  "project_id" uuid not null,
  "decision_sentence" text not null,
  "prepared_state" text,
  "rollback" text not null,
  "stub" boolean default false not null,
  "raised_at" timestamp with time zone default now() not null,
  "escalated_at" timestamp with time zone,
  constraint "queue_packets_item_id_fkey" FOREIGN KEY (item_id) REFERENCES project_intel_items(id) ON DELETE CASCADE,
  constraint "queue_packets_pkey" PRIMARY KEY (id),
  constraint "queue_packets_project_key" UNIQUE (project_id, item_key)
);

alter table public."queue_packets" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,anon=arwdDxtm/postgres,authenticated=arwdDxtm/postgres,service_role=arwdDxtm/postgres}

do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='queue_packets' and policyname='queue_packets_del_anon') then
    create policy "queue_packets_del_anon" on public."queue_packets" as permissive for delete to anon using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='queue_packets' and policyname='queue_packets_del_authenticated') then
    create policy "queue_packets_del_authenticated" on public."queue_packets" as permissive for delete to authenticated using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='queue_packets' and policyname='queue_packets_ins_anon') then
    create policy "queue_packets_ins_anon" on public."queue_packets" as permissive for insert to anon with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='queue_packets' and policyname='queue_packets_ins_authenticated') then
    create policy "queue_packets_ins_authenticated" on public."queue_packets" as permissive for insert to authenticated with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='queue_packets' and policyname='queue_packets_sel_anon') then
    create policy "queue_packets_sel_anon" on public."queue_packets" as permissive for select to anon using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='queue_packets' and policyname='queue_packets_sel_authenticated') then
    create policy "queue_packets_sel_authenticated" on public."queue_packets" as permissive for select to authenticated using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='queue_packets' and policyname='queue_packets_upd_anon') then
    create policy "queue_packets_upd_anon" on public."queue_packets" as permissive for update to anon using (true) with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='queue_packets' and policyname='queue_packets_upd_authenticated') then
    create policy "queue_packets_upd_authenticated" on public."queue_packets" as permissive for update to authenticated using (true) with check (true);
  end if;
end $$;

-- ---------------------------------------------------------------------------
-- Table: public.census_daily (9 columns, live)
create table if not exists public."census_daily" (
  "id" uuid default gen_random_uuid() not null,
  "day" date not null,
  "house" text not null,
  "jobs_run" integer default 0 not null,
  "wakeups" integer default 0 not null,
  "seat_actions" integer default 0 not null,
  "detail" jsonb default '{}'::jsonb not null,
  "created_at" timestamp with time zone default now() not null,
  "updated_at" timestamp with time zone default now() not null,
  constraint "census_daily_house_nonempty" CHECK ((char_length(btrim(house)) > 0)),
  constraint "census_daily_pkey" PRIMARY KEY (id),
  constraint "census_daily_day_house" UNIQUE (day, house)
);

alter table public."census_daily" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,anon=arwdDxtm/postgres,authenticated=arwdDxtm/postgres,service_role=arwdDxtm/postgres}

do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='census_daily' and policyname='census_daily_del_anon') then
    create policy "census_daily_del_anon" on public."census_daily" as permissive for delete to anon using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='census_daily' and policyname='census_daily_del_authenticated') then
    create policy "census_daily_del_authenticated" on public."census_daily" as permissive for delete to authenticated using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='census_daily' and policyname='census_daily_ins_anon') then
    create policy "census_daily_ins_anon" on public."census_daily" as permissive for insert to anon with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='census_daily' and policyname='census_daily_ins_authenticated') then
    create policy "census_daily_ins_authenticated" on public."census_daily" as permissive for insert to authenticated with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='census_daily' and policyname='census_daily_sel_anon') then
    create policy "census_daily_sel_anon" on public."census_daily" as permissive for select to anon using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='census_daily' and policyname='census_daily_sel_authenticated') then
    create policy "census_daily_sel_authenticated" on public."census_daily" as permissive for select to authenticated using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='census_daily' and policyname='census_daily_upd_anon') then
    create policy "census_daily_upd_anon" on public."census_daily" as permissive for update to anon using (true) with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='census_daily' and policyname='census_daily_upd_authenticated') then
    create policy "census_daily_upd_authenticated" on public."census_daily" as permissive for update to authenticated using (true) with check (true);
  end if;
end $$;

-- ---------------------------------------------------------------------------
-- Table: public.hub_cost_daily (9 columns, live)
create table if not exists public."hub_cost_daily" (
  "id" uuid default gen_random_uuid() not null,
  "day" date not null,
  "derivation_runs" integer default 0 not null,
  "census_runs" integer default 0 not null,
  "detector_runs" integer default 0 not null,
  "est_units" numeric,
  "detail" jsonb default '{}'::jsonb not null,
  "created_at" timestamp with time zone default now() not null,
  "updated_at" timestamp with time zone default now() not null,
  constraint "hub_cost_daily_pkey" PRIMARY KEY (id),
  constraint "hub_cost_daily_day_key" UNIQUE (day)
);

alter table public."hub_cost_daily" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,anon=arwdDxtm/postgres,authenticated=arwdDxtm/postgres,service_role=arwdDxtm/postgres}

do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='hub_cost_daily' and policyname='hub_cost_daily_del_anon') then
    create policy "hub_cost_daily_del_anon" on public."hub_cost_daily" as permissive for delete to anon using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='hub_cost_daily' and policyname='hub_cost_daily_del_authenticated') then
    create policy "hub_cost_daily_del_authenticated" on public."hub_cost_daily" as permissive for delete to authenticated using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='hub_cost_daily' and policyname='hub_cost_daily_ins_anon') then
    create policy "hub_cost_daily_ins_anon" on public."hub_cost_daily" as permissive for insert to anon with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='hub_cost_daily' and policyname='hub_cost_daily_ins_authenticated') then
    create policy "hub_cost_daily_ins_authenticated" on public."hub_cost_daily" as permissive for insert to authenticated with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='hub_cost_daily' and policyname='hub_cost_daily_sel_anon') then
    create policy "hub_cost_daily_sel_anon" on public."hub_cost_daily" as permissive for select to anon using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='hub_cost_daily' and policyname='hub_cost_daily_sel_authenticated') then
    create policy "hub_cost_daily_sel_authenticated" on public."hub_cost_daily" as permissive for select to authenticated using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='hub_cost_daily' and policyname='hub_cost_daily_upd_anon') then
    create policy "hub_cost_daily_upd_anon" on public."hub_cost_daily" as permissive for update to anon using (true) with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='hub_cost_daily' and policyname='hub_cost_daily_upd_authenticated') then
    create policy "hub_cost_daily_upd_authenticated" on public."hub_cost_daily" as permissive for update to authenticated using (true) with check (true);
  end if;
end $$;

-- ---------------------------------------------------------------------------
-- Table: public.seat_keys (5 columns, live)
create table if not exists public."seat_keys" (
  "seat" text not null,
  "key_hash" text not null,
  "label" text,
  "last_used" timestamp with time zone,
  "revoked_at" timestamp with time zone,
  constraint "seat_keys_pkey" PRIMARY KEY (key_hash)
);

alter table public."seat_keys" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,authenticated=arwdDxtm/postgres,service_role=arwdDxtm/postgres}

-- ---------------------------------------------------------------------------
-- Table: public.seat_lane_mapping (4 columns, live)
create table if not exists public."seat_lane_mapping" (
  "seat" text not null,
  "lane" text not null,
  "granted_by" text,
  "granted_at" timestamp with time zone,
  constraint "seat_lane_mapping_pkey" PRIMARY KEY (seat, lane)
);

alter table public."seat_lane_mapping" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,authenticated=arwdDxtm/postgres,service_role=arwdDxtm/postgres}

-- ---------------------------------------------------------------------------
-- Table: public.automation_events (14 columns, live)
create table if not exists public."automation_events" (
  "id" uuid default gen_random_uuid() not null,
  "owner_alias" text not null,
  "kind" text not null,
  "proposal_key" text not null,
  "subject_name" text not null,
  "subject_ref" text,
  "reason" text not null,
  "draft" text not null,
  "action_kind" text not null,
  "action_note" text not null,
  "status" text default 'proposed'::text not null,
  "outcome" text,
  "created_at" timestamp with time zone default now() not null,
  "decided_at" timestamp with time zone,
  constraint "automation_events_pkey" PRIMARY KEY (id),
  constraint "automation_events_proposal_key_key" UNIQUE (proposal_key)
);

alter table public."automation_events" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,anon=arwdDxtm/postgres,authenticated=arwdDxtm/postgres,service_role=arwdDxtm/postgres}

do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='automation_events' and policyname='pass2_anon_insert_automation_events') then
    create policy "pass2_anon_insert_automation_events" on public."automation_events" as permissive for insert to anon with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='automation_events' and policyname='pass2_anon_select_automation_events') then
    create policy "pass2_anon_select_automation_events" on public."automation_events" as permissive for select to anon using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='automation_events' and policyname='pass2_anon_update_automation_events') then
    create policy "pass2_anon_update_automation_events" on public."automation_events" as permissive for update to anon using (true) with check (true);
  end if;
end $$;
