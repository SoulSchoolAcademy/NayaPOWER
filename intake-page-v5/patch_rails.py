#!/usr/bin/env python3
src = open('gen.py').read()

old_cards = 'cards = "\\n".join(card(p) for p in PIECES)'
assert old_cards in src, "cards anchor"
rails_py = '''
def rail(cat):
    cs = "\\n".join(card(p) for p in PIECES if p["cat"] == cat)
    head = '<div class="railhead"><span class="pmodel">' + cat.upper() + '</span><span style="font-size:12px;opacity:.5">scroll sideways</span></div>'
    return '<div class="railblock">' + head + '<div class="rail">' + cs + '</div></div>'
rails = "\\n".join(rail(c) for c in CATS[1:])
'''
src = src.replace(old_cards, old_cards + "\n" + rails_py)

old_css = '.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:20px}}'
assert old_css in src, "css anchor"
new_css = old_css + '''
.railblock{margin:0 0 34px}
.railhead{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px}
.rail{display:flex;gap:18px;overflow-x:auto;padding:10px 4px 22px;scroll-snap-type:x mandatory}
.rail::-webkit-scrollbar{height:8px}.rail::-webkit-scrollbar-thumb{background:#2a2a35;border-radius:4px}
.rail .pcard{flex:0 0 300px;scroll-snap-align:start}'''
src = src.replace(old_css, new_css)

old_sec = '<div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:20px">{filters}</div>\n<div class="grid">{cards}</div>'
assert old_sec in src, "section anchor"
src = src.replace(old_sec, '{rails}')
open('gen.py','w').write(src)
print("rails in")
