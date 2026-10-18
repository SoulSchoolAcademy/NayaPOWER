#!/usr/bin/env python3
"""feature.contacts — "Contacts" (Smart Builder feature breaker).

Capability contract (functions/registry.json):
  id: feature.contacts, version 1.0.0, status tracked in the registry.
  activated_by: contract.features.contacts — the CONTRACT flips the
  breaker; the module never hand-wires itself into a page.
  depends_on: systems.contacts
  requires: authenticated_identity, contact_store
  permissions: contacts.read (reading contact details is a permission question)
  events: contacts.viewed
  acceptance: only_own_contacts_shown, list_renders
  connected: the ONLY connected action is "import and sync contacts"
             (grant: network — strict boolean, the consent-line refinement).
  ready: contacts UI, local address book (works with zero grants).

Activation input (from the contract, which carries the intake's data):
  contract.features.contacts = {
      "enabled": True,
      "contacts": [
          {"name": "Ada Lovelace", "owner": "shawn",
           "handle": "ada@example.com", "notes": "Weekly sync.",
           "added": "2026-10-01"},
      ]
  }
  name: non-empty string (required). owner: the identity id that owns the
  contact (required — acceptance: only_own_contacts_shown). handle, notes,
  added: optional strings (phone, email, free text, date-ish text).

Behavior:
  - Not declared (or enabled falsy) -> render nothing. The page refuses
    to render contacts the contract did not declare.
  - Declared + registry says anything else -> ContactsRefusal(
    'feature_not_built'). The contract never advertises a capability as
    operational unless the registry says it is built.
  - only_own_contacts_shown: the panel renders ONLY contacts whose owner
    matches context['identity']['id']. Another identity's contact never
    appears — not the name, not the handle, not a gated teaser. Without
    an identity, no contact details render at all (honest sign-in line).
  - Contact details are a permission question: with the contacts.read
    permission granted the viewer's own contacts render full; without it
    an honest gated block names the permission in human words. Never a
    dead panel, never silent.
  - Empty (declared, zero contacts) -> an honest empty line, never an
    empty section, never a crash, never a fake contact (list_renders).
  - The connected action: a live "Import and sync contacts" button ONLY
    when the network connection is strictly True (grant, not truthy).
    Otherwise an honest gated block naming the connection. Import is to
    contacts what sync is to intelligence: grant-gated, never dead.
  - Malformed contacts (missing/blank name, bad owner, wrong shape, bad
    handle/notes/added) -> ContactsRefusal('bad_contact'), never silently
    dropped.
  - Receipt hooks -> the panel carries data-receipt-events with the
    registry's own events (contacts.viewed) so the runtime can persist
    receipts. A claim of "viewed" without a receipt is a hope.

Judgment, named: the contact READ is a permission question (contacts.read)
and the IMPORT/SYNC is a connection question (network grant, strict
boolean) — the same grant/permission split the intelligence_today module
draws between its sync action (grant) and its report flow (permission).
Ownership is the finest control of all: it is checked before either gate,
because a panel that leaks another identity's contact under a granted
permission is a panel that cannot be trusted.

Acceptance (registry: only_own_contacts_shown, list_renders) is exercised
in functions/tests/test_feature_contacts.py.

Stdlib only. Pure functions — same declaration + same context -> same
bytes, always.
"""
import html as htmlmod

VERSION = "1.0.0"
FEATURE_ID = "feature.contacts"
# aliases the assembler imports
FEATURE_CONTACTS_ID = FEATURE_ID
FEATURE_CONTACTS_VERSION = VERSION

# The connected import/sync action fires only on this recorded grant
# (strict boolean — the consent-line refinement: grant = True, not truthy).
SYNC_GRANT = "network"

# Reading contact details is a permission question.
READ_PERMISSION = "contacts.read"


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


def _nonempty_str(value):
    return isinstance(value, str) and bool(value.strip())


