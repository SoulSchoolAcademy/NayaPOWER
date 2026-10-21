#!/usr/bin/env python3
"""feature.contacts — "Contacts" (Smart Builder feature breaker).

Capability contract (functions/registry.json):
  id: feature.contacts, version 1.0.0, status tracked in the registry.
  activated_by: contract.features.contacts — the CONTRACT flips the breaker;
  the module never hand-wires itself into a page.

Activation input (from the contract, which carries the owner's contacts):
  contract.features.contacts = {
      "enabled": true,
      "title": "Contacts (optional)",
      "sync_external": true (optional, CONNECTED — see below),
      "contacts": [{"name": "Ava Stone", "role": "Baker",
                    "link": "https://... (optional)"}, ...]
  }

Behavior (THREE-STATE interface — Shawn's product rule 21:32Z,
default-on, opt-out):
  - Explicit true (true, or {"enabled": truthy}) -> ON: contact-list HTML.
  - Explicit false (false, {"enabled": falsy}, or any other present-but-
    falsy value) -> OFF: no render, no claim, no refusal.
  - Omitted (key absent, or features not a dict) -> the ASSEMBLER's
    default-on policy decides; the module hardcodes no default.
    (Contacts is not a standard feature, so the assembler policy
    leaves it off unless the contract flips it.)
  - Declared + registry says built -> contact-list HTML.
  - Declared + registry says anything else ->
    ContactsRefusal('feature_not_built'). The contract never advertises
    a capability as operational unless the registry says it is built.
  - only_own_contacts_shown is structural: the module performs no I/O
    and renders ONLY what the contract carries — the owner's own store
    supplied those rows; nothing else is reachable from here.
  - Unsafe contact links -> ContactsRefusal('unsafe_contacts_url'),
    fail closed. Allowed: absolute http(s) URLs, mailto:, tel:.
    Rejected: javascript:, data:, vbscript:, file:, ftp:,
    protocol-relative, relative URLs, anything with control characters
    or whitespace.
  - Declared but contacts absent/empty -> graceful fallback: the empty
    state — never a blank section, never invented people.
    (Day-one: {"enabled": true} alone renders a useful section, zero errors.)
  - All names/roles are HTML-escaped; every rendered link href is verified
    against the declaration (L-2026-10-17-002 — no dead link claimed live).
  - Connections (contract["connections"]): this module performs no I/O
    and gates nothing on connections — the contact list renders when
    enabled, connections or not. Feature enabled ≠ connection available.
    mistakes private contacts for public ones.
  - READY vs CONNECTED (consent line, adopted 21:41Z) — carried in
    the capability contract as top-level "ready"/"connected" keys:
    READY (default): the contract-carried contact list — installed,
    working, no setup, no grant; renders with all connections false.
    CONNECTED: "sync_external": true -> sync external address books,
    needs contract.connections.network == true (explicit consent
    only). Without the grant -> grant_required refusal naming the
    grant; with the grant the sync is still specified-not-built in
    this stdlib-only module -> connected_action_not_built. The build
    receipt mirrors the evaluated grants; UI copy never says
    "connected" when the module is merely ready.

Stdlib only. Pure functions — same declaration -> same bytes, always.
"""
import html as htmlmod
from urllib.parse import urlparse

VERSION = "1.0.0"
FEATURE_ID = "feature.contacts"
# aliases the assembler imports
FEATURE_CONTACTS_ID = FEATURE_ID
FEATURE_CONTACTS_VERSION = VERSION

REGISTRY_KEY = "contacts"   # functions registry id minus the feature. prefix
SLOT = "contacts"           # template slot %%CONTACTS%%
EVENT = "contacts.updated"  # build-time event (F1: <breaker>.updated)

MAX_CONTACTS = 100  # a contract carrying more than this is malformed

PRIVACY_SCOPES = ("private", "network", "public")

GRANT_NAMES = ("muse", "github", "network", "nayanet")

# (declaration field, grant name, human description)
CONNECTED_ACTIONS = (
    ("sync_external", "network", "sync external address books"),
)


