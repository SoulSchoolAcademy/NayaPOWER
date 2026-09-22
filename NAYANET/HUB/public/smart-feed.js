(()=>{'use strict';
/*
 NayaNET Smart Feed V2
 Canonical Hub projection only.
 One feed. Three views:
   PERSONAL INTELLIGENCE = the owner's preserved intelligence
   COLLECTIVE INTELLIGENCE = intelligence intentionally shared across the boundary
   ACTIVITY = what actually happened
 No alternate store. No invented content.
*/
const V='naya-smart-feed-v2';
const root=()=>document.querySelector('.feed');
const nav=()=>document.querySelector('.feedNav');
const tone={personal:'#55b9ee',collective:'#9d75ff',activity:'#55e39a'};
const label={
 personal:['PERSONAL INTELLIGENCE','Your private intelligence — captured, saved, and carried forward.'],
 collective:['COLLECTIVE INTELLIGENCE','Shared intelligence worth discovering, understanding, and using.'],
 activity:['ACTIVITY','A living record of meaningful Naya, human, and system events.']
};
const esc=v=>String(v??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const clean=v=>String(v??'').replace(/\s+/g,' ').trim();
const text=v=>clean(v);
const value=(o,...keys)=>{for(const k of keys){const v=o?.[k];if(v!==undefined&&v!==null&&String(v).trim()!=='')return v}return ''};
const arr=v=>Array.isArray(v)?v:[];
const state={stream:'personal',items:[],before:null,loading:false,ready:false};

function styles(){
 if(document.getElementById('naya-smart-feed-v2-style'))return;
 const s=document.createElement('style');s.id='naya-smart-feed-v2-style';
 s.textContent=`
 .naya-sf-v2{margin:0 22px 30px;position:relative}
 .naya-sf-v2 .sf-intro{display:flex;align-items:flex-end;justify-content:space-between;gap:18px;margin:2px 0 14px}
 .naya-sf-v2 .sf-kicker{font-size:8px;font-weight:1000;letter-spacing:.18em;color:#938b9c}
 .naya-sf-v2 .sf-title{margin:5px 0 5px;font-size:clamp(28px,4vw,52px);line-height:.96;letter-spacing:-.055em;color:#fff}
 .naya-sf-v2 .sf-description{max-width:850px;margin:0;color:#aaa4b1;font-size:10px;line-height:1.55}
 .naya-sf-v2 .sf-authority{padding:9px 12px;border:1px solid #ffffff1d;border-radius:11px;background:#09090d;color:#bdb6c5;font-size:7px;font-weight:1000;letter-spacing:.1em;white-space:nowrap}
 .naya-sf-v2 .sf-tabs{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:9px;margin-bottom:14px}
 .naya-sf-v2 .sf-tab{min-height:58px;padding:8px 12px;border:2px solid #ffffff18;border-radius:15px;background:linear-gradient(145deg,#121119,#08080c);color:#a9a1b0;text-align:left;cursor:pointer;box-shadow:inset 0 1px #fff3,0 10px 24px #0008;transition:.22s cubic-bezier(.16,.84,.22,1)}
 .naya-sf-v2 .sf-tab:hover{transform:translateY(-2px);color:#fff;border-color:#ffffff45}
 .naya-sf-v2 .sf-tab.active{color:#fff;border-color:var(--tone);box-shadow:inset 0 1px #fff4,0 14px 30px #000a,0 0 28px color-mix(in srgb,var(--tone) 17%,transparent)}
 .naya-sf-v2 .sf-tab strong{display:block;font-size:10px;letter-spacing:.04em}.naya-sf-v2 .sf-tab span{display:block;margin-top:4px;color:#817a89;font-size:7px;line-height:1.35}.naya-sf-v2 .sf-tab.active span{color:#c7c0ce}
 .naya-sf-v2 .sf-status{display:flex;align-items:center;justify-content:space-between;gap:10px;margin:0 0 12px;padding:10px 12px;border:1px solid #ffffff13;border-radius:12px;background:#08080c;color:#928a99;font-size:8px}
 .naya-sf-v2 .sf-status strong{color:#fff}.naya-sf-v2 .sf-refresh{border:1px solid #8b63ff55;border-radius:9px;background:#0d0b11;color:#eeeaf2;padding:7px 10px;font-size:7px;font-weight:1000;cursor:pointer}
 .naya-sf-v2 .sf-list{display:grid;gap:14px}
 .naya-sf-v2 .sf-card{position:relative;overflow:hidden;border:2px solid color-mix(in srgb,var(--tone) 44%,#ffffff10);border-radius:22px;background:radial-gradient(700px 260px at 78% 0%,color-mix(in srgb,var(--tone) 10%,transparent),transparent 70%),linear-gradient(145deg,#121018,#07080b);box-shadow:inset 0 1px #fff4,0 22px 48px #000b;transition:.22s cubic-bezier(.16,.84,.22,1)}
 .naya-sf-v2 .sf-card:hover{transform:translateY(-3px);border-color:color-mix(in srgb,var(--tone) 72%,#fff 10%);box-shadow:inset 0 1px #fff5,0 30px 60px #000d,0 0 35px color-mix(in srgb,var(--tone) 10%,transparent)}
 .naya-sf-v2 .sf-card:before{content:"";position:absolute;left:0;top:0;bottom:0;width:4px;background:var(--tone);box-shadow:0 0 20px var(--tone)}
 .naya-sf-v2 .sf-main{padding:22px 24px 18px}
 .naya-sf-v2 .sf-head{display:flex;gap:13px;align-items:flex-start}
 .naya-sf-v2 .sf-jewel{width:48px;height:48px;flex:0 0 48px;display:grid;place-items:center;border-radius:15px;border:2px solid color-mix(in srgb,var(--tone) 72%,#fff 8%);background:radial-gradient(circle at 30% 20%,#fff8,transparent 16%),radial-gradient(circle at 50% 50%,color-mix(in srgb,var(--tone) 30%,transparent),#09090e 70%);color:#fff;font-size:20px;box-shadow:inset 0 1px #fff7,0 12px 26px #000b,0 0 24px color-mix(in srgb,var(--tone) 18%,transparent)}
 .naya-sf-v2 .sf-head-copy{min-width:0;flex:1}.naya-sf-v2 .sf-title2{margin:1px 0 7px;font-size:clamp(21px,2.7vw,34px);line-height:1.03;letter-spacing:-.04em;color:#fff}
 .naya-sf-v2 .sf-meta{display:flex;gap:6px;flex-wrap:wrap;align-items:center}.naya-sf-v2 .sf-pill{padding:5px 7px;border:1px solid #ffffff19;border-radius:999px;background:#ffffff05;color:#8e8796;font-size:6px;font-weight:1000;letter-spacing:.09em}.naya-sf-v2 .sf-pill.truth{color:#d9ffe9;border-color:#55e39a55;background:#55e39a08}.naya-sf-v2 .sf-pill.shared{color:#ddd0ff;border-color:#9d75ff55;background:#9d75ff08}
 .naya-sf-v2 .sf-body{margin:18px 0 0;padding:18px 19px;border:2px solid #ffffff15;border-radius:17px;background:#08080d;box-shadow:inset 0 1px #fff2}
 .naya-sf-v2 .sf-body-label{display:block;margin-bottom:7px;color:#aaa4b1;font-size:7px;font-weight:1000;letter-spacing:.14em}.naya-sf-v2 .sf-body p{margin:0;color:#f0edf3;font-size:15px;line-height:1.68}
 .naya-sf-v2 .sf-layers{display:grid;gap:8px;margin-top:12px}
 .naya-sf-v2 .sf-layer{border:1px solid color-mix(in srgb,var(--tone) 28%,#ffffff10);border-radius:14px;background:#09090d;overflow:hidden}
 .naya-sf-v2 .sf-layer summary{list-style:none;cursor:pointer;padding:11px 13px;color:#bdb6c5;font-size:7px;font-weight:1000;letter-spacing:.12em}.naya-sf-v2 .sf-layer summary::-webkit-details-marker{display:none}.naya-sf-v2 .sf-layer summary:after{content:"＋";float:right;color:#766e7d}.naya-sf-v2 .sf-layer[open] summary:after{content:"−"}
 .naya-sf-v2 .sf-layer-body{padding:0 13px 14px;color:#c8c1ce;font-size:9px;line-height:1.6;word-break:break-word}.naya-sf-v2 .sf-layer-body b{color:#fff}
 .naya-sf-v2 .sf-actions{display:flex;gap:7px;flex-wrap:wrap;padding:13px 24px;border-top:1px solid #ffffff12;background:#08080c}.naya-sf-v2 .sf-actions button{min-height:37px;padding:0 11px;border:1px solid #ffffff1c;border-radius:10px;background:linear-gradient(145deg,#14121a,#09090d);color:#eeeaf2;font-size:7px;font-weight:1000;cursor:pointer}.naya-sf-v2 .sf-actions button:hover{border-color:var(--tone);transform:translateY(-1px)}
 .naya-sf-v2 .sf-empty{padding:38px 24px;text-align:center;border:2px dashed #ffffff18;border-radius:18px;background:#08080c;color:#8e8796}.naya-sf-v2 .sf-empty strong{display:block;color:#fff;font-size:16px;margin-bottom:7px}.naya-sf-v2 .sf-empty span{font-size:9px;line-height:1.5}
 .naya-sf-v2 .sf-more{display:flex;justify-content:center;margin:16px 0}.naya-sf-v2 .sf-more button{min-height:40px;padding:0 16px;border:1px solid #9d75ff66;border-radius:11px;background:#0d0a13;color:#fff;font-size:7px;font-weight:1000;cursor:pointer}.naya-sf-v2 .sf-more button:disabled{opacity:.5;cursor:default}
 @media(max-width:760px){.naya-sf-v2{margin:0 14px 24px}.naya-sf-v2 .sf-intro{display:block}.naya-sf-v2 .sf-authority{display:inline-block;margin-top:10px}.naya-sf-v2 .sf-tabs{grid-template-columns:1fr;gap:7px}.naya-sf-v2 .sf-tab{min-height:53px}.naya-sf-v2 .sf-main{padding:18px 17px 15px}.naya-sf-v2 .sf-jewel{width:42px;height:42px;flex-basis:42px}.naya-sf-v2 .sf-actions{padding:12px 17px}.naya-sf-v2 .sf-body p{font-size:14px}}
 @media(prefers-reduced-motion:reduce){.naya-sf-v2 *{transition:none!important}}
 `;
 document.head.appendChild(s);
}

function actionButtons(item){
 const allowed=arr(item.available_actions).map(x=>String(x).toLowerCase());
 const actions=[];
 for(const a of ['save','favorite','like','love','publish']){
  if(allowed.includes(a))actions.push('<button type="button" data-sf-action="'+a+'" data-sf-id="'+esc(value(item,'source_id','id'))+'">'+({save:'🔖 SAVE',favorite:'★ FAVORITE',like:'👍 LIKE',love:'♥ LOVE',publish:'◇ SHARE'}[a])+'</button>');
 }
 return actions.join('');
}

function layer(title,body){
 if(!body)return '';
 return '<details class="sf-layer"><summary>'+esc(title)+'</summary><div class="sf-layer-body">'+body+'</div></details>';
}

function renderItem(item){
 const stream=state.stream,t=tone[stream],title=text(value(item,'title','name','event_type','event_id')||'Intelligence');
 const content=text(value(item,'content','summary','description')||'No content was returned by the canonical source.');
 const verified=text(value(item,'verification_state','verification','status')||'UNKNOWN');
 const visibility=text(value(item,'visibility','sharing_state')||'PRIVATE');
 const source=text(value(item,'source','source_type')||'CANONICAL RUNTIME');
 const event=text(value(item,'event_id','id')||'UNKNOWN');
 const id=text(value(item,'source_id','intelligence_id','id')||event);
 const cls=text(value(item,'classification','type')||'UNCLASSIFIED');
 const conf=value(item,'confidence');
 const date=text(value(item,'published_at','created_at','occurred_at','timestamp')||'');
 const mark=stream==='activity'?'↗':stream==='collective'?'◇':'✦';
 let layers='';
 if(stream!=='activity'){
  layers+=layer('WHAT THIS IS','<b>'+esc(cls)+'</b><br>'+esc(content));
  layers+=layer('SOURCE · PROVENANCE','<b>Source:</b> '+esc(source)+'<br><b>Event:</b> '+esc(event)+'<br><b>Intelligence ID:</b> '+esc(id));
  layers+=layer('TRUTH · VISIBILITY','<b>Verification:</b> '+esc(verified)+'<br><b>Visibility:</b> '+esc(visibility)+(conf!==''?'<br><b>Confidence:</b> '+esc(conf):''));
  const meaning=text(value(item,'meaning','what_it_means','significance'));
  const use=text(value(item,'how_to_use','how_to_apply','use'));
  const valueForHuman=text(value(item,'human_value','whats_in_it_for_you','benefit'));
  if(meaning)layers+=layer('WHAT IT MEANS',esc(meaning));
  if(use)layers+=layer('HOW TO USE',esc(use));
  if(valueForHuman)layers+=layer("WHAT'S IN IT FOR YOU",esc(valueForHuman));
 }else{
  layers+=layer('WHAT HAPPENED','<b>Event:</b> '+esc(event)+'<br><b>Type:</b> '+esc(cls)+'<br><b>Source:</b> '+esc(source));
  layers+=layer('TRUTH · AUTHORITY','<b>Verification:</b> '+esc(verified)+'<br><b>Visibility:</b> '+esc(visibility)+(conf!==''?'<br><b>Confidence:</b> '+esc(conf):'')); 
  const consequence=text(value(item,'consequence','outcome','result','what_changed'));
  if(consequence)layers+=layer('WHAT CHANGED',esc(consequence));
 }
 const acts=actionButtons(item);
 return '<article class="sf-card" style="--tone:'+t+'" data-sf-id="'+esc(id)+'"><div class="sf-main"><div class="sf-head"><div class="sf-jewel" aria-hidden="true">'+mark+'</div><div class="sf-head-copy"><h3 class="sf-title2">'+esc(title)+'</h3><div class="sf-meta"><span class="sf-pill">'+esc(stream.toUpperCase())+'</span><span class="sf-pill truth">'+esc(verified)+'</span><span class="sf-pill '+(stream==='collective'?'shared':'')+'">'+esc(visibility)+'</span>'+(date?'<span class="sf-pill">'+esc(date)+'</span>':'')+'</div></div></div><div class="sf-body"><span class="sf-body-label">'+(stream==='activity'?'EVENT':'IN A NUTSHELL')+'</span><p>'+esc(content)+'</p></div>'+(layers?'<div class="sf-layers">'+layers+'</div>':'')+'</div>'+(acts?'<div class="sf-actions">'+acts+'</div>':'')+'</article>';
}

function ensureHost(){
 const feed=root(); if(!feed)return null;
 let host=feed.querySelector('#naya-smart-feed-v2');
 if(!host){host=document.createElement('section');host.id='naya-smart-feed-v2';host.className='naya-sf-v2';feed.prepend(host)}
 return host;
}

function paintShell(){
 const host=ensureHost();if(!host)return;
 const [title,desc]=label[state.stream];
 host.innerHTML='<div class="sf-intro"><div><div class="sf-kicker">NAYANET · SMART FEED · LIVING INTELLIGENCE</div><h2 class="sf-title">Smart Feed</h2><p class="sf-description">'+esc(desc)+'</p></div><div class="sf-authority" id="sf-authority">AUTHORITY · CHECKING</div></div><div class="sf-tabs" role="tablist">'+Object.keys(label).map(k=>'<button type="button" class="sf-tab '+(k===state.stream?'active':'')+'" style="--tone:'+tone[k]+'" data-sf-stream="'+k+'" role="tab" aria-selected="'+(k===state.stream?'true':'false')+'"><strong>'+esc(label[k][0])+'</strong><span>'+esc(label[k][1])+'</span></button>').join('')+'</div><div class="sf-status" id="sf-status"><span>Loading canonical intelligence…</span><button class="sf-refresh" type="button" data-sf-refresh>REFRESH</button></div><div class="sf-list" id="sf-list"></div><div class="sf-more"><button type="button" id="sf-more">LOAD MORE</button></div>';
}

async function load(reset){
 if(state.loading)return;
 const rt=window.NayaAssistantRuntime;
 if(!rt?.smartFeed){setStatus('BLOCKED · canonical smartFeed() is unavailable');return}
 state.loading=true;
 setStatus(reset?'RETRIEVING '+state.stream.toUpperCase()+' FROM CANONICAL RUNTIME…':'RETRIEVING NEXT PAGE…');
 try{
  const data=await rt.smartFeed({stream:state.stream,limit:20,before:reset?null:state.before});
  if(reset)state.items=[];
  const incoming=arr(data?.items);
  state.items.push(...incoming);
  state.before=value(data,'next_before','nextBefore','cursor')||null;
  renderList();
  setStatus('LIVE · '+state.stream.toUpperCase()+' · '+state.items.length+' ITEM'+(state.items.length===1?'':'S')+' · CANONICAL RUNTIME');
 }catch(e){
  state.items=[];
  state.before=null;
  renderList();
  setStatus('BLOCKED / FAILED · '+(e?.message||e));
 }finally{state.loading=false}
}

function setStatus(msg){
 const el=document.getElementById('sf-status');if(!el)return;
 const span=el.querySelector('span');if(span)span.textContent=msg;
 const host=ensureHost(),auth=host?.querySelector('#sf-authority');
 if(auth)auth.textContent=/BLOCKED|FAILED|ERROR/.test(msg)?'AUTHORITY · BLOCKED':'AUTHORITY · ACTIVE';
}
function renderList(){
 const list=document.getElementById('sf-list'),more=document.getElementById('sf-more');
 if(!list)return;
 if(!state.items.length){
  list.innerHTML='<div class="sf-empty"><strong>'+esc(label[state.stream][0])+' IS QUIET</strong><span>No matching intelligence was returned by the canonical runtime for this view. Nothing is fabricated to fill the space.</span></div>';
 }else list.innerHTML=state.items.map(renderItem).join('');
 if(more){more.disabled=!state.before;more.textContent=state.before?'LOAD MORE':'END OF CURRENT PROJECTION'}
}

async function switchStream(stream){
 if(!label[stream]||state.loading)return;
 state.stream=stream;state.before=null;state.items=[];
 paintShell();
 await load(true);
}

async function interact(button){
 const rt=window.NayaAssistantRuntime;if(!rt?.smartFeedAction){setStatus('BLOCKED · smartFeedAction() unavailable');return}
 const action=button.dataset.sfAction,id=button.dataset.sfId;
 button.disabled=true;setStatus('AUTHORIZING '+action.toUpperCase()+'…');
 try{
  if(action==='publish')await rt.smartFeedAction({action:'publish',source_id:id});
  else await rt.smartFeedAction({action:'interact',interaction:action,source_id:id,stream:state.stream});
  setStatus('CONSEQUENCE RECORDED · REFRESHING '+state.stream.toUpperCase()+'…');
  state.before=null;await load(true);
 }catch(e){setStatus('BLOCKED / FAILED · '+(e?.message||e))}finally{button.disabled=false}
}

function bind(){
 const host=ensureHost();if(!host)return;
 host.addEventListener('click',async e=>{
  const tab=e.target.closest('[data-sf-stream]');if(tab){await switchStream(tab.dataset.sfStream);return}
  if(e.target.closest('[data-sf-refresh]')){state.before=null;await load(true);return}
  const more=e.target.closest('#sf-more');if(more&&!more.disabled){await load(false);return}
  const action=e.target.closest('[data-sf-action]');if(action)await interact(action);
 });
}

async function boot(){
 if(!root())return;
 if(document.documentElement.dataset[V]==='1')return;
 document.documentElement.dataset[V]='1';
 styles();
 const rt=window.NayaAssistantRuntime;
 paintShell();bind();
 try{
  const snap=rt?.init?await rt.init():null;
  const auth=ensureHost()?.querySelector('#sf-authority');
  if(!snap?.authenticated){
   if(auth)auth.textContent='AUTHORITY · AUTHENTICATION REQUIRED';
   setStatus('BLOCKED · AUTHENTICATION REQUIRED. Private intelligence is not exposed.');
   return;
  }
  await load(true);
 }catch(e){setStatus('BLOCKED / FAILED · '+(e?.message||e))}
}
function wait(){
 if(root())boot();
 else setTimeout(wait,50);
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',wait,{once:true});else wait();
window.NayaSmartFeedV2={boot,load,switchStream,state};
})();