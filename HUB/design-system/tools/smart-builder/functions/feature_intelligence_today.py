#!/usr/bin/env python3
"""feature.intelligence_today — "Intelligence Today" (Smart Builder feature breaker).

Capability contract (functions/registry.json):
  id: feature.intelligence_today, version 1.0.0, status tracked in the registry.
  activated_by: contract.features.intelligence_today — the CONTRACT flips the
  breaker; the module never hand-wires itself into a page.
  depends_on: systems.reports
  requires: authenticated_identity, report_pipeline, data_authorization
  permissions: reports.read (reading report bodies is a permission question)
  events: reports.generated, reports.viewed
  acceptance: only_own_data_shown, report_renders, empty_state_handled
  connected: the ONLY connected action is "sync intelligence"
             (grant: muse — strict boolean, the consent-line refinement).

Activation input (from the contract, which carries the intake's data):
  contract.features.intelligence_today = {
      "enabled": True,
      "reports": [
          {"title": "Your Tuesday briefing", "period": "daily",
           "owner": "shawn", "summary": "3 things moved today.",
           "generated": "2026-10-17"},
      ]
  }
  period: 'daily' | 'weekly' | 'monthly' | 'yearly' (required).
  owner: the identity id that owns the report (required — acceptance:
  only_own_data_shown). summary: optional body text. generated: optional.

Behavior:
  - Not declared (or enabled falsy) -> render nothing. The page refuses
    to render reports the contract did not declare.
  - Declared + registry says anything else -> IntelligenceTodayRefusal(
    'feature_not_built'). The contract never advertises a capability as
    operational unless the registry says it is built.
  - only_own_data_shown: the panel renders ONLY reports whose owner
    matches context['identity']['id']. Another identity's report never
    appears — not its title, not its body, not a gated teaser. Without
    an identity, no report bodies render at all (honest sign-in line).
  - Report bodies are a permission question: with the reports.read
    permission granted the viewer's own reports render full; without it
    an honest gated block names the permission in human words. Never a
    dead panel, never silent.
  - Empty (declared, zero reports) -> an honest empty line, never an
    empty section, never a crash, never a fake report (empty_state_handled).
  - The connected action: a live "Sync intelligence" button ONLY when
    the muse connection is strictly True (grant, not truthy). Otherwise
    an honest gated block naming the connection. Message is to connect
    what sync is to intelligence: grant-gated, never dead.
  - Malformed reports (missing/blank title, bad period, bad owner,
    wrong shape, bad summary) -> IntelligenceTodayRefusal(
    'bad_intelligence_report'), never silently dropped.
  - Receipt hooks -> the panel carries data-receipt-events with the
    registry's own events (reports.generated, reports.viewed) so the
    runtime can persist receipts. A claim of "generated" without a
    receipt is a hope.

Judgment, named: the report READ is a permission question (reports.read)
and the SYNC is a connection question (muse grant, strict boolean) —
the same grant/permission split the connect module draws between its
message action (grant) and its request flow (permissions). Ownership is
the finest control of all: it is checked before either gate, because a
panel that leaks another identity's report under a granted permission
is a panel that cannot be trusted.

Acceptance (registry: only_own_data_shown, report_renders,
empty_state_handled) is exercised in
functions/tests/test_feature_intelligence_today.py.

Stdlib only. Pure functions — same declaration + same context -> same
bytes, always.
"""
import html as htmlmod

VERSION = "1.0.0"
FEATURE_ID = "feature.intelligence_today"
# aliases the assembler imports
FEATURE_INTELLIGENCE_TODAY_ID = FEATURE_ID
FEATURE_INTELLIGENCE_TODAY_VERSION = VERSION

# The connected sync action fires only on this recorded grant
# (strict boolean — the consent-line refinement: grant = True, not truthy).
SYNC_GRANT = "muse"

# Reading report bodies is a permission question.
READ_PERMISSION = "reports.read"

PERIODS = ("daily", "weekly", "monthly", "yearly")

# Human words for the gates, so the gated block speaks plainly
# (same words the resolver uses).
GRANT_WORDS = {
    "muse": "the Muse connection switched on for this page",
    "reports.read": "your permission to read your reports",
    "authenticated_identity": "a signed-in identity for this page",
}


