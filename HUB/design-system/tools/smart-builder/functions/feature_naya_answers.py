#!/usr/bin/env python3
"""feature.naya_answers — "Ask Naya" (Smart Builder feature breaker).

Capability contract (functions/registry.json):
  id: feature.naya_answers, version 1.0.0, status tracked in the registry.
  activated_by: contract.features.naya_answers — the CONTRACT flips the breaker;
  the module never hand-wires itself into a page.
  requires: authenticated_identity, github_kb_sync, answer_service
  permissions: answers.ask
  events: answers.asked, answers.answered, answers.failed (runtime — the
  answer service fires them; the build fires nothing).

Activation input (from the contract):
  contract.features.naya_answers = {
      "enabled": true,
      "kb_source": "the owner's GitHub knowledge base",   # contract-declared
      "kb_ref": "SoulSchoolAcademy/NayaPOWER",            # optional text ref
      "answers_endpoint": "https://... (answer service, optional)",
      "greeting": "Ask me anything about this page.",     # optional
      "placeholder": "Type your question...",             # optional
      "unknown_message": "She doesn't know that one yet..."  # optional
  }

Honest scope (the anti-fabrication law):
  - The module NEVER answers questions and NEVER carries canned answers.
    It renders the Ask Naya widget bound to the contract-declared knowledge
    source and the contract-declared answer endpoint. The answering is done
    at runtime by the answer service, against the owner's KB only.
  - The "don't know" path is required: the widget always declares
    data-unknown-message (contract-overridable, honest default), and the
    runtime must show it — or the service's own structured unknown — rather
    than invent an answer. Refusing to know is a feature, tested below.
  - No answer endpoint declared -> the widget renders in DISCONNECTED state:
    visible, disabled, honest about what's missing. Never a dead control
    pretending to work (Shawn's function law).

Behavior (three-state, Shawn's 21:32Z default-on rule):
  - Omitted -> assembler policy (naya_answers is not a standard feature,
    so omitted = off). The module never hardcodes a default.
  - Explicit false -> off: no render, no claim.
  - Explicit true + registry built -> the ask widget (or the honest
    connect/disconnected states below).
  - Declared + registry says anything else -> NayaAnswersRefusal('feature_not_built').
    The contract never advertises a capability as operational unless the
    registry says it is built.
  - GitHub connection missing -> "connect GitHub to enable" panel, never
    a staged question box (Shawn's 21:34Z day-one rule).
  - Unsafe answers_endpoint -> NayaAnswersRefusal('unsafe_answers_endpoint'),
    fail closed. Allowed: absolute http(s) URLs only (an answer service is
    an HTTP endpoint; data: makes no sense here).

Stdlib only. Pure functions — same declaration -> same bytes, always.
"""
import html as htmlmod
from urllib.parse import urlparse

VERSION = "1.0.0"
FEATURE_ID = "feature.naya_answers"
# aliases the assembler imports
FEATURE_NAYA_ANSWERS_ID = FEATURE_ID
FEATURE_NAYA_ANSWERS_VERSION = VERSION

DEFAULT_KB_SOURCE = "the owner's knowledge base"

# Connections (Shawn's 21:34Z day-one rule), refined 21:41Z into the
# READY vs CONNECTED split:
#   ready     = local Ask widget shell: KB source named, don't-know path
#               declared, honest connect panel. No questions leave the page.
#   connected = live answers from the owner's GitHub KB via the declared
#               answer service. Requires the grant below.
# Declaring answers_endpoint is an explicit CONNECTED demand: without the
# grant it is a structured grant_required refusal, never a silent
# downgrade (never conflate ready with connected).
NEEDS_CONNECTION = "github"
GRANT = "connections.github"
READINESS = {
    "ready": "Local Ask widget shell: KB source named, don't-know path "
             "declared, honest connect panel. No questions leave the page.",
    "connected": "Live answers from the owner's GitHub knowledge base via "
                 "the declared answer service.",
    "grant": GRANT,
}


