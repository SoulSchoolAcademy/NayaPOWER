#!/usr/bin/env python3
"""feature.smart_mail — "Smart Mail" (Smart Builder feature breaker).

Capability contract (functions/registry.json):
  id: feature.smart_mail, version 1.0.0, status tracked in the registry.
  activated_by: contract.features.smart_mail — the CONTRACT flips the breaker;
  the module never hand-wires itself into a page.

Activation input (from the contract, which carries the intake's data):
  contract.features.smart_mail = {
      "enabled": True,
      "from": {"name": "Ada Narzan", "address": "ada@nayanet.live"},  # optional
      "to": ["friend@example.com", {"name": "Bo", "address": "bo@example.com"}],
      "subject": "Tomorrow's bread run",        # optional draft subject
      "body": "Warm loaves at 8.",              # optional draft body
      "drafts": [{"subject": "...", "body": "...", "to": [...]}],  # optional
      "delivered": [{"subject": "...", "to": [...], "at": "...",
                     "receipt": "mail.send.accepted"}]             # optional
  }
  "from" falls back to the assembler's centralized identity block.

Behavior:
  - Not declared (or enabled falsy) -> render nothing. The page refuses
    to render mail the contract did not declare.
  - Declared + registry says built -> the mail panel: compose UI, drafts
    and mailbox views (READY — work with zero grants), plus the send and
    broadcast actions. Send/broadcast are CONNECTED actions: they render
    as a live send form ONLY when every authorization holds —
    mail.send granted AND network connection ON AND message_service
    available AND recipient authorization present. Otherwise the panel
    shows an honest gated block naming exactly what is missing in human
    words — never a dead button pretending to send, never silent.
  - Declared + registry says anything else -> SmartMailRefusal('feature_not_built').
    The contract never advertises a capability as operational unless the
    registry says it is built.
  - Unauthorized send -> can_send() returns (False, reasons); the resolver's
    permission gate (mail.send) refuses activation first. The module never
    renders a live send affordance when the grant is absent.
  - Message service unavailable -> failure state renders visibly
    ("Smart Mail can't send right now"), not a silent break.
  - Delivery receipts -> every delivered entry carries its receipt event;
    the connected send block carries a receipt hook (data-receipt-events)
    so the runtime can persist receipts. A receipt-less "sent" is a hope,
    and this module does not traffic in hopes.

Acceptance (registry: unauthorized_send_denied, authorized_send_tested,
failure_state_visible, receipt_persisted) is exercised in
functions/tests/test_feature_smart_mail.py.

Stdlib only. Pure functions — same declaration + same context -> same
bytes, always.
"""
import html as htmlmod
import re

VERSION = "1.0.0"
FEATURE_ID = "feature.smart_mail"
# aliases the assembler imports
FEATURE_SMART_MAIL_ID = FEATURE_ID
FEATURE_SMART_MAIL_VERSION = VERSION

# The connected send/broadcast actions fire only on this recorded grant
# (strict boolean — the consent-line refinement: grant = True, not truthy).
SEND_GRANT = "network"

# Human words for send-gate reasons, so the gated block speaks plainly.
GRANT_WORDS = {
    "permission": "your permission to send mail through Smart Mail",
    "network": "the network connection switched on for this page",
    "message_service": "a message service to carry the mail",
    "recipient_authorization": "recipient authorization to receive mail",
}

# Strict address shape: local@label.label[.label]* — every label non-empty,
# no leading/trailing hyphens on labels, no spaces, no control chars.
_ADDRESS_RE = re.compile(
    r"^[A-Za-z0-9._%+-]{1,64}"
    r"@(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+"
    r"[A-Za-z]{2,}$")


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


def esc(s):
    return htmlmod.escape(str(s), quote=True)


def sanitize_recipient(rec):
    """Validate one recipient. Returns {'name': ..., 'address': ...}.
    Raises SmartMailRefusal('unsafe_recipient') for anything hostile."""
    if isinstance(rec, str):
        name, addr = "", rec
    elif isinstance(rec, dict):
        name, addr = rec.get("name") or "", rec.get("address") or ""
    else:
        raise SmartMailRefusal("unsafe_recipient",
                               "recipient must be a string or an object, "
                               "got %s" % type(rec).__name__)
    if not isinstance(addr, str):
        raise SmartMailRefusal("unsafe_recipient",
                               "recipient address must be a string, got %s"
                               % type(addr).__name__)
    addr = addr.strip()
    if not _ADDRESS_RE.match(addr):
        raise SmartMailRefusal("unsafe_recipient",
                               "not a deliverable address: %r" % addr[:80])
    return {"name": str(name).strip(), "address": addr}


