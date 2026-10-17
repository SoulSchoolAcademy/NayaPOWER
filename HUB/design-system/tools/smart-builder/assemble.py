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

ASSEMBLER_VERSION = "assemble-v1.2"  # v1.2: default-on (coverage-gated) + consent-line (ready/connected) + centralized identity

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

def lawcard(title, desc, color, attrs=''):
    return (
        '<div class="nb-chrome" style="margin-bottom:12px">'
        '<div class="lawcard"%s style="--lc:%s">'
        '<div class="ln" style="text-transform:uppercase"><span class="ld"></span><span>%s</span></div>'
        '<p>%s</p></div></div>' % (attrs, color, esc(title), esc(desc))
    )

# ---- Design Law 4: never similar together ----
# Adjacent spectrum positions look almost the same side by side (yellow/gold,
# orange/rich-orange). Sequences use this maximally-spaced order instead, so
# neighbors are always visibly distinct.
SPACED = [0, 5, 10, 3, 8, 1, 6, 11, 4, 9, 2, 7]
def seq_color(spectrum, i, fixed=None):
    """A sequence element's color: its fixed identity when the contract names
    one (Design Law 5), else the spaced spectrum order (Design Law 4)."""
    if fixed:
        return fixed
    return spectrum[SPACED[i % len(SPACED)]]

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


# ---- default-on mechanism (Shawn's product rule, 2026-10-17) ----
# Standard features ship ON by default (opt-out): every template is a full
# functioning app; the intake shows checkmarks all checked and the user
# unchecks to remove. The default-on policy is COVERAGE-GATED: it flips
# ACTIVE only when EVERY standard feature is registry-'built', computed
# deterministically from the registry at assembly time — no human gate.
# Until then the assembler stays opt-in and every existing contract keeps
# working byte-for-byte unchanged. reports rides on intelligence_today
# unless the registry ever splits them out.
STANDARD_FEATURES = [
    'feature.smart_mail',
    'feature.smart_list',
    'feature.space',
    'feature.connect',
    'feature.intelligence_today',
    'feature.social_feed',
    'feature.smart_tabs',
]
STANDARD_SHORT = {fid.replace('feature.', '') for fid in STANDARD_FEATURES}

def default_on_policy_active(reg_statuses):
    """Coverage gate: ACTIVE iff every standard feature id is registry-'built'.
    Pure function of the registry -> deterministic, no human gate.
    (reg_statuses is keyed by short name, e.g. 'smart_mail'.)"""
    return all(reg_statuses.get(fid.replace('feature.', '')) == 'built'
               for fid in STANDARD_FEATURES)

def standard_resolution(feats, reg_statuses, reg_present):
    """Three-state resolution for standard features.

    Returns (enabled_ids, problems):
      - explicit false  -> OFF (suppressed; renders nothing, never an error)
      - explicit true   -> ON  (registry-gated; refuse unless built)
      - omitted         -> ON iff the default-on policy is active, else OFF

    Sharpened fail-closed: ANY enabled standard feature with registry
    status != 'built' refuses the build with a structured error naming
    the feature. (When the policy is active the check is vacuous for
    default-on features — the gate required them built to flip.)
    """
    enabled, problems = [], []
    policy = default_on_policy_active(reg_statuses) if reg_present else False
    for fid in STANDARD_FEATURES:
        short = fid.replace('feature.', '')
        val = feats.get(short) if isinstance(feats, dict) else None
        if isinstance(val, dict):
            declared = bool(val.get('enabled'))
        elif val is True:
            declared = True
        elif not val:
            declared = None  # omitted / falsy -> defer to the policy
        else:
            problems.append({'code': 'bad_breaker_declaration',
                             'feature': fid,
                             'detail': 'must be an object or true'})
            continue
        if declared is None:
            if policy:
                enabled.append(fid)
            # policy inactive -> stays opt-in: OFF, no error
        elif declared:
            enabled.append(fid)
        # declared falsy -> explicit opt-out: OFF
    if not reg_present:
        for fid in enabled:
            problems.append({'code': 'registry_unavailable', 'feature': fid,
                             'detail': 'cannot bind the feature claim without '
                                       'the registry'})
    else:
        for fid in enabled:
            st = reg_statuses.get(fid.replace('feature.', ''))
            if st != 'built':
                problems.append({'code': 'feature_not_built', 'feature': fid,
                                 'detail': 'registry status is %r — the contract '
                                           'never activates an unbuilt capability'
                                           % (st,)})
    return enabled, problems

