import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {stripTypeScriptTypes} from 'node:module';
import vm from 'node:vm';
import {selectKnowContext,validateKnowAuthority} from '../supabase/functions/nayanet-know-runtime/know.ts';

const source=readFileSync(new URL('../supabase/functions/nayanet-know-runtime/index.ts',import.meta.url),'utf8');
const code=stripTypeScriptTypes(source.replace(/^import .*;\r?\n/gm,''));
const OWNER='adfdf0b8-5558-41d1-9fed-ec51abf4fe2f',NAYA='NAYA-NODE-0001';
const NOW='2026-09-29T20:00:00Z';
class Clock extends Date {constructor(...args){super(...(args.length?args:[NOW]));} static now(){return Date.parse(NOW);}}
const claims={repository:'SoulSchoolAcademy/NayaPOWER',ref:'refs/heads/main',
  workflow_ref:'SoulSchoolAcademy/NayaPOWER/.github/workflows/live-know-proof.yml@refs/heads/main',jti:'offline-handler-jti'};
const task={task_id:'held-out-provenance',task_class:'RELATED_HELDOUT',required_capability:'provenance_preservation'};
const block={intelligent_block_id:'IB-ELIGIBLE',owner_id:OWNER,status:'DURABLE',understanding_state:'VERIFIED',
  owner_scope:'PRIVATE',applicable_scope:{target:NAYA,capabilities:['provenance_preservation']},
  content:{lesson:'Preserve provenance before applying retained intelligence'},
  provenance:{source_event_id:'event-1'},evidence_refs:[{receipt_id:'proof-1'}],updated_at:NOW};

function runtime({time='2026-09-29T19:59:00Z',omitTime=false,grantPatch={},identity=claims,
  mode='retrieve',capability=task.required_capability,failWrite=false}={}) {
  let handler;
  const reads=[],writes=[],authOptions=[];
  const context={...task,required_capability:capability};
  const law={id:'law-1',user_id:OWNER,project_id:'NayaNET',action:'law_authority_decision',status:'SUCCESS',evidence:{
    node_id:'NAYA-KERNEL-LAW',law_request:{action:'naya_node_apply',target:NAYA},
    law_decision:{status:'AUTHORIZED',owner_id:OWNER,naya_id:NAYA,action:'naya_node_apply',target:NAYA,
      authority_refs:['grant-1'],evaluated_at:time,expires_at:null}}};
  if(omitTime) delete law.evidence.law_decision.evaluated_at;
  const grant={grant_id:'grant-1',issuer_id:OWNER,subject_id:OWNER,status:'ACTIVE',revoked_at:null,
    expires_at:null,actions:['naya_node_apply'],scope:{target:NAYA},...grantPatch};
  const isHit=capability==='provenance_preservation';
  const recorded={status:isHit?'HIT':'MISS',selected_block_id:isHit?'IB-ELIGIBLE':null,applicable:isHit,
    reason:isHit?'OWNER_SCOPED_CURRENT_BLOCK_MATCHES_REQUIRED_CAPABILITY':'NO_ELIGIBLE_APPLICABLE_INTELLIGENCE',
    retrieval_creates_authority:false};
  const prior={id:'retrieval-1',user_id:OWNER,project_id:'NayaNET',action:'know_context_retrieval',
    evidence:{law_receipt_id:'law-1',request:context,result:recorded}};
  const client={from(table){
    const call={table,filters:[]};reads.push(call);
    const matches=row=>call.filters.every(([key,value])=>row?.[key]===value);
    return {
      select(){return this;},eq(key,value){call.filters.push([key,value]);return this;},
      order(){return this;},limit(){return this;},
      async maybeSingle(){
        const candidates=table==='nayanet_execution_receipts'?[law,prior]:table==='nayanet_authority_grants'?[grant]:[];
        return {data:candidates.find(matches)??null,error:null};
      },
      then(resolve,reject){
        return Promise.resolve({data:table==='nayanet_intelligent_blocks'?[block].filter(matches):[],error:null}).then(resolve,reject);
      },
      insert(row){
        assert.equal(table,'nayanet_execution_receipts');writes.push(row);
        return {select(){return {async single(){return failWrite?{data:null,error:{message:'receipt interrupted'}}:
          {data:{...row,id:'offline-retrieval-receipt'},error:null};}};}};
      }
    };
  }};
  vm.runInNewContext(code,{URL,Request,Response,Date:Clock,console,selectKnowContext,validateKnowAuthority,
    Deno:{env:{get:key=>({SUPABASE_URL:'https://offline.invalid',SUPABASE_SERVICE_ROLE_KEY:'offline-key'})[key]},
      serve:callback=>{handler=callback;}},createRemoteJWKSet:()=>({}),
    jwtVerify:async(token,key,options)=>{authOptions.push(options);return {payload:identity};},createClient:()=>client});
  return {reads,writes,authOptions,invoke:(header='Bearer offline')=>handler(new Request('https://offline.invalid',{
    method:'POST',headers:{authorization:header,'content-type':'application/json'},
    body:JSON.stringify({mode,...context,law_receipt_id:'law-1',retrieval_receipt_id:'retrieval-1'})}))};
}

