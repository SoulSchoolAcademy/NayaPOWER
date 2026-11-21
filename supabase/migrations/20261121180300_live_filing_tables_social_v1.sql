-- Live filing: social tables (Seat 1, TABLES) — Supabase filing round 2026-11-21
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
-- NOTE (Seat 7 reorder, 2026-11-21 — SEAT-6-DECISION B5–B7): the
--   smart_mail_aliases section below now precedes smart_spaces (it was L158–L176):
--   smart_spaces / smart_space_members / user_connections FK to smart_mail_aliases,
--   which did not exist yet at those points (42P01). smart_mail_aliases is PK-only
--   with no FK back to any user table (re-checked first-hand), so the move is
--   cycle-free. Every statement in the moved section is byte-identical; order only.

-- ---------------------------------------------------------------------------
-- Table: public.smart_mail_aliases (4 columns, live)
create table if not exists public."smart_mail_aliases" (
  "alias" text not null,
  "display_name" text not null,
  "kind" text default 'seat'::text not null,
  "created_at" timestamp with time zone default now() not null,
  constraint "smart_mail_aliases_pkey" PRIMARY KEY (alias)
);

alter table public."smart_mail_aliases" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,service_role=arwdDxtm/postgres,anon=r/postgres}

do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='smart_mail_aliases' and policyname='smart_mail_aliases_owner_select') then
    create policy "smart_mail_aliases_owner_select" on public."smart_mail_aliases" as permissive for select to authenticated using ((alias = COALESCE(((auth.jwt() -> 'app_metadata'::text) ->> 'smart_alias'::text), ((auth.jwt() -> 'user_metadata'::text) ->> 'smart_alias'::text))));
  end if;
end $$;

-- ---------------------------------------------------------------------------
-- Table: public.smart_spaces (5 columns, live)
create table if not exists public."smart_spaces" (
  "id" uuid default gen_random_uuid() not null,
  "name" text not null,
  "alias" text not null,
  "description" text,
  "created_at" timestamp with time zone default now() not null,
  constraint "smart_spaces_alias_fkey" FOREIGN KEY (alias) REFERENCES smart_mail_aliases(alias),
  constraint "smart_spaces_pkey" PRIMARY KEY (id),
  constraint "smart_spaces_alias_key" UNIQUE (alias)
);

alter table public."smart_spaces" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,service_role=arwdDxtm/postgres,anon=r/postgres}

do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='smart_spaces' and policyname='pass2_anon_select_smart_spaces') then
    create policy "pass2_anon_select_smart_spaces" on public."smart_spaces" as permissive for select to anon using (true);
  end if;
end $$;

-- ---------------------------------------------------------------------------
-- Table: public.smart_space_members (4 columns, live)
create table if not exists public."smart_space_members" (
  "space_alias" text not null,
  "member_alias" text not null,
  "role" text default 'member'::text not null,
  "joined_at" timestamp with time zone default now() not null,
  constraint "smart_space_members_member_alias_fkey" FOREIGN KEY (member_alias) REFERENCES smart_mail_aliases(alias) ON DELETE CASCADE,
  constraint "smart_space_members_space_alias_fkey" FOREIGN KEY (space_alias) REFERENCES smart_mail_aliases(alias) ON DELETE CASCADE,
  constraint "smart_space_members_pkey" PRIMARY KEY (space_alias, member_alias)
);

alter table public."smart_space_members" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,service_role=arwdDxtm/postgres,anon=r/postgres}

do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='smart_space_members' and policyname='pass2_anon_select_smart_space_members') then
    create policy "pass2_anon_select_smart_space_members" on public."smart_space_members" as permissive for select to anon using (true);
  end if;
end $$;

-- ---------------------------------------------------------------------------
-- Table: public.connections (5 columns, live)
create table if not exists public."connections" (
  "id" uuid default gen_random_uuid() not null,
  "owner_alias" text not null,
  "connected_alias" text not null,
  "status" text default 'pending'::text,
  "created_at" timestamp with time zone default now(),
  constraint "connections_status_check" CHECK ((status = ANY (ARRAY['pending'::text, 'accepted'::text, 'blocked'::text]))),
  constraint "connections_pkey" PRIMARY KEY (id),
  constraint "connections_owner_alias_connected_alias_key" UNIQUE (owner_alias, connected_alias)
);

create index if not exists idx_connections_owner ON public.connections USING btree (owner_alias);

alter table public."connections" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,anon=arwdm/postgres,authenticated=arwdm/postgres,service_role=arwdDxtm/postgres}

do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='connections' and policyname='anon_all_connections') then
    create policy "anon_all_connections" on public."connections" as permissive for all to anon using (true) with check (true);
  end if;
end $$;

-- ---------------------------------------------------------------------------
-- Table: public.user_connections (7 columns, live)
create table if not exists public."user_connections" (
  "id" uuid default gen_random_uuid() not null,
  "display_name" text not null,
  "alias" text not null,
  "relationship" text,
  "notes_ref" text,
  "last_contact_at" timestamp with time zone,
  "created_at" timestamp with time zone default now() not null,
  constraint "user_connections_alias_fkey" FOREIGN KEY (alias) REFERENCES smart_mail_aliases(alias),
  constraint "user_connections_pkey" PRIMARY KEY (id),
  constraint "user_connections_alias_key" UNIQUE (alias)
);

alter table public."user_connections" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,service_role=arwdDxtm/postgres}

