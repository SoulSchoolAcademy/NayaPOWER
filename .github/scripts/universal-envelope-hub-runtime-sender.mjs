import { chromium } from 'playwright';
import fs from 'node:fs';
import crypto from 'node:crypto';
import { spawnSync } from 'node:child_process';
import { buildNoMutationProof, classifySenderFailure, resolveProofMode, summarizeReceiverBridgeResponse, summarizeReceiverResponse } from './stream-e-failure-diagnostics.mjs';
const hub=process.env.HUB_URL, run=process.env.GITHUB_RUN_ID||'LOCAL';
const currentRef=process.env.GITHUB_REF||'UNPINNED_LOCAL';
const eventName=process.env.GITHUB_EVENT_NAME||'LOCAL';
const headRef=process.env.GITHUB_HEAD_REF||'';
const headSha=process.env.GITHUB_SHA||'UNAVAILABLE';
const proofMode=resolveProofMode(currentRef,eventName,headRef);
if(proofMode==='NON_MAIN_NO_MUTATION'){
  const proof=buildNoMutationProof({ref:currentRef,eventName,headRef,headSha,runId:run});
  fs.writeFileSync('universal-envelope-hub-runtime-sender-proof.json',JSON.stringify(proof,null,2)+'\n');
  console.log('NON_MAIN_NO_MUTATION',JSON.stringify(proof));
  process.exit(0);
}
const alias=('envelopesender'+run+'-'+crypto.randomBytes(4).toString('hex')).toLowerCase().replace(/[^a-z0-9]/g,'').slice(0,48);
const title='Universal Envelope Hub Runtime Sender '+run;
const note='Meaningful output emitted by the canonical NayaNET Hub runtime and normalized into Universal Intelligence Envelope V1 for the existing Project Intelligence Bridge.';
const trace=[];
const mark=(step,extra={})=>{const row={step,at:new Date().toISOString(),...extra};trace.push(row);console.log('HUB_RUNTIME_SENDER_TRACE',JSON.stringify(row));};
const request=async(url,options={})=>{const r=await fetch(url,options);const raw=await r.text();let body;try{body=JSON.parse(raw)}catch{body={raw}};return {status:r.status,body}};
(async()=>{
  const browser=await chromium.launch({headless:true});
  const context=await browser.newContext({serviceWorkers:'block'});
  const page=await context.newPage();
  page.on('request',req=>{if(req.url().includes('/functions/v1/v7-smart-note-canonical'))mark('SMART_NOTE_RECEIVER_REQUEST',{method:req.method(),idempotency_key:req.headers()['x-idempotency-key']||'UNAVAILABLE'})});
  page.on('response',async response=>{if(!response.url().includes('/functions/v1/v7-smart-note-canonical'))return;let body={};try{body=JSON.parse(await response.text())}catch{};mark('SMART_NOTE_RECEIVER_RESPONSE',summarizeReceiverResponse(response.status(),body,response.request().headers()['x-idempotency-key']||''))});
  await page.goto(hub+'/?naya_release='+process.env.GITHUB_SHA,{waitUntil:'domcontentloaded',timeout:60000});
  await page.waitForFunction(()=>!!window.NayaAssistantRuntime&&!!window.__NayaNETSupabaseClient,{timeout:30000});
  const runtime=await page.evaluate(async({alias})=>{
    const c=window.__NayaNETSupabaseClient;
    let session=(await c.auth.getSession()).data.session;
    if(!session){
      const created=await c.auth.signInAnonymously({options:{data:{display_name:'Naya Hub Runtime Sender',smart_name:'Naya Hub Runtime Sender',smart_alias:alias}}});
      if(created.error)throw created.error;
      session=created.data.session;
    }
    const r=await window.NayaAssistantRuntime.init();
    const current=(await c.auth.getSession()).data.session||session;
    return {authenticated:r.authenticated,user_id:r.user_id,session:current};
  },{alias});
  if(!runtime.authenticated||!runtime.user_id||!runtime.session?.access_token)throw Error('HUB_RUNTIME_SESSION_NOT_ESTABLISHED');
  if(!runtime.authenticated||!runtime.user_id||!runtime.session?.access_token)throw Error('HUB_RUNTIME_SESSION_NOT_ESTABLISHED');
  const capture=await page.evaluate(async({title,note})=>window.NayaAssistantRuntime.captureSmartNote({title,content:note,source:'universal-envelope-hub-runtime-sender',status:'active',tags:['universal-envelope','hub-runtime','sender-coverage']}),{title,note});
  const eventId=String(capture?.event?.event_id||capture?.event_id||capture?.transaction?.evidence?.event_id||'');
  const transactionId=String(capture?.transaction?.id||'');
  if(!eventId||!transactionId)throw Error('HUB_RUNTIME_CAPTURE_LINEAGE_MISSING');
  mark('MEANINGFUL_OUTPUT_EMITTED',{event_id:eventId,transaction_id:transactionId});
  const envelope={
    schema:'NAYANET_UNIVERSAL_INTELLIGENCE_ENVELOPE_V1',
    envelope_id:'hub-runtime:'+run,
    source:{type:'nayanet_hub_runtime',id:'runtime:'+runtime.user_id},
    identity:{actor_type:'naya_runtime',actor_id:'NayaAssistantRuntime'},
    owner_scope:{owner_id:runtime.user_id,project_id:'NayaNET'},
    occurred_at:new Date().toISOString(),received_at:new Date().toISOString(),
    output:{kind:'smart_note_capture',title,content:note,capture},
    meaningfulness:'MEANINGFUL',
    provenance:{source_ref:'hub://'+new URL(hub).host+'/feed',source_event_id:eventId,source_id:transactionId},
    epistemic:{status:'OBSERVED'},privacy:{visibility:'PRIVATE'},
    authority:{status:'CONTEXT_ONLY'},
    context:{project:'NayaNET',surface:'Hub',runtime:'NayaAssistantRuntime',route:'/feed',proof_run:run},
    idempotency_key:'hub-runtime-envelope-'+run
  };
  fs.writeFileSync('/tmp/universal-envelope-hub-runtime.json',JSON.stringify(envelope,null,2));
  fs.writeFileSync('/tmp/hub-runtime-owner-id',runtime.user_id);
  const py=String.raw`
import hashlib,json,os
from pathlib import Path
import sys
sys.path.insert(0,str(Path('.naya/runtime').resolve()))
from universal_intelligence_envelope import UniversalIntelligenceEnvelope
from project_intelligence_bridge import packet,accept_universal_envelope,validate
env=json.loads(Path('/tmp/universal-envelope-hub-runtime.json').read_text())
os.environ['NAYANET_OWNER_ID']=Path('/tmp/hub-runtime-owner-id').read_text().strip()
UniversalIntelligenceEnvelope.from_mapping(env)
p=accept_universal_envelope(env,packet())
p['sender']={'type':'nayanet_hub_runtime','repository':'SoulSchoolAcademy/NayaPOWER','runtime':'NayaAssistantRuntime'}
p['source_ref']=env['provenance']['source_ref']
p['created_at']=env['occurred_at']
p['freshness']={'source_ref':p['source_ref'],'resolution':'LIVE'}
p['idempotency_key']=env['idempotency_key']
canonical=json.dumps(p,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
p['content_hash']=hashlib.sha256(canonical).hexdigest()
from uuid import NAMESPACE_URL,uuid5
p['packet_id']=str(uuid5(NAMESPACE_URL,'nayanet:project-intelligence:'+p['source_ref']+':'+os.environ['RUN_IDENTITY']+':'+p['content_hash']))
errors=validate(p)
if errors: raise SystemExit('ADAPTED_PACKET_INVALID:'+json.dumps(errors))
Path('/tmp/hub-runtime-packet.json').write_text(json.dumps(p,ensure_ascii=False,separators=(',',':')))
print(json.dumps({'status':'PASS','envelope_id':env['envelope_id'],'sender_type':p['sender']['type'],'packet_id':p['packet_id']}))
`;
  const pyResult=spawnSync('python',['-c',py],{encoding:'utf8',env:{...process.env,NAYANET_OWNER_ID:runtime.user_id}});
  if(pyResult.status!==0)throw Error('PYTHON_ADAPTER_FAILED:'+pyResult.stdout+pyResult.stderr);
  console.log('ENVELOPE_ADAPTER_PROOF='+pyResult.stdout.trim());
  const packet=JSON.parse(fs.readFileSync('/tmp/hub-runtime-packet.json','utf8'));
  const oidcReq=await fetch(process.env.ACTIONS_ID_TOKEN_REQUEST_URL+'&audience=nayanet-project-intelligence-bridge',{headers:{Authorization:'bearer '+process.env.ACTIONS_ID_TOKEN_REQUEST_TOKEN}});
  const oidc=await oidcReq.json(); if(!oidcReq.ok||!oidc.value)throw Error('OIDC_TOKEN_FAILED');
  const bridge=await request(process.env.SUPABASE_URL+'/functions/v1/nayanet-project-intelligence-bridge',{method:'POST',headers:{authorization:'Bearer '+oidc.value,'content-type':'application/json'},body:JSON.stringify(packet)});
  const bridgeTrace=summarizeReceiverBridgeResponse(bridge.status,bridge.body);
  mark('PRODUCTION_RECEIVER_RESPONSE',bridgeTrace);
  console.log('BRIDGE='+JSON.stringify(bridge.body));
  if(bridge.status===403&&bridge.body?.code==='REF_NOT_AUTHORIZED'){
    mark('PRODUCTION_RECEIVER_AUTHORITY_GATE',{status:'PASS',code:'REF_NOT_AUTHORIZED',detail:'Current proof runs from a non-main ref; the canonical production bridge correctly requires refs/heads/main. No production authority is weakened for PR execution.'});
    const proof={schema:'NAYANET_UNIVERSAL_ENVELOPE_HUB_RUNTIME_SENDER_PROOF_V1',status:'PARTIAL',first_failure_boundary:'PRODUCTION_RECEIVER_AUTHORIZATION',partial_state:'PARTIAL_STATE_OBSERVED',downstream_reachability:'REACHED_RECEIVER_AUTHORIZATION_FAILED',run_id:run,envelope_id:envelope.envelope_id,sender:{type:'nayanet_hub_runtime',runtime:'NayaAssistantRuntime',owner_id:runtime.user_id,source_event_id:eventId},checks:{meaningful_output_emitted:'PASS',envelope_v1_validated:'PASS',existing_adapter:'PASS',production_receiver_authority_gate:'PASS',production_receiver_positive_path:'NOT_RUN_NON_MAIN_REF'},receiver_response:bridgeTrace,truth_boundary:'Hub runtime is proven through the existing adapter and the production receiver authorization boundary rejects non-main refs. Positive production receiver persistence/retrieval/replay remains reserved for the main-ref production bridge proof.'};
    fs.writeFileSync('universal-envelope-hub-runtime-sender-proof.json',JSON.stringify(proof,null,2)+'\n');
    await context.close(); await browser.close(); return;
  }
  if(bridge.status!==200||bridge.body.status!=='COMPLETED'||!bridge.body.persisted||!bridge.body.indexed||!bridge.body.projected)throw Error('PRODUCTION_RECEIVER_FAILED');
  if(bridge.body.owner_id!==runtime.user_id)throw Error('OWNER_LINEAGE_MISMATCH');
  mark('PRODUCTION_RECEIVER_ACCEPTED',{packet_id:bridge.body.packet_id,receiver_event_id:bridge.body.receiver_event_id,receipt_id:bridge.body.receipt_id});
  const retrieved=await request(process.env.SUPABASE_URL+'/functions/v1/nayanet-project-intelligence-retrieve',{method:'POST',headers:{authorization:'Bearer '+runtime.session.access_token,apikey:process.env.SUPABASE_PUBLISHABLE_KEY,'content-type':'application/json'},body:JSON.stringify({query:bridge.body.receiver_event_id})});
  if(retrieved.status!==200||!retrieved.body.ok||!retrieved.body.result?.events?.length)throw Error('INDEPENDENT_RETRIEVAL_FAILED');
  const ev=retrieved.body.result.events.find(x=>x.event_id===bridge.body.receiver_event_id); if(!ev)throw Error('RECEIVER_EVENT_NOT_RECONSTRUCTED');
  const content=JSON.parse(ev.content), lineage=content.bridge||{}, intel=content.intelligence||[];
  if(lineage.receiver_transaction_id!==bridge.body.receiver_transaction_id||lineage.receiver_event_id!==bridge.body.receiver_event_id||lineage.receipt_id!==bridge.body.receipt_id||ev.receipt_id!==bridge.body.receipt_id)throw Error('RECEIVER_LINEAGE_MISMATCH');
  const universal=intel.find(x=>x.object_id==='envelope:'+envelope.envelope_id);
  if(!universal||universal.content?.source?.type!=='nayanet_hub_runtime'||universal.content?.envelope_id!==envelope.envelope_id)throw Error('UNIVERSAL_SENDER_LINEAGE_NOT_PRESERVED');
  const index=await request(process.env.SUPABASE_URL+'/rest/v1/nayanet_intelligence_index?select=id,owner_id&source_table=eq.nayanet_cognition_events&source_id=eq.'+encodeURIComponent(bridge.body.projection.cognition_event_id),{headers:{apikey:process.env.SUPABASE_PUBLISHABLE_KEY,authorization:'Bearer '+runtime.session.access_token}});
  if(index.status!==200||!index.body.some(x=>x.id===bridge.body.projection.index_id&&x.owner_id===runtime.user_id))throw Error('INDEX_RECONSTRUCTION_FAILED');
  mark('INDEPENDENT_RECONSTRUCTION',{receiver_event_id:bridge.body.receiver_event_id,receipt_id:bridge.body.receipt_id,index_id:bridge.body.projection.index_id,envelope_id:envelope.envelope_id});
  const replay=await request(process.env.SUPABASE_URL+'/functions/v1/nayanet-project-intelligence-bridge',{method:'POST',headers:{authorization:'Bearer '+oidc.value,'content-type':'application/json'},body:JSON.stringify(packet)});
  console.log('REPLAY='+JSON.stringify(replay.body));
  if(replay.status!==200||replay.body.status!=='ACCEPTED'||replay.body.replay!==true||replay.body.receiver_event_id!==bridge.body.receiver_event_id||replay.body.receipt_id!==bridge.body.receipt_id)throw Error('EXACT_REPLAY_FAILED');
  mark('EXACT_REPLAY_VERIFIED');
  const proof={schema:'NAYANET_UNIVERSAL_ENVELOPE_HUB_RUNTIME_SENDER_PROOF_V1',status:'VERIFIED',run_id:run,envelope_id:envelope.envelope_id,sender:{type:'nayanet_hub_runtime',runtime:'NayaAssistantRuntime',owner_id:runtime.user_id,source_event_id:eventId},receiver:{packet_id:bridge.body.packet_id,receiver_transaction_id:bridge.body.receiver_transaction_id,receiver_event_id:bridge.body.receiver_event_id,receipt_id:bridge.body.receipt_id,cognition_event_id:bridge.body.projection.cognition_event_id,index_id:bridge.body.projection.index_id},checks:{meaningful_output_emitted:'PASS',envelope_v1_validated:'PASS',existing_adapter:'PASS',existing_production_receiver:'PASS',sender_lineage_preserved:'PASS',independent_reconstruction:'PASS',exact_replay:'PASS'},truth_boundary:'Hub runtime is proven as a second sender into the same existing Project Intelligence Bridge; this does not prove every possible sender.'};
  fs.writeFileSync('universal-envelope-hub-runtime-sender-proof.json',JSON.stringify(proof,null,2)+'\n');
  console.log('CHAIN_RESULT='+JSON.stringify(proof));
  await context.close(); await browser.close();
})().catch(async error=>{await new Promise(resolve=>setTimeout(resolve,100));const requestTrace=trace.find(row=>row.step==='SMART_NOTE_RECEIVER_REQUEST')||null;const responseTrace=trace.find(row=>row.step==='SMART_NOTE_RECEIVER_RESPONSE')||null;const receiverResponseTrace=trace.find(row=>row.step==='PRODUCTION_RECEIVER_RESPONSE')||null;const classification=classifySenderFailure(error,responseTrace,receiverResponseTrace);const artifact={status:'FAILED',error:String(error?.stack||error),...classification,correlation:{idempotency_key:requestTrace?.idempotency_key||'UNAVAILABLE',receiver_response:responseTrace,production_receiver_response:receiverResponseTrace},trace};fs.writeFileSync('universal-envelope-hub-runtime-sender-proof.json',JSON.stringify(artifact,null,2)+'\n');console.error(error);process.exit(1)});