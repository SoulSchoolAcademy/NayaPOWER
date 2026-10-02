/* LIVING INTEL — the heartbeat of it all.
 * The unified living stream: intelligence reports, smart notes, ledger
 * actions, and connection states — every source keeping its identity color,
 * one heart beating underneath.
 *
 * Contract: window.NayaRooms.livingIntel(el, ctx)
 *   ctx.items — from LivingIntelAdapter.build (newest first)
 * Law: demo items keep their DEMO chip. Time-ago ticks live. Every
 * button has a real consequence. Color is stable source identity.
 */
(function(){
  'use strict';

  var FILTERS = [
    ['all',   'ALL',         '#ffffff', null],
    ['intel', 'INTEL',       '#38bdf8', ['report','note']],
    ['actions','ACTIONS',    '#d4a017', ['ledger']],
    ['connect','CONNECTIONS','#6366f1', ['connect']]
  ];

  function timeAgo(ts){
    var s = Math.max(0, Math.floor((Date.now()-ts)/1000));
    if(s < 60) return 'just now';
    var m = Math.floor(s/60); if(m < 60) return m+'m ago';
    var h = Math.floor(m/60); if(h < 24) return h+'h ago';
    var d = Math.floor(h/24); if(d < 7) return d+'d ago';
    return Math.floor(d/7)+'w ago';
  }

  function ekgPath(W, H, beats){
    var mid = H/2, seg = W/beats, p = 'M 0 '+mid;
    for(var b=0;b<beats;b++){
      var x = b*seg;
      /* P wave, QRS spike, T wave */
      p += ' L '+(x+seg*0.18).toFixed(1)+' '+mid;
      p += ' Q '+(x+seg*0.24).toFixed(1)+' '+(mid-14).toFixed(1)+' '+(x+seg*0.30).toFixed(1)+' '+mid;
      p += ' L '+(x+seg*0.40).toFixed(1)+' '+mid;
      p += ' L '+(x+seg*0.44).toFixed(1)+' '+(mid+10).toFixed(1);
      p += ' L '+(x+seg*0.50).toFixed(1)+' '+(mid-52).toFixed(1);
      p += ' L '+(x+seg*0.56).toFixed(1)+' '+(mid+16).toFixed(1);
      p += ' L '+(x+seg*0.60).toFixed(1)+' '+mid;
      p += ' Q '+(x+seg*0.72).toFixed(1)+' '+(mid-18).toFixed(1)+' '+(x+seg*0.84).toFixed(1)+' '+mid;
      p += ' L '+((x+seg)).toFixed(1)+' '+mid;
    }
    return p;
  }

  function LivingIntel(el, ctx){
    ctx = ctx || {};
    var items = Array.isArray(ctx.items) ? ctx.items : [];
    var state = { filter:'all' };

    var stage = el('div','li-stage');

    /* ============ HERO ============ */
    var hero = el('section','li-hero');
    var glow = el('div','li-glow'); hero.appendChild(glow);

    var svgNS='http://www.w3.org/2000/svg';
    var W=1200,H=220;
    var svg=document.createElementNS(svgNS,'svg');
    svg.setAttribute('viewBox','0 0 '+W+' '+H); svg.setAttribute('class','li-ekg');
    svg.setAttribute('preserveAspectRatio','none');
    var defs=document.createElementNS(svgNS,'defs');
    var grad=document.createElementNS(svgNS,'linearGradient');
    grad.setAttribute('id','li-ekg-grad'); grad.setAttribute('x1','0'); grad.setAttribute('y1','0');
    grad.setAttribute('x2','1'); grad.setAttribute('y2','0');
    [['0','#38bdf8'],['0.35','#c084fc'],['0.65','#d4a017'],['1','#ef4444']].forEach(function(s){
      var st=document.createElementNS(svgNS,'stop');
      st.setAttribute('offset',s[0]); st.setAttribute('stop-color',s[1]); defs.appendChild(st);
    });
    svg.appendChild(defs);
    var d = ekgPath(W,H,7);
    var base=document.createElementNS(svgNS,'path');
    base.setAttribute('d',d); base.setAttribute('class','li-ekg-base'); svg.appendChild(base);
    var flow=document.createElementNS(svgNS,'path');
    flow.setAttribute('d',d); flow.setAttribute('class','li-ekg-flow'); svg.appendChild(flow);
    var dot=document.createElementNS(svgNS,'circle');
    dot.setAttribute('r','7'); dot.setAttribute('class','li-ekg-dot');
    var mot=document.createElementNS(svgNS,'animateMotion');
    mot.setAttribute('dur','9s'); mot.setAttribute('repeatCount','indefinite');
    mot.setAttribute('path',d); dot.appendChild(mot); svg.appendChild(dot);
    hero.appendChild(svg);

    var hov = el('div','li-hero-over');
    var kick = el('p','li-kicker',''); 
    var liveDot = el('span','li-live-dot',''); kick.appendChild(liveDot);
    var ktx = el('span','',''); ktx.textContent=' LIVING INTEL \u00B7 LIVE'; kick.appendChild(ktx);
    hov.appendChild(kick);
    var h1 = el('h1','li-title',''); h1.textContent='The heartbeat of it all'; hov.appendChild(h1);
    var sub = el('p','li-sub','');
    sub.textContent='Every report, every note, every action, every connection \u2014 one living stream. This is Naya thinking, in the open.';
    hov.appendChild(sub);

    /* hero stats */
    var stats = el('div','li-stats');
    var sources = {};
    items.forEach(function(i){ sources[i.source]=(sources[i.source]||0)+1; });
    [['ITEMS FLOWING', items.length],['SOURCES ALIVE', Object.keys(sources).length],
     ['NEWEST', items.length? timeAgo(items[0].ts):'\u2014']].forEach(function(s){
      var c = el('div','li-stat');
      var n = el('span','li-stat-n',''); n.textContent=s[1]; c.appendChild(n);
      c.appendChild(el('span','li-stat-l',s[0]));
      stats.appendChild(c);
    });
    hov.appendChild(stats);
    hero.appendChild(hov);
    stage.appendChild(hero);

    /* ============ SOURCE JEWELS ============ */
    var jewels = el('div','li-jewels');
    var seen = {};
    items.forEach(function(i){ seen[i.source]=(seen[i.source]||0)+1; });
    var meta = {
      report:['\u25C8','#38bdf8','INTEL REPORTS'],
      note:['\u2726','#c084fc','SMART NOTES'],
      ledger:['\u25C6','#d4a017','LEDGER'],
      connect:['\u25C9','#6366f1','CONNECT']
    };
    Object.keys(meta).forEach(function(k){
      var j = el('button','li-jewel'); j.type='button';
      j.style.setProperty('--jc', meta[k][1]);
      j.setAttribute('aria-label','Filter to '+meta[k][2]);
      var g = el('span','li-jewel-g',''); g.textContent=meta[k][0]; j.appendChild(g);
      j.appendChild(el('span','li-jewel-n',meta[k][2]));
      var c = el('span','li-jewel-c',''); c.textContent=(seen[k]||0); j.appendChild(c);
      j.addEventListener('click', function(){ setFilter(k==='report'||k==='note' ? 'intel' : (k==='ledger'?'actions':'connect')); });
      jewels.appendChild(j);
    });
    stage.appendChild(jewels);

    /* ============ FILTERS ============ */
    var tabs = el('nav','li-tabs');
    FILTERS.forEach(function(f){
      var b = el('button','li-tab'+(f[0]===state.filter?' on':''), f[1]);
      b.type='button'; b.style.setProperty('--tab-c', f[2]);
      b.addEventListener('click', function(){ setFilter(f[0]); });
      tabs.appendChild(b);
    });
    stage.appendChild(tabs);

    /* ============ STREAM ============ */
    var stream = el('div','li-stream');
    stage.appendChild(stream);

    function setFilter(f){
      state.filter = f;
      var btns = tabs.querySelectorAll('.li-tab');
      FILTERS.forEach(function(ff,i){
        btns[i].classList.toggle('on', ff[0]===f);
      });
      renderStream();
    }

    function visible(){
      var f = FILTERS.filter(function(x){return x[0]===state.filter;})[0];
      if(!f || !f[3]) return items;
      return items.filter(function(i){ return f[3].indexOf(i.source)>=0; });
    }

    function renderStream(){
      stream.innerHTML='';
      var list = visible();
      if(!list.length){
        stream.appendChild(el('p','li-empty','Nothing flowing here yet.'));
        return;
      }
      list.forEach(function(it, idx){
        var card = el('article','li-card');
        card.style.setProperty('--ic', it.color);
        card.style.animationDelay = Math.min(idx*0.05, 1)+'s';
        var top = el('div','li-card-top');
        var jw = el('span','li-card-j',''); jw.textContent=it.jewel; top.appendChild(jw);
        top.appendChild(el('span','li-card-s', sourceLabel(it.source)));
        var ta = el('span','li-card-t',''); ta.textContent=timeAgo(it.ts); ta.setAttribute('data-ts', it.ts);
        top.appendChild(ta);
        if(it.demo) top.appendChild(el('span','li-demo-chip','DEMO'));
        card.appendChild(top);
        var t = el('h2','li-card-title',''); t.textContent=it.title; card.appendChild(t);
        if(it.nutshell){ var n=el('p','li-card-n',''); n.textContent=it.nutshell; card.appendChild(n); }
        if(it.meta){ var m=el('p','li-card-m',''); m.textContent=it.meta; card.appendChild(m); }
        stream.appendChild(card);
      });
    }
    renderStream();

    /* live time-ago ticker */
    var timer = setInterval(function(){
      if(!document.contains(stage)){ clearInterval(timer); return; }
      stream.querySelectorAll('[data-ts]').forEach(function(n){
        n.textContent = timeAgo(+n.getAttribute('data-ts'));
      });
    }, 30000);

    var foot = el('footer','li-foot','');
    foot.textContent = 'every source keeps its color \u00B7 demo items labeled \u00B7 identities never revealed';
    stage.appendChild(foot);
    return stage;
  }

  function sourceLabel(s){
    return {report:'INTEL REPORT', note:'SMART NOTE', ledger:'LEDGER', connect:'CONNECT'}[s] || s.toUpperCase();
  }

  window.NayaRooms = window.NayaRooms || {};
  window.NayaRooms.livingIntel = LivingIntel;
})();
