import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';

const path = 'supabase/migrations/20260930184500_fix_intelligence_commit_digest_schema_v2.sql';
const sql = fs.readFileSync(path, 'utf8');

test('intelligence commit qualifies pgcrypto digest under empty search_path', () => {
  assert.match(sql, /set search_path=''/);
  assert.match(sql, /extensions\.digest\(p_content,'sha256'\)/);
  assert.doesNotMatch(sql, /encode\(digest\(p_content,'sha256'\)/);
});

test('digest repair preserves target authority and graph writer seams', () => {
  assert.match(sql, /nayanet_validate_authority_grant\(p_authority_grant_id,'intelligence_commit',p_target_id\)/);
  assert.match(sql, /p_connections jsonb default null/);
  assert.match(sql, /nayanet_normalize_block_connections/);
  assert.match(sql, /insert into public\.nayanet_brain_relationships/);
});
