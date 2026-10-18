/* NayaFunction: smart-spaces v1.0.0
   What: Create and join smart spaces — space cards with live member counts.
   Activation: <div data-fn="smart-spaces" data-fn-config='{...}'></div>
   Config: {
     spaces: [{id, name, topic, desc, color, privacy, members: [names]}]  seed spaces
     storageKey: localStorage key for created spaces + joins (default 'naya.smartspaces.v1')
     title: heading text (default 'Smart Spaces')
   } — all optional.
   Ready behavior: space cards render from config + locally created spaces; Join/Leave
     toggles membership and updates the member count; Create Space opens the real
     create form (name, topic, description, privacy, cover color) and adds the card.
     All on this device, zero backend.
   Connected behavior: none — the `connected` key is reserved. Connecting would sync
     spaces and members across devices; until then membership lives on this device.
   Backend twin: builder-review/HUB/design-system/tools/smart-builder/functions/feature_space.py
     (noted here only — this unit is fully client-side and never calls it).
   Harvest-adapted: Smart_Spaces_Page_Design.html (join toggle with count update,
     create modal with topic row, privacy row, color swatches).
   Consent line: copy states spaces and membership live on this device; browsing and
     joining are free; connecting syncs them — ready vs connected never conflated.
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

var UNIT = 'smart-spaces';
var UNIT_COLOR = '#a06bff'; /* Law 9 token — one color job per unit */
var TOPICS = ['Start Here','Vision','Learn','Create','Connect','Grow','General']; /* harvested */
var SWATCHES = ['#e84fff','#a06bff','#3fb8ff','#2fe89e','#ffbf3d','#40d3bb','#6675ff','#ff9a5a']; /* Law 9 tokens */

