from pathlib import Path
import re

FILE=Path('2026 09 15 NayaNETHUB.html')
s=FILE.read_text(encoding='utf-8')
# V10 remains the single canonical visual authority. Only remove temporary/legacy mutation lanes.
s=re.sub(r'<style id="NAYA-SMART-BOARD-V11-GITHUB-FINAL">.*?</style>','',s,flags=re.S|re.I)
s=re.sub(r'<script id="NAYA-SMART-BOARD-V11-GITHUB-FINAL">.*?</script>','',s,flags=re.S|re.I)
s=re.sub(r'<style id="naya-elite-interface-refinement">.*?</style>','',s,flags=re.S|re.I)
s=re.sub(r'<script[^>]*>.*?Naya509NineNoteParser.*?</script>','',s,flags=re.S)
s=re.sub(r'<script[^>]*>.*?naya-509-real-smart-feed.*?</script>','',s,flags=re.S|re.I)
# Remove the older competing Smart Board mutation spine; V10 is the only Smart Board visual normalizer.
s=re.sub(r'<!-- NAYA-CANONICAL-HUB-SPINE-V1 -->.*?</script>','',s,flags=re.S|re.I)
s=s.replace('ADAPTIVE LEARNING','LEARNING LESSON').replace("WHAT'S IN IT FOR YOU?","WHAT'S IN IT FOR YOU")
s=re.sub(r'(<div class="layerHead">\s*<i class="dot"></i>\s*<b>)CHILD(</b>)',r'\1CHILD NOTE\2',s,flags=re.I)
# Make the canonical subject headline correct in source, not only at runtime.
s=re.sub(r'(<h3>)\s*WHAT IS NAYA POWER\?\s*(</h3>)',r'\1What is Naya Power\2',s,count=1,flags=re.I)
apply_html='<section class="layer" data-naya-layer="apply" style="--layer:#d4af37"><div class="layerHead"><i class="dot"></i><b>HOW TO APPLY / HOW TO USE</b><span class="state">APPLICATION</span></div><div class="layerBody">Turn the insight into one concrete next action: decide what matters, choose the smallest useful move, act within your authority and boundaries, then observe what happened and use the verified result to improve what comes next.</div></section>'
value_pat=re.compile(r'(<section class="layer"[^>]*>\s*<div class="layerHead">\s*<i class="dot"></i>\s*<b>WHAT\'S IN IT FOR YOU</b>)',re.I)
if 'HOW TO APPLY / HOW TO USE' not in s:
    s,n=value_pat.subn(apply_html+r'\1',s,count=1)
    if n!=1: raise SystemExit('Could not locate Value layer')