def sanitize_contact(contact):
    """Validate one contact. Returns {'name', 'owner', 'handle', 'notes',
    'added'}. Raises ContactsRefusal('bad_contact') for anything
    malformed — a contacts panel that swallows a bad contact silently is
    a panel that cannot be trusted."""
    if not isinstance(contact, dict):
        raise ContactsRefusal(
            "bad_contact",
            "each contact must be an object, got %s" % type(contact).__name__)
    name = contact.get("name")
    if not _nonempty_str(name):
        raise ContactsRefusal(
            "bad_contact",
            "contact needs a non-empty string name, got %r" % (name,))
    owner = contact.get("owner")
    if not _nonempty_str(owner):
        raise ContactsRefusal(
            "bad_contact",
            "contact needs a non-empty string owner (identity id), got %r"
            % (owner,))

    def _opt(key):
        value = contact.get(key)
        if value in (None,):
            return ""
        if not isinstance(value, str):
            raise ContactsRefusal(
                "bad_contact",
                "contact %s must be a string, got %s"
                % (key, type(value).__name__))
        return value.strip()

    return {"name": name.strip(), "owner": owner.strip(),
            "handle": _opt("handle"), "notes": _opt("notes"),
            "added": _opt("added")}


def decl_for(contract):
    """Extract the contacts declaration from a contract, or None.

    Accepts the PLUMBING.md breaker convention
    (contract.features.contacts):
      - dict  -> the declaration (task shape: enabled/contacts)
      - True  -> enabled with empty fields
      - falsy / absent / features-not-a-dict -> None (not declared)
      - anything else truthy -> ContactsRefusal('bad_contacts_declaration')
    """
    feats = contract.get("features") if isinstance(contract, dict) else None
    if not isinstance(feats, dict):
        return None  # contract-page contracts carry features as a list
    if "contacts" not in feats:
        return None
    decl = feats["contacts"]
    if not decl:
        return None
    if decl is True:
        return {"enabled": True}
    if isinstance(decl, dict):
        return decl
    raise ContactsRefusal(
        "bad_contacts_declaration",
        "contract.features.contacts must be an object or true, "
        "got %s" % type(decl).__name__)


def _viewer_id(context):
    """The signed-in viewer's identity id, or None. No identity means no
    personal data renders — fail closed on other people's contacts."""
    ctx = context or {}
    ident = ctx.get("identity") or {}
    ident_id = ident.get("id")
    return ident_id if _nonempty_str(ident_id) else None


def can_read(context):
    """Evaluate the contact-details read authorization.

    Returns (allowed, missing). allowed is True only when the
    contacts.read permission was granted. This is a permission question
    (the read), not a connection question — the grant gates the import
    action, the permission gates reading details.
    """
    missing = []
    ctx = context or {}
    granted = list(ctx.get("granted_permissions") or [])
    if READ_PERMISSION not in granted:
        missing.append("read your contacts")
    return (len(missing) == 0, missing)


def can_sync(context):
    """Evaluate the import-and-sync authorization.

    Returns (allowed, missing). allowed is True only when the network
    grant holds — strictly True. This is the connected action: importing
    contacts is a connection question, not a permission question.
    """
    missing = []
    ctx = context or {}
    connections = ctx.get("connections") or {}
    if connections.get(SYNC_GRANT) is not True:
        missing.append("the network connection switched on for this page")
    return (len(missing) == 0, missing)


def _sync_block(context):
    """The connected action: a live import button only when the network
    grant holds strictly, otherwise an honest gated block naming the
    connection. Never a dead button."""
    allowed, missing = can_sync(context)
    if allowed:
        return (
            '<div class="contacts-sync" data-consent="connected" '
            'data-sync-grant="network">'
            '<button type="button" class="contacts-sync-btn">'
            'Import and sync contacts</button>'
            '<div class="contacts-receipts" data-receipt-events='
            '"contacts.viewed">'
            '<span class="contacts-receipts-note">Receipts are recorded for '
            'every viewed contact.</span></div>'
            '</div>')
    reasons = "".join("<li>%s</li>" % esc(r) for r in missing)
    return (
        '<div class="contacts-sync contacts-sync-gated" data-consent="ready">'
        '<p class="contacts-gated-title">Sync is ready but off.</p>'
        '<p class="contacts-gated-why">To import and sync contacts, the page '
        'needs:</p>'
        '<ul class="contacts-gated-list">%s</ul>'
        '<p class="contacts-gated-note">Your contacts stay put — import '
        'waits for the grant.</p>'
        '</div>' % reasons)


