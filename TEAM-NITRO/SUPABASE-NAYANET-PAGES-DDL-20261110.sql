-- Create the citizen-pages table — Supabase master first pass, 2026-11-10.
-- Prepared for Shawn's hand in the Supabase SQL Editor (production database).
-- Paste the whole file, run it, done. No app code changes needed.
--
-- WHAT THIS DOES, IN PLAIN WORDS:
-- Today a citizen finishes the walkthrough and has nowhere to put their
-- page. The audit proved it live: asking for the nayanet_pages table
-- returns "Could not find the table 'public.nayanet_pages'". The
-- walkthrough writes who they are into nayanet_identities (10 rows) and
-- then stops, because there is no pages table to write the page into.
-- This file creates that table: one row per citizen page.
--
-- WHAT EACH COLUMN IS:
--   id            — the page's own id, made up by the database.
--   owner_alias   — whose page it is: the citizen's alias, the same alias
--                   in nayanet_identities. (Identities have no numeric id;
--                   alias is the link between the two tables.)
--   kind          — what sort of page: personal, business, space, or
--                   membership. Only those four words are allowed.
--   title         — the page's title, as the citizen wrote it.
--   slug          — the short web address piece, unique per owner.
--   body          — the page itself, as structured data (blocks, links,
--                   settings). The page template stays one shared template;
--                   this column holds only what makes this page theirs.
--   published     — true once the citizen has published it; false while
--                   it is still a draft.
--   created_at / updated_at — when the page was made and last changed.
--
-- WHAT IT LOCKS:
-- Row-level security is ON, and the public key gets READ ONLY. Anyone can
-- read a published page (that is what a page is for), but the public key
-- cannot insert, change, or delete any page. Page writes go through the
-- service role — the server side — never through the public key.
-- If the walkthrough ever needs to write a page straight from the
-- browser with the public key, that needs a narrow INSERT rule added
-- here at run time. Do NOT add one by copying the notes table's open
-- rules: the notes table lets anyone holding the public key rewrite any
-- note, and pages must never work that way.
--
-- NOTE ON THE SHAPE: no code anywhere in the repo writes a pages table
-- yet (zero references to nayanet_pages in the repo), so this shape is
-- the master's proposal from what the walkthrough needs — one row per
-- page, owned by alias, kind + title + slug + body — not a copy of an
-- existing writer. If the walkthrough team needs another column, add it
-- in a second small change; do not rebuild this table.

CREATE TABLE public.nayanet_pages (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  owner_alias text NOT NULL REFERENCES public.nayanet_identities(alias) ON DELETE CASCADE,
  kind text NOT NULL CHECK (kind IN ('personal', 'business', 'space', 'membership')),
  title text NOT NULL,
  slug text NOT NULL,
  body jsonb NOT NULL DEFAULT '{}'::jsonb,
  published boolean NOT NULL DEFAULT false,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (owner_alias, slug)
);

CREATE INDEX IF NOT EXISTS nayanet_pages_owner_idx
  ON public.nayanet_pages (owner_alias, created_at DESC);

ALTER TABLE public.nayanet_pages ENABLE ROW LEVEL SECURITY;

-- Public read only: anyone may read a page; nobody may write via the key.
GRANT SELECT ON public.nayanet_pages TO anon;
REVOKE INSERT, UPDATE, DELETE ON public.nayanet_pages FROM anon;

DROP POLICY IF EXISTS "nayanet_pages_select_all" ON public.nayanet_pages;
CREATE POLICY "nayanet_pages_select_all" ON public.nayanet_pages
  FOR SELECT TO anon USING (true);

-- AFTER RUNNING, VERIFY (same SQL Editor, run these and check):
--   SELECT tablename, rowsecurity FROM pg_tables
--     WHERE schemaname = 'public' AND tablename = 'nayanet_pages';
-- Rowsecurity must be true.
--   SELECT grantee, privilege_type FROM information_schema.role_table_grants
--     WHERE table_schema = 'public' AND table_name = 'nayanet_pages'
--     AND grantee = 'anon';
-- Only SELECT should be listed.
-- Then re-run the audit's check: an anonymous read of nayanet_pages
-- should now return an empty list ([]) instead of PGRST205
-- "Could not find the table".
