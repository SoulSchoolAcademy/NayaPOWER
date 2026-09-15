(()=>{'use strict';
const q=(s,r=document)=>r.querySelector(s),qq=(s,r=document)=>[...r.querySelectorAll(s)];
const H=s=>(s||'').replace(/\s+/g,' ').trim().toUpperCase();
function removeUnrequested(){
  const exact=new Set(['PROVIDENCE','TRUTH','PROTECTION']);
  qq('button,a,[role="button"]').forEach(el=>{if(exact.has(H(el.textContent)))el.remove()});
  const groups=[['SOURCE','UNDERSTAND','ACT','VERIFY','LEARN'],['WHAT','WHY','SO WHAT','FOR YOU']];
  qq('nav,section,div,header,footer').forEach(el=>{
    const t=H(el.textContent); if(t.length>240)return;
    for(const g of groups){if(g.every(x=>t.includes(x))){el.remove();break}}
  });
}
function style(){if(q('#naya509-smart-board-v9'))return;const s=document.createElement('style');s.id='naya509-smart-board-v9';s.textContent=`
.blocks{display:grid!important;grid-template-columns:minmax(0,1fr)!important;grid-auto-flow:row!important;gap:0!important;width:100%!important}
.block[data-real-smart-note].naya-feature-board-v2{width:calc(100% - 20px)!important;max-width:none!important;margin-left:10px!important;margin-right:10px!important}
.block[data-real-smart-note].naya-feature-board-v2 .blockInner{width:100%!important;max-width:none!important}
.block[data-real-smart-note].naya-feature-board-v2 .blockTop{position:relative!important;padding-top:12px!important}
.block[data-real-smart-note].naya-feature-board-v2 .naya-feature-actions{position:absolute!important;top:8px!important;left:auto!important;right:8px!important;display:flex!important;flex-direction:row!important;flex-wrap:nowrap!important;justify-content:flex-end!important;align-items:center!important;gap:9px!important;z-index:30!important}
.block[data-real-smart-note].naya-feature-board-v2 .naya-feature-actions .action{margin:0!important;min-height:50px!important;border-width:2px!important;background:linear-gradient(145deg,#16161d,#07070b)!important;box-shadow:inset 0 1px #fff8,0 10px 22px #000b!important}
.block[data-real-smart-note].naya-feature-board-v2 .naya-feature-actions .action[data-c4-kind="create-space"]{border-color:#9d75ffcc!important;color:#eadfff!important;box-shadow:inset 0 1px #fff9,0 0 20px #9d75ff55,0 10px 22px #000b!important}
.block[data-real-smart-note].naya-feature-board-v2 .naya-feature-actions .action[data-c4-kind="favorite"]{border-color:#f1d75acc!important;color:#fff5b5!important;box-shadow:inset 0 1px #fff9,0 0 20px #f1d75a55,0 10px 22px #000b!important}
.block[data-real-smart-note].naya-feature-board-v2 .naya-feature-actions .action[data-c4-kind="save"]{border-color:#55b9eecc!important;color:#d9f3ff!important;box-shadow:inset 0 1px #fff9,0 0 20px #55b9ee55,0 10px 22px #000b!important}
.block[data-real-smart-note].naya-feature-board-v2 .naya-feature-actions .action[data-c4-kind="create-space"]:hover{box-shadow:inset 0 1px #fff9,0 0 28px #9d75ff88,0 12px 25px #000c!important}
.block[data-real-smart-note].naya-feature-board-v2 .naya-feature-actions .action[data-c4-kind="favorite"]:hover{box-shadow:inset 0 1px #fff9,0 0 28px #f1d75a88,0 12px 25px #000c!important}
.block[data-real-smart-note].naya-feature-board-v2 .naya-feature-actions .action[data-c4-kind="save"]:hover{box-shadow:inset 0 1px #fff9,0 0 28px #55b9ee88,0 12px 25px #000c!important}
.block[data-real-smart-note].naya-feature-board-v2 .layer[data-feature-key]{width:100%!important;margin-left:0!important;margin-right:0!important}
.block[data-real-smart-note].naya-feature-board-v2 .layer[data-feature-key="human"]{--layer:#ff3bbf!important}
.block[data-real-smart-note].naya-feature-board-v2 .layer[data-feature-key="child"]{--layer:#9d75ff!important}
.block[data-real-smart-note].naya-feature-board-v2 .layer[data-feature-key="grandma"]{--layer:#6675ff!important}
.block[data-real-smart-note].naya-feature-board-v2 .layer[data-feature-key="naya"]{--layer:#c97a4a!important}
.block[data-real-smart-note].naya-feature-board-v2 .layer[data-feature-key="machine"]{--layer:#35d39a!important}
.block[data-real-smart-note].naya-feature-board-v2 .layer[data-feature-key="learning"]{--layer:#b8ee57!important}
.block[data-real-smart-note].naya-feature-board-v2 .layer[data-feature-key="meaning"]{--layer:#f1d75a!important}
.block[data-real-smart-note].naya-feature-board-v2 .layer[data-feature-key="apply"]{--layer:#e8c766!important}
.block[data-real-smart-note].naya-feature-board-v2 .layer[data-feature-key="benefit"]{--layer:#e9edf5!important}
@media(max-width:900px){.block[data-real-smart-note].naya-feature-board-v2{width:calc(100% - 10px)!important;margin-left:5px!important;margin-right:5px!important}.block[data-real-smart-note].naya-feature-board-v2 .naya-feature-actions{position:relative!important;top:auto!important;right:auto!important;justify-content:flex-end!important;margin:0 0 10px!important;flex-wrap:wrap!important}.block[data-real-smart-note].naya-feature-board-v2 .blockTop{padding-top:8px!important}}
`;document.head.appendChild(s)}
function normalize(){
  removeUnrequested();
  const blocks=qq('.block[data-real-smart-note]'); if(blocks.length!==9)return false;
  blocks.forEach(b=>{
    b.classList.add('naya-feature-board-v2');
    const acts=q('.naya509-board-actions',b);if(acts){const a=qq('.action',acts);['create-space','favorite','save'].forEach((k,i)=>{if(a[i])a[i].dataset.c4Kind=k})}
    const ns=qq('.nutshell',b);if(ns.length>1)ns.slice(1).forEach(x=>x.remove());
    const layers=q('.layers',b);if(layers){const order=['human','child','grandma','naya','machine','learning','meaning','apply','benefit'];[...layers.children].filter(x=>x.matches('.layer')).sort((a,z)=>order.indexOf(a.dataset.semanticLayer)-order.indexOf(z.dataset.semanticLayer)).forEach(x=>layers.appendChild(x))}
  });
  window.NAYA509_SMART_BOARD_V9='surgical-restoration+one-column+equal-board-width+lit-controls+unrequested-ui-removal';return true
}
style();normalize();[3000,7000,12000,17000,24000].forEach(ms=>setTimeout(()=>{style();normalize()},ms));
})();
