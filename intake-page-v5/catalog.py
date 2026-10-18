
# ============ PIECE CATALOG — every piece gets a model number ============
# (specimen HTML uses the verbatim library classes)
ICON_SVGS = {
 'home':'<path d="M3 11l9-8 9 8"/><path d="M5 10v10h5v-6h4v6h5V10"/>',
 'bolt':'<path d="M13 2L4 14h6l-1 8 9-12h-6l1-8z"/>',
 'user':'<circle cx="12" cy="8" r="3.5"/><path d="M5 20v-1c0-7 14-7 14 0v1"/>',
 'cal':'<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
 'doc':'<path d="M6 2h9l5 5v15H6z"/><path d="M14 2v6h6"/>',
 'eye':'<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7-10-7-10-7z"/><circle cx="12" cy="12" r="3"/>',
 'save':'<path d="M6 3h12v18l-6-4-6 4z"/>',
 'compass':'<circle cx="12" cy="12" r="9"/><path d="M15 9l-2 5-4 1 2-5z"/>',
 'star':'<path d="m12 2 2.1 7.9L22 12l-7.9 2.1L12 22l-2.1-7.9L2 12l7.9-2.1Z"/>',
 'chart':'<path d="M4 19v-8m5 8V5m5 14V9m5 10V3"/>',
 'heart':'<path d="M12 21C7 16.5 2 12.8 2 8.5 2 5.5 4.5 3 7.5 3c1.8 0 3.4.9 4.5 2.3C13.1 3.9 14.7 3 16.5 3 19.5 3 22 5.5 22 8.5c0 4.3-5 8-10 12.5z"/>',
 'share':'<circle cx="6" cy="12" r="2.5"/><circle cx="18" cy="6" r="2.5"/><circle cx="18" cy="18" r="2.5"/><path d="M8.2 10.8l7.6-3.6M8.2 13.2l7.6 3.6"/>',
}
BB = [("Home","home","#a06bff"),("Pulse","bolt","#3fb8ff"),("People","user","#2fe89e"),
      ("Calendar","cal","#ffbf3d"),("Docs","doc","#e84fff"),("Vision","eye","#6675ff"),
      ("Saved","save","#40d3bb"),("Explore","compass","#ff9a5a"),("Favorite","star","#ff5e6c"),
      ("Reports","chart","#b8ee57"),("Love","heart","#e84fff"),("Share","share","#a06bff")]
DUAL = [("Today","#e84fff","diamond","intelligence"),("Spaces","#a06bff","circle","state"),
        ("Reports","#6675ff","square","destination"),("Mail","#3fb8ff","diamond","intelligence"),
        ("Ask","#40d3bb","circle","state"),("Doors","#2fe89e","square","destination"),
        ("People","#2fe89e","circle","state"),("Ledger","#ffbf3d","diamond","intelligence"),
        ("Grow","#ff9a5a","circle","state"),("Guard","#ff5e6c","square","destination")]
DUAL_SVG = {'Today':'<path d="M12 3l2.2 6.6L21 12l-6.8 2.4L12 21l-2.2-6.6L3 12l6.8-2.4z"/>',
 'Spaces':'<rect x="4" y="4" width="7" height="7" rx="1.5"/><rect x="13" y="4" width="7" height="7" rx="1.5"/><rect x="4" y="13" width="7" height="7" rx="1.5"/><rect x="13" y="13" width="7" height="7" rx="1.5"/>',
 'Reports':'<path d="M5 19v-6m5 6V5m5 14v-9m4 9H3"/>',
 'Mail':'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
 'Ask':'<circle cx="11" cy="11" r="7"/><path d="M16.5 16.5L21 21"/>',
 'Doors':'<rect x="5" y="3" width="14" height="18" rx="1"/><circle cx="15" cy="12" r="1.2"/>',
 'People':'<circle cx="9" cy="8" r="3"/><path d="M3 20v-2c0-6 12-6 12 0v2M17 5a3 3 0 0 1 0 6m1 4c2 0 3 2 3 4v1"/>',
 'Ledger':'<path d="M4 19v-8m5 8V5m5 14V9m5 10V3"/>',
 'Grow':'<circle cx="12" cy="12" r="8"/><path d="M12 4v16M4 12h16"/>',
 'Guard':'<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/>'}

def svg_wrap(path, size=22):
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{path}</svg>'

def bb_btn(name, key, color):
    return f'<a class="eco-bb-btn elev-1" style="--eco:{color}" title="{name}">{svg_wrap(ICON_SVGS[key])}</a>'

