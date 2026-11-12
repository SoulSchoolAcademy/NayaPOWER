#!/usr/bin/env python3
"""v6 patches: idea header, icon functions + extras, spectrum law, template rebuild, white text."""
src = open('gen.py').read()
def rep(old, new):
    global src
    assert old in src, "ANCHOR MISSING: " + old[:60]
    src = src.replace(old, new)

# ---- 1. Step 1: idea, not vision ----
rep('<h2 class="stept">Tell Naya your vision</h2>\n<p class="lede">Type it, paste it, or dictate it — however your vision comes out.</p>',
    '<h2 class="stept">Tell Naya your idea</h2>\n<p class="lede">Type it, paste it, dictate it — however your idea comes out.</p>')

# ---- 2. Step 2: icon function rows ----
FUNCS = [
 ("Smart Mail","#3fb8ff","Mail","Your email, turned into an intelligent inbox.",True,
  '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>'),
 ("Smart Lists","#ffbf3d","Ledger","Living collections that organize what matters.",True,
  '<path d="M4 19v-8m5 8V5m5 14V9m5 10V3"/>'),
 ("Smart Space","#a06bff","Spaces","A home base for a project, topic, or part of your life.",True,
  '<rect x="4" y="4" width="7" height="7" rx="1.5"/><rect x="13" y="4" width="7" height="7" rx="1.5"/><rect x="4" y="13" width="7" height="7" rx="1.5"/><rect x="13" y="13" width="7" height="7" rx="1.5"/>'),
 ("Connect + communicate","#2fe89e","People","Message and share with people, right from the app.",True,
  '<circle cx="9" cy="8" r="3"/><path d="M3 20v-2c0-6 12-6 12 0v2M17 5a3 3 0 0 1 0 6m1 4c2 0 3 2 3 4v1"/>'),
 ("Intelligence Today","#e84fff","Today","Your daily briefing — what matters, every morning.",True,
  '<path d="M12 3l2.2 6.6L21 12l-6.8 2.4L12 21l-2.2-6.6L3 12l6.8-2.4z"/>'),
 ("Personal social feed","#ff9a5a","Grow","Your own feed — post once, it goes everywhere you allow.",True,
  '<circle cx="12" cy="12" r="8"/><path d="M12 4v16M4 12h16"/>'),
 ("Smart Tabs","#6675ff","Vision","Contextual windows — the right view for the moment.",True,
  '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7-10-7-10-7z"/><circle cx="12" cy="12" r="3"/>'),
]
EXTRAS = [
 ("Ask Naya","#40d3bb","Ask anything — answers from your own intelligence.",'<circle cx="11" cy="11" r="7"/><path d="M16.5 16.5L21 21"/>'),
 ("Reports","#6675ff","Daily, weekly, monthly — your numbers, explained.",'<path d="M5 19v-6m5 6V5m5 14v-9m4 9H3"/>'),
 ("Booking doors","#2fe89e","Let people book time with you.",'<rect x="5" y="3" width="14" height="18" rx="1"/><circle cx="15" cy="12" r="1.2"/>'),
 ("Guard","#ff5e6c","You decide who sees what. Always.",'<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/>'),
 ("Saved","#40d3bb","Everything you keep, in one place.",'<path d="M6 3h12v18l-6-4-6 4z"/>'),
 ("Calendar","#ffbf3d","Your schedule, intelligent.",'<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>'),
 ("Share","#a06bff","Send anything, anywhere.",'<circle cx="6" cy="12" r="2.5"/><circle cx="18" cy="6" r="2.5"/><circle cx="18" cy="18" r="2.5"/><path d="M8.2 10.8l7.6-3.6M8.2 13.2l7.6 3.6"/>'),
]
def frow(name,color,sub,path,on):
    return ('<div class="frow elev-1"><span class="fic" style="--fc:'+color+'">'
      '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">'+path+'</svg></span>'
      '<span style="flex:1"><b>'+name+'</b><span class="fsub">'+sub+'</span></span>'
      '<span class="tog'+(' on' if on else '')+'"></span></div>')
std_rows = "\n".join(frow(n,c,s,p,True) for n,c,s,p,_ in [(f[0],f[1],f[3],f[5],f[4]) for f in FUNCS])
ext_rows = "\n".join(frow(n,c,s,p,False) for n,c,s,p in EXTRAS)
funcs_html = ('<div class="frow-head">STANDARD — ON, UNCHECK TO REMOVE</div>'+std_rows+
 '<details class="xdrop elev-1"><summary>EXTRA FEATURES — TAP TO BROWSE</summary>'+ext_rows+'</details>')

