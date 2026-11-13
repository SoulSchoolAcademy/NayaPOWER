#!/usr/bin/env python3
"""AUTO-TRANSLATE build — Personal page, staged only.
Reads the BASE Personal complete page (sha asserted), applies the
AUTO-TRANSLATE round's edits, writes the result into the worktree.
Build-script shape, never hand-edited staged bytes (same shape as
build-complete.py). Every replacement asserts its count; a miss aborts."""
import hashlib, json, sys

BASE = '/home/hatch/workspace/personal-complete-wt/TEAM-NITRO/personal-page-complete-20261113/personal-complete.html'
BASE_SHA = '4872414a1d428a940a4e12ac31c419f999843a2fde072a9ac91d09b42051c666'
WORK = '/home/hatch/workspace/team-nitro/auto-translate-20261113/'
OUT = BASE  # in-place in the worktree, on branch personal/auto-translate-20261113

def TR(k):
    """guarded mwTr call for scripts that run after parse: English fallback."""
    return "(window.mwTr?window.mwTr('%s'):'%s')" % (k.replace("'", "\\'"), k.replace("'", "\\'"))

h = open(BASE, encoding='utf-8', errors='replace').read()
sha = hashlib.sha256(h.encode('utf-8')).hexdigest()
assert sha == BASE_SHA, 'BASE MOVED: %s (expected %s) — STOP, re-ground' % (sha, BASE_SHA)
print('base sha OK', sha[:12], 'lines', h.count('\n') + 1)

def rep(old, new, n=1):
    global h
    c = h.count(old)
    assert c == n, 'rep count %d != %d for: %s' % (c, n, old[:90])
    h = h.replace(old, new)

# ---- 1. the grown language block (span replace, boundary-asserted) ----
lang = open(WORK + 'mw-lang-block.js', encoding='utf-8').read()
d = json.load(open(WORK + 'dict-final.json', encoding='utf-8'))
lang = lang.replace('/*__MW_I18N_JSON__*/', json.dumps(d, ensure_ascii=False))
a = h.index('/* ---------- language (fix 18) ---------- */')
b = h.index('/* ---------- settings binding ---------- */')
assert 'var MW_I18N={' in h[a:b] and 'function mwApplyLang(){' in h[a:b], 'language span boundaries wrong'
h = h[:a] + lang.rstrip() + '\n' + h[b:]
print('language block grown: 17 keys -> 167 keys/language')

# ---- 2. switch caps translate ----
rep("  if(cap) cap.textContent=on?'On':'Off';",
    "  if(cap) cap.textContent=on?(window.mwTr?window.mwTr('On'):'On'):(window.mwTr?window.mwTr('Off'):'Off');")
rep("    if (cap) cap.textContent=on?'On':'Off';",
    "    if (cap) cap.textContent=on?(window.mwTr?window.mwTr('On'):'On'):(window.mwTr?window.mwTr('Off'):'Off');")

# ---- 3. Settings picker shows the effective language (stored pick, else browser default) ----
rep("  if(lang){ lang.value=mwGet('lang','en'); lang.addEventListener('change', function(){ mwPut('lang', lang.value); mwApplyLang(); }); }",
    "  if(lang){ lang.value=mwLangCode(); lang.addEventListener('change', function(){ mwPut('lang', lang.value); mwApplyLang(); }); }")

# ---- 4. feed tabs: icon twin + data-mw-tr on the label ----
rep('id="mwTabSmart" data-mw-tab="personal" role="tab" aria-selected="true" style="--glow:#3fb8ff"><b>Personal</b></button>',
    'id="mwTabSmart" data-mw-tab="personal" role="tab" aria-selected="true" style="--glow:#3fb8ff"><span class="os-jewel os-jewel-sm" style="--jc:#a06bff">✦</span> <b data-mw-tr="tab">Personal</b></button>')