def decl_for(contract):
    """Extract the smart-mail declaration from a contract, or None.

    Accepts the PLUMBING.md breaker convention
    (contract.features.smart_mail):
      - dict  -> the declaration (task shape: enabled/from/to/subject/…)
      - True  -> enabled with empty fields
      - falsy / absent / features-not-a-dict -> None (not declared)
      - anything else truthy -> SmartMailRefusal('bad_smart_mail_declaration')
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
        return {"enabled": True}
    if isinstance(decl, dict):
        return decl
    raise SmartMailRefusal("bad_smart_mail_declaration",
                           "contract.features.smart_mail must be an object or true, "
                           "got %s" % type(decl).__name__)


def can_send(context):
    """Evaluate the send authorization. Returns (allowed, missing).

    missing: human-readable reasons, longest list first is NOT needed —
    every missing gate is named. allowed is True only when all four hold:
      mail.send granted, network grant strictly True, message_service
      available, recipient_authorization available.
    """
    missing = []
    ctx = context or {}
    granted = list(ctx.get("granted_permissions") or [])
    if "mail.send" not in granted:
        missing.append(GRANT_WORDS["permission"])
    connections = ctx.get("connections") or {}
    if connections.get(SEND_GRANT) is not True:
        missing.append(GRANT_WORDS["network"])
    available = list(ctx.get("available") or [])
    if "message_service" not in available:
        missing.append(GRANT_WORDS["message_service"])
    if "recipient_authorization" not in available:
        missing.append(GRANT_WORDS["recipient_authorization"])
    return (len(missing) == 0, missing)


def _draft_fields(decl):
    """The compose form is prefilled from the declaration draft, if any."""
    to = decl.get("to") or []
    if isinstance(to, str):
        to = [to]  # a lone string is one recipient, not a dropped draft
    recs = [sanitize_recipient(r) for r in to] if isinstance(to, list) else []
    return (", ".join(r["address"] for r in recs),
            str(decl.get("subject") or ""),
            str(decl.get("body") or ""))


def _drafts_html(decl):
    drafts = decl.get("drafts") or []
    if not isinstance(drafts, list):
        drafts = []
    items = []
    for d in drafts:
        if not isinstance(d, dict):
            continue
        items.append(
            '<li class="mail-draft"><span class="mail-draft-subject">%s</span>'
            '<span class="mail-draft-to">%s</span></li>'
            % (esc(str(d.get("subject") or "(no subject)")),
               esc(", ".join(str(t) for t in (d.get("to") or [])))))
    if not items:
        return ('<p class="mail-empty">No drafts yet — compose above.</p>')
    return '<ul class="mail-drafts">%s</ul>' % "".join(items)


def _mailbox_html(decl):
    delivered = decl.get("delivered") or []
    if not isinstance(delivered, list):
        delivered = []
    items = []
    for m in delivered:
        if not isinstance(m, dict):
            continue
        receipt = str(m.get("receipt") or "")
        # A receipt is the proof the mail landed. No receipt -> no claim.
        receipt_line = ('<span class="mail-receipt">Delivered · receipt %s</span>'
                        % esc(receipt)) if receipt else \
            '<span class="mail-receipt mail-receipt-missing">Sent — receipt pending</span>'
        items.append(
            '<li class="mail-sent"><span class="mail-sent-subject">%s</span>'
            '<span class="mail-sent-to">%s</span>%s</li>'
            % (esc(str(m.get("subject") or "(no subject)")),
               esc(", ".join(str(t) for t in (m.get("to") or []))),
               receipt_line))
    if not items:
        return '<p class="mail-empty">Nothing delivered yet.</p>'
    return '<ul class="mail-mailbox">%s</ul>' % "".join(items)


def _send_block(allowed, missing):
    """The connected action: a live send form only when authorized,
    otherwise an honest gated block naming what is missing. The two are
    visually distinct and the verifier asserts data-consent honesty."""
    if allowed:
        return (
            '<div class="mail-send" data-consent="connected" '
            'data-send-grant="network">'
            '<button type="submit" class="mail-send-btn">Send</button>'
            '<button type="button" class="mail-broadcast-btn">Broadcast</button>'
            '<div class="mail-receipts" data-receipt-events='
            '"mail.send.accepted mail.send.failed">'
            '<span class="mail-receipts-note">Delivery receipts are '
            'recorded for every send.</span></div>'
            '</div>')
    reasons = "".join("<li>%s</li>" % esc(r) for r in missing)
    return (
        '<div class="mail-send mail-send-gated" data-consent="ready">'
        '<p class="mail-gated-title">Send is ready but off.</p>'
        '<p class="mail-gated-why">To send mail, this page needs:</p>'
        '<ul class="mail-gated-list">%s</ul>'
        '<p class="mail-gated-note">Connect to enable — the feature stays '
        'honest: composing and drafts work now, sending waits for the grant.</p>'
        '</div>' % reasons)


def render_smart_mail(decl, registry_status, context=None):
    """Render the Smart Mail panel. Returns '' when the contract did not
    declare smart_mail; raises SmartMailRefusal otherwise.

    registry_status: the registry's status string for feature.smart_mail.
    Rendering is proof the registry says 'built' — the page carries
    data-mail-status="built" as the binding.
    context: resolved contract context {'connections': {...}, 'privacy': ...,
    'granted_permissions': [...], 'available': [...], 'identity': {...}}.
    """
    if decl is None or not decl.get("enabled"):
        return ""  # not declared -> refuse to render mail
    if registry_status != "built":
        raise SmartMailRefusal(
            "feature_not_built",
            "contract declares smart_mail but registry status is %r "
            "(contract never activates an unbuilt capability)" % (registry_status,))

    to_line, subject, body = _draft_fields(decl)
    allowed, missing = can_send(context)

    # data-consent on the panel mirrors the assembler contract: "connected"
    # ONLY when a grant-active connected action renders; else "ready".
    consent_word = "connected" if allowed else "ready"
    return (
        '<section class="smart-mail" data-feature="smart_mail" '
        'data-mail-status="built" data-consent="%s">'
        '<h2 class="mail-title">Smart Mail</h2>'
        '<div class="mail-compose"><h3>Compose</h3>'
        '<form class="mail-form" onsubmit="return false">'
        '<label>To<input type="text" name="to" value="%s"></label>'
        '<label>Subject<input type="text" name="subject" value="%s"></label>'
        '<label>Message<textarea name="body">%s</textarea></label>'
        '</form></div>'
        '<div class="mail-drafts-pane"><h3>Drafts</h3>%s</div>'
        '<div class="mail-mailbox-pane"><h3>Mailbox</h3>%s</div>'
        '%s'
        '</section>'
        % (consent_word, esc(to_line), esc(subject), esc(body),
           _drafts_html(decl), _mailbox_html(decl), _send_block(allowed, missing))
    )
