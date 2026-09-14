/* NayaNET 509 AAA — NINE CANONICAL SMART NOTE PARSER
 * Surgical source adapter. The canonical SMART FEED CONTENT file contains
 * the first three notes with SMART NOTE headings and notes 4–9 with the
 * established #4/#6/#7/#8/#9 subject markers. This layer normalizes those
 * existing source identities into exactly nine Smart Feed boards.
 */
(()=>{'use strict';
const PAYLOAD='__SMART_FEED_B64__';
if(!PAYLOAD||PAYLOAD==='__SMART_FEED_B64__')return;
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const body=t=>esc(t).replace(/\n/g,'<br>');
function decode(){try{return decodeURIComponent(escape(atob(PAYLOAD)))}catch(_){try{return atob(PAYLOAD)}catch(e){return''}}}
const source=decode();if(!source)return;
const tones=['#ffffff','#ff4fd8','#d86cff','#9d75ff','#55b9ee','#55e39a','#b8ee57','#e8c766','#ff5e6c'];
const glyphs=['◈','✦','◇','◉','✧','◆','⬢','✺','✦'];
const markers=[
 {n:1,re:/^🧠\s*NAYA\s+POWER\s*[—-]\s*SMART\s+NOTE\s*01\b/im,title:'Naya Power'},
 {n:2,re:/^🧠\s*NAYA\s+POWER\s*[—-]\s*SMART\s+NOTE\s*02\b/im,title:'Naya'},
 {n:3,re:/^🧠\s*NAYA\s+POWER\s*[—-]\s*SMART\s+NOTE\s*03\b/im,title:'Smart Notes'},
 {n:4,re:/^🧠\s*#4\s*[—-]\s*YOUR\s+INTELLIGENCE\s+TODAY\s*$/im,title:'Your Intelligence Today'},
 {n:6,re:/^Naya\s+Power\s*#06\s*[—-]\s*What\s+Is\s+the\s+Intelligent\s+Library\?/im,title:'Intelligent Library'},
 {n:7,re:/^07\s*[—-]\s*SMART\s+LISTS\s*$/im,title:'Smart Lists'},
 {n:8,re:/^08\s*[—-]\s*INTELLIGENT\s+FEED\s*\/\s*SMART\s+FEED\s*$/im,title:'Intelligent Feed / Smart Feed'},
 {n:9,re:/^09\s*[—-]\s*SMART\s+TABS\s*$/im,title:'Smart Tabs'}
];
function pos(re,from=0){const s=source.slice(from),m=s.match(re);return m?from+m.index:-1}
function parseSections(text){
 const sections={};
 const re=/(?:^|\n)\s*(\d+)\.\s*([^\n]+)\n([\s\S]*?)(?=\n\s*\d+\.\s|$)/g;let m;
 while((m=re.exec(text)))sections[Number(m[1])]={name:m[2].trim(),text:m[3].trim()};
 return sections;
}
function cleanChunk(chunk,n,title){
 let rest=chunk.trim();
 if(n<=3){const lines=rest.split(/\r?\n/);while(lines.length){const x=(lines[0]||'').trim();if(!x){lines.shift();continue}if(/^🧠\s*NAYA\s+POWER/i.test(x)){lines.shift();continue}if(n===1||n===2||n===3){if(n===1&&/^What\s+Is\s+Naya\s+Power\?/i.test(x)){lines.shift();continue}if(n===2&&/^What\s+Is\s+Naya\?/i.test(x)){lines.shift();continue}if(n===3&&/^What\s+Are\s+Smart\s+Notes\?/i.test(x)){lines.shift();continue}}break}rest=lines.join('\n')}
 if(n===6){rest=rest.replace(/^Status:[^\n]*\n?/im,'').replace(/^Date:[^\n]*\n?/im,'').replace(/^Subject:[^\n]*\n?/im,'').replace(/^Smart Note Type:[^\n]*\n?/im,'').replace(/^Naya\s+Power\s*#06[^\n]*\n?/im,'')}
 return {number:n,title,sections:parseSections(rest)};
}
function parse(){
 const found=[];
 for(const m of markers){const p=pos(m.re);if(p>=0)found.push({...m,p})}
 found.sort((a,b)=>a.p-b.p);
 // Note 5 is the established Intelligence Reports block between the #4 block and #6 marker.
 const note5Start=found.find(x=>x.n===4)?.p;
 const p6=found.find(x=>x.n===6)?.p;
 const ranges=[];
 for(let i=0;i<found.length;i++){const a=found[i],b=found[i+1];if(a.n===4&&p6>=0){
     const chunk4=source.slice(a.p,p6);
     const split=chunk4.search(/\n[-_]{20,}\s*\n\s*1\.\s*IN A NUTSHELL\s*\n\s*Intelligence Reports\b/i);
     if(split>0){ranges.push([4,a.p,a.p+split]);ranges.push([5,a.p+split,p6])}else ranges.push([4,a.p,p6]);
   } else if(a.n!==4){ranges.push([a.n,a.p,b?b.p:source.length])}
 }
 const out=[];
 for(const [n,a,b] of ranges){let chunk=source.slice(a,b);const meta=markers.find(x=>x.n===n);if(!meta)continue;let title=meta.title;if(n===5)title='Intelligence Reports';out.push(cleanChunk(chunk,n,title))}
 return out.sort((a,b)=>a.number-b.number);
}
function actions(){return `<div class="actions" role="group" aria-label="Intelligence actions"><button class="action create" type="button" data-c4-kind="create-space">＋ CREATE SPACE</button><button class="action favorite" type="button" data-c4-kind="favorite">★ FAVORITE</button><button class="action save" type="button" data-c4-kind="save">SAVE</button><button class="action love" type="button" data-c4-kind="love" aria-pressed="false">❤️ LOVE</button><button class="action like" type="button" data-c4-kind="like" aria-pressed="false">LIKE</button><span class="naya509-rating" data-c4-kind="rating" role="group" aria-label="Rate this intelligence"><span class="ratingLabel">RATE THIS INTELLIGENCE</span><span class="ratingStars">${[1,2,3,4,5].map(n=>`<button type="button" class="ratingStar" data-rating="${n}" aria-label="Rate ${n} out of 5">★</button>`).join('')}</span></span><button class="action share" type="button" data-c4-kind="share-intel">＋ SHARE INTEL</button></div>`}
function board(note,idx){const tone=tones[idx],nums=Object.keys(note.sections).map(Number).sort((a,b)=>a-b),nuts=note.sections[1];const layers=nums.filter(n=>n!==1).map(n=>{const s=note.sections[n];return `<article class="layer" style="--layer:${tone}"><div class="layerHead"><span class="dot"></span><b>${esc(s.name)}</b><span class="state">SMART NOTE · ${String(note.number).padStart(2,'0')}</span></div><div class="layerBody">${body(s.text)}</div></article>`}).join('');return `<article class="block naya509-board" data-real-smart-note="${note.number}" data-intelligence-id="smart-note-${String(note.number).padStart(2,'0')}" style="--tone:${tone}"><div class="blockInner"><div class="blockTop"><div class="identity"><div class="glyph">${glyphs[idx]}</div><div><h3>${esc(note.title)}</h3><div class="meta"><span>SMART NOTE ${String(note.number).padStart(2,'0')}</span><span>CANONICAL INTELLIGENCE</span></div></div></div><div class="truth">SOURCE CONTENT</div></div>${nuts?`<div class="nutshell"><b>IN A NUTSHELL</b><p>${body(nuts.text)}</p></div>`:''}<div class="layers">${layers}</div>${actions()}<div class="blockFoot"><span>REAL SMART NOTE CONTENT · SOURCE: SMART FEED CONTENT</span><span>INTELLIGENCE EVENT ${String(note.number).padStart(2,'0')}</span></div></div></article>`}
function boot(){const blocks=document.querySelector('.blocks');if(!blocks)return false;const notes=parse();if(notes.length!==9||notes.some((n,i)=>n.number!==i+1))return false;const sig=notes.map(n=>`${n.number}:${n.title}`).join('|');if(blocks.dataset.nayaRealNineSignature!==sig||blocks.querySelectorAll('[data-real-smart-note]').length!==9){blocks.dataset.nayaRealRendering='1';blocks.innerHTML=notes.map(board).join('');blocks.dataset.nayaRealNineSignature=sig;blocks.dataset.nayaRealRendering='0'}document.documentElement.dataset.nayaRealSmartNoteCount='9';return true}
window.Naya509NineNoteParser={boot,parse,version:'1.0'};
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
})();