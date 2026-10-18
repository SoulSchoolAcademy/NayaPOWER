#!/usr/bin/env python3
"""feature.naya_answers — "Naya answers" (Smart Builder feature breaker).

Capability contract (functions/registry.json):
  id: feature.naya_answers, version 1.0.0, status tracked in the registry.
  activated_by: contract.features.naya_answers — the CONTRACT flips the
  breaker; the module never hand-wires itself into a page.
  depends_on: ["systems.github_kb"]
  requires: authenticated_identity, github_kb_sync, answer_service
  permissions: answers.ask (asking is a permission question)
  events: answers.asked, answers.answered, answers.failed
  acceptance: answer_uses_owner_kb, unknown_question_handled,
              failure_state_visible
  connected: [{action: "answer via Muse", grant: "muse"}]
  ready: ask UI

Activation input (from the contract, which carries the intake's data):
  contract.features.naya_answers = {
      "enabled": True,
      "kb_answers": [
          {"question": "When is the next launch?",
           "answer": "The next launch is Friday at 9am."},
      ]
  }
  kb_answers: list of {question, answer} pairs — the answers the owner's
  GitHub knowledge-base sync carried into the contract. The module renders
  ONLY these answers, byte-identical: an answer the contract did not
  declare is an answer the page does not show. The owner syncs the KB;
  the page never invents.
  question: non-empty string (required — an answer needs its question).
  answer: non-empty string (required — a blank answer is a lie about
  knowing).

Behavior:
  - Not declared (or enabled falsy) -> render nothing. The page refuses
    to render answers the contract did not declare.
  - Declared + registry says anything else -> NayaAnswersRefusal(
    'feature_not_built'). The contract never advertises a capability as
    operational unless the registry says it is built.
  - answer_uses_owner_kb: every rendered answer is byte-identical to the
    declared KB entry, HTML-escaped. An answer that the declaration lists
    but the page paraphrases is an answer the owner cannot trust.
  - unknown_question_handled: a declared ask (contract asks a question
    with no KB entry) renders an honest "not yet known" line naming the
    question — never a faked answer. The KB sync is the source; gaps are
    said out loud.
  - failure_state_visible: when the answer service is down (context flag),
    the panel renders a visible failure note — never a silent empty panel,
    never a stale answer presented as live.
  - Asking is a permission question: without the answers.ask permission
    the ask box renders an honest gated block naming the permission in
    human words. Never a dead ask button, never silent answer text.
  - The "answer via Muse" action is the connected action (grant: muse —
    strict boolean, the consent-line refinement): the live answer
    affordance renders ONLY when the muse connection is ON. Otherwise an
    honest gated block names exactly what is missing in human words.
  - Receipt hooks -> the panel carries data-receipt-events with the
    registry's own events (answers.asked, answers.answered,
    answers.failed) so the runtime can persist receipts. A claim of
    "answered" without a receipt is a hope.
  - Answers are local to the declaration (ready: "ask UI"): the rendered
    answers come from the contract's own kb_answers (the owner KB sync).
    There is no remote fetch, no invented Q&A, no seeded strangers.

Judgment, named: the resolver enforces the three requirements
(authenticated_identity, github_kb_sync, answer_service) and the
answers.ask permission BEFORE this module is ever called — resolve()
fails closed on requirement_unmet / permission_denied with the human
words. Inside the module, the muse grant is the finer control (the
connected action), checked with the strict boolean the connect module
uses. The ask box is always askable-or-honest; the live answer is
grant-gated. data-consent is "connected" ONLY on the live answer
affordance; every other surface says "ready". The verifier asserts this.

Acceptance (registry: answer_uses_owner_kb, unknown_question_handled,
failure_state_visible) is exercised in
functions/tests/test_feature_naya_answers.py.

Stdlib only. Pure functions — same declaration + same context -> same
bytes, always.
"""
import html as htmlmod

VERSION = "1.0.0"
FEATURE_ID = "feature.naya_answers"
# aliases the assembler imports
FEATURE_NAYA_ANSWERS_ID = FEATURE_ID
FEATURE_NAYA_ANSWERS_VERSION = VERSION

# Asking is a permission question. The human words match the resolver's
# PERMISSION_EXPLAIN['answers.ask'] byte-for-byte — two surfaces, one truth.
ASK_PERMISSION = "answers.ask"
ASK_PERMISSION_HUMAN = "ask Naya questions against your knowledge base"

