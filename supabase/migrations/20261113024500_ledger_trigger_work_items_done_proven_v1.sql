-- Ledger trigger: unfreeze the Smart Ledger by mechanism, never by hand.
--
-- One trigger (+ its function) on public.work_items. On every adapter-confirmed
-- transition into done_proven it appends exactly one row to
-- public.ledger_entries, chained from the live chain's tip on the LIVE hash
-- formula:
--   entry_hash = sha256(canon(12 fields) + "|" + prev_hash)
-- canon is JSON with keys sorted, separators (",", ":"), non-ASCII literal --
-- exactly Python's json.dumps(sort_keys=True, separators=(",", ":"),
-- ensure_ascii=False), as written by the ledger writer
-- (~/workspace/smart-ledger-build/stage/02-ledger-append.py) and checked by
-- the verifier (03-ledger-verify.py, CHAIN OK 30/30 at filing).
-- The staged demo's form (sha256(prev_hash + canonical(10 fields)), no
-- separator) is NOT used here: it recomputes 0 of 30 live rows.
--
-- Adapter-confirmed = the row lands in done_proven carrying its receipt:
-- evidence_url + prover_seat, prover different from maker. The database
-- already enforces this on every done_proven row
-- (constraint work_items_done_proven_law); the trigger's WHEN clause states
-- the same rule, so casual edits mint nothing.
--
-- Field mapping (work_items -> ledger_entries), all read from the live row:
--   entry_id     LE-<yyyymmdd>-<count+1, zero-padded to 3> (the writer's rule)
--   issued_at    now, truncated to seconds (the canon's seconds form)
--   kind         'execution' (live kind CHECK: execution, decision, census,
--                signal -- never the staged demo's 'transition')
--   lane         'team-nitro' (the live chain's dominant lane, 23 of 30 rows;
--                the floor that operates these items)
--   title        the item's title
--   outcome      'DONE_PROVEN'
--   nutshell     the item's detail, or its title when detail is empty
--                (first 500 characters)
--   proof_kind   'url'
--   proof_url    the item's evidence_url (the receipt)
--   proof_detail 'item <item_key> proven by <prover_seat>'
--   proof_state  'VERIFIED'
--   prev_hash    the live tip's entry_hash, read locked at insert time
--   scores       {}   raw {}
--
-- The SQL canon was checked against the Python canon before filing:
-- the escape helper matches json.dumps on a 27-string battery (quotes,
-- backslashes, every control character 0x01-0x1F, non-ASCII kept literal),
-- and a full simulated canon + hash matches the Python recompute exactly.
-- First real execution proof is the preview battery (one transition ->
-- exactly one chained row; full chain recomputes valid, 31 entries).
--
-- Rollback: DROP TRIGGER trg_work_items_done_proven_to_ledger, then
-- DROP FUNCTION public.nayanet_work_item_done_proven_to_ledger(). Entries
-- already appended stay; history is never deleted. The gap (seq 1 missing,
-- 2026-10-22 -> apply day frozen) is never backfilled.
--
-- Documented edges:
--   * A direct INSERT of a work_items row already in done_proven mints
--     nothing: this is a single AFTER UPDATE trigger, and items enter
--     through the adapter as queued.
--   * done_proven is terminal by the state machine, but no constraint blocks
--     leaving it; a re-entry into done_proven would mint a second row for
--     the same item (a second landing, a second event).
--   * The trigger trusts the chain tip at append time; the independent
--     verifier (03-ledger-verify.py) is the guard that the chain is whole.
--     It was CHAIN OK 30/30 at filing. No second writer of ledger_entries
--     exists: the older ledger functions write to nayanet_smart_ledger,
--     a different table, and no trigger on work_items calls them.

-- 1. JSON string escaping, Python json.dumps-compatible (ensure_ascii=False).
--    Escapes backslash, double quote, and control characters 0x01-0x1F only;
--    non-ASCII stays literal. Order matters: backslash first, then quote,
--    then control characters (each replacement introduces backslashes that
--    must not be re-escaped).
CREATE OR REPLACE FUNCTION public.nayanet_ledger_json_escape(p_text text)
RETURNS text
LANGUAGE plpgsql
IMMUTABLE
AS $function$
DECLARE
  v text := coalesce(p_text, '');
  i int;
BEGIN
  v := replace(v, '\', '\\');
  v := replace(v, '"', '\"');
  FOR i IN 1..31 LOOP
    IF i = 8 THEN
      v := replace(v, chr(8), '\b');
    ELSIF i = 9 THEN
      v := replace(v, chr(9), '\t');
    ELSIF i = 10 THEN
      v := replace(v, chr(10), '\n');
    ELSIF i = 12 THEN
      v := replace(v, chr(12), '\f');
    ELSIF i = 13 THEN
      v := replace(v, chr(13), '\r');
    ELSE
      v := replace(v, chr(i), '\u' || lpad(to_hex(i), 4, '0'));
    END IF;
  END LOOP;
  RETURN v;
END;
$function$;

-- 2. The append function: one chained ledger row per adapter-confirmed landing.
CREATE OR REPLACE FUNCTION public.nayanet_work_item_done_proven_to_ledger()
RETURNS trigger
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path TO 'public', 'extensions'
AS $function$
DECLARE
  v_prev text;
  v_count bigint;
  v_issued timestamptz;
  v_issued_s text;
  v_entry_id text;
  v_title text;
  v_nutshell text;
  v_proof_detail text;
  v_canon text;
  v_hash text;
BEGIN
  -- Serialize appends so two concurrent landings cannot fork the chain.
  LOCK TABLE public.ledger_entries IN EXCLUSIVE MODE;

  SELECT entry_hash INTO v_prev
    FROM public.ledger_entries
   ORDER BY seq DESC
   LIMIT 1;
  IF v_prev IS NULL THEN
    v_prev := 'GENESIS-20261022';
  END IF;
  SELECT count(*) INTO v_count FROM public.ledger_entries;

  v_issued := date_trunc('second', now());
  v_issued_s := to_char(v_issued AT TIME ZONE 'UTC', 'YYYY-MM-DD"T"HH24:MI:SS"+00:00"');
  v_entry_id := 'LE-' || to_char(v_issued AT TIME ZONE 'UTC', 'YYYYMMDD')
    || '-' || lpad((v_count + 1)::text, 3, '0');

  v_title := NEW.title;
  v_nutshell := left(coalesce(nullif(btrim(NEW.detail), ''), NEW.title), 500);
  v_proof_detail := 'item ' || NEW.item_key || ' proven by ' || NEW.prover_seat;

  -- canon: the 12 fields in sorted key order, separators (",", ":").
  v_canon := '{"entry_id":"' || public.nayanet_ledger_json_escape(v_entry_id)
    || '","issued_at":"' || public.nayanet_ledger_json_escape(v_issued_s)
    || '","kind":"execution"'
    || ',"lane":"team-nitro"'
    || ',"nutshell":"' || public.nayanet_ledger_json_escape(v_nutshell)
    || '","outcome":"DONE_PROVEN"'
    || ',"prev_hash":"' || public.nayanet_ledger_json_escape(v_prev)
    || '","proof_detail":"' || public.nayanet_ledger_json_escape(v_proof_detail)
    || '","proof_kind":"url"'
    || ',"proof_url":"' || public.nayanet_ledger_json_escape(NEW.evidence_url)
    || '","scores":{}'
    || ',"title":"' || public.nayanet_ledger_json_escape(v_title)
    || '"}';

  v_hash := encode(extensions.digest(v_canon || '|' || v_prev, 'sha256'), 'hex');

  INSERT INTO public.ledger_entries
    (entry_id, issued_at, kind, lane, title, outcome, nutshell,
     proof_kind, proof_url, proof_detail, proof_state, prev_hash, entry_hash,
     scores, raw)
  VALUES
    (v_entry_id, v_issued, 'execution', 'team-nitro', v_title, 'DONE_PROVEN',
     v_nutshell, 'url', NEW.evidence_url, v_proof_detail, 'VERIFIED',
     v_prev, v_hash, '{}'::jsonb, '{}'::jsonb);

  RETURN NEW;
END;
$function$;

-- 3. The trigger: AFTER UPDATE OF state, adapter-confirmed landings only.
DROP TRIGGER IF EXISTS trg_work_items_done_proven_to_ledger ON public.work_items;
CREATE TRIGGER trg_work_items_done_proven_to_ledger
AFTER UPDATE OF state ON public.work_items
FOR EACH ROW
WHEN (OLD.state IS DISTINCT FROM 'done_proven'
  AND NEW.state = 'done_proven'
  AND NEW.evidence_url IS NOT NULL AND NEW.evidence_url <> ''
  AND NEW.prover_seat IS NOT NULL AND NEW.prover_seat <> ''
  AND (NEW.maker_seat IS NULL OR NEW.prover_seat IS DISTINCT FROM NEW.maker_seat))
EXECUTE FUNCTION public.nayanet_work_item_done_proven_to_ledger();
