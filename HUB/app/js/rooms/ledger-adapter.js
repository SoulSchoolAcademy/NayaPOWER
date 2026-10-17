/* LEDGER ADAPTER v2 — receipt artifacts -> ledger entry view-models.
 *
 * Sources of truth: decision receipts ({decision_receipt, input_state}) and
 * execution receipts (flat ACT receipts). Production: nayanet_smart_ledger /
 * nayanet_execution_receipts. This adapter never invents entries; unparseable
 * input yields null and is skipped.
 *
 * Entry shape (v2):
 *   {kind, id, smartName, glyph, outcome, issuedAt, proofState, banner,
 *    scores:{q, deltaV, confidence, vPred, vActual},
 *    nodes:[{node,status}], edges:[{source,target,type,status}],
 *    hashes:{receipt,inputs}, hash, authorityBasis, effectsObserved,
 *    durationMs, decisionRef, calculusVersion, kernel, demo, raw}
 *
 * Smart names: deterministic friendly labels derived from the entry hash
 * ("Amber Falcon") — the beautiful face of a cryptographic id. The hash
 * behind it is always one click away.
 *
 * demoStream(): a seeded, deterministic DEMO stream for design review and
 * system testing. Clearly labeled demo:true on every entry. The live stream
 * replaces it at launch; the room renders either through the same views.
 */
