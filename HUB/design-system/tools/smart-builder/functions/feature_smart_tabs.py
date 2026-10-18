#!/usr/bin/env python3
"""feature.smart_tabs — "Smart tabs" (Smart Builder feature breaker).

Capability contract (functions/registry.json):
  id: feature.smart_tabs, version 1.0.0, status tracked in the registry.
  activated_by: contract.features.smart_tabs — the CONTRACT flips the
  breaker; the module never hand-wires itself into a page.
  depends_on: systems.tabs
  requires: page_registry, navigation_service
  permissions: tabs.navigate (moving between the owner's pages is a
  permission question — navigation is the capability, the grant is the key)
  events: tabs.switched
  acceptance: all_owned_pages_reachable, tab_switch_tested
  connected: none — tabs are navigation, not a connection.
  ready: tabs UI, local page list (works with zero grants).

Activation input (from the contract, which carries the intake's data):
  contract.features.smart_tabs = {
      "enabled": True,
      "pages": [
          {"title": "My kitchen", "owner": "shawn",
           "address": "/pages/kitchen", "icon": "🍳"},
      ]
  }
  title: non-empty string (required — a tab without a title is a lie).
  owner: the identity id that owns the page (required — acceptance:
  all_owned_pages_reachable; a tab to a page the viewer doesn't own
  never renders — not the title, not the address, not a gated teaser).
  address: non-empty string starting with "/" (required — reachability
  needs an address; the tab links it).
  icon: optional string.

Behavior:
  - Not declared (or enabled falsy) -> render nothing. The page refuses
    to render tabs the contract did not declare.
  - Declared + registry says anything else -> TabsRefusal(
    'feature_not_built'). The contract never advertises a capability as
    operational unless the registry says it is built.
  - all_owned_pages_reachable: the tabs bar renders ONLY pages whose
    owner matches context['identity']['id']. Every rendered page carries
    a real href (reachable). Without an identity, no page tabs render
    at all (honest sign-in line) — tabs belong to an identity.
  - Navigation is a permission question: with the tabs.navigate
    permission granted the viewer's own pages render as a working tabs
    bar; without it an honest gated block names the permission in human
    words. Never a dead bar, never silent.
  - Empty (declared, zero own pages) -> an honest empty line, never an
    empty bar, never a crash, never a fake tab (tab_switch_tested).
  - Malformed pages (missing/blank title, bad owner, missing or
    non-rooted address, wrong shape, bad icon) -> TabsRefusal(
    'bad_page'), never silently dropped.
  - Receipt hooks -> the tabs bar carries data-receipt-events with the
    registry's own events (tabs.switched) so the runtime can persist
    receipts. A claim of "switched" without a receipt is a hope.

Judgment, named: the tab RENDER is a permission question
(tabs.navigate), checked after ownership — a bar that leaks another
identity's page under a granted permission is a bar that cannot be
trusted. There is no connected action for tabs (connected: [] in the
registry) — navigation is not a connection, so the consent word is
always "ready": wired and ready, no grant gates the bar itself.

Acceptance (registry: all_owned_pages_reachable, tab_switch_tested) is
exercised in functions/tests/test_feature_smart_tabs.py.

Stdlib only. Pure functions — same declaration + same context -> same
bytes, always.
"""
import html as htmlmod

VERSION = "1.0.0"
FEATURE_ID = "feature.smart_tabs"
# aliases the assembler imports
FEATURE_SMART_TABS_ID = FEATURE_ID
FEATURE_SMART_TABS_VERSION = VERSION

# Navigating between the owner's pages is a permission question.
NAVIGATE_PERMISSION = "tabs.navigate"
NAVIGATE_PERMISSION_HUMAN = "navigate between your pages via smart tabs"


