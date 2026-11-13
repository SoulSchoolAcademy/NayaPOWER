#!/usr/bin/env python3
"""PERSONAL-COMPLETE FOLLOW-UP build — 2026-11-13 (maker seat, Team Nitro).
Fixes the checker verdict on round 1 (maker DONE 9/10 build / 8/10 proof +
checker PASS 8/10): Defect 1 (both drawers stranded), two record corrections
(record-only, in RECORD), the Public-tab widening + keyword pull, and the
Naya Notes dead-client line found while preparing the fetching-browser leg.
Exact-string replacements with asserted counts; the base file is edited,
never rebuilt. Nothing is invented; the search rides the mechanism already
on the page (Smart Bar search level as a centered popup + NayaSmartBar.onSearch).

Base:  TEAM-NITRO/personal-page-complete-20261113/personal-complete.html
       in ~/workspace/personal-complete-wt (branch personal/personal-page-complete-20261113)
       — must be SHA ec5c4cce... (round-1 staged file) or the script stops.
Usage: python3 build-followup.py
"""
import hashlib, difflib

WT = "/home/hatch/workspace/personal-complete-wt/TEAM-NITRO/personal-page-complete-20261113/personal-complete.html"
BASE_SHA = "ec5c4cce083708fa6ea301da45e8097e35174cdffc8216910c8953f70b4ba281"
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

# ---------------------------------------------------------------- H1: one drawer toggle, exposed
old = """  var drawer=$('os-drawer'), rDrawer=$('os-drawer-right'), backdrop=$('os-backdrop'), roomsBtn=$('os-rooms-plus'), ecoBtn=$('os-eco-plus');
  function closePlus(){ drawer.classList.remove('open'); rDrawer.classList.remove('open'); backdrop.classList.remove('open'); roomsBtn.setAttribute('aria-expanded','false'); ecoBtn.setAttribute('aria-expanded','false'); }
  roomsBtn.addEventListener('click', function(e){ e.stopPropagation(); var willOpen=!drawer.classList.contains('open'); closePlus(); if(willOpen){ drawer.classList.add('open'); backdrop.classList.add('open'); roomsBtn.setAttribute('aria-expanded','true'); } });
  ecoBtn.addEventListener('click', function(e){ e.stopPropagation(); var willOpen=!rDrawer.classList.contains('open'); closePlus(); if(willOpen){ rDrawer.classList.add('open'); backdrop.classList.add('open'); ecoBtn.setAttribute('aria-expanded','true'); } });"""
new = """  var drawer=$('os-drawer'), rDrawer=$('os-drawer-right'), backdrop=$('os-backdrop'), roomsBtn=$('os-rooms-plus'), ecoBtn=$('os-eco-plus');
  function closePlus(){ drawer.classList.remove('open'); rDrawer.classList.remove('open'); backdrop.classList.remove('open'); roomsBtn.setAttribute('aria-expanded','false'); ecoBtn.setAttribute('aria-expanded','false'); }
  /* PERSONAL-COMPLETE FOLLOW-UP (Defect 1, checker 2026-11-13): the two floating pluses are gone, so the drawers' only openers went with them. The openers now live in the bottom bar (Spaces seg = left drawer, ECO seg = right drawer) and call this one toggle — the hidden plus buttons keep calling it too, so there is one path, not three. */
  window.pcToggleDrawer=function(side){ var d=(side==='right')?rDrawer:drawer, btn=(side==='right')?ecoBtn:roomsBtn; var willOpen=!d.classList.contains('open'); closePlus(); if(willOpen){ d.classList.add('open'); backdrop.classList.add('open'); btn.setAttribute('aria-expanded','true'); } return willOpen; };
  window.pcCloseDrawers=closePlus;
  roomsBtn.addEventListener('click', function(e){ e.stopPropagation(); window.pcToggleDrawer('left'); });
  ecoBtn.addEventListener('click', function(e){ e.stopPropagation(); window.pcToggleDrawer('right'); });"""
