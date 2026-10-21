#!/usr/bin/env python3
"""feature.space — "Smart Space" (Smart Builder feature breaker).

Capability contract (functions/registry.json):
  id: feature.space, version 1.0.0, status tracked in the registry.
  activated_by: contract.features.space — the CONTRACT flips the breaker;
  the module never hand-wires itself into a page.

Activation input (from the contract, which carries the intake's answers):
  contract.features.space = {
      "enabled": true,
      "name": "Morning Crumb Regulars",
      "description": "Gather around warm bread.",  # optional
      "visibility": "public",      # public | private | invite;
                                   # omitted -> the privacy dial decides
      "join_url": "https://...",   # optional join/invite link
      "join_mode": "link",         # link | connected (default: link)
      "member_count": 42            # optional
  }
Contract-level settings this module consumes (resolved in decl_for):
  contract["privacy"] = "private" | "network" | "public" (default "private").
      Validated; anything else -> SpaceRefusal('bad_privacy_dial'). When the
      declaration omits visibility, the dial decides: private->private,
      network->invite, public->public. An explicit visibility always wins —
      public is a legitimate first-class choice, never framed as a violation.
  contract["connections"] = {"muse":..,"github":..,"network":..,"nayanet":..}
      (default all false; missing block = all false). Malformed block ->
      SpaceRefusal('bad_connections_block').

READY vs CONNECTED (consent line, product rule 21:41Z) — two distinct
states, never conflated:
  READY (default): the space panel, and join via a declared join_url
      (a hyperlink needs no grant). Installed, working, usable immediately.
  CONNECTED (explicit consent only): join_mode "connected" — joining flows
      through the NayaNET connection. Activates ONLY on the recorded grant
      contract.connections.nayanet == true (the user's explicit opt-in).
      The grant is mirrored in the build receipt for audit. Requesting
      connected join without the grant is a structured refusal naming the
      missing grant — never a crash, never a staged join button.
The panel's copy never says "connected" when the feature is merely ready.

Behavior:
  - Not declared (or enabled falsy) -> render nothing. The page refuses
    to render a space the contract did not declare.
  - THREE-STATE (product rule 21:32Z): explicit true/false honored exactly;
    an omitted flag follows assembler default policy (opt-in today). The
    module never hardcodes an on/off default — it renders the resolved
    state the assembler hands it.
  - DAY-ONE (product rule 21:34Z): a minimal contract (no optional blocks,
    no connections, no privacy set) renders a useful panel with zero errors.
  - Declared + registry says built -> space panel: name, description,
    visibility badge, member count, and a join control.
  - join_mode "link" (default, READY): join_url -> a real anchor;
    no join_url -> honest "ask the owner" text, never a dead button.
  - join_mode "connected" (explicit opt-in, CONNECTED): the grant
    connections.nayanet is required. Absent -> SmartMailRefusal-style
    SpaceRefusal('grant_required') naming the grant. Present -> the
    declared join_url renders as the handoff link with an honest
    "Connected via NayaNET" status; none declared -> honest
    "no link published" text.
  - Declared + registry says anything else -> SpaceRefusal('feature_not_built').
    The contract never advertises a capability as operational unless the
    registry says it is built.
  - visibility == "private" -> the panel renders a members-only state and
    NEVER renders member_count or join_url, even when the contract declares
    them (private_space_stays_private — acceptance, fail closed).
  - Hostile join_url -> SpaceRefusal('unsafe_join_url'), fail closed.
    Allowed: absolute http(s) URLs only. Rejected: javascript:, data:,
    relative URLs, anything with control characters.
  - Unknown visibility / join_mode / bad member_count / bad text ->
    structured refusals, never improvised defaults that change meaning
    (except visibility, which falls back to the privacy dial, itself
    defaulting to "private" — fail closed).

Stdlib only. Pure functions — same declaration -> same bytes, always.
"""
import html as htmlmod
from urllib.parse import urlparse

VERSION = "1.0.0"
FEATURE_ID = "feature.space"
# aliases the assembler imports
FEATURE_SPACE_ID = FEATURE_ID
FEATURE_SPACE_VERSION = VERSION
FEATURE_VERSION = VERSION  # uniform interface for the assembler

VISIBILITIES = ("public", "private", "invite")
JOIN_MODES = ("link", "connected")
PRIVACY_LEVELS = ("private", "network", "public")
CONNECTION_KEYS = ("muse", "github", "network", "nayanet")
# Privacy dial -> default space visibility. "network" (visible to the
# network, not the open web) maps to invite-only: join by link, not open.
PRIVACY_TO_VISIBILITY = {"private": "private", "network": "invite",
                         "public": "public"}

MAX_NAME = 120
MAX_DESC = 500


class SpaceRefusal(Exception):
    """Structured refusal: the space breaker declined to activate.

    code: machine-readable failure class (never a transport error —
    this module performs no I/O, so every refusal is a content/contract
    failure, cf. lesson L-2026-10-16-004).
    detail: human-readable explanation for the receipt.
    """
    def __init__(self, code, detail=""):
        super().__init__("%s: %s" % (code, detail))
        self.code = code
        self.detail = detail


