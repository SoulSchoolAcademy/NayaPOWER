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

# ---- library quality gate (Shawn's law, 2026-10-17) ----
# A piece is assemblable only if it clears the bar. Substandard pieces are
# QUARANTINED: they stay identifiable in the index with a structured reason,
# and the assembler refuses any contract that references one (fail closed) —
# they never reach a page. "Not entering the index" = excluded from the
# assemblable surface, never silently dropped (the reason must travel).
QUARANTINE = {
    # Manual list — Shawn's eye, honored by the gate (his word 2026-10-17):
    # NAYA-NAV-001/007 are below standard: no human labels, ugly.
    'NAYA-NAV-001': 'below standard — extracted CSS is a variables-only fragment, '
                    'renders as unstyled raw buttons; label is a source code, not a '
                    'human label (Shawn 2026-10-17)',
    'NAYA-NAV-007': 'below standard — CTA pill miscategorized as navigation; no human '
                    "label (Shawn 2026-10-17: 'horrible', shouldn't be in the system)",
}

def css_is_broken_fragment(css):
    """True when the extracted CSS is a broken fragment: empty, no complete
    rule block, or ONLY a bare .nb-scope block of custom properties (styles
    nothing — the piece renders unstyled, cf. NAYA-NAV-001)."""
    if css is None:
        return False  # no CSS is fine — self-styled HTML
    c = re.sub(r'/\*.*?\*/', '', css, flags=re.S).strip()
    if not c:
        return False  # unarchived sources ship CSS-less by library doctrine
    rules = re.findall(r'([^{}]+)\{([^{}]*)\}', c)
    if not rules:
        return True
    for sel, body in rules:
        sels = [s.strip() for s in sel.split(',')]
        real = [d for d in (d.strip() for d in body.split(';'))
                if d and not d.startswith('--')]
        if any(s != '.nb-scope' for s in sels) or real:
            return False
    return True

def quality_gate(model, label, html, css):
    """The automated bar. Returns a quarantine reason, or None when the piece
    clears it: human label (>=3 chars), non-empty HTML, CSS that is not a
    broken fragment. The manual quarantine list is honored first."""
    if model in QUARANTINE:
        return 'quarantine list: ' + QUARANTINE[model]
    if len(label.strip()) < 3:
        return 'label is not a human label (%r is under 3 chars)' % label
    if not html.strip():
        return 'empty HTML — nothing to render'
    if css_is_broken_fragment(css):
        return 'CSS is a broken fragment — the piece renders unstyled'
    return None

cat = json.load(open(args.catalog))
css_cache, css_bank = {}, {}
pieces, stats = {}, {'archived': 0, 'unarchived': 0, 'no_source': 0}
qcount = 0  # quarantined pieces — separate from source_status

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
    label = clean_label(x['name'])
    qreason = quality_gate(model, label, x.get('html', ''), css)
    if qreason:
        qcount += 1
    pieces[model] = {
        'model': model,
        'label': label,
        'category': x['category'],
        'kind': CATNAME.get(x['category'], x['category'].lower()),
        'tags': x.get('tags', [])[:8],
        'html': x.get('html', ''),
        'css_id': css_id,
        'source_file': src_file,
        'source_status': status,
        'quarantined': bool(qreason),
        'quarantine_reason': qreason,
    }

index = {
    'meta': {
        'name': 'builder-index-v1',
        'built': '2026-10-17',
        'entries': len(pieces),
        'css_bank_entries': len(css_bank),
        'source_status': stats,
        'quarantined_count': qcount,
        'quarantine': {m: v['quarantine_reason'] for m, v in pieces.items()
                       if v['quarantined']},
        'note': 'Every model number resolves to its real HTML and real extracted CSS. Unarchived = source file not in the library; HTML still ships. '
                'Quarantined pieces stay listed with a reason and the assembler refuses them (fail closed) — they never reach a page.',
    },
    'css_bank': css_bank,
    'pieces': pieces,
}
out = args.out
json.dump(index, open(out, 'w'), ensure_ascii=False)
print('entries:', len(pieces), '| css bank:', len(css_bank), '| status:', stats)
print('wrote:', out, round(os.path.getsize(out) / 1048576, 2), 'MB')
print('sha256:', hashlib.sha256(open(out, 'rb').read()).hexdigest())
# check a board + jewel render CSS presence
for m in ['NAYA-CRD-001', 'NAYA-JWL-001', 'NAYA-TYP-001']:
    p = pieces.get(m)
    print(m, '| css:', bool(p and p['css_id']), '| html bytes:', len(p['html']) if p else 0)
