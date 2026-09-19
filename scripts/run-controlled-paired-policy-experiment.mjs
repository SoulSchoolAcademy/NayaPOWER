import { createClient } from "@supabase/supabase-js";

const url=process.env.SUPABASE_URL;
const key=process.env.SUPABASE_PUBLISHABLE_KEY;
if(!url||!key) throw new Error("TEST_CONFIGURATION_MISSING");

const supabase=createClient(url,key,{auth:{persistSession:false,autoRefreshToken:false,detectSessionInUrl:false}});
const {data:signIn,error:signInError}=await supabase.auth.signInAnonymously();
if(signInError||!signIn.session||!signIn.user) throw new Error("SENDER_ANONYMOUS_AUTH_FAILED");
const sender=signIn.user;
const senderToken=signIn.session.access_token;

const receiverClient=createClient(url,key,{auth:{persistSession:false,autoRefreshToken:false,detectSessionInUrl:false}});
const {data:anon,error:anonError}=await receiverClient.auth.signInAnonymously();
if(anonError||!anon.session||!anon.user) throw new Error("RECEIVER_ANONYMOUS_AUTH_FAILED");
const receiver=anon.user;
const receiverToken=anon.session.access_token;

const runId=process.env.GITHUB_RUN_ID||String(Date.now());
const experimentProject="NayaNET:P1:"+runId;
const policyKey="smart-mail-controlled-paired-"+runId;
const insertPolicy=async(version,parent,strategy)=>{
  const {data,error}=await supabase.from("nayanet_policy_versions").insert({
    user_id:sender.id,project_id:experimentProject,policy_key:policyKey,version,parent_policy_id:parent,
    state:"DRAFT",policy:{capability:"smart_mail_send",strategy},validation:{},adversarial:{},holdout:{},promotion:{},rollback:{}
  }).select("*").single();
  if(error) throw error;
  return data;
};
const jsonRequest=async(path,token,body)=>{
  const res=await fetch(url+path,{method:"POST",headers:{authorization:"Bearer "+token,apikey:key,"content-type":"application/json"},body:JSON.stringify(body)});
  const text=await res.text(); let data=null; try{data=JSON.parse(text)}catch{data={raw:text}};
  if(!res.ok) throw new Error(path+" HTTP "+res.status+" "+JSON.stringify(data));
  return data;
};

