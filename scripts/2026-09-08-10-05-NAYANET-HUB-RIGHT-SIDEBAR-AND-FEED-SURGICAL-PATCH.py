from pathlib import Path

# 2026-09-08 10:20 — execute the locked current Hub mission against the exact timestamped HTML artifact.
TARGET = Path('2026 09 08 9:59 NAYANET HUB.html')
MARKER = 'NAYANET-HUB-RIGHT-SIDEBAR-FEED-MIRROR-V1'

CSS = '''<style id="nayanet-right-sidebar-feed-mirror-style">
/* NAYANET-HUB-RIGHT-SIDEBAR-FEED-MIRROR-V1 — surgical current Hub overlay */
.activationRail{display:none!important}
.homeWorkspace{display:block!important;grid-template-columns:1fr!important}
.homeFeed{width:100%!important;max-width:none!important}
#nayanet-elite-feed{width:100%!important;max-width:none!important}
.nhm-actions{display:flex;gap:8px;flex-wrap:wrap;margin:16px 18px 18px;padding-top:14px;border-top:1px solid #ffffff14}
.nhm-actions button{min-height:40px;padding:0 13px;border:1px solid #8b63ff66;border-radius:11px;background:linear-gradient(145deg,#17111f,#08080c);color:#fff;font-size:8px;font-weight:1000;letter-spacing:.05em;box-shadow:inset 0 1px #fff4,0 8px 18px #0009;transition:.2s ease}
.nhm-actions button:hover,.nhm-actions button.active{border-color:#d86cff;box-shadow:0 0 22px #d86cff22;transform:translateY(-1px)}
.nhm-actions .rank{color:#ffd98a}.nhm-actions .comment{border-color:#55b9ee66}
@media(max-width:900px){.activationRail{display:none!important}.homeWorkspace{display:block!important}.nhm-actions button{flex:1 1 auto}}
</style>'''