def dual_icon(name, color, shape):
    shp = {'diamond':'transform:rotate(45deg);border-radius:8px','circle':'border-radius:50%','square':'border-radius:10px'}[shape]
    return f'''<span style="width:54px;height:54px;{shp};background:radial-gradient(circle at 35% 30%,{color}55,#0a0a0e 75%);border:1.5px solid {color};display:flex;align-items:center;justify-content:center;box-shadow:0 6px 18px rgba(0,0,0,.6),0 0 16px -4px {color},inset 0 1px 0 rgba(255,255,255,.3)"><span style="width:30px;height:30px;display:flex">{svg_wrap(DUAL_SVG[name],30)}</span></span>'''

PIECES = []
def add(model, name, cat, html, note=""):
    PIECES.append({"model":model,"name":name,"cat":cat,"html":html,"note":note})

# BUTTONS
add("NAYA-BTN-001","Black Ground","Buttons",'<button class="naya-btn naya-btn--foundation naya-btn--foundation-obsidian elev-2" type="button"><span class="nb-jewel">◆</span><span class="nb-copy"><span class="nb-title">BLACK GROUND</span><span class="nb-sub">Obsidian field</span></span></button>',"foundation skin")
add("NAYA-BTN-002","White Light","Buttons",'<button class="naya-btn naya-btn--foundation naya-btn--foundation-light elev-2" type="button"><span class="nb-jewel">✦</span><span class="nb-copy"><span class="nb-title">WHITE LIGHT</span><span class="nb-sub">Living light</span></span></button>',"foundation skin")
add("NAYA-BTN-003","Purple Soul","Buttons",'<button class="naya-btn naya-btn--foundation naya-btn--foundation-soul elev-2" type="button"><span class="nb-jewel">▲</span><span class="nb-copy"><span class="nb-title">PURPLE SOUL</span><span class="nb-sub">Soul signature</span></span></button>',"foundation skin")
for i,(t,cls) in enumerate([("Magenta","theme-magenta"),("Purple","theme-purple"),("Blue","theme-blue"),("Green","theme-green"),("Gold","theme-gold")],4):
    add(f"NAYA-BTN-{i:03d}",f"Primo {t}","Buttons",f'<button class="primo {cls} elev-2" type="button">{t}</button>',"edge-ignition on hover")
add("NAYA-BTN-009","Hero · Enter the Standard","Buttons",'<span class="nb-scope"><button class="living-btn elev-3" type="button"><span class="btn-glow"></span><span class="btn-label">✦ ENTER THE STANDARD</span></button></span>',"flagship primary")
add("NAYA-BTN-010","Hero · See It Working","Buttons",'<span class="nb-scope"><button class="living-btn elev-3" type="button"><span class="btn-glow"></span><span class="btn-label">◆ SEE IT WORKING</span></button></span>',"flagship primary")
add("NAYA-BTN-011","Hero · Read the Law","Buttons",'<span class="nb-scope"><button class="living-btn elev-3" type="button"><span class="btn-glow"></span><span class="btn-label">+ READ THE LAW</span></button></span>',"flagship primary")
add("NAYA-BTN-012","Essential · Create","Buttons",'<button class="cx-btn elev-1" type="button">+ CREATE</button>',"quiet secondary")
add("NAYA-BTN-013","Essential · Details","Buttons",'<button class="cx-btn elev-1" type="button">◆ DETAILS</button>',"quiet secondary")
add("NAYA-BTN-014","Essential · Continue","Buttons",'<button class="cx-btn elev-1" type="button">→ CONTINUE</button>',"quiet secondary")
# ICONS — dual set
for i,(name,color,shape,lang) in enumerate(DUAL,1):
    add(f"NAYA-ICO-{i:03d}",f"{name} · dual","Icons",dual_icon(name,color,shape),f"{shape} = {lang}")
# ICONS — bottom bar set
for i,(name,key,color) in enumerate(BB,11):
    add(f"NAYA-ICO-{i:03d}",f"{name} · dock","Icons",bb_btn(name,key,color),"eco bottom bar")
# ORBS
for i,(name,color) in enumerate([("Magenta","#e84fff"),("Purple","#a06bff"),("Blue","#3fb8ff"),("Green","#2fe89e"),("Gold","#ffbf3d")],1):
    add(f"NAYA-ORB-{i:03d}",f"Orb · {name}","Orbs",f'<span class="orb" style="--oc:{color};--oc-rgb:{color[1:3]},{color[3:5]},{color[5:7]}"></span>',"breathes + orbits")
for i,(name,color,rgb) in enumerate([("Verified","#2fe89e","47,232,158"),("Demonstration","#ffbf3d","255,191,61"),("Claim","#3fb8ff","63,184,255")],6):
    add(f"NAYA-ORB-{i:03d}",f"Truth orb · {name}","Orbs",f'<span class="orb orb-sm" style="--oc:{color};--oc-rgb:{rgb}"></span>',"truth state")