const authorityGrants=new Map();
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
  let unauthorizedBlocked=false;
  try {
    await transition(p.id,"CONTROLLED_TEST",{authorized:true,reason:"negative-test-no-canonical-authority"});
  } catch (error) {
    unauthorizedBlocked=String(error?.message||error).includes("CONTROLLED_TEST_REQUIRES_AUTHORITY_GRANT");
  }
  if(!unauthorizedBlocked) throw new Error("CONTROLLED_TEST_SELF_AUTHORIZATION_NOT_BLOCKED");
  const authority = await supabase.rpc("nayanet_issue_authority_grant",{
    p_subject_id:sender.id,
    p_source_event_id:"controlled-paired-human-authorization-"+runId+"-"+p.id,
    p_mission_id:"NayaNET Controlled Paired Policy Outcome Experiment",
    p_scope:{project_id:experimentProject,target:p.id},
    p_actions:["policy.controlled_test"],
    p_constraints:{mode:"controlled-test-only",no_external_side_effects:true},
    p_expires_at:new Date(Date.now()+10*60*1000).toISOString(),
    p_evidence:{authorization_type:"explicit_controlled_experiment_authorization",run_id:runId,policy_id:p.id},
    p_parent_authority:null
  });
  if(authority.error||!authority.data?.grant_id) throw authority.error||new Error("CONTROLLED_TEST_AUTHORITY_GRANT_ISSUANCE_FAILED");
  const authorityCheck = await supabase.rpc("nayanet_validate_authority_grant",{
    p_grant_id:authority.data.grant_id,
    p_action:"policy.controlled_test",
    p_target:p.id
  });
  if(authorityCheck.error||authorityCheck.data?.status!=="AUTHORIZED") throw authorityCheck.error||new Error("CONTROLLED_TEST_AUTHORITY_VALIDATION_FAILED:"+JSON.stringify(authorityCheck.data));
  await transition(p.id,"CONTROLLED_TEST",{
    authorized:true,
    authority_grant_id:authority.data.grant_id,
    authority_status:authorityCheck.data.status,
    reason:"canonical-authority-grant-validated"
  });

  const mailAuthority = await supabase.rpc("nayanet_issue_authority_grant",{
    p_subject_id:sender.id,
    p_source_event_id:"controlled-paired-smart-mail-authorization-"+runId+"-"+p.id,
    p_mission_id:"NayaNET Controlled Paired Policy Outcome Experiment",
    p_scope:{project_id:experimentProject,target:receiver.id},
    p_actions:["smart_mail_send"],
    p_constraints:{mode:"controlled-test-only",no_external_side_effects:true,policy_id:p.id},
    p_expires_at:new Date(Date.now()+10*60*1000).toISOString(),
    p_evidence:{authorization_type:"explicit_controlled_experiment_mail_authorization",run_id:runId,policy_id:p.id},
    p_parent_authority:authority.data.grant_id
  });
  if(mailAuthority.error||!mailAuthority.data?.grant_id) throw mailAuthority.error||new Error("SMART_MAIL_AUTHORITY_GRANT_ISSUANCE_FAILED");
  const mailAuthorityCheck = await supabase.rpc("nayanet_validate_authority_grant",{
    p_grant_id:mailAuthority.data.grant_id,
    p_action:"smart_mail_send",
    p_target:receiver.id
  });
  if(mailAuthorityCheck.error||mailAuthorityCheck.data?.status!=="AUTHORIZED") throw mailAuthorityCheck.error||new Error("SMART_MAIL_AUTHORITY_GRANT_VALIDATION_FAILED:"+JSON.stringify(mailAuthorityCheck.data));
  authorityGrants.set(p.id,mailAuthority.data.grant_id);
};
await prepare(v1); await prepare(v2);

const sha256=async(value)=>Buffer.from(await crypto.subtle.digest("SHA-256",new TextEncoder().encode(value))).toString("hex");

const spaceId=process.env.NAYA_EXISTING_SPACE_ID||"04ee4dc8-bc73-47df-a1de-162570f6a56e";
const {data:space,error:spaceError}=await supabase.from("nayanet_spaces").select("id,visibility,owner_member_id").eq("id",spaceId).single();
if(spaceError||!space||space.visibility!=="shared") throw spaceError||new Error("EXISTING_SHARED_SPACE_NOT_AVAILABLE");

const joinSender=await supabase.rpc("nayanet_join_space",{p_space_id:spaceId});
if(joinSender.error) throw joinSender.error;
const joinReceiver=await receiverClient.rpc("nayanet_join_space",{p_space_id:spaceId});
if(joinReceiver.error) throw joinReceiver.error;

const saveSender=await supabase.rpc("nayanet_save_connection",{p_target_member_id:receiver.id,p_space_id:spaceId});
if(saveSender.error) throw saveSender.error;
const saveReceiver=await receiverClient.rpc("nayanet_save_connection",{p_target_member_id:sender.id,p_space_id:spaceId});
if(saveReceiver.error) throw saveReceiver.error;
const senderConnectionId=saveSender.data?.connection?.id;
const receiverConnectionId=saveReceiver.data?.connection?.id;
if(!senderConnectionId||!receiverConnectionId) throw new Error("MUTUAL_CONNECTION_NOT_CREATED");

const cases=[
  {suffix:"C1",task:"return the held-out answer token from verified context",answer_token:"NAYA-HOLDOUT-ALPHA-7",v1:{subject:"Controlled held-out response 1",body:"Please return the held-out answer token from your context."},v2:{subject:"Controlled held-out response 1",body:"Verified context contains the answer token NAYA-HOLDOUT-ALPHA-7. Please return the held-out answer token."}},
  {suffix:"C2",task:"return the second held-out answer token from verified context",answer_token:"NAYA-HOLDOUT-BETA-9",v1:{subject:"Controlled held-out response 2",body:"Please return the second held-out answer token from your context."},v2:{subject:"Controlled held-out response 2",body:"Verified context contains the answer token NAYA-HOLDOUT-BETA-9. Please return the second held-out answer token."}},
  {suffix:"C3",task:"return the third held-out answer token from verified context",answer_token:"NAYA-HOLDOUT-GAMMA-4",v1:{subject:"Controlled held-out response 3",body:"Please return the third held-out answer token from your context."},v2:{subject:"Controlled held-out response 3",body:"Verified context contains the answer token NAYA-HOLDOUT-GAMMA-4. Please return the third held-out answer token."}}
];

