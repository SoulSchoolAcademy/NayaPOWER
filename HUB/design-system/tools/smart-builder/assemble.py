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
import argparse, copy, json, hashlib, html as htmlmod, os, sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                'functions'))
from feature_cover import (CoverRefusal, decl_for, render_cover,
                           FEATURE_COVER_ID, FEATURE_COVER_VERSION)
from feature_smart_notes import (SmartNotesRefusal, decl_for as sn_decl_for,
                                 render_smart_notes,
                                 FEATURE_SMART_NOTES_ID, FEATURE_SMART_NOTES_VERSION)
from feature_notifications import (NotificationsRefusal,
                                    decl_for as nt_decl_for,
                                    render_notifications,
                                    FEATURE_NOTIFICATIONS_ID,
                                    FEATURE_NOTIFICATIONS_VERSION)

from feature_automation import (AutomationRefusal, decl_for as am_decl_for,
                                 render_automation, FEATURE_AUTOMATION_ID,
                                 FEATURE_AUTOMATION_VERSION)
from feature_smart_mail import (SmartMailRefusal, decl_for as sm_decl_for,
                                 render_smart_mail, FEATURE_ID as FEATURE_SMART_MAIL_ID,
                                 FEATURE_VERSION as FEATURE_SMART_MAIL_VERSION)
from feature_space import (SpaceRefusal, decl_for as sp_decl_for,
                            render_space, FEATURE_ID as FEATURE_SPACE_ID,
                            FEATURE_VERSION as FEATURE_SPACE_VERSION)
from feature_social_feed import (SocialFeedRefusal, decl_for as sf_decl_for,
                                 render_social_feed,
                                 FEATURE_ID as FEATURE_SOCIAL_FEED_ID,
                                 FEATURE_VERSION as FEATURE_SOCIAL_FEED_VERSION)
from feature_smart_list import (SmartListRefusal, decl_for as sl_decl_for,
                                 render_smart_list, mode_for as sl_mode_for,
                                 granted as sl_granted,
                                 FEATURE_ID as FEATURE_SMART_LIST_ID,
                                 FEATURE_SMART_LIST_VERSION)
from feature_smart_bars import (SmartBarsRefusal, decl_for as sb_decl_for,
                                 render_smart_bars,
                                 FEATURE_ID as FEATURE_SMART_BARS_ID,
                                 FEATURE_SMART_BARS_VERSION)
from feature_connect import (ConnectRefusal, decl_for as cn_decl_for,
                              render_connect,
                              FEATURE_ID as FEATURE_CONNECT_ID,
                              FEATURE_CONNECT_VERSION)
from feature_community import (CommunityRefusal, decl_for as cm_decl_for,
                                render_community,
                                FEATURE_ID as FEATURE_COMMUNITY_ID,
                                FEATURE_COMMUNITY_VERSION)
from feature_smart_tabs import (TabsRefusal, decl_for as st_decl_for,
                                 render_smart_tabs,
                                 FEATURE_ID as FEATURE_SMART_TABS_ID,
                                 FEATURE_SMART_TABS_VERSION)
from feature_intelligence_today import (IntelligenceRefusal,
                                         decl_for as it_decl_for,
                                         render_intelligence_today,
                                         FEATURE_ID as FEATURE_INTELLIGENCE_TODAY_ID,
                                         FEATURE_INTELLIGENCE_TODAY_VERSION)
from feature_contacts import (ContactsRefusal, decl_for as ct_decl_for,
                               render_contacts,
                               FEATURE_ID as FEATURE_CONTACTS_ID,
                               FEATURE_CONTACTS_VERSION)
from feature_naya_answers import (NayaAnswersRefusal, decl_for as na_decl_for,
                                   render_naya_answers,
                                   FEATURE_ID as FEATURE_NAYA_ANSWERS_ID,
                                   FEATURE_NAYA_ANSWERS_VERSION)
from feature_scheduler import (SchedulerRefusal, decl_for as sc_decl_for,
                                render_scheduler,
                                FEATURE_ID as FEATURE_SCHEDULER_ID,
                                FEATURE_SCHEDULER_VERSION)
from feature_broadcast import (BroadcastRefusal, decl_for as bc_decl_for,
                                render_broadcast,
                                FEATURE_ID as FEATURE_BROADCAST_ID,
                                FEATURE_BROADCAST_VERSION)

ASSEMBLER_VERSION = "assemble-v1.14"  # v1.14: + quarantine refusal (piece_quarantined) + intake-page seam (contract["intake_page"]) — additive, existing contracts byte-identical

# ---- breaker module wiring ----
# Every wired module follows the cover pattern: decl_for(contract) parses
# the declaration (three-state: explicit true/false honored, omitted ->
# assembler policy, never a module-level default); render_* renders on the
# resolved state; Refusal carries structured fail-closed errors.
# The adapter signature: adapter(decl, registry_status, context, contract)
#   -> (html, events, extra_receipt_dict).
# Modules render on their OWN flags — never behind cover's early-return
# (Wave A fix: F1 gated everything behind cover because cover was the only
# breaker; with N breakers each stands on its own declaration).
def _render_smart_notes(decl, st, ctx, contract):
    html, events = render_smart_notes(decl, st, contract.get('address') or '',
                                      context=ctx)
    return html, events, {}

def _render_notifications(decl, st, ctx, contract):
    html, events = render_notifications(decl, st, context=ctx)
    return html, events, {}

def _render_automation(decl, st, ctx, contract):
    html, events, audit = render_automation(decl, st, context=ctx)
    return html, events, {'automation_audit': audit}

def _wavea_connected_events(mod_fid, mod_version, connected):
    # Wave A modules return (html, connected) where connected is a list of
    # {"event": ..., "grant": ...} for the CONNECTED capabilities actually
    # wired — the grant mirror for the receipt (audit trail).
    return [{'event': c.get('event', 'connected.wired'), 'feature': mod_fid,
             'grant': c.get('grant'), 'version': mod_version}
            for c in (connected or [])]

def _render_smart_mail(decl, st, ctx, contract):
    html, connected = render_smart_mail(decl, st, context=ctx)
    evts = [{'event': 'smart_mail.wired', 'feature': FEATURE_SMART_MAIL_ID,
             'version': FEATURE_SMART_MAIL_VERSION}]
    evts.extend(_wavea_connected_events(
        FEATURE_SMART_MAIL_ID, FEATURE_SMART_MAIL_VERSION, connected))
    return html, evts, {}

def _render_space(decl, st, ctx, contract):
    html, connected = render_space(decl, st, context=ctx)
    evts = [{'event': 'space.wired', 'feature': FEATURE_SPACE_ID,
             'version': FEATURE_SPACE_VERSION}]
    evts.extend(_wavea_connected_events(
        FEATURE_SPACE_ID, FEATURE_SPACE_VERSION, connected))
    return html, evts, {}

