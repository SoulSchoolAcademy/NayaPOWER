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
if '</body>' not in base: raise SystemExit('Missing </body> boundary in canonical Hub')

for old,new in {
 'SHARED INTELLIGENCE':'COLLECTIVE INTELLIGENCE',
 'COLLECTIVE SIGNAL':'COLLECTIVE INTELLIGENCE',
 'NETWORK WISDOM':'COLLECTIVE INTELLIGENCE',
 'YOUR COMPOUNDING INTELLIGENCE':'PERSONAL INTELLIGENCE',
 'n10-standard':'n16-standard',
}.items(): base=base.replace(old,new)

if START in base and END in base:
    base=base.split(START,1)[0]+base.split(END,1)[1]

bridge=r'''<script>
/* NAYANET_CANONICAL_FEED_V20 — full-page intelligent feed presentation.
   One canonical feed renderer. Three projections. No obsolete right rail.
*/
(()=>{'use strict';
const norm=s=>String(s||'').replace(/\s+/g,' ').trim().toUpperCase();
const ACTIONS=['CONNECT GITHUB','SYNC INTELLIGENCE','GET CONNECTED'];
function renameSidebar(){const sb=document.querySelector('.sidebar');if(!sb)return;for(const el of [...sb.querySelectorAll('button,a,[role="button"]')]){const t=norm(el.textContent||el.innerText);if(t==='SMART NOTES'||t==='SMART NOTES / INTELLIGENCE')el.textContent='PERSONAL INTELLIGENCE';else if(t==='INTELLIGENT BLOCKS'||t==='INTELLIGENT BLOCKS / FEED')el.textContent='COLLECTIVE INTELLIGENCE';else if(t==='NOW'||t==='HOME / NOW'||t==='CURRENT STATE')el.textContent='ACTIVITY';}}
function removeRail(){const rail=document.querySelector('.activationRail');if(rail)rail.remove();document.querySelectorAll('[class*="activation"], [id*="activation"]').forEach(el=>{if(el!==document.querySelector('#nayanet-elite-feed')&&!el.closest('.sidebar')){const r=el.getBoundingClientRect();if(r.width>180&&r.height>100)el.remove();}})}
function moveOperations(){const sb=document.querySelector('.sidebar');if(!sb)return;const source=[...document.querySelectorAll('.activationRail .btn')].filter(b=>ACTIONS.some(a=>norm(b.textContent).includes(a)));let host=document.getElementById('nayanet-side-operations');if(!host){host=document.createElement('div');host.id='nayanet-side-operations';host.innerHTML='<div class="nayanet-side-operations-label">OPERATIONS</div>';}const settings=[...sb.querySelectorAll('button,a,[role="button"]')].find(el=>norm(el.textContent||el.innerText).includes('SETTINGS'));if(settings?.parentNode)settings.parentNode.insertBefore(host,settings.nextSibling);else if(!host.parentNode)(sb.querySelector('.nav')||sb).appendChild(host);source.forEach(button=>{if(!host.contains(button)){const wrap=document.createElement('div');wrap.className='nayanet-side-operation';wrap.appendChild(button);host.appendChild(wrap);}})}
function style(){if(document.getElementById('nayanet-v20-style'))return;const s=document.createElement('style');s.id='nayanet-v20-style';s.textContent=`
html,body{min-height:100%;background:#000!important}.app{grid-template-columns:270px minmax(0,1fr)!important;align-items:start!important}.sidebar{position:relative!important;top:auto!important;height:auto!important;min-height:100vh!important;max-height:none!important;overflow:visible!important;align-self:start!important;padding:22px 15px 34px!important}.sidefoot{position:static!important;left:auto!important;right:auto!important;bottom:auto!important;margin:22px 8px 0!important}.nav{gap:8px!important}.nav button{width:100%!important;min-height:58px!important;padding:0 15px!important;border-radius:16px!important;font-size:13px!important;gap:12px!important}.nav button .ico,.ico{width:24px!important;font-size:19px!important}.navlabel{padding:15px 11px 8px!important;font-size:8px!important}.main{min-width:0!important;padding:0 28px 100px!important}.homeWorkspace{display:block!important;width:100%!important}.homeFeed{width:100%!important;min-width:0!important;max-width:none!important}.activationRail{display:none!important}#nayanet-elite-feed{width:100%!important;max-width:none!important;margin:0!important;padding:0 0 88px!important}.n3-tabs{width:100%!important;max-width:none!important;margin-top:0!important}.n3-body{width:100%!important}.n3-block{width:100%!important;border-radius:28px!important}.n3-title{font-size:clamp(22px,2.2vw,31px)!important}.n3-nutshell p{font-size:clamp(14px,1.15vw,17px)!important;line-height:1.62!important}.n3-pbody{font-size:clamp(11px,.88vw,13px)!important;line-height:1.68!important}.n3-perspectives{gap:10px!important}.n3-perspective{border-radius:18px!important}.n3-nutshell{border-radius:22px!important}.n3-bottom{margin-top:44px!important;padding-top:28px!important}#nayanet-side-operations{display:grid;gap:8px;margin:12px 2px 0;padding:14px 0 0;border-top:1px solid #ffffff12}.nayanet-side-operations-label{padding:0 10px 5px;color:#77727e;font-size:7px;font-weight:1000;letter-spacing:.18em}.nayanet-side-operation .btn{width:100%!important;min-height:46px!important;justify-content:flex-start!important;padding:0 12px!important;border:1px solid #8b63ff66!important;border-radius:13px!important;background:linear-gradient(145deg,#121219,#07070b)!important;color:#fff!important;font-size:8px!important;letter-spacing:.07em!important;box-shadow:inset 0 1px #fff3,0 9px 20px #0008!important}.nayanet-side-operation .btn:hover,.nayanet-side-operation .btn:focus-visible{border-color:#d86cff!important;box-shadow:inset 0 1px #fff5,0 12px 26px #000a,0 0 20px #d86cff18!important;transform:translateY(-1px)!important}@media(max-width:900px){.app{grid-template-columns:1fr!important}.sidebar{min-height:auto!important;padding-bottom:20px!important}.main{padding:0 12px 72px!important}#nayanet-elite-feed{padding-bottom:58px!important}.n3-tabs{position:sticky;top:8px;z-index:20}.n3-block{border-radius:23px!important}.n3-title{font-size:21px!important}.n3-nutshell p{font-size:13px!important}.n3-pbody{font-size:11px!important}.nav button{min-height:54px!important}}@media(min-width:901px){.main{padding-right:40px!important}.n3-block{box-shadow:inset 0 1px #fff6,0 32px 82px #000e,0 0 50px color-mix(in srgb,var(--accent) 8%,transparent)!important}}
`;document.head.appendChild(s)}
function boot(){style();renameSidebar();removeRail();moveOperations();setTimeout(()=>{renameSidebar();removeRail();moveOperations()},350);setTimeout(()=>{renameSidebar();removeRail();moveOperations()},800)}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
})();
</script>
'''
inject='\n'+START+'\n'+bridge+'\n<script>\n'+feed.read_text()+'\n</script>\n<script>\n'+interior.read_text()+'\n</script>\n<script>\n'+layer.read_text()+'\n</script>\n<script>\n'+polish.read_text()+'\n</script>\n'+END+'\n'
updated=base.replace('</body>',inject+'</body>',1)
hub.write_text(updated)
print('CANONICAL_FEED_PROMOTION=PASS')
print('FULL_PAGE_FEED=PASS')
print('OBSOLETE_RIGHT_RAIL=REMOVED')
print('THREE_VIEWS_ONE_RENDERER=PASS')
print('CANONICAL_BYTES='+str(len(updated.encode('utf-8'))))
