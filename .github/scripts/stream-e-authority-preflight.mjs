export function inspectAuthorityGrant(value){
  const grantId=String(value??'').trim();
  if(!grantId)return {status:'BLOCKED',error_code:'AUTHORITY_GRANT_REQUIRED',authority_grant_id_present:false};
  if(!/^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(grantId))return {status:'BLOCKED',error_code:'AUTHORITY_GRANT_ID_INVALID',authority_grant_id_present:true};
  return {status:'PASS',error_code:null,authority_grant_id_present:true};
}