text = replace_once(text, old, new, "H1 drawer toggle")

# ------------------------------------------------- H1b: drawer closer exempts its own openers
old = """  document.addEventListener('click', function(e){ if(rDrawer.classList.contains('open') && !rDrawer.contains(e.target)) closePlus(); });"""
new = """  document.addEventListener('click', function(e){ if(rDrawer.classList.contains('open') && !rDrawer.contains(e.target) && !(e.target.closest && e.target.closest('[data-notif="spaces"],[data-notif="eco"]'))) closePlus(); });"""
text = replace_once(text, old, new, "H1b drawer closer guard")

# ------------------------------------------------- H2a: Spaces seg opens the left drawer, in place
old = """      else if (k === 'spaces') { this.set('spaces', 0); window.location.href = 'https://nayanet.app/#/hub/spaces'; }"""
new = """      else if (k === 'spaces') { this.set('spaces', 0); if (window.pcToggleDrawer) window.pcToggleDrawer('left'); }
      else if (k === 'eco') { if (window.pcToggleDrawer) window.pcToggleDrawer('right'); }"""
text = replace_once(text, old, new, "H2a spaces/eco tap")

# ------------------------------------------------- H2b: fifth seg (ECO) in the bottom bar
old = """      var SEGS = [['plus', 'ADD', '#a06bff'], ['mail', 'MAIL', '#3fb8ff'], ['activity', 'ACTIVITY', '#2fe89e'], ['spaces', 'SPACES', '#ffbf3d']];"""
new = """      var SEGS = [['plus', 'ADD', '#a06bff'], ['mail', 'MAIL', '#3fb8ff'], ['activity', 'ACTIVITY', '#2fe89e'], ['spaces', 'SPACES', '#ffbf3d'], ['eco', 'ECOSYSTEM', '#a06bff']];"""
text = replace_once(text, old, new, "H2b SEGS eco")

# ------------------------------------------------- H2c: ECO icon (four-square factory glyph, page's own SVG language)
old = """        spaces: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 11l8-7.5L20 11"/><path d="M6 9.5V20h12V9.5"/><path d="M12 12.2l2.3 2.8L12 17.8 9.7 15z"/></svg>',"""
new = """        spaces: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 11l8-7.5L20 11"/><path d="M6 9.5V20h12V9.5"/><path d="M12 12.2l2.3 2.8L12 17.8 9.7 15z"/></svg>',
        eco: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3.5" y="3.5" width="7" height="7" rx="1.5"/><rect x="13.5" y="3.5" width="7" height="7" rx="1.5"/><rect x="3.5" y="13.5" width="7" height="7" rx="1.5"/><rect x="13.5" y="13.5" width="7" height="7" rx="1.5"/></svg>',"""
text = replace_once(text, old, new, "H2c eco icon")

# ------------------------------------------------- H3: five segs fit at phone widths
old = """/* (2) four segs fit the bar at 390 — the gap drops so the row never squeezes. */
@media(max-width:400px){.notif-row{gap:24px;}}"""
new = """/* (2) FOLLOW-UP (Defect 1): five segs fit the bar at 390/360 — the gap drops and the tiles shrink to 46px (still above the 44px tap floor) so the row never squeezes. Desktop keeps the 54px tiles. */
@media(max-width:400px){.notif-row{gap:12px;}.notif-tile{width:46px;height:46px;}.notif-seg{padding:2px 2px 0;}}"""
text = replace_once(text, old, new, "H3 five segs fit")

# ------------------------------------------------- H4: Search button at the top of the feed
old = """<div class="lens-tabs" id="mwFeedTabs" role="tablist" aria-label="Feed categories">"""
new = """<button type="button" class="pc-search-btn" id="pcSearchBtn" aria-label="Search the public feed">&#128269; Search the public feed</button>
<div class="lens-tabs" id="mwFeedTabs" role="tablist" aria-label="Feed categories">"""
text = replace_once(text, old, new, "H4 search button")