# ---- consent-line refinement (Naya 3, adopted 2026-10-17) ----
# Every feature's capability contract carries ready (works with zero
# grants) vs connected (each action names its required grant). The resolver
# enforces: feature ON -> ready behaviors active; a connected action fires
# ONLY when its grant is recorded (grant = contract.connections.<name>
# is True — strict boolean, not truthy). Modules receive the grants in
# context and must gate connected actions themselves; the receipt mirrors
# the grants as the audit trail.
def resolve_consent(enabled_fids, reg_by_id, grants):
    """Consent resolution over the enabled feature set (same code path as
    default-on resolution: the enabled set flows here). Returns
    {fid: {'ready': [...], 'connected_active': [...], 'connected_gated': [...]}}.
    connected entries keep their {action, grant} shape."""
    consent = {}
    for fid in enabled_fids:
        entry = reg_by_id.get(fid, {})
        ready = list(entry.get('ready', []))
        active, gated = [], []
        for c in entry.get('connected', []):
            (active if grants.get(c.get('grant')) is True else gated).append(c)
        consent[fid] = {'ready': ready, 'connected_active': active,
                        'connected_gated': gated}
    return consent

def resolve_identity(contract):
    """Identity resolves ONCE, here in the assembler — never per template.
    One person, one connected smart world: identity/relationships/
    intelligence are shared across pages/rooms; templates decide
    PRESENTATION only. Returns (identity_dict_or_None, problems)."""
    raw = contract.get('identity')
    if raw is None:
        return None, []
    if not isinstance(raw, dict):
        return None, [{'code': 'bad_identity',
                       'detail': 'identity must be an object, got %s'
                                 % type(raw).__name__}]
    return raw, []

def activate_breakers(contract, reg_statuses, reg_present, context):
    """Contract flips breakers; the registry gates them (fail closed).

    Returns (cover_html, problems, events, enabled_fids).
    - features as a list (contract-page) -> no breakers; cover not rendered.
    - features as a dict -> standard features resolve via the three-state
      default-on mechanism; non-standard breakers (incl. cover) keep the
      existing registry gate. Any enabled-but-unbuilt feature refuses.
    context: the resolved connections+privacy+identity dict, handed to
    every feature module (connections stay opt-in inside modules).
    """
    problems, events, cover_html, enabled = [], [], '', []
    feats = contract.get('features')
    if not isinstance(feats, dict):
        return cover_html, problems, events, enabled
    # standard features: three-state resolution (explicit / default-on / off)
    std_enabled, std_problems = standard_resolution(feats, reg_statuses,
                                                    reg_present)
    problems += std_problems
    enabled += std_enabled
    decl = None
    try:
        decl = decl_for(contract)
    except CoverRefusal as e:
        # malformed cover is reported, but the other breakers are still
        # checked so the refusal names every problem, not just the first
        problems.append({'code': e.code, 'feature': FEATURE_COVER_ID,
                         'detail': e.detail})
    for key, val in feats.items():
        if str(key) in STANDARD_SHORT:
            continue  # handled by standard_resolution above
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
        else:
            enabled.append('feature.' + str(key))
    if problems or decl is None or not decl.get('enabled'):
        return cover_html, problems, events, enabled
    try:
        cover_html = render_cover(decl, reg_statuses.get('cover'),
                                context=context)
    except CoverRefusal as e:
        problems.append({'code': e.code, 'feature': FEATURE_COVER_ID,
                         'detail': e.detail})
        return '', problems, events, enabled
    events.append({'event': 'cover.updated', 'feature': FEATURE_COVER_ID,
                   'version': FEATURE_COVER_VERSION})
    return cover_html, problems, events, enabled