# The connected action's grant: strict boolean, the consent-line
# refinement. The human words match the connect module's GRANT_WORDS.
ANSWER_GRANT = "muse"
ANSWER_GRANT_HUMAN = "the Muse connection switched on for this page"


class NayaAnswersRefusal(Exception):
    """Structured refusal: the naya_answers breaker declined to activate.

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


def sanitize_qa(qa):
    """Validate one Q&A pair. Returns {'question', 'answer'}.
    Raises NayaAnswersRefusal('bad_qa') for anything malformed — an
    answers panel that swallows a bad pair silently is a panel that
    cannot be trusted."""
    if not isinstance(qa, dict):
        raise NayaAnswersRefusal(
            "bad_qa",
            "each Q&A must be an object, got %s" % type(qa).__name__)
    question = qa.get("question")
    if not _nonempty_str(question):
        raise NayaAnswersRefusal(
            "bad_qa",
            "Q&A needs a non-empty string question, got %r" % (question,))
    answer = qa.get("answer")
    if not _nonempty_str(answer):
        raise NayaAnswersRefusal(
            "bad_qa",
            "Q&A needs a non-empty string answer, got %r" % (answer,))
    return {"question": question.strip(), "answer": answer.strip()}


def decl_for(contract):
    """Extract the naya_answers declaration from a contract, or None.

    Accepts the PLUMBING.md breaker convention
    (contract.features.naya_answers):
      - dict  -> the declaration (task shape: enabled/kb_answers)
      - True  -> enabled with empty fields
      - falsy / absent / features-not-a-dict -> None (not declared)
      - anything else truthy -> NayaAnswersRefusal(
        'bad_naya_answers_declaration')
    """
    feats = contract.get("features") if isinstance(contract, dict) else None
    if not isinstance(feats, dict):
        return None  # contract-page contracts carry features as a list
    if "naya_answers" not in feats:
        return None
    decl = feats["naya_answers"]
    if not decl:
        return None
    if decl is True:
        return {"enabled": True}
    if isinstance(decl, dict):
        return decl
    raise NayaAnswersRefusal(
        "bad_naya_answers_declaration",
        "contract.features.naya_answers must be an object or true, "
        "got %s" % type(decl).__name__)


def _granted_permissions(context):
    ctx = context or {}
    return list(ctx.get("granted_permissions") or [])


def can_ask(context):
    """Evaluate the ask authorization. Returns (allowed, missing):
    allowed only when answers.ask is granted. Asking is the permission
    question; the LIVE answer is the connection question (muse grant)."""
    missing = []
    granted = _granted_permissions(context)
    if ASK_PERMISSION not in granted:
        missing.append(ASK_PERMISSION_HUMAN)
    return (len(missing) == 0, missing)


def can_answer_live(context):
    """The connected action fires ONLY on the recorded muse grant —
    strict boolean, the consent-line refinement."""
    return (context or {}).get("connections", {}).get(
        ANSWER_GRANT) is True


def _qa_html(qa):
    """Render one Q&A pair: byte-identical content, HTML-escaped (XSS
    probe territory). The caller guarantees the pair passed sanitize_qa.
    answer_uses_owner_kb is literal here — the rendered answer IS the
    declared KB text, unchanged."""
    return (
        '<article class="naya-answers-qa">'
        '<p class="naya-answers-question">%s</p>'
        '<p class="naya-answers-answer">%s</p>'
        '</article>' % (esc(qa["question"]), esc(qa["answer"])))


def _ask_box_html(context):
    """The ask UI: askable when answers.ask is granted, otherwise an
    honest gated block naming the permission. Never a dead ask button,
    never silent answer text. data-consent stays 'ready' — the ask is
    not the connected action."""
    allowed, missing = can_ask(context)
    if allowed:
        return (
            '<div class="naya-answers-ask" data-consent="ready">'
            '<label class="naya-answers-label">Ask Naya</label>'
            '<input type="text" class="naya-answers-input" '
            'placeholder="Ask about this page" />'
            '<button type="button" class="naya-answers-btn">Ask</button>'
            '</div>')
    reasons = "".join("<li>%s</li>" % esc(r) for r in missing)
    return (
        '<div class="naya-answers-ask naya-answers-gated" '
        'data-consent="ready">'
        '<p class="naya-answers-gated-title">Asking is ready but off.</p>'
        '<p class="naya-answers-gated-why">To ask questions, the page '
        'needs:</p>'
        '<ul class="naya-answers-gated-list">%s</ul>'
        '<p class="naya-answers-gated-note">The answers below stay readable; '
        'asking waits for the permission.</p>'
        '</div>' % reasons)


def _live_answer_html(context):
    """The connected action: a live 'answer via Muse' affordance ONLY
    when the muse connection is strictly True. Otherwise an honest gated
    block naming the connection in human words. Never a dead button."""
    if can_answer_live(context):
        return (
            '<div class="naya-answers-live" data-consent="connected" '
            'data-answers-grant="muse">'
            '<button type="button" class="naya-answers-live-btn">'
            'Answer via Muse</button>'
            '<div class="naya-answers-receipts" data-receipt-events='
            '"answers.asked answers.answered answers.failed">'
            '<span class="naya-answers-receipts-note">Receipts are recorded '
            'for every question asked and answered.</span></div>'
            '</div>')
    return (
        '<div class="naya-answers-live naya-answers-gated" '
        'data-consent="ready">'
        '<p class="naya-answers-gated-title">Live answers are ready but '
        'off.</p>'
        '<p class="naya-answers-gated-why">For live answers the page '
        'needs: %s.</p>'
        '<p class="naya-answers-gated-note">Saved answers still show '
        'above; live answering waits for the connection.</p>'
        '</div>' % esc(ANSWER_GRANT_HUMAN))


def _unknown_html(question):
    """unknown_question_handled: a declared ask with no KB entry says the
    gap out loud — never a faked answer."""
    return (
        '<p class="naya-answers-unknown">Naya doesn\'t have an answer to '
        '"%s" in the owner\'s knowledge base yet — ask the owner, and '
        'syncing the knowledge base will teach it.</p>'
        % esc(question))


def render_naya_answers(decl, registry_status, context=None):
    """Render the Naya answers panel. Returns '' when the contract did not
    declare naya_answers; raises NayaAnswersRefusal otherwise.

    registry_status: the registry's status string for feature.naya_answers.
    Rendering is proof the registry says 'built' — the section carries
    data-naya-answers-status="built" as the binding.
    context: resolved contract context {'connections': {...}, 'privacy': ...,
    'granted_permissions': [...], 'available': [...], 'identity': {...},
    'service_down': bool, 'pending_question': str}.
    """
    if decl is None or not decl.get("enabled"):
        return ""  # not declared -> refuse to render answers
    if registry_status != "built":
        raise NayaAnswersRefusal(
            "feature_not_built",
            "contract declares naya_answers but registry status is %r "
            "(contract never activates an unbuilt capability)"
            % (registry_status,))

    # failure_state_visible: a down answer service is said, never silent.
    if (context or {}).get("service_down") is True:
        return (
            '<section class="naya-answers" data-feature="naya_answers" '
            'data-naya-answers-status="failed" data-consent="ready">'
            '<h2 class="naya-answers-title">Naya answers</h2>'
            '<p class="naya-answers-failure">The answer service is down — '
            'saved answers are hidden until it recovers, so nothing stale '
            'shows as live.</p>'
            '</section>')

    kb = [sanitize_qa(q) for q in (decl.get("kb_answers") or [])]
    if not kb:
        body = ('<p class="naya-answers-empty">No synced answers yet — '
                'sync the owner\'s knowledge base and the answers appear '
                'here.</p>')
    else:
        body = "".join(_qa_html(q) for q in kb)

    # unknown_question_handled: a pending ask with no KB entry is named.
    pending = (context or {}).get("pending_question")
    unknown = ""
    if pending and _nonempty_str(pending):
        known = any(q["question"].strip().lower() == pending.strip().lower()
                    for q in kb)
        if not known:
            unknown = _unknown_html(pending.strip())

    return (
        '<section class="naya-answers" data-feature="naya_answers" '
        'data-naya-answers-status="built" data-consent="ready">'
        '<h2 class="naya-answers-title">Naya answers</h2>'
        '<div class="naya-answers-kb" data-receipt-events='
        '"answers.asked answers.answered answers.failed">%s</div>%s%s%s'
        '</section>' % (body, unknown, _ask_box_html(context),
                        _live_answer_html(context)))
