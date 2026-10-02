/* SMART CONNECT — THE PORTAL BAY. Canonical registry drives the door inventory. */
function ConnectRoom() {
  const { el, Board, DoorCard, toast } = window.NayaUI;
  const R = window.NayaRuntime;
  const wrap = el('div','room-scene');
  wrap.style.setProperty('--room-accent','var(--accent-connect)');

  const intro = Board({
    accent:'var(--accent-connect)',icon:'connect',title:'One brain. Many doors.',
    sub:'Connection reveals capability. LAW determines permission. ACT executes. VERIFY proves.',
    lift:false
  });
  intro.body.innerHTML='<p style="color:var(--ink-dim);font-size:13.5px;max-width:720px;line-height:1.6">Connect your intelligence without creating another brain. Authentication, authorization, health, and connection are separate states. <b style="color:var(--ink)">CONNECTED ≠ AUTHORIZED.</b></p>';
  wrap.appendChild(intro);

  const sourceLine=el('div','room-status-line','<span class="led"></span><span>LOADING CANONICAL SMART DOOR REGISTRY…</span>');
  wrap.appendChild(sourceLine);
  const grid=el('div','board-grid');wrap.appendChild(grid);

  loadRegistry();

  const road=Board({accent:'var(--accent-connect)',icon:'clock',title:'Roadmap horizon',sub:'Ideas are not registered/live Doors',lift:false});
  road.body.innerHTML='<div style="display:grid;gap:10px">'+R.DOOR_ROADMAP.map(x=>
    '<div style="display:flex;gap:12px;align-items:baseline;padding:11px 4px;border-bottom:1px solid var(--line-soft)"><span class="pill soon"><span class="dot"></span>IDEA</span><div><b style="font-size:13.5px">'+esc(x.name)+'</b><div style="color:var(--muted);font-size:12.5px;margin-top:2px">'+esc(x.desc)+'</div></div></div>'
  ).join('')+'</div>';
  wrap.appendChild(road);

  const law=Board({accent:'var(--accent-connect)',icon:'shield',title:'The Door Law',sub:'One capability interface; authority remains elsewhere',lift:false});
  law.body.innerHTML='<ul style="margin:0;padding-left:18px;color:var(--ink-dim);font-size:13px;display:grid;gap:8px">'+
    '<li>Doors expose what Naya <b style="color:var(--ink)">can</b> do. LAW decides what Naya <b style="color:var(--ink)">may</b> do.</li>'+
    '<li><b style="color:var(--ink)">CONNECTED ≠ AUTHORIZED.</b> Retrieval also does not grant authorization.</li>'+
    '<li>Consequential crossings require the applicable authority path and verification.</li>'+
    '<li>A registry entry is discoverability metadata, not permission.</li>'+
    '</ul>';
  wrap.appendChild(law);
  return wrap;

  async function loadRegistry(){
    const res=await R.loadDoorRegistry();
    let doors,sourceVerified=false;
    if(res.ok){
      sourceVerified=true;
      doors=(res.data.doors||[]).map((d,i)=>normalize(d,i));
      sourceLine.innerHTML='<span class="led"></span><span>CANONICAL REGISTRY LOADED · '+esc(res.data.version||'V1')+' · '+doors.length+' DOORS</span>';
    }else{
      doors=[...R.DOORS];
      sourceLine.innerHTML='<span class="led" style="background:var(--orange);box-shadow:0 0 10px var(--orange)"></span><span>REGISTRY FETCH UNAVAILABLE · SHOWING BUNDLED MIRROR AS NOT VERIFIED</span>';
    }
    grid.innerHTML='';
    doors.sort((a,b)=>(a.priority??99)-(b.priority??99)).forEach(door=>{
      const card=DoorCard(door,d=>{
        if(!sourceVerified){toast('Canonical registry is not loaded; connection action is withheld rather than inferred from the mirror.',d.accent);return;}
        const out=R.connectDoor(d.id);
        toast(out.message,d.accent);
      });
      grid.appendChild(card);
    });
  }

  function normalize(d,priority){
    const short=String(d.door_id||'').replace(/^DOOR-/,'').toLowerCase();
    const color={github:'#55b9ee',mcp:'#d86cff',ai:'#9d75ff',data:'#55e39a',email:'#ff9a5a',calendar:'#f1d75a',voice:'#ff5e6c',web:'#6675ff',naya:'#b8ee57'}[short]||'#40d3bb';
    const icon={github:'github',mcp:'mcp',ai:'spark',data:'db',email:'mail',calendar:'cal',voice:'mic',web:'connect',naya:'a2a'}[short]||'connect';
    return {id:short,name:d.name,for:(d.capabilities||[]).join(' · '),desc:'Authority: '+(d.required_authority||'governed scope')+' · Health: '+(d.health||'unknown'),accent:color,icon,status:String(d.status||'').startsWith('LIVE')?'live':'contract',priority,registry:d.status};
  }
  function esc(x){return String(x??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
}
window.NayaRooms=window.NayaRooms||{};window.NayaRooms.connect=ConnectRoom;