def _contact_html(contact):
    """Render one owned contact card. The caller guarantees ownership —
    this function never decides who may see what."""
    card = ('<article class="contact-card" data-owner="%s">'
            '<h3 class="contact-name">%s</h3>' % (esc(contact["owner"]),
                                                  esc(contact["name"])))
    if contact["handle"]:
        card += ('<p class="contact-handle">%s</p>'
                 % esc(contact["handle"]))
    if contact["notes"]:
        card += ('<p class="contact-notes">%s</p>'
                 % esc(contact["notes"]))
    if contact["added"]:
        card += ('<p class="contact-added">Added %s</p>'
                 % esc(contact["added"]))
    return card + '</article>'


def render_contacts(decl, registry_status, context=None):
    """Render the contacts panel. Returns '' when the contract did not
    declare contacts; raises ContactsRefusal otherwise.

    registry_status: the registry's status string for feature.contacts.
    Rendering is proof the registry says 'built' — the panel carries
    data-contacts-status="built" as the binding.
    context: resolved contract context {'connections': {...}, 'privacy': ...,
    'granted_permissions': [...], 'available': [...], 'identity': {'id': ...}}.
    """
    if decl is None or not decl.get("enabled"):
        return ""  # not declared -> refuse to render contacts
    if registry_status != "built":
        raise ContactsRefusal(
            "feature_not_built",
            "contract declares contacts but registry status is %r "
            "(contract never activates an unbuilt capability)"
            % (registry_status,))

    contacts = [sanitize_contact(c) for c in (decl.get("contacts") or [])]
    viewer = _viewer_id(context)
    if viewer is None:
        # No identity: no personal data renders, ever. The panel stays
        # honest about why.
        return (
            '<section class="contacts-panel" data-feature="contacts" '
            'data-contacts-status="built" data-consent="ready">'
            '<h2 class="contacts-title">Contacts</h2>'
            '<p class="contacts-no-identity">Sign in to see your contacts — '
            'contacts belong to an identity, and no identity is signed in '
            'on this page.</p>'
            '</section>')

    own = [c for c in contacts if c["owner"] == viewer]
    readable, _ = can_read(context)
    sync_live, _ = can_sync(context)

    # data-consent mirrors the assembler contract: "connected" ONLY when
    # the grant-active import affordance renders; else "ready".
    consent_word = "connected" if sync_live else "ready"
    panel = ('<section class="contacts-panel" data-feature="contacts" '
             'data-contacts-status="built" data-consent="%s">'
             '<h2 class="contacts-title">Contacts</h2>' % consent_word)
    if not own:
        panel += ('<p class="contacts-empty">No contacts yet — the people '
                  'you add land here, one tap away.</p>')
    elif readable:
        panel += ('<div class="contacts-list">%s</div>'
                  % "".join(_contact_html(c) for c in own))
    else:
        panel += (
            '<div class="contacts-read-gated" data-consent="ready">'
            '<p class="contacts-gated-title">Your contacts are ready but '
            'private.</p>'
            '<p class="contacts-gated-why">To read your contacts, the page '
            'needs:</p>'
            '<ul class="contacts-gated-list">'
            '<li>read your contacts</li></ul>'
            '<p class="contacts-gated-note">Nothing is shown until you '
            'grant it.</p>'
            '</div>')
    panel += _sync_block(context)
    return panel + '</section>'
