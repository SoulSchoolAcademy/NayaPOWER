-- Live filing: membership tables (Seat 1, TABLES) — Supabase filing round 2026-11-21
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

-- Sequences owned by columns in this group (live pg_sequences values).
create sequence if not exists public."nayanet_identities_cert_no_seq" as bigint increment by 1 minvalue 1 maxvalue 9223372036854775807 start with 1 cache 1 no cycle;
alter sequence public."nayanet_identities_cert_no_seq" owned by public."nayanet_identities"."cert_no";

-- ---------------------------------------------------------------------------
-- Table: public.memberships (15 columns, live)
create table if not exists public."memberships" (
  "id" uuid default gen_random_uuid() not null,
  "page_kind" text not null,
  "page_alias" text not null,
  "owner_alias" text not null,
  "name" text not null,
  "slug" text not null,
  "description" text,
  "cover_url" text,
  "access_type" text default 'free'::text not null,
  "price_cents" integer default 0 not null,
  "currency" text default 'USD'::text not null,
  "payment_link_id" uuid,
  "active" boolean default true not null,
  "created_at" timestamp with time zone default now() not null,
  "updated_at" timestamp with time zone default now() not null,
  constraint "memberships_access_type_check" CHECK ((access_type = ANY (ARRAY['free'::text, 'paid'::text, 'invite'::text]))),
  constraint "memberships_page_kind_check" CHECK ((page_kind = ANY (ARRAY['personal'::text, 'business'::text, 'space'::text]))),
  constraint "memberships_payment_link_id_fkey" FOREIGN KEY (payment_link_id) REFERENCES payment_links(id) ON DELETE SET NULL,
  constraint "memberships_pkey" PRIMARY KEY (id),
  constraint "memberships_page_kind_page_alias_slug_key" UNIQUE (page_kind, page_alias, slug)
);

create index if not exists idx_memberships_owner ON public.memberships USING btree (owner_alias);
create index if not exists idx_memberships_page ON public.memberships USING btree (page_kind, page_alias);

alter table public."memberships" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,anon=arwdDxtm/postgres,authenticated=arwdDxtm/postgres,service_role=arwdDxtm/postgres}

do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='memberships' and policyname='mship_public_sel') then
    create policy "mship_public_sel" on public."memberships" as permissive for select to anon using ((active = true));
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='memberships' and policyname='mship_sel_anon') then
    create policy "mship_sel_anon" on public."memberships" as permissive for select to anon using ((active = true));
  end if;
end $$;

-- ---------------------------------------------------------------------------
-- Table: public.membership_members (9 columns, live)
create table if not exists public."membership_members" (
  "id" uuid default gen_random_uuid() not null,
  "membership_id" uuid not null,
  "member_alias" text not null,
  "status" text default 'active'::text not null,
  "joined_at" timestamp with time zone default now() not null,
  "expires_at" timestamp with time zone,
  "last_login_at" timestamp with time zone,
  "created_at" timestamp with time zone default now() not null,
  "updated_at" timestamp with time zone default now() not null,
  constraint "membership_members_status_check" CHECK ((status = ANY (ARRAY['active'::text, 'pending'::text, 'cancelled'::text, 'expired'::text]))),
  constraint "membership_members_membership_id_fkey" FOREIGN KEY (membership_id) REFERENCES memberships(id) ON DELETE CASCADE,
  constraint "membership_members_pkey" PRIMARY KEY (id),
  constraint "membership_members_membership_id_member_alias_key" UNIQUE (membership_id, member_alias)
);

create index if not exists idx_mship_members_alias ON public.membership_members USING btree (member_alias);
create index if not exists idx_mship_members_mship ON public.membership_members USING btree (membership_id);

alter table public."membership_members" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,anon=arwdDxtm/postgres,authenticated=arwdDxtm/postgres,service_role=arwdDxtm/postgres}

-- ---------------------------------------------------------------------------
-- Table: public.membership_content (13 columns, live)
create table if not exists public."membership_content" (
  "id" uuid default gen_random_uuid() not null,
  "membership_id" uuid not null,
  "kind" text not null,
  "title" text not null,
  "description" text,
  "media_url" text,
  "thumbnail_url" text,
  "duration_seconds" integer,
  "position" integer default 0 not null,
  "drip_days" integer,
  "published" boolean default true not null,
  "created_at" timestamp with time zone default now() not null,
  "updated_at" timestamp with time zone default now() not null,
  constraint "membership_content_kind_check" CHECK ((kind = ANY (ARRAY['video'::text, 'pdf'::text, 'audio'::text, 'note'::text, 'link'::text]))),
  constraint "membership_content_membership_id_fkey" FOREIGN KEY (membership_id) REFERENCES memberships(id) ON DELETE CASCADE,
  constraint "membership_content_pkey" PRIMARY KEY (id)
);