def _render_social_feed(decl, st, ctx, contract):
    html, connected = render_social_feed(decl, st, context=ctx)
    evts = [{'event': 'social_feed.wired', 'feature': FEATURE_SOCIAL_FEED_ID,
             'version': FEATURE_SOCIAL_FEED_VERSION}]
    evts.extend(_wavea_connected_events(
        FEATURE_SOCIAL_FEED_ID, FEATURE_SOCIAL_FEED_VERSION, connected))
    return html, evts, {}

def _render_smart_list(decl, st, ctx, contract):
    # D/E smart_list returns a plain HTML string ('' when not enabled).
    # The readiness entry mirrors the consent line in the receipt:
    # mode is "connected" only when the decl demands sync/share AND holds
    # the nayanet grant; otherwise "ready". (Audit trail, never a claim.)
    html = render_smart_list(decl, st, context=ctx)
    mode = sl_mode_for(decl, ctx)
    is_granted = sl_granted(ctx)
    readiness = [{'feature': FEATURE_SMART_LIST_ID, 'mode': mode,
                  'grant': 'connections.nayanet', 'granted': is_granted}]
    evts = [{'event': 'smart_list.wired', 'feature': FEATURE_SMART_LIST_ID,
             'version': FEATURE_SMART_LIST_VERSION}] if html else []
    return html, evts, {'readiness': readiness}

def _wavec_adapter(decl, st, ctx, render_fn, fid, version, wired_event):
    # Wave C modules return (html, meta); meta = {"mode": ..., "consent":
    # "ready"|"connected"}. The meta rides the readiness receipt key
    # (audit trail). wired_event may be None (modules documenting
    # "Build-time events: none" emit no event).
    html, meta = render_fn(decl, st, context=ctx)
    readiness = [{'feature': fid, 'mode': meta.get('mode'),
                  'consent': meta.get('consent')}]
    evts = [{'event': wired_event, 'feature': fid,
             'version': version}] if (html and wired_event) else []
    return html, evts, {'readiness': readiness}

def _render_smart_bars(decl, st, ctx, contract):
    # The module documents its build-time event as bars.rendered.
    return _wavec_adapter(decl, st, ctx, render_smart_bars,
                          FEATURE_SMART_BARS_ID, FEATURE_SMART_BARS_VERSION,
                          'bars.rendered')

def _render_connect(decl, st, ctx, contract):
    # The module documents "Build-time events: none" — the registry's
    # connect events are visitor-lifecycle, not build-time. No wired event.
    return _wavec_adapter(decl, st, ctx, render_connect,
                          FEATURE_CONNECT_ID, FEATURE_CONNECT_VERSION,
                          None)

def _render_community(decl, st, ctx, contract):
    # The module documents "Build-time events: none". No wired event.
    return _wavec_adapter(decl, st, ctx, render_community,
                          FEATURE_COMMUNITY_ID, FEATURE_COMMUNITY_VERSION,
                          None)

def _waveb_adapter(decl, st, ctx, render_fn, fid, version, wired_event):
    # Wave B modules return a plain HTML string ('' when not enabled).
    # Their grant_required refusals are the fail-closed defense-in-depth
    # for the connections-grant layer (the assembler adds the missing[]
    # field for structural parity with the resolver's permission_denied).
    # The wired event carries the grants (audit: ready with zero grants).
    html = render_fn(decl, st, context=ctx)
    grants = (ctx or {}).get('connections', {}) if isinstance(ctx, dict) else {}
    evts = [{'event': wired_event, 'feature': fid, 'version': version,
             'grants': grants}] if (html and wired_event) else []
    return html, evts, {}

def _render_smart_tabs(decl, st, ctx, contract):
    return _waveb_adapter(decl, st, ctx, render_smart_tabs,
                          FEATURE_SMART_TABS_ID, FEATURE_SMART_TABS_VERSION,
                          'smart_tabs.updated')

def _render_intelligence_today(decl, st, ctx, contract):
    return _waveb_adapter(decl, st, ctx, render_intelligence_today,
                          FEATURE_INTELLIGENCE_TODAY_ID,
                          FEATURE_INTELLIGENCE_TODAY_VERSION,
                          'intelligence_today.updated')

def _render_contacts(decl, st, ctx, contract):
    return _waveb_adapter(decl, st, ctx, render_contacts,
                          FEATURE_CONTACTS_ID, FEATURE_CONTACTS_VERSION,
                          'contacts.updated')

def _waved_adapter(decl, st, ctx, render_fn, fid, version, mode_fn,
                   granted_fn, grant, wired_event=None):
    # Wave D modules return a plain HTML string. The readiness entry
    # mirrors the consent line in the receipt (mode/grant/granted audit
    # trail, like smart_list). wired_event is optional (scheduler emits
    # scheduler.job.created; others emit none).
    html = render_fn(decl, st, context=ctx)
    mode = mode_fn(decl, ctx)
    is_granted = granted_fn(ctx)
    readiness = [{'feature': fid, 'mode': mode, 'grant': grant,
                  'granted': is_granted}]
    evts = [{'event': wired_event, 'feature': fid,
             'version': version}] if (html and wired_event) else []
    return html, evts, {'readiness': readiness}

def _render_naya_answers(decl, st, ctx, contract):
    from feature_naya_answers import mode_for, granted, GRANT
    return _waved_adapter(decl, st, ctx, render_naya_answers,
                          FEATURE_NAYA_ANSWERS_ID, FEATURE_NAYA_ANSWERS_VERSION,
                          mode_for, granted, GRANT)

def _render_scheduler(decl, st, ctx, contract):
    from feature_scheduler import mode_for, granted, GRANT, JOB_CREATED_EVENT
    return _waved_adapter(decl, st, ctx, render_scheduler,
                          FEATURE_SCHEDULER_ID, FEATURE_SCHEDULER_VERSION,
                          mode_for, granted, GRANT, JOB_CREATED_EVENT)

def _render_broadcast(decl, st, ctx, contract):
    from feature_broadcast import mode_for, granted, GRANT
    return _waved_adapter(decl, st, ctx, render_broadcast,
                          FEATURE_BROADCAST_ID, FEATURE_BROADCAST_VERSION,
                          mode_for, granted, GRANT)

# Reserved receipt keys — modules may not shadow them via extra_receipt.
_RECEIPT_RESERVED_KEYS = frozenset(
    {'built_utc', 'events', 'grants', 'privacy', 'identity', 'consent'})