# ------------------------------------------------- H5: Search button styling (page's own primo pill language)
old = """.pc-feedline{text-align:center;font-size:12px;font-weight:800;letter-spacing:.22em;color:#cfc9da;margin:14px 0 10px;text-transform:uppercase;}"""
new = """.pc-feedline{text-align:center;font-size:12px;font-weight:800;letter-spacing:.22em;color:#cfc9da;margin:14px 0 10px;text-transform:uppercase;}
/* FOLLOW-UP: the search opener — a button that opens the existing centered popup on purpose. Never a visible search bar (popup-only search law). */
.pc-search-btn{display:block;margin:0 auto 10px;padding:10px 18px;border-radius:999px;border:1.5px solid rgba(255,255,255,.85);background:linear-gradient(180deg,#17171f,#0a0a0f);color:#fff;font:inherit;font-size:13px;font-weight:800;cursor:pointer;box-shadow:inset 0 1px 0 rgba(255,255,255,.22),inset 0 -3px 6px rgba(0,0,0,.55),0 6px 16px rgba(0,0,0,.5),0 0 17px rgba(160,107,255,.42);}
.pc-search-btn:hover{border-color:#a06bff;box-shadow:inset 0 1px 0 rgba(255,255,255,.3),inset 0 -3px 6px rgba(0,0,0,.5),0 0 22px #a06bff,0 8px 20px rgba(0,0,0,.55);}"""
text = replace_once(text, old, new, "H5 search button CSS")

# ------------------------------------------------- H6: collective loader + keyword state
old = """  window.osLoadWall = loadWall; /* TRUE-BLOCK REPAIR: re-expose (build ate the original line) */"""
new = """  window.osLoadWall = loadWall; /* TRUE-BLOCK REPAIR: re-expose (build ate the original line) */

  /* PERSONAL-COMPLETE FOLLOW-UP — the Public tab pulls the COLLECTIVE (Shawn 2026-11-13 14:11Z: any topic, type a keyword and it pulls the feed, changeable at will). The owner's burst read (osNotesRows, owner-scoped) is untouched — the collective is a second read with no owner filter, newest 500, through the same client the wall uses. The P6 verification filter is reused verbatim, so no verification artifact ever renders in the collective either. If the read fails, the honest skeleton stays — never a faked feed. */
  window.MW_PUBLIC_POSTS=[];
  window.MW_PUBLIC_KEYWORD='';
  window.MW_PUBLIC_LOADED=false;
  function pcPublicRows(){
    var client=null;
    try{ client=(typeof getSb==='function')?getSb():((typeof sb!=='undefined'&&sb)?sb:((window.getSb)?window.getSb():null)); }catch(e){ client=null; }
    if(!client) return Promise.resolve([]);
    return client.from('smart_notes').select('id,content,created_at,owner_alias').order('created_at',{ascending:false}).limit(500)
      .then(function(res){ return (res&&res.data)||[]; }, function(){ return []; });
  }
  function pcLoadPublicWall(){
    if(window.MW_PUBLIC_LOADED){ if(typeof window.mwPaintWallPosts==='function') window.mwPaintWallPosts(window.MW_PUBLIC_POSTS||[]); return; }
    pcPublicRows().then(function(rows){
      var now=Date.now();
      var posts=rows.map(function(r){ var j; try{ j=JSON.parse(r.content); }catch(e){ j=null; } if(!j||!j.k) j={k:'wall',a:'',b:r.content}; return {j:j,at:r.created_at,id:r.id,owner:r.owner_alias}; })
        .filter(function(p){ if(p.j.k!=='wall') return false; if(upIsVerificationPost(p.j)) return false; if(p.j.schedFor&&Date.parse(p.j.schedFor)>now) return false; if(p.j.scheduled&&p.j.scheduled.ts&&p.j.scheduled.ts>now) return false; return true; });
      posts.sort(function(a,b){ var pa=a.j.pinned?1:0,pb=b.j.pinned?1:0; if(pa!==pb) return pb-pa; return new Date(b.at)-new Date(a.at); });
      window.MW_PUBLIC_POSTS=posts; window.MW_PUBLIC_LOADED=true;
      if(typeof window.mwPaintWallPosts==='function') window.mwPaintWallPosts(posts);
    }, function(){ /* keep the honest skeleton on failure — never a faked feed */ });
  }
  window.pcLoadPublicWall=pcLoadPublicWall;
  window.pcSetPublicKeyword=function(q){
    window.MW_PUBLIC_KEYWORD=(q||'').trim();
    var pub=false; try{ var t=document.getElementById('mwTabNaya'); pub=!!(t&&t.classList.contains('active')); }catch(e){}
    if(!pub){ var tab=document.getElementById('mwTabNaya'); if(tab) tab.click(); }
    else if(typeof window.mwPaintWallPosts==='function') window.mwPaintWallPosts(window.MW_PUBLIC_POSTS||[]);
  };
  window.pcClearPublicKeyword=function(){ window.pcSetPublicKeyword(''); };"""
