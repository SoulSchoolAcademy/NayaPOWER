/* NayaNET Intelligent Feed V2 — 2026-09-07 10:00 PM
 * Surgical presentation evolution.
 * Preserves the existing Intelligent Block model and content, while making the
 * intelligence easier to read, more dimensional, and more obviously reusable.
 */
(function(){
  'use strict';
  const root=document.querySelector('.intelligentBlocks');
  if(!root || root.dataset.nayanetFeedV2==='1') return;
  root.dataset.nayanetFeedV2='1';

  const icons={
    nutshell:'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3v18M3 12h18"/><circle cx="12" cy="12" r="7"/></svg>',
    human:'<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="7" r="3"/><path d="M5.5 21c.8-4.1 3-6.2 6.5-6.2s5.7 2.1 6.5 6.2"/></svg>',
    child:'<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="11" r="7.5"/><circle cx="9.2" cy="10" r=".8"/><circle cx="14.8" cy="10" r=".8"/><path d="M9 13.5c1.7 1.3 4.3 1.3 6 0"/></svg>',
    grandma:'<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="9" r="4"/><path d="M6 21c.6-4 2.7-6 6-6s5.4 2 6 6M7.2 7.1c.7-3.9 8.9-3.9 9.6 0"/><path d="M8.1 9h2.2M13.7 9h2.2M10.3 9h3.4"/></svg>',
    naya:'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.8l1.8 6L20 10.6l-6.2 1.8L12 18.5l-1.8-6.1L4 10.6l6.2-1.8L12 2.8z"/><path d="M19 16.2l.8 2.1 2.1.8-2.1.8-.8 2.1-.8-2.1-2.1-.8 2.1-.8.8-2.1z"/></svg>',
    machine:'<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="5" y="5" width="14" height="14" rx="2"/><path d="M9 9h6M9 13h4M9 19v2M15 19v2M3 9h2M3 15h2M19 9h2M19 15h2M9 3v2M15 3v2"/></svg>',
    lesson:'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 5.5A2.5 2.5 0 0 1 7.5 3H20v16H7.5A2.5 2.5 0 0 0 5 21V5.5z"/><path d="M5 5.5V21M9 7h7M9 11h7M9 15h5"/></svg>',
    heart:'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.8 8.9c0 5.4-8.8 10.3-8.8 10.3S3.2 14.3 3.2 8.9A4.6 4.6 0 0 1 12 6.5a4.6 4.6 0 0 1 8.8 2.4z"/></svg>'
  };

  const tones={
    red:'#ff4057',orange:'#ff8a3d',gold:'#e8c766',yellow:'#ffe45c',lime:'#a8e63f',
    forest:'#31c875',teal:'#29d4c4',sapphire:'#55b9ee',indigo:'#6675ff',purple:'#9a68ff',
    magenta:'#d86cff',white:'#f8f8f4'
  };
  const cycle=['red','orange','gold','yellow','lime','forest','teal','sapphire','indigo','purple','magenta','white'];
  const clean=t=>(t||'').replace(/\s+/g,' ').trim();
  const textOf=el=>clean(el?.innerText||el?.textContent||'');
  const esc=t=>String(t||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');

  document.head.insertAdjacentHTML('beforeend',`<style id="nayanet-intelligent-feed-v2-style">
  .intelligentBlocks.nayanet-feed-v2{display:block;position:relative}
  .nayanet-feed-v2 .intelligentBlock{--outer-tone:#d86cff;position:relative;margin:0 0 30px;padding:32px 34px 30px;border:1px solid color-mix(in srgb,var(--outer-tone) 82%,#fff 10%);border-radius:28px;background:#000!important;box-shadow:inset 0 1px 0 #fff8,0 28px 62px #000e,0 0 34px color-mix(in srgb,var(--outer-tone) 20%,transparent),0 0 90px color-mix(in srgb,var(--outer-tone) 8%,transparent);overflow:visible}
  .nayanet-feed-v2 .intelligentBlock:before{left:0;top:20px;bottom:20px;width:2px;background:linear-gradient(180deg,transparent,var(--outer-tone) 12%,var(--outer-tone) 88%,transparent);opacity:1;box-shadow:0 0 13px var(--outer-tone),0 0 34px color-mix(in srgb,var(--outer-tone) 65%,transparent)}
  .nayanet-feed-v2 .intelligentBlock:after{content:"";position:absolute;inset:0;border-radius:28px;pointer-events:none;background:radial-gradient(circle at 14% 0,color-mix(in srgb,var(--outer-tone) 11%,transparent),transparent 32%),radial-gradient(circle at 100% 100%,color-mix(in srgb,var(--outer-tone) 6%,transparent),transparent 35%)}
  .nayanet-feed-v2 .blockHeader,.nayanet-feed-v2 .blockBody,.nayanet-feed-v2 .perspectiveMap,.nayanet-feed-v2 .blockFooter{position:relative;z-index:1}
  .nayanet-feed-v2 .blockHeader{margin:0 0 20px;padding:0 2px 18px;border-bottom:1px solid #ffffff20}
  .nayanet-feed-v2 .blockIdentity{gap:16px}
  .nayanet-feed-v2 .blockGlyph{width:52px;height:52px;border-radius:16px;box-shadow:inset 0 1px #fff7,0 12px 28px #000a,0 0 24px color-mix(in srgb,var(--outer-tone) 32%,transparent)}
  .nayanet-feed-v2 .blockGlyph svg{width:25px;height:25px;fill:none;stroke:#fff;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
  .nayanet-feed-v2 .blockTitle h3{font-size:clamp(34px,4vw,58px);line-height:.98;color:#fff;letter-spacing:-.065em;margin:0 0 9px}
  .nayanet-feed-v2 .blockMeta,.nayanet-feed-v2 .blockMeta *{color:#fff!important}
  .nayanet-feed-v2 .blockBody{margin:0 0 20px;padding:0;border:0}.nayanet-feed-v2 .blockBody:before{display:none!important}.nayanet-feed-v2 .blockBody p{display:none}
  .nayanet-nutshell{position:relative;margin:0 0 24px;padding:24px 25px 23px;border:1px solid #fff;border-radius:21px;background:#000!important;box-shadow:inset 0 1px 0 #fff,0 11px 0 #000,0 20px 34px #000e,0 0 28px #fff2;transform:translateY(-2px)}
  .nayanet-nutshell:after{content:"";position:absolute;left:20px;right:20px;top:-1px;height:1px;background:#fff;box-shadow:0 0 15px #fff,0 0 34px #fff9}
  .nayanet-nutshell-head{display:flex;align-items:center;gap:11px;margin-bottom:11px;color:#fff!important;font-size:10px;font-weight:1000;letter-spacing:.18em}.nayanet-nutshell-head .nayanet-mini-icon{width:30px;height:30px;border-radius:10px;display:grid;place-items:center;background:#fff;color:#000;box-shadow:0 0 17px #fff5,0 7px 15px #000a}
  .nayanet-nutshell-head svg,.nayanet-perspective-icon svg,.nayanet-share svg{width:17px;height:17px;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
  .nayanet-nutshell p{margin:0!important;color:#fff!important;font-size:20px!important;line-height:1.55!important;letter-spacing:-.015em;max-width:1000px}
  .nayanet-perspectives{display:grid;gap:14px}.nayanet-perspective-card{--inner-tone:#55b9ee;position:relative;padding:21px 22px 22px;border:1px solid color-mix(in srgb,var(--inner-tone) 78%,#fff 4%);border-radius:20px;background:#000!important;box-shadow:inset 0 1px #fff5,0 11px 0 #000,0 18px 30px #000d,0 0 24px color-mix(in srgb,var(--inner-tone) 14%,transparent);overflow:hidden}
  .nayanet-perspective-card:before{content:"";position:absolute;left:0;top:14px;bottom:14px;width:3px;border-radius:3px;background:var(--inner-tone);box-shadow:0 0 13px var(--inner-tone),0 0 27px color-mix(in srgb,var(--inner-tone) 65%,transparent)}
  .nayanet-perspective-card:after{content:"";position:absolute;inset:0;pointer-events:none;background:linear-gradient(115deg,color-mix(in srgb,var(--inner-tone) 5%,transparent),transparent 34%)}
  .nayanet-perspective-head,.nayanet-perspective-content{position:relative;z-index:1}.nayanet-perspective-head{display:flex;align-items:center;gap:12px;margin-bottom:11px}.nayanet-perspective-icon{width:38px;height:38px;border-radius:12px;display:grid;place-items:center;color:var(--inner-tone);background:#000;border:1px solid color-mix(in srgb,var(--inner-tone) 58%,#fff 4%);box-shadow:inset 0 1px #fff5,0 8px 17px #000a,0 0 18px color-mix(in srgb,var(--inner-tone) 22%,transparent)}
  .nayanet-perspective-head b,.nayanet-perspective-head span,.nayanet-perspective-content{color:#fff!important}.nayanet-perspective-head b{font-size:11px;letter-spacing:.14em}.nayanet-perspective-head span{display:block;font-size:8px;margin-top:3px;opacity:.75}.nayanet-perspective-content{font-size:16px;line-height:1.7}.nayanet-perspective-content.empty{opacity:.55;font-style:italic}
  .nayanet-perspective-card.lesson{background:#000!important;border-color:#e8c76688;box-shadow:inset 0 1px #fff8,0 11px 0 #000,0 18px 32px #000d,0 0 28px #e8c7661c}.nayanet-perspective-card.lesson:before{background:linear-gradient(#fff,#e8c766);box-shadow:0 0 13px #fff,0 0 26px #e8c766}.nayanet-perspective-card.lesson .nayanet-perspective-icon{color:#fff;background:#000;border-color:#e8c766}.nayanet-perspective-card.lesson .nayanet-perspective-content{color:#fff!important}
  .nayanet-share{display:inline-flex;align-items:center;gap:7px;min-height:42px;padding:0 13px;border:1px solid #fff;border-radius:13px;background:#000;color:#fff!important;font-size:9px;font-weight:1000;letter-spacing:.06em;box-shadow:inset 0 1px #fff4,0 8px 18px #000a;cursor:pointer;transition:.2s ease}.nayanet-share:hover{transform:translateY(-2px);box-shadow:inset 0 1px #fff6,0 13px 25px #000b,0 0 20px var(--outer-tone)}
  .nayanet-share svg{width:16px;height:16px;stroke:#fff}.nayanet-share .love{font-size:14px;line-height:1}.nayanet-feed-v2 .blockFooter{margin-top:23px;padding-top:15px;color:#fff!important;border-top:1px solid #ffffff18}.nayanet-feed-v2 .blockFooter span,.nayanet-feed-v2 .blockFooter span:last-child{color:#fff!important}
  .nayanet-demo-block{order:-1}.nayanet-demo-badge{display:inline-flex;align-items:center;min-height:28px;padding:0 10px;border:1px solid #e8c766;border-radius:999px;color:#fff!important;background:#000;font-size:8px;font-weight:1000;letter-spacing:.12em;box-shadow:0 0 15px #e8c76618}
  @media(max-width:700px){.nayanet-feed-v2 .intelligentBlock{padding:23px 15px 25px;border-radius:22px;margin-bottom:20px}.nayanet-feed-v2 .blockTitle h3{font-size:34px}.nayanet-nutshell{padding:19px}.nayanet-nutshell p{font-size:17px!important}.nayanet-perspective-card{padding:17px}.nayanet-perspective-content{font-size:14px}.nayanet-share{min-height:40px}}
  </style>`);

  const toneFor=i=>tones[cycle[i%cycle.length]];
  function findExisting(block,key){
    const selectors=[`.perspective.${key}`,`[data-perspective="${key}"]`];
    for(const s of selectors){const el=block.querySelector(s);if(el)return textOf(el.querySelector('p')||el)}
    const all=[...block.querySelectorAll('.perspective')];
    const needles={human:['human'],child:['child'],grandma:['grandma','grandmother'],naya:['naya','ai'],machine:['machine'],lesson:['lesson','feed','learned','meaning']};
    const hit=all.find(el=>needles[key]?.some(n=>textOf(el).toLowerCase().includes(n)));
    return hit?textOf(hit.querySelector('p')||hit):'';
  }
  function blockText(block){return clean(block.querySelector('.blockBody p')?.textContent||block.querySelector('.blockTitle h3')?.textContent||'This intelligence event is still being distilled.')}

  const demo={
    title:'WHAT A SMART NOTE REALLY IS',
    nutshell:'A Smart Note turns a moment into reusable intelligence. Naya captures what happened, distills what matters, adds meaning and perspectives, and stores it so the lesson can be found, remembered, and compounded later.',
    human:'I do not just want Naya to remember my words. I want the system to remember why the moment mattered, what I learned from it, and how that learning can help me make a better decision later.',
    child:'A Smart Note is a good idea or lesson we do not want to lose. We write it down, make it easy to find, and use it again when we need it.',
    grandma:'Life teaches us in moments, but memory fades. A wise system should help us keep the lesson, not merely the story, so yesterday can make tomorrow a little wiser.',
    naya:'I see a Smart Note as one canonical intelligence event: the experience, the distilled wisdom, the human meaning, the AI interpretation, and the machine-readable structure belong together. That makes the note searchable, retrievable, explainable, and capable of compounding into future intelligence.',
    machine:'Store one event with a timestamp, source, type, human perspective, AI perspective, machine representation, meaning, tags, relationships, permissions, and retrieval signals. Keep content identity separate from interaction metadata so the intelligence remains stable while activity can evolve.',
    lesson:'Capture the moment. Distill the wisdom. Give it meaning. Preserve every useful perspective inside one intelligence event. Make it searchable. Then let future conversations retrieve it, connect it to other events, and compound it into better understanding and action.'
  };

  function makePerspective(key,label,sub,tone,content){
    const toneMap={magenta:'#d86cff',purple:'#9a68ff',indigo:'#6675ff',sapphire:'#55b9ee',emerald:'#31c875',gold:'#e8c766'};
    const card=document.createElement('section');
    card.className='nayanet-perspective-card '+(key==='lesson'?'lesson':'');
    card.style.setProperty('--inner-tone',toneMap[tone]);
    card.innerHTML=`<div class="nayanet-perspective-head"><span class="nayanet-perspective-icon">${icons[key]}</span><div><b>${label}</b><span>${sub}</span></div></div><div class="nayanet-perspective-content">${esc(content)}</div>`;
    return card;
  }

  function renderBlock(block,index){
    block.style.setProperty('--outer-tone',toneFor(index));
    const oldMap=block.querySelector('.perspectiveMap');
    if(!oldMap) return;
    const title=clean(block.querySelector('.blockTitle h3')?.textContent||'INTELLIGENCE');
    const nutshellText=blockText(block);
    const wrap=document.createElement('div');
    wrap.className='nayanet-perspective-v2-wrap';
    wrap.innerHTML=`<div class="nayanet-nutshell"><div class="nayanet-nutshell-head"><span class="nayanet-mini-icon">${icons.nutshell}</span><span>IN A NUTSHELL</span></div><p>${esc(nutshellText)}</p></div><div class="nayanet-perspectives"></div>`;
    const grid=wrap.querySelector('.nayanet-perspectives');
    const slots=[
      ['human','HUMAN NOTE','Your lived experience','magenta'],
      ['child','CHILD NOTE','The simplest human truth','purple'],
      ['grandma','GRANDMA NOTE','Wisdom that survives the jargon','indigo'],
      ['naya','NAYA NOTE','What Naya understands','sapphire'],
      ['machine','MACHINE NOTE','What the system can carry forward','emerald'],
      ['lesson','WHAT WE LEARNED · WHAT IT MEANS','The golden nugget','gold']
    ];
    slots.forEach(([key,label,sub,tone])=>grid.appendChild(makePerspective(key,label,sub,tone,findExisting(block,key)||'Perspective not yet captured.')));
    oldMap.replaceWith(wrap);
    const badge=block.querySelector('.demoBadge');
    if(badge) badge.className='nayanet-demo-badge';
    const footer=block.querySelector('.blockFooter');
    if(footer){
      footer.style.justifyContent='flex-end';
      footer.innerHTML=`<button class="nayanet-share" type="button" aria-label="Love and share this intelligence"><span class="love">♥</span><span>LOVE · SHARE</span>${icons.heart}</button>`;
      const btn=footer.querySelector('.nayanet-share');
      btn.addEventListener('click',async()=>{
        const shareText=`${title} — ${nutshellText}`;
        try{if(navigator.share){await navigator.share({title,text:shareText});}else if(navigator.clipboard){await navigator.clipboard.writeText(shareText);btn.querySelector('span:last-of-type').textContent='COPIED';setTimeout(()=>{btn.querySelector('span:last-of-type').textContent='LOVE · SHARE'},1400)}}catch(_){ }
      });
    }
  }

  const existing=[...root.querySelectorAll(':scope > .intelligentBlock')];
  existing.forEach((block,i)=>renderBlock(block,i+1));

  const demoBlock=document.createElement('article');
  demoBlock.className='intelligentBlock nayanet-demo-block liveNoteBlock';
  demoBlock.style.setProperty('--outer-tone',tones.magenta);
  demoBlock.innerHTML=`<div class="blockHeader"><div class="blockIdentity"><div class="blockGlyph">${icons.naya}</div><div class="blockTitle"><h3>${esc(demo.title)}</h3><div class="blockMeta"><span>SMART NOTE EXAMPLE</span><span>INTELLIGENT MEANING</span><span>NAYANET</span></div></div></div><span class="nayanet-demo-badge">EXAMPLE INTELLIGENT BLOCK</span></div><div class="blockBody"><p>${esc(demo.nutshell)}</p></div><div class="nayanet-perspective-v2-wrap"><div class="nayanet-nutshell"><div class="nayanet-nutshell-head"><span class="nayanet-mini-icon">${icons.nutshell}</span><span>IN A NUTSHELL</span></div><p>${esc(demo.nutshell)}</p></div><div class="nayanet-perspectives"></div></div><div class="blockFooter"></div>`;
  const demoGrid=demoBlock.querySelector('.nayanet-perspectives');
  [
    ['human','HUMAN NOTE','Your lived experience','magenta',demo.human],
    ['child','CHILD NOTE','The simplest human truth','purple',demo.child],
    ['grandma','GRANDMA NOTE','Wisdom that survives the jargon','indigo',demo.grandma],
    ['naya','NAYA NOTE','What Naya understands','sapphire',demo.naya],
    ['machine','MACHINE NOTE','What the system can carry forward','emerald',demo.machine],
    ['lesson','WHAT WE LEARNED · WHAT IT MEANS','The golden nugget','gold',demo.lesson]
  ].forEach(args=>demoGrid.appendChild(makePerspective(...args)));
  const demoFooter=demoBlock.querySelector('.blockFooter');
  demoFooter.style.justifyContent='flex-end';
  demoFooter.innerHTML=`<button class="nayanet-share" type="button" aria-label="Love and share this intelligence"><span class="love">♥</span><span>LOVE · SHARE</span>${icons.heart}</button>`;
  const demoShare=demoFooter.querySelector('.nayanet-share');
  demoShare.addEventListener('click',async()=>{try{if(navigator.share){await navigator.share({title:demo.title,text:demo.nutshell})}else if(navigator.clipboard){await navigator.clipboard.writeText(`${demo.title} — ${demo.nutshell}`);demoShare.querySelector('span:nth-child(2)').textContent='COPIED';setTimeout(()=>demoShare.querySelector('span:nth-child(2)').textContent='LOVE · SHARE',1400)}}catch(_){}});
  root.prepend(demoBlock);
})();
