import test from 'node:test';
import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
import {readFileSync} from 'node:fs';
const require=createRequire(import.meta.url);
const C=require('../HUB/citizen-discovery-core.js');
function complete(values={},publicKeys=[],optIn=false){
  const s=C.createSession({alias:'alice',name:'Alice'});
  for(const q of C.FIELDS){if(q.key in values)s.answer(values[q.key]);else s.skip();}
  for(const x of publicKeys)s.setPublic(x,true);
  s.setDiscoveryOptIn(optIn);return s;
}
test('ten structured post-Welcome questions, not email or automatic account claims',()=>{
  assert.equal(C.FIELDS.length,10);
  assert.deepEqual(C.FIELDS.map(x=>x.key),['about','interests','mission','vision','goals',
    'motto','business','offer','space_topics','looking_for']);
  assert.ok(!C.FIELDS.some(x=>x.key==='email'));
});
test('three answer modes are input-equivalent and drafts are unpublished',()=>{
  const s=complete({about:'I teach science',mission:'Accessible learning'});
  const p=s.packet(),d=s.preview();
  assert.equal(d.personal.mission,'Accessible learning');
  assert.equal(d.state,'UNPUBLISHED_PREVIEW');
  assert.equal(d.requires_authenticated_save,true);
  assert.equal(p.requires_explicit_review_and_publish,true);
});
test('every step is skippable, with no fabricated business or community',()=>{
  const s=complete();
  const d=s.preview();
  assert.equal(s.state().at_review,true);
  assert.equal(d.business.applicable,false);
  assert.equal(d.space.applicable,false);
  assert.equal(d.personal.mission,'');
});
test('back and edit keep answers until user changes them',()=>{
  const s=complete({mission:'Make good things'});
  assert.equal(s.back(),true);
  assert.equal(s.edit('mission'),true);
  s.answer('Help everyone learn');
  assert.equal(s.packet().answers.mission,'Help everyone learn');
});
test('private by default; opt-in alone reveals no answers',()=>{
  const s=complete({interests:'machine learning',mission:'Kindness'});
  assert.equal(C.discoveryFeatures(s.packet()),null);
  s.setDiscoveryOptIn(true);
  assert.deepEqual(C.discoveryFeatures(s.packet()).topics,[]);
  assert.equal(s.packet().visibility.mission,'private');
  assert.equal(s.packet().visibility.interests,'private');
});
test('only allowed public discovery fields are eligible',()=>{
  const s=complete({about:'sensitive personal story',interests:'learning and astronomy',
      goals:'teach science',mission:'Private life'});
  assert.equal(s.setPublic('mission',true),false);
  s.setPublic('interests',true);s.setPublic('goals',true);s.setDiscoveryOptIn(true);
  const t=C.discoveryFeatures(s.packet());
  assert.ok(t.topics.includes('astronomy'));
  assert.ok(!JSON.stringify(t).includes('sensitive'));
  assert.ok(!JSON.stringify(t).includes('private'));
});
test('public-only ranking requires two independent matching signals',()=>{
  const s=complete({interests:'astronomy science',goals:'science education'},['interests','goals'],true);
  const result=C.rankPublicCandidates(s.packet(),[
    {id:'x',visibility:'public',discoverable:true,public_features:{topics:['astronomy','science'],goals:['science','education']}},
    {id:'y',visibility:'public',discoverable:true,public_features:{topics:['astronomy'],goals:['unrelated']}}
  ]);
  assert.deepEqual(result.map(x=>x.id),['x']);
  assert.ok(result[0].estimated_relevance_percent>0);
  assert.equal(result[0].uncalibrated,true);
  assert.equal(result[0].authorized_action,'SUGGEST_ONLY');
});
test('non-public, opted-out, self and blocked people are never ranked',()=>{
  const s=complete({interests:'science astronomy',goals:'science education'},['interests','goals'],true);
  const data={visibility:'public',discoverable:true,public_features:{topics:'science astronomy',goals:'science education'}};
  const items=[{id:'private',...data,visibility:'private'},
    {id:'opted',...data,opted_out:true},
    {id:'not_discoverable',...data,discoverable:false},
    {id:'self',alias:'alice',...data},
    {id:'blocked',...data},
    {id:'allowed',...data}];
  const r=C.rankPublicCandidates(s.packet(),items,{blocked_ids:['blocked']});
  assert.deepEqual(r.map(x=>x.id),['allowed']);
});
test('unknown or unilateral claims do not create a match',()=>{
  const s=complete({interests:'astronomy'},['interests'],true);
  const c={id:'a',visibility:'public',discoverable:true,public_features:{topics:'astronomy'}};
  assert.deepEqual(C.rankPublicCandidates(s.packet(),[c]),[]);
});
test('no matching at all without discovery opt in',()=>{
  const s=complete({interests:'astronomy',goals:'science teaching'},['interests','goals'],false);
  const c={id:'a',visibility:'public',discoverable:true,public_features:{topics:'astronomy',goals:'science teaching'}};
  assert.deepEqual(C.rankPublicCandidates(s.packet(),[c]),[]);
});
test('match ranking is stable, reasoned and does not mutate people',()=>{
  const s=complete({interests:'community science',goals:'education science'},['interests','goals'],true);
  const person={id:'a',visibility:'public',discoverable:true,
    public_features:{topics:'community science',goals:'education science'}};
  const before=JSON.stringify(person),r=C.rankPublicCandidates(s.packet(),[person, {...person,id:'b'}]);
  assert.equal(JSON.stringify(person),before);
  assert.deepEqual(r.map(x=>x.id),['a','b']);
  assert.ok(r[0].reasons.length>=2);
  assert.ok(r[0].signal_coverage_percent>=60);
  assert.equal(r[0].uncalibrated,true);
});
test('editing or skipping previously shared answers revokes the old visibility grant',()=>{
  const s=complete({interests:'astronomy learning',goals:'teach astronomy'},['interests','goals'],true);
  assert.equal(s.packet().visibility.interests,'public');
  s.edit('interests');s.answer('Private family subject');
  assert.equal(s.packet().visibility.interests,'private');
  assert.deepEqual(C.discoveryFeatures(s.packet()).topics,[]);
  assert.equal(s.packet().visibility.goals,'public');
  s.edit('goals');s.skip();
  assert.equal(s.packet().answers.goals,'');
  assert.equal(s.packet().visibility.goals,'private');
  assert.deepEqual(C.discoveryFeatures(s.packet()).goals,[]);
});
test('mission vision and business enrich matches only with explicit field consent',()=>{
  const s=complete({mission:'community science',vision:'education astronomy',
    business:'science coaching',interests:'astronomy community'},['interests'],true);
  const a=C.discoveryFeatures(s.packet());
  assert.equal(a.goals.length,0);
  assert.equal(a.offers.length,0);
  for(const key of ['mission','vision','business'])assert.equal(s.setPublic(key,true),true);
  const b=C.discoveryFeatures(s.packet());
  assert.ok(b.goals.includes('science'));
  assert.ok(b.offers.includes('coaching'));
});
test('AI prompt is explicitly for editable draft, no user data and no fake generation',()=>{
  assert.match(C.aiPrompt('vision'),/Do not invent information/);
  assert.match(C.aiPrompt('vision'),/copy and paste/);
  assert.equal(C.aiPrompt('unknown'),'');
});
test('answer text control cleaning is bounded',()=>{
  assert.equal(C.clean('Hi\u0001 there'),'Hi there');
  assert.equal(C.clean('x'.repeat(2000)).length,1800);
});
test('UI supplies three methods and has no auto-publish network call',()=>{
  const html=readFileSync(new URL('../HUB/citizen-discovery-preview.html',import.meta.url),'utf8');
  for(const label of ['Speak','Type','Ask my AI','Preview my three worlds','private by default'])
    assert.ok(html.includes(label),label);
  assert.ok(!html.includes('fetch('));
  assert.ok(!html.includes('localStorage'));
});
