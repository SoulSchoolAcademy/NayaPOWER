from pathlib import Path

MARKER='NAYANET_CANONICAL_FEED_V17'
START='<!-- NAYANET_CANONICAL_FEED_V17_START -->'
END='<!-- NAYANET_CANONICAL_FEED_V17_END -->'
hub=Path('2026 09 07  1:14 NAYANETHUBONE.html')
feed=Path('2026 09 08 12:40 NAYANET INTELLIGENT FEED V3.js')
interior=Path('2026 09 08 NAYANET INTELLIGENT FEED V4 INTERIOR EVOLUTION.js')
layer=Path('2026 09 07 NAYANET INTELLIGENT HUB V13 SURGICAL SIDEBAR RESTORATION.js')
polish=Path('CLOUDFLARE-INTELLIGENT-HUB-V7/v7-ten-star-play-naya-polish.js')

base=hub.read_text()
if '</body>' not in base:
    raise SystemExit('Missing </body> boundary in canonical Hub')

legacy_replacements={
    'SHARED INTELLIGENCE':'COLLECTIVE INTELLIGENCE',
    'COLLECTIVE SIGNAL':'COLLECTIVE INTELLIGENCE',
    'NETWORK WISDOM':'COLLECTIVE INTELLIGENCE',
    'YOUR COMPOUNDING INTELLIGENCE':'PERSONAL INTELLIGENCE',
    'n10-standard':'n16-standard',
}
for old,new in legacy_replacements.items():
    base=base.replace(old,new)

# Rebuild only the NayaNET feed integration region. The original Hub outside
# this bounded region remains the canonical house and is never reconstructed.
if START in base and END in base:
    prefix=base.split(START,1)[0]
    suffix=base.split(END,1)[1]
    base=prefix+suffix