def render_breaker_rows(enabled_fids, consent, reg_by_id, reg_statuses,
                         spectrum, sec_idx):
    """§7 for customer contracts: one honest row per ENABLED breaker —
    its registry name, its intent, and its registry status. Never claims
    operational unless the registry says built (unbuilt breakers cannot
    reach this code — activate_breakers refuses them first).

    Consent honesty: the row carries data-feature + data-consent. The word
    "connected" appears ONLY when the receipt shows an active grant for
    that feature; otherwise the row says "ready". The verifier asserts this.
    """
    rows = []
    for i, fid in enumerate(enabled_fids):
        short = fid.replace('feature.', '')
        entry = reg_by_id.get(fid, {})
        status = reg_statuses.get(short, 'unknown')
        c = consent.get(fid, {})
        if c.get('connected_active'):
            grants = sorted({a['grant'] for a in c['connected_active']})
            consent_word = 'connected (%s)' % ', '.join(grants)
            data_consent = 'connected'
        else:
            consent_word = 'ready'
            data_consent = 'ready'
        rows.append(lawcard(
            '%s — %s · %s' % (entry.get('name', fid), status, consent_word),
            entry.get('intent', ''),
            spectrum[(sec_idx + i) % len(spectrum)],
            attrs=' data-feature="%s" data-consent="%s"' % (fid, data_consent)))
    return ''.join(rows)

