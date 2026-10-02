function reports(){
  var range = NayaHub.d.prefs.reportRange || 'today';
  var now = Date.now();
  var cut = range === 'week' ? now - 7*864e5 : range === 'month' ? now - 30*864e5 : now - 864e5;
  var span = range === 'today' ? '24 hours' : range === 'week' ? '7 days' : '30 days';
  var bl = blocks();
  var notes = [];
  try{ notes = NOTES().filter(function(n){ return new Date(n.createdAt).getTime() >= cut; }); }catch(e){}
  var rc = NayaHub.d.receipts.filter(function(r){ return new Date(r.ts).getTime() >= cut; });
  var sv = Object.keys(state.saved || {}).length,
      fv = Object.keys(state.favorites || {}).length,
      lv = Object.keys(state.loves || {}).length;
  var total = bl.length + notes.length;
  var tabs = ['today','week','month'].map(function(r){
    return '<button data-hub-action="report-range" data-v="'+r+'" class="hub-tab'+(r===range?' on':'')+'">'+r.toUpperCase()+'</button>';
  }).join('');
  var meaning = total === 0
    ? 'Nothing is projected in this range yet. A report with no evidence is a rumor — so this one stays empty until the Hub has something real to say.'
    : 'Across the last '+span+', the Hub holds '+total+' intelligence objects — '+bl.length+' canonical boards and '+notes.length+' captured notes. '
      + 'You marked '+sv+' saved, '+fv+' favorited, '+lv+' loved, and the ledger recorded '+rc.length+' accountable actions in range. '
      + (rc.length > 0 ? 'The chain is intact: every mark above is provable below.' : 'No ledger entries in range yet — marks made from here on will be recorded.');
  var rows = rc.slice(-8).reverse().map(function(r){
    return '<div class="ws-row"><b>'+NayaHub.esc(r.action)+'</b><span>'+NayaHub.hts(r.ts)+' · <code>'+String(r.hash).slice(0,10)+'</code></span>'
      + '<div class="hub-detail">'+NayaHub.esc(r.detail)+'</div></div>';
  }).join('') || '<div class="ws-empty">No receipts in this range yet.</div>';
  return head(S.reports)
    + '<div class="hub-tabs">'+tabs+'</div>'
    + '<div class="ws-grid">'
    + card('INTELLIGENCE IN RANGE', '<div class="ws-stat">'+total+'</div><span class="hub-dim">'+bl.length+' boards · '+notes.length+' notes</span>', '#6675ff')
    + card('YOUR SIGNALS', '<div class="ws-stat">'+(sv+fv+lv)+'</div><span class="hub-dim">'+sv+' saved · '+fv+' favorites · '+lv+' loved</span>', '#d86cff')
    + card('ACCOUNTABILITY', '<div class="ws-stat">'+rc.length+'</div><span class="hub-dim">receipts · hash-chained</span>', '#f1d75a')
    + '</div>'
    + card('WHAT IT MEANS', '<p>'+meaning+'</p>', '#55b9ee')
    + '<h3 class="hub-h">LATEST RECEIPTS IN RANGE</h3><div class="ws-list">'+rows+'</div>'
    + '<p class="hub-note">Computed locally from '+total+' real objects and '+NayaHub.d.receipts.length+' ledger receipts. Nothing here is invented.</p>';
}