class IntelligenceTodayRefusal(Exception):
    """Structured refusal: the intelligence_today breaker declined to activate.

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


def sanitize_report(report):
    """Validate one intelligence report. Returns {'title', 'period',
    'owner', 'summary', 'generated'}. Raises
    IntelligenceTodayRefusal('bad_intelligence_report') for anything
    malformed — a report panel that swallows a bad report silently is a
    panel that cannot be trusted."""
    if not isinstance(report, dict):
        raise IntelligenceTodayRefusal(
            "bad_intelligence_report",
            "each report must be an object, got %s" % type(report).__name__)
    title = report.get("title")
    if not _nonempty_str(title):
        raise IntelligenceTodayRefusal(
            "bad_intelligence_report",
            "report needs a non-empty string title, got %r" % (title,))
    period = report.get("period")
    if period not in PERIODS:
        raise IntelligenceTodayRefusal(
            "bad_intelligence_report",
            "report period must be one of %s, got %r"
            % (list(PERIODS), period))
    owner = report.get("owner")
    if not _nonempty_str(owner):
        raise IntelligenceTodayRefusal(
            "bad_intelligence_report",
            "report needs a non-empty string owner (identity id), got %r"
            % (owner,))
    summary = report.get("summary")
    if summary not in (None,) and not isinstance(summary, str):
        raise IntelligenceTodayRefusal(
            "bad_intelligence_report",
            "report summary must be a string, got %s"
            % type(summary).__name__)
    generated = report.get("generated")
    if generated not in (None,) and not isinstance(generated, str):
        raise IntelligenceTodayRefusal(
            "bad_intelligence_report",
            "report generated must be a string, got %s"
            % type(generated).__name__)
    return {"title": title.strip(), "period": period,
            "owner": owner.strip(),
            "summary": summary.strip() if isinstance(summary, str)
            and summary.strip() else "",
            "generated": generated.strip() if isinstance(generated, str)
            and generated.strip() else ""}


def decl_for(contract):
    """Extract the intelligence_today declaration from a contract, or None.

    Accepts the PLUMBING.md breaker convention
    (contract.features.intelligence_today):
      - dict  -> the declaration (task shape: enabled/reports)
      - True  -> enabled with empty fields
      - falsy / absent / features-not-a-dict -> None (not declared)
      - anything else truthy -> IntelligenceTodayRefusal(
        'bad_intelligence_declaration')
    """
    feats = contract.get("features") if isinstance(contract, dict) else None
    if not isinstance(feats, dict):
        return None  # contract-page contracts carry features as a list
    if "intelligence_today" not in feats:
        return None
    decl = feats["intelligence_today"]
    if not decl:
        return None
    if decl is True:
        return {"enabled": True}
    if isinstance(decl, dict):
        return decl
    raise IntelligenceTodayRefusal(
        "bad_intelligence_declaration",
        "contract.features.intelligence_today must be an object or true, "
        "got %s" % type(decl).__name__)


def _viewer_id(context):
    """The signed-in viewer's identity id, or None. No identity means no
    personal data renders — fail closed on other people's reports."""
    ctx = context or {}
    ident = ctx.get("identity") or {}
    ident_id = ident.get("id")
    return ident_id if _nonempty_str(ident_id) else None


def can_read(context):
    """Evaluate the report-body read authorization.

    Returns (allowed, missing). allowed is True only when the
    reports.read permission was granted. This is a permission question
    (the read), not a connection question — the grant gates the sync
    action, the permission gates reading bodies.
    """
    missing = []
    ctx = context or {}
    granted = list(ctx.get("granted_permissions") or [])
    if READ_PERMISSION not in granted:
        missing.append(GRANT_WORDS[READ_PERMISSION])
    return (len(missing) == 0, missing)


def can_sync(context):
    """Evaluate the sync-intelligence authorization.

    Returns (allowed, missing). allowed is True only when the muse
    grant holds — strictly True. This is the connected action: syncing
    intelligence is a connection question, not a permission question.
    """
    missing = []
    ctx = context or {}
    connections = ctx.get("connections") or {}
    if connections.get(SYNC_GRANT) is not True:
        missing.append(GRANT_WORDS[SYNC_GRANT])
    return (len(missing) == 0, missing)


