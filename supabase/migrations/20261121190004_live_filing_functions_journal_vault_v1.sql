-- Live filing: journal + Vault auto-file RPCs — 3 functions
-- Supabase filing round 2026-11-21, Seat 2 (FUNCTIONS). Branch: supabase/filing-20261121-functions.
-- Source: LIVE definitions captured first-hand 2026-11-21 via Supabase Management API
--   POST /v1/projects/dahisasgpfvziswqvmvm/database/query — pg_get_functiondef / pg_get_triggerdef.
--   Read-only capture. No live writes were made. Definitions below are verbatim live
--   bytes (CREATE OR REPLACE FUNCTION as returned by pg_get_functiondef), grouped by
--   area; only this header and per-function provenance comments were added.
-- Journal reads/writes (token-resolved owner) + note auto-categorization.
-- NOTE (scope limit, stated honestly): a fresh-apply diff against a test database is
--   NOT in scope for this round (coordinator brief). These migrations assume the
--   live-only tables they read exist — Seat 1's table filings on the same filing
--   branch supply them; apply tables first on a fresh rebuild.
-- Inventory: DATABASE.md §(b) B1/B2 + §(c); INVENTORY.md §3.2 / §3.4 (64 riders).

-- ---------------------------------------------------------------------------
-- journal_read(p_token text, p_from date, p_to date)
--   live: public.journal_read — SECURITY DEFINER, language sql, kind f, volatile s
--   purpose (DATABASE.md): Read a citizen's journal entries in a date range (token-resolved owner). (Journal / Vault)
--   captured: pg_get_functiondef(journal_read) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.journal_read(p_token text, p_from date, p_to date)
 RETURNS SETOF journal_entries
 LANGUAGE sql
 STABLE SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
  SELECT j.* FROM public.journal_entries j
  WHERE j.owner_alias = public.owner_alias_for(p_token)
    AND public.owner_alias_for(p_token) <> ''
    AND j.entry_date BETWEEN COALESCE(p_from, j.entry_date) AND COALESCE(p_to, j.entry_date)
  ORDER BY j.entry_date DESC
$function$;

-- ---------------------------------------------------------------------------
-- journal_upsert(p_token text, p_entry_date date, p_title text, p_body text, p_mood text)
--   live: public.journal_upsert — SECURITY DEFINER, language plpgsql, kind f, volatile v
--   purpose (DATABASE.md): Create/update one journal entry for the token's owner. (Journal / Vault)
--   captured: pg_get_functiondef(journal_upsert) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.journal_upsert(p_token text, p_entry_date date, p_title text, p_body text, p_mood text)
 RETURNS uuid
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
DECLARE v_owner text; v_id uuid;
BEGIN
  v_owner := public.owner_alias_for(p_token);
  IF v_owner = '' THEN RAISE EXCEPTION 'not authorized'; END IF;
  INSERT INTO public.journal_entries (owner_alias, entry_date, title, body, mood)
  VALUES (v_owner, p_entry_date, p_title, p_body, p_mood)
  ON CONFLICT (owner_alias, entry_date) DO UPDATE SET
    title = EXCLUDED.title, body = EXCLUDED.body, mood = EXCLUDED.mood,
    updated_at = now()
  RETURNING id INTO v_id;
  RETURN v_id;
END $function$;

-- ---------------------------------------------------------------------------
-- auto_categorize_note(p_note_id uuid)
--   live: public.auto_categorize_note — SECURITY INVOKER (default), language plpgsql, kind f, volatile v
--   purpose (DATABASE.md): Auto-assign a category to a note (the auto-filing brain). (Smart Vault)
--   captured: pg_get_functiondef(auto_categorize_note) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.auto_categorize_note(p_note_id uuid)
 RETURNS text
 LANGUAGE plpgsql
AS $function$
DECLARE
  v_content text;
  v_owner text;
  v_terms text[];
  v_best_cat text := NULL;
  v_best_score numeric := 0;
  v_cat record;
  v_score numeric;
BEGIN
  -- Get the note content
  SELECT content, owner_alias INTO v_content, v_owner
  FROM smart_notes WHERE id = p_note_id;
  
  IF v_content IS NULL THEN RETURN NULL; END IF;
  
  -- Extract terms from content (simple: lowercase words, 4+ chars, no stopwords)
  -- The intelligence: what is this about?
  SELECT array_agg(DISTINCT w) INTO v_terms
  FROM (
    SELECT lower(regexp_replace(word, '[^a-z]', '', 'g')) as w
    FROM regexp_split_to_table(v_content, '\s+') as word
  ) t
  WHERE length(w) >= 4
    AND w NOT IN ('this','that','with','from','have','will','your','about','into','over','after','before','between','through','during','under','again','further','then','once','here','there','when','where','which','while','who','whom','what','these','those','them','they','their','been','were','said','each','make','like','just','over','such','only','also','back','after','use','how','our','out','day','get','has','him','his','how','its','may','new','now','old','see','two','way','who','boy','did','its','let','put','say','she','too','use')
  LIMIT 20;
  
  IF v_terms IS NULL OR array_length(v_terms, 1) = 0 THEN
    v_terms := ARRAY['general'];
  END IF;
  
  -- Match against existing category prototypes using smart_match math
  -- The intelligence: what does this relate to?
  FOR v_cat IN 
    SELECT category_name, term_signature 
    FROM naya_category_prototypes 
    WHERE owner_alias = v_owner
  LOOP
    SELECT (smart_match(
      jsonb_build_object('topics', to_jsonb(v_terms)),
      jsonb_build_object('topics', v_cat.term_signature)
    )->>'score')::numeric INTO v_score;
    
    IF v_score > v_best_score THEN
      v_best_score := v_score;
      v_best_cat := v_cat.category_name;
    END IF;
  END LOOP;
  
  -- If best match is weak (< 30), a new category emerges from the dominant terms
  -- The intelligence: this is something new, give it a name
  IF v_best_cat IS NULL OR v_best_score < 30 THEN
    v_best_cat := v_terms[1] || '-' || v_terms[2];
    IF v_best_cat IS NULL THEN v_best_cat := 'general'; END IF;
    INSERT INTO naya_category_prototypes (category_name, owner_alias, term_signature, member_count)
    VALUES (v_best_cat, v_owner, to_jsonb(v_terms), 1)
    ON CONFLICT (category_name) DO UPDATE SET
      member_count = naya_category_prototypes.member_count + 1,
      updated_at = now();
    v_best_score := 100;
  ELSE
    -- Strengthen the matched category
    UPDATE naya_category_prototypes
    SET member_count = member_count + 1, updated_at = now()
    WHERE category_name = v_best_cat;
  END IF;
  
  -- File the note
  INSERT INTO naya_note_filing (note_id, category_name, match_score)
  VALUES (p_note_id, v_best_cat, v_best_score)
  ON CONFLICT (note_id) DO UPDATE SET
    category_name = EXCLUDED.category_name,
    match_score = EXCLUDED.match_score,
    filed_at = now();
  
  RETURN v_best_cat;
END;
$function$;
