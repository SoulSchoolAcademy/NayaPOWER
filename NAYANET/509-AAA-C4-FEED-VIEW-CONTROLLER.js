/* NayaNET 509 AAA — C4 FEED VIEW CONTROLLER v1.0
 * Surgical controller for the sacred Personal / Collective / Activity feed views.
 * Personal and Collective project the same canonical nine Smart Notes differently;
 * Activity restores the pre-canonical feed projection preserved by the parser.
 * No backend claims. No content invention. No C5 redesign.
 */
(()=>{'use strict';
const FEEDS={
 personal:{label:'Personal Intelligence',title:'Personal Intelligence',desc:'Your intelligence — private by default. Capture, understand, remember, and compound what is yours.',mode:'personal'},
 collective:{label:'Collective Intelligence',title:'Collective Intelligence',desc:'Shared intelligence for discovery, contribution, and useful connection. Social actions belong here.',mode:'collective'},
 activity:{label:'Activity Feed',title:'Activity Feed',desc:'What is happening: actions, changes, contributions, processing, results, and intelligence events.',mode:'activity'}
};
const STORE='nayanet-509-feed-view-v1';
const q=(s,r=document)=>r.querySelector(s),qq=(s,r=document)=>[...r.querySelectorAll(s)];
const text=e=>(e?.innerText||e?.textContent||'').replace(/\s+/g,' ').trim();
const keyFor=b=>b?.dataset?.feedView||'';
function read(){try{return localStorage.getItem(STORE)||'personal'}catch{return 'personal'}}
function write(v){try{localStorage.setItem(STORE,v)}catch{}}
function navButtons(){const nav=q('.feedNav');if(!nav)return [];return qq('button,a,[role="button"]',nav).filter(b=>/^(PERSONAL\s+INTELLIGENCE|COLLECTIVE\s+INTELLIGENCE|ACTIVITY\s+FEED)$/i.test(text(b)))}
function feedKey(el){const t=text(el).toLowerCase();if(t.includes('personal'))return'personal';if(t.includes('collective'))return'collective';if(t.includes('activity'))return'activity';return''}
function preserveCanonical(){const blocks=q('.blocks');if(!blocks)return;const canonical=blocks.querySelectorAll('[data-real-smart-note]');if(canonical.length===9&&!window.__naya509CanonicalNineHTML)window.__naya509CanonicalNineHTML=blocks.innerHTML}
function preserveActivity(){if(window.__naya509LegacyFeedHTML)return window.__naya509LegacyFeedHTML;return ''}
function setVisible(board,visible){board.hidden=!visible;board.style.display=visible?'':'none'}
function socialVisibility(mode){qq('[data-real-smart-note] .action,[data-real-smart-note] .naya509-rating').forEach(el=>{const kind=(el.dataset.c4Kind||'').toLowerCase();const social=kind==='love'||kind==='like'||kind==='rating';if(mode==='collective'){el.hidden=false;el.style.removeProperty('display')}else if(mode==='personal'){if(social){el.hidden=true;el.style.setProperty('display','none','important')}else{el.hidden=false;el.style.removeProperty('display')}}else{el.hidden=true;el.style.setProperty('display','none','important')}})}
function updateHeader(mode){const f=FEEDS[mode],h=q('.feedHead h2'),p=q('.feedHead p');if(h)h.textContent=f.title;if(p){p.textContent=f.desc;p.style.setProperty('font-size','20px','important');p.style.setProperty('line-height','1.5','important');p.style.setProperty('color','#d8d1df','important');p.style.setProperty('max-width','1100px','important')}}
function activityMarkup(){const html=preserveActivity();return html||`<article class="block naya509-board naya509-activity-empty"><div class="blockInner"><div class="blockTop"><div class="identity"><div class="glyph">◌</div><div><h3>Activity Feed</h3><div class="meta"><span>ACTIVITY PROJECTION</span><span>NO LEGACY EVENTS PRESERVED</span></div></div></div></div><div class="nutshell"><b>ACTIVITY</b><p>No prior activity markup was available at the moment this projection was created. New truthful intelligence events remain locally observable through the interaction layer.</p></div></div></article>`}
function render(mode){const blocks=q('.blocks');if(!blocks)return;preserveCanonical();if(mode==='activity'){if(blocks.dataset.feedMode!=='activity'){blocks.innerHTML=activityMarkup();blocks.dataset.feedMode='activity'}}else{if(!blocks.querySelectorAll('[data-real-smart-note]').length&&window.__naya509CanonicalNineHTML)blocks.innerHTML=window.__naya509CanonicalNineHTML;blocks.dataset.feedMode=mode;qq('[data-real-smart-note]',blocks).forEach(b=>setVisible(b,true))}socialVisibility(mode);updateHeader(mode);document.documentElement.dataset.naya509FeedMode=mode;write(mode)}
function sync(mode){const bs=navButtons();bs.forEach(b=>{const k=feedKey(b),on=k===mode;b.classList.toggle('active',on);b.setAttribute('aria-selected',on?'true':'false');b.setAttribute('aria-current',on?'page':'false');b.setAttribute('tabindex',on?'0':'-1')});}
function activate(mode){if(!FEEDS[mode])return;render(mode);sync(mode);setTimeout(()=>{if(window.Naya509NineNoteParser&&mode!=='activity'){try{window.Naya509NineNoteParser.boot()}catch(_){}}render(mode);sync(mode)},0)}
function install(){const nav=q('.feedNav');if(!nav||nav.dataset.naya509Controller==='1')return;nav.dataset.naya509Controller='1';nav.setAttribute('role','tablist');navButtons().forEach(b=>{b.addEventListener('click',e=>{const k=feedKey(b);if(!k)return;e.preventDefault();e.stopPropagation();e.stopImmediatePropagation();activate(k)},{capture:true});b.addEventListener('keydown',e=>{if(!['ArrowRight','ArrowLeft','Home','End'].includes(e.key))return;e.preventDefault();e.stopImmediatePropagation();const bs=navButtons(),i=bs.indexOf(b);let n=i;if(e.key==='ArrowRight')n=(i+1)%bs.length;if(e.key==='ArrowLeft')n=(i-1+bs.length)%bs.length;if(e.key==='Home')n=0;if(e.key==='End')n=bs.length-1;bs[n].focus();activate(feedKey(bs[n]))},{capture:true})});activate(FEEDS[read()]?read():'personal')}
function css(){if(q('#naya509-feed-controller-css'))return;const s=document.createElement('style');s.id='naya509-feed-controller-css';s.textContent=`
.feedNav{display:grid!important;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px!important;width:100%!important;overflow:visible!important;padding:0 22px 18px!important}.feedNav button,.feedNav a,.feedNav [role="button"]{width:100%!important;justify-content:center!important;min-width:0!important;height:52px!important;min-height:52px!important;font-size:15px!important;font-weight:850!important}.feedNav button.active,.feedNav a.active,.feedNav [role="button"].active{transform:none!important}
.feedHead p{font-size:20px!important;line-height:1.5!important;color:#d8d1df!important;max-width:1100px!important}
@media(max-width:760px){.feedNav{grid-template-columns:1fr!important;gap:8px!important;padding:0 14px 14px!important}.feedNav button,.feedNav a,.feedNav [role="button"]{height:50px!important;min-height:50px!important;font-size:14px!important}.feedHead p{font-size:19px!important;line-height:1.5!important}}
`;document.head.appendChild(s)}
function boot(){css();preserveCanonical();install()}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
let tries=0;const iv=setInterval(()=>{tries++;if(q('.feedNav')){boot();if(tries>12)clearInterval(iv)}else if(tries>12)clearInterval(iv)},250);
})();