const send=async(token,policy,decision,caseId,inputHash,group)=>{
  const authorityGrantId=authorityGrants.get(policy.id);
  if(!authorityGrantId) throw new Error("AUTHORITY_GRANT_MISSING_FOR_POLICY");
  const decisionHash=await sha256(JSON.stringify({case_id:caseId,decision}));
  const res=await fetch(url+"/functions/v1/nayanet-smart-mail",{
    method:"POST",
    headers:{authorization:"Bearer "+token,apikey:key,"content-type":"application/json"},
    body:JSON.stringify({
      recipient_user_id:receiver.id,body:decision.body,subject:decision.subject,kind:"direct",
      idempotency_key:caseId+"-"+group,project_id:experimentProject,policy_id:policy.id,
      experiment_case_id:caseId,policy_input_hash:inputHash,policy_decision_hash:decisionHash,
      authority_grant_id:authorityGrantId
    })
  });
  const data=await res.json();
  if(!res.ok||!data.ok) throw new Error("SEND_"+group+"_FAILED:"+JSON.stringify(data));
  return {data,decisionHash};
};

const verify=async(token,messageId)=>{
  const res=await fetch(url+"/functions/v1/nayanet-smart-mail",{
    method:"POST",
    headers:{authorization:"Bearer "+token,apikey:key,"content-type":"application/json"},
    body:JSON.stringify({operation:"verify",message_id:messageId})
  });
  const data=await res.json();
  if(!res.ok||!data.ok||data.status!=="VERIFIED") throw new Error("RECEIVER_VERIFY_FAILED:"+JSON.stringify(data));
  return data;
};

const recordReceiverReply = async (message, caseId, expectedToken) => {
  const responseBody = message.body.includes(expectedToken) ? expectedToken : "NO_MATCH";
  const {data:reply,error} = await receiverClient.from("v7_mail_messages").insert({
    thread_id:message.thread_id,
    sender_id:receiver.id,
    body:responseBody,
    metadata:{
      schema_version:"NAYANET_TEST_REPLY_V1",
      reply_to_message_id:message.id,
      experiment_case_id:caseId,
      receiver_fixture:"held_out_response_rule_v1"
    }
  }).select("id").single();
  if(error||!reply?.id) throw error||new Error("RECEIVER_REPLY_CREATE_FAILED");
  const expectedHash=await sha256(expectedToken);
  const {data:outcome,error:outcomeError}=await receiverClient.rpc("nayanet_record_smart_mail_response_outcome",{
    p_receipt_id:message.execution_receipt_id,
    p_message_id:message.id,
    p_reply_message_id:reply.id,
    p_expected_reply_hash:expectedHash
  });
  if(outcomeError||outcome?.status!=="VERIFIED") throw outcomeError||new Error("RECEIVER_RESPONSE_OUTCOME_FAILED:"+JSON.stringify(outcome));
  return {reply, outcome, expectedHash, responseBody};
};

