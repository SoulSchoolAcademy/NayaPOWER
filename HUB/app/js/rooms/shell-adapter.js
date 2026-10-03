/* SHELL ADAPTER — Naya 4 rooms, Hub-shell render contract.
   ------------------------------------------------------------------
   The Hub shells (naya/hub-complete-app-v1, 509 chassis) mount rooms with:
       body.appendChild(window.NayaRooms[roomId]())
   i.e. a ZERO-ARGUMENT function returning an Element.
   Naya 4's rich rooms register as window.NayaRooms.<richName>(el, ctx),
   where `el` is the element factory and `ctx` carries data + callbacks.
   This file bridges the two contracts. It is additive and reversible:
   it never edits a room; it only registers shell-facing wrappers.
   Load AFTER the room files (and after *-adapter.js files).

   Data: the host page injects window.__NayaShellSeeds = {
       contacts, spaces, threads, notes, entries, doors, reports, me }
   before loading this file. When seeds are absent, minimal built-in
   fallback seeds keep the shell from hard-crashing (rooms render, honest
   about being empty). Seeded demo content is DEMO-labeled by the rooms.
   ------------------------------------------------------------------ */
(function(){
  'use strict';

  function el(tag, cls, text){
    var e = document.createElement(tag);
    if(cls) e.className = cls;
    if(text !== undefined && text !== null) e.textContent = text;
    return e;
  }

  var S = window.__NayaShellSeeds || {};

  /* ---------- minimal honest fallback seeds (never crash the shell) ---------- */
  var FALLBACK_CONTACTS = [
    {id:'shawn', name:'Shawn Vibert', role:'Human Director', color:'#facc15'},
    {id:'naya4', name:'Naya 4', role:'Builder seat', color:'#a3e635'}
  ];
  var FALLBACK_SPACES = [
    {id:'team-naya', name:'Team Naya', color:'#a855f7',
     members:['shawn','naya4'], desc:'The full build team.',
     activity:[{ts:new Date().toISOString(), author:'Naya 4',
                text:'Shell adapter online — this space renders through the Hub shell now.', demo:true}]}
  ];

  var contacts = Array.isArray(S.contacts) && S.contacts.length ? S.contacts : FALLBACK_CONTACTS;
  var me = S.me || 'shawn';

  /* Seed the shared people spine so every room resolves one truth. */
  try{
    if(window.NayaPeople && typeof window.NayaPeople.ensureSeeded === 'function')
      window.NayaPeople.ensureSeeded(contacts);
  }catch(err){ /* spine is best-effort; rooms degrade to raw contacts */ }

  function rawSpaces(){
    return (Array.isArray(S.spaces) && S.spaces.length ? S.spaces : FALLBACK_SPACES);
  }
  function parsedSpaces(){
    var raw = rawSpaces();
    try{
      if(window.SpacesAdapter && typeof window.SpacesAdapter.parseSpaces === 'function')
        return window.SpacesAdapter.parseSpaces(raw, contacts);
    }catch(err){ /* fall through to raw */ }
    return raw;
  }
  function parsedThreads(){
    var raw = Array.isArray(S.threads) ? S.threads : [];
    try{
      if(window.MailAdapter && typeof window.MailAdapter.parseThreads === 'function')
        return window.MailAdapter.parseThreads(raw);
    }catch(err){ /* fall through to raw */ }
    return raw;
  }

  var R = window.NayaRooms = window.NayaRooms || {};

  function unavailable(name){
    var d = el('div', 'shell-room-unavailable');
    d.style.cssText = 'padding:48px 24px;text-align:center;color:#b8b3c7;font:500 15px system-ui;';
    d.textContent = 'The ' + name + ' room is not loaded in this shell build.';
    return d;
  }

  /* Wrap a rich (el, ctx) room as a zero-arg shell renderer. */
  function wrap(richName, ctx, label){
    var orig = R[richName];
    return function(){
      if(typeof orig !== 'function') return unavailable(label || richName);
      try{
        var node = orig(el, ctx);
        if(node && node.nodeType === 1) return node;
        return unavailable(label || richName);
      }catch(err){
        var d = el('div', 'shell-room-error');
        d.style.cssText = 'padding:48px 24px;text-align:center;color:#b8b3c7;font:500 15px system-ui;';
        d.textContent = 'The ' + (label || richName) + ' room hit a render fault and stayed quiet instead of breaking the shell.';
        return d;
      }
    };
  }

  var ctxSpaces = {spaces: parsedSpaces(), contacts: contacts, me: me, initialSpaceId: 'team-naya'};

  /* Shell-facing registrations. Names match the shell's ROOMS ids. */
  R.spaces      = wrap('smartSpaces', ctxSpaces, 'Smart Spaces');
  /* Forward the "create around this intelligence" entry contract so the
   * shell (or any room) can launch space creation pre-filled. */
  try{
    if(window.NayaRooms.smartSpaces && typeof window.NayaRooms.smartSpaces.createAround === 'function'){
      R.spaces.createAround = window.NayaRooms.smartSpaces.createAround;
    }
  }catch(err){}
  R.mail        = wrap('smartMail', {threads: parsedThreads(), contacts: contacts,
                                    spaces: rawSpaces(), me: me}, 'Smart Mail');
  R.lists       = wrap('smartList', {notes: Array.isArray(S.notes) ? S.notes : []}, 'Smart Lists');
  R.reports     = wrap('reports', {reports: Array.isArray(S.reports) ? S.reports : []}, 'Reports');
  R.connect     = wrap('connect', {doors: Array.isArray(S.doors) ? S.doors : []}, 'Smart Connect');
  R.ledger      = wrap('ledger', {entries: Array.isArray(S.entries) ? S.entries : [],
                                 demo: S.demo}, 'Smart Ledger');
  R.connections = wrap('connections', {contacts: contacts}, 'Connections');
  R.settings    = wrap('settings', {userName: S.userName || 'Shawn Vibert'}, 'Settings');
  R.library     = wrap('library', {objects: Array.isArray(S.objects) ? S.objects : null,
                                   verified: S.verified !== false}, 'Intelligent Library');

  /* Introspection for the shell/debugger: which slots this adapter serves. */
  R.__shellAdapter = {
    slots: ['spaces','mail','lists','reports','connect','ledger','connections','settings','library'],
    seeded: !!window.__NayaShellSeeds,
    at: new Date().toISOString()
  };
})();
