/* INTELLIGENT LIBRARY — "Shelved, not stored."
   The identity lookup for the whole Hub: every canonical object findable
   by identity. Shelves hold REFERENCES; nothing here is a copy.
   Implements the DRAFT blueprint (room-library-BLUEPRINT-DRAFT.pdf) —
   NOT locked. Shawn's corrections become the locked spec.

   window.NayaRooms.library(el, ctx)
   ctx.objects  — parsed references (LibraryAdapter.parseMany); defaults to
                  the adapter's REAL + DEMO seeds when absent (DEMO labeled).
   ctx.verified — false renders the honest NOT_VERIFIED state.
   ctx.onViewInStream(id), ctx.onViewInToday(id) — handoffs; otherwise a
                  quiet toast explains the handoff target.
*/
(function(){
  'use strict';

  var LS_QUERY = 'naya.library.query';

  var TRUTH_COLORS = {
    'RATIFIED': '#a3e635',
    'DIRECTOR-STATED': '#facc15',
    'CANDIDATE': '#fb923c',
    'DEMO': '#a855f7'
  };

  function LibraryRoom(el, ctx){
    ctx = ctx || {};
    var A = window.LibraryAdapter;
    var objects = Array.isArray(ctx.objects) && ctx.objects.length
      ? A.parseMany(ctx.objects)
      : A.parseMany(A.REAL.concat(A.DEMO));
    var verified = ctx.verified !== false;

    var stage = el('div', 'lib-stage');

    /* ---------- hero ---------- */
    var hero = el('header', 'lib-hero');
    hero.appendChild(el('p', 'lib-kicker', 'INTELLIGENT LIBRARY'));
    hero.appendChild(el('h1', 'lib-title', 'Intelligent Library'));
    hero.appendChild(el('p', 'lib-thesis', 'Shelved, not stored.'));
    var searchWrap = el('div', 'lib-searchwrap');
    var search = el('input', 'lib-search');
    search.type = 'search';
    search.setAttribute('aria-label', 'Search the library by canonical ID or text');
    search.placeholder = 'Type a canonical ID (e.g. SN-217) or any text…';
    var cap = el('span', 'lib-cap', '(retrieval, not capture)');
    cap.title = 'The search box retrieves. Nothing is captured or filed here.';
    searchWrap.appendChild(search);
    searchWrap.appendChild(cap);
    hero.appendChild(searchWrap);
    var idHint = el('p', 'lib-idhint', '');
    hero.appendChild(idHint);
    stage.appendChild(hero);

    /* ---------- browse the major areas ---------- */
    var activeArea = null;
    var areasEl = el('div', 'lib-areas');
    areasEl.appendChild(el('p', 'lib-areas-label', 'Browse the major areas of NayaPOWER'));
    var chipsEl = el('div', 'lib-chips');
    A.AREAS.forEach(function(a){
      var chip = el('button', 'lib-chip', a.name);
      chip.type = 'button';
      chip.setAttribute('aria-pressed', 'false');
      chip.addEventListener('click', function(){
        activeArea = (activeArea === a.id) ? null : a.id;
        Array.prototype.forEach.call(chipsEl.children, function(c){
          c.setAttribute('aria-pressed', c.textContent === a.name && activeArea ? 'true' : 'false');
          c.classList.toggle('on', c.textContent === a.name && !!activeArea);
        });
        try{ localStorage.setItem(LS_QUERY, search.value); }catch(e){}
        paint(search.value);
      });
      chipsEl.appendChild(chip);
    });
    areasEl.appendChild(chipsEl);
    stage.appendChild(areasEl);

    var answerEl = el('div', 'lib-answerwrap');
    stage.appendChild(answerEl);

    var shelvesEl = el('div', 'lib-shelves');
    stage.appendChild(shelvesEl);

    /* ---------- evidence drawer ---------- */
    var scrim = el('div', 'lib-scrim');
    scrim.hidden = true;
    var drawer = el('aside', 'lib-drawer');
    drawer.setAttribute('role', 'dialog');
    drawer.setAttribute('aria-modal', 'true');
    drawer.setAttribute('aria-label', 'Object evidence');
    drawer.hidden = true;
    stage.appendChild(scrim);
    stage.appendChild(drawer);

    var toast = el('div', 'lib-toast');
    toast.hidden = true;
    stage.appendChild(toast);
    var toastH = null;
    function say(msg){
      toast.textContent = msg;
      toast.hidden = false;
      clearTimeout(toastH);
      toastH = setTimeout(function(){ toast.hidden = true; }, 2600);
    }

    function pill(truth){
      var p = el('span', 'lib-pill', truth);
      p.style.setProperty('--pill', TRUTH_COLORS[truth] || '#888888');
      return p;
    }

    function openEvidence(obj){
      drawer.innerHTML = '';
      drawer.hidden = false;
      scrim.hidden = false;
      var prevFocus = document.activeElement;

      var close = el('button', 'lib-x', '×');
      close.setAttribute('aria-label', 'Close evidence');
      drawer.appendChild(close);

      drawer.appendChild(el('p', 'lib-ev-eyebrow', obj.stream));
      var t = el('h2', 'lib-ev-title', obj.title);
      drawer.appendChild(t);
      var meta = el('div', 'lib-ev-meta');
      meta.appendChild(el('code', 'lib-id', obj.id));
      meta.appendChild(pill(obj.truth));
      if(obj.demo) meta.appendChild(el('span', 'lib-demotag', 'DEMO'));
      drawer.appendChild(meta);
      drawer.appendChild(el('p', 'lib-ev-excerpt', obj.excerpt));

      var qs = [
        ['What is it?', obj.title + ' — ' + obj.excerpt],
        ['Where did it come from?', obj.provenance.source],
        ['What supports it?', obj.provenance.evidence],
        ['What is its standing?', obj.provenance.status +
          (obj.provenance.supersededBy ? ' Superseded by ' + obj.provenance.supersededBy + '.' : '')]
      ];
      qs.forEach(function(q){
        var block = el('div', 'lib-ev-q');
        block.appendChild(el('p', 'lib-ev-qq', q[0]));
        block.appendChild(el('p', 'lib-ev-qa', q[1]));
        drawer.appendChild(block);
      });

      var hands = el('div', 'lib-ev-hands');
      var bStream = el('button', 'lib-hbtn', 'View in stream');
      var bToday = el('button', 'lib-hbtn', 'View in Today');
      bStream.addEventListener('click', function(){
        if(typeof ctx.onViewInStream === 'function') ctx.onViewInStream(obj.id);
        else say('Hands ' + obj.id + ' to the Feed — same canonical ID, the stream position.');
      });
      bToday.addEventListener('click', function(){
        if(typeof ctx.onViewInToday === 'function') ctx.onViewInToday(obj.id);
        else say('Hands ' + obj.id + ' to Today — same canonical ID, the reel context.');
      });
      hands.appendChild(bStream);
      hands.appendChild(bToday);
      drawer.appendChild(hands);

      function shut(){
        drawer.hidden = true;
        scrim.hidden = true;
        document.removeEventListener('keydown', onKey, true);
        if(prevFocus && prevFocus.focus) prevFocus.focus();
      }
      function onKey(e){
        if(e.key === 'Escape'){ e.stopPropagation(); shut(); return; }
        if(e.key === 'Tab'){
          var f = drawer.querySelectorAll('button');
          if(!f.length) return;
          var first = f[0], last = f[f.length - 1];
          if(e.shiftKey && document.activeElement === first){ e.preventDefault(); last.focus(); }
          else if(!e.shiftKey && document.activeElement === last){ e.preventDefault(); first.focus(); }
        }
      }
      close.addEventListener('click', shut);
      scrim.addEventListener('click', shut);
      document.addEventListener('keydown', onKey, true);
      close.focus();
    }

    function card(obj){
      var c = el('article', 'lib-card' + (obj.demo ? ' is-demo' : ''));
      c.tabIndex = 0;
      c.setAttribute('role', 'button');
      c.setAttribute('aria-label', obj.title + ', ' + obj.id + ', ' + obj.truth);
      c.appendChild(el('p', 'lib-card-eyebrow', obj.stream));
      c.appendChild(el('h3', 'lib-card-title', obj.title));
      c.appendChild(el('p', 'lib-card-ex', obj.excerpt));
      var meta = el('div', 'lib-card-meta');
      meta.appendChild(el('code', 'lib-id', obj.id));
      meta.appendChild(pill(obj.truth));
      c.appendChild(meta);
      function open(){ openEvidence(obj); }
      c.addEventListener('click', open);
      c.addEventListener('keydown', function(e){
        if(e.key === 'Enter' || e.key === ' '){ e.preventDefault(); open(); }
      });
      return c;
    }

    function answerCard(obj, score){
      var a = el('div', 'lib-answer');
      a.appendChild(el('p', 'lib-answer-label', 'Best match from the shelves — retrieved, not generated'));
      a.appendChild(el('h2', 'lib-answer-title', obj.title));
      a.appendChild(el('p', 'lib-answer-text', obj.excerpt));
      var meta = el('div', 'lib-card-meta');
      meta.appendChild(el('code', 'lib-id', obj.id));
      meta.appendChild(pill(obj.truth));
      a.appendChild(meta);
      var open = el('button', 'lib-hbtn lib-answer-open', 'Open the evidence');
      open.type = 'button';
      open.addEventListener('click', function(){ openEvidence(obj); });
      a.appendChild(open);
      return a;
    }

    function paint(query){
      shelvesEl.innerHTML = '';
      answerEl.innerHTML = '';
      idHint.textContent = '';

      if(!verified){
        var nv = el('div', 'lib-state');
        nv.appendChild(el('p', 'lib-state-t', 'No governed runtime connected yet.'));
        nv.appendChild(el('p', 'lib-state-d',
          'The Library shelves references from the canonical runtime. Nothing is shown — and nothing is faked — until the runtime answers.'));
        shelvesEl.appendChild(nv);
        return;
      }
      if(!objects.length){
        var em = el('div', 'lib-state');
        em.appendChild(el('p', 'lib-state-t', 'The shelves are empty.'));
        em.appendChild(el('p', 'lib-state-d', 'Shelving is automatic from canonical intelligence — nothing is filed by hand.'));
        shelvesEl.appendChild(em);
        return;
      }

      var q = String(query || '').trim();
      var pool = activeArea ? A.byArea(objects, activeArea) : objects;
      var idHit = q ? A.resolveId(pool, q) : null;
      var ranked = q ? A.rank(pool, q) : pool.map(function(o){ return {obj:o, score:0}; });
      var list = ranked.map(function(r){ return r.obj; });

      if(idHit){
        idHint.textContent = 'Canonical ID resolved: ' + idHit.id + ' — the primary path.';
        list = [idHit].concat(list.filter(function(o){ return o.id !== idHit.id; }));
      }

      /* Q&A: a question with a strong hit gets the answer card. */
      if(q && !idHit && A.isQuestion(q) && ranked.length && ranked[0].score >= 15){
        answerEl.appendChild(answerCard(ranked[0].obj, ranked[0].score));
      }

      if(q && !list.length){
        var nr = el('div', 'lib-state');
        nr.appendChild(el('p', 'lib-state-t', 'No references match "' + q + '".'));
        nr.appendChild(el('p', 'lib-state-d', 'The shelves stay honest — no results invented.'));
        if(activeArea){
          var clr = el('button', 'lib-hbtn', 'Clear the area filter');
          clr.type = 'button';
          clr.addEventListener('click', function(){
            activeArea = null;
            Array.prototype.forEach.call(chipsEl.children, function(c){
              c.setAttribute('aria-pressed', 'false'); c.classList.remove('on');
            });
            paint(search.value);
          });
          nr.appendChild(clr);
        }
        shelvesEl.appendChild(nr);
        return;
      }

      A.KINDS.forEach(function(kind){
        var items = list.filter(function(o){ return o.kind === kind.id; });
        if(!items.length) return;
        var shelf = el('section', 'lib-shelf');
        var head = el('div', 'lib-shelf-head');
        head.appendChild(el('h2', 'lib-shelf-name', kind.name));
        head.appendChild(el('p', 'lib-shelf-count', items.length + ' REFERENCES · 0 COPIES'));
        shelf.appendChild(head);
        var grid = el('div', 'lib-grid');
        items.forEach(function(o){ grid.appendChild(card(o)); });
        shelf.appendChild(grid);
        shelvesEl.appendChild(shelf);
      });
    }

    /* query persists across reload */
    var saved = null;
    try{ saved = localStorage.getItem(LS_QUERY); }catch(e){}
    if(saved){ search.value = saved; }
    var deb = null;
    search.addEventListener('input', function(){
      clearTimeout(deb);
      deb = setTimeout(function(){
        try{ localStorage.setItem(LS_QUERY, search.value); }catch(e){}
        paint(search.value);
      }, 160);
    });
    search.addEventListener('keydown', function(e){
      if(e.key === 'Enter'){
        clearTimeout(deb);
        try{ localStorage.setItem(LS_QUERY, search.value); }catch(e){}
        paint(search.value);
      }
    });

    paint(search.value || '');
    return stage;
  }

  window.NayaRooms = window.NayaRooms || {};
  window.NayaRooms.library = LibraryRoom;
})();
