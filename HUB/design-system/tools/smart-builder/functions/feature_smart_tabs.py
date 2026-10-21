#!/usr/bin/env python3
"""feature.smart_tabs — "Smart tabs" (Smart Builder feature breaker).

Capability contract (functions/registry.json):
  id: feature.smart_tabs, version 1.0.0, status tracked in the registry.
  activated_by: contract.features.smart_tabs — the CONTRACT flips the breaker;
  the module never hand-wires itself into a page.

Activation input (from the contract, which carries the owner's page list):
  contract.features.smart_tabs = {
      "enabled": true,
      "pages": [{"title": "Morning Crumb", "url": "https://..."}, ...],
      "active_url": "https://... (which tab is current, optional)",
      "aria_label": "Your pages (optional)",
      "fallback_title": "This page (optional, used when pages is empty)"
  }

Behavior (THREE-STATE interface — Shawn's product rule 21:32Z,
default-on, opt-out):
  - Explicit true (true, or {"enabled": truthy}) -> ON: tab-bar HTML.
  - Explicit false (false, {"enabled": falsy}, or any other present-but-
    falsy value) -> OFF: no render, no claim, no refusal.
  - Omitted (key absent, or features not a dict) -> the ASSEMBLER's
    default-on policy decides; the module hardcodes no default.
  - Declared + registry says built -> tab-bar HTML: one real anchor per
    owned page, every href verified against the declaration (L-2026-10-17-002
    — no dead link is ever claimed live).
  - Declared + registry says anything else -> TabsRefusal('feature_not_built').
    The contract never advertises a capability as operational unless the
    registry says it is built.
  - Unsafe page URLs -> TabsRefusal('unsafe_tabs_url'), fail closed.
    Allowed: absolute http(s) URLs. Rejected: javascript:, data:,
    vbscript:, file:, ftp:, protocol-relative, relative URLs, anything
    with control characters or whitespace in the host.
  - Declared but pages absent/empty -> graceful fallback: the tabs chrome
    with a single current tab labeled "This page" — never a broken list.
    (Day-one: {"enabled": true} alone renders useful chrome, zero errors.)
  - Tabs are plain anchors; no JS handler is bound, so no handler can
    point at DOM that does not exist (L-2026-10-17-004).
  - Connections (contract["connections"]): this module performs no I/O
    and gates nothing on connections — the tab bar renders when enabled,
    connections or not. Feature enabled ≠ connection available.
  - Privacy: the resolved contract context carries the privacy dial
    (private|network|public, default private); the rendered markup
    stamps it as data-privacy-scope. Enforcement beyond the stamp is
    serve-time (static HTML cannot authenticate a viewer); the stamp
    exists so nothing downstream mistakes the scope.
  - READY vs CONNECTED (consent line, adopted 21:41Z) — carried in
    the capability contract as top-level "ready"/"connected" keys:
    READY (default): local navigation from contract-carried pages —
    installed, working, no setup, no grant; renders with all
    connections false. CONNECTED: none — this module has no connected
    actions, so there is nothing to consent to. The build receipt
    mirrors the evaluated grants; UI copy never says "connected"
    when the module is merely ready.

Stdlib only. Pure functions — same declaration -> same bytes, always.
"""
import html as htmlmod
from urllib.parse import urlparse

VERSION = "1.0.0"
FEATURE_ID = "feature.smart_tabs"
# aliases the assembler imports
FEATURE_SMART_TABS_ID = FEATURE_ID
FEATURE_SMART_TABS_VERSION = VERSION

REGISTRY_KEY = "smart_tabs"   # functions registry id minus the feature. prefix
SLOT = "smart_tabs"           # template slot %%SMART_TABS%%
EVENT = "smart_tabs.updated"  # build-time event (F1: <breaker>.updated)

MAX_PAGES = 24  # a contract carrying more than this is malformed

