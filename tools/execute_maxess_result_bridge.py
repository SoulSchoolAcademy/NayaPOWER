from pathlib import Path
import re

ASSESSMENT = Path('AIScoreMAXESS code')
MARKER = '/* MAXESS_RESULT_BRIDGE_V1 */'

BRIDGE = r'''
/* MAXESS_RESULT_BRIDGE_V1 */
(function(){
  'use strict';

  const RESULT_KEY = 'MAXESS_RESULT_V1';
  const RESULT_EVENT = 'MAXESS_RESULT_READY';
  const RESULTS_URL = 'https://results.nayanet.app/';

  function finite(value){
    const n = Number(value);
    return Number.isFinite(n) ? n : null;
  }

  function clampScore(value){
    const n = finite(value);
    return n === null ? null : Math.max(0, Math.min(100, n));
  }

  function safeJson(value){
    try { return JSON.stringify(value); } catch(e) { return null; }
  }

  function persist(contract){
    const json = safeJson(contract);
    if(!json) return false;
    try { sessionStorage.setItem(RESULT_KEY, json); } catch(e) {}
    try { localStorage.setItem(RESULT_KEY, json); } catch(e) {}
    return true;
  }

  function encodeContract(contract){
    const json = safeJson(contract);
    if(!json) return null;
    const bytes = new TextEncoder().encode(json);
    let binary = '';
    bytes.forEach(byte => binary += String.fromCharCode(byte));
    return btoa(binary).replace(/\+/g,'-').replace(/\//g,'_').replace(/=+$/,'');
  }

  function dimensionLevel(score){
    if(score >= 90) return 'MASTERING';
    if(score >= 75) return 'ADVANCING';
    if(score >= 60) return 'DEVELOPING';
    return 'EMERGING';
  }

  function buildContract(){
    const questions = Array.isArray(MAXESS_ASSESSMENT.questions)
      ? [...MAXESS_ASSESSMENT.questions].sort((a,b)=>a.order-b.order) : [];
    const responses = Array.isArray(state.responses) ? state.responses.slice() : [];
    if(questions.length !== 15 || responses.length !== 15) return null;

    const dimensions = (MAXESS_ASSESSMENT.dimensions || []).map(dimension => {
      const relevant = responses.filter(r => r.dimensionId === dimension.id);
      if(relevant.length !== 3) return null;
      const raw = relevant.reduce((sum,r)=>sum + Number(r.score || 0),0);
      // Authoritative MAXESS response scores are 0–4. Normalize each
      // three-question dimension to the canonical 0–100 scale.
      const score = Math.round((raw / 12) * 100 * 10) / 10;
      return { id:dimension.id, name:dimension.name, color:dimension.color, weight:dimension.weight, score, level:dimensionLevel(score) };
    }).filter(Boolean);
    if(dimensions.length !== 5) return null;

    const weightTotal = dimensions.reduce((sum,d)=>sum + Number(d.weight || 0),0);
    if(!weightTotal) return null;
    const overallScore = Math.round((dimensions.reduce((sum,d)=>sum + d.score * Number(d.weight || 0),0) / weightTotal) * 10) / 10;
    const band = (MAXESS_ASSESSMENT.scoreBands || []).find(item => overallScore >= item.min && overallScore <= item.max);
    if(!band) return null;

    const strongest = [...dimensions].sort((a,b)=>b.score-a.score)[0];
    const opportunity = [...dimensions].sort((a,b)=>a.score-b.score)[0];
    const selectedInterests = Array.from(state.selectedInterests || []);
    const interestMeta = (typeof AI_AREAS !== 'undefined' ? AI_AREAS : []).filter(area => selectedInterests.includes(area.id));

    return {
      contractVersion:'MAXESS_RESULT_V1', assessmentId:MAXESS_ASSESSMENT.id, assessmentVersion:MAXESS_ASSESSMENT.version,
      completedAt:state.completedAt || new Date().toISOString(), overallScore, masteryStage:band.label, masteryBand:band,
      fiveDimensions:dimensions, dimensions,
      strongestCapability:{id:strongest.id,name:strongest.name,score:strongest.score},
      highestLeverageOpportunity:{id:opportunity.id,name:opportunity.name,score:opportunity.score},
      overallPattern:dimensions.map(d=>({id:d.id,name:d.name,score:d.score,level:d.level})),
      personalizedInterpretation:{strongestCapability:strongest.name,strongestScore:strongest.score,highestLeverageOpportunity:opportunity.name,opportunityScore:opportunity.score,masteryStage:band.label,summary:band.description},
      nextMove:{primary:`Strengthen ${opportunity.name}`,reason:`Your highest-leverage opportunity is ${opportunity.name}.`},
      responses, selectedInterests, selectedInterestMeta:interestMeta,
      naya:{name:'Naya',image:'https://i.postimg.cc/bw4fyKF8/Naya-Profile-black-face-zoom.jpg'}
    };
  }

  function validateContract(contract){
    if(!contract || contract.contractVersion !== 'MAXESS_RESULT_V1') return false;
    if(clampScore(contract.overallScore) === null) return false;
    if(!Array.isArray(contract.dimensions) || contract.dimensions.length !== 5) return false;
    if(!Array.isArray(contract.responses) || contract.responses.length !== 15) return false;
    if(contract.dimensions.some(d => clampScore(d.score) === null)) return false;
    return true;
  }

  function publish(){
    const contract = buildContract();
    if(!validateContract(contract)){ console.error('MAXESS_RESULT bridge refused to publish invalid result.'); return false; }
    window.MAXESS_RESULT = contract;
    persist(contract);
    window.dispatchEvent(new CustomEvent(RESULT_EVENT,{detail:contract}));
    window.dispatchEvent(new CustomEvent('maxess:result-updated',{detail:contract}));
    const encoded = encodeContract(contract);
    if(!encoded) return false;
    window.location.assign(`${RESULTS_URL}#maxess-result=${encoded}`);
    return true;
  }

  function ensureNayaFields(){
    MAXESS_ASSESSMENT.questions.forEach(question=>{
      if(!Object.prototype.hasOwnProperty.call(question,'nayaScript')) question.nayaScript=question.teaching || '';
      if(!Object.prototype.hasOwnProperty.call(question,'nayaAudio')) question.nayaAudio=null;
    });
  }

  window.MAXESS_RESULT_BRIDGE={buildContract,validateContract,publish,ensureNayaFields};
  ensureNayaFields();
  window.finishInterestSelection=function(){ publish(); };
  const oldResults=document.getElementById('resultsView');
  if(oldResults){ oldResults.setAttribute('data-retired-renderer','true'); oldResults.style.display='none'; }
})();
'''

s = ASSESSMENT.read_text(encoding='utf-8')
if MARKER not in s:
    idx = s.rfind('</script>')
    if idx < 0:
        raise SystemExit('No closing script tag found in assessment source')
    s = s[:idx] + '\n' + BRIDGE + '\n' + s[idx:]

pattern = re.compile(r'function finishInterestSelection\(\)\{.*?\n\}', re.S)
replacement = '''function finishInterestSelection(){

  if(window.MAXESS_RESULT_BRIDGE && typeof window.MAXESS_RESULT_BRIDGE.publish === "function"){
    window.MAXESS_RESULT_BRIDGE.publish();
    return;
  }

  throw new Error("MAXESS_RESULT_BRIDGE unavailable; refusing legacy Results renderer.");

}'''
s, count = pattern.subn(replacement, s, count=1)
if count != 1:
    raise SystemExit(f'Expected exactly one finishInterestSelection function, found {count}')

ASSESSMENT.write_text(s, encoding='utf-8')
print('MAXESS_RESULT bridge applied successfully.')