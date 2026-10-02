/* LEDGER ADAPTER — receipt artifacts → ledger entry view-models.
 *
 * Sources of truth: decision receipts ({decision_receipt, input_state}) and
 * execution receipts (flat ACT receipts). Production: nayanet_smart_ledger /
 * nayanet_execution_receipts. This adapter never invents entries; unparseable
 * input yields null and is skipped.
 *
 *   const entries = LedgerAdapter.parseMany([obj1, obj2, ...]);
 *   // -> [{kind:'decision'|'execution', id, verdict, issuedAt, proofState,
 *   //      nodes:[{node,status}], edges:[{source,target,type,status}],
 *   //      hashes:{receipt,inputs}, authorityBasis, effectsObserved,
 *   //      durationMs, decisionRef, calculusVersion}]
 */
(function(){
  'use strict';

  function proofStateOf(obj, dr){
    var banner = (dr && dr.candidate_banner) || obj.candidate_banner || '';
    if(/NOT RATIFIED/.test(banner)) return 'CANDIDATE';
    if(/RATIFIED/.test(banner)) return 'RATIFIED';
    return 'RECORDED';
  }

  function parseDecision(obj){
    var dr = obj.decision_receipt || obj;
    if(!dr || !dr.decision_id) return null;
    var gates = {};
    (dr.gates||[]).forEach(function(g){ gates[g.node]=g; });
    var nodes = (dr.evaluation_order||[]).map(function(n){
      var g = gates[n]||{};
      var st = 'EVALUATED';
      if(g.evaluated===false) st='NOT RUN';
      else if(dr.first_non_pass_at===n) st='NON-PASS';
      else if(g.evaluated) st='PASS';
      return {node:n, status:st};
    });
    var edges = (dr.edge_trace||[]).map(function(e){
      return {source:e.source||'', target:e.target||'', type:e.type||'', status:e.status||''};
    });
    return {
      kind:'decision',
      id: dr.decision_id || dr.receipt_id || 'UNKNOWN',
      verdict: dr.verdict || 'UNKNOWN',
      issuedAt: dr.issued_at || '',
      proofState: proofStateOf(obj, dr),
      banner: dr.candidate_banner || '',
      nodes: nodes,
      edges: edges,
      hashes: { receipt:(dr.receipt_hash||'').slice(0,16), inputs:(dr.inputs_hash||'').slice(0,16),
                receiptFull:dr.receipt_hash||'', inputsFull:dr.inputs_hash||'' },
      kernel: dr.kernel_version || '',
      graphSeed: dr.graph_seed || ''
    };
  }

  function parseExecution(obj){
    if(!obj || (!obj.decision_ref && !obj.receipt_id)) return null;
    var ab = obj.authority_basis || {};
    return {
      kind:'execution',
      id: obj.receipt_id || obj.decision_ref || 'UNKNOWN',
      decisionRef: obj.decision_ref || '',
      verdict: obj.verdict || (obj.effects_observed ? 'EFFECTS OBSERVED' : 'UNKNOWN'),
      issuedAt: obj.issued_at || obj.executed_at || '',
      proofState: proofStateOf(obj, null),
      banner: obj.candidate_banner || '',
      authorityBasis: (ab.kind||'') + (ab.ref ? ' · ' + ab.ref : ''),
      effectsObserved: obj.effects_observed || '',
      durationMs: (obj.duration_ms!=null ? obj.duration_ms : ''),
      calculusVersion: obj.calculusVersion || '',
      attempts: obj.attempts || 1,
      nodes: [], edges: [], hashes:{}
    };
  }

  function parseOne(obj){
    if(!obj || typeof obj!=='object') return null;
    if(obj.decision_receipt || obj.decision_id) return parseDecision(obj);
    return parseExecution(obj);
  }

  function parseMany(list){
    var out=[];
    (list||[]).forEach(function(o){
      try{ var e=parseOne(o); if(e) out.push(e); }catch(err){ /* skip unparseable */ }
    });
    /* newest first by issuedAt */
    out.sort(function(a,b){ return String(b.issuedAt||'').localeCompare(String(a.issuedAt||'')); });
    return out;
  }

  window.LedgerAdapter = { parseOne:parseOne, parseMany:parseMany };
})();
