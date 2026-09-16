from pathlib import Path
import re

FILE=Path('2026 09 15 NayaNETHUB.html')
s=FILE.read_text(encoding='utf-8')

# V11 was a temporary finalizer. Remove it so V10 remains the single visual authority.
s=re.sub(r'<style id="NAYA-SMART-BOARD-V11-GITHUB-FINAL">.*?</style>','',s,flags=re.S)
s=re.sub(r'<script id="NAYA-SMART-BOARD-V11-GITHUB-FINAL">.*?</script>','',s,flags=re.S)

# Keep the architectural Apply layer in the canonical source.
apply_html='<section class="layer" data-naya-layer="apply" style="--layer:#d4af37"><div class="layerHead"><i class="dot"></i><b>HOW TO APPLY / HOW TO USE</b><span class="state">APPLICATION</span></div><div class="layerBody">Turn the insight into one concrete next action: decide what matters, choose the smallest useful move, act within your authority and boundaries, then observe what happened and use the verified result to improve what comes next.</div></section>'
value_pat=re.compile(r'(<section class="layer"[^>]*>\s*<div class="layerHead">\s*<i class="dot"></i>\s*<b>WHAT\'S IN IT FOR YOU\?</b>)',re.I)
if 'HOW TO APPLY / HOW TO USE' not in s:
    s,n=value_pat.subn(apply_html+r'\1',s,count=1)
    if n!=1: raise SystemExit('Could not locate Value layer')

# Replace the V10 surgical style with the final locked typography/spacing authority.
css=r'''<style id="NAYA-SMART-BOARD-V10-SURGICAL-FINAL">
.elite-board:first-child .blockTop{display:flex!important;align-items:center!important;gap:28px!important;margin:0 0 26px!important}.elite-board:first-child .identity{display:flex!important;align-items:center!important;gap:24px!important;min-width:0!important}.elite-board:first-child .glyph{width:116px!important;height:116px!important;flex:0 0 116px!important}.elite-board:first-child .glyph .v10-icon{width:78px!important;height:78px!important}.elite-board:first-child .blockTop h3{font-size:clamp(42px,5.4vw,74px)!important;line-height:.96!important;letter-spacing:-.065em!important;margin:0!important}
.elite-board:first-child .nutshell{margin:0 0 28px!important;padding:0!important;border:2px solid #e3e8efaa!important;border-radius:22px!important;background:linear-gradient(145deg,#171a20,#08090c)!important;overflow:hidden!important}.elite-board:first-child .nutshell b{display:flex!important;align-items:center!important;justify-content:flex-start!important;gap:24px!important;min-height:116px!important;padding:14px 30px!important;text-align:left!important;font-size:18px!important;font-weight:1000!important}.elite-board:first-child .nutshell b .v10-nutshell-star{width:78px!important;height:78px!important;flex:0 0 78px!important;margin:0!important}.elite-board:first-child .nutshell p,.elite-board .layerBody{font-size:14px!important;line-height:1.6!important}.elite-board:first-child .nutshell p{padding:27px 32px 33px!important}.elite-board .layerBody{padding:27px 32px 33px!important}
.elite-board .layers{display:flex!important;flex-direction:column!important;align-items:stretch!important;gap:16px!important;width:100%!important}.elite-board .layer{width:100%!important;display:block!important;float:none!important;overflow:hidden!important}.elite-board .layerHead{display:flex!important;align-items:center!important;gap:28px!important;min-height:116px!important;padding:14px 30px!important}.elite-board .layerHead .dot{width:88px!important;height:88px!important;flex:0 0 88px!important;margin:0!important}.elite-board .dot .v10-icon{width:68px!important;height:68px!important}.elite-board .layerHead b{font-size:18px!important;line-height:1.15!important;letter-spacing:.02em!important;color:#fff!important}.elite-board .layer[data-naya-layer="apply"]{--layer:#d4af37!important;border-color:#d4af376f!important;box-shadow:inset 0 1px #fff3,0 18px 38px #000c,0 0 36px #d4af3740!important}.elite-board .layer[data-naya-layer="value"]{--layer:#dfe6ee!important}.elite-board:first-child .nutshell svg,.elite-board:first-child .nutshell img,.elite-board:first-child .nutshell .nutshellIcon,.elite-board:first-child .nutshell .naya-elite-icon,.elite-board:first-child .nutshell .ico{display:none!important}.elite-board .layerHead .dot{border-radius:50%;background:radial-gradient(circle at 32% 28%,#fff8 0 8%,transparent 9%),radial-gradient(circle at 50% 48%,color-mix(in srgb,var(--layer) 82%,#fff 8%),#07070b 72%);border:2px solid color-mix(in srgb,var(--layer) 70%,#fff 12%);box-shadow:inset 0 2px 3px #fff5,0 0 24px color-mix(in srgb,var(--layer) 45%,transparent),0 12px 24px #000b)}
@media(max-width:820px){.elite-board:first-child .blockTop{gap:16px!important}.elite-board:first-child .identity{gap:16px!important}.elite-board:first-child .glyph{width:78px!important;height:78px!important;flex-basis:78px!important}.elite-board:first-child .glyph .v10-icon{width:54px!important;height:54px!important}.elite-board:first-child .nutshell b,.elite-board .layerHead{min-height:92px!important;padding:11px 18px!important;gap:18px!important}.elite-board:first-child .nutshell b .v10-nutshell-star{width:62px!important;height:62px!important;flex-basis:62px!important}.elite-board .layerHead .dot{width:68px!important;height:68px!important;flex-basis:68px!important}.elite-board .dot .v10-icon{width:50px!important;height:50px!important}.elite-board:first-child .nutshell p,.elite-board .layerBody{font-size:14px!important;line-height:1.58!important;padding:20px 21px 25px!important}.elite-board .layerHead b{font-size:18px!important}}
.top .status{display:none!important}
</style>'''
s,n=re.subn(r'<style id="NAYA-SMART-BOARD-V10-SURGICAL-FINAL">.*?</style>',css,s,count=1,flags=re.S)
if n!=1: raise SystemExit('Expected exactly one V10 surgical style')

# Preserve V10's canonical faceted jewel renderer. Normalize the one legacy Child label statically.
s=re.sub(r'(<div class="layerHead">\s*<i class="dot"></i>\s*<b>)CHILD(</b>)',r'\1CHILD NOTE\2',s,flags=re.I)

# Proof: exactly one V10 surgical style/script and no V11 artifacts.
if len(re.findall(r'id="NAYA-SMART-BOARD-V10-SURGICAL-FINAL"',s))!=2:
    raise SystemExit('V10 surgical style/script authority is not singular')
if 'NAYA-SMART-BOARD-V11-GITHUB-FINAL' in s:
    raise SystemExit('V11 artifact remains')
for marker in ('What is Naya Power','HOW TO APPLY / HOW TO USE','font-size:18px!important','font-size:14px!important'):
    if marker not in s: raise SystemExit(f'missing {marker}')

FILE.write_text(s,encoding='utf-8')
print('WROTE',FILE.stat().st_size)