class NayaAnswersRefusal(Exception):
    """Structured refusal: the Ask Naya breaker declined to activate.

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
    """Contract text: stripped, no control characters (except tab/newline),
    escaped at render. Refuses rather than smuggling control bytes."""
    t = str(s or "").strip()
    if any(ord(c) < 0x20 and c not in ("\t", "\n", "\r") for c in t):
        raise NayaAnswersRefusal("bad_naya_answers_declaration",
                                 "%s: control characters in text" % field)
    return t


def sanitize_endpoint(url, field):
    """Allowlist the answer-service endpoint. Returns the cleaned URL, None
    when absent, raises NayaAnswersRefusal('unsafe_answers_endpoint') for
    anything hostile. Absolute http(s) only — the answer service is a real
    HTTP endpoint, never a data: URL or a relative path."""
    if url is None:
        return None
    if not isinstance(url, str):
        raise NayaAnswersRefusal("unsafe_answers_endpoint",
                                 "%s: not a string (%s)"
                                 % (field, type(url).__name__))
    u = url.strip()
    if not u:
        return None
    if any(ord(c) < 0x20 for c in u):
        raise NayaAnswersRefusal("unsafe_answers_endpoint",
                                 "%s: control characters in URL" % field)
    p = urlparse(u)
    scheme = (p.scheme or "").lower()
    if scheme in ("http", "https"):
        if not p.hostname:
            raise NayaAnswersRefusal("unsafe_answers_endpoint",
                                     "%s: %s URL has no host" % (field, scheme))
        if any(c.isspace() for c in p.hostname):
            raise NayaAnswersRefusal("unsafe_answers_endpoint",
                                     "%s: whitespace in host" % field)
        return u
    reason = "relative URLs are not allowed" if not scheme \
        else "disallowed scheme %r (answer service must be http(s))" % p.scheme
    raise NayaAnswersRefusal("unsafe_answers_endpoint",
                             "%s: %s" % (field, reason))


def decl_for(contract):
    """Extract the naya_answers declaration from a contract, or None.

    Three-state interface (Shawn's 21:32Z default-on rule):
      - features not a dict (contract-page) -> None: no breakers at all.
      - key absent from the features dict -> None: OMITTED. The assembler
        applies its policy (registry-marked standard features default on);
        the module never hardcodes a default.
      - True -> {"enabled": True}: explicit ON.
      - dict -> itself: explicit; on iff decl.get("enabled") is truthy.
      - other falsy (False/None/0/"") -> {"enabled": False}: explicit OFF.
        Off renders nothing and claims nothing.
      - other truthy -> NayaAnswersRefusal('bad_naya_answers_declaration').
    """
    feats = contract.get("features") if isinstance(contract, dict) else None
    if not isinstance(feats, dict):
        return None  # contract-page contracts carry features as a list
    if "naya_answers" not in feats:
        return None  # omitted -> assembler policy applies
    decl = feats["naya_answers"]
    if decl is True:
        return {"enabled": True}
    if isinstance(decl, dict):
        return decl
    if not decl:
        return {"enabled": False}  # explicit off: no render, no claim
    raise NayaAnswersRefusal("bad_naya_answers_declaration",
                             "contract.features.naya_answers must be an object, "
                             "true, or false, got %s" % type(decl).__name__)


def granted(ctx):
    """The grant: contract.connections.github == true (strict)."""
    conns = (ctx or {}).get("connections", {}) or {}
    return conns.get(NEEDS_CONNECTION) is True


def mode_for(decl, ctx):
    """READY vs CONNECTED for this declaration: connected only when the
    contract demands live answers (a SANITIZED answers_endpoint) AND holds
    the grant. Sanitizing here (not just truthiness) keeps data-mode
    honest against what render actually wires — never conflate."""
    try:
        ep = sanitize_endpoint((decl or {}).get("answers_endpoint"),
                               "answers_endpoint")
    except NayaAnswersRefusal:
        return "ready"
    return "connected" if (ep and granted(ctx)) else "ready"


def unknown_message_for(decl):
    """The required don't-know path: contract-overridable, honest default.
    The widget always declares it; the runtime shows it rather than
    inventing an answer."""
    kb = clean_text(decl.get("kb_source"), "kb_source") or DEFAULT_KB_SOURCE
    custom = decl.get("unknown_message")
    if custom is None:
        return ("She doesn't know that one yet — it's not in %s. "
                "Try rephrasing, or ask the owner." % kb)
    return clean_text(custom, "unknown_message")


def render_naya_answers(decl, registry_status, context=None):
    """Render the Ask Naya widget. Returns '' when the contract did not
    declare naya_answers (omitted non-standard, explicit off, or disabled);
    raises NayaAnswersRefusal otherwise.

    registry_status: the registry's status string for feature.naya_answers.
    context: {"connections": {...}, "privacy": ...} from the assembler.

    Connections: without the GitHub connection the widget renders an
    honest "connect to enable" panel — enabled != available, never staged.
    """
    if decl is None or not decl.get("enabled"):
        return ""  # not declared / explicit off -> no render, no claim
    if registry_status != "built":
        raise NayaAnswersRefusal(
            "feature_not_built",
            "contract declares naya_answers but registry status is %r "
            "(contract never activates an unbuilt capability)"
            % (registry_status,))

    is_granted = granted(context)
    kb_source = clean_text(decl.get("kb_source"), "kb_source") \
        or DEFAULT_KB_SOURCE
    endpoint = sanitize_endpoint(decl.get("answers_endpoint"),
                                 "answers_endpoint")

    if endpoint and not is_granted:
        # Explicit CONNECTED demand without the grant: structured refusal
        # naming the grant. Never silently downgrade connected to ready.
        raise NayaAnswersRefusal(
            "grant_required",
            "live answers (connected) require grant %s — connect GitHub, "
            "or remove answers_endpoint to render the ready shell" % GRANT)

    if not is_granted:
        # Honest, not staged: no question box until GitHub is connected.
        return (
            '<section class="ask-naya ask-naya-connect" data-feature="naya_answers" '
            'data-naya-answers-status="built" data-mode="ready" '
            'data-grant="connections.github" data-needs-connection="github" '
            'data-kb-source="%s">'
            '<div class="ask-head"><h2>Ask Naya</h2></div>'
            '<p class="ask-connect">Ask Naya answers from %s — '
            '<b>connect GitHub to enable it.</b> Nothing here is staged: '
            'the question box appears once it\u2019s connected.</p>'
            '</section>' % (esc(kb_source), esc(kb_source))
        )

    kb_ref = clean_text(decl.get("kb_ref"), "kb_ref")
    greeting = clean_text(decl.get("greeting"), "greeting")
    placeholder = clean_text(decl.get("placeholder"), "placeholder") \
        or "Type your question..."
    unknown = unknown_message_for(decl)

    mode = "connected" if endpoint else "ready"
    data_attrs = (
        'data-mode="%s" data-grant="%s" '
        'data-kb-source="%s" data-unknown-message="%s"%s'
        % (mode, esc(GRANT), esc(kb_source), esc(unknown),
           ' data-kb-ref="%s"' % esc(kb_ref) if kb_ref else "")
    )
    kb_line = ('<p class="ask-kb">Answers come from %s — she never invents them.</p>'
               % esc(kb_source))
    head = ('<div class="ask-head"><h2>Ask Naya</h2>%s%s</div>'
            % (('<p class="ask-greet">%s</p>' % esc(greeting)) if greeting else "",
               kb_line))

    if endpoint:
        # Wired: a real form posting to the contract-declared answer
        # service. Works without JS (progressive enhancement); the runtime
        # upgrades it in place and fills .ask-answer. The service answers
        # from the owner's KB only and must surface the don't-know path
        # instead of fabricating.
        body = (
            '<form class="ask-form" method="post" action="%s">'
            '<label class="ask-label" for="ask-q">Your question</label>'
            '<div class="ask-row">'
            '<input id="ask-q" name="q" type="text" required maxlength="500" '
            'placeholder="%s" autocomplete="off">'
            '<button type="submit" class="naya-btn ask-btn">'
            '<span class="nb-label">Ask</span></button></div></form>'
            '<div class="ask-answer" role="status" aria-live="polite"></div>'
            % (esc(endpoint), esc(placeholder))
        )
        cls = "ask-naya"
        data_attrs += ' data-answer-endpoint="%s"' % esc(endpoint)
    else:
        # Disconnected: visible, disabled, honest. No dead control.
        body = (
            '<p class="ask-off">Ask Naya isn\u2019t connected yet \u2014 the owner '
            'hasn\u2019t linked an answer service. Nothing here is fake: the box '
            'below stays disabled until it\u2019s wired.</p>'
            '<form class="ask-form" aria-disabled="true">'
            '<div class="ask-row">'
            '<input type="text" disabled placeholder="%s" aria-label="Ask Naya (not connected)">'
            '<button type="submit" class="naya-btn ask-btn" disabled>'
            '<span class="nb-label">Ask</span></button></div></form>'
            % esc("Ask Naya is not connected yet")
        )
        cls = "ask-naya ask-naya-off"

    return (
        '<section class="%s" data-feature="naya_answers" '
        'data-naya-answers-status="built" %s>%s%s</section>'
        % (cls, data_attrs, head, body)
    )
