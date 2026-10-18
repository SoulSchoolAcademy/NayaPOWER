
#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build import LIB_CSS, ELEV_CSS, OUT
from catalog import PIECES
from functions import FUNCS_HTML

SIZES = [("XS",0.55),("S",0.75),("M",1.0),("L",1.3),("XL",1.6),("AUTO",1.0)]
CATS = ["All","Buttons","Icons","Orbs","Jewels","Boards","Rows","Inputs","Headers","Markers","Navigation"]

SPECTRUM = ["#e84fff","#a06bff","#3fb8ff","#2fe89e","#ffbf3d","#ff5e6c","#ff9a5a"]
_ci = [0]
def card(p):
    _ci[0] += 1
    sc = SPECTRUM[(_ci[0]-1) % len(SPECTRUM)]
    sz = "".join(f'<button class="szpill{" on" if s=="M" else ""}" data-s="{s}" data-z="{z}">{s}</button>' for s,z in SIZES)
    return f'''<div class="pcard" style="--sc:{sc}" data-cat="{p["cat"]}" data-model="{p["model"]}" data-name="{p["name"]}">
  <div class="pstage carve-1"><div class="zoom">{p["html"]}</div></div>
  <div><div class="pmodel">{p["model"]}</div><div class="pname">{p["name"]}</div>
  <div style="font-size:12px;opacity:.6">{p["note"]}</div></div>
  <div class="psizes">{sz}</div>
  <div class="prow"><button class="btn-select elev-1" type="button">Select</button><button class="btn-notes carve-1" type="button">Notes</button></div>
</div>'''

cards = "\n".join(card(p) for p in PIECES)

def rail(cat):
    cs = "\n".join(card(p) for p in PIECES if p["cat"] == cat)
    head = '<div class="railhead"><span class="pmodel">' + cat.upper() + '</span><span style="font-size:12px;opacity:.5">scroll sideways</span></div>'
    return '<div class="railblock">' + head + '<div class="rail">' + cs + '</div></div>'
rails = "\n".join(rail(c) for c in CATS[1:])

filters = "".join(f'<button class="filterpill{" on" if c=="All" else ""}" data-f="{c}">{c}</button>' for c in CATS)

from templates2 import TMPLS2
tmpls = TMPLS2

