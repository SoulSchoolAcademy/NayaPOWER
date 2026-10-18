#!/usr/bin/env python3
"""feature.space — "Smart Space" (Smart Builder feature breaker).

Capability contract (functions/registry.json):
  id: feature.space, version 1.0.0, status tracked in the registry.
  activated_by: contract.features.space — the CONTRACT flips the breaker;
  the module never hand-wires itself into a page.

Activation input (from the contract, which carries the intake's data):
  contract.features.space = {
      "enabled": True,
      "spaces": [
          {"name": "Book club", "visibility": "network",  # private default
           "description": "Monthly reads and arguments.",
           "members": [{"id": "u1", "name": "Bo"},
                       {"id": "u2", "name": "Rae"}]},
      ]
  }
  visibility: 'private' | 'network' | 'public', default 'private'.

Behavior:
  - Not declared (or enabled falsy) -> render nothing. The page refuses
    to render spaces the contract did not declare.
  - Declared + registry says built -> the spaces panel: space views with
    member lists and the local gathering view (READY — works with zero
    grants: gathering is a local act), plus the join action. Join is a
    CONNECTED action: it renders as a live join button ONLY when the
    join authorization holds — space.join granted AND the NayaNET
    connection ON — otherwise an honest gated block naming exactly what
    is missing in human words. Never a dead button, never silent.
  - Declared + registry says anything else -> SpaceRefusal('feature_not_built').
    The contract never advertises a capability as operational unless the
    registry says it is built.
  - Private spaces stay private: a private space renders NO join
    affordance at all — a "Private — members only" line stands in its
    place. Joining a private space is not a gated state, it is an absent
    one. member_list_correct holds for every visibility: members render
    with their declared names, never invented ones.
  - Malformed members (missing id/name, wrong shape) ->
    SpaceRefusal('bad_space_member'), never silently dropped.
  - Receipt hooks -> the spaces block carries data-receipt-events with the
    registry's own events (space.created, space.joined, space.left) so the
    runtime can persist receipts. A claim of "joined" without a receipt
    is a hope.

Judgment, named: page-level privacy (context['privacy']) stays
informational — the space's own visibility (private/network/public) is
the finer, per-space control and governs joining, mirroring how the
lists module treats page privacy. Join is the only runtime connected
action; creating a space is a contract-time act (the contract declares
the spaces), so the space.create permission is enforced at the resolver
gate, not as a page button. A private page with a public space allows
joining; a public page with a private space never does.

Acceptance (registry: private_space_stays_private, join_flow_tested,
member_list_correct) is exercised in
functions/tests/test_feature_space.py.

Stdlib only. Pure functions — same declaration + same context -> same
bytes, always.
"""
import html as htmlmod

VERSION = "1.0.0"
FEATURE_ID = "feature.space"
# aliases the assembler imports
FEATURE_SPACE_ID = FEATURE_ID
FEATURE_SPACE_VERSION = VERSION

# The connected join action fires only on this recorded grant
# (strict boolean — the consent-line refinement: grant = True, not truthy).
JOIN_GRANT = "nayanet"

VISIBILITIES = ("private", "network", "public")

# Human words for join-gate reasons, so the gated block speaks plainly.
GRANT_WORDS = {
    "permission": "your permission to join spaces",
    "nayanet": "the NayaNET connection switched on for this page",
}


class SpaceRefusal(Exception):
    """Structured refusal: the smart-space breaker declined to activate.

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


def sanitize_member(member):
    """Validate one space member. Returns {'id', 'name'}.
    Raises SpaceRefusal('bad_space_member') for anything malformed —
    member_list_correct means the list is exactly what the contract
    declared, never silently trimmed."""
    if not isinstance(member, dict):
        raise SpaceRefusal("bad_space_member",
                           "space member must be an object, got %s"
                           % type(member).__name__)
    mid = member.get("id")
    if not isinstance(mid, str) or not mid.strip():
        raise SpaceRefusal("bad_space_member",
                           "space member needs a non-empty string id, got %r"
                           % (mid,))
    name = member.get("name")
    if not isinstance(name, str) or not name.strip():
        raise SpaceRefusal("bad_space_member",
                           "space member %r needs a non-empty string name"
                           % (mid,))
    return {"id": mid.strip(), "name": name.strip()}


def sanitize_space(sp):
    """Validate one space. Returns {'name', 'visibility', 'description',
    'members'}. Raises SpaceRefusal on bad visibility or bad members."""
    if not isinstance(sp, dict):
        raise SpaceRefusal("bad_smart_space_declaration",
                           "each space must be an object, got %s"
                           % type(sp).__name__)
    vis = sp.get("visibility") or "private"
    if vis not in VISIBILITIES:
        raise SpaceRefusal("bad_space_visibility",
                           "space visibility must be one of %s, got %r"
                           % (list(VISIBILITIES), vis))
    members = sp.get("members") or []
    if not isinstance(members, list):
        raise SpaceRefusal("bad_smart_space_declaration",
                           "space members must be a list, got %s"
                           % type(members).__name__)
    return {"name": str(sp.get("name") or "(unnamed space)"),
            "visibility": vis,
            "description": str(sp.get("description") or ""),
            "members": [sanitize_member(m) for m in members]}


def decl_for(contract):
    """Extract the smart-space declaration from a contract, or None.

    Accepts the PLUMBING.md breaker convention
    (contract.features.space):
      - dict  -> the declaration (task shape: enabled/spaces)
      - True  -> enabled with empty fields
      - falsy / absent / features-not-a-dict -> None (not declared)
      - anything else truthy -> SpaceRefusal('bad_smart_space_declaration')
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
        return {"enabled": True}
    if isinstance(decl, dict):
        return decl
    raise SpaceRefusal("bad_smart_space_declaration",
                       "contract.features.space must be an object or true, "
                       "got %s" % type(decl).__name__)


