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

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                'functions'))
from feature_cover import (CoverRefusal, decl_for, render_cover,
                           FEATURE_COVER_ID, FEATURE_COVER_VERSION)

ASSEMBLER_VERSION = "assemble-v1.1"  # v1.1: feature breakers wired (cover first)

def esc(s):
    return htmlmod.escape(str(s), quote=True)

def sha16(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()[:16]

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

# ---- trust boundary + structured validation (fail closed) ----
# The assembler resolves ONLY models present in the governed builder index.
# Unknown models, missing sections, or incompatible entries are structured
# failures — never silent substitutions, never improvised pieces.
REQUIRED_TOP_KEYS = ['title', 'kicker', 'lede', 'intake', 'fields', 'wall',
                     'gallery', 'customize', 'templates', 'features', 'loop',
                     'promise', 'machine', 'design']

def validate_contract(contract, pieces):
    errors = []
    for k in REQUIRED_TOP_KEYS:
        if k not in contract:
            errors.append({'code': 'missing_key', 'key': k})
    for cat, models in contract.get('wall', {}).items():
        for m in models:
            if m not in pieces:
                errors.append({'code': 'unknown_model', 'model': m, 'category': cat})
            elif not pieces[m].get('html'):
                errors.append({'code': 'empty_piece', 'model': m})
    design = contract.get('design', {})
    n = len(design.get('spectrum', []))
    for sec, idx in design.get('sections', {}).items():
        if not isinstance(idx, int) or not (0 <= idx < n):
            errors.append({'code': 'bad_section_color', 'section': sec, 'index': idx})
    # features: contract-page contracts carry a list of [title, desc] pairs;
    # customer contracts carry a breaker dict (contract.features.<breaker>).
    # Anything else is a malformed contract — fail closed.
    feats = contract.get('features')
    if feats is not None and not isinstance(feats, (list, dict)):
        errors.append({'code': 'bad_features_shape',
                       'detail': 'features must be a list or an object, got %s'
                                 % type(feats).__name__})
    return errors


def activate_breakers(contract, reg_statuses, reg_present):
    """Contract flips breakers; the registry gates them (fail closed).

    Returns (cover_html, problems, events).
    - features as a list (contract-page) -> no breakers; cover not rendered.
    - features as a dict -> each declared breaker must be registry-'built',
      else a structured refusal. Only then does cover render.
    """
    problems, events, cover_html = [], [], ''
    feats = contract.get('features')
    if not isinstance(feats, dict):
        return cover_html, problems, events
    decl = None
    try:
        decl = decl_for(contract)
    except CoverRefusal as e:
        # malformed cover is reported, but the other breakers are still
        # checked so the refusal names every problem, not just the first
        problems.append({'code': e.code, 'feature': FEATURE_COVER_ID,
                         'detail': e.detail})
    for key, val in feats.items():
        if isinstance(val, dict):
            declared = bool(val.get('enabled'))
        elif val is True:
            declared = True
        elif not val:
            continue  # falsy -> breaker not flipped
        else:
            problems.append({'code': 'bad_breaker_declaration',
                             'feature': 'feature.' + str(key),
                             'detail': 'must be an object or true'})
            continue
        if not declared:
            continue
        if not reg_present:
            problems.append({'code': 'registry_unavailable',
                             'feature': 'feature.' + str(key),
                             'detail': 'cannot bind the feature claim without the registry'})
        elif reg_statuses.get(key) != 'built':
            problems.append({'code': 'feature_not_built',
                             'feature': 'feature.' + str(key),
                             'detail': 'registry status is %r — the contract never '
                                       'activates an unbuilt capability'
                                       % (reg_statuses.get(key),)})
    if problems or decl is None or not decl.get('enabled'):
        return cover_html, problems, events
    try:
        cover_html = render_cover(decl, reg_statuses.get('cover'))
    except CoverRefusal as e:
        problems.append({'code': e.code, 'feature': FEATURE_COVER_ID,
                         'detail': e.detail})
        return '', problems, events
    events.append({'event': 'cover.updated', 'feature': FEATURE_COVER_ID,
                   'version': FEATURE_COVER_VERSION})
    return cover_html, problems, events


def render_breaker_rows(feats, reg_by_id, reg_statuses, spectrum, sec_idx):
    """§7 for customer contracts: one honest row per flipped breaker —
    its registry name, its intent, and its registry status. Never claims
    operational unless the registry says built (unbuilt breakers cannot
    reach this code — activate_breakers refuses them first)."""
    rows = []
    for i, (key, val) in enumerate(feats.items()):
        declared = val is True or (isinstance(val, dict) and val.get('enabled'))
        if not declared:
            continue
        entry = reg_by_id.get('feature.' + str(key), {})
        status = reg_statuses.get(key, 'unknown')
        rows.append(lawcard(
            '%s — %s' % (entry.get('name', key), status),
            entry.get('intent', ''),
            spectrum[(sec_idx + i) % len(spectrum)]))
    return ''.join(rows)

def safe_json_for_pre(obj):
    # A </pre> or <script> sequence inside contract data must never break out
    # of the embedding element. \u-escapes are valid JSON and parse back clean.
    return (json.dumps(obj, indent=2, ensure_ascii=False)
            .replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026'))

def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

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

    # raw bytes for deterministic identity
    contract_bytes = open(a.contract, 'rb').read()
    index_bytes = open(a.index, 'rb').read()
    template_bytes = open(a.template, 'rb').read()

    # ---- registry first: every feature claim binds to it, before anything renders ----
    reg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'functions', 'registry.json')
    reg_present = os.path.exists(reg_path)
    reg = json.load(open(reg_path)) if reg_present else None
    reg_statuses = ({f['id'].replace('feature.', ''): f['status']
                     for f in reg['groups']['feature']['functions']}
                    if reg_present else {})
    reg_by_id = ({f['id']: f for f in reg['groups']['feature']['functions']}
                 if reg_present else {})

    # ---- validate before assembling: fail closed, structured errors ----
    problems = validate_contract(contract, pieces)
    # feature breakers: the contract flips them, the registry gates them.
    cover_html, breaker_problems, breaker_events = activate_breakers(
        contract, reg_statuses, reg_present)
    problems += breaker_problems
    if problems:
        print(json.dumps({'status': 'refused', 'errors': problems}, indent=2))
        sys.exit(2)
    print('ok: contract validates —', len(problems), 'problems')

    # ---- design decisions come from the contract, not the assembler ----
    SPECTRUM = contract['design']['spectrum']
    SEC = contract['design']['sections']
    def spec(sec):
        return SPECTRUM[SEC[sec] % len(SPECTRUM)]

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
        c = SPECTRUM[(SEC['intake'] + i) % len(SPECTRUM)]
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
        % (SPECTRUM[(SEC['templates'] + i) % len(SPECTRUM)], esc(n), esc(t), esc(d))
        for i, (n, t, d) in enumerate(contract['templates']))
    templates = '<div class="grid g4">%s</div>' % templates

    # features / gallery / customize -> the real .lawcard piece
    # contract-page contracts carry features as [title, desc] pairs;
    # customer contracts carry flipped breakers — rendered with their
    # honest registry statuses, never claimed operational unless built.
    feats = contract['features']
    if isinstance(feats, dict):
        features = render_breaker_rows(feats, reg_by_id, reg_statuses,
                                       SPECTRUM, SEC['features'])
    else:
        features = ''.join(
            lawcard(t, d, SPECTRUM[(SEC['features'] + i) % len(SPECTRUM)])
            for i, (t, d) in enumerate(feats))
    gallery_html = ''.join(
        lawcard(t, d, SPECTRUM[(SEC['gallery'] + i) % len(SPECTRUM)])
        for i, (t, d) in enumerate(contract['gallery']['points']))
    customize_html = ''.join(
        lawcard(t, d, SPECTRUM[(SEC['customize'] + i) % len(SPECTRUM)])
        for i, (t, d) in enumerate(contract['customize']['points']))

    # loop -> the real .lawcard piece
    loop = ''.join(
        lawcard(t, d, SPECTRUM[(SEC['loop'] + i) % len(SPECTRUM)])
        for i, (t, d) in enumerate(contract['loop']))

    page = tpl
    # feature claims bound to registry statuses: the contract never advertises
    # a capability as operational unless the registry says it is built.
    if reg_present:
        contract['machine']['features_status'] = reg_statuses
    machine_raw = safe_json_for_pre(contract['machine'])
    for key, val in {
        '%%TITLE%%': esc(contract['title']),
        '%%KICKER%%': esc(contract['kicker']),
        '%%LEDE%%': esc(contract['lede']),
        '%%COVER%%': cover_html,  # '' unless the contract flipped the cover breaker
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
    page_bytes = page.encode()

    # Deterministic build identity: same contract + index + template +
    # assembler -> same bytes, every time. The receipt (time, verification)
    # legitimately changes between runs; the identity never does.
    build_id = sha256(contract_bytes + index_bytes + template_bytes
                      + ASSEMBLER_VERSION.encode())

    manifest = {
        # 1. DESIGN CONTRACT — what the customer wanted
        'contract': {'path': a.contract, 'sha256': sha256(contract_bytes)},
        # 2. RESOLUTION PLAN — exact component versions resolved
        'resolution': {
            'index': {'path': a.index, 'sha256': sha256(index_bytes),
                      'entries': len(pieces)},
            'wall_pieces': [m for models in contract['wall'].values() for m in models],
        },
        # 3. BUILD ARTIFACT — deterministic
        'build': {
            'id': build_id,
            'assembler': ASSEMBLER_VERSION,
            'template_sha256': sha256(template_bytes),
            'page': {'path': a.out, 'bytes': len(page_bytes),
                     'sha256': sha256(page_bytes)},
        },
        # 4. VERIFICATION RECORD — appended by verify-build.py
        'verification': 'pending — run verify-build.py',
        # 5. DEPLOYMENT RECEIPT — appended at deploy time
        'deployment': 'pending — human approves preview first',
        # execution-time receipt metadata (not part of the identity)
        'receipt': {
            'built_utc': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
            # capability-contract events the build actually fired
            'events': breaker_events,
        },
    }
    json.dump(manifest, open(a.manifest, 'w'), indent=2)
    print('page:', a.out, manifest['build']['page']['bytes'], 'bytes')
    print('build id:', build_id[:16])
    print('manifest:', a.manifest)

if __name__ == '__main__':
    main()
