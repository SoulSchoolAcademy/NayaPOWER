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
})();