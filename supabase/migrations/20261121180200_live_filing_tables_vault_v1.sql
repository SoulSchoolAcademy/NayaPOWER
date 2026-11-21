-- Live filing: vault tables (Seat 1, TABLES) — Supabase filing round 2026-11-21
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
-- Table: public.journal_entries (8 columns, live)
create table if not exists public."journal_entries" (
  "id" uuid default gen_random_uuid() not null,
  "owner_alias" text not null,
  "entry_date" date not null,
  "title" text,
  "body" text,
  "mood" text,
  "created_at" timestamp with time zone default now() not null,
  "updated_at" timestamp with time zone default now() not null,
  constraint "journal_entries_pkey" PRIMARY KEY (id),
  constraint "journal_entries_owner_alias_entry_date_key" UNIQUE (owner_alias, entry_date)
);

create index if not exists idx_journal_owner_date ON public.journal_entries USING btree (owner_alias, entry_date DESC);

alter table public."journal_entries" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,anon=arwdDxtm/postgres,authenticated=arwdDxtm/postgres,service_role=arwdDxtm/postgres}

-- ---------------------------------------------------------------------------
-- Table: public.smart_notes (7 columns, live)
create table if not exists public."smart_notes" (
  "id" uuid default gen_random_uuid() not null,
  "content" text not null,
  "owner_alias" text,
  "created_at" timestamp with time zone default now(),
  "updated_at" timestamp with time zone default now(),
  "author_name" text,
  "sender_name" text,
  constraint "smart_notes_pkey" PRIMARY KEY (id)
);

create index if not exists idx_smart_notes_created ON public.smart_notes USING btree (created_at DESC);
create index if not exists idx_smart_notes_owner ON public.smart_notes USING btree (owner_alias);

alter table public."smart_notes" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,anon=arm/postgres,service_role=arwdDxtm/postgres}

do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='smart_notes' and policyname='pass2_anon_insert_smart_notes') then
    create policy "pass2_anon_insert_smart_notes" on public."smart_notes" as permissive for insert to anon with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='smart_notes' and policyname='pass2_anon_select_smart_notes') then
    create policy "pass2_anon_select_smart_notes" on public."smart_notes" as permissive for select to anon using (true);
  end if;
end $$;

-- trigger trg_auto_file_note on smart_notes
do $$ begin
  if not exists (select 1 from pg_trigger where tgname='trg_auto_file_note' and tgrelid='public."smart_notes"'::regclass) then
    CREATE TRIGGER trg_auto_file_note AFTER INSERT ON public.smart_notes FOR EACH ROW EXECUTE FUNCTION trg_file_note();
  end if;
end $$;
-- trigger trg_smart_notes_touch on smart_notes
do $$ begin
  if not exists (select 1 from pg_trigger where tgname='trg_smart_notes_touch' and tgrelid='public."smart_notes"'::regclass) then
    CREATE TRIGGER trg_smart_notes_touch BEFORE UPDATE ON public.smart_notes FOR EACH ROW EXECUTE FUNCTION touch_updated_at();
  end if;
end $$;

-- ---------------------------------------------------------------------------
-- Table: public.media_notes (15 columns, live)
create table if not exists public."media_notes" (
  "id" uuid default gen_random_uuid() not null,
  "owner_alias" text not null,
  "kind" text not null,
  "title" text,
  "media_url" text not null,
  "storage_path" text not null,
  "mime" text,
  "duration_s" integer,
  "list_name" text,
  "category" text,
  "transcript" text,
  "summary" text,
  "status" text default 'recorded'::text not null,
  "created_at" timestamp with time zone default now() not null,
  "updated_at" timestamp with time zone default now() not null,
  constraint "media_notes_kind_check" CHECK ((kind = ANY (ARRAY['voice'::text, 'video'::text]))),
  constraint "media_notes_status_check" CHECK ((status = ANY (ARRAY['recorded'::text, 'transcribing'::text, 'ready'::text, 'failed'::text]))),
  constraint "media_notes_pkey" PRIMARY KEY (id)
);

create index if not exists media_notes_owner_created ON public.media_notes USING btree (owner_alias, created_at DESC);
create index if not exists media_notes_status ON public.media_notes USING btree (status) WHERE (status = ANY (ARRAY['recorded'::text, 'transcribing'::text]));

alter table public."media_notes" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,anon=arwdDxtm/postgres,authenticated=arwdDxtm/postgres,service_role=arwdDxtm/postgres}

