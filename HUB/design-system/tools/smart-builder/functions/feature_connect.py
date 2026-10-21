#!/usr/bin/env python3
"""feature.connect — "Connect + communicate" (Smart Builder feature breaker).

Capability contract (functions/registry.json):
  id: feature.connect, version 1.0.0, status tracked in the registry.
  activated_by: contract.features.connect — the CONTRACT flips the breaker;
  the module never hand-wires itself into a page.

THREE-STATE INTERFACE (Shawn 21:32Z):
  explicit true  -> on. With no details: the honest idle shell (never a
                   staged control, never a refusal — day-one working).
  explicit false -> off: no render, no claim, no error.
  omitted        -> the assembler applies its policy (connect is a standard
                   feature: default-on, opt-out — the module hardcodes
                   nothing; the policy arrives as enabled:true).

Activation input (from the contract, which carries the intake's answers):
  contract.features.connect = {
      "enabled": true,
      "owner_name": "Morning Crumb",
      "consent": true,                 # REQUIRED when channels are declared:
                                       # the owner opted in to being contacted
                                       # (registry acceptance:
                                       # no_contact_without_consent). The
                                       # contract declaration IS the consent
                                       # record at build time.
      "channels": [                    # owner-published contact paths
          {"kind": "email", "label": "Write to us", "href": "mailto:hello@example.com"},
          {"kind": "phone", "label": "Call", "href": "tel:+15550123456"},
          {"kind": "link",  "label": "Instagram", "href": "https://instagram.com/..."},
          {"kind": "chat",  "label": "Chat", "href": "https://chat.example.com/..."}
      ],
      "form_action": "https://forms.example.com/connect",  # optional: the request
                                       # form renders only when the owner wired
                                       # a real endpoint (no dead forms).
      "note": "We reply within a day." # optional, plain text
  }

Behavior:
  - Not declared / explicit false / policy-off -> render nothing.
  - Declared + registry says built -> connect panel HTML.
  - Declared + registry says anything else -> ConnectRefusal('feature_not_built').
  - Channels declared without consent -> ConnectRefusal('no_consent'): no
    contact paths publish without consent. (No channels -> nothing to gate:
    the idle shell needs no consent.)
  - Channel hrefs allowlisted by kind: email->mailto:, phone->tel:,
    link/chat->absolute http(s). Hostile -> ConnectRefusal('unsafe_contact_url').
  - Enabled with no channels and no form_action -> honest idle shell
    ("Direct connections open when the owner adds a contact path") — a
    useful day-one render, zero errors, nothing staged.
  - form_action absent -> channels only, no form. A request form that posts
    nowhere is staged functionality — never rendered.
  - PRIVACY DIAL (contract.privacy): channels are owner-published paths —
    they render at every dial (consent-gated, not dial-gated). The request
    form is inbound: private -> suppressed; network -> needs the recorded
    nayanet grant; public -> needs the recorded network grant. A wired form
    without its grant -> ConnectRefusal('missing_grant') naming the grant
    (the contract claims a connected capability it has no grant for); an
    unwired form at a wider dial is simply absent, never staged.
  - CONSENT LINE: the contact surface is READY (works with zero grants —
    incoming requests are viewable by the owner, channels work). Accepting /
    initiating across systems is CONNECTED (grant-recorded). The page carries
    data-mode="idle"|"ready"|"connected" and data-grant when connected;
    copy never conflates the two.
  - Build-time events: none. The registry's connect events
    (connect.requested / .accepted / .declined) are visitor-lifecycle
    events; firing one at build time would misrepresent what happened.

Returns (html, meta); meta = {"mode": ..., "consent": "ready"|"connected"}.
Stdlib only. Pure functions — same declaration -> same bytes, always.
"""
import html as htmlmod
import re
from urllib.parse import urlparse

VERSION = "1.0.0"
FEATURE_ID = "feature.connect"
# aliases the assembler imports
FEATURE_CONNECT_ID = FEATURE_ID
FEATURE_CONNECT_VERSION = VERSION

_CHANNEL_KINDS = ("email", "phone", "link", "chat")
_EMAIL_RE = re.compile(r"^mailto:[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+$")
_PHONE_RE = re.compile(r"^tel:\+?[0-9().\- ]+$")
# dial -> grant that gates the inbound request form at that dial
# (private needs none: the form is suppressed there, not granted)
_DIAL_GRANT = {"network": "nayanet", "public": "network"}


class ConnectRefusal(Exception):
    """Structured refusal: the connect breaker declined to activate.

    code: machine-readable failure class (never a transport error —
    this module performs no I/O, so every refusal is a content/contract
    failure, cf. lesson L-2026-10-16-004).
    detail: human-readable explanation for the receipt.
    """
    def __init__(self, code, detail=""):
        super().__init__("%s: %s" % (code, detail))
        self.code = code
        self.detail = detail


