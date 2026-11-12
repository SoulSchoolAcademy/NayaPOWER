import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {validateCapabilityCatalog,assessClaim,intendedBenefits,recommendedPath,MODES}
  from '../tools/product/nayanet-capability-boundary.mjs';
const catalog=JSON.parse(readFileSync(new URL('../HUB/nayanet-capability-boundary.v1.json',import.meta.url),'utf8'));
const feat=id=>catalog.features.find(x=>x.id===id);
const change=fn=>{const c=structuredClone(catalog);fn(c);return c;};
test('25 proposed benefits; no implicit live proof',()=>{assert.equal(validateCapabilityCatalog(catalog),true);assert.equal(catalog.features.length,25);});
test('citizens may use a limited public-scope Naya guide without a fork when proven',()=>{const x=feat('public_naya_guide');assert.equal(x.offered_in.citizen,true);assert.ok(x.required_verified_gates.includes('rate_budget_limits_verified'));assert.equal(x.current_delivery,'UNKNOWN');});
test('three identity presences do not create a third subscription tier',()=>{
  assert.deepEqual(catalog.product_taxonomy.experiences,['nayanet_citizen','nayapower_connected']);
  assert.deepEqual(catalog.product_taxonomy.operator_deployments,['shared_managed','owner_controlled_fork']);
  assert.equal(catalog.product_taxonomy.operating_presences.naya_agent.human_owner,false);
});
test('Naya seat may join without fork but never inherits human authority',()=>{
  assert.equal(catalog.product_taxonomy.operating_presences.naya_agent.needs_fork_to_join,false);
  assert.equal(catalog.product_taxonomy.operating_presences.naya_agent.private_operator_grant,'requires_distinct_seat_identity_and_delegated_law_receipt');
  assert.throws(()=>validateCapabilityCatalog(change(c=>c.product_taxonomy.operating_presences.naya_agent.human_owner=true)));
});
test('seven doors are planned, no running doors fabricated',()=>{
  assert.equal(catalog.shared_door_contract.proposed_doors.length,7);
  assert.ok(Object.values(catalog.shared_door_contract.runtime_proof_by_door).every(v=>v==='UNKNOWN'));
  assert.throws(()=>validateCapabilityCatalog(change(c=>c.shared_door_contract.runtime_proof_by_door.mcp='PRODUCTION_PROVEN')));
});
test('certificate then skippable discovery then personal/business/space Hub is planned, not deployed',()=>{
  assert.equal(catalog.welcome_world_contract.status,'SPECIFIED_NOT_LIVE_VERIFIED');
  const xs=catalog.welcome_world_contract.ordered_journey;
  assert.ok(xs.indexOf('certificate')<xs.indexOf('one_question_per_screen'));
  assert.ok(xs.indexOf('one_question_per_screen')<xs.indexOf('hub_personal_business_space_top_three'));
  assert.equal(catalog.welcome_world_contract.business_and_space_may_be_skipped,true);
  assert.throws(()=>validateCapabilityCatalog(change(c=>c.welcome_world_contract.status='LIVE_VERIFIED')));
});
test('unbounded creation is desired, not falsely certified unlimited server capacity',()=>{
  assert.equal(catalog.operational_truth_policy.intended_unbounded_creation,true);
  assert.equal(catalog.operational_truth_policy.unlimited_capacity_production_verified,false);
  assert.throws(()=>validateCapabilityCatalog(change(c=>c.operational_truth_policy.unlimited_capacity_production_verified=true)));
});
test('mail transport evidence never certifies private mail security',()=>{
  assert.equal(catalog.operational_truth_policy.mail_transport_is_not_mail_confidentiality,true);
  assert.equal(catalog.operational_truth_policy.production_mail_privacy_status,'BLOCKED_PENDING_AUTHENTICATED_ISOLATION');
  assert.throws(()=>validateCapabilityCatalog(change(c=>c.operational_truth_policy.mail_transport_is_not_mail_confidentiality=false)));
});
test('all per-feature operations and independent verification remain deliberately unproven',()=>{
  assert.equal(catalog.features.length,25);
  catalog.features.forEach(f=>{assert.equal(f.delivery_evidence_contract.source_of_truth,null);
    assert.equal(f.delivery_evidence_contract.verified_at,null);
    assert.equal(f.delivery_evidence_contract.cost_profile,'UNMEASURED');});
  assert.throws(()=>validateCapabilityCatalog(change(c=>c.features[0].delivery_evidence_contract.verified_at='2026-10-24')));
});
test('every page has three separate controls with correct public/private defaults',()=>{
  const p=catalog.page_settings_contract;
  assert.deepEqual(p.independent_controls,['visibility','discoverability','installation']);
  assert.equal(p.defaults.personal,'private/findable/install-enabled');
  assert.equal(p.defaults.business,'public/findable/install-enabled');
  assert.equal(p.defaults.space,'public/findable/install-enabled');
  assert.equal(p.start_unpublished,true);
  assert.equal(p.multiple_pages_per_category,true);
});
test('no page can claim public discovery and install work without server acceptance',()=>{
  const p=catalog.page_settings_contract;
  assert.equal(p.production_state,'SPECIFIED_PROTOTYPED__SERVER_NOT_VERIFIED');
  for(const id of ['personal_world','business_page','starter_space','page_addons','private_visibility','smart_app_builder']){
    const f=feat(id);assert.ok(f.required_verified_gates.includes('per_page_visibility_and_discovery_server_verified'));
    assert.ok(f.required_verified_gates.includes('per_page_settings_owner_scope_verified'));
  }
  assert.throws(()=>validateCapabilityCatalog(change(c=>c.page_settings_contract.production_state='PRODUCTION_PROVEN')));
});
test('SN-0852 private findable is alias/topic Connect, never private content',()=>{
 const p=catalog.page_settings_contract;
 assert.equal(p.canonical_lesson_id,'SN-0852');
 assert.equal(p.defaults.personal,'private/findable/install-enabled');
 assert.equal(p.private_findable_requires_separately_approved_teaser,false);
 assert.equal(p.private_findable_alias_topic_connect_allowed,true);
 assert.equal(p.connect_and_page_content_are_separate_indexes,true);
 assert.equal(p.no_public_index_of_private_contents,true);
 assert.equal(p.real_identity_and_username_never_indexed,true);
 assert.equal(p.per_page_world_circle_membership_isolated,true);
 assert.equal(p.connect_and_share_and_reveal_are_separate_actions,true);
 assert.throws(()=>validateCapabilityCatalog(change(c=>c.page_settings_contract.no_public_index_of_private_contents=false)));
 assert.throws(()=>validateCapabilityCatalog(change(c=>c.page_settings_contract.real_identity_and_username_never_indexed=false)));
});
test('different public and private worlds never inherit each others community members',()=>{
 const p=catalog.page_settings_contract;
 assert.equal(p.per_page_world_circle_membership_isolated,true);
 assert.equal(p.connect_and_share_and_reveal_are_separate_actions,true);
 assert.throws(()=>validateCapabilityCatalog(change(c=>c.page_settings_contract.per_page_world_circle_membership_isolated=false)));
});
test('installable preference does not bypass real PWA deployment and privacy',()=>{
  assert.equal(catalog.page_settings_contract.all_installable_claim_requires_real_deployed_pwa_per_page,true);
  assert.ok(feat('page_addons').required_verified_gates.includes('per_page_pwa_installability_tested'));
  assert.throws(()=>validateCapabilityCatalog(change(c=>c.page_settings_contract.all_installable_claim_requires_real_deployed_pwa_per_page=false)));
});
test('citizens never require GitHub',()=>assert.equal(catalog.audiences.citizen.requires_github,false));
test('managed operator has no fork but is not deployed',()=>{assert.equal(catalog.audiences.managed_operator.requires_github,false);assert.equal(catalog.audiences.managed_operator.production_state,'NOT_VERIFIED');});
test('fork path is implementation partial',()=>assert.equal(catalog.audiences.owner_fork.production_state,'IMPLEMENTATION_PARTIAL'));
test('features all UNKNOWN by default',()=>catalog.features.forEach(f=>{assert.equal(f.current_delivery,'UNKNOWN');assert.deepEqual(f.live_evidence,[]);assert.equal(f.exact_deployed_sha,null);}));
test('private operator features never part of citizen contract',()=>catalog.features.forEach(f=>{if(f.operator_requirement)assert.equal(f.offered_in.citizen,false);}));
test('network benefits remain included after operator connection',()=>catalog.features.forEach(f=>{if(f.offered_in.citizen)assert.equal(f.offered_in.owner_fork,true);}));
test('match cannot silently consent to Connect or messaging',()=>{assert.ok(catalog.boundaries.connection_is_not_message_consent);assert.ok(feat('connections').required_verified_gates.includes('recipient_consent_verified'));});
test('private Smart Mail requires A/B/C denial test',()=>assert.ok(feat('private_mail').required_verified_gates.includes('real_a_b_c_denial_verified')));
test('public wisdom is not permission to publish private notes',()=>{assert.ok(catalog.boundaries.public_read_never_implies_collective_contribution);assert.equal(feat('collective_contribution').offered_in.citizen,false);});
test('privacy controls require server RLS',()=>assert.ok(feat('private_visibility').required_verified_gates.includes('server_visibility_rls_verified')));
test('additional pages subject to actual capacity not unlimited promise',()=>assert.ok(feat('page_addons').required_verified_gates.includes('capacity_limits_verified')));
test('literal zero operating cost prohibited',()=>assert.throws(()=>validateCapabilityCatalog(change(c=>c.unit_economics.cost_is_literally_zero=true))));
test('even valid spec never grants anything',()=>{for(const mode of MODES)for(const f of catalog.features){const r=assessClaim(catalog,f.id,mode);assert.equal(r.can_execute,false);assert.equal(r.marketing_claim_allowed,false);}});
test('fake client-provided proof fails closed without independent verifier',()=>{const f={verified:true,sha:'f'.repeat(40)};assert.equal(assessClaim(catalog,'private_mail','citizen',f).state,'SPECIFIED_NOT_PRODUCTION_PROVEN');});
test('invalid or failing independent proof remains blocked',()=>{assert.equal(assessClaim(catalog,'private_mail','citizen',{},()=>false).state,'NO_INDEPENDENT_PRODUCTION_ATTESTATION');});
test('even a forged trusted callback can neither authorize nor advertise production',()=>{const r=assessClaim(catalog,'public_knowledge','citizen',{},()=>true);assert.equal(r.state,'INDEPENDENT_PUBLICATION_RECEIPT_REQUIRED');assert.equal(r.can_execute,false);assert.equal(r.marketing_claim_allowed,false);});
test('citizen never gets personal private memory from UI marketing',()=>assert.equal(assessClaim(catalog,'owner_private_memory','citizen',{},()=>true).state,'NOT_IN_THIS_EXPERIENCE'));
test('managed operator never inherits a personal fork',()=>assert.equal(assessClaim(catalog,'personal_fork_projection','managed_operator',{},()=>true).state,'NOT_IN_THIS_EXPERIENCE'));
test('no feature advertised from proposed comparison data',()=>{const xs=intendedBenefits(catalog);assert.equal(xs.length,25);assert.ok(xs.every(x=>x.live_status==='UNKNOWN'&&!x.advertise_as_available));});
test('rejects duplicate feature ids',()=>assert.throws(()=>validateCapabilityCatalog(change(c=>c.features[1].id=c.features[0].id))));
test('rejects unsafe user seat becoming owner',()=>assert.throws(()=>validateCapabilityCatalog(change(c=>c.boundaries.agent_seat_is_not_owner=false))));
test('rejects fabricated production status in manifest',()=>assert.throws(()=>validateCapabilityCatalog(change(c=>c.features[0].current_delivery='PRODUCTION_PROVEN'))));
test('no-fork owner can later choose hosted vs independent fork',()=>{assert.equal(recommendedPath({}),'citizen');assert.equal(recommendedPath({wants_authorized_naya_operation:true}),'managed_operator');assert.equal(recommendedPath({wants_code_ownership:true}),'owner_fork');});