rep('id="mwTabNaya" data-mw-tab="public" role="tab" aria-selected="false" style="--glow:#ffbf3d"><b>Public smart feed</b></button>',
    'id="mwTabNaya" data-mw-tab="public" role="tab" aria-selected="false" style="--glow:#ffbf3d"><span class="os-jewel os-jewel-sm" style="--jc:#3fb8ff">🌍</span> <b data-mw-tr="tab">Public smart feed</b></button>')
rep('id="mwTabActivity" data-mw-tab="naya" role="tab" aria-selected="false" style="--glow:#2fe89e"><b>Naya Notes</b></button>',
    'id="mwTabActivity" data-mw-tab="naya" role="tab" aria-selected="false" style="--glow:#2fe89e"><span class="os-jewel os-jewel-sm" style="--jc:#2fe89e">✦</span> <b data-mw-tr="tab">Naya Notes</b></button>')

# ---- 5. feedname buttons + feed line + search button ----
for fid, label in [('mwFeedNameSmart', 'Shawn&rsquo;s Personal feed — tap for the full feed ↓'),
                  ('mwFeedNameNaya', 'Shawn&rsquo;s Public smart feed — tap for the full feed ↓'),
                  ('mwFeedNameActivity', 'Shawn&rsquo;s Naya Notes — tap for the full feed ↓')]:
    rep('id="%s"' % fid, 'id="%s" data-mw-tr="feedname"' % fid)
rep('<div class="pc-feedline" aria-label="How the feed works">MATCH &rarr; ORGANIZE &rarr; CONNECT</div>',
    '<div class="pc-feedline" aria-label="How the feed works" data-mw-tr="feedline">MATCH &rarr; ORGANIZE &rarr; CONNECT</div>')
rep('id="pcSearchBtn" aria-label="Search the public feed">&#128269; Search the public feed</button>',
    'id="pcSearchBtn" aria-label="Search the public feed">&#128269; <span data-mw-tr="search">Search the public feed</span></button>')

# ---- 6. create row + plus menu + creator mode buttons: wrap labels ----
for mode, icon, label in [('post', '✎', 'Make a post'), ('naya', '✎', 'Naya note'), ('smart', '✦', 'Smart note')]:
    rep('class="tg-mode fc-create" data-fc-create="%s" style="--mc:%s"><span class="tg-dot"></span>%s %s</button>' % (
        mode, {'post': '#e8e8ec', 'naya': '#2fe89e', 'smart': '#a06bff'}[mode], icon, label),
        'class="tg-mode fc-create" data-fc-create="%s" style="--mc:%s"><span class="tg-dot"></span>%s <span data-mw-tr="cr">%s</span></button>' % (
        mode, {'post': '#e8e8ec', 'naya': '#2fe89e', 'smart': '#a06bff'}[mode], icon, label))
    cls = 'tg-mode on' if mode == 'naya' else 'tg-mode'  # naya is the default mode: class carries 'on'
    rep('class="%s" data-tg-mode="%s" style="--mc:%s"><span class="tg-dot"></span>%s %s</button>' % (
        cls, mode, {'post': '#e8e8ec', 'naya': '#2fe89e', 'smart': '#a06bff'}[mode], icon, label),
        'class="%s" data-tg-mode="%s" style="--mc:%s"><span class="tg-dot"></span>%s <span data-mw-tr="cm">%s</span></button>' % (
        cls, mode, {'post': '#e8e8ec', 'naya': '#2fe89e', 'smart': '#a06bff'}[mode], icon, label))
for key, icon, label in [('post', '✎', 'Make a post'), ('naya', '✎', 'Naya note'),
                         ('smart', '✦', 'Smart note'), ('msg', '💬', 'Message'), ('mail', '✉️', 'Mail')]:
    rep('<span class="fc-pi-ico">%s</span>%s</div>' % (icon, label),
        '<span class="fc-pi-ico">%s</span><span data-mw-tr="pm">%s</span></div>' % (icon, label))

