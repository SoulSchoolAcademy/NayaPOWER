-- Live filing: personal tables (Seat 1, TABLES) — Supabase filing round 2026-11-21
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

-- ---------------------------------------------------------------------------
-- Table: public.person_stages (5 columns, live)
create table if not exists public."person_stages" (
  "id" uuid default gen_random_uuid() not null,
  "owner_alias" text not null,
  "person_id" text not null,
  "def_id" uuid not null,
  "updated_at" timestamp with time zone default now() not null,
  constraint "person_stages_def_id_fkey" FOREIGN KEY (def_id) REFERENCES custom_defs(id),
  constraint "person_stages_pkey" PRIMARY KEY (id),
  constraint "person_stages_owner_alias_person_id_key" UNIQUE (owner_alias, person_id)
);

alter table public."person_stages" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,anon=arwdDxtm/postgres,authenticated=arwdDxtm/postgres,service_role=arwdDxtm/postgres}

do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='person_stages' and policyname='person_stages_del_anon') then
    create policy "person_stages_del_anon" on public."person_stages" as permissive for delete to anon using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='person_stages' and policyname='person_stages_del_authenticated') then
    create policy "person_stages_del_authenticated" on public."person_stages" as permissive for delete to authenticated using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='person_stages' and policyname='person_stages_ins_anon') then
    create policy "person_stages_ins_anon" on public."person_stages" as permissive for insert to anon with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='person_stages' and policyname='person_stages_ins_authenticated') then
    create policy "person_stages_ins_authenticated" on public."person_stages" as permissive for insert to authenticated with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='person_stages' and policyname='person_stages_sel_anon') then
    create policy "person_stages_sel_anon" on public."person_stages" as permissive for select to anon using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='person_stages' and policyname='person_stages_sel_authenticated') then
    create policy "person_stages_sel_authenticated" on public."person_stages" as permissive for select to authenticated using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='person_stages' and policyname='person_stages_upd_anon') then
    create policy "person_stages_upd_anon" on public."person_stages" as permissive for update to anon using (true) with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='person_stages' and policyname='person_stages_upd_authenticated') then
    create policy "person_stages_upd_authenticated" on public."person_stages" as permissive for update to authenticated using (true) with check (true);
  end if;
end $$;

-- ---------------------------------------------------------------------------
-- Table: public.person_values (6 columns, live)
create table if not exists public."person_values" (
  "id" uuid default gen_random_uuid() not null,
  "owner_alias" text not null,
  "person_id" text not null,
  "def_id" uuid not null,
  "value" text default ''::text not null,
  "updated_at" timestamp with time zone default now() not null,
  constraint "person_values_def_id_fkey" FOREIGN KEY (def_id) REFERENCES custom_defs(id),
  constraint "person_values_pkey" PRIMARY KEY (id),
  constraint "person_values_owner_alias_person_id_def_id_key" UNIQUE (owner_alias, person_id, def_id)
);

alter table public."person_values" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,anon=arwdDxtm/postgres,authenticated=arwdDxtm/postgres,service_role=arwdDxtm/postgres}

do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='person_values' and policyname='person_values_ins_anon') then
    create policy "person_values_ins_anon" on public."person_values" as permissive for insert to anon with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='person_values' and policyname='person_values_ins_authenticated') then
    create policy "person_values_ins_authenticated" on public."person_values" as permissive for insert to authenticated with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='person_values' and policyname='person_values_sel_anon') then
    create policy "person_values_sel_anon" on public."person_values" as permissive for select to anon using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='person_values' and policyname='person_values_sel_authenticated') then
    create policy "person_values_sel_authenticated" on public."person_values" as permissive for select to authenticated using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='person_values' and policyname='person_values_upd_anon') then
    create policy "person_values_upd_anon" on public."person_values" as permissive for update to anon using (true) with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='person_values' and policyname='person_values_upd_authenticated') then
    create policy "person_values_upd_authenticated" on public."person_values" as permissive for update to authenticated using (true) with check (true);
  end if;
end $$;

-- ---------------------------------------------------------------------------
-- Table: public.scheduled_messages (15 columns, live)
create table if not exists public."scheduled_messages" (
  "id" uuid default gen_random_uuid() not null,
  "owner_alias" text not null,
  "kind" text default 'mail'::text not null,
  "recipients" jsonb default '[]'::jsonb not null,
  "subject" text not null,
  "body" text not null,
  "fire_at" timestamp with time zone not null,
  "recur" jsonb,
  "status" text default 'pending'::text not null,
  "attempts" integer default 0 not null,
  "last_error" text,
  "fired_at" timestamp with time zone,
  "result" jsonb,
  "created_at" timestamp with time zone default now() not null,
  "updated_at" timestamp with time zone default now() not null,
  constraint "scheduled_messages_pkey" PRIMARY KEY (id)
);

