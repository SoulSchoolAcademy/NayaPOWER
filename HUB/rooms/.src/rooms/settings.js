function settings(){
  var r = R();
  var snap = null, verify = null;
  try{ snap = r && r.snapshot ? r.snapshot() : null; verify = r && r.verify ? r.verify() : null; }catch(e){}
  var nRcpt = NayaHub.d.receipts.length;
  var nSaved = Object.keys(state.saved || {}).length;
  var nNotes = 0;
  try{ nNotes = NOTES().length; }catch(e){}
  var rm = NayaHub.d.prefs.reduceMotion ? ' checked' : '';
  return head(S.settings)
    + '<span class="hub-state" data-s="READY">READY</span>'
    + '<div class="ws-grid">'
    + card('IDENTITY',
        '<p><b>Shawn</b> · Director</p>'
        + '<p class="hub-dim">The human authority. Merges, deploys, ratification — your word only.</p>'
        + '<p class="hub-dim">Naya · Trusted thinking partner — interprets, never acts alone.</p>', '#d86cff')
    + card('PREFERENCES',
        '<label class="hub-check"><input type="checkbox" data-hub-check="reduce-motion"'+rm+'> Reduce motion</label>'
        + '<p class="hub-dim">Stills the glows and transitions. The Hub stays fully usable.</p>', '#55b9ee')
    + card('RUNTIME',
        '<p><b>'+(r ? 'EXPOSED' : 'NOT EXPOSED')+'</b></p>'
        + '<p class="hub-dim">'+(snap && snap.authenticated ? 'Authenticated' : 'Not authenticated')
        + ' · '+(snap && snap.user_id ? esc(snap.user_id) : 'no user exposed')+'</p>'
        + '<p class="hub-dim">Verify: '+(verify ? esc(JSON.stringify(verify)).slice(0,80) : 'unavailable')+'</p>'
        + '<p class="hub-dim">Hub → governed runtime → managed persistence.</p>', '#55e39a')
    + card('HUB DATA',
        '<p><b>'+nRcpt+'</b> receipts · <b>'+nSaved+'</b> saved · <b>'+nNotes+'</b> notes</p>'
        + '<p class="hub-dim">Everything above lives in this browser — yours, not ours.</p>'
        + '<div class="ws-actions"><button data-hub-action="hub-export">EXPORT MY DATA</button>'
        + '<button data-hub-action="hub-clear" class="hub-danger">ERASE LOCAL DATA</button></div>', '#f1d75a')
    + card('PRIVACY',
        '<p><b>Private by default.</b> Shared by choice. Collective by consent. Public by decision.</p>'
        + '<p class="hub-dim">Captures land in Personal unless you file them elsewhere. Nothing leaves this browser except what you explicitly send.</p>'
        + '<p class="hub-dim">Door Law: connection never implies permission to act. Every connection, request, and share is receipted in the Ledger.</p>', '#b8ee57')
    + card('TRUST',
        '<p>Source and interpretation are marked separately, everywhere in this Hub.</p>'
        + '<p class="hub-dim">No remote result is fabricated in this static build. What the Hub cannot prove, it says so.</p>', '#d86cff')
    + '</div>'
    + '<p class="hub-note">Your relationship with NayaNET: identity, runtime state, data, trust. Infrastructure stays under the hood.</p>';
}
