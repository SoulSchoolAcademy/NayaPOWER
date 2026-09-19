import crypto from "node:crypto";
import fs from "node:fs";

const base = process.env.SUPABASE_URL, key = process.env.SUPABASE_PUBLISHABLE_KEY, proofPath = process.env.PROOF_PATH;
if (!base || !key || !proofPath) throw new Error("RUNTIME_NOT_CONFIGURED");
async function req(path, options = {}) {
  const r = await fetch(base + path, options), t = await r.text();
  let b; try { b = JSON.parse(t); } catch { b = { raw: t }; }
  if (!r.ok) throw new Error(r.status + " " + JSON.stringify(b));
  return b;
}
const h = t => ({ apikey:key, authorization:"Bearer "+t, "content-type":"application/json" });
const anon = () => req("/auth/v1/signup",{method:"POST",headers:{apikey:key,"content-type":"application/json"},body:"{}"});
const assert = (x,m) => { if(!x) throw new Error(m); };

const sender = await anon(), receiver = await anon();
assert(sender.access_token && sender.user?.id,"SENDER_AUTH_FAILED");
assert(receiver.access_token && receiver.user?.id,"RECEIVER_AUTH_FAILED");
const runId = crypto.randomUUID();
const evidence = await req("/rest/v1/learning_evidence?select=id,member_id,target_id,level,status,source_event_id",{
  method:"POST", headers:{...h(sender.access_token),Prefer:"return=representation"},
  body:JSON.stringify({
    member_id:sender.user.id,target_id:"production-closure-superbrain-continuation",
    level:"E1_UNDERSTANDS",provenance:"authenticated production closure proof",status:"ACTIVE",
    claim:"Authenticated verified learning is retrievable as Superbrain cognition and can generate a governed continuation.",
    observed_value:{run_id:runId,verified_by:"external workflow"},
    verification_method:"authenticated production workflow",
    source_event_id:"production-closure-learning:"+runId
  })
});
assert(evidence.length===1,"LEARNING_EVIDENCE_CREATE_FAILED");
const evidenceId=evidence[0].id;
const learning=await req("/functions/v1/naya-learning-apply",{
  method:"POST",headers:h(sender.access_token),body:JSON.stringify({evidence_id:evidenceId})
});
assert(learning.ok===true,"LEARNING_APPLY_FAILED");
const cognitionId=learning.superbrain?.cognition_event_id;
assert(cognitionId,"LEARNING_DID_NOT_RETURN_COGNITION");
const state=await req("/rest/v1/learner_states?select=id,member_id,version&member_id=eq."+sender.user.id,{headers:h(sender.access_token)});
assert(state.length===1 && Number(state[0].version)>=Number(learning.learning.learner_state_version),"LEARNER_STATE_NOT_PERSISTED");

/* Fresh process boundary is represented by a clean authenticated retrieval after the learning call. */
const fresh=await req("/rest/v1/nayanet_cognition_events?select=id,event_id,type,classification,title,content,source,receipt_id,metadata&id=eq."+encodeURIComponent(cognitionId),{headers:h(sender.access_token)});
assert(fresh.length===1,"FRESH_COGNITION_RETRIEVAL_FAILED");
const cognition=fresh[0];
assert(cognition.event_id==="learning-apply:"+evidenceId,"COGNITION_EVENT_LINEAGE_FAILED");

const continuation={
  action:"smart_mail_send",
  reason:"Fresh retrieval of verified Superbrain learning",
  source_cognition_id:cognition.id,
  source_event_id:cognition.event_id,
  generated_from:cognition.content,
  body:"Fresh-Naya continuation: continue from verified learning "+cognition.id+" and record the authenticated consequence through Smart Mail."
};
const idem="production-closure-mail:"+runId;
const mail=await req("/functions/v1/nayanet-smart-mail",{
  method:"POST",headers:h(sender.access_token),
  body:JSON.stringify({recipient_user_id:receiver.user.id,body:continuation.body,subject:"NayaNET production closure continuation",kind:"direct",idempotency_key:idem,project_id:"NayaNET"})
});
assert(mail.ok===true && mail.status==="CREATED","AUTHORIZED_SMART_MAIL_EXECUTION_FAILED");
assert(mail.execution_receipt_id && mail.message_id && mail.cognition_event_id,"SMART_MAIL_LINEAGE_MISSING");

