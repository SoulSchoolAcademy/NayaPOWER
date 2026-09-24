import { chromium } from 'playwright';
import fs from 'node:fs';
import crypto from 'node:crypto';

const B=process.env.SUPABASE_URL;
const K=process.env.SUPABASE_PUBLISHABLE_KEY;
const RUN=process.env.RUN_IDENTITY;
const HUB=process.env.HUB_URL;
const SAME_OUTPUT='Equivalent meaningful output for cross-sender Universal Intelligence Envelope V1 invariance proof.';
const request=async(path,options={})=>{
  const r=await fetch(B+path,options); const raw=await r.text(); let body; try{body=JSON.parse(raw)}catch{body={raw}};
  return {status:r.status,body};
};
const post=async(path,token,body)=>request('/functions/v1/'+path,{method:'POST',headers:{apikey:K,authorization:'Bearer '+token,'content-type':'application/json'},body:JSON.stringify(body)});
const signup=async()=>{const r=await request('/auth/v1/signup',{method:'POST',headers:{apikey:K,'content-type':'application/json'},body:'{}'});if(r.status!==200||!r.body.access_token)throw Error('FRESH_OWNER_AUTH_FAILED');return r.body};
const oidc=async()=>{const r=await fetch(process.env.ACTIONS_ID_TOKEN_REQUEST_URL+'&audience=nayanet-project-intelligence-bridge',{headers:{Authorization:'bearer '+process.env.ACTIONS_ID_TOKEN_REQUEST_TOKEN}});const j=await r.json();if(!r.ok||!j.value)throw Error('OIDC_TOKEN_FAILED');return j.value};
const bridge=async(token,p)=>post('nayanet-project-intelligence-bridge',token,p);
const retrieve=async(token,eventId)=>post('nayanet-project-intelligence-retrieve',token,{query:eventId});

const envelopeInvariants={
  schema:'NAYANET_UNIVERSAL_INTELLIGENCE_ENVELOPE_V1',
  required:['envelope_id','source','identity','owner_scope','occurred_at','received_at','output','meaningfulness','provenance','epistemic','privacy','authority','context','idempotency_key'],
  meaningfulness:'MEANINGFUL',
  epistemic:'OBSERVED',
  privacy:'PRIVATE',
  authority:'CONTEXT_ONLY'
};
const shape=(e)=>{
  const required=Object.fromEntries(envelopeInvariants.required.map(k=>[k,Object.prototype.hasOwnProperty.call(e,k)]));
  return {
    schema:e.schema,
    required,
    source_type:typeof e.source?.type,
    source_id:typeof e.source?.id,
    identity_actor_type:typeof e.identity?.actor_type,
    identity_actor_id:typeof e.identity?.actor_id,
    owner_id_present:typeof e.owner_scope?.owner_id==='string'&&e.owner_scope.owner_id.length>0,
    project_id:e.owner_scope?.project_id,
    meaningfulness:e.meaningfulness,
    provenance_source_ref:typeof e.provenance?.source_ref,
    provenance_source_id:typeof e.provenance?.source_id,
    epistemic_status:e.epistemic?.status,
    privacy_visibility:e.privacy?.visibility,
    authority_status:e.authority?.status,
    idempotency_present:typeof e.idempotency_key==='string'&&e.idempotency_key.length>0
  };
};

async function makeGithubSender(){
  const a=await signup();
  const envelope={
    schema:envelopeInvariants.schema,envelope_id:'cross:github:'+RUN,
    source:{type:'github_actions',id:'run:'+process.env.GITHUB_RUN_ID},
    identity:{actor_type:'naya',actor_id:'github-actions'},
    owner_scope:{owner_id:a.user.id,project_id:'NayaNET'},
    occurred_at:new Date().toISOString(),received_at:new Date().toISOString(),
    output:{kind:'equivalent_meaningful_output',content:SAME_OUTPUT},
    meaningfulness:'MEANINGFUL',
    provenance:{source_ref:'github://actions/'+process.env.GITHUB_RUN_ID,source_id:'run:'+process.env.GITHUB_RUN_ID},
    epistemic:{status:'OBSERVED'},privacy:{visibility:'PRIVATE'},authority:{status:'CONTEXT_ONLY'},
    context:{project:'NayaNET',sender:'github_actions',proof_run:RUN},
    idempotency_key:'cross-sender-github-'+RUN
  };
  return {name:'github_actions',token:a.access_token,owner:a.user.id,envelope};
}