do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='media_notes' and policyname='media_notes_anon_insert') then
    create policy "media_notes_anon_insert" on public."media_notes" as permissive for insert to anon with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='media_notes' and policyname='media_notes_anon_select') then
    create policy "media_notes_anon_select" on public."media_notes" as permissive for select to anon using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='media_notes' and policyname='media_notes_anon_update') then
    create policy "media_notes_anon_update" on public."media_notes" as permissive for update to anon using (true) with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='media_notes' and policyname='media_notes_authenticated_select') then
    create policy "media_notes_authenticated_select" on public."media_notes" as permissive for select to authenticated using (true);
  end if;
end $$;

-- trigger media_notes_touch on media_notes
do $$ begin
  if not exists (select 1 from pg_trigger where tgname='media_notes_touch' and tgrelid='public."media_notes"'::regclass) then
    CREATE TRIGGER media_notes_touch BEFORE UPDATE ON public.media_notes FOR EACH ROW EXECUTE FUNCTION naya_notes_touch_updated_at();
  end if;
end $$;

-- ---------------------------------------------------------------------------
-- Table: public.hub_smart_notes (17 columns, live)
create table if not exists public."hub_smart_notes" (
  "id" uuid default gen_random_uuid() not null,
  "ib_id" text not null,
  "title" text not null,
  "nutshell" text,
  "human_note" text,
  "child_note" text,
  "grandma_note" text,
  "naya_note" text,
  "machine_note" jsonb,
  "what_it_means" text,
  "whats_in_it_for_you" text,
  "how_it_applies" text,
  "source" text,
  "author" text,
  "github_path" text,
  "created_at" timestamp with time zone default now(),
  "note_created" text,
  constraint "hub_smart_notes_pkey" PRIMARY KEY (id),
  constraint "hub_smart_notes_ib_id_key" UNIQUE (ib_id)
);

create index if not exists idx_hub_notes_created ON public.hub_smart_notes USING btree (created_at DESC);

alter table public."hub_smart_notes" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,anon=arwm/postgres,service_role=arwDxtm/postgres}

do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='hub_smart_notes' and policyname='pass2_anon_insert_hub_smart_notes') then
    create policy "pass2_anon_insert_hub_smart_notes" on public."hub_smart_notes" as permissive for insert to anon with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='hub_smart_notes' and policyname='pass2_anon_select_hub_smart_notes') then
    create policy "pass2_anon_select_hub_smart_notes" on public."hub_smart_notes" as permissive for select to anon using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='hub_smart_notes' and policyname='pass2_anon_update_hub_smart_notes') then
    create policy "pass2_anon_update_hub_smart_notes" on public."hub_smart_notes" as permissive for update to anon using (true) with check (true);
  end if;
end $$;

-- trigger hub_smart_notes_delete_guard on hub_smart_notes
do $$ begin
  if not exists (select 1 from pg_trigger where tgname='hub_smart_notes_delete_guard' and tgrelid='public."hub_smart_notes"'::regclass) then
    CREATE TRIGGER hub_smart_notes_delete_guard BEFORE DELETE ON public.hub_smart_notes FOR EACH ROW EXECUTE FUNCTION guard_hub_smart_notes_delete();
  end if;
end $$;

-- ---------------------------------------------------------------------------
-- Table: public.hub_smart_notes_archive (16 columns, live)
create table if not exists public."hub_smart_notes_archive" (
  "id" uuid default gen_random_uuid() not null,
  "ib_id" text not null,
  "title" text not null,
  "nutshell" text,
  "human_note" text,
  "child_note" text,
  "grandma_note" text,
  "naya_note" text,
  "machine_note" jsonb,
  "what_it_means" text,
  "whats_in_it_for_you" text,
  "how_it_applies" text,
  "source" text,
  "author" text,
  "github_path" text,
  "created_at" timestamp with time zone default now(),
  constraint "hub_smart_notes_archive_pkey" PRIMARY KEY (id),
  constraint "hub_smart_notes_archive_ib_id_key" UNIQUE (ib_id)
);

create index if not exists hub_smart_notes_archive_created_at_idx ON public.hub_smart_notes_archive USING btree (created_at DESC);

alter table public."hub_smart_notes_archive" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,service_role=arwdDxtm/postgres}

-- ---------------------------------------------------------------------------
-- Table: public.naya_note_categories (3 columns, live)
create table if not exists public."naya_note_categories" (
  "owner_alias" text not null,
  "name" text not null,
  "created_at" timestamp with time zone default now() not null,
  constraint "naya_note_categories_name_nonempty" CHECK ((length(btrim(name)) > 0)),
  constraint "naya_note_categories_pkey" PRIMARY KEY (owner_alias, name)
);

alter table public."naya_note_categories" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,service_role=arwdDxtm/postgres,anon=arw/postgres}