text = replace_once(text, old, new, "H6 collective loader")

# ------------------------------------------------- H7a: painter keeps two stores
old = """    var list=$('os-wall-list'); if(!list) return;
    MW_WALL_POSTS=posts||[];"""
new = """    var list=$('os-wall-list'); if(!list) return;
    /* FOLLOW-UP: the wall has two stores now — the owner's (Personal) and the collective (Public). The Public tab never overwrites the owner's store. */
    var publicOn=false; try{ var _pt=document.getElementById('mwTabNaya'); publicOn=!!(_pt&&_pt.classList.contains('active')); }catch(e){}
    if(!publicOn){ MW_WALL_POSTS=posts||[]; }"""
text = replace_once(text, old, new, "H7a two stores")

# ------------------------------------------------- H7b: painter reads the active tab's store
old = """    window.MW_WALL_POSTS=MW_WALL_POSTS;
    var pill=(typeof window.MW_FEED_PILL!=='undefined')?window.MW_FEED_PILL:'all';
    var shown=MW_WALL_POSTS;"""
new = """    window.MW_WALL_POSTS=MW_WALL_POSTS;
    var pill=(typeof window.MW_FEED_PILL!=='undefined')?window.MW_FEED_PILL:'all';
    var shown=publicOn?(window.MW_PUBLIC_POSTS||[]):MW_WALL_POSTS;"""
text = replace_once(text, old, new, "H7b active store")

# ------------------------------------------------- H7c: author pill filters the shown list, not the owner store
old = """    if(pill && pill!=='all'){
      shown=MW_WALL_POSTS.filter(function(p){ return (p.j.a||'Guest').toLowerCase()===pill; });
    }"""
new = """    if(pill && pill!=='all'){
      shown=shown.filter(function(p){ return (p.j.a||'Guest').toLowerCase()===pill; });
    }"""
text = replace_once(text, old, new, "H7c pill filter")

# ------------------------------------------------- H7d: keyword filter on the collective
old = """    list.innerHTML = shown.length
      ? shown.map(function(p, i){ return wallCard(p.j, p.at, p.id, i); }).join('')
      : '<div class="ph-card" style="--ac:#a06bff;"><p>No posts yet — be the first to make a post on this feed.</p></div>';"""
new = """    /* FOLLOW-UP: a keyword typed in the search popup pulls the Public feed — the collective filtered to that topic, changeable at will. Personal never takes a keyword. */
    var kw=publicOn?((window.MW_PUBLIC_KEYWORD||'').toLowerCase()):'';
    if(kw){
      shown=shown.filter(function(p){ var hay=''; try{ hay=JSON.stringify(p.j||{}); }catch(e){ hay=''; } return (hay+' '+(p.owner||'')).toLowerCase().indexOf(kw)>=0; });
    }
    list.innerHTML = shown.length
      ? shown.map(function(p, i){ return wallCard(p.j, p.at, p.id, i); }).join('')
      : '<div class="ph-card" style="--ac:#a06bff;"><p>No posts yet — be the first to make a post on this feed.</p></div>';"""