async function makePiSender(){
  const a=await signup();
  const s=await post('nayanet-pi-understand',a.access_token,{title:'Cross-Sender Invariance '+RUN,content:SAME_OUTPUT,confidence:1,tags:['cross-sender','invariance']});
  if(s.status!==200||!s.body.ok)throw Error('PI_SENDER_FAILED:'+JSON.stringify(s.body));
  const ev=s.body.result.event;
  const envelope={
    schema:envelopeInvariants.schema,envelope_id:'cross:pi:'+RUN,
    source:{type:'nayanet_pi_understand',id:'edge:nayanet-pi-understand'},
    identity:{actor_type:'naya_edge_function',actor_id:'nayanet-pi-understand'},
    owner_scope:{owner_id:a.user.id,project_id:'NayaNET'},
    occurred_at:new Date().toISOString(),received_at:new Date().toISOString(),
    output:{kind:'equivalent_meaningful_output',content:SAME_OUTPUT,event:ev},
    meaningfulness:'MEANINGFUL',
    provenance:{source_ref:'supabase://functions/nayanet-pi-understand',source_event_id:ev.event_id,source_id:ev.event_id},
    epistemic:{status:'OBSERVED'},privacy:{visibility:'PRIVATE'},authority:{status:'CONTEXT_ONLY'},
    context:{project:'NayaNET',sender:'nayanet_pi_understand',proof_run:RUN},
    idempotency_key:'cross-sender-pi-'+RUN
  };
  return {name:'nayanet_pi_understand',token:a.access_token,owner:a.user.id,envelope};
}

async function makeHubSender(){
  const browser=await chromium.launch({headless:true});
  const page=await browser.newPage();
  const alias=('cross'+RUN+crypto.randomBytes(4).toString('hex')).toLowerCase().replace(/[^a-z0-9]/g,'').slice(0,48);
  await page.goto(HUB+'/?naya_release='+process.env.GITHUB_SHA,{waitUntil:'domcontentloaded',timeout:60000});
  await page.waitForFunction(()=>!!window.NayaAssistantRuntime&&!!window.__NayaNETSupabaseClient,{timeout:30000});
  const r=await page.evaluate(async({alias,text})=>{
    const c=window.__NayaNETSupabaseClient;
    let s=(await c.auth.getSession()).data.session;
    if(!s){const x=await c.auth.signInAnonymously({options:{data:{display_name:'Cross Sender Invariance',smart_name:'Cross Sender Invariance',smart_alias:alias}}});if(x.error)throw x.error;s=x.data.session}
    const runtime=await window.NayaAssistantRuntime.init();
    const cap=await window.NayaAssistantRuntime.captureSmartNote({title:'Cross-Sender Invariance',content:text,source:'cross-sender-invariance',status:'active',tags:['cross-sender','invariance']});
    return {runtime_user:runtime.user_id,session:s,event:cap?.event||cap};
  },{alias,text:SAME_OUTPUT});
  if(!r.session?.access_token||!r.runtime_user)throw Error('HUB_SENDER_AUTH_FAILED');
  const envelope={
    schema:envelopeInvariants.schema,envelope_id:'cross:hub:'+RUN,
    source:{type:'nayanet_hub_runtime',id:'runtime:'+r.runtime_user},
    identity:{actor_type:'naya_runtime',actor_id:'NayaAssistantRuntime'},
    owner_scope:{owner_id:r.runtime_user,project_id:'NayaNET'},
    occurred_at:new Date().toISOString(),received_at:new Date().toISOString(),
    output:{kind:'equivalent_meaningful_output',content:SAME_OUTPUT,event:r.event},
    meaningfulness:'MEANINGFUL',
    provenance:{source_ref:'hub://'+new URL(HUB).host+'/feed',source_event_id:String(r.event?.event_id||''),source_id:String(r.event?.transaction_id||r.event?.id||'')},
    epistemic:{status:'OBSERVED'},privacy:{visibility:'PRIVATE'},authority:{status:'CONTEXT_ONLY'},
    context:{project:'NayaNET',sender:'nayanet_hub_runtime',runtime:'NayaAssistantRuntime',proof_run:RUN},
    idempotency_key:'cross-sender-hub-'+RUN
  };
  await browser.close();
  return {name:'nayanet_hub_runtime',token:r.session.access_token,owner:r.runtime_user,envelope};
}

