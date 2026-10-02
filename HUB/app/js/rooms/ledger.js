/* SMART LEDGER — Room: inspect what happened and what proves it.
 * Registry: HUB app rooms registry id "ledger", route "/ledger", theme gold.
 * Contract: window.NayaRooms.ledger(el, ctx)
 *   ctx.entries — ledger entries from LedgerAdapter.parseMany (receipt artifacts)
 *   ctx.onCopy  — optional fn(text); defaults to navigator.clipboard
 * Law: the ledger shows what is recorded. Proof states are never inflated:
 * UNKNOWN != IMPLEMENTED != VERIFIED != PRODUCTION-PROVEN. Candidate receipts
 * say CANDIDATE. Every button has a real consequence.
 */
(function(){
  'use strict';

  var GOLD = '#d4a017';

  /* the ratified decision pipeline (Smart Ledger Core Math V2.1, RATIFIED) */
  var PIPELINE = ['RESOLVE','GATE','SCORE','COMPARE','SELECT','ACT / ESCALATE','OBSERVE','VERIFY','LEDGER','LEARN','RECALIBRATE'];

  /* proof-maturity ladder */
  var LADDER = ['UNKNOWN','IMPLEMENTED','VERIFIED','PRODUCTION-PROVEN'];

  function fmtDate(iso){
    if(!iso) return '';
    var d = new Date(iso);
    if(isNaN(d)) return String(iso).slice(0,10);
    return d.toLocaleDateString('en-US',{month:'long',day:'numeric',year:'numeric'});
  }

  function shortHash(h){ return h ? String(h).slice(0,12) + '\u2026' : '\u2014'; }

  function LedgerRoom(el, ctx){
    ctx = ctx || {};
    var entries = Array.isArray(ctx.entries) ? ctx.entries : [];
    var onCopy = (typeof ctx.onCopy==='function') ? ctx.onCopy
      : function(t){ if(navigator.clipboard) navigator.clipboard.writeText(t); };

    var stage = el('div','ledger-stage');

    /* header */
    var head = el('header','lg-head');
    head.appendChild(el('p','lg-kicker','SMART LEDGER'));
    var h1 = el('h1','lg-title',''); h1.textContent = 'What happened, and what proves it';
    head.appendChild(h1);
    var sub = el('p','lg-sub','');
    sub.textContent = 'Every decision Naya makes leaves a receipt \u2014 what was decided, what the evidence said, and which proof rung it stands on. Nothing here is a claim; it is the record.';
    head.appendChild(sub);
    stage.appendChild(head);

    /* proof ladder */
    var lad = el('div','lg-ladder');
    lad.appendChild(el('span','lg-ladder-label','PROOF LADDER'));
    LADDER.forEach(function(r,i){
      if(i){ var ar=el('span','lg-ladder-arrow','\u2192'); lad.appendChild(ar); }
      var rung=el('span','lg-rung',''); rung.textContent=r; lad.appendChild(rung);
    });
    stage.appendChild(lad);

    /* decision pipeline */
    var pipe = el('div','lg-pipe');
    pipe.appendChild(el('span','lg-pipe-label','HOW NAYA DECIDES'));
    var chain = el('div','lg-pipe-chain');
    PIPELINE.forEach(function(p,i){
      if(i){ chain.appendChild(el('span','lg-pipe-arrow','\u2192')); }
      var s=el('span','lg-pipe-step',''); s.textContent=p; chain.appendChild(s);
    });
    pipe.appendChild(chain);
    stage.appendChild(pipe);

    /* entries */
    var list = el('div','lg-list');
    if(!entries.length){
      var empty = el('div','lg-empty','');
      empty.textContent = 'No ledger entries in view. Entries appear here as decision and execution receipts are recorded.';
      list.appendChild(empty);
    }
    entries.forEach(function(e){ list.appendChild(entryBoard(el, e, onCopy)); });
    stage.appendChild(list);

    var foot = el('footer','lg-foot','');
    foot.textContent = 'UNKNOWN \u2260 IMPLEMENTED \u2260 VERIFIED \u2260 PRODUCTION-PROVEN \u00B7 Production ledger: nayanet_smart_ledger / nayanet_execution_receipts';
    stage.appendChild(foot);

    return stage;
  }

  function entryBoard(el, e, onCopy){
    var board = el('article','lg-entry');

    var top = el('div','lg-top');
    var kind = el('span','lg-kind '+e.kind,''); kind.textContent = e.kind==='decision' ? 'DECISION' : 'EXECUTION';
    top.appendChild(kind);
    var nm = el('h2','lg-id',''); nm.textContent = e.id;
    top.appendChild(nm);
    var v = el('span','lg-verdict '+String(e.verdict).toLowerCase().replace(/[^a-z]+/g,'-'),'');
    v.textContent = e.verdict;
    top.appendChild(v);
    board.appendChild(top);

    var meta = el('div','lg-meta');
    if(e.issuedAt){ var dt=el('span','lg-date',''); dt.textContent=fmtDate(e.issuedAt); meta.appendChild(dt); }
    var ps = el('span','lg-proof',''); ps.textContent = e.proofState;
    meta.appendChild(ps);
    if(e.kernel){ var kv=el('span','lg-kernel',''); kv.textContent=e.kernel; meta.appendChild(kv); }
    board.appendChild(meta);

    if(e.banner){ var bn=el('p','lg-banner',''); bn.textContent=e.banner; board.appendChild(bn); }

    /* the nine nodes, in evaluation order, with their status */
    if(e.nodes && e.nodes.length){
      var nn = el('div','lg-nodes');
      nn.appendChild(el('span','lg-nodes-label','NODES'));
      var row = el('div','lg-node-row');
      e.nodes.forEach(function(n,i){
        if(i) row.appendChild(el('span','lg-node-arrow','\u2192'));
        var nd = el('span','lg-node '+n.status.toLowerCase().replace(/[^a-z]+/g,'-'),'');
        nd.textContent = n.node;
        nd.title = n.node + ': ' + n.status;
        row.appendChild(nd);
      });
      nn.appendChild(row);
      board.appendChild(nn);
    }

    /* the handoff chain */
    if(e.edges && e.edges.length){
      var ch = el('details','lg-edges');
      var sum = el('summary','',''); sum.textContent = 'Handoff chain \u00B7 ' + e.edges.length + ' edges';
      ch.appendChild(sum);
      var ul = el('ul','lg-edge-list');
      e.edges.forEach(function(g){
        var li = el('li','lg-edge '+String(g.status).toLowerCase().replace(/[^a-z]+/g,'-'),'');
        li.textContent = g.source + ' \u2192 ' + g.target + ' \u00B7 ' + g.status;
        ul.appendChild(li);
      });
      ch.appendChild(ul);
      board.appendChild(ch);
    }

    /* execution specifics */
    if(e.kind==='execution'){
      var ex = el('div','lg-exec');
      if(e.authorityBasis){ var ab=el('p','lg-exec-line',''); ab.textContent='Authority: '+e.authorityBasis; ex.appendChild(ab); }
      if(e.effectsObserved){ var eo=el('p','lg-exec-line',''); eo.textContent='Observed: '+String(e.effectsObserved).slice(0,220); ex.appendChild(eo); }
      if(e.calculusVersion || e.durationMs!==''){
        var cv=el('p','lg-exec-line dim',''); cv.textContent=[e.calculusVersion, e.durationMs!==''?e.durationMs+' ms':null].filter(Boolean).join(' \u00B7 ');
        ex.appendChild(cv);
      }
      board.appendChild(ex);
    }

    /* hashes with copy */
    if(e.hashes && (e.hashes.receipt || e.hashes.inputs)){
      var hh = el('div','lg-hashes');
      [['Receipt', e.hashes.receiptFull || e.hashes.receipt],
       ['Inputs', e.hashes.inputsFull || e.hashes.inputs]].forEach(function(pair){
        if(!pair[1]) return;
        var hrow = el('div','lg-hashrow');
        var lab = el('span','lg-hash-label',''); lab.textContent = pair[0] + ' hash';
        hrow.appendChild(lab);
        var code = el('code','lg-hash',''); code.textContent = shortHash(pair[1]);
        code.title = pair[1];
        hrow.appendChild(code);
        var cp = el('button','lg-copy','COPY'); cp.type='button';
        cp.setAttribute('aria-label','Copy full ' + pair[0].toLowerCase() + ' hash');
        (function(full){
          cp.addEventListener('click', function(){
            onCopy(full);
            cp.textContent='COPIED'; setTimeout(function(){cp.textContent='COPY';},1400);
          });
        })(pair[1]);
        hrow.appendChild(cp);
        hh.appendChild(hrow);
      });
      board.appendChild(hh);
    }

    return board;
  }

  window.NayaRooms = window.NayaRooms || {};
  window.NayaRooms.ledger = LedgerRoom;
})();
