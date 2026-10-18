#!/usr/bin/env python3
"""feature.smart_bars — "Smart bars" (Smart Builder feature breaker).

Capability contract (functions/registry.json):
  id: feature.smart_bars, version 1.0.0, status tracked in the registry.
  activated_by: contract.features.smart_bars — the CONTRACT flips the
  breaker; the module never hand-wires itself into a page.
  depends_on: []
  requires: navigation_service
  permissions: bars.render (rendering navigation is a permission
  question — the bar is the capability, the grant is the key)
  events: bars.rendered
  acceptance: bars_present_on_sections, mobile_collapse_tested
  connected: none — bars are navigation chrome, not a connection.
  ready: navigation bars render (works with zero grants).

Activation input (from the contract, which carries the intake's data):
  contract.features.smart_bars = {
      "enabled": True,
      "sections": [
          {"id": "about", "title": "About", "address": "/about"},
      ]
  }
  id: non-empty string (required — the section's stable key).
  title: non-empty string (required — a link without a title is a lie).
  address: non-empty string starting with "/" (required — reachability
  needs an address; the bar links it).

Behavior:
  - Not declared (or enabled falsy) -> render nothing. The page refuses
    to render bars the contract did not declare.
  - Declared + registry says anything else -> BarsRefusal(
    'feature_not_built'). The contract never advertises a capability as
    operational unless the registry says it is built.
  - bars_present_on_sections: every declared section renders as a real
    link (href = its address). A bar that drops a section silently is a
    bar that cannot be trusted.
  - Rendering is a permission question: with the bars.render permission
    granted the sections render as a working bar; without it an honest
    gated block names the permission in human words. Never a dead bar,
    never silent.
  - Empty (declared, zero sections) -> an honest empty line, never an
    empty nav, never a crash, never a fake link (mobile_collapse_tested).
  - Malformed sections (missing/blank id, missing/blank title, missing
    or non-rooted address, wrong shape) -> BarsRefusal('bad_bar'), never
    silently dropped.
  - mobile_collapse_tested: when the section count exceeds the mobile
    threshold (5), the bar ALSO renders a collapsed mobile variant — a
    <details> block carrying every section link — so a long bar stays
    usable on a phone. 5 or fewer sections -> a single list, no collapse
    chrome. The desktop list and the mobile collapse carry the same links
    — collapse never hides a section.
  - Receipt hooks -> the bar carries data-receipt-events with the
    registry's own events (bars.rendered) so the runtime can persist
    receipts. A claim of "rendered" without a receipt is a hope.
  - No identity input: a nav bar is page chrome, not personal data — the
    bar renders for any viewer once declared and granted. (Contrast
    feature.smart_tabs, which is ownership-first because pages belong to
    identities.)

Judgment, named: the bar RENDER is a permission question
(bars.render), checked before any section renders — a bar that renders
working navigation without the grant cannot be trusted. There is no
connected action for bars (connected: [] in the registry) — navigation
is not a connection, so the consent word is always "ready": wired and
ready, no grant gates the bar itself.

Acceptance (registry: bars_present_on_sections, mobile_collapse_tested)
is exercised in functions/tests/test_feature_smart_bars.py.

Stdlib only. Pure functions — same declaration + same context -> same
bytes, always.
"""
import html as htmlmod

VERSION = "1.0.0"
FEATURE_ID = "feature.smart_bars"
# aliases the assembler imports
FEATURE_SMART_BARS_ID = FEATURE_ID
FEATURE_SMART_BARS_VERSION = VERSION

# Rendering navigation is a permission question. The human words match
# the resolver's PERMISSION_EXPLAIN['bars.render'] byte-for-byte (the
# tabs module does the same with tabs.navigate) — two surfaces, one truth.
RENDER_PERMISSION = "bars.render"
RENDER_PERMISSION_HUMAN = "render the smart navigation bars"

# Above this many sections the bar gains the collapsed mobile variant.
MOBILE_COLLAPSE_THRESHOLD = 5