style_pat=re.compile(r'(<style id="NAYA-SMART-BOARD-ELITE-REFINEMENT-V10">)(.*?)(</style>)',re.S|re.I)
m=style_pat.search(s)
if not m: raise SystemExit('Canonical V10 style not found')
css=m.group(2)
repls={'gap:26px!important':'gap:28px!important','gap:20px!important;min-width:0!important':'gap:24px!important;min-width:0!important','gap:18px!important;min-height:116px!important':'gap:24px!important;min-height:116px!important','font-size:13px!important;font-weight:1000':'font-size:18px!important;font-weight:1000','justify-content:center!important;gap:18px!important':'justify-content:flex-start!important;gap:24px!important','font-size:clamp(22px,1.9vw,30px)!important;line-height:1.6!important;color:#f5f7f9':'font-size:14px!important;line-height:1.6!important;color:#f5f7f9','gap:22px!important;min-height:116px!important':'gap:28px!important;min-height:116px!important','.elite-board .layerHead b{font-size:14px!important;':'.elite-board .layerHead b{font-size:18px!important;','.elite-board .layerBody{padding:27px 31px 33px!important;font-size:clamp(22px,1.9vw,30px)!important;':'.elite-board .layerBody{padding:27px 31px 33px!important;font-size:14px!important;','.elite-board .dot{width:64px!important;height:64px!important;flex-basis:64px!important}':'.elite-board .dot{width:68px!important;height:68px!important;flex-basis:68px!important}','.elite-board .dot .v10-icon{width:46px!important;height:46px!important}':'.elite-board .dot .v10-icon{width:50px!important;height:50px!important}','.elite-board:first-child .nutshell p,.elite-board .layerBody{padding:20px 21px 25px!important;font-size:21px!important;line-height:1.58!important}':'.elite-board:first-child .nutshell p,.elite-board .layerBody{padding:20px 21px 25px!important;font-size:14px!important;line-height:1.58!important}'}
for a,b in repls.items(): css=css.replace(a,b)
extra='\n.elite-board .layerHead{padding:16px 26px!important;gap:24px!important}.elite-board .dot{width:78px!important;height:78px!important;flex-basis:78px!important}.elite-board .dot .v10-icon{width:58px!important;height:58px!important}.elite-board .layerBody{font-size:14px!important;line-height:1.6!important}.elite-board:first-child .nutshell b{justify-content:flex-start!important;padding-left:26px!important;gap:24px!important}.elite-board:first-child .nutshell p{font-size:14px!important;line-height:1.6!important}.elite-board .layerHead b{font-size:18px!important;line-height:1.25!important}\n.elite-board .layer[data-naya-layer="apply"]{--layer:#d4af37!important;border-color:#d4af376f!important;box-shadow:inset 0 1px #fff3,0 18px 38px #000c,0 0 36px #d4af3740!important}.elite-board .layer[data-naya-layer="value"]{--layer:#dfe6ee!important}\n.top .status{display:none!important}\n'
# Keep one final authoritative override block; repeated runs remain idempotent.
css=re.sub(r'\n\.elite-board \.layerHead\{padding:16px 26px!important;.*?\.top \.status\{display:none!important\}\n','\n',css,flags=re.S)
css=css.rstrip()+extra
s=style_pat.sub(m.group(1)+css+m.group(3),s,count=1)
# The live clock is the visible board timestamp. The first Smart Board's metadata uses the same timestamp,
# with a quiet semantic category instead of an internal Smart Note/build designation.
date_expr="new Intl.DateTimeFormat(undefined,{weekday:'short',month:'short',day:'numeric',year:'numeric',hour:'numeric',minute:'2-digit'}).format(new Date())"
s=re.sub(r"(const topTitle=document\.getElementById\('topTitle'\);if\(topTitle\))topTitle\.textContent='Smart Notes'",r"\1topTitle.textContent="+date_expr,s)
# Remove the literal legacy emoji/text node before installing the canonical jewel SVG.
s=s.replace("if(g){g.querySelectorAll('svg,img,.ico,.naya-elite-icon').forEach(x=>x.remove());jewel(g,'power')}","if(g){g.textContent='';jewel(g,'power')}")
# Keep the first board's visible metadata clean and current.
needle="if(h && index===0) h.textContent='What is Naya Power';"
replacement=needle+"\n    if(index===0){const meta=b.querySelector('.meta');if(meta){const spans=meta.querySelectorAll('span');if(spans[0])spans[0].textContent=new Intl.DateTimeFormat(undefined,{weekday:'short',month:'short',day:'numeric',year:'numeric',hour:'numeric',minute:'2-digit'}).format(new Date());if(spans[1])spans[1].textContent='·';if(spans[2])spans[2].textContent='AI / SYSTEM';}}"
s=s.replace(needle,replacement)
if len(re.findall(r'id="NAYA-SMART-BOARD-ELITE-REFINEMENT-V10"',s))!=2: raise SystemExit('Expected exactly one V10 style + one V10 script')
for bad in ('NAYA-SMART-BOARD-V11-GITHUB-FINAL','NAYA-SMART-BOARD-V10-SURGICAL-FINAL','naya-elite-interface-refinement','Naya509NineNoteParser','naya-509-real-smart-feed-','NAYA-CANONICAL-HUB-SPINE-V1'):
    if bad in s: raise SystemExit('Legacy Smart Board artifact remains: '+bad)
for marker in ('What is Naya Power','LEARNING LESSON',"WHAT'S IN IT FOR YOU",'HOW TO APPLY / HOW TO USE','font-size:18px!important','font-size:14px!important','core','facet','shade','edge','Intl.DateTimeFormat','g.textContent=\'\''):
    if marker not in s: raise SystemExit(f'missing {marker}')
FILE.write_text(s,encoding='utf-8')
print('WROTE',FILE.stat().st_size)
