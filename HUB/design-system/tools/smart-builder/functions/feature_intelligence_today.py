#!/usr/bin/env python3
"""feature.intelligence_today — "Intelligence Today" (Smart Builder feature breaker).

Capability contract (functions/registry.json):
  id: feature.intelligence_today, version 1.0.0, status tracked in the registry.
  activated_by: contract.features.intelligence_today — the CONTRACT flips the
  breaker; the module never hand-wires itself into a page.

Activation input (from the contract, which carries the owner's report data):
  contract.features.intelligence_today = {
      "enabled": true,
      "title": "Intelligence Today (optional)",
      "external_sources": true (optional, CONNECTED — see below),
      "reports": [
          {"period": "daily", "label": "Today", "summary": "...",
           "generated_at": "2026-10-17 (optional free text)",
           "metrics": [{"label": "Smart notes", "value": "12"}, ...]},
          ...
      ]
  }

Behavior (THREE-STATE interface — Shawn's product rule 21:32Z,
default-on, opt-out):
  - Explicit true (true, or {"enabled": truthy}) -> ON: report cards HTML.
  - Explicit false (false, {"enabled": falsy}, or any other present-but-
    falsy value) -> OFF: no render, no claim, no refusal.
  - Omitted (key absent, or features not a dict) -> the ASSEMBLER's
    default-on policy decides; the module hardcodes no default.
  - Declared + registry says built -> report cards HTML.
  - Declared + registry says anything else ->
    IntelligenceRefusal('feature_not_built'). The contract never advertises
    a capability as operational unless the registry says it is built.
  - only_own_data_shown is structural: the module performs no I/O and
    renders ONLY what the contract carries — the owner's own pipeline
    wrote that data; nothing else is reachable from here. Reports the
    contract does not carry are never invented.
  - Unknown periods -> IntelligenceRefusal('bad_intelligence_declaration'),
    fail closed. The declared vocabulary is daily/weekly/monthly/yearly.
  - Declared but reports absent/empty -> graceful fallback: the empty
    state ("No reports yet") — never a blank section, never invented data.
    (Day-one: {"enabled": true} alone renders a useful section, zero errors.)
  - All text is HTML-escaped; no URLs are emitted by this module at all.
  - Connections (contract["connections"]): this module performs no I/O
    and gates nothing on connections — reports render when enabled,
    connections or not. Feature enabled ≠ connection available.
    mistakes private reports for public ones.
  - READY vs CONNECTED (consent line, adopted 21:41Z) — carried in
    the capability contract as top-level "ready"/"connected" keys:
    READY (default): contract-carried reports — installed, working, no
    setup, no grant; renders with all connections false.
    CONNECTED: "external_sources": true -> fetch external report
    sources, needs contract.connections.network == true (explicit
    consent only). Without the grant -> grant_required refusal naming
    the grant; with the grant the fetch is still specified-not-built
    in this stdlib-only module -> connected_action_not_built. The
    build receipt mirrors the evaluated grants; UI copy never says
    "connected" when the module is merely ready.

Stdlib only. Pure functions — same declaration -> same bytes, always.
"""
import html as htmlmod

VERSION = "1.0.0"
FEATURE_ID = "feature.intelligence_today"
# aliases the assembler imports
FEATURE_INTELLIGENCE_TODAY_ID = FEATURE_ID
FEATURE_INTELLIGENCE_TODAY_VERSION = VERSION

REGISTRY_KEY = "intelligence_today"  # registry id minus the feature. prefix
SLOT = "intelligence_today"          # template slot %%INTELLIGENCE_TODAY%%
EVENT = "intelligence_today.updated"  # build-time event (F1: <breaker>.updated)

PERIODS = ("daily", "weekly", "monthly", "yearly")
MAX_METRICS = 12  # a report carrying more than this is malformed

PRIVACY_SCOPES = ("private", "network", "public")

GRANT_NAMES = ("muse", "github", "network", "nayanet")

# (declaration field, grant name, human description)
CONNECTED_ACTIONS = (
    ("external_sources", "network", "fetch external report sources"),
)


