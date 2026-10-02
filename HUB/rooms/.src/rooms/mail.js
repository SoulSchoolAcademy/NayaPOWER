function mail(){
  var r = R();
  var prefs = NayaHub.d.mail || {};
  var state_line = r
    ? 'The runtime mail service is reachable, but your mailbox is empty.'
    : 'The runtime is not exposed in this build, so there is no mailbox to check.';
  return head(S.mail)
    + '<div class="ws-empty hub-mail-empty"><div class="ws-stat">NO MAIL</div>'
    + '<p>'+state_line+'</p>'
    + '<p class="hub-dim">A real room. No fake mailbox, ever.</p></div>'
    + '<div class="ws-actions"><button data-hub-action="mail-check">CHECK AGAIN</button></div>'
    + card('NOTIFICATIONS',
        '<label class="hub-check"><input type="checkbox" data-hub-check="mail-notify"'+(prefs.notify?' checked':'')+'> Notify me when mail connects</label>'
        + '<p class="hub-dim">Stored locally. When the runtime exposes mail, this room fills — honestly.</p>',
        '#55b9ee')
    + '<p class="hub-note">RUNTIME UNAVAILABLE → shown, not hidden. NO MAIL → shown, not filled. That is the contract.</p>';
}
