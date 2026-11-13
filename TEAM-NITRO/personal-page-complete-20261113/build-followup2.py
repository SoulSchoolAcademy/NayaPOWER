#!/usr/bin/env python3
"""PERSONAL-COMPLETE FOLLOW-UP build, pass 2 — 2026-11-13 (maker seat).
Restores the original re-tap-to-close behaviour the first probe found missing:
the original floating pluses rose above the drawer when open (z-index 970,
icon rotated to an x) — the bottom bar sits at z-index 45, so the scrim (950)
covered it entirely and no seg could be re-tapped while a drawer was open.
This pass raises the bar to 955 while a drawer is open (above the scrim 950,
below the drawer 960), lights the open drawer's seg, and closes the drawer
first when any other seg is tapped. At phone widths the drawer still covers
the bar geometrically, so the scrim tap / Escape close it there.

Base: SHA 31890cf1... (follow-up pass 1) or the script stops.
"""
import hashlib, difflib

WT = "/home/hatch/workspace/personal-complete-wt/TEAM-NITRO/personal-page-complete-20261113/personal-complete.html"
BASE_SHA = "31890cf1fb6c53f3f81663521cd5ec178cc692831800fd646564d7c5cf2b2683"
OUT = "/home/hatch/workspace/team-nitro/personal-page-complete-20261113"

def sha(b): return hashlib.sha256(b).hexdigest()

with open(WT, "rb") as f: raw = f.read()
assert sha(raw) == BASE_SHA, "BASE SHA MISMATCH: got %s" % sha(raw)
text = raw.decode("utf-8")
orig_lines = text.split("\n")
print("base ok: %d lines, sha %s" % (len(orig_lines), BASE_SHA[:8]))

def replace_once(s, old, new, tag):
    n = s.count(old)
    assert n == 1, "%s: anchor count %d (want 1): %r" % (tag, n, old[:90])
    return s.replace(old, new, 1)

# ------------------------------------------------- H13a: drawer state syncs the bar
old = """  function closePlus(){ drawer.classList.remove('open'); rDrawer.classList.remove('open'); backdrop.classList.remove('open'); roomsBtn.setAttribute('aria-expanded','false'); ecoBtn.setAttribute('aria-expanded','false'); }"""
new = """  function closePlus(){ drawer.classList.remove('open'); rDrawer.classList.remove('open'); backdrop.classList.remove('open'); roomsBtn.setAttribute('aria-expanded','false'); ecoBtn.setAttribute('aria-expanded','false'); pcSyncDrawerBar(); }
  /* FOLLOW-UP pass 2: the bar rises above the scrim (950) but stays below the drawer (960) while a drawer is open, and the open drawer's seg lights up — the bottom-bar version of the original plus rising above the drawer and turning into an x. */
  function pcSyncDrawerBar(){ try{ var l=drawer.classList.contains('open'), r=rDrawer.classList.contains('open'); document.body.classList.toggle('pc-drawer-open', !!(l||r)); document.body.classList.toggle('pc-drawer-left', l); document.body.classList.toggle('pc-drawer-right', r); var sp=document.querySelector('.notif-seg[data-notif="spaces"]'), ec=document.querySelector('.notif-seg[data-notif="eco"]'); if(sp) sp.classList.toggle('pc-open', l); if(ec) ec.classList.toggle('pc-open', r); }catch(e){} }
  window.pcSyncDrawerBar=pcSyncDrawerBar;"""
text = replace_once(text, old, new, "H13a sync helper")

old = """  window.pcToggleDrawer=function(side){ var d=(side==='right')?rDrawer:drawer, btn=(side==='right')?ecoBtn:roomsBtn; var willOpen=!d.classList.contains('open'); closePlus(); if(willOpen){ d.classList.add('open'); backdrop.classList.add('open'); btn.setAttribute('aria-expanded','true'); } return willOpen; };"""
new = """  window.pcToggleDrawer=function(side){ var d=(side==='right')?rDrawer:drawer, btn=(side==='right')?ecoBtn:roomsBtn; var willOpen=!d.classList.contains('open'); closePlus(); if(willOpen){ d.classList.add('open'); backdrop.classList.add('open'); btn.setAttribute('aria-expanded','true'); } pcSyncDrawerBar(); return willOpen; };"""
text = replace_once(text, old, new, "H13a toggle syncs")

