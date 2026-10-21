#!/usr/bin/env python3
"""feature.smart_list — "Smart lists" (Smart Builder feature breaker).

Capability contract (functions/registry.json):
  id: feature.smart_list, version 1.0.0, status tracked in the registry.
  activated_by: contract.features.smart_list — the CONTRACT flips the breaker;
  the module never hand-wires itself into a page.
  standard: true — a STANDARD FEATURE (Shawn's 21:32Z rule): on by default,
  opt-out. The intake ships it checked; the user unchecks to remove.
  requires: authenticated_identity
  permissions: lists.edit
  events: smart_list.wired (build — the list is wired here),
          lists.item.added, lists.item.removed (runtime)

Activation input (from the contract):
  contract.features.smart_list = {
      "enabled": true,
      "title": "Reading list",        # optional, default "Smart list"
      "kind": "notes",                # notes|contacts|topics|posts|links|tasks
      "items": [                      # optional; the contract's data
          {"label": "Sourdough 101", "detail": "Ch. 3 — hydration",
           "url": "https://..."},
      ],
      "manage_endpoint": "https://... (list service, optional)",
      "empty_message": "No notes yet."  # optional
  }

Cross-cutting (Shawn's rule): a smart list organizes ANYTHING — notes,
contacts, topics, posts — and LAYERS INTO every template. It is never a
standalone page.

Privacy dial (Shawn's 21:34Z rule): contract["privacy"] =
"private"|"network"|"public" (default "private"). The list's visibility
follows the dial: rendered as data-visibility plus an honest badge.
Public = legitimate.

Connections: smart_list needs none — it organizes the contract's own
data and works day one with zero connections.

Behavior (three-state):
  - Omitted -> assembler policy: STANDARD, so omitted = ON. The module
    never hardcodes this; the registry's "standard": true drives it.
  - Explicit false -> off: no render, no claim.
  - Explicit true (or policy-on) + registry built -> the list.
  - Empty items -> honest empty state, never a blank hole.
  - manage_endpoint declared -> working add form + remove buttons (real
    POSTs to the declared list service) — the CONNECTED path, requiring
    grant connections.nayanet; without it, grant_required refuses (never
    a silent downgrade). Absent -> read-only READY list.
    Never a dead control (Shawn's function law).
  - Bad kind/items/endpoint/privacy -> SmartListRefusal, fail closed.
    Hostile item URLs -> SmartListRefusal('unsafe_list_url').

Stdlib only. Pure functions — same declaration -> same bytes, always.
"""
import html as htmlmod
from urllib.parse import urlparse

VERSION = "1.0.0"
FEATURE_ID = "feature.smart_list"
# aliases the assembler imports
FEATURE_SMART_LIST_ID = FEATURE_ID
FEATURE_SMART_LIST_VERSION = VERSION
# Build event recorded in the manifest receipt when the list wires.
SMART_LIST_WIRED_EVENT = "smart_list.wired"

# Cross-cutting kinds a smart list may organize. The allowlist keeps
# rendering sane; the contract names the kind, the module never invents one.
KINDS = ("notes", "contacts", "topics", "posts", "links", "tasks")
DEFAULT_KIND = "notes"
# Privacy dial values (Shawn's 21:34Z rule). Default: private.
PRIVACY_LEVELS = ("private", "network", "public")
DEFAULT_PRIVACY = "private"
# Fail-closed bound: a contract cannot smuggle an unbounded page.
MAX_ITEMS = 500

# Connections: smart_list needs none for READY (organize local). Refined
# 21:41Z into the READY vs CONNECTED split:
#   ready     = organize local: the contract's items render; read-only
#               without a list service. Works with zero connections.
#   connected = sync/share through the declared list service (add/remove
#               wired); visibility follows the privacy dial. Requires the
#               grant below.
# Declaring manage_endpoint is an explicit CONNECTED demand (sync/share):
# without the grant it is a structured grant_required refusal, never a
# silent downgrade.
GRANT = "connections.nayanet"
READINESS = {
    "ready": "Organize local: the contract's items render; read-only "
             "without a list service. Works with zero connections.",
    "connected": "List syncs/shares through the declared list service "
                 "(add/remove wired); visibility follows the privacy dial.",
    "grant": GRANT,
}


