import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {PAGE_TYPES,makePagePolicy,proposePageSettings,validatePagePolicy,
        describePageSettings,publicIndexCandidate,changeImpact}
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
test('personal starts PRIVATE and UNLISTED but install preference on',()=>{
  const x=makePagePolicy('personal','my-personal');
  assert.deepEqual([x.visibility,x.discoverability,x.installation],['private','unlisted','enabled']);
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
  assert.deepEqual([x.visibility,x.discoverability],['private','unlisted']);
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
  assert.equal(manifest.test_status,'NO_LIVE_SERVER_OR_PWA_ACCEPTANCE_YET');
});
test('public+unlisted excludes recommendations, indexing and sitemap by contract',()=>{
  assert.match(manifest.indexing_policy['public/unlisted'],/omit from directory, suggestions, sitemap/);
  const p=proposePageSettings(makePagePolicy('space','unlisted-space'),{discoverability:'unlisted'});
  assert.equal(publicIndexCandidate(p,facts).candidate,false);
});
test('manifest defaults and code must agree exactly',()=>{
  for(const type of PAGE_TYPES){
    const x=makePagePolicy(type,'example');
    for(const key of ['visibility','discoverability','installation'])
      assert.equal(x[key],manifest.defaults[type][key]);
  }
});
