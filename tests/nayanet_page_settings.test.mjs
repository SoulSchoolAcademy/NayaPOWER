import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {PAGE_TYPES,makePagePolicy,proposePageSettings,validatePagePolicy,
        describePageSettings,publicIndexCandidate,aliasTopicDiscoveryCandidate,
        separateWorldMembership,discoveryPlan,changeImpact}
  from '../tools/product/nayanet-page-settings.mjs';
const manifest=JSON.parse(readFileSync(new URL('../HUB/nayanet-page-settings.v1.json',import.meta.url),'utf8'));
const facts={issuer_auth_verified:true,published_on_server:true,viewer_scope_allowed:true,
  owner_choice_at_revision_verified:true,safe_public_projection_verified:true,not_blocked_or_revoked:true};
test('all six page classes have independent private/public, findability and install settings',()=>{
  assert.equal(PAGE_TYPES.length,6);
  assert.deepEqual(Object.keys(manifest.defaults).sort(),[...PAGE_TYPES].sort());
  for(const type of PAGE_TYPES){
    const policy=makePagePolicy(type,'some-page-id');
    assert.equal(validatePagePolicy(policy),true);
    assert.equal(policy.lifecycle,'DRAFT_UNPUBLISHED');
    assert.equal(policy.installation,'enabled');
  }
});
test('personal starts PRIVATE and FINDABLE but install preference on',()=>{
  const x=makePagePolicy('personal','my-personal');
  assert.deepEqual([x.visibility,x.discoverability,x.installation],['private','findable','enabled']);
  assert.equal(describePageSettings(x).public_content_after_explicit_publish,false);
});
test('business defaults PUBLIC / FINDABLE yet still unpublished draft',()=>{
  const p=makePagePolicy('business','new-business');
  assert.deepEqual([p.visibility,p.discoverability,p.lifecycle],['public','findable','DRAFT_UNPUBLISHED']);
  assert.equal(p.production_verified,false);
  assert.equal(p.last_receipt,null);
});
test('space defaults PUBLIC / FINDABLE but does not authorize anonymous reads',()=>{
  const p=makePagePolicy('space','topic-space');
  assert.deepEqual([p.visibility,p.discoverability],['public','findable']);
  assert.equal(publicIndexCandidate(p,null).candidate,false);
});
test('additional personal public and private pages are independent',()=>{
  const privatePage=makePagePolicy('personal','my-diary');
  const other=proposePageSettings(makePagePolicy('personal','my-public'),{visibility:'public',discoverability:'findable'});
  assert.equal(privatePage.visibility,'private');
  assert.equal(other.visibility,'public');
  assert.notEqual(privatePage.page_id,other.page_id);
});
test('owner can make a business private and a space unlisted independently',()=>{
  const business=proposePageSettings(makePagePolicy('business','local-business'),{visibility:'private'});
  const space=proposePageSettings(makePagePolicy('space','local-space'),{discoverability:'unlisted'});
  assert.equal(business.visibility,'private');
  assert.equal(business.discoverability,'findable');
  assert.equal(space.visibility,'public');
  assert.equal(space.discoverability,'unlisted');
});
test('private+findable never grants public private content or teaser by default',()=>{
  const p=proposePageSettings(makePagePolicy('personal','owner-private'),{discoverability:'findable'});
  const v=describePageSettings(p);
  assert.equal(v.appear_in_search_after_verified_publish,false);
  assert.equal(v.public_teaser_permitted,false);
  assert.equal(publicIndexCandidate(p,facts).candidate,false);
});
test('public+unlisted means direct-link could work but not discoverable',()=>{
  const p=proposePageSettings(makePagePolicy('business','unlisted-firm'),{discoverability:'unlisted'});
  const v=describePageSettings(p);
  assert.equal(v.public_content_after_explicit_publish,true);
  assert.equal(v.appear_in_search_after_verified_publish,false);
  assert.equal(publicIndexCandidate(p,facts).candidate,false);
  assert.match(v.warnings.join(' '),/Unlisted does not mean secret/);
});
test('install preference NEVER changes privacy or findability',()=>{
  const p=makePagePolicy('personal','private-app');
  const x=proposePageSettings(p,{installation:'disabled'});
  assert.deepEqual([x.visibility,x.discoverability],['private','findable']);
  assert.equal(x.installation,'disabled');
  assert.equal(publicIndexCandidate(x,facts).candidate,false);
});
test('page-owner intent alone cannot authorize index and Smart Match',()=>{
  const p=makePagePolicy('business','public-page');
  assert.equal(publicIndexCandidate(p,{}).candidate,false);
  assert.equal(publicIndexCandidate(p,{...facts,published_on_server:false}).candidate,false);
  assert.equal(publicIndexCandidate(p,{...facts,safe_public_projection_verified:false}).candidate,false);
  assert.equal(publicIndexCandidate(p,{...facts,not_blocked_or_revoked:false}).candidate,false);
});
test('even all nominal server facts only yield a candidate, never authority',()=>{
  const p=makePagePolicy('business','public-page');
  const r=publicIndexCandidate(p,facts);
  assert.equal(r.candidate,true);
  assert.equal(r.authorize_read,false);
  assert.equal(r.authorize_connect,false);
  assert.equal(r.authorize_send,false);
  assert.equal(r.reason,'ONLY_A_CANDIDATE_RECHECK_ON_TRUSTED_SERVER');
});
test('changing private into public forces owner review, never auto publication',()=>{
  const p=makePagePolicy('personal','me');
  const pub=proposePageSettings(p,{visibility:'public',discoverability:'findable'});
  const c=changeImpact(p,pub);
  assert.equal(c.requires_consent_review,true);
  assert.equal(c.requires_owner_authenticated_write,true);
  assert.equal(c.writes_performed,0);
  assert.equal(pub.lifecycle,'DRAFT_UNPUBLISHED');
});
test('changing public to private must unindex and invalidate caches',()=>{
  const p=makePagePolicy('space','project');
  const pri=proposePageSettings(p,{visibility:'private'});
  const c=changeImpact(p,pri);
  assert.equal(c.requires_unindex,true);
  assert.equal(c.requires_cache_invalidation,true);
});
test('switching findable to unlisted unindexes even if content stays public',()=>{
  const p=makePagePolicy('business','firm');
  const unlisted=proposePageSettings(p,{discoverability:'unlisted'});
  assert.equal(changeImpact(p,unlisted).requires_unindex,true);
});
test('one page cannot mutate another page id',()=>{
  assert.throws(()=>changeImpact(makePagePolicy('personal','alice'),makePagePolicy('personal','bob')),/CROSS_PAGE/);
});
test('no client can forge publication or server revision into proposed policy',()=>{
  assert.throws(()=>validatePagePolicy({...makePagePolicy('space','x'),lifecycle:'PUBLISHED'}),/UNVERIFIED_PUBLICATION/);
  assert.throws(()=>validatePagePolicy({...makePagePolicy('space','x'),server_revision:12}),/FABRICATED_SERVER/);
  assert.throws(()=>validatePagePolicy({...makePagePolicy('space','x'),private_teaser_approved:true}),/UNVERIFIED_PRIVATE_TEASER/);
});
test('unknown types and malicious input refuse rather than quietly default public',()=>{
  assert.throws(()=>makePagePolicy('profile','foo'),/UNKNOWN/);
  assert.throws(()=>makePagePolicy('personal','foo\nbar'),/INVALID_PAGE_ID/);
  assert.throws(()=>proposePageSettings(makePagePolicy('personal','x'),{visibility:'friends'}),/INVALID_PAGE_SETTING/);
  assert.throws(()=>proposePageSettings(makePagePolicy('personal','x'),{owner_id:'evil'}),/FORBIDDEN_PAGE_CHANGE/);
});
test('installable is per-page choice, not permission to offline-cache private records',()=>{
  const p=makePagePolicy('personal','diary');
  assert.equal(p.installation,'enabled');
  assert.equal(manifest.production_hard_gates.some(v=>/no storing private bytes in public service-worker caches/i.test(v)),true);
  assert.equal(manifest.test_status,'AUTHOR_PROTO_ONLY__SERVER_DISCOVERY_AND_ISOLATION_UNVERIFIED');
});
test('public+unlisted excludes recommendations, indexing and sitemap by contract',()=>{
  assert.match(manifest.indexing_policy['public/unlisted'],/omit ALL alias\/topic discovery and page content from search/);
  const p=proposePageSettings(makePagePolicy('space','unlisted-space'),{discoverability:'unlisted'});
  assert.equal(publicIndexCandidate(p,facts).candidate,false);
});
const aliasProof={issuer_auth_verified:true,claimed_alias_verified:true,
 alias_distinct_from_real_identity_verified:true,topic_consent_verified:true,
 discovery_audience_allowed:true,owner_choice_at_revision_verified:true,
 not_blocked_or_revoked:true,safe_connect_projection_verified:true,
 safe_alias:'sunflower_17',approved_topics:['science','community building']};
