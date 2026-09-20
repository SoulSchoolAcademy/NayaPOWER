(()=>{'use strict';
/* 509 C4 MICRO PATCH — preserve the beautiful unified board and original interaction model.
   Surgical fixes only: Love/Like local toggle/count, compact Personal visibility action,
   readable lower feed support bars/tagline. No new board, no redesign, no C5. */
const q=(s,r=document)=>r.querySelector(s),qq=(s,r=document)=>[...r.querySelectorAll(s)];
const tx=e=>(e?.innerText||e?.textContent||'').replace(/\s+/g,' ').trim();
const store='nayanet-509-social-counts-v1';
const read=()=>{try{return JSON.parse(localStorage.getItem(store)||'{}')}catch{return{}}};
const write=v=>{try{localStorage.setItem(store,JSON.stringify(v))}catch{}};
function key(block,kind,i){return (block.dataset.intelligenceId||block.id||`block-${i}`)+':'+kind}
function setActionText(el,kind,on){if(!el)return;el.textContent=kind==='love'?(on?'❤️ LOVE 1':'❤️ LOVE'):(on?'LIKE 1':'LIKE');el.setAttribute('aria-pressed',on?'true':'false');el.classList.toggle('on',on)}
function bindSocial(){
  const root=document.body;if(!root||root.dataset.naya509LoveLikePatch)return;root.dataset.naya509LoveLikePatch='1';
  root.addEventListener('click',e=>{
    const a=e.target.closest('[data-c4-kind="love"],[data-c4-kind="like"]');if(!a||!root.contains(a)||a.hidden)return;
    const block=a.closest('.block');if(!block)return;
    e.preventDefault();e.stopPropagation();e.stopImmediatePropagation();
    const k=a.dataset.c4Kind,i=qq('.block').indexOf(block),id=key(block,k,i),s=read(),on=!Boolean(s[id]);s[id]=on;write(s);setActionText(a,k,on);
  },true);
  qq('[data-c4-kind="love"],[data-c4-kind="like"]').forEach((a,i)=>{const b=a.closest('.block');const k=a.dataset.c4Kind;if(b&&k)setActionText(a,k,Boolean(read()[key(b,k,qq('.block').indexOf(b))]))});
}
function polishVisibility(){
  qq('.naya509-visibility,[data-c4-kind="make-public"]').forEach(b=>{b.style.minHeight='46px';b.style.padding='0 18px';b.style.fontSize='14px';b.style.maxWidth='260px';b.style.width='auto';b.style.alignSelf='flex-start'});
}
function findAndPolishText(){
  qq('body *').forEach(el=>{
    if(el.children.length>0)return;const t=tx(el);if(!t)return;
    if(/^INTELLIGENCE (CONTEXT|COLLECTIVE)$/i.test(t)){el.style.fontSize='14px';el.style.minHeight='44px';el.style.padding='0 14px';el.style.display='inline-flex';el.style.alignItems='center';el.style.fontWeight='900'}
    if(/Your life creates your intelligence every day/i.test(t)){el.style.fontSize='24px';el.style.lineHeight='1.45';el.style.fontWeight='650';el.style.color='#f0edf4'}
  });
}
function run(){bindSocial();polishVisibility();findAndPolishText()}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run);else run();
new MutationObserver(run).observe(document.documentElement,{childList:true,subtree:true});
})();
