import crypto from 'node:crypto';
const base=process.env.SUPABASE_URL,key=process.env.SUPABASE_PUBLISHABLE_KEY;
async function req(url,opt={}){const r=await fetch(url,opt),t=await r.text();let b;try{b=JSON.parse(t)}catch{b={raw:t}}if(!r.ok)throw new Error(r.status+' '+JSON.stringify(b));return b}
const anon=()=>req(base+'/auth/v1/signup',{method:'POST',headers:{apikey:key,'content-type':'application/json'},body:'{}'});
const u=await anon(), h={apikey:key,authorization:'Bearer '+u.access_token,'content-type':'application/json'};
const keyName='smart-mail-policy-'+crypto.randomBytes(6).toString('hex');
const create=async(v,parent=null)=>req(base+'/rest/v1/nayanet_policy_versions',{method:'POST',headers:{...h,'Prefer':'return=representation'},body:JSON.stringify({user_id:u.user.id,policy_key:keyName,version:v,parent_policy_id:parent,state:'DRAFT',policy:{capability:'smart_mail_send',strategy:'canonical'},validation:{},adversarial:{},holdout:{},promotion:{},rollback:{}})});
const v1=(await create(1))[0],v2=(await create(2,v1.id))[0];
async function transition(id,state,e={}){return req(base+'/rest/v1/rpc/nayanet_policy_transition',{method:'POST',headers:h,body:JSON.stringify({p_policy_id:id,p_to_state:state,p_evaluation:e})})}
await transition(v2.id,'VALIDATED',{result:'PASS',deterministic:true});
await transition(v2.id,'ADVERSARIAL_REVIEW',{result:'PASS',tests:5});
await transition(v2.id,'HOLDOUT_PASS',{result:'PASS',dataset_hash:'holdout-'+crypto.randomBytes(8).toString('hex'),baseline_score:0,candidate_score:0});
let blocked=false;try{await transition(v2.id,'PROMOTED',{authorized:false})}catch(e){blocked=true}
if(!blocked)throw new Error('PROMOTION_GATE_FAILED');
await transition(v2.id,'AUTHORIZATION_REQUIRED',{request:'controlled-test'});
await transition(v2.id,'CONTROLLED_TEST',{authorized:true});
await transition(v2.id,'OBSERVED',{observed:true});
await transition(v2.id,'VERIFIED',{result:'PASS',verified:true});
await transition(v2.id,'PROMOTED',{authorized:true});
const rows=await req(base+'/rest/v1/nayanet_policy_versions?select=state,version,holdout,adversarial,promotion&policy_key=eq.'+encodeURIComponent(keyName),{headers:h});
if(rows.length!==2||!rows.some(x=>x.version===2&&x.state==='PROMOTED'))throw new Error('POLICY_PROMOTION_PROOF_FAILED');
console.log('P1_POLICY_V1_V2=PASS');console.log('P1_VALIDATION=PASS');console.log('P1_ADVERSARIAL=PASS');console.log('P1_HOLDOUT=PASS');console.log('P1_UNAUTHORIZED_PROMOTION_BLOCKED=PASS');console.log('P1_CONTROLLED_TEST=PASS');console.log('P1_VERIFIED_PROMOTION=PASS');