# ---- 7. creator: hint + placeholders ----
rep('<p class="os-note tg-hint" id="tg-hint">Naya note &mdash; Naya formats your words beautifully. Write it, dictate it with the microphone &mdash; Naya writing it for you is coming soon.</p>',
    '<p class="os-note tg-hint" id="tg-hint" data-mw-tr="hint">Naya note — Naya formats your words beautifully. Write it, dictate it with the microphone — Naya writing it for you is coming soon.</p>')
rep('placeholder="Make a post on this app&rsquo;s feed&hellip;"',
    'data-mw-ph="Make a post on this app’s feed…" placeholder="Make a post on this app&rsquo;s feed&hellip;"')

# ---- 8. tgSetMode: mode labels through mwTr ----
rep("if(h) h.textContent='Smart note — your words distilled into an intelligent block. You review it before it posts.';",
    "if(h) h.textContent=%s;" % TR('Smart note — your words distilled into an intelligent block. You review it before it posts.'))
rep("if(pb) pb.innerHTML='✦ Smart note it';",
    "if(pb) pb.innerHTML='✦ '+%s;" % TR('Smart note it'))
rep("if(ft) ft.textContent='Smart note';", "if(ft) ft.textContent=%s;" % TR('Smart note'))
rep("if(h) h.textContent='Make a post — your words, straight up. No auto-format, no distillation — what you write is what lands on the feed.';",
    "if(h) h.textContent=%s;" % TR('Make a post — your words, straight up. No auto-format, no distillation — what you write is what lands on the feed.'))
rep("if(pb) pb.textContent='✎ Post it';",
    "if(pb) pb.textContent='✎ '+%s;" % TR('Post it'))
rep("if(ft) ft.textContent='Make a post';", "if(ft) ft.textContent=%s;" % TR('Make a post'))
rep("if(h) h.textContent='Naya note — Naya formats your words beautifully. Write it, dictate it with the microphone — Naya writing it for you is coming soon.';",
    "if(h) h.textContent=%s;" % TR('Naya note — Naya formats your words beautifully. Write it, dictate it with the microphone — Naya writing it for you is coming soon.'))
rep("if(pb) pb.textContent='✦ Post my Naya note';",
    "if(pb) pb.textContent='✦ '+%s;" % TR('Post my Naya note'))
rep("if(ft) ft.textContent='Naya note';", "if(ft) ft.textContent=%s;" % TR('Naya note'))

# ---- 9. Schedule resets through mwTr ----
rep("if (sbtn){ sbtn.textContent='\\uD83D\\uDD50 Schedule'; sbtn.classList.remove('set'); }",
    "if (sbtn){ sbtn.textContent='\\uD83D\\uDD50 '+%s; sbtn.classList.remove('set'); }" % TR('Schedule'))
rep("var s=$('os-sched-btn'); if(s){ s.textContent='\\uD83D\\uDD50 Schedule'; s.classList.remove('set'); }",
    "var s=$('os-sched-btn'); if(s){ s.textContent='\\uD83D\\uDD50 '+%s; s.classList.remove('set'); }" % TR('Schedule'))

# ---- 10. picker + chat ----
rep('<h3 id="fcPickerTitle"><span class="os-jewel os-jewel-h" style="--jc:#3fb8ff">💬</span> Message someone</h3>',
    '<h3 id="fcPickerTitle"><span class="os-jewel os-jewel-h" style="--jc:#3fb8ff">💬</span> <span data-mw-tr="pick">Message someone</span></h3>')
rep('<p class="os-note">Search your people and spaces — pick one and the message pops up.</p>',
    '<p class="os-note" data-mw-tr="pickhint">Search your people and spaces — pick one and the message pops up.</p>')
rep('placeholder="Search people and spaces&hellip;"',
    'data-mw-ph="Search people and spaces…" placeholder="Search people and spaces&hellip;"')
