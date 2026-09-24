import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const cors={"Access-Control-Allow-Origin":"*","Access-Control-Allow-Headers":"content-type,x-github-delivery,x-hub-signature-256","Access-Control-Allow-Methods":"POST,OPTIONS"};

function json(body:unknown,status=200){return new Response(JSON.stringify(body),{status,headers:{...cors,"Content-Type":"application/json"}})}

function hex(bytes:ArrayBuffer){return [...new Uint8Array(bytes)].map(b=>b.toString(16).padStart(2,"0")).join("")}

async function verifySignature(secret:string,body:string,signature:string){
  if(!/^sha256=[0-9a-f]{64}$/i.test(signature)) return false;
  const key=await crypto.subtle.importKey("raw",new TextEncoder().encode(secret),{name:"HMAC",hash:"SHA-256"},false,["sign"]);
  const expected="sha256="+hex(await crypto.subtle.sign("HMAC",key,new TextEncoder().encode(body)));
  const a=new TextEncoder().encode(expected),b=new TextEncoder().encode(signature.toLowerCase());
  if(a.length!==b.length)return false;
  let diff=0;for(let i=0;i<a.length;i++)diff|=a[i]^b[i];return diff===0;
}

function normalize(payload:any,delivery:string){
  const repo=payload?.repository?.full_name||"";
  const sha=payload?.after||payload?.pull_request?.head?.sha||payload?.workflow_run?.head_sha||null;
  const eventType=String(payload?.action?payload?.action:"github.webhook");
  return {
    event_id:"github:"+delivery,
    source_event_id:delivery,
    source_system:"github",
    event_type:eventType,
    repository:repo,
    ref:payload?.ref||payload?.pull_request?.base?.ref||payload?.workflow_run?.head_branch||null,
    commit_sha:sha,
    actor:payload?.sender?.login||payload?.pusher?.name||null,
    occurred_at:payload?.head_commit?.timestamp||payload?.workflow_run?.created_at||new Date().toISOString(),
    received_at:new Date().toISOString(),
    correlation_id:"github:"+delivery,
    idempotency_key:"github:"+delivery,
    authority:{source:"github_app",scope:repo},
    provenance:{delivery_id:delivery,provider:"github"},
    verification:{state:"SIGNED_WEBHOOK_VERIFIED"},
    processing_state:"RECEIVED",
    projection_targets:["Personal Intelligence","Activity","Intelligence Today"],
    payload
  };
}

Deno.serve(async(req)=>{
  if(req.method==="OPTIONS")return new Response("ok",{headers:cors});
  if(req.method!=="POST")return json({ok:false,error:"METHOD_NOT_ALLOWED"},405);
  const delivery=req.headers.get("x-github-delivery")||"";
  const signature=req.headers.get("x-hub-signature-256")||"";
  const secret=Deno.env.get("GITHUB_WEBHOOK_SECRET")||"";
  if(!secret)return json({ok:false,error:"GITHUB_WEBHOOK_SECRET_NOT_CONFIGURED",status:"BLOCKED_EXTERNAL_CREDENTIAL"},503);
  if(!delivery)return json({ok:false,error:"GITHUB_DELIVERY_ID_REQUIRED"},400);
  const body=await req.text();
  if(!(await verifySignature(secret,body,signature)))return json({ok:false,error:"INVALID_GITHUB_SIGNATURE"},401);
  let payload:any;try{payload=JSON.parse(body)}catch{return json({ok:false,error:"INVALID_JSON"},400)}
  const event=normalize(payload,delivery);
  const installationId=payload?.installation?.id;
  const repository=payload?.repository?.full_name;
  if(!Number.isSafeInteger(installationId)||installationId<=0||typeof repository!=="string"||!repository){
    return json({ok:false,error:"GITHUB_OWNER_BINDING_REQUIRED",status:"BLOCKED_OWNER_BINDING"},403);
  }

  const url=Deno.env.get("SUPABASE_URL"),serviceKey=Deno.env.get("SUPABASE_SERVICE_ROLE_KEY");
  if(!url||!serviceKey)return json({ok:false,error:"SUPABASE_SERVICE_ROLE_NOT_CONFIGURED",status:"BLOCKED_EXTERNAL_CREDENTIAL"},503);
  const sb=createClient(url,serviceKey,{auth:{persistSession:false,autoRefreshToken:false}});

  const {data:owner,error:ownerError}=await sb.rpc("nayanet_resolve_github_webhook_owner",{
    p_installation_id:installationId,
    p_repository:repository
  });
  if(ownerError||!owner){
    return json({ok:false,error:"GITHUB_OWNER_BINDING_NOT_RESOLVED",status:"BLOCKED_OWNER_BINDING",detail:ownerError?.message||"NO_ACTIVE_UNAMBIGUOUS_BINDING"},403);
  }

  const executionAuthorization={
    source:"github_app_webhook",
    actor_id:owner,
    installation_id:String(installationId),
    repository,
    verification:"SIGNED_GITHUB_WEBHOOK"
  };

  const {data,error}=await sb.rpc("nayanet_record_cognition_event",{
    p_project_id:"NayaNET",
    p_event:event,
    p_action:"github_webhook_received",
    p_expected_result:"Signed GitHub event normalized and persisted exactly once for its bound owner.",
    p_observed_result:"Signed GitHub event accepted by the NayaNET bridge after owner-binding resolution.",
    p_learning:[{status:"captured",at:event.received_at,source_event_id:delivery}],
    p_execution_authorization:executionAuthorization
  });
  if(error)return json({ok:false,error:"CANONICAL_EVENT_PERSISTENCE_FAILED",detail:error.message,status:"PERSISTENCE_FAILED",event_id:event.event_id},502);
  return json({ok:true,status:data?.replayed?"REPLAYED":"PERSISTED",event_id:event.event_id,delivery_id:delivery,repository:event.repository,commit_sha:event.commit_sha,owner_id:owner,transaction:data});
});