alter table public."scheduled_messages" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,anon=arwdDxtm/postgres,authenticated=arwdDxtm/postgres,service_role=arwdDxtm/postgres}

do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='scheduled_messages' and policyname='pass2_anon_insert_scheduled_messages') then
    create policy "pass2_anon_insert_scheduled_messages" on public."scheduled_messages" as permissive for insert to anon with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='scheduled_messages' and policyname='pass2_anon_select_scheduled_messages') then
    create policy "pass2_anon_select_scheduled_messages" on public."scheduled_messages" as permissive for select to anon using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='scheduled_messages' and policyname='pass2_anon_update_scheduled_messages') then
    create policy "pass2_anon_update_scheduled_messages" on public."scheduled_messages" as permissive for update to anon using (true) with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='scheduled_messages' and policyname='scheduled_messages_owner_delete') then
    create policy "scheduled_messages_owner_delete" on public."scheduled_messages" as permissive for delete to authenticated using ((owner_alias = COALESCE(((auth.jwt() -> 'app_metadata'::text) ->> 'smart_alias'::text), ((auth.jwt() -> 'user_metadata'::text) ->> 'smart_alias'::text))));
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='scheduled_messages' and policyname='scheduled_messages_owner_select') then
    create policy "scheduled_messages_owner_select" on public."scheduled_messages" as permissive for select to authenticated using ((owner_alias = COALESCE(((auth.jwt() -> 'app_metadata'::text) ->> 'smart_alias'::text), ((auth.jwt() -> 'user_metadata'::text) ->> 'smart_alias'::text))));
  end if;
end $$;

-- ---------------------------------------------------------------------------
-- Table: public.voice_requests (7 columns, live)
create table if not exists public."voice_requests" (
  "key" text not null,
  "text" text not null,
  "status" text default 'pending'::text not null,
  "created_at" timestamp with time zone default now() not null,
  "claimed_at" timestamp with time zone,
  "done_at" timestamp with time zone,
  "error" text,
  constraint "voice_requests_pkey" PRIMARY KEY (key)
);

alter table public."voice_requests" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,anon=arwm/postgres,service_role=arwdDxtm/postgres}

do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='voice_requests' and policyname='pass2_anon_insert_voice_requests') then
    create policy "pass2_anon_insert_voice_requests" on public."voice_requests" as permissive for insert to anon with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='voice_requests' and policyname='pass2_anon_select_voice_requests') then
    create policy "pass2_anon_select_voice_requests" on public."voice_requests" as permissive for select to anon using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='voice_requests' and policyname='pass2_anon_update_voice_requests') then
    create policy "pass2_anon_update_voice_requests" on public."voice_requests" as permissive for update to anon using (true) with check (true);
  end if;
end $$;

-- ---------------------------------------------------------------------------
-- Table: public.alarms (9 columns, live)
create table if not exists public."alarms" (
  "id" uuid default gen_random_uuid() not null,
  "probe" text not null,
  "failure" text not null,
  "item_key" text,
  "first_seen" timestamp with time zone default now() not null,
  "last_seen" timestamp with time zone default now() not null,
  "state" text default 'firing'::text not null,
  "cleared_by_proof_url" text,
  "detail" jsonb default '{}'::jsonb not null,
  constraint "alarms_pkey" PRIMARY KEY (id)
);

create UNIQUE index if not exists alarms_firing_uniq ON public.alarms USING btree (probe, COALESCE(item_key, ''::text)) WHERE (state = 'firing'::text);

alter table public."alarms" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,anon=arwdDxtm/postgres,authenticated=arwdDxtm/postgres,service_role=arwdDxtm/postgres}

