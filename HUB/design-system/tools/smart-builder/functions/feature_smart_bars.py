#!/usr/bin/env python3
"""feature.smart_bars — "Smart bars" (Smart Builder feature breaker).

Capability contract (functions/registry.json):
  id: feature.smart_bars, version 1.0.0, status tracked in the registry.
  activated_by: contract.features.smart_bars — the CONTRACT flips the breaker;
  the module never hand-wires itself into a page.

THREE-STATE INTERFACE (Shawn 21:32Z):
  explicit true  -> on (defaults: brand + section links)
  explicit false -> off: no render, no claim, no error — the registry gate
                    does not even run for an opted-out breaker
  omitted        -> the assembler applies its policy (the module hardcodes
                    no default); the policy value arrives as enabled:true

Activation input (from the contract):
  contract.features.smart_bars = {
      "enabled": true,
      "brand": "Morning Crumb",          # optional; falls back to "Your page"
      "links": [                          # optional; default bar when absent
          {"label": "Menu", "href": "#menu", "audience": "public"},
          {"label": "Order", "href": "https://order.example.com/"}
      ],
      "sticky": true,                     # optional, default true
      "sync": false                       # optional: cross-page sync (connected)
  }

Behavior:
  - Not declared / explicit false / policy-off -> render nothing.
  - Declared + registry says built -> navigation bar HTML.
  - Declared + registry says anything else -> SmartBarsRefusal('feature_not_built').
  - hrefs: safe in-page anchors (#section) or absolute http(s) URLs.
    Declared anchors are owner content (like cover photo URLs): verified
    safe and well-formed, never verified live — the builder-generated
    default bar's anchors ARE verified against the template.
    Anything hostile -> SmartBarsRefusal('unsafe_bar_href'), fail closed.
    (L-2026-10-17-002: no dead link claimed live.)
  - No links declared -> default bar: brand + links to real page sections
    (#top, #features, #templates, #machine — all present in the template).
  - PRIVACY DIAL (contract.privacy): links may declare "audience":
    private|network|public (default private = visible everywhere). A link
    renders iff level(audience) <= level(dial). Unknown audience -> refusal.
  - CONSENT LINE: local bars = READY (zero grants). "sync": true requests
    cross-page sync = CONNECTED -> requires the recorded nayanet grant
    (contract.connections.nayanet); without it -> SmartBarsRefusal
    ('missing_grant') naming the grant. Never conflated: the page carries
    data-mode="ready"|"connected" and data-grant when connected.
  - Mobile collapse is pure HTML/CSS (checkbox toggle, media query):
    no script binds to anything, so L-2026-10-17-004 holds structurally.
  - Build-time event: bars.rendered (the bars genuinely were rendered).

Returns (html, meta); meta = {"mode": "ready"|"connected"|"off",
"consent": "ready"|"connected"}. Stdlib only. Pure functions.
"""
import html as htmlmod
import re
from urllib.parse import urlparse

VERSION = "1.0.0"
FEATURE_ID = "feature.smart_bars"
# aliases the assembler imports
FEATURE_SMART_BARS_ID = FEATURE_ID
FEATURE_SMART_BARS_VERSION = VERSION

MAX_LINKS = 24  # fail closed: a contract declaring more is malformed

# Default bar: every anchor provably exists in templates/page.html
# (#top is on <body>; the sections ship in the shared template).
DEFAULT_LINKS = (
    ("Top", "#top"),
    ("Features", "#features"),
    ("Templates", "#templates"),
    ("Machine", "#machine"),
)

_ANCHOR_RE = re.compile(r"^#[A-Za-z][\w\-.]*$")
_PRIVACY_LEVEL = {"private": 0, "network": 1, "public": 2}


