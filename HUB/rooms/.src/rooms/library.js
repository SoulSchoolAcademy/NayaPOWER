function library(){
  var q = (NayaHub.d.prefs.libQ || '').toLowerCase();
  var facet = NayaHub.d.prefs.libFacet || 'all';
  var tcut = NayaHub.d.prefs.libTime || 'all';
  var now = Date.now();
  var cut = tcut === '7d' ? now - 7*864e5 : (tcut === '30d' ? now - 30*864e5 : 0);
  var insp = NayaHub.d.prefs.libInspect || null;
  var idx = [];
  blocks().forEach(function(b, i){
    var h3 = Q('h3', b);
    var title = h3 ? txt(h3) : ('Board ' + (i+1));
    var idBtn = Q('[data-act][data-id]', b);
    var id = idBtn ? idBtn.getAttribute('data-id') : ('board-' + i);
    var kickEl = Q('.kicker, .ws-kicker, [class*="kicker"]', b);
    idx.push({ kind:'board', id:id, title:title, kicker: kickEl ? txt(kickEl).slice(0,60) : 'SMART NOTE',
      color:'#6675ff', text: txt(b).slice(0, 6000), el:i, ts: 0 });
  });
  var notes = [];
  try{ notes = NOTES(); }catch(e){}
  notes.forEach(function(n, i){
    idx.push({ kind:'note', id: n.id || ('note-'+i),
      title: String(n.text || '').split(/[.!?\n]/)[0].slice(0, 80) || 'Captured note',
      kicker: String(n.type || 'INSIGHT'), color:'#55e39a', text: String(n.text || ''),
      el:-1, ts: new Date(n.createdAt).getTime() || 0 });
  });
  function match(o){
    if (facet === 'saved' && !(state.saved || {})[o.id]) return false;
    if (facet === 'favorites' && !(state.favorites || {})[o.id]) return false;
    if (facet === 'notes' && o.kind !== 'note') return false;
    if (facet === 'boards' && o.kind !== 'board') return false;
    if (cut && o.ts && o.ts < cut) return false;
    if (!q) return true;
    return (o.title + ' ' + o.kicker + ' ' + o.text).toLowerCase().indexOf(q) >= 0;
  }
  var res = idx.filter(match);
  var facets = [['all','ALL'],['boards','BOARDS'],['notes','CAPTURED'],['saved','SAVED'],['favorites','FAVORITES']].map(function(f){
    return '<button data-hub-action="lib-facet" data-v="'+f[0]+'" class="hub-tab'+(facet===f[0]?' on':'')+'">'+f[1]+'</button>';
  }).join('');
  var times = [['all','ALL TIME'],['7d','7 DAYS'],['30d','30 DAYS']].map(function(f){
    return '<button data-hub-action="lib-time" data-v="'+f[0]+'" class="hub-tab'+(tcut===f[0]?' on':'')+'">'+f[1]+'</button>';
  }).join('');
  var rows = res.slice(0, 80).map(function(o){
    var marks = ((state.saved||{})[o.id] ? ' 🔖' : '') + ((state.favorites||{})[o.id] ? ' ★' : '') + ((state.loves||{})[o.id] ? ' ❤' : '');
    var open = o.kind === 'board' ? '<button data-hub-action="lib-open" data-v="'+o.el+'">OPEN</button>' : '';
    var open2 = '<button data-hub-action="lib-inspect" data-v="'+o.id+'">'+(insp===o.id ? 'CLOSE' : 'INSPECT')+'</button>';
    var detail;
    if (insp === o.id){
      detail = '<div class="hub-detail hub-fulltext">'+NayaHub.esc(o.text).slice(0, 3000)+'</div>';
    } else if (q){
      detail = (function(){
        var t = (o.title + ' ' + o.kicker + ' ' + o.text).toLowerCase();
        var p = t.indexOf(q);
        var raw = o.title + ' — ' + o.text;
        return '<div class="hub-detail hub-dim">'+NayaHub.esc(raw.slice(Math.max(0, p - 40), p + 120)) + '…</div>';
      })();
    } else {
      detail = '<div class="hub-detail hub-dim">'+NayaHub.esc(o.kicker)+'</div>';
    }
    return '<div class="ws-row"><i class="dot" style="background:'+o.color+';color:'+o.color+'"></i>'
      + '<b>'+NayaHub.esc(o.title).slice(0, 90)+marks+'</b>'
      + '<span>'+o.kind.toUpperCase()+' · '+NayaHub.esc(o.kicker).slice(0, 40)+'</span>' + open + open2
      + detail + '</div>';
  }).join('') || '<div class="ws-empty">'+(q ? 'No matches for “'+NayaHub.esc(NayaHub.d.prefs.libQ)+'”. The library never invents results.' : 'The library is empty.')+'</div>';
  return head(S.library)
    + '<span class="hub-state" data-s="READY">READY</span>'
    + '<div class="hub-search"><input id="hubLibQ" data-hub-input="lib-q" placeholder="Search boards, notes, layers — title, meaning, source…" value="'+NayaHub.esc(NayaHub.d.prefs.libQ || '')+'"></div>'
    + '<div class="hub-tabs">'+facets+'</div>'
    + '<div class="hub-tabs">'+times+'</div>'
    + '<div class="ws-list">'+rows+'</div>'
    + '<p class="hub-note">'+res.length+' of '+idx.length+' objects · deliberate retrieval of preserved intelligence — never a second brain.</p>';
}
