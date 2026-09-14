(()=>{'use strict';
const q=(s,r=document)=>r.querySelector(s);
const qq=(s,r=document)=>[...r.querySelectorAll(s)];
const text=e=>(e?.innerText||e?.textContent||'').replace(/\s+/g,' ').trim();
const OBSOLETE=['Blockers Never Stop the Mission','Source Intent Is Not Runtime Truth','The Intelligent Block Is the Star'];
const FEED_SOURCE='https://raw.githubusercontent.com/SoulSchoolAcademy/NayaPOWER/main/SMART%20FEED%20CONTENT';
const NAV=['Your Intelligence','Your Reports','Intelligent Library','Smart Share','Smart Ledger','Your Connections','Smart Lists','Smart Spaces','Smart Mail'];
function removeObsolete(){qq('.block').forEach(b=>{const t=text(q('h3',b));if(OBSOLETE.some(x=>t===x||t.includes(x)))b.remove()})}
function sidebar(){
  const rail=q('.rail');if(!rail)return;
  const els=qq('.nav button,.nav a,.rail button,.rail a',rail);
  const rename={'Home':'Your Intelligence','Reports':'Your Reports','Evidence':'Smart Ledger','Collective':'Smart Share','Connections':'Your Connections'};
  els.forEach(el=>{
    const t=text(el),low=t.toLowerCase();
    if(t==='Smart Notes'){el.remove();return}
    if(low.startsWith('smart mail')&&low.includes('new')){el.remove();return}
    const key=Object.keys(rename).find(k=>new RegExp('^'+k+'$','i').test(t));
    if(key){
      const walker=document.createTreeWalker(el,NodeFilter.SHOW_TEXT);
      while(walker.nextNode()){const n=walker.currentNode;if(n.nodeValue.trim()===key){n.nodeValue=rename[key];break}}
      el.setAttribute('aria-label',rename[key]);
    }
  });
  const mail=qq('.nav button,.nav a',rail).filter(el=>text(el).toLowerCase().startsWith('smart mail'));
  mail.slice(1).forEach(el=>el.remove());
}
function noteHowToUse(src,title){
  const chunks=src.split(/🧠\s*NAYA POWER\s*[—-]\s*SMART NOTE\s*\d+/i);
  const chunk=chunks.find(c=>{const lines=c.trim().split(/\n/).map(x=>x.trim()).filter(Boolean);return lines[0]===title||lines.slice(0,3).includes(title)});
  if(!chunk)return '';
  const m=chunk.match(/(?:^|\n)\s*10\s*[.:)\-]?\s*HOW TO APPLY IT\s*\n([\s\S]*?)(?=\n\s*11\s*[.:)\-]?\s*(?:WHAT'S IN IT FOR YOU|BENEFITS)\b|$)/i);
  return m?m[1].trim():'';
}
async function addHowToUse(){
  const blocks=qq('.block[data-real-smart-note]');
  if(blocks.length<9)return;
  let src='';try{const r=await fetch(FEED_SOURCE,{cache:'no-store'});if(r.ok)src=await r.text()}catch{}
  blocks.slice(0,9).forEach(b=>{
    if(q('.naya509-how-to-use',b))return;
    const layers=q('.layers',b);if(!layers)return;
    const title=text(q('h3',b));
    const body=noteHowToUse(src,title)||'Use this intelligence as a practical guide. Choose one action that fits your situation, apply it, observe the result, and improve from what you learn.';
    const layer=document.createElement('section');layer.className='layer naya509-how-to-use';
    layer.innerHTML='<div class="layerHead"><span class="dot" style="--layer:var(--green)"></span><b>10 · HOW TO USE IT</b><span class="state">APPLICATION</span></div><div class="layerBody"></div>';
    q('.layerBody',layer).textContent=body;layers.appendChild(layer);
  });
}
function injectStyles(){if(q('#naya509-hub-projections'))return;const s=document.createElement('style');s.id='naya509-hub-projections';s.textContent=`
.naya509-view{padding:24px 22px 80px;min-height:calc(100vh - 72px)}
.naya509-hero{padding:24px 0 20px}.naya509-kicker{font-size:8px;font-weight:1000;letter-spacing:.18em;color:#a997ff}.naya509-view h1{font-size:clamp(34px,5vw,62px);line-height:.92;letter-spacing:-.07em;margin:8px 0 10px}.naya509-view .lead{max-width:900px;color:#c9c3cf;font-size:13px;line-height:1.65;margin:0}
.naya509-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}.naya509-card{border:2px solid #ffffff14;border-radius:18px;background:linear-gradient(145deg,#111019,#08080c);padding:17px;box-shadow:inset 0 1px #fff3,0 16px 32px #0009}.naya509-card h3{font-size:16px;margin:0 0 8px}.naya509-card p{color:#aaa4b1;font-size:10px;line-height:1.6;margin:0}.naya509-stat{font-size:29px;font-weight:950;margin-bottom:3px}.naya509-list{display:grid;gap:8px}.naya509-item{display:flex;justify-content:space-between;gap:12px;align-items:center;padding:13px 14px;border:1px solid #ffffff12;border-radius:13px;background:#08080c}.naya509-item b{font-size:10px}.naya509-item span{color:#817a89;font-size:8px}.naya509-btn{border:2px solid #8b63ff55;border-radius:10px;background:#0c0b11;color:#eeeaf2;padding:8px 10px;font-size:7px;font-weight:1000;letter-spacing:.06em;cursor:pointer}.naya509-btn:hover{border-color:#d86cff;transform:translateY(-1px)}
.naya509-view[data-tone="blue"] .naya509-kicker{color:var(--blue)}.naya509-view[data-tone="green"] .naya509-kicker{color:var(--green)}.naya509-view[data-tone="yellow"] .naya509-kicker{color:var(--yellow)}.naya509-view[data-tone="pink"] .naya509-kicker{color:var(--magenta)}
@media(max-width:900px){.naya509-grid{grid-template-columns:1fr 1fr}}@media(max-width:620px){.naya509-view{padding:18px 14px 70px}.naya509-grid{grid-template-columns:1fr}.naya509-view h1{font-size:40px}}
`;document.head.appendChild(s)}
function realBlocks(){return qq('.block[data-real-smart-note]').slice(0,9)}
function blockData(){return realBlocks().map((b,i)=>({i,title:text(q('h3',b))||('Smart Note '+(i+1)),summary:text(q('.nutshell p',b))||'',truth:text(q('.truth',b))||'ACTIVE',block:b}))}
function gotoBlock(i){const b=realBlocks()[i];if(!b)return;showBase();b.scrollIntoView({behavior:'smooth',block:'start'})}
function showBase(){const main=q('.main');if(!main)return;qq('.naya509-view',main).forEach(v=>v.remove());qq(':scope > *',main).forEach(el=>{if(!el.dataset.naya509Persistent)el.hidden=false});document.body.dataset.naya509View='base'}
function mountView(title,kicker,lead,html,tone='purple'){
  const main=q('.main');if(!main)return;
  qq('.naya509-view',main).forEach(v=>v.remove());
  qq(':scope > *',main).forEach(el=>{if(!el.dataset.naya509Persistent)el.hidden=true});
  const v=document.createElement('section');v.className='naya509-view';v.dataset.tone=tone;
  v.innerHTML='<div class="naya509-hero"><div class="naya509-kicker">'+kicker+'</div><h1>'+title+'</h1><p class="lead">'+lead+'</p></div><div class="naya509-content">'+html+'</div>';
  main.appendChild(v);document.body.dataset.naya509View=title;
}
function cards(items){return '<div class="naya509-grid">'+items.map(x=>'<article class="naya509-card">'+x+'</article>').join('')+'</div>'}
function renderProjection(name){
  const d=blockData();
  if(name==='Your Intelligence'){
    const html=cards(['<div class="naya509-stat">'+d.length+'</div><h3>Active intelligence objects</h3><p>Your current Smart Notes are the source objects behind this view. Nothing is copied; this is a projection of the same intelligence.</p>','<div class="naya509-stat">'+d.length+'</div><h3>Current intelligence set</h3><p>Truth and state metadata remain attached to the underlying intelligence objects.</p>','<div class="naya509-stat">∞</div><h3>Next intelligent action</h3><p>Open the intelligence that matters most, understand it, apply it, then verify what changed.</p>'])+'<div class="naya509-list" style="margin-top:14px">'+d.map(x=>'<div class="naya509-item"><div><b>'+x.title+'</b><span>'+x.summary.slice(0,150)+'</span></div><button class="naya509-btn" data-note="'+x.i+'">OPEN</button></div>').join('')+'</div>';
    mountView('Your Intelligence Today','YOUR INTELLIGENCE','The cockpit for what matters now — a curated projection of the same Smart Notes, feed activity, reports, connections, and learning that make up your intelligence system.',html);return;
  }
  if(name==='Your Reports'){const html=cards(['<h3>Intelligence over time</h3><p>Reports interpret the intelligence lifecycle: events → patterns → meaning → change → learning → result → recommendation.</p>','<h3>Current signal</h3><p>'+d.length+' canonical Smart Note objects are available to report on. Reports should interpret, not merely count.</p>','<h3>Verification</h3><p>Report claims inherit the underlying object’s provenance and truth state rather than becoming a new source of truth.</p>']);mountView('Your Reports','INTELLIGENCE REPORTING','Turn accumulated intelligence into patterns, decisions, results, learning, and better next actions without creating disconnected copies.',html,'blue');return}
  if(name==='Intelligent Library'){const html='<div class="naya509-list">'+d.map(x=>'<div class="naya509-item"><div><b>'+x.title+'</b><span>'+x.truth+' · canonical intelligence</span></div><button class="naya509-btn" data-note="'+x.i+'">OPEN BOARD</button></div>').join('')+'</div>';mountView('Intelligent Library','CANONICAL INTELLIGENCE','The reusable body of intelligence. The Library indexes the same Smart Note objects; opening one returns you to its Intelligent Block and Smart Board presentation.',html,'yellow');return}
  if(name==='Smart Share'){const html=cards(['<h3>Collective intelligence</h3><p>Smart Share is the shared projection of intelligence. Sharing changes visibility or contribution context; it does not create a second intelligence object.</p>','<h3>Contribution</h3><p>Useful comments, discoveries, corrections, evidence, and relationships can become new intelligence through the appropriate pathway.</p>','<h3>Human authority</h3><p>Personal intelligence remains private by default. Public contribution is an explicit human choice.</p>']);mountView('Smart Share','COLLECTIVE INTELLIGENCE','Where intelligence becomes voluntarily shareable and capable of creating more intelligence through other humans.',html,'pink');return}
  if(name==='Smart Ledger'){const html='<div class="naya509-grid">'+d.map((x,i)=>'<article class="naya509-card"><h3>'+x.title+'</h3><p><strong>STATE:</strong> '+x.truth+'</p><p style="margin-top:7px"><strong>RECORD:</strong> intelligence object '+(i+1)+' · provenance preserved · verification remains distinct from interpretation.</p></article>').join('')+'</div>';mountView('Smart Ledger','TRUTH + PROVENANCE','The record layer: what happened, who or what acted, when, source, artifact, state change, verification, evidence, and next action.',html,'yellow');return}
  if(name==='Your Connections'){const html='<div class="naya509-grid">'+d.map((x,i)=>'<article class="naya509-card"><h3>'+x.title+'</h3><p>Connected intelligence: Naya interpretation · related notes · reports · evidence · lists · spaces · share pathways · activity.</p><button class="naya509-btn" data-note="'+i+'" style="margin-top:12px">EXPLORE</button></article>').join('')+'</div>';mountView('Your Connections','RELATIONSHIP GRAPH','See how the same intelligence object relates to other intelligence, people, projects, spaces, evidence, events, decisions, results, and learning.',html,'blue');return}
  if(name==='Smart Lists'){const groups=[['Favorites','Intelligence you intentionally marked as important.'],['Saved Intelligence','Objects you want available for later use.'],['Current Projects','Intelligence organized around active work.'],['Ideas','Potential intelligence waiting for development.'],['Learning','Lessons and discoveries worth compounding.'],['To Act On','Intelligence that has a meaningful next action.']];const html=cards(groups.map(g=>'<h3>'+g[0]+'</h3><p>'+g[1]+'</p><button class="naya509-btn" style="margin-top:12px">VIEW LIST</button>'));mountView('Smart Lists','PERSONAL ORGANIZATION','Your chosen organization layer. Lists organize the same intelligence objects without duplicating them or changing their provenance.',html);return}
  if(name==='Smart Spaces'){const html=cards(['<h3>Mission Space</h3><p>A living environment organized around a subject, mission, problem, or opportunity.</p>','<h3>Intelligence inside</h3><p>Spaces can contain the same Smart Notes, conversations, people, contributions, evidence, learning, and next actions.</p>','<h3>Continuity</h3><p>Creating or materially changing a Space is itself consequential activity and should have an Activity/event pathway.</p>']);mountView('Smart Spaces','LIVING INTELLIGENCE ENVIRONMENTS','Spaces gather related intelligence and people around something that matters, while preserving the identity of every intelligence object inside.',html,'green');return}
  if(name==='Smart Mail'){const html=cards(['<h3>Communication → intelligence</h3><p>Messages can carry intent, people, projects, possible events, actions, decisions, and discoveries.</p>','<h3>Useful consequence</h3><p>Meaningful communication can feed Smart Notes, tasks, connections, Spaces, saved intelligence, report inputs, and relationship updates.</p>','<h3>Human authority</h3><p>Mail never silently becomes an authorized action. The human remains the authority over consequential communication and commitments.</p>']);mountView('Smart Mail','COMMUNICATION INTELLIGENCE','Communication becomes part of the intelligence system when it creates meaningful context, action, evidence, relationships, or learning.',html,'purple');return}
  showBase();
}
function bindHub(){
  injectStyles();const rail=q('.rail');if(!rail)return;
  const buttons=qq('.nav button,.nav a',rail);
  buttons.forEach(el=>{const name=text(el);if(!NAV.includes(name)||el.dataset.naya509Bound==='1')return;el.dataset.naya509Bound='1';el.addEventListener('click',e=>{e.preventDefault();e.stopPropagation();buttons.forEach(x=>x.classList.toggle('active',x===el));renderProjection(name)},true)});
  const main=q('.main');if(main&&!main.dataset.naya509ClickBound){main.dataset.naya509ClickBound='1';main.addEventListener('click',e=>{const b=e.target.closest('[data-note]');if(b){showBase();const target=realBlocks()[Number(b.dataset.note)];target?.scrollIntoView({behavior:'smooth',block:'start'})}})}
}
function run(){removeObsolete();sidebar();addHowToUse();bindHub()}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run);else run();[400,1000,2000,4000].forEach(ms=>setTimeout(run,ms));
new MutationObserver(()=>{removeObsolete();sidebar();addHowToUse();bindHub()}).observe(document.documentElement,{childList:true,subtree:true});
window.NAYA509_FEED_FINISH='2026-09-14-integrated-hub-projections';
})();
