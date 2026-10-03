/* SMART SPACES — Room: groups within NayaNET.
 * Registry theme: VIOLET #8b5cf6 (room chrome). Space cards carry each
 * space's OWN identity color (color = stable identity, never list position).
 *
 * Contract: window.NayaRooms.smartSpaces(el, ctx)
 *   ctx.spaces  — from SpacesAdapter.parseSpaces (normalized)
 *   ctx.onMail  — optional fn(space, text) called when a message is posted
 * Law: no canonical group store exists; seeded spaces/activity are DEMO.
 * Members are real network contacts. Every button has a real consequence.
 * Posts persist to localStorage `naya.smartspaces.posts`.
 */
(function(){
  'use strict';

  var ROOM = '#8b5cf6';
  var STORE_KEY = 'naya.smartspaces.posts';

  function fmtTime(ts){
    if(!ts) return '';
    var d = new Date(ts);
    if(isNaN(d)) return '';
    var diff = Date.now() - d.getTime();
    var m = Math.floor(diff/60000);
    if(m < 1) return 'just now';
    if(m < 60) return m + 'm ago';
    var h = Math.floor(m/60);
    if(h < 24) return h + 'h ago';
    return Math.floor(h/24) + 'd ago';
  }

  function loadPosts(){
    try {
      var raw = localStorage.getItem(STORE_KEY);
      var p = raw ? JSON.parse(raw) : {};
      return (p && typeof p === 'object') ? p : {};
    } catch(e){ return {}; }
  }
  function savePosts(posts){
    try { localStorage.setItem(STORE_KEY, JSON.stringify(posts)); } catch(e){}
  }

  function SmartSpaces(el, ctx){
    ctx = ctx || {};
    var spaces = Array.isArray(ctx.spaces) ? ctx.spaces : [];
    var onMail = (typeof ctx.onMail === 'function') ? ctx.onMail : null;
    var posts = loadPosts();

    var stage = el('div','sp-stage');
    var state = { view:'grid', space:null };

    /* header */
    var head = el('header','sp-head');
    head.appendChild(el('p','sp-kicker','SMART SPACES'));
    var h1 = el('h1','sp-title',''); h1.textContent = 'Groups that move as one';
    head.appendChild(h1);
    var sub = el('p','sp-sub','');
    sub.textContent = 'The teams inside NayaNET. Open a space to see its people, what is happening, and mail them all at once.';
    head.appendChild(sub);
    var demo = el('p','sp-demo','');
    demo.textContent = 'DEMO SPACES \u00B7 illustrative groups for design review \u00B7 members are real network contacts';
    head.appendChild(demo);
    stage.appendChild(head);

    var body = el('div','sp-body');
    stage.appendChild(body);

    var foot = el('footer','sp-foot','');
    foot.textContent = 'no canonical group store yet \u00B7 your posts are saved on this device';
    stage.appendChild(foot);

    function allActivity(space){
      var seeded = space.activity || [];
      var mine = (posts[space.id] || []).map(function(p){
        return {ts:p.ts, text:p.text, demo:false, mine:true, author:p.author||'You'};
      });
      var all = seeded.concat(mine);
      all.sort(function(a,b){ return String(b.ts).localeCompare(String(a.ts)); });
      return all;
    }

    function render(){
      body.innerHTML = '';
      if(state.view === 'grid') body.appendChild(gridView());
      else body.appendChild(detailView(state.space));
    }

    /* ---------------- GRID ---------------- */
    function gridView(){
      var grid = el('div','sp-grid');
      if(!spaces.length){
        grid.appendChild(el('p','sp-empty','No spaces yet.'));
        return grid;
      }
      spaces.forEach(function(s, i){
        var card = el('article','sp-card');
        card.style.setProperty('--sc', s.color);
        card.style.setProperty('--i', i);
        card.setAttribute('role','button');
        card.setAttribute('tabindex','0');
        card.setAttribute('aria-label','Open space: ' + s.name);
        var top = el('div','sp-card-top');
        var jewel = el('span','sp-jewel',''); jewel.textContent = '\u25C9';
        top.appendChild(jewel);
        var nm = el('h2','sp-card-name',''); nm.textContent = s.name;
        top.appendChild(nm);
        if(s.demo) top.appendChild(el('span','sp-demo-chip','DEMO'));
        card.appendChild(top);
        var dc = el('p','sp-card-desc',''); dc.textContent = s.desc;
        card.appendChild(dc);
        var row = el('div','sp-card-members');
        s.members.slice(0,5).forEach(function(m){
          var dot = el('span','sp-mdot','');
          dot.style.setProperty('--mc', m.color || '#888888');
          dot.title = m.name;
          row.appendChild(dot);
        });
        var cnt = el('span','sp-card-count','');
        cnt.textContent = s.members.length + ' members \u00B7 ' + allActivity(s).length + ' updates';
        row.appendChild(cnt);
        card.appendChild(row);
        var open = function(){ state.view = 'detail'; state.space = s; render(); };
        card.addEventListener('click', open);
        card.addEventListener('keydown', function(ev){
          if(ev.key === 'Enter' || ev.key === ' '){ ev.preventDefault(); open(); }
        });
        grid.appendChild(card);
      });
      return grid;
    }

    /* ---------------- DETAIL ---------------- */
    function detailView(s){
      var d = el('div','sp-detail');
      d.style.setProperty('--sc', s.color);

      var back = el('button','sp-back','\u2190 ALL SPACES');
      back.type = 'button';
      var goBack = function(){ state.view = 'grid'; state.space = null; render(); };
      back.addEventListener('click', goBack);
      d.appendChild(back);

      var hero = el('div','sp-dhero');
      var jewel = el('span','sp-djewel',''); jewel.textContent = '\u25C9';
      hero.appendChild(jewel);
      var ht = el('div','sp-dhead');
      var nm = el('h2','sp-dname',''); nm.textContent = s.name; ht.appendChild(nm);
      var dc = el('p','sp-ddesc',''); dc.textContent = s.desc; ht.appendChild(dc);
      hero.appendChild(ht);
      if(s.demo) hero.appendChild(el('span','sp-demo-chip','DEMO'));
      d.appendChild(hero);

      /* members */
      d.appendChild(el('h3','sp-sec','MEMBERS \u00B7 ' + s.members.length));
      var ml = el('div','sp-members');
      s.members.forEach(function(m){
        var chip = el('div','sp-member');
        var av = el('span','sp-avatar','');
        av.textContent = initials(m.name);
        av.style.setProperty('--av', m.color || '#888888');
        chip.appendChild(av);
        var tx = el('div','sp-member-tx');
        var mn = el('span','sp-member-n',''); mn.textContent = m.name; tx.appendChild(mn);
        if(m.role){ var mr = el('span','sp-member-r',''); mr.textContent = m.role; tx.appendChild(mr); }
        chip.appendChild(tx);
        ml.appendChild(chip);
      });
      d.appendChild(ml);

      /* activity */
      d.appendChild(el('h3','sp-sec','ACTIVITY'));
      var feed = el('div','sp-feed');
      function paintFeed(){
        feed.innerHTML = '';
        var acts = allActivity(s);
        if(!acts.length) feed.appendChild(el('p','sp-empty','Nothing here yet. Be the first to post.'));
        acts.forEach(function(a){
          var row = el('div','sp-arow' + (a.mine ? ' mine' : ''));
          var tx = el('p','sp-atext',''); tx.textContent = a.text; row.appendChild(tx);
          var meta = el('div','sp-ameta');
          var t = el('span','sp-atime',''); t.textContent = fmtTime(a.ts);
          if(a.mine && a.author){ t.textContent = a.author + ' \u00B7 ' + t.textContent; }
          meta.appendChild(t);
          if(a.demo) meta.appendChild(el('span','sp-demo-chip sm','DEMO'));
          row.appendChild(meta);
          feed.appendChild(row);
        });
      }
      paintFeed();
      d.appendChild(feed);

      /* mail this space */
      d.appendChild(el('h3','sp-sec','MAIL THIS SPACE'));
      var box = el('div','sp-compose');
      var ta = el('textarea','sp-ta','');
      ta.placeholder = 'Message everyone in ' + s.name + '\u2026';
      ta.setAttribute('aria-label','Message to ' + s.name);
      ta.rows = 3;
      box.appendChild(ta);
      var sendRow = el('div','sp-sendrow');
      var hint = el('span','sp-sendhint','');
      hint.textContent = 'Posts to the space feed \u00B7 saved on this device';
      sendRow.appendChild(hint);
      var send = el('button','sp-send','SEND TO SPACE');
      send.type = 'button';
      send.disabled = true;
      ta.addEventListener('input', function(){ send.disabled = !ta.value.trim(); });
      send.addEventListener('click', function(){
        var text = ta.value.trim();
        if(!text) return;
        var entry = {ts:new Date().toISOString(), text:text, author:'You'};
        posts[s.id] = posts[s.id] || [];
        posts[s.id].push(entry);
        savePosts(posts);
        ta.value = '';
        send.disabled = true;
        paintFeed();
        var prior = sendRow.querySelector('.sp-sent');
        if(prior) prior.remove();
        var note = el('span','sp-sent','SENT \u2713');
        sendRow.appendChild(note);
        setTimeout(function(){ note.remove(); }, 1800);
        if(onMail){ try { onMail(s, text); } catch(e){} }
      });
      sendRow.appendChild(send);
      box.appendChild(sendRow);
      d.appendChild(box);

      return d;
    }

    render();

    /* Escape returns to grid from detail */
    stage.addEventListener('keydown', function(ev){
      if(ev.key === 'Escape' && state.view === 'detail'){
        state.view = 'grid'; state.space = null; render();
      }
    });

    return stage;
  }

  function initials(name){
    return String(name || '').split(/\s+/).map(function(w){ return w[0]; })
      .join('').slice(0,2).toUpperCase();
  }

  window.NayaRooms = window.NayaRooms || {};
  window.NayaRooms.smartSpaces = SmartSpaces;
})();