(function(){
  'use strict';

  var ADJ = ('Amber Quiet Iron Velvet Solar Crimson Silent Golden Rapid Still Bright Hollow '
    + 'Lucid Marble Neon Onyx Pale Quick Rustic Silver Tawny Umber Vivid Woven Xenon '
    + 'Yielding Zephyr Ashen Bold Clear Distant Ember').split(' ');
  var NOUN = ('Falcon Harbor Signal Anchor Beacon Cipher Delta Ember Field Grove Horizon Iris '
    + 'Junction Keystone Lantern Meridian Nexus Orbit Prism Quill Relay Summit Tether Union '
    + 'Vector Wharf Yield Zephyr Atlas Bridge Compass Drift').split(' ');

  function smartNameFor(hash){
    var h = String(hash||'').replace(/[^0-9a-f]/gi,'');
    if(h.length < 4) h = (h + '0000').slice(0,4);
    var b0 = parseInt(h.slice(0,2),16), b1 = parseInt(h.slice(2,4),16);
    return ADJ[b0 % ADJ.length] + ' ' + NOUN[b1 % NOUN.length];
  }

  function mulberry32(a){
    return function(){
      a |= 0; a = a + 0x6D2B79F5 | 0;
      var t = Math.imul(a ^ a >>> 15, 1 | a);
      t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
  }

  function hexN(rnd, n){
    var s = '';
    for(var i=0;i<n;i++) s += '0123456789abcdef'[Math.floor(rnd()*16)];
    return s;
  }

  var GLYPH = {decision:'\u25C6', execution:'\u25CF', contribution:'\u25B2', signal:'\u25CB'};

  function normalize(e){
    e = e || {};
    e.scores = e.scores || {};
    e.nodes = e.nodes || []; e.edges = e.edges || []; e.hashes = e.hashes || {};
    e.hash = e.hash || e.hashes.receiptFull || e.hashes.receipt || '';
    e.smartName = e.smartName || smartNameFor(e.hash || e.id);
    e.glyph = GLYPH[e.kind] || '\u25C6';
    e.raw = e.raw || e;
    return e;
  }

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
    return normalize({
      kind:'decision',
      id: dr.decision_id || dr.receipt_id || 'UNKNOWN',
      outcome: dr.verdict || 'UNKNOWN',
      issuedAt: dr.issued_at || '',
      proofState: proofStateOf(obj, dr),
      banner: dr.candidate_banner || '',
      nodes: nodes, edges: edges,
      hashes: { receipt:(dr.receipt_hash||'').slice(0,16), inputs:(dr.inputs_hash||'').slice(0,16),
                receiptFull:dr.receipt_hash||'', inputsFull:dr.inputs_hash||'' },
      kernel: dr.kernel_version || '',
      raw: obj
    });
  }

  function parseExecution(obj){
    if(!obj || (!obj.decision_ref && !obj.receipt_id)) return null;
    var ab = obj.authority_basis || {};
    return normalize({
      kind:'execution',
      id: obj.receipt_id || obj.decision_ref || 'UNKNOWN',
      decisionRef: obj.decision_ref || '',
      outcome: obj.verdict || (obj.effects_observed ? 'EFFECTS OBSERVED' : 'UNKNOWN'),
      issuedAt: obj.issued_at || obj.executed_at || '',
      proofState: proofStateOf(obj, null),
      banner: obj.candidate_banner || '',
      authorityBasis: (ab.kind||'') + (ab.ref ? ' \u00B7 ' + ab.ref : ''),
      effectsObserved: obj.effects_observed || '',
      durationMs: (obj.duration_ms!=null ? obj.duration_ms : ''),
      calculusVersion: obj.calculusVersion || '',
      raw: obj
    });
  }

  function parseOne(obj){
    if(!obj || typeof obj!=='object') return null;
    if(obj.decision_receipt || obj.decision_id) return parseDecision(obj);
    return parseExecution(obj);
  }

  function parseMany(list){
    var out=[];
    (list||[]).forEach(function(o){
      try{ var e=parseOne(o); if(e) out.push(e); }catch(err){}
    });
    out.sort(function(a,b){ return String(b.issuedAt||'').localeCompare(String(a.issuedAt||'')); });
    return out;
  }

  /* ---------------- DEMO STREAM (seeded, deterministic) ---------------- */

  var NODES9 = ['SELF','LAW','KNOW','ACT','PROVE','CONNECT','VERIFY','LEARN','EVOLVE'];

  function demoStream(){
    var rnd = mulberry32(20261002);
    var now = Date.now();
    /* [kind, outcome, q, deltaV, proofState, label] */
    var plan = [
      ['decision','ACT',9.6,7.2,'VERIFIED'],
      ['execution','EFFECTS OBSERVED',null,null,'VERIFIED'],
      ['contribution','VALUED',null,2.1,'RECORDED','Morning report valued'],
      ['decision','ACT',9.2,4.8,'VERIFIED'],
      ['signal','RECORDED',null,1.4,'RECORDED','Smart board published'],
      ['decision','READ_MORE',8.4,2.2,'CANDIDATE'],
      ['execution','EFFECTS OBSERVED',null,null,'VERIFIED'],
      ['contribution','VALUED',null,0.8,'RECORDED','Share valued'],
      ['decision','ASK',8.9,5.1,'IMPLEMENTED'],
      ['decision','ACT',9.8,8.7,'PRODUCTION-PROVEN'],
      ['execution','EFFECTS OBSERVED',null,null,'VERIFIED'],
      ['contribution','VALUED',null,0.3,'RECORDED','Like valued'],
      ['decision','REFUSE',6.1,-1.2,'IMPLEMENTED'],
      ['signal','RECORDED',null,0.0,'RECORDED','Nightly checkpoint'],
      ['decision','ACT',9.1,3.9,'VERIFIED'],
      ['execution','EFFECTS OBSERVED',null,null,'VERIFIED'],
      ['contribution','VALUED',null,1.1,'RECORDED','Note valued'],
      ['decision','READ_MORE',7.8,1.9,'CANDIDATE'],
      ['decision','ACT',9.4,6.3,'VERIFIED'],
      ['execution','EFFECTS OBSERVED',null,null,'VERIFIED'],
      ['signal','RECORDED',null,0.9,'RECORDED','Weekly rollup'],
      ['decision','ASK',8.2,3.3,'IMPLEMENTED'],
      ['contribution','VALUED',null,2.6,'RECORDED','Report valued'],
      ['decision','ACT',9.7,5.5,'VERIFIED'],
      ['execution','EFFECTS OBSERVED',null,null,'VERIFIED'],
      ['decision','ACT',8.8,-2.4,'VERIFIED'],
      ['execution','EFFECTS OBSERVED',null,null,'VERIFIED'],
      ['contribution','VALUED',null,1.7,'RECORDED','Share valued']
    ];
    var entries = [];
    var lastDec = null;
    plan.forEach(function(p, i){
      var kind=p[0], outcome=p[1], q=p[2], dv=p[3], proof=p[4], label=p[5]||'';
      var t = new Date(now - rnd()*36*3600*1000).toISOString();
      var hash = hexN(rnd, 64);
      var id = 'demo-20261002-' + String(i+1).padStart(3,'0');
      var e = { kind:kind, id:id, demo:true, issuedAt:t, proofState:proof,
                hash:hash, hashes:{receipt:hash.slice(0,16), receiptFull:hash},
                scores:{}, raw:{demo:true, id:id} };
      if(kind==='decision'){
        e.outcome = outcome;
        e.scores = { q:q, deltaV:dv, confidence:+(0.6+rnd()*0.39).toFixed(2) };
        if(outcome==='ACT'){
          e.scores.vPred = dv;
          e.scores.vActual = +(dv + (rnd()-0.5)*1.6).toFixed(1);
        }
        e.nodes = NODES9.map(function(n){
          var st='PASS';
          if(outcome==='READ_MORE' && n==='KNOW') st='READ_MORE';
          if(outcome==='ASK' && n==='ACT') st='ASK';
          if(outcome==='REFUSE' && n==='LAW') st='REFUSED';
          return {node:n, status:st};
        });
        e.edges = NODES9.slice(1).map(function(n, j){
          return {source:NODES9[j], target:n, type:'HANDOFF', status:'SATISFIED'};
        });
        lastDec = id;
      } else if(kind==='execution'){
        e.outcome = outcome;
        e.decisionRef = lastDec || '';
        e.effectsObserved = 'Demo effect recorded for ' + (lastDec||'decision') + ' (' + (100+Math.floor(rnd()*900)) + ' bytes, sha256-bound).';
        e.durationMs = Math.floor(rnd()*900);
        e.authorityBasis = 'director_order \u00B7 order-demo-' + (i+1);
      } else {
        e.outcome = outcome;
        e.effectsObserved = label;
        e.scores = { deltaV:dv };
      }
      entries.push(normalize(e));
    });
    entries.sort(function(a,b){ return String(b.issuedAt).localeCompare(String(a.issuedAt)); });
    return entries;
  }

  /* One fresh demo beat for simulated-live mode. Labeled demo:true, always. */
  function demoBeat(){
    var kinds=['decision','execution','contribution','signal'];
    var k=kinds[Math.floor(Math.random()*kinds.length)];
    var hash=''; for(var i=0;i<64;i++) hash+='0123456789abcdef'[Math.floor(Math.random()*16)];
    var e={kind:k, id:'sim-'+Date.now().toString(36), demo:true,
           issuedAt:new Date().toISOString(), proofState:'RECORDED',
           hash:hash, hashes:{receipt:hash.slice(0,16), receiptFull:hash},
           scores:{}, raw:{simulated:true}};
    if(k==='decision'){
      var outcomes=['ACT','ACT','ACT','READ_MORE','ASK'];
      var o=outcomes[Math.floor(Math.random()*outcomes.length)];
      var q=+(7.5+Math.random()*2.4).toFixed(1);
      var dv=+(Math.random()*10-2).toFixed(1);
      e.outcome=o;
      e.scores={q:q, deltaV:dv, confidence:+(0.65+Math.random()*0.34).toFixed(2)};
      if(o==='ACT'){ e.scores.vPred=dv; e.scores.vActual=+(dv+(Math.random()-0.5)*1.6).toFixed(1); }
    } else if(k==='execution'){
      e.outcome='EFFECTS OBSERVED';
      e.effectsObserved='Simulated effect recorded ('+(100+Math.floor(Math.random()*900))+' bytes, sha256-bound).';
      e.durationMs=Math.floor(Math.random()*900);
      e.authorityBasis='director_order \u00B7 order-sim';
    } else {
      e.outcome=(k==='contribution'?'VALUED':'RECORDED');
      e.effectsObserved=(k==='contribution'?'Share valued':'Heartbeat signal');
      e.scores={deltaV:+(Math.random()*2).toFixed(1)};
    }
    return normalize(e);
  }

  window.LedgerAdapter = { parseOne:parseOne, parseMany:parseMany,
                           demoStream:demoStream, demoBeat:demoBeat,
                           smartNameFor:smartNameFor, normalize:normalize };
})();