BREAKER_MODULES = [
    # key, feature id, decl_for, refusal class, version, render adapter
    {'key': 'smart_notes', 'fid': FEATURE_SMART_NOTES_ID,
     'decl_for': sn_decl_for, 'refusal': SmartNotesRefusal,
     'version': FEATURE_SMART_NOTES_VERSION,
     'render': _render_smart_notes},
    {'key': 'notifications', 'fid': FEATURE_NOTIFICATIONS_ID,
     'decl_for': nt_decl_for, 'refusal': NotificationsRefusal,
     'version': FEATURE_NOTIFICATIONS_VERSION,
     'render': _render_notifications},
    {'key': 'automation', 'fid': FEATURE_AUTOMATION_ID,
     'decl_for': am_decl_for, 'refusal': AutomationRefusal,
     'version': FEATURE_AUTOMATION_VERSION,
     'render': _render_automation},
    {'key': 'smart_mail', 'fid': FEATURE_SMART_MAIL_ID,
     'decl_for': sm_decl_for, 'refusal': SmartMailRefusal,
     'version': FEATURE_SMART_MAIL_VERSION,
     'render': _render_smart_mail},
    {'key': 'space', 'fid': FEATURE_SPACE_ID,
     'decl_for': sp_decl_for, 'refusal': SpaceRefusal,
     'version': FEATURE_SPACE_VERSION,
     'render': _render_space},
    {'key': 'social_feed', 'fid': FEATURE_SOCIAL_FEED_ID,
     'decl_for': sf_decl_for, 'refusal': SocialFeedRefusal,
     'version': FEATURE_SOCIAL_FEED_VERSION,
     'render': _render_social_feed},
    {'key': 'smart_list', 'fid': FEATURE_SMART_LIST_ID,
     'decl_for': sl_decl_for, 'refusal': SmartListRefusal,
     'version': FEATURE_SMART_LIST_VERSION,
     'render': _render_smart_list},
    {'key': 'smart_bars', 'fid': FEATURE_SMART_BARS_ID,
     'decl_for': sb_decl_for, 'refusal': SmartBarsRefusal,
     'version': FEATURE_SMART_BARS_VERSION,
     'render': _render_smart_bars},
    {'key': 'connect', 'fid': FEATURE_CONNECT_ID,
     'decl_for': cn_decl_for, 'refusal': ConnectRefusal,
     'version': FEATURE_CONNECT_VERSION,
     'render': _render_connect},
    {'key': 'community', 'fid': FEATURE_COMMUNITY_ID,
     'decl_for': cm_decl_for, 'refusal': CommunityRefusal,
     'version': FEATURE_COMMUNITY_VERSION,
     'render': _render_community},
    {'key': 'smart_tabs', 'fid': FEATURE_SMART_TABS_ID,
     'decl_for': st_decl_for, 'refusal': TabsRefusal,
     'version': FEATURE_SMART_TABS_VERSION,
     'render': _render_smart_tabs},
    {'key': 'intelligence_today', 'fid': FEATURE_INTELLIGENCE_TODAY_ID,
     'decl_for': it_decl_for, 'refusal': IntelligenceRefusal,
     'version': FEATURE_INTELLIGENCE_TODAY_VERSION,
     'render': _render_intelligence_today},
    {'key': 'contacts', 'fid': FEATURE_CONTACTS_ID,
     'decl_for': ct_decl_for, 'refusal': ContactsRefusal,
     'version': FEATURE_CONTACTS_VERSION,
     'render': _render_contacts},
    {'key': 'naya_answers', 'fid': FEATURE_NAYA_ANSWERS_ID,
     'decl_for': na_decl_for, 'refusal': NayaAnswersRefusal,
     'version': FEATURE_NAYA_ANSWERS_VERSION,
     'render': _render_naya_answers},
    {'key': 'scheduler', 'fid': FEATURE_SCHEDULER_ID,
     'decl_for': sc_decl_for, 'refusal': SchedulerRefusal,
     'version': FEATURE_SCHEDULER_VERSION,
     'render': _render_scheduler},
    {'key': 'broadcast', 'fid': FEATURE_BROADCAST_ID,
     'decl_for': bc_decl_for, 'refusal': BroadcastRefusal,
     'version': FEATURE_BROADCAST_VERSION,
     'render': _render_broadcast},
]
BREAKER_MODULE_KEYS = {m['key'] for m in BREAKER_MODULES}

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
            elif pieces[m].get('quarantined'):
                # library quality gate: quarantined pieces never reach a page.
                # Structured reason travels so the builder knows what to swap.
                errors.append({'code': 'piece_quarantined', 'model': m, 'category': cat,
                               'reason': pieces[m].get('quarantine_reason')})
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

_BREAKER_OMITTED = object()  # sentinel: the flag was not declared at all

def _default_breaker_enabled(key, reg_statuses):
    """Assembler policy for OMITTED breaker flags (Shawn's product rule
    21:32Z — default-on, opt-out). THE single landing point for the
    coverage-gated flip: an omitted flag renders iff the key is a standard
    feature AND every standard feature is registry-'built'. No module may
    hardcode a default — modules render only the resolved state the
    assembler hands them. (Wave C's hardcoded BREAKER_DEFAULTS was stripped
    per the single-policy resolution: one policy, no drift.)"""
    return ('feature.' + key in STANDARD_FEATURES
            and default_on_policy_active(reg_statuses))

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
    for fid in STANDARD_FEATURES:
        short = fid.replace('feature.', '')
        if not isinstance(feats, dict) or short not in feats:
            declared = None  # omitted (or features not a dict) -> defer to policy
            val = None
        else:
            val = feats.get(short)
            if isinstance(val, dict):
                declared = bool(val.get('enabled'))
            elif val is True:
                declared = True
            elif not val:
                declared = False  # explicit false (or other falsy) -> OFF
            else:
                problems.append({'code': 'bad_breaker_declaration',
                                 'feature': fid,
                                 'detail': 'must be an object or true'})
                continue
        if declared is None:
            # omitted -> the single policy landing point (coverage-gated)
            if reg_present and _default_breaker_enabled(short, reg_statuses):
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
def _connection_key(connection_name):
    """Map a capability contract's connection name to a contract.connections
    key (muse|github|network|nayanet). Unmappable -> '' (always gated:
    fail closed — a grant that names no real connection can never fire)."""
    n = (connection_name or '').lower()
    for key in CONNECTION_KEYS:
        if key in n:
            return key
    return ''

def _connected_as_list(entry):
    """Normalize the connected schema to [{action, grant, ...}]. Accepts the
    list shape [{action, grant}] and the object shape {capability,
    connection, grant, without_grant} — both preserved, nothing dropped."""
    c = entry.get('connected', [])
    if isinstance(c, dict):
        item = {'action': c.get('capability') or '',
                'grant': _connection_key(c.get('connection', ''))}
        if c.get('without_grant'):
            item['without_grant'] = c['without_grant']
        if c.get('grant'):
            item['grant_namespaced'] = c['grant']
        return [item]
    return c

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
        for c in _connected_as_list(entry):
            (active if grants.get(c.get('grant')) is True else gated).append(c)
        consent[fid] = {'ready': ready, 'connected_active': active,
                        'connected_gated': gated}
    return consent

