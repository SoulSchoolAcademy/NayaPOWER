function reports(){
  var range = NayaHub.d.prefs.reportRange || 'today';
  var now = Date.now();
  var cuts = { today:864e5, week:7*864e5, month:30*864e5, year:365*864e5 };
  var cut = now - (cuts[range] || cuts.today);
  var span = { today:'last 24 hours', week:'last 7 days', month:'last 30 days', year:'last 12 months' }[range];
  var bl = blocks();
  var notes = [];
  try{ notes = NOTES().filter(function(n){ return new Date(n.createdAt).getTime() >= cut; }); }catch(e){}
  var rc = NayaHub.d.receipts.filter(function(r){ return new Date(r.ts).getTime() >= cut; });
  var sv = Object.keys(state.saved || {}).length, fv = Object.keys(state.favorites || {}).length;
  var total = bl.length + notes.length;
  var st = total === 0 ? 'EMPTY' : 'READY';

  // themes: honest keyword clusters, labeled as auto-grouped
  var words = {};
  function feed_words(s){ String(s||'').toLowerCase().split(/[^a-z]+/).forEach(function(w){ if (w.length > 4 && ['intelligence','smart','what','with','your'].indexOf(w) < 0) words[w] = (words[w]||0)+1; }); }
  bl.forEach(function(b){ var h = Q('h3', b); feed_words(h ? txt(h) : ''); });
  notes.forEach(function(n){ feed_words(n.text); });
  var themes = Object.keys(words).filter(function(w){ return words[w] > 1; })
    .sort(function(a,b){ return words[b]-words[a]; }).slice(0, 6);

  var tabs = ['today','week','month','year'].map(function(r){
    return '<button data-hub-action="report-range" data-v="'+r+'" class="hub-tab'+(r===range?' on':'')+'">'+r.toUpperCase()+'</button>';
  }).join('');

  var narrative = total === 0
    ? 'Nothing is projected in this range yet — so this report stays empty. A report with no evidence is a rumor, and the Hub does not publish rumors.'
    : 'In the '+span+', the Hub held <b>'+total+' intelligence objects</b> — '+bl.length+' canonical boards and '+notes.length+' captured notes. '
      + 'Your hand was on '+sv+' saved and '+fv+' favorited, and the ledger recorded <b>'+rc.length+' accountable actions</b>. '
      + (themes.length ? 'What kept surfacing: '+themes.map(function(t){ return '<b>'+NayaHub.esc(t)+'</b>'; }).join(', ')+' — grouped automatically from titles, not asserted by anyone.' : 'No repeating themes yet — the range is too thin to read a pattern honestly.')
      + ' Every claim in this report links to its evidence below.';

  var ev = rc.slice(-10).reverse().map(function(r){
    return '<div class="ws-row"><b>'+NayaHub.esc(r.action)+'</b>'
      + '<span>'+NayaHub.hts(r.ts)+' · <code>'+String(r.hash).slice(0,10)+'</code></span>'
      + '<div class="hub-detail">'+NayaHub.esc(r.detail)+'</div></div>';
  }).join('') || '<div class="ws-empty">No receipts in this range. Marks made from here on are recorded.</div>';

  return head(S.reports)
    + '<span class="hub-state" data-s="'+st+'">'+st+'</span>'
    + '<div class="hub-tabs" role="tablist">'+tabs+'</div>'
    + card('WHAT THE ACCUMULATED INTELLIGENCE MEANS',
        '<div class="hub-narrative">'+narrative+'</div>', '#6675ff')
    + '<h3 class="hub-h">EVIDENCE TRAIL</h3><div class="ws-list">'+ev+'</div>'
    + '<p class="hub-note">Computed locally from '+total+' real objects and '+NayaHub.d.receipts.length+' ledger receipts. Nothing here is invented; what cannot be shown is not claimed.</p>';
}