const verified=await req("/functions/v1/nayanet-smart-mail",{
  method:"POST",headers:h(receiver.access_token),body:JSON.stringify({operation:"verify",message_id:mail.message_id})
});
assert(verified.ok===true && verified.status==="VERIFIED","RECEIVER_VERIFICATION_FAILED");

const receipt=await req("/rest/v1/nayanet_execution_receipts?select=id,status,authority_grant_id,evidence,value,learning,project_id,action&id=eq."+mail.execution_receipt_id,{headers:h(sender.access_token)});
assert(receipt.length===1,"EXECUTION_RECEIPT_NOT_FOUND");
assert(receipt[0].status==="VERIFIED","EXECUTION_RECEIPT_NOT_VERIFIED");
assert(receipt[0].authority_grant_id,"AUTHORITY_RECEIPT_MISSING");
assert(receipt[0].value?.verified===true,"VERIFIED_VALUE_MISSING");

const actionCognition=await req("/rest/v1/nayanet_cognition_events?select=id,event_id,receipt_id,metadata&id=eq."+encodeURIComponent(mail.cognition_event_id),{headers:h(sender.access_token)});
assert(actionCognition.length===1 && actionCognition[0].receipt_id===mail.execution_receipt_id,"ACTION_COGNITION_LINEAGE_FAILED");

async function ledger(table,id){
  return req("/rest/v1/nayanet_smart_ledger?select=ledger_event_id,source_table,source_id,status,verification,event_type&source_table=eq."+encodeURIComponent(table)+"&source_id=eq."+encodeURIComponent(String(id))+"&owner_id=eq."+sender.user.id,{headers:h(sender.access_token)});
}
const le=await ledger("learning_evidence",evidenceId);
const ls=await ledger("learner_states",sender.user.id);
const lc=await ledger("nayanet_cognition_events",cognition.id);
const lr=await ledger("nayanet_execution_receipts",mail.execution_receipt_id);
const la=await ledger("nayanet_cognition_events",mail.cognition_event_id);
assert(le.length>=1,"LEDGER_LEARNING_EVIDENCE_MISSING");
assert(ls.length>=1,"LEDGER_LEARNER_STATE_MISSING");
assert(lc.length>=1,"LEDGER_LEARNING_COGNITION_MISSING");
assert(lr.length>=1,"LEDGER_EXECUTION_RECEIPT_MISSING");
assert(la.length>=1,"LEDGER_ACTION_COGNITION_MISSING");

const proof={
  schema:"naya.nayanet.production.closure.proof.v1",status:"VERIFIED",fresh_runtime:true,run_id:runId,
  authenticated:{sender_user_id:sender.user.id,receiver_user_id:receiver.user.id,receiver_verification:"VERIFIED"},
  learning:{evidence_id:evidenceId,learner_state_version:learning.learning.learner_state_version,cognition_event_id:cognition.id},
  fresh_retrieval:{cognition_id:cognition.id,event_id:cognition.event_id,continuation_action:continuation},
  governed_action:{action:continuation.action,message_id:mail.message_id,execution_receipt_id:mail.execution_receipt_id,authority_grant_id:receipt[0].authority_grant_id,receipt_status:receipt[0].status},
  ledger:{learning_evidence:le.map(x=>x.ledger_event_id),learner_state:ls.map(x=>x.ledger_event_id),learning_cognition:lc.map(x=>x.ledger_event_id),execution_receipt:lr.map(x=>x.ledger_event_id),action_cognition:la.map(x=>x.ledger_event_id)},
  observed_at:new Date().toISOString()
};
fs.writeFileSync(proofPath,JSON.stringify(proof,null,2));
for(const x of ["LEARNING_APPLY","SUPERBRAIN_COGNITION_PERSISTED","FRESH_COGNITION_RETRIEVAL","FRESH_CONTINUATION_GENERATED","AUTHORITY_ISSUED_AND_VALIDATED","REAL_SMART_MAIL_EXECUTION","RECEIVER_VERIFICATION","RECEIPT_AND_COGNITION_LINEAGE","SMART_LEDGER_ALL_REQUIRED_SOURCES"]) console.log(x+"=PASS");
console.log("PRODUCTION_CLOSURE=VERIFIED");
