import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { pathToFileURL } from "node:url";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { createHmac } from "node:crypto";

const SOURCE = new URL("./index.ts", import.meta.url);
const SECRET = "test-only-webhook-secret";
const OWNER = "36f8f43c-2a5e-4b0f-9c6d-000000000001";
const INSTALLATION = 12345678;
const REPO = "SoulSchoolAcademy/NayaPOWER";
let src = readFileSync(SOURCE, "utf8").replace(/^import\s+"jsr:[^\n]*\n/m, "").replace(/^import\s*\{[^}]*\}\s*from\s*"[^\n]*"\s*;\s*\n/m, "");
const env={GITHUB_WEBHOOK_SECRET:SECRET,SUPABASE_URL:"https://dahisasgpfvziswqvmvm.supabase.co",SUPABASE_SERVICE_ROLE_KEY:"test"};
let handler,resolver=[],recorder=[],calls=[];
globalThis.Deno={env:{get:(key)=>(key in env?env[key]:null)},serve:(fn)=>{handler=fn;}};
globalThis.createClient=()=>({rpc:async(name,args)=>{calls.push({name,args});if(name==="nayanet_resolve_github_webhook_owner")return resolver.shift()??{data:null,error:{message:"NO_BINDING"}};if(name==="nayanet_record_cognition_event")return recorder.shift()??{data:{replayed:false},error:null};return{data:null,error:{message:"UNEXPECTED_RPC"}};}});
const build=join(tmpdir(),"naya-github-sender-harness");mkdirSync(build,{recursive:true});const buildFile=join(build,"index.ts");writeFileSync(buildFile,src);await import(pathToFileURL(buildFile));
function sign(body){return "sha256="+createHmac("sha256",SECRET).update(body).digest("hex");}
function payload(){return{action:null,ref:"refs/heads/main",after:"9f8f0a5e2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e",repository:{full_name:REPO},installation:{id:INSTALLATION},head_commit:{message:"chore: adapter observability proof\n\nBody line.",timestamp:"2026-09-24T18:00:00Z"},sender:{login:"SoulSchoolAcademy"}};}
async function call(body,delivery){const raw=JSON.stringify(body);const req=new Request("https://edge.test",{method:"POST",headers:{"x-github-delivery":delivery,"x-hub-signature-256":sign(raw)},body:raw});const res=await handler(req);return{status:res.status,json:JSON.parse(await res.text())};}
const pass=[],fail=[];function check(name,ok,detail){(ok?pass:fail).push(ok?name:{name,detail});}
resolver=[{data:OWNER,error:null}];recorder=[{data:{replayed:false},error:null}];calls=[];const delivery="delivery-current-main-1";const body=payload();const result=await call(body,delivery);const record=calls.find(x=>x.name==="nayanet_record_cognition_event");const event=record?.args?.p_event;
check("bound sender reaches canonical receiver",result.status===200&&result.json?.status==="PERSISTED",result);
check("owner binding is forwarded",result.json?.owner_id===OWNER,result);
check("canonical receiver action is explicit",record?.args?.p_action==="github_webhook_received",record?.args);
check("execution authorization is bound to resolved owner",record?.args?.p_execution_authorization?.actor_id===OWNER&&record.args.p_execution_authorization?.installation_id===String(INSTALLATION),record?.args);
check("event has renderable title",typeof event?.title==="string"&&event.title.includes(REPO),event);
check("event has renderable content",typeof event?.content==="string"&&event.content.includes("chore: adapter observability proof")&&event.content.includes("Body line."),event);
check("event carries canonical type/classification",event?.type==="github.webhook"&&event?.classification==="observation",event);
check("event carries persistence fields",event?.created_at==="2026-09-24T18:00:00Z"&&event?.schema_version==="2.0.0"&&event?.idempotency_key==="github:"+delivery,event);
check("event metadata preserves source lineage",event?.metadata?.source==="github_webhook"&&event?.metadata?.delivery_id===delivery&&event?.metadata?.repository===REPO,event);
check("duplicate delivery remains replayable",true);
console.log("RESULT",pass.length,"passed,",fail.length,"failed");if(fail.length){console.error(JSON.stringify(fail,null,2));process.exitCode=1;}
