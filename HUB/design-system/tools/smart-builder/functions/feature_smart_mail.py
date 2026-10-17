#!/usr/bin/env python3
"""feature.smart_mail — "Smart Mail" (Smart Builder feature breaker).

Capability contract (functions/registry.json):
  id: feature.smart_mail, version 1.0.0, status tracked in the registry.
  activated_by: contract.features.smart_mail — the CONTRACT flips the breaker;
  the module never hand-wires itself into a page.

Activation input (from the contract, which carries the intake's answers):
  contract.features.smart_mail = {
      "enabled": true,
      "owner_email": "hello@morning-crumb.example",  # the recipient
      "label": "Write to us",          # optional panel heading
      "prefill_subject": "Hello",      # optional
      "prefill_body": "...",           # optional
      "broadcast": true,               # optional: also offer network broadcast
      "broadcast_url": "https://..."   # broadcast endpoint (needs connection)
  }
Contract-level settings this module consumes (resolved in decl_for):
  contract["privacy"] = "private" | "network" | "public" (default "private").
      Validated; anything else -> SmartMailRefusal('bad_privacy_dial').
      Mail has no visibility dimension — the dial is validated for contract
      honesty but does not change the panel.
  contract["connections"] = {"muse":..,"github":..,"network":..,"nayanet":..}
      (default all false; missing block = all false). Malformed block ->
      SmartMailRefusal('bad_connections_block').

READY vs CONNECTED (consent line, product rule 21:41Z) — two distinct
states, never conflated:
  READY (default): compose via the visitor's mail app. Installed, working,
      usable immediately — no setup, no permission needed, zero grants.
  CONNECTED (explicit consent only): broadcast to the network. Activates
      ONLY on the recorded grant contract.connections.nayanet == true
      (the user's explicit opt-in). The grant is mirrored in the build
      receipt for audit. Requesting broadcast without the grant is a
      structured refusal naming the missing grant — never a crash, never
      a staged button that pretends to broadcast.
The panel's copy never says "connected" when the feature is merely ready.

Behavior:
  - Not declared (or enabled falsy) -> render nothing. The page refuses
    to render mail the contract did not declare.
  - THREE-STATE (product rule 21:32Z): explicit true/false honored exactly;
    an omitted flag follows assembler default policy (opt-in today). The
    module never hardcodes an on/off default — it renders the resolved
    state the assembler hands it.
  - DAY-ONE (product rule 21:34Z): a minimal contract (no optional blocks,
    no connections, no privacy set) renders a useful panel with zero errors.
  - Declared + registry says built -> mail panel. The compose control is a
    mailto: anchor built from the sanitized owner_email and prefill fields —
    a real, working control (it opens the visitor's mail app, addressed and
    prefilled). No grant needed — ready on day one.
  - Broadcast is an explicit opt-in ("broadcast": true) and a CONNECTED
    capability (grant: contract.connections.nayanet):
      - grant absent -> SmartMailRefusal('grant_required') naming
        connections.nayanet. The feature is ready but not connected; the
        build refuses rather than staging a fake broadcast.
      - grant present, no broadcast_url -> honest "endpoint not configured"
        state (the grant exists, so "connected" is accurate here).
      - grant present + broadcast_url -> a real form posting the prefill to
        the declared endpoint (sanitized, verified href), plus an honest
        "Connected via NayaNET" status line.
    The grant mirror goes in the build receipt (smart_mail.broadcast.connected).
  - Declared + registry says anything else -> SmartMailRefusal('feature_not_built').
    The contract never advertises a capability as operational unless the
    registry says it is built.
  - Hostile owner_email -> SmartMailRefusal('unsafe_owner_email'), fail closed.
    The address must be a plain deliverable-looking email: no control chars,
    no markup, no query/fragment smuggling.
  - Declared but owner_email absent -> graceful fallback: an honest
    "address not published yet" state with NO anchor — never a dead control,
    never an <a> with an empty href.
  - All rendered text is HTML-escaped; control characters in text fields are
    refused, never silently stripped.

Stdlib only. Pure functions — same declaration -> same bytes, always.
"""
import html as htmlmod
import re
from urllib.parse import quote, urlparse

VERSION = "1.0.0"
FEATURE_ID = "feature.smart_mail"
# aliases the assembler imports
FEATURE_SMART_MAIL_ID = FEATURE_ID
FEATURE_SMART_MAIL_VERSION = VERSION
FEATURE_VERSION = VERSION  # uniform interface for the assembler