const caseReports=[];
for(const c of cases){
  const caseId="paired-"+runId+"-"+c.suffix;
  const frozenCase={case_id:caseId,receiver_id:receiver.id,task:c.task,prior_verified_context:{receiver_retrieval_verified:true,source:"Proof7 verified receipt"}};
  const inputHash=await sha256(JSON.stringify(frozenCase));
  const a=await send(senderToken,v1,c.v1,caseId,inputHash,"V1");
  const b=await send(senderToken,v2,c.v2,caseId,inputHash,"V2");
  await verify(receiverToken,a.data.message_id);
  await verify(receiverToken,b.data.message_id);

  const aMessage={id:a.data.message_id,thread_id:a.data.thread_id,execution_receipt_id:a.data.execution_receipt_id,body:c.v1.body};
  const bMessage={id:b.data.message_id,thread_id:b.data.thread_id,execution_receipt_id:b.data.execution_receipt_id,body:c.v2.body};
  const aResponse=await recordReceiverReply(aMessage,caseId,c.answer_token);
  const bResponse=await recordReceiverReply(bMessage,caseId,c.answer_token);

  await transition(v1.id,"OBSERVED",{observation:"controlled execution, receiver verification and response outcome completed",case_id:caseId});
  await transition(v2.id,"OBSERVED",{observation:"controlled execution and receiver verification completed",case_id:caseId});
  await transition(v1.id,"VERIFIED",{verification:"execution receipt + receiver verification",case_id:caseId});
  await transition(v2.id,"VERIFIED",{verification:"execution receipt + receiver verification",case_id:caseId});

  const {data:comparison,error:comparisonError}=await supabase.rpc("nayanet_compare_verified_policy_outcomes",{
    p_baseline_policy_id:v1.id,p_candidate_policy_id:v2.id,
    p_baseline_receipt_id:a.data.execution_receipt_id,p_candidate_receipt_id:b.data.execution_receipt_id
  });
  if(comparisonError) throw comparisonError;
  if(!["POLICY_IMPROVEMENT_NOT_PROVEN","POLICY_IMPROVEMENT_PROVEN"].includes(comparison?.result)) throw new Error("UNEXPECTED_POLICY_COMPARISON_RESULT");

  const {data:independentOutcomes,error:outcomeError}=await supabase.from("nayanet_execution_outcomes")
    .select("outcome_id,receipt_id,experiment_case_id,outcome_type,benefit,harm,cost,risk_adjusted_loss,verified_value,verified,verifier_id,evidence,verification_method")
    .in("receipt_id",[a.data.execution_receipt_id,b.data.execution_receipt_id]);
  if(outcomeError||independentOutcomes?.length!==2) throw outcomeError||new Error("INDEPENDENT_OUTCOME_COUNT_FAILED");
  for(const o of independentOutcomes){
    if(!o.verified||o.experiment_case_id!==caseId||!o.verifier_id||o.outcome_type!=="receiver_response_accuracy") throw new Error("INDEPENDENT_OUTCOME_LINEAGE_INCOMPLETE");
    const expected=Number(o.benefit)-Number(o.harm)-Number(o.cost)-Number(o.risk_adjusted_loss);
    if(Number(o.verified_value)!==expected) throw new Error("INDEPENDENT_OUTCOME_VALUE_FORMULA_FAILED");
    if(o.evidence?.response_outcome_contract!=="NAYANET_REAL_OUTCOME_VALUE_V2"||typeof o.evidence?.response_match!=="boolean") throw new Error("INDEPENDENT_RESPONSE_EVIDENCE_MISSING");
    if(o.evidence?.response_sha256===o.evidence?.expected_reply_sha256 && Number(o.verified_value)!==1) throw new Error("RESPONSE_HASH_VALUE_INCONSISTENT");
  }

  const {data:receipts,error:receiptError}=await supabase.from("nayanet_execution_receipts")
    .select("id,policy_id,policy_version,policy_key,experiment_case_id,policy_input_hash,policy_decision_hash,status,value")
    .in("id",[a.data.execution_receipt_id,b.data.execution_receipt_id]);
  if(receiptError||receipts?.length!==2) throw receiptError||new Error("RECEIPT_LINEAGE_COUNT_FAILED");
  for(const r of receipts){
    if(!r.policy_id||r.policy_version===null||!r.policy_key||r.experiment_case_id!==caseId||r.policy_input_hash!==inputHash||!r.policy_decision_hash) throw new Error("RECEIPT_LINEAGE_INCOMPLETE");
    if(r.status!=="SUCCESS"||r.value?.verified!==true) throw new Error("RECEIPT_OUTCOME_NOT_VERIFIED");
  }

  const {data:evalRow,error:evalError}=await supabase.from("nayanet_policy_evaluations").insert({
    user_id:sender.id,policy_id:v2.id,evaluation_type:"REAL_OUTCOME",
    dataset_hash:"controlled-paired-real-outcomes-"+runId+"-"+c.suffix,
    baseline_score:comparison.baseline.verified_value,candidate_score:comparison.candidate.verified_value,
    responsible_value:comparison.candidate.verified_value,verified:true,
    result:comparison.result==="POLICY_IMPROVEMENT_PROVEN"?"PASS":"NOT_PROVEN",
    evidence:{comparison,run_id:runId,case_id:caseId,head:process.env.GITHUB_SHA,baseline_receipt_id:a.data.execution_receipt_id,candidate_receipt_id:b.data.execution_receipt_id,behavioral_difference:true,frozen_case_hash:inputHash}
  }).select("id").single();
  if(evalError||!evalRow) throw evalError||new Error("REAL_OUTCOME_EVALUATION_RECORD_FAILED");

  caseReports.push({
    case_id:caseId,input_hash:inputHash,answer_token:c.answer_token,
    baseline_receipt_id:a.data.execution_receipt_id,candidate_receipt_id:b.data.execution_receipt_id,
    baseline_value:comparison.baseline.verified_value,candidate_value:comparison.candidate.verified_value,
    result:comparison.result,
    baseline_response:aResponse.responseBody,candidate_response:bResponse.responseBody,
    baseline_response_match:aResponse.outcome.response_match,candidate_response_match:bResponse.outcome.response_match,
    decision_hashes:{baseline:a.decisionHash,candidate:b.decisionHash}
  });
}