def safe_json_for_pre(obj):
    # A </pre> or <script> sequence inside contract data must never break out
    # of the embedding element. \u-escapes are valid JSON and parse back clean.
    return (json.dumps(obj, indent=2, ensure_ascii=False)
            .replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026'))

def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

# ---- connections + privacy schema (Shawn's rule, 2026-10-17) ----
# connections: each opt-IN (default False); missing block = all false.
# privacy: 'private' | 'network' | 'public', default 'private'; anything
# else is a structured fail-closed refusal.
# The resolved context is passed to every feature module. Invariant the
# wave modules must preserve: default-on enables FEATURES; connections
# stay OPT-IN. A default-on feature with its connection off renders UI +
# honest "connect to enable" — never blocked, never faked. The sharpened
# fail-closed refuses publish only on enabled-but-UNVERIFIED features,
# never on missing connections.
CONNECTION_KEYS = ('muse', 'github', 'network', 'nayanet')
PRIVACY_MODES = ('private', 'network', 'public')

def resolve_contract_context(contract):
    """Resolve connections + privacy from the contract.

    Returns (context, problems):
      context = {'connections': {k: bool}, 'privacy': 'private'|'network'|'public'}
      problems: structured fail-closed errors (bad privacy enum,
                malformed connections block).
    """
    problems = []
    raw = contract.get('connections')
    if raw is None:
        raw = {}
    elif not isinstance(raw, dict):
        problems.append({'code': 'bad_connections',
                         'detail': 'connections must be an object of booleans, got %s'
                                   % type(raw).__name__})
        raw = {}
    connections = {k: bool(raw.get(k, False)) for k in CONNECTION_KEYS}
    privacy = contract.get('privacy', 'private')
    if privacy not in PRIVACY_MODES:
        problems.append({'code': 'bad_privacy',
                         'detail': "privacy must be one of %s, got %r"
                                   % (list(PRIVACY_MODES), privacy)})
    return {'connections': connections, 'privacy': privacy}, problems

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
    # connections + privacy: resolved once, handed to every feature module.
    context, context_problems = resolve_contract_context(contract)
    problems += context_problems
    # identity: resolved ONCE here — templates reference it, never redefine it.
    identity, identity_problems = resolve_identity(contract)
    problems += identity_problems
    context['identity'] = identity
    # feature breakers: the contract flips them, the registry gates them.
    # default-on resolution and the consent grant check share this code path:
    # the enabled set flows into both rendering and consent resolution.
    cover_html, breaker_problems, breaker_events, enabled_fids = activate_breakers(
        contract, reg_statuses, reg_present, context)
    problems += breaker_problems
    if problems:
        print(json.dumps({'status': 'refused', 'errors': problems}, indent=2))
        sys.exit(2)
    print('ok: contract validates —', len(problems), 'problems')
    # consent-line: feature ON -> ready active; connected actions fire only
    # on recorded grants. The receipt mirrors the grants (audit trail).
    consent = resolve_consent(enabled_fids, reg_by_id, context['connections'])

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
        c = seq_color(SPECTRUM, i)
        modes.append(
            '<div class="nb-chrome"><button class="card mode" aria-pressed="%s" data-mode="%s" '
            'style="--accent:%s;--accent-soft:%s73;text-align:left;cursor:pointer;width:100%%;'
            'font:inherit;color:inherit">'
            '<span style="display:block;font-size:11px;letter-spacing:.22em;text-transform:uppercase;'
            'font-weight:700;color:var(--white);margin-bottom:10px">%s</span>'
            '<h3>%s</h3><p class="fine">%s</p></button></div>'
            % ("true" if i == 0 else "false", esc(m['id']), c, c,
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
        % (seq_color(SPECTRUM, i, e[3] if len(e) > 3 else None), esc(e[0]), esc(e[1]), esc(e[2]))
        for i, e in enumerate(contract['templates']))
    templates = '<div class="grid g4">%s</div>' % templates

    # features / gallery / customize -> the real .lawcard piece
    # contract-page contracts carry features as [title, desc] pairs;
    # customer contracts carry flipped breakers — rendered with their
    # honest registry statuses, never claimed operational unless built.
    feats = contract['features']
    if isinstance(feats, dict):
        features = render_breaker_rows(enabled_fids, consent, reg_by_id,
                                       reg_statuses, SPECTRUM, SEC['features'])
    else:
        features = ''.join(
            lawcard(t, d, seq_color(SPECTRUM, i))
            for i, (t, d) in enumerate(feats))
    gallery_html = ''.join(
        lawcard(t, d, seq_color(SPECTRUM, i))
        for i, (t, d) in enumerate(contract['gallery']['points']))
    customize_html = ''.join(
        lawcard(t, d, seq_color(SPECTRUM, i))
        for i, (t, d) in enumerate(contract['customize']['points']))

    # loop -> the real .lawcard piece
    loop = ''.join(
        lawcard(t, d, seq_color(SPECTRUM, i))
        for i, (t, d) in enumerate(contract['loop']))

    page = tpl
    # feature claims bound to registry statuses: the contract never advertises
    # a capability as operational unless the registry says it is built.
    if reg_present:
        contract['machine']['features_status'] = reg_statuses
    # resolved connections + privacy + identity travel with the machine block
    # so every consumer (and every feature module) reads the same resolved
    # context. consent: per-feature ready vs grant-gated connected actions.
    contract['machine']['connections'] = context['connections']
    contract['machine']['privacy'] = context['privacy']
    contract['machine']['identity'] = identity
    contract['machine']['consent'] = {
        fid: {'ready': c['ready'],
              'connected_active': [a['action'] for a in c['connected_active']],
              'connected_gated': [a['action'] for a in c['connected_gated']]}
        for fid, c in consent.items()}
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
                      + open(__file__, 'rb').read())

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
            # consent-line audit trail: the active grants, mirrored on
            # EVERY build receipt, plus the per-feature ready/connected
            # resolution the resolver computed.
            'grants': context['connections'],
            'identity': identity,
            'consent': consent,
        },
    }
    json.dump(manifest, open(a.manifest, 'w'), indent=2)
    print('page:', a.out, manifest['build']['page']['bytes'], 'bytes')
    print('build id:', build_id[:16])
    print('manifest:', a.manifest)

if __name__ == '__main__':
    main()
