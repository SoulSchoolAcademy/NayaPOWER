#!/usr/bin/env python3
"""Bridge presentation FIX #2 (2026-11-17) — welcome file build.

Base: the presentation welcome, rebuilt deterministically from the
presentation round's builder (../bridge-presentation-20261117/
build-bridge-presentation.py), which itself builds from the bridge-page-fix
welcome. Base must verify: 1,132,653 B, sha256 9eea1703... (blob 2cd15b96).
Out: welcome-fix2.html (stdout; shell redirect does the write, because
python writes are EPERM-blocked in this window).

Every change is an anchored replacement with an exact-occurrence check.
If any anchor is missing or occurs an unexpected number of times, the
script fails loudly and writes nothing.

D1 — W8 broke script block 1: the dedupe edit's `else if(...){...}` line
  already closes itself, leaving the lone `}` (block-1 line 237) to close
  the outer `try{` (line 220) with no catch — the whole block is dead at
  parse time on every load ("Missing catch or finally after try"). FIX:
  delete that one stray `}`. The try then closes at the `}catch(e){}`
  (line 266) as it always did; the dedupe code itself is untouched.
D2 — `?stage=deck` never lands: the restore block (end of script block 2)
  runs AFTER the hook in the same init, and render() saves 'bridge' for
  the deck view (the A2 browser-back rule), so the restore reads 'bridge'
  and calls enterStage(), clobbering the deck the hook just landed. FIX:
  the restore stands down when the URL carried a stage the hook handled
  (`_fpStage` is the hook's own var, same IIFE scope). render()'s
  deck->'bridge' save is NOT touched — the A2 rule stands.
D3 — corner emblems overlap the kicker: the head shrink-wraps to its
  widest child (the title, 482px), so the kicker spans the head's full
  width and the head's top corners sit ON the kicker line (44x15px at
  1920/635; 26x30px + viewport-clipped at 390). FIX: the top pair moves
  UP into the empty logo gap above the head (the logo is centred, so the
  emblems flank it without touching it); the bottom pair stays flanking
  the title/sub, where it reads clean. At <=480px the emblems sit 8px
  inside the head's edges, so no rotated corner leaves the viewport at
  390. Angles and the die-cut are unchanged.
D4 — W6 fails at 635/390: the presentation round's wrap override made
  the legal strip 150px tall at 635 / 226px at 390, taller than the 72px
  bar lift, so it struck through the bar, the board text and Continue.
  FIX: delete the wrap override — the bridge strip rule already sets
  flex-wrap:nowrap + overflow-x:auto, so the strip stays ONE ROW (~53px)
  at every width and the 72px lift clears it. Also fixes the stale W6
  comment (it described an eyebrow-shrink rule that never existed).
"""
import hashlib
import subprocess
import sys

HERE = '/home/hatch/workspace/team-nitro/bridge-presentation-fix2-20261117'
PRES = '/home/hatch/workspace/team-nitro/bridge-presentation-20261117/build-bridge-presentation.py'

p = subprocess.run([sys.executable, PRES], capture_output=True)
if p.returncode != 0:
    sys.stderr.write(p.stderr.decode('utf-8', 'replace'))
    sys.exit('FIX2: presentation builder failed')
s = p.stdout.decode('utf-8')
ORIG_LEN = len(s)
sha = hashlib.sha256(s.encode()).hexdigest()
print(f'# base: {len(s)} chars, {len(s.encode())} B, sha256 {sha[:16]}', file=sys.stderr)
assert len(s.encode()) == 1132653, 'FIX2: base size moved'
assert sha.startswith('9eea1703'), 'FIX2: base is not the presentation welcome (9eea1703)'


def rep(old, new, count=1, label=''):
    global s
    n = s.count(old)
    assert n == count, f'REP FAIL [{label}]: anchor occurs {n}x, expected {count}x :: {old[:90]!r}'
    s = s.replace(old, new)
    print(f'# rep ok [{label}]', file=sys.stderr)


# ---------------------------------------------------------------- D1: delete the stray `}` (block-1 line 237)
rep('}catch(e){} }\n    }\n    var others=',
    '}catch(e){} }\n    var others=',
    1, 'D1 stray brace out (try/catch balance restored)')

# ---------------------------------------------------------------- D2: restore stands down when ?stage= was handled
rep("""  try{
    if(localStorage.getItem('nayanet_fp_stage')==='agree'){enterStage();S.view='agree';S.all=null;render();}
     else if(localStorage.getItem('nayanet_fp_stage')==='bridge'){enterStage();}
  }catch(e){}""",
    """  /* BRIDGE PRESENTATION FIX #2 (2026-11-17) — D2: ?stage=deck never
     landed. The hook above calls enterStage()+goResume() for ?stage=deck,
     and render() saves 'bridge' for the deck view (the A2 browser-back
     rule), so this restore block — running after the hook in the same
     init — read 'bridge' and dragged the deck back to the bridge. When
     the URL carried a stage the hook handled, the restore stands down.
     render()'s deck->'bridge' save is untouched: the A2 rule stands. */
  try{
    var _fpRestoreStage=(_fpStage==='deck'||_fpStage==='letter'||_fpStage==='bridge')?null:localStorage.getItem('nayanet_fp_stage');
    if(_fpRestoreStage==='agree'){enterStage();S.view='agree';S.all=null;render();}
     else if(_fpRestoreStage==='bridge'){enterStage();}
  }catch(e){}""",
    1, 'D2 restore guard')

