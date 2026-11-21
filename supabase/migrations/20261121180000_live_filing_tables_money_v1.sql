-- Live filing: money tables (Seat 1, TABLES) — Supabase filing round 2026-11-21
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
-- NOTE (Seat 7 reorder, 2026-11-21 — SEAT-6-DECISION B2): the payment_links
--   section below now precedes payments (it was L99–L147, before payment_connections):
--   payments L61 FKs to payment_links, which did not exist yet at that point (42P01).
--   payment_links has no FK back to payments (re-checked first-hand), so the move is
--   cycle-free. Every statement in the moved section is byte-identical; order only.

-- ---------------------------------------------------------------------------
-- Table: public.smart_link_joins (6 columns, live)
create table if not exists public."smart_link_joins" (
  "id" uuid default gen_random_uuid() not null,
  "link_id" uuid not null,
  "joined_alias" text,
  "invite_code" text,
  "source" text default 'cookie'::text not null,
  "joined_at" timestamp with time zone default now() not null,
  constraint "smart_link_joins_link_id_fkey" FOREIGN KEY (link_id) REFERENCES smart_links(id) ON DELETE CASCADE,
  constraint "smart_link_joins_pkey" PRIMARY KEY (id)
);

create index if not exists smart_link_joins_link_time_idx ON public.smart_link_joins USING btree (link_id, joined_at);

alter table public."smart_link_joins" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,service_role=arwdDxtm/postgres,anon=a/postgres}

do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='smart_link_joins' and policyname='smart_link_joins_append') then
    create policy "smart_link_joins_append" on public."smart_link_joins" as permissive for insert to anon with check (true);
  end if;
end $$;

-- ---------------------------------------------------------------------------
-- Table: public.payment_links (12 columns, live)
create table if not exists public."payment_links" (
  "id" uuid default gen_random_uuid() not null,
  "owner_alias" text not null,
  "owner_id" uuid,
  "slug" text not null,
  "title" text not null,
  "description" text,
  "amount_cents" integer not null,
  "currency" text default 'usd'::text not null,
  "smart_link_name" text,
  "active" boolean default true not null,
  "created_at" timestamp with time zone default now() not null,
  "updated_at" timestamp with time zone default now() not null,
  constraint "payment_links_amount_positive" CHECK ((amount_cents > 0)),
  constraint "payment_links_currency_shape" CHECK ((char_length(currency) = 3)),
  constraint "payment_links_slug_shape" CHECK ((slug ~ '^[a-z0-9][a-z0-9-]{1,62}$'::text)),
  constraint "payment_links_title_nonempty" CHECK ((char_length(btrim(title)) > 0)),
  constraint "payment_links_pkey" PRIMARY KEY (id)
);

create index if not exists payment_links_owner_idx ON public.payment_links USING btree (owner_alias, created_at DESC);
create UNIQUE index if not exists payment_links_slug_unique ON public.payment_links USING btree (lower(slug));

alter table public."payment_links" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,anon=arwdDxtm/postgres,authenticated=arwdDxtm/postgres,service_role=arwdDxtm/postgres}

do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='payment_links' and policyname='payment_links_owner_delete') then
    create policy "payment_links_owner_delete" on public."payment_links" as permissive for delete to authenticated using ((owner_id = ( SELECT auth.uid() AS uid)));
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='payment_links' and policyname='payment_links_owner_insert') then
    create policy "payment_links_owner_insert" on public."payment_links" as permissive for insert to authenticated with check ((owner_id = ( SELECT auth.uid() AS uid)));
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='payment_links' and policyname='payment_links_owner_select') then
    create policy "payment_links_owner_select" on public."payment_links" as permissive for select to authenticated using ((owner_id = ( SELECT auth.uid() AS uid)));
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='payment_links' and policyname='payment_links_owner_update') then
    create policy "payment_links_owner_update" on public."payment_links" as permissive for update to authenticated using ((owner_id = ( SELECT auth.uid() AS uid))) with check ((owner_id = ( SELECT auth.uid() AS uid)));
  end if;
end $$;