# membership open closes the drawers directly (not via closePlus) — keep the bar in step
old = """    var _r=document.getElementById('os-rooms-plus'), _e=document.getElementById('os-eco-plus');
    if(_r) _r.setAttribute('aria-expanded','false');
    if(_e) _e.setAttribute('aria-expanded','false');"""
new = """    var _r=document.getElementById('os-rooms-plus'), _e=document.getElementById('os-eco-plus');
    if(_r) _r.setAttribute('aria-expanded','false');
    if(_e) _e.setAttribute('aria-expanded','false');
    if(window.pcSyncDrawerBar) window.pcSyncDrawerBar();"""
text = replace_once(text, old, new, "H13a membership syncs")

# ------------------------------------------------- H13b: bar raise + lit open seg
old = """@media(max-width:400px){.notif-row{gap:12px;}.notif-tile{width:46px;height:46px;}.notif-seg{padding:2px 2px 0;}}"""
new = """@media(max-width:400px){.notif-row{gap:12px;}.notif-tile{width:46px;height:46px;}.notif-seg{padding:2px 2px 0;}}
/* FOLLOW-UP pass 2: while a drawer is open the bar (base z-index 45) rises to 955 — above the scrim (950), below the drawer (960) — so it stays lit and tappable, and the open drawer's seg lights in its own colour. At phone widths the drawer still covers the bar geometrically, so the scrim tap / Escape close it there. */
body.pc-drawer-open #naya-notif-bar{z-index:955!important;}
.notif-seg.pc-open .notif-tile{border-color:var(--nc);box-shadow:inset 0 1px 0 rgba(255,255,255,.45),inset 0 -9px 15px rgba(0,0,0,.6),0 7px 16px rgba(0,0,0,.6),0 0 26px var(--nc);}"""
text = replace_once(text, old, new, "H13b bar raise CSS")

# ------------------------------------------------- H13c: other segs close the drawer first
old = """    tap(k) {
      if (k === 'mail') { this.set('mail', 0); window.osShowView && window.osShowView('inbox'); }"""
new = """    tap(k) {
      /* FOLLOW-UP pass 2: the bar stays tappable above the scrim while a drawer is open — tapping anything but a drawer seg closes the drawer first, so no view opens underneath it. */
      if (k !== 'spaces' && k !== 'eco' && window.pcCloseDrawers) { try { window.pcCloseDrawers(); } catch (e) {} }
      if (k === 'mail') { this.set('mail', 0); window.osShowView && window.osShowView('inbox'); }"""
text = replace_once(text, old, new, "H13c tap closes drawer")

assert text.count('window.location.href = \'https://nayanet.app/#/hub/spaces\'') == 0, "spaces navigation must be gone"
assert 'pc-drawer-open' in text and 'pcSyncDrawerBar' in text, "pass-2 wiring"
for frag in ('<b>Personal</b>', '<b>Public smart feed</b>', '<b>Naya Notes</b>',
             'MATCH &rarr; ORGANIZE &rarr; CONNECT', 'id="pcRail"',
             '<div class="ph-points pc-restyled" id="pointsdisplay"', 'id="settingsbtn"'):
    assert frag in text, "round-1 fragment missing: %r" % frag[:40]

out = text.encode("utf-8")
with open(WT, "wb") as f: f.write(out)
new_sha = sha(out)
print("WROTE %s  sha %s  %d bytes  %d lines" % (WT, new_sha, len(out), len(text.split("\n"))))

diff = list(difflib.unified_diff(orig_lines, text.split("\n"), lineterm="", n=1))
print("--- DIFF (%d lines) ---" % len(diff))
hunks = [l for l in diff if l.startswith("@@")]
print("hunks: %d" % len(hunks))
for h in hunks: print(h)
with open(OUT + "/diff-followup2.txt", "w") as f:
    f.write("\n".join(diff))
print("diff saved")
