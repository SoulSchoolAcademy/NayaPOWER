/* NAYA PEOPLE REGISTRY — the shared people spine for the Hub rooms.
 *
 * One graph, four views: Connections, Smart Mail, Smart Spaces, Smart Lists
 * all resolve people against this single registry instead of carrying their
 * own copies. Local persistence: localStorage['naya.people.registry'].
 *
 * Contract: window.NayaPeople = { load, save, ensureSeeded, add, get, KEY }.
 *   ensureSeeded(ctxContacts) — first room opened seeds the registry from
 *     ctx.contacts; every room after that reads the shared truth. Returns
 *     the people array.
 *   add(person) — {id,name,role,color,note}; no-ops when the id exists.
 *     Returns the people array.
 *   get(id) — one person or null.
 *
 * Shell note: the shell owns the canonical registry. When it feeds canonical
 * contacts it should save() them first so rooms never read a stale local
 * seed; rooms treat the registry as read-mostly and add() only on explicit
 * user action (e.g. "add to connections" from a thread).
 */
(function(){
  'use strict';

  var KEY = 'naya.people.registry';

  function clean(p){
    if(!p || typeof p !== 'object' || p.id == null) return null;
    return {
      id: String(p.id),
      name: String(p.name != null ? p.name : p.id),
      role: String(p.role || ''),
      color: String(p.color || '#8b93a3'),
      note: String(p.note || '')
    };
  }

  function load(){
    try{
      var raw = localStorage.getItem(KEY);
      var a = raw ? JSON.parse(raw) : null;
      if(!Array.isArray(a)) return null;
      var out = [];
      a.forEach(function(p){ var c = clean(p); if(c) out.push(c); });
      return out;
    }catch(e){ return null; }
  }

  function save(people){
    try{ localStorage.setItem(KEY, JSON.stringify(people || [])); }catch(e){}
  }

  function ensureSeeded(ctxContacts){
    var people = load();
    if(people) return people;
    people = [];
    (Array.isArray(ctxContacts) ? ctxContacts : []).forEach(function(p){
      var c = clean(p); if(c) people.push(c);
    });
    save(people);
    return people;
  }

  function add(person){
    var people = load() || [];
    var c = clean(person);
    if(c && !people.some(function(p){ return p.id === c.id; })){
      people.push(c);
      save(people);
    }
    return people;
  }

  function get(id){
    var people = load() || [];
    for(var i = 0; i < people.length; i++){
      if(people[i].id === String(id)) return people[i];
    }
    return null;
  }

  window.NayaPeople = {
    KEY: KEY,
    load: load,
    save: save,
    ensureSeeded: ensureSeeded,
    add: add,
    get: get
  };
})();