# Uniform interface for the assembler's additive registration block.
Refusal = SpaceRefusal


def esc(s):
    return htmlmod.escape(str(s), quote=True)


def clean_text(s, field, max_len):
    """Text fields are escaped at render; control characters and overlong
    input are refused, never silently stripped or truncated."""
    if not isinstance(s, str):
        raise SpaceRefusal("unsafe_space_text",
                           "%s: not a string (%s)" % (field, type(s).__name__))
    if any(ord(c) < 0x20 and c not in "\n\t" for c in s):
        raise SpaceRefusal("unsafe_space_text",
                           "%s: control characters in text" % field)
    if len(s) > max_len:
        raise SpaceRefusal("space_text_too_long",
                           "%s: %d chars, max %d" % (field, len(s), max_len))
    return s


def sanitize_join_url(url):
    """Allowlist join URLs: absolute http(s) only. Returns the cleaned URL,
    None when absent, raises SpaceRefusal('unsafe_join_url') otherwise —
    every href on the page is verified (lesson L-2026-10-17-002)."""
    if url is None:
        return None
    if not isinstance(url, str):
        raise SpaceRefusal("unsafe_join_url",
                           "not a string (%s)" % type(url).__name__)
    u = url.strip()
    if not u:
        return None
    if any(ord(c) < 0x20 for c in u):
        raise SpaceRefusal("unsafe_join_url", "control characters in URL")
    p = urlparse(u)
    scheme = (p.scheme or "").lower()
    if scheme not in ("http", "https"):
        reason = "relative URLs are not allowed" if not scheme \
            else "disallowed scheme %r" % p.scheme
        raise SpaceRefusal("unsafe_join_url", reason)
    if not p.hostname:
        raise SpaceRefusal("unsafe_join_url", "URL has no host")
    if any(c.isspace() for c in p.hostname):
        raise SpaceRefusal("unsafe_join_url", "whitespace in host")
    return u


def sanitize_visibility(v):
    """Validate an explicit visibility. Omitted visibility never reaches
    here — decl_for fills it from the privacy dial first."""
    if not isinstance(v, str) or v.strip().lower() not in VISIBILITIES:
        raise SpaceRefusal("bad_space_visibility",
                           "visibility must be one of %s, got %r"
                           % ("/".join(VISIBILITIES), v))
    return v.strip().lower()


def sanitize_join_mode(m):
    if m is None:
        return "link"
    if not isinstance(m, str) or m.strip().lower() not in JOIN_MODES:
        raise SpaceRefusal("bad_join_mode",
                           "join_mode must be one of %s, got %r"
                           % ("/".join(JOIN_MODES), m))
    return m.strip().lower()


def resolve_privacy(contract):
    """The privacy dial: contract['privacy'], default 'private'. Anything
    outside the fixed vocabulary is a structured refusal — fail closed."""
    p = contract.get("privacy", "private")
    if p is None:
        return "private"
    if not isinstance(p, str) or p not in PRIVACY_LEVELS:
        raise SpaceRefusal("bad_privacy_dial",
                           "contract.privacy must be one of %s, got %r"
                           % ("/".join(PRIVACY_LEVELS), p))
    return p


def resolve_connections(contract):
    """The connections block: missing block = all false. A malformed block
    is a structured refusal — the module never guesses at connectivity."""
    c = contract.get("connections", None)
    if c is None:
        return {k: False for k in CONNECTION_KEYS}
    if not isinstance(c, dict):
        raise SpaceRefusal("bad_connections_block",
                           "contract.connections must be an object, got %s"
                           % type(c).__name__)
    return {k: bool(c.get(k, False)) for k in CONNECTION_KEYS}


def sanitize_member_count(n):
    if n is None:
        return None
    if isinstance(n, bool) or not isinstance(n, int):
        raise SpaceRefusal("bad_member_count",
                           "member_count must be an integer, got %s"
                           % type(n).__name__)
    if n < 0 or n > 10 ** 9:
        raise SpaceRefusal("bad_member_count",
                           "member_count out of range: %r" % (n,))
    return n


