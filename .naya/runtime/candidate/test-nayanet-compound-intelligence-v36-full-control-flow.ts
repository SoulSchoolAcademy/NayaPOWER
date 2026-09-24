import { readFileSync } from "node:fs";
import * as vm from "node:vm";
import { generateKeyPairSync, sign } from "node:crypto";

const path=".naya/runtime/candidate/nayanet-compound-intelligence-v36-production-shaped.ts";
const source=readFileSync(path,"utf8");
const helperStart=source.indexOf("/* ===== V36 NON-PRODUCTION PORTABLE INTELLIGENCE BOUNDARY ===== */");
const commitStart=source.indexOf("async function commitIntelligence(client: any, userId: string, body: any) {");
const healthStart=source.indexOf("async function health(",commitStart);
if(helperStart<0||commitStart<0||healthStart<0||helperStart>commitStart)throw new Error("EXTRACTION_SEAM_NOT_FOUND");
const extracted=source.slice(helperStart,healthStart)+
"\nmodule.exports={verifyV36PortableArtifact,commitIntelligence};\n";
const js=extracted.replace(/:\s*(unknown|string|any|Promise<[^>]+>)/g,"");

const {publicKey,privateKey}=generateKeyPairSync("ed25519");
const pubDer=publicKey.export({format:"der",type:"spki"});
const pubHex=pubDer.subarray(pubDer.length-32).toString("hex");

const actor="fixture-actor", authorityId="fixture-authority", commitSha="fixture-source-sha";
const grant={authority_id:authorityId,principal_id:actor,purpose:"fixture",scope:"NayaNET",granted_actions:["intelligence_commit"],expires_at:"2030-01-01T00:00:00.000Z",revoked:false};
const canonical=(v)=>Array.isArray(v)?"["+v.map(canonical).join(",")+"]":v!==null&&typeof v==="object"?"{"+Object.entries(v).sort(([a],[b])=>a.localeCompare(b)).map(([k,x])=>JSON.stringify(k)+":"+canonical(x)).join(",")+"}":JSON.stringify(v);
const hash=async s=>Buffer.from(await crypto.subtle.digest("SHA-256",Buffer.from(s))).toString("hex");
const binding=async a=>hash([a.authority_id,a.decision_id,a.action_id,a.action_type,a.target,a.actor_id,a.scope,a.permission].join("|"));
const grantFp=async g=>hash(canonical({authority_id:g.authority_id,principal_id:g.principal_id,purpose:g.purpose,scope:g.scope,granted_actions:[...g.granted_actions].sort(),expires_at:g.expires_at,revoked:g.revoked}));
const registryRev=async g=>hash(canonical([[g.authority_id,g.principal_id,g.purpose,g.scope,[...g.granted_actions].sort(),g.expires_at,g.revoked]]));

const ordinary={authority_id:authorityId,decision_id:"fixture-decision",action_id:"fixture-action",action_type:"INTELLIGENCE_COMMIT",target:"NayaNET",actor_id:actor,scope:"NayaNET",permission:"intelligence_commit",governance_state:"AUTHORIZED",binding_hash:""};
ordinary.binding_hash=await binding(ordinary);
const authorization={...ordinary,repository:"SoulSchoolAcademy/NayaPOWER",commit_sha:commitSha,issued_at:new Date(Date.now()-1000).toISOString(),expires_at:new Date(Date.now()+60000).toISOString(),authority_fingerprint:await grantFp(grant),registry_revision:await registryRev(grant)};
const signature=sign(null,Buffer.from(canonical(authorization)),privateKey).toString("hex");
const artifact={schema:"naya/portable_authorization/v1",authorization,signature};
const artifactHash=await hash(canonical(artifact));

let recordCalls=0;
const sourceEvent={id:"fixture-source-row",event_id:"intelligence:fixture",title:"Fixture",content:"fixture",metadata:{idempotency_key:"fixture"},created_at:new Date().toISOString()};
const chain=(table)=>{let singleMode=null;const api={select(){return api},eq(){return api},in(){return api},order(){return api},limit(){return api},or(){return api},maybeSingle(){singleMode="maybe";return api},single(){singleMode="single";return api},insert(){return api},update(){return api},then(resolve,reject){let data=null;if(table==="nayanet_cognition_events"&&singleMode==="single")data=sourceEvent;if(table==="learning_evidence"&&singleMode==="single")data={id:"learning-1",status:"CANDIDATE",target_id:"target"};if(table==="nayanet_intelligent_blocks"&&singleMode==="single")data={id:"block-1"};resolve({data,error:null});}};return api};
const client={from(table){return chain(table)}};
const admin={rpc:async(name,args)=>({data:grant,error:null}),from(table){return chain(table)}};

const context={console,crypto,structuredClone,TextEncoder,Date,Buffer,require,module:{exports:{}},exports:{},Deno:{env:{get(k){return k==="NAYANET_PORTABLE_ISSUER_PUBLIC_KEY_HEX"?pubHex:undefined}}},admin,record:async()=>{recordCalls++;return{id:"fixture-receipt"}},projectIntelligence:async()=>({index:{id:"index-1"}}),checkpointIntelligence:async()=>({status:"CHECKPOINT_VERIFIED",checkpoint:{metadata:{checkpoint_id:"checkpoint:fixture"}},receipt:{id:"checkpoint-receipt"}})};
vm.runInNewContext(js,context,{filename:path});
const fn=context.module.exports.commitIntelligence;
if(typeof fn!=="function")throw new Error("COMMIT_FUNCTION_NOT_EXTRACTED");

const base={execution_authorization:ordinary,portable_authorization:artifact,portable_authorization_artifact_hash:artifactHash,idempotency_key:"fixture",content:"fixture intelligence",source_head:commitSha};

const attacks=[
 ["missing artifact",{...base,portable_authorization:undefined}],
 ["missing hash",{...base,portable_authorization_artifact_hash:""}],
 ["tampered hash",{...base,portable_authorization_artifact_hash:"0".repeat(64)}],
 ["tampered signature",{...base,portable_authorization:{...artifact,signature:"00".repeat(64)}}],
 ["wrong actor",{...base,portable_authorization:{...artifact,authorization:{...authorization,actor_id:"wrong"}}}],
 ["wrong permission",{...base,portable_authorization:{...artifact,authorization:{...authorization,permission:"repo_write"}}}],
 ["ordinary mismatch",{...base,execution_authorization:{...ordinary,actor_id:"other"}}],
 ["wrong source",{...base,source_head:"other-sha"}],
 ["expired",{...base,portable_authorization:{...artifact,authorization:{...authorization,expires_at:new Date(Date.now()-1000).toISOString()}}}],
];
for(const [name,req] of attacks){const before=recordCalls;let ok=false;try{await fn(client,actor,req)}catch{ok=true}if(!ok||recordCalls!==before)throw new Error(name+": record path reached or attack accepted")}

const valid=await fn(client,actor,base);
if(recordCalls!==1)throw new Error("legitimate path did not reach record exactly once");
if(!valid||valid.schema!=="NAYANET_INTELLIGENCE_COMMIT_V1")throw new Error("legitimate commit failed");

console.log("V36_FULL_FUNCTION_CONTROL_FLOW=PASS");
console.log("9 local attack fixtures: FAIL-CLOSED + record_calls=0");
console.log("legitimate fixture: PASS + record_calls=1");
console.log("existing v35 commitIntelligence body exercised through injected local seams");
console.log("portable verification occurs before capture record seam");
console.log("production deployment: NOT RUN");
console.log("production mutation: NOT RUN");
console.log("live intelligence_commit: NOT RUN");