create index if not exists idx_mship_content_mship ON public.membership_content USING btree (membership_id, "position");

alter table public."membership_content" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,anon=arwdDxtm/postgres,authenticated=arwdDxtm/postgres,service_role=arwdDxtm/postgres}

-- ---------------------------------------------------------------------------
-- Table: public.membership_member_emails (5 columns, live)
create table if not exists public."membership_member_emails" (
  "membership_id" uuid not null,
  "member_alias" text not null,
  "email_hash" text not null,
  "verified_at" timestamp with time zone,
  "created_at" timestamp with time zone default now() not null,
  constraint "membership_member_emails_membership_id_fkey" FOREIGN KEY (membership_id) REFERENCES memberships(id) ON DELETE CASCADE,
  constraint "membership_member_emails_membership_id_member_alias_fkey" FOREIGN KEY (membership_id, member_alias) REFERENCES membership_members(membership_id, member_alias) ON DELETE CASCADE,
  constraint "membership_member_emails_pkey" PRIMARY KEY (membership_id, member_alias)
);

alter table public."membership_member_emails" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,anon=arwdDxtm/postgres,authenticated=arwdDxtm/postgres,service_role=arwdDxtm/postgres}

-- ---------------------------------------------------------------------------
-- Table: public.membership_code_prefs (6 columns, live)
create table if not exists public."membership_code_prefs" (
  "membership_id" uuid not null,
  "member_alias" text not null,
  "email" text,
  "wants_email_codes" boolean default false not null,
  "created_at" timestamp with time zone default now() not null,
  "updated_at" timestamp with time zone default now() not null,
  constraint "membership_code_prefs_membership_id_fkey" FOREIGN KEY (membership_id) REFERENCES memberships(id) ON DELETE CASCADE,
  constraint "membership_code_prefs_membership_id_member_alias_fkey" FOREIGN KEY (membership_id, member_alias) REFERENCES membership_members(membership_id, member_alias) ON DELETE CASCADE,
  constraint "membership_code_prefs_pkey" PRIMARY KEY (membership_id, member_alias)
);

create index if not exists idx_mcp_email ON public.membership_code_prefs USING btree (wants_email_codes) WHERE (wants_email_codes = true);

alter table public."membership_code_prefs" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,anon=arwdDxtm/postgres,authenticated=arwdDxtm/postgres,service_role=arwdDxtm/postgres}

-- ---------------------------------------------------------------------------
-- Table: public.membership_invites (8 columns, live)
create table if not exists public."membership_invites" (
  "id" uuid default gen_random_uuid() not null,
  "membership_id" uuid not null,
  "code_hash" text not null,
  "max_uses" integer default 1 not null,
  "uses" integer default 0 not null,
  "expires_at" timestamp with time zone,
  "created_by_alias" text not null,
  "created_at" timestamp with time zone default now() not null,
  constraint "membership_invites_max_uses_check" CHECK ((max_uses >= 1)),
  constraint "membership_invites_uses_check" CHECK ((uses >= 0)),
  constraint "membership_invites_membership_id_fkey" FOREIGN KEY (membership_id) REFERENCES memberships(id) ON DELETE CASCADE,
  constraint "membership_invites_pkey" PRIMARY KEY (id),
  constraint "membership_invites_code_hash_key" UNIQUE (code_hash)
);

create index if not exists idx_minv_mship ON public.membership_invites USING btree (membership_id);

alter table public."membership_invites" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,anon=arwdDxtm/postgres,authenticated=arwdDxtm/postgres,service_role=arwdDxtm/postgres}

-- ---------------------------------------------------------------------------
-- Table: public.member_sessions (8 columns, live)
create table if not exists public."member_sessions" (
  "id" uuid default gen_random_uuid() not null,
  "kind" text not null,
  "alias" text not null,
  "membership_id" uuid,
  "token_hash" text not null,
  "expires_at" timestamp with time zone not null,
  "revoked_at" timestamp with time zone,
  "created_at" timestamp with time zone default now() not null,
  constraint "member_sessions_check" CHECK ((((kind = 'owner'::text) AND (membership_id IS NULL)) OR ((kind = 'member'::text) AND (membership_id IS NOT NULL)))),
  constraint "member_sessions_kind_check" CHECK ((kind = ANY (ARRAY['owner'::text, 'member'::text]))),
  constraint "member_sessions_membership_id_fkey" FOREIGN KEY (membership_id) REFERENCES memberships(id) ON DELETE CASCADE,
  constraint "member_sessions_pkey" PRIMARY KEY (id),
  constraint "member_sessions_token_hash_key" UNIQUE (token_hash)
);

