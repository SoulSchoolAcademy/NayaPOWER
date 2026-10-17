function notes(){
  var spaces = [{ id:'personal', name:'Personal' }, { id:'family', name:'Family' }, { id:'project', name:'Project' },
    { id:'business', name:'Business' }, { id:'research', name:'Research' }, { id:'collective', name:'Collective' }]
    .concat((NayaHub.d.spaces || []).map(function(s){ return { id:s.id, name:s.name }; }));
  var spaceOpts = spaces.map(function(s){ return '<option value="'+s.id+'">'+NayaHub.esc(s.name)+'</option>'; }).join('');
  var existing = '';
  try{
    existing = NOTES().slice(0, 6).map(function(n){
      return '<div class="ws-row"><b>'+NayaHub.esc(String(n.text).split(/[.!?\n]/)[0].slice(0, 70))+'</b>'
        + '<span>'+NayaHub.hts(n.createdAt)+' · '+NayaHub.esc(n.type || 'INSIGHT')+' · '+NayaHub.esc(n.space || 'personal')+'</span></div>';
    }).join('');
  }catch(e){}
  return head(S.notes)
    + '<span class="hub-state" data-s="READY">READY</span>'
    + card('CAPTURE',
        '<div class="hub-form"><input id="hubNoteTitle" placeholder="Title (optional)…" style="width:100%;box-sizing:border-box"></div>'
        + '<div class="hub-form"><textarea id="hubNoteText" rows="3" placeholder="What should the Hub remember?"></textarea></div>'
        + '<div class="hub-form"><select id="hubNoteType"><option>INSIGHT</option><option>DECISION</option><option>LESSON</option><option>QUESTION</option></select>'
        + '<select id="hubNoteSpace" aria-label="File into space">'+spaceOpts+'</select>'
        + '<button data-hub-action="note-save">CAPTURE</button></div>'
        + '<div id="hubNoteStatus" class="hub-dim" role="status"></div>', '#9d75ff')
    + '<h3 class="hub-h">RECENT CAPTURES</h3><div class="ws-list">'
    + (existing || '<div class="ws-empty">Nothing captured yet.</div>') + '</div>'
    + '<p class="hub-note">Captured notes persist, surface in your Library and Lists, feed the Today diary — and every capture is receipted in the Ledger.</p>';
}
