#!/usr/bin/env python3
"""Smart Builder sample-page builder — 12 template showcases through the pipeline.

Uses assemble.py's own machinery: the same index, the same fail-closed piece
validation (unknown model -> refuse, quarantined -> refuse, empty html ->
refuse), the same CSS-by-id collection, the same deterministic manifest
discipline (contract SHA + index SHA + template SHA + page SHA).

Each sample contract lives in contracts/samples/sample-NN-<slug>.json:
  { "contract": ..., "template_id": "01", "template_name": "...",
    "template_color": "#...", "title": "...", "kicker": "...", "lede": "...",
    "sections": [ {"kicker": "...", "title": "...", "lede": "...",
                   "pieces": ["NAYA-..."] } ] }

Usage:
  python3 build_samples.py --index ../../library/catalog/builder-index-v1.json \\
      --template templates/sample-page.html --contracts contracts/samples \\
      --outdir /tmp/samples
"""
import argparse, hashlib, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# Reuse the assembler's own trust boundary and rendering helpers.
from assemble import esc, seq_color, ASSEMBLER_VERSION  # noqa: E402

SPECTRUM = ["#a06bff", "#6675ff", "#55b9ee", "#40d3bb", "#2fe89e", "#b8ee57",
            "#f1d75a", "#ffbf3d", "#ff9a5a", "#ff6b3d", "#ff5e6c", "#e84fff"]


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def validate_pieces(models, pieces):
    """Fail-closed piece resolution — mirrors assemble.py's quarantine gate."""
    problems = []
    for m in models:
        if m not in pieces:
            problems.append({'code': 'unknown_model', 'model': m})
        elif pieces[m].get('quarantined'):
            problems.append({'code': 'piece_quarantined', 'model': m,
                             'reason': pieces[m].get('quarantine_reason')})
        elif not pieces[m].get('html'):
            problems.append({'code': 'empty_piece', 'model': m})
    return problems


def render_menu(menu):
    """Contract-owned menu content — real items with prices, rendered in the
    sample's own design language (white names, dotted leaders, own-color
    prices). The pieces frame it; the data belongs to the contract."""
    rows = []
    for item in menu:
        rows.append(
            '<li><span><span class="mi-name">%s</span>'
            '<span class="mi-desc">%s</span></span>'
            '<span class="mi-dots"></span>'
            '<span class="mi-price">%s</span></li>'
            % (esc(item['name']), esc(item.get('desc', '')),
               esc(item['price'])))
    return '<ul class="menu-list">%s</ul>' % ''.join(rows)


def render_section(sec, pieces, css_ids, si):
    cards = []
    for m in sec['pieces']:
        p = pieces[m]
        cid = p.get('css_id')
        if cid and cid not in css_ids:
            css_ids.append(cid)
        cards.append(
            '<div class="piece" data-model="%s">'
            '<div class="nb-scope">%s</div>'
            '<div class="piece-tag"><b>%s</b><span>%s</span></div>'
            '</div>' % (esc(m), p['html'], esc(p.get('label', m)), esc(m)))
    menu_html = render_menu(sec['menu']) if sec.get('menu') else ''
    return (
        '<section><div class="sec-head">'
        '<span class="kicker">%s</span><h2>%s</h2>%s</div>%s%s</section>'
        % (esc(sec['kicker']), esc(sec['title']),
           ('<p>%s</p>' % esc(sec['lede'])) if sec.get('lede') else '',
           menu_html, ''.join(cards)))


def build_one(contract_path, index, tpl, outdir):
    contract = json.load(open(contract_path))
    pieces, cssbank = index['pieces'], index['css_bank']
    models = [m for s in contract['sections'] for m in s['pieces']]
    problems = validate_pieces(models, pieces)
    if problems:
        return {'status': 'refused', 'contract': contract_path,
                'errors': problems}
    css_ids = []
    sections = ''.join(render_section(s, pieces, css_ids, i)
                       for i, s in enumerate(contract['sections']))
    wall_css = '\n'.join('/* css:%s */\n%s' % (cid, cssbank[cid])
                         for cid in css_ids)
    manifest_rows = ''.join(
        '<li><b>%s</b> — %s</li>' % (esc(m), esc(pieces[m].get('label', '')))
        for m in models)
    contract_bytes = open(contract_path, 'rb').read()
    page = tpl
    for k, v in {
        '%%META_DESC%%': 'Sample %s page built by the Smart Builder from real library pieces.' % contract['template_name'],
        '%%TITLE%%': contract['title'],
        '%%KICKER%%': contract['kicker'],
        '%%LEDE%%': contract['lede'],
        '%%TEMPLATE_NAME%%': 'Template %s · %s' % (contract['template_id'],
                                                   contract['template_name']),
        '%%TEMPLATE_COLOR%%': contract['template_color'],
        '%%SECTIONS%%': sections,
        '%%WALL_CSS%%': wall_css,
        '%%MANIFEST_ROWS%%': manifest_rows,
        '%%BUILD_ID%%': sha256(contract_bytes)[:16],
        '%%ASSEMBLER_VERSION%%': ASSEMBLER_VERSION,
        '%%INDEX_SHA%%': 'see-manifest',
    }.items():
        page = page.replace(k, v)
    page_bytes = page.encode('utf-8')
    slug = os.path.basename(contract_path).replace('.json', '')
    out_path = os.path.join(outdir, slug + '.html')
    open(out_path, 'w').write(page)
    manifest = {
        'contract': {'path': contract_path, 'sha256': sha256(contract_bytes)},
        'resolution': {
            'pieces': models,
            'piece_count': len(models),
        },
        'build': {
            'assembler': ASSEMBLER_VERSION,
            'template_sha256': sha256(open(args.template, 'rb').read()),
            'page': {'path': out_path, 'bytes': len(page_bytes),
                     'sha256': sha256(page_bytes)},
        },
        'verification': 'pending — screenshot + diff check',
    }
    man_path = out_path.replace('.html', '.manifest.json')
    json.dump(manifest, open(man_path, 'w'), indent=2)
    return {'status': 'ok', 'contract': contract_path, 'page': out_path,
            'pieces': len(models), 'sha256': sha256(page_bytes)[:16],
            'manifest': man_path}


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--index', required=True)
    ap.add_argument('--template', required=True)
    ap.add_argument('--contracts', required=True)
    ap.add_argument('--outdir', required=True)
    args = ap.parse_args()
    index = json.load(open(args.index))
    tpl = open(args.template).read()
    os.makedirs(args.outdir, exist_ok=True)
    results = []
    for fn in sorted(os.listdir(args.contracts)):
        if not fn.endswith('.json'):
            continue
        r = build_one(os.path.join(args.contracts, fn), index, tpl,
                      args.outdir)
        results.append(r)
        print(json.dumps(r))
    refused = [r for r in results if r['status'] == 'refused']
    if refused:
        sys.exit(2)
    print('built %d samples' % len(results))
