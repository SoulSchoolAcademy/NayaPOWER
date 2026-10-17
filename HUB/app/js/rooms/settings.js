/* SETTINGS — the Hub's control surface.
 * No canonical source: pure control surface, so EVERY control has a real,
 * visible consequence inside the preview. That is the whole test of this room.
 *
 * Contract: window.NayaRooms.settings(el, ctx)
 *   ctx.userName — optional display name for the Identity card (default "Shawn Vibert")
 * All settings persist to localStorage key "naya.settings" and apply live.
 * Room identity color: SLATE #94a3b8.
 */
(function(){
  'use strict';

  var STORE_KEY = 'naya.settings';
  var SLATE = '#94a3b8';

  var DEFAULTS = {
    density: 'comfortable',   // 'comfortable' | 'compact'
    reduceMotion: false,
    simLive: true,            // local demo heartbeat of the Living Intel stream setting
    maskIdentity: true,       // privacy-first default
    notifReports: true,
    notifBuilds: true,
    notifMentions: true
  };

  var ROOMS = ['today','reports','connect','ledger','living-intel','settings'];

  function load(){
    var s = {};
    try { s = JSON.parse(localStorage.getItem(STORE_KEY) || '{}') || {}; } catch(e){ s = {}; }
    var out = {};
    Object.keys(DEFAULTS).forEach(function(k){
      out[k] = (k in s) ? s[k] : DEFAULTS[k];
    });
    return out;
  }
  function save(st){
    try { localStorage.setItem(STORE_KEY, JSON.stringify(st)); } catch(e){}
  }

  function masked(name){
    return name.split(' ').map(function(w){
      return w.charAt(0) + '\u2022'.repeat(Math.max(2, w.length - 1));
    }).join(' ');
  }

  function SettingsRoom(el, ctx){
    ctx = ctx || {};
    var userName = ctx.userName || 'Shawn Vibert';
    var st = load();
    var stage = el('div','st-stage');

    /* ---------- header ---------- */
    var head = el('header','st-head');
    head.appendChild(el('p','st-kicker','SETTINGS'));
    var h1 = el('h1','st-title',''); h1.textContent = 'The control surface';
    head.appendChild(h1);
    var sub = el('p','st-sub','');
    sub.textContent = 'Every control here does something real, right now, on this page. Nothing decorative.';
    head.appendChild(sub);
    stage.appendChild(head);

    /* saved-confirmation pill: visible proof that a change persisted */
    var savedPill = el('span','st-saved','SAVED');
    head.querySelector('.st-kicker').appendChild(savedPill);
    function markSaved(){
      savedPill.classList.add('show');
      clearTimeout(markSaved._t);
      markSaved._t = setTimeout(function(){ savedPill.classList.remove('show'); }, 1400);
    }
    function persist(){ save(st); markSaved(); }

    function applyGlobal(){
      stage.classList.toggle('st-compact', st.density === 'compact');
      stage.classList.toggle('st-reduced', !!st.reduceMotion);
    }

    /* ---------- switch component ---------- */
    function switchRow(label, desc, get, set){
      var row = el('div','st-row');
      var tx = el('div','st-row-tx');
      tx.appendChild(el('span','st-row-label', label));
      if(desc) tx.appendChild(el('span','st-row-desc', desc));
      row.appendChild(tx);
      var b = el('button','st-switch');
      b.type = 'button';
      b.setAttribute('role','switch');
      var knob = el('span','st-knob','');
      b.appendChild(knob);
      function paint(){
        b.setAttribute('aria-checked', get() ? 'true' : 'false');
        b.setAttribute('aria-label', label + ': ' + (get() ? 'on' : 'off'));
      }
      b.addEventListener('click', function(){ set(!get()); persist(); paint(); });
      paint();
      row.appendChild(b);
      row._repaint = paint;
      return row;
    }

    function section(title, hint){
      var s = el('section','st-section');
      s.appendChild(el('h2','st-sec-title', title));
      if(hint) s.appendChild(el('p','st-sec-hint', hint));
      stage.appendChild(s);
      return s;
    }

    /* ---------- 1. Appearance ---------- */
    var app = section('Appearance', 'How the Hub looks and moves.');
    /* density segmented */
    var drow = el('div','st-row');
    var dtx = el('div','st-row-tx');
    dtx.appendChild(el('span','st-row-label','Density'));
    dtx.appendChild(el('span','st-row-desc','Changes this page\u2019s spacing live.'));
    drow.appendChild(dtx);
    var seg = el('div','st-seg'); seg.setAttribute('role','group'); seg.setAttribute('aria-label','Density');
    ['comfortable','compact'].forEach(function(mode){
      var b = el('button','st-seg-btn' + (st.density===mode ? ' on' : ''), mode.charAt(0).toUpperCase()+mode.slice(1));
      b.type='button'; b.setAttribute('aria-pressed', st.density===mode ? 'true':'false');
      b.addEventListener('click', function(){
        st.density = mode; persist(); applyGlobal();
        var btns = seg.querySelectorAll('.st-seg-btn');
        ['comfortable','compact'].forEach(function(m,i){
          btns[i].classList.toggle('on', m===mode);
          btns[i].setAttribute('aria-pressed', m===mode ? 'true':'false');
        });
      });
      seg.appendChild(b);
    });
    drow.appendChild(seg);
    app.appendChild(drow);
    /* reduce motion */
    var motionRow = switchRow('Reduce motion',
      'Disables animations on this page.',
      function(){ return st.reduceMotion; },
      function(v){ st.reduceMotion = v; applyGlobal(); });
    app.appendChild(motionRow);

    /* ---------- 2. Stream ---------- */
    var str = section('Stream', 'A local demo of the Living Intel stream setting. No network.');
    var beat = { n:0, timer:null };
    var erow = el('div','st-ekg-wrap');
    var svgNS = 'http://www.w3.org/2000/svg';
    var svg = document.createElementNS(svgNS,'svg');
    svg.setAttribute('viewBox','0 0 300 70'); svg.setAttribute('class','st-ekg');
    var pl = document.createElementNS(svgNS,'polyline');
    pl.setAttribute('points','0,35 40,35 55,35 62,20 70,50 78,28 86,35 130,35 145,35 152,20 160,50 168,28 176,35 220,35 235,35 242,20 250,50 258,28 266,35 300,35');
    pl.setAttribute('class','st-ekg-line');
    svg.appendChild(pl);
    erow.appendChild(svg);
    var estatus = el('div','st-ekg-side');
    var estate = el('span','st-ekg-state','BEATING'); estatus.appendChild(estate);
    var ecount = el('span','st-ekg-count','0 beats'); estatus.appendChild(ecount);
    erow.appendChild(estatus);
    str.appendChild(erow);
    function startBeat(){
      stopBeat();
      erow.classList.remove('st-paused');
      estate.textContent = 'BEATING';
      beat.timer = setInterval(function(){
        beat.n++;
        ecount.textContent = beat.n + (beat.n===1 ? ' beat' : ' beats');
        erow.classList.remove('st-beat'); void erow.offsetWidth; erow.classList.add('st-beat');
      }, 1200);
    }
    function stopBeat(){
      if(beat.timer){ clearInterval(beat.timer); beat.timer = null; }
      erow.classList.add('st-paused');
      estate.textContent = 'PAUSED';
    }
    var srow = switchRow('Simulated live',
      'Starts / stops the demo heartbeat above.',
      function(){ return st.simLive; },
      function(v){ st.simLive = v; if(v) startBeat(); else stopBeat(); });
    str.appendChild(srow);
    if(st.simLive) startBeat(); else stopBeat();

    /* ---------- 3. Privacy ---------- */
    var priv = section('Privacy', 'What the Hub shows about you.');
    var idcard = el('div','st-idcard');
    var avatar = el('span','st-avatar','SV');
    idcard.appendChild(avatar);
    var idtx = el('div','st-idtx');
    idtx.appendChild(el('span','st-id-label','IDENTITY'));
    var idname = el('span','st-id-name','');
    idtx.appendChild(idname);
    idcard.appendChild(idtx);
    priv.appendChild(idcard);
    function paintIdentity(){
      idname.textContent = st.maskIdentity ? masked(userName) : userName;
    }
    var prow = switchRow('Mask identity',
      'Masks your name on this page\u2019s identity card (local demo).',
      function(){ return st.maskIdentity; },
      function(v){ st.maskIdentity = v; paintIdentity(); });
    priv.appendChild(prow);
    paintIdentity();

    /* ---------- 4. Notifications ---------- */
    var notif = section('Notifications', 'What the Hub tells you about.');
    var summary = el('p','st-notif-sum','');
    function paintSummary(){
      var n = [st.notifReports, st.notifBuilds, st.notifMentions].filter(Boolean).length;
      summary.textContent = n + ' of 3 on';
    }
    [['Reports ready', function(){return st.notifReports;}, function(v){st.notifReports=v;}],
     ['Build events', function(){return st.notifBuilds;}, function(v){st.notifBuilds=v;}],
     ['Lane mentions', function(){return st.notifMentions;}, function(v){st.notifMentions=v;}]
    ].forEach(function(cfg){
      var r = switchRow(cfg[0], '', cfg[1], function(v){ cfg[2](v); paintSummary(); });
      notif.appendChild(r);
    });
    notif.appendChild(summary);
    paintSummary();

    /* ---------- 5. About ---------- */
    var about = section('About', 'This build, read-only.');
    var kv = el('div','st-kv');
    [['Hub version','0.4.0-candidate'],
     ['Rooms in this build', String(ROOMS.length)],
     ['Branch','naya4/room-02-reports-v2'],
     ['Settings store','localStorage \u00B7 naya.settings']
    ].forEach(function(pair){
      var r = el('div','st-kv-row');
      r.appendChild(el('span','st-kv-k', pair[0]));
      var v = el('span','st-kv-v',''); v.textContent = pair[1]; r.appendChild(v);
      kv.appendChild(r);
    });
    about.appendChild(kv);
    var reset = el('button','st-reset','Reset all settings');
    reset.type = 'button';
    var armed = false, armTimer = null;
    reset.addEventListener('click', function(){
      if(!armed){
        armed = true;
        reset.textContent = 'Tap again to confirm reset';
        reset.classList.add('armed');
        armTimer = setTimeout(function(){
          armed = false; reset.textContent = 'Reset all settings'; reset.classList.remove('armed');
        }, 4000);
        return;
      }
      clearTimeout(armTimer);
      try { localStorage.removeItem(STORE_KEY); } catch(e){}
      st = load(); /* back to defaults */
      /* repaint everything live */
      applyGlobal();
      paintIdentity();
      paintSummary();
      var btns = seg.querySelectorAll('.st-seg-btn');
      ['comfortable','compact'].forEach(function(m,i){
        btns[i].classList.toggle('on', m===st.density);
        btns[i].setAttribute('aria-pressed', m===st.density ? 'true':'false');
      });
      if(st.simLive) startBeat(); else stopBeat();
      /* repaint each switch via stored order */
      repaintSwitches();
      armed = false; reset.textContent = 'Reset all settings'; reset.classList.remove('armed');
      reset.textContent = 'Settings reset \u2713';
      setTimeout(function(){ reset.textContent = 'Reset all settings'; }, 1800);
    });
    about.appendChild(reset);

    /* repaint all switches (used after reset) */
    var switchRepaints = [];
    function repaintSwitches(){ switchRepaints.forEach(function(f){ f(); }); }
    /* collect repaint fns from rows already built */
    [motionRow, srow, prow].forEach(function(r){ if(r._repaint) switchRepaints.push(r._repaint); });
    notif.querySelectorAll('.st-row').forEach(function(r){ if(r._repaint) switchRepaints.push(r._repaint); });

    applyGlobal();

    var foot = el('footer','st-foot','');
    foot.textContent = 'settings are local to this device \u00B7 slate is the control color';
    stage.appendChild(foot);
    return stage;
  }

  window.NayaRooms = window.NayaRooms || {};
  window.NayaRooms.settings = SettingsRoom;
})();