JS = r'''
const cart=[];
function sizeOf(card){const b=card.querySelector('.szpill.on');return b?b.dataset.s:'M';}
document.querySelectorAll('.pcard').forEach(card=>{
  card.querySelectorAll('.szpill').forEach(b=>b.onclick=()=>{card.querySelectorAll('.szpill').forEach(x=>x.classList.remove('on'));b.classList.add('on');card.querySelector('.zoom').style.transform='scale('+b.dataset.z+')';});
  card.querySelector('.btn-select').onclick=e=>{const m=card.dataset.model,n=card.dataset.name,s=sizeOf(card);
    const ex=cart.find(i=>i.model===m&&i.size===s); if(ex){ex.qty++;} else cart.push({model:m,name:n,size:s,qty:1});
    e.target.classList.add('picked');e.target.textContent='In cart ✓';renderCart();};
  card.querySelector('.btn-notes').onclick=()=>openNote(card);
});
document.querySelectorAll('.filterpill').forEach(f=>f.onclick=()=>{document.querySelectorAll('.filterpill').forEach(x=>x.classList.remove('on'));f.classList.add('on');const v=f.dataset.f;document.querySelectorAll('.pcard').forEach(c=>c.style.display=(v==='All'||c.dataset.cat===v)?'':'none');});
const TSLUG=k=>({"Smart List":"smartlist"}[k]||k.toLowerCase());
document.querySelectorAll('.tcard2').forEach(t=>{t.onclick=()=>{document.querySelectorAll('.tcard2').forEach(x=>x.classList.remove('open','sel'));t.classList.add('open','sel');saveDraft();};
const v=t.querySelector('.tview');v.onclick=e=>{e.stopPropagation();if(!t.classList.contains('sel')){t.click();}window.open('smart-templates/'+TSLUG(t.dataset.t)+'/index.html','_blank');};});
document.querySelectorAll('.tog').forEach(t=>t.onclick=()=>t.classList.toggle('on'));
let noteCard=null;
function openNote(card){noteCard=card;document.getElementById('noteTitle').textContent='Note — '+card.dataset.model+' · '+card.dataset.name;const ex=cart.find(i=>i.model===card.dataset.model);document.getElementById('noteText').value=ex?ex.note||'':'';document.getElementById('noteWrap').classList.add('open');setTimeout(()=>document.getElementById('noteText').focus(),50);}
function closeNote(){document.getElementById('noteWrap').classList.remove('open');noteCard=null;}
function saveNote(){const v=document.getElementById('noteText').value.trim();if(noteCard&&v){const ex=cart.find(i=>i.model===noteCard.dataset.model);(ex||cart[cart.push({model:noteCard.dataset.model,name:noteCard.dataset.name,size:sizeOf(noteCard),qty:1,note:''})-1]&&cart[cart.length-1]).note=v;renderCart();}closeNote();}
document.getElementById('noteSave').onclick=saveNote;
document.getElementById('noteCancel').onclick=closeNote;
document.getElementById('noteWrap').addEventListener('click',e=>{if(e.target.id==='noteWrap')closeNote();});
function saveDraft(){try{const d={v:document.getElementById('visionText').value,h:document.getElementById('handleIn').value,q:[document.getElementById('qVision').value,document.getElementById('qDo').value,document.getElementById('qBehave').value],togs:[...document.querySelectorAll('.frow .tog')].map(t=>t.classList.contains('on')),cart:cart,tmpl:(document.querySelector('.tcard2.sel')||{dataset:{}}).dataset.t||'',sizes:{}};document.querySelectorAll('.pcard').forEach(c=>{const s=c.querySelector('.szpill.on');if(s)d.sizes[c.dataset.model]=s.dataset.s;});localStorage.setItem('nayaFactoryDraft',JSON.stringify(d));}catch(e){}}
function loadDraft(){try{const d=JSON.parse(localStorage.getItem('nayaFactoryDraft'));if(!d||(!d.v&&!d.h&&!d.cart.length&&!d.tmpl))return false;document.getElementById('visionText').value=d.v||'';document.getElementById('handleIn').value=d.h||'';const qs=['qVision','qDo','qBehave'];(d.q||[]).forEach((v,i)=>{if(qs[i])document.getElementById(qs[i]).value=v||'';});const togs=document.querySelectorAll('.frow .tog');(d.togs||[]).forEach((on,i)=>{if(togs[i])togs[i].classList.toggle('on',!!on);});cart.length=0;(d.cart||[]).forEach(i=>cart.push(i));Object.entries(d.sizes||{}).forEach(([m,s])=>{const c=document.querySelector('.pcard[data-model="'+m+'"]');if(c){c.querySelectorAll('.szpill').forEach(x=>x.classList.toggle('on',x.dataset.s===s));}});if(d.tmpl){const t=document.querySelector('.tcard2[data-t="'+d.tmpl+'"]');if(t){document.querySelectorAll('.tcard2').forEach(x=>x.classList.remove('open','sel'));t.classList.add('open','sel');}}document.getElementById('handleIn').dispatchEvent(new Event('input',{bubbles:true}));renderCart();saveDraft();return true;}catch(e){return false;}}
function renderCart(){document.getElementById('cartCount').textContent=cart.reduce((a,i)=>a+i.qty,0);
 const box=document.getElementById('cartItems');box.innerHTML=cart.length?'':'<p style="opacity:.5;padding:20px">Your cart is empty — tap Select on any piece.</p>';
 cart.forEach((i,x)=>{const d=document.createElement('div');d.className='cartitem elev-1';
  d.innerHTML='<div style="flex:1"><b>'+i.name+'</b><div style="font-size:11px;opacity:.6">'+i.model+' · size '+i.size+(i.note?' · “'+i.note+'”':'')+'</div></div><span style="opacity:.7">×'+i.qty+'</span><button style="background:none;border:none;color:#ff5e6c;font-size:18px;cursor:pointer" data-x="'+x+'">×</button>';
  d.querySelector('[data-x]').onclick=()=>{cart.splice(x,1);renderCart();};box.appendChild(d);});}

function openSummary(){
 const t=document.querySelector('.tcard2.sel');
 document.getElementById('sumTmpl').innerHTML=t?'<div class="sumrow"><span style="color:'+t.style.getPropertyValue('--tc')+'">\u25c6</span> <b>'+t.querySelector('.tbrand').textContent+'</b></div>':'<div class="sumrow" style="opacity:.6">No template picked yet</div>';
 const onF=[...document.querySelectorAll('.frow .tog.on')].map(x=>x.closest('.frow').querySelector('b').textContent);
 document.getElementById('sumFunc').innerHTML=onF.map(f=>'<div class="sumrow">\u2713 '+f+'</div>').join('')||'<div class="sumrow" style="opacity:.6">none</div>';
 const sp=document.getElementById('sumPieces');
 sp.innerHTML=cart.length?cart.map((c,i)=>'<div class="sumpiece"><span><b>'+c.name+'</b><br><span class="pm">'+c.model+' \u00b7 size '+c.size+(c.note?' \u00b7 \u201c'+c.note+'\u201d':'')+'</span></span><span class="x" data-rm="'+i+'">\u00d7</span></div>').join(''):'<div class="sumrow" style="opacity:.6">No pieces yet</div>';
 sp.querySelectorAll('[data-rm]').forEach(x=>x.onclick=()=>{cart.splice(+x.dataset.rm,1);renderCart();openSummary();});
 document.getElementById('sumVision').textContent=document.getElementById('visionText').value||'(not written yet)';
 document.getElementById('cartDrawer').classList.remove('open');
document.getElementById('sumWrap').classList.add('open');
}
document.getElementById('cartFab').ondblclick=()=>openSummary();
document.getElementById('sumClose').onclick=()=>document.getElementById('sumWrap').classList.remove('open');
document.getElementById('sumBuild').onclick=()=>{document.getElementById('sumWrap').classList.remove('open');draftContract();};
document.addEventListener('click',e=>{const go=e.target.closest&&e.target.closest('[data-go]');if(go){document.getElementById('sumWrap').classList.remove('open');const el=document.getElementById(go.dataset.go);if(el)el.scrollIntoView({behavior:'smooth'});}});
document.addEventListener('click',e=>{if(e.target&&e.target.id==='reviewBtn')openSummary();});
document.getElementById('cartFab').onclick=()=>document.getElementById('cartDrawer').classList.toggle('open');
document.getElementById('closeCart').onclick=()=>document.getElementById('cartDrawer').classList.remove('open');
// dictation
let rec=null;
document.getElementById('dictBtn').onclick=()=>{const SR=window.SpeechRecognition||window.webkitSpeechRecognition;
 if(!SR){const b=document.getElementById('dictBtn');b.textContent='🎙 VOICE NOT AVAILABLE — TAP TO TYPE';const vt=document.getElementById('visionText');vt.placeholder='Voice typing is not available in this browser — type or paste your idea here.';vt.focus();return;}
 if(rec){rec.stop();rec=null;document.getElementById('dictBtn').textContent='START DICTATING';return;}
 rec=new SR();rec.continuous=true;rec.interimResults=true;
 rec.onresult=e=>{let t='';for(const r of e.results)t+=r[0].transcript;document.getElementById('visionText').value=t;};
 rec.onend=()=>{document.getElementById('dictBtn').textContent='START DICTATING';rec=null;};
 rec.start();document.getElementById('dictBtn').textContent='● LISTENING — tap to stop';};
// contract
const FN_MAP = {"Smart Mail":"smart-mail","Smart Lists":"smart-lists","Smart Space":"smart-spaces","Connect + communicate":"connections","Intelligence Today":"intelligence-today","Personal social feed":"feed","Smart Tabs":"smart-tabs","Share":"share","Ask Naya":null,"Reports":"reports","Booking doors":"booking","Guard":null,"Saved":"save","Calendar":null};
function draftContract(){
 const v=document.getElementById('visionText').value||'[not yet — tell Naya your idea in Step 1, that is what she builds from]';
 const h=(document.getElementById('handleIn').value||'').toLowerCase().replace(/[^a-z0-9]/g,'')||'yourname';
 const t=document.querySelector('.tcard2.sel');const tn=t?t.dataset.t:'[not yet — pick your template in Step 4, your pieces land on it]';
 const lines=cart.map(i=>`  - ${i.model} · ${i.name} · size ${i.size} ×${i.qty}${i.note?' · note: '+i.note:''}`);
 const c=`DESIGN BUILD CONTRACT — SMART FACTORY
vision: ${v}
template: ${tn}
pieces (${cart.length} kinds):
${lines.join('\n')||'  (no pieces yet — tap Select on anything you love in Step 3)'}
rules: Naya design laws v1 (white text, edge-only ignition, one board one color, rectangles not squares, 24/18/14 type, mobile-first). Auto-size pieces marked AUTO to the app.\ndelivers to: nayanet.live/${h} — your app, live on NayaNET.`;
 document.getElementById('contract').textContent=c;
 const fnStates={};document.querySelectorAll('.frow').forEach(r=>{const nmEl=r.querySelector('b');const nm=nmEl?nmEl.textContent.trim():'';const id=FN_MAP[nm];const on=r.querySelector('.tog').classList.contains('on');if(id)fnStates[id]=on;else if(on)fnStates['!no-unit:'+nm]=true;});
 const jc={version:"contract-v1",handle:h,idea:document.getElementById('visionText').value||'',vision:document.getElementById('qVision').value||'',do:document.getElementById('qDo').value||'',behave:document.getElementById('qBehave').value||'',template:tn,functions:fnStates,pieces:cart.map(i=>({model:i.model,name:i.name,size:i.size,qty:i.qty,note:i.note||''})),rules:"Naya design laws v1"};
 document.getElementById('contractJson').textContent=JSON.stringify(jc,null,1);
 document.getElementById('contractWrap').style.display='block';
 const nu=document.getElementById('nextUrl');if(nu)nu.textContent='nayanet.live/'+h;
 document.getElementById('contractWrap').scrollIntoView({behavior:'smooth'});}
document.getElementById('buildBtn').onclick=()=>{draftContract();openSummary();};
function copyText(t,done){function ok(){if(done)done(true);}function legacy(){try{const ta=document.createElement('textarea');ta.value=t;ta.style.cssText='position:fixed;top:0;left:0;opacity:0';document.body.appendChild(ta);ta.focus();ta.select();const r=document.execCommand('copy');ta.remove();if(done)done(!!r);}catch(e){if(done)done(false);}}if(window.isSecureContext&&navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t).then(ok).catch(legacy);}else{legacy();}}
document.getElementById('copyBtn').onclick=()=>{copyText(document.getElementById('contract').textContent+"\n\n--- MACHINE CONTRACT ---\n"+document.getElementById('contractJson').textContent,()=>{document.getElementById('copyBtn').textContent='COPIED ✓';});};
document.getElementById('sendNayaBtn').onclick=()=>{copyText(document.getElementById('contract').textContent+"\n\n--- MACHINE CONTRACT ---\n"+document.getElementById('contractJson').textContent,(good)=>{const b=document.getElementById('sendNayaBtn');b.textContent=good?'COPIED ✓ — NOW PASTE IT TO ME IN CHAT':'COPY FAILED — SELECT THE CONTRACT TEXT MANUALLY';document.getElementById('sendHint').style.display='block';});};
document.getElementById('handleIn').addEventListener('input',e=>{const h=e.target.value.toLowerCase().replace(/[^a-z0-9]/g,'')||'yourname';document.getElementById('handlePrev').textContent=h;const nu=document.getElementById('nextUrl');if(nu)nu.textContent='nayanet.live/'+h;});
document.addEventListener('input',()=>saveDraft());
document.addEventListener('click',()=>saveDraft());
if(loadDraft()){const t=document.getElementById('draftToast');t.classList.add('show');setTimeout(()=>t.classList.remove('show'),3500);}
renderCart();
'''

