/* NayaFunction: feed v1.0.0
   What: Living stream — composer posts to the stream; like and save, persisted.
   Activation: <div data-fn="feed" data-fn-config='{...}'></div>
   Config: {
     seed: [{id, author, text, ts, likes}]  opening posts, loaded once
     storageKey: localStorage key (default 'naya.feed.v1')
     title: heading text (default 'Feed')
   } — all optional.
   Ready behavior: composer → post appears at the top; like toggles with a count;
     save toggles and the All/Saved filter shows saved posts; delete removes your
     post. Everything persists in localStorage, zero backend.
   Connected behavior: none — the `connected` key is reserved. Connecting a network
     would stream other people's posts; until then the stream is this device's own.
   Backend twin: builder-review/HUB/design-system/tools/smart-builder/functions/feature_social_feed.py
     (noted here only — this unit is fully client-side and never calls it).
   Consent line: copy states the stream lives on this device and connecting a
     network would bring other people's posts — ready vs connected never conflated.
   Lesson L-2026-10-17-004: every control below is bound to DOM this unit creates.
*/
(function(){
'use strict';
var NF = window.NayaFunctions = window.NayaFunctions || {};
NF._r = NF._r || {};
NF.register = NF.register || function(id, def){
  if (NF._r[id]) return;
  NF._r[id] = def;
};

var UNIT = 'feed';
var UNIT_COLOR = '#ff9a5a'; /* Law 9 token — one color job per unit */

function storeGet(key, fallback){
  try {
    var raw = window.localStorage.getItem(key);
    if (raw == null) return fallback;
    var v = JSON.parse(raw);
    return Array.isArray(v) ? v : fallback;
  } catch(e){ return fallback; }
}
function storeSet(key, val){
  try { window.localStorage.setItem(key, JSON.stringify(val)); return true; }
  catch(e){ return false; }
}
function uid(prefix){ return prefix + '-' + Date.now().toString(36) + '-' + Math.floor(Math.random()*1e6).toString(36); }
function relTime(ts){
  var s = Math.max(0, Math.floor((Date.now() - ts) / 1000));
  if (s < 60) return 'just now';
  var m = Math.floor(s / 60);
  if (m < 60) return m + 'm ago';
  var hh = Math.floor(m / 60);
  if (hh < 24) return hh + 'h ago';
  var d = Math.floor(hh / 24);
  return d + 'd ago';
}
function cssOnce(){
  if (document.querySelector('style[data-nf-css="feed"]')) return;
  var st = document.createElement('style');
  st.setAttribute('data-nf-css','feed');
  st.textContent = [
    '.nf-feed{font-family:Inter,system-ui,sans-serif;color:#fff;background:#0a0a0d;',
    ' border:1px solid rgba(255,255,255,.14);border-radius:14px;padding:14px 16px;',
    ' box-shadow:0 10px 30px rgba(0,0,0,.55), inset 0 1px 0 rgba(255,255,255,.06);}',
    '.nf-feed h3{margin:0 0 4px;font-size:18px;font-weight:700;color:#fff;}',
    '.nf-feed .nf-sub{font-size:14px;color:#fff;opacity:.75;margin:0 0 12px;}',
    '.nf-composer textarea{width:100%;box-sizing:border-box;background:#141419;color:#fff;',
    ' border:1px solid rgba(255,255,255,.25);border-radius:8px;padding:10px;font-size:14px;',
    ' min-height:80px;font-family:inherit;resize:vertical;}',
    '.nf-composer textarea:focus{outline:none;border-color:' + UNIT_COLOR + ';}',
    '.nf-feed .nf-rowbtns{display:flex;gap:8px;margin:10px 0 4px;flex-wrap:wrap;}',
    '.nf-btn{background:#141419;color:#fff;border:1.5px solid rgba(255,255,255,.35);',
    ' border-radius:10px;padding:10px 14px;font-size:14px;min-height:44px;cursor:pointer;}',
    '.nf-btn:hover{border-color:' + UNIT_COLOR + ';box-shadow:0 0 14px -4px ' + UNIT_COLOR + ';}',
    '.nf-feedtabs{display:flex;gap:8px;margin:8px 0;}',
    '.nf-feedtab{background:#101014;color:#fff;border:1.5px solid rgba(255,255,255,.35);',
    ' border-radius:999px;padding:8px 16px;font-size:14px;min-height:44px;cursor:pointer;}',
    '.nf-feedtab.active{border-color:' + UNIT_COLOR + ';box-shadow:0 0 14px -4px ' + UNIT_COLOR + ';}',
    '.nf-post{border:1px solid rgba(255,255,255,.14);border-radius:10px;padding:12px 14px;',
    ' margin:10px 0;background:#0d0d11;}',
    '.nf-post .pa{font-size:18px;font-weight:700;color:#fff;margin:0;}',
    '.nf-post .pt{font-size:14px;color:#fff;opacity:.6;margin:0 0 6px;}',
    '.nf-post .px{font-size:14px;color:#fff;margin:0 0 10px;white-space:pre-wrap;word-break:break-word;}',
    '.nf-post .pacts{display:flex;gap:8px;flex-wrap:wrap;}',
    '.nf-pact{background:none;border:1.5px solid rgba(255,255,255,.3);color:#fff;',
    ' border-radius:999px;padding:8px 14px;font-size:14px;min-height:44px;cursor:pointer;}',
    '.nf-pact:hover{border-color:' + UNIT_COLOR + ';}',
    '.nf-pact.on{border-color:' + UNIT_COLOR + ';box-shadow:0 0 12px -4px ' + UNIT_COLOR + ';}',
    '.nf-feed .nf-status{font-size:14px;color:#fff;opacity:.85;margin:10px 2px 0;min-height:20px;}',
    '.nf-feed .nf-empty{font-size:14px;color:#fff;opacity:.6;padding:18px 4px;}',
    '.nf-consent{font-size:14px;color:#fff;opacity:.6;margin:10px 0 0;}'
  ].join('\n');
  document.head.appendChild(st);
}

NF.register(UNIT, {
  version: '1.0.0',
  activate: function(root, config){
    config = config || {};
    if (!root) return { destroy: function(){} };
    cssOnce();
    var key = config.storageKey || 'naya.feed.v1';
    var listeners = [];
    function on(el, ev, fn){ el.addEventListener(ev, fn); listeners.push([el, ev, fn]); }

    var posts = storeGet(key, null);
    if (!Array.isArray(posts)) {
      posts = Array.isArray(config.seed) ? JSON.parse(JSON.stringify(config.seed)) : [];
      posts.forEach(function(p){
        p.id = p.id || uid('post');
        p.likes = p.likes || 0;
        p.liked = false; p.saved = false;
        p.ts = p.ts || Date.now();
        p.mine = false;
      });
      storeSet(key, posts);
    }
    var filter = 'all';
    var timer = null;

    root.innerHTML = '';
    var wrap = document.createElement('div');
    wrap.className = 'nf-feed';
    var h = document.createElement('h3');
    h.textContent = config.title || 'Feed';
    wrap.appendChild(h);
    var sub = document.createElement('p');
    sub.className = 'nf-sub';
    sub.textContent = 'What\u2019s alive in your world — post it, keep what matters.';
    wrap.appendChild(sub);
    var composer = document.createElement('div');
    composer.className = 'nf-composer';
    var ta = document.createElement('textarea');
    ta.placeholder = 'Share something…';
    ta.setAttribute('aria-label','New post text');
    composer.appendChild(ta);
    var crow = document.createElement('div'); crow.className = 'nf-rowbtns';
    var postBtn = document.createElement('button');
    postBtn.type = 'button'; postBtn.className = 'nf-btn primary'; postBtn.textContent = 'Post';
    crow.appendChild(postBtn);
    composer.appendChild(crow);
    wrap.appendChild(composer);
    var ftabs = document.createElement('div');
    ftabs.className = 'nf-feedtabs';
    wrap.appendChild(ftabs);
    var stream = document.createElement('div');
    wrap.appendChild(stream);
    var status = document.createElement('p');
    status.className = 'nf-status';
    status.setAttribute('aria-live','polite');
    wrap.appendChild(status);
    var consent = document.createElement('p');
    consent.className = 'nf-consent';
    consent.textContent = 'Ready now: this stream lives on this device. Connect a network to see other people\u2019s posts (connected is off).';
    wrap.appendChild(consent);
    root.appendChild(wrap);

    function say(msg){ status.textContent = msg; }
    function persist(){ storeSet(key, posts); }

    on(postBtn, 'click', function(){
      var text = ta.value.trim();
      if (!text) { say('Write something first — the feed stays honest, not empty.'); ta.focus(); return; }
      posts.unshift({ id: uid('post'), author: 'You', text: text, ts: Date.now(), likes: 0, liked: false, saved: false, mine: true });
      ta.value = '';
      persist(); render();
      say('Posted — it\u2019s live in your stream.');
    });

    function postCard(p){
      var d = document.createElement('div');
      d.className = 'nf-post';
      d.setAttribute('data-id', p.id);
      var a = document.createElement('p'); a.className = 'pa'; a.textContent = p.author || 'Someone';
      var t = document.createElement('p'); t.className = 'pt'; t.textContent = relTime(p.ts);
      var x = document.createElement('p'); x.className = 'px'; x.textContent = p.text || '';
      var acts = document.createElement('div'); acts.className = 'pacts';
      var like = document.createElement('button');
      like.type = 'button';
      like.className = 'nf-pact' + (p.liked ? ' on' : '');
      like.textContent = (p.liked ? '♥ ' : '♡ ') + (p.likes || 0);
      like.setAttribute('aria-label','Like this post');
      on(like, 'click', function(){
        p.liked = !p.liked;
        p.likes = Math.max(0, (p.likes || 0) + (p.liked ? 1 : -1));
        persist(); render();
      });
      var save = document.createElement('button');
      save.type = 'button';
      save.className = 'nf-pact' + (p.saved ? ' on' : '');
      save.textContent = p.saved ? '★ Saved' : '☆ Save';
      save.setAttribute('aria-label','Save this post');
      on(save, 'click', function(){
        p.saved = !p.saved;
        persist(); render();
        say(p.saved ? 'Saved — find it under Saved.' : 'Unsaved.');
      });
      acts.appendChild(like); acts.appendChild(save);
      if (p.mine) {
        var del = document.createElement('button');
        del.type = 'button'; del.className = 'nf-pact'; del.textContent = 'Delete';
        del.setAttribute('aria-label','Delete this post');
        on(del, 'click', function(){
          posts = posts.filter(function(q){ return q.id !== p.id; });
          persist(); render();
          say('Post deleted.');
        });
        acts.appendChild(del);
      }
      d.appendChild(a); d.appendChild(t); d.appendChild(x); d.appendChild(acts);
      return d;
    }

    function render(){
      ftabs.innerHTML = '';
      [['all','All'],['saved','Saved']].forEach(function(f){
        var b = document.createElement('button');
        b.type = 'button';
        b.className = 'nf-feedtab' + (filter === f[0] ? ' active' : '');
        b.textContent = f[1] + (f[0] === 'saved' ? ' (' + posts.filter(function(p){ return p.saved; }).length + ')' : '');
        on(b, 'click', function(){ filter = f[0]; render(); });
        ftabs.appendChild(b);
      });
      stream.innerHTML = '';
      var shown = filter === 'saved' ? posts.filter(function(p){ return p.saved; }) : posts;
      if (!shown.length) {
        var e = document.createElement('p'); e.className = 'nf-empty';
        e.textContent = filter === 'saved' ? 'Nothing saved yet — tap ☆ Save on a post to keep it.' : 'No posts yet — be the first to share something.';
        stream.appendChild(e); return;
      }
      shown.forEach(function(p){ stream.appendChild(postCard(p)); });
    }

    render();
    say('Composer is live — post to begin.');
    timer = setInterval(function(){ /* refresh relative times; deterministic render, no content change */
      var times = stream.querySelectorAll('.nf-post .pt');
      var cards = stream.querySelectorAll('.nf-post');
      for (var i = 0; i < cards.length; i++) {
        var id = cards[i].getAttribute('data-id');
        for (var j = 0; j < posts.length; j++) if (posts[j].id === id) { times[i].textContent = relTime(posts[j].ts); break; }
      }
    }, 60000);

    return {
      destroy: function(){
        if (timer) clearInterval(timer);
        listeners.forEach(function(l){ try { l[0].removeEventListener(l[1], l[2]); } catch(e){} });
        root.innerHTML = '';
      }
    };
  }
});
})();