rep('<p class="os-note">Match is figured on this device from shared posts, messages and invites — highest first. Spaces show by name; their match comes from the Auto-Match engine, which is not switched on for citizens yet.</p>',
    '<p class="os-note" data-mw-tr="picknote">Match is figured on this device from shared posts, messages and invites — highest first. Spaces show by name; their match comes from the Auto-Match engine, which is not switched on for citizens yet.</p>')
rep('<b id="fcChatName">Someone</b>', '<b id="fcChatName" data-mw-tr="chatname">Someone</b>')
rep('<span id="fcChatMeta">Instant message</span>', '<span id="fcChatMeta" data-mw-tr="chatmeta">Instant message</span>')
rep('<p class="os-note" id="fcChatHint">Write it — it pops up in their Smart Mail inbox as an instant message.</p>',
    '<p class="os-note" id="fcChatHint" data-mw-tr="chathint">Write it — it pops up in their Smart Mail inbox as an instant message.</p>')
rep('id="fcChatSubject" type="text" placeholder="Subject"',
    'id="fcChatSubject" type="text" data-mw-ph="Subject" placeholder="Subject"')
rep('id="fcChatBody" rows="3" placeholder="Write your message&hellip;"',
    'id="fcChatBody" rows="3" data-mw-ph="Write your message…" placeholder="Write your message&hellip;"')
rep("if(mt) mt.textContent=(f&&typeof f.match==='number'?f.match+'% match · ':'')+(who.kind==='space'?'Space · ':'')+(isMail?'Smart Mail':'Instant message');",
    "if(mt) mt.textContent=(f&&typeof f.match==='number'?f.match+'% match · ':'')+(who.kind==='space'?'Space · ':'')+(isMail?'Smart Mail':" + TR('Instant message') + ");")
rep("if(hint) hint.textContent=isMail?'Write it — it lands in their Smart Mail inbox.':'Write it — it pops up in their Smart Mail inbox as an instant message.';",
    "if(hint) hint.textContent=isMail?%s:%s;" % (TR('Write it — it lands in their Smart Mail inbox.'), TR('Write it — it pops up in their Smart Mail inbox as an instant message.')))

# ---- 11. Settings: join-cover row, notif rows, reset, install, home-hub link ----
rep('<b>Join NayaNET on the cover too</b>', '<b data-mw-tr="set">Join NayaNET on the cover too</b>')
rep('<span class="os-setrow-sub">Join NayaNET already sits in the hero row — turn this on to add it to the cover as an extra spot.</span>',
    '<span class="os-setrow-sub" data-mw-tr="set">Join NayaNET already sits in the hero row — turn this on to add it to the cover as an extra spot.</span>')
for label in ['New posts and notes on your feed.', 'Feed activity',
              'Mentions &amp; replies', 'Someone replies to you or mentions you.',
              'New connections', 'Someone connects with you or joins from your invite.',
              'Membership news', 'Something new in a membership you hold.']:
    rep('>%s<' % label, ' data-mw-tr="set">%s<' % label)
rep('>Bring everything back</button>', ' data-mw-tr="set">Bring everything back</button>')
rep('<p class="os-note" id="mw-set-reset-note" style="margin:6px 0 0">Worst case, hit this — every hidden bar, strip and button comes back.</p>',
    '<p class="os-note" data-mw-tr="set">Worst case, hit this — every hidden bar, strip and button comes back.</p>')
rep('<h3><span class="os-jewel os-jewel-h" style="--jc:#3fb8ff">📲</span> Install as app</h3>',
    '<h3><span class="os-jewel os-jewel-h" style="--jc:#3fb8ff">📲</span> <span data-mw-tr="set">Install as app</span></h3>')
rep('<p>Put this app on your home screen &mdash; it opens like any other app, no browser bars.</p>',
    '<p data-mw-tr="set">Put this app on your home screen &mdash; it opens like any other app, no browser bars.</p>')
