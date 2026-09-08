/* NayaNET V4 — surgical evolution of the V3 feed.
   Layout corrections, nine substantive demo events, sidebar priority, and human/Naya imagery.
   This layer is additive: it does not replace the authoritative Hub or V3 architecture.
*/
(()=>{
'use strict';
if(window.__NAYA_V4_SURGICAL_POLISH__) return;
window.__NAYA_V4_SURGICAL_POLISH__=true;

const clean=v=>String(v??'').replace(/\s+/g,' ').trim();
const esc=v=>String(v??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
const ROOT='#nayanet-elite-feed';

const EXTRA=[
 {id:'capture-meaning',title:'CAPTURE THE MEANING, NOT JUST THE MOMENT',human:'The best notes preserve why something mattered, not merely the sequence of events.',child:'Keep the part that helps us later.',grandma:'A memory becomes useful when it still carries the lesson with it.',naya:'The intelligence layer should distinguish raw experience from the meaning extracted from it, so future retrieval can surface both the source and the interpretation.',machine:'SOURCE_EVENT → INTERPRETATION → DISTILLED_LESSON → RETRIEVAL_CONTEXT.',lesson:'A timestamp tells you when something happened. Meaning tells you why it matters.',use:'When capturing a note, add the reason it matters and what you want your future self to remember.',nutshell:'A useful Smart Note does more than preserve a moment. It preserves the meaning that made the moment worth remembering. That gives future-you something actionable to retrieve instead of another pile of history.'},
 {id:'one-event-many-views',title:'ONE EVENT, MANY INTELLIGENT PERSPECTIVES',human:'I can look at the same experience from different angles without creating different truths.',child:'One thing happened. We can look at it in a few helpful ways.',grandma:'Wisdom often comes from seeing one thing from more than one point of view.',naya:'Multiple perspectives are projections of one canonical intelligence event. They enrich understanding without fragmenting the underlying truth.',machine:'EVENT_ID remains stable while perspective projections vary by semantic role and audience.',lesson:'Perspective should multiply understanding, not multiply conflicting records.',use:'Capture one event once, then let the system derive the perspectives that help you understand and use it.',nutshell:'One meaningful event can contain more than one useful interpretation. Smart Notes keep those perspectives together so the system can compare, connect, and retrieve them as one intelligence event. The result is richer understanding without duplicated records.'},
 {id:'experience-compounds',title:'EXPERIENCE COMPOUNDS WHEN YOU CAN FIND IT AGAIN',human:'A lesson I cannot retrieve when I need it is almost as useful as a lesson I never captured.',child:'If we forget where we put it, it is hard to use.',grandma:'Remembering is only half the gift. Being able to find it when needed is the other half.',naya:'Compounding intelligence requires retrieval, not merely storage. Relevance, relationships, and context turn yesterday’s experience into tomorrow’s decision support.',machine:'CAPTURE + INDEX + RELATE + RETRIEVE = COMPOUNDING_VALUE.',lesson:'The intelligence system must bring the right lesson back at the right time.',use:'Connect important Smart Notes to people, projects, decisions, and future questions so retrieval has context.',nutshell:'Captured intelligence becomes more valuable when it can return at the moment it is useful. Search finds the note, relationships add context, and retrieval turns the old experience into a new advantage. That is the practical engine of compounding.'},
 {id:'collective-consent',title:'COLLECTIVE WISDOM REQUIRES CONSENT',human:'I should be able to keep my intelligence private and choose what becomes useful to the wider network.',child:'Share the good stuff when we want to.',grandma:'What is yours should remain yours until you decide to give it away.',naya:'Collective intelligence is formed from consented contributions, not from silently harvesting personal intelligence. Privacy and contribution are compatible when permission is explicit.',machine:'PRIVATE_BY_DEFAULT; SHARED_BY_CHOICE; COLLECTIVE_BY_CONSENT; PUBLIC_BY_DECISION.',lesson:'A trustworthy collective layer is built on choice, provenance, and permission.',use:'Keep personal intelligence private by default and explicitly choose which insights are worth contributing to the collective.',nutshell:'Collective intelligence is strongest when people choose to contribute rather than being automatically exposed. Personal intelligence remains private unless its owner shares it. Consent turns individual learning into trusted network wisdom.'},
 {id:'daily-briefing',title:'THE DAILY BRIEFING TURNS MEMORY INTO ACTION',human:'I want my intelligence brought back to me when it can actually help me move today forward.',child:'Tell me the important stuff for today.',grandma:'A good briefing does not give you everything. It gives you what matters now.',naya:'The Daily Intelligence Report is a retrieval surface over the user’s evolving intelligence. It should prioritize relevant lessons, unfinished loops, patterns, decisions, and opportunities rather than simply listing activity.',machine:'RELEVANCE × RECENCY × IMPORTANCE × CONTEXT → DAILY_INTELLIGENCE_REPORT.',lesson:'Remembering becomes powerful when memory arrives at the right moment.',use:'Start the day with the Daily Intelligence Report, then let it point you toward the intelligence most likely to improve today’s decisions.',nutshell:'Your intelligence should not sit quietly in a library waiting for you to remember where you put it. The Daily Intelligence Report brings forward the patterns, lessons, decisions, and opportunities that matter now. It turns accumulated memory into a daily operating advantage.'}
];

function nayaImage(){return document.querySelector('.avatar img')?.getAttribute('src')||'';}
function person(){return clean(document.querySelector('.avatar img')?.alt||document.body.dataset.userName||'Your')||'Your';}
function block(n,index){
 const accent=['#8b5cf6','#55b9ee','#e8c766','#d86cff','#6675ff'][index%5];
 const ps=[['👤',person().toUpperCase()+' NOTE',n.human,'#d86cff'],['👶','CHILD NOTE',n.child,'#8b5cf6'],['👵','GRANDMA NOTE',n.grandma,'#6675ff'],['✨','NAYA NOTE',n.naya,'#55b9ee'],['⚙️','MACHINE NOTE',n.machine,'#55e39a'],['💡','LESSON',n.lesson,'#e8c766'],['🧭','HOW TO USE IT',n.use,'#fff']];
 const img=nayaImage();
 return `<article class="n3-block n4-added" data-id="${esc(n.id)}" style="--accent:${accent}">
  <div class="n3-head"><div><div class="n3-eyebrow"><span class="n3-led"></span><b>INTELLIGENT BLOCK</b></div><div class="n3-title">${esc(n.title)}</div></div><div class="n3-topactions"><button class="n3-action" type="button" aria-label="Favorite this intelligence">☆</button><button class="n3-action naya-play" type="button" data-play="${esc(n.id)}" aria-label="Play Naya for this intelligence">▶ PLAY NAYA</button></div></div>
  <div class="n3-nutshell"><div class="n3-label">IN A NUTSHELL</div><h4>THE CORE INTELLIGENCE</h4><p>${esc(n.nutshell)}</p></div>
  <div class="n3-perspectives">${ps.map((p,j)=>`<section class="n3-perspective" style="--p:${p[3]}"><div class="n3-phead">${j===0&&img?`<img class="n4-person-photo" src="${esc(img)}" alt="${esc(person())}">`:`<span class="n3-picon">${p[0]}</span>`}<b>${esc(p[1])}</b></div><div class="n3-pbody">${esc(p[2])}</div></section>`).join('')}</div>
  <div class="n3-footer"><div class="n3-love"><button class="n3-btn" type="button">♡ LOVE</button><button class="n3-btn" type="button">KEEP / SAVE</button><button class="n3-btn" type="button">＋ SHARE</button></div><div class="n3-stars" aria-label="Rate usefulness"><button class="n3-star" type="button">★</button><button class="n3-star" type="button">★</button><button class="n3-star" type="button">★</button><button class="n3-star" type="button">★</button><button class="n3-star" type="button">★</button></div></div>
 </article>`;
}

function addStyles(){
 if(document.getElementById('n4-surgical-style')) return;
 const s=document.createElement('style'); s.id='n4-surgical-style'; s.textContent=`
 .n4-person-photo{width:27px;height:27px;border-radius:9px;object-fit:cover;border:1px solid #d86cff70;box-shadow:0 0 16px #d86cff22;display:block}
 #nayanet-elite-feed .n4-added .n3-nutshell p{font-size:15px;line-height:1.62}
 #nayanet-elite-feed .n4-added .n3-pbody{font-size:11px;line-height:1.68;min-height:38px}
 #nayanet-elite-feed .n4-added{margin-top:2px}
 .n4-daily-report{position:relative;display:flex;align-items:center;gap:10px;width:100%;min-height:58px;margin:0 0 10px;padding:10px 12px;border:1px solid #e8c76665;border-radius:15px;background:linear-gradient(145deg,#18140b,#08080b);color:#fff;text-align:left;box-shadow:inset 0 1px #fff5,0 14px 30px #000b,0 0 25px #e8c7660c;cursor:pointer}
 .n4-daily-report:hover{transform:translateY(-2px);border-color:#e8c766a0;box-shadow:inset 0 1px #fff7,0 18px 36px #000c,0 0 30px #e8c76618}
 .n4-daily-report .n4-report-icon{width:31px;height:31px;display:grid;place-items:center;border-radius:10px;border:1px solid #e8c76655;background:#e8c7660d;font-size:15px;box-shadow:0 0 16px #e8c76615}
 .n4-daily-report b{display:block;font-size:9px;letter-spacing:.08em}.n4-daily-report span{display:block;margin-top:3px;color:#aaa3ad;font-size:7px;letter-spacing:.04em}
 .n4-sidebar-priority{order:-10}
 @media(max-width:820px){.n4-daily-report{min-height:52px}.n4-person-photo{width:25px;height:25px}}
 `; document.head.appendChild(s);
}

function removeSideSmartNotes(){
 document.querySelectorAll('aside, .homeRail, .rightRail, [class*="rail"]').forEach(rail=>{
   rail.querySelectorAll('*').forEach(el=>{
     if(el.children.length>8) return;
     const t=clean(el.textContent).toUpperCase();
     if(t==='SMART NOTES' || t==='SMART NOTE'){
       const card=el.closest('[class*="card"],section,article,div');
       if(card && card!==rail) card.remove();
     }
   });
 });
}
function findRail(){return document.querySelector('.homeRail,.rightRail,aside,[class*="sidebar"]')}
function prioritizeSidebar(){
 const rail=findRail(); if(!rail) return false;
 let old=[];
 rail.querySelectorAll('button,a,[role="button"]').forEach(el=>{
   const t=clean(el.textContent).toUpperCase();
   if(t.includes('CONNECT GITHUB')||t.includes('SYNC INTELLIGENCE')||t.includes('GET CONNECTED')) old.push(el.closest('section,article,div')||el);
 });
 const report=document.createElement('button'); report.className='n4-daily-report n4-sidebar-priority'; report.type='button'; report.innerHTML='<span class="n4-report-icon">◈</span><span><b>YOUR DAILY INTELLIGENCE REPORT</b><span>Daily Intelligence Briefing</span></span>';
 report.onclick=()=>{const target=document.querySelector('[data-nav="today"],#today,.todayPage,[class*="dailyReport"]'); if(target) target.scrollIntoView({behavior:'smooth',block:'start'}); else alert('Your Daily Intelligence Report is ready to become the daily retrieval surface.');};
 const existing=Array.from(rail.querySelectorAll('.n4-daily-report')); if(existing.length) existing.forEach(x=>x.remove());
 rail.prepend(report);
 // Keep the three connection actions directly beneath the report when their containers are found.
 old.reverse().forEach(x=>{if(x&&x.parentElement===rail) rail.insertBefore(x,rail.children[1]||null)});
 return true;
}
function ensureNine(){
 const root=document.querySelector(ROOT); if(!root) return false;
 const body=root.querySelector('.n3-body'); if(!body) return false;
 EXTRA.forEach((n,i)=>{if(!body.querySelector(`[data-id="${n.id}"]`)) body.insertAdjacentHTML('beforeend',block(n,i));});
 const bottom=root.querySelector('.n3-bottom');
 if(bottom) root.appendChild(bottom); // footer remains below the complete feed
 return true;
}
function moveFeedUp(){
 const root=document.querySelector(ROOT); if(!root) return false;
 // V3 owns the tabs and feed; keep the feed immediately below the tabs with no extra heading injected by this layer.
 const tabs=root.querySelector('.n3-tabs'); if(tabs) tabs.style.marginBottom='18px';
 const bottom=root.querySelector('.n3-bottom'); if(bottom){bottom.style.marginTop='38px';}
 return true;
}
function init(){addStyles();removeSideSmartNotes();prioritizeSidebar();ensureNine();moveFeedUp();}
init();
let runs=0; const timer=setInterval(()=>{init(); if(++runs>12) clearInterval(timer)},500);
})();
