/* SMART LEDGER DASHBOARD — Room 4 v2: the heartbeat of the system.
 * Registry: "ledger", route "/ledger", theme gold.
 * Contract: window.NayaRooms.ledger(el, ctx)
 *   ctx.entries — ledger entries (LedgerAdapter.parseMany or demoStream)
 *   ctx.demo    — true when the stream is demo content (banner shown)
 *   ctx.onCopy  — optional fn(text); defaults to navigator.clipboard
 * Law: demo content is always labeled DEMO. Real entries are never mixed
 * with demo without the banner. Proof states never inflated. Every button
 * has a real consequence.
 */
(function(){
  'use strict';

  var VIEWS = [
    ['heartbeat','Heartbeat'],
    ['value','Value'],
    ['nodes','Nodes'],
    ['proof','Proof'],
    ['receipts','Receipts']
  ];
  /* stable identity color per view — color belongs to the object, never the position */
  var VIEW_COLORS = {heartbeat:'#ef4444', value:'#4ade80', nodes:'#22d3ee', proof:'#a371f7', receipts:'#d4a017'};
  var LADDER = ['UNKNOWN','IMPLEMENTED','VERIFIED','PRODUCTION-PROVEN'];
  var STAGES = [
    ['GATES','Every action passes the gates first'],
    ['QUALITY','Q \u2265 9 to proceed'],
    ['VALUE','\u0394V > 0 vs baseline'],
    ['CONFIDENCE','Critical facts certain']
  ];

  function fmtTime(iso){
    var d = new Date(iso); if(isNaN(d)) return '';
    return d.toLocaleTimeString('en-US',{hour:'numeric',minute:'2-digit'});
  }
  function fmtDate(iso){
    var d = new Date(iso); if(isNaN(d)) return '';
    return d.toLocaleDateString('en-US',{month:'short',day:'numeric'});
  }
  function shortHash(h){ return h ? String(h).slice(0,10) + '\u2026' : '\u2014'; }
  function dvClass(dv){ return dv==null||isNaN(dv) ? '' : (dv>0?'pos':(dv<0?'neg':'')); }

  function LedgerRoom(el, ctx){
    ctx = ctx || {};
    var entries = Array.isArray(ctx.entries) ? ctx.entries : [];
    var demo = !!ctx.demo;
    var onCopy = (typeof ctx.onCopy==='function') ? ctx.onCopy
      : function(t){ if(navigator.clipboard) navigator.clipboard.writeText(t); };

    var stage = el('div','ledger-stage');
    var state = { view:'heartbeat', modalEntry:null };

    /* header */
    var head = el('header','lg-head');
    head.appendChild(el('p','lg-kicker','SMART LEDGER'));
    var h1 = el('h1','lg-title',''); h1.textContent='The heartbeat of the system'; head.appendChild(h1);
    var sub = el('p','lg-sub','');
    sub.textContent = 'Every action in and out \u2014 decisions, executions, contributions, signals \u2014 recorded as it happens. Beautiful math, transparent chain, identities never revealed.';
    head.appendChild(sub);
    if(demo){
      var db = el('p','lg-demo','');
      db.textContent = 'DEMO STREAM \u00B7 illustrative data for design review \u00B7 the live stream connects at launch';
      head.appendChild(db);
    }
    stage.appendChild(head);

    /* counters */
    stage.appendChild(counters(el, entries));

    /* view tabs */
    var tabs = el('nav','lg-tabs'); tabs.setAttribute('role','tablist');
    var body = el('div','lg-body');
    VIEWS.forEach(function(v){
      var b = el('button','lg-tab'+(v[0]===state.view?' on':''), v[1].toUpperCase());
      b.type='button'; b.setAttribute('role','tab');
      b.style.setProperty('--tab-c', VIEW_COLORS[v[0]]);
      b.setAttribute('aria-selected', v[0]===state.view ? 'true':'false');
      b.addEventListener('click', function(){
        state.view = v[0];
        tabs.querySelectorAll('.lg-tab').forEach(function(t){
          t.classList.remove('on'); t.setAttribute('aria-selected','false');
        });
        b.classList.add('on'); b.setAttribute('aria-selected','true');
        renderView();
      });
      tabs.appendChild(b);
    });
    stage.appendChild(tabs);
    stage.appendChild(body);

    function renderView(){
      body.innerHTML='';
      var fn = {heartbeat:viewHeartbeat, value:viewValue, nodes:viewNodes,
                proof:viewProof, receipts:viewReceipts}[state.view];
      body.appendChild(fn(el, entries, onCopy, openModal));
    }
    renderView();

    /* smart-id modal */
    var overlay = el('div','lg-overlay'); overlay.style.display='none';
    var card = el('div','lg-modal');
    overlay.appendChild(card);
    overlay.addEventListener('click', function(ev){ if(ev.target===overlay) closeModal(); });
    stage.appendChild(overlay);
    function openModal(e){
      state.modalEntry = e;
      card.innerHTML='';
      var k = el('p','lg-kicker','SMART ID'); card.appendChild(k);
      var nm = el('h2','lg-modal-name',''); nm.textContent = e.glyph + ' ' + e.smartName; card.appendChild(nm);
      var meta = el('p','lg-modal-meta','');
      meta.textContent = e.kind.toUpperCase() + ' \u00B7 ' + e.outcome + ' \u00B7 ' + fmtDate(e.issuedAt) + ' ' + fmtTime(e.issuedAt);
      card.appendChild(meta);
      var lab = el('p','lg-hash-label','FULL HASH \u00B7 the cryptographic id behind the name'); card.appendChild(lab);
      var code = el('code','lg-modal-hash',''); code.textContent = e.hash || '\u2014'; card.appendChild(code);
      var row = el('div','lg-modal-row');
      var cp = el('button','lg-copy','COPY HASH'); cp.type='button';
      cp.addEventListener('click', function(){ onCopy(e.hash||''); cp.textContent='COPIED'; setTimeout(function(){cp.textContent='COPY HASH';},1400); });
      row.appendChild(cp);
      var raw = el('button','lg-copy','VIEW RAW'); raw.type='button';
      raw.addEventListener('click', function(){
        var pre = card.querySelector('.lg-modal-raw');
        if(pre){ pre.remove(); raw.textContent='VIEW RAW'; return; }
        var p2 = el('pre','lg-modal-raw',''); p2.textContent = JSON.stringify(e.raw||e, null, 2);
        card.appendChild(p2); raw.textContent='HIDE RAW';
      });
      row.appendChild(raw);
      var x = el('button','lg-copy','CLOSE'); x.type='button';
      x.addEventListener('click', closeModal); row.appendChild(x);
      card.appendChild(row);
      overlay.style.display='flex';
    }
    function closeModal(){ overlay.style.display='none'; state.modalEntry=null; }

    var foot = el('footer','lg-foot','');
    foot.textContent = 'UNKNOWN \u2260 IMPLEMENTED \u2260 VERIFIED \u2260 PRODUCTION-PROVEN \u00B7 identities never revealed';
    stage.appendChild(foot);
    return stage;
  }

  /* ---------------- counters ---------------- */
  function counters(el, entries){
    var wrap = el('div','lg-counters');
    var inn = entries.filter(function(e){ return e.kind!=='execution'; }).length;
    var out = entries.filter(function(e){ return e.kind==='execution'; }).length;
    var ver = entries.filter(function(e){ return e.proofState==='VERIFIED'||e.proofState==='PRODUCTION-PROVEN'; }).length;
    var ref = entries.filter(function(e){ return e.outcome==='REFUSE'; }).length;
    [['ACTIONS IN',inn,true],['ACTIONS OUT',out],['VERIFIED',ver],['REFUSED',ref]].forEach(function(c){
      var d = el('div','lg-counter');
      var n = el('span','lg-counter-n',''); n.textContent='0'; d.appendChild(n);
      var lab = el('span','lg-counter-l');
      if(c[2]){ var dot=el('span','lg-live-dot',''); lab.appendChild(dot); }
      var t = el('span','',''); t.textContent=c[0]; lab.appendChild(t);
      d.appendChild(lab);
      wrap.appendChild(d);
      /* living numbers: count up on load */
      (function(node, target){
        var t0=null, dur=900;
        function step(ts){
          if(t0===null)t0=ts;
          var k=Math.min(1,(ts-t0)/dur), ease=1-Math.pow(1-k,3);
          node.textContent=Math.round(target*ease);
          if(k<1) requestAnimationFrame(step);
        }
        if(typeof requestAnimationFrame==='function') requestAnimationFrame(step);
        else node.textContent=target;
      })(n, c[1]);
    });
    return wrap;
  }

  function smartChip(el, e, openModal){
    var b = el('button','lg-chip'); b.type='button';
    b.setAttribute('aria-label','Inspect '+e.smartName);
    var g = el('span','lg-chip-g',''); g.textContent=e.glyph; b.appendChild(g);
    var n = el('span','lg-chip-n',''); n.textContent=e.smartName; b.appendChild(n);
    var h = el('span','lg-chip-h',''); h.textContent=shortHash(e.hash); b.appendChild(h);
    b.addEventListener('click', function(){ openModal(e); });
    return b;
  }

  function kindPill(el, kind){
    var p = el('span','lg-kind '+kind,''); p.textContent=kind.toUpperCase(); return p;
  }
  function outcomePill(el, outcome){
    var p = el('span','lg-outcome '+String(outcome).toLowerCase().replace(/[^a-z]+/g,'-'),'');
    p.textContent=outcome; return p;
  }

  /* ---------------- HEARTBEAT view ---------------- */
  function viewHeartbeat(el, entries, onCopy, openModal){
    var v = el('div','lg-view');
    /* pulse */
    var pw = el('div','lg-pulse-wrap');
    var svgNS='http://www.w3.org/2000/svg';
    var W=1160,H=170,mid=H/2;
    var svg=document.createElementNS(svgNS,'svg');
    svg.setAttribute('viewBox','0 0 '+W+' '+H); svg.setAttribute('class','lg-pulse');
    var line=document.createElementNS(svgNS,'line');
    line.setAttribute('x1',0);line.setAttribute('x2',W);
    line.setAttribute('y1',mid);line.setAttribute('y2',mid);
    line.setAttribute('class','lg-pulse-base'); svg.appendChild(line);
    var chrono = entries.slice().reverse();
    var maxDV = 1;
    chrono.forEach(function(e){ var dv=e.scores&&e.scores.deltaV; if(dv!=null&&Math.abs(dv)>maxDV) maxDV=Math.abs(dv); });
    chrono.forEach(function(e,i){
      var x = 30 + (W-60)*(i/Math.max(1,chrono.length-1));
      var dv = (e.scores&&e.scores.deltaV)||0;
      var amp = 12 + Math.min(1,Math.abs(dv)/maxDV)*52;
      var up = dv>=0;
      var pl=document.createElementNS(svgNS,'polyline');
      pl.setAttribute('points',(x-14)+','+mid+' '+x+','+(up?mid-amp:mid+amp)+' '+(x+14)+','+mid);
      pl.setAttribute('class','lg-beat '+dvClass(dv));
      pl.style.animationDelay=(i*0.12)+'s';
      svg.appendChild(pl);
      var dot=document.createElementNS(svgNS,'circle');
      dot.setAttribute('cx',x);dot.setAttribute('cy',up?mid-amp:mid+amp);dot.setAttribute('r',4.5);
      dot.setAttribute('class','lg-beat-dot '+dvClass(dv));
      dot.style.animationDelay=(i*0.12)+'s';
      svg.appendChild(dot);
    });
    var sweep=document.createElementNS(svgNS,'line');
    sweep.setAttribute('x1',0);sweep.setAttribute('x2',0);
    sweep.setAttribute('y1',8);sweep.setAttribute('y2',H-8);
    sweep.setAttribute('class','lg-sweep'); svg.appendChild(sweep);
    pw.appendChild(svg);
    var pl = el('p','lg-pulse-label','');
    var dot = el('span','lg-live-dot',''); pl.appendChild(dot);
    var ptx = el('span','',''); ptx.textContent = ' LIVE \u00B7 ' + entries.length + ' recorded actions \u00B7 newest on the right \u00B7 click any action to inspect its smart id';
    pl.appendChild(ptx);
    pw.appendChild(pl);
    v.appendChild(pw);
    /* ticker */
    var tick = el('div','lg-ticker');
    entries.forEach(function(e){
      var row = el('div','lg-trow');
      var t = el('span','lg-trow-t',''); t.textContent=fmtTime(e.issuedAt); row.appendChild(t);
      row.appendChild(smartChip(el, e, openModal));
      row.appendChild(kindPill(el, e.kind));
      row.appendChild(outcomePill(el, e.outcome));
      var dv=e.scores&&e.scores.deltaV;
      if(dv!=null&&!isNaN(dv)){
        var d=el('span','lg-dv '+dvClass(dv),''); d.textContent=(dv>0?'+':'')+dv; row.appendChild(d);
      }
      tick.appendChild(row);
    });
    if(!entries.length) tick.appendChild(el('p','lg-empty-t','No actions recorded yet.'));
    v.appendChild(tick);
    return v;
  }

  /* ---------------- VALUE view ---------------- */
  function viewValue(el, entries, onCopy, openModal){
    var v = el('div','lg-view');
    var dec = entries.filter(function(e){ return e.kind==='decision' && e.scores && e.scores.q!=null; });
    /* engine strip */
    var strip = el('div','lg-engine');
    var gates = entries.length;
    var hq = dec.filter(function(e){ return e.scores.q>=9; }).length;
    var pv = dec.filter(function(e){ return e.scores.deltaV>0; }).length;
    var cf = dec.filter(function(e){ return e.scores.confidence>=0.8; }).length;
    var counts=[gates,hq,pv,cf];
    STAGES.forEach(function(s,i){
      var c=el('div','lg-stage');
      c.appendChild(el('span','lg-stage-n',String(counts[i])));
      c.appendChild(el('span','lg-stage-t',s[0]));
      var d=el('span','lg-stage-d',''); d.textContent=s[1]; c.appendChild(d);
      strip.appendChild(c);
      if(i<3) strip.appendChild(el('span','lg-stage-arrow','\u2192'));
    });
    v.appendChild(strip);
    /* deltaV chart */
    v.appendChild(el('h3','lg-sec','\u0394V per decision \u00B7 value vs doing nothing'));
    var chart = el('div','lg-chart');
    var maxDV=1;
    dec.forEach(function(e){ var a=Math.abs(e.scores.deltaV||0); if(a>maxDV)maxDV=a; });
    dec.forEach(function(e){
      var dv=e.scores.deltaV||0;
      var row=el('div','lg-crow');
      var nm=el('span','lg-crow-n',''); nm.textContent=e.smartName; row.appendChild(nm);
      var track=el('div','lg-crow-track');
      track.appendChild(el('span','lg-zero'));
      var bar=el('span','lg-crow-bar '+dvClass(dv),'');
      bar.style.width=(Math.abs(dv)/maxDV*50)+'%';
      if(dv>=0){ bar.style.left='50%'; } else { bar.style.right='50%'; }
      track.appendChild(bar); row.appendChild(track);
      var val=el('span','lg-crow-v '+dvClass(dv),''); val.textContent=(dv>0?'+':'')+dv; row.appendChild(val);
      chart.appendChild(row);
    });
    if(!dec.length) chart.appendChild(el('p','lg-empty-t','No scored decisions yet.'));
    v.appendChild(chart);
    /* quality bars */
    v.appendChild(el('h3','lg-sec','Quality \u00B7 Q \u2265 9 to proceed'));
    var qb = el('div','lg-chart');
    dec.forEach(function(e){
      var row=el('div','lg-crow');
      var nm=el('span','lg-crow-n',''); nm.textContent=e.smartName; row.appendChild(nm);
      var track=el('div','lg-crow-track q');
      var bar=el('span','lg-crow-bar q',''); bar.style.width=(e.scores.q/10*100)+'%'; track.appendChild(bar);
      var mark=el('span','lg-qmark'); mark.style.left='90%'; track.appendChild(mark);
      row.appendChild(track);
      var val=el('span','lg-crow-v',''); val.textContent=e.scores.q.toFixed(1); row.appendChild(val);
      qb.appendChild(row);
    });
    v.appendChild(qb);
    return v;
  }

  /* ---------------- NODES view ---------------- */
  function viewNodes(el, entries, onCopy, openModal){
    var v = el('div','lg-view');
    var stats={};
    entries.forEach(function(e){
      (e.nodes||[]).forEach(function(n){
        var s=stats[n.node]=stats[n.node]||{evals:0,pass:0,edges:0};
        s.evals++; if(n.status==='PASS')s.pass++;
      });
      (e.edges||[]).forEach(function(g){
        [g.source,g.target].forEach(function(n){
          if(!n)return; var s=stats[n]=stats[n]||{evals:0,pass:0,edges:0}; s.edges++;
        });
      });
    });
    var order=['SELF','LAW','KNOW','ACT','PROVE','CONNECT','VERIFY','LEARN','EVOLVE'];
    var grid=el('div','lg-nodes-grid');
    order.forEach(function(n){
      var s=stats[n]||{evals:0,pass:0,edges:0};
      var rate=s.evals?Math.round(s.pass/s.evals*100):0;
      var card=el('button','lg-node-card'); card.type='button';
      var nm=el('span','lg-node-card-n',''); nm.textContent=n; card.appendChild(nm);
      var svgNS='http://www.w3.org/2000/svg';
      var svg=document.createElementNS(svgNS,'svg'); svg.setAttribute('viewBox','0 0 60 60'); svg.setAttribute('class','lg-ring');
      var bg=document.createElementNS(svgNS,'circle');
      bg.setAttribute('cx',30);bg.setAttribute('cy',30);bg.setAttribute('r',24);bg.setAttribute('class','lg-ring-bg'); svg.appendChild(bg);
      var fg=document.createElementNS(svgNS,'circle');
      fg.setAttribute('cx',30);fg.setAttribute('cy',30);fg.setAttribute('r',24);fg.setAttribute('class','lg-ring-fg');
      fg.style.strokeDasharray=(rate*1.508)+' 151'; svg.appendChild(fg);
      var tx=document.createElementNS(svgNS,'text');
      tx.setAttribute('x',30);tx.setAttribute('y',35);tx.setAttribute('class','lg-ring-tx');
      tx.textContent=rate+'%'; svg.appendChild(tx);
      card.appendChild(svg);
      var meta=el('span','lg-node-card-m',''); meta.textContent=s.evals+' evals \u00B7 '+s.edges+' handoffs'; card.appendChild(meta);
      card.setAttribute('aria-label',n+': '+rate+' percent pass');
      grid.appendChild(card);
    });
    v.appendChild(grid);
    v.appendChild(el('p','lg-pulse-label','Rings show pass rate across recorded evaluations.'));
    return v;
  }

  /* ---------------- PROOF view ---------------- */
  function viewProof(el, entries, onCopy, openModal){
    var v = el('div','lg-view');
    var cols=el('div','lg-proof-cols');
    LADDER.forEach(function(rung){
      var col=el('div','lg-proof-col');
      col.appendChild(el('h4','lg-proof-rung',rung));
      var mine=entries.filter(function(e){ return e.proofState===rung; });
      var n=el('span','lg-proof-n',''); n.textContent=mine.length; col.appendChild(n);
      mine.forEach(function(e){ col.appendChild(smartChip(el, e, openModal)); });
      cols.appendChild(col);
    });
    v.appendChild(cols);
    /* calibration */
    var cal=entries.filter(function(e){ return e.scores&&(e.scores.vPred!=null&&e.scores.vActual!=null); });
    if(cal.length){
      v.appendChild(el('h3','lg-sec','Calibration \u00B7 predicted vs observed value'));
      var chart=el('div','lg-chart');
      var mx=1;
      cal.forEach(function(e){ mx=Math.max(mx,Math.abs(e.scores.vPred),Math.abs(e.scores.vActual)); });
      cal.forEach(function(e){
        var row=el('div','lg-calrow');
        var nm=el('span','lg-crow-n',''); nm.textContent=e.smartName; row.appendChild(nm);
        [['pred',e.scores.vPred],['act',e.scores.vActual]].forEach(function(pair){
          var track=el('div','lg-crow-track cal');
          var bar=el('span','lg-crow-bar '+pair[0]+' '+dvClass(pair[1]),'');
          bar.style.width=(Math.abs(pair[1])/mx*100)+'%'; track.appendChild(bar);
          var lab=el('span','lg-cal-lab',''); lab.textContent=pair[0]+' '+(pair[1]>0?'+':'')+pair[1];
          var wrap=el('div','lg-calwrap'); wrap.appendChild(track); wrap.appendChild(lab); row.appendChild(wrap);
        });
        chart.appendChild(row);
      });
      v.appendChild(chart);
      v.appendChild(el('p','lg-pulse-label','No score laundering: a predicted +9 that lands +2 is recorded as a bad prediction.'));
    }
    return v;
  }

  /* ---------------- RECEIPTS view (the record) ---------------- */
  function viewReceipts(el, entries, onCopy, openModal){
    var v = el('div','lg-view');
    var list = el('div','lg-list');
    if(!entries.length) list.appendChild(el('p','lg-empty-t','No receipts recorded yet.'));
    entries.forEach(function(e){ list.appendChild(entryBoard(el, e, onCopy, openModal)); });
    v.appendChild(list);
    return v;
  }

  function entryBoard(el, e, onCopy, openModal){
    var board = el('article','lg-entry');
    var top = el('div','lg-top');
    top.appendChild(kindPill(el, e.kind));
    var nm = el('h2','lg-id',''); nm.textContent = e.glyph+' '+e.smartName;
    nm.style.cursor='pointer'; nm.addEventListener('click', function(){ openModal(e); });
    top.appendChild(nm);
    top.appendChild(outcomePill(el, e.outcome));
    board.appendChild(top);
    var meta = el('div','lg-meta');
    if(e.issuedAt){ var dt=el('span','lg-date',''); dt.textContent=fmtDate(e.issuedAt)+' '+fmtTime(e.issuedAt); meta.appendChild(dt); }
    var ps = el('span','lg-proof',''); ps.textContent = e.proofState; meta.appendChild(ps);
    if(e.demo){ var dm=el('span','lg-demo-tag',''); dm.textContent='DEMO'; meta.appendChild(dm); }
    board.appendChild(meta);
    if(e.effectsObserved){ var eo=el('p','lg-exec-line',''); eo.textContent=e.effectsObserved; board.appendChild(eo); }
    if(e.authorityBasis){ var ab=el('p','lg-exec-line dim',''); ab.textContent='Authority: '+e.authorityBasis; board.appendChild(ab); }
    var hh = el('div','lg-hashes');
    var hrow = el('div','lg-hashrow');
    hrow.appendChild(el('span','lg-hash-label','SMART ID \u00B7 backed by'));
    var code = el('code','lg-hash',''); code.textContent=shortHash(e.hash); code.title=e.hash||'';
    hrow.appendChild(code);
    var insp = el('button','lg-copy','INSPECT'); insp.type='button';
    insp.addEventListener('click', function(){ openModal(e); });
    hrow.appendChild(insp);
    hh.appendChild(hrow); board.appendChild(hh);
    return board;
  }

  window.NayaRooms = window.NayaRooms || {};
  window.NayaRooms.ledger = LedgerRoom;
})();
