import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';

const path = 'supabase/migrations/20260930190000_fix_intelligence_commit_lineage_revision_v2.sql';
const sql = fs.readFileSync(path, 'utf8');

test('intelligence commit lineage targets a cognition event, not block row', () => {
  assert.match(sql, /'CREATED_INTELLIGENT_BLOCK',event_row/);
  assert.doesNotMatch(sql, /'CREATED_INTELLIGENT_BLOCK',block_row/);
});

test('intelligence commit serializes governed revision allocation', () => {
  assert.match(sql, /pg_advisory_xact_lock\(hashtext\(uid::text \|\| ':' \|\| p_project_id\)::bigint\)/);
});

test('lineage repair preserves later authority, digest, and graph invariants', () => {
  assert.match(sql, /nayanet_validate_authority_grant\(p_authority_grant_id,'intelligence_commit',p_target_id\)/);
  assert.match(sql, /extensions\.digest\(p_content,'sha256'\)/);
  assert.match(sql, /p_connections jsonb default null/);
  assert.match(sql, /nayanet_normalize_block_connections/);
  assert.match(sql, /insert into public\.nayanet_brain_relationships/);
});