def esc(s):
    return htmlmod.escape(str(s), quote=True)


def default_ctx():
    """Assembler context when the caller passes none: most private,
    zero grants — the fail-closed default."""
    return {"privacy": "private",
            "connections": {"muse": False, "github": False,
                            "network": False, "nayanet": False}}


def _check_http_url(u, label):
    p = urlparse(u)
    scheme = (p.scheme or "").lower()
    if scheme in ("http", "https"):
        if not p.hostname:
            raise ConnectRefusal("unsafe_contact_url",
                                 "channel %r: %s URL has no host" % (label, scheme))
        if any(c.isspace() for c in p.hostname):
            raise ConnectRefusal("unsafe_contact_url",
                                 "channel %r: whitespace in host" % label)
        return u
    reason = "relative URLs are not allowed" if not scheme \
        else "disallowed scheme %r" % p.scheme
    raise ConnectRefusal("unsafe_contact_url",
                         "channel %r: %s" % (label, reason))


def sanitize_channel_href(kind, href, label):
    """Allowlist contact hrefs by channel kind. Returns the cleaned href,
    raises ConnectRefusal('unsafe_contact_url') for anything hostile."""
    if not isinstance(href, str):
        raise ConnectRefusal("unsafe_contact_url",
                             "channel %r: not a string (%s)"
                             % (label, type(href).__name__))
    u = href.strip()
    if not u:
        raise ConnectRefusal("unsafe_contact_url",
                             "channel %r: empty href" % label)
    if any(ord(c) < 0x20 for c in u):
        raise ConnectRefusal("unsafe_contact_url",
                             "channel %r: control characters in href" % label)
    if kind == "email":
        if _EMAIL_RE.match(u):
            return u
        raise ConnectRefusal("unsafe_contact_url",
                             "channel %r: not a valid mailto: address" % label)
    if kind == "phone":
        if _PHONE_RE.match(u):
            return u
        raise ConnectRefusal("unsafe_contact_url",
                             "channel %r: not a valid tel: number" % label)
    return _check_http_url(u, label)


def decl_for(contract):
    """Extract the connect declaration: the three-state interface.

      False            -> {"enabled": False}: explicit opt-out. Off means
                          off — no render, no claim, no error.
      None/falsy/absent-> None: omitted. The assembler applies its policy
                          (connect is default-on standard); the module
                          hardcodes no default.
      True             -> {"enabled": True}: on; with no details the idle
                          shell renders (day-one working, zero errors).
      dict             -> as-is: explicit configuration. A dict without an
                          "enabled" key counts as on; "enabled": false as off.
      other truthy     -> ConnectRefusal('bad_connect_declaration').
    """
    feats = contract.get("features") if isinstance(contract, dict) else None
    if not isinstance(feats, dict):
        return None  # contract-page contracts carry features as a list
    if "connect" not in feats:
        return None
    decl = feats["connect"]
    if decl is False:
        return {"enabled": False}
    if not decl:
        return None
    if decl is True:
        return {"enabled": True}
    if isinstance(decl, dict):
        return decl
    raise ConnectRefusal("bad_connect_declaration",
                         "contract.features.connect must be an object, "
                         "true, or false — got %s" % type(decl).__name__)


def channels_for(decl):
    """Declared channels, sanitized. Raises on malformed entries."""
    raw = decl.get("channels") or []
    if not isinstance(raw, list):
        raise ConnectRefusal("bad_channel",
                             "channels must be a list, got %s" % type(raw).__name__)
    out = []
    for i, item in enumerate(raw):
        if not isinstance(item, dict):
            raise ConnectRefusal("bad_channel",
                                 "channel #%d: must be an object, got %s"
                                 % (i, type(item).__name__))
        kind = str(item.get("kind") or "").strip().lower()
        if kind not in _CHANNEL_KINDS:
            raise ConnectRefusal("bad_channel",
                                 "channel #%d: unknown kind %r (want one of %s)"
                                 % (i, item.get("kind"), ", ".join(_CHANNEL_KINDS)))
        label = str(item.get("label") or "").strip()
        if not label:
            raise ConnectRefusal("bad_channel", "channel #%d: empty label" % i)
        href = sanitize_channel_href(kind, item.get("href"), label)
        out.append((kind, label, href))
    return out