# BOARDS
add("NAYA-BRD-001","Feature board","Boards",'<div class="hubboard elev-2" style="--bc:#a06bff;max-width:340px"><div class="hb-head"><span class="orb orb-sm" style="--oc:#a06bff;--oc-rgb:160,107,255"></span><div><div class="hb-kicker">Features</div><h3>Smart Note</h3></div></div><div class="hubsub" style="--bc:#e84fff"><span class="jw" style="--j:#e84fff">◆</span><b>Human Note</b></div></div>',"one color, one world")
add("NAYA-BRD-002","Sub-board","Boards",'<div class="hubsub elev-1" style="--bc:#3fb8ff;min-width:260px"><span class="jw" style="--j:#3fb8ff">◆</span><b>Child Note</b><span class="hb-play">▶</span></div>',"nests inside feature boards")
add("NAYA-BRD-003","Jewel bullets","Boards",'<div style="display:flex;gap:10px">'+"".join(f'<span class="jw elev-1" style="--j:{c}">◆</span>' for c in ["#e84fff","#a06bff","#3fb8ff","#2fe89e","#ffbf3d"])+'</div>',"five-cycle markers")
add("NAYA-BRD-004","Law rectangle","Boards",'<div class="lawrect elev-1" style="--lc:#a06bff;min-width:240px"><b>LAW 07 · RECTANGLES</b><span>Boards are rectangles — horizontal, stacked. Never grids of squares.</span></div>',"laws as rectangles")
# JEWELS — the beautiful ones, verbatim from the N5 jewel library
JWL_SPECTRUM = [("Magenta","#e84fff","232,79,255"),("Purple","#a06bff","160,107,255"),("Blue","#3fb8ff","63,184,255"),("Green","#2fe89e","47,232,158"),("Gold","#ffbf3d","255,191,61")]
for i,(name,color,rgb) in enumerate(JWL_SPECTRUM,1):
    add(f"NAYA-JWL-{i:03d}",f"Gem bullet · {name}","Jewels",f'<span class="gem-bullet" style="--tone:{color}"></span>',"drawn jewel, not a dot")
for i,(name,color,rgb) in enumerate(JWL_SPECTRUM,6):
    add(f"NAYA-JWL-{i:03d}",f"Mini-orb · {name}","Jewels",f'<span class="mini-orb" style="--c:{color}"></span>',"the luminous mark")
for i,(glyph,name,color,rgb) in enumerate([("✦","Spark","#e84fff","232,79,255"),("♥","Love","#3fb8ff","63,184,255"),("▶","Play","#2fe89e","47,232,158"),("◈","Focus","#ffbf3d","255,191,61")],11):
    add(f"NAYA-JWL-{i:03d}",f"Glyph orb · {name}","Jewels",f'<span class="orb orb--glyph orb--icon" style="--oc:{color};--oc-rgb:{rgb}">{glyph}</span>',"app icon, glyph at the core")
