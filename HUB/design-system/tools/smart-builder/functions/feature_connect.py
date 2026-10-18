#!/usr/bin/env python3
"""feature.connect — "Connect + communicate" (Smart Builder feature breaker).

Capability contract (functions/registry.json):
  id: feature.connect, version 1.0.0, status tracked in the registry.
  activated_by: contract.features.connect — the CONTRACT flips the breaker;
  the module never hand-wires itself into a page.
  depends_on: systems.identity
  requires: authenticated_identity, identity_directory, consent_records
  permissions: connect.request (send connection requests on your behalf),
               connect.accept (accept connection requests from visitors)
  events: connect.requested, connect.accepted, connect.declined
  acceptance: no_contact_without_consent, request_flow_tested,
              decline_respected
  connected: the ONLY connected action is "message a connection"
             (grant: nayanet — strict boolean, the consent-line refinement).

Activation input (from the contract, which carries the intake's data):
  contract.features.connect = {
      "enabled": True,
      "people": [
          {"name": "Ada Lovelace", "relation": "accepted"},  # mutual — may message
          {"name": "Bob Stone",    "relation": "pending"},   # request sent, awaiting
          {"name": "Carla Reyes",  "relation": "requested"},# incoming request
          {"name": "Dana Fox",     "relation": "declined"}, # declined — honest line
      ]
  }
  relation: 'accepted' | 'pending' | 'requested' | 'declined' (required).
  note: optional free-text note attached to the person.

Behavior:
  - Not declared (or enabled falsy) -> render nothing. The page refuses
    to render people the contract did not declare.
  - Declared + registry says anything else -> ConnectRefusal('feature_not_built').
    The contract never advertises a capability as operational unless the
    registry says it is built.
  - Message is the ONLY connected action: a live "Message <name>" button
    ONLY when the nayanet connection is strictly ON. Otherwise an honest
    gated block naming exactly what is missing in human words. Never a
    dead button, never silent.
  - Pending people are not contacts yet: they render NO message affordance
    at all — absent, not gated (acceptance: no_contact_without_consent).
  - Declined requests are respected: an honest declined line, never
    messageable, never re-requestable from here (decline_respected).
  - Incoming requests ('requested'): accept/decline affordances are live
    only when the connect.accept permission is granted; otherwise an
    honest gated block naming the permission in human words. Requesting
    (the outgoing leg) follows the same honesty via connect.request —
    a request card with no granted request permission renders its honest
    gated line, never a dead "Send request".
  - Malformed people (missing name, blank name, bad relation, wrong shape,
    bad note) -> ConnectRefusal('bad_connect_person'), never silently dropped.
  - Receipt hooks -> the connect block carries data-receipt-events with
    the registry's own events (connect.requested, connect.accepted,
    connect.declined) so the runtime can persist receipts. A claim of
    "connected" without a receipt is a hope.

Judgment, named: the message grant is a connection question, not a
permission question — the NayaNET connection being on is what makes
messaging a live capability. Permissions (request/accept) gate the
request FLOW; the grant gates the connected ACTION. A pending page with
nayanet on still messages nobody: the relation is the finer control,
mirroring how the feed module treats per-post visibility as finer than
page-level privacy.

Acceptance (registry: no_contact_without_consent, request_flow_tested,
decline_respected) is exercised in
functions/tests/test_feature_connect.py.

Stdlib only. Pure functions — same declaration + same context -> same
bytes, always.
"""
import html as htmlmod

VERSION = "1.0.0"
FEATURE_ID = "feature.connect"
# aliases the assembler imports
FEATURE_CONNECT_ID = FEATURE_ID
FEATURE_CONNECT_VERSION = VERSION

# The connected message action fires only on this recorded grant
# (strict boolean — the consent-line refinement: grant = True, not truthy).
MESSAGE_GRANT = "nayanet"

RELATIONS = ("accepted", "pending", "requested", "declined")

# Human words for the request-flow permission gates, so the gated block
# speaks plainly (same words the resolver uses).
GRANT_WORDS = {
    "nayanet": "the NayaNET connection switched on for this page",
    "connect.accept": "your permission to accept connection requests "
                      "from visitors",
    "connect.request": "your permission to send connection requests "
                       "on your behalf",
}


