-- Isolated synthetic fixture. NOT a production schema dump.
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
CREATE TABLE public.smart_mail_threads(id uuid PRIMARY KEY, to_alias text NOT NULL);
CREATE TABLE public.smart_mail_messages(id uuid PRIMARY KEY, thread_id uuid REFERENCES public.smart_mail_threads(id), from_alias text NOT NULL);
CREATE TABLE public.intake_events(id int PRIMARY KEY, owner_alias text NOT NULL);
CREATE TABLE public.owner_alias_claims(owner_id uuid NOT NULL, alias_normalized text NOT NULL);
GRANT SELECT, INSERT, UPDATE ON public.smart_mail_messages, public.smart_mail_threads TO anon;
GRANT SELECT, DELETE ON public.smart_mail_messages TO authenticated;
GRANT SELECT ON public.smart_mail_threads, public.intake_events, public.owner_alias_claims TO authenticated;
ALTER TABLE public.smart_mail_threads ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.smart_mail_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.intake_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.owner_alias_claims ENABLE ROW LEVEL SECURITY;
CREATE POLICY owner_alias_claims_owner_select ON public.owner_alias_claims FOR SELECT TO authenticated USING (owner_id=auth.uid());
CREATE POLICY intake_events_auth_select ON public.intake_events FOR SELECT TO authenticated USING (true);
CREATE POLICY pass2_anon_select_smart_mail_messages ON public.smart_mail_messages FOR SELECT TO anon USING (true);
CREATE POLICY pass2_anon_insert_smart_mail_messages ON public.smart_mail_messages FOR INSERT TO anon WITH CHECK (true);
CREATE POLICY pass2_anon_update_smart_mail_messages ON public.smart_mail_messages FOR UPDATE TO anon USING (true);
CREATE POLICY pass2_anon_select_smart_mail_threads ON public.smart_mail_threads FOR SELECT TO anon USING (true);
CREATE POLICY pass2_anon_insert_smart_mail_threads ON public.smart_mail_threads FOR INSERT TO anon WITH CHECK (true);
CREATE POLICY pass2_anon_update_smart_mail_threads ON public.smart_mail_threads FOR UPDATE TO anon USING (true);
CREATE POLICY smart_mail_threads_owner_select ON public.smart_mail_threads FOR SELECT TO authenticated USING (to_alias=(auth.jwt()->'user_metadata'->>'smart_alias'));
CREATE POLICY smart_mail_messages_owner_select ON public.smart_mail_messages FOR SELECT TO authenticated USING (from_alias=(auth.jwt()->'user_metadata'->>'smart_alias'));
CREATE POLICY smart_mail_messages_owner_delete ON public.smart_mail_messages FOR DELETE TO authenticated USING (from_alias=(auth.jwt()->'user_metadata'->>'smart_alias'));
INSERT INTO public.smart_mail_threads VALUES
('00000000-0000-4000-8000-000000000001', 'bob'),
('00000000-0000-4000-8000-000000000002','charlie');
INSERT INTO public.smart_mail_messages VALUES
('00000000-0000-4000-8000-000000000011','00000000-0000-4000-8000-000000000001','alice'),
('00000000-0000-4000-8000-000000000012','00000000-0000-4000-8000-000000000002','carol');
INSERT INTO public.intake_events VALUES(1,'alice'),(2,'bob');
INSERT INTO public.owner_alias_claims VALUES
('11111111-1111-4111-8111-111111111111','alice'),
('22222222-2222-4222-8222-222222222222','bob');
