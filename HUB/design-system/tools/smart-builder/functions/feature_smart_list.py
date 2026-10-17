#!/usr/bin/env python3
"""feature.smart_list — "Smart Lists" (Smart Builder feature breaker).

Capability contract (functions/registry.json):
  id: feature.smart_list, version 1.0.0, status tracked in the registry.
  activated_by: contract.features.smart_list — the CONTRACT flips the breaker;
  the module never hand-wires itself into a page.

Activation input (from the contract, which carries the intake's data):
  contract.features.smart_list = {
      "enabled": True,
      "lists": [
          {"name": "Reading", "visibility": "network",  # private default
           "items": [{"type": "note", "id": "n1", "title": "First note"},
                     {"type": "contact", "id": "c2", "title": "Bo"}]},
      ]
  }
  visibility: 'private' | 'network' | 'public', default 'private'.

Behavior:
  - Not declared (or enabled falsy) -> render nothing. The page refuses
    to render lists the contract did not declare.
  - Declared + registry says built -> the lists panel: list views with
    items of ANY permitted type (READY — works with zero grants: organizing
    is a local act), add-to-list UI, plus the share action. Share is a
    CONNECTED action: it renders as a live share button ONLY when the
    share authorization holds — list.share granted AND the network
    connection ON — otherwise an honest gated block naming exactly what
    is missing in human words. Never a dead button, never silent.
  - Declared + registry says anything else -> SmartListRefusal('feature_not_built').
    The contract never advertises a capability as operational unless the
    registry says it is built.
  - Private lists stay private: a private list renders NO share affordance
    at all — a "Private — never shared" line stands in its place. Sharing
    a private list is not a gated state, it is an absent one.
  - Unpermitted object types -> SmartListRefusal('unpermitted_object').
    Lists organize notes, contacts, topics, posts — the registry's intent
    ("the cross-cutting way to organize anything"). Anything else is
    refused, never silently dropped.
  - Receipt hooks -> the lists block carries data-receipt-events with the
    registry's own events (list.created, list.item_added) so the runtime
    can persist receipts. A claim of "shared" without a receipt is a hope.

Judgment, named: page-level privacy (context['privacy']) stays
informational — the list's own visibility (private/network/public) is
the finer, per-list control and governs sharing, mirroring how mail's
module treats page privacy. A private page with a public list shares;
a public page with a private list never shares.

Acceptance (registry: organizes_any_permitted_object,
private_lists_stay_private, share_flow_tested) is exercised in
functions/tests/test_feature_smart_list.py.

Stdlib only. Pure functions — same declaration + same context -> same
bytes, always.
"""
import html as htmlmod

VERSION = "1.0.0"
FEATURE_ID = "feature.smart_list"
# aliases the assembler imports
FEATURE_SMART_LIST_ID = FEATURE_ID
FEATURE_SMART_LIST_VERSION = VERSION

# The registry's intent: lists organize notes, contacts, topics, posts.
# Anything else is refused — never silently dropped.
PERMITTED_TYPES = ("note", "contact", "topic", "post")

# The connected share action fires only on this recorded grant
# (strict boolean — the consent-line refinement: grant = True, not truthy).
SHARE_GRANT = "network"

VISIBILITIES = ("private", "network", "public")