do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='naya_note_categories' and policyname='naya_note_categories_anon_insert') then
    create policy "naya_note_categories_anon_insert" on public."naya_note_categories" as permissive for insert to anon with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='naya_note_categories' and policyname='naya_note_categories_anon_select') then
    create policy "naya_note_categories_anon_select" on public."naya_note_categories" as permissive for select to anon using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='naya_note_categories' and policyname='naya_note_categories_anon_update') then
    create policy "naya_note_categories_anon_update" on public."naya_note_categories" as permissive for update to anon using (true) with check (true);
  end if;
end $$;

-- ---------------------------------------------------------------------------
-- Table: public.naya_note_filing (4 columns, live)
create table if not exists public."naya_note_filing" (
  "note_id" uuid not null,
  "category_name" text,
  "match_score" numeric,
  "filed_at" timestamp with time zone default now(),
  constraint "naya_note_filing_note_id_fkey" FOREIGN KEY (note_id) REFERENCES smart_notes(id) ON DELETE CASCADE,
  constraint "naya_note_filing_pkey" PRIMARY KEY (note_id)
);

alter table public."naya_note_filing" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,authenticated=arwdDxtm/postgres,service_role=arwdDxtm/postgres,anon=r/postgres}

do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='naya_note_filing' and policyname='naya_note_filing_select_anon') then
    create policy "naya_note_filing_select_anon" on public."naya_note_filing" as permissive for select to anon using (true);
  end if;
end $$;

-- ---------------------------------------------------------------------------
-- Table: public.naya_category_prototypes (6 columns, live)
create table if not exists public."naya_category_prototypes" (
  "category_name" text not null,
  "owner_alias" text,
  "term_signature" jsonb,
  "member_count" integer default 0,
  "created_at" timestamp with time zone default now(),
  "updated_at" timestamp with time zone default now(),
  constraint "naya_category_prototypes_pkey" PRIMARY KEY (category_name)
);

alter table public."naya_category_prototypes" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,authenticated=arwdDxtm/postgres,service_role=arwdDxtm/postgres,anon=r/postgres}

do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='naya_category_prototypes' and policyname='naya_category_prototypes_select_anon') then
    create policy "naya_category_prototypes_select_anon" on public."naya_category_prototypes" as permissive for select to anon using (true);
  end if;
end $$;

-- ---------------------------------------------------------------------------
-- Table: public.custom_defs (6 columns, live)
create table if not exists public."custom_defs" (
  "id" uuid default gen_random_uuid() not null,
  "owner_alias" text not null,
  "kind" text not null,
  "name" text not null,
  "position" integer default 0 not null,
  "created_at" timestamp with time zone default now() not null,
  constraint "custom_defs_kind_check" CHECK ((kind = ANY (ARRAY['field'::text, 'stage'::text]))),
  constraint "custom_defs_pkey" PRIMARY KEY (id),
  constraint "custom_defs_owner_alias_kind_name_key" UNIQUE (owner_alias, kind, name)
);

alter table public."custom_defs" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,anon=arwdDxtm/postgres,authenticated=arwdDxtm/postgres,service_role=arwdDxtm/postgres}

do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='custom_defs' and policyname='custom_defs_ins_anon') then
    create policy "custom_defs_ins_anon" on public."custom_defs" as permissive for insert to anon with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='custom_defs' and policyname='custom_defs_ins_authenticated') then
    create policy "custom_defs_ins_authenticated" on public."custom_defs" as permissive for insert to authenticated with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='custom_defs' and policyname='custom_defs_sel_anon') then
    create policy "custom_defs_sel_anon" on public."custom_defs" as permissive for select to anon using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='custom_defs' and policyname='custom_defs_sel_authenticated') then
    create policy "custom_defs_sel_authenticated" on public."custom_defs" as permissive for select to authenticated using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='custom_defs' and policyname='custom_defs_upd_anon') then
    create policy "custom_defs_upd_anon" on public."custom_defs" as permissive for update to anon using (true) with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='custom_defs' and policyname='custom_defs_upd_authenticated') then
    create policy "custom_defs_upd_authenticated" on public."custom_defs" as permissive for update to authenticated using (true) with check (true);
  end if;
end $$;

-- ---------------------------------------------------------------------------
-- Table: public.citizen_worlds (7 columns, live)
create table if not exists public."citizen_worlds" (
  "alias" text not null,
  "name" text,
  "answers" jsonb default '{}'::jsonb not null,
  "topics" text[] default '{}'::text[] not null,
  "settings" jsonb default '{"space": {"findable": true, "visibility": "public"}, "business": {"findable": true, "visibility": "public"}, "personal": {"findable": true, "visibility": "private"}}'::jsonb not null,
  "created_at" timestamp with time zone default now() not null,
  "updated_at" timestamp with time zone default now() not null,
  constraint "citizen_worlds_pkey" PRIMARY KEY (alias)
);

alter table public."citizen_worlds" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,anon=arwdDxtm/postgres,authenticated=arwdDxtm/postgres,service_role=arwdDxtm/postgres}

