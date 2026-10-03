/* SPACES ADAPTER — raw space records + contacts -> normalized space view-models.
 *
 * No canonical group store exists; seeded records are clearly-labeled DEMO
 * (director-authorized demo policy). Members are real network contacts.
 *
 *   const spaces = SpacesAdapter.parseSpaces(rawSpaces, contacts);
 *   // -> [{id, name, color, desc, members:[{id,name,role,color}], activity:[{ts,text,demo}]}]
 *
 * Member ids are resolved to contact objects. Unresolvable members are kept
 * as {id, name:id, role:'', color:'#888'} so nothing silently vanishes.
 * Unparseable space records are skipped.
 */
(function(){
  'use strict';

  function parseSpaces(raw, contacts){
    var out = [];
    var byId = {};
    (contacts || []).forEach(function(c){
      if(c && c.id) byId[c.id] = c;
    });
    (raw || []).forEach(function(r){
      try {
        if(!r || typeof r !== 'object' || !r.id || !r.name) return;
        var members = (r.members || []).map(function(mid){
          var c = byId[mid];
          if(c) return {id:c.id, name:c.name, role:c.role||'', color:c.color||'#888888'};
          return {id:String(mid), name:String(mid), role:'', color:'#888888'};
        });
        var activity = (r.activity || []).map(function(a){
          if(!a || typeof a !== 'object') return null;
          return {ts:a.ts || '', text:String(a.text || ''), demo:!!a.demo,
                  author:String(a.author || '')};
        }).filter(Boolean);
        /* newest first */
        activity.sort(function(a,b){ return String(b.ts).localeCompare(String(a.ts)); });
        out.push({
          id: String(r.id),
          name: String(r.name),
          color: r.color || '#8b5cf6',
          desc: String(r.desc || ''),
          members: members,
          activity: activity,
          demo: r.demo !== false
        });
      } catch(err){ /* skip unparseable */ }
    });
    return out;
  }

  window.SpacesAdapter = { parseSpaces: parseSpaces };
})();
