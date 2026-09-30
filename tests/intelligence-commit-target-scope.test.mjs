import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';

const path = 'supabase/migrations/20260930183000_fix_intelligence_commit_target_scope_v1.sql';
const sql = fs.readFileSync(path, 'utf8');

test('intelligence commit validates authority against p_target_id', () => {
  assert.match(sql, /nayanet_validate_authority_grant\(p_authority_grant_id,'intelligence_commit',p_target_id\)/);
  assert.doesNotMatch(sql, /nayanet_validate_authority_grant\(p_authority_grant_id,'intelligence_commit',p_project_id\)/);
});

test('repair preserves canonical writer signature and graph projection seam', () => {
  assert.match(sql, /create or replace function public\.nayanet_intelligence_commit\(/i);
  assert.match(sql, /p_connections jsonb default null/);
  assert.match(sql, /nayanet_normalize_block_connections/);
  assert.match(sql, /insert into public\.nayanet_brain_relationships/);
});
