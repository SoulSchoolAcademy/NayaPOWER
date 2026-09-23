(()=>{'use strict';
/* NayaNET CANONICAL SMART FEED V2
   This script is the Hub's one Smart Feed projection.
   PERSONAL = owner's intelligence.
   COLLECTIVE = intelligence intentionally shared.
   ACTIVITY = what happened.
   Event is history. Intelligent Block is current understanding. Runtime remains canonical.
*/
const KEY='nayaSmartFeedV2';
const tone={personal:'#55b9ee',collective:'#9d75ff',activity:'#55e39a'};
const views={
 personal:['PERSONAL INTELLIGENCE','Your private intelligence — captured, saved, and carried forward.'],
 collective:['COLLECTIVE INTELLIGENCE','Shared intelligence worth discovering, understanding, and using.'],
 activity:['ACTIVITY','A living record of meaningful Naya, human, and system events.']
};
const state={stream:'personal',items:[],before:null,loading:false};
const $=(s,r=document)=>r.querySelector(s);
const esc=v=>String(v??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const clean=v=>String(v??'').replace(/\s+/g,' ').trim();
const pick=(o,...ks)=>{for(const k of ks){const v=o?.[k];if(v!==undefined&&v!==null&&clean(v))return v}return ''};
const list=v=>Array.isArray(v)?v:[];

function css(){
 if($('#naya-smart-feed-v2-css'))return;
 const s=document.createElement('style');s.id='naya-smart-feed-v2-css';s.textContent=`
 .feed:has(#naya-smart-feed-v2)>.feedHead,.feed:has(#naya-smart-feed-v2)>.blocks{display:none!important}
 #naya-smart-feed-v2{margin:0 22px 34px;position:relative}
 #naya-smart-feed-v2 .sf-intro{display:flex;align-items:flex-end;justify-content:space-between;gap:18px;margin:2px 0 15px}
 #naya-smart-feed-v2 .sf-kicker{font-size:8px;font-weight:1000;letter-spacing:.18em;color:#938b9c}
 #naya-smart-feed-v2 .sf-title{margin:5px 0 5px;font-size:clamp(30px,4vw,54px);line-height:.95;letter-spacing:-.055em;color:#fff}
 #naya-smart-feed-v2 .sf-description{max-width:900px;margin:0;color:#aaa4b1;font-size:10px;line-height:1.55}
 #naya-smart-feed-v2 .sf-authority{padding:9px 12px;border:1px solid #ffffff1d;border-radius:11px;background:#09090d;color:#bdb6c5;font-size:7px;font-weight:1000;letter-spacing:.1em;white-space:nowrap}
 #naya-smart-feed-v2 .sf-tabs{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:9px;margin-bottom:13px}
 #naya-smart-feed-v2 .sf-tab{min-height:62px;padding:9px 13px;border:2px solid #ffffff18;border-radius:16px;background:linear-gradient(145deg,#121119,#08080c);color:#a9a1b0;text-align:left;cursor:pointer;box-shadow:inset 0 1px #fff3,0 10px 24px #0008;transition:.22s cubic-bezier(.16,.84,.22,1)}
 #naya-smart-feed-v2 .sf-tab:hover{transform:translateY(-2px);color:#fff;border-color:#ffffff45}
 #naya-smart-feed-v2 .sf-tab.active{color:#fff;border-color:var(--tone);box-shadow:inset 0 1px #fff5,0 15px 32px #000b,0 0 30px color-mix(in srgb,var(--tone) 18%,transparent)}
 #naya-smart-feed-v2 .sf-tab strong{display:block;font-size:11px;letter-spacing:.03em}
 #naya-smart-feed-v2 .sf-tab span{display:block;margin-top:5px;color:#817a89;font-size:7px;line-height:1.35}
 #naya-smart-feed-v2 .sf-tab.active span{color:#c7c0ce}
 #naya-smart-feed-v2 .sf-status{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:12px;padding:10px 12px;border:1px solid #ffffff13;border-radius:12px;background:#08080c;color:#928a99;font-size:8px}
 #naya-smart-feed-v2 .sf-status strong{color:#fff}
 #naya-smart-feed-v2 .sf-refresh,#naya-smart-feed-v2 .sf-more button{border:1px solid #8b63ff66;border-radius:10px;background:#0d0b11;color:#fff;padding:8px 11px;font-size:7px;font-weight:1000;cursor:pointer}
 #naya-smart-feed-v2 .sf-list{display:grid;gap:15px}
 #naya-smart-feed-v2 .sf-card{position:relative;overflow:hidden;border:2px solid color-mix(in srgb,var(--tone) 46%,#ffffff10);border-radius:24px;background:radial-gradient(720px 280px at 78% 0%,color-mix(in srgb,var(--tone) 11%,transparent),transparent 70%),linear-gradient(145deg,#131019,#07080b);box-shadow:inset 0 1px #fff4,0 23px 50px #000b;transition:.22s cubic-bezier(.16,.84,.22,1)}
 #naya-smart-feed-v2 .sf-card:before{content:"";position:absolute;left:0;top:0;bottom:0;width:4px;background:var(--tone);box-shadow:0 0 20px var(--tone)}
 #naya-smart-feed-v2 .sf-card:hover{transform:translateY(-3px);border-color:color-mix(in srgb,var(--tone) 74%,#fff 10%);box-shadow:inset 0 1px #fff5,0 31px 62px #000d,0 0 36px color-mix(in srgb,var(--tone) 11%,transparent)}
 #naya-smart-feed-v2 .sf-main{padding:23px 25px 18px}
 #naya-smart-feed-v2 .sf-head{display:flex;gap:13px;align-items:flex-start}
 #naya-smart-feed-v2 .sf-jewel{width:50px;height:50px;flex:0 0 50px;display:grid;place-items:center;border-radius:16px;border:2px solid color-mix(in srgb,var(--tone) 75%,#fff 8%);background:radial-gradient(circle at 28% 15%,#fff9,transparent 17%),radial-gradient(circle at 50% 50%,color-mix(in srgb,var(--tone) 32%,transparent),#09090e 70%);color:#fff;font-size:21px;box-shadow:inset 0 1px #fff8,0 12px 28px #000b,0 0 26px color-mix(in srgb,var(--tone) 20%,transparent)}
 #naya-smart-feed-v2 .sf-head-copy{min-width:0;flex:1}
 #naya-smart-feed-v2 .sf-title2{margin:1px 0 7px;font-size:clamp(21px,2.8vw,35px);line-height:1.03;letter-spacing:-.045em;color:#fff}
 #naya-smart-feed-v2 .sf-meta{display:flex;gap:6px;flex-wrap:wrap;align-items:center}
 #naya-smart-feed-v2 .sf-pill{padding:5px 7px;border:1px solid #ffffff1b;border-radius:999px;background:#ffffff05;color:#918999;font-size:6px;font-weight:1000;letter-spacing:.09em}
 #naya-smart-feed-v2 .sf-pill.truth{color:#d9ffe9;border-color:#55e39a55;background:#55e39a08}
 #naya-smart-feed-v2 .sf-pill.shared{color:#ddd0ff;border-color:#9d75ff55;background:#9d75ff08}
 #naya-smart-feed-v2 .sf-body{margin:18px 0 0;padding:19px 20px;border:2px solid #ffffff15;border-radius:18px;background:#08080d;box-shadow:inset 0 1px #fff2}
 #naya-smart-feed-v2 .sf-body-label{display:block;margin-bottom:7px;color:#aaa4b1;font-size:7px;font-weight:1000;letter-spacing:.14em}
 #naya-smart-feed-v2 .sf-body p{margin:0;color:#f0edf3;font-size:16px;line-height:1.68}
 #naya-smart-feed-v2 .sf-layers{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:9px;margin-top:12px}
 #naya-smart-feed-v2 .sf-layer{border:1px solid color-mix(in srgb,var(--tone) 29%,#ffffff10);border-radius:14px;background:#09090d;overflow:hidden}
 #naya-smart-feed-v2 .sf-layer summary{list-style:none;cursor:pointer;padding:12px 13px;color:#c2bacb;font-size:7px;font-weight:1000;letter-spacing:.11em}
 #naya-smart-feed-v2 .sf-layer summary::-webkit-details-marker{display:none}
 #naya-smart-feed-v2 .sf-layer summary:after{content:"＋";float:right;color:#766e7d}
 #naya-smart-feed-v2 .sf-layer[open] summary:after{content:"−"}
 #naya-smart-feed-v2 .sf-layer-body{padding:0 13px 14px;color:#c9c2ce;font-size:9px;line-height:1.6;word-break:break-word}
 #naya-smart-feed-v2 .sf-layer-body b{color:#fff}
 #naya-smart-feed-v2 .sf-actions{display:flex;gap:7px;flex-wrap:wrap;padding:13px 25px;border-top:1px solid #ffffff12;background:#08080c}
 #naya-smart-feed-v2 .sf-actions button{min-height:38px;padding:0 11px;border:1px solid #ffffff1c;border-radius:10px;background:linear-gradient(145deg,#14121a,#09090d);color:#eeeaf2;font-size:7px;font-weight:1000;cursor:pointer}
 #naya-smart-feed-v2 .sf-actions button:hover{border-color:var(--tone);transform:translateY(-1px)}
 #naya-smart-feed-v2 .sf-empty{padding:42px 24px;text-align:center;border:2px dashed #ffffff18;border-radius:19px;background:#08080c;color:#8e8796}
 #naya-smart-feed-v2 .sf-empty strong{display:block;color:#fff;font-size:17px;margin-bottom:7px}
 #naya-smart-feed-v2 .sf-empty span{font-size:9px;line-height:1.55}
 #naya-smart-feed-v2 .sf-more{display:flex;justify-content:center;margin:16px 0}
 #naya-smart-feed-v2 .sf-more button:disabled{opacity:.45;cursor:default}
 @media(max-width:760px){#naya-smart-feed-v2{margin:0 14px 25px}#naya-smart-feed-v2 .sf-intro{display:block}#naya-smart-feed-v2 .sf-authority{display:inline-block;margin-top:10px}#naya-smart-feed-v2 .sf-tabs{grid-template-columns:1fr;gap:7px}#naya-smart-feed-v2 .sf-tab{min-height:54px}#naya-smart-feed-v2 .sf-main{padding:18px 17px 15px}#naya-smart-feed-v2 .sf-jewel{width:43px;height:43px;flex-basis:43px}#naya-smart-feed-v2 .sf-layers{grid-template-columns:1fr}#naya-smart-feed-v2 .sf-actions{padding:12px 17px}#naya-smart-feed-v2 .sf-body p{font-size:14px}}
 @media(prefers-reduced-motion:reduce){#naya-smart-feed-v2 *{transition:none!important}}
 `;
 document.head.appendChild(s);
}

function actionButtons(item){
 const allowed=list(item.available_actions).map(x=>String(x).toLowerCase());
 return ['save','favorite','like','love','publish'].filter(a=>allowed.includes(a)).map(a=>'<button type="button" data-sf-action="'+a+'" data-sf-id="'+esc(pick(item,'source_id','id'))+'">'+({save:'🔖 SAVE',favorite:'★ FAVORITE',like:'👍 LIKE',love:'♥ LOVE',publish:'◇ SHARE'}[a])+'</button>').join('');
}
function layer(title,body){return body?'<details class="sf-layer"><summary>'+esc(title)+'</summary><div class="sf-layer-body">'+body+'</div></details>':''}
function metadataLayers(item){
 const ib=item?.metadata?.intelligent_block_v1;
 if(!ib||typeof ib!=='object')return '';
 const identity=ib.identity||{},context=ib.context||{},truth=ib.truth||{},authority=ib.authority||{},value=ib.value||{},life=ib.lifecycle||{},integrity=ib.integrity||{};
 let out='';
 out+=layer('BLOCK · IDENTITY','<b>Schema:</b> '+esc(pick(identity,'schema_version','schema')||'NOT RECORDED')+'<br><b>Event:</b> '+esc(pick(identity,'event_id')||item.event_id||'UNKNOWN'));
 out+=layer('TRUTH · VERIFICATION','<b>State:</b> '+esc(pick(truth,'state','status')||item.verification_state||'UNKNOWN')+'<br><b>Evidence:</b> '+esc(pick(truth,'evidence_state','evidence')||'NOT RECORDED'));
 out+=layer('AUTHORITY','<b>State:</b> '+esc(pick(authority,'state','status')||'UNKNOWN')+'<br><b>Scope:</b> '+esc(pick(authority,'scope','reason')||'NOT RECORDED'));
 out+=layer('PRIVACY · CONTEXT','<b>Visibility:</b> '+esc(pick(context,'visibility')||item.visibility||'UNKNOWN')+'<br><b>Classification:</b> '+esc(item.classification||'UNKNOWN'));
 out+=layer('LIFECYCLE','<b>Stage:</b> '+esc(pick(life,'stage','status')||'UNKNOWN')+'<br><b>Lineage:</b> '+esc(pick(life,'lineage','parent_event_id')||'NOT RECORDED'));
 out+=layer('VALUE','<b>State:</b> '+esc(pick(value,'state','status')||'UNKNOWN')+'<br><b>Confidence:</b> '+esc(item.confidence??'unknown'));
 out+=layer('INTEGRITY','<b>Content hash:</b> '+esc(pick(integrity,'content_hash','sha256')||'NOT RECORDED'));
 const p=ib.perspectives||ib.layers||{};
 const names=[['HUMAN NOTE','human_note','human'],['CHILD NOTE','child_note','child'],['GRANDMA NOTE','grandma_note','grandma'],['NAYA NOTE','naya_note','naya'],['MACHINE NOTE','machine_note','machine'],['ADAPTIVE LEARNING','adaptive_learning','learning'],['WHAT IT MEANS','what_it_means','meaning'],["WHAT'S IN IT FOR YOU",'human_value','value']];
 for(const [title,key,alt] of names){const v=pick(p,key,alt, title.toLowerCase().replace(/[^a-z]+/g,'_'));if(v)out+=layer(title,esc(v))}
 return out;
}
function renderItem(item){
 const stream=state.stream,t=tone[stream],ib=item?.metadata?.intelligent_block_v1||{};
 const title=clean(pick(item,'title','name','event_type','event_id')||'Intelligence');
 const body=clean(pick(item,'content','summary','description')||'No content was returned by the canonical runtime.');
 const verification=clean(pick(item,'verification_state','verification','status')||ib?.truth?.state||'UNKNOWN');
 const visibility=clean(pick(item,'visibility','sharing_state')||ib?.context?.visibility||(stream==='collective'?'SHARED':'PRIVATE'));
 const source=clean(pick(item,'source','source_type')||'CANONICAL RUNTIME');
 const event=clean(pick(item,'event_id','id')||'UNKNOWN');
 const id=clean(pick(item,'source_id','intelligence_id','id')||event);
 const classification=clean(pick(item,'classification','type')||'UNCLASSIFIED');
 const date=clean(pick(item,'published_at','created_at','occurred_at','timestamp')||'');
 const mark=stream==='activity'?'↗':stream==='collective'?'◇':'✦';
 let layers='';
 if(stream==='activity'){
   layers+=layer('WHAT HAPPENED','<b>Event:</b> '+esc(event)+'<br><b>Type:</b> '+esc(classification)+'<br><b>Source:</b> '+esc(source)+(date?'<br><b>When:</b> '+esc(date):''));
   layers+=layer('TRUTH · VISIBILITY','<b>Verification:</b> '+esc(verification)+'<br><b>Visibility:</b> '+esc(visibility));
   const consequence=clean(pick(item,'consequence','outcome','result','what_changed'));
   if(consequence)layers+=layer('WHAT CHANGED',esc(consequence));
 }else{
   layers+=metadataLayers(item);
   if(!layers)layers=layer('SOURCE · PROVENANCE','<b>Source:</b> '+esc(source)+'<br><b>Event:</b> '+esc(event)+'<br><b>Classification:</b> '+esc(classification));
 }
 const acts=actionButtons(item);
 return '<article class="sf-card" style="--tone:'+t+'" data-sf-id="'+esc(id)+'" data-event-id="'+esc(event)+'" data-intelligent-block-schema="'+esc(pick(ib.identity,'schema_version','schema'))+'" data-intelligent-block-event-id="'+esc(pick(ib.identity,'event_id')||event)+'" data-intelligent-block-truth="'+esc(pick(ib.truth,'state','status'))+'" data-intelligent-block-authority="'+esc(pick(ib.authority,'state','status'))+'" data-intelligent-block-value="'+esc(pick(ib.value,'state','status'))+'" data-intelligent-block-privacy="'+esc(pick(ib.context,'visibility'))+'" data-intelligent-block-lifecycle="'+esc(pick(ib.lifecycle,'stage','status'))+'" data-intelligent-block-hash="'+esc(pick(ib.integrity,'content_hash','sha256'))+'"><div class="sf-main"><div class="sf-head"><div class="sf-jewel" aria-hidden="true">'+mark+'</div><div class="sf-head-copy"><h2 class="sf-title2">'+esc(title)+'</h2><div class="sf-meta"><span class="sf-pill">'+esc(stream.toUpperCase())+'</span><span class="sf-pill truth">'+esc(verification)+'</span><span class="sf-pill '+(stream==='collective'?'shared':'')+'">'+esc(visibility)+'</span>'+(date?'<span class="sf-pill">'+esc(date)+'</span>':'')+'</div></div></div><div class="sf-body"><span class="sf-body-label">'+(stream==='activity'?'WHAT HAPPENED':'IN A NUTSHELL')+'</span><p>'+esc(body)+'</p></div>'+(layers?'<div class="sf-layers">'+layers+'</div>':'')+'</div>'+(acts?'<div class="sf-actions">'+acts+'</div>':'')+'</article>';
}
function host(){
 const feed=$('.feed');if(!feed)return null;
 let h=$('#naya-smart-feed-v2',feed);
 if(!h){h=document.createElement('section');h.id='naya-smart-feed-v2';h.className='naya-sf-v2';feed.prepend(h)}
 return h;
}
function shell(){
 const h=host();if(!h)return;
 const [title,desc]=views[state.stream];
 h.innerHTML='<div class="sf-intro"><div><div class="sf-kicker">NAYANET · SMART FEED · LIVING INTELLIGENCE</div><h2 class="sf-title">Smart Feed</h2><p class="sf-description">'+esc(desc)+'</p></div><div class="sf-authority" id="sf-authority">AUTHORITY · CHECKING</div></div><div class="sf-tabs" role="tablist">'+Object.keys(views).map(k=>'<button type="button" class="sf-tab '+(k===state.stream?'active':'')+'" style="--tone:'+tone[k]+'" data-sf-stream="'+k+'" role="tab" aria-selected="'+(k===state.stream?'true':'false')+'"><strong>'+esc(views[k][0])+'</strong><span>'+esc(views[k][1])+'</span></button>').join('')+'</div><div class="sf-status" id="sf-status"><span>Loading canonical intelligence…</span><button class="sf-refresh" type="button" data-sf-refresh>REFRESH</button></div><div class="sf-list" id="sf-list"></div><div class="sf-more"><button type="button" id="sf-more">LOAD MORE</button></div>';
}
function status(msg){
 const h=host();if(!h)return;
 const s=$('#sf-status',h),a=$('#sf-authority',h);if(s){const span=$('span',s);if(span)span.textContent=msg}
 if(a)a.textContent=/BLOCKED|FAILED|ERROR/.test(msg)?'AUTHORITY · BLOCKED':'AUTHORITY · ACTIVE';
}
function draw(){
 const l=$('#sf-list',host()),m=$('#sf-more',host());if(!l)return;
 if(!state.items.length)l.innerHTML='<div class="sf-empty"><strong>'+esc(views[state.stream][0])+' IS QUIET</strong><span>No matching intelligence was returned by the canonical runtime for this view. Nothing is fabricated to fill the space.</span></div>';
 else l.innerHTML=state.items.map(renderItem).join('');
 if(m){m.disabled=!state.before;m.textContent=state.before?'LOAD MORE':'END OF CURRENT PROJECTION'}
}
async function load(reset){
 if(state.loading)return;
 const rt=window.NayaAssistantRuntime;
 if(!rt?.smartFeed){status('BLOCKED · canonical smartFeed() is unavailable');return}
 state.loading=true;status(reset?'RETRIEVING '+state.stream.toUpperCase()+' FROM CANONICAL RUNTIME…':'RETRIEVING NEXT PAGE…');
 try{
   const data=await rt.smartFeed({stream:state.stream,limit:20,before:reset?null:state.before});
   if(reset)state.items=[];
   const incoming=list(data?.items);
   const probe=incoming.find(x=>String(x?.event_id||'')==='__P0_02_PROBE__');
   if(typeof window.__nayaSmartFeedProbe==='function')window.__nayaSmartFeedProbe({items:incoming,probe});
   state.items.push(...incoming);state.before=pick(data,'next_before','nextBefore','cursor')||null;draw();
   status('LIVE · '+state.stream.toUpperCase()+' · '+state.items.length+' ITEM'+(state.items.length===1?'':'S')+' · CANONICAL RUNTIME');
 }catch(e){state.items=[];state.before=null;draw();status('BLOCKED / FAILED · '+(e?.message||e))}finally{state.loading=false}
}
async function switchStream(k){if(!views[k]||state.loading)return;state.stream=k;state.items=[];state.before=null;shell();await load(true)}
async function act(btn){
 const rt=window.NayaAssistantRuntime;if(!rt?.smartFeedAction){status('BLOCKED · smartFeedAction() unavailable');return}
 const action=btn.dataset.sfAction,id=btn.dataset.sfId;btn.disabled=true;status('AUTHORIZING '+action.toUpperCase()+'…');
 try{
   if(action==='publish')await rt.smartFeedAction({action:'publish',source_id:id});
   else await rt.smartFeedAction({action:'interact',interaction:action,source_id:id,stream:state.stream});
   state.before=null;status('CONSEQUENCE RECORDED · REFRESHING…');await load(true);
 }catch(e){status('BLOCKED / FAILED · '+(e?.message||e))}finally{btn.disabled=false}
}
function bind(){
 const h=host();if(!h||h.dataset.bound==='1')return;h.dataset.bound='1';
 h.addEventListener('click',async e=>{
   const tab=e.target.closest('[data-sf-stream]');if(tab){await switchStream(tab.dataset.sfStream);return}
   if(e.target.closest('[data-sf-refresh]')){state.before=null;await load(true);return}
   const more=e.target.closest('#sf-more');if(more&&!more.disabled){await load(false);return}
   const action=e.target.closest('[data-sf-action]');if(action)await act(action);
 });
}
async function waitForIdentity(){
 const auth=window.NayaNETNameFirstAuth;
 if(!auth?.current)return null;
 for(let i=0;i<60;i++){
   try{const identity=await auth.current();if(identity?.authenticated&&identity?.userId)return identity}catch(_){}
   await new Promise(r=>setTimeout(r,250));
 }
 return null;
}
async function boot(){
 const feedRoute=location.pathname==='/feed'||location.hash==='#feed';
 if(!feedRoute&&!document.documentElement.dataset.nayaExplicitSmartFeed)return;
 if(!$('.feed'))return;
 if(document.documentElement.dataset[KEY]==='1')return;
 document.documentElement.dataset[KEY]='1';css();shell();bind();
 try{
   const identity=await waitForIdentity();
   if(!identity?.authenticated){status('BLOCKED · AUTHENTICATION REQUIRED. Private intelligence is not exposed.');return}
   const snap=window.NayaAssistantRuntime?.init?await window.NayaAssistantRuntime.init():null;
   if(!snap?.authenticated){status('BLOCKED · AUTHENTICATION REQUIRED. Private intelligence is not exposed.');return}
   await load(true);
 }catch(e){status('BLOCKED / FAILED · '+(e?.message||e))}
}
function wait(){if($('.feed'))boot();else setTimeout(wait,50)}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',wait,{once:true});else wait();
window.NayaSmartFeedV2={boot,load,switchStream,state};
})();