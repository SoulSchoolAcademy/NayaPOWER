#!/usr/bin/env python3
"""feature.broadcast — "Broadcasts" (Smart Builder feature breaker).

Capability contract (functions/registry.json):
  id: feature.broadcast, version 1.0.0, status tracked in the registry.
  activated_by: contract.features.broadcast — the CONTRACT flips the breaker;
  the module never hand-wires itself into a page.
  requires: authenticated_identity, recipient_authorization,
            message_service, delivery_receipts
  permissions: broadcast.send
  events: broadcast.sent, broadcast.failed (runtime — the message service
  fires them; the build fires nothing).

Activation input (from the contract):
  contract.features.broadcast = {
      "enabled": true,
      "authorized": true,              # REQUIRED truthy — the owner said send
      "audience": "everyone following this page",
      "channels": ["smart_mail"],      # allowlist: smart_mail | spaces | feed
      "compose_endpoint": "https://... (message service, optional)",
      "receipts_endpoint": "https://... (delivery receipts, optional)"
  }

Honest scope (the anti-spam gate):
  - A broadcast reaches real people, so the builder enforces the registry's
    recipient_authorization requirement AT BUILD TIME: the contract must
    declare "authorized": true (set by the intake only when the owner
    explicitly authorizes sending). Anything else -> BroadcastRefusal
    ('unauthorized_broadcast') — a hard, build-stopping refusal. An
    unauthorized broadcast declaration must never ship, quietly or loudly.
  - The module never sends anything (no I/O). It renders the compose card
    bound to the contract-declared compose endpoint. Sending, delivery, and
    receipts belong to the runtime message service.
  - Authorized but no compose_endpoint -> the card renders in NOT-WIRED
    state: visible, honest, no compose box. Never a dead send button
    (Shawn's function law).

Behavior (three-state, Shawn's 21:32Z default-on rule):
  - Omitted -> assembler policy (broadcast is not a standard feature,
    so omitted = off). The module never hardcodes a default.
  - Explicit false -> off: no render, no claim, and never trips the
    authorization gate.
  - Explicit true + registry built + authorized -> compose card (or the
    honest connect/not-wired states below).
  - Declared + registry says anything else -> BroadcastRefusal('feature_not_built').
  - Declared without authorized === true -> BroadcastRefusal('unauthorized_broadcast').
  - Network connection missing -> "connect your network to enable" panel,
    never a staged compose box (Shawn's 21:34Z day-one rule).
  - Bad channels/declaration -> BroadcastRefusal('bad_broadcast_declaration'),
    fail closed. Hostile endpoints -> BroadcastRefusal('unsafe_broadcast_endpoint').

Stdlib only. Pure functions — same declaration -> same bytes, always.
"""
import html as htmlmod
from urllib.parse import urlparse

VERSION = "1.0.0"
FEATURE_ID = "feature.broadcast"
# aliases the assembler imports
FEATURE_BROADCAST_ID = FEATURE_ID
FEATURE_BROADCAST_VERSION = VERSION

# The only channels a broadcast may declare. The runtime message service
# owns delivery; the builder owns the allowlist — no improvised channels.
CHANNELS = ("smart_mail", "spaces", "feed")

# Connections (Shawn's 21:34Z day-one rule), refined 21:41Z into the
# READY vs CONNECTED split (notifications: local reminders = ready;
# external delivery = connected):
#   ready     = authorized card shell: audience and channels named, honest
#               connect/not-wired states. Nothing is sent.
#   connected = composed broadcasts send through the declared message
#               service, with delivery receipts. Requires the grant below.
# Declaring compose_endpoint is an explicit CONNECTED demand (no transport
# = the notification stays BLOCKED): without the grant it is a structured
# grant_required refusal, never a silent downgrade.
NEEDS_CONNECTION = "network"
GRANT = "connections.network"
READINESS = {
    "ready": "Authorized compose card shell: audience and channels named; "
             "honest connect/not-wired states. Nothing is sent.",
    "connected": "Composed broadcasts send through the declared message "
                 "service with delivery receipts.",
    "grant": GRANT,
}