class ConnectRefusal(Exception):
    """Structured refusal: the connect breaker declined to activate.

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


def sanitize_person(person):
    """Validate one connect person. Returns {'name', 'relation', 'note'}.
    Raises ConnectRefusal('bad_connect_person') for anything malformed —
    a connect panel that swallows a bad person silently is a panel that
    cannot be trusted."""
    if not isinstance(person, dict):
        raise ConnectRefusal("bad_connect_person",
                             "each person must be an object, got %s"
                             % type(person).__name__)
    name = person.get("name")
    if not _nonempty_str(name):
        raise ConnectRefusal("bad_connect_person",
                             "person needs a non-empty string name, got %r"
                             % (name,))
    rel = person.get("relation")
    if rel not in RELATIONS:
        raise ConnectRefusal("bad_connect_person",
                             "person relation must be one of %s, got %r"
                             % (list(RELATIONS), rel))
    note = person.get("note")
    if note not in (None,) and not isinstance(note, str):
        raise ConnectRefusal("bad_connect_person",
                             "person note must be a string, got %s"
                             % type(note).__name__)
    return {"name": name.strip(), "relation": rel,
            "note": note.strip() if isinstance(note, str) and note.strip()
            else ""}


def decl_for(contract):
    """Extract the connect declaration from a contract, or None.

    Accepts the PLUMBING.md breaker convention
    (contract.features.connect):
      - dict  -> the declaration (task shape: enabled/people)
      - True  -> enabled with empty fields
      - falsy / absent / features-not-a-dict -> None (not declared)
      - anything else truthy -> ConnectRefusal('bad_connect_declaration')
    """
    feats = contract.get("features") if isinstance(contract, dict) else None
    if not isinstance(feats, dict):
        return None  # contract-page contracts carry features as a list
    if "connect" not in feats:
        return None
    decl = feats["connect"]
    if not decl:
        return None
    if decl is True:
        return {"enabled": True}
    if isinstance(decl, dict):
        return decl
    raise ConnectRefusal("bad_connect_declaration",
                         "contract.features.connect must be an object or true, "
                         "got %s" % type(decl).__name__)


def can_message(context):
    """Evaluate the message authorization for an accepted connection.

    Returns (allowed, missing). allowed is True only when the nayanet
    grant holds — strictly True. Relations are checked by the caller:
    only 'accepted' people ever reach this gate, so a pending/requested/
    declined person is never a grant question (no_contact_without_consent,
    decline_respected — the affordance is absent for them, never gated).
    """
    missing = []
    ctx = context or {}
    connections = ctx.get("connections") or {}
    if connections.get(MESSAGE_GRANT) is not True:
        missing.append(GRANT_WORDS[MESSAGE_GRANT])
    return (len(missing) == 0, missing)


def can_accept(context):
    """Evaluate the accept/decline authorization for an incoming request.

    Returns (allowed, missing). allowed is True only when the
    connect.accept permission was granted. This is a permission question
    (the request flow), not a connection question — the grant gates the
    message action, the permission gates the request flow.
    """
    missing = []
    ctx = context or {}
    granted = list(ctx.get("granted_permissions") or [])
    if "connect.accept" not in granted:
        missing.append(GRANT_WORDS["connect.accept"])
    return (len(missing) == 0, missing)


def _message_block(person, context):
    """The connected action: a live message button only when authorized,
    otherwise an honest gated block naming what is missing. The two are
    visually distinct and the verifier asserts data-consent honesty."""
    allowed, missing = can_message(context)
    if allowed:
        return (
            '<div class="connect-message" data-consent="connected" '
            'data-message-grant="nayanet">'
            '<button type="button" class="connect-message-btn">Message %s</button>'
            '<div class="connect-receipts" data-receipt-events='
            '"connect.requested connect.accepted connect.declined">'
            '<span class="connect-receipts-note">Receipts are recorded for '
            'every request and message.</span></div>'
            '</div>' % esc(person["name"]))
    reasons = "".join("<li>%s</li>" % esc(r) for r in missing)
    return (
        '<div class="connect-message connect-message-gated" '
        'data-consent="ready">'
        '<p class="connect-gated-title">Messaging is ready but off.</p>'
        '<p class="connect-gated-why">To message %s, the page needs:</p>'
        '<ul class="connect-gated-list">%s</ul>'
        '<p class="connect-gated-note">Your connection is kept — messaging '
        'waits for the grant.</p>'
        '</div>' % (esc(person["name"]), reasons))


def _accept_block(person, context):
    """The incoming-request flow: live accept/decline affordances only
    when the connect.accept permission is granted, otherwise an honest
    gated block naming the permission. Never a dead button."""
    allowed, missing = can_accept(context)
    if allowed:
        return (
            '<div class="connect-request-actions" data-consent="ready">'
            '<button type="button" class="connect-accept-btn">Accept request</button>'
            '<button type="button" class="connect-decline-btn">Decline</button>'
            '<div class="connect-receipts" data-receipt-events='
            '"connect.requested connect.accepted connect.declined">'
            '<span class="connect-receipts-note">Receipts are recorded for '
            'every request and message.</span></div>'
            '</div>')
    reasons = "".join("<li>%s</li>" % esc(r) for r in missing)
    return (
        '<div class="connect-request-actions connect-request-gated" '
        'data-consent="ready">'
        '<p class="connect-gated-title">This request is ready but waiting.</p>'
        '<p class="connect-gated-why">To answer %s&#39;s request, the page needs:</p>'
        '<ul class="connect-gated-list">%s</ul>'
        '</div>' % (esc(person["name"]), reasons))


def _person_html(person, context):
    """Render one person card. Only 'accepted' people carry the message
    affordance; pending/requested/declined people are not contacts —
    no message affordance renders for them at all (absent, never gated).
    Declined requests render the honest declined line."""
    rel = person["relation"]
    card = ('<article class="connect-person" data-relation="%s">'
            '<h3 class="connect-person-name">%s</h3>' % (esc(rel),
                                                        esc(person["name"])))
    if person["note"]:
        card += '<p class="connect-person-note">%s</p>' % esc(person["note"])
    if rel == "accepted":
        card += '<p class="connect-badge">Connected</p>'
        card += _message_block(person, context)
    elif rel == "pending":
        card += ('<p class="connect-pending">Request sent to %s — waiting '
                 'for them to accept. No contact is shared yet.</p>'
                 % esc(person["name"]))
    elif rel == "requested":
        card += ('<p class="connect-incoming">%s wants to connect with you.</p>'
                 % esc(person["name"]))
        card += _accept_block(person, context)
    else:  # declined
        card += ('<p class="connect-declined">You declined %s&#39;s request — '
                 'nothing was shared.</p>' % esc(person["name"]))
    return card + '</article>'


def render_connect(decl, registry_status, context=None):
    """Render the connect panel. Returns '' when the contract did not
    declare connect; raises ConnectRefusal otherwise.

    registry_status: the registry's status string for feature.connect.
    Rendering is proof the registry says 'built' — the page carries
    data-connect-status="built" as the binding.
    context: resolved contract context {'connections': {...}, 'privacy': ...,
    'granted_permissions': [...], 'available': [...], 'identity': {...}}.
    """
    if decl is None or not decl.get("enabled"):
        return ""  # not declared -> refuse to render people
    if registry_status != "built":
        raise ConnectRefusal(
            "feature_not_built",
            "contract declares connect but registry status is %r "
            "(contract never activates an unbuilt capability)"
            % (registry_status,))

    people = [sanitize_person(p) for p in (decl.get("people") or [])]
    # data-consent on the panel mirrors the assembler contract: "connected"
    # ONLY when a grant-active message affordance renders; else "ready".
    any_live_message = any(
        p["relation"] == "accepted" and can_message(context)[0]
        for p in people)
    consent_word = "connected" if any_live_message else "ready"
    return (
        '<section class="connect" data-feature="connect" '
        'data-connect-status="built" data-consent="%s">'
        '<h2 class="connect-title">Connect</h2>'
        '<div class="connect-people">%s</div>'
        '</section>'
        % (consent_word,
           "".join(_person_html(p, context) for p in people))
    )
