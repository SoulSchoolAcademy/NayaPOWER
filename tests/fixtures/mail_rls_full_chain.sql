-- Complete synthetic pre-migration baseline for GT-039 four-migration test.
-- No private data, no production keys or remote SQL execution.
CREATE ROLE anon;
CREATE ROLE authenticated;
CREATE SCHEMA auth;
CREATE FUNCTION auth.jwt() RETURNS jsonb LANGUAGE sql STABLE
AS $$ SELECT coalesce(nullif(current_setting('request.jwt.claims', true), '')::jsonb, '{}'::jsonb) $$;
CREATE FUNCTION auth.uid() RETURNS uuid LANGUAGE sql STABLE
AS $$ SELECT nullif(current_setting('request.jwt.claim.sub', true), '')::uuid $$;
GRANT USAGE ON SCHEMA auth TO authenticated, anon;
GRANT EXECUTE ON FUNCTION auth.jwt() TO authenticated, anon;
GRANT EXECUTE ON FUNCTION auth.uid() TO authenticated, anon;
-- Read-only catalog observation of live Supabase defaults on 2026-11-11:
-- postgres + supabase_admin both grant table ALL to anon/authenticated
-- in public by default. Local PGlite must emulate these grants, which
-- the app's RLS policies subsequently narrow. These are test-only grants.
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO anon, authenticated;
CREATE TABLE public.person_identities(
 person_key text PRIMARY KEY,owner_id uuid,owner_alias text,display_name text,
 last_seen_at timestamptz,created_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE public.naya_notes(
 id uuid PRIMARY KEY, owner_id uuid,owner_alias text, "text" text,
 category text,list_name text,created_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE public.smart_links(
 id uuid PRIMARY KEY,owner_id uuid,owner_alias text,name text,target_url text,
 active boolean NOT NULL DEFAULT true,created_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE public.smart_notes(
 owner_alias text,content text,author_name text,sender_name text,
 created_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE public.smart_mail_threads(
 id uuid PRIMARY KEY,thread_key text,to_alias text, owner_alias text,
 subject text,participants jsonb, updated_at timestamptz,
 created_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE public.smart_mail_messages(
 id uuid PRIMARY KEY,thread_id uuid REFERENCES public.smart_mail_threads(id),
 from_alias text
);
CREATE FUNCTION public.search_score(needle text,query text)
RETURNS double precision LANGUAGE sql IMMUTABLE
AS $$ SELECT CASE WHEN lower(coalesce(needle,'')) LIKE '%'||lower(query)||'%' THEN 1.0 ELSE 0.0 END $$;
GRANT SELECT, INSERT, UPDATE ON public.smart_mail_messages, public.smart_mail_threads TO anon;
GRANT SELECT, DELETE ON public.smart_mail_messages TO authenticated;
GRANT SELECT ON public.smart_mail_threads TO authenticated;
ALTER TABLE public.smart_mail_threads ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.smart_mail_messages ENABLE ROW LEVEL SECURITY;
CREATE POLICY pass2_anon_select_smart_mail_messages ON public.smart_mail_messages FOR SELECT TO anon USING (true);
CREATE POLICY pass2_anon_insert_smart_mail_messages ON public.smart_mail_messages FOR INSERT TO anon WITH CHECK (true);
CREATE POLICY pass2_anon_update_smart_mail_messages ON public.smart_mail_messages FOR UPDATE TO anon USING (true);
CREATE POLICY pass2_anon_select_smart_mail_threads ON public.smart_mail_threads FOR SELECT TO anon USING (true);
CREATE POLICY pass2_anon_insert_smart_mail_threads ON public.smart_mail_threads FOR INSERT TO anon WITH CHECK (true);
CREATE POLICY pass2_anon_update_smart_mail_threads ON public.smart_mail_threads FOR UPDATE TO anon USING (true);
CREATE POLICY smart_mail_threads_owner_select ON public.smart_mail_threads FOR SELECT TO authenticated USING (to_alias=(auth.jwt()->'user_metadata'->>'smart_alias'));
CREATE POLICY smart_mail_messages_owner_select ON public.smart_mail_messages FOR SELECT TO authenticated USING (from_alias=(auth.jwt()->'user_metadata'->>'smart_alias'));
CREATE POLICY smart_mail_messages_owner_delete ON public.smart_mail_messages FOR DELETE TO authenticated USING (from_alias=(auth.jwt()->'user_metadata'->>'smart_alias'));
INSERT INTO public.person_identities (person_key, owner_id, owner_alias, display_name)
 VALUES ('person-alice','11111111-1111-4111-8111-111111111111','alice','Alice');
INSERT INTO public.smart_mail_threads(id,thread_key,to_alias,owner_alias,subject,participants)
 VALUES
('00000000-0000-4000-8000-000000000001','th1','bob','alice','Synthetic test 1','["alice","bob"]'),
('00000000-0000-4000-8000-000000000002','th2','charlie','carol','Synthetic test 2','["carol","charlie"]');
INSERT INTO public.smart_mail_messages VALUES
('00000000-0000-4000-8000-000000000011','00000000-0000-4000-8000-000000000001','alice'),
('00000000-0000-4000-8000-000000000012','00000000-0000-4000-8000-000000000002','carol');