rep('>Install this app</button>', ' data-mw-tr="set">Install this app</button>')
rep('<p id="os-install-state">Checking install state&hellip;</p>',
    '<p id="os-install-state" data-mw-tr="set">Checking install state&hellip;</p>')
rep('style="text-decoration:none;display:inline-flex;align-items:center;justify-content:center;">Go to Home Hub →</a>',
    'style="text-decoration:none;display:inline-flex;align-items:center;justify-content:center;" data-mw-tr="set">Go to Home Hub →</a>')
rep('<button class="ph-msg" type="button" data-os-go="settings">Change what shows here</button>',
    '<button class="ph-msg" type="button" data-os-go="settings" data-mw-tr="set">Change what shows here</button>')


# ---- 11b. Settings seg buttons (static markup — Top/Bottom/Off, feed tab, Any) ----
for v, label in [('top', 'Top'), ('bottom', 'Bottom'), ('off', 'Off'),
                 ('smart', 'Smart Notes'), ('naya', 'Naya Notes'), ('activity', 'Activity'),
                 ('0', 'Any')]:
    rep('<button type="button" data-v="%s"' % v, '<button type="button" data-v="%s" data-mw-tr="seg"' % v, n=1)

# ---- 12. drawers: heads + links (Home/Hub stays — two proper names, not in the inventory) ----
rep('<div class="os-drawer-head">NAYANET AREAS</div>',
    '<div class="os-drawer-head" data-mw-tr="drawer">NAYANET AREAS</div>')
rep('<div class="os-drawer-head">NAYANET ECOSYSTEM</div>',
    '<div class="os-drawer-head" data-mw-tr="drawer">NAYANET ECOSYSTEM</div>')
rep('<div class="os-drawer-sec">ABOUT NAYANET</div>',
    '<div class="os-drawer-sec" data-mw-tr="drawer">ABOUT NAYANET</div>')
for label in ['Your Reports', 'Intel Today', 'Your Connections', 'Smart Meet',
              'Smart Factory', 'Leaderboards',
              'My Spaces', '＋ Add a custom link', 'About Us', 'White Paper']:
    rep('>%s</a>' % label, ' data-mw-tr="drawer">%s</a>' % label)
# MEMBERSHIPS / YOUR WORLD are section divs, not links (the membership names
# Naya Academy / AI Masterclass / Fast Action Club and the page names
# Personal / Business / Space are proper names and stay as they are)
for sec in ['MEMBERSHIPS', 'YOUR WORLD']:
    rep('<div class="os-drawer-sec">%s</div>' % sec,
        '<div class="os-drawer-sec" data-mw-tr="drawer">%s</div>' % sec)

# ---- 12b. Part 3 (fresh maker, 2026-11-13): the three worlds get their gem
# twins — the drawer rows are text-only today, so with words hidden the three
# worlds are three identical boards and the no-words step "find your world"
# cannot tell them apart. The jewel is the tab twin's own span (.os-jewel),
# in the colour the page already assigns that world in this drawer (--rc).
# (The other drawer links stay text-only — navigation, not one of the five
# no-words steps; named as a gap in the record, not silently claimed.) ----
rep('<a href="https://nayanet.app/personal" style="--rc:#3fb8ff">Personal</a>',
    '<a href="https://nayanet.app/personal" style="--rc:#3fb8ff"><span class="os-jewel os-jewel-sm" style="--jc:#3fb8ff">✦</span> Personal</a>')
rep('<a href="https://nayanet.app/business" style="--rc:#2fe89e">Business</a>',
    '<a href="https://nayanet.app/business" style="--rc:#2fe89e"><span class="os-jewel os-jewel-sm" style="--jc:#2fe89e">✦</span> Business</a>')