test('PRIVATE+FINDABLE Personal includes approved alias/tags but not page content',()=>{
 const p=makePagePolicy('personal','journal');
 assert.equal(p.visibility,'private');
 assert.equal(p.discoverability,'findable');
 const match=aliasTopicDiscoveryCandidate(p,aliasProof);
 assert.equal(match.candidate,true);
 assert.deepEqual(Object.keys(match).filter(k=>/identity|content|private/i.test(k)),
  ['authorize_private_read','authorize_identity_reveal','expose_private_page_content']);
 assert.equal(match.authorize_private_read,false);
 assert.equal(match.authorize_identity_reveal,false);
 assert.equal(match.expose_private_page_content,false);
 assert.equal(publicIndexCandidate(p,facts).candidate,false);
 assert.deepEqual(discoveryPlan(p),{alias_topic_connect_candidate:true,
   public_page_content_candidate:false,actual_publication:false,actual_server_read_grant:false});
});
test('unfindable disables all alias/topic matching even for a private world',()=>{
 const p=proposePageSettings(makePagePolicy('personal','journal'),{discoverability:'unlisted'});
 assert.equal(aliasTopicDiscoveryCandidate(p,aliasProof).candidate,false);
 assert.equal(discoveryPlan(p).alias_topic_connect_candidate,false);
});
test('public findable has separate page-content and alias projection',()=>{
 const p=makePagePolicy('business','business');
 assert.equal(discoveryPlan(p).public_page_content_candidate,true);
 assert.equal(aliasTopicDiscoveryCandidate(p,aliasProof).candidate,true);
 assert.equal(publicIndexCandidate(p,facts).candidate,true);
});
test('no alias, no reviewed topics, no trust -> no private world match',()=>{
 const p=makePagePolicy('personal','private');
 for(const proof of [null,{}, {...aliasProof,topic_consent_verified:false},
   {...aliasProof,alias_distinct_from_real_identity_verified:false},
   {...aliasProof,not_blocked_or_revoked:false},
   {...aliasProof,approved_topics:[]},
   {...aliasProof,safe_alias:'<script>alert(1)</script>'},
   {...aliasProof,approved_topics:['private\\npost']}]){
   assert.equal(aliasTopicDiscoveryCandidate(p,proof).candidate,false);
 }
});
test('extra private profile fields do not enter alias/topic match card',()=>{
 const p=makePagePolicy('personal','private');
 const proof={...aliasProof,real_name:'Do Not Index',username:'hidden_user',
   private_posts:['SECRET STORY'],membership_list:['secret member'],
   private_page_text:'my private diary'};
 const result=aliasTopicDiscoveryCandidate(p,proof);
 assert.equal(result.candidate,true);
 assert.equal(JSON.stringify(result).includes('Do Not Index'),false);
 assert.equal(JSON.stringify(result).includes('SECRET STORY'),false);
 assert.equal(JSON.stringify(result).includes('hidden_user'),false);
 assert.equal(JSON.stringify(result).includes('secret member'),false);
});
test('one owner with public/private worlds never shares membership automatically',()=>{
 const pri=makePagePolicy('personal','privateworld');
 const pub=proposePageSettings(makePagePolicy('personal','publicworld'),{visibility:'public'});
 const x=separateWorldMembership(pri,pub);
 assert.equal(x.same_world,false);
 assert.equal(x.cross_world_membership_grant,false);
 assert.equal(x.cross_world_post_copy,false);
 assert.equal(x.requires_individual_server_membership_check,true);
 assert.equal(x.private_world_link_is_not_access_grant,true);
});
test('page visibility toggle never changes alias matching or other circles',()=>{
 const pri=makePagePolicy('personal','private');
 const pub=proposePageSettings(pri,{visibility:'public'});
 const changed=changeImpact(pri,pub);
 assert.equal(changed.requires_alias_match_reindex,false);
 assert.equal(changed.cross_world_membership_changes,false);
 assert.equal(discoveryPlan(pub).alias_topic_connect_candidate,true);
});
test('findability off removes alias search, not private read permissions',()=>{
 const before=makePagePolicy('personal','private');
 const after=proposePageSettings(before,{discoverability:'unlisted'});
 const effect=changeImpact(before,after);
 assert.equal(effect.requires_alias_match_reindex,true);
 assert.equal(effect.requires_content_index_recheck,true);
 assert.equal(effect.cross_world_membership_changes,false);
});
test('manifest defaults and code must agree exactly',()=>{
  for(const type of PAGE_TYPES){
    const x=makePagePolicy(type,'example');
    for(const key of ['visibility','discoverability','installation'])
      assert.equal(x[key],manifest.defaults[type][key]);
  }
});
