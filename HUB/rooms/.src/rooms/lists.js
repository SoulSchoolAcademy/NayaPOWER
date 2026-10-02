function lists(){
  var tab = NayaHub.d.prefs.listTab || 'saved';
  function titleFor(id){
    var b = document.querySelector('.block [data-id="'+id+'"]');
    if (b){
      var blk = b.closest('.block');
      var h = blk && Q('h3', blk);
      return h ? txt(h).slice(0, 70) : id;
    }
    var ns = [];
    try{ ns = NOTES(); }catch(e){}
    var n = ns.filter(function(x){ return x.id === id; })[0];
    if (n) return String(n.text).split(/[.!?\n]/)[0].slice(0, 70);
    return id;
  }
  function rowsFor(ids, kind){
    if (!ids.length) return '<div class="ws-empty">Nothing here yet — mark boards in the feed and they land here.</div>';
    return '<div class="ws-list">' + ids.map(function(id){
      return '<div class="ws-row"><b>'+NayaHub.esc(titleFor(id))+'</b><span class="hub-dim">'+id+'</span>'
        + '<button data-hub-action="item-unsave" data-k="'+kind+'" data-v="'+NayaHub.esc(id)+'">REMOVE</button></div>';
    }).join('') + '</div>';
  }
  var tabs = [['saved','SAVED'],['favorites','FAVORITES'],['loves','LOVED'],['top','TOP RATED'],['collections','COLLECTIONS']].map(function(x){
    return '<button data-hub-action="list-tab" data-v="'+x[0]+'" class="hub-tab'+(tab===x[0]?' on':'')+'">'+x[1]+'</button>';
  }).join('');
  var body = '';
  if (tab === 'collections'){
    var cols = NayaHub.d.collections;
    var candidates = [];
    ['saved','favorites','loves'].forEach(function(k){
      Object.keys((function(){ try{ return JSON.parse(localStorage.getItem('nayanet_509_aaa')||'{}')[k]||{}; }catch(e){ return {}; } })()).forEach(function(id){
        if (!candidates.some(function(c){ return c.id === id; })) candidates.push({ id:id, title:titleFor(id) });
      });
    });
    var opts = candidates.map(function(c){ return '<option value="'+NayaHub.esc(c.id)+'">'+NayaHub.esc(c.title).slice(0,60)+'</option>'; }).join('');
    body = '<div class="hub-form"><input id="hubColName" placeholder="New collection name…"><button data-hub-action="col-create">CREATE</button></div>'
      + (cols.map(function(c){
          var items = c.items.map(function(it){
            return '<div class="ws-row"><b>'+NayaHub.esc(it.title).slice(0,80)+'</b><span class="hub-dim">'+NayaHub.esc(it.ref)+'</span>'
              + '<button data-hub-action="col-remove" data-c="'+c.id+'" data-v="'+NayaHub.esc(it.ref)+'">REMOVE</button></div>';
          }).join('') || '<div class="ws-empty">Empty — add boards below.</div>';
          return '<h3 class="hub-h">'+NayaHub.esc(c.name).toUpperCase()+' <button data-hub-action="col-delete" data-v="'+c.id+'" class="hub-danger" style="font-size:10px;padding:6px 10px;min-height:0">DELETE</button></h3>'
            + '<div class="ws-list">'+items+'</div>'
            + (opts ? '<div class="hub-form"><select id="hubColPick-'+c.id+'">'+opts+'</select><button data-hub-action="col-add" data-c="'+c.id+'">ADD</button></div>' : '<p class="hub-dim">Save or favorite boards in the feed to add them here.</p>');
        }).join('') || '<div class="ws-empty">No collections yet. Name one above — “Decisions”, “Ideas”, “Lessons”.</div>');
  } else if (tab === 'top'){
    var top = Object.keys(state.ratings || {}).filter(function(k){ return state.ratings[k] >= 4; });
    body = rowsFor(top, 'ratings');
  } else {
    var ids = Object.keys(state[tab] || {});
    body = rowsFor(ids, tab);
  }
  return head(S.lists)
    + '<div class="hub-tabs">'+tabs+'</div>'
    + body
    + '<p class="hub-note">The human-friendly organization layer. Lists organize canonical intelligence — they never become another storage system.</p>';
}