PRIVACY_SCOPES = ("private", "network", "public")

GRANT_NAMES = ("muse", "github", "network", "nayanet")

# (declaration field, grant name, human description) — empty here:
# smart_tabs has no connected actions; local navigation is ready.
CONNECTED_ACTIONS = ()


class TabsRefusal(Exception):
    """Structured refusal: the smart-tabs breaker declined to activate.

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


def sanitize_tab_url(url, field):
    """Allowlist tab URLs. Returns the cleaned URL; raises
    TabsRefusal('unsafe_tabs_url') for anything hostile."""
    if not isinstance(url, str):
        raise TabsRefusal("unsafe_tabs_url",
                          "%s: not a string (%s)" % (field, type(url).__name__))
    u = url.strip()
    if any(ord(c) < 0x20 for c in u):
        raise TabsRefusal("unsafe_tabs_url",
                          "%s: control characters in URL" % field)
    p = urlparse(u)
    scheme = (p.scheme or "").lower()
    if scheme in ("http", "https"):
        if not p.hostname:
            raise TabsRefusal("unsafe_tabs_url",
                              "%s: %s URL has no host" % (field, scheme))
        if any(c.isspace() for c in p.hostname):
            raise TabsRefusal("unsafe_tabs_url",
                              "%s: whitespace in host" % field)
        return u
    reason = "relative URLs are not allowed" if not scheme \
        else "disallowed scheme %r" % p.scheme
    raise TabsRefusal("unsafe_tabs_url", "%s: %s" % (field, reason))


def decl_for(contract):
    """Extract the smart-tabs declaration from a contract.

    THREE-STATE interface (Shawn's product rule 21:32Z — default-on,
    opt-out):
      - True -> {"enabled": True} (explicit ON)
      - dict -> the declaration as-is (enabled truthy -> ON,
        enabled falsy -> OFF)
      - False / 0 / "" / [] / any other present-but-falsy value ->
        False (explicit OFF — opt-out: no render, no claim)
      - key absent, or features not a dict -> None (OMITTED — the
        assembler's default-on policy decides; the module hardcodes
        no default)
      - anything else truthy -> TabsRefusal('bad_tabs_declaration')
    """
    feats = contract.get("features") if isinstance(contract, dict) else None
    if not isinstance(feats, dict):
        return None  # contract-page contracts carry features as a list
    if "smart_tabs" not in feats:
        return None
    decl = feats["smart_tabs"]
    if decl is True:
        return {"enabled": True}
    if isinstance(decl, dict):
        return decl
    if not decl:
        return False  # explicit opt-out
    raise TabsRefusal("bad_tabs_declaration",
                      "contract.features.smart_tabs must be an object, true, "
                      "or false, got %s" % type(decl).__name__)


def pages_for(decl):
    """Sanitized page list: [(title, url), ...]. Raises TabsRefusal on
    malformed entries."""
    raw = decl.get("pages")
    if raw is None:
        return []
    if not isinstance(raw, list):
        raise TabsRefusal("bad_tabs_declaration",
                          "pages must be a list, got %s" % type(raw).__name__)
    if len(raw) > MAX_PAGES:
        raise TabsRefusal("tabs_too_many",
                          "pages carries %d entries (max %d)" % (len(raw), MAX_PAGES))
    out = []
    for i, entry in enumerate(raw):
        field = "pages[%d]" % i
        if not isinstance(entry, dict):
            raise TabsRefusal("bad_tabs_declaration",
                              "%s must be an object, got %s"
                              % (field, type(entry).__name__))
        title = entry.get("title")
        if not isinstance(title, str) or not title.strip():
            raise TabsRefusal("bad_tabs_declaration",
                              "%s.title must be a non-empty string" % field)
        url = sanitize_tab_url(entry.get("url"), field + ".url")
        out.append((title.strip(), url))
    return out


def _norm_url(u):
    """Trailing-slash-insensitive comparison: the contract may declare the
    active tab as https://a.example while the page list carries
    https://a.example/ — both name the same tab."""
    return u.rstrip("/") or "/"