-- ---------------------------------------------------------------------------
-- Table: public.payments (14 columns, live)
create table if not exists public."payments" (
  "id" uuid default gen_random_uuid() not null,
  "link_id" uuid not null,
  "owner_alias" text not null,
  "owner_id" uuid,
  "status" text default 'pending'::text not null,
  "amount_cents" integer not null,
  "currency" text default 'usd'::text not null,
  "buyer_name" text,
  "buyer_email_hash" text,
  "smart_link_name" text,
  "provider" text default 'stripe'::text not null,
  "provider_ref" text,
  "failure_reason" text,
  "created_at" timestamp with time zone default now() not null,
  constraint "payments_amount_nonneg" CHECK ((amount_cents >= 0)),
  constraint "payments_currency_shape" CHECK ((char_length(currency) = 3)),
  constraint "payments_status_known" CHECK ((status = ANY (ARRAY['succeeded'::text, 'failed'::text, 'pending'::text, 'refunded'::text]))),
  constraint "payments_link_id_fkey" FOREIGN KEY (link_id) REFERENCES payment_links(id) ON DELETE CASCADE,
  constraint "payments_pkey" PRIMARY KEY (id)
);

create index if not exists payments_link_time_idx ON public.payments USING btree (link_id, created_at DESC);
create index if not exists payments_owner_time_idx ON public.payments USING btree (owner_alias, created_at DESC);

alter table public."payments" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,anon=arwdDxtm/postgres,authenticated=arwdDxtm/postgres,service_role=arwdDxtm/postgres}

do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='payments' and policyname='payments_owner_delete') then
    create policy "payments_owner_delete" on public."payments" as permissive for delete to authenticated using ((owner_id = ( SELECT auth.uid() AS uid)));
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='payments' and policyname='payments_owner_insert') then
    create policy "payments_owner_insert" on public."payments" as permissive for insert to authenticated with check ((owner_id = ( SELECT auth.uid() AS uid)));
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='payments' and policyname='payments_owner_select') then
    create policy "payments_owner_select" on public."payments" as permissive for select to authenticated using ((owner_id = ( SELECT auth.uid() AS uid)));
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='payments' and policyname='payments_owner_update') then
    create policy "payments_owner_update" on public."payments" as permissive for update to authenticated using ((owner_id = ( SELECT auth.uid() AS uid))) with check ((owner_id = ( SELECT auth.uid() AS uid)));
  end if;
end $$;

-- trigger payments_fill_owner on payments
do $$ begin
  if not exists (select 1 from pg_trigger where tgname='payments_fill_owner' and tgrelid='public."payments"'::regclass) then
    CREATE TRIGGER payments_fill_owner BEFORE INSERT ON public.payments FOR EACH ROW EXECUTE FUNCTION payments_fill_owner();
  end if;
end $$;

-- ---------------------------------------------------------------------------
-- Table: public.payment_connections (7 columns, live)
create table if not exists public."payment_connections" (
  "owner_alias" text not null,
  "owner_id" uuid,
  "provider" text default 'stripe'::text not null,
  "state" text default 'not_connected'::text not null,
  "account_label" text,
  "connected_at" timestamp with time zone,
  "updated_at" timestamp with time zone default now() not null,
  constraint "payment_connections_state_known" CHECK ((state = ANY (ARRAY['not_connected'::text, 'test'::text, 'connected'::text]))),
  constraint "payment_connections_pkey" PRIMARY KEY (owner_alias)
);

alter table public."payment_connections" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,anon=arwdDxtm/postgres,authenticated=arwdDxtm/postgres,service_role=arwdDxtm/postgres}

do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='payment_connections' and policyname='payment_connections_owner_delete') then
    create policy "payment_connections_owner_delete" on public."payment_connections" as permissive for delete to authenticated using ((owner_id = ( SELECT auth.uid() AS uid)));
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='payment_connections' and policyname='payment_connections_owner_insert') then
    create policy "payment_connections_owner_insert" on public."payment_connections" as permissive for insert to authenticated with check ((owner_id = ( SELECT auth.uid() AS uid)));
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='payment_connections' and policyname='payment_connections_owner_select') then
    create policy "payment_connections_owner_select" on public."payment_connections" as permissive for select to authenticated using ((owner_id = ( SELECT auth.uid() AS uid)));
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='payment_connections' and policyname='payment_connections_owner_update') then
    create policy "payment_connections_owner_update" on public."payment_connections" as permissive for update to authenticated using ((owner_id = ( SELECT auth.uid() AS uid))) with check ((owner_id = ( SELECT auth.uid() AS uid)));
  end if;
