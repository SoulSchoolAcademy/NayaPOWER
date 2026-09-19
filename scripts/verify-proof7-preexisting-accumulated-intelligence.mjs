import fs from 'node:fs';
import crypto from 'node:crypto';

const base=process.env.SUPABASE_URL,key=process.env.SUPABASE_PUBLISHABLE_KEY,token=process.env.PROOF7_OWNER_ACCESS_TOKEN;
if(!base||!key) throw new Error('RUNTIME_NOT_CONFIGURED');
if(!token) throw new Error('PREEXISTING_OWNER_ACCESS_TOKEN_REQUIRED');

async function req(url,opt={}){const r=await fetch(url,opt),t=await r.text();let b;try{b=JSON.parse(t)}catch{b={raw:t}}if(!r.ok)throw new Error(r.status+' '+JSON.stringify(b));return b}
const h=t=>({apikey:key,authorization:'Bearer '+t,'content-type':'application/json'});
const started=new Date().toISOString();
const activityPath='NAYA-TEAM/2026/09/18/2026-09-18T19-28-00-0700__PROOF7-ACCUMULATED-INTELLIGENCE-CONTINUATION.md';
const activity=fs.readFileSync(activityPath,'utf8');
const activityHash=crypto.createHash('sha256').update(activity).digest('hex');

const owner=await req(base+'/auth/v1/user',{headers:h(token)});
if(!owner.id)throw new Error('AUTHENTICATED_OWNER_NOT_OBSERVED');
const states=await req(base+'/rest/v1/learner_states?select=member_id,version,current_evidence_by_target&member_id=eq.'+encodeURIComponent(owner.id),{headers:h(token)});
if(states.length!==1)throw new Error('OWNER_LEARNER_STATE_NOT_FOUND');

let source=null;
for(const [target,p] of Object.entries(states[0].current_evidence_by_target||{})){
 if(!p?.evidence_id)continue;
 const rows=await req(base+'/rest/v1/learning_evidence?select=id,member_id,target_id,level,provenance,status,claim,source_event_id,created_at&member_id=eq.'+encodeURIComponent(owner.id)+'&id=eq.'+encodeURIComponent(p.evidence_id)+'&status=eq.ACTIVE',{headers:h(token)});
 if(rows.length===1&&new Date(rows[0].created_at)<new Date(started)&&!target.startsWith('proof7-')&&!rows[0].claim.toLowerCase().includes('proof 7')){source={target,evidence:rows[0],replay_id:p.replay_id||null};break}
}
if(!source)throw new Error('NO_PREEXISTING_AUTHENTICATED_ACCUMULATED_INTELLIGENCE');

const decision=await req(base+'/functions/v1/naya-decision-context',{method:'POST',headers:h(token),body:JSON.stringify({target_id:source.target})});
if(!decision.ok||decision.decision?.influenced!==true)throw new Error('PREEXISTING_INTELLIGENCE_NOT_RETRIEVABLE');
if(decision.decision.context?.evidence_id!==source.evidence.id)throw new Error('PREEXISTING_EVIDENCE_LINEAGE_MISMATCH');
if(decision.decision.context?.source_event_id!==source.evidence.source_event_id)throw new Error('PREEXISTING_SOURCE_LINEAGE_MISMATCH');
if(decision.decision.authority?.changed!==false||decision.decision.authority?.granted!==false)throw new Error('AUTHORITY_CHANGED');

const receiver=await req(base+'/auth/v1/signup',{method:'POST',headers:{apikey:key,'content-type':'application/json'},body:'{}'});
if(!receiver.access_token||!receiver.user?.id)throw new Error('RECEIVER_PROVISIONING_FAILED');
const idem='proof7-preexisting-action-'+crypto.randomBytes(8).toString('hex');
const action=await req(base+'/functions/v1/nayanet-smart-mail',{method:'POST',headers:h(token),body:JSON.stringify({recipient_user_id:receiver.user.id,body:'Fresh-Naya continuation selected from pre-existing accumulated intelligence target '+source.target+': '+source.evidence.claim,subject:'NayaNET Proof 7 pre-existing intelligence continuation',kind:'direct',idempotency_key:idem,project_id:'NayaNET'})});
if(action.status!=='CREATED'||action.authority_changed!==false)throw new Error('PREEXISTING_INTELLIGENCE_ACTION_FAILED');

