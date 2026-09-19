import crypto from "node:crypto";
import fs from "node:fs";

const BASE = process.env.SUPABASE_URL;
const PUBLISHABLE = process.env.SUPABASE_PUBLISHABLE_KEY;
const SERVICE_ROLE = process.env.SUPABASE_SERVICE_ROLE_KEY;
const PROOF_PATH = process.env.PROOF_PATH;
if (!BASE || !PUBLISHABLE || !SERVICE_ROLE || !PROOF_PATH) throw new Error("RUNTIME_NOT_CONFIGURED");

const runId = crypto.randomUUID();
const now = new Date();
const later = new Date(now.getTime() + 60_000);
const json = x => JSON.stringify(x);
const sleep = ms => new Promise(r => setTimeout(r, ms));

async function request(path, {token, service=false, method="GET", body, headers={}}={}) {
  const h = { apikey: service ? SERVICE_ROLE : PUBLISHABLE, authorization: "Bearer " + (service ? SERVICE_ROLE : token), ...headers };
  if (body !== undefined) h["content-type"] = "application/json";
  const r = await fetch(BASE + path, {method, headers:h, body:body===undefined?undefined:json(body)});
  const text = await r.text();
  let data; try { data = text ? JSON.parse(text) : null; } catch { data = {raw:text}; }
  return {status:r.status, ok:r.ok, data};
}
const fail = m => { throw new Error(m); };
const ok = (x,m) => { if(!x) fail(m); };

async function adminCreate(label) {
  const email = `naya-owner-isolation-${label}-${runId}@example.invalid`;
  const password = crypto.randomBytes(36).toString("base64url");
  const r = await request("/auth/v1/admin/users", {service:true, method:"POST", body:{
    email, password, email_confirm:true, user_metadata:{naya_test:true, run_id:runId, role:label}
  }});
  ok(r.ok && r.data?.user?.id, `AUTH_${label}_CREATE_FAILED:${r.status}`);
  return {label,email,password,user_id:r.data.user.id};
}
async function signIn(u) {
  const r = await request("/auth/v1/token?grant_type=password", {method:"POST", body:{email:u.email,password:u.password}});
  ok(r.ok && r.data?.access_token && r.data?.user?.id, `AUTH_${u.label}_SIGNIN_FAILED:${r.status}`);
  ok(r.data.user.id===u.user_id, `AUTH_${u.label}_IDENTITY_MISMATCH`);
  return {...u, access_token:r.data.access_token};
}
async function create(token, table, body) {
  const r = await request("/rest/v1/"+table+"?select=*", {token, method:"POST", headers:{Prefer:"return=representation"}, body});
  ok(r.ok && Array.isArray(r.data) && r.data.length===1, `${table}_CREATE_FAILED:${r.status}_${json(r.data)}`);
  return r.data[0];
}
async function select(token, table, query) {
  const r = await request("/rest/v1/"+table+"?select=*"+query, {token});
  ok(r.ok && Array.isArray(r.data), `${table}_SELECT_FAILED:${r.status}_${json(r.data)}`);
  return r.data;
}
async function mutate(token, table, query, body) {
  return request("/rest/v1/"+table+"?"+query, {token, method:"PATCH", headers:{Prefer:"return=representation"}, body});
}
async function assertDeniedRead(token, table, idField, id, label) {
  const rows = await select(token, table, `&${idField}=eq.${encodeURIComponent(id)}`);
  ok(rows.length===0, `CROSS_OWNER_READ_VISIBLE:${label}`);
  return {label,status:"DENIED",observed_rows:0};
}
async function assertDeniedMutation(token, table, idField, id, body, label) {
  const r = await mutate(token, table, `${idField}=eq.${encodeURIComponent(id)}`, body);
  const denied = !r.ok || !Array.isArray(r.data) || r.data.length===0;
  ok(denied, `CROSS_OWNER_MUTATION_SUCCEEDED:${label}`);
  return {label,status:"DENIED",http_status:r.status};
}
async function waitForProjection(token, table, query, label) {
  for(let i=0;i<8;i++) {
    const rows=await select(token,table,query);
    if(rows.length) return rows;
    await sleep(750);
  }
  fail(`PROJECTION_NOT_OBSERVED:${label}`);
}

const A = await signIn(await adminCreate("A"));
const B = await signIn(await adminCreate("B"));

const smartA = await create(A.access_token,"smart_note_events",{
  member_id:A.user_id,subject:"OWNER_ISOLATION_A_"+runId,event_type:"SMART_NOTE",
  source_context:{run_id:runId,owner:"A"},privacy_state:"PRIVATE",status:"INCOMPLETE"
});
for (const [type,content] of [
  ["HUMAN_NOTE","A human artifact "+runId],
  ["NAYA_NOTE","A Naya artifact "+runId],
  ["MACHINE_NOTE","A machine artifact "+runId],
  ["INTELLIGENCE_FEED_NOTE","A feed artifact "+runId]
]) await create(A.access_token,"smart_note_artifacts",{event_id:smartA.id,artifact_type:type,content});
const receiptA=await create(A.access_token,"smart_note_receipts",{
  event_id:smartA.id,status:"VERIFIED",verification:{run_id:runId,owner:"A",verified:true}
});
const smartVerify=await mutate(A.access_token,"smart_note_events",`id=eq.${smartA.id}`,{status:"VERIFIED",verified_at:new Date().toISOString()});
ok(smartVerify.ok && smartVerify.data?.length===1,"SMART_NOTE_VERIFY_FAILED");