# Human words for share-gate reasons, so the gated block speaks plainly.
GRANT_WORDS = {
    "permission": "your permission to share lists with others",
    "network": "the network connection switched on for this page",
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


def sanitize_item(item):
    """Validate one list item. Returns {'type', 'id', 'title'}.
    Raises SmartListRefusal('unpermitted_object') for anything outside
    the registry's permitted types, and for malformed items."""
    if not isinstance(item, dict):
        raise SmartListRefusal("unpermitted_object",
                               "list item must be an object, got %s"
                               % type(item).__name__)
    itype = item.get("type")
    if itype not in PERMITTED_TYPES:
        raise SmartListRefusal("unpermitted_object",
                               "lists organize notes, contacts, topics and "
                               "posts — refusing object of type %r"
                               % (itype,))
    iid = item.get("id")
    if not isinstance(iid, str) or not iid.strip():
        raise SmartListRefusal("unpermitted_object",
                               "list item needs a non-empty string id, got %r"
                               % (iid,))
    return {"type": itype, "id": iid.strip(),
            "title": str(item.get("title") or "(untitled)")}


def sanitize_list(lst):
    """Validate one list. Returns {'name', 'visibility', 'items'}.
    Raises SmartListRefusal on bad visibility or bad items."""
    if not isinstance(lst, dict):
        raise SmartListRefusal("bad_smart_list_declaration",
                               "each list must be an object, got %s"
                               % type(lst).__name__)
    vis = lst.get("visibility") or "private"
    if vis not in VISIBILITIES:
        raise SmartListRefusal("bad_list_visibility",
                               "list visibility must be one of %s, got %r"
                               % (list(VISIBILITIES), vis))
    items = lst.get("items") or []
    if not isinstance(items, list):
        raise SmartListRefusal("bad_smart_list_declaration",
                               "list items must be a list, got %s"
                               % type(items).__name__)
    return {"name": str(lst.get("name") or "(unnamed list)"),
            "visibility": vis,
            "items": [sanitize_item(i) for i in items]}


def decl_for(contract):
    """Extract the smart-list declaration from a contract, or None.

    Accepts the PLUMBING.md breaker convention
    (contract.features.smart_list):
      - dict  -> the declaration (task shape: enabled/lists)
      - True  -> enabled with empty fields
      - falsy / absent / features-not-a-dict -> None (not declared)
      - anything else truthy -> SmartListRefusal('bad_smart_list_declaration')
    """
    feats = contract.get("features") if isinstance(contract, dict) else None
    if not isinstance(feats, dict):
        return None  # contract-page contracts carry features as a list
    if "smart_list" not in feats:
        return None
    decl = feats["smart_list"]
    if not decl:
        return None
    if decl is True:
        return {"enabled": True}
    if isinstance(decl, dict):
        return decl
    raise SmartListRefusal("bad_smart_list_declaration",
                           "contract.features.smart_list must be an object or true, "
                           "got %s" % type(decl).__name__)


def can_share(context, lst):
    """Evaluate the share authorization for one list.

    Returns (allowed, missing). allowed is True only when the share grant
    holds: list.share granted AND the network connection strictly ON.
    Private lists are not a grant question — they never render a share
    affordance at all (private_lists_stay_private), so callers check
    visibility first; this gate answers only the authorization question.
    """
    missing = []
    ctx = context or {}
    granted = list(ctx.get("granted_permissions") or [])
    if "list.share" not in granted:
        missing.append(GRANT_WORDS["permission"])
    connections = ctx.get("connections") or {}
    if connections.get(SHARE_GRANT) is not True:
        missing.append(GRANT_WORDS["network"])
    return (len(missing) == 0, missing)


def _items_html(items):
    if not items:
        return '<p class="list-empty">No items yet — add one below.</p>'
    lis = []
    for it in items:
        lis.append(
            '<li class="list-item" data-item-type="%s" data-item-id="%s">'
            '<span class="list-item-type">%s</span>'
            '<span class="list-item-title">%s</span></li>'
            % (esc(it["type"]), esc(it["id"]),
               esc(it["type"]), esc(it["title"])))
    return '<ul class="list-items">%s</ul>' % "".join(lis)


def _share_block(allowed, missing):
    """The connected action: a live share button only when authorized,
    otherwise an honest gated block naming what is missing. The two are
    visually distinct and the verifier asserts data-consent honesty."""
    if allowed:
        return (
            '<div class="list-share" data-consent="connected" '
            'data-share-grant="network">'
            '<button type="button" class="list-share-btn">Share list</button>'
            '<div class="list-receipts" data-receipt-events='
            '"list.created list.item_added">'
            '<span class="list-receipts-note">Receipts are recorded for '
            'every share.</span></div>'
            '</div>')
    reasons = "".join("<li>%s</li>" % esc(r) for r in missing)
    return (
        '<div class="list-share list-share-gated" data-consent="ready">'
        '<p class="list-gated-title">Sharing is ready but off.</p>'
        '<p class="list-gated-why">To share this list, the page needs:</p>'
        '<ul class="list-gated-list">%s</ul>'
        '<p class="list-gated-note">Connect to enable — organizing works '
        'now, sharing waits for the grant.</p>'
        '</div>' % reasons)


def _list_html(lst, context):
    """Render one list. Private lists render NO share affordance —
    the share flow does not exist for them (acceptance:
    private_lists_stay_private)."""
    vis = lst["visibility"]
    badge = '<span class="list-visibility list-visibility-%s">%s</span>' \
        % (esc(vis), esc(vis))
    if vis == "private":
        share = ('<p class="list-private-note">Private — stays on this page, '
                 'never shared.</p>')
    else:
        allowed, missing = can_share(context, lst)
        share = _share_block(allowed, missing)
    return (
        '<section class="smart-list-list" data-visibility="%s">'
        '<h3 class="list-name">%s</h3>%s'
        '%s'
        '<div class="list-add"><h4>Add to list</h4>'
        '<form class="list-add-form" onsubmit="return false">'
        '<label>Type<select name="type">%s</select></label>'
        '<label>Title<input type="text" name="title"></label>'
        '<button type="submit" class="list-add-btn">Add</button>'
        '</form></div>'
        '%s'
        '</section>'
        % (esc(vis), esc(lst["name"]), badge, _items_html(lst["items"]),
           "".join('<option value="%s">%s</option>' % (t, t)
                   for t in PERMITTED_TYPES),
           share)
    )


def render_smart_list(decl, registry_status, context=None):
    """Render the Smart Lists panel. Returns '' when the contract did not
    declare smart_list; raises SmartListRefusal otherwise.

    registry_status: the registry's status string for feature.smart_list.
    Rendering is proof the registry says 'built' — the page carries
    data-list-status="built" as the binding.
    context: resolved contract context {'connections': {...}, 'privacy': ...,
    'granted_permissions': [...], 'available': [...], 'identity': {...}}.
    """
    if decl is None or not decl.get("enabled"):
        return ""  # not declared -> refuse to render lists
    if registry_status != "built":
        raise SmartListRefusal(
            "feature_not_built",
            "contract declares smart_list but registry status is %r "
            "(contract never activates an unbuilt capability)" % (registry_status,))

    lists = [sanitize_list(l) for l in (decl.get("lists") or [])]
    # data-consent on the panel mirrors the assembler contract: "connected"
    # ONLY when a grant-active share affordance renders; else "ready".
    any_live_share = any(
        l["visibility"] != "private" and can_share(context, l)[0]
        for l in lists)
    consent_word = "connected" if any_live_share else "ready"
    return (
        '<section class="smart-lists" data-feature="smart_list" '
        'data-list-status="built" data-consent="%s">'
        '<h2 class="lists-title">Smart Lists</h2>'
        '%s'
        '</section>'
        % (consent_word, "".join(_list_html(l, context) for l in lists))
    )
