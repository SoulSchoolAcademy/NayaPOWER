(()=>{'use strict';
const q=(s,r=document)=>r.querySelector(s),qq=(s,r=document)=>[...r.querySelectorAll(s)];
const tx=e=>(e?.innerText||e?.textContent||'').replace(/\s+/g,' ').trim();
const mode=()=>{const b=q('.feedNav button.active');const t=tx(b).toLowerCase();return t.includes('personal')?'personal':t.includes('activity')?'activity':'collective'};
function cleanBlock(block){
  if(!block||!block.matches('.block'))return;
  block.classList.add('naya509-board');
  const a=q('.actions',block);if(!a)return;
  const all=qq('button,.naya509-rating',a),keep={love:null,like:null,rate:null,share:null};
  all.forEach(el=>{
    const t=tx(el).toLowerCase();
    if(el.classList.contains('naya509-rating')){if(keep.rate)el.remove();else keep.rate=el;return}
    if(/\bfavorite\b|\bsave\b|\brank\b/.test(t)){el.remove();return}
    if(/\blove\b/.test(t)){if(keep.love)el.remove();else{keep.love=el;el.dataset.c4Kind='love';el.classList.add('love');el.textContent='❤️ LOVE'}return}
    if(/\blike\b/.test(t)){if(keep.like)el.remove();else{keep.like=el;el.dataset.c4Kind='like';el.classList.add('like');el.textContent='LIKE'}return}
    if(/\bshare(?:\s+intel(?:ligence)?)?\b/.test(t)){if(keep.share)el.remove();else{keep.share=el;el.dataset.c4Kind='share-intel';el.textContent='＋ SHARE INTEL'}return}
    if(/\brate\b|rating|stars/.test(t))el.remove();
  });
  const m=mode();
  if(m!=='collective'){keep.love?.remove();keep.like?.remove();keep.rate?.remove();keep.love=null;keep.like=null;keep.rate=null}
  qq('.naya509-action-left,.naya509-action-center,.naya509-action-right',a).forEach(x=>x.remove());
  const left=document.createElement('div'),center=document.createElement('div'),right=document.createElement('div');
  left.className='naya509-action-left';center.className='naya509-action-center';right.className='naya509-action-right';
  if(m==='collective'){if(keep.love)left.append(keep.love);if(keep.like)left.append(keep.like);if(keep.rate)center.append(keep.rate)}
  if(keep.share)right.append(keep.share);
  a.append(left,center,right);a.classList.add('naya509-actions-structured');
}
function apply(){
  qq('.block').forEach(cleanBlock);
  qq('.layerHead b').forEach(e=>{const t=tx(e);if(/child view/i.test(t))e.textContent=t.replace(/child view/ig,'CHILD NOTE');if(/grabber view|grandma view/i.test(t))e.textContent=t.replace(/grabber view|grandma view/ig,'GRANDMA NOTE')});
}
function css(){if(q('#naya509-single-board-runtime-css'))return;const s=document.createElement('style');s.id='naya509-single-board-runtime-css';s.textContent=`
.naya509-unified-board{position:relative!important;margin:0 22px 28px!important;border:2px solid #8b63ff66!important;border-radius:30px!important;background:radial-gradient(900px 260px at 50% -8%,#9d75ff16,transparent 70%),linear-gradient(145deg,#0b0a10,#050507)!important;box-shadow:inset 0 1px #fff8,0 28px 70px #000c,0 0 45px #8b63ff14!important;overflow:hidden!important}
.naya509-unified-board>.blocks{display:grid!important;gap:14px!important;padding:0 14px 18px!important}
.naya509-unified-board>.blocks>.block.naya509-board{margin:0!important;padding:30px 30px 28px!important;border:2px solid color-mix(in srgb,var(--tone) 58%,#fff 18%)!important;border-radius:24px!important;background:linear-gradient(145deg,#0b0a10,#050507)!important;box-shadow:inset 0 1px #fff8,0 18px 40px #000a,0 0 26px color-mix(in srgb,var(--tone) 18%,transparent)!important}
.naya509-unified-board .layer{border-color:color-mix(in srgb,var(--tone) 48%,#fff 12%)!important;box-shadow:inset 0 1px #fff5,0 12px 28px #0008,0 0 20px color-mix(in srgb,var(--tone) 15%,transparent)!important}
.naya509-unified-board .layerBody{font-size:14px!important;line-height:1.72!important;color:#f0edf4!important}
.naya509-unified-board .layerBody *{font-size:14px!important;line-height:1.72!important}
.naya509-unified-board .nutshell p{font-size:18px!important;line-height:1.65!important;color:#f7f4f9!important;font-weight:500!important}
.naya509-unified-board .nutshell p *{font-size:18px!important}
.naya509-unified-board .layerHead b{font-size:18px!important}
.naya509-unified-board .meta,.naya509-unified-board .state,.naya509-unified-board .truth{font-size:14px!important}
.naya509-unified-board .actions.naya509-actions-structured{display:grid!important;grid-template-columns:minmax(0,1fr) auto minmax(0,1fr)!important;align-items:center!important;gap:12px!important;width:100%!important}
.naya509-action-left{display:flex;gap:10px;justify-content:flex-start;align-items:center;min-width:0}.naya509-action-center{display:flex;justify-content:center;align-items:center;min-width:0}.naya509-action-right{display:flex;justify-content:flex-end;align-items:center;min-width:0}
.naya509-actions-structured .action{min-height:56px!important;font-size:14px!important;padding:0 18px!important}.naya509-actions-structured [data-c4-kind="love"]{color:#fff!important;border-color:#ff3f52!important;background:linear-gradient(145deg,#391019,#09090d)!important;box-shadow:inset 0 1px #fff6,0 10px 22px #0009,0 0 22px #ff3f5233!important}.naya509-actions-structured [data-c4-kind="share-intel"]{margin-left:0!important}.naya509-actions-structured .naya509-rating button{min-width:50px!important;min-height:46px!important;font-size:20px!important}
@media(max-width:800px){.naya509-unified-board{margin:0 10px 20px!important;border-radius:23px!important}.naya509-unified-board>.blocks{padding:0 9px 12px!important}.naya509-unified-board>.blocks>.block.naya509-board{padding:25px 18px 24px!important;border-radius:21px!important}.naya509-unified-board .actions.naya509-actions-structured{grid-template-columns:1fr!important;gap:10px!important}.naya509-action-left{justify-content:flex-start}.naya509-action-center{justify-content:center}.naya509-action-right{justify-content:flex-end}.naya509-actions-structured .action{min-height:58px!important}}
`;document.head.appendChild(s)}
function boot(){css();apply();const root=q('.blocks');if(root){new MutationObserver(()=>{if(!window.__naya509Repairing){window.__naya509Repairing=true;queueMicrotask(()=>{apply();window.__naya509Repairing=false})}}).observe(root,{childList:true,subtree:true})}}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot);else boot();
})();