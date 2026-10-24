/* NayaNET Citizen Discovery + AutoMatch candidate prototype.
 * One post-Welcome extension, not a new identity/intake database.
 * NO network calls, NO automatic writes, connections, mail, joins or publish.
 * Source contracts: Citizen Trinity 2026-10-23, #1598, SN-0843.
 * Browser: window.NayaCitizenDiscovery; Node: module.exports.
 */
(function(root) {
  'use strict';
  const FIELDS = Object.freeze([
    {key:'about',question:'Tell Naya a little about yourself.',hint:'Your story, in your words.',section:'personal'},
    {key:'interests',question:'What are you into?',hint:'Interests, subjects, activities or ideas.',section:'personal'},
    {key:'mission',question:'What is your mission?',hint:'What matters enough to work toward?',section:'personal'},
    {key:'vision',question:'What is your vision?',hint:'What would a better future look like?',section:'personal'},
    {key:'goals',question:'What goals would you like help achieving?',hint:'Small steps or big ambitions are welcome.',section:'personal'},
    {key:'motto',question:'Do you have a motto?',hint:'A phrase you live by. Skip if you like.',section:'personal'},
    {key:'business',question:'Do you have a business, project or cause?',hint:'Optional. No business? Skip.',section:'business'},
    {key:'offer',question:'What do you offer or hope to contribute?',hint:'Skills, services, products or help.',section:'business'},
    {key:'space_topics',question:'What would your community Space be about?',hint:'People and topics you want to bring together.',section:'space'},
    {key:'looking_for',question:'Who or what would you like to connect with?',hint:'Interests, skills, projects or communities.',section:'space'}
  ]);
  const PUBLIC_DISCOVERY_FIELDS = new Set(['interests','goals','offer','space_topics','looking_for']);
  const MAX_ANSWER = 1800;
  const STOP = new Set(['and','the','with','for','are','but','that','this','you','your','our',
    'into','about','would','like','what','from','have','make','been','their','there','they',
    'some','more','want','people','things','doing','will','where','when','can','how']);
  function clean(value) {
    return typeof value === 'string' ? value.replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/g,'').trim().slice(0,MAX_ANSWER) : '';
  }
  function words(value) {
    const normalized = Array.isArray(value) ? value.join(' ') : value;
    return [...new Set((clean(String(normalized || '')).toLowerCase().normalize('NFKC')
      .match(/[\p{L}\p{N}]{3,}/gu) || []).filter(w => !STOP.has(w)))].slice(0,60);
  }
  function createSession(identity) {
    // Identity claims must be verified by the existing issuer at write time.
    // Strings here are display hints, never authentication proof.
    const actor = {alias:clean(identity && identity.alias), name:clean(identity && identity.name)};
    const answers = Object.create(null);
    const publicFields = Object.create(null);
    let index = 0;
    let review = false;
    let discoveryOptIn = false;
    function packet() {
      return {
        version:'citizen-discovery-v1', actor_hint:actor,
        answers:Object.fromEntries(FIELDS.map(f => [f.key, answers[f.key] || ''])),
        visibility:Object.fromEntries(FIELDS.map(f => [f.key,
          publicFields[f.key] === true && PUBLIC_DISCOVERY_FIELDS.has(f.key) ? 'public' : 'private'])),
        discovery_opt_in:discoveryOptIn, state:'DRAFT_ONLY',
        requires_issuer_authenticated_owner:true,
        requires_explicit_review_and_publish:true
      };
    }
    return {
      fields:FIELDS,
      state() {return {step:index,total:FIELDS.length,at_review:review,
        question:review ? null : FIELDS[index],answers:{...answers},
        visibility:{...publicFields},discovery_opt_in:discoveryOptIn};},
      answer(input) {if(review)return {ok:false,reason:'at_review'};
        const v=clean(input);
        if(typeof input !== 'string')return {ok:false,reason:'invalid_input'};
        answers[FIELDS[index].key]=v;
        return this.next();},
      skip(){if(review)return {ok:false,reason:'at_review'};return this.next();},
      next(){if(index === FIELDS.length-1){review=true;}else index++;
        return {ok:true,at_review:review};},
      back(){if(review){review=false;index=FIELDS.length-1;return true;}
        if(index===0)return false;index--;return true;},
      edit(key){const i=FIELDS.findIndex(f=>f.key===key);if(i<0)return false;
        index=i;review=false;return true;},
      setPublic(key,flag){if(!PUBLIC_DISCOVERY_FIELDS.has(key))return false;
        publicFields[key]=flag === true;return true;},
      setDiscoveryOptIn(flag){discoveryOptIn=flag===true;},
      packet(){return packet();},
      preview(){return makeDrafts(packet());}
    };
  }
  function makeDrafts(packet) {
    if(!packet || packet.state!=='DRAFT_ONLY' || !packet.answers)throw Error('draft_packet_required');
    const a=packet.answers;
    return {
      state:'UNPUBLISHED_PREVIEW',requires_authenticated_save:true,
      personal:{name:packet.actor_hint?.name||'',about:clean(a.about),interests:clean(a.interests),
        mission:clean(a.mission),vision:clean(a.vision),goals:clean(a.goals),motto:clean(a.motto)},
      business:{applicable:!!(clean(a.business)||clean(a.offer)),
        business:clean(a.business),offer:clean(a.offer)},
      space:{applicable:!!(clean(a.space_topics)||clean(a.looking_for)),
        topics:clean(a.space_topics),looking_for:clean(a.looking_for)},
      visibility:packet.visibility,discovery_opt_in:packet.discovery_opt_in,
      note:'Preview only. No account, Space, message, connection or page has been created.'
    };
  }
  function discoveryFeatures(packet) {
    if(!packet || packet.state!=='DRAFT_ONLY' || packet.discovery_opt_in!==true)return null;
    const a=packet.answers||{},visibility=packet.visibility||{};
    const take=(key)=>visibility[key]==='public' && PUBLIC_DISCOVERY_FIELDS.has(key)
      ? words(a[key]) : [];
    return {topics:[...new Set([...take('interests'),...take('space_topics')])],
      goals:take('goals'),offers:take('offer'),seeks:take('looking_for')};
  }
  function overlap(a,b) {
    if(!a.length || !b.length)return null;
    const x=new Set(a),y=new Set(b);
    const common=[...x].filter(k=>y.has(k));
    return {ratio:common.length / new Set([...x,...y]).size,shared:common};
  }
  const WEIGHTS=Object.freeze({topics:40,goals:25,offers:20,seeks:15});
  function rankPublicCandidates(packet,candidates,opts) {
    opts=opts||{};
    const user=discoveryFeatures(packet);
    if(!user)return [];
    const blocked=new Set(Array.isArray(opts.blocked_ids)?opts.blocked_ids:[]);
    const self=packet.actor_hint&&packet.actor_hint.alias;
    const results=[];
    for(const item of Array.isArray(candidates)?candidates:[]) {
      if(!item || typeof item.id!=='string' || !item.id || item.visibility!=='public'
        || item.discoverable!==true || item.opted_out===true
        || blocked.has(item.id) || (self && item.alias===self))continue;
      const publicData=item.public_features||{};
      let scored=0,available=0,independent=0;
      const reasons=[];
      for(const [key,weight] of Object.entries(WEIGHTS)){
        const v=overlap(user[key],words(publicData[key]));
        if(!v)continue;
        available+=weight;
        scored+=v.ratio*weight;
        if(v.shared.length){independent++;reasons.push({signal:key,shared:v.shared.slice(0,4)});}
      }
      // Single coincidental word is insufficient to advertise a match.
      if(available<60 || independent<2)continue;
      results.push({id:item.id,kind:item.kind||'public_item',
        estimated_relevance_percent:Math.round(scored/available*100),
        signal_coverage_percent:available,uncalibrated:true,reasons,
        explanation:'Experimental topic/goal relevance, not a compatibility or value judgment.',
        authorized_action:'SUGGEST_ONLY'});
    }
    return results.sort((a,b)=>b.estimated_relevance_percent-a.estimated_relevance_percent
      || a.id.localeCompare(b.id));
  }
  function aiPrompt(question) {
    const q=typeof question==='string'?FIELDS.find(f=>f.key===question):question;
    if(!q || !FIELDS.includes(q))return '';
    return 'Help me write a short, authentic first-person answer to this NayaNET question: '
      +q.question+' Ask me for the details you need. Do not invent information or publish anything. '
      +'Give me editable text to copy and paste into my private draft.';
  }
  const api={FIELDS,PUBLIC_DISCOVERY_FIELDS,clean,words,createSession,makeDrafts,
    discoveryFeatures,rankPublicCandidates,aiPrompt};
  if(typeof module!=='undefined'&&module.exports)module.exports=api;
  root.NayaCitizenDiscovery=api;
})(typeof window!=='undefined'?window:globalThis);
