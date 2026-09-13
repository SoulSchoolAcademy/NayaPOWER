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
function parseNotes(text){
 const chunks=text.split(/(?=^\s*🧠\s*NAYA\s+POWER\s*[—-]\s*SMART\s+NOTE\s*\d+\b)/im).map(x=>x.trim()).filter(Boolean);
 const notes=[];
 for(const chunk of chunks){
   const head=chunk.match(/^🧠\s*NAYA\s+POWER\s*[—-]\s*SMART\s+NOTE\s*(\d+)\s*\n([\s\S]*)$/i);if(!head)continue;
   const number=Number(head[1]);if(number<1||number>9)continue;
   let rest=head[2].trim();
   const lines=rest.split(/\r?\n/);let title='';
   while(lines.length){const x=(lines[0]||'').trim();if(!x) {lines.shift();continue} if(/^Subject\s+ID\s*:/i.test(x)||/^Status\s*:/i.test(x)||/^SAY\s+EVERYTHING/i.test(x)){lines.shift();continue} title=x;lines.shift();break}
   const chunkBody=lines.join('\n').trim(),sections={};
   const re=/(?:^|\n)\s*(\d+)\.\s*([^\n]+)\n([\s\S]*?)(?=\n\s*\d+\.\s|$)/g;let m;
   while((m=re.exec(chunkBody)))sections[Number(m[1])]={name:m[2].trim(),text:m[3].trim()};
   if(Object.keys(sections).length)notes.push({number,title,sections});
 }
 return notes.sort((a,b)=>a.number-b.number).filter((n,i,a)=>i===0||n.number!==a[i-1].number);
}
const body=t=>esc(t).replace(/\n/g,'<br>');
function actions(){return `<div class="actions" role="group" aria-label="Intelligence actions"><button class="action create" type="button" data-c4-kind="create-space">＋ CREATE SPACE</button><button class="action favorite" type="button" data-c4-kind="favorite">★ FAVORITE</button><button class="action save" type="button" data-c4-kind="save">SAVE</button><button class="action love" type="button" data-c4-kind="love" aria-pressed="false">❤️ LOVE</button><button class="action like" type="button" data-c4-kind="like" aria-pressed="false">LIKE</button><span class="naya509-rating" data-c4-kind="rating" role="group" aria-label="Rate this intelligence"><span class="ratingLabel">RATE THIS INTELLIGENCE</span><span class="ratingStars">${[1,2,3,4,5].map(n=>`<button type="button" class="ratingStar" data-rating="${n}" aria-label="Rate ${n} out of 5">★</button>`).join('')}</span></span><button class="action share" type="button" data-c4-kind="share-intel">＋ SHARE INTEL</button></div>`}
function board(note,idx){const tone=tones[idx%tones.length],nums=Object.keys(note.sections).map(Number).sort((a,b)=>a-b),nuts=note.sections[1];const layers=nums.filter(n=>n!==1).map(n=>{const s=note.sections[n];return `<article class="layer" style="--layer:${tone}"><div class="layerHead"><span class="dot"></span><b>${esc(s.name)}</b><span class="state">SMART NOTE · ${String(note.number).padStart(2,'0')}</span></div><div class="layerBody">${body(s.text)}</div></article>`}).join('');return `<article class="block naya509-board" data-real-smart-note="${note.number}" data-intelligence-id="smart-note-${String(note.number).padStart(2,'0')}" style="--tone:${tone}"><div class="blockInner"><div class="blockTop"><div class="identity"><div class="glyph">${glyphs[idx%glyphs.length]}</div><div><h3>${esc(note.title)}</h3><div class="meta"><span>SMART NOTE ${String(note.number).padStart(2,'0')}</span><span>CANONICAL INTELLIGENCE</span></div></div></div><div class="truth">SOURCE CONTENT</div></div>${nuts?`<div class="nutshell"><b>IN A NUTSHELL</b><p>${body(nuts.text)}</p></div>`:''}<div class="layers">${layers}</div>${actions()}<div class="blockFoot"><span>REAL SMART NOTE CONTENT · SOURCE: SMART FEED CONTENT</span><span>INTELLIGENCE EVENT ${String(note.number).padStart(2,'0')}</span></div></div></article>`}
function stripLegacyBars(){
 document.querySelectorAll('.railCard,.contextBar,.collectiveBar,.statusBar,.feedStatus,.feedBanner,.runtimeBar').forEach(e=>{if(e.closest('.feedNav'))return;const t=(e.textContent||'').trim();if(/INTELLIGENCE\s+(CONTEXT|COLLECTIVE)/i.test(t)||/^COLLECTIVE\s+INTELLIGENCE\s+WORTH/i.test(t)||/^ACTIONS\s+ARE\s+REMEMBERED\s+ON\s+THIS\s+DEVICE/i.test(t)||/^RUNTIME\s+STATE\s+VISIBLE/i.test(t))e.remove()});
 document.querySelectorAll('body *').forEach(e=>{if(e.closest('.feedNav')||e.children.length)return;const t=(e.textContent||'').trim();if(/^INTELLIGENCE\s+(CONTEXT|COLLECTIVE)$/i.test(t)||/^ACTIONS\s+ARE\s+REMEMBERED\s+ON\s+THIS\s+DEVICE$/i.test(t)||/^RUNTIME\s+STATE\s+VISIBLE$/i.test(t)){const p=e.closest('.railCard,.contextBar,.collectiveBar,.statusBar,.feedStatus,.feedBanner,.runtimeBar');if(p&&!p.closest('.feedNav'))p.remove()}}
 document.querySelectorAll('.naya509-mission').forEach(e=>e.remove());
}
function run(){const blocks=document.querySelector('.blocks');if(!blocks)return false;const notes=parseNotes(source);if(notes.length!==9||notes.some((n,i)=>n.number!==i+1))return false;const sig=notes.map(n=>`${n.number}:${n.title}`).join('|');if(blocks.dataset.nayaRealSignature!==sig||blocks.querySelectorAll('[data-real-smart-note]').length!==9){blocks.dataset.nayaRealRendering='1';blocks.innerHTML=notes.map(board).join('');blocks.dataset.nayaRealSignature=sig;blocks.dataset.nayaRealRendering='0'}stripLegacyBars();document.documentElement.dataset.nayaRealSmartFeed='true';document.documentElement.dataset.nayaRealSmartNoteCount='9';return true}
function style(){if(document.getElementById('naya509-real-content-style'))return;const s=document.createElement('style');s.id='naya509-real-content-style';s.textContent=`
.naya509-board{min-height:0!important;padding:34px 38px 42px 42px!important}.naya509-board .blockInner{max-width:1500px!important;margin:0 auto!important}.naya509-board .meta,.naya509-board .truth,.naya509-board .state{font-size:14px!important;line-height:1.4!important}.naya509-board .layerHead b{font-size:18px!important}.naya509-board .layerBody{font-size:20px!important;line-height:1.62!important;color:#e7e2eb!important}.naya509-board .nutshell b{font-size:15px!important}.naya509-board .nutshell p{font-size:24px!important;line-height:1.58!important}.naya509-board .action{font-size:15px!important;min-height:52px!important;padding:0 17px!important}.naya509-board .ratingLabel{font-size:14px!important}.naya509-board .ratingStar{font-size:30px!important;width:46px!important;height:46px!important}
@media(max-width:760px){.naya509-board{padding:26px 18px 34px 28px!important}.naya509-board .layerBody{font-size:19px!important}.naya509-board .layerHead b{font-size:17px!important}.naya509-board .nutshell p{font-size:21px!important}.naya509-board .action{font-size:14px!important}.naya509-board .ratingStar{width:42px!important;height:44px!important;font-size:28px!important}}
`;document.head.appendChild(s)}
function boot(){style();run();const b=document.querySelector('.blocks');if(b&&!b.dataset.nayaRealObserver){const mo=new MutationObserver(()=>{if(b.dataset.nayaRealRendering!=='1')run()});mo.observe(b,{childList:true});b.dataset.nayaRealObserver='1'}return !!b}
window.Naya509RealSmartFeed={boot,run,version:'final-boot-3'};
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
})();