import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2.57.0";
type SendBody={recipient_user_id:string;body:string;subject?:string;kind?:"direct"|"room"|"group"|"list";idempotency_key:string;project_id?:string};
const json=(payload:unknown,status=200)=>new Response(JSON.stringify(payload),{status,headers:{"content-type":"application/json","cache-control":"no-store"}});
Deno.serve(async(req)=>{
 if(req.method!=="POST")return json({ok:false,error:"METHOD_NOT_ALLOWED"},405);
 const authHeader=req.headers.get("authorization");
 if(!authHeader?.startsWith("Bearer "))return json({ok:false,error:"AUTH_REQUIRED"},401);
 const url=Deno.env.get("SUPABASE_URL")!,anon=Deno.env.get("SUPABASE_ANON_KEY")!,service=Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
 const userClient=createClient(url,anon,{global:{headers:{Authorization:authHeader}}}),admin=createClient(url,service);
 const {data:userData,error:userError}=await userClient.auth.getUser();
 if(userError||!userData.user)return json({ok:false,error:"AUTH_INVALID"},401);
 const senderId=userData.user.id;
 let input:SendBody;try{input=await req.json()}catch{return json({ok:false,error:"INVALID_JSON"},400)}
 if(!input?.recipient_user_id||!input?.body||!input?.idempotency_key)return json({ok:false,error:"RECIPIENT_BODY_IDEMPOTENCY_REQUIRED"},400);
 if(input.recipient_user_id===senderId)return json({ok:false,error:"SELF_RECIPIENT_NOT_ALLOWED"},400);
 if(input.body.length>10000)return json({ok:false,error:"BODY_TOO_LARGE"},400);
 const {data:recipient}=await admin.auth.admin.getUserById(input.recipient_user_id);
 if(!recipient?.user)return json({ok:false,error:"RECIPIENT_NOT_FOUND"},404);
 const {data:result,error}=await admin.rpc("nayanet_send_smart_mail",{
   p_sender_id:senderId,p_receiver_id:input.recipient_user_id,p_body:input.body,
   p_subject:input.subject??"NayaNET P0 communication proof",p_kind:input.kind??"direct",
   p_idempotency_key:input.idempotency_key,p_project_id:input.project_id??"NayaNET"
 });
 if(error)return json({ok:false,error:"SMART_MAIL_TRANSACTION_FAILED",detail:error.message},500);
 return json({ok:true,...result});
});