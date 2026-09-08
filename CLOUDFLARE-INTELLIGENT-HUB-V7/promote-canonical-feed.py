from pathlib import Path

MARKER='NAYANET_CANONICAL_FEED_V17'
hub=Path('2026 09 07  1:14 NAYANETHUBONE.html')
feed=Path('2026 09 08 12:40 NAYANET INTELLIGENT FEED V3.js')
interior=Path('2026 09 08 NAYANET INTELLIGENT FEED V4 INTERIOR EVOLUTION.js')
layer=Path('2026 09 07 NAYANET INTELLIGENT HUB V13 SURGICAL SIDEBAR RESTORATION.js')
polish=Path('CLOUDFLARE-INTELLIGENT-HUB-V7/v7-ten-star-play-naya-polish.js')

base=hub.read_text()
if MARKER in base:
    print('CANONICAL_FEED_PROMOTION=ALREADY_PRESENT')
    raise SystemExit(0)
if '</body>' not in base:
    raise SystemExit('Missing </body> boundary in canonical Hub')

# Promote the proven feed/presentation layers into the visible canonical source.
# This makes the source file itself the inspectable working artifact instead of
# hiding the real product change in a generated deployment-only file.
# The sidebar normalization is deliberately tiny and additive: it does not
# rebuild navigation; it only removes obsolete duplicate feed labels and gives
# the three canonical intelligence views their current names when matching
# existing navigation targets are present.
bridge=r'''<script>
/* NAYANET_CANONICAL_FEED_V17
   Canonical source integration: the visible 1:14 Hub now carries the proven
   Intelligent Feed + interior evolution + presentation layers directly.
   Preserve the house. Change only the feed surface. */
(()=>{
'use strict';
function normalizeSidebar(){
 const sb=document.querySelector('.sidebar'); if(!sb)return;
 const items=[...sb.querySelectorAll('button,a,[role="button"]')];
 for(const el of items){
  const t=String(el.textContent||'').replace(/\s+/g,' ').trim().toUpperCase();
  if(t==='SMART NOTES'||t==='SMART NOTES / INTELLIGENCE') el.textContent='PERSONAL INTELLIGENCE';
  else if(t==='INTELLIGENT BLOCKS'||t==='INTELLIGENT BLOCKS / FEED') el.textContent='COLLECTIVE INTELLIGENCE';
  else if(t==='NOW'||t==='HOME / NOW'||t==='CURRENT STATE') el.textContent='ACTIVITY';
 }
}
function boot(){normalizeSidebar(); setTimeout(normalizeSidebar,350); setTimeout(normalizeSidebar,1200);}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
})();
</script>
'''

inject='\n<!-- NAYANET_CANONICAL_FEED_V17_START -->\n'+bridge+'\n<script>\n'+feed.read_text()+'\n</script>\n<script>\n'+interior.read_text()+'\n</script>\n<script>\n'+layer.read_text()+'\n</script>\n'+polish.read_text()+'\n<!-- NAYANET_CANONICAL_FEED_V17_END -->\n'
updated=base.replace('</body>',inject+'</body>',1)
hub.write_text(updated)
print('CANONICAL_FEED_PROMOTION=PASS')
print(f'CANONICAL_BYTES={len(updated.encode("utf-8"))}')
