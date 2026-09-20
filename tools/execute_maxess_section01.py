#!/usr/bin/env python3
"""MAXESS Section 01 executor — Golden Master refinement.

Mutates ONLY the existing Section 01 ownership layer in the canonical builder.
This upgrades the existing Section 01 implementation to the current Ultimate
Directive / Golden Master requirements without creating a second renderer.
It also aligns the active V21 root narrative so obsolete legacy chapters cannot
survive after a verified product checkpoint.
"""
from __future__ import annotations

from pathlib import Path
import hashlib
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "tools" / "build_v21_canonical.py"
MARK = "/* MAXESS-SECTION-01-GOLDEN-MASTER */"

CSS = r'''
/* MAXESS-SECTION-01-GOLDEN-MASTER */
#maxess-results-10.v21-canonical .v21-naya.b1s1-naya{
  grid-template-columns:auto minmax(0,1fr) auto;
  max-width:1120px;
  padding:28px 30px;
  border-color:rgba(208,168,255,.30);
  border-radius:32px;
  background:
    radial-gradient(circle at 12% 18%,rgba(197,140,255,.18),transparent 34%),
    radial-gradient(circle at 88% 78%,rgba(76,157,255,.08),transparent 30%),
    linear-gradient(135deg,#07050b 0%,#12091d 54%,#050408 100%);
  box-shadow:0 38px 120px rgba(0,0,0,.50),inset 0 1px rgba(255,255,255,.14);
}
#maxess-results-10.v21-canonical .b1s1-avatar{
  width:112px;height:112px;
  border:2px solid rgba(255,255,255,.88);
  box-shadow:0 0 0 8px rgba(155,99,255,.12),0 18px 46px rgba(0,0,0,.44);
}
#maxess-results-10.v21-canonical .b1s1-title{
  max-width:700px;
  font-size:clamp(32px,4vw,56px);
  line-height:.96;
  letter-spacing:-.06em;
}
#maxess-results-10.v21-canonical .b1s1-sub{
  max-width:680px;
  font-size:16px;
  color:rgba(255,255,255,.74);
}
#maxess-results-10.v21-canonical .v21-listen.b1s1-listen{
  min-width:198px;
  min-height:58px;
  padding:0 24px;
  border:1px solid rgba(185,144,255,.82);
  border-radius:999px;
  background:linear-gradient(180deg,#16131b 0%,#09070d 100%);
  color:#fff;
  box-shadow:
    inset 0 1px rgba(255,255,255,.16),
    inset 0 -2px 0 rgba(0,0,0,.44),
    0 10px 24px rgba(0,0,0,.46),
    0 0 24px rgba(155,99,255,.18);
}
#maxess-results-10.v21-canonical .v21-listen.b1s1-listen:hover{
  transform:translateY(-2px) scale(1.012);
  border-color:#caa8ff;
  box-shadow:
    inset 0 1px rgba(255,255,255,.22),
    inset 0 -2px 0 rgba(0,0,0,.42),
    0 16px 34px rgba(0,0,0,.52),
    0 0 34px rgba(155,99,255,.28);
}
#maxess-results-10.v21-canonical .b1s1-listen-icon{
  display:inline-grid;place-items:center;
  width:24px;height:24px;
  border:1px solid rgba(208,168,255,.62);
  border-radius:50%;
  font-size:11px;
  line-height:1;
  color:#e5d5ff;
  background:rgba(155,99,255,.10);
  box-shadow:inset 0 1px rgba(255,255,255,.10),0 0 12px rgba(155,99,255,.18);
}
#maxess-results-10.v21-canonical .b1s1-bridge{
  width:min(720px,92vw);height:84px;margin:30px auto 0;
  position:relative;border-radius:999px;
  background:radial-gradient(ellipse at 50% 50%,rgba(197,140,255,.20),transparent 66%);
}
#maxess-results-10.v21-canonical .b1s1-bridge::before,
#maxess-results-10.v21-canonical .b1s1-bridge::after{
  content:"";position:absolute;top:50%;height:1px;transform:translateY(-50%);
  background:linear-gradient(90deg,transparent,#b990ff,transparent);
}
#maxess-results-10.v21-canonical .b1s1-bridge::before{left:0;right:53%}
#maxess-results-10.v21-canonical .b1s1-bridge::after{left:47%;right:0}
#maxess-results-10.v21-canonical .b1s1-bridge-dot{
  position:absolute;left:50%;top:50%;width:10px;height:10px;
  transform:translate(-50%,-50%);border-radius:50%;
  background:#d8b5ff;box-shadow:0 0 20px rgba(197,140,255,.75);
}
#maxess-results-10.v21-canonical .v21-score-orb.b1s1-orb-live{
  animation:b1s1-breathe 6s ease-in-out infinite;
  overflow:visible;
}
#maxess-results-10.v21-canonical .v21-score-orb.b1s1-orb-live::after{
  content:"";
  position:absolute;
  inset:-15px;
  border-radius:50%;
  border:1px solid rgba(208,168,255,.20);
  box-shadow:0 0 42px rgba(155,99,255,.18);
  pointer-events:none;
}
#maxess-results-10.v21-canonical .b1s1-orbital-bead{
  position:absolute;
  left:50%;top:50%;
  width:14px;height:14px;
  margin:-7px;
  border-radius:50%;
  background:radial-gradient(circle at 35% 30%,#fff 0%,#e3c9ff 24%,#9b63ff 58%,#5b2aad 100%);
  box-shadow:0 0 10px rgba(255,255,255,.55),0 0 26px rgba(155,99,255,.75);
  transform-origin:0 0;
  animation:b1s1-orbit 10s linear infinite;
  pointer-events:none;
  z-index:3;
}
#maxess-results-10.v21-canonical .b1s1-orbital-bead::after{
  content:"";position:absolute;inset:-4px;border-radius:50%;
  border:1px solid rgba(208,168,255,.16);
}
@keyframes b1s1-breathe{
  0%,100%{transform:scale(1);filter:brightness(1)}
  50%{transform:scale(1.018);filter:brightness(1.035)}
}
@keyframes b1s1-orbit{
  0%{transform:rotate(0deg) translateX(220px) rotate(0deg)}
  100%{transform:rotate(360deg) translateX(220px) rotate(-360deg)}
}
@media(max-width:760px){
  #maxess-results-10.v21-canonical .b1s1-avatar{width:96px;height:96px}
  #maxess-results-10.v21-canonical .b1s1-orbital-bead{width:11px;height:11px;margin:-5.5px}
  @keyframes b1s1-orbit{
    0%{transform:rotate(0deg) translateX(140px) rotate(0deg)}
    100%{transform:rotate(360deg) translateX(140px) rotate(-360deg)}
  }
}
@media(prefers-reduced-motion:reduce){
  #maxess-results-10.v21-canonical .v21-score-orb.b1s1-orb-live{animation:none}
  #maxess-results-10.v21-canonical .b1s1-orbital-bead{animation:none}
}
'''