do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='alarms' and policyname='alarms_del_anon') then
    create policy "alarms_del_anon" on public."alarms" as permissive for delete to anon using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='alarms' and policyname='alarms_del_authenticated') then
    create policy "alarms_del_authenticated" on public."alarms" as permissive for delete to authenticated using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='alarms' and policyname='alarms_ins_anon') then
    create policy "alarms_ins_anon" on public."alarms" as permissive for insert to anon with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='alarms' and policyname='alarms_ins_authenticated') then
    create policy "alarms_ins_authenticated" on public."alarms" as permissive for insert to authenticated with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='alarms' and policyname='alarms_sel_anon') then
    create policy "alarms_sel_anon" on public."alarms" as permissive for select to anon using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='alarms' and policyname='alarms_sel_authenticated') then
    create policy "alarms_sel_authenticated" on public."alarms" as permissive for select to authenticated using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='alarms' and policyname='alarms_upd_anon') then
    create policy "alarms_upd_anon" on public."alarms" as permissive for update to anon using (true) with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='alarms' and policyname='alarms_upd_authenticated') then
    create policy "alarms_upd_authenticated" on public."alarms" as permissive for update to authenticated using (true) with check (true);
  end if;
end $$;

-- ---------------------------------------------------------------------------
-- Table: public.node_notes (5 columns, live)
create table if not exists public."node_notes" (
  "id" uuid default gen_random_uuid() not null,
  "node_key" text not null,
  "seat" text not null,
  "body" text not null,
  "at" timestamp with time zone default now() not null,
  constraint "node_notes_pkey" PRIMARY KEY (id)
);

create index if not exists node_notes_key_idx ON public.node_notes USING btree (node_key, at DESC);

alter table public."node_notes" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,anon=arwdDxtm/postgres,authenticated=arwdDxtm/postgres,service_role=arwdDxtm/postgres}

do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='node_notes' and policyname='node_notes_ins_anon') then
    create policy "node_notes_ins_anon" on public."node_notes" as permissive for insert to anon with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='node_notes' and policyname='node_notes_ins_authenticated') then
    create policy "node_notes_ins_authenticated" on public."node_notes" as permissive for insert to authenticated with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='node_notes' and policyname='node_notes_sel_anon') then
    create policy "node_notes_sel_anon" on public."node_notes" as permissive for select to anon using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='node_notes' and policyname='node_notes_sel_authenticated') then
    create policy "node_notes_sel_authenticated" on public."node_notes" as permissive for select to authenticated using (true);
  end if;
end $$;

-- ---------------------------------------------------------------------------
-- Table: public.production_daily (21 columns, live)
create table if not exists public."production_daily" (
  "id" uuid default gen_random_uuid() not null,
  "day" date not null,
  "transitions_today" integer default 0 not null,
  "transitions_7d" integer default 0 not null,
  "done_proven_total" integer default 0 not null,
  "ledger_proven_total" integer default 0 not null,
  "ledger_gap" integer default 0 not null,
  "activity_today" integer,
  "ratio_today" numeric,
  "ratio_null_reason" text,
  "detail" jsonb default '{}'::jsonb not null,
  "created_at" timestamp with time zone default now() not null,
  "updated_at" timestamp with time zone default now() not null,
  "effort_per_outcome" numeric,
  "effort_null_reason" text,
  "exec_productive" integer,
  "exec_monitoring" integer,
  "exec_refusal" integer,
  "exec_waste" integer,
  "productive_rate" numeric,
  "human_value" jsonb,
  constraint "production_daily_pkey" PRIMARY KEY (id),
  constraint "production_daily_day_key" UNIQUE (day)
);

alter table public."production_daily" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,anon=arwdDxtm/postgres,authenticated=arwdDxtm/postgres,service_role=arwdDxtm/postgres}

do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='production_daily' and policyname='production_daily_del_anon') then
    create policy "production_daily_del_anon" on public."production_daily" as permissive for delete to anon using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='production_daily' and policyname='production_daily_del_authenticated') then
    create policy "production_daily_del_authenticated" on public."production_daily" as permissive for delete to authenticated using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='production_daily' and policyname='production_daily_ins_anon') then
    create policy "production_daily_ins_anon" on public."production_daily" as permissive for insert to anon with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='production_daily' and policyname='production_daily_ins_authenticated') then
    create policy "production_daily_ins_authenticated" on public."production_daily" as permissive for insert to authenticated with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='production_daily' and policyname='production_daily_sel_anon') then
    create policy "production_daily_sel_anon" on public."production_daily" as permissive for select to anon using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='production_daily' and policyname='production_daily_sel_authenticated') then
    create policy "production_daily_sel_authenticated" on public."production_daily" as permissive for select to authenticated using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='production_daily' and policyname='production_daily_upd_anon') then
    create policy "production_daily_upd_anon" on public."production_daily" as permissive for update to anon using (true) with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='production_daily' and policyname='production_daily_upd_authenticated') then
    create policy "production_daily_upd_authenticated" on public."production_daily" as permissive for update to authenticated using (true) with check (true);
  end if;
end $$;
