import crypto from 'node:crypto';
import fs from 'node:fs';
const base=process.env.SUPABASE_URL,key=process.env.SUPABASE_PUBLISHABLE_KEY;
async function req(url,opt={}){const r=await fetch(url,opt),t=await r.text();let b;try{b=JSON.parse(t)}catch{b={raw:t}}if(!r.ok)throw new Error(r.status+' '+JSON.stringify(b));return b}
const h=t=>({apikey:key,authorization:'Bearer '+t,'content-type':'application/json'});
const anon=()=>req(base+'/auth/v1/signup',{method:'POST',headers:{apikey:key,'content-type':'application/json'},body:'{}'});
const sender=await anon(),receiver=await anon();
const target='proof7-controlled-mail-'+crypto.randomBytes(8).toString('hex');
const send=(token,recipient,body,idem)=>req(base+'/functions/v1/nayanet-smart-mail',{method:'POST',headers:h(token),body:JSON.stringify({recipient_user_id:recipient,body,subject:'NayaNET Proof 7 controlled action',kind:'direct',idempotency_key:idem,project_id:'NayaNET'})});
const verify=(token,messageId)=>req(base+'/functions/v1/nayanet-smart-mail',{method:'POST',headers:h(token),body:JSON.stringify({operation:'verify',message_id:messageId})});
const initial=await send(sender.access_token,receiver.user.id,'Proof 7 historical experience: the receiver successfully retrieved a governed Smart Mail message.', 'proof7-history-'+crypto.randomBytes(8).toString('hex'));
const initialRows=await req(base+'/rest/v1/v7_mail_messages?select=id&thread_id=eq.'+initial.thread_id,{headers:h(receiver.access_token)});
if(initialRows.length!==1)throw new Error('INITIAL_RECEIVER_RETRIEVAL_FAILED');
await verify(receiver.access_token,initial.message_id);
const initialCognition=await req(base+'/rest/v1/nayanet_cognition_events?select=id,event_id,receipt_id&id=eq.'+initial.cognition_event_id,{headers:h(sender.access_token)});
if(initialCognition.length!==1||initialCognition[0].receipt_id!==initial.execution_receipt_id)throw new Error('INITIAL_COGNITION_LINEAGE_FAILED');
const dreamKey='proof7-dream-'+crypto.randomBytes(8).toString('hex');
const dream=await req(base+'/functions/v1/naya-dream-replay',{method:'POST',headers:{...h(sender.access_token),'x-idempotency-key':dreamKey},body:JSON.stringify({event_id:initialCognition[0].event_id,idempotency_key:dreamKey,project_id:'NayaNET'})});
if(!dream.ok||dream.replay?.status!=='SIMULATED')throw new Error('PROOF7_DREAM_FAILED');
const evidence=await req(base+'/rest/v1/learning_evidence',{
 method:'POST',headers:{...h(sender.access_token),'Prefer':'return=representation'},
 body:JSON.stringify({member_id:sender.user.id,target_id:target,level:'E1_UNDERSTANDS',provenance:'VERIFICATION',status:'ACTIVE',claim:'A verified Smart Mail outcome can be reused by a later Naya decision to choose the same governed communication path.',observed_value:{initial_message_id:initial.message_id,initial_receipt_id:initial.execution_receipt_id,dream_replay_id:dream.replay.id},verification_method:'production receiver retrieval + canonical Dream replay',source_event_id:initialCognition[0].event_id})
});
if(!Array.isArray(evidence)||evidence.length!==1)throw new Error('LEARNING_EVIDENCE_FAILED');
const evidenceId=evidence[0].id;
const applied=await req(base+'/functions/v1/naya-learning-apply',{method:'POST',headers:h(sender.access_token),body:JSON.stringify({evidence_id:evidenceId,replay_id:dream.replay.id})});
if(!applied.ok||!applied.learning?.learner_state_version)throw new Error('LEARNING_APPLY_FAILED');
const freshDecision=await req(base+'/functions/v1/naya-decision-context',{method:'POST',headers:h(sender.access_token),body:JSON.stringify({target_id:target})});
if(!freshDecision.ok||freshDecision.decision?.decision!=='USE_VERIFIED_LEARNING_CONTEXT'||freshDecision.decision?.influenced!==true)throw new Error('PROOF7_DECISION_NOT_INFLUENCED');
if(freshDecision.decision?.authority?.changed!==false||freshDecision.decision?.authority?.granted!==false)throw new Error('PROOF7_AUTHORITY_CHANGED');
if(freshDecision.decision?.context?.replay_id!==dream.replay.id)throw new Error('PROOF7_LINEAGE_LOST');
if(freshDecision.decision?.verification?.evidence_status!=='ACTIVE')throw new Error('PROOF7_EVIDENCE_NOT_ACTIVE');
if(freshDecision.decision?.decision!=='USE_VERIFIED_LEARNING_CONTEXT')throw new Error('ACTION_GATE_NOT_SATISFIED');
const action=await send(sender.access_token,receiver.user.id,'Proof 7 controlled action: this message was sent only after a later decision consumed verified learning context.', 'proof7-action-'+crypto.randomBytes(8).toString('hex'));
if(action.status!=='CREATED'||action.authority_changed!==false)throw new Error('PROOF7_ACTION_FAILED');
const actionRows=await req(base+'/rest/v1/v7_mail_messages?select=id,thread_id,body,metadata&thread_id=eq.'+action.thread_id,{headers:h(receiver.access_token)});
if(actionRows.length!==1||actionRows[0].id!==action.message_id)throw new Error('PROOF7_ACTION_NOT_RECEIVED');
const actionVerify=await verify(receiver.access_token,action.message_id);
if(actionVerify.status!=='VERIFIED')throw new Error('PROOF7_ACTION_NOT_VERIFIED');
const actionCognition=await req(base+'/rest/v1/nayanet_cognition_events?select=id,event_id,receipt_id&id=eq.'+action.cognition_event_id,{headers:h(sender.access_token)});
const actionReceipt=await req(base+'/rest/v1/nayanet_execution_receipts?select=id,action,status,evidence,learning,value&id=eq.'+action.execution_receipt_id,{headers:h(sender.access_token)});
if(actionCognition.length!==1||actionCognition[0].receipt_id!==action.execution_receipt_id)throw new Error('PROOF7_ACTION_COGNITION_LINEAGE_FAILED');
if(actionReceipt.length!==1||actionReceipt[0].status!=='SUCCESS'||actionReceipt[0].value?.verified!==true)throw new Error('PROOF7_ACTION_RECEIPT_VALUE_FAILED');
const outcomeEvidence=await req(base+'/rest/v1/learning_evidence',{
 method:'POST',headers:{...h(sender.access_token),'Prefer':'return=representation'},
 body:JSON.stringify({member_id:sender.user.id,target_id:target+'-outcome',level:'E1_UNDERSTANDS',provenance:'VERIFICATION',status:'ACTIVE',claim:'The learned decision produced a real governed Smart Mail action whose receiver retrieval and receipt were verified.',observed_value:{decision:'USE_VERIFIED_LEARNING_CONTEXT',action_message_id:action.message_id,action_receipt_id:action.execution_receipt_id,verified_value:actionReceipt[0].value.verified_value},verification_method:'receiver verification + execution receipt + cognition receipt lineage',source_event_id:actionCognition[0].event_id})
});
if(outcomeEvidence.length!==1)throw new Error('PROOF7_OUTCOME_LEARNING_FAILED');
const outcomeApplied=await req(base+'/functions/v1/naya-learning-apply',{method:'POST',headers:h(sender.access_token),body:JSON.stringify({evidence_id:outcomeEvidence[0].id})});
if(!outcomeApplied.ok||outcomeApplied.learning?.learner_state_version<=applied.learning.learner_state_version)throw new Error('PROOF7_NEW_LEARNING_NOT_COMPOUNDING');
const nextDreamKey='proof7-next-dream-'+crypto.randomBytes(8).toString('hex');
const nextDream=await req(base+'/functions/v1/naya-decision-context',{method:'POST',headers:h(sender.access_token),body:JSON.stringify({target_id:target+'-outcome'})});
if(!nextDream.ok||nextDream.decision?.influenced!==true)throw new Error('PROOF7_NEXT_NAYA_CANNOT_RETRIEVE_NEW_LEARNING');
const proof={schema:'naya.nayanet.superbrain.proof7.production.v1',status:'VERIFIED',proofs:{experience:true,memory:true,dream:true,learning:true,continuity:true,decision:true,outcome:true},lineage:{initial_event_id:initialCognition[0].event_id,initial_dream_id:dream.replay.id,learning_evidence_id:evidenceId,learner_state_version:applied.learning.learner_state_version,decision:'USE_VERIFIED_LEARNING_CONTEXT',action_message_id:action.message_id,action_cognition_event_id:actionCognition[0].event_id,action_receipt_id:action.execution_receipt_id,action_verified_value:actionReceipt[0].value.verified_value,outcome_learning_evidence_id:outcomeEvidence[0].id,next_learner_state_version:outcomeApplied.learning.learner_state_version,next_learning_retrievable:nextDream.decision.influenced===true},governance:{authority_changed:false,authority_granted:false},policy:{improvement:'NOT_PROVEN'},observed_at:new Date().toISOString()};
fs.writeFileSync(process.env.PROOF_PATH,JSON.stringify(proof,null,2));
console.log('PROOF7_EXPERIENCE=PASS');console.log('PROOF7_MEMORY=PASS');console.log('PROOF7_DREAM=PASS');console.log('PROOF7_LEARNING=PASS');console.log('PROOF7_CONTINUITY=PASS');console.log('PROOF7_DECISION=PASS');console.log('PROOF7_OUTCOME=PASS');console.log('PROOF7_AUTHORITY_UNCHANGED=PASS');console.log('PROOF7_NEW_LEARNING=PASS');console.log('PROOF7_NEXT_DREAM_CONTEXT=PASS');console.log('PROOF7_POLICY_IMPROVEMENT=NOT_PROVEN');console.log('PROOF7_STATUS=VERIFIED');