add("NAYA-JWL-015","Black orb","Jewels",'<span class="orb orb--black" style="--oc:#2fe89e;--oc-rgb:47,232,158"></span>',"dark soul, color rim")
add("NAYA-JWL-016","Hero orb","Jewels",'<span class="orb orb--hero" style="--oc:#a06bff;--oc-rgb:160,107,255"></span>',"the centerpiece, one per page")
add("NAYA-JWL-017","Twin orbit orb","Jewels",'<span class="orb orb--twin" style="--oc:#2fe89e;--oc-rgb:47,232,158"></span>',"two rings, counter-rotating")
# HUB ELEMENTS — extracted verbatim from Shawn's 12 hub pages (audit 2026-10-18)
add("NAYA-BTN-015","Ghost button","Buttons",'<button class="btn btn-ghost mini" type="button"><span>Open</span></button>',"hub workhorse button")
add("NAYA-BTN-016","Toggle chip","Buttons",'<button class="tgl on" type="button">Live</button>',"small on/off chip")
add("NAYA-BTN-017","Smart-note · Save","Buttons",'<button class="sn-btn primary sn-save" type="button">Save</button>',"dialog primary")
add("NAYA-BTN-018","Nav button · About","Buttons",'<a class="nav-button about-button" href="#"><span class="nav-icon">\u2726</span> ABOUT US</a>',"wide uppercase nav")
add("NAYA-ICO-023","Icon socket","Icons",'<span class="ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 11l9-8 9 8"/></svg></span>',"40px tinted tile")
add("NAYA-JWL-018","LED","Jewels",'<span class="led"></span>',"8px status dot")
add("NAYA-JWL-019","Corner jewel","Jewels",'<div style="position:relative;width:120px;height:80px"><span class="corner-jewel" style="top:6px;left:6px;--tone:#a06bff"></span><span class="corner-jewel" style="top:6px;right:6px;--tone:#e84fff"></span><span class="corner-jewel" style="bottom:6px;left:6px;--tone:#3fb8ff"></span><span class="corner-jewel" style="bottom:6px;right:6px;--tone:#2fe89e"></span></div>',"diamond card accents")
add("NAYA-BRD-005","Metric stat","Boards",'<div class="metric"><b>1,284</b><span>Plays this week</span></div>',"big-number stat")
add("NAYA-BRD-006","Empty state","Boards",'<div class="empty-instrument"><strong>Nothing here yet.</strong><p>This space exists — nothing has landed in it.</p></div>',"honest empty, never blank")
add("NAYA-BRD-007","Identity box","Boards",'<div class="id-box" style="--tone:#a06bff;--tone-glow:rgba(160,107,255,.5)"><div class="id-box-text"><div class="id-box-label">Your mark</div><div class="id-box-value">nayanet.live/shawn</div></div></div>',"tone-topped credential card")
add("NAYA-ROW-001","Meta row","Rows",'<div class="meta-row"><span>Today</span><span>Evidence-based</span><span>3 plays</span></div>',"metadata chips")
add("NAYA-ROW-002","Action row","Rows",'<div class="action-row"><button class="btn btn-ghost mini" type="button"><span>Open</span></button><button class="btn btn-ghost mini" type="button"><span>Share</span></button></div>',"card button container")
add("NAYA-ROW-003","Menu item","Rows",'<div style="min-width:220px"><div class="mi">Smart Lists</div><div class="mi">Spaces</div><div class="mi">Reports</div></div>',"divided menu row")
add("NAYA-ROW-004","Method row","Rows",'<div class="im-row"><span class="im-jewel"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><rect x="7" y="2.5" width="10" height="19" rx="2.5"/></svg></span><div><strong>iPhone</strong><ol class="im-steps"><li>Open Settings</li><li>Tap your name</li></ol></div></div>',"icon + title + steps")
add("NAYA-INP-001","Search bar","Inputs",'<div class="search-wrap"><input class="search-input" type="search" placeholder="Search today\u2026" aria-label="Search"></div>',"full-width search")
add("NAYA-INP-002","Alias field","Inputs",'<div class="alias-input-box"><label class="alias-label">Your handle</label><div class="alias-field-wrapper"><input type="text" class="alias-field-input" placeholder="pioneer" autocomplete="off"></div></div>',"display text input")
add("NAYA-HDR-001","Eyebrow","Headers",'<div class="eyebrow">NAYANET \u00b7 HUMAN-FACING INTELLIGENCE</div>',"small caps section label")
add("NAYA-HDR-002","Intelligence trio","Headers",'<div><div class="intel-type">Briefing</div><div class="intel-title">What today became</div><div class="intel-summary">Three plays finished, two spaces gained members.</div></div>',"type/title/summary stack")
add("NAYA-HDR-003","Step number","Headers",'<div class="num" style="--c:#a06bff"><span class="jewel"></span>Step One</div>',"numbered step label")
add("NAYA-MRK-001","Status pill","Markers",'<span class="pill live"><span class="dot"></span>Live</span>',"status badge")
add("NAYA-MRK-002","Done mark","Markers",'<div class="done-mark"><span class="tick">\u2713</span> AI ready</div>',"completion confirmation")
add("NAYA-MRK-003","Search highlight","Markers",'<div style="font-size:15px">quarterly <mark class="hl">report</mark> ready</div>',"match highlight")
add("NAYA-MRK-004","Divider bar","Markers",'<div style="display:flex;align-items:center;width:100%"><div class="bar"></div></div>',"hairline divider")
# NAV
add("NAYA-NAV-001","Smart tabs","Navigation",'<div class="smarttabs elev-1" style="display:flex;gap:8px;padding:8px"><button class="smarttab on" type="button">All</button><button class="smarttab" type="button">Start Here</button><button class="smarttab" type="button">+ Add</button></div>',"pill navigation")
add("NAYA-NAV-002","View tabs","Navigation",'<div style="display:flex;gap:8px"><button class="primo theme-purple elev-1" type="button" style="padding:10px 22px;font-size:12px">COLLECTIVE</button><button class="primo theme-blue elev-1" type="button" style="padding:10px 22px;font-size:12px">PERSONAL</button></div>',"collective / personal / activity")
add("NAYA-NAV-003","Eco bottom bar","Navigation",'<div class="eco-bottombar elev-2" style="position:static;border-radius:18px;padding:12px;gap:8px">'+"".join(bb_btn(n,k,c) for n,k,c in BB[:6])+'</div>',"the thumb row")