class SmartBarsRefusal(Exception):
    """Structured refusal: the smart-bars breaker declined to activate.

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


def sanitize_bar_href(href, label):
    """Allowlist bar hrefs. Returns the cleaned href.

    Allowed: safe in-page anchors (#section) and absolute http(s) URLs.
    Raises SmartBarsRefusal('unsafe_bar_href') for anything hostile.
    (L-2026-10-17-002: a dead or hostile link claimed live is a content
    failure — fail closed instead of rendering it.)
    """
    if not isinstance(href, str):
        raise SmartBarsRefusal("unsafe_bar_href",
                               "link %r: not a string (%s)"
                               % (label, type(href).__name__))
    u = href.strip()
    if not u:
        raise SmartBarsRefusal("unsafe_bar_href",
                               "link %r: empty href" % label)
    if any(ord(c) < 0x20 for c in u):
        raise SmartBarsRefusal("unsafe_bar_href",
                               "link %r: control characters in href" % label)
    if u.startswith("#"):
        if _ANCHOR_RE.match(u):
            return u
        raise SmartBarsRefusal("unsafe_bar_href",
                               "link %r: malformed anchor %r" % (label, u))
    p = urlparse(u)
    scheme = (p.scheme or "").lower()
    if scheme in ("http", "https"):
        if not p.hostname:
            raise SmartBarsRefusal("unsafe_bar_href",
                                   "link %r: %s URL has no host" % (label, scheme))
        if any(c.isspace() for c in p.hostname):
            raise SmartBarsRefusal("unsafe_bar_href",
                                   "link %r: whitespace in host" % label)
        return u
    reason = "relative URLs are not allowed" if not scheme \
        else "disallowed scheme %r" % p.scheme
    raise SmartBarsRefusal("unsafe_bar_href",
                           "link %r: %s" % (label, reason))


def decl_for(contract):
    """Extract the smart-bars declaration: the three-state interface.

      False            -> {"enabled": False}: explicit opt-out. Off means
                          off — no render, no claim, no error.
      None/falsy/absent-> None: omitted. The assembler applies its policy;
                          the module hardcodes no default.
      True             -> {"enabled": True}: on with defaults.
      dict             -> as-is: explicit configuration. A dict without an
                          "enabled" key counts as on (presence is the flip);
                          "enabled": false inside the dict counts as off.
      other truthy     -> SmartBarsRefusal('bad_smart_bars_declaration').
    """
    feats = contract.get("features") if isinstance(contract, dict) else None
    if not isinstance(feats, dict):
        return None  # contract-page contracts carry features as a list
    if "smart_bars" not in feats:
        return None
    decl = feats["smart_bars"]
    if decl is False:
        return {"enabled": False}
    if not decl:
        return None
    if decl is True:
        return {"enabled": True}
    if isinstance(decl, dict):
        return decl
    raise SmartBarsRefusal("bad_smart_bars_declaration",
                           "contract.features.smart_bars must be an object, "
                           "true, or false — got %s" % type(decl).__name__)


def links_for(decl, privacy):
    """Declared links: sanitized, then audience-filtered by the privacy dial.

    Link "audience": private|network|public (default private = visible at
    every dial). A link renders iff level(audience) <= level(dial): a
    public-scoped link shows only on public pages, a network-scoped link on
    network and public, a private-scoped (or unscoped) link everywhere.
    All-filtered or absent -> the default bar, never an empty nav.
    """
    raw = decl.get("links")
    if raw is None:
        return list(DEFAULT_LINKS)
    if not isinstance(raw, list):
        raise SmartBarsRefusal("bad_bar_link",
                               "links must be a list, got %s" % type(raw).__name__)
    if len(raw) > MAX_LINKS:
        raise SmartBarsRefusal("too_many_links",
                               "%d links declared, max %d" % (len(raw), MAX_LINKS))
    dial_level = _PRIVACY_LEVEL[privacy]
    out = []
    for i, item in enumerate(raw):
        if not isinstance(item, dict):
            raise SmartBarsRefusal("bad_bar_link",
                                   "link #%d: must be an object, got %s"
                                   % (i, type(item).__name__))
        label = str(item.get("label") or "").strip()
        if not label:
            raise SmartBarsRefusal("bad_bar_link",
                                   "link #%d: empty label" % i)
        href = sanitize_bar_href(item.get("href"), label)
        audience = str(item.get("audience") or "private").strip().lower()
        if audience not in _PRIVACY_LEVEL:
            raise SmartBarsRefusal("bad_bar_link",
                                   "link #%d: unknown audience %r (want one of %s)"
                                   % (i, item.get("audience"),
                                      ", ".join(sorted(_PRIVACY_LEVEL))))
        if _PRIVACY_LEVEL[audience] <= dial_level:
            out.append((label, href))
    if not out:
        return list(DEFAULT_LINKS)  # all filtered -> default bar, never empty
    return out


def render_smart_bars(decl, registry_status, context=None):
    """Render the navigation bar. Returns (html, meta).

    html is '' when the contract did not declare smart_bars or opted out;
    raises SmartBarsRefusal otherwise. meta = {"mode": ..., "consent": ...}.
    registry_status: the registry's status string — rendering is proof the
    registry says 'built' (data-smart-bars-status="built" is the binding).
    """
    ctx = context or default_ctx()
    privacy = ctx["privacy"]
    if decl is None or decl.get("enabled") is False:
        return "", {"mode": "off", "consent": "ready"}
    if registry_status != "built":
        raise SmartBarsRefusal(
            "feature_not_built",
            "contract declares smart_bars but registry status is %r "
            "(contract never activates an unbuilt capability)" % (registry_status,))

    brand = str(decl.get("brand") or "").strip() or "Your page"
    links = links_for(decl, privacy)
    sticky = bool(decl.get("sticky", True))

    # Consent line: local bars are READY (zero grants). Cross-page sync is
    # CONNECTED — it needs the recorded nayanet grant, named on refusal.
    sync = bool(decl.get("sync"))
    grants = ctx["connections"]
    if sync and not grants.get("nayanet"):
        raise SmartBarsRefusal(
            "missing_grant",
            "smart_bars declares sync=true (cross-page sync) but the nayanet "
            "grant is not recorded (contract.connections.nayanet) — sync is "
            "a connected capability; local bars are ready without grants")
    mode = "connected" if sync else "ready"

    items = "".join(
        '<a class="sb-link" href="%s">%s</a>' % (esc(href), esc(label))
        for label, href in links)

    html = (
        '<div class="smart-bars" data-feature="smart_bars" '
        'data-smart-bars-status="built" data-privacy="%s" data-mode="%s"%s>'
        '<input type="checkbox" id="sb-nav-toggle" class="sb-nav-toggle" '
        'tabindex="-1" aria-hidden="true">'
        '<nav class="sb-bar%s" aria-label="Page navigation">'
        '<a class="sb-brand" href="#top">%s</a>'
        '<label class="sb-menu-btn" for="sb-nav-toggle" aria-label="Open menu">'
        '<span></span><span></span><span></span></label>'
        '<div class="sb-links">%s</div>'
        '</nav></div>'
        % (esc(privacy), mode,
           ' data-grant="nayanet"' if sync else "",
           " sb-sticky" if sticky else "", esc(brand), items)
    )
    return html, {"mode": mode, "consent": "connected" if sync else "ready"}
