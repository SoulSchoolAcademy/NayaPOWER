/* NAYA-4 ROOMS CORE · shared store, receipts, hash routing, hub actions.
   Separate classic script AFTER the Hub scripts: sees top-level consts
   (state, save, esc, NOTES) via the global lexical environment. */
window.NayaHub = (function(){
  var K = 'nayanet_hub_v1';
  var d;
  try { d = JSON.parse(localStorage.getItem(K) || '{}'); } catch(e){ d = {}; }
  d.receipts = d.receipts || []; d.collections = d.collections || [];
  d.spaces = d.spaces || []; d.prefs = d.prefs || {};
  d.requests = d.requests || []; d.mail = d.mail || {};
  function w(){ try{ localStorage.setItem(K, JSON.stringify(d)); }catch(e){} }
  function uid(p){ return (p||'id') + '-' + Date.now().toString(36) + Math.floor(Math.random()*46656).toString(36); }
  function hts(t){ try{ return new Date(t).toLocaleString([], {month:'short', day:'numeric', hour:'numeric', minute:'2-digit'}); }catch(e){ return String(t); } }
  function esc(s){ return String(s == null ? '' : s).replace(/[&<>"']/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]; }); }
  function fhash(s){
    var h1 = 0x811c9dc5;
    for (var i = 0; i < s.length; i++){ h1 ^= s.charCodeAt(i); h1 = Math.imul(h1, 0x01000193) >>> 0; }
    return 'f' + h1.toString(16);
  }
  function sha(s, cb){
    function done(h){ try{ cb(h); }catch(e){} }
    try{
      if (window.crypto && crypto.subtle && window.isSecureContext !== false){
        crypto.subtle.digest('SHA-256', new TextEncoder().encode(s)).then(function(b){
          var h = '';
          new Uint8Array(b).forEach(function(x){ h += ('0' + x.toString(16)).slice(-2); });
          done(h.slice(0, 32));
        }).catch(function(){ done(fhash(s)); });
        return;
      }
    }catch(e){}
    done(fhash(s));
  }
  function receipt(action, detail, cb){
    var prev = d.receipts.length ? d.receipts[d.receipts.length - 1].hash : 'GENESIS';
    var ts = new Date().toISOString();
    sha(prev + '|' + ts + '|' + action + '|' + String(detail || ''), function(hash){
      d.receipts.push({ id:'rcpt-' + String(hash).slice(0,8), ts:ts, actor:'Shawn · local session',
        action:String(action), detail:String(detail || '').slice(0, 280), prev:prev, hash:hash });
      w();
      if (cb) cb();
    });
  }
  function rerender(){
    var a = document.querySelector('.naya-intelligence-nav [data-page].active');
    if (a){ a.click(); return; }
    var wEl = document.getElementById('nayaIntelligenceWorkspace');
    if (wEl) wEl.innerHTML = '';
  }
  function download(name, text){
    try{
      var b = new Blob([text], {type:'application/json'});
      var u = URL.createObjectURL(b);
      var l = document.createElement('a');
      l.href = u; l.download = name;
      document.body.appendChild(l); l.click();
      setTimeout(function(){ URL.revokeObjectURL(u); l.remove(); }, 500);
    }catch(e){}
  }
  return { d:d, w:w, uid:uid, hts:hts, esc:esc, receipt:receipt, rerender:rerender, download:download, sha:sha };
})();

/* Hub action dispatch: every [data-hub-action] in room HTML lands here. */
window.HubActions = {
  'report-range': function(t){ NayaHub.d.prefs.reportRange = t.getAttribute('data-v'); NayaHub.w(); NayaHub.rerender(); },
  'lib-facet': function(t){
    NayaHub.d.prefs.libFacet = t.getAttribute('data-v'); NayaHub.w(); NayaHub.rerender();
    setTimeout(function(){ var q = document.getElementById('hubLibQ'); if (q){ q.focus(); q.setSelectionRange(q.value.length, q.value.length); } }, 80);
  },
  'lib-open': function(t){
    var i = parseInt(t.getAttribute('data-v'), 10);
    var bl = document.querySelectorAll('.block');
    var home = document.querySelector('[data-main-hub]');
    function go(){
      var b = bl[i];
      if (b){ b.scrollIntoView({behavior:'smooth', block:'start'}); }
    }
    if (home){ home.click(); setTimeout(go, 450); } else { go(); }
  },
  'req-access': function(t){
    var door = t.getAttribute('data-v');
    NayaHub.d.requests.push({ id:NayaHub.uid('req'), door:door, ts:new Date().toISOString() });
    NayaHub.w();
    NayaHub.receipt('connect.request', 'Access requested: ' + door, function(){ NayaHub.rerender(); });
  },
  'conn-request': function(t){
    var who = t.getAttribute('data-v');
    NayaHub.d.requests.push({ id:NayaHub.uid('req'), door:who, ts:new Date().toISOString() });
    NayaHub.w();
    NayaHub.receipt('connections.request', 'Connection requested: ' + who, function(){ NayaHub.rerender(); });
  },
  'ledger-verify': function(){
    var box = document.getElementById('hubVerify');
    var rs = NayaHub.d.receipts;
    if (!rs.length){ if (box){ box.className=''; box.textContent = 'Nothing to verify yet.'; } return; }
    var prev = 'GENESIS', i = 0;
    function step(){
      if (i >= rs.length){
        if (box){ box.className = 'ok'; box.textContent = 'CHAIN VALID · ' + rs.length + ' receipts · every link verified.'; }
        return;
      }
      var r = rs[i];
      if (r.prev !== prev){ if (box){ box.className = 'bad'; box.textContent = 'CHAIN BROKEN at ' + r.id + ' — prev link mismatch.'; } return; }
      NayaHub.sha(r.prev + '|' + r.ts + '|' + r.action + '|' + r.detail, function(h){
        if (h !== r.hash){ if (box){ box.className = 'bad'; box.textContent = 'CHAIN BROKEN at ' + r.id + ' — hash mismatch.'; } return; }
        prev = r.hash; i++; step();
      });
    }
    if (box){ box.className=''; box.textContent = 'Verifying…'; }
    step();
  },
  'hub-export': function(){
    var payload = { exported_at:new Date().toISOString(), hub:NayaHub.d,
      feed_actions:(function(){ try{ return JSON.parse(localStorage.getItem('nayanet_509_aaa') || '{}'); }catch(e){ return {}; } })(),
      notes:(function(){ try{ return JSON.parse(localStorage.getItem('nayanet_v7_live_notes') || '[]'); }catch(e){ return []; } })() };
    NayaHub.download('nayanet-hub-data.json', JSON.stringify(payload, null, 2));
    NayaHub.receipt('hub.export', 'Hub data exported by Shawn');
  },
  'hub-clear': function(){
    if (!window.confirm('Erase ALL local Hub data (saves, favorites, notes, receipts, collections)? This cannot be undone.')) return;
    ['nayanet_hub_v1','nayanet_509_aaa','nayanet_v7_live_notes'].forEach(function(k){ try{ localStorage.removeItem(k); }catch(e){} });
    location.reload();
  },
  'mail-check': function(){ NayaHub.rerender(); NayaHub.receipt('mail.check', 'Mailbox re-checked · still no mail'); },
  'space-create': function(){
    var inp = document.getElementById('hubSpaceName');
    var name = inp && inp.value.trim();
    if (!name) return;
    NayaHub.d.spaces.push({ id:NayaHub.uid('sp'), name:name, rule:'SHARED BY CHOICE', color:'#b8ee57', desc:'Created by Shawn.', custom:true });
    NayaHub.w();
    NayaHub.receipt('spaces.create', 'Space created: ' + name, function(){ NayaHub.rerender(); });
  },
  'list-tab': function(t){ NayaHub.d.prefs.listTab = t.getAttribute('data-v'); NayaHub.w(); NayaHub.rerender(); },
  'item-unsave': function(t){
    var kind = t.getAttribute('data-k'), id = t.getAttribute('data-v');
    try{
      var st = JSON.parse(localStorage.getItem('nayanet_509_aaa') || '{}');
      if (st[kind]){ delete st[kind][id]; localStorage.setItem('nayanet_509_aaa', JSON.stringify(st)); }
    }catch(e){}
    NayaHub.receipt('lists.remove', kind + ' removed: ' + id, function(){ NayaHub.rerender(); });
  },
  'col-create': function(){
    var inp = document.getElementById('hubColName');
    var name = inp && inp.value.trim();
    if (!name) return;
    NayaHub.d.collections.push({ id:NayaHub.uid('col'), name:name, items:[] });
    NayaHub.w();
    NayaHub.receipt('lists.collection.create', name, function(){ NayaHub.rerender(); });
  },
  'col-delete': function(t){
    var id = t.getAttribute('data-v');
    NayaHub.d.collections = NayaHub.d.collections.filter(function(c){ return c.id !== id; });
    NayaHub.w(); NayaHub.rerender();
  },
  'col-add': function(t){
    var cid = t.getAttribute('data-c');
    var sel = document.getElementById('hubColPick-' + cid);
    if (!sel || !sel.value) return;
    var col = NayaHub.d.collections.filter(function(c){ return c.id === cid; })[0];
    if (!col) return;
    var ref = sel.value, title = sel.options[sel.selectedIndex].text;
    if (!col.items.some(function(x){ return x.ref === ref; })){ col.items.push({ ref:ref, title:title }); }
    NayaHub.w();
    NayaHub.receipt('lists.collection.add', col.name + ' ← ' + title.slice(0, 60), function(){ NayaHub.rerender(); });
  },
  'col-remove': function(t){
    var cid = t.getAttribute('data-c'), ref = t.getAttribute('data-v');
    var col = NayaHub.d.collections.filter(function(c){ return c.id === cid; })[0];
    if (!col) return;
    col.items = col.items.filter(function(x){ return x.ref !== ref; });
    NayaHub.w(); NayaHub.rerender();
  },
  'note-save': function(){
    var title = (document.getElementById('hubNoteTitle') || {}).value || '';
    var text = (document.getElementById('hubNoteText') || {}).value || '';
    var type = (document.getElementById('hubNoteType') || {}).value || 'INSIGHT';
    var st = document.getElementById('hubNoteStatus');
    function say(m){ if (st) st.textContent = m; }
    if (!text.trim()){ say('Write the note first — empty captures are not kept.'); return; }
    var rt = null;
    try{ rt = window.NayaAssistantRuntime || null; }catch(e){}
    function localSave(){
      var arr = [];
      try{ arr = JSON.parse(localStorage.getItem('nayanet_v7_live_notes') || '[]'); }catch(e){}
      var rec = { id:'note-' + Date.now().toString(36), text:(title.trim() ? title.trim() + ' — ' : '') + text.trim(), type:type, createdAt:new Date().toISOString(), space:'personal' };
      arr.unshift(rec);
      try{ localStorage.setItem('nayanet_v7_live_notes', JSON.stringify(arr)); }catch(e){}
      NayaHub.receipt('notes.capture', '“' + String(rec.text).slice(0, 80) + '”', function(){
        say('CAPTURED · stored locally · receipted in the Ledger.');
        setTimeout(function(){ NayaHub.rerender(); }, 900);
      });
    }
    if (rt && typeof rt.captureSmartNote === 'function'){
      say('Capturing through the governed runtime…');
      rt.captureSmartNote({ title:title.trim(), content:text.trim(), source:'nayanet-hub.smart-notes' }).then(function(out){
        var eid = (out && (out.event_id || (out.event || {}).event_id)) || 'runtime';
        NayaHub.receipt('notes.capture', 'runtime · ' + eid, function(){
          say('CAPTURED · ' + eid + ' · receipted in the Ledger.');
          setTimeout(function(){ NayaHub.rerender(); }, 900);
        });
      }).catch(function(){ say('Runtime refused — saving locally instead.'); localSave(); });
    } else {
      say('Runtime not exposed — LOCAL CAPTURE · stored in this browser, receipted.');
      localSave();
    }
  }
};

/* Delegated events for hub actions + hub inputs + hub checks. */
(function(){
  document.addEventListener('click', function(e){
    var t = e.target && e.target.closest ? e.target.closest('[data-hub-action]') : null;
    if (!t) return;
    var fn = window.HubActions[t.getAttribute('data-hub-action')];
    if (typeof fn === 'function'){ e.preventDefault(); try{ fn(t, e); }catch(err){} }
  });
  var deb = null;
  document.addEventListener('input', function(e){
    var t = e.target && e.target.getAttribute ? e.target.getAttribute('data-hub-input') : null;
    if (!t) return;
    if (t === 'lib-q'){
      clearTimeout(deb);
      deb = setTimeout(function(){
        NayaHub.d.prefs.libQ = document.getElementById('hubLibQ').value;
        NayaHub.w();
        var pos = document.getElementById('hubLibQ').selectionStart;
        NayaHub.rerender();
        setTimeout(function(){
          var q = document.getElementById('hubLibQ');
          if (q){ q.focus(); try{ q.setSelectionRange(pos, pos); }catch(x){} }
        }, 60);
      }, 280);
    }
  });
  document.addEventListener('change', function(e){
    var t = e.target && e.target.getAttribute ? e.target.getAttribute('data-hub-check') : null;
    if (!t) return;
    if (t === 'mail-notify'){ NayaHub.d.mail.notify = !!e.target.checked; NayaHub.w(); }
  });

  /* Wrap the feed action() so marks become ledger receipts. */
  try{
    if (typeof window.action === 'function' && !window.action.__hubWrapped){
      (function(orig){
        window.action = function(act, id){
          var r = orig.apply(this, arguments);
          try{
            if (['save','favorite','love','like'].indexOf(act) >= 0){
              var st = {};
              try{ st = JSON.parse(localStorage.getItem('nayanet_509_aaa') || '{}'); }catch(x){}
              var map = { save:'saved', favorite:'favorites', love:'loves', like:'likes' };
              var on = !!((st[map[act]] || {})[id]);
              NayaHub.receipt('feed.' + act, '“' + String(id) + '” ' + (on ? 'marked' : 'unmarked'));
            }
          }catch(x){}
          return r;
        };
        window.action.__hubWrapped = true;
      })(window.action);
    }
  }catch(e){}

  /* Hash routing: each room owns an address (#/today …). Reflect + follow. */
  var PAGES = ['today','reports','library','share','ledger','connections','lists','mail','spaces','settings','notes'];
  function fromHash(){
    var h = (location.hash || '').replace(/^#\/?/, '');
    if (PAGES.indexOf(h) >= 0){
      var b = document.querySelector('.naya-intelligence-nav [data-page="' + h + '"]');
      if (b && !b.classList.contains('active')){ b.click(); }
    }
  }
  if (document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', function(){ setTimeout(fromHash, 600); setTimeout(fromHash, 1700); });
  } else { setTimeout(fromHash, 600); }
  window.addEventListener('hashchange', fromHash);
  function watchNav(){
    var nav = document.querySelector('.naya-intelligence-nav');
    if (!nav){ setTimeout(watchNav, 500); return; }
    new MutationObserver(function(){
      var a = nav.querySelector('[data-page].active');
      if (a){
        var h = '#/' + a.getAttribute('data-page');
        if (location.hash !== h){ try{ history.replaceState(null, '', h); }catch(e){} }
      }
    }).observe(nav, { subtree:true, attributes:true, attributeFilter:['class'] });
  }
  watchNav();
})();
