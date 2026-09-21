import "jsr:@supabase/functions-js/edge-runtime.d.ts";

const URL = Deno.env.get("SUPABASE_URL")!;
const ANON = Deno.env.get("SUPABASE_ANON_KEY")!;
const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization,apikey,content-type,x-idempotency-key",
  "Access-Control-Allow-Methods": "POST,OPTIONS"
};
const json=(body:unknown,status=200)=>new Response(JSON.stringify(body),{status,headers:{...cors,"Content-Type":"application/json"}});
const ACTION="reconcile";
Deno.serve(async(req)=>{
  if(req.method==="OPTIONS") return new Response("ok",{headers:cors});
  if(req.method!=="POST") return json({ok:false,error:"METHOD_NOT_ALLOWED"},405);
  const authorization=req.headers.get("Authorization");
  if(!authorization?.startsWith("Bearer ")) return json({ok:false,error:"AUTHORIZATION_REQUIRED"},401);
  let body:any={};
  try{body=await req.json();}catch{}
  const headers:any={"Authorization":authorization,"apikey":ANON,"Content-Type":"application/json"};
  const idem=req.headers.get("x-idempotency-key");
  if(idem) headers["x-idempotency-key"]=idem;
  try{
    const response=await fetch(`${URL}/functions/v1/nayanet-compound-intelligence`,{
      method:"POST",headers,body:JSON.stringify({...body,action:ACTION})
    });
    const result=await response.json().catch(()=>({ok:false,error:"INVALID_DELEGATE_RESPONSE"}));
    return json({ok:response.ok,edge_function:"nayanet-pi-reconcile",action:ACTION,delegated_to:"nayanet-compound-intelligence",result},response.status);
  }catch(e){
    return json({ok:false,edge_function:"nayanet-pi-reconcile",action:ACTION,error:String((e as Error)?.message||e)},502);
  }
});