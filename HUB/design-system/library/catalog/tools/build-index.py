"""Build the builder's index: every catalog model -> human label + real HTML + real CSS.

Portable: all paths resolve relative to this repo checkout. Run from anywhere:
  python3 HUB/design-system/library/catalog/tools/build-index.py [--catalog PATH] [--out PATH]
A cold checkout reproduces the checked-in index byte-for-byte (compare SHA-256).
"""
import json, re, sys, hashlib, os, argparse

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TOOLS_DIR)
from extract_css import find_source, get_css, extract_for

ap = argparse.ArgumentParser()
ap.add_argument('--catalog', default=os.path.join(TOOLS_DIR, '..', 'block-catalog.json'),
                help='source catalog (default: library/catalog/block-catalog.json in this repo)')
ap.add_argument('--out', default=os.path.join(TOOLS_DIR, '..', 'builder-index-v1.json'),
                help='output index (default: library/catalog/builder-index-v1.json in this repo)')
args = ap.parse_args()

def clean_label(name):
    parts = [p.strip() for p in name.split('\u2014')]
    label = ''
    for p in reversed(parts):
        s = re.sub(r'^[\s\u25c8\u25c6\u2726\ufb70\u2713\d\.\u00b7+\-_/\\>]+', '', p).strip()
        s = re.sub(r'\s+', ' ', s).strip()
        if not s or s.startswith('.') or len(s) < 3 or re.search(r'forbidden|production block|shrunken', s, re.I) or re.match(r'^[a-z]+-[a-z]+$', s):
            continue
        label = s
        break
    if not label:
        label = re.sub(r'^[\d\s\.\u00b7]+', '', parts[0]).strip() or name[:40]
    if label == label.upper() and len(label) > 3:
        label = label.title()
    return label[:60]

CATNAME = {'BTN':'button','CRD':'board','TYP':'banner','JWL':'jewel','LST':'list',
           'NAV':'navigation','FRM':'form','CHT':'chat','PAY':'payment','CAL':'calendar',
           'LAY':'layout','ONB':'onboarding','CMT':'comment','MED':'media'}

cat = json.load(open(args.catalog, encoding='utf-8'))
css_cache, css_bank = {}, {}
pieces, stats = {}, {'archived': 0, 'unarchived': 0, 'no_source': 0}

for x in cat:
    model = x['model']
    src_file = x['sources'][0]['source_file'] if x.get('sources') else None
    css, status = '', 'no_source'
    if src_file:
        if src_file.endswith('.md'):
            status = 'unarchived'
        else:
            path = find_source(src_file)
            if path:
                status = 'archived'
                key = src_file + '|' + '|'.join(sorted(x.get('css_classes', [])))
                if key not in css_cache:
                    css_cache[key] = extract_for(x.get('css_classes', []), get_css(path))
                css = css_cache[key]
            else:
                status = 'unarchived'
    stats[status] = stats.get(status, 0) + 1
    # dedupe css via bank
    css_id = None
    if css:
        h = hashlib.sha256(css.encode()).hexdigest()[:12]
        css_bank[h] = css
        css_id = h
    pieces[model] = {
        'model': model,
        'label': clean_label(x['name']),
        'category': x['category'],
        'kind': CATNAME.get(x['category'], x['category'].lower()),
        'tags': x.get('tags', [])[:8],
        'html': x.get('html', ''),
        'css_id': css_id,
        'source_file': src_file,
        'source_status': status,
    }

index = {
    'meta': {
        'name': 'builder-index-v1',
        'built': '2026-10-17',
        'entries': len(pieces),
        'css_bank_entries': len(css_bank),
        'source_status': stats,
        'note': 'Every model number resolves to its real HTML and real extracted CSS. Unarchived = source file not in the library; HTML still ships.',
    },
    'css_bank': css_bank,
    'pieces': pieces,
}
out = args.out
json.dump(index, open(out, 'w', encoding='utf-8'), ensure_ascii=False)
print('entries:', len(pieces), '| css bank:', len(css_bank), '| status:', stats)
print('wrote:', out, round(os.path.getsize(out) / 1048576, 2), 'MB')
print('sha256:', hashlib.sha256(open(out, 'rb').read()).hexdigest())
# check a board + jewel render CSS presence
for m in ['NAYA-CRD-001', 'NAYA-JWL-001', 'NAYA-TYP-001']:
    p = pieces.get(m)
    print(m, '| css:', bool(p and p['css_id']), '| html bytes:', len(p['html']) if p else 0)