def sanitize_form_action(action):
    """The request form posts only to a declared absolute https URL."""
    if action is None:
        return None
    if not isinstance(action, str) or not action.strip():
        raise ConnectRefusal("unsafe_contact_url",
                             "form_action: must be a non-empty string")
    u = action.strip()
    if any(ord(c) < 0x20 for c in u):
        raise ConnectRefusal("unsafe_contact_url",
                             "form_action: control characters in URL")
    p = urlparse(u)
    if (p.scheme or "").lower() != "https" or not p.hostname:
        raise ConnectRefusal("unsafe_contact_url",
                             "form_action: must be an absolute https URL")
    if any(c.isspace() for c in p.hostname):
        raise ConnectRefusal("unsafe_contact_url",
                             "form_action: whitespace in host")
    return u


def _idle_shell(privacy):
    html = (
        '<section class="connect connect-idle" data-feature="connect" '
        'data-connect-status="built" data-privacy="%s" data-mode="idle" '
        'aria-label="Connect with the owner">'
        '<h2 class="connect-title">Connect</h2>'
        '<p class="connect-note">Direct connections open when the owner '
        'adds a contact path.</p>'
        '</section>' % esc(privacy))
    return html, {"mode": "idle", "consent": "ready"}


def render_connect(decl, registry_status, context=None):
    """Render the connect panel. Returns (html, meta).

    html is '' when the contract did not declare connect or opted out;
    raises ConnectRefusal otherwise. meta = {"mode": ..., "consent": ...}.
    registry_status: the registry's status string — rendering is proof the
    registry says 'built' (data-connect-status="built" is the binding).
    """
    ctx = context or default_ctx()
    privacy = ctx["privacy"]
    grants = ctx["connections"]
    if decl is None or decl.get("enabled") is False:
        return "", {"mode": "off", "consent": "ready"}
    if registry_status != "built":
        raise ConnectRefusal(
            "feature_not_built",
            "contract declares connect but registry status is %r "
            "(contract never activates an unbuilt capability)" % (registry_status,))

    # Validate everything declared, always — fail closed on hostile input
    # even when the dial will suppress parts of the render.
    channels = channels_for(decl)
    if channels and not decl.get("consent"):
        raise ConnectRefusal(
            "no_consent",
            "contract declares connect channels without owner consent — "
            "no contact paths publish without consent (registry acceptance: "
            "no_contact_without_consent)")
    form_action = sanitize_form_action(decl.get("form_action"))

    owner = str(decl.get("owner_name") or "").strip() or "The owner"
    note = str(decl.get("note") or "").strip()

    if not channels and not form_action:
        return _idle_shell(privacy)

    # Consent line + privacy dial for the inbound request form:
    # private -> suppressed (inbound is members-only); network/public ->
    # the recorded grant gates it. A wired form without its grant is a
    # connected capability claimed without a grant -> structured refusal
    # naming the grant. An unwired form is simply absent, never staged.
    form = ""
    mode, consent = "ready", "ready"
    grant_attr = ""
    if form_action and privacy in _DIAL_GRANT:
        grant = _DIAL_GRANT[privacy]
        if not grants.get(grant):
            raise ConnectRefusal(
                "missing_grant",
                "connect wires a request form for the %s audience but the %s "
                "grant is not recorded (contract.connections.%s) — "
                "requesting across that boundary is a connected capability"
                % (privacy, grant, grant))
        mode, consent = "connected", "connected"
        grant_attr = ' data-grant="%s"' % esc(grant)
        form = (
            '<form class="connect-form" action="%s" method="post">'
            '<label>Your name<input type="text" name="name" required '
            'autocomplete="name" maxlength="80"></label>'
            '<label>Your email<input type="email" name="email" required '
            'autocomplete="email" maxlength="120"></label>'
            '<label>Message<textarea name="message" required maxlength="2000" '
            'rows="4"></textarea></label>'
            '<button type="submit" class="naya-btn">'
            '<span class="nb-label">Send request</span></button>'
            '</form>' % esc(form_action))

    cards = "".join(
        '<a class="connect-card connect-%s" href="%s">'
        '<span class="connect-label">%s</span></a>'
        % (esc(kind), esc(href), esc(label))
        for kind, label, href in channels)
    note_html = ('<p class="connect-note">%s</p>' % esc(note)) if note else ""

    html = (
        '<section class="connect" data-feature="connect" '
        'data-connect-status="built" data-privacy="%s" data-mode="%s"%s '
        'aria-label="Connect with the owner">'
        '<h2 class="connect-title">Connect with %s</h2>'
        '%s'
        '<div class="connect-channels">%s</div>'
        '%s'
        '</section>'
        % (esc(privacy), mode, grant_attr, esc(owner), note_html, cards, form)
    )
    return html, {"mode": mode, "consent": consent}