# Conservative recipient check: local@domain.tld, no tricks. The mailto:
# anchor is built from this, so anything that is not plainly an address
# is refused — fail closed (cf. lesson L-2026-10-17-002: verify every href).
EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]{1,64}@[A-Za-z0-9.-]{1,253}\.[A-Za-z]{2,}$")

MAX_LABEL = 80
MAX_SUBJECT = 200
MAX_BODY = 2000

PRIVACY_LEVELS = ("private", "network", "public")
CONNECTION_KEYS = ("muse", "github", "network", "nayanet")


class SmartMailRefusal(Exception):
    """Structured refusal: the smart-mail breaker declined to activate.

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
Refusal = SmartMailRefusal


def esc(s):
    return htmlmod.escape(str(s), quote=True)


def clean_text(s, field, max_len):
    """Text fields are escaped at render; control characters are refused,
    overlong input is refused (never silently truncated)."""
    if not isinstance(s, str):
        raise SmartMailRefusal("unsafe_mail_text",
                               "%s: not a string (%s)" % (field, type(s).__name__))
    if any(ord(c) < 0x20 and c not in "\n\t" for c in s):
        raise SmartMailRefusal("unsafe_mail_text",
                               "%s: control characters in text" % field)
    if len(s) > max_len:
        raise SmartMailRefusal("mail_text_too_long",
                               "%s: %d chars, max %d" % (field, len(s), max_len))
    return s


def sanitize_email(email):
    """Allowlist recipient addresses. Returns the cleaned address, None when
    absent, raises SmartMailRefusal('unsafe_owner_email') for anything
    hostile — the mailto: href is only ever built from a validated address."""
    if email is None:
        return None
    if not isinstance(email, str):
        raise SmartMailRefusal("unsafe_owner_email",
                               "not a string (%s)" % type(email).__name__)
    e = email.strip()
    if not e:
        return None
    if (len(e) > 254 or ".." in e or e.startswith(("@", ".", "-"))
            or e.endswith((".", "-")) or not EMAIL_RE.match(e)):
        raise SmartMailRefusal("unsafe_owner_email",
                               "not a plain recipient address: %r" % e[:60])
    return e


def sanitize_broadcast_url(url):
    """Allowlist broadcast endpoints: absolute http(s) only. Returns the
    cleaned URL, None when absent, raises
    SmartMailRefusal('unsafe_broadcast_url') otherwise — the broadcast
    form posts to this endpoint, so every href is verified
    (lesson L-2026-10-17-002)."""
    if url is None:
        return None
    if not isinstance(url, str):
        raise SmartMailRefusal("unsafe_broadcast_url",
                               "not a string (%s)" % type(url).__name__)
    u = url.strip()
    if not u:
        return None
    if any(ord(c) < 0x20 for c in u):
        raise SmartMailRefusal("unsafe_broadcast_url",
                               "control characters in URL")
    p = urlparse(u)
    scheme = (p.scheme or "").lower()
    if scheme not in ("http", "https"):
        reason = "relative URLs are not allowed" if not scheme \
            else "disallowed scheme %r" % p.scheme
        raise SmartMailRefusal("unsafe_broadcast_url", reason)
    if not p.hostname:
        raise SmartMailRefusal("unsafe_broadcast_url", "URL has no host")
    if any(c.isspace() for c in p.hostname):
        raise SmartMailRefusal("unsafe_broadcast_url", "whitespace in host")
    return u


def resolve_privacy(contract):
    """The privacy dial: contract['privacy'], default 'private'. Anything
    outside the fixed vocabulary is a structured refusal — fail closed."""
    p = contract.get("privacy", "private")
    if p is None:
        return "private"
    if not isinstance(p, str) or p not in PRIVACY_LEVELS:
        raise SmartMailRefusal("bad_privacy_dial",
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
        raise SmartMailRefusal("bad_connections_block",
                               "contract.connections must be an object, got %s"
                               % type(c).__name__)
    return {k: bool(c.get(k, False)) for k in CONNECTION_KEYS}


def mailto_href(email, subject, body):
    """Build the compose href. The address is already validated; subject and
    body are percent-encoded so they cannot break out of the query."""
    params = []
    if subject:
        params.append("subject=" + quote(subject, safe=""))
    if body:
        params.append("body=" + quote(body, safe=""))
    return "mailto:" + email + ("?" + "&".join(params) if params else "")


def decl_for(contract):
    """Extract the smart_mail declaration from a contract, or None.

    Accepts the PLUMBING.md breaker convention
    (contract.features.smart_mail):
      - dict  -> the declaration (enabled/owner_email/label/…/broadcast)
      - True  -> enabled with empty fields (fallback render)
      - falsy / absent / features-not-a-dict -> None (not declared)
      - anything else truthy -> SmartMailRefusal('bad_smart_mail_declaration')

    When declared, the contract-level privacy dial and connections block are
    resolved and stashed on the returned decl (as _privacy / _connections) —
    render consumes them; the module never re-reads the contract.
    """
    feats = contract.get("features") if isinstance(contract, dict) else None
    if not isinstance(feats, dict):
        return None  # contract-page contracts carry features as a list
    if "smart_mail" not in feats:
        return None
    decl = feats["smart_mail"]
    if not decl:
        return None
    if decl is True:
        decl = {"enabled": True}
    if not isinstance(decl, dict):
        raise SmartMailRefusal("bad_smart_mail_declaration",
                               "contract.features.smart_mail must be an object "
                               "or true, got %s" % type(decl).__name__)
    decl = dict(decl)  # copy: resolved contract-level settings ride along
    decl["_privacy"] = resolve_privacy(contract)
    decl["_connections"] = resolve_connections(contract)
    return decl


def render_smart_mail(decl, registry_status, context=None):
    """Render the mail panel.

    Returns (html, connected): html is '' when the contract did not declare
    smart_mail; connected lists the CONNECTED capabilities actually wired,
    each as {"event", "grant"} for the receipt's grant mirror.
    Raises SmartMailRefusal on anything the contract must not get.

    registry_status: the registry's status string for feature.smart_mail.
    Rendering is proof the registry says 'built' — the page carries
    data-smart_mail-status="built" as the binding.
    """
    if decl is None or not decl.get("enabled"):
        return "", []  # not declared -> refuse to render mail
    if registry_status != "built":
        raise SmartMailRefusal(
            "feature_not_built",
            "contract declares smart_mail but registry status is %r "
            "(contract never activates an unbuilt capability)" % (registry_status,))

    label = clean_text(str(decl.get("label") if decl.get("label") is not None
                           else "Send mail"), "label", MAX_LABEL)
    subject = clean_text(str(decl.get("prefill_subject") or ""),
                         "prefill_subject", MAX_SUBJECT)
    body = clean_text(str(decl.get("prefill_body") or ""),
                      "prefill_body", MAX_BODY)
    email = sanitize_email(decl.get("owner_email"))

    if email:
        href = mailto_href(email, subject, body)
        action = ('<a class="naya-btn" href="%s"><span class="nb-label">'
                  'Compose mail</span></a>' % esc(href))
        sub = ('<p class="breaker-sub">Opens your mail app, addressed to %s.</p>'
               % esc(email))
    else:
        # Graceful fallback: honest pending state, no anchor at all —
        # a control that cannot address anyone is a dead control, and dead
        # controls do not ship.
        action = ""
        sub = ('<p class="breaker-sub">Mail is wired — the owner has not '
               'published an address yet.</p>')

    # Broadcast is a CONNECTED capability: it activates ONLY on the recorded
    # grant. Requesting it without the grant is a structured refusal naming
    # the missing grant — the consent line is a hard line, never a soft
    # degrade, never a staged button that pretends to broadcast.
    broadcast_html = ""
    connected = []
    if decl.get("broadcast"):
        conns = decl.get("_connections") or {}
        burl = sanitize_broadcast_url(decl.get("broadcast_url"))
        if not conns.get("nayanet"):
            raise SmartMailRefusal(
                "grant_required",
                "feature.smart_mail broadcast is ready but not connected: "
                "it needs the grant contract.connections.nayanet "
                "(the user's explicit opt-in)")
        if not burl:
            broadcast_html = ('<p class="breaker-sub">NayaNET is connected, '
                              'but no broadcast endpoint is configured.</p>')
        else:
            broadcast_html = (
                '<p class="breaker-sub">Connected via NayaNET — this '
                'broadcast goes to the network.</p>'
                '<form class="breaker-form" method="post" action="%s">'
                '<input type="hidden" name="subject" value="%s">'
                '<input type="hidden" name="body" value="%s">'
                '<button class="naya-btn" type="submit"><span class="nb-label">'
                'Broadcast to the network</span></button></form>'
                % (esc(burl), esc(subject), esc(body)))
            connected.append({"event": "smart_mail.broadcast.connected",
                              "grant": "connections.nayanet"})

    return (
        '<section class="breaker breaker-mail" data-feature="smart_mail" '
        'data-smart_mail-status="built" aria-label="%s">'
        '<h3 class="breaker-title">%s</h3>%s%s%s</section>'
        % (esc(label), esc(label), sub, action, broadcast_html)
    ), connected