const received=await req(base+'/rest/v1/v7_mail_messages?select=id&thread_id=eq.'+encodeURIComponent(action.thread_id),{headers:h(receiver.access_token)});
if(received.length!==1||received[0].id!==action.message_id)throw new Error('RECEIVER_RETRIEVAL_FAILED');
const verified=await req(base+'/functions/v1/nayanet-smart-mail',{method:'POST',headers:h(receiver.access_token),body:JSON.stringify({operation:'verify',message_id:action.message_id})});
if(verified.status!=='VERIFIED')throw new Error('RECEIVER_VERIFICATION_FAILED');

const cog=await req(base+'/rest/v1/nayanet_cognition_events?select=id,event_id,receipt_id&id=eq.'+encodeURIComponent(action.cognition_event_id),{headers:h(token)});
const receipt=await req(base+'/rest/v1/nayanet_execution_receipts?select=id,status,value&id=eq.'+encodeURIComponent(action.execution_receipt_id),{headers:h(token)});
if(cog.length!==1||cog[0].receipt_id!==action.execution_receipt_id)throw new Error('ACTION_COGNITION_RECEIPT_LINEAGE_FAILED');
if(receipt.length!==1||receipt[0].status!=='SUCCESS'||receipt[0].value?.verified!==true)throw new Error('ACTION_RECEIPT_VERIFICATION_FAILED');

const evidence=await req(base+'/rest/v1/learning_evidence',{method:'POST',headers:{...h(token),Prefer:'return=representation'},body:JSON.stringify({member_id:owner.id,target_id:source.target+'-continuation-'+action.message_id,level:'E1_UNDERSTANDS',provenance:'VERIFICATION',status:'ACTIVE',claim:'Pre-existing accumulated intelligence was retrieved by the authenticated owner and produced a real governed Smart Mail action whose receiver retrieval and receipt were verified.',observed_value:{source_target_id:source.target,source_evidence_id:source.evidence.id,action_message_id:action.message_id,action_receipt_id:action.execution_receipt_id,verified:true},verification_method:'authenticated owner retrieval + receiver verification + execution receipt + cognition lineage',source_event_id:cog[0].event_id})});
if(evidence.length!==1)throw new Error('OUTCOME_LEARNING_PERSISTENCE_FAILED');
const applied=await req(base+'/functions/v1/naya-learning-apply',{method:'POST',headers:h(token),body:JSON.stringify({evidence_id:evidence[0].id})});
if(!applied.ok||!applied.learning?.learner_state_version)throw new Error('OUTCOME_LEARNING_APPLY_FAILED');
const next=await req(base+'/functions/v1/naya-decision-context',{method:'POST',headers:h(token),body:JSON.stringify({target_id:evidence[0].target_id})});
if(!next.ok||next.decision?.influenced!==true)throw new Error('NEXT_NAYA_CANNOT_RETRIEVE_NEW_LEARNING');

const proof={schema:'naya.nayanet.superbrain.proof7.preexisting-accumulated-intelligence.v1',status:'VERIFIED',proof_started_at:started,activity_record:{path:activityPath,sha256:activityHash},owner:{user_id:owner.id},source:{target_id:source.target,evidence_id:source.evidence.id,source_event_id:source.evidence.source_event_id,evidence_created_at:source.evidence.created_at,learner_state_version_at_start:states[0].version},decision:{decision:decision.decision.decision,influenced:true,evidence_id:decision.decision.context.evidence_id,source_event_id:decision.decision.context.source_event_id,authority_changed:decision.decision.authority.changed,authority_granted:decision.decision.authority.granted},action:{message_id:action.message_id,cognition_event_id:action.cognition_event_id,receipt_id:action.execution_receipt_id,receiver_id:receiver.user.id,receiver_verified:true,receipt_status:receipt[0].status,verified_value:receipt[0].value.verified_value},outcome_learning:{evidence_id:evidence[0].id,learner_state_version:applied.learning.learner_state_version,fresh_retrieval_influenced:true},policy:{improvement:'NOT_PROVEN'},observed_at:new Date().toISOString()};
fs.writeFileSync(process.env.PROOF_PATH,JSON.stringify(proof,null,2));
console.log('PREEXISTING_SOURCE=PASS');
console.log('AUTHENTICATED_OWNER_RETRIEVAL=PASS');
console.log('DECISION_DERIVED_FROM_PREEXISTING_INTELLIGENCE=PASS');
console.log('AUTHORITY_UNCHANGED=PASS');
console.log('REAL_SMART_MAIL_ACTION=PASS');
console.log('RECEIVER_VERIFICATION=PASS');
console.log('RECEIPT_COGNITION_LINEAGE=PASS');
console.log('NEW_LEARNING=PASS');
console.log('FRESH_NEXT_NAYA_RETRIEVAL=PASS');
console.log('PROOF7_PREEXISTING_ACCUMULATED_INTELLIGENCE=VERIFIED');