# ---- composable templates: many templates, one app ----
# Implements the contract's declared composition law
# (composition: multi_template, hub plus rooms, all in sync).
# A customer contract may compose MULTIPLE templates instead of picking one:
#   "templates": ["template-personal", "template-business"]
# Backward compat: a single string still works: "templates": "template-personal".
# The contract-page contracts keep "templates" as the display list of
# [badge, name, desc] triples — resolve_templates() passes those through
# untouched, so the existing gallery rendering never changes.
# Merge law (deterministic; full spec in contracts/COMPOSABLE-TEMPLATES.md):
#  1. sections: ordered UNION in listed template order (deduped);
#  2. on section-name collision the FIRST template's content wins, unless
#     "overrides" names another composed template for that section;
#  3. features: explicit false in ANY template disables (prune wins);
#     explicit true flips the breaker on only if no template prunes it
#     (still registry-gated); a template that never mentions a feature has
#     no opinion on it;
#  4. the contract's own "features" dict wins over composed features.
# Unknown template ids, unknown override targets, or malformed shapes are
# structured refusals (fail closed): nothing is improvised, ever.

def _template_ids(contract):
    """Normalize contract['templates'] to a list of template ids.

    Returns (ids, problems). ids is None when the contract does not request
    a composition: the key is missing, or it holds the display-triples list
    used by the contract-page contracts (those keep the existing render path).
    """
    t = contract.get('templates')
    if t is None:
        return None, []
    if isinstance(t, str):
        return [t], []
    if isinstance(t, list):
        if not t:
            return [], [{'code': 'empty_templates',
                         'detail': 'templates is an empty list — name at least '
                                   'one template'}]
        if all(isinstance(x, str) for x in t):
            return list(t), []
        if all(isinstance(x, list) for x in t):
            return None, []  # display triples: not a composition request
        return [], [{'code': 'bad_templates_shape',
                     'detail': 'templates must be a string, a list of template-id '
                               'strings, or the display list of [badge, name, desc] '
                               'triples — mixed shapes are refused'}]
    return [], [{'code': 'bad_templates_shape',
                 'detail': 'templates must be a string or a list, got %s'
                           % type(t).__name__}]


def _feature_opinion(val):
    """One template's opinion on one feature: True (flip on), False (prune),
    None (no opinion), or the 'bad' sentinel for a malformed declaration."""
    if isinstance(val, dict):
        return bool(val.get('enabled'))
    if val is True:
        return True
    if val is False:
        return False
    if not val:
        return None  # falsy -> no opinion, same as activate_breakers
    return 'bad'


def resolve_templates(contract):
    """Resolve a multi-template composition.

    Returns (composition, problems). composition is None when the contract
    does not request one. A non-empty problems list means the assembler must
    refuse (fail closed). Pure function of the contract.
    """
    ids, problems = _template_ids(contract)
    if problems or ids is None:
        return None, problems
    if not ids or any(not isinstance(tid, str) or not tid for tid in ids):
        return None, [{'code': 'bad_template_id',
                       'detail': 'every template id must be a non-empty string'}]
    shapes = contract.get('template_shapes')
    if not isinstance(shapes, dict):
        return None, [{'code': 'missing_template_shapes',
                       'detail': 'templates names %d template(s) but the contract '
                                 'declares no template_shapes object' % len(ids)}]
    resolved = []
    for tid in ids:
        shape = shapes.get(tid)
        if not isinstance(shape, dict):
            problems.append({'code': 'unknown_template', 'template': tid,
                             'detail': 'not declared in template_shapes — '
                                       'the assembler never invents a template'})
            continue
        secs = shape.get('sections', {})
        feats = shape.get('features', {})
        if not isinstance(secs, dict):
            problems.append({'code': 'bad_template_shape', 'template': tid,
                             'detail': 'sections must be an object of '
                                       'section-name -> content'})
            continue
        if not isinstance(feats, dict):
            problems.append({'code': 'bad_template_shape', 'template': tid,
                             'detail': 'features must be an object of '
                                       'feature-id -> declaration'})
            continue
        bad_secs = [n for n, c in secs.items() if not isinstance(c, dict)]
        if bad_secs:
            problems.append({'code': 'bad_section_shape', 'template': tid,
                             'sections': bad_secs,
                             'detail': 'section content must be an object'})
            continue
        resolved.append((tid, secs, feats))
    if problems:
        return None, problems
    by_id = {tid: secs for tid, secs, _ in resolved}
    overrides = contract.get('overrides', {})
    if not isinstance(overrides, dict):
        return None, [{'code': 'bad_overrides_shape',
                       'detail': 'overrides must be an object of '
                                 'section-name -> template-id, got %s'
                                 % type(overrides).__name__}]
    defined = {}
    for tid, secs, _ in resolved:
        for name in secs:
            defined.setdefault(name, tid)
    ov = {}
    for sec, tid in overrides.items():
        if sec not in defined:
            problems.append({'code': 'unknown_override_section', 'section': sec,
                             'detail': 'no composed template defines this section'})
            continue
        if tid not in by_id:
            problems.append({'code': 'unknown_override_template', 'section': sec,
                             'template': tid,
                             'detail': 'override target is not one of the '
                                       "contract's composed templates"})
            continue
        if sec not in by_id[tid]:
            problems.append({'code': 'override_section_missing', 'section': sec,
                             'template': tid,
                             'detail': 'the override target does not define '
                                       'this section'})
            continue
        ov[sec] = tid
    if problems:
        return None, problems
    sections = []
    for name, first_tid in defined.items():
        winner = ov.get(name, first_tid)
        sections.append({'name': name, 'source': winner,
                         'content': copy.deepcopy(by_id[winner][name])})
    opinions = {}
    for tid, _, feats in resolved:
        for key, val in feats.items():
            op = _feature_opinion(val)
            if op == 'bad':
                problems.append({'code': 'bad_feature_declaration',
                                 'template': tid, 'feature': key,
                                 'detail': 'must be true, false, or an object '
                                           'with an enabled flag'})
                continue
            opinions.setdefault(key, []).append(op)
    if problems:
        return None, problems
    features = {}
    for key, ops in opinions.items():
        vals = [op for op in ops if op is not None]
        if any(v is False for v in vals):
            features[key] = False   # prune wins
        elif any(v is True for v in vals):
            features[key] = True
    composition = {
        'templates': [tid for tid, _, _ in resolved],
        'sections': sections,
        'features': features,
        'overrides_applied': [{'section': s, 'winner': w, 'default': defined[s]}
                              for s, w in ov.items()],
    }
    return composition, []