function storeGet(key, fallback){
  try {
    var raw = window.localStorage.getItem(key);
    if (raw == null) return fallback;
    return JSON.parse(raw);
  } catch(e){ return fallback; }
}
function storeSet(key, val){
  try { window.localStorage.setItem(key, JSON.stringify(val)); return true; }
  catch(e){ return false; }
}
function uid(prefix){ return prefix + '-' + Date.now().toString(36) + '-' + Math.floor(Math.random()*1e6).toString(36); }
function cssOnce(){
  if (document.querySelector('style[data-nf-css="smart-spaces"]')) return;
  var st = document.createElement('style');
  st.setAttribute('data-nf-css','smart-spaces');
  st.textContent = [
    '.nf-spaces{font-family:Inter,system-ui,sans-serif;color:#fff;background:#0a0a0d;',
    ' border:1px solid rgba(255,255,255,.14);border-radius:14px;padding:14px 16px;',
    ' box-shadow:0 10px 30px rgba(0,0,0,.55), inset 0 1px 0 rgba(255,255,255,.06);}',
    '.nf-spaces h3{margin:0 0 4px;font-size:18px;font-weight:700;color:#fff;}',
    '.nf-spaces .nf-sub{font-size:14px;color:#fff;opacity:.75;margin:0 0 12px;}',
    '.nf-space{border:1px solid rgba(255,255,255,.14);border-radius:12px;margin:10px 0;',
    ' background:#0d0d11;overflow:hidden;box-shadow:0 6px 20px rgba(0,0,0,.5);}', /* Law 7 rectangles */
    '.nf-space .cover{height:8px;background:var(--sc);box-shadow:0 0 16px -2px var(--sc);}',
    '.nf-space .spbody{padding:12px 14px;}',
    '.nf-space .nm{font-size:18px;font-weight:700;color:#fff;margin:0 0 2px;}',
    '.nf-space .tp{font-size:14px;color:#fff;opacity:.7;margin:0 0 6px;}',
    '.nf-space .ds{font-size:14px;color:#fff;opacity:.9;margin:0 0 10px;}',
    '.nf-space .meta{display:flex;align-items:center;gap:12px;flex-wrap:wrap;}',
    '.nf-space .count{font-size:14px;color:#fff;opacity:.85;}',
    '.nf-join{background:#101014;color:#fff;border:1.5px solid rgba(255,255,255,.35);',
    ' border-radius:999px;padding:10px 18px;font-size:14px;min-height:44px;cursor:pointer;',
    ' transition:border-color .18s, box-shadow .18s;}',
    '.nf-join:hover{border-color:var(--sc);box-shadow:0 0 16px -4px var(--sc);}',
    '.nf-join.in{border-color:#2fe89e;box-shadow:0 0 14px -6px #2fe89e;}', /* green = proven membership */
    '.nf-btn{background:#141419;color:#fff;border:1.5px solid rgba(255,255,255,.35);',
    ' border-radius:10px;padding:10px 14px;font-size:14px;min-height:44px;cursor:pointer;}',
    '.nf-btn:hover{border-color:' + UNIT_COLOR + ';box-shadow:0 0 14px -4px ' + UNIT_COLOR + ';}',
    '.nf-create{display:none;border:1px solid rgba(255,255,255,.16);border-radius:10px;',
    ' padding:12px;margin-top:10px;background:#0d0d11;}',
    '.nf-create.open{display:block;}',
    '.nf-create label{display:block;font-size:14px;color:#fff;margin:8px 0 4px;}',
    '.nf-create input,.nf-create textarea{background:#141419;color:#fff;',
    ' border:1px solid rgba(255,255,255,.25);border-radius:8px;padding:10px;',
    ' font-size:14px;width:100%;box-sizing:border-box;font-family:inherit;}',
    '.nf-create textarea{min-height:64px;resize:vertical;}',
    '.nf-create input:focus,.nf-create textarea:focus{outline:none;border-color:' + UNIT_COLOR + ';}',
    '.nf-optrow{display:flex;gap:8px;flex-wrap:wrap;}',
    '.nf-opt{background:#101014;color:#fff;border:1.5px solid rgba(255,255,255,.35);',
    ' border-radius:999px;padding:8px 14px;font-size:14px;min-height:44px;cursor:pointer;}',
    '.nf-opt.on{border-color:' + UNIT_COLOR + ';box-shadow:0 0 12px -4px ' + UNIT_COLOR + ';}',
    '.nf-swatches{display:flex;gap:8px;flex-wrap:wrap;}',
    '.nf-sw{width:44px;height:44px;border-radius:50%;border:2px solid transparent;cursor:pointer;padding:0;}',
    '.nf-sw.on{border-color:#fff;box-shadow:0 0 12px -2px currentColor;}',
    '.nf-rowbtns{display:flex;gap:8px;margin-top:12px;flex-wrap:wrap;}',
    '.nf-spaces .nf-status{font-size:14px;color:#fff;opacity:.85;margin:10px 2px 0;min-height:20px;}',
    '.nf-spaces .nf-empty{font-size:14px;color:#fff;opacity:.6;padding:18px 4px;}',
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
    var key = config.storageKey || 'naya.smartspaces.v1';
    var listeners = [];
    function on(el, ev, fn){ el.addEventListener(ev, fn); listeners.push([el, ev, fn]); }

    var saved = storeGet(key, null) || {};
    var custom = Array.isArray(saved.custom) ? saved.custom : [];
    var mine = Array.isArray(saved.mine) ? saved.mine : [];
    var seeds = Array.isArray(config.spaces) ? config.spaces : [];

    root.innerHTML = '';
    var wrap = document.createElement('div');
    wrap.className = 'nf-spaces';
    var h = document.createElement('h3');
    h.textContent = config.title || 'Smart Spaces';
    wrap.appendChild(h);
    var sub = document.createElement('p');
    sub.className = 'nf-sub';
    sub.textContent = 'Until you create a smart space you have no connection — make one, join one.';
    wrap.appendChild(sub);
    var createBtn = document.createElement('button');
    createBtn.type = 'button'; createBtn.className = 'nf-btn primary';
    createBtn.textContent = '＋ Create Space';
    wrap.appendChild(createBtn);
    var form = document.createElement('div');
    form.className = 'nf-create';
    wrap.appendChild(form);
    var grid = document.createElement('div');
    wrap.appendChild(grid);
    var status = document.createElement('p');
    status.className = 'nf-status';
    status.setAttribute('aria-live','polite');
    wrap.appendChild(status);
    var consent = document.createElement('p');
    consent.className = 'nf-consent';
    consent.textContent = 'Ready now: spaces and membership live on this device — browsing and joining are free. Connect your account to sync spaces and members across devices (connected is off).';
    wrap.appendChild(consent);
    root.appendChild(wrap);

    function say(msg){ status.textContent = msg; }
    function persist(){ storeSet(key, { custom: custom, mine: mine }); }
    function allSpaces(){
      var out = custom.slice();
      seeds.forEach(function(s){ out.push(s); });
      return out;
    }
    function joined(id){ return mine.indexOf(id) >= 0; }
    function memberCount(s){
      var base = Array.isArray(s.members) ? s.members.length : 0;
      return base + (joined(s.id) ? 1 : 0);
    }

    function render(){
      grid.innerHTML = '';
      var spaces = allSpaces();
      if (!spaces.length) {
        var e = document.createElement('p'); e.className = 'nf-empty';
        e.textContent = 'No spaces yet — create the first one.';
        grid.appendChild(e); return;
      }
      spaces.forEach(function(s){
        var card = document.createElement('div');
        card.className = 'nf-space';
        card.style.setProperty('--sc', s.color || UNIT_COLOR);
        var cover = document.createElement('div'); cover.className = 'cover';
        var body = document.createElement('div'); body.className = 'spbody';
        var nm = document.createElement('p'); nm.className = 'nm'; nm.textContent = s.name || 'Untitled space';
        var tp = document.createElement('p'); tp.className = 'tp';
        tp.textContent = (s.topic || 'General') + (s.privacy === 'private' ? ' · 🔒 Private' : ' · Public');
        body.appendChild(nm); body.appendChild(tp);
        if (s.desc) { var ds = document.createElement('p'); ds.className = 'ds'; ds.textContent = s.desc; body.appendChild(ds); }
        var meta = document.createElement('div'); meta.className = 'meta';
        var count = document.createElement('span'); count.className = 'count';
        var n = memberCount(s);
        count.textContent = n + (n === 1 ? ' member' : ' members');
        var jbtn = document.createElement('button');
        jbtn.type = 'button';
        var isIn = joined(s.id);
        jbtn.className = 'nf-join' + (isIn ? ' in' : '');
        jbtn.textContent = isIn ? '✓ Joined' : '＋ Join';
        on(jbtn, 'click', function(){
          if (joined(s.id)) {
            mine = mine.filter(function(id){ return id !== s.id; });
            say('Left "' + s.name + '".');
          } else {
            mine.push(s.id);
            say('Welcome to "' + s.name + '" — you are member ' + memberCount(s) + '.');
          }
          persist(); render();
        });
        meta.appendChild(count); meta.appendChild(jbtn);
        body.appendChild(meta);
        card.appendChild(cover); card.appendChild(body);
        grid.appendChild(card);
      });
    }

    function openCreate(){
      form.classList.add('open');
      form.innerHTML = '';
      var title = document.createElement('p');
      title.style.cssText = 'margin:0 0 4px;font-size:18px;font-weight:700;color:#fff;';
      title.textContent = 'Create a Space';
      form.appendChild(title);
      function lab(t){ var l = document.createElement('label'); l.textContent = t; form.appendChild(l); return l; }
      lab('Name');
      var nameIn = document.createElement('input'); nameIn.placeholder = 'Space name (e.g. Design Crew)';
      form.appendChild(nameIn);
      lab('Topic');
      var topicRow = document.createElement('div'); topicRow.className = 'nf-optrow';
      var selTopic = TOPICS[0];
      TOPICS.forEach(function(t){
        var b = document.createElement('button');
        b.type = 'button'; b.className = 'nf-opt' + (t === selTopic ? ' on' : ''); b.textContent = t;
        on(b, 'click', function(){
          selTopic = t;
          var btns = topicRow.querySelectorAll('.nf-opt');
          for (var i = 0; i < btns.length; i++) btns[i].classList.remove('on');
          b.classList.add('on');
        });
        topicRow.appendChild(b);
      });
      form.appendChild(topicRow);
      lab('Description');
      var descIn = document.createElement('textarea'); descIn.placeholder = 'What is this space about?';
      form.appendChild(descIn);
      lab('Privacy');
      var privRow = document.createElement('div'); privRow.className = 'nf-optrow';
      var selPriv = 'public';
      [['public','🌐 Public'],['private','🔒 Private']].forEach(function(p){
        var b = document.createElement('button');
        b.type = 'button'; b.className = 'nf-opt' + (p[0] === selPriv ? ' on' : ''); b.textContent = p[1];
        on(b, 'click', function(){
          selPriv = p[0];
          var btns = privRow.querySelectorAll('.nf-opt');
          for (var i = 0; i < btns.length; i++) btns[i].classList.remove('on');
          b.classList.add('on');
        });
        privRow.appendChild(b);
      });
      form.appendChild(privRow);
      lab('Cover color');
      var swRow = document.createElement('div'); swRow.className = 'nf-swatches';
      var selColor = SWATCHES[0];
      SWATCHES.forEach(function(c){
        var sw = document.createElement('button');
        sw.type = 'button'; sw.className = 'nf-sw' + (c === selColor ? ' on' : '');
        sw.style.background = c; sw.style.color = c;
        sw.setAttribute('aria-label','Cover color ' + c);
        on(sw, 'click', function(){
          selColor = c;
          var sws = swRow.querySelectorAll('.nf-sw');
          for (var i = 0; i < sws.length; i++) sws[i].classList.remove('on');
          sw.classList.add('on');
        });
        swRow.appendChild(sw);
      });
      form.appendChild(swRow);
      var row = document.createElement('div'); row.className = 'nf-rowbtns';
      var cancel = document.createElement('button');
      cancel.type = 'button'; cancel.className = 'nf-btn'; cancel.textContent = 'Cancel';
      on(cancel, 'click', closeCreate);
      var create = document.createElement('button');
      create.type = 'button'; create.className = 'nf-btn primary'; create.textContent = 'Create Space';
      on(create, 'click', function(){
        var name = nameIn.value.trim();
        if (!name) { say('Give your space a name.'); nameIn.focus(); return; }
        var sp = { id: uid('sp'), name: name, topic: selTopic, desc: descIn.value.trim(),
                   color: selColor, privacy: selPriv, members: [], custom: true };
        custom.unshift(sp);
        mine.push(sp.id);
        persist(); render(); closeCreate();
        say('"' + name + '" created — you are its first member. Invite people to join.');
      });
      row.appendChild(cancel); row.appendChild(create);
      form.appendChild(row);
      setTimeout(function(){ nameIn.focus(); }, 50);
    }
    function closeCreate(){ form.classList.remove('open'); form.innerHTML = ''; }

    on(createBtn, 'click', function(){
      if (form.classList.contains('open')) closeCreate(); else openCreate();
    });

    render();
    say(allSpaces().length ? 'Join a space, or create your own.' : 'No spaces yet — create the first one.');

    return {
      destroy: function(){
        listeners.forEach(function(l){ try { l[0].removeEventListener(l[1], l[2]); } catch(e){} });
        root.innerHTML = '';
      }
    };
  }
});
})();