funcs = FUNCS_HTML
HTML = f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Smart Factory — pick your pieces</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#050507;color:#F8F7FB;font-family:Inter,system-ui,sans-serif;padding:0 0 120px}}
.wrap{{max-width:1180px;margin:0 auto;padding:0 24px}}
.topnav{{display:flex;gap:26px;justify-content:center;padding:18px;font-size:12px;letter-spacing:.18em;opacity:.6;border-bottom:1px solid rgba(255,255,255,.07);position:sticky;top:0;background:rgba(5,5,7,.9);backdrop-filter:blur(10px);z-index:50}}
{LIB_CSS}
{ELEV_CSS}
.lawrect{{background:#0c0c11;border:1.5px solid var(--lc);border-radius:12px;padding:16px 18px}}
.lawrect b{{display:block;font-size:11px;letter-spacing:.16em;color:var(--lc);margin-bottom:6px}}
.lawrect span{{font-size:13px;line-height:1.6}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:20px}}
.railblock{{margin:0 0 34px}}
.railhead{{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px}}
.rail{{display:flex;gap:18px;overflow-x:auto;padding:10px 4px 22px;scroll-snap-type:x mandatory}}
.rail::-webkit-scrollbar{{height:8px}}.rail::-webkit-scrollbar-thumb{{background:#2a2a35;border-radius:4px}}
.rail .pcard{{flex:0 0 300px;scroll-snap-align:start}}
.tgrid{{display:flex;flex-direction:column;gap:14px}}
h1{{font-family:'Cormorant Garamond',Georgia,serif;font-size:52px;margin:10px 0}}
section{{margin:64px 0}}
.jw{{font-size:20px;color:var(--j);text-shadow:0 0 12px var(--j)}}
.smarttab{{padding:9px 18px;border-radius:20px;border:1px solid rgba(255,255,255,.2);background:#101016;color:#fff;font-size:13px;cursor:pointer}}
.smarttab.on{{border-color:#a06bff;box-shadow:0 0 12px -4px #a06bff}}
.eco-bb-btn{{width:46px;height:46px;flex:0 0 46px}}
/* ---- mobile breakpoints (intake JSON contract P2, Zeta w444): page claimed mobile-first with 0 @media queries ---- */
@media (max-width:860px){{.wrap{{padding:0 16px}}.topnav{{gap:14px;font-size:10px;padding:14px 8px}}h1{{font-size:36px}}section{{margin:44px 0}}.grid{{grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:14px}}.rail .pcard{{flex:0 0 260px}}}}
@media (max-width:560px){{.topnav{{flex-wrap:wrap;gap:10px;justify-content:flex-start}}h1{{font-size:30px}}body{{padding:0 0 100px}}.rail .pcard{{flex:0 0 230px}}.smarttab{{padding:8px 14px;font-size:12px}}.lawrect{{padding:14px}}}}
</style></head><body>
<nav class="topnav"><span>1 · INTENT</span><span>2 · QUESTIONS</span><span>3 · PIECES</span><span>4 · TEMPLATES</span><span>5 · CONTRACT</span></nav>
<div class="wrap">
<section style="text-align:left;padding-top:36px">
<div class="kicker">THE SMART FACTORY · INTAKE V5</div>
<h1>Your Smart App,<br>piece by piece.</h1>
<p class="lede">Everything here is real, elevated, and selectable. Tap <b>Select</b> on anything you love — it goes in your cart. Pick a size, or leave it on <b>AUTO</b> and Naya sizes it for your app. Then tell Naya your vision and hit <b>Build app</b>.</p>
</section>

<section id="step1"><div class="kicker">STEP 1</div><h2 class="stept">Tell Naya your idea</h2>
<p class="lede">Type it, paste it, dictate it — however your idea comes out.</p><br>
<div class="visioncard elev-2">
<textarea id="visionText" class="visionin carve-2" placeholder="My app is..."></textarea>
<div style="display:flex;gap:12px;margin-top:14px;flex-wrap:wrap">
<button id="dictBtn" class="primo theme-green elev-2" type="button">🎙 START DICTATING</button>
<button class="primo theme-purple elev-2" type="button" onclick="document.getElementById('visionText').focus()">✎ TYPE / PASTE</button>
</div></div></section>

<section id="step2"><div class="kicker">STEP 2</div><h2 class="stept">Answer five questions</h2>
<p class="lede">Plain words — these let Naya draft your contract.</p><br>
<div class="visioncard elev-2">
<label style="font-size:13px;opacity:.7">What is your vision?</label>
<textarea id="qVision" class="visionin carve-2" style="min-height:70px;margin:8px 0 16px" placeholder="Say it like you'd tell a friend."></textarea>
<label style="font-size:13px;opacity:.7">What should it do for you?</label>
<textarea id="qDo" class="visionin carve-2" style="min-height:70px;margin:8px 0 16px" placeholder="Bookings, sales, gathering people..."></textarea>
<label style="font-size:13px;color:#fff">Which functions must it have?</label>
{funcs}
<label style="font-size:13px;opacity:.7">How should it behave?</label>
<textarea id="qBehave" class="visionin carve-2" style="min-height:70px;margin:8px 0 16px" placeholder="Calm, energetic, playful, serious..."></textarea>
<label style="font-size:13px;opacity:.7">Your handle on NayaNET</label>
<input id="handleIn" class="visionin carve-2" style="min-height:20px;margin:8px 0 4px" placeholder="yourname" maxlength="30">
<div style="font-size:12px;opacity:.55;margin-bottom:8px">One word, lowercase, no dashes — this becomes your address: <span style="opacity:.9">nayanet.live/<span id="handlePrev" style="color:#2fe89e">yourname</span></span></div>
</div></section>

<section id="step3"><div class="kicker">STEP 3</div><h2 class="stept">Pick your pieces</h2>
<p class="lede">The real library — every piece numbered. Tap <b>Select</b> and it goes in your cart. Sizes: XS–XL, or AUTO and Naya sizes it for you.</p><br>
{rails}</section>

<section id="step4"><div class="kicker">STEP 4</div><h2 class="stept">Choose your template</h2>
<p class="lede">Twelve starting points. Pick one — your pieces land on it.</p><br>
<div class="tgrid">{tmpls}</div></section>

<section><div class="kicker">STEP 5</div><h2 class="stept">Your build contract</h2>
<p class="lede">Everything you chose, in one contract. Copy it, paste it to Naya, and she builds your app.</p><br>
<button id="buildBtn" class="primo theme-gold elev-3" type="button" style="padding:18px 44px;font-size:16px">★ BUILD APP — DRAFT MY CONTRACT</button>
<div id="contractWrap" style="display:none;margin-top:20px">
<div class="contractbox elev-2" id="contract"></div><details style="margin-top:12px"><summary style="cursor:pointer;font-size:13px;letter-spacing:.1em;opacity:.7">MACHINE CONTRACT (JSON \u2014 what the assembler reads)</summary><pre id="contractJson" style="margin-top:10px;max-height:320px;overflow:auto;font-size:12px;white-space:pre-wrap"></pre></details>
<div style="display:flex;gap:10px;flex-wrap:wrap"><button id="copyBtn" class="primo theme-purple elev-2" type="button" style="margin-top:14px">⧉ COPY CONTRACT</button>
<button id="sendNayaBtn" class="primo theme-green elev-2" type="button" style="margin-top:14px">➤ SEND TO NAYA</button></div>
<p id="sendHint" style="display:none;margin-top:10px;font-size:14px;color:#2fe89e">Contract copied — paste it to me right here in chat and say "build this."</p>
<p style="margin-top:12px;font-size:13px;opacity:.7">Paste it to Naya in chat and say "build this" — she'll know every model number.</p>
<div class="nextbox elev-1"><b>What happens next:</b> Naya takes this contract and builds your app — it lands on your page at <b id="nextUrl">nayanet.live/yourname</b>, live.</div>
</div></section>
</div>

<div id="sumWrap"><div class="sumpanel">
<h2>Make it official.</h2>
<p class="lede" style="margin-bottom:8px">Here is the whole thing &mdash; your app, exactly as you designed it. Change anything, or build it.</p>
<div class="sumsec"><h4>YOUR TEMPLATE <span class="sumchg" data-go="step4">CHANGE &rarr;</span></h4><div id="sumTmpl"></div></div>
<div class="sumsec"><h4>YOUR FUNCTIONS <span class="sumchg" data-go="step2">CHANGE &rarr;</span></h4><div id="sumFunc"></div></div>
<div class="sumsec"><h4>YOUR PIECES <span class="sumchg" data-go="step3">CHANGE &rarr;</span></h4><div id="sumPieces"></div></div>
<div class="sumsec"><h4>YOUR IDEA <span class="sumchg" data-go="step1">CHANGE &rarr;</span></h4><div id="sumVision" class="lede"></div></div>
<button class="sumbtn" id="sumBuild" type="button">BUILD MY APP &mdash; DRAFT THE CONTRACT</button>
<button class="tview" id="sumClose" type="button" style="width:100%;margin-top:12px">KEEP EDITING</button>
</div></div>
<div id="noteWrap"><div class="notebox">
<h3 id="noteTitle">Note</h3>
<p>Tell Naya what this piece should do in your app — she reads every note when she builds.</p>
<textarea id="noteText" class="visionin carve-2" placeholder="This button should..."></textarea>
<div style="display:flex;gap:12px;margin-top:14px">
<button id="noteSave" class="primo theme-green elev-2" type="button" style="flex:1;padding:14px">SAVE NOTE</button>
<button id="noteCancel" class="tview" type="button" style="margin-top:0">CANCEL</button>
</div></div></div>
<div id="draftToast">Draft restored — welcome back.</div>
<button id="cartFab" type="button">🛒<span id="cartCount">0</span></button>
<div id="cartDrawer">
<div style="padding:20px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid rgba(255,255,255,.1)">
<b style="font-size:18px">Your cart</b><button id="closeCart" style="background:none;border:none;color:#fff;font-size:22px;cursor:pointer">×</button></div>
<div id="cartItems" style="flex:1;overflow:auto;padding:8px 0"></div>
<div style="padding:20px;border-top:1px solid rgba(255,255,255,.1)">
<button class="primo theme-gold elev-2" type="button" style="width:100%;padding:16px" onclick="document.getElementById('buildBtn').click();document.getElementById('cartDrawer').classList.remove('open')">★ BUILD APP</button>
<button class="tview" id="reviewBtn" type="button" style="width:100%;margin-top:10px">REVIEW — MAKE IT OFFICIAL</button>
</div></div>
<script>{JS}</script>
</body></html>'''

open(OUT,'w').write(HTML)
print("v5 bytes:", len(HTML))
# STANDING GATE (Naya Zeta w449): regen is RED unless the page's contract emitter matches contract-v1.
# The blob only exists at user-interaction time, so the gate validates the emitter bytes against the spec.
import subprocess
_gate = subprocess.run(["node", os.path.join(os.path.dirname(os.path.abspath(__file__)), "gate_regen_contract.js"), OUT])
if _gate.returncode != 0:
    print("REGEN RED: contract emitter gate failed"); sys.exit(_gate.returncode)
print("contract emitter gate: PASS")
