import crypto from 'node:crypto';

const base=process.env.SUPABASE_URL;
const key=process.env.SUPABASE_PUBLISHABLE_KEY;
const spaceId=process.env.NAYA_EXISTING_SPACE_ID||'04ee4dc8-bc73-47df-a1de-162570f6a56e';
const project='NayaNET-waveA-relationship-'+Date.now()+'-'+crypto.randomBytes(4).toString('hex');

async function req(url,opt={}) {
  const r=await fetch(url,opt);
  const t=await r.text();
  let b; try { b=JSON.parse(t); } catch { b={raw:t}; }
  if(!r.ok) throw new Error(r.status+' '+JSON.stringify(b));
  return b;
}
async function expectDenied(promise,label){
  try { await promise; throw new Error(label+'_UNEXPECTED_SUCCESS'); }
  catch(e){ const s=String(e); if(!/403|AUTHORITY_GRANT|DENIED|FAILED/.test(s)) throw new Error(label+'_UNEXPECTED_ERROR '+s); }
}
const h=t=>({apikey:key,authorization:'Bearer '+t,'content-type':'application/json'});
const signup=()=>req(base+'/auth/v1/signup',{method:'POST',headers:{apikey:key,'content-type':'application/json'},body:'{}'});
const A=await signup(),B=await signup(),C=await signup();
if(!A.access_token||!B.access_token||!C.access_token) throw new Error('USER_CREATION_FAILED');

const join=async(u)=>req(base+'/rest/v1/rpc/nayanet_join_space',{method:'POST',headers:h(u.access_token),body:JSON.stringify({p_space_id:spaceId})});
await join(A); await join(B); await join(C);

const save=async(u,target)=>req(base+'/rest/v1/rpc/nayanet_save_connection',{method:'POST',headers:h(u.access_token),body:JSON.stringify({p_target_member_id:target,p_space_id:spaceId})});
const ab=await save(A,B.user.id);
const ba=await save(B,A.user.id);
if(!ab?.connection?.id||!ba?.connection?.id) throw new Error('MUTUAL_CONNECTION_NOT_CREATED');

const connA=await req(base+'/rest/v1/nayanet_connections?select=id,owner_member_id,connected_member_id,status,source_space_id&owner_member_id=eq.'+A.user.id+'&connected_member_id=eq.'+B.user.id,{headers:h(A.access_token)});
const connB=await req(base+'/rest/v1/nayanet_connections?select=id,owner_member_id,connected_member_id,status&owner_member_id=eq.'+B.user.id+'&connected_member_id=eq.'+A.user.id,{headers:h(B.access_token)});
if(connA.length!==1||connB.length!==1||connA[0].status!=='active'||connB[0].status!=='active') throw new Error('MUTUAL_CONNECTION_READBACK_FAILED');

const list=await req(base+'/rest/v1/rpc/nayanet_create_smart_list',{method:'POST',headers:h(A.access_token),body:JSON.stringify({p_name:'Wave A B relationship '+project})});
const listId=list?.list_id||list?.id||list?.list?.id;
if(!listId) throw new Error('SMART_LIST_CREATE_FAILED');
await req(base+'/rest/v1/rpc/nayanet_add_connection_to_list',{method:'POST',headers:h(A.access_token),body:JSON.stringify({p_list_id:listId,p_connection_id:connA[0].id})});
const listA=await req(base+'/rest/v1/nayanet_smart_lists?select=id,owner_member_id,name&id=eq.'+listId,{headers:h(A.access_token)});
const listMembersA=await req(base+'/rest/v1/nayanet_smart_list_members?select=list_id,connection_id&list_id=eq.'+listId,{headers:h(A.access_token)});
const listB=await req(base+'/rest/v1/nayanet_smart_lists?select=id,owner_member_id,name&id=eq.'+listId,{headers:h(B.access_token)});
const listC=await req(base+'/rest/v1/nayanet_smart_lists?select=id,owner_member_id,name&id=eq.'+listId,{headers:h(C.access_token)});
if(listA.length!==1||listA[0].owner_member_id!==A.user.id||listMembersA.length!==1) throw new Error('SMART_LIST_OWNER_VISIBILITY_FAILED');
if(listB.length!==0||listC.length!==0) throw new Error('SMART_LIST_PRIVACY_ISOLATION_FAILED');

const send=(token,recipient,body,idem,grant)=>req(base+'/functions/v1/nayanet-smart-mail',{method:'POST',headers:h(token),body:JSON.stringify({recipient_user_id:recipient,body,subject:'Wave A relationship proof',kind:'direct',idempotency_key:idem,project_id:project,authority_grant_id:grant})});
const verify=(token,messageId)=>req(base+'/functions/v1/nayanet-smart-mail',{method:'POST',headers:h(token),body:JSON.stringify({operation:'verify',message_id:messageId})});