text = replace_once(text, old, new, "H7d keyword filter")

# ------------------------------------------------- H7e: honest meta line carries the keyword (textContent — safe)
old = """    /* F5 (fix, self-check round 3) — mwBuildFeedPills + mwRevealWallCards
       live in #mw-script, a separate IIFE; resolving through window (they
       are exposed there, see the feed-board block). The bare typeof guard
       silently skipped them — the ribbon never gained author pills and the
       cards never lit. */
    if(typeof window.mwBuildFeedPills==='function') window.mwBuildFeedPills();"""
new = """    /* FOLLOW-UP: the meta line says what the feed is showing — including the keyword, when one is pulling it. textContent, never HTML, so a typed keyword can never inject markup. */
    if(meta && kw){ meta.textContent=shown.length? (meta.textContent+' Matching \\u201c'+window.MW_PUBLIC_KEYWORD+'\\u201d.') : ('No notes match \\u201c'+window.MW_PUBLIC_KEYWORD+'\\u201d — try another word.'); }
    /* F5 (fix, self-check round 3) — mwBuildFeedPills + mwRevealWallCards
       live in #mw-script, a separate IIFE; resolving through window (they
       are exposed there, see the feed-board block). The bare typeof guard
       silently skipped them — the ribbon never gained author pills and the
       cards never lit. */
    if(typeof window.mwBuildFeedPills==='function') window.mwBuildFeedPills();"""
text = replace_once(text, old, new, "H7e keyword meta")

# ------------------------------------------------- H8: ribbon grows from the collective on Public
old = """    (typeof window.MW_WALL_POSTS!=='undefined'?window.MW_WALL_POSTS:[]).forEach(function(p){"""
new = """    /* FOLLOW-UP: on the Public tab the ribbon grows from the collective, not the owner's wall. */
    var _base=(typeof window.MW_WALL_POSTS!=='undefined'?window.MW_WALL_POSTS:[]);
    if(t==='public') _base=(typeof window.MW_PUBLIC_POSTS!=='undefined'?window.MW_PUBLIC_POSTS:[]);
    _base.forEach(function(p){"""
text = replace_once(text, old, new, "H8 ribbon collective")

# ------------------------------------------------- H9: switching to Public loads the collective
old = """  if(t==='naya') mwLoadNayaFeed();
  else if(typeof window.mwPaintWallPosts==='function') window.mwPaintWallPosts(window.MW_WALL_POSTS||[]);"""
new = """  if(t==='naya') mwLoadNayaFeed();
  else if(t==='public'){ if(typeof window.mwPaintWallPosts==='function') window.mwPaintWallPosts(window.MW_PUBLIC_POSTS||[]); if(typeof window.pcLoadPublicWall==='function') window.pcLoadPublicWall(); }
  else if(typeof window.mwPaintWallPosts==='function') window.mwPaintWallPosts(window.MW_WALL_POSTS||[]);"""
text = replace_once(text, old, new, "H9 public loads collective")

# ------------------------------------------------- H12: Naya Notes dead-client fix (found preparing the captain's leg)
old = """  var sb=null; try{ sb=window.getSb?window.getSb():null; }catch(e){}"""
new = """  /* FOLLOW-UP (found preparing the fetching-browser leg): window.getSb is never assigned anywhere in this file, so this always resolved to null and the Naya Notes tab could never load — the same NayaAuth-first resolution the Lists room already uses. */
  var sb=null; try{ sb=(window.NayaAuth&&window.NayaAuth.client)||(window.getSb?window.getSb():null)||((typeof getSb==='function')?getSb():null); }catch(e){}"""