class SmartListRefusal(Exception):
    """Structured refusal: the smart-list breaker declined to activate.

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
        raise SmartListRefusal("bad_smart_list_declaration",
                               "%s: control characters in text" % field)
    return t


def sanitize_url(url, field):
    """Allowlist item/manage URLs. Absolute http(s) only."""
    if url is None:
        return None
    if not isinstance(url, str):
        raise SmartListRefusal("unsafe_list_url",
                               "%s: not a string (%s)"
                               % (field, type(url).__name__))
    u = url.strip()
    if not u:
        return None
    if any(ord(c) < 0x20 for c in u):
        raise SmartListRefusal("unsafe_list_url",
                               "%s: control characters in URL" % field)
    p = urlparse(u)
    scheme = (p.scheme or "").lower()
    if scheme in ("http", "https"):
        if not p.hostname:
            raise SmartListRefusal("unsafe_list_url",
                                   "%s: %s URL has no host" % (field, scheme))
        if any(c.isspace() for c in p.hostname):
            raise SmartListRefusal("unsafe_list_url",
                                   "%s: whitespace in host" % field)
        return u
    reason = "relative URLs are not allowed" if not scheme \
        else "disallowed scheme %r (must be http(s))" % p.scheme
    raise SmartListRefusal("unsafe_list_url", "%s: %s" % (field, reason))


def decl_for(contract):
    """Extract the smart_list declaration from a contract, or None.

    Three-state interface (Shawn's 21:32Z default-on rule):
      - features not a dict (contract-page) -> None: no breakers at all.
      - key absent -> None: OMITTED. The assembler applies its policy —
        smart_list is registry-marked standard, so omitted = ON. The
        module never hardcodes the default.
      - True -> {"enabled": True}: explicit ON.
      - dict -> itself: explicit; on iff decl.get("enabled") is truthy.
      - other falsy (False/None/0/"") -> {"enabled": False}: explicit OFF
        (opt-out). Off renders nothing and claims nothing.
      - other truthy -> SmartListRefusal('bad_smart_list_declaration').
    """
    feats = contract.get("features") if isinstance(contract, dict) else None
    if not isinstance(feats, dict):
        return None  # contract-page contracts carry features as a list
    if "smart_list" not in feats:
        return None  # omitted -> assembler policy (standard = default on)
    decl = feats["smart_list"]
    if decl is True:
        return {"enabled": True}
    if isinstance(decl, dict):
        return decl
    if not decl:
        return {"enabled": False}  # explicit opt-out: no render, no claim
    raise SmartListRefusal("bad_smart_list_declaration",
                           "contract.features.smart_list must be an object, "
                           "true, or false, got %s" % type(decl).__name__)


def validated_kind(decl):
    kind = str(decl.get("kind") or "").strip().lower() or DEFAULT_KIND
    if kind not in KINDS:
        raise SmartListRefusal(
            "bad_smart_list_declaration",
            "kind must be one of %s, got %r" % ("/".join(KINDS),
                                                decl.get("kind")))
    return kind


def validated_items(decl):
    """The contract's list data, validated item by item. Fail closed:
    one bad item refuses the list — never silently drop owner's data."""
    items = decl.get("items")
    if items is None:
        return []
    if not isinstance(items, (list, tuple)):
        raise SmartListRefusal("bad_smart_list_declaration",
                               "items must be a list")
    if len(items) > MAX_ITEMS:
        raise SmartListRefusal("bad_smart_list_declaration",
                               "too many items (%d > %d)"
                               % (len(items), MAX_ITEMS))
    out = []
    for i, it in enumerate(items):
        if not isinstance(it, dict):
            raise SmartListRefusal(
                "bad_smart_list_declaration",
                "items[%d] must be an object" % i)
        label = clean_text(it.get("label"), "items[%d].label" % i)
        if not label:
            raise SmartListRefusal(
                "bad_smart_list_declaration",
                "items[%d].label is required" % i)
        detail = clean_text(it.get("detail"), "items[%d].detail" % i)
        url = sanitize_url(it.get("url"), "items[%d].url" % i)
        out.append({"label": label, "detail": detail, "url": url})
    return out


def granted(ctx):
    """The grant for sync/share: contract.connections.nayanet == true."""
    conns = (ctx or {}).get("connections", {}) or {}
    return conns.get(GRANT.split(".", 1)[1]) is True


def mode_for(decl, ctx):
    """READY vs CONNECTED for this declaration: connected only when the
    contract demands sync/share (a SANITIZED manage_endpoint) AND holds
    the grant. Sanitizing here keeps data-mode honest — never conflate."""
    try:
        ep = sanitize_url((decl or {}).get("manage_endpoint"),
                          "manage_endpoint")
    except SmartListRefusal:
        return "ready"
    return "connected" if (ep and granted(ctx)) else "ready"


def visibility_for(ctx):
    """The privacy dial (Shawn's 21:34Z rule): private|network|public,
    default private. An invalid dial is a contract error — fail closed,
    exactly where the visibility claim is made."""
    privacy = ((ctx or {}).get("privacy") or DEFAULT_PRIVACY)
    privacy = str(privacy).strip().lower()
    if privacy not in PRIVACY_LEVELS:
        raise SmartListRefusal(
            "bad_smart_list_declaration",
            "contract.privacy must be one of %s, got %r"
            % ("/".join(PRIVACY_LEVELS), (ctx or {}).get("privacy")))
    return privacy


VISIBILITY_COPY = {
    "private": ("Private", "Only you can see this list."),
    "network": ("Network", "Your NayaNET network can see this list."),
    "public": ("Public", "Anyone can see this list."),
}


def render_smart_list(decl, registry_status, context=None):
    """Render the smart list. Returns '' when the contract opted out
    (explicit false) or disabled; raises SmartListRefusal otherwise.

    registry_status: the registry's status string for feature.smart_list.
    context: {"connections": {...}, "privacy": ...} from the assembler.
    """
    if decl is None or not decl.get("enabled"):
        return ""  # explicit off / disabled -> no render, no claim
    if registry_status != "built":
        raise SmartListRefusal(
            "feature_not_built",
            "contract declares smart_list but registry status is %r "
            "(contract never activates an unbuilt capability)"
            % (registry_status,))

    kind = validated_kind(decl)
    items = validated_items(decl)
    visibility = visibility_for(context)
    title = clean_text(decl.get("title"), "title") or "Smart list"
    endpoint = sanitize_url(decl.get("manage_endpoint"), "manage_endpoint")

    if endpoint and not granted(context):
        # Explicit CONNECTED demand (sync/share) without the grant:
        # structured refusal naming the grant. The local list still
        # works — drop the endpoint or connect NayaNET.
        raise SmartListRefusal(
            "grant_required",
            "list sync/share (connected) requires grant %s — connect "
            "NayaNET, or remove manage_endpoint to render the ready "
            "local list" % GRANT)

    empty_message = clean_text(decl.get("empty_message"), "empty_message") \
        or ("No %s yet." % kind)
    mode = "connected" if endpoint else "ready"

    vis_label, vis_note = VISIBILITY_COPY[visibility]
    head = (
        '<div class="slist-head"><h2>%s</h2>'
        '<span class="slist-visibility slist-vis-%s" title="%s">%s</span></div>'
        % (esc(title), esc(visibility), esc(vis_note), esc(vis_label))
    )

    if items:
        rows = []
        for it in items:
            if it["url"]:
                label = '<a class="slist-link" href="%s">%s</a>' % (
                    esc(it["url"]), esc(it["label"]))
            else:
                label = '<span class="slist-label">%s</span>' % esc(it["label"])
            detail = ('<p class="slist-detail">%s</p>' % esc(it["detail"])
                      if it["detail"] else "")
            if endpoint:
                remove = (
                    '<form class="slist-remove" method="post" action="%s/remove">'
                    '<input type="hidden" name="label" value="%s">'
                    '<button type="submit" class="slist-rm" aria-label="Remove %s">'
                    '\u00d7</button></form>'
                    % (esc(endpoint.rstrip("/")), esc(it["label"]),
                       esc(it["label"]))
                )
            else:
                remove = ""
            rows.append('<li class="slist-item">%s%s%s</li>'
                        % (label, detail, remove))
        body = '<ul class="slist-items">%s</ul>' % "".join(rows)
    else:
        # Empty is honest, never a blank hole.
        body = '<p class="slist-empty">%s</p>' % esc(empty_message)

    if endpoint:
        # Wired: a real add form posting to the declared list service.
        # lists.edit is the service's permission; this is its binding.
        add = (
            '<form class="slist-add" method="post" action="%s/items">'
            '<label class="slist-add-label" for="slist-new">Add to this list</label>'
            '<div class="slist-add-row">'
            '<input id="slist-new" name="label" type="text" required maxlength="140" '
            'placeholder="New %s...">'
            '<button type="submit" class="naya-btn slist-add-btn">'
            '<span class="nb-label">Add</span></button></div></form>'
            % (esc(endpoint.rstrip("/")), esc(kind))
        )
    else:
        add = ""  # no endpoint -> read-only list. Never a dead control.

    return (
        '<section class="smart-list" data-feature="smart_list" '
        'data-smart-list-status="built" data-mode="%s" data-grant="%s" '
        'data-kind="%s" data-visibility="%s">'
        '%s%s%s</section>'
        % (mode, esc(GRANT), esc(kind), esc(visibility), head, body, add)
    )