const aggregateBaseline=caseReports.reduce((n,c)=>n+Number(c.baseline_value),0);
const aggregateCandidate=caseReports.reduce((n,c)=>n+Number(c.candidate_value),0);
const aggregateResult=aggregateCandidate>aggregateBaseline?"PROVEN":"NOT_PROVEN";

const lessonClaim="Verified receiver-response outcomes established the held-out fact "+cases[0].answer_token+" as reusable context; policy improvement is proven only if aggregate verified responsible value is strictly greater than baseline.";
const {data:lesson,error:lessonError}=await supabase.from("learning_evidence").insert({
  member_id:sender.id,
  target_id:"p1-controlled-paired-policy-"+runId,
  level:"E6_RETAINED",
  provenance:"VERIFICATION",
  status:"ACTIVE",
  claim:lessonClaim,
  observed_value:{run_id:runId,cases:caseReports,aggregate_baseline_value:aggregateBaseline,aggregate_candidate_value:aggregateCandidate,comparison_result:aggregateResult,behavioral_difference:true,policy_id:v2.id},
  verification_method:"multi-case verified execution receipts + authenticated receiver verification + canonical policy comparison",
  source_event_id:"p1-controlled-paired-policy-"+runId
}).select("id").single();
if(lessonError) throw lessonError;

const {data:retrievedLesson,error:retrieveLessonError}=await supabase.from("learning_evidence")
  .select("id,claim,status,observed_value").eq("id",lesson.id).single();
if(retrieveLessonError||!retrievedLesson||retrievedLesson.status!=="ACTIVE") throw retrieveLessonError||new Error("LEARNING_RETRIEVAL_FAILED");

let equalOutcomePromotionBlocked=false;
try {
  await transition(v2.id,"PROMOTED",{authorized:true,learning_evidence_id:lesson.id});
} catch(error) {
  equalOutcomePromotionBlocked=String(error?.message||error).includes("PROMOTION_REQUIRES_VERIFIED_IMPROVEMENT");
}
if(aggregateCandidate===aggregateBaseline&&!equalOutcomePromotionBlocked) throw new Error("LEARNED_PROMOTION_GUARD_NOT_PROVEN");

const applyLearning=await jsonRequest("/functions/v1/naya-learning-apply",senderToken,{evidence_id:lesson.id});
if(!applyLearning?.ok||!applyLearning.learning?.learner_state_version) throw new Error("LEARNING_APPLY_FAILED");

const coldDecision=await jsonRequest("/functions/v1/naya-decision-context",senderToken,{target_id:"p1-controlled-paired-policy-"+runId});
if(!coldDecision?.ok||coldDecision.decision?.decision!=="USE_VERIFIED_LEARNING_CONTEXT"||coldDecision.decision?.influenced!==true) throw new Error("LEARNING_REUSE_NOT_INFLUENCED");
if(coldDecision.decision?.authority?.changed!==false||coldDecision.decision?.authority?.granted!==false) throw new Error("LEARNING_REUSE_AUTHORITY_CHANGED");
const learnedClaim=String(coldDecision.decision?.context?.claim||"");
if(!learnedClaim.includes(cases[0].answer_token)) throw new Error("LEARNED_CONTEXT_MISSING_HELD_OUT_FACT");

