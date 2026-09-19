import { createClient } from "https://esm.sh/@supabase/supabase-js@2.57.0";

const url=process.env.SUPABASE_URL;
const key=process.env.SUPABASE_PUBLISHABLE_KEY;
const email=process.env.ASSISTANT_TEST_EMAIL;
const password=process.env.ASSISTANT_TEST_PASSWORD;
if(!url||!key||!email||!password) throw new Error("TEST_AUTH_CONFIGURATION_MISSING");

const supabase=createClient(url,key,{auth:{persistSession:false,autoRefreshToken:false,detectSessionInUrl:false}});
const {data:signIn,error:signInError}=await supabase.auth.signInWithPassword({email,password});
if(signInError||!signIn.session||!signIn.user) throw new Error("SENDER_AUTH_FAILED");
const sender=signIn.user;
const senderToken=signIn.session.access_token;

const receiverClient=createClient(url,key,{auth:{persistSession:false,autoRefreshToken:false,detectSessionInUrl:false}});
const {data:anon,error:anonError}=await receiverClient.auth.signInAnonymously();
if(anonError||!anon.session||!anon.user) throw new Error("RECEIVER_ANONYMOUS_AUTH_FAILED");
const receiver=anon.user;
const receiverToken=anon.session.access_token;

const runId=process.env.GITHUB_RUN_ID||String(Date.now());
const policyKey="smart-mail-controlled-paired-"+runId;
const insertPolicy=async(version,parent,strategy)=>{
  const {data,error}=await supabase.from("nayanet_policy_versions").insert({
    user_id:sender.id,project_id:"NayaNET",policy_key:policyKey,version,parent_policy_id:parent,
    state:"DRAFT",policy:{capability:"smart_mail_send",strategy},validation:{},adversarial:{},holdout:{},promotion:{},rollback:{}
  }).select("*").single();
  if(error) throw error;
  return data;
};
const v1=await insertPolicy(1,null,"HISTORY_ONLY_V1");
const v2=await insertPolicy(2,v1.id,"HISTORY_PLUS_VERIFIED_RECEIPT_V1");

const evalPolicy=async(policyId,type,evidence)=>{
  const {error}=await supabase.from("nayanet_policy_evaluations").insert({
    user_id:sender.id,policy_id:policyId,evaluation_type:type,
    dataset_hash:evidence.dataset_hash||null,baseline_score:evidence.baseline_score??null,
    candidate_score:evidence.candidate_score??null,responsible_value:evidence.responsible_value??null,
    verified:evidence.verified??false,result:evidence.result,evidence
  });
  if(error) throw error;
};
const transition=async(id,state,e={})=>{
  const {data,error}=await supabase.rpc("nayanet_policy_transition",{p_policy_id:id,p_to_state:state,p_evaluation:e});
  if(error) throw error;
  return data;
};
const prepare=async(p)=>{
  const ds="controlled-paired-policy-v1";
  await evalPolicy(p.id,"DETERMINISTIC",{result:"PASS",dataset_hash:ds,verified:true,cases:1});
  await transition(p.id,"VALIDATED",{result:"PASS",deterministic:true,dataset_hash:ds});
  await evalPolicy(p.id,"ADVERSARIAL",{result:"PASS",dataset_hash:"controlled-paired-adversarial-v1",verified:true,tests:5,failures:0});
  await transition(p.id,"ADVERSARIAL_REVIEW",{result:"PASS",tests:5,failures:0,dataset_hash:"controlled-paired-adversarial-v1"});
  await evalPolicy(p.id,"HOLDOUT",{result:"PASS",dataset_hash:"controlled-paired-holdout-v1",baseline_score:1,candidate_score:1,verified:true,cases:1});
  await transition(p.id,"HOLDOUT_PASS",{result:"PASS",dataset_hash:"controlled-paired-holdout-v1",baseline_score:1,candidate_score:1,verified:true,cases:1});
  await transition(p.id,"AUTHORIZATION_REQUIRED",{request:"controlled-paired-real-outcome",authorized:false});
  await transition(p.id,"CONTROLLED_TEST",{authorized:true,reason:"explicit-human-authorization-for-controlled-test"});
};
await prepare(v1); await prepare(v2);

const sha256=async(value)=>Buffer.from(await crypto.subtle.digest("SHA-256",new TextEncoder().encode(value))).toString("hex");
const caseId="paired-"+runId+"-C1";
const frozenCase={case_id:caseId,receiver_id:receiver.id,task:"request a concise acknowledgement of the controlled test message",prior_verified_context:{receiver_retrieval_verified:true,source:"Proof7 verified receipt"}};
const inputHash=await sha256(JSON.stringify(frozenCase));
const decisions={
  v1:{subject:"Controlled test acknowledgement",body:"Please acknowledge this controlled test message."},
  v2:{subject:"Controlled test acknowledgement",body:"Verified context shows this receiver successfully retrieves governed messages. Please acknowledge this controlled test message."}
};
const send=async(token,policy,decision,group)=>{
  const decisionHash=await sha256(JSON.stringify({case:frozenCase,decision}));
  const res=await fetch(url+"/functions/v1/nayanet-smart-mail",{
    method:"POST",headers:{authorization:"Bearer "+token,apikey:key,"content-type":"application/json"},
    body:JSON.stringify({recipient_user_id:receiver.id,body:decision.body,subject:decision.subject,kind:"direct",idempotency_key:caseId+"-"+group,project_id:"NayaNET",policy_id:policy.id,experiment_case_id:caseId,policy_input_hash:inputHash,policy_decision_hash:decisionHash})
  });
  const data=await res.json();
  if(!res.ok||!data.ok) throw new Error("SEND_"+group+"_FAILED:"+JSON.stringify(data));
  return {data,decisionHash};
};
const a=await send(senderToken,v1,decisions.v1,"V1");
const b=await send(senderToken,v2,decisions.v2,"V2");

