/* NayaNET 509 AAA — REAL SMART FEED CONTENT RENDERER
 * SOURCE-DRIVEN: the build injects the complete canonical SMART FEED CONTENT payload.
 * This renderer never invents demo notes and never removes feed navigation, mission,
 * or Feature Reports. It renders exactly the nine canonical Smart Notes from source.
 */
(()=>{'use strict';
const PAYLOAD='__SMART_FEED_B64__';if(!PAYLOAD||PAYLOAD==='__SMART_FEED_B64__')return;
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const dec=()=>{try{return decodeURIComponent(escape(atob(PAYLOAD)))}catch(_){try{return atob(PAYLOAD)}catch(e){return''}}};
const source=dec();if(!source)return;
const tones=['#ffffff','#ff4fd8','#d86cff','#9d75ff','#55b9ee','#55e39a','#b8ee57','#e8c766','#ff5e6c'];
const glyphs=['◈','✦','◇','◉','✧','◆','⬢','✺','✦'];
function parseSections(text){const sections={};const re=/(?:^|\n)\s*(\d+)\.\s*([^\n]+)\n([\s\S]*?)(?=\n\s*\d+\.\s|$)/g;let m;while((m=re.exec(text)))sections[Number(m[1])]={name:m[2].trim(),text:m[3].trim()};return sections}
function parseNotes(text){
 const markers=[
  {number:1,re:/^🧠\s*NAYA\s+POWER\s*[—-]\s*SMART\s+NOTE\s*01\b/im,title:'Naya Power'},
  {number:2,re:/^🧠\s*NAYA\s+POWER\s*[—-]\s*SMART\s+NOTE\s*02\b/im,title:'Naya'},
  {number:3,re:/^🧠\s*NAYA\s+POWER\s*[—-]\s*SMART\s+NOTE\s*03\b/im,title:'Smart Notes'},
  {number:4,re:/^🧠\s*#4\s*[—-]\s*YOUR\s+INTELLIGENCE\s+TODAY\s*$/im,title:'Your Intelligence Today'},
  {number:6,re:/Naya\s+Power\s*#06\s*[—-]\s*What\s+Is\s+the\s+Intelligent\s+Library\?/im,title:'Intelligent Library'},
  {number:7,re:/^07\s*[—-]\s*SMART\s+LISTS\s*$/im,title:'Smart Lists'},
  {number:8,re:/^08\s*[—-]\s*INTELLIGENT\s+FEED\s*\/\s*SMART\s+FEED\s*$/im,title:'Intelligent Feed / Smart Feed'},
  {number:9,re:/^09\s*[—-]\s*SMART\s+TABS\s*$/im,title:'Smart Tabs'}
 ];
 const found=markers.map(x=>{const m=text.match(x.re);return m?{...x,pos:m.index}:null}).filter(Boolean).sort((a,b)=>a.pos-b.pos);
 const p6=found.find(x=>x.number===6)?.pos??-1;
 const ranges=[];
 for(let i=0;i<found.length;i++){
  const a=found[i],b=found[i+1];
  if(a.number===4&&p6>=0){
   const chunk=text.slice(a.pos,p6);
   const split=chunk.search(/\n[-_]{20,}\s*\n\s*1\.\s*IN A NUTSHELL\s*\n\s*Intelligence Reports\b/i);
   if(split>0){ranges.push({number:4,start:a.pos,end:a.pos+split,title:a.title});ranges.push({number:5,start:a.pos+split,end:p6,title:'Intelligence Reports'})}
   else ranges.push({number:4,start:a.pos,end:p6,title:a.title});
  }else if(a.number!==4){ranges.push({number:a.number,start:a.pos,end:b?b.pos:text.length,title:a.title})}
 }
 const notes=ranges.map(r=>{
  let rest=text.slice(r.start,r.end).trim();
  if(r.number<=3){
   const lines=rest.split(/\r?\n/);
   while(lines.length){const x=(lines[0]||'').trim();if(!x){lines.shift();continue}if(/^🧠\s*NAYA\s+POWER/i.test(x)){lines.shift();continue}if(r.number===1&&/^What\s+Is\s+Naya\s+Power\?/i.test(x)){lines.shift();continue}if(r.number===2&&/^What\s+Is\s+Naya\?/i.test(x)){lines.shift();continue}if(r.number===3&&/^What\s+Are\s+Smart\s+Notes\?/i.test(x)){lines.shift();continue}break}
   rest=lines.join('\n');
  }
  if(r.number===6)rest=rest.replace(/^Status:[^\n]*\n?/im,'').replace(/^Date:[^\n]*\n?/im,'').replace(/^Subject:[^\n]*\n?/im,'').replace(/^Smart Note Type:[^\n]*\n?/im,'').replace(/^Naya\s+Power\s*#06[^\n]*\n?/im,'');
  return {number:r.number,title:r.title,sections:parseSections(rest)};
 }).filter(n=>Object.keys(n.sections).length).sort((a,b)=>a.number-b.number);
 return notes.length===9&&notes.every((n,i)=>n.number===i+1)?notes:[];
}
const body=t=>esc(t).replace(/\n/g,'<br>');
function actions(){return `<div class="actions" role="group" aria-label="Intelligence actions"><button class="action create" type="button" data-c4-kind="create-space">＋ CREATE SPACE</button><button class="action favorite" type="button" data-c4-kind="favorite">★ FAVORITE</button><button class="action save" type="button" data-c4-kind="save">SAVE</button><button class="action love" type="button" data-c4-kind="love" aria-pressed="false">❤️ LOVE</button><button class="action like" type="button" data-c4-kind="like" aria-pressed="false">LIKE</button><span class="naya509-rating" data-c4-kind="rating" role="group" aria-label="Rate this intelligence"><span class="ratingLabel">RATE THIS INTELLIGENCE</span><span class="ratingStars">${[1,2,3,4,5].map(n=>`<button type="button" class="ratingStar" data-rating="${n}" aria-label="Rate ${n} out of 5">★</button>`).join('')}</span></span><button class="action share" type="button" data-c4-kind="share-intel">＋ SHARE INTEL</button></div>`}
function board(note,idx){const tone=tones[idx%tones.length],nums=Object.keys(note.sections).map(Number).sort((a,b)=>a-b),nuts=note.sections[1];const layers=nums.filter(n=>n!==1).map(n=>{const s=note.sections[n];return `<article class="layer" style="--layer:${tone}"><div class="layerHead"><span class="dot"></span><b>${esc(s.name)}</b><span class="state">SMART NOTE · ${String(note.number).padStart(2,'0')}</span></div><div class="layerBody">${body(s.text)}</div></article>`}).join('');return `<article class="block naya509-board" data-real-smart-note="${note.number}" data-intelligence-id="smart-note-${String(note.number).padStart(2,'0')}" style="--tone:${tone}"><div class="blockInner"><div class="blockTop"><div class="identity"><div class="glyph">${glyphs[idx%glyphs.length]}</div><div><h3>${esc(note.title)}</h3><div class="meta"><span>SMART NOTE ${String(note.number).padStart(2,'0')}</span><span>CANONICAL INTELLIGENCE</span></div></div></div><div class="truth">SOURCE CONTENT</div></div>${nuts?`<div class="nutshell"><b>IN A NUTSHELL</b><p>${body(nuts.text)}</p></div>`:''}<div class="layers">${layers}</div>${actions()}<div class="blockFoot"><span>REAL SMART NOTE CONTENT · SOURCE: SMART FEED CONTENT</span><span>INTELLIGENCE EVENT ${String(note.number).padStart(2,'0')}</span></div></div></article>`}
function stripLegacyBars(){
 document.querySelectorAll('.railCard,.contextBar,.collectiveBar,.statusBar,.feedStatus,.feedBanner,.runtimeBar').forEach(e=>{if(e.closest('.feedNav'))return;const t=(e.textContent||'').trim();if(/INTELLIGENCE\s+(CONTEXT|COLLECTIVE)/i.test(t)||/^COLLECTIVE\s+INTELLIGENCE\s+WORTH/i.test(t)||/^ACTIONS\s+ARE\s+REMEMBERED\s+ON\s+THIS\s+DEVICE/i.test(t)||/^RUNTIME\s+STATE\s+VISIBLE/i.test(t))e.remove()});
 document.querySelectorAll('body *').forEach(e=>{if(e.closest('.feedNav')||e.children.length)return;const t=(e.textContent||'').trim();if(/^INTELLIGENCE\s+(CONTEXT|COLLECTIVE)$/i.test(t)||/^ACTIONS\s+ARE\s+REMEMBERED\s+ON\s+THIS\s+DEVICE$/i.test(t)||/^RUNTIME\s+STATE\s+VISIBLE$/i.test(t)){const p=e.closest('.railCard,.contextBar,.collectiveBar,.statusBar,.feedStatus,.feedBanner,.runtimeBar');if(p&&!p.closest('.feedNav'))p.remove()}});
 document.querySelectorAll('.naya509-mission').forEach(e=>e.remove());
}
function run(){const blocks=document.querySelector('.blocks');if(!blocks)return false;const notes=parseNotes(source);if(notes.length!==9)return false;const sig=notes.map(n=>`${n.number}:${n.title}`).join('|');if(blocks.dataset.nayaRealSignature!==sig||blocks.querySelectorAll('[data-real-smart-note]').length!==9){blocks.dataset.nayaRealRendering='1';blocks.innerHTML=notes.map(board).join('');blocks.dataset.nayaRealSignature=sig;blocks.dataset.nayaRealRendering='0'}stripLegacyBars();document.documentElement.dataset.nayaRealSmartFeed='true';document.documentElement.dataset.nayaRealSmartNoteCount='9';return true}
function style(){if(document.getElementById('naya509-real-content-style'))return;const s=document.createElement('style');s.id='naya509-real-content-style';s.textContent=`
.naya509-board{min-height:0!important;padding:34px 38px 42px 42px!important}.naya509-board .blockInner{max-width:1500px!important;margin:0 auto!important}.naya509-board .meta,.naya509-board .truth,.naya509-board .state{font-size:14px!important;line-height:1.4!important}.naya509-board .layerHead b{font-size:18px!important}.naya509-board .layerBody{font-size:20px!important;line-height:1.62!important;color:#e7e2eb!important}.naya509-board .nutshell b{font-size:15px!important}.naya509-board .nutshell p{font-size:24px!important;line-height:1.58!important}.naya509-board .action{font-size:15px!important;min-height:52px!important;padding:0 17px!important}.naya509-board .ratingLabel{font-size:14px!important}.naya509-board .ratingStar{font-size:30px!important;width:46px!important;height:46px!important}
@media(max-width:760px){.naya509-board{padding:26px 18px 34px 28px!important}.naya509-board .layerBody{font-size:19px!important}.naya509-board .layerHead b{font-size:17px!important}.naya509-board .nutshell p{font-size:21px!important}.naya509-board .action{font-size:14px!important}.naya509-board .ratingStar{width:42px!important;height:44px!important;font-size:28px!important}}
`;document.head.appendChild(s)}
function boot(){style();run();const b=document.querySelector('.blocks');if(b&&!b.dataset.nayaRealObserver){const mo=new MutationObserver(()=>{if(b.dataset.nayaRealRendering!=='1')run()});mo.observe(b,{childList:true});b.dataset.nayaRealObserver='1'}return !!b}
window.Naya509RealSmartFeed={boot,run,version:'final-boot-4'};
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
})();

/* C4 NAV RESTORE — the real-content renderer must never collapse the three sacred feed controls. */
(()=>{'use strict';
const LABELS=/^(PERSONAL\s+INTELLIGENCE|COLLECTIVE\s+INTELLIGENCE|ACTIVITY\s+FEED)$/i;
function norm(s){return String(s||'').replace(/\s+/g,' ').trim()}
function tone(t){t=t.toUpperCase();return t.startsWith('COLLECTIVE')?'purple':t.startsWith('PERSONAL')?'blue':'green'}
function run(){const nav=document.querySelector('.feedNav');if(!nav)return false;
 const controls=[...nav.querySelectorAll('button,a,[role="button"]')].filter(x=>LABELS.test(norm(x.textContent)));
 const unique=[];const seen=new Set();controls.forEach(x=>{const k=norm(x.textContent).toUpperCase();if(!seen.has(k)){seen.add(k);unique.push(x)}else{x.remove()}});
 unique.forEach(el=>{el.dataset.naya509FeedTone=tone(norm(el.textContent));el.style.setProperty('display','inline-flex','important');el.style.setProperty('visibility','visible','important');el.style.setProperty('opacity','1','important');el.style.setProperty('width','100%','important');el.style.setProperty('max-width','none','important');el.style.setProperty('height','52px','important');el.style.setProperty('min-height','52px','important');el.style.setProperty('align-items','center','important');el.style.setProperty('justify-content','center','important');el.style.setProperty('text-align','center','important');el.style.setProperty('box-sizing','border-box','important')});
 nav.style.setProperty('display','grid','important');nav.style.setProperty('grid-template-columns','repeat(3,minmax(0,1fr))','important');nav.style.setProperty('gap','12px','important');nav.style.setProperty('width','100%','important');nav.style.setProperty('padding','0 22px 15px','important');nav.style.setProperty('box-sizing','border-box','important');return unique.length===3}
function css(){if(document.getElementById('naya509-real-content-nav-css'))return;const s=document.createElement('style');s.id='naya509-real-content-nav-css';s.textContent=`
.feedNav{display:grid!important;grid-template-columns:repeat(3,minmax(0,1fr))!important;gap:12px!important;width:100%!important;align-items:stretch!important}
.feedNav button,.feedNav a,.feedNav [role="button"]{display:inline-flex!important;width:100%!important;max-width:none!important;height:52px!important;min-height:52px!important;align-items:center!important;justify-content:center!important;text-align:center!important;box-sizing:border-box!important;border-radius:15px!important;background:#09090e!important;color:#f4f0f7!important;font-size:15px!important;font-weight:850!important;line-height:1!important}
.feedNav [data-naya509-feed-tone="purple"]{border:2px solid #b06cff99!important;background:linear-gradient(180deg,#21122f,#0c0a12)!important;box-shadow:0 0 22px #a95cff20,0 7px 20px #00000066,inset 0 1px 0 #ffffff18!important}
.feedNav [data-naya509-feed-tone="blue"]{border:2px solid #55b9ee99!important;background:linear-gradient(180deg,#102333,#090c11)!important;box-shadow:0 0 22px #55b9ee20,0 7px 20px #00000066,inset 0 1px 0 #ffffff18!important}
.feedNav [data-naya509-feed-tone="green"]{border:2px solid #55e39a99!important;background:linear-gradient(180deg,#10271d,#090d0b)!important;box-shadow:0 0 22px #55e39a20,0 7px 20px #00000066,inset 0 1px 0 #ffffff18!important}
.feedNav [data-naya509-feed-tone="purple"].active{border-color:#c58aff!important;box-shadow:0 0 30px #b86cff55,0 8px 22px #00000077,inset 0 1px 0 #ffffff25!important}
.feedNav [data-naya509-feed-tone="blue"].active{border-color:#7bd4ff!important;box-shadow:0 0 30px #55b9ee55,0 8px 22px #00000077,inset 0 1px 0 #ffffff25!important}
.feedNav [data-naya509-feed-tone="green"].active{border-color:#79f4b1!important;box-shadow:0 0 30px #55e39a55,0 8px 22px #00000077,inset 0 1px 0 #ffffff25!important}
@media(max-width:760px){.feedNav{grid-template-columns:1fr!important;gap:8px!important;padding:0 14px 13px!important}.feedNav button,.feedNav a,.feedNav [role="button"]{height:50px!important;min-height:50px!important;font-size:14px!important}}
`;document.head.appendChild(s)}
function boot(){css();run();if(!window.__naya509RealContentNavObserver){const mo=new MutationObserver(()=>{css();run()});mo.observe(document.body,{childList:true,subtree:true});window.__naya509RealContentNavObserver=mo}}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
})();