def apply_composition(contract, composition):
    """Feed a resolved composition into the existing pipeline (additive).

    Composed features merge into the contract's breaker dict: the contract's
    own declarations win — composition fills only keys the contract did not
    declare itself. Returns problems (usually []).
    """
    feats = contract.get('features')
    if feats is None:
        feats = {}
        contract['features'] = feats
    if not isinstance(feats, dict):
        return [{'code': 'features_shape_conflict',
                 'detail': 'a template composition needs features as a breaker '
                           'object, but this contract carries the contract-page '
                           'features list — pick one grammar'}]
    for key, val in composition['features'].items():
        if key not in feats:
            feats[key] = val
    return []


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

    Returns (cover_html, module_html, problems, events, enabled_fids,
             extra_receipt).
    - features as a list (contract-page) -> no breakers; nothing renders.
    - features as a dict -> standard features resolve via the three-state
      default-on mechanism; non-standard breakers keep the registry gate.
      Any enabled-but-unbuilt feature refuses (fail closed — no
      best-effort skip: under the coverage gate that state is unreachable
      by construction for default-on, and explicit claims are refused).
    - module_html: {module key -> section HTML} ('' unless declared+built).
      Every breaker renders on its OWN declaration — never behind cover's
      early-return (Wave A fix).
    - extra_receipt: per-module receipt additions (e.g. automation_audit),
      merged into manifest['receipt'] by main().
    context: the resolved connections+privacy+identity dict, handed to
    every feature module (connections stay opt-in inside modules).
    """
    problems, events, cover_html = [], [], ''
    module_html, extra_receipt = {}, {}
    enabled = []
    feats = contract.get('features')
    if not isinstance(feats, dict):
        return cover_html, module_html, problems, events, enabled, extra_receipt
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
    # per-module declarations: malformed decls are reported, but every
    # breaker is still checked so the refusal names every problem.
    mod_decls = {}
    for mod in BREAKER_MODULES:
        try:
            mod_decls[mod['key']] = mod['decl_for'](contract)
        except mod['refusal'] as e:
            problems.append({'code': e.code, 'feature': mod['fid'],
                             'detail': e.detail})
            mod_decls[mod['key']] = None
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
    # cover renders on its OWN declaration — never gating other breakers
    # (Wave A fix: F1's early-return made all breakers unreachable without
    # cover declared; each breaker now stands on its own contract flag).
    if not problems and decl is not None and decl.get('enabled'):
        try:
            cover_html = render_cover(decl, reg_statuses.get('cover'),
                                      context=context)
        except CoverRefusal as e:
            problems.append({'code': e.code, 'feature': FEATURE_COVER_ID,
                             'detail': e.detail})
            return cover_html, module_html, problems, events, enabled, extra_receipt
        events.append({'event': 'cover.updated', 'feature': FEATURE_COVER_ID,
                       'version': FEATURE_COVER_VERSION})
    # module rendering: each enabled module on its own flag. A module
    # enabled via omission under the default-on policy renders with a
    # fallback declaration (the module never hardcodes the default).
    if not problems:
        for mod in BREAKER_MODULES:
            fid = mod['fid']
            if fid not in enabled:
                continue
            mdecl = mod_decls.get(mod['key'])
            if mdecl is None:
                # Omitted + gate active: synthesize an enabled decl THROUGH
                # the module's decl_for (not a bare fallback) so its
                # defaults, dial-filling, and _connections/_privacy stashing
                # run — the module never hardcodes the default, but its
                # decl_for owns the declaration shape.
                synth_feats = dict(feats) if isinstance(feats, dict) else {}
                synth_feats[mod['key']] = {'enabled': True}
                synth = dict(contract)
                synth['features'] = synth_feats
                try:
                    mdecl = mod['decl_for'](synth)
                except mod['refusal'] as e:
                    problems.append({'code': e.code, 'feature': fid,
                                     'detail': e.detail})
                    return (cover_html, module_html, problems, events,
                            enabled, extra_receipt)
                if mdecl is None:
                    mdecl = {'enabled': True}  # module declined; bare fallback
            # decl_for may return False (explicit opt-out) — not a dict.
            if mdecl is False or not (mdecl.get('enabled') if isinstance(mdecl, dict) else mdecl):
                continue
            try:
                html, evts, extra = mod['render'](
                    mdecl, reg_statuses.get(mod['key']), context, contract)
            except mod['refusal'] as e:
                # Consent-line shape: the module's grant refusal
                # ('grant_required' / 'missing_grant') names the missing
                # connection grant; the resolver's gate 4
                # (permission_denied) names the missing registry permission.
                # Both are fail-closed; both carry the same STRUCTURE
                # {code, feature, detail, missing} — one shape, honest codes
                # for distinct layers (connection grant vs registry perm).
                err = {'code': e.code, 'feature': fid, 'detail': e.detail}
                if e.code in ('grant_required', 'missing_grant'):
                    err['missing'] = [e.detail.split(
                        'contract.connections.')[-1].split()[0]
                        if 'contract.connections.' in e.detail else 'unknown']
                problems.append(err)
                return (cover_html, module_html, problems, events,
                        enabled, extra_receipt)
            module_html[mod['key']] = html
            events.extend(evts)
            for k, v in extra.items():
                if k in _RECEIPT_RESERVED_KEYS:
                    problems.append(
                        {'code': 'receipt_key_collision', 'feature': fid,
                         'detail': 'extra receipt key %r is reserved' % (k,)})
                    return (cover_html, module_html, problems, events,
                            enabled, extra_receipt)
                if k in extra_receipt:
                    # list-valued extras (e.g. readiness) accumulate across
                    # modules; scalar collisions are a structured refusal.
                    if isinstance(extra_receipt[k], list) and isinstance(v, list):
                        extra_receipt[k].extend(v)
                    else:
                        problems.append(
                            {'code': 'receipt_key_collision', 'feature': fid,
                             'detail': 'extra receipt key %r already set'
                                       % (k,)})
                        return (cover_html, module_html, problems, events,
                                enabled, extra_receipt)
                else:
                    extra_receipt[k] = v
    return cover_html, module_html, problems, events, enabled, extra_receipt


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

# ---- intake page seam (assemble v1.14, additive) ----
# Renders the Smart Builder intake page (Shawn's 22:30Z rebuild spec) from
# contract['intake_page']. Active ONLY when the contract carries the
# 'intake_page' key — every existing contract assembles byte-for-byte as before.
# New placeholders (all consumed by templates/intake-page.html):
#   %%INTAKE_INTENT%% %%INTAKE_QUESTIONS%% %%PIECE_GALLERY%% %%SELECTION_TRAY%%
#   %%TEMPLATE_COLUMN%% %%FEATURE_SHOWCASE%% %%FEATURE_DATA_JSON%%
#   %%CONTRACT_OUTPUT%% %%PIECE_MANIFEST%%
INTAKE_PAGE_REQUIRED = ['steps', 'intent', 'questions', 'feature_showcase',
                        'feature_icons', 'template_samples']

def validate_intake_page(ip, contract, pieces, reg_by_id):
    """Fail-closed validation for the intake_page block. Returns problems."""
    problems = []
    if not isinstance(ip, dict):
        return [{'code': 'bad_intake_page',
                 'detail': 'intake_page must be an object, got %s'
                           % type(ip).__name__}]
    for k in INTAKE_PAGE_REQUIRED:
        if k not in ip:
            problems.append({'code': 'missing_key', 'key': 'intake_page.' + k})
    if problems:
        return problems
    # every icon model must resolve to a real, non-quarantined piece
    icon_models = list(ip['feature_icons'].values())
    for a in ip['intent'].get('affordances', []):
        if a.get('icon'):
            icon_models.append(a['icon'])
    for m in icon_models:
        if m not in pieces:
            problems.append({'code': 'unknown_model', 'model': m,
                             'where': 'intake_page icon'})
        elif pieces[m].get('quarantined'):
            problems.append({'code': 'piece_quarantined', 'model': m,
                             'where': 'intake_page icon',
                             'reason': pieces[m].get('quarantine_reason')})
        elif not pieces[m].get('html'):
            problems.append({'code': 'empty_piece', 'model': m,
                             'where': 'intake_page icon'})
    for fid in ip['feature_showcase']:
        if 'feature.' + fid not in reg_by_id:
            problems.append({'code': 'unknown_feature',
                             'feature': 'feature.' + fid})
    if len(ip['template_samples']) != len(contract.get('templates', [])):
        problems.append({'code': 'template_sample_mismatch',
                         'detail': 'template_samples has %d entries for %d templates'
                                   % (len(ip['template_samples']),
                                      len(contract.get('templates', [])))})
    return problems


def intake_sec_head(step_n, title, lede, color):
    return (
        '<div class="sec-head"><span class="kicker" style="color:%s">Step %d</span>'
        '<h2>%s</h2><p>%s</p></div>' % (color, step_n, esc(title), esc(lede)))


def render_intake_intent(ip, pieces, spectrum):
    st = ip['steps'][0]
    cards = []
    for i, a in enumerate(ip['intent']['affordances']):
        c = seq_color(spectrum, i)
        icon = ('<div class="a-icon"><div class="nb-scope">%s</div></div>'
                % pieces[a['icon']]['html']) if a.get('icon') else ''
        aid = a['id']
        if aid == 'type':
            control = (
                '<label class="fine" for="vision-type" style="font-weight:700;color:var(--paper)">'
                'Your vision</label>'
                '<textarea id="vision-type" placeholder="My app is\u2026"></textarea>'
                '<button class="naya-btn small teal" id="btn-save-type">'
                '<span class="nb-label">%s</span></button>' % esc(a['cta']))
        elif aid == 'paste':
            control = (
                '<label class="fine" for="vision-paste" style="font-weight:700;color:var(--paper)">'
                'Paste it here</label>'
                '<textarea id="vision-paste" placeholder="Paste notes, docs, messages\u2026"></textarea>'
                '<button class="naya-btn small teal" id="btn-import-paste">'
                '<span class="nb-label">%s</span></button>' % esc(a['cta']))
        else:
            control = (
                '<button class="naya-btn small teal" id="btn-dictate">'
                '<span class="nb-label">%s</span></button>'
                '<p class="fine" id="dictate-status" role="status"></p>' % esc(a['cta']))
        cards.append(
            '<div class="afford" style="--ac:%s">%s<h3>%s</h3><p>%s</p>%s</div>'
            % (c, icon, esc(a['label']), esc(a['desc']), control))
    return (intake_sec_head(st['n'], st['title'], st['lede'],
                            seq_color(spectrum, 1))
            + '<div class="afford-grid">%s</div>' % ''.join(cards))


def render_intake_questions(ip, spectrum, reg_by_id):
    st = ip['steps'][1]
    qs = {q['id']: q for q in ip['questions']}
    chips = []
    for fid in ip['feature_showcase']:
        entry = reg_by_id['feature.' + fid]
        chips.append(
            '<label class="fn-chip"><input type="checkbox" name="fn" value="%s" checked> %s</label>'
            % (esc(fid), esc(entry.get('name', fid))))
    q = qs['functions']
    return (
        intake_sec_head(st['n'], st['title'], st['lede'], seq_color(spectrum, 2))
        + '<div class="nb-chrome"><div class="demo-board" style="--c:%s">'
          '<form id="qform">'
          '<div class="qfield"><label for="q-vision">%s</label>'
          '<textarea id="q-vision" placeholder="%s"></textarea></div>'
          '<div class="qfield"><label for="q-goal">%s</label>'
          '<textarea id="q-goal" placeholder="%s"></textarea></div>'
          '<div class="qfield"><label id="fn-label">%s</label>'
          '<p class="fine">%s</p><div class="fn-chips" role="group" aria-labelledby="fn-label">%s</div></div>'
          '<div class="qfield"><label for="q-behavior">%s</label>'
          '<textarea id="q-behavior" placeholder="%s"></textarea></div>'
          '<button class="naya-btn small teal" type="submit" id="btn-save-answers">'
          '<span class="nb-label">Save my answers</span></button>'
          '</form></div></div>'
        % (seq_color(spectrum, 2),
           esc(qs['vision']['q']), esc(qs['vision'].get('hint', '')),
           esc(qs['goal']['q']), esc(qs['goal'].get('hint', '')),
           esc(q['q']), esc(q.get('hint', '')), ''.join(chips),
           esc(qs['behavior']['q']), esc(qs['behavior'].get('hint', ''))))


def intake_piece_card(cat, model, p, color):
    search = ' '.join([model, p['label'], p['kind'], p['category']]
                      + p.get('tags', [])).lower()
    return (
        '<div class="piece-card" style="--pc:%s" data-model="%s" data-cat="%s" '
        'data-label="%s" data-search="%s" aria-pressed="false">'
        '<div class="piece-stage"><div class="nb-scope">%s</div></div>'
        '<div class="piece-cat">%s</div>'
        '<div class="piece-meta"><b>%s</b><span class="model">%s \u00b7 %s</span>'
        '<p class="piece-note" hidden></p>'
        '<div class="piece-actions">'
        '<button class="mini-btn piece-select" data-model="%s" aria-pressed="false">Select</button>'
        '<button class="mini-btn piece-notes" aria-expanded="false" '
        'aria-label="Add a note to %s">Notes</button>'
        '</div>'
        '<div class="note-editor" hidden>'
        '<textarea aria-label="Note for %s" placeholder="\u201cMake this one coral\u2026\u201d"></textarea>'
        '<button class="mini-btn note-save">Save note</button>'
        '</div></div></div>'
        % (color, esc(model), esc(cat), esc(p['label']), esc(search), p['html'],
           esc(cat), esc(p['label']), esc(model), esc(p['kind']),
           esc(model), esc(model), esc(model)))


def render_intake_gallery(ip, wall, pieces, spectrum):
    st = ip['steps'][2]
    chips = ['<button class="catchip" data-cat="All" aria-pressed="true">All</button>']
    cards = []
    i = 0
    for cat, models in wall.items():
        c = seq_color(spectrum, i)
        chips.append('<button class="catchip" data-cat="%s" aria-pressed="false">%s</button>'
                     % (esc(cat), esc(cat)))
        for m in models:
            cards.append(intake_piece_card(cat, m, pieces[m], c))
        i += 1
    return (
        intake_sec_head(st['n'], st['title'], st['lede'], seq_color(spectrum, 3))
        + '<div class="gal-tools">'
          '<input type="search" id="piece-search" aria-label="Search pieces" '
          'placeholder="Search pieces \u2014 try \u201cbuttons\u201d">'
          '%s</div>'
          '<p class="fine" id="gal-empty" style="display:none">No pieces match \u2014 '
          'try a different word.</p>'
          '<div class="piece-grid" id="piece-grid">%s</div>'
        % (''.join(chips), ''.join(cards)))


def render_intake_tray():
    return (
        '<div class="tray" id="tray"><div class="tray-head"><h3>Your selection</h3>'
        '<button class="mini-btn" id="tray-clear">Clear</button></div>'
        '<div class="tray-items" id="tray-items">'
        '<p class="tray-empty">Nothing selected yet \u2014 tap <b>Select</b> on any piece '
        'above and it lands here.</p></div></div>')


def render_intake_templates(ip, templates, spectrum):
    st = ip['steps'][3]
    rows = []
    for i, e in enumerate(templates):
        num, title, desc, color = e[0], e[1], e[2], e[3] if len(e) > 3 else seq_color(spectrum, i)
        sample = ip['template_samples'][i]
        flag = ''
        if '\u00b7' in num:
            tag = num.split('\u00b7', 1)[1].strip()
            flag = '<span class="tpl-flag">%s</span>' % esc(tag)
        rows.append(
            '<div class="tpl-row" style="--tc:%s" data-tpl="%d">'
            '<div class="tpl-num">%s</div>'
            '<div class="tpl-main"><h3>%s</h3><p>%s</p>'
            '<div class="tpl-actions">'
            '<a class="naya-btn small" href="%s" target="_blank" rel="noopener">'
            '<span class="nb-label">Open the real sample page</span></a>'
            '<button class="naya-btn small teal tpl-pick" data-tpl="%d">'
            '<span class="nb-label">Pick this template</span></button>'
            '</div></div>%s</div>'
            % (color, i, esc(num), esc(title), esc(desc), esc(sample), i, flag))
    return (intake_sec_head(st['n'], st['title'], st['lede'], seq_color(spectrum, 4))
            + '<div class="tpl-col">%s</div>' % ''.join(rows))


def feature_status_badge(status):
    if status == 'built':
        return '<span class="badge built">Built \u00b7 live</span>'
    return '<span class="badge specified">Specified \u00b7 wiring in progress</span>'


def render_intake_features(ip, spectrum, reg_by_id, pieces):
    rows, data = [], []
    for i, fid in enumerate(ip['feature_showcase']):
        entry = reg_by_id['feature.' + fid]
        c = seq_color(spectrum, i)
        icon_model = ip['feature_icons'][fid]
        icon_html = ('<div class="feat-icon"><div class="nb-scope">%s</div></div>'
                     % pieces[icon_model]['html'])
        status = entry.get('status', 'specified')
        rows.append(
            '<div class="feat-row" style="--fc:%s" data-feature="feature.%s" data-consent="ready">'
            '%s<div class="feat-main"><h3>%s</h3><p>%s</p></div>'
            '%s'
            '<label class="feat-check"><input type="checkbox" data-feat="%s" checked> On</label>'
            '<button class="naya-btn small feat-see" data-fid="%s">'
            '<span class="nb-label">See it</span></button></div>'
            % (c, esc(fid), icon_html, esc(entry.get('name', fid)),
               esc(entry.get('intent', '')),
               feature_status_badge(status), esc(fid), esc(fid)))
        note = ip.get('reports_note') if fid == 'intelligence_today' else ''
        data.append({
            'fid': fid, 'name': entry.get('name', fid),
            'intent': entry.get('intent', ''),
            'status': status,
            'statusLabel': ('Built \u00b7 live on day one' if status == 'built'
                            else 'Specified \u00b7 wiring in progress'),
            'requires': entry.get('requires', []),
            'permissions': entry.get('permissions', []),
            'acceptance': entry.get('acceptance', []),
            'note': note,
            'iconHtml': pieces[icon_model]['html'],
        })
    reports = ('<p class="feat-reports"><b style="color:var(--paper)">Reports</b> \u2014 %s</p>'
               % esc(ip.get('reports_note', ''))) if ip.get('reports_note') else ''
    head = ('<div class="sec-head"><span class="kicker" style="color:%s">Standard features</span>'
            '<h2>Every Naya app comes with these</h2>'
            '<p>Not add-ons, not upsells. Each one is <b>on</b> \u2014 untick to remove. '
            'Tap <b>See it</b> on any feature to see it the way it will live on your phone: '
            'the real module where one is built, an honest status where it is still being wired '
            '\u2014 never a fake.</p></div>' % seq_color(spectrum, 5))
    return head + '<div class="feat-list">%s</div>' % ''.join(rows) + reports, data


def render_intake_output(ip, spectrum):
    st = ip['steps'][4]
    return (
        intake_sec_head(st['n'], st['title'], st['lede'], seq_color(spectrum, 6))
        + '<div class="out-grid">'
          '<div class="out-panel"><h3>Your vision</h3>'
          '<p class="out-empty" id="out-vision">Saved in steps 1\u20132 \u2014 it appears here.</p></div>'
          '<div class="out-panel"><h3>Your pieces<span class="count" id="out-pieces-count"></span></h3>'
          '<div id="out-pieces"><p class="out-empty">No pieces yet \u2014 pick some in step 3.</p></div></div>'
          '<div class="out-panel"><h3>Your template</h3>'
          '<p class="out-empty" id="out-template">Not chosen yet \u2014 pick one in step 4.</p></div>'
          '<div class="out-panel"><h3>Your features</h3><div id="out-features"></div></div>'
          '</div>'
          '<div class="out-actions">'
          '<button class="naya-btn" id="btn-copy-contract"><span class="nb-label">Copy the contract JSON</span></button>'
          '<button class="naya-btn gold" id="btn-ok-build"><span class="nb-label">Okay, build</span></button>'
          '</div>'
          '<p class="fine">This is the intake\u2019s output \u2014 the contract your app is built from. '
          '\u201cOkay, build\u201d hands it to the builder; nothing deploys without your word.</p>')


def render_intake_manifest(ip, wall, pieces, spectrum):
    groups = []
    wall_models = [(m, cat) for cat, models in wall.items() for m in models]
    groups.append(('Gallery pieces', wall_models))
    icon_models = sorted((set(ip['feature_icons'].values())
                         | {a['icon'] for a in ip['intent'].get('affordances', []) if a.get('icon')})
                         - {m for m, _ in wall_models})
    groups.append(('Icons', [(m, 'icon') for m in icon_models]))
    out = ['<div class="manifest"><h3>Piece manifest \u2014 every piece on this page, on the record</h3>'
           '<p class="fine">The human reads the name, the Naya reads the number. '
           'Quarantined pieces never appear here.</p>']
    for gname, models in groups:
        out.append('<div class="mgroup">%s \u00b7 %d</div><ul>' % (esc(gname), len(models)))
        for m, cat in models:
            p = pieces[m]
            out.append('<li><b>%s</b>%s</li>' % (esc(m), esc(p['label'])))
        out.append('</ul>')
    out.append('</div>')
    return ''.join(out)


def render_intake(contract, pieces, spectrum, sec, reg_by_id, reg_statuses):
    """Render every intake placeholder. Returns (replacements, extra_css_ids).

    extra_css_ids: CSS for icon pieces referenced outside the wall (feature
    and affordance icons) so they render in their real code too."""
    ip = contract['intake_page']
    wall, templates = contract['wall'], contract['templates']
    features_html, feature_data = render_intake_features(ip, spectrum, reg_by_id, pieces)
    replacements = {
        '%%INTAKE_INTENT%%': render_intake_intent(ip, pieces, spectrum),
        '%%INTAKE_QUESTIONS%%': render_intake_questions(ip, spectrum, reg_by_id),
        '%%PIECE_GALLERY%%': render_intake_gallery(ip, wall, pieces, spectrum),
        '%%SELECTION_TRAY%%': render_intake_tray(),
        '%%TEMPLATE_COLUMN%%': render_intake_templates(ip, templates, spectrum),
        '%%FEATURE_SHOWCASE%%': features_html,
        '%%FEATURE_DATA_JSON%%': safe_json_for_pre(feature_data),
        '%%CONTRACT_OUTPUT%%': render_intake_output(ip, spectrum),
        '%%PIECE_MANIFEST%%': render_intake_manifest(ip, wall, pieces, spectrum),
    }
    icon_models = (set(ip['feature_icons'].values())
                   | {a['icon'] for a in ip['intent'].get('affordances', []) if a.get('icon')})
    wall_css_seen = set()
    extra = [pieces[m]['css_id'] for m in icon_models
             if pieces[m].get('css_id') and pieces[m]['css_id'] not in wall_css_seen
             and not wall_css_seen.add(pieces[m]['css_id'])]
    return replacements, extra


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
    # intake page: validate the intake_page block with the same fail-closed bar
    if 'intake_page' in contract:
        problems += validate_intake_page(contract['intake_page'], contract,
                                         pieces, reg_by_id)
    # composable templates: resolve the multi-template composition BEFORE
    # the feature gate runs, so composed features flow through the
    # default-on three-state resolution (explicit composed false reads as
    # OFF — prune wins) and the registry's fail-closed binding below.
    # Additive: contracts that do not request a composition get
    # composition=None and behave exactly as before.
    composition, tmpl_problems = resolve_templates(contract)
    problems += tmpl_problems
    if composition is not None:
        problems += apply_composition(contract, composition)
    # feature breakers: the contract flips them, the registry gates them.
    # default-on resolution and the consent grant check share this code path:
    # the enabled set flows into both rendering and consent resolution.
    cover_html, module_html, breaker_problems, breaker_events, enabled_fids, \
        extra_receipt = activate_breakers(
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
    # intake seam: render the intake placeholders; collect icon CSS the wall missed
    intake_replacements = {}
    if 'intake_page' in contract:
        intake_replacements, intake_extra_css = render_intake(
            contract, pieces, SPECTRUM, SEC, reg_by_id, reg_statuses)
        for cid in intake_extra_css:
            if cid and cid not in wall_css_ids:
                wall_css_ids.append(cid)
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

    # templates -> the real .typecard piece, one spectrum color per card.
    # When a composition was resolved, render one card per composed template
    # (badge, the shape's declared name, sections contributed). Every value
    # comes from the contract; nothing is invented. The contract-page display
    # triples keep the existing path, byte-identical.
    if composition is not None:
        template_cards = []
        for i, tid in enumerate(composition['templates']):
            shape = contract['template_shapes'][tid]
            contributed = [s['name'] for s in composition['sections']
                           if s['source'] == tid]
            template_cards.append(
                ("0%d · composed" % (i + 1),
                 shape.get('name', tid),
                 "Sections: " + ", ".join(contributed) if contributed
                 else "No sections declared."))
    else:
        template_cards = contract['templates']
    templates = ''.join(
        '<div class="nb-chrome"><div class="typecard" style="--tc:%s">'
        '<div class="tk">%s</div>'
        '<h3 style="font-size:19px;margin:0 0 6px;color:var(--white)">%s</h3>'
        '<p style="font-size:14px;color:var(--slate);margin:0">%s</p></div></div>'
        % (seq_color(SPECTRUM, i, e[3] if len(e) > 3 else None), esc(e[0]), esc(e[1]), esc(e[2]))
        for i, e in enumerate(template_cards))
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
    for key, val in dict({
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
        '%%SMART_NOTES%%': module_html.get('smart_notes', ''),
        '%%NOTIFICATIONS%%': module_html.get('notifications', ''),
        '%%AUTOMATION%%': module_html.get('automation', ''),
        '%%SMART_MAIL%%': module_html.get('smart_mail', ''),
        '%%SPACE%%': module_html.get('space', ''),
        '%%SOCIAL_FEED%%': module_html.get('social_feed', ''),
        '%%SMART_LIST%%': module_html.get('smart_list', ''),
        '%%SMART_BARS%%': module_html.get('smart_bars', ''),
        '%%CONNECT%%': module_html.get('connect', ''),
        '%%COMMUNITY%%': module_html.get('community', ''),
        '%%SMART_TABS%%': module_html.get('smart_tabs', ''),
        '%%INTELLIGENCE_TODAY%%': module_html.get('intelligence_today', ''),
        '%%CONTACTS%%': module_html.get('contacts', ''),
        '%%NAYA_ANSWERS%%': module_html.get('naya_answers', ''),
        '%%SCHEDULER%%': module_html.get('scheduler', ''),
        '%%BROADCAST%%': module_html.get('broadcast', ''),
        '%%LOOP%%': loop,
        '%%PROMISE_BIG%%': esc(contract['promise']['big']).replace('within 24 hours.', '<em>within 24 hours.</em>'),
        '%%PROMISE_SUB%%': esc(contract['promise']['sub']),
        '%%MACHINE_JSON%%': machine_raw,  # raw: <pre> content, never an attribute
    }, **intake_replacements).items():
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
            # the resolved template composition (None when the contract did
            # not request one) — deterministic, part of the build record.
            'composition': composition,
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
        'receipt': dict({
            'built_utc': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
            # capability-contract events the build actually fired
            'events': breaker_events,
            # consent-line audit trail: the active grants, mirrored on
            # EVERY build receipt, plus the per-feature ready/connected
            # resolution the resolver computed.
            'grants': context['connections'],
            'privacy': context['privacy'],
            'identity': identity,
            'consent': consent,
        }, **extra_receipt),
    }
    json.dump(manifest, open(a.manifest, 'w'), indent=2)
    print('page:', a.out, manifest['build']['page']['bytes'], 'bytes')
    print('build id:', build_id[:16])
    print('manifest:', a.manifest)

if __name__ == '__main__':
    main()
