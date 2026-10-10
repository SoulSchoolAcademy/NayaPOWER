function connections(){
  var reqs = NayaHub.d.requests;
  var mine = NayaHub.d.conns || [];
  function connCard(name, role, st, color, scope, extra){
    var stv = st === 'ACTIVE' ? 'READY' : 'NOT_VERIFIED';
    return '<article class="ws-card" style="--accent:'+color+'"><h3>'+NayaHub.esc(name)+'</h3>'
      + '<p><b>'+NayaHub.esc(role)+'</b></p>'
      + '<span class="hub-state" data-s="'+stv+'">'+st+'</span>'
      + '<p class="hub-dim">Scope — '+NayaHub.esc(scope)+'</p>'
      + '<div class="ws-actions">'+extra+'</div></article>';
  }
  var mineCards = mine.map(function(c){
    return connCard(c.name, c.kind, 'ADDED BY YOU', '#55e39a', c.scope,
      '<button data-hub-action="conn-remove" data-v="'+c.id+'">REMOVE</button>');
  }).join('');
  var pend = reqs.filter(function(r){ return r.door === 'collective' || r.door === 'human'; });
  var pendHtml = pend.length
    ? '<h3 class="hub-h">PENDING REQUESTS</h3><div class="ws-list">' + pend.map(function(r){
        return '<div class="ws-row"><b>'+NayaHub.esc(r.door)+'</b><span>requested '+NayaHub.hts(r.ts)+'</span></div>';
      }).join('') + '</div>'
    : '';
  var total = 2 + mine.length;
  var st = total > 0 ? 'READY' : 'EMPTY';
  return head(S.connections)
    + '<span class="hub-state" data-s="'+st+'">'+st+' · '+total+' CONNECTIONS</span>'
    + '<div class="ws-grid">'
    + connCard('Naya', 'Trusted thinking partner', 'ACTIVE', '#d86cff',
        'Interprets what the Hub holds. Reads with you, writes nothing alone.',
        '<span class="hub-dim">Connection ≠ permission. It cannot act, share, or persist without your word.</span>')
    + connCard('Shawn', 'Director — you', 'ACTIVE', '#55e39a',
        'Full authority. Merges, deploys, ratification: your word only.',
        '<span class="hub-dim">This connection is you. It cannot be removed from here.</span>')
    + mineCards
    + '</div>'
    + card('ADD A CONNECTION',
        '<div class="hub-form"><input id="hubConnName" placeholder="Name — person, Naya, organization…">'
        + '<select id="hubConnKind"><option>Person</option><option>Naya</option><option>Organization</option><option>Space</option></select>'
        + '<button data-hub-action="conn-add">ADD CONNECTION</button></div>'
        + '<p class="hub-dim">Every connection is receipted. Adding one grants a relationship — never permission to act.</p>', '#55b9ee')
    + pendHtml
    + '<p class="hub-note">Relationships are governed. A connection is a relationship — it is never, by itself, permission.</p>';
}