# ---------------------------------------------------------------- D3: top emblems up into the logo gap; phone inset
rep(""".fp-bridge-corner-tl{top:-10px;left:-4px;transform:rotate(-20deg)}
.fp-bridge-corner-tr{top:-10px;right:-4px;transform:rotate(20deg)}
.fp-bridge-corner-bl{bottom:-10px;left:-4px;transform:rotate(20deg)}
.fp-bridge-corner-br{bottom:-10px;right:-4px;transform:rotate(-20deg)}
@media(max-width:480px){.fp-bridge-corners .fp-bridge-emblem{width:40px;height:40px}}""",
    """/* ---- BRIDGE PRESENTATION FIX #2 (2026-11-17, D3) ----
   The top pair sat ON the kicker (44x15px at 1920/635, clipped at 390):
   the head shrink-wraps to its widest child (the title, 482px), so the
   kicker spans the head's full width and the head's top corners are ON
   the kicker line. The top pair moves UP into the empty logo gap above
   the head (the logo is centred, so the emblems flank it without
   touching it); the bottom pair stays flanking the title/sub, where it
   reads clean. At <=480px the emblems sit 8px inside the head's edges,
   so no rotated corner leaves the viewport at 390. Angles and the
   die-cut are unchanged. */
.fp-bridge-corner-tl{top:-76px;left:-4px;transform:rotate(-20deg)}
.fp-bridge-corner-tr{top:-76px;right:-4px;transform:rotate(20deg)}
.fp-bridge-corner-bl{bottom:-10px;left:-4px;transform:rotate(20deg)}
.fp-bridge-corner-br{bottom:-10px;right:-4px;transform:rotate(-20deg)}
@media(max-width:480px){.fp-bridge-corners .fp-bridge-emblem{width:40px;height:40px}
.fp-bridge-corner-tl{top:-56px;left:8px}
.fp-bridge-corner-tr{top:-56px;right:8px}
.fp-bridge-corner-bl{left:8px}
.fp-bridge-corner-br{right:8px}}""",
    1, 'D3 emblems off the kicker')

# ---------------------------------------------------------------- D4: strip stays one row; stale comment fixed
rep("""/* ---- BRIDGE PRESENTATION (2026-11-17, BRIEF-BRIDGE-PRESENTATION-20261117.md §7b) ----
   The stage bottom bar rides ABOVE the fixed legal strip in bridge view:
   the strip painted over the bar (same bottom:0, later in the DOM) and
   half-buried 'Back to the login'. At phone widths the legal links wrap
   instead of overflowing, and the bar rides higher to clear the taller
   wrapped strip. The centred eyebrow lines shrink at phone widths so
   their span clears the ‹ Login button at the left. */
body.fp-stage-on.fp-bridge #fpStageBarB{bottom:44px}
@media(max-width:640px){
html.fp-locked body.fp-stage-on.fp-bridge #fpLegal .fp-legal-links{flex-wrap:wrap;justify-content:center;overflow-x:visible}
body.fp-stage-on.fp-bridge #fpStageBarB{bottom:72px}
body.fp-stage-on #fpStageBarT .fp-dots{display:none}
}""",
    """/* ---- BRIDGE PRESENTATION FIX #2 (2026-11-17, D4) ----
   The stage bottom bar rides ABOVE the fixed legal strip in bridge view:
   the strip painted over the bar (same bottom:0, later in the DOM) and
   half-buried 'Back to the login'. The strip stays ONE ROW at every
   width: the bridge strip rule already sets flex-wrap:nowrap +
   overflow-x:auto, so the links scroll sideways instead of wrapping —
   the presentation round's wrap override made the strip 150px tall at
   635 and 226px at 390, taller than any lift, and it struck through
   the bar, the board text and Continue. No wrap override here: the
   72px lift clears the one-row strip (~53px) with room to spare.
   (The old comment described an eyebrow-shrink rule that never
   existed; it is gone.) */
body.fp-stage-on.fp-bridge #fpStageBarB{bottom:44px}
@media(max-width:640px){
body.fp-stage-on.fp-bridge #fpStageBarB{bottom:72px}
body.fp-stage-on #fpStageBarT .fp-dots{display:none}
}""",
    1, 'D4 strip one row + comment')

# ---------------------------------------------------------------- self-checks (bytes, not claims)
assert s.count("}catch(e){} }\n    }\n    var others=") == 0, 'D1: stray brace still present'
assert s.count('_fpRestoreStage') == 3, 'D2: guard not in place'
assert s.count('top:-76px') == 2, 'D3: desktop top pair not moved'
assert s.count('top:-56px') == 2, 'D3: phone top pair not moved'
assert s.count('html.fp-locked body.fp-stage-on.fp-bridge #fpLegal .fp-legal-links{flex-wrap:wrap') == 0, 'D4: wrap override still present'
assert 'welcome-staged' not in s, 'words: welcome-staged leaked in'
assert s.count('centred eyebrow lines shrink') == 0, 'D4: stale comment still present'
assert s.count('The centred eyebrow lines') == 0, 'D4: stale comment still present'

print(f'# done: {ORIG_LEN} -> {len(s)} chars, sha256 {hashlib.sha256(s.encode()).hexdigest()[:16]}', file=sys.stderr)
sys.stdout.write(s)