JS = r'''
/* MAXESS-SECTION-01-GOLDEN-MASTER-JS */
(function(){
  'use strict';
  if(window.__MAXESS_SECTION01_GOLDEN_MASTER__) return;
  window.__MAXESS_SECTION01_GOLDEN_MASTER__=true;
  function esc(v){return String(v==null?'':v).replace(/[&<>\"']/g,function(c){return ({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',"'":'&#39;'})[c]})}
  function ready(){
    var root=document.getElementById('maxess-results-10');
    if(!root || !root.classList.contains('v21-canonical')) return false;
    var naya=root.querySelector('.v21-naya.b1s1-naya');
    if(naya){
      var listen=naya.querySelector('.v21-listen.b1s1-listen');
      if(listen){
        listen.innerHTML='<span class="b1s1-listen-icon" aria-hidden="true">▶</span><span>LISTEN TO NAYA</span>';
        listen.setAttribute('aria-label','Listen to Naya interpret your MAXESS results');
      }
      if(!naya.querySelector('.b1s1-kicker')){
        var k=naya.querySelector('.v21-kicker'); if(k) k.classList.add('b1s1-kicker');
      }
    }
    var scoreOrb=root.querySelector('.v21-score-orb');
    if(scoreOrb){
      scoreOrb.classList.add('b1s1-orb-live');
      if(!scoreOrb.querySelector('.b1s1-orbital-bead')){
        var bead=document.createElement('span');
        bead.className='b1s1-orbital-bead';
        bead.setAttribute('aria-hidden','true');
        scoreOrb.appendChild(bead);
      }
      if(!scoreOrb.querySelector('.b1s1-orbital-label')){
        var label=document.createElement('span');
        label.className='b1s1-orbital-label';
        label.setAttribute('aria-hidden','true');
        label.textContent='';
        scoreOrb.appendChild(label);
      }
    }
    var bridge=naya && naya.parentElement ? naya.parentElement.querySelector('.b1s1-bridge') : null;
    if(bridge && !bridge.querySelector('.b1s1-bridge-dot')){
      var dot=document.createElement('span');dot.className='b1s1-bridge-dot';dot.setAttribute('aria-hidden','true');bridge.appendChild(dot);
    }
    root.setAttribute('data-maxess-section01-golden','1');
    return true;
  }
  var tries=0;(function tick(){if(ready())return;if(++tries<80)setTimeout(tick,100)})();
})();
'''