-- ---------------------------------------------------------------------------
-- Table: public.smart_mail_threads (11 columns, live)
create table if not exists public."smart_mail_threads" (
  "id" uuid default gen_random_uuid() not null,
  "subject" text not null,
  "from_alias" text not null,
  "to_alias" text not null,
  "preview" text,
  "created_at" timestamp with time zone default now() not null,
  "updated_at" timestamp with time zone default now() not null,
  "owner_alias" text,
  "participants" text,
  "status" text,
  "thread_key" text,
  constraint "smart_mail_threads_pkey" PRIMARY KEY (id)
);

alter table public."smart_mail_threads" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,service_role=arwdDxtm/postgres,anon=arw/postgres,authenticated=r/postgres}

do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='smart_mail_threads' and policyname='smart_mail_threads_owner_select') then
    create policy "smart_mail_threads_owner_select" on public."smart_mail_threads" as permissive for select to authenticated using (((from_alias = COALESCE(((auth.jwt() -> 'app_metadata'::text) ->> 'smart_alias'::text), ((auth.jwt() -> 'user_metadata'::text) ->> 'smart_alias'::text))) OR (to_alias = COALESCE(((auth.jwt() -> 'app_metadata'::text) ->> 'smart_alias'::text), ((auth.jwt() -> 'user_metadata'::text) ->> 'smart_alias'::text)))));
  end if;
end $$;

-- ---------------------------------------------------------------------------
-- Table: public.smart_mail_messages (9 columns, live)
create table if not exists public."smart_mail_messages" (
  "id" uuid default gen_random_uuid() not null,
  "thread_id" uuid not null,
  "from_alias" text not null,
  "body" text not null,
  "created_at" timestamp with time zone default now() not null,
  "thread_key" text,
  "direction" text,
  "sender_name" text,
  "sender" text,
  constraint "smart_mail_messages_thread_id_fkey" FOREIGN KEY (thread_id) REFERENCES smart_mail_threads(id) ON DELETE CASCADE,
  constraint "smart_mail_messages_pkey" PRIMARY KEY (id)
);

alter table public."smart_mail_messages" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,service_role=arwdDxtm/postgres,anon=arw/postgres,authenticated=rd/postgres}

do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='smart_mail_messages' and policyname='smart_mail_messages_owner_delete') then
    create policy "smart_mail_messages_owner_delete" on public."smart_mail_messages" as permissive for delete to authenticated using ((from_alias = COALESCE(((auth.jwt() -> 'app_metadata'::text) ->> 'smart_alias'::text), ((auth.jwt() -> 'user_metadata'::text) ->> 'smart_alias'::text))));
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='smart_mail_messages' and policyname='smart_mail_messages_owner_select') then
    create policy "smart_mail_messages_owner_select" on public."smart_mail_messages" as permissive for select to authenticated using ((from_alias = COALESCE(((auth.jwt() -> 'app_metadata'::text) ->> 'smart_alias'::text), ((auth.jwt() -> 'user_metadata'::text) ->> 'smart_alias'::text))));
  end if;
end $$;

-- ---------------------------------------------------------------------------
-- Table: public.messenger_messages (8 columns, live)
create table if not exists public."messenger_messages" (
  "id" uuid default gen_random_uuid() not null,
  "thread_id" uuid,
  "from_alias" text not null,
  "to_alias" text not null,
  "body" text not null,
  "sent_at" timestamp with time zone default now() not null,
  "read_at" timestamp with time zone,
  "created_at" timestamp with time zone default now() not null,
  constraint "messenger_messages_thread_id_fkey" FOREIGN KEY (thread_id) REFERENCES smart_mail_threads(id) ON DELETE CASCADE,
  constraint "messenger_messages_pkey" PRIMARY KEY (id)
);

create index if not exists idx_messenger_thread ON public.messenger_messages USING btree (thread_id, sent_at);
create index if not exists idx_messenger_to ON public.messenger_messages USING btree (to_alias, sent_at);

alter table public."messenger_messages" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,anon=arwdDxtm/postgres,authenticated=arwdDxtm/postgres,service_role=arwdDxtm/postgres}

-- ---------------------------------------------------------------------------
-- Table: public.pending_email_sends (8 columns, live)
create table if not exists public."pending_email_sends" (
  "id" uuid default gen_random_uuid() not null,
  "to_email" text not null,
  "subject" text not null,
  "body" text not null,
  "created_at" timestamp with time zone default now() not null,
  "sent_at" timestamp with time zone,
  "attempts" integer default 0 not null,
  "last_error" text,
  constraint "pending_email_sends_pkey" PRIMARY KEY (id)
);

create index if not exists idx_pes_unsent ON public.pending_email_sends USING btree (created_at) WHERE (sent_at IS NULL);

alter table public."pending_email_sends" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,anon=arwdDxtm/postgres,authenticated=arwdDxtm/postgres,service_role=arwdDxtm/postgres}

-- ---------------------------------------------------------------------------
-- Table: public.invite_send_log (7 columns, live)
create table if not exists public."invite_send_log" (
  "id" uuid default gen_random_uuid() not null,
  "invite_id" uuid not null,
  "rendered_subject" text not null,
  "rendered_body" text not null,
  "provider" text not null,
  "message_id" text,
  "at" timestamp with time zone default now() not null,
  constraint "invite_send_log_invite_id_fkey" FOREIGN KEY (invite_id) REFERENCES invites(id) ON DELETE CASCADE,
  constraint "invite_send_log_pkey" PRIMARY KEY (id)
);

create index if not exists idx_invite_send_log_invite ON public.invite_send_log USING btree (invite_id);

alter table public."invite_send_log" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,service_role=arwdDxtm/postgres}
