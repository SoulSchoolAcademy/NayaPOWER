#!/usr/bin/env python3
src = open('gen.py').read()

old_t = '''TEMPLATES = [("Personal","#a06bff","flagship"),("Today","#40d3bb","briefing"),("Smart list","#ffbf3d","lists"),
 ("Business","#3fb8ff","landing"),("Booking","#2fe89e","schedule"),("Product","#e84fff","sell"),
 ("Event","#ff9a5a","gather"),("Community","#ff5e6c","belong"),("Portfolio","#6675ff","show"),
 ("Menu","#b8ee57","taste"),("Signup","#40d3bb","join"),("Dashboard","#a06bff","track")]
tmpls = "\\n".join(f\'\'\'<div class="tmpl elev-1" data-t="{n}" style="--tc:{c}"><span class="tdot" style="--tc:{c}"></span><b>{n}</b><div style="font-size:12px;opacity:.6;margin-top:6px">{d}</div></div>\'\'\' for n,c,d in TEMPLATES)'''
assert old_t in src, "tmpl anchor"

T = [
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
 ("Dashboard","#a06bff","track","Your numbers, live — track everything that matters."),
]
lines = []
for n, c, tag, desc in T:
    lines.append(
        '<div class="tcard" data-t="' + n + '" style="--tc:' + c + '">'
        '<span class="tdot" style="--tc:' + c + '"></span>'
        '<b style="font-size:17px;color:#fff">' + n + '</b>'
        '<div style="font-size:12px;color:#fff;opacity:.75;margin-top:4px">' + tag + '</div>'
        '<div class="tdetail">' + desc + '<br><br><b style="color:' + c + '">Ships with the standard seven functions on.</b> Your cart pieces land on top.</div>'
        '<br><button class="tview" style="--tc:' + c + '" type="button">VIEW</button></div>'
    )
new_t = "TEMPLATES = " + repr([(n, c, t) for n, c, t, d in T]) + '\ntmpls = "\\n".join([\n' + ",\n".join('"""' + l + '"""' for l in lines) + '\n])'
src = src.replace(old_t, new_t)

old_js = "document.querySelectorAll('.tmpl').forEach(t=>t.onclick=()=>{document.querySelectorAll('.tmpl').forEach(x=>x.classList.remove('sel'));t.classList.add('sel');});"
assert old_js in src, "js anchor"
new_js = ("document.querySelectorAll('.tcard').forEach(t=>{const v=t.querySelector('.tview');"
 "v.onclick=e=>{e.stopPropagation();const was=t.classList.contains('open');"
 "document.querySelectorAll('.tcard').forEach(x=>{x.classList.remove('open','sel');x.querySelector('.tview').textContent='VIEW';});"
 "t.classList.add('open','sel');v.textContent=was?'VIEW':'SELECTED';};});")
src = src.replace(old_js, new_js)
src = src.replace('document.querySelector(\'.tmpl.sel\')', 'document.querySelector(\'.tcard.sel\')')

open('gen.py', 'w').write(src)
print("templates rebuilt")
