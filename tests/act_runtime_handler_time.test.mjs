import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { stripTypeScriptTypes } from 'node:module';
import vm from 'node:vm';
import { validateAct } from '../supabase/functions/nayanet-act-runtime/act.ts';

const source=readFileSync(new URL('../supabase/functions/nayanet-act-runtime/index.ts',import.meta.url),'utf8');
const code=stripTypeScriptTypes(source.replace(/^import .*;\r?\n/gm,''));
const OWNER='adfdf0b8-5558-41d1-9fed-ec51abf4fe2f';
const NAYA='NAYA-NODE-0001';
const claims={repository:'SoulSchoolAcademy/NayaPOWER',ref:'refs/heads/main',
  workflow_ref:'SoulSchoolAcademy/NayaPOWER/.github/workflows/live-act-proof.yml@refs/heads/main',jti:'offline-time-proof'};

function runtime(time, {failReceipt=false, identity=claims}={}) {
  let handler;
  const reads=[], writes=[];
  const law={id:'law1',user_id:OWNER,action:'law_authority_decision',status:'SUCCESS',evidence:{
    node_id:'NAYA-KERNEL-LAW',law_request:{action:'naya_node_apply',target:NAYA},
    law_decision:{status:'AUTHORIZED',owner_id:OWNER,naya_id:NAYA,action:'naya_node_apply',target:NAYA,
      authority_refs:['g1'],evaluated_at:time,expires_at:null}}};
  const grant={grant_id:'g1',issuer_id:OWNER,subject_id:OWNER,scope:{target:NAYA},
    actions:['naya_node_apply'],status:'ACTIVE',expires_at:null};
  const client={from(table){
    reads.push(table);
    return {
      select(){return this;},eq(){return this;},order(){return this;},limit(){return this;},
      async maybeSingle(){
        if(table==='nayanet_execution_receipts') return {data:law,error:null};
        if(table==='nayanet_authority_grants') return {data:grant,error:null};
        throw new Error('PRIVATE_BLOCK_READ_BEFORE_REFUSAL');
      },
      then(resolve,reject){return Promise.resolve({data:[],error:null}).then(resolve,reject);},
      insert(row){
        assert.equal(table,'nayanet_execution_receipts'); writes.push(row);
        return {select(){return {async single(){return failReceipt
          ? {data:null,error:{message:'receipt unavailable'}}
          : {data:{...row,id:'offline-refusal'},error:null};}};}};
      }
    };
  }};
  vm.runInNewContext(code,{URL,Request,Response,Date,console,validateAct,
    Deno:{env:{get:key=>({SUPABASE_URL:'https://offline.invalid',SUPABASE_SERVICE_ROLE_KEY:'offline-key'})[key]},
      serve:callback=>{handler=callback;}},
    createRemoteJWKSet:()=>({}),jwtVerify:async()=>({payload:identity}),createClient:()=>client});
  return {reads,writes,invoke:()=>handler(new Request('https://offline.invalid',{
    method:'POST',headers:{authorization:'Bearer offline','content-type':'application/json'},
    body:JSON.stringify({mode:'execute',law_receipt_id:'law1',action:'naya_node_apply',target:NAYA,
      door_id:'DOOR-AI',operation:'apply_retained_intelligence'})}))};
}

test('actual ACT handler refuses invalid freshness before private block access and persists refusal',async()=>{
  for(const time of [undefined,null,'','not-a-date','2999-01-01T00:00:00Z']) {
    const rt=runtime(time),response=await rt.invoke(),body=await response.json();
    assert.equal(response.status,403);
    assert.equal(body.guard.reason,'LAW_RECEIPT_TIME_INVALID');
    assert.equal(rt.reads.includes('nayanet_intelligent_blocks'),false);
    assert.equal(rt.writes.length,1);
    assert.equal(rt.writes[0].action,'act_node_refusal');
    assert.equal(rt.writes[0].status,'BLOCKED');
    assert.equal(rt.writes[0].evidence.action_executed,false);
    assert.equal(rt.writes[0].evidence.observed,false);
    assert.equal(body.refusal_receipt.id,'offline-refusal');
  }
});

test('interrupted refusal persistence cannot report a persisted refusal or execution',async()=>{
  const rt=runtime('not-a-date',{failReceipt:true});
  const body=await (await rt.invoke()).json();
  assert.equal(body.ok,false); assert.equal(body.error,'receipt unavailable');
  assert.equal(body.refusal_receipt,undefined);
  assert.equal(rt.reads.includes('nayanet_intelligent_blocks'),false);
});

test('OIDC workflow mismatch reaches no privileged state',async()=>{
  const rt=runtime('not-a-date',{identity:{...claims,workflow_ref:'wrong-workflow'}});
  const body=await (await rt.invoke()).json();
  assert.equal(body.error,'WORKFLOW_BINDING_MISMATCH');
  assert.equal(rt.reads.length,0); assert.equal(rt.writes.length,0);
});