class IntelligenceRefusal(Exception):
    """Structured refusal: the intelligence-today breaker declined to activate.

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


def decl_for(contract):
    """Extract the intelligence-today declaration from a contract.

    THREE-STATE interface (Shawn's product rule 21:32Z — default-on,
    opt-out):
      - True -> {"enabled": True} (explicit ON)
      - dict -> the declaration as-is (enabled truthy -> ON,
        enabled falsy -> OFF)
      - False / 0 / "" / [] / any other present-but-falsy value ->
        False (explicit OFF — opt-out: no render, no claim)
      - key absent, or features not a dict -> None (OMITTED — the
        assembler's default-on policy decides; the module hardcodes
        no default)
      - anything else truthy ->
        IntelligenceRefusal('bad_intelligence_declaration')
    """
    feats = contract.get("features") if isinstance(contract, dict) else None
    if not isinstance(feats, dict):
        return None  # contract-page contracts carry features as a list
    if "intelligence_today" not in feats:
        return None
    decl = feats["intelligence_today"]
    if decl is True:
        return {"enabled": True}
    if isinstance(decl, dict):
        return decl
    if not decl:
        return False  # explicit opt-out
    raise IntelligenceRefusal(
        "bad_intelligence_declaration",
        "contract.features.intelligence_today must be an object, true, "
        "or false, got %s" % type(decl).__name__)


def reports_for(decl):
    """Sanitized report list: [(period, label, summary, generated_at,
    [(metric_label, metric_value), ...]), ...]. Raises IntelligenceRefusal
    on malformed entries."""
    raw = decl.get("reports")
    if raw is None:
        return []
    if not isinstance(raw, list):
        raise IntelligenceRefusal(
            "bad_intelligence_declaration",
            "reports must be a list, got %s" % type(raw).__name__)
    seen, out = set(), []
    for i, entry in enumerate(raw):
        field = "reports[%d]" % i
        if not isinstance(entry, dict):
            raise IntelligenceRefusal(
                "bad_intelligence_declaration",
                "%s must be an object, got %s"
                % (field, type(entry).__name__))
        period = entry.get("period")
        if period not in PERIODS:
            raise IntelligenceRefusal(
                "bad_intelligence_declaration",
                "%s.period must be one of %s, got %r"
                % (field, "/".join(PERIODS), period))
        if period in seen:
            raise IntelligenceRefusal(
                "bad_intelligence_declaration",
                "%s: duplicate period %r" % (field, period))
        seen.add(period)
        label = entry.get("label")
        if not isinstance(label, str) or not label.strip():
            raise IntelligenceRefusal(
                "bad_intelligence_declaration",
                "%s.label must be a non-empty string" % field)
        summary = entry.get("summary")
        if summary is not None and not isinstance(summary, str):
            raise IntelligenceRefusal(
                "bad_intelligence_declaration",
                "%s.summary must be a string" % field)
        generated_at = entry.get("generated_at")
        if generated_at is not None and not isinstance(generated_at, str):
            raise IntelligenceRefusal(
                "bad_intelligence_declaration",
                "%s.generated_at must be a string" % field)
        metrics = entry.get("metrics")
        mout = []
        if metrics is not None:
            if not isinstance(metrics, list):
                raise IntelligenceRefusal(
                    "bad_intelligence_declaration",
                    "%s.metrics must be a list" % field)
            if len(metrics) > MAX_METRICS:
                raise IntelligenceRefusal(
                    "intelligence_too_many_metrics",
                    "%s.metrics carries %d entries (max %d)"
                    % (field, len(metrics), MAX_METRICS))
            for j, m in enumerate(metrics):
                mfield = "%s.metrics[%d]" % (field, j)
                if not isinstance(m, dict):
                    raise IntelligenceRefusal(
                        "bad_intelligence_declaration",
                        "%s must be an object" % mfield)
                mlabel, mvalue = m.get("label"), m.get("value")
                if not isinstance(mlabel, str) or not mlabel.strip() \
                        or not isinstance(mvalue, str):
                    raise IntelligenceRefusal(
                        "bad_intelligence_declaration",
                        "%s.label must be a non-empty string and %s.value "
                        "a string" % (mfield, mfield))
                mout.append((mlabel.strip(), mvalue))
        out.append((period, label.strip(),
                    (summary or "").strip(),
                    (generated_at or "").strip(), mout))
    return out


def _context_parts(context):
    """Split the assembler's resolved context into (privacy, grants).

    The assembler resolves connections + privacy once per build
    (resolve_contract_context); modules read the resolved values here.
    Defaults match the assembler's: privacy 'private', all grants False.
    """
    ctx = context or {}
    privacy = ctx.get("privacy", "private")
    raw_grants = ctx.get("connections", {}) or {}
    grants = {k: bool(raw_grants.get(k, False)) for k in GRANT_NAMES}
    return privacy, grants


def check_connected_actions(decl, grants):
    """Refuse connected actions without their explicit grant (fail
    closed). With the grant but no implementation, refuse honestly too —
    this stdlib-only module performs no I/O, so a connected action can
    never be staged as working."""
    for field, grant, desc in CONNECTED_ACTIONS:
        if decl.get(field):
            if not grants.get(grant):
                raise IntelligenceRefusal(
                    "grant_required",
                    "%s needs contract.connections.%s == true "
                    "(explicit consent only)" % (desc, grant))
            raise IntelligenceRefusal(
                "connected_action_not_built",
                "%s is a connected action: declared in the capability "
                "contract, not implemented in this stdlib-only build "
                "(no I/O, no credentials)" % desc)


def render_intelligence_today(decl, registry_status, context=None):
    """Render the Intelligence Today section. Returns '' when the contract
    did not declare it (or explicitly opted out); raises
    IntelligenceRefusal otherwise.

    registry_status: the registry's status string for
    feature.intelligence_today. Rendering is proof the registry says
    'built' — the page carries data-intelligence_today-status="built" as
    the binding.
    context: the assembler's resolved contract context
    {'connections': {k: bool}, 'privacy': mode}. The privacy dial is
    stamped as data-privacy-scope; the READY surface needs no grants.
    """
    if decl is None or decl is False or not decl.get("enabled"):
        return ""  # omitted or explicit opt-out -> refuse to render reports
    if registry_status != "built":
        raise IntelligenceRefusal(
            "feature_not_built",
            "contract declares intelligence_today but registry status is %r "
            "(contract never activates an unbuilt capability)" % (registry_status,))
    privacy, grants = _context_parts(context)
    if privacy not in PRIVACY_SCOPES:
        raise IntelligenceRefusal("bad_privacy_scope",
                                  "privacy must be one of %s, got %r"
                                  % ("/".join(PRIVACY_SCOPES), privacy))
    check_connected_actions(decl, grants)

    title = str(decl.get("title") or "Intelligence Today").strip() \
        or "Intelligence Today"
    reports = reports_for(decl)
    if not reports:
        # graceful fallback: the empty state — the section is honest that
        # no report data arrived, and invents none
        body = ('<p class="intelligence-empty">No reports yet — '
                'your first report lands here.</p>')
    else:
        cards = []
        for period, label, summary, generated_at, metrics in reports:
            parts = ['<div class="intelligence-card" data-period="%s">' % esc(period),
                     '<h3 class="intelligence-label">%s</h3>' % esc(label)]
            if summary:
                parts.append('<p class="intelligence-summary">%s</p>' % esc(summary))
            if metrics:
                rows = "".join(
                    '<div class="intelligence-metric"><dt>%s</dt><dd>%s</dd></div>'
                    % (esc(ml), esc(mv)) for ml, mv in metrics)
                parts.append('<dl class="intelligence-metrics">%s</dl>' % rows)
            if generated_at:
                parts.append('<p class="intelligence-generated">Generated %s</p>'
                             % esc(generated_at))
            parts.append('</div>')
            cards.append("".join(parts))
        body = '<div class="intelligence-cards">%s</div>' % "".join(cards)

    return (
        '<section class="intelligence-today" data-feature="intelligence_today" '
        'data-intelligence_today-status="built" data-privacy-scope="%s" '
        'aria-label="%s">'
        '<h2 class="intelligence-title">%s</h2>%s</section>'
        % (esc(privacy), esc(title), esc(title), body)
    )