def can_join(context):
    """Evaluate the join authorization for a space.

    Returns (allowed, missing). allowed is True only when the join grant
    holds: space.join granted AND the NayaNET connection strictly ON.
    Private spaces are not a grant question — they never render a join
    affordance at all (private_space_stays_private), so callers check
    visibility first; this gate answers only the authorization question.
    """
    missing = []
    ctx = context or {}
    granted = list(ctx.get("granted_permissions") or [])
    if "space.join" not in granted:
        missing.append(GRANT_WORDS["permission"])
    connections = ctx.get("connections") or {}
    if connections.get(JOIN_GRANT) is not True:
        missing.append(GRANT_WORDS["nayanet"])
    return (len(missing) == 0, missing)


def _members_html(members):
    if not members:
        return '<p class="space-empty">No members yet — be the first to gather.</p>'
    lis = []
    for m in members:
        lis.append(
            '<li class="space-member" data-member-id="%s">'
            '<span class="space-member-name">%s</span></li>'
            % (esc(m["id"]), esc(m["name"])))
    return '<ul class="space-members">%s</ul>' % "".join(lis)


def _join_block(allowed, missing):
    """The connected action: a live join button only when authorized,
    otherwise an honest gated block naming what is missing. The two are
    visually distinct and the verifier asserts data-consent honesty."""
    if allowed:
        return (
            '<div class="space-join" data-consent="connected" '
            'data-join-grant="nayanet">'
            '<button type="button" class="space-join-btn">Join space</button>'
            '<div class="space-receipts" data-receipt-events='
            '"space.created space.joined space.left">'
            '<span class="space-receipts-note">Receipts are recorded for '
            'every join.</span></div>'
            '</div>')
    reasons = "".join("<li>%s</li>" % esc(r) for r in missing)
    return (
        '<div class="space-join space-join-gated" data-consent="ready">'
        '<p class="space-gated-title">Joining is ready but off.</p>'
        '<p class="space-gated-why">To join this space, the page needs:</p>'
        '<ul class="space-gated-list">%s</ul>'
        '<p class="space-gated-note">Gathering works now — joining waits '
        'for the grant.</p>'
        '</div>' % reasons)


def _space_html(sp, context):
    """Render one space. Private spaces render NO join affordance —
    the join flow does not exist for them (acceptance:
    private_space_stays_private)."""
    vis = sp["visibility"]
    badge = '<span class="space-visibility space-visibility-%s">%s</span>' \
        % (esc(vis), esc(vis))
    desc = ('<p class="space-description">%s</p>' % esc(sp["description"])
            if sp["description"] else "")
    if vis == "private":
        join = ('<p class="space-private-note">Private — members only, '
                'never joinable from here.</p>')
    else:
        allowed, missing = can_join(context)
        join = _join_block(allowed, missing)
    return (
        '<section class="smart-space-space" data-visibility="%s">'
        '<h3 class="space-name">%s</h3>%s'
        '%s'
        '<div class="space-gather"><h4>Gather</h4>%s</div>'
        '%s'
        '</section>'
        % (esc(vis), esc(sp["name"]), badge, desc,
           _members_html(sp["members"]), join)
    )


def render_smart_space(decl, registry_status, context=None):
    """Render the Smart Spaces panel. Returns '' when the contract did not
    declare space; raises SpaceRefusal otherwise.

    registry_status: the registry's status string for feature.space.
    Rendering is proof the registry says 'built' — the page carries
    data-space-status="built" as the binding.
    context: resolved contract context {'connections': {...}, 'privacy': ...,
    'granted_permissions': [...], 'available': [...], 'identity': {...}}.
    """
    if decl is None or not decl.get("enabled"):
        return ""  # not declared -> refuse to render spaces
    if registry_status != "built":
        raise SpaceRefusal(
            "feature_not_built",
            "contract declares space but registry status is %r "
            "(contract never activates an unbuilt capability)" % (registry_status,))

    spaces = [sanitize_space(s) for s in (decl.get("spaces") or [])]
    # data-consent on the panel mirrors the assembler contract: "connected"
    # ONLY when a grant-active join affordance renders; else "ready".
    any_live_join = any(
        s["visibility"] != "private" and can_join(context)[0]
        for s in spaces)
    consent_word = "connected" if any_live_join else "ready"
    return (
        '<section class="smart-spaces" data-feature="smart_space" '
        'data-space-status="built" data-consent="%s">'
        '<h2 class="spaces-title">Smart Spaces</h2>'
        '%s'
        '</section>'
        % (consent_word, "".join(_space_html(s, context) for s in spaces))
    )