await expectDenied(send(A.access_token,B.user.id,'This must be denied without explicit authority.','wavea-no-grant-'+project,null),'NO_GRANT');

const grant=await req(base+'/rest/v1/rpc/nayanet_issue_authority_grant',{method:'POST',headers:h(A.access_token),body:JSON.stringify({
 p_subject_id:A.user.id,p_source_event_id:'wavea-authority-'+project,p_mission_id:'NayaNET Wave A real relationship journey',
 p_scope:{project_id:project,target:B.user.id,space_id:spaceId},p_actions:['smart_mail_send'],
 p_constraints:{mode:'wave-a-proof',no_external_side_effects:true},p_expires_at:new Date(Date.now()+15*60*1000).toISOString(),
 p_evidence:{authorization_type:'explicit_wave_a_authorization',space_id:spaceId,connection_id:connA[0].id},p_parent_authority:null
})});
if(!grant?.grant_id) throw new Error('AUTHORITY_GRANT_ISSUANCE_FAILED');
const valid=await req(base+'/rest/v1/rpc/nayanet_validate_authority_grant',{method:'POST',headers:h(A.access_token),body:JSON.stringify({p_grant_id:grant.grant_id,p_action:'smart_mail_send',p_target:B.user.id})});
if(valid?.status!=='AUTHORIZED') throw new Error('AUTHORITY_NOT_AUTHORIZED');

const idem='wavea-mail-'+project;
const first=await send(A.access_token,B.user.id,'Wave A real A-to-B governed Smart Mail action.',idem,grant.grant_id);
if(first.status!=='CREATED'||!first.message_id||!first.execution_receipt_id||!first.cognition_event_id) throw new Error('SMART_MAIL_CREATE_FAILED');
const replay=await send(A.access_token,B.user.id,'Wave A real A-to-B governed Smart Mail action.',idem,grant.grant_id);
if(replay.status!=='REPLAY'||replay.message_id!==first.message_id||replay.execution_receipt_id!==first.execution_receipt_id) throw new Error('IDEMPOTENT_REPLAY_FAILED');
const threadRows=await req(base+'/rest/v1/v7_mail_messages?select=id,metadata&thread_id=eq.'+first.thread_id,{headers:h(B.access_token)});
if(threadRows.length!==1||threadRows[0].id!==first.message_id) throw new Error('IDEMPOTENT_DUPLICATE_DURABLE_MESSAGE');
const outcome=await verify(B.access_token,first.message_id);
if(outcome.status!=='VERIFIED') throw new Error('RECEIVER_VERIFICATION_FAILED');

const receipt=await req(base+'/rest/v1/nayanet_execution_receipts?select=id,status,value,evidence,learning&id=eq.'+first.execution_receipt_id,{headers:h(A.access_token)});
const cognition=await req(base+'/rest/v1/nayanet_cognition_events?select=id,event_id,receipt_id&id=eq.'+first.cognition_event_id,{headers:h(A.access_token)});
if(receipt.length!==1||receipt[0].status!=='SUCCESS'||receipt[0].value?.verified!==true) throw new Error('RECEIPT_VERIFICATION_FAILED');
if(cognition.length!==1||cognition[0].receipt_id!==first.execution_receipt_id) throw new Error('COGNITION_RECEIPT_LINEAGE_FAILED');

const ledger=await req(base+'/rest/v1/nayanet_smart_ledger?select=ledger_event_id,source_table,source_id&source_table=eq.nayanet_cognition_events&source_id=eq.'+encodeURIComponent(cognition[0].event_id),{headers:h(A.access_token)});
if(ledger.length<1) throw new Error('LEDGER_LINEAGE_MISSING');

const evidence=await req(base+'/rest/v1/learning_evidence',{method:'POST',headers:{...h(A.access_token),'Prefer':'return=representation'},body:JSON.stringify({
 member_id:A.user.id,target_id:'wavea-'+project,level:'E1_UNDERSTANDS',provenance:'VERIFICATION',status:'ACTIVE',
 claim:'A real A-to-B governed Smart Mail action was independently verified by the receiver and linked to cognition and Ledger.',
 observed_value:{message_id:first.message_id,receipt_id:first.execution_receipt_id,cognition_event_id:cognition[0].event_id,ledger_event_id:ledger[0].id},
 verification_method:'receiver verification + receipt + cognition/Ledger lineage',source_event_id:cognition[0].event_id
})});
if(evidence.length!==1) throw new Error('LEARNING_EVIDENCE_FAILED');
const learning=await req(base+'/functions/v1/naya-learning-apply',{method:'POST',headers:h(A.access_token),body:JSON.stringify({evidence_id:evidence[0].id})});
if(!learning.ok||!learning.learning?.learner_state_version) throw new Error('LEARNING_APPLY_FAILED');