const senderResults=[];
try{
  const senders=[await makeGithubSender(),await makeHubSender(),await makePiSender()];
  const auth=await oidc();
  for(const s of senders){
    const env=s.envelope;
    const required=env.schema===envelopeInvariants.schema && envelopeInvariants.required.every(k=>Object.prototype.hasOwnProperty.call(env,k));
    if(!required||env.meaningfulness!=='MEANINGFUL'||env.epistemic.status!=='OBSERVED'||env.privacy.visibility!=='PRIVATE'||env.authority.status!=='CONTEXT_ONLY'||!env.idempotency_key)throw Error('LOCAL_ENVELOPE_INVARIANTS_FAILED:'+s.name);
    const packet={
      protocol:'NAYANET_PROJECT_INTELLIGENCE_BRIDGE_V1',packet_id:crypto.randomUUID(),project_id:'NayaNET',owner_id:s.owner,
      sender:{type:s.name,repository:'SoulSchoolAcademy/NayaPOWER',ref:'main'},
      receiver:{type:'nayanet_intelligent_hub',canonical_source:'NAYANET/HUB/index.html'},
      source_ref:env.provenance.source_ref,created_at:env.occurred_at,
      freshness:{source_ref:env.provenance.source_ref,resolution:'LIVE'},
      operating_context:{project:'NayaNET',sender:s.name,proof_run:RUN},
      intelligence:[{object_id:'envelope:'+env.envelope_id,operation:'UPSERT',content:env}],
      provenance:[{path:env.provenance.source_ref,sha256:crypto.createHash('sha256').update(JSON.stringify(env.output)).digest('hex'),bytes:JSON.stringify(env.output).length}],
      privacy:{default_visibility:'PRIVATE'},idempotency_key:env.idempotency_key,
      content_hash:'pending',universal_envelope_ids:[env.envelope_id]
    };
    packet.content_hash=crypto.createHash('sha256').update(JSON.stringify(packet)).digest('hex');
    const br=await bridge(auth,packet);
    if(br.status!==200||br.body.status!=='COMPLETED'||!br.body.persisted||!br.body.indexed||!br.body.projected)throw Error('RECEIVER_FAILED:'+s.name+':'+JSON.stringify(br.body));
    if(br.body.owner_id!==s.owner)throw Error('OWNER_LINEAGE_FAILED:'+s.name);
    const rr=await retrieve(s.token,br.body.receiver_event_id);
    if(rr.status!==200||!rr.body.ok)throw Error('RETRIEVAL_FAILED:'+s.name);
    const ev=rr.body.result.events.find(x=>x.event_id===br.body.receiver_event_id);
    if(!ev)throw Error('RECEIVER_EVENT_NOT_FOUND:'+s.name);
    const content=JSON.parse(ev.content);
    const observed=content.intelligence?.find(x=>x.object_id==='envelope:'+env.envelope_id)?.content;
    if(!observed)throw Error('ENVELOPE_NOT_OBSERVED:'+s.name);
    const observedShape=shape(observed);
    const expected=shape(env);
    if(JSON.stringify(observedShape)!==JSON.stringify(expected))throw Error('OBSERVED_INVARIANTS_CHANGED:'+s.name+':'+JSON.stringify({expected,observed:observedShape}));
    const replay=await bridge(auth,packet);
    if(replay.status!==200||replay.body.status!=='ACCEPTED'||replay.body.replay!==true||replay.body.receiver_transaction_id!==br.body.receiver_transaction_id||replay.body.receiver_event_id!==br.body.receiver_event_id||replay.body.receipt_id!==br.body.receipt_id)throw Error('REPLAY_FAILED:'+s.name);
    senderResults.push({sender:s.name,envelope_id:env.envelope_id,owner_scope_present:true,observed_shape:observedShape,receiver:{packet_id:br.body.packet_id,receiver_transaction_id:br.body.receiver_transaction_id,receiver_event_id:br.body.receiver_event_id,receipt_id:br.body.receipt_id,cognition_event_id:br.body.projection.cognition_event_id,index_id:br.body.projection.index_id},replay_same_lineage:true});
  }
  const shapes=senderResults.map(x=>JSON.stringify(x.observed_shape));
  const invariant=shapes.every(x=>x===shapes[0]);
  const identities=senderResults.map(x=>x.observed_shape.source_type);
  if(!invariant)throw Error('CROSS_SENDER_INVARIANCE_FAILED');
  if(new Set(identities).size!==3)throw Error('SENDER_IDENTITIES_COLLAPSED');
  const proof={schema:'NAYANET_UNIVERSAL_ENVELOPE_CROSS_SENDER_INVARIANCE_PROOF_V1',status:'VERIFIED',run_id:RUN,equivalent_output:SAME_OUTPUT,sender_classes:senderResults.map(x=>x.sender),invariant_fields:['schema','required envelope fields','source identity shape','owner scope presence','meaningfulness','provenance shape','epistemic status','privacy visibility','authority status','idempotency presence'],sender_results:senderResults,cross_sender_invariants_identical:true,sender_identities_distinct:true,truth_boundary:'Three sender classes produced equivalent meaningful output, normalized to Universal Intelligence Envelope V1, and the existing production receiver observed identical required envelope invariants while preserving distinct sender identity. This proves cross-sender contract invariance for these three sender classes, not universal interoperability across every possible sender.'};
  fs.writeFileSync('universal-envelope-cross-sender-invariance-proof.json',JSON.stringify(proof,null,2)+'\n');
  console.log('CROSS_SENDER_INVARIANCE=VERIFIED');
  console.log('SENDER_IDENTITIES='+identities.join(','));
  console.log('CHAIN_RESULT='+JSON.stringify(proof));
}catch(e){
  fs.writeFileSync('universal-envelope-cross-sender-invariance-proof.json',JSON.stringify({status:'FAILED',error:String(e?.stack||e),sender_results:senderResults},null,2)+'\n');
  console.error(e);process.exit(1);
}