old_q2 = """<label style="font-size:13px;opacity:.7">Which functions must it have?</label>
<div style="display:flex;gap:10px;flex-wrap:wrap;margin:10px 0 18px;align-items:center">
<span style="display:flex;align-items:center;gap:8px;font-size:13px">Smart Mail <span class="tog on"></span></span>
<span style="display:flex;align-items:center;gap:8px;font-size:13px">Smart Lists <span class="tog on"></span></span>
<span style="display:flex;align-items:center;gap:8px;font-size:13px">Smart Space <span class="tog on"></span></span>
<span style="display:flex;align-items:center;gap:8px;font-size:13px">Smart Tabs <span class="tog on"></span></span>
<span style="display:flex;align-items:center;gap:8px;font-size:13px">Intelligence Today <span class="tog"></span></span>
</div>"""
rep(old_q2, '<label style="font-size:13px;color:#fff">Which functions must it have?</label>\n'+funcs_html)

# ---- 3. spectrum law on cards ----
SPECTRUM = ["#e84fff","#a06bff","#3fb8ff","#2fe89e","#ffbf3d","#ff5e6c","#ff9a5a"]
old_card = '''def card(p):
    sz = "".join(f'<button class="szpill{" on" if s=="M" else ""}" data-s="{s}" data-z="{z}">{s}</button>' for s,z in SIZES)
    new_tail = "return f" + q*3 + '<div class="pcard" style="--sc:"+q+"'"+sc+"'"""'+" data-cat="{p["cat"]}" data-model="{p["model"]}" data-name="{p["name"]}">' + q*3
assert old_card in src, "card anchor"
new_card = '''_ci = [0]
def card(p):
    _ci[0] += 1
    sc = SPECTRUM[(_ci[0]-1) % len(SPECTRUM)]
    sz = "".join(f'<button class="szpill{" on" if s=="M" else ""}" data-s="{s}" data-z="{z}">{s}</button>' for s,z in SIZES)
    return f\'\'\'<div class="pcard" style="--sc:'''+sc+'''" data-cat="{p["cat"]}" data-model="{p["model"]}" data-name="{p["name"]}">'''
src = src.replace(old_card, new_card)
src = src.replace("SIZES = [", "SPECTRUM = " + repr(SPECTRUM) + "\nSIZES = [")

# ---- 4. CSS: select green / notes blue hover, spectrum card glow, frow, templates, white text ----
old_elev_end = '.tdot{width:14px;height:14px;border-radius:50%;background:var(--tc);box-shadow:0 0 10px var(--tc);display:inline-block;margin-right:8px}'
assert old_elev_end in src, "elev anchor"
add_css = old_elev_end + '''
.pcard{background:linear-gradient(180deg,#101016,#0a0a0f);border:1.5px solid rgba(255,255,255,.1);box-shadow:0 8px 22px rgba(0,0,0,.6),inset 0 1px 0 rgba(255,255,255,.14)}
.pcard:hover{transform:translateY(-4px);border-color:var(--sc);box-shadow:0 16px 40px rgba(0,0,0,.65),0 0 28px -8px var(--sc),inset 0 1px 0 rgba(255,255,255,.2)}
.pmodel{color:var(--sc)}
.btn-select:hover{border-color:#2fe89e;box-shadow:0 0 20px -4px #2fe89e,inset 0 1px 0 rgba(255,255,255,.2);transform:translateY(-2px)}
.btn-notes:hover{border-color:#3fb8ff;box-shadow:0 0 20px -4px #3fb8ff,inset 0 1px 0 rgba(255,255,255,.2);transform:translateY(-2px)}
.frow{display:flex;gap:14px;align-items:center;background:#0d0d13;border:1px solid rgba(255,255,255,.09);border-radius:16px;padding:14px 16px;margin:10px 0}
.frow b{display:block;font-size:15px;color:#fff}
.fsub{display:block;font-size:13px;color:#fff;opacity:.75;margin-top:2px}
.fic{width:48px;height:48px;flex:none;border-radius:14px;display:flex;align-items:center;justify-content:center;background:radial-gradient(circle at 35% 30%,var(--fc),#0a0a0e 78%);border:1.5px solid var(--fc);box-shadow:0 6px 16px rgba(0,0,0,.6),0 0 14px -4px var(--fc),inset 0 1px 0 rgba(255,255,255,.25)}
.frow-head{font-size:11px;letter-spacing:.2em;color:#fff;opacity:.7;margin:14px 0 4px}
.xdrop{margin:14px 0;border:1px solid rgba(255,255,255,.12);border-radius:16px;background:#0d0d13;overflow:hidden}
.xdrop summary{padding:16px;cursor:pointer;font-size:13px;letter-spacing:.14em;color:#fff;list-style:none}
.xdrop summary::-webkit-details-marker{display:none}
.xdrop .frow{margin:10px 14px}
.tcard{border:1.5px solid var(--tc);border-radius:20px;padding:24px;cursor:default;background:linear-gradient(180deg,#121218,#0b0b0f);transition:all .3s var(--ease)}
.tcard:hover{box-shadow:0 16px 40px rgba(0,0,0,.6),0 0 30px -8px var(--tc);transform:translateY(-4px)}
.tcard.sel{box-shadow:0 0 0 2px var(--tc),0 0 34px -6px var(--tc)}
.tview{display:inline-block;margin-top:14px;padding:13px 34px;border-radius:30px;border:1.5px solid rgba(255,255,255,.35);background:#0a0a0e;color:#fff;font-size:13px;font-weight:800;letter-spacing:.1em;cursor:pointer;transition:all .25s var(--ease)}
.tview:hover{border-color:var(--tc);box-shadow:0 0 22px -4px var(--tc),inset 0 1px 0 rgba(255,255,255,.2);transform:translateY(-2px)}
.tdetail{display:none;margin-top:14px;font-size:14px;line-height:1.7;color:#fff}
.tcard.open .tdetail{display:block}
.lede{color:#F8F7FB;opacity:.92}
label{color:#fff !important}'''
src = src.replace(old_elev_end, add_css)

