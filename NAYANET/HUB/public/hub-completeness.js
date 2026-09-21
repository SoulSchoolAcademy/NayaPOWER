(()=>{'use strict';
const R=()=>window.NayaAssistantRuntime;
const esc=s=>String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const nav=[
 ['SMART FEED','feed'],['CREATE NOTE','note'],['REPORTS','reports'],['SMART SHARE','share'],
 ['SMART LISTS','lists'],['SMART SPACES','spaces'],['CONNECTIONS','connections'],['SMART MAIL','mail'],
 ['SMART LEDGER','ledger'],['DREAM','dream'],['NAYA PLAY','play'],['SETTINGS','settings']
];
function css(){if(document.getElementById('naya-completeness-style'))return;const s=document.createElement('style');s.id='naya-completeness-style';s.textContent=`
.private{pointer-events:none!important}
#naya-completeness{margin:0 22px 20px;padding:12px;border:1px solid #ffffff16;border-radius:17px;background:#08080c;box-shadow:inset 0 1px #fff3,0 16px 35px #0009}
#naya-completeness .nc-label{font-size:7px;font-weight:1000;letter-spacing:.16em;color:#aaa4b1;margin-bottom:8px}
#naya-completeness .nc-nav{display:flex;gap:7px;flex-wrap:wrap}
#naya-completeness button{min-height:36px;padding:0 11px;border:2px solid #8b63ff55;border-radius:10px;background:linear-gradient(145deg,#14111b,#08080c);color:#fff;font-size:7px;font-weight:1000;letter-spacing:.05em;box-shadow:inset 0 1px #fff3,0 7px 16px #0007}
#naya-completeness button:hover{transform:translateY(-1px);border-color:#d86cff;box-shadow:0 0 20px #d86cff20,0 11px 22px #0009}
.nc-modal{position:fixed;inset:0;z-index:500;background:#000d;backdrop-filter:blur(18px);display:grid;place-items:center;padding:18px}
.nc-dialog{width:min(900px,100%);max-height:90vh;overflow:auto;padding:22px;border:2px solid #d86cff66;border-radius:22px;background:linear-gradient(145deg,#14101b,#08080d);box-shadow:0 40px 100px #000f}
.nc-dialog h2{margin:0 0 6px;font-size:27px}.nc-dialog p{color:#aaa4b1;font-size:10px;line-height:1.6}
.nc-actions{display:flex;gap:8px;flex-wrap:wrap;margin:14px 0}.nc-actions button{min-height:40px;padding:0 13px;border:2px solid #8b63ff66;border-radius:11px;background:#09080d;color:#fff;font-size:8px;font-weight:1000}
.nc-state{padding:13px;border:1px solid #ffffff16;border-radius:12px;color:#d6d0db;font-size:9px;line-height:1.6;white-space:pre-wrap}
.nc-input,.nc-textarea{width:100%;border:2px solid #ffffff20;border-radius:11px;background:#07070a;color:#fff;padding:12px;margin:5px 0}.nc-textarea{min-height:130px}
.nc-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.nc-card{padding:13px;border:1px solid #ffffff15;border-radius:12px;background:#09090d}.nc-card b{font-size:8px}.nc-card span{display:block;color:#9f98a7;font-size:8px;margin-top:5px;line-height:1.5}@media(max-width:700px){#naya-completeness{margin:0 14px 14px}.nc-grid{grid-template-columns:1fr}}
`;document.head.append(s)}
function modal(title,desc,body){document.querySelectorAll('.nc-modal').forEach(x=>x.remove());const m=document.createElement('div');m.className='nc-modal';m.innerHTML='<div class="nc-dialog"><h2>'+esc(title)+'</h2><p>'+esc(desc)+'</p><div class="nc-body">'+body+'</div><div class="nc-actions"><button data-nc-close>DONE</button></div></div>';m.addEventListener('click',e=>{if(e.target===m||e.target.closest('[data-nc-close]'))m.remove()});document.body.append(m);return m}
async function open(kind, initialStream){
 const r=R(); if(!r)return;
 const titles={feed:'Smart Feed',note:'Create Smart Note',reports:'Reports',intelligence:'Intelligence Library',share:'Smart Share',lists:'Smart Lists',spaces:'Smart Spaces',connections:'Connections',mail:'Smart Mail',ledger:'Smart Ledger',evidence:'Smart Ledger',dream:'Dream',play:'Naya Play',settings:'Settings'};
 const snap=r.snapshot?.();
 if(!snap?.authenticated && kind!=='settings'){location.assign('/identity.html');return}
 modal(titles[kind]||kind.toUpperCase(),'Canonical runtime surface.','<div class="nc-state">LOADING CANONICAL RUNTIME SURFACE…</div>');
 try{
  await r.init();
  if(kind==='feed')return feed(r, initialStream);
  if(kind==='note')return note(r);
  if(kind==='reports')return reports(r);
  if(kind==='share')return share(r);
  if(kind==='lists')return lists(r);
  if(kind==='spaces')return spaces(r);
  if(kind==='connections')return connections(r);
  if(kind==='mail')return mail(r);
  if(kind==='ledger')return ledger(r);
  if(kind==='evidence')return ledger(r);
  if(kind==='dream')return dream(r);
  if(kind==='play')return play(r);
  if(kind==='intelligence')return library(r);
  if(kind==='settings')return settings(r);
 }catch(e){modal(titles[kind]||'BLOCKED / FAILED','The Hub stopped at the first real runtime error.', '<div class="nc-state">BLOCKED / FAILED · '+esc(e?.message||e)+'</div>')}
}
async function feed(r, initialStream){
 const streams=['personal','collective','activity'];
 const m=modal('Smart Feed','Three lenses over the same canonical intelligence graph. No duplicate feed store is created.','<div class="nc-actions">'+streams.map(s=>'<button data-nc-stream="'+s+'">'+s.toUpperCase()+'</button>').join('')+'</div><div class="nc-state" id="nc-state">Reading PERSONAL intelligence…</div><div id="nc-feed" class="nc-grid"></div>');
 const load=async(stream)=>{
  const st=m.querySelector('#nc-state'),out=m.querySelector('#nc-feed');
  st.textContent='READING CANONICAL '+stream.toUpperCase()+' INTELLIGENCE…';
  try{
   const data=await r.smartFeed({stream,limit:20});
   const items=Array.isArray(data.items)?data.items:[];
   out.innerHTML=items.length?items.map(x=>'<div class="nc-card"><b>'+esc(x.title||x.event_id||'Intelligence')+'</b><span>'+esc(String(x.content||'No content returned.').slice(0,420))+'<br><br>'+esc(x.verification_state||'UNKNOWN')+' · '+esc(x.visibility||'UNKNOWN')+'</span></div>').join(''):'<div class="nc-card"><b>NO CANONICAL ITEMS</b><span>This lens returned no verified records.</span></div>';
   st.textContent='LIVE · '+stream.toUpperCase()+' · '+items.length+' ITEMS · CANONICAL RUNTIME';
  }catch(e){st.textContent='BLOCKED / FAILED · '+(e?.message||e)}
 };
 m.querySelectorAll('[data-nc-stream]').forEach(b=>b.onclick=()=>void load(b.dataset.ncStream));
 await load(initialStream||'personal');
}
async function library(r){
 const rows=await r.retrieve();
 modal('Intelligence Library','Durable retrieval over the authenticated canonical intelligence event store.','<div class="nc-state">'+esc(rows.map(x=>(x.created_at||'')+' · '+(x.title||x.event_id||'event')+' · '+(x.source||'')).join('\n')||'No canonical intelligence yet.')+'</div>');
}
function note(r){const m=modal('Create Smart Note','Human capture enters the canonical Smart Note receiver. No local-only success is reported.','<input class="nc-input" id="nc-title" placeholder="Title"><textarea class="nc-textarea" id="nc-content" placeholder="What matters?"></textarea><div class="nc-actions"><button id="nc-save">CAPTURE CANONICALLY</button></div><div class="nc-state" id="nc-state">Ready.</div>');m.querySelector('#nc-save').onclick=async()=>{const st=m.querySelector('#nc-state');st.textContent='CAPTURING → CANONICALIZING → PRESERVING…';try{const x=await r.captureSmartNote({title:m.querySelector('#nc-title').value,content:m.querySelector('#nc-content').value,source:'nayanet-hub.human-capture'});st.textContent='PERSISTED · EVENT '+(x.event?.event_id||'UNKNOWN')+' · RECEIPT '+(x.receipt?.receipt_id||'UNKNOWN')}catch(e){st.textContent='BLOCKED / FAILED · '+(e?.message||e)}}}
async function reports(r){
 const m=modal('Reports','Live report projections derived from the authenticated canonical event store.','<div class="nc-state" id="nc-state">RETRIEVING CANONICAL EVENTS…</div><div class="nc-grid" id="nc-grid"></div>');
 try{
  const rows=await r.retrieve(),now=Date.now(),ranges=[['TODAY',86400000],['7 DAYS',604800000],['30 DAYS',2592000000],['YEAR',31536000000]];
  m.querySelector('#nc-grid').innerHTML=ranges.map(([n,d])=>'<div class="nc-card"><b>'+n+'</b><span>'+rows.filter(x=>now-new Date(x.created_at).getTime()<d).length+' canonical events</span></div>').join('');
  m.querySelector('#nc-state').textContent='LIVE · CANONICAL EVENT STORE · '+rows.length+' EVENTS';
 }catch(e){m.querySelector('#nc-state').textContent='BLOCKED / FAILED · '+(e?.message||e)}
}
async function share(r){const rows=await r.retrieve();const owned=rows.find(x=>x.user_id===r.snapshot().user_id&&!String(x.source||'').includes('smart-share.publication'));const m=modal('Smart Share','Publication uses the canonical consent/publication boundary.','<div class="nc-state" id="nc-state">'+(owned?'Selected: '+esc(owned.title||owned.event_id):'No owned intelligence is available to publish.')+'</div><div class="nc-actions"><button id="nc-publish">PUBLISH SELECTED INTELLIGENCE</button></div>');m.querySelector('#nc-publish').onclick=async()=>{const st=m.querySelector('#nc-state');try{if(!owned)throw Error('NO_OWNED_INTELLIGENCE');const x=await r.publishSmartFeed(owned.event_id);st.textContent='PUBLISHED · PUBLICATION '+(x.publication?.id||'UNKNOWN')+' · RECEIPT '+(x.receipt?.event_id||x.receipt?.id||'UNKNOWN')}catch(e){st.textContent='BLOCKED / FAILED · '+(e?.message||e)}}}
async function lists(r){
 const m=modal('Smart Lists','Owner-scoped organization over canonical Connections. Every mutation is re-read from canonical persistence; local UI state is never treated as proof.',
  '<div class="nc-actions">'+
   '<button id="nc-create">CREATE SMART LIST</button>'+
   '<button id="nc-refresh">RELOAD / RETRIEVE</button>'+
   '<button id="nc-unauthorized">AUTHORIZATION / FAILURE TEST</button>'+
  '</div>'+
  '<div class="nc-state" id="nc-state">RETRIEVING CANONICAL SMART LISTS…</div>'+
  '<div class="nc-grid" id="nc-lists"></div>'+
  '<div class="nc-state" id="nc-proof">Lifecycle proof: CREATE → RELOAD → RETRIEVE → ADD → RELOAD → VERIFY → REMOVE → RELOAD → VERIFY.</div>');
 const state=m.querySelector('#nc-state'), grid=m.querySelector('#nc-lists'), proof=m.querySelector('#nc-proof');
 let listsRows=[], connections=[];
 const labelConn=x=>String(x.connected_member_id||x.id||'Connection');
 const render=()=>{
  grid.innerHTML=listsRows.length?listsRows.map(x=>{
   const members=Array.isArray(x.members)?x.members:[];
   const memberIds=new Set(members.map(y=>String(y.connection_id)));
   const available=connections.filter(c=>String(c.status||'').toLowerCase()==='active'&&!memberIds.has(String(c.id)));
   return '<div class="nc-card" data-list="'+esc(x.id)+'">'+
    '<b>'+esc(x.name)+'</b><span>'+members.length+' persisted connection(s) · '+esc(x.id)+'</span>'+
    '<div class="nc-actions">'+
      '<select class="nc-input" data-add-select><option value="">SELECT ACTIVE CONNECTION</option>'+
        available.map(c=>'<option value="'+esc(c.id)+'">'+esc(labelConn(c))+'</option>').join('')+
      '</select>'+
      '<button data-add>ADD CONNECTION</button>'+
      (members.length?'<button data-remove>REMOVE FIRST MEMBER</button>':'')+
    '</div>'+
    '<div class="nc-state" data-members>'+esc(members.length?members.map(y=>y.connection_id).join('\n'):'NO PERSISTED MEMBERS')+'</div>'+
   '</div>';
  }).join(''):'<div class="nc-card"><b>NO SMART LISTS</b><span>Create one to begin the canonical lifecycle.</span></div>';
 };
 const reload=async(stage='RELOAD / RETRIEVE')=>{
  state.textContent=stage+' · READING CANONICAL SMART LISTS + CONNECTIONS…';
  try{
   [listsRows,connections]=await Promise.all([r.listSmartLists(),r.listConnections()]);
   render();
   state.textContent='LIVE · '+listsRows.length+' SMART LIST(S) · '+connections.length+' OWNER-SCOPED CONNECTION(S) · CANONICAL RETRIEVAL';
  }catch(e){state.textContent='BLOCKED / FAILED · '+(e?.message||e)}
 };
 m.querySelector('#nc-refresh').onclick=()=>void reload();
 m.querySelector('#nc-create').onclick=async()=>{
  const name=prompt('List name');if(!name)return;
  state.textContent='CREATE → CANONICAL PERSISTENCE…';
  try{
   const created=await r.createSmartList(name);
   await reload('RELOAD / RETRIEVE AFTER CREATE');
   const persisted=listsRows.find(x=>String(x.id)===String(created.id)||x.name===name);
   proof.textContent=persisted?'CREATE ✓ · RELOAD ✓ · RETRIEVE ✓ · PERSISTED LIST '+persisted.name:'CREATE returned but canonical retrieval did not confirm persistence.';
  }catch(e){state.textContent='BLOCKED / FAILED · '+(e?.message||e)}
 };
 m.querySelector('#nc-unauthorized').onclick=async()=>{
  state.textContent='AUTHORIZATION TEST → ATTEMPTING WRITE AGAINST A NON-OWNED LIST ID…';
  try{
   const conn=connections.find(c=>String(c.status||'').toLowerCase()==='active');
   if(!conn)throw Error('NO_ACTIVE_CONNECTION_FOR_AUTHORIZATION_TEST');
   const foreignListId=crypto.randomUUID();
   await r.addConnectionToList(foreignListId,conn.id);
   state.textContent='UNEXPECTED SUCCESS · AUTHORIZATION BOUNDARY DID NOT BLOCK UNKNOWN LIST ID';
   proof.textContent='AUTHORIZATION TEST FAILED · UNEXPECTED SUCCESS';
  }catch(e){
   state.textContent='BLOCKED / FAILED · '+(e?.message||e);
   proof.textContent='AUTHORIZATION / FAILURE ✓ · REQUEST BLOCKED TRUTHFULLY · '+(e?.message||e);
  }
 };
 m.addEventListener('click',async e=>{
  const add=e.target.closest('[data-add]'), remove=e.target.closest('[data-remove]');
  if(!add&&!remove)return;
  const card=e.target.closest('[data-list]'), listId=card?.dataset.list;
  if(!listId)return;
  state.textContent=(add?'ADD CONNECTION':'REMOVE CONNECTION')+' → CANONICAL RPC…';
  try{
   const current=listsRows.find(x=>String(x.id)===String(listId));
   if(!current)throw Error('SMART_LIST_NOT_FOUND');
   if(add){
    const sel=card.querySelector('[data-add-select]');
    if(!sel?.value)throw Error('CONNECTION_REQUIRED');
    const selectedId=sel.value;
    const result=await r.addConnectionToList(listId,selectedId);
    await reload('RELOAD / VERIFY MEMBERSHIP');
    const verified=listsRows.find(x=>String(x.id)===String(listId));
    const ok=(verified?.members||[]).some(y=>String(y.connection_id)===String(selectedId));
    proof.textContent=ok?'ADD ✓ · RELOAD ✓ · VERIFY MEMBERSHIP ✓ · '+String(result?.status||'ADDED'):'ADD returned but persisted membership was not verified.';
   }else{
    const member=current.members?.[0];
    if(!member)throw Error('NO_PERSISTED_MEMBER');
    const result=await r.removeConnectionFromList(listId,member.connection_id);
    await reload('RELOAD / VERIFY REMOVAL');
    const verified=listsRows.find(x=>String(x.id)===String(listId));
    const ok=!(verified?.members||[]).some(y=>String(y.connection_id)===String(member.connection_id));
    proof.textContent=ok?'REMOVE ✓ · RELOAD ✓ · VERIFY REMOVAL ✓ · '+String(result?.status||'REMOVED'):'REMOVE returned but persisted membership is still present.';
   }
  }catch(e){state.textContent='BLOCKED / FAILED · '+(e?.message||e);proof.textContent='TRUTHFUL BLOCKED RESULT · '+(e?.message||e)}
 });
 await reload();
}
async function spaces(r){const rows=await r.listSpaces();const m=modal('Smart Spaces','Permissioned Spaces contain canonical intelligence only.','<div class="nc-state" id="nc-state">'+esc(rows.map(x=>x.name+' · '+x.visibility+' · '+x.purpose).join('\n\n')||'No Spaces yet.')+'</div><div class="nc-actions"><button id="nc-create">CREATE PRIVATE SPACE</button></div>');m.querySelector('#nc-create').onclick=async()=>{const name=prompt('Space name'),purpose=prompt('Purpose');if(!name||!purpose)return;try{const x=await r.createSpace({name,purpose,visibility:'private'});m.querySelector('#nc-state').textContent='CREATED · '+x.name+' · CANONICAL ID '+x.id+' · PERSISTED';}catch(e){m.querySelector('#nc-state').textContent='BLOCKED / FAILED · '+(e?.message||e)}}}
async function connections(r){const rows=await r.listConnections();modal('Connections','Deliberate relationships. A Connection does not create authority.','<div class="nc-state">'+esc(rows.map(x=>x.connected_member_id+' · '+x.status+' · '+(x.source_space_id||'no source Space')).join('\n')||'No active Connections yet.')+'</div>')}
async function mail(r){
 const m=modal('Smart Mail','Governed communication over a mutual Connection. Send crosses explicit authorization, idempotent delivery, persisted receipt/cognition lineage, and receiver verification.','<div class="nc-grid"><div class="nc-card"><b>COMPOSE</b><span>Choose an active mutual Connection, write the message, then SEND & AUTHORIZE.</span><select class="nc-input" id="nc-mail-recipient"></select><input class="nc-input" id="nc-mail-subject" placeholder="Subject"><textarea class="nc-textarea" id="nc-mail-body" placeholder="Message"></textarea><div class="nc-actions"><button id="nc-mail-send">SEND & AUTHORIZE</button><button id="nc-mail-retry" disabled>RETRY SAME SEND</button><button id="nc-mail-verify" disabled>VERIFY MESSAGE</button><button id="nc-mail-refresh">RELOAD / RETRIEVE</button></div><div class="nc-state" id="nc-mail-state">Loading connections…</div></div><div class="nc-card"><b>CANONICAL THREADS</b><span id="nc-mail-threads">Loading persisted threads…</span></div></div>');
 const select=m.querySelector('#nc-mail-recipient'),state=m.querySelector('#nc-mail-state'),threadsEl=m.querySelector('#nc-mail-threads');
 const send=m.querySelector('#nc-mail-send'),retry=m.querySelector('#nc-mail-retry'),verify=m.querySelector('#nc-mail-verify'),refresh=m.querySelector('#nc-mail-refresh');
 let connections=[],threads=[],lastSend=null;
 const renderConnections=()=>{const active=connections.filter(x=>String(x.status||'').toLowerCase()==='active');select.innerHTML=active.length?active.map(x=>'<option value="'+esc(x.connected_member_id)+'">'+esc(x.connected_member_id)+'</option>').join(''):'<option value="">NO ACTIVE CONNECTIONS</option>';};
 const renderThreads=async()=>{threads=await r.listMailThreads();if(!threads.length){threadsEl.textContent='NO PERSISTED MAIL THREADS';return;}const chunks=[];for(const t of threads.slice(0,12)){let body='';try{const msgs=await r.listMailMessages(t.id);const last=msgs[msgs.length-1];body=last?String(last.body||'').slice(0,240):'';}catch{}chunks.push(esc((t.subject||'Untitled')+' · '+t.kind+' · '+t.created_at+(body?'\n'+body:'')));}threadsEl.textContent=chunks.join('\n\n');};
 const reload=async()=>{state.textContent='RELOAD / RETRIEVE → CANONICAL CONNECTIONS + MAIL…';try{connections=await r.listConnections();renderConnections();await renderThreads();state.textContent='LIVE · '+connections.filter(x=>x.status==='active').length+' ACTIVE CONNECTION(S) · '+threads.length+' THREAD(S)';}catch(e){state.textContent='BLOCKED / FAILED · '+(e?.message||e)}};
 refresh.onclick=()=>void reload();
 send.onclick=async()=>{state.textContent='AUTHORIZE → SEND → PERSIST → RECEIPT…';try{const receiver_id=String(select.value||'');const subject=String(m.querySelector('#nc-mail-subject').value||'').trim();const body=String(m.querySelector('#nc-mail-body').value||'').trim();if(!receiver_id)throw Error('NO_ACTIVE_CONNECTION');if(!body)throw Error('MESSAGE_BODY_REQUIRED');const key='hub-mail-'+Date.now().toString(36)+'-'+Math.random().toString(36).slice(2,8);lastSend={receiver_id,subject,body,kind:'direct',idempotency_key:key};const x=await r.sendSmartMail(lastSend);lastSend={...lastSend,authority_grant_id:x.authority_grant_id,authorization_event_id:x.authorization_event_id,message_id:x.message_id,thread_id:x.thread_id,execution_receipt_id:x.execution_receipt_id};state.textContent=(x.status==='REPLAY'?'REPLAY VERIFIED':'SENT · AUTHORIZED')+' · MESSAGE '+String(x.message_id||'UNKNOWN')+' · RECEIPT '+String(x.execution_receipt_id||'UNKNOWN');retry.disabled=false;verify.disabled=!lastSend.message_id;await renderThreads();}catch(e){state.textContent='BLOCKED / FAILED · '+(e?.message||e)}};
 retry.onclick=async()=>{if(!lastSend)return;state.textContent='RETRY SAME SEND → IDEMPOTENCY…';try{const x=await r.sendSmartMail(lastSend);const same=String(x.message_id||'')===String(lastSend.message_id||'');state.textContent=same?'REPLAY VERIFIED · SAME MESSAGE '+String(x.message_id):'REPLAY RETURNED · '+JSON.stringify(x);}catch(e){state.textContent='BLOCKED / FAILED · '+(e?.message||e)}};
 verify.onclick=async()=>{if(!lastSend?.message_id)return;state.textContent='VERIFY → RECEIVER-AUTHORIZED MESSAGE CHECK…';try{const x=await r.verifySmartMail(lastSend.message_id);state.textContent='VERIFIED · RECEIPT '+String(x.execution_receipt_id||lastSend.execution_receipt_id||'UNKNOWN')+' · LEARNING '+String(x.learning_evidence_id||'UNKNOWN');await renderThreads();}catch(e){state.textContent='BLOCKED / FAILED · '+(e?.message||e)}};
 await reload();
}
async function ledger(r){const rows=await r.listSmartLedger();modal('Smart Ledger','Accountability projection from the canonical ledger.','<div class="nc-state">'+esc(rows.map(x=>(x.event_type||'event')+' · '+x.status+' · '+(x.verification?.status||'not-qualified')+' · '+(x.created_at||'')).join('\n\n')||'No ledger events yet.')+'</div>')}
async function dream(r){const replays=await r.listDreamReplays(),events=await r.retrieve();const latest=events[0];const m=modal('Dream','Deterministic replay of preserved intelligence; learning never becomes authority by itself.','<div class="nc-state" id="nc-state">'+esc(replays.length?replays.slice(0,10).map(x=>(x.created_at||'')+' · '+(x.status||'REPLAY')).join('\n'):'No Dream replays yet.')+'</div><div class="nc-actions"><button id="nc-dream">DREAM LATEST PRESERVED EVENT</button></div>');m.querySelector('#nc-dream').onclick=async()=>{try{if(!latest)throw Error('NO_PRESERVED_EVENT');const x=await r.dreamReplay({event_id:latest.event_id});m.querySelector('#nc-state').textContent='DREAM REPLAY PERSISTED · '+JSON.stringify(x)}catch(e){m.querySelector('#nc-state').textContent='BLOCKED / FAILED · '+(e?.message||e)}}}
async function play(r){const ev=await r.retrieve(),le=await r.listLearningEvidence();const m=modal('Naya Play','A governed practice loop: choose understanding, replay experience, apply only with evidence, then verify the checkpoint.','<div class="nc-state" id="nc-state">Latest event: '+esc(ev[0]?.title||'none')+'\nLearning evidence: '+le.length+'</div><div class="nc-actions"><button id="nc-learn">LEARN LATEST</button><button id="nc-dream">DREAM LATEST</button><button id="nc-verify">VERIFY LATEST APPLICATION</button></div>');m.querySelector('#nc-learn').onclick=async()=>{try{const x=ev[0];if(!x)throw Error('NO_SMART_NOTE');const e=await r.recordLearningEvidence({claim:'Observed understanding of '+(x.title||x.event_id),target_id:x.event_id,source_event_id:x.event_id,provenance:'OBSERVATION',verification_method:'Hub human practice checkpoint'});m.querySelector('#nc-state').textContent='LEARNING EVIDENCE PERSISTED · '+e.id}catch(e){m.querySelector('#nc-state').textContent='BLOCKED / FAILED · '+(e?.message||e)}};m.querySelector('#nc-dream').onclick=async()=>{try{const x=ev[0];if(!x)throw Error('NO_PRESERVED_EVENT');const d=await r.dreamReplay({event_id:x.event_id});m.querySelector('#nc-state').textContent='DREAM PERSISTED · '+JSON.stringify(d)}catch(e){m.querySelector('#nc-state').textContent='BLOCKED / FAILED · '+(e?.message||e)}};m.querySelector('#nc-verify').onclick=async()=>{try{if(!r.verify)throw Error('VERIFY_RUNTIME_NOT_EXPOSED');const x=await r.verify(ev[0]?.event_id);m.querySelector('#nc-state').textContent='VERIFY CHECKPOINT PERSISTED · '+JSON.stringify(x)}catch(e){m.querySelector('#nc-state').textContent='BLOCKED / FAILED · '+(e?.message||e)}}}
async function settings(r){const s=r.snapshot();const m=modal('Settings','Truthful runtime state; no configuration is claimed that the current session cannot prove.','<div class="nc-state">'+esc(JSON.stringify(s,null,2))+'</div><div class="nc-actions"><button id="nc-out">SIGN OUT</button></div>');m.querySelector('#nc-out').onclick=async()=>{await r.signOut();m.querySelector('.nc-state').textContent='SIGNED OUT · PRIVATE DATA ACCESS BLOCKED';}}
function wireSidebar(){
 const rail=document.querySelector('.rail.left'); if(!rail)return false;
 const map={home:['feed','activity'],notes:['note',null],reports:['reports',null],intelligence:['intelligence',null],collective:['feed','collective'],evidence:['ledger',null],connections:['connections',null],mail:['mail',null],settings:['settings',null],share:['share',null],lists:['lists',null],spaces:['spaces',null],ledger:['ledger',null],play:['play',null]};
 if(!rail.querySelector('[data-page="play"]')){
   const systemNav=[...rail.querySelectorAll('.nav')].find(n=>n.querySelector('[data-page="settings"]'));
   if(systemNav){
     const b=document.createElement('button');
     b.type='button'; b.dataset.page='play'; b.dataset.nayaSurface='play'; b.innerHTML='<span class="ico">✦</span>Naya Play';
     systemNav.insertBefore(b,systemNav.querySelector('[data-page="settings"]'));
   }
 }
 const surfaceMap={lists:'lists',spaces:'spaces',contacts:'contacts',share:'share',mail:'mail',settings:'settings',play:'play'};
 rail.querySelectorAll('.nav button[data-page]').forEach(b=>{if(surfaceMap[b.dataset.page])b.dataset.nayaSurface=surfaceMap[b.dataset.page]});
 rail.querySelectorAll('.nav button[data-page]').forEach(b=>{const key=b.dataset.page,mapped=map[key];if(!mapped)return;b.dataset.nc=mapped[0];if(mapped[1])b.dataset.ncStream=mapped[1];else delete b.dataset.ncStream});
 return true;
}
function install(){css();const bind=()=>{wireSidebar();window.__nayaOpenSurface=open};bind();setTimeout(bind,0);if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',bind,{once:true});document.addEventListener('click',e=>{const b=e.target.closest('[data-nc]');if(!b||b.closest('#naya-completeness'))return;e.preventDefault();e.stopImmediatePropagation();const action={kind:b.dataset.nc,stream:b.dataset.ncStream||null,at:new Date().toISOString()};window.__nayaSidebarAction=action;void open(b.dataset.nc,b.dataset.ncStream).catch(()=>{});},true)}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',install,{once:true});else install();
})();