end $$;

-- ---------------------------------------------------------------------------
-- Table: public.products_services (14 columns, live)
create table if not exists public."products_services" (
  "id" uuid default gen_random_uuid() not null,
  "page_kind" text not null,
  "page_alias" text not null,
  "owner_alias" text not null,
  "kind" text not null,
  "name" text not null,
  "description" text,
  "cover_url" text,
  "price_cents" integer default 0 not null,
  "currency" text default 'USD'::text not null,
  "payment_link_id" uuid,
  "active" boolean default true not null,
  "created_at" timestamp with time zone default now() not null,
  "updated_at" timestamp with time zone default now() not null,
  constraint "products_services_kind_check" CHECK ((kind = ANY (ARRAY['product'::text, 'service'::text]))),
  constraint "products_services_page_kind_check" CHECK ((page_kind = ANY (ARRAY['personal'::text, 'business'::text, 'space'::text]))),
  constraint "products_services_payment_link_id_fkey" FOREIGN KEY (payment_link_id) REFERENCES payment_links(id) ON DELETE SET NULL,
  constraint "products_services_pkey" PRIMARY KEY (id)
);

create index if not exists idx_products_services_page ON public.products_services USING btree (page_kind, page_alias);

alter table public."products_services" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,anon=arwdDxtm/postgres,authenticated=arwdDxtm/postgres,service_role=arwdDxtm/postgres}

do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='products_services' and policyname='ps_public_sel') then
    create policy "ps_public_sel" on public."products_services" as permissive for select to anon using ((active = true));
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='products_services' and policyname='ps_sel_anon') then
    create policy "ps_sel_anon" on public."products_services" as permissive for select to anon using ((active = true));
  end if;
end $$;

-- ---------------------------------------------------------------------------
-- Table: public.page_about (9 columns, live)
create table if not exists public."page_about" (
  "id" uuid default gen_random_uuid() not null,
  "page_kind" text not null,
  "page_alias" text not null,
  "owner_alias" text not null,
  "headline" text,
  "body" text,
  "cover_url" text,
  "created_at" timestamp with time zone default now() not null,
  "updated_at" timestamp with time zone default now() not null,
  constraint "page_about_page_kind_check" CHECK ((page_kind = ANY (ARRAY['personal'::text, 'business'::text, 'space'::text]))),
  constraint "page_about_pkey" PRIMARY KEY (id),
  constraint "page_about_page_kind_page_alias_key" UNIQUE (page_kind, page_alias)
);

alter table public."page_about" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,anon=arwdDxtm/postgres,authenticated=arwdDxtm/postgres,service_role=arwdDxtm/postgres}

do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='page_about' and policyname='pa_public_sel') then
    create policy "pa_public_sel" on public."page_about" as permissive for select to anon using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='page_about' and policyname='pa_sel_anon') then
    create policy "pa_sel_anon" on public."page_about" as permissive for select to anon using (true);
  end if;
end $$;

-- ---------------------------------------------------------------------------
-- Table: public.invites (14 columns, live)
create table if not exists public."invites" (
  "id" uuid default gen_random_uuid() not null,
  "code" text default gen_invite_code() not null,
  "inviter_alias" text not null,
  "invitee_name" text default ''::text not null,
  "invitee_email_hash" text not null,
  "status" text default 'pending'::text not null,
  "template_id" text default 'template_warm'::text not null,
  "dry_run" boolean default true not null,
  "created_at" timestamp with time zone default now() not null,
  "sent_at" timestamp with time zone,
  "visited_at" timestamp with time zone,
  "joined_at" timestamp with time zone,
  "nudged_at" timestamp with time zone,
  "owner_alias" text,
  constraint "invites_status_check" CHECK ((status = ANY (ARRAY['pending'::text, 'queued'::text, 'sent'::text, 'visited'::text, 'joined'::text, 'nudged'::text]))),
  constraint "invites_pkey" PRIMARY KEY (id),
  constraint "invites_code_key" UNIQUE (code)
);

create index if not exists idx_invites_alias ON public.invites USING btree (inviter_alias);
create index if not exists idx_invites_code ON public.invites USING btree (code);

alter table public."invites" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,service_role=arwdDxtm/postgres,anon=arw/postgres,authenticated=rd/postgres}

