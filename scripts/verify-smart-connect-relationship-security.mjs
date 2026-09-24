import crypto from 'node:crypto';

const base=process.env.SUPABASE_URL;
const key=process.env.SUPABASE_PUBLISHABLE_KEY;
const spaceId=process.env.NAYA_EXISTING_SPACE_ID||'04ee4dc8-bc73-47df-a1de-162570f6a56e';
const project='NayaNET-smart-connect-'+Date.now()+'-'+crypto.randomBytes(4).toString('hex');

async function req(url,opt={}) {
  const r=await fetch(url,opt);
  const t=await r.text();
  let b; try { b=JSON.parse(t); } catch { b={raw:t}; }
  if(!r.ok) throw new Error(r.status+' '+JSON.stringify(b));
  return b;
}
const h=t=>({apikey:key,authorization:'Bearer '+t,'content-type':'application/json'});
const signup=()=>req(base+'/auth/v1/signup',{method:'POST',headers:{apikey:key,'content-type':'application/json'},body:'{}'});
const list=token=>req(base+'/rest/v1/nayanet_connections?select=id,owner_member_id,connected_member_id,status,source_type,source_space_id&order=created_at.desc',{headers:h(token)});
const save=(token,target)=>req(base+'/rest/v1/rpc/nayanet_save_connection',{method:'POST',headers:h(token),body:JSON.stringify({p_target_member_id:target,p_space_id:spaceId})});
const revoke=(token,target)=>req(base+'/rest/v1/rpc/nayanet_revoke_connection',{method:'POST',headers:h(token),body:JSON.stringify({p_target_member_id:target})});
const join=token=>req(base+'/rest/v1/rpc/nayanet_join_space',{method:'POST',headers:h(token),body:JSON.stringify({p_space_id:spaceId})});

async function expectDenied(promise,label){
  try { const out=await promise; throw new Error(label+'_UNEXPECTED_SUCCESS:'+JSON.stringify(out)); }
  catch(e) { const s=String(e); if(/UNEXPECTED_SUCCESS/.test(s)) throw e; return s; }
}

const A=await signup(),B=await signup(),C=await signup();
if(!A.access_token||!B.access_token||!C.access_token) throw new Error('USER_CREATION_FAILED');

await join(A.access_token); await join(B.access_token); await join(C.access_token);

const first=await save(A.access_token,B.user.id);
if(first.status!=='CONNECTED'||!first.connection?.id||first.connection.owner_member_id!==A.user.id||first.connection.connected_member_id!==B.user.id) throw new Error('OWNER_CREATE_FAILED');

const ownerRows=await list(A.access_token);
const ownerRow=ownerRows.find(x=>x.id===first.connection.id);
if(!ownerRow||ownerRow.owner_member_id!==A.user.id||ownerRow.connected_member_id!==B.user.id||ownerRow.status!=='active') throw new Error('OWNER_RETRIEVAL_FAILED');

const nonOwnerRows=await list(B.access_token);
if(nonOwnerRows.some(x=>x.id===first.connection.id)) throw new Error('NON_OWNER_RETRIEVAL_LEAK');

const nonOwnerRevoke=await expectDenied(revoke(B.access_token,A.user.id),'NON_OWNER_REVOKE');
if(!/CONNECTION_NOT_FOUND|403|DENIED|FAILED/i.test(nonOwnerRevoke)) throw new Error('NON_OWNER_REVOKE_WRONG_ERROR:'+nonOwnerRevoke);

const replaySave=await save(A.access_token,B.user.id);
if(replaySave.status!=='ALREADY_CONNECTED'||replaySave.connection?.id!==first.connection.id) throw new Error('CONNECT_REPLAY_NOT_IDEMPOTENT');

const revoked=await revoke(A.access_token,B.user.id);
if(revoked.status!=='REVOKED'||revoked.connection?.id!==first.connection.id||revoked.connection?.status!=='revoked') throw new Error('OWNER_REVOKE_FAILED');

const revokeReplay=await revoke(A.access_token,B.user.id);
if(revokeReplay.status!=='ALREADY_REVOKED'||revokeReplay.connection?.id!==first.connection.id) throw new Error('REVOKE_REPLAY_NOT_IDEMPOTENT');

const afterOwner=await list(A.access_token);
const after=afterOwner.find(x=>x.id===first.connection.id);
if(!after||after.status!=='revoked') throw new Error('OWNER_POST_REVOKE_RETRIEVAL_FAILED');

const afterNonOwner=await list(B.access_token);
if(afterNonOwner.some(x=>x.id===first.connection.id)) throw new Error('NON_OWNER_POST_REVOKE_LEAK');

console.log('SMART_CONNECT_RELATIONSHIP_SECURITY=VERIFIED');
console.log('OWNER_CREATE=PASS');
console.log('OWNER_RETRIEVAL=PASS');
console.log('NON_OWNER_RETRIEVAL=BLOCKED');
console.log('NON_OWNER_REVOKE=BLOCKED');
console.log('CONNECT_REPLAY=IDEMPOTENT');
console.log('OWNER_REVOKE=PASS');
console.log('REVOKE_REPLAY=IDEMPOTENT');
console.log('POST_REVOKE_OWNER_STATE=REVOKED');
console.log('POST_REVOKE_NON_OWNER_STATE=BLOCKED');
console.log(JSON.stringify({schema:'NAYANET_SMART_CONNECT_RELATIONSHIP_SECURITY_PROOF_V1',project,space_id:spaceId,connection_id:first.connection.id,owner_id:A.user.id,connected_member_id:B.user.id,checks:{owner_create:true,owner_retrieval:true,non_owner_retrieval:false,non_owner_revoke:false,connect_replay_same_id:true,owner_revoke:true,revoke_replay_same_id:true,post_revoke_owner_visible:true,post_revoke_non_owner_hidden:true}}));