def decl_for(contract):
    """Extract the space declaration from a contract, or None.

    Accepts the PLUMBING.md breaker convention (contract.features.space):
      - dict  -> the declaration (enabled/name/…/visibility/join_mode)
      - True  -> enabled with empty fields (private-by-default fallback)
      - falsy / absent / features-not-a-dict -> None (not declared)
      - anything else truthy -> SpaceRefusal('bad_space_declaration')

    When declared, the privacy dial fills an omitted visibility and the
    connections block is resolved; both ride the returned decl (as the
    visibility value and _connections) — render consumes them and never
    re-reads the contract.
    """
    feats = contract.get("features") if isinstance(contract, dict) else None
    if not isinstance(feats, dict):
        return None  # contract-page contracts carry features as a list
    if "space" not in feats:
        return None
    decl = feats["space"]
    if not decl:
        return None
    if decl is True:
        decl = {"enabled": True}
    if not isinstance(decl, dict):
        raise SpaceRefusal("bad_space_declaration",
                           "contract.features.space must be an object or "
                           "true, got %s" % type(decl).__name__)
    decl = dict(decl)  # copy: resolved contract-level settings ride along
    if decl.get("visibility") is None:
        # Privacy dial decides the default; explicit visibility always wins.
        decl["visibility"] = PRIVACY_TO_VISIBILITY[resolve_privacy(contract)]
    else:
        resolve_privacy(contract)  # validate the dial even when unused
    decl["_connections"] = resolve_connections(contract)
    return decl


def render_space(decl, registry_status, context=None):
    """Render the space panel.

    Returns (html, connected): html is '' when the contract did not declare
    space; connected lists the CONNECTED capabilities actually wired,
    each as {"event", "grant"} for the receipt's grant mirror.
    Raises SpaceRefusal on anything the contract must not get.

    registry_status: the registry's status string for feature.space.
    Rendering is proof the registry says 'built' — the page carries
    data-space-status="built" as the binding.

    Privacy law of this module: a private space NEVER renders member_count
    or join_url, even when declared — private_space_stays_private.
    """
    if decl is None or not decl.get("enabled"):
        return "", []  # not declared -> refuse to render a space
    if registry_status != "built":
        raise SpaceRefusal(
            "feature_not_built",
            "contract declares space but registry status is %r "
            "(contract never activates an unbuilt capability)" % (registry_status,))

    name = clean_text(str(decl.get("name") if decl.get("name") is not None
                          else "A space"), "name", MAX_NAME)
    desc = clean_text(str(decl.get("description") or ""),
                      "description", MAX_DESC)
    visibility = sanitize_visibility(decl.get("visibility"))
    join_url = sanitize_join_url(decl.get("join_url"))
    join_mode = sanitize_join_mode(decl.get("join_mode"))
    member_count = sanitize_member_count(decl.get("member_count"))
    conns = decl.get("_connections") or {}

    badge = ('<span class="breaker-badge">%s</span>'
             % esc({"public": "Public space",
                    "private": "Private space",
                    "invite": "Invite only"}[visibility]))
    desc_html = ('<p class="breaker-sub">%s</p>' % esc(desc)) if desc else ""

    if visibility == "private":
        # private_space_stays_private: member_count and join_url are
        # deliberately never rendered, even when the contract declares them.
        body = ('<p class="breaker-sub">Members gather here. Nothing inside '
                'this space is shown on this page.</p>')
        connected = []
    elif join_mode == "connected":
        # CONNECTED capability: joining flows through the NayaNET connection
        # and activates ONLY on the recorded grant. Requesting it without
        # the grant is a structured refusal naming the missing grant — the
        # consent line is a hard line, never a staged join button.
        if not conns.get("nayanet"):
            raise SpaceRefusal(
                "grant_required",
                "feature.space join is ready but not connected: it needs "
                "the grant contract.connections.nayanet "
                "(the user's explicit opt-in)")
        parts = []
        if member_count is not None:
            parts.append('<p class="breaker-sub">%d %s.</p>'
                         % (member_count,
                            "member" if member_count == 1 else "members"))
        if join_url:
            parts.append('<p class="breaker-sub">Connected via NayaNET.</p>'
                         '<a class="naya-btn" href="%s"><span class="nb-label">'
                         'Join the space</span></a>' % esc(join_url))
        else:
            parts.append('<p class="breaker-sub">NayaNET is connected — join '
                         'opens inside the Hub. No join link is published '
                         'yet.</p>')
        body = "".join(parts)
        connected = [{"event": "space.join.connected",
                      "grant": "connections.nayanet"}]
    else:
        parts = []
        if member_count is not None:
            parts.append('<p class="breaker-sub">%d %s.</p>'
                         % (member_count,
                            "member" if member_count == 1 else "members"))
        if join_url:
            cta = "Join the space" if visibility == "public" \
                else "Request an invite"
            parts.append('<a class="naya-btn" href="%s"><span class="nb-label">'
                         '%s</span></a>' % (esc(join_url), esc(cta)))
        else:
            # Honest pending state — no anchor, because an anchor that goes
            # nowhere is a dead control, and dead controls do not ship.
            parts.append('<p class="breaker-sub">Ask the owner for an invite '
                         'link — none is published yet.</p>')
        body = "".join(parts)
        connected = []  # link mode is READY: no grant, nothing to mirror

    return (
        '<section class="breaker breaker-space" data-feature="space" '
        'data-space-status="built" aria-label="%s">'
        '%s<h3 class="breaker-title">%s</h3>%s%s</section>'
        % (esc(name), badge, esc(name), desc_html, body)
    ), connected
