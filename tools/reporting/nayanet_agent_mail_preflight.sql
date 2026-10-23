-- NayaNET first-user Smart Mail authorization preflight (read-only).
-- Scope: metadata only. Never reads user messages or credentials.
-- A RED result blocks real cross-Naya private-mail pilot. See security owner #2823.
-- This query is an audit preflight; it is NOT a substitute for two real independent
-- authenticated identities + one unauthorized negative-control actor.
WITH tables(name) AS (
  VALUES ('smart_mail_threads'), ('smart_mail_messages')
), role_grants AS (
 SELECT t.name,
   has_table_privilege('anon', 'public.'||t.name, 'SELECT') anon_select,
   has_table_privilege('anon', 'public.'||t.name, 'INSERT') anon_insert,
   has_table_privilege('anon', 'public.'||t.name, 'UPDATE') anon_update
 FROM tables t
), policies AS (
 SELECT tablename,
   count(*) FILTER (WHERE 'anon'=ANY(roles) AND cmd IN ('SELECT','ALL')
     AND lower(btrim(coalesce(qual,''))) IN ('true','(true)')) anon_allow_all_reads,
   count(*) FILTER (WHERE 'anon'=ANY(roles) AND cmd IN ('INSERT','UPDATE','ALL')
     AND lower(btrim(coalesce(with_check,''))) IN ('true','(true)')) anon_allow_all_writes,
   count(*) FILTER (WHERE lower(coalesce(qual,'')||' '||coalesce(with_check,'')) LIKE '%user_metadata%') mutable_identity_policies
 FROM pg_policies WHERE schemaname='public' AND tablename IN (SELECT name FROM tables)
 GROUP BY tablename
), reported AS (
 SELECT g.name,
   g.anon_select,g.anon_insert,g.anon_update,
   coalesce(p.anon_allow_all_reads,0)::int anon_allow_all_reads,
   coalesce(p.anon_allow_all_writes,0)::int anon_allow_all_writes,
   coalesce(p.mutable_identity_policies,0)::int mutable_identity_policies,
   CASE WHEN (g.anon_select AND coalesce(p.anon_allow_all_reads,0)>0)
       OR ((g.anon_insert OR g.anon_update) AND coalesce(p.anon_allow_all_writes,0)>0)
       OR coalesce(p.mutable_identity_policies,0)>0
     THEN 'BLOCKED' ELSE 'METADATA_CHECK_PASSED__RUNTIME_NEGATIVE_TEST_STILL_REQUIRED'
   END gate
 FROM role_grants g LEFT JOIN policies p ON p.tablename=g.name
)
SELECT statement_timestamp() checked_at, name, gate,
       anon_select, anon_insert,anon_update,
       anon_allow_all_reads,anon_allow_all_writes,mutable_identity_policies
FROM reported ORDER BY name;