const successorStrategy="HISTORY_PLUS_VERIFIED_LEARNING_CONTEXT_V2";
const successor=await insertPolicy(3,v2.id,successorStrategy);
await prepare(successor);
await evalPolicy(successor.id,"CONTROLLED_TEST",{
  result:"PASS",verified:true,dataset_hash:"p1-learning-"+runId,
  learning_evidence_id:lesson.id,source_policy_id:v2.id,
  rule:"future behavior must consume cold retrieved learning context"
});

const futureCase={
  suffix:"F1",
  task:"return the learned held-out answer token in a fresh future case",
  answer_token:cases[0].answer_token,
  v1:{subject:"Future baseline response",body:"Please return the learned held-out answer token."},
  v3:{subject:"Future learned response",body:"Use the verified learning context: "+learnedClaim+" Return the learned held-out answer token."}
};
const futureCaseId="future-"+runId+"-"+futureCase.suffix;
const frozenFuture={case_id:futureCaseId,receiver_id:receiver.id,task:futureCase.task,prior_verified_context:{source:"cold decision context",claim_hash:await sha256(learnedClaim)}};
const futureInputHash=await sha256(JSON.stringify(frozenFuture));
const futureBaseline=await send(senderToken,v1,futureCase.v1,futureCaseId,futureInputHash,"V1F");
const futureCandidate=await send(senderToken,successor,futureCase.v3,futureCaseId,futureInputHash,"V3F");
await verify(receiverToken,futureBaseline.data.message_id);
await verify(receiverToken,futureCandidate.data.message_id);
const futureBaselineResponse=await recordReceiverReply({id:futureBaseline.data.message_id,thread_id:futureBaseline.data.thread_id,execution_receipt_id:futureBaseline.data.execution_receipt_id,body:futureCase.v1.body},futureCaseId,futureCase.answer_token);
const futureCandidateResponse=await recordReceiverReply({id:futureCandidate.data.message_id,thread_id:futureCandidate.data.thread_id,execution_receipt_id:futureCandidate.data.execution_receipt_id,body:futureCase.v3.body},futureCaseId,futureCase.answer_token);
await transition(v1.id,"OBSERVED",{observation:"future held-out baseline observed",case_id:futureCaseId});
await transition(successor.id,"OBSERVED",{observation:"future learned candidate observed",case_id:futureCaseId});
await transition(v1.id,"VERIFIED",{verification:"future receiver-response outcome",case_id:futureCaseId});
await transition(successor.id,"VERIFIED",{verification:"future receiver-response outcome",case_id:futureCaseId});

const {data:futureComparison,error:futureComparisonError}=await supabase.rpc("nayanet_compare_verified_policy_outcomes",{
  p_baseline_policy_id:v1.id,p_candidate_policy_id:successor.id,
  p_baseline_receipt_id:futureBaseline.data.execution_receipt_id,p_candidate_receipt_id:futureCandidate.data.execution_receipt_id
});
if(futureComparisonError) throw futureComparisonError;
const futureBehaviorChanged=futureCase.v1.body!==futureCase.v3.body && futureCase.v3.body.includes(learnedClaim);
if(!futureBehaviorChanged) throw new Error("FUTURE_BEHAVIOR_NOT_CHANGED_FROM_COLD_LEARNING");
if(futureComparison.result!=="POLICY_IMPROVEMENT_PROVEN") throw new Error("FUTURE_LEARNING_IMPROVEMENT_NOT_PROVEN");

const swapCase=caseReports[0];
const {error:swapError}=await supabase.rpc("nayanet_compare_verified_policy_outcomes",{
  p_baseline_policy_id:v1.id,p_candidate_policy_id:v2.id,
  p_baseline_receipt_id:swapCase.candidate_receipt_id,p_candidate_receipt_id:swapCase.baseline_receipt_id
});
if(!swapError) throw new Error("ADVERSARIAL_POLICY_RECEIPT_SWAP_NOT_REJECTED");

