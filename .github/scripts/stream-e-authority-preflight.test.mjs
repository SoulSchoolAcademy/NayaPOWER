import test from 'node:test';
import assert from 'node:assert/strict';
import { inspectAuthorityGrant } from './stream-e-authority-preflight.mjs';

test('blocks a missing authority grant before runtime work',()=>{
  assert.deepEqual(inspectAuthorityGrant(''),{status:'BLOCKED',error_code:'AUTHORITY_GRANT_REQUIRED',authority_grant_id_present:false});
});

test('blocks a malformed authority grant identifier',()=>{
  assert.deepEqual(inspectAuthorityGrant('not-a-grant'),{status:'BLOCKED',error_code:'AUTHORITY_GRANT_ID_INVALID',authority_grant_id_present:true});
});

test('accepts a UUID-shaped grant identifier without logging it',()=>{
  assert.deepEqual(inspectAuthorityGrant('123e4567-e89b-42d3-a456-426614174000'),{status:'PASS',error_code:null,authority_grant_id_present:true});
});