const smartB = await create(B.access_token,"smart_note_events",{
  member_id:B.user_id,subject:"OWNER_ISOLATION_B_"+runId,event_type:"SMART_NOTE",
  source_context:{run_id:runId,owner:"B"},privacy_state:"PRIVATE",status:"INCOMPLETE"
});

const cognitionA=await create(A.access_token,"nayanet_cognition_events",{
  user_id:A.user_id,project_id:"OWNER_ISOLATION",event_id:"owner-isolation:"+runId+":A",
  type:"intelligence",classification:"observation",title:"Owner Isolation A",
  content:"Authenticated owner-isolation cognition A "+runId,source:"owner-isolation-e2e",
  status:"active",actor:"human",confidence:1,tags:["owner-isolation","A"],
  source_hash:crypto.createHash("sha256").update(runId+":A").digest("hex"),
  schema_version:"1.0.0",receipt_id:"owner-isolation:"+runId+":A"
});
const cognitionB=await create(B.access_token,"nayanet_cognition_events",{
  user_id:B.user_id,project_id:"OWNER_ISOLATION",event_id:"owner-isolation:"+runId+":B",
  type:"intelligence",classification:"observation",title:"Owner Isolation B",
  content:"Authenticated owner-isolation cognition B "+runId,source:"owner-isolation-e2e",
  status:"active",actor:"human",confidence:1,tags:["owner-isolation","B"],
  source_hash:crypto.createHash("sha256").update(runId+":B").digest("hex"),
  schema_version:"1.0.0",receipt_id:"owner-isolation:"+runId+":B"
});

const learningA=await create(A.access_token,"learning_evidence",{
  member_id:A.user_id,target_id:"owner-isolation:"+runId+":A",level:"E1_UNDERSTANDS",provenance:"TEST",
  status:"ACTIVE",claim:"A owns this learning evidence "+runId,
  observed_value:{run_id:runId,owner:"A"},verification_method:"authenticated owner-isolation E2E"
});
const learningB=await create(B.access_token,"learning_evidence",{
  member_id:B.user_id,target_id:"owner-isolation:"+runId+":B",level:"E1_UNDERSTANDS",provenance:"TEST",
  status:"ACTIVE",claim:"B owns this learning evidence "+runId,
  observed_value:{run_id:runId,owner:"B"},verification_method:"authenticated owner-isolation E2E"
});

const stateA=await create(A.access_token,"learner_states",{
  member_id:A.user_id,goals:["owner-isolation-A"],active_target_ids:[learningA.id],demonstrated_capability_ids:[],
  current_evidence_by_target:{[learningA.id]:"ACTIVE"},unresolved_gap_ids:[],misconception_ids:[],
  successful_teaching_approach_ids:[],version:1
});
const stateB=await create(B.access_token,"learner_states",{
  member_id:B.user_id,goals:["owner-isolation-B"],active_target_ids:[learningB.id],demonstrated_capability_ids:[],
  current_evidence_by_target:{[learningB.id]:"ACTIVE"},unresolved_gap_ids:[],misconception_ids:[],
  successful_teaching_approach_ids:[],version:1
});

const reportA=await create(A.access_token,"v7_intelligence_reports",{
  user_id:A.user_id,period_type:"owner-isolation",period_start:now.toISOString(),
  period_end:later.toISOString(),report:{run_id:runId,owner:"A",claim:"private report A"},status:"COMPLETED"
});
const reportB=await create(B.access_token,"v7_intelligence_reports",{
  user_id:B.user_id,period_type:"owner-isolation",period_start:now.toISOString(),
  period_end:later.toISOString(),report:{run_id:runId,owner:"B",claim:"private report B"},status:"COMPLETED"
});

const spaceA=await create(A.access_token,"nayanet_spaces",{
  owner_member_id:A.user_id,name:"Owner Isolation A "+runId,purpose:"private E2E proof",visibility:"private"
});
const spaceB=await create(B.access_token,"nayanet_spaces",{
  owner_member_id:B.user_id,name:"Owner Isolation B "+runId,purpose:"private E2E proof",visibility:"private"
});

const indexA=await waitForProjection(A.access_token,"nayanet_intelligence_index",
  `&owner_id=eq.${A.user_id}&source_id=in.(${smartA.id},${cognitionA.id},${learningA.id},${reportA.id},${spaceA.id})`,"A index");
const ledgerA=await waitForProjection(A.access_token,"nayanet_smart_ledger",
  `&owner_id=eq.${A.user_id}&source_id=in.(${smartA.id},${cognitionA.id},${learningA.id},${reportA.id},${spaceA.id})`,"A ledger");