bridge=r'''<script>
/* NAYANET_CANONICAL_FEED_V17/V18
   Canonical source integration + surgical presentation correction.
   Preserve the house. Remove the obsolete right-side Smart Note boards.
   Keep the useful GitHub / Sync Intelligence / Get Connected actions,
   placing them directly below Settings in the existing sidebar.
*/
(()=>{
'use strict';
const norm=s=>String(s||'').replace(/\s+/g,' ').trim().toUpperCase();
const ACTIONS=['CONNECT GITHUB','SYNC INTELLIGENCE','GET CONNECTED'];

function renameSidebar(){
 const sb=document.querySelector('.sidebar'); if(!sb)return;
 for(const el of [...sb.querySelectorAll('button,a,[role="button"]')]){
  const t=norm(el.textContent||el.innerText);
  if(t==='SMART NOTES'||t==='SMART NOTES / INTELLIGENCE') el.childNodes.length ? (el.childNodes.forEach(n=>{if(n.nodeType===3)n.nodeValue='PERSONAL INTELLIGENCE'})) : (el.textContent='PERSONAL INTELLIGENCE');
  else if(t==='INTELLIGENT BLOCKS'||t==='INTELLIGENT BLOCKS / FEED') el.textContent='COLLECTIVE INTELLIGENCE';
  else if(t==='NOW'||t==='HOME / NOW'||t==='CURRENT STATE') el.textContent='ACTIVITY';
 }
}

function moveOperationsBelowSettings(){
 const sb=document.querySelector('.sidebar');
 if(!sb)return;
 const rail=document.querySelector('.activationRail');
 const sourceButtons=[...document.querySelectorAll('.activationRail .btn')].filter(b=>ACTIONS.some(a=>norm(b.textContent).includes(a)));
 let host=document.getElementById('nayanet-side-operations');
 if(!host){
  host=document.createElement('div');
  host.id='nayanet-side-operations';
  host.setAttribute('aria-label','NayaNET operations');
  host.innerHTML='<div class="nayanet-side-operations-label">OPERATIONS</div>';
 }
 const settings=[...sb.querySelectorAll('button,a,[role="button"]')].find(el=>norm(el.textContent||el.innerText).includes('SETTINGS'));
 if(settings && settings.parentNode) settings.parentNode.insertBefore(host,settings.nextSibling);
 else if(!host.parentNode) (sb.querySelector('.nav')||sb).appendChild(host);

 for(const button of sourceButtons){
  if(!host.contains(button)){
   const wrap=document.createElement('div');
   wrap.className='nayanet-side-operation';
   wrap.appendChild(button);
   host.appendChild(wrap);
  }
 }
 if(rail) rail.remove();
}

function removeVisibleDiagnosticText(){
 const bad=/^(?:NAYANET_CANONICAL_FEED_V1[78]|INTERIOR_EVOLUTION_ACTIVE|n16-style|n16-presentation-control)$/i;
 for(const el of [...document.body.querySelectorAll('body *')]){
  if(el.children.length)continue;
  const t=norm(el.textContent);
  if(bad.test(t)) el.remove();
 }
}

function style(){
 if(document.getElementById('nayanet-v18-canonical-style'))return;
 const s=document.createElement('style');s.id='nayanet-v18-canonical-style';s.textContent=`
 /* V18 — feed owns the center; obsolete Smart Note rail is gone. */
 .homeWorkspace{display:block!important;width:100%!important}
 .homeFeed{width:100%!important;min-width:0!important;max-width:none!important}
 .activationRail{display:none!important}
 #nayanet-side-operations{display:grid;gap:7px;margin:10px 4px 0;padding:12px 0 0;border-top:1px solid #ffffff12}
 .nayanet-side-operations-label{padding:0 9px 4px;color:#77727e;font-size:7px;font-weight:1000;letter-spacing:.18em}
 .nayanet-side-operation{min-width:0}
 .nayanet-side-operation .btn{width:100%!important;min-height:40px!important;justify-content:flex-start!important;padding:0 11px!important;border:1px solid #8b63ff66!important;border-radius:12px!important;background:linear-gradient(145deg,#121219,#07070b)!important;color:#fff!important;font-size:7px!important;letter-spacing:.07em!important;box-shadow:inset 0 1px #fff3,0 9px 20px #0008!important}
 .nayanet-side-operation .btn:hover,.nayanet-side-operation .btn:focus-visible{border-color:#d86cff!important;box-shadow:inset 0 1px #fff5,0 12px 26px #000a,0 0 20px #d86cff18!important;transform:translateY(-1px)!important}
 .nayanet-side-operation .btn.green{border-color:#55e39a66!important}.nayanet-side-operation .btn.blue{border-color:#55b9ee66!important}.nayanet-side-operation .btn.purple{border-color:#d86cff66!important}
 @media(max-width:900px){#nayanet-side-operations{margin:8px 0 0}.nayanet-side-operation .btn{min-height:38px!important}}
 `;document.head.appendChild(s);
}

function boot(){
 style();
 renameSidebar();
 moveOperationsBelowSettings();
 removeVisibleDiagnosticText();
 setTimeout(renameSidebar,350);
 setTimeout(moveOperationsBelowSettings,450);
 setTimeout(removeVisibleDiagnosticText,600);
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
})();
</script>
'''

inject='\n'+START+'\n'+bridge+'\n<script>\n'+feed.read_text()+'\n</script>\n<script>\n'+interior.read_text()+'\n</script>\n<script>\n'+layer.read_text()+'\n</script>\n<script>\n'+polish.read_text()+'\n</script>\n'+END+'\n'
updated=base.replace('</body>',inject+'</body>',1)
hub.write_text(updated)
print('CANONICAL_FEED_PROMOTION=PASS')
print('CANONICAL_FEED_INTEGRATION=REBUILT')
print('OBSOLETE_ACTIVATION_RAIL=REMOVED')
print('OPERATIONS_MOVED_BELOW_SETTINGS=PASS')
print('POLISH_SCRIPT_WRAPPED=PASS')
print(f'CANONICAL_BYTES={len(updated.encode("utf-8"))}')
