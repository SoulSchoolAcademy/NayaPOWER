/**
 * NayaNET universal per-page policy: UI intent + safe catalog projections.
 * NOT server authorization. Production must independently validate owner,
 * scope, revision and RLS on every read/write/index/publish/install action.
 */
export const PAGE_TYPES=Object.freeze(['personal','business','space','smart_app','project_page','other_page']);
export const VISIBILITY=Object.freeze(['private','public']);
export const DISCOVERABILITY=Object.freeze(['unlisted','findable']);
export const INSTALLATION=Object.freeze(['enabled','disabled']);
export const DEFAULTS=Object.freeze({
  personal:{visibility:'private',discoverability:'unlisted',installation:'enabled'},
  business:{visibility:'public',discoverability:'findable',installation:'enabled'},
  space:{visibility:'public',discoverability:'findable',installation:'enabled'},
  smart_app:{visibility:'private',discoverability:'unlisted',installation:'enabled'},
  project_page:{visibility:'private',discoverability:'unlisted',installation:'enabled'},
  other_page:{visibility:'private',discoverability:'unlisted',installation:'enabled'}
});
const SIMPLE_ID=/^[a-zA-Z0-9:_./-]{1,180}$/;
const ALLOWED_KEYS=new Set(['visibility','discoverability','installation']);
function assertChoice(key,value){
  const values={visibility:VISIBILITY,discoverability:DISCOVERABILITY,installation:INSTALLATION}[key];
  if(!values||!values.includes(value))throw Error('INVALID_PAGE_SETTING_'+key.toUpperCase());
}
export function validatePagePolicy(policy){
  if(!policy || !PAGE_TYPES.includes(policy.page_type) ||
      typeof policy.page_id!=='string'||!SIMPLE_ID.test(policy.page_id))
    throw Error('INVALID_PAGE_IDENTITY');
  for(const key of ALLOWED_KEYS)assertChoice(key,policy[key]);
  if(policy.lifecycle!=='DRAFT_UNPUBLISHED')
    throw Error('UNVERIFIED_PUBLICATION');
  if(policy.server_revision!==null || policy.production_verified!==false ||
     policy.last_receipt!==null)throw Error('FABRICATED_SERVER_EVIDENCE');
  if(policy.private_teaser_approved!==false)throw Error('UNVERIFIED_PRIVATE_TEASER');
  return true;
}
export function makePagePolicy(page_type,page_id){
  if(!PAGE_TYPES.includes(page_type))throw Error('UNKNOWN_PAGE_TYPE');
  if(typeof page_id!=='string'||!SIMPLE_ID.test(page_id))
    throw Error('INVALID_PAGE_ID');
  const d=DEFAULTS[page_type];
  return {contract:'nayanet.page-settings.v1',page_type,page_id,
    visibility:d.visibility,discoverability:d.discoverability,
    installation:d.installation,lifecycle:'DRAFT_UNPUBLISHED',
    private_teaser_approved:false,server_revision:null,production_verified:false,
    last_receipt:null};
}
/** Change only proposed values on one page. This does not persist anything. */
export function proposePageSettings(policy,changes){
  validatePagePolicy(policy);
  if(!changes || typeof changes!=='object'||Array.isArray(changes))
    throw Error('INVALID_PAGE_CHANGES');
  if(Object.keys(changes).some(k=>!ALLOWED_KEYS.has(k)))
    throw Error('FORBIDDEN_PAGE_CHANGE');
  const proposal={...policy};
  for(const [key,value] of Object.entries(changes)){
    assertChoice(key,value); proposal[key]=value;
  }
  // A private -> public change must be consciously reviewed on the backend,
  // not promoted because a toggle on this untrusted object flipped.
  validatePagePolicy(proposal);
  return proposal;
}
/** Explanations only; not authorization and never a publication event. */
export function describePageSettings(policy){
  validatePagePolicy(policy);
  const visible=policy.visibility==='public';
  const listed=policy.discoverability==='findable';
  const warnings=[];
  if(visible&&!listed)warnings.push('Anyone with a shared link may view this page after you publish it. Unlisted does not mean secret.');
  if(!visible&&listed)warnings.push('Private content stays locked. A findable preview is separate opt-in, not enabled by this setting alone.');
  if(!visible)warnings.push('Private data must remain protected by server permissions, even with a known URL.');
  if(policy.installation==='enabled')warnings.push('Install is available only if the deployed Smart App and your browser support it. Private data is not cached publicly.');
  return {preview_only:true,public_content_after_explicit_publish:visible,
    appear_in_search_after_verified_publish:visible&&listed,
    hidden_from_network_search:!listed || !visible,
    public_teaser_permitted:false,install_preference_enabled:policy.installation==='enabled',
    current_status:'DRAFT_UNPUBLISHED',warnings};
}
/** Models the *extra* proven server conditions needed for index and AutoMatch.
 * An untrusted client calling this can NEVER grant server access or publish.
 */
export function publicIndexCandidate(policy,verifiedServerFacts){
  validatePagePolicy(policy);
  const p=verifiedServerFacts;
  if(policy.visibility!=='public'||policy.discoverability!=='findable')
    return {candidate:false,reason:'OWNER_VISIBILITY_OR_DISCOVERY_REFUSED'};
  // A browser can supply an object that LOOKS like this. Actual matching
  // service MUST derive these facts from trusted DB and RLS, never arguments.
  if(!p || p.issuer_auth_verified!==true || p.published_on_server!==true ||
     p.viewer_scope_allowed!==true || p.owner_choice_at_revision_verified!==true ||
     p.safe_public_projection_verified!==true || p.not_blocked_or_revoked!==true)
    return {candidate:false,reason:'SERVER_PROOF_REQUIRED'};
  return {candidate:true,reason:'ONLY_A_CANDIDATE_RECHECK_ON_TRUSTED_SERVER',
    authorize_read:false,authorize_connect:false,authorize_send:false};
}
export function changeImpact(before,after){
  validatePagePolicy(before);validatePagePolicy(after);
  if(before.page_id!==after.page_id || before.page_type!==after.page_type)
    throw Error('CROSS_PAGE_MUTATION');
  return {same_page:true,
    requires_owner_authenticated_write:true,
    requires_server_revision_check:true,
    requires_consent_review:(before.visibility==='private'&&after.visibility==='public'),
    requires_unindex:(before.visibility==='public'&&after.visibility==='private')||
      (before.discoverability==='findable'&&after.discoverability==='unlisted'),
    requires_cache_invalidation:before.visibility!==after.visibility ||
      before.discoverability!==after.discoverability,
    requires_install_manifest_recheck:before.installation!==after.installation,
    writes_performed:0};
}
