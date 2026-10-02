function spaces(){
  var BASE = [
    { id:'personal', name:'Personal', rule:'PRIVATE BY DEFAULT', color:'#d86cff', desc:'Only you. Captures land here unless you move them.' },
    { id:'family', name:'Family', rule:'SHARED BY CHOICE', color:'#ff9a5a', desc:'The people closest to you. Nothing enters without your choice.' },
    { id:'project', name:'Project', rule:'SHARED BY CHOICE', color:'#6675ff', desc:'Work with a boundary around it. Members see the work, not your life.' },
    { id:'business', name:'Business', rule:'SHARED BY CHOICE', color:'#55b9ee', desc:'The professional surface. Governed like everything else.' },
    { id:'research', name:'Research', rule:'COLLECTIVE BY CONSENT', color:'#b8ee57', desc:'Exploration that can compound — shared only with consent.' },
    { id:'collective', name:'Collective', rule:'PUBLIC BY DECISION', color:'#55e39a', desc:'Many minds, one intelligence. Publication is always a decision.' }
  ];
  var all = BASE.concat(NayaHub.d.spaces || []);
  var notes = [];
  try{ notes = NOTES(); }catch(e){}
  var cards = all.map(function(sp){
    var n = notes.filter(function(x){ return (x.space || 'personal') === sp.id; }).length;
    return '<article class="ws-card" style="--accent:'+sp.color+'"><h3>'+NayaHub.esc(sp.name)+'</h3>'
      + '<p><span class="hub-chip">'+sp.rule+'</span></p>'
      + '<p class="hub-dim">'+NayaHub.esc(sp.desc)+'</p>'
      + '<p><b>'+n+'</b> captured notes visible here</p></article>';
  }).join('');
  return head(S.spaces)
    + '<span class="hub-state" data-s="READY">READY · '+all.length+' SPACES</span>'
    + '<div class="ws-grid">'+cards+'</div>'
    + '<div class="hub-form"><input id="hubSpaceName" placeholder="New space name…"><button data-hub-action="space-create">CREATE SPACE</button></div>'
    + '<p class="hub-note">Spaces are context boundaries, not folders. Private by default · shared by choice · collective by consent · public by decision.</p>';
}
