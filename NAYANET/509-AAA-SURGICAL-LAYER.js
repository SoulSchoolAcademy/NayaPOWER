(function(){
'use strict';
function inject(){
 if(document.getElementById('naya509-aaa-style')) return;
 const s=document.createElement('style');s.id='naya509-aaa-style';s.textContent=`
.nayanet-ecosystem-bar,.nayanet-feature-bar,.nayanet-v7-actions,.nh72-feedback,#nh72Today{display:none!important}
.main{padding-left:clamp(20px,4vw,64px);padding-right:clamp(20px,4vw,64px)}
.topbar{height:70px}
#page-home{padding-top:18px}
#page-home .heroIntro{display:none}
#page-home .hero{margin-top:10px;border-radius:30px;grid-template-columns:minmax(0,1fr) 330px;min-height:310px;border-color:#d86cff55;background:radial-gradient(650px 260px at 10% 0%,#d86cff18,transparent 65%),linear-gradient(135deg,#181321,#0a090e 65%,#07070a)}
#page-home .heroCopy{padding:40px 42px}
#page-home .heroCopy h2{font-size:clamp(38px,4.5vw,64px);max-width:850px;line-height:.96}
#page-home .heroCopy p{font-size:15px;max-width:720px;color:#d8d2dc}
#page-home .hero .eyebrow{color:#b99aff}
#page-home .naya{min-height:310px;background:radial-gradient(circle at 50% 44%,#d86cff25,transparent 62%)}
#page-home .nayaPhoto{width:166px;height:166px}
.naya509-mission{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin-top:22px;max-width:780px}
.naya509-mission div{padding:12px 14px;border:1px solid #ffffff18;border-radius:13px;background:#08080c}
.naya509-mission b{display:block;font-size:8px;letter-spacing:.12em}
.naya509-mission span{display:block;margin-top:4px;color:#9993a0;font-size:9px;line-height:1.45}
#page-home .homeWorkspace{margin-top:22px}
#page-home .intelligentFeed{border-top:1px solid #ffffff12}
#page-home .intelligentFeedHead{padding:22px 4px 18px}
#page-home .intelligentFeedHead h2{font-size:clamp(26px,3vw,38px);letter-spacing:-.05em}
#page-home .intelligentBlocks{border:1px solid #ffffff12;border-radius:26px;background:linear-gradient(145deg,#0b0b10,#060609);box-shadow:inset 0 1px #fff3,0 30px 70px #000b;overflow:hidden}
#page-home .intelligentBlock{padding:46px clamp(22px,4vw,56px) 54px}
#page-home .intelligentBlock:before{left:12px}
#page-home .blockTitle h3{font-size:clamp(30px,3.4vw,48px)}
#page-home .blockBody p{font-size:18px;line-height:1.72;max-width:980px}
#page-home .perspectiveMap{max-width:1020px}
#page-home .perspective{padding-bottom:34px}
#page-home .perspective p{font-size:16px;line-height:1.72}
.naya509-empty{padding:64px 28px;text-align:center;border:1px solid #55b9ee38;border-radius:24px;background:radial-gradient(600px 220px at 50% 0%,#55b9ee0d,transparent 70%),#08080c}
.naya509-empty .kicker{font-size:8px;font-weight:1000;letter-spacing:.18em;color:#8ed9ff}
.naya509-empty h3{font-size:clamp(28px,3vw,42px);letter-spacing:-.05em;margin:10px 0 9px}
.naya509-empty p{max-width:650px;margin:0 auto;color:#aaa4b1;font-size:12px;line-height:1.7}
.naya509-empty .btn{margin-top:20px}
@media(max-width:900px){#page-home .hero{grid-template-columns:1fr}.naya509-mission{grid-template-columns:1fr}.main{padding-left:16px;padding-right:16px}}
`;
document.head.appendChild(s);
}
function coreBlocks(){return [
{tone:'var(--magenta)',glyph:'✦',title:'Intelligence should reveal itself.',time:'NAYA CORE',type:'FOUNDATION',tags:['COMPLEXITY UNDERNEATH','CLARITY ABOVE'],body:['NayaNET exists to make intelligence easier for humans to understand, remember, connect, and use. The system can be extraordinarily complex underneath; the human experience should feel extraordinarily clear above.'],human:'Human value comes first: understand what matters quickly, know why it matters, and know what can be done with it.',naya:'Naya should separate what is known from what is inferred, expose uncertainty honestly, and turn useful complexity into a clear next move.',machine:'FOUNDATION PRINCIPLE · This is curated NayaNET product intelligence, not a personal activity event.',feed:'SEE → UNDERSTAND → EXPLORE → TRUST → CONNECT → ACT → LEARN'},
{tone:'var(--sapphire)',glyph:'◇',title:'An Intelligent Block is not a post.',time:'NAYA CORE',type:'FOUNDATION',tags:['INTELLIGENT BLOCK','PROGRESSIVE DISCLOSURE'],body:['One intelligence event can contain human experience, Naya interpretation, machine evidence, learning, meaning, action, trust, and connections without forcing the human to read everything at once.'],human:'The first layer should answer the essential question. Deeper intelligence should be available when the human wants it.',naya:'Reveal the smallest complete explanation first. Expand only when more depth increases understanding or action.',machine:'FOUNDATION PRINCIPLE · The block is a presentation of intelligence, not merely a database row.',feed:'NUTSHELL → HUMAN → CHILD → GRANDMA → NAYA → MACHINE → LEARNING → MEANING → ACTION → TRUST → CONNECTIONS'},
{tone:'var(--green)',glyph:'✓',title:'Trust is part of the intelligence.',time:'NAYA CORE',type:'FOUNDATION',tags:['FACT','EVIDENCE','INTERPRETATION','UNKNOWN'],body:['A useful intelligence interface must make it possible to distinguish source-backed fact, human input, Naya interpretation, machine evidence, and what remains unknown.'],human:'Do not make confidence look like truth. Make the boundary visible without burying the human in audit metadata.',naya:'Never present inference as verified fact. When evidence is missing, say so. When the system cannot act, show the boundary and the next legitimate path.',machine:'FOUNDATION PRINCIPLE · Source → artifact → deployment → runtime → observation is a proof chain for consequential system claims.',feed:'TRUTH → EVIDENCE → CONTEXT → ACTION → OBSERVATION → LEARNING'}
]}
function renderCore(){
 const root=document.getElementById('homeIntelligentBlocks'); if(!root)return;
 const count=document.getElementById('homeFeedCount');
 let notes=[];try{notes=JSON.parse(localStorage.getItem('nayanet_v7_live_notes')||'[]')}catch(e){}
 if(notes.length){if(typeof window.renderHomeFeed==='function') window.renderHomeFeed();return;}
 const render=(b)=>`<article class="intelligentBlock" style="--tone:${b.tone}"><header class="blockHeader"><div class="blockIdentity"><div class="blockGlyph">${b.glyph}</div><div class="blockTitle"><h3>${b.title}</h3><div class="blockMeta"><span>${b.time}</span><span>·</span><span>${b.type}</span><span>·</span><span>CURATED NAYA INTELLIGENCE</span></div></div></div></header><div class="blockBody"><p>${b.body[0]}</p><div class="blockTagRow">${b.tags.map(x=>`<span class="blockTag">${x}</span>`).join('')}</div></div><div class="perspectiveMap"><section class="perspective human" style="--perspective:var(--green)"><div class="perspectiveHead"><b>01 · HUMAN</b><span class="perspectiveState">VALUE</span></div><p>${b.human}</p></section><section class="perspective naya" style="--perspective:var(--sapphire)"><div class="perspectiveHead"><b>02 · NAYA</b><span class="perspectiveState">INTERPRETATION</span></div><p>${b.naya}</p></section><section class="perspective machine" style="--perspective:var(--gold)"><div class="perspectiveHead"><b>03 · MACHINE</b><span class="perspectiveState">SYSTEM CONTEXT</span></div><p>${b.machine}</p></section><section class="perspective feed" style="--perspective:var(--magenta)"><div class="perspectiveHead"><b>04 · CARRY FORWARD</b><span class="perspectiveState">ACTION MODEL</span></div><p>${b.feed}</p></section></div><footer class="blockFooter"><span>FOUNDATIONAL NAYA INTELLIGENCE</span><span>NOT PERSONAL ACTIVITY</span></footer></article>`;
 count.textContent='NAYA CORE · FOUNDATIONAL INTELLIGENCE'; root.innerHTML=coreBlocks().map(render).join('');
}
function addMission(){if(document.querySelector('.naya509-mission'))return;const c=document.querySelector('#page-home .heroCopy');if(!c)return;const d=document.createElement('div');d.className='naya509-mission';d.innerHTML='<div><b>UNDERSTAND</b><span>See the essential intelligence without reading everything.</span></div><div><b>TRUST</b><span>Know what is fact, inference, evidence, and unknown.</span></div><div><b>ACT</b><span>Turn understanding into a useful next move.</span></div>';c.appendChild(d)}
function addEmptyState(){if(document.getElementById('naya509-empty'))return;const host=document.querySelector('#page-home .homeFeed');if(!host)return;const d=document.createElement('section');d.id='naya509-empty';d.className='naya509-empty';d.innerHTML='<div class="kicker">YOUR PERSONAL INTELLIGENCE</div><h3>Nothing personal is captured yet.</h3><p>That is not a failure. It is an honest state. Start with one meaningful event and NayaNET can turn it into an Intelligent Block you can understand, remember, and build on.</p><button class="btn green" data-page="notes">CREATE YOUR FIRST INTELLIGENT BLOCK</button>';host.insertAdjacentElement('beforebegin',d)}
function init(){inject();addMission();renderCore();const hasNotes=(()=>{try{return JSON.parse(localStorage.getItem('nayanet_v7_live_notes')||'[]').length>0}catch(e){return false}})();if(!hasNotes)addEmptyState()}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();