-- ---------------------------------------------------------------------------
-- Table: public.hub_meta (3 columns, live)
create table if not exists public."hub_meta" (
  "key" text not null,
  "value" jsonb default '{}'::jsonb not null,
  "updated_at" timestamp with time zone default now() not null,
  constraint "hub_meta_pkey" PRIMARY KEY (key)
);

alter table public."hub_meta" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,anon=arwdDxtm/postgres,authenticated=arwdDxtm/postgres,service_role=arwdDxtm/postgres}

do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='hub_meta' and policyname='hub_meta_del_anon') then
    create policy "hub_meta_del_anon" on public."hub_meta" as permissive for delete to anon using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='hub_meta' and policyname='hub_meta_del_authenticated') then
    create policy "hub_meta_del_authenticated" on public."hub_meta" as permissive for delete to authenticated using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='hub_meta' and policyname='hub_meta_ins_anon') then
    create policy "hub_meta_ins_anon" on public."hub_meta" as permissive for insert to anon with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='hub_meta' and policyname='hub_meta_ins_authenticated') then
    create policy "hub_meta_ins_authenticated" on public."hub_meta" as permissive for insert to authenticated with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='hub_meta' and policyname='hub_meta_sel_anon') then
    create policy "hub_meta_sel_anon" on public."hub_meta" as permissive for select to anon using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='hub_meta' and policyname='hub_meta_sel_authenticated') then
    create policy "hub_meta_sel_authenticated" on public."hub_meta" as permissive for select to authenticated using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='hub_meta' and policyname='hub_meta_upd_anon') then
    create policy "hub_meta_upd_anon" on public."hub_meta" as permissive for update to anon using (true) with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='hub_meta' and policyname='hub_meta_upd_authenticated') then
    create policy "hub_meta_upd_authenticated" on public."hub_meta" as permissive for update to authenticated using (true) with check (true);
  end if;
end $$;

-- ---------------------------------------------------------------------------
-- Table: public.distillation_queue (7 columns, live)
create table if not exists public."distillation_queue" (
  "id" uuid default gen_random_uuid() not null,
  "ib_id" text not null,
  "github_path" text,
  "title" text,
  "queued_at" timestamp with time zone default now() not null,
  "distilled_at" timestamp with time zone,
  "super_id" text,
  constraint "distillation_queue_pkey" PRIMARY KEY (id),
  constraint "distillation_queue_ib_id_key" UNIQUE (ib_id)
);

alter table public."distillation_queue" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,service_role=arwdDxtm/postgres}

-- ---------------------------------------------------------------------------
-- Table: public.hub_daily_intelligence_reports (8 columns, live)
create table if not exists public."hub_daily_intelligence_reports" (
  "report_date" date not null,
  "report_id" text,
  "headline" text not null,
  "lessons_summary" text not null,
  "body_md" text not null,
  "source_path" text,
  "created_at" timestamp with time zone default now() not null,
  "updated_at" timestamp with time zone default now() not null,
  constraint "hub_daily_intelligence_reports_pkey" PRIMARY KEY (report_date),
  constraint "hub_daily_intelligence_reports_report_id_key" UNIQUE (report_id)
);

alter table public."hub_daily_intelligence_reports" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,anon=arwdDxtm/postgres,authenticated=arwdDxtm/postgres,service_role=arwdDxtm/postgres}

do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='hub_daily_intelligence_reports' and policyname='reports are publicly readable') then
    create policy "reports are publicly readable" on public."hub_daily_intelligence_reports" as permissive for select to anon using (true);
  end if;
end $$;

-- ---------------------------------------------------------------------------
-- Table: public.hub_daily_intelligence_reports_backup_20261022 (8 columns, live)
create table if not exists public."hub_daily_intelligence_reports_backup_20261022" (
  "report_date" date,
  "report_id" text,
  "headline" text,
  "lessons_summary" text,
  "body_md" text,
  "source_path" text,
  "created_at" timestamp with time zone,
  "updated_at" timestamp with time zone
);

alter table public."hub_daily_intelligence_reports_backup_20261022" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,anon=arwdDxtm/postgres,authenticated=arwdDxtm/postgres,service_role=arwdDxtm/postgres}

do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='hub_daily_intelligence_reports_backup_20261022' and policyname='hub_daily_backup_sel_anon') then
    create policy "hub_daily_backup_sel_anon" on public."hub_daily_intelligence_reports_backup_20261022" as permissive for select to anon using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='hub_daily_intelligence_reports_backup_20261022' and policyname='hub_daily_backup_sel_authenticated') then
    create policy "hub_daily_backup_sel_authenticated" on public."hub_daily_intelligence_reports_backup_20261022" as permissive for select to authenticated using (true);
  end if;
end $$;
