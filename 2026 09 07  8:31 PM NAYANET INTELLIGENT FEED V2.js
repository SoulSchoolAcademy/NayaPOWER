/* NayaNET Intelligent Feed V2 — timestamped surgical presentation layer.
 * Preserves the existing Intelligent Block content model and upgrades presentation only.
 */
(function(){
  'use strict';
  const root=document.querySelector('.intelligentBlocks');
  if(!root || root.dataset.nayanetFeedV2==='1') return;
  root.dataset.nayanetFeedV2='1';
  const svg={
    nutshell:'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3v18M3 12h18"/><circle cx="12" cy="12" r="7"/></svg>',
    human:'<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="8" r="3.2"/><path d="M5.5 21c.7-4.2 3-6.3 6.5-6.3s5.8 2.1 6.5 6.3"/></svg>',
    child:'<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="8"/><circle cx="9" cy="10" r="1"/><circle cx="15" cy="10" r="1"/><path d="M8.5 14.5c1.8 1.5 5.2 1.5 7 0"/></svg>',
    grandma:'<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="9" r="4"/><path d="M6 21c.5-4 2.6-6 6-6s5.5 2 6 6M7 6c1.4-3.2 8.6-3.2 10 0"/></svg>',
    naya:'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8L12 3z"/><path d="M19 16l.8 2.2L22 19l-2.2.8L19 22l-.8-2.2L16 19l2.2-.8L19 16z"/></svg>',
    machine:'<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="4" y="5" width="16" height="14" rx="2"/><path d="M8 9h8M8 13h5M9 19v2M15 19v2"/><circle cx="8" cy="9" r=".7"/></svg>',
    lesson:'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3l7 4v5c0 4.2-2.4 7-7 9-4.6-2-7-4.8-7-9V7l7-4z"/><path d="M8.5 12l2.2 2.2 4.8-5"/></svg>'
  };
  const slots=[
    ['human','HUMAN NOTE','Your lived experience','magenta'],
    ['child','CHILD NOTE','The simplest human truth','purple'],
    ['grandma','GRANDMA NOTE','Wisdom that survives the jargon','indigo'],
    ['naya','NAYA NOTE','What Naya understands','sapphire'],
    ['machine','MACHINE NOTE','What the system can carry forward','emerald'],
    ['lesson','WHAT WE LEARNED · WHAT IT MEANS','The golden nugget','gold']
  ];
  const tones={red:'#ff4057',orange:'#ff8a3d',gold:'#e8c766',yellow:'#ffe45c',lime:'#a8e63f',forest:'#31c875',teal:'#29d4c4',sapphire:'#55b9ee',indigo:'#6675ff',purple:'#9a68ff',magenta:'#d86cff',white:'#f8f8f4'};
  const cycle=['red','orange','gold','yellow','lime','forest','teal','sapphire','indigo','purple','magenta','white'];
  const clean=t=>(t||'').replace(/\s+/g,' ').trim();
  const textOf=el=>clean(el?.innerText||el?.textContent||'');
  const esc=t=>String(t||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');
  document.head.insertAdjacentHTML('beforeend',`<style id="nayanet-intelligent-feed-v2-style">
  .intelligentBlocks.nayanet-feed-v2{display:block;position:relative}
  .nayanet-feed-v2 .intelligentBlock{--outer-tone:#d86cff;position:relative;margin:0 0 30px;padding:28px 28px 32px;border:1px solid color-mix(in srgb,var(--outer-tone) 78%,#fff 10%);border-radius:28px;background:linear-gradient(145deg,#0c0c12,#050507 62%,#0a080e);box-shadow:inset 0 1px 0 #fff7,0 24px 55px #000d,0 0 30px color-mix(in srgb,var(--outer-tone) 17%,transparent),0 0 85px color-mix(in srgb,var(--outer-tone) 7%,transparent);overflow:visible}
  .nayanet-feed-v2 .intelligentBlock:before{left:0;top:22px;bottom:22px;width:2px;background:linear-gradient(180deg,transparent,var(--outer-tone) 12%,var(--outer-tone) 88%,transparent);opacity:1;box-shadow:0 0 12px var(--outer-tone),0 0 32px color-mix(in srgb,var(--outer-tone) 65%,transparent)}
  .nayanet-feed-v2 .intelligentBlock:after{content:"";position:absolute;inset:0;border-radius:28px;pointer-events:none;background:radial-gradient(circle at 14% 0,color-mix(in srgb,var(--outer-tone) 13%,transparent),transparent 34%),radial-gradient(circle at 100% 100%,color-mix(in srgb,var(--outer-tone) 7%,transparent),transparent 35%)}
  .nayanet-feed-v2 .blockHeader,.nayanet-feed-v2 .blockBody,.nayanet-feed-v2 .perspectiveMap,.nayanet-feed-v2 .blockFooter{position:relative;z-index:1}
  .nayanet-feed-v2 .blockHeader{margin:0 0 20px;padding:0 4px 18px;border-bottom:1px solid #ffffff12}
  .nayanet-feed-v2 .blockGlyph{width:48px;height:48px;border-radius:15px;box-shadow:inset 0 1px #fff6,0 10px 25px #0009,0 0 22px color-mix(in srgb,var(--outer-tone) 30%,transparent)}
  .nayanet-feed-v2 .blockBody{margin:0 0 18px;padding:0;border:0}.nayanet-feed-v2 .blockBody:before{display:none!important}.nayanet-feed-v2 .blockBody p{display:none}
  .nayanet-nutshell{position:relative;margin:0 0 22px;padding:21px 22px 20px;border:1px solid #fff;border-radius:20px;background:linear-gradient(145deg,#18181b,#09090c 72%);box-shadow:inset 0 1px 0 #fff,0 10px 0 #030304,0 18px 30px #000c,0 0 25px #fff2;transform:translateY(-3px)}
  .nayanet-nutshell:after{content:"";position:absolute;left:18px;right:18px;top:-1px;height:1px;background:#fff;box-shadow:0 0 14px #fff,0 0 32px #fff8}
  .nayanet-nutshell-head{display:flex;align-items:center;gap:10px;margin-bottom:9px;color:#fff;font-size:7px;font-weight:1000;letter-spacing:.18em}.nayanet-nutshell-head .nayanet-mini-icon{width:27px;height:27px;border-radius:9px;display:grid;place-items:center;background:#fff;color:#050507;box-shadow:0 0 16px #fff5,0 6px 13px #0008}
  .nayanet-nutshell-head svg,.nayanet-perspective-icon svg{width:16px;height:16px;fill:none;stroke:currentColor;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round}.nayanet-nutshell p{margin:0;color:#fff;font-size:15px;line-height:1.58;letter-spacing:-.01em}
  .nayanet-perspectives{display:grid;gap:13px}.nayanet-perspective-card{--inner-tone:#55b9ee;position:relative;padding:18px 19px 19px;border:1px solid color-mix(in srgb,var(--inner-tone) 72%,#fff 4%);border-radius:19px;background:linear-gradient(145deg,#121218,#07070a 78%);box-shadow:inset 0 1px #fff4,0 10px 0 #030304,0 17px 27px #000b,0 0 22px color-mix(in srgb,var(--inner-tone) 13%,transparent);overflow:hidden}
  .nayanet-perspective-card:before{content:"";position:absolute;left:0;top:14px;bottom:14px;width:2px;border-radius:3px;background:var(--inner-tone);box-shadow:0 0 12px var(--inner-tone),0 0 25px color-mix(in srgb,var(--inner-tone) 65%,transparent)}.nayanet-perspective-card:after{content:"";position:absolute;inset:0;pointer-events:none;background:linear-gradient(115deg,color-mix(in srgb,var(--inner-tone) 7%,transparent),transparent 35%)}
  .nayanet-perspective-head,.nayanet-perspective-content{position:relative;z-index:1}.nayanet-perspective-head{display:flex;align-items:center;gap:11px;margin-bottom:10px}.nayanet-perspective-icon{width:35px;height:35px;border-radius:11px;display:grid;place-items:center;color:var(--inner-tone);background:color-mix(in srgb,var(--inner-tone) 11%,#07070a);border:1px solid color-mix(in srgb,var(--inner-tone) 52%,#fff 4%);box-shadow:inset 0 1px #fff4,0 7px 16px #0008,0 0 17px color-mix(in srgb,var(--inner-tone) 20%,transparent)}
  .nayanet-perspective-head b{font-size:8px;letter-spacing:.15em;color:#fff}.nayanet-perspective-head span{display:block;color:#77717d;font-size:7px;margin-top:3px}.nayanet-perspective-content{color:#dcd6e0;font-size:12px;line-height:1.62}.nayanet-perspective-content.empty{color:#77717f;font-style:italic}
  .nayanet-perspective-card.lesson{background:linear-gradient(145deg,#17150c,#08080a 78%);border-color:#e8c76688;box-shadow:inset 0 1px #fff7,0 10px 0 #030304,0 17px 30px #000b,0 0 28px #e8c76618,0 0 15px #fff1}.nayanet-perspective-card.lesson:before{background:linear-gradient(#fff,#e8c766);box-shadow:0 0 12px #fff,0 0 25px #e8c766}.nayanet-perspective-card.lesson .nayanet-perspective-icon{color:#17120a;background:linear-gradient(145deg,#fff,#e8c766);border-color:#fff;box-shadow:0 0 20px #e8c76655,0 0 10px #fff8}.nayanet-perspective-card.lesson .nayanet-perspective-content{color:#f1e6b8}
  .nayanet-feed-v2 .blockFooter{margin-top:22px;padding-top:13px}@media(max-width:700px){.nayanet-feed-v2 .intelligentBlock{padding:21px 14px 24px;border-radius:22px;margin-bottom:20px}.nayanet-feed-v2 .intelligentBlock:before{top:18px;bottom:18px}.nayanet-nutshell{padding:17px}.nayanet-nutshell p{font-size:14px}.nayanet-perspective-card{padding:15px}.nayanet-perspective-content{font-size:11px}}
  </style>`);
  function toneFor(index){return tones[cycle[index%cycle.length]]}
  function extractBlockText(block){const body=block.querySelector('.blockBody');const first=body?.querySelector('p');return clean(first?.innerText||first?.textContent||block.querySelector('.blockTitle h3')?.textContent||'')}
  function findExisting(block,key){
    const selectors=[`.perspective.${key}`,`[data-perspective="${key}"]`];for(const s of selectors){const el=block.querySelector(s);if(el)return textOf(el.querySelector('p')||el)}
    const all=[...block.querySelectorAll('.perspective')];const needles={human:['human'],child:['child'],grandma:['grandma','grandmother'],naya:['naya','ai'],machine:['machine'],lesson:['lesson','feed','learned','meaning']};const hit=all.find(el=>needles[key]?.some(n=>textOf(el).toLowerCase().includes(n)));return hit?textOf(hit.querySelector('p')||hit):'';
  }
  [...root.querySelectorAll(':scope > .intelligentBlock')].forEach((block,i)=>{
    block.style.setProperty('--outer-tone',toneFor(i));const oldMap=block.querySelector('.perspectiveMap');const nutshellText=extractBlockText(block);if(oldMap){
      const wrap=document.createElement('div');wrap.className='nayanet-perspective-v2-wrap';wrap.innerHTML=`<div class="nayanet-nutshell"><div class="nayanet-nutshell-head"><span class="nayanet-mini-icon">${svg.nutshell}</span><span>IN A NUTSHELL</span></div><p>${esc(nutshellText||'This intelligence event is still being distilled.')}</p></div><div class="nayanet-perspectives"></div>`;
      const grid=wrap.querySelector('.nayanet-perspectives');slots.forEach(([key,label,sub,tone])=>{const content=findExisting(block,key);const card=document.createElement('section');card.className='nayanet-perspective-card '+(key==='lesson'?'lesson':'');const toneMap={magenta:'#d86cff',purple:'#9a68ff',indigo:'#6675ff',sapphire:'#55b9ee',emerald:'#31c875',gold:'#e8c766'};card.style.setProperty('--inner-tone',toneMap[tone]);card.innerHTML=`<div class="nayanet-perspective-head"><span class="nayanet-perspective-icon">${svg[key]}</span><div><b>${label}</b><span>${sub}</span></div></div><div class="nayanet-perspective-content ${content?'':'empty'}">${esc(content||'Perspective not yet captured.')}</div>`;grid.appendChild(card)});oldMap.replaceWith(wrap);
    }
  });
})();