# ---- 5. templates rebuild ----
old_t = '''TEMPLATES = [("Personal","#a06bff","flagship"),("Today","#40d3bb","briefing"),("Smart list","#ffbf3d","lists"),
 ("Business","#3fb8ff","landing"),("Booking","#2fe89e","schedule"),("Product","#e84fff","sell"),
 ("Event","#ff9a5a","gather"),("Community","#ff5e6c","belong"),("Portfolio","#6675ff","show"),
 ("Menu","#b8ee57","taste"),("Signup","#40d3bb","join"),("Dashboard","#a06bff","track")]
tmpls = "\\n".join(f\'\'\'<div class="tmpl elev-1" data-t="{n}" style="--tc:{c}"><span class="tdot" style="--tc:{c}"></span><b>{n}</b><div style="font-size:12px;opacity:.6;margin-top:6px">{d}</div></div>\'\'\' for n,c,d in TEMPLATES)'''
assert old_t in src, "tmpl anchor"
new_t = '''TEMPLATES = [
 ("Personal","#a06bff","flagship","Your home on NayaNET — profile, feed, spaces. The one everything orbits."),
 ("Today","#40d3bb","briefing","Your daily briefing — what matters, every morning, in your voice."),
 ("Smart list","#ffbf3d","lists","Living lists that organize what matters and stay useful."),
 ("Business","#3fb8ff","landing","Your business front door — services, booking, contact."),
 ("Booking","#2fe89e","schedule","Appointments made simple — a calendar that books itself."),
 ("Product","#e84fff","sell","Sell one thing beautifully — page, price, buy."),
 ("Event","#ff9a5a","gather","Gather people — invites, RSVP, day-of, all handled."),
 ("Community","#ff5e6c","belong","Your people's home base — feed, spaces, belonging."),
 ("Portfolio","#6675ff","show","Show your work — the gallery that sells for you."),
 ("Menu","#b8ee57","taste","Your menu, your prices — order-ready."),
 ("Signup","#40d3bb","join","One page that converts — join, subscribe, start."),
 ("Dashboard","#a06bff","track","Your numbers, live — track everything that matters.")]
tmpls = "\\n".join('<div class="tcard" data-t="'+n+'" style="--tc:'+c+'"><span class="tdot" style="--tc:'+c+'"></span><b style="font-size:17px">'+n+'</b><div style="font-size:12px;color:#fff;opacity:.75;margin-top:4px">'+tag+'</div><div class="tdetail">'+desc+'<br><br><b style="color:'+c+'">This template ships with the standard seven functions on.</b> Your cart pieces land on top.</div><br><button class="tview" style="--tc:'+c+'" type="button">VIEW</button></div>' for n,c,tag,desc in TEMPLATES)'''
src = src.replace(old_t, new_t)
src = src.replace('<div class="tgrid">{tmpls}</div>', '<div class="tgrid">{tmpls}</div>')

# ---- 6. JS: template view/expand + select ----
old_js_t = '''document.querySelectorAll('.tmpl').forEach(t=>t.onclick=()=>{document.querySelectorAll('.tmpl').forEach(x=>x.classList.remove('sel'));t.classList.add('sel');});'''
assert old_js_t in src, "js tmpl anchor"
new_js_t = '''document.querySelectorAll('.tcard').forEach(t=>{const v=t.querySelector('.tview');
 v.onclick=e=>{e.stopPropagation();const was=t.classList.contains('open');
  document.querySelectorAll('.tcard').forEach(x=>{x.classList.remove('open','sel');x.querySelector('.tview').textContent='VIEW';});
  t.classList.add('open','sel');v.textContent=was?'VIEW':'✓ SELECTED';};});'''
src = src.replace(old_js_t, new_js_t)
src = src.replace("document.querySelector('.tmpl.sel')", "document.querySelector('.tcard.sel')")

open('gen.py','w').write(src)
print("v6 patched")