const indexB=await waitForProjection(B.access_token,"nayanet_intelligence_index",
  `&owner_id=eq.${B.user_id}&source_id=in.(${smartB.id},${cognitionB.id},${learningB.id},${reportB.id},${spaceB.id})`,"B index");
const ledgerB=await waitForProjection(B.access_token,"nayanet_smart_ledger",
  `&owner_id=eq.${B.user_id}&source_id=in.(${smartB.id},${cognitionB.id},${learningB.id},${reportB.id},${spaceB.id})`,"B ledger");

const deniedReads=[];
const deniedMutations=[];
for (const [table,idField,id,label] of [
  ["smart_note_events","id",smartA.id,"Smart Notes"],
  ["nayanet_cognition_events","id",cognitionA.id,"Cognition"],
  ["learning_evidence","id",learningA.id,"Learning"],
  ["v7_intelligence_reports","id",reportA.id,"Reports"],
  ["nayanet_spaces","id",spaceA.id,"Spaces"]
]) {
  deniedReads.push(await assertDeniedRead(B.access_token,table,idField,id,label));
}
for (const [table,idField,id,body,label] of [
  ["smart_note_events","id",smartA.id,{subject:"CROSS_OWNER_MUTATION"},"Smart Notes"],
  ["nayanet_cognition_events","id",cognitionA.id,{title:"CROSS_OWNER_MUTATION"},"Cognition"],
  ["learning_evidence","id",learningA.id,{claim:"CROSS_OWNER_MUTATION"},"Learning"],
  ["v7_intelligence_reports","id",reportA.id,{report:{tampered:true}},"Reports"],
  ["nayanet_spaces","id",spaceA.id,{name:"CROSS_OWNER_MUTATION"},"Spaces"]
]) {
  deniedMutations.push(await assertDeniedMutation(B.access_token,table,idField,id,body,label));
}
for (const [table,label] of [["nayanet_intelligence_index","Index"],["nayanet_smart_ledger","Smart Ledger"]]) {
  const r=await request("/rest/v1/"+table,{token:B.access_token,method:"POST",headers:{Prefer:"return=representation"},body:{}});
  ok(!r.ok && (r.status===401 || r.status===403 || r.status===405 || r.status===406 || r.status===422),`PROJECTION_WRITE_NOT_REJECTED:${label}:${r.status}`);
}

const projectionIsolation = {
  A_index_rows:indexA.length,A_ledger_rows:ledgerA.length,
  B_index_rows:indexB.length,B_ledger_rows:ledgerB.length,
  A_sources:[smartA.id,cognitionA.id,learningA.id,reportA.id,spaceA.id],
  B_sources:[smartB.id,cognitionB.id,learningB.id,reportB.id,spaceB.id]
};

const proof={
  schema:"naya.nayanet.owner-isolation.proof.v1",status:"VERIFIED",run_id:runId,
  identities:{A:{user_id:A.user_id,email:A.email},B:{user_id:B.user_id,email:B.email}},
  surfaces:{
    "Smart Notes":{A:{event_id:smartA.id,receipt_id:receiptA.id},B:{event_id:smartB.id}},
    Cognition:{A:{event_id:cognitionA.id},B:{event_id:cognitionB.id}},
    "Smart Ledger":{A_rows:ledgerA.map(x=>x.ledger_event_id),B_rows:ledgerB.map(x=>x.ledger_event_id),write_boundary:"projection_read_only"},
    Index:{A_rows:indexA.map(x=>x.id),B_rows:indexB.map(x=>x.id),write_boundary:"projection_read_only"},
    Learning:{A:{evidence_id:learningA.id,learner_state_member_id:stateA.member_id},B:{evidence_id:learningB.id,learner_state_member_id:stateB.member_id}},
    Reports:{A:{report_id:reportA.id},B:{report_id:reportB.id}},
    Spaces:{A:{space_id:spaceA.id},B:{space_id:spaceB.id}}
  },
  cross_owner:{reads:deniedReads,mutations:deniedMutations},
  projection_isolation:projectionIsolation,
  authenticated_runtime:true,
  credentials_exposed_in_source:false,
  observed_at:new Date().toISOString()
};
fs.writeFileSync(PROOF_PATH,JSON.stringify(proof,null,2));
console.log(JSON.stringify({PROOF:"VERIFIED",run_id:runId,A_user_id:A.user_id,B_user_id:B.user_id,smart_note_A:smartA.id,smart_note_B:smartB.id,cognition_A:cognitionA.id,cognition_B:cognitionB.id,learning_A:learningA.id,learning_B:learningB.id,report_A:reportA.id,report_B:reportB.id,space_A:spaceA.id,space_B:spaceB.id,index_A:indexA.length,index_B:indexB.length,ledger_A:ledgerA.length,ledger_B:ledgerB.length},null,2));

// The identities are deliberately left alive for the authenticated proof artifact; the generated passwords and access tokens never leave process memory.