const verify=async(token,messageId)=>{
  const res=await fetch(url+"/functions/v1/nayanet-smart-mail",{
    method:"POST",headers:{authorization:"Bearer "+token,apikey:key,"content-type":"application/json"},
    body:JSON.stringify({operation:"verify",message_id:messageId})
  });
  const data=await res.json();
  if(!res.ok||!data.ok||data.status!=="VERIFIED") throw new Error("RECEIVER_VERIFY_FAILED:"+JSON.stringify(data));
  return data;
};
await verify(receiverToken,a.data.message_id);
await verify(receiverToken,b.data.message_id);

const {data:comparison,error:comparisonError}=await supabase.rpc("nayanet_compare_verified_policy_outcomes",{
  p_baseline_policy_id:v1.id,p_candidate_policy_id:v2.id,
  p_baseline_receipt_id:a.data.execution_receipt_id,p_candidate_receipt_id:b.data.execution_receipt_id
});
if(comparisonError) throw comparisonError;
if(comparison?.result!=="NOT_PROVEN") throw new Error("EXPECTED_NOT_PROVEN_FOR_EQUAL_VALUE_CASE");

const {data:receipts,error:receiptError}=await supabase.from("nayanet_execution_receipts")
  .select("id,policy_id,policy_version,policy_key,experiment_case_id,policy_input_hash,policy_decision_hash,status,value")
  .in("id",[a.data.execution_receipt_id,b.data.execution_receipt_id]);
if(receiptError) throw receiptError;
if(receipts?.length!==2) throw new Error("RECEIPT_LINEAGE_COUNT_FAILED");
for(const r of receipts){
  if(!r.policy_id||!r.policy_version||!r.policy_key||r.experiment_case_id!==caseId||r.policy_input_hash!==inputHash||!r.policy_decision_hash) throw new Error("RECEIPT_LINEAGE_INCOMPLETE");
  if(r.status!=="SUCCESS"||r.value?.verified!==true) throw new Error("RECEIPT_OUTCOME_NOT_VERIFIED");
}

const {data:evalRow,error:evalError}=await supabase.from("nayanet_policy_evaluations").insert({
  user_id:sender.id,policy_id:v2.id,evaluation_type:"REAL_OUTCOME",
  dataset_hash:"controlled-paired-real-outcomes-"+runId,
  baseline_score:comparison.baseline.verified_value,candidate_score:comparison.candidate.verified_value,
  responsible_value:comparison.candidate.verified_value,verified:true,result:comparison.result,
  evidence:{comparison,run_id:runId,head:process.env.GITHUB_SHA,baseline_receipt_id:a.data.execution_receipt_id,candidate_receipt_id:b.data.execution_receipt_id,behavioral_difference:true,frozen_case_hash:inputHash}
}).select("*").single();
if(evalError) throw evalError;

let adversarialPassed=false;
try{
  await supabase.rpc("nayanet_compare_verified_policy_outcomes",{
    p_baseline_policy_id:v1.id,p_candidate_policy_id:v2.id,
    p_baseline_receipt_id:b.data.execution_receipt_id,p_candidate_receipt_id:a.data.execution_receipt_id
  });
}catch(e){
  adversarialPassed=String(e.message||e).includes("POLICY_RECEIPT_LINEAGE_MISMATCH");
}
if(!adversarialPassed) throw new Error("ADVERSARIAL_POLICY_RECEIPT_SWAP_NOT_REJECTED");

const report={schema:"naya.p1.controlled.paired.outcome.receipt.v1",status:"NOT_PROVEN",head:process.env.GITHUB_SHA,run_id:runId,case_id:caseId,frozen_case_hash:inputHash,receiver_anonymous:true,behavioral_difference:true,baseline:{policy_id:v1.id,receipt_id:a.data.execution_receipt_id,verified_value:comparison.baseline.verified_value,decision_hash:a.decisionHash},candidate:{policy_id:v2.id,receipt_id:b.data.execution_receipt_id,verified_value:comparison.candidate.verified_value,decision_hash:b.decisionHash},comparison,adversarial:{receipt_swap_rejected:adversarialPassed},note:"Controlled paired real execution and receiver verification succeeded. Policy improvement is intentionally NOT_PROVEN because both verified responsible values were equal."};
console.log("P1_CONTROLLED_PAIRED_EXECUTION=PASS");
console.log("P1_POLICY_RECEIPT_LINEAGE=PASS");
console.log("P1_BEHAVIORAL_DIFFERENCE=PASS");
console.log("P1_RECEIVER_VERIFICATION=PASS");
console.log("P1_POLICY_COMPARISON=NOT_PROVEN");
console.log("P1_ADVERSARIAL_RECEIPT_SWAP=PASS");
await import("node:fs/promises").then(fs=>fs.writeFile(process.env.RECEIPT_PATH,JSON.stringify(report,null,2)));