JS = '''<script id="nayanet-right-sidebar-feed-mirror-runtime">
(()=>{
'use strict';
const ROOT='#nayanet-elite-feed';
const clean=s=>String(s||'').replace(/\\s+/g,' ').trim();
const readState=()=>{try{return JSON.parse(localStorage.getItem('nayanet:feed-mirror-actions')||'{}')}catch{return{}}};
const saveState=s=>{try{localStorage.setItem('nayanet:feed-mirror-actions',JSON.stringify(s))}catch{}};
const keyFor=b=>clean(b.querySelector('.n3-title,.blockTitle h3')?.textContent||b.id||'intelligent-block').toLowerCase().replace(/[^a-z0-9]+/g,'-').slice(0,90);
function addActions(block){
 if(block.querySelector('.nhm-actions'))return;
 const title=clean(block.querySelector('.n3-title,.blockTitle h3')?.textContent||'Intelligent Block');
 const key=keyFor(block),st=readState(),a=st[key]||{};
 const bar=document.createElement('div');bar.className='nhm-actions';
 bar.innerHTML='<button data-a="share">＋ SHARE</button><button data-a="like">👍 LIKE</button><button data-a="love">♥ LOVE</button><button class="rank" data-a="rank">★ RANK</button><button class="comment" data-a="comment">💬 COMMENT</button><button data-a="save">🔖 SAVE</button>';
 bar.querySelectorAll('button').forEach(btn=>{
   const k=btn.dataset.a;
   if(a[k])btn.classList.add('active');
   if(k==='rank'&&a.rank)btn.textContent='★ RANK '+a.rank+'/5';
   if(k==='comment'&&a.comments?.length)btn.textContent='💬 COMMENT '+a.comments.length;
   btn.onclick=()=>{
     const s=readState();s[key]=s[key]||{};const x=s[key];
     if(k==='share'){
       const text=title+'\\n\\n'+clean(block.querySelector('.n3-nutshell p,.blockBody p,.perspective p')?.textContent||'')+'\\n\\nNayaNET — Create. Connect. Grow with US.';
       if(navigator.share)navigator.share({title,text,url:location.href}).catch(()=>{});
       else if(navigator.clipboard)navigator.clipboard.writeText(text).then(()=>{btn.textContent='✓ COPIED';setTimeout(()=>btn.textContent='＋ SHARE',1200)});
       return;
     }
     if(k==='comment'){
       const text=prompt('Add a comment to this Intelligent Block:');if(!text?.trim())return;
       x.comments=x.comments||[];x.comments.push({text:text.trim(),createdAt:new Date().toISOString()});btn.textContent='💬 COMMENT '+x.comments.length;saveState(s);return;
     }
     if(k==='rank'){
       const n=Number(prompt('How valuable is this intelligence? Enter 1–5.',x.rank||''));if(!Number.isFinite(n)||n<1||n>5)return;
       x.rank=Math.round(n);btn.textContent='★ RANK '+x.rank+'/5';saveState(s);return;
     }
     x[k]=!x[k];btn.classList.toggle('active',!!x[k]);saveState(s);
   };
 });
 const footer=block.querySelector('.n3-footer,.blockFooter');
 if(footer)footer.insertAdjacentElement('beforebegin',bar);else block.appendChild(bar);
}
function decorate(){document.querySelectorAll(ROOT+' .n3-block,'+ROOT+' .intelligentBlock').forEach(addActions)}
function captureCanonical(){
 const feed=document.querySelector(ROOT);if(!feed)return null;
 const first=feed.querySelector('.n3-block');return first?first.cloneNode(true):null;
}
let canonical=null;
function mirrorActivity(){
 const feed=document.querySelector(ROOT),body=feed?.querySelector('.n3-body');if(!body)return;
 const events=[...body.querySelectorAll('.n3-event')];if(!events.length)return;
 if(!canonical)canonical=captureCanonical();
 if(!canonical)return;
 const source=canonical.cloneNode(true);
 const eventData=events.map(e=>({title:clean(e.querySelector('b')?.textContent||'ACTIVITY'),text:clean(e.querySelector('p')?.textContent||'')}));
 body.innerHTML=eventData.map((ev,i)=>{
   const b=source.cloneNode(true);b.dataset.nhmActivity='1';
   const title=b.querySelector('.n3-title');if(title)title.textContent=ev.title;
   const nut=b.querySelector('.n3-nutshell p');if(nut)nut.textContent=ev.text;
   const eye=b.querySelector('.n3-eyebrow');if(eye)eye.innerHTML='<span class="n3-led"></span><b>INTELLIGENT BLOCK</b> · ACTIVITY · EVENT '+String(i+1).padStart(2,'0');
   return b.outerHTML;
 }).join('');
 decorate();
}
function guard(){
 const rail=document.querySelector('.activationRail');if(rail)rail.style.setProperty('display','none','important');
 const ws=document.querySelector('.homeWorkspace');if(ws)ws.style.setProperty('grid-template-columns','1fr','important');
 decorate();
 const active=document.querySelector(ROOT+' .n3-tab.active');
 if(active?.dataset.view==='activity')setTimeout(mirrorActivity,0);
}
function observe(){
 const feed=document.querySelector(ROOT);if(!feed||feed.dataset.nhmObserver)return;feed.dataset.nhmObserver='1';
 const obs=new MutationObserver(()=>{guard()});obs.observe(feed,{subtree:true,childList:true});
}
function boot(){
 guard();observe();
 document.addEventListener('click',e=>{if(e.target.closest(ROOT+' .n3-tab'))setTimeout(()=>{guard();if(e.target.closest(ROOT+' .n3-tab')?.dataset.view==='activity')mirrorActivity()},20)},true);
 let n=0;const t=setInterval(()=>{guard();if(++n>20)clearInterval(t)},300);
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
})();
</script>'''


def apply():
    if not TARGET.exists():
        raise FileNotFoundError(f'Current canonical Hub artifact not found: {TARGET}')
    html = TARGET.read_text(encoding='utf-8')
    if MARKER in html:
        return False
    payload = CSS + '\n' + JS + '\n<!-- ' + MARKER + ' -->\n'
    if '</head>' not in html:
        raise RuntimeError('Current Hub artifact has no </head> insertion point; refusing destructive reconstruction.')
    html = html.replace('</head>', payload + '</head>', 1)
    TARGET.write_text(html, encoding='utf-8')
    return True

if __name__ == '__main__':
    print('PATCHED' if apply() else 'ALREADY_PATCHED')
'''