for(const mode of ['retrieve','inspect']) {
  for(const invalid of [{omitTime:true},{time:null},{time:''},{time:'2026-09-29T20:00:01Z'}]) {
    test(`actual KNOW ${mode} refuses time ${JSON.stringify(invalid)} before private reads`,async()=>{
      const rt=runtime({mode,...invalid}),response=await rt.invoke(),body=await response.json();
      assert.deepEqual({status:response.status,privateRead:rt.reads.some(x=>x.table==='nayanet_intelligent_blocks'),writes:rt.writes.length},
        {status:403,privateRead:false,writes:0});assert.equal(body.ok,false);
      assert.equal(body.error,'LAW_EVALUATED_AT_INVALID');
      assert.equal(rt.reads.some(x=>x.table==='nayanet_intelligent_blocks'),false);
      assert.equal(rt.writes.length,0);
    });
  }
  for(const capability of ['provenance_preservation','arithmetic_only']) {
    test(`actual KNOW ${mode} preserves authorized ${capability} selection`,async()=>{
      const rt=runtime({mode,capability}),response=await rt.invoke(),body=await response.json();
      assert.equal(response.status,200);assert.equal(body.ok,true);
      const result=mode==='retrieve'?body.result:body.recomputed;
      assert.equal(result.status,capability==='provenance_preservation'?'HIT':'MISS');
      assert.equal(result.selected_block_id,capability==='provenance_preservation'?'IB-ELIGIBLE':null);
      assert.equal(result.retrieval_creates_authority,false);
      const grantRead=rt.reads.findIndex(x=>x.table==='nayanet_authority_grants');
      const privateRead=rt.reads.findIndex(x=>x.table==='nayanet_intelligent_blocks');
      assert.ok(grantRead>=0&&privateRead>grantRead);
      assert.deepEqual(rt.reads[privateRead].filters,[['owner_id',OWNER]]);
      assert.equal(rt.writes.length,mode==='retrieve'?1:0);
      if(mode==='retrieve') {
        assert.equal(body.receipt.id,'offline-retrieval-receipt');
        assert.equal(rt.writes[0].evidence.law_receipt_id,'law-1');
        assert.deepEqual(Array.from(rt.writes[0].evidence.authority_refs),['grant-1']);
      } else assert.equal(body.persisted_universe_reread,true);
      assert.equal(rt.authOptions[0].issuer,'https://token.actions.githubusercontent.com');
      assert.equal(rt.authOptions[0].audience,'nayanet-runtime');
    });
  }
  test(`actual KNOW ${mode} preserves live-grant refusal before private reads`,async()=>{
    for(const [grantPatch,reason] of [
      [{status:'REVOKED',revoked_at:NOW},'LIVE_AUTHORITY_NOT_ACTIVE'],
      [{expires_at:NOW},'LIVE_AUTHORITY_EXPIRED'],
      [{issuer_id:'other'},'LIVE_AUTHORITY_OWNER_MISMATCH'],
      [{scope:{target:'OTHER'}},'LIVE_AUTHORITY_TARGET_MISMATCH'],
      [{actions:[]},'LIVE_AUTHORITY_ACTION_MISMATCH']
    ]) {
      const rt=runtime({mode,grantPatch}),response=await rt.invoke(),body=await response.json();
      assert.equal(response.status,403);assert.equal(body.error,reason);
      assert.equal(rt.reads.some(x=>x.table==='nayanet_intelligent_blocks'),false);
      assert.equal(rt.writes.length,0);
    }
  });
  test(`actual KNOW ${mode} preserves OIDC binding before privileged access`,async()=>{
    for(const identity of [{...claims,workflow_ref:'wrong'},{...claims,ref:'refs/heads/other'},
      {...claims,repository:'other/repo'}]) {
      const rt=runtime({mode,identity}),body=await (await rt.invoke()).json();
      assert.equal(body.error,'WORKFLOW_BINDING_MISMATCH');
      assert.equal(rt.reads.length,0);assert.equal(rt.writes.length,0);
    }
    const rt=runtime({mode}),body=await (await rt.invoke('')).json();
    assert.equal(body.error,'RUNTIME_IDENTITY_REQUIRED');assert.equal(rt.reads.length,0);
  });
}

test('actual KNOW interrupted receipt persistence cannot claim completed retrieval',async()=>{
  const rt=runtime({failWrite:true}),body=await (await rt.invoke()).json();
  assert.equal(body.ok,false);assert.equal(body.error,'receipt interrupted');
  assert.equal(body.receipt,undefined);
});


test('actual KNOW explicitly trusts canonical PROVE workflow without widening arbitrary workflows', async()=>{
  const proveClaims={...claims,
    workflow_ref:'SoulSchoolAcademy/NayaPOWER/.github/workflows/live-prove-proof.yml@refs/heads/main'};
  const rt=runtime({identity:proveClaims}),response=await rt.invoke(),body=await response.json();
  assert.equal(response.status,200);
  assert.equal(body.ok,true);
  assert.equal(body.status,'KNOW_RETRIEVED');
  assert.equal(body.result.status,'HIT');
  assert.equal(body.retrieval_creates_authority,false);
  assert.equal(rt.writes.length,1);
  assert.equal(rt.writes[0].evidence.workflow_ref,proveClaims.workflow_ref);

  const unlisted={...claims,
    workflow_ref:'SoulSchoolAcademy/NayaPOWER/.github/workflows/unlisted-proof.yml@refs/heads/main'};
  const denied=runtime({identity:unlisted}),deniedResponse=await denied.invoke(),deniedBody=await deniedResponse.json();
  assert.equal(deniedResponse.status,400);
  assert.equal(deniedBody.error,'WORKFLOW_BINDING_MISMATCH');
  assert.equal(denied.reads.length,0);
  assert.equal(denied.writes.length,0);
});