create index if not exists idx_msess_alias ON public.member_sessions USING btree (alias, kind);
create index if not exists idx_msess_token ON public.member_sessions USING btree (token_hash) WHERE (revoked_at IS NULL);

alter table public."member_sessions" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,anon=arwdDxtm/postgres,authenticated=arwdDxtm/postgres,service_role=arwdDxtm/postgres}

-- ---------------------------------------------------------------------------
-- Table: public.member_otp_codes (7 columns, live)
create table if not exists public."member_otp_codes" (
  "id" uuid default gen_random_uuid() not null,
  "membership_id" uuid not null,
  "member_alias" text not null,
  "code_hash" text not null,
  "expires_at" timestamp with time zone not null,
  "consumed_at" timestamp with time zone,
  "created_at" timestamp with time zone default now() not null,
  constraint "member_otp_codes_membership_id_fkey" FOREIGN KEY (membership_id) REFERENCES memberships(id) ON DELETE CASCADE,
  constraint "member_otp_codes_pkey" PRIMARY KEY (id)
);

create index if not exists idx_otp_alias ON public.member_otp_codes USING btree (membership_id, member_alias, created_at DESC);

alter table public."member_otp_codes" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,anon=arwdDxtm/postgres,authenticated=arwdDxtm/postgres,service_role=arwdDxtm/postgres}

-- ---------------------------------------------------------------------------
-- Table: public.member_email_tokens (6 columns, live)
create table if not exists public."member_email_tokens" (
  "alias" text not null,
  "provider" text not null,
  "refresh_token_enc" text not null,
  "updated_at" timestamp with time zone default now() not null,
  "email" text,
  "scopes" text,
  constraint "member_email_tokens_provider_check" CHECK ((provider = ANY (ARRAY['google'::text, 'microsoft'::text]))),
  constraint "member_email_tokens_pkey" PRIMARY KEY (alias)
);

alter table public."member_email_tokens" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,service_role=arwdDxtm/postgres}

-- ---------------------------------------------------------------------------
-- Table: public.citizen_tiers (3 columns, live)
create table if not exists public."citizen_tiers" (
  "alias" text not null,
  "tier" text default 'free'::text not null,
  "updated_at" timestamp with time zone default now() not null,
  constraint "citizen_tiers_tier_check" CHECK ((tier = ANY (ARRAY['free'::text, 'power'::text, 'pro'::text, 'max'::text]))),
  constraint "citizen_tiers_pkey" PRIMARY KEY (alias)
);

alter table public."citizen_tiers" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,anon=arwdDxtm/postgres,authenticated=arwdDxtm/postgres,service_role=arwdDxtm/postgres}

do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='citizen_tiers' and policyname='citizen_tiers_owner_read') then
    create policy "citizen_tiers_owner_read" on public."citizen_tiers" as permissive for select to authenticated using ((alias = ((current_setting('request.jwt.claims'::text, true))::jsonb ->> 'alias'::text)));
  end if;
end $$;

-- ---------------------------------------------------------------------------
-- Table: public.nayanet_identities (5 columns, live)
create table if not exists public."nayanet_identities" (
  "alias" text not null,
  "name" text,
  "device_key" text not null,
  "created_at" timestamp with time zone default now() not null,
  "cert_no" bigint default nextval('nayanet_identities_cert_no_seq'::regclass) not null,
  constraint "nayanet_identities_pkey" PRIMARY KEY (alias)
);

create UNIQUE index if not exists nayanet_identities_cert_no_key ON public.nayanet_identities USING btree (cert_no);

alter table public."nayanet_identities" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,anon=arwdDxtm/postgres,authenticated=arwdDxtm/postgres,service_role=arwdDxtm/postgres}

do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='nayanet_identities' and policyname='anon_insert_nayanet_identities') then
    create policy "anon_insert_nayanet_identities" on public."nayanet_identities" as permissive for insert to anon with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='nayanet_identities' and policyname='anon_select_nayanet_identities') then
    create policy "anon_select_nayanet_identities" on public."nayanet_identities" as permissive for select to anon using (true);
  end if;
end $$;

-- ---------------------------------------------------------------------------
-- Table: public.login_attempts (4 columns, live)
create table if not exists public."login_attempts" (
  "id" uuid default gen_random_uuid() not null,
  "alias" text not null,
  "attempted_at" timestamp with time zone default now() not null,
  "ok" boolean default false not null,
  constraint "login_attempts_pkey" PRIMARY KEY (id)
);

create index if not exists idx_login_att_alias ON public.login_attempts USING btree (alias, attempted_at DESC);

alter table public."login_attempts" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,anon=arwdDxtm/postgres,authenticated=arwdDxtm/postgres,service_role=arwdDxtm/postgres}
