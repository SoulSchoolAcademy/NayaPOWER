/* SETTINGS — THE CONTROL DECK.
   Human controls first; diagnostics are secondary and read from current artifacts. */
function SettingsRoom(){
  const {el,Board,Pill}=window.NayaUI,R=window.NayaRuntime;
  const wrap=el('div','room-scene'), ACC='var(--accent-settings)';
  wrap.style.setProperty('--room-accent',ACC);

  const human=Board({accent:ACC,icon:'gear',title:'Your intelligence, your rules',sub:'Identity · Privacy · Authority · Connections · Notifications · Data · Security · Appearance',lift:false});
  const cats=['Identity','Privacy','Authority','Connections','Notifications','Data & Security','Appearance'];
  human.body.innerHTML='<p style="color:var(--ink-dim);font-size:16px;line-height:1.6;max-width:720px">A setting is only real when its persistence/enforcement scope is known. Local presentation preferences must never masquerade as governed privacy or authority controls.</p>'+
    '<div class="domain-grid" style="margin-top:16px">'+cats.map(x=>'<div class="domain"><strong>'+esc(x)+'</strong><p>Governed control surface · exact runtime scope must be verified before modification is enabled.</p></div>').join('')+'</div>';
  wrap.appendChild(human);

  const ownership=Board({accent:ACC,icon:'shield',title:'Your Intelligence',sub:'Private by default · shared by choice · collective by consent',lift:false});
  ownership.body.innerHTML='<div class="metric-ribbon">'+
    '<div class="metric"><b>YOURS</b><span>INTELLIGENCE</span></div>'+
    '<div class="metric"><b>CHOICE</b><span>SHARING</span></div>'+
    '<div class="metric"><b>LAW</b><span>AUTHORITY</span></div>'+
    '<div class="metric"><b>PROOF</b><span>CONSEQUENCE</span></div></div>';
  wrap.appendChild(ownership);

  const health=Board({accent:ACC,icon:'core',title:'System Health',sub:'Advanced · current build truth, not flattering static scores',lift:false});
  health.body.innerHTML='<div class="empty-instrument"><strong>Loading completion truth…</strong><p>The control deck reads the branch completion matrix instead of hardcoding a stale score.</p></div>';
  wrap.appendChild(health);

  const registry=Board({accent:ACC,icon:'connect',title:'Door registry',sub:'Canonical capability inventory',lift:false});
  registry.body.innerHTML='<div class="empty-instrument"><strong>Loading Smart Door registry…</strong><p>Connection status comes from the canonical registry artifact when this deployment can load it.</p></div>';
  wrap.appendChild(registry);

  hydrate();
  return wrap;

  async function hydrate(){
    const matrix=await R.loadCompletionMatrix();
    if(matrix.ok){
      const m=matrix.data, rooms=m.rooms||{}, journeys=m.whole_app_journeys||[];
      const counts={};
      Object.values(rooms).forEach(x=>counts[x.state]=(counts[x.state]||0)+1);
      health.body.innerHTML='<div class="metric-ribbon">'+
        metric(Object.keys(rooms).length,'ROOMS DECLARED')+
        metric(counts.IMPLEMENTED||0,'IMPLEMENTED')+
        metric(counts.PRODUCTION_PROVEN||0,'PRODUCTION PROVEN')+
        metric(journeys.filter(x=>x.state==='PRODUCTION_PROVEN').length+'/'+journeys.length,'JOURNEYS PROVEN')+
        '</div><div class="intelligence-list" style="margin-top:16px">'+
        Object.entries(rooms).map(([id,x])=>'<div class="intel-row"><div class="intel-type">'+esc(id)+'</div><div class="intel-title">'+esc(x.metaphor||id)+'</div><div class="meta-row"><span>'+esc(x.state)+'</span><span>RUNTIME '+esc(x.runtime||'—')+'</span></div></div>').join('')+
        '</div><p style="color:var(--muted);font-size:16px;margin-top:14px">Overall: <b style="color:var(--ink)">'+esc(m.overall_state)+'</b> · target '+esc(m.quality_target?.target||'10')+' · IMPLEMENTED is not DONE.</p>';
    }else{
      health.body.innerHTML='<div class="empty-instrument"><strong>Completion matrix unavailable</strong><p>'+esc(matrix.message)+'</p></div>';
    }

    const reg=await R.loadDoorRegistry();
    if(reg.ok){
      registry.body.innerHTML='<div class="intelligence-list">'+(reg.data.doors||[]).map(d=>
        '<div class="intel-row"><div class="intel-title">'+esc(d.name)+'</div><div class="meta-row"><span>'+esc(d.status)+'</span><span>'+esc(d.health)+'</span><span>'+esc((d.capabilities||[]).join(' · '))+'</span></div></div>'
      ).join('')+'</div><p style="color:var(--muted);font-size:16px;margin-top:12px">Source: '+esc(reg.source)+'</p>';
    }else registry.body.innerHTML='<div class="empty-instrument"><strong>Canonical registry unavailable</strong><p>'+esc(reg.message)+'</p></div>';
  }
  function metric(v,l){return '<div class="metric"><b>'+esc(v)+'</b><span>'+esc(l)+'</span></div>';}
  function esc(x){return String(x??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
}
window.NayaRooms=window.NayaRooms||{};window.NayaRooms.settings=SettingsRoom;
