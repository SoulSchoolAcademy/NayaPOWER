-- Project Intelligence content parity — INTERNAL READ-ONLY diagnostic (2026-10-23).
-- Purpose: detect canonical source records missing from the live /projects display projection.
-- Do not count 'production:' pseudo-records as work. Counts alone hide missing keys.
-- Privacy: run only under an authorized internal audit role; never expose raw keys
-- or private project data from this query to unauthenticated clients.
-- Source of work truth: public.work_items. Current /projects reader: public.project_intel_items.
-- This is a diagnostic, NOT an auto-sync mechanism and NOT proof of user-facing rendering.
WITH source AS (
 SELECT w.project_id,w.item_key,w.state,w.evidence_url,w.maker_seat,w.prover_seat,
 CASE WHEN w.state='done_proven' AND nullif(btrim(coalesce(w.evidence_url,'')),'') IS NOT NULL
   AND nullif(btrim(coalesce(w.prover_seat,'')),'') IS NOT NULL
   AND coalesce(w.maker_seat,'')<>coalesce(w.prover_seat,'') THEN 'done-proven'
  WHEN w.state='needs_shawn' THEN 'needs-his-hands'
  WHEN w.state='blocked' THEN 'blocked'
  WHEN w.state='queued' THEN 'queued'
  ELSE 'in-motion' END expected_state
 FROM public.work_items w
),
display AS (
 SELECT i.project_id,i.item_key,i.state,i.evidence_url
 FROM public.project_intel_items i
 WHERE i.item_key NOT LIKE 'production:%'
),
missing AS (
 SELECT s.project_id,s.item_key FROM source s LEFT JOIN display d
 ON d.project_id=s.project_id AND d.item_key=s.item_key WHERE d.item_key IS NULL
),
extras AS (
 SELECT d.project_id,d.item_key FROM display d LEFT JOIN source s
 ON s.project_id=d.project_id AND s.item_key=d.item_key WHERE s.item_key IS NULL
),
misstated AS (
 SELECT s.project_id,s.item_key FROM source s JOIN display d
 ON d.project_id=s.project_id AND d.item_key=s.item_key
 WHERE d.state IS DISTINCT FROM s.expected_state
 OR (d.state='done-proven' AND nullif(btrim(coalesce(d.evidence_url,'')),'') IS NULL)
)
SELECT statement_timestamp() AS checked_at,p.name,
 (SELECT count(*) FROM source s WHERE s.project_id=p.id)::int canonical_work,
 (SELECT count(*) FROM display d WHERE d.project_id=p.id)::int displayed_work,
 (SELECT count(*) FROM missing m WHERE m.project_id=p.id)::int missing_keys,
 (SELECT count(*) FROM extras e WHERE e.project_id=p.id)::int stale_extra_keys,
 (SELECT count(*) FROM misstated t WHERE t.project_id=p.id)::int differing_state_or_proof,
 (SELECT coalesce(jsonb_agg(m.item_key ORDER BY m.item_key),'[]'::jsonb)
  FROM missing m WHERE m.project_id=p.id) missing_key_list
FROM public.projects p
ORDER BY p.parent_id NULLS FIRST,p.name;
