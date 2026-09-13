(()=>{'use strict';
/* 509 C4 INTERACTION CONTINUITY — surgical repair only.
   Law: preserve the existing C3/C4 DOM, listeners, local state and visual architecture.
   This layer never removes, recreates, or reparents interactive controls.
*/
const q=(s,r=document)=>r.querySelector(s),qq=(s,r=document)=>[...r.querySelectorAll(s)];
const tx=e=>(e?.innerText||e?.textContent||'').replace(/\s+/g,' ').trim();
const kind=e=>{if(!e)return'';const k=e.dataset?.c4Kind||e.dataset?.c3Kind||'';if(k)return k;const t=tx(e).toLowerCase();if(/create\s+space/.test(t))return'create-space';if(/favorite/.test(t))return'favorite';if(/^save$|\bsave\b/.test(t))return'save';if(/love/.test(t))return'love';if(/like/.test(t))return'like';if(/share/.test(t))return'share-intel';if(/rate|rating|stars/.test(t))return'rate';return''};
const mode=()=>{const b=q('.feedNav button.active');const t=tx(b).toLowerCase();return t.includes('personal')?'personal':t.includes('activity')?'activity':'collective'};
function markLabels(){qq('.layerHead b').forEach(e=>{const t=tx(e);if(/child view/i.test(t))e.textContent=t.replace(/child view/ig,'CHILD NOTE');if(/grabber view|grandma view/i.test(t))e.textContent=t.replace(/grabber view|grandma view/ig,'GRANDMA NOTE')})}
function hideDuplicates(){qq('.block').forEach(block=>{
  const seen={};
  qq('.actions [data-c4-kind],.actions .action,.actions .naya509-rating',block).forEach(el=>{
    const k=kind(el);if(!k)return;
    if(!seen[k]){seen[k]=el;el.hidden=false;return}
    /* Preserve the original node and its listeners; only hide the duplicate. */
    el.hidden=true;
  });
})}
function applyMode(){
  const m=mode();
  document.documentElement.dataset.naya509FeedMode=m;
  qq('.block').forEach((block,i)=>{
    block.classList.add('naya509-board');
    if(!block.style.getPropertyValue('--tone'))block.style.setProperty('--tone',['#9d75ff','#6675ff','#55b9ee','#55e39a','#b8ee57','#f1d75a','#e8c766','#ff9a5a','#ff5e6c','#f8f7fb','#f29ad8','#f15bd6','#d86cff'][i%13]);
    const actions=q('.actions',block);if(!actions)return;
    const love=q('[data-c4-kind="love"]',actions),like=q('[data-c4-kind="like"]',actions),rating=q('.naya509-rating',actions),share=q('[data-c4-kind="share-intel"]',actions);
    if(love)love.hidden=m!=='collective';
    if(like)like.hidden=m!=='collective';
    if(rating)rating.hidden=m!=='collective';
    if(share)share.hidden=false;
  });
  hideDuplicates();
  const h=q('.feedHead h2');const active=q('.feedNav button.active');if(h&&active)h.textContent=tx(active)||h.textContent;
  const count=q('.feedCount');if(count)count.setAttribute('data-mode',m);
}
function switchMode(button){
  const nav=q('.feedNav');if(!nav||!button)return;
  const buttons=qq('button',nav);
  const already=button.classList.contains('active');
  /* The original tab pathway can invoke the old loading/wait route. The same-board contract
     requires a local mode presentation instead; no navigation and no page reload. */
  if(already){
    applyMode();
    return;
  }
  buttons.forEach(b=>{const on=b===button;b.classList.toggle('active',on);b.setAttribute('aria-selected',on?'true':'false');b.setAttribute('tabindex',on?'0':'-1')});
  applyMode();
}
function bindTabs(){
  const nav=q('.feedNav');if(!nav||nav.dataset.naya509InteractionContinuity)return;
  nav.dataset.naya509InteractionContinuity='1';
  nav.addEventListener('click',e=>{
    const b=e.target.closest('button');if(!b||!nav.contains(b))return;
    e.preventDefault();
    e.stopPropagation();
    e.stopImmediatePropagation();
    switchMode(b);
  },true);
  nav.addEventListener('keydown',e=>{
    if(!['ArrowRight','ArrowLeft','Home','End'].includes(e.key))return;
    const bs=qq('button',nav),current=Math.max(0,bs.indexOf(document.activeElement));let n=current;
    if(e.key==='ArrowRight')n=(current+1)%bs.length;if(e.key==='ArrowLeft')n=(current-1+bs.length)%bs.length;if(e.key==='Home')n=0;if(e.key==='End')n=bs.length-1;
    e.preventDefault();bs[n]?.focus();
  },true);
}
function css(){if(q('#naya509-c4-interaction-continuity-css'))return;const s=document.createElement('style');s.id='naya509-c4-interaction-continuity-css';s.textContent=`
/* Existing C4 nodes stay in place; CSS supplies presentation only. */
.naya509-unified-board .actions.naya509-actions-structured,.naya509-unified-board .actions{display:grid!important;grid-template-columns:minmax(0,1fr) auto minmax(0,1fr)!important;align-items:center!important;gap:12px!important;width:100%!important}
.naya509-unified-board .actions [data-c4-kind="love"],.naya509-unified-board .actions [data-c4-kind="like"]{grid-column:1;justify-self:start}
.naya509-unified-board .actions [data-c4-kind="love"]{order:1}.naya509-unified-board .actions [data-c4-kind="like"]{order:2}
.naya509-unified-board .actions .naya509-rating{grid-column:2;grid-row:1;justify-self:center;order:3}
.naya509-unified-board .actions [data-c4-kind="share-intel"]{grid-column:3;grid-row:1;justify-self:end;order:4}
.naya509-unified-board .actions .action[hidden],.naya509-unified-board .actions .naya509-rating[hidden]{display:none!important}
.naya509-unified-board .actions [data-c4-kind="love"]{color:#fff!important;border-color:#ff3f52!important;background:linear-gradient(145deg,#391019,#09090d)!important;box-shadow:inset 0 1px #fff6,0 10px 22px #0009,0 0 22px #ff3f5233!important}
.naya509-unified-board .actions [data-c4-kind="love"].on{background:linear-gradient(145deg,#651522,#16070b)!important;border-color:#ff7b89!important;color:#fff!important}
.naya509-unified-board .actions [data-c4-kind="like"].on{border-color:#7ed0ff!important;color:#d9f2ff!important;background:#0b1822!important}
.naya509-unified-board .naya509-rating button:hover,.naya509-unified-board .naya509-rating button.on{color:#fff3a6!important;border-color:#f8e7a0!important;background:#2a230f!important;text-shadow:0 0 14px #f4d97899!important}
@media(max-width:800px){.naya509-unified-board .actions{grid-template-columns:1fr!important}.naya509-unified-board .actions [data-c4-kind="love"],.naya509-unified-board .actions [data-c4-kind="like"]{grid-column:1;justify-self:start}.naya509-unified-board .actions .naya509-rating{grid-column:1;grid-row:auto;justify-self:center}.naya509-unified-board .actions [data-c4-kind="share-intel"]{grid-column:1;grid-row:auto;justify-self:end}}
@media(prefers-reduced-motion:reduce){.naya509-unified-board .actions *{transition:none!important}}
`;
document.head.appendChild(s)}
function boot(){css();markLabels();bindTabs();applyMode();}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot);else boot();
})();
// 509 C4 interaction continuity: no interactive-node reconstruction; same Intelligence Board, local mode switching, original C4 behavior preserved.
