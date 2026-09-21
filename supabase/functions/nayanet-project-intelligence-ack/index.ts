import { createClient } from "npm:@supabase/supabase-js@2";
const URL=Deno.env.get("SUPABASE_URL")!,ANON=Deno.env.get("SUPABASE_ANON_KEY")!,SECRET=Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const admin=createClient(URL,SECRET);
const cors={"Access-Control-Allow-Origin":"*","Access-Control-Allow-Headers":"authorization,apikey,content-type,x-idempotency-key","Access-Control-Allow-Methods":"POST,OPTIONS"};
const out=(x:any,s=200)=>new Response(JSON.stringify(x),{status:s,headers:{...cors,"content-type":"application/json","cache-control":"no-store"}});
async function auth(req:Request){const a=req.headers.get("authorization");if(!a?.startsWith("Bearer "))throw new Error("AUTH_REQUIRED");const c=createClient(URL,ANON,{global:{headers:{Authorization:a}}});const {data,error}=await c.auth.getUser();if(error||!data.user)throw new Error("AUTH_INVALID");return data.user}
Deno.serve(async req=>{
 if(req.method==="OPTIONS")return out({ok:true});if(req.method!=="POST")return out({ok:false,error:"METHOD_NOT_ALLOWED"},405);
 try{
  const user=await auth(req);const b=await req.json().catch(()=>({}));const packet=String(b.packet_id||"").trim();if(!packet)throw new Error("PACKET_ID_REQUIRED");
  const {data:row,error}=await admin.from("nayanet_project_intelligence_bridge").select("*").eq("packet_id",packet).maybeSingle();if(error)throw error;if(!row)throw new Error("PACKET_NOT_FOUND");
  if(row.owner_id!==user.id)throw new Error("BRIDGE_OWNER_MISMATCH");
  if(!row.persisted||!row.indexed||!row.projected)throw new Error("BRIDGE_PROJECTION_NOT_COMPLETE");
  const retrievalEvidence=Array.isArray(b.retrieval_evidence)?b.retrieval_evidence:[],renderEvidence=Array.isArray(b.render_evidence)?b.render_evidence:[];
  const {data:event,error:ee}=await admin.from("nayanet_cognition_events").select("id,event_id,user_id,project_id").eq("id",row.receiver_event_id).eq("user_id",user.id).eq("project_id","NayaNET").maybeSingle();if(ee)throw ee;if(!event)throw new Error("RECEIVER_EVENT_NOT_FOUND_OR_NOT_OWNED");
  const {data:index,error:ie}=await admin.from("nayanet_intelligence_index").select("id,owner_id,source_id").eq("owner_id",user.id).eq("source_table","nayanet_cognition_events").eq("source_id",event.id).maybeSingle();if(ie)throw ie;if(!index)throw new Error("RECEIVER_INDEX_NOT_FOUND_OR_NOT_OWNED");
  if(retrievalEvidence.length===0||renderEvidence.length===0)throw new Error("ACK_REQUIRES_RETRIEVAL_AND_RENDER_EVIDENCE");
  const now=new Date().toISOString();const {data:updated,error:ue}=await admin.from("nayanet_project_intelligence_bridge").update({retrieved:true,rendered:true,retrieval_evidence:retrievalEvidence,render_evidence:renderEvidence,acknowledged_at:now,verified_at:now}).eq("packet_id",packet).eq("owner_id",user.id).select("*").single();if(ue)throw ue;
  return out({ok:true,ack:{schema:"NAYANET_PROJECT_INTELLIGENCE_ACK_V2",packet_id:updated.packet_id,project_id:updated.project_id,source_ref:updated.source_ref,content_hash:updated.content_hash,owner_id:updated.owner_id,receiver_transaction_id:updated.receiver_transaction_id,receiver_event_id:updated.receiver_event_id,receipt_id:updated.receipt_id,persisted:updated.persisted,indexed:updated.indexed,projected:updated.projected,retrieved:true,rendered:true,acknowledged_at:now,verified_at:now,evidence:{retrieval:retrievalEvidence,render:renderEvidence},canonical:{cognition_event_id:event.id,index_id:index.id}}});
 }catch(e){return out({ok:false,error:String((e as Error)?.message||e)},400)}
});