/* ROOM CONTRACT ADAPTER - runtime projection of the canonical machine room contract.
   Canonical identity/route/theme/job/composition comes from HUB/NAYANET-SMART-APP-ROOMS-V1.json.
   This adapter adds UI consumption metadata; it is not a second room registry or truth store. */
(function(){
  'use strict';
  const SOURCE='../NAYANET-SMART-APP-ROOMS-V1.json';
  const STATE_MODEL=['loading','empty','ready','blocked','unauthorized','not_verified','verified','error','offline','disabled','unknown'];
  const BASE={
    state_model:STATE_MODEL,
    loading_state:'loading',
    empty_state:'empty',
    unavailable_state:'not_verified',
    blocked_unauthorized_state:['blocked','unauthorized'],
    error_recovery_state:'error',
    authority_requirements:'runtime-governed; capability never implies authority',
    evidence_provenance_surface:'canonical object provenance + runtime receipt/evidence when returned',
    responsive_behavior:'shared Hub shell; no horizontal overflow; one mobile navigation surface',
    accessibility_requirements:'keyboard operable; visible focus; semantic controls; reduced-motion safe',
    continuity_behavior:'route + canonical object identity + context survive room navigation where applicable',
    proof_requirements:['runtime truth','failure states','browser render','keyboard/mobile','cross-room identity','independent review']
  };
  const SPECS=[
    {id:'feed',name:'Smart Feed',kicker:'STREAM',accent:'var(--accent-feed)',icon:'feed',
      human_purpose:'Distill the most important intelligence now.',human_question_answered:'What matters now, why, and what can I do?',
      canonical_intelligence_object_types:['Intelligent Block','Event','Learning','Decision'],source_of_truth:'NayaPOWER governed runtime',
      dependencies:['runtime_adapter','canonical_object_identity','evidence'],allowed_actions:['open','retrieve evidence','ask Naya','governed action'],
      primary_intelligence_query:'smartFeed by active Collective/Personal/Activity context',contextual_naya_contribution:'Explain the selected canonical object and next useful action.',
      semantic_color:'semantic per intelligence object; shell neutral',design_object_composition:['Intelligence Surface','Intelligence Icon','Power Object']},
    {id:'today',name:'Your Intelligence Today',kicker:'TODAY',accent:'var(--accent-today)',icon:'spark',
      human_purpose:'Distill the day into changes, learning, priorities, gaps, and next action.',human_question_answered:'What happened, changed, matters, or needs me today?',
      canonical_intelligence_object_types:['Intelligent Block','Event','Learning'],source_of_truth:'NayaPOWER governed runtime',
      dependencies:['runtime_adapter','canonical_object_identity'],allowed_actions:['inspect','ask Naya'],primary_intelligence_query:'dailyIntelligence for current identity/context',
      contextual_naya_contribution:'Explain daily significance without inventing missing evidence.',semantic_color:'var(--accent-today)',design_object_composition:['Intelligence Surface','Intelligence Icon']},
    {id:'reports',name:'Your Reports',kicker:'REPORTS',accent:'var(--accent-reports)',icon:'report',
      human_purpose:'Show evidence-grounded synthesis over time.',human_question_answered:'What does the evidence show across day, week, month, or year?',
      canonical_intelligence_object_types:['Report','Intelligent Block','Receipt'],source_of_truth:'NayaPOWER governed runtime',dependencies:['runtime_adapter','evidence'],
      allowed_actions:['change period','inspect evidence'],primary_intelligence_query:'intelligenceReports by period/context',contextual_naya_contribution:'Explain report meaning and evidence boundaries.',
      semantic_color:'var(--accent-reports)',design_object_composition:['Intelligence Surface','Energy Path']},
    {id:'library',name:'Intelligent Library',kicker:'LIBRARY',accent:'var(--accent-library)',icon:'library',
      human_purpose:'Retrieve retained intelligence by meaning.',human_question_answered:'What do we already know about this?',
      canonical_intelligence_object_types:['Intelligent Block','Knowledge','Learning'],source_of_truth:'NayaPOWER governed runtime',dependencies:['runtime_adapter','canonical_object_identity'],
      allowed_actions:['search','open','inspect evidence'],primary_intelligence_query:'semantic library retrieval',contextual_naya_contribution:'Help interpret retrieved canonical intelligence.',
      semantic_color:'var(--accent-library)',design_object_composition:['Identity Portal','Intelligence Surface']},
    {id:'connect',name:'Smart Connect',kicker:'CONNECT',accent:'var(--accent-connect)',icon:'connect',
      human_purpose:'Project governed doors into the intelligence network.',human_question_answered:'What can connect, under what authority, and what is live?',
      canonical_intelligence_object_types:['Smart Door','Authority','Capability'],source_of_truth:'canonical Smart Door registry + governed runtime',dependencies:['door_registry','authority'],
      allowed_actions:['inspect door','request governed connection'],primary_intelligence_query:'canonical door registry projection',contextual_naya_contribution:'Explain connection state and authority boundary.',
      semantic_color:'connection semantic',design_object_composition:['Intelligence Surface','Power Object','Intelligence Icon']},
    {id:'ledger',name:'Smart Ledger',kicker:'ACCOUNTABILITY',accent:'var(--accent-ledger)',icon:'ledger',
      human_purpose:'Expose consequential actions, receipts, outcomes, and verification.',human_question_answered:'What happened, what changed, and where is the proof?',
      canonical_intelligence_object_types:['Receipt','Outcome','Verification'],source_of_truth:'NayaPOWER governed runtime',dependencies:['runtime_adapter','evidence'],
      allowed_actions:['inspect receipt','inspect outcome'],primary_intelligence_query:'executionLedger by identity/context',contextual_naya_contribution:'Explain causal action → outcome → proof chain.',
      semantic_color:'var(--accent-ledger)',design_object_composition:['Intelligence Surface','Energy Path']},
    {id:'connections',name:'Your Connections',kicker:'CONNECTIONS',accent:'var(--accent-connections)',icon:'nodes',
      human_purpose:'Show governed human/AI/machine relationships.',human_question_answered:'Who or what is connected, with what consent and scope?',
      canonical_intelligence_object_types:['Relationship','Consent','Identity'],source_of_truth:'NayaPOWER governed runtime',dependencies:['runtime_adapter','authority'],
      allowed_actions:['inspect relationship','revoke/request where authorized'],primary_intelligence_query:'relationshipIntelligence by identity/context',contextual_naya_contribution:'Explain relationship provenance and consent.',
      semantic_color:'var(--accent-connections)',design_object_composition:['Intelligence Surface','Intelligence Icon']},
    {id:'lists',name:'Smart Lists',kicker:'LISTS',accent:'var(--accent-lists)',icon:'lists',
      human_purpose:'Project living canonical references into useful lists.',human_question_answered:'What belongs together for this goal or rule?',
      canonical_intelligence_object_types:['Canonical Reference','List'],source_of_truth:'NayaPOWER governed runtime',dependencies:['runtime_adapter','canonical_object_identity'],
      allowed_actions:['open reference','change view'],primary_intelligence_query:'intelligenceLists by context',contextual_naya_contribution:'Explain why an item belongs and what changed.',
      semantic_color:'var(--accent-lists)',design_object_composition:['Intelligence Surface','Power Object']},
    {id:'mail',name:'Smart Mail',kicker:'MAIL',accent:'var(--accent-mail)',icon:'mail',
      human_purpose:'Project governed message intelligence without silently acting.',human_question_answered:'What communication matters, why, and what am I allowed to do?',
      canonical_intelligence_object_types:['Message','Thread','Intent'],source_of_truth:'governed mail/runtime connector',dependencies:['runtime_adapter','authority'],
      allowed_actions:['inspect','draft/request send when authorized'],primary_intelligence_query:'smartMail by identity/context',contextual_naya_contribution:'Summarize message meaning and authority-safe next action.',
      semantic_color:'var(--accent-mail)',design_object_composition:['Intelligence Surface','Power Object']},
    {id:'spaces',name:'Smart Spaces',kicker:'SPACES',accent:'var(--accent-spaces)',icon:'spaces',
      human_purpose:'Project intelligence inside an explicit project/person/idea context.',human_question_answered:'What matters inside this space and how does context change the view?',
      canonical_intelligence_object_types:['Space','Context','Intelligent Block'],source_of_truth:'NayaPOWER governed runtime',dependencies:['runtime_adapter','canonical_object_identity','authority'],
      allowed_actions:['enter space','inspect intelligence'],primary_intelligence_query:'smartSpaces and scoped intelligence by space id',contextual_naya_contribution:'Reason only within the active governed space context.',
      semantic_color:'var(--accent-spaces)',design_object_composition:['Intelligence Surface','Intelligence Icon']},
    {id:'settings',name:'Settings',kicker:'SETTINGS',accent:'var(--accent-settings)',icon:'gear',
      human_purpose:'Expose identity, privacy, preferences, connections, and system health.',human_question_answered:'What governs my Hub and what is its current health?',
      canonical_intelligence_object_types:['Identity','Permission','Preference','Runtime Health'],source_of_truth:'governed runtime; local UI preferences explicitly local-only',
      dependencies:['runtime_adapter','identity','authority'],allowed_actions:['inspect health','change supported preference'],primary_intelligence_query:'settingsSnapshot/runtimeSnapshot',
      contextual_naya_contribution:'Explain settings consequences before change.',semantic_color:'var(--accent-settings)',design_object_composition:['Identity Portal','Power Object','Intelligence Surface']}
  ];
  function appRoute(id){return '/hub/'+id;}
  let contracts=[];
  let byId=Object.freeze({});
  let sourceMeta=Object.freeze({state:'not_loaded',path:SOURCE});

  function validate(contract){
    const required=['id','route','human_purpose','human_question_answered','canonical_intelligence_object_types','source_of_truth','dependencies','allowed_actions',
      'authority_requirements','primary_intelligence_query','state_model','loading_state','empty_state','unavailable_state','blocked_unauthorized_state',
      'error_recovery_state','evidence_provenance_surface','contextual_naya_contribution','semantic_color','design_object_composition','responsive_behavior',
      'accessibility_requirements','continuity_behavior','proof_requirements'];
    const missing=required.filter(key=>contract?.[key]===undefined||contract?.[key]===null||contract?.[key]==='');
    return {ok:missing.length===0,missing};
  }

  async function load(){
    if(contracts.length) return contracts;
    const res=await fetch(SOURCE,{cache:'no-store'});
    if(!res.ok) throw new Error('Canonical room contract unavailable: HTTP '+res.status);
    const canonical=await res.json();
    if(canonical?.schema!=='nayanet.smart-app.rooms.v1') throw new Error('Unexpected canonical room schema: '+String(canonical?.schema||'missing'));
    const canonicalRooms=Array.isArray(canonical.rooms)?canonical.rooms:[];
    const detailById=Object.fromEntries(SPECS.map(spec=>[spec.id,spec]));
    const canonicalIds=canonicalRooms.map(room=>room.id);
    const detailIds=SPECS.map(spec=>spec.id);
    if(JSON.stringify(canonicalIds)!==JSON.stringify(detailIds)){
      throw new Error('Canonical room identity/order differs from the Hub adapter. canonical='+JSON.stringify(canonicalIds)+' adapter='+JSON.stringify(detailIds));
    }
    const canonicalStates=(canonical.states||[]).map(state=>String(state).toLowerCase());
    if(JSON.stringify(canonicalStates)!==JSON.stringify(STATE_MODEL)){
      throw new Error('Canonical room state model differs from the Hub adapter.');
    }

    contracts=canonicalRooms.map(canon=>{
      const spec=detailById[canon.id];
      return Object.freeze({...BASE,...spec,
        id:canon.id,
        name:canon.name,
        route:canon.route,
        canonical_route:canon.route,
        app_route:appRoute(canon.id),
        canonical_theme:canon.theme,
        canonical_job:canon.job,
        primary_action:canon.primary,
        canonical_composition:Object.freeze([...(canon.composition||[])]),
        canonical_source:'HUB/NAYANET-SMART-APP-ROOMS-V1.json@'+String(canonical.version||'unknown')
      });
    });
    const invalid=contracts.map(c=>({id:c.id,...validate(c)})).filter(x=>!x.ok);
    if(invalid.length) throw new Error('Invalid NayaNET room contract adapter: '+JSON.stringify(invalid));
    contracts=Object.freeze(contracts);
    byId=Object.freeze(Object.fromEntries(contracts.map(c=>[c.id,c])));
    sourceMeta=Object.freeze({
      state:'ready',
      path:SOURCE,
      schema:canonical.schema,
      version:canonical.version,
      status:canonical.status,
      runtime_truth:canonical.runtime_truth,
      shell:canonical.shell||null,
      hub_home:canonical.hub_home||null
    });
    return contracts;
  }

  window.NayaRoomContract=Object.freeze({
    schema:'nayanet.hub.room-contract-adapter.v1',
    version:'1.1.0',
    states:Object.freeze([...STATE_MODEL]),
    source:()=>sourceMeta,
    load,
    list:()=>contracts,
    get:id=>byId[id]||null,
    validate
  });
})();