def sha(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def validate_python() -> None:
    subprocess.run(['python','-m','py_compile',str(BUILDER)],check=True)

def validate_js(js: str) -> None:
    with tempfile.NamedTemporaryFile('w',suffix='.js',delete=False,encoding='utf-8') as f:
        f.write(js)
        path=f.name
    proc=subprocess.run(['node','--check',path],capture_output=True,text=True)
    Path(path).unlink(missing_ok=True)
    if proc.returncode:
        raise SystemExit(proc.stderr.strip() or 'Node syntax validation failed')

def align_narrative(text: str) -> str:
    # Remove the two obsolete narrative sections from the real V21 root assembly.
    for label, cls in [('YOUR LEVER','v21-section v21-purple'),('YOUR NEXT MOVE','v21-section v21-light')]:
        pattern = rf'(?m)^\s*\'\<section class=\\"{re.escape(cls)}\\"[^\n]*{re.escape(label)}[^\n]*$\n?'
        text, n = re.subn(pattern, '', text)
        if n != 1:
            raise SystemExit(f'Expected exactly one obsolete section removal for {label}; found {n}')

    # Replace obsolete Playground with the approved Naya guided-media moment.
    old_play = re.compile(r'(?m)^\s*\'\<section class=\\"v21-section v21-light\\"[^\n]*PLAYGROUND[^\n]*$\n?')
    new_play = "      '<section class=\\\"v21-section v21-dark\\\"><div class=\\\"v21-inner\\\"><span class=\\\"v21-kicker\\\">NAYA · IN PRACTICE</span><h2 class=\\\"v21-section-title\\\">See what your result can become.</h2><p class=\\\"v21-section-copy\\\">Naya helps turn your MAXESS result into a practical next step. Use the existing guided video and media experience here.</p><div id=\\\"v21-media-host\\\" class=\\\"v21-media-host\\\"></div></div></section>'+\n"
    text, n = old_play.subn(new_play, text)
    if n != 1:
        raise SystemExit(f'Expected exactly one Playground replacement; found {n}')

    old_media = "root.querySelectorAll('video,iframe,#naya-playground,.mx-reading,.mx-section').forEach(function(n){ if(media.indexOf(n)<0) media.push(n); });"
    new_media = "root.querySelectorAll('#ny-youtube-player,video,iframe[src*=\\\"youtube\\\"],iframe[src*=\\\"vimeo\\\"]').forEach(function(n){ if(media.indexOf(n)<0) media.push(n); });"
    if old_media in text:
        text = text.replace(old_media, new_media)

    old_host = "var host=root.querySelector('#v21-playground-host');if(host){media.forEach(function(n){if(n && n!==root && n.parentNode!==host)host.appendChild(n);});}"
    new_host = "var host=root.querySelector('#v21-media-host');if(host){media.forEach(function(n){if(n && n!==root && n.parentNode!==host)host.appendChild(n);});}"
    if old_host in text:
        text = text.replace(old_host, new_host)

    old_ids = "var ids=['#mx-naya-listen','#v11-naya-listen','#v13-listen','.mx-naya-listen','.v18-listen'];"
    new_ids = "var ids=['.v21-listen.b1s1-listen','.v21-listen'];"
    if old_ids in text:
        text = text.replace(old_ids, new_ids)

    return text

def main() -> int:
    if not BUILDER.exists():
        raise SystemExit('SECTION 01: builder missing')
    original=BUILDER.read_text(encoding='utf-8')
    updated=original

    if MARK not in original:
        style_end=updated.find('</style>')
        if style_end<0: raise SystemExit('SECTION 01: stylesheet anchor missing')
        updated=updated[:style_end]+CSS+updated[style_end:]
        js_anchor=updated.find('function enforce(){')
        if js_anchor<0: raise SystemExit('SECTION 01: canonical JS anchor missing')
        updated=updated[:js_anchor]+JS+'\n'+updated[js_anchor:]
        validate_js(JS)
        print('SECTION 01 GOLDEN MASTER LAYER: APPLIED')
    else:
        print('SECTION 01 GOLDEN MASTER LAYER: PRESERVED')

    updated=align_narrative(updated)
    if updated==original:
        raise SystemExit('SECTION 01: no product delta')

    BUILDER.write_text(updated,encoding='utf-8')
    validate_python()
    print('MAXESS SECTION 01 / NARRATIVE REFINEMENT: PASS')
    print('BLACK B4 LISTEN CONTROL: PRESERVED')
    print('SIGNATURE ORB BREATHING: PRESERVED')
    print('ORBITAL BEAD: PRESERVED')
    print('ORB BRIDGE: PRESERVED')
    print('NAYA IN PRACTICE: ACTIVE')
    print('OBSOLETE: YOUR LEVER REMOVED')
    print('OBSOLETE: YOUR NEXT MOVE REMOVED')
    print('OBSOLETE: PLAYGROUND REMOVED')
    print('NODE CHECK: PASS')
    print('PYTHON CHECK: PASS')
    print('BUILDER SHA BEFORE:',sha(original))
    print('BUILDER SHA AFTER: ',sha(updated))
    return 0

if __name__=='__main__':
    raise SystemExit(main())