def _context_parts(context):
    """Split the assembler's resolved context into (privacy, grants).

    The assembler resolves connections + privacy once per build
    (resolve_contract_context); modules read the resolved values here.
    Defaults match the assembler's: privacy 'private', all grants False.
    """
    ctx = context or {}
    privacy = ctx.get("privacy", "private")
    raw_grants = ctx.get("connections", {}) or {}
    grants = {k: bool(raw_grants.get(k, False)) for k in GRANT_NAMES}
    return privacy, grants


def check_connected_actions(decl, grants):
    """Refuse connected actions without their explicit grant (fail
    closed). With the grant but no implementation, refuse honestly too —
    this stdlib-only module performs no I/O, so a connected action can
    never be staged as working."""
    for field, grant, desc in CONNECTED_ACTIONS:
        if decl.get(field):
            if not grants.get(grant):
                raise TabsRefusal(
                    "grant_required",
                    "%s needs contract.connections.%s == true "
                    "(explicit consent only)" % (desc, grant))
            raise TabsRefusal(
                "connected_action_not_built",
                "%s is a connected action: declared in the capability "
                "contract, not implemented in this stdlib-only build "
                "(no I/O, no credentials)" % desc)


def render_smart_tabs(decl, registry_status, context=None):
    """Render the tab bar. Returns '' when the contract did not declare
    smart tabs (or explicitly opted out); raises TabsRefusal otherwise.

    registry_status: the registry's status string for feature.smart_tabs.
    Rendering is proof the registry says 'built' — the page carries
    data-smart_tabs-status="built" as the binding.
    context: the assembler's resolved contract context
    {'connections': {k: bool}, 'privacy': mode}. The privacy dial is
    stamped as data-privacy-scope; the READY surface needs no grants.
    """
    if decl is None or decl is False or not decl.get("enabled"):
        return ""  # omitted or explicit opt-out -> refuse to render tabs
    if registry_status != "built":
        raise TabsRefusal(
            "feature_not_built",
            "contract declares smart_tabs but registry status is %r "
            "(contract never activates an unbuilt capability)" % (registry_status,))
    privacy, grants = _context_parts(context)
    if privacy not in PRIVACY_SCOPES:
        raise TabsRefusal("bad_privacy_scope",
                          "privacy must be one of %s, got %r"
                          % ("/".join(PRIVACY_SCOPES), privacy))
    check_connected_actions(decl, grants)

    pages = pages_for(decl)
    aria_label = str(decl.get("aria_label") or "Your pages").strip() or "Your pages"
    if not pages:
        # graceful fallback: the tabs chrome, one current tab, never a
        # broken list and never a link the contract did not declare
        fallback_title = str(decl.get("fallback_title") or "This page").strip() \
            or "This page"
        tabs = ('<span class="smart-tab is-current" aria-current="page">%s</span>'
                % esc(fallback_title))
    else:
        active = decl.get("active_url")
        active_url = sanitize_tab_url(active, "active_url") \
            if active not in (None, "") else None
        active_norm = _norm_url(active_url) if active_url is not None else None
        bits = []
        for title, url in pages:
            cur = ' class="smart-tab is-current" aria-current="page"' \
                if active_norm is not None and _norm_url(url) == active_norm \
                else ' class="smart-tab"'
            bits.append('<a%s href="%s">%s</a>' % (cur, esc(url), esc(title)))
        tabs = "".join(bits)

    return (
        '<nav class="smart-tabs" data-feature="smart_tabs" '
        'data-smart_tabs-status="built" data-privacy-scope="%s" aria-label="%s">'
        '<div class="smart-tabs-bar" role="list">%s</div>'
        '</nav>' % (esc(privacy), esc(aria_label), tabs)
    )