text = replace_once(text, old, new, "H12 naya client")

# ------------------------------------------------- H10: search wiring (end of file, runs last)
old = """</body></html>"""
new = """<script>
/* ═══ PERSONAL-COMPLETE FOLLOW-UP — the Public keyword pull (Shawn 2026-11-13 14:11Z) ═══
   The Hub shell (hub-index-main-8f2af988.html in the lane dir) carries NO search identifiers at all — 0 hits for NayaSmartBar / nsbSearch / openSearch / onSearch, verified by grep — so there is no Hub search to harvest from the shell. The search mechanism as it stands is the one already on this page: the Smart Bar search level (#nsbSearchLevel) as a centered popup (openSearchModal, popup-only law) with the host hook NayaSmartBar.onSearch. This block wires that hook — nothing new is invented, and no visible search bar is added: the one new control is a button that opens the existing popup on purpose.
   Behaviour: typing in the popup pulls the Public feed to that keyword (pcSetPublicKeyword) and the dropdown lists the matching notes; clicking a result closes the popup onto the already-pulled feed; clearing the popup's field clears the keyword. */
(function(){
"use strict";
var btn=document.getElementById('pcSearchBtn');
if(btn){ btn.addEventListener('click', function(){ if(typeof openSearchModal==='function'){ openSearchModal(); } }); }
if(window.NayaSmartBar){
  window.NayaSmartBar.onSearch=function(q, show){
    var query=(q||'').trim();
    if(query && typeof window.pcSetPublicKeyword==='function'){ try{ window.pcSetPublicKeyword(query); }catch(e){} }
    if(!query){ if(typeof show==='function') show([]); return; }
    var rows=window.MW_PUBLIC_POSTS||[];
    var ql=query.toLowerCase();
    var hits=rows.filter(function(p){ var hay=''; try{ hay=JSON.stringify(p.j||{}); }catch(e){ hay=''; } return (hay+' '+(p.owner||'')).toLowerCase().indexOf(ql)>=0; });
    var list=hits.slice(0,12).map(function(p){ var title=''; try{ title=(p.j.b||'').split('\\n')[0].slice(0,90)||'Note'; }catch(e){ title='Note'; } return {label:title, sub:(p.j.a||'Guest')+' \\u00b7 public feed', url:'#'}; });
    if(typeof show==='function') show(list);
  };
}
/* clearing the popup's field clears the keyword on the feed */
try{
  var sIn=document.querySelector('#nsbSearchLevel input[type="search"]');
  if(sIn){ sIn.addEventListener('input', function(){ if(!sIn.value.trim() && typeof window.pcSetPublicKeyword==='function'){ try{ window.pcSetPublicKeyword(''); }catch(e){} } }); }
}catch(e){}
/* a result click closes the popup onto the already-pulled feed (the links themselves go nowhere by design) */
document.addEventListener('click', function(e){
  var a=e.target&&e.target.closest?e.target.closest('.nsb-sr-item'):null;
  if(a && typeof closeSearchModal==='function'){ try{ closeSearchModal(); }catch(err){} }
});
})();
</script>
</body></html>"""
text = replace_once(text, old, new, "H10 search wiring")

# ------------------------------------------------- guards: no regressions by construction
assert text.count('window.location.href = \'https://nayanet.app/#/hub/spaces\'') == 0, "spaces navigation must be gone"
assert 'SEGS = ' in text and "'eco', 'ECOSYSTEM'" in text, "eco seg"
assert text.count('id="pcSearchBtn"') == 1, "one search button"
assert 'up to 6' not in text and 'up to 10' not in text, "limit numbers leaked"
assert text.count('id="pluswrap"') == 1, "pluswrap intact"
# the seven items survive: tabs, feed line, rail, pill, gear
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
with open(OUT + "/diff-followup.txt", "w") as f:
    f.write("\n".join(diff))
print("diff saved")
