(()=>{'use strict';
const q=(s,r=document)=>r.querySelector(s),qq=(s,r=document)=>[...r.querySelectorAll(s)];
const text=e=>(e?.innerText||e?.textContent||'').replace(/\s+/g,' ').trim();
const OBSOLETE=['Blockers Never Stop the Mission','Source Intent Is Not Runtime Truth','The Intelligent Block Is the Star'];
const FEED_SOURCE='https://raw.githubusercontent.com/SoulSchoolAcademy/NayaPOWER/main/SMART%20FEED%20CONTENT';
function removeObsolete(){qq('.block').forEach(b=>{const t=text(q('h3',b));if(OBSOLETE.some(x=>t===x||t.includes(x)))b.remove()})}
function sidebar(){
  const rail=q('.rail');if(!rail)return;
  const els=qq('.nav button,.nav a,.rail button,.rail a',rail);
  const rename={
    'Home':'Your Intelligence',
    'Reports':'Your Reports',
    'Evidence':'Smart Ledger',
    'Collective':'Smart Share',
    'Connections':'Your Connections'
  };
  els.forEach(el=>{
    const t=text(el);
    if(/^Smart Notes$/i.test(t)){el.remove();return}
    if(/^Smart Mail\b.*\bNew\b/i.test(t)){el.remove();return}
    const key=Object.keys(rename).find(k=>new RegExp('^'+k+'$','i').test(t));
    if(key){
      const walker=document.createTreeWalker(el,NodeFilter.SHOW_TEXT);
      while(walker.nextNode()){
        const n=walker.currentNode;
        if(n.nodeValue.trim()===key){n.nodeValue=n.nodeValue.replace(key,rename[key]);break}
      }
      el.setAttribute('aria-label',rename[key]);
    }
  });
}
function parseHowToUse(src){const m=src.match(/(?:^|\n)\s*(?:10\s*[·.:)-]?\s*)?HOW TO APPLY IT\s*\n([\s\S]*?)(?=\n\s*(?:11\s*[·.:)-]?\s*)?BENEFITS\b|$)/i);return m?m[1].trim():''}
async function addHowToUse(){const blocks=qq('.block[data-real-smart-note="1"],.block[data-real-smart-note="2"],.block[data-real-smart-note="3"],.block[data-real-smart-note="4"],.block[data-real-smart-note="5"],.block[data-real-smart-note="6"],.block[data-real-smart-note="7"],.block[data-real-smart-note="8"],.block[data-real-smart-note="9"]');if(blocks.length!==9)return;if(q('.naya509-how-to-use',blocks[0]))return;let body='';try{const r=await fetch(FEED_SOURCE,{cache:'no-store'});if(r.ok)body=parseHowToUse(await r.text())}catch{}if(!body)body='Use this intelligence as a practical guide. Choose one action that fits your situation, apply it, observe the result, and improve from what you learn.';blocks.forEach(b=>{if(q('.naya509-how-to-use',b))return;const layers=q('.layers',b);if(!layers)return;const layer=document.createElement('section');layer.className='layer naya509-how-to-use';layer.innerHTML='<div class="layerHead"><span class="dot" style="--layer:var(--green)"></span><b>10 · HOW TO USE IT</b><span class="state">APPLICATION</span></div><div class="layerBody"></div>';q('.layerBody',layer).textContent=body;layers.appendChild(layer)})}
function run(){removeObsolete();sidebar();addHowToUse()}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run);else run();[400,1000,2000,4000].forEach(ms=>setTimeout(run,ms));
new MutationObserver(()=>{removeObsolete();sidebar();addHowToUse()}).observe(document.documentElement,{childList:true,subtree:true});
window.NAYA509_FEED_FINISH='2026-09-14-sidebar-canonical';
})();