rep('<a href="https://nayanet.app/space" style="--rc:#ffbf3d">Space</a>',
    '<a href="https://nayanet.app/space" style="--rc:#ffbf3d"><span class="os-jewel os-jewel-sm" style="--jc:#ffbf3d">✦</span> Space</a>')

# ---- 13. Live Feed strip ----
rep('<div class="ph-sec-t"><span class="ph-dot" style="background:#a06bff;color:#a06bff;"></span> Live Feed</div>',
    '<div class="ph-sec-t"><span class="ph-dot" style="background:#a06bff;color:#a06bff;"></span> <span data-mw-tr="lf">Live Feed</span></div>')
rep('<span class="os-hlbar-lab">Your world &middot; live</span>',
    '<span class="os-hlbar-lab" data-mw-tr="lf">Your world &middot; live</span>')
for cell in ['Posts', 'Smart notes', 'Messages', 'Invites', 'Link clicks', 'Joins']:
    rep('<i>%s</i>' % cell, '<i data-mw-tr="lf">%s</i>' % cell)
rep('<button class="ph-msg" type="button" data-mw-real-dash>Go to my Dashboard →</button>',
    '<button class="ph-msg" type="button" data-mw-real-dash data-mw-tr="lf">Go to my Dashboard →</button>')  # cover-top
rep('<button class="ph-connect os-hlbar-btn" type="button" data-mw-real-dash>Go to my Dashboard →</button>',
    '<button class="ph-connect os-hlbar-btn" type="button" data-mw-real-dash data-mw-tr="lf">Go to my Dashboard →</button>')  # Live Feed strip

# ---- 14. rail head / foot, points pill, login bottombar ----
rep('<h3>People around you</h3>',
    '<h3 data-mw-tr="rail">People around you</h3>')
rep('<p class="pc-rail-note">Live matches come from the Smart Feed engine, with their reasons attached. Standing profiles are the family, marked as standing &mdash; never shown as online.</p>',
    '<p class="pc-rail-note" data-mw-tr="rail">Live matches come from the Smart Feed engine, with their reasons attached. Standing profiles are the family, marked as standing &mdash; never shown as online.</p>')
rep('<p class="pc-rail-foot">One more seat is held open for the next live citizen.</p>',
    '<p class="pc-rail-foot" data-mw-tr="rail">One more seat is held open for the next live citizen.</p>')
rep('<span class="ph-points-label">pts</span>', '<span class="ph-points-label" data-mw-tr="pts">pts</span>')
# (bottombar intentionally unmarked — guarded in mwApplyLang)

# ---- 15. bottom-bar aria-labels at init (guarded: mwTr may not exist yet at parse) ----
rep("        b.setAttribute('aria-label', s[1] + ' — open');",
    "        b.setAttribute('aria-label', (window.mwTr?window.mwTr(s[1]):s[1]) + ' — ' + (window.mwTr?window.mwTr('open'):'open'));")
rep("        b.setAttribute('title', s[1]);",
    "        b.setAttribute('title', (window.mwTr?window.mwTr(s[1]):s[1]));")

# ---- 16. rail renderer: icons + translated labels/counts ----
rep("function pcCard(p, live){",
    "function pcTr(x){ try{ return window.mwTr?window.mwTr(x):x; }catch(e){ return x; } }\nfunction pcCard(p, live){")
rep("'<button type=\"button\" class=\"pc-btn\" data-pc-act=\"chat\" style=\"--mc:#3fb8ff\">Chat</button>'",
    "'<button type=\"button\" class=\"pc-btn\" data-pc-act=\"chat\" style=\"--mc:#3fb8ff\">💬 '+pcTr('Chat')+'</button>'")
rep("'<button type=\"button\" class=\"pc-btn\" data-pc-act=\"mail\" style=\"--mc:#ffbf3d\">Mail</button>'",
    "'<button type=\"button\" class=\"pc-btn\" data-pc-act=\"mail\" style=\"--mc:#ffbf3d\">✉️ '+pcTr('Mail')+'</button>'")