const revoked=await req(base+'/rest/v1/rpc/nayanet_revoke_authority_grant',{method:'POST',headers:h(A.access_token),body:JSON.stringify({p_grant_id:grant.grant_id,p_evidence:{reason:'Wave A revocation gate',project_id:project}})});
if(revoked?.status==='FAILED') throw new Error('AUTHORITY_REVOCATION_FAILED');
await expectDenied(send(A.access_token,B.user.id,'This must be denied after authority revocation.','wavea-after-revoke-'+project,grant.grant_id),'REVOKED_AUTHORITY');

const cRows=await req(base+'/rest/v1/v7_mail_messages?select=id,thread_id&sender_id=eq.'+A.user.id,{headers:h(C.access_token)});
if(cRows.length!==0) throw new Error('C_ISOLATION_FAILED');

const fresh=await req(base+'/functions/v1/naya-decision-context',{method:'POST',headers:h(A.access_token),body:JSON.stringify({target_id:'wavea-'+project})});
if(!fresh.ok||fresh.decision?.influenced!==true||fresh.decision?.context?.evidence_id!==evidence[0].id) throw new Error('FRESH_NAYA_RETRIEVAL_FAILED');
if(fresh.decision?.authority?.changed!==false) throw new Error('FRESH_NAYA_AUTHORITY_CHANGED');

const successor=await req(base+'/rest/v1/rpc/nayanet_issue_authority_grant',{method:'POST',headers:h(A.access_token),body:JSON.stringify({
 p_subject_id:A.user.id,p_source_event_id:'wavea-successor-authority-'+project,p_mission_id:'NayaNET Wave A fresh-Naya continuation',
 p_scope:{project_id:project,target:B.user.id,space_id:spaceId},p_actions:['smart_mail_send'],
 p_constraints:{mode:'fresh-naya-continuation',requires_verified_learning:evidence[0].id},
 p_expires_at:new Date(Date.now()+15*60*1000).toISOString(),
 p_evidence:{authorization_type:'explicit_successor_authorization',prior_learning_evidence_id:evidence[0].id},p_parent_authority:{revoked_grant_id:grant.grant_id}
})});
if(!successor?.grant_id) throw new Error('SUCCESSOR_AUTHORITY_FAILED');
const successorValid=await req(base+'/rest/v1/rpc/nayanet_validate_authority_grant',{method:'POST',headers:h(A.access_token),body:JSON.stringify({p_grant_id:successor.grant_id,p_action:'smart_mail_send',p_target:B.user.id})});
if(successorValid?.status!=='AUTHORIZED') throw new Error('SUCCESSOR_AUTHORITY_NOT_AUTHORIZED');
const continuation=await send(A.access_token,B.user.id,'Fresh-Naya continuation: durable verified learning was retrieved before this new governed action.', 'wavea-continuation-'+project,successor.grant_id);
if(continuation.status!=='CREATED') throw new Error('FRESH_NAYA_CONTINUATION_ACTION_FAILED');
const continuationVerify=await verify(B.access_token,continuation.message_id);
if(continuationVerify.status!=='VERIFIED') throw new Error('FRESH_NAYA_CONTINUATION_OUTCOME_FAILED');

console.log('WAVE_A_RELATIONSHIP=PASS');
console.log('SMART_LIST_PRIVACY=PASS');
console.log('NO_GRANT_DENIAL=PASS');
console.log('EXPLICIT_AUTHORITY=PASS');
console.log('SMART_MAIL_A_TO_B=PASS');
console.log('RECEIVER_VERIFICATION=PASS');
console.log('COGNITION_RECEIPT_LEDGER_LINEAGE=PASS');
console.log('IDEMPOTENT_REPLAY=PASS');
console.log('REVOCATION_DENIAL=PASS');
console.log('C_ISOLATION=PASS');
console.log('FRESH_NAYA_RETRIEVAL=PASS');
console.log('FRESH_NAYA_CONTINUATION=PASS');
console.log('PROJECT='+project);
console.log('INITIAL_MESSAGE_ID='+first.message_id);
console.log('INITIAL_RECEIPT_ID='+first.execution_receipt_id);
console.log('INITIAL_COGNITION_EVENT_ID='+cognition[0].event_id);
console.log('INITIAL_LEDGER_EVENT_ID='+ledger[0].id);
console.log('CONTINUATION_MESSAGE_ID='+continuation.message_id);