class BroadcastRefusal(Exception):
    """Structured refusal: the broadcast breaker declined to activate.

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


def clean_text(s, field):
    t = str(s or "").strip()
    if any(ord(c) < 0x20 and c not in ("\t", "\n", "\r") for c in t):
        raise BroadcastRefusal("bad_broadcast_declaration",
                               "%s: control characters in text" % field)
    return t


def sanitize_endpoint(url, field):
    """Allowlist a message-service endpoint. Absolute http(s) only."""
    if url is None:
        return None
    if not isinstance(url, str):
        raise BroadcastRefusal("unsafe_broadcast_endpoint",
                               "%s: not a string (%s)"
                               % (field, type(url).__name__))
    u = url.strip()
    if not u:
        return None
    if any(ord(c) < 0x20 for c in u):
        raise BroadcastRefusal("unsafe_broadcast_endpoint",
                               "%s: control characters in URL" % field)
    p = urlparse(u)
    scheme = (p.scheme or "").lower()
    if scheme in ("http", "https"):
        if not p.hostname:
            raise BroadcastRefusal("unsafe_broadcast_endpoint",
                                   "%s: %s URL has no host" % (field, scheme))
        if any(c.isspace() for c in p.hostname):
            raise BroadcastRefusal("unsafe_broadcast_endpoint",
                                   "%s: whitespace in host" % field)
        return u
    reason = "relative URLs are not allowed" if not scheme \
        else "disallowed scheme %r (message service must be http(s))" % p.scheme
    raise BroadcastRefusal("unsafe_broadcast_endpoint",
                           "%s: %s" % (field, reason))


def decl_for(contract):
    """Extract the broadcast declaration from a contract, or None.

    Three-state interface (Shawn's 21:32Z default-on rule):
      - features not a dict (contract-page) -> None: no breakers at all.
      - key absent -> None: OMITTED. The assembler applies its policy
        (registry-marked standard features default on); the module never
        hardcodes a default.
      - True -> {"enabled": True}: explicit ON (authorization still required
        at render — the anti-spam gate is independent of the on/off state).
      - dict -> itself: explicit; on iff decl.get("enabled") is truthy.
      - other falsy (False/None/0/"") -> {"enabled": False}: explicit OFF.
        Off renders nothing, claims nothing, and never trips the
        authorization gate.
      - other truthy -> BroadcastRefusal('bad_broadcast_declaration').
    """
    feats = contract.get("features") if isinstance(contract, dict) else None
    if not isinstance(feats, dict):
        return None  # contract-page contracts carry features as a list
    if "broadcast" not in feats:
        return None  # omitted -> assembler policy applies
    decl = feats["broadcast"]
    if decl is True:
        return {"enabled": True}
    if isinstance(decl, dict):
        return decl
    if not decl:
        return {"enabled": False}  # explicit off: no render, no claim
    raise BroadcastRefusal("bad_broadcast_declaration",
                           "contract.features.broadcast must be an object, "
                           "true, or false, got %s" % type(decl).__name__)


def granted(ctx):
    """The grant: contract.connections.network == true (strict)."""
    conns = (ctx or {}).get("connections", {}) or {}
    return conns.get(NEEDS_CONNECTION) is True


def mode_for(decl, ctx):
    """READY vs CONNECTED for this declaration: connected only when the
    contract demands live sending (a SANITIZED compose_endpoint) AND holds
    the grant. Sanitizing here keeps data-mode honest — never conflate."""
    try:
        ep = sanitize_endpoint((decl or {}).get("compose_endpoint"),
                               "compose_endpoint")
    except BroadcastRefusal:
        return "ready"
    return "connected" if (ep and granted(ctx)) else "ready"


def validated_channels(decl):
    """Channels come from the allowlist, or the declaration is refused.
    No improvised channels — a broadcast must name where it goes."""
    chans = decl.get("channels")
    if chans is None:
        return ("smart_mail",)  # the registry's intent: smart mail first
    if not isinstance(chans, (list, tuple)) or not chans:
        raise BroadcastRefusal("bad_broadcast_declaration",
                               "channels must be a non-empty list")
    out = []
    for c in chans:
        c = str(c).strip().lower()
        if c not in CHANNELS:
            raise BroadcastRefusal(
                "bad_broadcast_declaration",
                "channel %r not allowed (allowlist: %s)"
                % (c, ", ".join(CHANNELS)))
        if c not in out:
            out.append(c)
    return tuple(out)


def render_broadcast(decl, registry_status, context=None):
    """Render the broadcast compose card. Returns '' when the contract did
    not declare broadcast (omitted non-standard, explicit off, or disabled);
    raises BroadcastRefusal otherwise.

    registry_status: the registry's status string for feature.broadcast.
    context: {"connections": {...}, "privacy": ...} from the assembler.

    Connections: without the network connection the card renders an honest
    "connect to enable" panel — enabled != available, never staged.
    """
    if decl is None or not decl.get("enabled"):
        return ""  # not declared / explicit off -> no render, no claim
    if registry_status != "built":
        raise BroadcastRefusal(
            "feature_not_built",
            "contract declares broadcast but registry status is %r "
            "(contract never activates an unbuilt capability)"
            % (registry_status,))
    # The anti-spam gate: recipient_authorization, enforced at build time.
    # Only the boolean True authorizes — the intake sets it when the owner
    # explicitly says send. Strings ("true", "yes"), 1, or anything else
    # are NOT authorization. Fail closed, always.
    if decl.get("authorized") is not True:
        raise BroadcastRefusal(
            "unauthorized_broadcast",
            "contract declares broadcast but the owner has not authorized "
            "sending (authorized is not boolean true) — an unauthorized "
            "broadcast declaration never ships")

    conns = (context or {}).get("connections", {}) or {}
    channels = validated_channels(decl)
    audience = clean_text(decl.get("audience"), "audience") \
        or "everyone related to this page"
    compose = sanitize_endpoint(decl.get("compose_endpoint"), "compose_endpoint")

    if compose and not granted(context):
        # Explicit CONNECTED demand (transport declared) without the
        # grant: structured refusal naming the grant. No transport without
        # its grant — the notification stays BLOCKED, honestly.
        raise BroadcastRefusal(
            "grant_required",
            "sending broadcasts (connected) requires grant %s — connect "
            "your network, or remove compose_endpoint to render the ready "
            "shell" % GRANT)

    if not granted(context):
        # Honest, not staged: no compose box until the network is connected.
        chips = "".join('<span class="bcast-chip">%s</span>' % esc(c)
                        for c in channels)
        return (
            '<section class="bcast-card bcast-card-connect" data-feature="broadcast" '
            'data-broadcast-status="built" data-mode="ready" '
            'data-grant="connections.network" data-needs-connection="network" '
            'data-channels="%s">'
            '<div class="bcast-head"><h2>Broadcasts</h2>'
            '<p class="bcast-audience">To %s — the owner authorized this.</p>'
            '<div class="bcast-channels">%s</div></div>'
            '<p class="bcast-connect">Broadcasts reach your network — '
            '<b>connect your network to enable sending.</b> Nothing here is '
            'staged: the compose box appears once it\u2019s connected.</p>'
            '</section>' % (esc(",".join(channels)), esc(audience), chips)
        )

    compose = sanitize_endpoint(decl.get("compose_endpoint"), "compose_endpoint")
    receipts = sanitize_endpoint(decl.get("receipts_endpoint"), "receipts_endpoint")

    chips = "".join('<span class="bcast-chip">%s</span>' % esc(c)
                    for c in channels)
    head = (
        '<div class="bcast-head"><h2>Broadcasts</h2>'
        '<p class="bcast-audience">To %s — the owner authorized this.</p>'
        '<div class="bcast-channels">%s</div></div>' % (esc(audience), chips)
    )
    receipt_shell = (
        '<div class="bcast-receipts"%s>'
        '<h3>Delivery receipts</h3>'
        '<p class="fine">Sent and failed broadcasts land here.</p>'
        '<ul class="bcast-receipt-list"></ul></div>'
        % (' data-receipts-endpoint="%s"' % esc(receipts) if receipts else "")
    )

    if compose:
        # Wired: a real compose form posting to the contract-declared
        # message service. broadcast.send is the service's permission;
        # this is its contract binding.
        body = (
            '<form class="bcast-form" method="post" action="%s">'
            '<label class="bcast-label" for="bcast-subject">Subject</label>'
            '<input id="bcast-subject" name="subject" type="text" required '
            'maxlength="140" placeholder="What\u2019s the news?">'
            '<label class="bcast-label" for="bcast-body">Message</label>'
            '<textarea id="bcast-body" name="body" required maxlength="5000" '
            'rows="4" placeholder="Write it once — it goes to %s."></textarea>'
            '<button type="submit" class="naya-btn bcast-btn">'
            '<span class="nb-label">Send broadcast</span></button></form>'
            % (esc(compose), esc(audience))
        )
        cls = "bcast-card"
        data = ('data-feature="broadcast" data-broadcast-status="built" '
                'data-mode="connected" data-grant="connections.network" '
                'data-compose-endpoint="%s" data-channels="%s"'
                % (esc(compose), esc(",".join(channels))))
    else:
        # Authorized but not wired: visible, honest, no send button.
        body = (
            '<p class="bcast-off">Broadcasts are authorized but not wired yet '
            '\u2014 the owner hasn\u2019t linked a message service. No send '
            'button appears until it\u2019s real.</p>'
        )
        cls = "bcast-card bcast-card-off"
        data = ('data-feature="broadcast" data-broadcast-status="built" '
                'data-mode="ready" data-grant="connections.network" '
                'data-channels="%s"' % esc(",".join(channels)))

    return ('<section class="%s" %s>%s%s%s</section>'
            % (cls, data, head, body, receipt_shell))
