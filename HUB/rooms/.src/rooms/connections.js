function connections(){
  var reqs = NayaHub.d.requests;
  function conn(name, role, st, color, scope, id, active){
    var act = active
      ? '<span class="hub-dim">Connection ≠ permission. It still cannot act, share, or persist without your word.</span>'
      : '<button data-hub-action="conn-request" data-v="'+id+'">REQUEST CONNECTION</button>';
    return '<article class="ws-card" style="--accent:'+color+'"><h3>'+name+'</h3>'
      + '<p><b>'+role+'</b> · <span class="hub-chip'+(active?' on':'')+'">'+st+'</span></p>'
      + '<p class="hub-dim">Scope — '+scope+'</p>'
      + '<div class="hub-actions">'+act+'</div></article>';
  }
  var pend = reqs.filter(function(r){ return r.door === 'collective' || r.door === 'human'; });
  var pendHtml = pend.length
    ? '<h3 class="hub-h">PENDING REQUESTS</h3><div class="ws-list">' + pend.map(function(r){
        return '<div class="ws-row"><b>'+NayaHub.esc(r.door)+'</b><span>requested '+NayaHub.hts(r.ts)+'</span></div>';
      }).join('') + '</div>'
    : '';
  return head(S.connections)
    + '<div class="ws-grid">'
    + conn('Naya', 'Trusted thinking partner', 'ACTIVE', '#d86cff',
        'Interprets what the Hub holds. Reads with you, writes nothing alone.', 'naya', true)
    + conn('Shawn', 'Director — you', 'ACTIVE', '#55e39a',
        'Full authority. Merges, deploys, ratification: your word only.', 'shawn', true)
    + conn('Collective Intelligence', 'Many minds, one intelligence', 'BY CONSENT', '#55b9ee',
        'Reads what is shared by choice. Writes nothing into your private rooms.', 'collective', false)
    + '</div>'
    + pendHtml
    + '<p class="hub-note">Relationships are governed. A connection is a relationship — it is never, by itself, permission.</p>';
}
