import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { stripTypeScriptTypes } from 'node:module';
import vm from 'node:vm';
import { evaluateLaw } from '../supabase/functions/nayanet-law-runtime/law.ts';

const source = readFileSync(new URL('../supabase/functions/nayanet-law-runtime/index.ts', import.meta.url), 'utf8');
const code = stripTypeScriptTypes(source.replace(/^import[\s\S]*?;\r?\n/gm, ''));
const OWNER = 'adfdf0b8-5558-41d1-9fed-ec51abf4fe2f';
const NAYA = 'NAYA-NODE-0001';
const claims = {
  repository: 'SoulSchoolAcademy/NayaPOWER', ref: 'refs/heads/main',
  workflow_ref: 'SoulSchoolAcademy/NayaPOWER/.github/workflows/live-law-proof.yml@refs/heads/main',
  jti: 'offline-law-scope-jti',
};

function runtime(scope, identity = claims, failReceipt = false, expires_at = null, verifyReceipt = null, mode = 'evaluate') {
  let handler;
  const writes = [];
  const reads = [];
  const grant = { grant_id: 'g1', issuer_id: OWNER, subject_id: OWNER,
    scope, actions: ['data_read'], status: 'ACTIVE', expires_at };
  const client = { from(table) {
    reads.push(table);
    assert.ok(['nayanet_authority_grants', 'nayanet_execution_receipts'].includes(table));
    const query = {
      select() { return this; }, eq() { return this; }, order() { return this; }, limit() { return this; },
      maybeSingle() { return Promise.resolve({data: table === 'nayanet_execution_receipts' ? verifyReceipt : null, error: null}); },
      then(resolve, reject) { return Promise.resolve({data: table === 'nayanet_authority_grants' ? [grant] : [], error: null}).then(resolve,reject); },
      insert(row) {
        assert.equal(table, 'nayanet_execution_receipts');
        writes.push({table, row});
        return {select() {return {async single() {
          return failReceipt ? {data:null,error:{message:'receipt unavailable'}} :
            {data:{...row,id:'offline-law-receipt'},error:null};
        }};}};
      },
    };
    return query;
  }};
  vm.runInNewContext(code, {
    URL, Request, Response, Date, console, evaluateLaw,
    Deno: {env:{get: key => ({SUPABASE_URL:'https://offline.invalid', SUPABASE_SERVICE_ROLE_KEY:'offline-key'})[key]},
      serve: callback => {handler = callback;}},
    createRemoteJWKSet: () => ({}), jwtVerify: async () => ({payload:identity}), createClient: () => client,
  });
  return {writes, reads, invoke: () => handler(new Request('https://offline.invalid', {
    method:'POST',headers:{authorization:'Bearer offline','content-type':'application/json'},
    body:JSON.stringify(mode === 'verify' ? {mode:'verify',receipt_id:String(verifyReceipt?.id ?? '')} : {mode:'evaluate',request:{action:'data_read',target:NAYA}}),
  }))};
}

test('CV-05 FALSIFIER -- LAW decision mismatch cannot claim independent verification', async () => {
  const receipt = {
    id: 'offline-law-verify-mismatch',
    user_id: OWNER,
    action: 'law_authority_decision',
    evidence: {
      law_request: {owner_id: OWNER, naya_id: NAYA, action: 'data_read', target: NAYA},
      law_decision: {status: 'NEEDS_HUMAN_AUTHORIZATION', reason: 'FORGED_MISMATCH', authority_refs: []},
    },
  };
  const rt = runtime({target:NAYA}, claims, false, null, receipt, 'verify');
  const response = await rt.invoke();
  const body = await response.json();
  assert.equal(response.status, 200);
  assert.equal(body.ok, false);
  assert.equal(body.status, 'LAW_DECISION_MISMATCH');
  assert.equal(body.independent_verification, false);
});