class ContactsRefusal(Exception):
    """Structured refusal: the contacts breaker declined to activate.

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


def sanitize_contact_link(url, field):
    """Allowlist contact links. Returns the cleaned URL; raises
    ContactsRefusal('unsafe_contacts_url') for anything hostile."""
    if not isinstance(url, str):
        raise ContactsRefusal("unsafe_contacts_url",
                              "%s: not a string (%s)" % (field, type(url).__name__))
    u = url.strip()
    if any(ord(c) < 0x20 for c in u):
        raise ContactsRefusal("unsafe_contacts_url",
                              "%s: control characters in link" % field)
    if any(c.isspace() for c in u):
        raise ContactsRefusal("unsafe_contacts_url",
                              "%s: whitespace in link" % field)
    p = urlparse(u)
    scheme = (p.scheme or "").lower()
    if scheme in ("http", "https"):
        if not p.hostname:
            raise ContactsRefusal("unsafe_contacts_url",
                                  "%s: %s link has no host" % (field, scheme))
        return u
    if scheme in ("mailto", "tel"):
        # no host on these schemes; the address itself is the payload —
        # nonempty and control/whitespace-free is the whole check
        if not p.path:
            raise ContactsRefusal("unsafe_contacts_url",
                                  "%s: empty %s address" % (field, scheme))
        return u
    reason = "relative links are not allowed" if not scheme \
        else "disallowed scheme %r" % p.scheme
    raise ContactsRefusal("unsafe_contacts_url", "%s: %s" % (field, reason))


def decl_for(contract):
    """Extract the contacts declaration from a contract.

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
      - anything else truthy -> ContactsRefusal('bad_contacts_declaration')
    """
    feats = contract.get("features") if isinstance(contract, dict) else None
    if not isinstance(feats, dict):
        return None  # contract-page contracts carry features as a list
    if "contacts" not in feats:
        return None
    decl = feats["contacts"]
    if decl is True:
        return {"enabled": True}
    if isinstance(decl, dict):
        return decl
    if not decl:
        return False  # explicit opt-out
    raise ContactsRefusal("bad_contacts_declaration",
                          "contract.features.contacts must be an object, true, "
                          "or false, got %s" % type(decl).__name__)


def contacts_for(decl):
    """Sanitized contact list: [(name, role, link_or_None), ...].
    Raises ContactsRefusal on malformed entries."""
    raw = decl.get("contacts")
    if raw is None:
        return []
    if not isinstance(raw, list):
        raise ContactsRefusal("bad_contacts_declaration",
                              "contacts must be a list, got %s"
                              % type(raw).__name__)
    if len(raw) > MAX_CONTACTS:
        raise ContactsRefusal("contacts_too_many",
                              "contacts carries %d entries (max %d)"
                              % (len(raw), MAX_CONTACTS))
    out = []
    for i, entry in enumerate(raw):
        field = "contacts[%d]" % i
        if not isinstance(entry, dict):
            raise ContactsRefusal("bad_contacts_declaration",
                                  "%s must be an object, got %s"
                                  % (field, type(entry).__name__))
        name = entry.get("name")
        if not isinstance(name, str) or not name.strip():
            raise ContactsRefusal("bad_contacts_declaration",
                                  "%s.name must be a non-empty string" % field)
        role = entry.get("role")
        if role is not None and not isinstance(role, str):
            raise ContactsRefusal("bad_contacts_declaration",
                                  "%s.role must be a string" % field)
        link = entry.get("link")
        link_url = sanitize_contact_link(link, field + ".link") \
            if link not in (None, "") else None
        out.append((name.strip(), (role or "").strip(), link_url))
    return out


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
                raise ContactsRefusal(
                    "grant_required",
                    "%s needs contract.connections.%s == true "
                    "(explicit consent only)" % (desc, grant))
            raise ContactsRefusal(
                "connected_action_not_built",
                "%s is a connected action: declared in the capability "
                "contract, not implemented in this stdlib-only build "
                "(no I/O, no credentials)" % desc)


def render_contacts(decl, registry_status, context=None):
    """Render the contacts list. Returns '' when the contract did not
    declare contacts (or explicitly opted out); raises ContactsRefusal
    otherwise.

    registry_status: the registry's status string for feature.contacts.
    Rendering is proof the registry says 'built' — the page carries
    data-contacts-status="built" as the binding.
    context: the assembler's resolved contract context
    {'connections': {k: bool}, 'privacy': mode}. The privacy dial is
    stamped as data-privacy-scope; the READY surface needs no grants.
    """
    if decl is None or decl is False or not decl.get("enabled"):
        return ""  # omitted or explicit opt-out -> refuse to render contacts
    if registry_status != "built":
        raise ContactsRefusal(
            "feature_not_built",
            "contract declares contacts but registry status is %r "
            "(contract never activates an unbuilt capability)" % (registry_status,))
    privacy, grants = _context_parts(context)
    if privacy not in PRIVACY_SCOPES:
        raise ContactsRefusal("bad_privacy_scope",
                              "privacy must be one of %s, got %r"
                              % ("/".join(PRIVACY_SCOPES), privacy))
    check_connected_actions(decl, grants)

    title = str(decl.get("title") or "Contacts").strip() or "Contacts"
    contacts = contacts_for(decl)
    if not contacts:
        # graceful fallback: the empty state — the section is honest that
        # no contacts arrived, and invents no people
        body = ('<p class="contacts-empty">No contacts yet — '
                'add your people and they&#8217;re one tap away.</p>')
    else:
        items = []
        for name, role, link in contacts:
            head = ('<a class="contact-name" href="%s">%s</a>'
                    % (esc(link), esc(name))) if link \
                else ('<span class="contact-name">%s</span>' % esc(name))
            sub = ('<span class="contact-role">%s</span>' % esc(role)) if role else ""
            items.append('<li class="contact">%s%s</li>' % (head, sub))
        body = '<ul class="contacts-list">%s</ul>' % "".join(items)

    return (
        '<section class="contacts" data-feature="contacts" '
        'data-contacts-status="built" data-privacy-scope="%s" aria-label="%s">'
        '<h2 class="contacts-title">%s</h2>%s</section>'
        % (esc(privacy), esc(title), esc(title), body)
    )