def _sync_block(context):
    """The connected action: a live sync button only when the muse grant
    holds strictly, otherwise an honest gated block naming the
    connection. Never a dead button."""
    allowed, missing = can_sync(context)
    if allowed:
        return (
            '<div class="intel-sync" data-consent="connected" '
            'data-sync-grant="muse">'
            '<button type="button" class="intel-sync-btn">'
            'Sync intelligence</button>'
            '<div class="intel-receipts" data-receipt-events='
            '"reports.generated reports.viewed">'
            '<span class="intel-receipts-note">Receipts are recorded for '
            'every generated and viewed report.</span></div>'
            '</div>')
    reasons = "".join("<li>%s</li>" % esc(r) for r in missing)
    return (
        '<div class="intel-sync intel-sync-gated" data-consent="ready">'
        '<p class="intel-gated-title">Sync is ready but off.</p>'
        '<p class="intel-gated-why">To sync intelligence, the page needs:</p>'
        '<ul class="intel-gated-list">%s</ul>'
        '<p class="intel-gated-note">Your reports stay put — sync waits '
        'for the grant.</p>'
        '</div>' % reasons)


def _report_html(report):
    """Render one owned report card. The caller guarantees ownership —
    this function never decides who may see what."""
    card = ('<article class="intel-report" data-period="%s">'
            '<h3 class="intel-report-title">%s</h3>' % (esc(report["period"]),
                                                       esc(report["title"])))
    if report["generated"]:
        card += ('<p class="intel-report-generated">Generated %s</p>'
                 % esc(report["generated"]))
    if report["summary"]:
        card += ('<p class="intel-report-summary">%s</p>'
                 % esc(report["summary"]))
    return card + '</article>'


def render_intelligence_today(decl, registry_status, context=None):
    """Render the intelligence-today panel. Returns '' when the contract
    did not declare intelligence_today; raises IntelligenceTodayRefusal
    otherwise.

    registry_status: the registry's status string for
    feature.intelligence_today. Rendering is proof the registry says
    'built' — the panel carries data-intel-status="built" as the binding.
    context: resolved contract context {'connections': {...}, 'privacy': ...,
    'granted_permissions': [...], 'available': [...], 'identity': {'id': ...}}.
    """
    if decl is None or not decl.get("enabled"):
        return ""  # not declared -> refuse to render reports
    if registry_status != "built":
        raise IntelligenceTodayRefusal(
            "feature_not_built",
            "contract declares intelligence_today but registry status is %r "
            "(contract never activates an unbuilt capability)"
            % (registry_status,))

    reports = [sanitize_report(r) for r in (decl.get("reports") or [])]
    viewer = _viewer_id(context)
    if viewer is None:
        # No identity: no personal data renders, ever. The panel stays
        # honest about why.
        return (
            '<section class="intel-today" data-feature="intelligence_today" '
            'data-intel-status="built" data-consent="ready">'
            '<h2 class="intel-title">Intelligence Today</h2>'
            '<p class="intel-no-identity">Sign in to see your reports — '
            'reports belong to an identity, and no identity is signed in '
            'on this page.</p>'
            '</section>')

    own = [r for r in reports if r["owner"] == viewer]
    readable, _ = can_read(context)
    sync_live, _ = can_sync(context)

    # data-consent mirrors the assembler contract: "connected" ONLY when
    # the grant-active sync affordance renders; else "ready".
    consent_word = "connected" if sync_live else "ready"
    panel = ('<section class="intel-today" data-feature="intelligence_today" '
             'data-intel-status="built" data-consent="%s">'
             '<h2 class="intel-title">Intelligence Today</h2>' % consent_word)
    if not own:
        panel += ('<p class="intel-empty">No reports yet — your first '
                  'briefing lands here.</p>')
    elif readable:
        panel += ('<div class="intel-reports">%s</div>'
                  % "".join(_report_html(r) for r in own))
    else:
        panel += (
            '<div class="intel-read-gated" data-consent="ready">'
            '<p class="intel-gated-title">Your reports are ready but private.</p>'
            '<p class="intel-gated-why">To read your reports, the page needs:</p>'
            '<ul class="intel-gated-list"><li>%s</li></ul>'
            '<p class="intel-gated-note">Nothing is shown until you grant it.</p>'
            '</div>' % esc(GRANT_WORDS[READ_PERMISSION]))
    panel += _sync_block(context)
    return panel + '</section>'
