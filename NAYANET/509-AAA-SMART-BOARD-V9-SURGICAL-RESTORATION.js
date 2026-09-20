(()=>{'use strict';
const q=(s,r=document)=>r.querySelector(s),qq=(s,r=document)=>[...r.querySelectorAll(s)];
const H=s=>(s||'').replace(/\s+/g,' ').trim().toUpperCase();
function removeUnrequested(){
  const exact=new Set(['PROVIDENCE','TRUTH','PROTECTION']);
  qq('button,a,[role="button"]').forEach(el=>{if(exact.has(H(el.textContent)))el.remove()});
  const groups=[['SOURCE','UNDERSTAND','ACT','VERIFY','LEARN'],['WHAT','WHY','SO WHAT','FOR YOU']];
  qq('nav,section,div,header,footer').forEach(el=>{const t=H(el.textContent);if(t.length>240)return;for(const g of groups){if(g.every(x=>t.includes(x))){el.remove();break}}});
}
function style(){if(q('#naya509-smart-board-v9'))return;const s=document.createElement('style');s.id='naya509-smart-board-v9';s.textContent=`
.blocks{display:grid!important;grid-template-columns:minmax(0,1fr)!important;grid-template-rows:none!important;grid-auto-flow:row!important;grid-auto-columns:100%!important;gap:0!important;width:100%!important}
.block[data-real-smart-note].naya-feature-board-v2{display:block!important;box-sizing:border-box!important;width:calc(100% - 20px)!important;max-width:none!important;min-width:0!important;margin-left:10px!important;margin-right:10px!important}
.block[data-real-smart-note].naya-feature-board-v2 .blockInner{display:block!important;width:100%!important;max-width:none!important;min-width:0!important}
.block[data-real-smart-note].naya-feature-board-v2 .layers{display:flex!important;flex-direction:column!important;flex-wrap:nowrap!important;width:100%!important;min-width:0!important}
.block[data-real-smart-note].naya-feature-board-v2 .layer[data-feature-key]{display:block!important;box-sizing:border-box!important;width:100%!important;max-width:none!important;min-width:0!important;margin-left:0!important;margin-right:0!important;flex:0 0 auto!important}
.block[data-real-smart-note].naya-feature-board-v2 .blockTop{position:relative!important;padding-top:12px!important}
.block[data-real-smart-note].naya-feature-board-v2 .naya-feature-actions{position:absolute!important;top:8px!important;left:auto!important;right:8px!important;display:flex!important;flex-direction:row!important;flex-wrap:nowrap!important;justify-content:flex-end!important;align-items:center!important;gap:9px!important;z-index:30!important}
.block[data-real-smart-note].naya-feature-board-v2 .naya-feature-actions .action{margin:0!important;min-height:50px!important;border-width:2px!important;background:linear-gradient(145deg,#16161d,#07070b)!important;box-shadow:inset 0 1px #fff8,0 10px 22px #000b!important}
.block[data-real-smart-note].naya-feature-board-v2 .naya-feature-actions .action[data-c4-kind="create-space"]{border-color:#9d75ffcc!important;color:#eadfff!important;box-shadow:inset 0 1px #fff9,0 0 20px #9d75ff55,0 10px 22px #000b!important}
.block[data-real-smart-note].naya-feature-board-v2 .naya-feature-actions .action[data-c4-kind="favorite"]{border-color:#f1d75acc!important;color:#fff5b5!important;box-shadow:inset 0 1px #fff9,0 0 20px #f1d75a55,0 10px 22px #000b!important}
.block[data-real-smart-note].naya-feature-board-v2 .naya-feature-actions .action[data-c4-kind="save"]{border-color:#55b9eecc!important;color:#d9f3ff!important;box-shadow:inset 0 1px #fff9,0 0 20px #55b9ee55,0 10px 22px #000b!important}
.block[data-real-smart-note].naya-feature-board-v2 .naya-feature-actions .action[data-c4-kind="create-space"]:hover{box-shadow:inset 0 1px #fff9,0 0 28px #9d75ff88,0 12px 25px #000c!important}
.block[data-real-smart-note].naya-feature-board-v2 .naya-feature-actions .action[data-c4-kind="favorite"]:hover{box-shadow:inset 0 1px #fff9,0 0 28px #f1d75a88,0 12px 25px #000c!important}
.block[data-real-smart-note].naya-feature-board-v2 .naya-feature-actions .action[data-c4-kind="save"]:hover{box-shadow:inset 0 1px #fff9,0 0 28px #55b9ee88,0 12px 25px #000c!important}
.block[data-real-smart-note].naya-feature-board-v2 .layerIcon{position:relative!important;display:grid!important;place-items:center!important}
.block[data-real-smart-note].naya-feature-board-v2 .layerIcon svg{width:28px!important;height:28px!important;filter:drop-shadow(0 3px 3px #000c)!important}
@media(max-width:900px){.block[data-real-smart-note].naya-feature-board-v2{width:calc(100% - 10px)!important;margin-left:5px!important;margin-right:5px!important}.block[data-real-smart-note].naya-feature-board-v2 .naya-feature-actions{position:relative!important;top:auto!important;right:auto!important;justify-content:flex-end!important;margin:0 0 10px!important;flex-wrap:wrap!important}.block[data-real-smart-note].naya-feature-board-v2 .blockTop{padding-top:8px!important}}
`;document.head.appendChild(s)}
function normalize(){
  removeUnrequested();
  const blocks=qq('.block[data-real-smart-note]');if(blocks.length!==9)return false;
  const order=['human','child','grandma','naya','machine','learning','meaning','apply','benefit'];
  blocks.forEach(b=>{
    b.classList.add('naya-feature-board-v2');
    const acts=q('.naya509-board-actions',b);if(acts){const a=qq('.action',acts);['create-space','favorite','save'].forEach((k,i)=>{if(a[i])a[i].dataset.c4Kind=k})}
    const ns=qq('.nutshell',b);if(ns.length>1)ns.slice(1).forEach(x=>x.remove());
    const layers=q('.layers',b);if(layers){const els=[...layers.children].filter(x=>x.matches('.layer'));els.sort((a,z)=>order.indexOf(a.dataset.semanticLayer)-order.indexOf(z.dataset.semanticLayer));els.forEach(x=>layers.appendChild(x));const ap=q('.layer[data-semantic-layer="apply"]',b),be=q('.layer[data-semantic-layer="benefit"]',b);if(ap&&be&&ap.parentElement===be.parentElement)be.parentElement.insertBefore(ap,be)}
  });
  window.NAYA509_SMART_BOARD_V9='surgical-restoration+one-column+equal-board-width+lit-controls+late-order-lock+unrequested-ui-removal';return true
}
style();normalize();
let ticks=0;const settle=setInterval(()=>{style();normalize();if(++ticks>=120)clearInterval(settle)},250);
})();
