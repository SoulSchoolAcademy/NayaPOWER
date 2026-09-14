(()=>{'use strict';
const q=(s,r=document)=>r.querySelector(s),qq=(s,r=document)=>[...r.querySelectorAll(s)];
const text=e=>(e?.innerText||e?.textContent||'').replace(/\s+/g,' ').trim().toLowerCase();
function cleanBlock(block){
  const a=q('.actions',block); if(!a)return;
  const all=qq('button,.naya509-rating',a);
  const seen={love:false,like:false,share:false,rate:false};
  all.forEach(el=>{
    if(el.classList.contains('naya509-rating')){
      if(seen.rate)el.remove(); else seen.rate=true;
      return;
    }
    const t=text(el),kind=el.dataset.c4Kind||'';
    if(kind==='favorite'||kind==='save'||/\bfavorite\b|\bsave\b/.test(t)){el.remove();return}
    if(kind==='rank'||/\brank\b/.test(t)){el.remove();return}
    if(kind==='love'||/love/.test(t)){
      if(seen.love){el.remove();return}
      seen.love=true;el.dataset.c4Kind='love';el.textContent='❤️ LOVE';el.classList.add('love');return;
    }
    if(kind==='like'||/like/.test(t)){
      if(seen.like){el.remove();return}
      seen.like=true;el.dataset.c4Kind='like';el.textContent='LIKE';el.classList.add('like');return;
    }
    if(kind==='share-intel'||/share\s*intel/.test(t)){
      if(seen.share){el.remove();return}
      seen.share=true;el.dataset.c4Kind='share-intel';el.textContent='＋ SHARE INTEL';return;
    }
    if(/\brate\b|rating|stars/.test(t)){el.remove();return}
  });
  if(!seen.love||!seen.like||!seen.rate||!seen.share)return;
  const love=q('[data-c4-kind="love"]',a),like=q('[data-c4-kind="like"]',a),rate=q('.naya509-rating',a),share=q('[data-c4-kind="share-intel"]',a);
  [love,like,rate,share].forEach(x=>{if(x)a.appendChild(x)});
  a.style.justifyContent='flex-end';
  if(share){share.style.marginLeft='0';share.setAttribute('aria-label','Share intelligence')}
}
function css(){if(q('#naya509-c4-action-cleanup-css'))return;const s=document.createElement('style');s.id='naya509-c4-action-cleanup-css';s.textContent=`
.naya509-board .actions{display:flex!important;justify-content:flex-end!important;align-items:center!important;gap:10px!important;flex-wrap:wrap!important}
.naya509-board .actions [data-c4-kind="love"],.naya509-board .actions [data-c4-kind="like"],.naya509-board .actions .naya509-rating,.naya509-board .actions [data-c4-kind="share-intel"]{flex:0 0 auto!important}
.naya509-board .actions [data-c4-kind="love"]{--action-color:#ff5e6c!important}
.naya509-board .actions [data-c4-kind="share-intel"]{margin-left:0!important}
@media(max-width:800px){.naya509-board .actions{justify-content:flex-start!important}.naya509-board .actions [data-c4-kind="share-intel"]{margin-left:auto!important}}
`;document.head.appendChild(s)}
function run(){css();qq('.block.naya509-board,.block').forEach(cleanBlock)}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run);else run();
setTimeout(run,700);setTimeout(run,1800);

/* 509 SMART FEED FINISH — preserve the approved note structure, fill the missing final layer,
   and remove the three obsolete demo blocks. Source is the canonical SMART FEED CONTENT file. */
const FEED_SOURCE='https://raw.githubusercontent.com/SoulSchoolAcademy/NayaPOWER/main/SMART%20FEED%20CONTENT';
const DEMO_TITLES=['Blockers Never Stop the Mission','Source Intent Is Not Runtime Truth','The Intelligent Block Is the Star'];
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const body=v=>esc(v).replace(/\r?\n/g,'<br>');
function removeDemoBlocks(){
  const blocks=q('.blocks'); if(!blocks)return false;
  qq('.block',blocks).forEach(b=>{const t=(q('h3',b)?.textContent||'').trim();if(DEMO_TITLES.includes(t))b.remove()});
  return true;
}
function parseHowToUse(source){
  const out={};
  const marks=[...source.matchAll(/🧠\s*NAYA POWER\s*[—-]\s*SMART NOTE\s*(\d+)/gi)];
  marks.forEach((m,i)=>{
    const n=Number(m[1]),chunk=source.slice(m.index,i+1<marks.length?marks[i+1].index:source.length);
    const hit=chunk.match(/(?:^|\n)10\.\s*HOW TO APPLY IT\s*\n([\s\S]*?)(?=\n11\.\s*WHAT'S IN IT FOR YOU\?|\n11\.\s*WHAT’S IN IT FOR YOU\?|\n={20,}|$)/i);
    if(hit&&hit[1].trim())out[n]=hit[1].trim();
  });
  return out;
}
function addHowToUse(map){
  const blocks=q('.blocks'); if(!blocks)return false;
  const real=qq('[data-real-smart-note]',blocks).filter(b=>b.dataset.realSmartNote||b.classList.contains('naya509-board'));
  if(real.length<9)return false;
  real.forEach(b=>{
    if(q('.naya509-how-to-use',b))return;
    const n=Number(b.getAttribute('data-real-smart-note'));const value=map[n];if(!value)return;
    let layers=q('.layers',b);if(!layers){layers=document.createElement('div');layers.className='layers';b.querySelector('.blockInner')?.appendChild(layers)}
    const layer=document.createElement('article');layer.className='layer naya509-how-to-use';layer.style.setProperty('--layer','var(--tone)');
    layer.innerHTML='<div class="layerHead"><span class="dot"></span><b>10 · HOW TO USE IT</b><span class="state">SMART NOTE · '+String(n).padStart(2,'0')+'</span></div><div class="layerBody">'+body(value)+'</div>';
    layers.appendChild(layer);
  });
  document.documentElement.dataset.naya509FeedFinished='true';
  document.documentElement.dataset.naya509RealSmartNoteCount=String(real.length);
  return true;
}
async function finishFeed(){
  removeDemoBlocks();
  const blocks=q('.blocks');if(!blocks)return false;
  if(blocks.dataset.naya509HowToMap==='ready'){removeDemoBlocks();return addHowToUse(window.__naya509HowToMap||{})}
  if(blocks.dataset.naya509HowToMap==='loading')return false;
  blocks.dataset.naya509HowToMap='loading';
  try{
    const r=await fetch(FEED_SOURCE,{cache:'no-store'});if(!r.ok)throw new Error('source '+r.status);
    const source=await r.text();const map=parseHowToUse(source);
    if(Object.keys(map).length<9)throw new Error('expected 9 HOW TO APPLY IT sections');
    window.__naya509HowToMap=map;blocks.dataset.naya509HowToMap='ready';
    removeDemoBlocks();return addHowToUse(map);
  }catch(e){blocks.dataset.naya509HowToMap='error';console.warn('[NAYA509-FEED-FINISH]',e);return false}
}
function bootFeed(){finishFeed();const blocks=q('.blocks');if(blocks&&!blocks.dataset.naya509FeedFinishObserver){const mo=new MutationObserver(()=>{removeDemoBlocks();if(blocks.dataset.naya509HowToMap==='ready')addHowToUse(window.__naya509HowToMap||{})});mo.observe(blocks,{childList:true,subtree:true});blocks.dataset.naya509FeedFinishObserver='1'}}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',bootFeed,{once:true});else bootFeed();
setTimeout(bootFeed,900);setTimeout(bootFeed,2200);setTimeout(bootFeed,4500);
})();