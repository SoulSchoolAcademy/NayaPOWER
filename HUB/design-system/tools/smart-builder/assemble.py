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
KICKERS = ["indigo", "sapphire", "teal", "emerald", "lime",
           "yellow", "gold", "orange", "rich-orange", "magenta"]

def specimen_card(model, p, add_btn=True):
    add = ''
    if add_btn:
        add = ('<button class="spec-add" data-add="%s" aria-label="Add %s to the build tray">+ Add</button>'
               % (esc(model), esc(p['label'])))
    return (
        '<div class="spec" data-model="%s">'
        '<div class="spec-stage"><div class="nb-scope">%s</div></div>'
        '<div class="spec-meta"><div><b>%s</b><i>%s · %s</i></div>%s</div>'
        '</div>' % (esc(model), p['html'], esc(p['label']), esc(model), esc(p['kind']), add)
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

    # ---- contract-driven sections ----
    modes = []
    for i, m in enumerate(contract['intake']['modes']):
        modes.append(
            '<button class="board mode" aria-pressed="%s" data-mode="%s">'
            '<span class="kicker" style="color:var(--sp-%s)">%s</span>'
            '<h3>%s</h3><p>%s</p></button>'
            % ("true" if i == 0 else "false", esc(m['id']),
               KICKERS[i % len(KICKERS)], esc(m['n']), esc(m['title']), esc(m['desc'])))
    intake_modes = '<div class="grid g3" role="group" aria-label="Intake modes">%s</div>' % ''.join(modes)

    fields = ''.join(
        '<div class="field"><span class="fk">%s</span><span class="fv">%s</span></div>' % (esc(k), esc(v))
        for k, v in contract['fields'])
    fields = '<div class="contract">%s</div>' % fields

    templates = ''.join(
        '<div class="tpl"><div class="n">%s</div><h3>%s</h3><p>%s</p></div>' % (esc(n), esc(t), esc(d))
        for n, t, d in contract['templates'])
    templates = '<div class="grid g5">%s</div>' % templates

    features = ''.join(
        '<div class="feat"><span class="dot" style="background:var(--sp-%s)"></span>'
        '<div><b>%s</b><p>%s</p></div></div>' % (KICKERS[i % len(KICKERS)], esc(t), esc(d))
        for i, (t, d) in enumerate(contract['features']))
    features = '<div class="board">%s</div>' % features

    loop = ''.join(
        '<div class="step"><span class="kicker" style="color:var(--sp-%s)">%d</span>'
        '<b>%s</b><small>%s</small></div>' % (KICKERS[i % len(KICKERS)], i + 1, esc(t), esc(d))
        for i, (t, d) in enumerate(contract['loop']))
    loop = '<div class="board loop">%s</div>' % loop

    # ---- search corpus: full piece list, compact ----
    search_pieces = [
        {'model': m, 'label': p['label'], 'cat': p['category'], 'kind': p['kind'],
         'tags': p['tags'], 'html': p['html'], 'css_id': p['css_id']}
        for m, p in pieces.items()
    ]

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
        '%%TEMPLATES%%': templates,
        '%%FEATURES%%': features,
        '%%LOOP%%': loop,
        '%%PROMISE_BIG%%': esc(contract['promise']['big']).replace('within 24 hours.', '<em>within 24 hours.</em>'),
        '%%PROMISE_SUB%%': esc(contract['promise']['sub']),
        '%%PIECES_JSON%%': json.dumps(search_pieces, ensure_ascii=False),
        '%%CSSBANK_JSON%%': json.dumps(cssbank, ensure_ascii=False),
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
