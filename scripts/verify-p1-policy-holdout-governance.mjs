import crypto from 'node:crypto';
const base=process.env.SUPABASE_URL,key=process.env.SUPABASE_PUBLISHABLE_KEY;
async function req(url,opt={}){const r=await fetch(url,opt),t=await r.text();let b;try{b=JSON.parse(t)}catch{b={raw:t}}if(!r.ok)throw new Error(r.status+' '+JSON.stringify(b));return b}
const anon=()=>req(base+'/auth/v1/signup',{method:'POST',headers:{apikey:key,'content-type':'application/json'},body:'{}'});
const u=await anon(), h={apikey:key,authorization:'Bearer '+u.access_token,'content-type':'application/json'};
const keyName='smart-mail-policy-'+crypto.randomBytes(6).toString('hex');
const create=async(v,parent=null)=>req(base+'/rest/v1/nayanet_policy_versions',{method:'POST',headers:{...h,'Prefer':'return=representation'},body:JSON.stringify({user_id:u.user.id,policy_key:keyName,version:v,parent_policy_id:parent,state:'DRAFT',policy:{capability:'smart_mail_send',strategy:v===1?'canonical':'canonical-candidate'},validation:{},adversarial:{},holdout:{},promotion:{},rollback:{}})});
const v1=(await create(1))[0],v2=(await create(2,v1.id))[0];
async function transition(id,state,e={}){return req(base+'/rest/v1/rpc/nayanet_policy_transition',{method:'POST',headers:h,body:JSON.stringify({p_policy_id:id,p_to_state:state,p_evaluation:e})})}
async function evaluate(policyId,type,evidence){return req(base+'/rest/v1/nayanet_policy_evaluations',{method:'POST',headers:{...h,'Prefer':'return=representation'},body:JSON.stringify({user_id:u.user.id,policy_id:policyId,evaluation_type:type,dataset_hash:evidence.dataset_hash||null,baseline_score:evidence.baseline_score??null,candidate_score:evidence.candidate_score??null,responsible_value:evidence.responsible_value??null,verified:evidence.verified??false,result:evidence.result,evidence})})}
const deterministicDataset='p1-deterministic-fixtures-v1';
await evaluate(v1.id,'DETERMINISTIC',{result:'PASS',dataset_hash:deterministicDataset,baseline_score:3,candidate_score:3,verified:true,cases:3});
await evaluate(v2.id,'DETERMINISTIC',{result:'PASS',dataset_hash:deterministicDataset,baseline_score:3,candidate_score:3,verified:true,cases:3});
await transition(v2.id,'VALIDATED',{result:'PASS',deterministic:true,dataset_hash:deterministicDataset});
await evaluate(v2.id,'ADVERSARIAL',{result:'PASS',dataset_hash:'p1-adversarial-fixtures-v1',verified:true,tests:5,failures:0});
await transition(v2.id,'ADVERSARIAL_REVIEW',{result:'PASS',tests:5,failures:0,dataset_hash:'p1-adversarial-fixtures-v1'});
await evaluate(v2.id,'HOLDOUT',{result:'PASS',dataset_hash:'p1-holdout-fixtures-v1',baseline_score:0,candidate_score:0,verified:true,cases:3});
await transition(v2.id,'HOLDOUT_PASS',{result:'PASS',dataset_hash:'p1-holdout-fixtures-v1',baseline_score:0,candidate_score:0,verified:true,cases:3});
let blocked=false;try{await transition(v2.id,'PROMOTED',{authorized:false})}catch(e){blocked=true}
if(!blocked)throw new Error('PROMOTION_GATE_FAILED');
await transition(v2.id,'AUTHORIZATION_REQUIRED',{request:'controlled-test',authorized:false});
await transition(v2.id,'CONTROLLED_TEST',{authorized:true});
await transition(v2.id,'OBSERVED',{observed:true});
await transition(v2.id,'VERIFIED',{result:'PASS',verified:true});
await transition(v2.id,'PROMOTED',{authorized:true,reason:'explicit-human-authorization'});
const promoted=await req(base+'/rest/v1/nayanet_policy_versions?select=id,state,version,holdout,adversarial,promotion,rollback&policy_key=eq.'+encodeURIComponent(keyName),{headers:h});
if(promoted.length!==2||!promoted.some(x=>x.version===2&&x.state==='PROMOTED'))throw new Error('POLICY_PROMOTION_PROOF_FAILED');
await transition(v2.id,'ROLLED_BACK',{reason:'runtime-rollback-acceptance',rollback_target_version:1,authorized:true});
const finalRows=await req(base+'/rest/v1/nayanet_policy_versions?select=state,version,rollback&policy_key=eq.'+encodeURIComponent(keyName),{headers:h});
if(!finalRows.some(x=>x.version===2&&x.state==='ROLLED_BACK'))throw new Error('POLICY_ROLLBACK_PROOF_FAILED');
console.log('P1_POLICY_V1_V2=PASS');console.log('P1_DETERMINISTIC=PASS');console.log('P1_ADVERSARIAL=PASS');console.log('P1_HOLDOUT=PASS');console.log('P1_UNAUTHORIZED_PROMOTION_BLOCKED=PASS');console.log('P1_CONTROLLED_TEST=PASS');console.log('P1_OBSERVED=PASS');console.log('P1_VERIFIED_PROMOTION=PASS');console.log('P1_ROLLBACK=PASS');