class BarsRefusal(Exception):
    """Structured refusal: the smart bars breaker declined to activate.

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


def sanitize_section(section):
    """Validate one section. Returns {'id', 'title', 'address'}.
    Raises BarsRefusal('bad_bar') for anything malformed — a nav bar
    that swallows a bad section silently is a bar that cannot be
    trusted."""
    if not isinstance(section, dict):
        raise BarsRefusal(
            "bad_bar",
            "each section must be an object, got %s"
            % type(section).__name__)
    sid = section.get("id")
    if not _nonempty_str(sid):
        raise BarsRefusal(
            "bad_bar",
            "section needs a non-empty string id, got %r" % (sid,))
    title = section.get("title")
    if not _nonempty_str(title):
        raise BarsRefusal(
            "bad_bar",
            "section needs a non-empty string title, got %r" % (title,))
    address = section.get("address")
    if not _nonempty_str(address) or not address.strip().startswith("/"):
        raise BarsRefusal(
            "bad_bar",
            "section needs a rooted address (starting with '/'), got %r"
            % (address,))
    return {"id": sid.strip(), "title": title.strip(),
            "address": address.strip()}


def decl_for(contract):
    """Extract the smart-bars declaration from a contract, or None.

    Accepts the PLUMBING.md breaker convention
    (contract.features.smart_bars):
      - dict  -> the declaration (task shape: enabled/sections)
      - True  -> enabled with empty fields
      - falsy / absent / features-not-a-dict -> None (not declared)
      - anything else truthy -> BarsRefusal('bad_smart_bars_declaration')
    """
    feats = contract.get("features") if isinstance(contract, dict) else None
    if not isinstance(feats, dict):
        return None  # contract-page contracts carry features as a list
    if "smart_bars" not in feats:
        return None
    decl = feats["smart_bars"]
    if not decl:
        return None
    if decl is True:
        return {"enabled": True}
    if isinstance(decl, dict):
        return decl
    raise BarsRefusal(
        "bad_smart_bars_declaration",
        "contract.features.smart_bars must be an object or true, "
        "got %s" % type(decl).__name__)


def can_render(context):
    """Evaluate the bars render authorization.

    Returns (allowed, missing). allowed is True only when the
    bars.render permission was granted. Rendering the navigation bar is
    a permission question — the bar renders nothing working until the
    grant names it in human words.
    """
    missing = []
    ctx = context or {}
    granted = list(ctx.get("granted_permissions") or [])
    if RENDER_PERMISSION not in granted:
        missing.append(RENDER_PERMISSION_HUMAN)
    return (len(missing) == 0, missing)


def _link_html(section):
    """Render one section's link. The caller guarantees the section
    passed sanitize_section — this function never decides what renders."""
    return ('<a class="smart-bar-link" href="%s" data-bar-id="%s" '
            'data-section-title="%s">%s</a>'
            % (esc(section["address"]), esc(section["id"]),
               esc(section["title"]), esc(section["title"])))


def _list_html(sections, cls):
    """One complete list of section links (desktop list or the mobile
    collapse's list — identical links either way; collapse never hides
    a section)."""
    items = "".join('<li>%s</li>' % _link_html(s) for s in sections)
    return ('<ul class="%s" data-receipt-events="bars.rendered">%s</ul>'
            % (cls, items))


def render_smart_bars(decl, registry_status, context=None):
    """Render the smart bars navigation. Returns '' when the contract
    did not declare smart bars; raises BarsRefusal otherwise.

    registry_status: the registry's status string for feature.smart_bars.
    Rendering is proof the registry says 'built' — the bar carries
    data-bars-status="built" as the binding.
    context: resolved contract context {'connections': {...}, 'privacy': ...,
    'granted_permissions': [...], 'available': [...], 'identity': {'id': ...}}.
    """
    if decl is None or not decl.get("enabled"):
        return ""  # not declared -> refuse to render bars
    if registry_status != "built":
        raise BarsRefusal(
            "feature_not_built",
            "contract declares smart bars but registry status is %r "
            "(contract never activates an unbuilt capability)"
            % (registry_status,))

    sections = [sanitize_section(s) for s in (decl.get("sections") or [])]
    renderable, _ = can_render(context)

    # data-consent is always "ready": bars carry no connected action
    # (registry connected: []), so no grant ever gates the bar itself.
    nav_open = ('<nav class="smart-bars" data-feature="smart_bars" '
                'data-bars-status="built" data-consent="ready">')
    if not sections:
        return (nav_open +
                '<p class="smart-bars-empty">No sections yet — the '
                'sections you declare land here, one tap away.</p></nav>')
    if not renderable:
        return (
            nav_open +
            '<div class="smart-bars-gated" data-consent="ready">'
            '<p class="smart-bars-gated-title">Navigation is ready but '
            'unwired.</p>'
            '<p class="smart-bars-gated-why">To show the navigation bars, '
            'the page needs:</p>'
            '<ul class="smart-bars-gated-list">'
            '<li>render the smart navigation bars</li></ul>'
            '<p class="smart-bars-gated-note">Nothing is wired until you '
            'grant it.</p>'
            '</div></nav>')

    bar = nav_open + _list_html(sections, "smart-bars-list")
    if len(sections) > MOBILE_COLLAPSE_THRESHOLD:
        # mobile_collapse_tested: long bars collapse on mobile. The
        # collapse carries the SAME links — it never hides a section.
        bar += ('<details class="smart-bars-mobile">'
                '<summary class="smart-bars-mobile-summary">Menu</summary>'
                + _list_html(sections, "smart-bars-mobile-list") +
                '</details>')
    return bar + '</nav>'