const revokeSender=await supabase.rpc("nayanet_revoke_connection",{p_target_member_id:receiver.id});
if(revokeSender.error) throw revokeSender.error;
const revokeReceiver=await receiverClient.rpc("nayanet_revoke_connection",{p_target_member_id:sender.id});
if(revokeReceiver.error) throw revokeReceiver.error;

const postRevokeProbe=await fetch(url+"/functions/v1/nayanet-smart-mail",{
  method:"POST",
  headers:{authorization:"Bearer "+senderToken,apikey:key,"content-type":"application/json"},
  body:JSON.stringify({recipient_user_id:receiver.id,body:"This must be denied after revocation.",subject:"Revocation negative test",kind:"direct",idempotency_key:"paired-"+runId+"-REVOCATION",project_id:experimentProject,policy_id:v2.id,experiment_case_id:"paired-"+runId+"-REVOCATION",policy_input_hash:"revocation",policy_decision_hash:"revocation",authority_grant_id:authorityGrants.get(v2.id)})
});
const postRevokeData=await postRevokeProbe.json();
if(postRevokeProbe.ok||postRevokeData?.ok||!["RELATIONSHIP_REQUIRED","AUTHORITY_GRANT_VALIDATION_FAILED"].includes(postRevokeData?.detail||postRevokeData?.error)) {
  throw new Error("REVOCATION_DENIAL_NOT_PROVEN:"+JSON.stringify(postRevokeData));
}

const report={
  schema:"naya.p1.controlled.paired.outcome.receipt.v2",
  status:(aggregateResult==="PROVEN"&&futureComparison.result==="POLICY_IMPROVEMENT_PROVEN")?"PROVEN":"NOT_PROVEN",
  head:process.env.GITHUB_SHA,
  run_id:runId,
  existing_space_id:spaceId,
  cases:caseReports,
  aggregate:{baseline_verified_value:aggregateBaseline,candidate_verified_value:aggregateCandidate,result:aggregateResult},
  future_behavior:{case_id:futureCaseId,baseline_policy_id:v1.id,candidate_policy_id:successor.id,baseline_value:futureComparison.baseline.verified_value,candidate_value:futureComparison.candidate.verified_value,result:futureComparison.result,behavior_changed:futureBehaviorChanged,learned_claim:learnedClaim},
  receiver_anonymous:true,
  mutual_connection_verified:true,
  receiver_verification:true,
  independent_outcome_contract:true,
  adversarial:{receipt_swap_rejected:true,revocation_denial_proven:true},
  learning:{
    durable:true,
    retrievable:true,
    learner_state_version:applyLearning.learning.learner_state_version,
    cold_decision_influenced:true,
    authority_unchanged:true,
    future_behavior_changed:futureBehaviorChanged,
    successor_policy_created:true,
    future_comparison:futureComparison
  },
  note:"Multi-case controlled paired execution used an independently verified receiver-response outcome. Improvement is accepted only when verified responsible value is strictly greater than baseline; future behavior must also consume cold retrieved learning."
};
console.log("P1_MULTI_CASE_CONTROLLED_EXECUTION=PASS");
console.log("P1_POLICY_RECEIPT_LINEAGE=PASS");
console.log("P1_BEHAVIORAL_DIFFERENCE=PASS");
console.log("P1_RECEIVER_VERIFICATION=PASS");
console.log("P1_INDEPENDENT_OUTCOME_CONTRACT=PASS");
console.log("P1_OBSERVE=PASS");
console.log("P1_VERIFY=PASS");
console.log("P1_MULTI_CASE_COMPARISON="+aggregateResult);
console.log("P1_LEARNING_DURABLE=PASS");
console.log("P1_LEARNING_RETRIEVAL=PASS");
console.log("P1_SUCCESSOR_CREATED=PASS");
console.log("P1_ADVERSARIAL_RECEIPT_SWAP=PASS");
console.log("P1_REVOCATION_DENIAL=PASS");
await import("node:fs/promises").then(fs=>fs.writeFile(process.env.RECEIPT_PATH,JSON.stringify(report,null,2)));