test('CV-05 FIX -- matching LAW decision may claim independent verification', async () => {
  const req = {owner_id: OWNER, naya_id: NAYA, action: 'data_read', target: NAYA};
  const decision = evaluateLaw(req, [{grant_id:'g1', issuer_id:OWNER, subject_id:OWNER, mission_id:'M1', scope:{target:NAYA}, actions:['data_read'], constraints:{}, issued_at:'2026-09-29T18:00:00Z', expires_at:null, status:'ACTIVE', revoked_at:null}], new Date());
  const receipt = {
    id: 'offline-law-verify-match', user_id: OWNER, action: 'law_authority_decision',
    evidence: {law_request:req, law_decision:decision},
  };
  const rt = runtime({target:NAYA}, claims, false, null, receipt, 'verify');
  const response = await rt.invoke();
  const body = await response.json();
  assert.equal(response.status, 200);
  assert.equal(body.ok, true);
  assert.equal(body.status, 'LAW_DECISION_VERIFIED');
  assert.equal(body.independent_verification, true);
});

test('actual LAW handler persists refusal for wrong or missing target scope', async () => {
  for(const scope of [{target:'OTHER-NAYA'}, {}, {project_id:''}]) {
    const rt = runtime(scope);
    const body = await (await rt.invoke()).json();
    assert.equal(body.ok,true); // evaluation completed; requested action remains unauthorized
    assert.equal(body.decision.status,'NEEDS_HUMAN_AUTHORIZATION');
    assert.deepEqual(body.decision.authority_refs,[]);
    assert.equal(rt.writes.length,1);
    assert.equal(rt.writes[0].row.status,'BLOCKED');
    assert.equal(rt.writes[0].row.evidence.execution_boundary,'LAW_DECIDES_ONLY_DOES_NOT_EXECUTE');
  }
});

test('actual LAW handler preserves valid target authorization without action effects', async () => {
  const rt = runtime({target:NAYA});
  const body = await (await rt.invoke()).json();
  assert.equal(body.decision.status,'AUTHORIZED');
  assert.deepEqual(body.decision.authority_refs,['g1']);
  assert.equal(rt.writes.length,1);
  assert.equal(rt.writes[0].row.action,'law_authority_decision');
});

test('wrong OIDC workflow cannot reach privileged reads or writes', async () => {
  const rt = runtime({target:NAYA},{...claims,workflow_ref:'wrong-workflow'});
  const body = await (await rt.invoke()).json();
  assert.equal(body.ok,false);
  assert.equal(body.error,'WORKFLOW_BINDING_MISMATCH');
  assert.equal(rt.reads.length,0);
  assert.equal(rt.writes.length,0);
});

test('receipt failure cannot return a completed LAW evaluation', async () => {
  const rt = runtime({target:NAYA},claims,true);
  const body = await (await rt.invoke()).json();
  assert.equal(body.ok,false);
  assert.equal(body.error,'receipt unavailable');
});

test('actual LAW handler persists malformed matching grant expiry as refusal, never authorization', async () => {
  for(const expiry of ['not-a-date', '', '   ', 123]) {
    const rt=runtime({target:NAYA},claims,false,expiry);
    const response=await rt.invoke(), body=await response.json();
    assert.equal(response.status,200); // completed evaluation, not action permission
    assert.equal(body.decision.status,'BLOCKED');
    assert.equal(body.decision.reason,'GRANT_TIME_INVALID');
    assert.equal(rt.writes.length,1);
    assert.equal(rt.writes[0].row.status,'BLOCKED');
    assert.equal(rt.writes[0].row.evidence.execution_boundary,'LAW_DECIDES_ONLY_DOES_NOT_EXECUTE');
  }
});


test('live PROVE workflow is explicitly trusted without widening arbitrary workflow access', async () => {
  const proveClaims = {
    ...claims,
    workflow_ref: 'SoulSchoolAcademy/NayaPOWER/.github/workflows/live-prove-proof.yml@refs/heads/main',
  };
  const rt = runtime({target:NAYA}, proveClaims);
  const response = await rt.invoke();
  const body = await response.json();
  assert.equal(response.status, 200);
  assert.equal(body.ok, true);
  assert.equal(body.decision.status, 'AUTHORIZED');
  assert.deepEqual(body.decision.authority_refs, ['g1']);
  assert.equal(rt.writes.length, 1);
});
