#!/usr/bin/env python3
"""Smart Builder assembler v1 — contract data + library pieces -> working page.

Usage:
  python3 assemble.py --contract contracts/smart-builder-v1.json \
      --index ../../library/catalog/builder-index-v1.json \
      --template templates/page.html \
      --out /tmp/page.html --manifest /tmp/page.manifest.json

Repeatable: same contract + same index + same assembler -> same page.
Fine-tuning = edit the contract (words, wall picks), re-run.
"""
import argparse, json, hashlib, html as htmlmod, os, sys
from datetime import datetime, timezone

ASSEMBLER_VERSION = "assemble-v1"

def esc(s):
    return htmlmod.escape(str(s), quote=True)

def sha16(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()[:16]

# spectrum in law order, by section position (hero takes purple)
SPECTRUM = ["#a06bff", "#6675ff", "#55b9ee", "#40d3bb", "#2fe89e", "#b8ee57",
            "#f1d75a", "#ffbf3d", "#ff9a5a", "#ff6b3d", "#ff5e6c", "#e84fff"]

# section chrome: real library CSS blocks, re-scoped .nb-scope -> .nb-chrome
# so section chrome never collides with wall specimen CSS.
CHROME_CSS_IDS = [
    '0d880c7f3c3d',  # demo-board — the section shell
    'dd8909d6a903',  # card — intake mode cards
    'e880e2feafeb',  # typecard — template cards
    '577bb46a3477',  # lawcard — feature / point / loop rows
]

def chrome_css(cssbank):
    out = []
    for cid in CHROME_CSS_IDS:
        css = cssbank[cid].replace('.nb-scope', '.nb-chrome')
        out.append('/* chrome:%s */\n%s' % (cid, css))
    return '\n'.join(out)

def specimen_card(model, p):
    # contract page: specimens are sampled, not shopped — no dead controls.
    return (
        '<div class="spec" data-model="%s">'
        '<div class="spec-stage"><div class="nb-scope">%s</div></div>'
        '<div class="spec-meta"><div><b>%s</b><i>%s · %s</i></div></div>'
        '</div>' % (esc(model), p['html'], esc(p['label']), esc(model), esc(p['kind']))
    )

def lawcard(title, desc, color):
    return (
        '<div class="nb-chrome" style="margin-bottom:12px">'
        '<div class="lawcard" style="--lc:%s">'
        '<div class="ln" style="text-transform:uppercase"><span class="ld"></span><span>%s</span></div>'
        '<p>%s</p></div></div>' % (color, esc(title), esc(desc))
    )

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--contract', required=True)
    ap.add_argument('--index', required=True)
    ap.add_argument('--template', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--manifest', required=True)
    a = ap.parse_args()

    contract = json.load(open(a.contract))
    index = json.load(open(a.index))
    tpl = open(a.template).read()
    pieces, cssbank = index['pieces'], index['css_bank']

    # ---- wall: real pieces, CSS collected for inlining ----
    wall_css_ids, wall_html = [], []
    for cat, models in contract['wall'].items():
        cards = []
        for m in models:
            p = pieces[m]
            if p['css_id'] and p['css_id'] not in wall_css_ids:
                wall_css_ids.append(p['css_id'])
            cards.append(specimen_card(m, p))
        wall_html.append(
            '<h3 class="wallcat">%s <span>%d pieces</span></h3>'
            '<div class="grid g4 wallgrid">%s</div>' % (esc(cat), len(models), ''.join(cards)))
    wall_css = '\n'.join('/* css:%s */\n%s' % (cid, cssbank[cid]) for cid in wall_css_ids)

    # ---- contract-driven sections: every section composed from real pieces ----
    # intake modes -> the real .card piece
    modes = []
    for i, m in enumerate(contract['intake']['modes']):
        c = SPECTRUM[(i + 1) % len(SPECTRUM)]
        modes.append(
            '<div class="nb-chrome"><button class="card mode" aria-pressed="%s" data-mode="%s" '
            'style="--accent:%s;--accent-soft:%s73;text-align:left;cursor:pointer;width:100%%;'
            'font:inherit;color:inherit">'
            '<span style="display:block;font-size:11px;letter-spacing:.22em;text-transform:uppercase;'
            'font-weight:700;color:%s;margin-bottom:10px">%s</span>'
            '<h3>%s</h3><p class="fine">%s</p></button></div>'
            % ("true" if i == 0 else "false", esc(m['id']), c, c, c,
               esc(m['n']), esc(m['title']), esc(m['desc'])))
    intake_modes = '<div class="grid g3" role="group" aria-label="Intake modes">%s</div>' % ''.join(modes)

    # contract fields -> rows inside the real demo-board shell (shell is in the template)
    fields = ''.join(
        '<div class="field"><span class="fk">%s</span><span class="fv">%s</span></div>' % (esc(k), esc(v))
        for k, v in contract['fields'])

    # templates -> the real .typecard piece, one spectrum color per card
    templates = ''.join(
        '<div class="nb-chrome"><div class="typecard" style="--tc:%s">'
        '<div class="tk">%s</div>'
        '<h3 style="font-size:19px;margin:0 0 6px;color:var(--white)">%s</h3>'
        '<p style="font-size:14px;color:var(--slate);margin:0">%s</p></div></div>'
        % (SPECTRUM[(6 + i) % len(SPECTRUM)], esc(n), esc(t), esc(d))
        for i, (n, t, d) in enumerate(contract['templates']))
    templates = '<div class="grid g4">%s</div>' % templates

    # features / gallery / customize -> the real .lawcard piece
    features = ''.join(
        lawcard(t, d, SPECTRUM[(7 + i) % len(SPECTRUM)])
        for i, (t, d) in enumerate(contract['features']))
    gallery_html = ''.join(
        lawcard(t, d, SPECTRUM[(4 + i) % len(SPECTRUM)])
        for i, (t, d) in enumerate(contract['gallery']['points']))
    customize_html = ''.join(
        lawcard(t, d, SPECTRUM[(5 + i) % len(SPECTRUM)])
        for i, (t, d) in enumerate(contract['customize']['points']))

    # loop -> the real .lawcard piece
    loop = ''.join(
        lawcard(t, d, SPECTRUM[(9 + i) % len(SPECTRUM)])
        for i, (t, d) in enumerate(contract['loop']))

    page = tpl
    machine_raw = json.dumps(contract['machine'], indent=2, ensure_ascii=False)
    for key, val in {
        '%%TITLE%%': esc(contract['title']),
        '%%KICKER%%': esc(contract['kicker']),
        '%%LEDE%%': esc(contract['lede']),
        '%%INTAKE_MODES%%': intake_modes,
        '%%FIELDS%%': fields,
        '%%WALL_HTML%%': ''.join(wall_html),
        '%%WALL_CSS%%': wall_css,
        '%%CHROME_CSS%%': chrome_css(cssbank),
        '%%GALLERY_TITLE%%': esc(contract['gallery']['title']),
        '%%GALLERY_LEDE%%': esc(contract['gallery']['lede']),
        '%%GALLERY_POINTS%%': gallery_html,
        '%%CUSTOMIZE_TITLE%%': esc(contract['customize']['title']),
        '%%CUSTOMIZE_LEDE%%': esc(contract['customize']['lede']),
        '%%CUSTOMIZE_POINTS%%': customize_html,
        '%%TEMPLATES%%': templates,
        '%%FEATURES%%': features,
        '%%LOOP%%': loop,
        '%%PROMISE_BIG%%': esc(contract['promise']['big']).replace('within 24 hours.', '<em>within 24 hours.</em>'),
        '%%PROMISE_SUB%%': esc(contract['promise']['sub']),
        '%%MACHINE_JSON%%': machine_raw,  # raw: <pre> content, never an attribute
    }.items():
        page = page.replace(key, val)

    open(a.out, 'w').write(page)

    manifest = {
        'assembler': ASSEMBLER_VERSION,
        'built_utc': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'contract': {'path': a.contract, 'sha16': sha16(open(a.contract, 'rb').read())},
        'index': {'path': a.index, 'entries': len(pieces),
                  'meta': index.get('meta', {})},
        'template_sha16': sha16(open(a.template, 'rb').read()),
        'page': {'path': a.out, 'bytes': len(page.encode()), 'sha16': sha16(page.encode())},
        'wall_pieces': [m for models in contract['wall'].values() for m in models],
        'verification': 'pending — run verify-build.py',
    }
    json.dump(manifest, open(a.manifest, 'w'), indent=2)
    print('page:', a.out, manifest['page']['bytes'], 'bytes')
    print('manifest:', a.manifest)

if __name__ == '__main__':
    main()
