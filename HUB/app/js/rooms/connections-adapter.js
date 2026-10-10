/* CONNECTIONS ADAPTER — contact records -> normalized contact view-models.
 *
 * Sources of truth: the CONTACTS pack supplied by the shell (real people in
 * the user's network — never demo, never invented). Unparseable records are
 * skipped, never fabricated.
 *
 *   const contacts = ConnectionsAdapter.parseContacts(raw);
 *   // -> [{id, name, role, color, kind, note}]
 */
(function(){
  'use strict';

  function parseOne(c){
    if(!c || typeof c !== 'object') return null;
    if(!c.id || !c.name) return null;
    return {
      id:    String(c.id),
      name:  String(c.name),
      role:  c.role ? String(c.role) : '',
      color: /^#[0-9a-fA-F]{6}$/.test(String(c.color||'')) ? String(c.color) : '#9aa3b2',
      kind:  c.kind === 'seat' ? 'seat' : 'person',
      note:  c.note ? String(c.note) : ''
    };
  }

  function parseContacts(raw){
    var out = [];
    var seen = {};
    (Array.isArray(raw) ? raw : []).forEach(function(c){
      try{
        var p = parseOne(c);
        if(p && !seen[p.id]){ seen[p.id] = true; out.push(p); }
      }catch(err){ /* skip unparseable */ }
    });
    return out;
  }

  window.ConnectionsAdapter = { parseContacts: parseContacts };
})();