do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='invites' and policyname='invites_owner_delete') then
    create policy "invites_owner_delete" on public."invites" as permissive for delete to authenticated using ((inviter_alias = COALESCE(((auth.jwt() -> 'app_metadata'::text) ->> 'smart_alias'::text), ((auth.jwt() -> 'user_metadata'::text) ->> 'smart_alias'::text))));
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='invites' and policyname='invites_owner_select') then
    create policy "invites_owner_select" on public."invites" as permissive for select to authenticated using ((inviter_alias = COALESCE(((auth.jwt() -> 'app_metadata'::text) ->> 'smart_alias'::text), ((auth.jwt() -> 'user_metadata'::text) ->> 'smart_alias'::text))));
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='invites' and policyname='pass2_anon_insert_invites') then
    create policy "pass2_anon_insert_invites" on public."invites" as permissive for insert to anon with check (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='invites' and policyname='pass2_anon_select_invites') then
    create policy "pass2_anon_select_invites" on public."invites" as permissive for select to anon using (true);
  end if;
end $$;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname='public' and tablename='invites' and policyname='pass2_anon_update_invites') then
    create policy "pass2_anon_update_invites" on public."invites" as permissive for update to anon using (true) with check (true);
  end if;
end $$;

-- ---------------------------------------------------------------------------
-- Table: public.ambassador_links (5 columns, live)
create table if not exists public."ambassador_links" (
  "alias" text not null,
  "link_url" text not null,
  "issued_at" timestamp with time zone default now() not null,
  "status" text default 'active'::text not null,
  "paypal_email" text,
  constraint "ambassador_links_pkey" PRIMARY KEY (alias)
);

alter table public."ambassador_links" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,authenticated=arwdDxtm/postgres,service_role=arwdDxtm/postgres}

-- ---------------------------------------------------------------------------
-- Table: public.ambassador_events (9 columns, live)
create table if not exists public."ambassador_events" (
  "id" uuid default gen_random_uuid() not null,
  "alias" text not null,
  "kind" text not null,
  "visitor_key" text,
  "subject_ref" text,
  "amount_cents" integer,
  "currency" text,
  "source" text,
  "created_at" timestamp with time zone default now() not null,
  constraint "ambassador_events_kind_check" CHECK ((kind = ANY (ARRAY['click'::text, 'signup'::text, 'sale'::text, 'refund'::text, 'payout'::text]))),
  constraint "ambassador_events_pkey" PRIMARY KEY (id)
);

alter table public."ambassador_events" enable row level security;
-- live ACL (recorded verbatim, not applied as grants): {postgres=arwdDxtm/postgres,authenticated=arwdDxtm/postgres,service_role=arwdDxtm/postgres}

-- ---------------------------------------------------------------------------
-- View: public.smart_link_daily_stats (live)
create or replace view public."smart_link_daily_stats" as
SELECT l.id AS link_id,
    l.owner_alias,
    l.name,
    x.day,
    sum(x.clicks)::bigint AS clicks,
    sum(x.joins)::bigint AS joins
   FROM smart_links l
     JOIN ( SELECT smart_link_clicks.link_id,
            smart_link_clicks.clicked_at::date AS day,
            count(*) AS clicks,
            0::bigint AS joins
           FROM smart_link_clicks
          GROUP BY smart_link_clicks.link_id, (smart_link_clicks.clicked_at::date)
        UNION ALL
         SELECT smart_link_joins.link_id,
            smart_link_joins.joined_at::date AS day,
            0::bigint AS int8,
            count(*) AS count
           FROM smart_link_joins
          GROUP BY smart_link_joins.link_id, (smart_link_joins.joined_at::date)) x ON x.link_id = l.id
  GROUP BY l.id, l.owner_alias, l.name, x.day;

-- ---------------------------------------------------------------------------
-- View: public.smart_link_dimension_stats (live)
create or replace view public."smart_link_dimension_stats" as
SELECT l.id AS link_id,
    l.owner_alias,
    l.name,
    c.clicked_at::date AS day,
    c.referrer_class,
    c.user_agent_class,
    c.country,
    count(*) AS clicks
   FROM smart_link_clicks c
     JOIN smart_links l ON l.id = c.link_id
  GROUP BY l.id, l.owner_alias, l.name, (c.clicked_at::date), c.referrer_class, c.user_agent_class, c.country;