class TabsRefusal(Exception):
    """Structured refusal: the smart tabs breaker declined to activate.

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


def _nonempty_str(value):
    return isinstance(value, str) and bool(value.strip())


def sanitize_page(page):
    """Validate one page. Returns {'title', 'owner', 'address', 'icon'}.
    Raises TabsRefusal('bad_page') for anything malformed — a tabs bar
    that swallows a bad page silently is a bar that cannot be trusted."""
    if not isinstance(page, dict):
        raise TabsRefusal(
            "bad_page",
            "each page must be an object, got %s" % type(page).__name__)
    title = page.get("title")
    if not _nonempty_str(title):
        raise TabsRefusal(
            "bad_page",
            "page needs a non-empty string title, got %r" % (title,))
    owner = page.get("owner")
    if not _nonempty_str(owner):
        raise TabsRefusal(
            "bad_page",
            "page needs a non-empty string owner (identity id), got %r"
            % (owner,))
    address = page.get("address")
    if not _nonempty_str(address) or not address.strip().startswith("/"):
        raise TabsRefusal(
            "bad_page",
            "page needs a rooted address (starting with '/'), got %r"
            % (address,))

    def _opt(key):
        value = page.get(key)
        if value is None:
            return ""
        if not isinstance(value, str):
            raise TabsRefusal(
                "bad_page",
                "page %s must be a string, got %s"
                % (key, type(value).__name__))
        return value.strip()

    return {"title": title.strip(), "owner": owner.strip(),
            "address": address.strip(), "icon": _opt("icon")}


def decl_for(contract):
    """Extract the smart-tabs declaration from a contract, or None.

    Accepts the PLUMBING.md breaker convention
    (contract.features.smart_tabs):
      - dict  -> the declaration (task shape: enabled/pages)
      - True  -> enabled with empty fields
      - falsy / absent / features-not-a-dict -> None (not declared)
      - anything else truthy -> TabsRefusal('bad_smart_tabs_declaration')
    """
    feats = contract.get("features") if isinstance(contract, dict) else None
    if not isinstance(feats, dict):
        return None  # contract-page contracts carry features as a list
    if "smart_tabs" not in feats:
        return None
    decl = feats["smart_tabs"]
    if not decl:
        return None
    if decl is True:
        return {"enabled": True}
    if isinstance(decl, dict):
        return decl
    raise TabsRefusal(
        "bad_smart_tabs_declaration",
        "contract.features.smart_tabs must be an object or true, "
        "got %s" % type(decl).__name__)


def _viewer_id(context):
    """The signed-in viewer's identity id, or None. No identity means no
    personal pages render — fail closed on other people's pages."""
    ctx = context or {}
    ident = ctx.get("identity") or {}
    ident_id = ident.get("id")
    return ident_id if _nonempty_str(ident_id) else None


def can_navigate(context):
    """Evaluate the tabs navigation authorization.

    Returns (allowed, missing). allowed is True only when the
    tabs.navigate permission was granted. Navigation between the owner's
    pages is a permission question — the tab bar renders nothing working
    until the grant names it in human words.
    """
    missing = []
    ctx = context or {}
    granted = list(ctx.get("granted_permissions") or [])
    if NAVIGATE_PERMISSION not in granted:
        missing.append(NAVIGATE_PERMISSION_HUMAN)
    return (len(missing) == 0, missing)


def _tab_html(page):
    """Render one owned page's tab. The caller guarantees ownership —
    this function never decides who may see what."""
    icon = ('<span class="tab-icon">%s</span>' % esc(page["icon"])
            if page["icon"] else "")
    return ('<a class="smart-tab" href="%s" data-tab data-owner="%s" '
            'data-page-title="%s">%s<span class="tab-title">%s</span></a>'
            % (esc(page["address"]), esc(page["owner"]),
               esc(page["title"]), icon, esc(page["title"])))


def render_smart_tabs(decl, registry_status, context=None):
    """Render the smart tabs bar. Returns '' when the contract did not
    declare smart tabs; raises TabsRefusal otherwise.

    registry_status: the registry's status string for feature.smart_tabs.
    Rendering is proof the registry says 'built' — the bar carries
    data-tabs-status="built" as the binding.
    context: resolved contract context {'connections': {...}, 'privacy': ...,
    'granted_permissions': [...], 'available': [...], 'identity': {'id': ...}}.
    """
    if decl is None or not decl.get("enabled"):
        return ""  # not declared -> refuse to render tabs
    if registry_status != "built":
        raise TabsRefusal(
            "feature_not_built",
            "contract declares smart tabs but registry status is %r "
            "(contract never activates an unbuilt capability)"
            % (registry_status,))

    pages = [sanitize_page(p) for p in (decl.get("pages") or [])]
    viewer = _viewer_id(context)
    if viewer is None:
        # No identity: no personal pages render, ever. The bar stays
        # honest about why.
        return (
            '<nav class="smart-tabs" data-feature="smart_tabs" '
            'data-tabs-status="built" data-consent="ready">'
            '<p class="smart-tabs-no-identity">Sign in to reach your pages '
            '— tabs belong to an identity, and no identity is signed in '
            'on this page.</p>'
            '</nav>')

    own = [p for p in pages if p["owner"] == viewer]
    navigable, _ = can_navigate(context)

    # data-consent is always "ready": tabs carry no connected action
    # (registry connected: []), so no grant ever gates the bar itself.
    bar = ('<nav class="smart-tabs" data-feature="smart_tabs" '
           'data-tabs-status="built" data-consent="ready">'
           '<div class="smart-tabs-list" data-receipt-events='
           '"tabs.switched">')
    if not own:
        bar += ('<p class="smart-tabs-empty">No pages yet — the pages you '
                'create land here, one tap away.</p>')
    elif navigable:
        bar += "".join(_tab_html(p) for p in own)
    else:
        bar += (
            '<div class="smart-tabs-navigate-gated" data-consent="ready">'
            '<p class="smart-tabs-gated-title">Your pages are ready but '
            'unreachable.</p>'
            '<p class="smart-tabs-gated-why">To move between your pages, '
            'the page needs:</p>'
            '<ul class="smart-tabs-gated-list">'
            '<li>navigate between your pages via smart tabs</li></ul>'
            '<p class="smart-tabs-gated-note">Nothing is wired until you '
            'grant it.</p>'
            '</div>')
    return bar + '</div></nav>'
