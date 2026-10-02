function settings(){
  var r = R();
  var snap = null, verify = null;
  try{ snap = r && r.snapshot ? r.snapshot() : null; verify = r && r.verify ? r.verify() : null; }catch(e){}
  var nRcpt = NayaHub.d.receipts.length;
  var nSaved = Object.keys(state.saved || {}).length;
  var nNotes = 0;
  try{ nNotes = NOTES().length; }catch(e){}
  return head(S.settings)
    + '<div class="ws-grid">'
    + card('RUNTIME',
        '<p><b>'+(r ? 'EXPOSED' : 'NOT EXPOSED')+'</b></p>'
        + '<p class="hub-dim">'+(snap && snap.authenticated ? 'Authenticated' : 'Not authenticated')
        + ' · '+(snap && snap.user_id ? esc(snap.user_id) : 'no user exposed')+'</p>'
        + '<p class="hub-dim">Verify: '+(verify ? esc(JSON.stringify(verify)).slice(0,80) : 'unavailable')+'</p>'
        + '<p class="hub-dim">Hub → governed runtime → managed persistence.</p>', '#55e39a')
    + card('HUB DATA',
        '<p><b>'+nRcpt+'</b> receipts · <b>'+nSaved+'</b> saved · <b>'+nNotes+'</b> notes</p>'
        + '<p class="hub-dim">Everything above lives in this browser — yours, not ours.</p>'
        + '<div class="hub-actions"><button data-hub-action="hub-export">EXPORT MY DATA</button>'
        + '<button data-hub-action="hub-clear" class="hub-danger">ERASE LOCAL DATA</button></div>', '#f1d75a')
    + card('TRUST',
        '<p>Source and interpretation are marked separately, everywhere in this Hub.</p>'
        + '<p class="hub-dim">No remote result is fabricated in this static build. What the Hub cannot prove, it says so.</p>', '#d86cff')
    + '</div>'
    + '<p class="hub-note">Your relationship with NayaNET: identity, runtime state, data, trust. Infrastructure stays under the hood.</p>';
}
