/**
 * Product claim audit only, NOT LAW/ACT authorization or subscription billing.
 * Unverified specs, user-editable JSON, JS callbacks and UI cannot grant access.
 * Every real read/write must enforce server-side owner/tenant and fresh scopes.
 */
export const MODES = Object.freeze(['citizen','managed_operator','owner_fork']);
export function validateCapabilityCatalog(c) {
  if (!c || c.schema!=='nayanet.capability-boundary.v1' ||
      c.state!=='PROPOSED_AND_UNVERIFIED' ||
      !Array.isArray(c.features) || c.features.length!==25) throw Error('invalid_catalog');
  const t=c.product_taxonomy||{};
  if(JSON.stringify(t.experiences)!==JSON.stringify(['nayanet_citizen','nayapower_connected']) ||
     JSON.stringify(t.operator_deployments)!==JSON.stringify(['shared_managed','owner_controlled_fork']) ||
     !t.builder_is_optional_operational_role_not_required_subscription_tier ||
     !t.product_mode_is_not_identity_or_authority ||
     !t.hosting_location_does_not_grant_personal_intelligence_access)
    throw Error('product_role_and_deployment_conflated');
  const presences=t.operating_presences||{};
  if(Object.keys(presences).sort().join(',')!=='citizen,connected_owner,naya_agent' ||
     Object.values(presences).some(x=>x.needs_fork_to_join!==false) ||
     presences.naya_agent.human_owner!==false ||
     presences.naya_agent.private_operator_grant!=='requires_distinct_seat_identity_and_delegated_law_receipt')
    throw Error('invalid_principal_role_model');
  const doors=c.shared_door_contract||{};
  const requiredDoors=['hub','mcp','rest_api','github_app','sdk','webhook','a2a'];
  if(doors.proposed_doors?.join(',')!==requiredDoors.join(',') ||
     Object.keys(doors.runtime_proof_by_door||{}).sort().join(',')!==[...requiredDoors].sort().join(',') ||
     !Object.values(doors.runtime_proof_by_door).every(x=>x==='UNKNOWN') ||
     !String(doors.canonical_operation_path||'').includes('LAW'))
    throw Error('independent_unverified_one_brain_doors_required');
  const welcome=c.welcome_world_contract||{};
  if(welcome.status!=='SPECIFIED_NOT_LIVE_VERIFIED' ||
     !welcome.ordered_journey?.includes('certificate') ||
     !welcome.ordered_journey?.includes('hub_personal_business_space_top_three') ||
     welcome.business_and_space_may_be_skipped!==true ||
     welcome.app_and_space_creation_must_be_authenticated!==true ||
     welcome.empty_answers_are_never_invented!==true ||
     welcome.recommendation_never_implies_connect_send_or_join!==true)
    throw Error('invalid_first_citizen_journey');
  const truth=c.operational_truth_policy||{};
  if(truth.intended_unbounded_creation!==true ||
     truth.unlimited_capacity_production_verified!==false ||
     truth.mail_transport_is_not_mail_confidentiality!==true ||
     truth.production_mail_privacy_status!=='BLOCKED_PENDING_AUTHENTICATED_ISOLATION')
    throw Error('unproven_operational_claim');
  if(c.unit_economics?.cost_is_literally_zero!==false) throw Error('zero_cost_false');
  const b=c.boundaries||{};
  for(const key of ['one_network','agent_seat_is_not_owner',
    'personal_state_isolated_by_owner','connection_is_not_message_consent',
    'public_read_never_implies_collective_contribution',
    'fork_not_equal_to_runtime_activation','unlimited_pages_not_promised'])
    if(b[key]!==true) throw Error('missing_boundary:'+key);
  const seen=new Set();
  for(const f of c.features){
    if (!/^[a-z0-9_]+$/.test(f.id||'')||seen.has(f.id)) throw Error('invalid_feature_id');
    seen.add(f.id);
    if(!f.label||!f.human_benefit||f.current_delivery!=='UNKNOWN' ||
       f.exact_deployed_sha!==null||!Array.isArray(f.live_evidence)||f.live_evidence.length)
      throw Error('false_product_proof:'+f.id);
    if(!Array.isArray(f.required_verified_gates)||!f.required_verified_gates.length)
      throw Error('no_acceptance_gate:'+f.id);
    for(const mode of MODES)
      if(typeof f.offered_in?.[mode]!=='boolean')throw Error('invalid_mode:'+mode);
    const e=f.delivery_evidence_contract||{};
    if(e.canonical_operation!==null||e.source_of_truth!==null ||
       e.server_authority_scope!==null||e.independent_verifier!==null ||
       e.verified_at!==null||e.privacy_class!=='UNASSESSED' ||
       e.cost_profile!=='UNMEASURED' ||
       !Array.isArray(e.additional_evidence)||e.additional_evidence.length)
      throw Error('unverified_runtime_metadata_fabricated:'+f.id);
    if(f.operator_requirement && f.offered_in.citizen)throw Error('operator_granted_to_citizen');
    if(f.offered_in.citizen && !f.offered_in.owner_fork)throw Error('base_world_removed');
  }
  function requires(id,key){const f=c.features.find(x=>x.id===id);
    if(!f||!f.required_verified_gates.includes(key))throw Error('missing_gate:'+id+':'+key);}
  requires('private_mail','real_a_b_c_denial_verified');
  requires('connections','recipient_consent_verified');
  requires('collective_contribution','explicit_share_verified');
  requires('private_visibility','server_visibility_rls_verified');
  requires('page_addons','capacity_limits_verified');
  if(c.features.find(x=>x.id==='personal_fork_projection')?.offered_in.managed_operator)
    throw Error('fork_projection_without_fork');
  return true;
}
/** Status for customer-facing evidence audit only. This never authorizes. */
export function assessClaim(c,id,mode,proofPacket=null,trustedServerVerifier=null){
  validateCapabilityCatalog(c);
  const blocked=(state)=>({state,marketing_claim_allowed:false,can_execute:false});
  if(!MODES.includes(mode))return blocked('UNKNOWN_MODE');
  const f=c.features.find(x=>x.id===id);
  if(!f)return blocked('UNKNOWN_FEATURE');
  if(!f.offered_in[mode])return blocked('NOT_IN_THIS_EXPERIENCE');
  if(!proofPacket||typeof trustedServerVerifier!=='function')
    return blocked('SPECIFIED_NOT_PRODUCTION_PROVEN');
  let valid=false;
  try{valid=trustedServerVerifier({featureId:id,mode,
    requiredGates:f.required_verified_gates,proofPacket})===true;}catch(_){}
  if(!valid)return blocked('NO_INDEPENDENT_PRODUCTION_ATTESTATION');
  // Do not grant a marketing/live claim from a callback either: an actual
  // independently authenticated receipt publisher must own this transition.
  return {state:'INDEPENDENT_PUBLICATION_RECEIPT_REQUIRED',marketing_claim_allowed:false,can_execute:false};
}
export function intendedBenefits(c){
  validateCapabilityCatalog(c);
  return c.features.map(f=>({id:f.id,benefit:f.human_benefit,
    citizen:f.offered_in.citizen?'INTENDED':'NOT_INCLUDED',
    managed_operator:f.offered_in.managed_operator?'PROPOSED':'NOT_INCLUDED',
    owner_fork:f.offered_in.owner_fork?'INTENDED':'NOT_INCLUDED',
    live_status:'UNKNOWN',advertise_as_available:false}));
}
export function recommendedPath(request={}){
  return request.wants_code_ownership===true?'owner_fork':
    request.wants_authorized_naya_operation===true?'managed_operator':'citizen';
}
