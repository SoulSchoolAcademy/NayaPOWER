async function ledger(){
  var rs = NayaHub.d.receipts.slice().reverse();
  var rows = rs.map(function(r){
    return '<div class="ws-row"><b>'+NayaHub.esc(r.action)+'</b>'
      + '<span>'+NayaHub.hts(r.ts)+' · '+NayaHub.esc(r.id)+' · <code>'+String(r.hash).slice(0,12)+'</code></span>'
      + '<div class="hub-detail">'+NayaHub.esc(r.detail)
      + '<br><span class="hub-dim">'+NayaHub.esc(r.actor)+' · prev <code>'+String(r.prev).slice(0,12)+'</code></span></div></div>';
  }).join('') || '<div class="ws-empty">No receipts yet. Save, favorite, capture, or request — the ledger records it.</div>';
  return head(S.ledger)
    + '<div class="hub-actions"><button data-hub-action="ledger-verify">VERIFY CHAIN</button>'
    + '<button data-hub-action="hub-export">EXPORT LEDGER</button></div>'
    + '<div id="hubVerify" role="status"></div>'
    + '<div class="ws-list">'+rows+'</div>'
    + '<p class="hub-note">'+rs.length+' receipts · each one hashes the previous. If anyone tampers, the chain breaks and verification says so.</p>';
}