rep("'<button type=\"button\" class=\"pc-btn\" data-pc-act=\"audio\" style=\"--mc:#2fe89e\">Audio</button>'",
    "'<button type=\"button\" class=\"pc-btn\" data-pc-act=\"audio\" style=\"--mc:#2fe89e\">🔊 '+pcTr('Audio')+'</button>'")
rep("'<button type=\"button\" class=\"pc-btn\" data-pc-act=\"video\" style=\"--mc:#a06bff\">Video</button>'",
    "'<button type=\"button\" class=\"pc-btn\" data-pc-act=\"video\" style=\"--mc:#a06bff\">🎥 '+pcTr('Video')+'</button>'")
rep("'<p class=\"pc-rail-sec\">Live matches</p>'", "'<p class=\"pc-rail-sec\">'+pcTr('Live matches')+'</p>'")
rep("'<p class=\"pc-rail-sec\">Standing</p>'", "'<p class=\"pc-rail-sec\">'+pcTr('Standing')+'</p>'")
rep("live.length+' live match'+(live.length===1?'':'es')",
    "live.length+' '+(live.length===1?pcTr('live match'):pcTr('live matches'))")
rep("standing.length+' standing'", "standing.length+' '+pcTr('standing')")
rep("'<span class=\"pc-mark you\">YOU &middot; STANDING</span>'",
    "'<span class=\"pc-mark you\">'+pcTr('YOU \\u00b7 STANDING')+'</span>'")
rep("'<span class=\"pc-mark\">STANDING</span>'", "'<span class=\"pc-mark\">'+pcTr('STANDING')+'</span>'")
rep("st.textContent=(act==='audio'?'Audio calls':'Video calls')+' arrive with Smart Meet — for now, message them here.';",
    "st.textContent=pcTr(act==='audio'?'Audio calls arrive with Smart Meet — for now, message them here.':'Video calls arrive with Smart Meet — for now, message them here.');")

# ---- 17. empty states + ribbon through mwTr ----
rep("'<div class=\"ph-card\" style=\"--ac:#a06bff;\"><p>No posts yet — be the first to make a post on this feed.</p></div>'",
    "'<div class=\"ph-card\" style=\"--ac:#a06bff;\"><p>'+%s+'</p></div>'" % TR('No posts yet — be the first to make a post on this feed.'))
rep("box.innerHTML='<p class=\"os-note\">No Naya Notes yet — the first one lands here.</p>';",
    "box.innerHTML='<p class=\"os-note\">'+%s+'</p>';" % TR('No Naya Notes yet — the first one lands here.'))
rep("box.innerHTML='<p class=\"os-note\">No Naya Notes in this category yet.</p>';",
    "box.innerHTML='<p class=\"os-note\">'+%s+'</p>';" % TR('No Naya Notes in this category yet.'))
rep("html+='<div class=\"smart-tab add-tab\" data-mw-pill=\"__add\">+ Add</div>';",
    "html+='<div class=\"smart-tab add-tab\" data-mw-pill=\"__add\">+ '+%s+'</div>';" % TR('Add'))

# ---- 18. inject the Translate module + CSS before </body> ----
css = open(WORK + 'mw-translate.css', encoding='utf-8').read()
js = open(WORK + 'mw-translate.js', encoding='utf-8').read()
assert '</script>' not in js, 'translate JS must not contain a closing script tag'
inject = '<style id="mw-translate-css">\n' + css + '\n</style>\n<script id="mw-translate">\n' + js + '\n</script>\n</body></html>'
rep('</body></html>', inject)

out = h.encode('utf-8')
open(OUT, 'wb').write(out)
print('written', OUT, len(out), 'bytes, sha256', hashlib.sha256(out).hexdigest())
print('data-mw-tr count:', h.count('data-mw-tr'), '| data-mw-ph count:', h.count('data-mw-ph'))
