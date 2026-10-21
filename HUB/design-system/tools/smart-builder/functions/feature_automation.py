#!/usr/bin/env python3
"""feature.automation — "Authorized automation and scheduling" (Smart Builder feature breaker).

Capability contract (functions/registry.json):
  id: feature.automation, version 1.0.0, status tracked in the registry.
  activated_by: contract.features.automation — the CONTRACT flips the breaker;
  the module never hand-wires itself into a page.
  Built on PR #2747's not_wired declaration: label "Authorized automation and
  scheduling", default_enabled false, required false.

Activation input (from the contract):
  contract.features.automation = {
      "enabled": True,
      "actions": [                          # declared automatic actions
          {"id": "morning-post", "kind": "scheduled_post",
           "schedule": "daily 08:00", "permission": "automation.run",
           "payload": {"template": "daily-intel"}}
      ],
      "grants": ["automation.run"]          # permissions the owner granted
  }

Behavior:
  - Not declared (or enabled falsy) -> render nothing. The page refuses
    to declare automation the contract did not authorize.
  - Declared + registry says built -> an automation panel listing every
    declared action with its schedule, permission, and gate state.
  - Declared + registry says anything else ->
    AutomationRefusal('feature_not_built'). The contract never advertises
    a capability as operational unless the registry says it is built.
  - EVERY declared action is permission-gated: an action whose permission
    is not in grants is a structured refusal (automation_permission_denied),
    never silently armed. Unknown action kinds and malformed declarations
    are refused, fail closed.
  - EVERY declared action is logged to the receipt: the module returns an
    automation.audit[] entry per action (id, kind, schedule, permission,
    gate decision, status) alongside its events — the audit trail is the
    proof, not a screenshot.
  - READY vs CONNECTED (Naya 3's consent-line refinement, 21:41Z): declaring,
    gating, and auditing actions is READY (local, no grant needed); execution is
    CONNECTED and needs the recorded grant 'transport.automation.run'. Without it
    the module shows the honest ready-not-connected state — never staged as run,
    never silent.
  - HONESTY (the hard rule): there is no execution transport in this module,
    and the module never stages one. Every action's status is
    "declared — execution transport BLOCKED (scheduler runner not wired)".
    No fake "running" badges, no invented "last run" timestamps, no staged
    execution — ever (cf. lesson L-2026-10-16-004 — transport-blocked is its
    own failure class, never a content failure, and state is preserved for
    intelligent resume).

Stdlib only. Pure functions — same declaration -> same bytes, always.
"""
import html as htmlmod

VERSION = "1.0.0"
FEATURE_ID = "feature.automation"
# aliases the assembler imports
FEATURE_AUTOMATION_ID = FEATURE_ID
FEATURE_AUTOMATION_VERSION = VERSION

# The automatic actions this module knows how to declare. Anything else is
# refused — the module never improvises an action it was not built for.
ACTION_KINDS = ("scheduled_post", "digest", "backup")
# The named BLOCKED transport: honesty, not a placeholder.
EXECUTION_TRANSPORT = "scheduler runner"
# READY vs CONNECTED (Naya 3's consent-line refinement, 21:41Z): declaring +
# gating + auditing actions is READY (local, no grant needed); execution is
# CONNECTED and needs this recorded grant.
GRANT_RUN = "transport.automation.run"


class AutomationRefusal(Exception):
    """Structured refusal: the automation breaker declined to activate.

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
    """Extract the automation declaration from a contract, or None.

    Accepts the PLUMBING.md breaker convention (contract.features.automation):
      - dict  -> the declaration (task shape: enabled/actions/grants)
      - True  -> enabled with empty fields
      - falsy / absent / features-not-a-dict -> None (not declared)
      - anything else truthy -> AutomationRefusal('bad_automation_declaration')
    """
    feats = contract.get("features") if isinstance(contract, dict) else None
    if not isinstance(feats, dict):
        return None  # contract-page contracts carry features as a list
    if "automation" not in feats:
        return None
    decl = feats["automation"]
    if not decl:
        return None
    if decl is True:
        return {"enabled": True}
    if isinstance(decl, dict):
        return decl
    raise AutomationRefusal("bad_automation_declaration",
                            "contract.features.automation must be an object or true, "
                            "got %s" % type(decl).__name__)


def sanitize_action(act, i, grants):
    """Validate one declared action. Returns a clean action dict or raises.
    The permission gate is enforced here: ungranted -> refused."""
    if not isinstance(act, dict):
        raise AutomationRefusal("bad_automation_action",
                                "actions[%d]: must be an object, got %s"
                                % (i, type(act).__name__))
    aid = str(act.get("id") or "").strip()
    if not aid:
        raise AutomationRefusal("bad_automation_action",
                                "actions[%d]: id is required" % i)
    if len(aid) > 80:
        raise AutomationRefusal("bad_automation_action",
                                "actions[%d]: id too long" % i)
    kind = str(act.get("kind") or "").strip()
    if kind not in ACTION_KINDS:
        raise AutomationRefusal("bad_automation_kind",
                                "actions[%d]: unknown kind %r (catalog: %s)"
                                % (i, kind, "/".join(ACTION_KINDS)))
    schedule = act.get("schedule")
    if not isinstance(schedule, str) or not schedule.strip():
        raise AutomationRefusal("bad_automation_action",
                                "actions[%d]: schedule must be a non-empty string" % i)
    schedule = schedule.strip()
    if len(schedule) > 64:
        raise AutomationRefusal("bad_automation_action",
                                "actions[%d]: schedule too long" % i)
    permission = str(act.get("permission") or "").strip()
    if not permission:
        raise AutomationRefusal("bad_automation_action",
                                "actions[%d]: permission is required" % i)
    if permission not in grants:
        raise AutomationRefusal("automation_permission_denied",
                                "actions[%d]: permission %r not granted — "
                                "the action is not armed" % (i, permission))
    payload = act.get("payload")
    if payload is not None and not isinstance(payload, (dict, str)):
        raise AutomationRefusal("bad_automation_action",
                                "actions[%d]: payload must be an object or string" % i)
    return {"id": aid, "kind": kind, "schedule": schedule,
            "permission": permission, "payload": payload}


def action_row(act):
    return (
        '<div class="am-action" data-action-id="%s">'
        '<div class="am-id">%s</div>'
        '<div class="am-kind">%s</div>'
        '<div class="am-schedule">%s</div>'
        '<div class="am-perm">%s · granted</div>'
        '<div class="am-exec" data-exec-state="not-connected">execution: not connected — '
        'connect a %s to enable</div>'
        '</div>'
        % (esc(act["id"]), esc(act["id"]), esc(act["kind"]),
           esc(act["schedule"]), esc(act["permission"]),
           esc(EXECUTION_TRANSPORT))
    )


def render_automation(decl, registry_status, context=None):
    """Render the automation panel. Returns (html, events, audit).

    audit: one entry per declared action — the receipt's proof that every
    automatic action was logged. Raises AutomationRefusal unless the
    registry says 'built' — rendering is proof the registry says built;
    the section carries data-automation-status="built" as the binding.

    context: resolved contract context (connections+privacy+identity),
    plumbed for interface uniformity; execution transport stays BLOCKED
    until a scheduler runner is wired (never staged as run).
    """
    if decl is None or not decl.get("enabled"):
        return "", [], []  # not declared -> refuse to declare automation
    if registry_status != "built":
        raise AutomationRefusal(
            "feature_not_built",
            "contract declares automation but registry status is %r "
            "(contract never activates an unbuilt capability)" % (registry_status,))

    raw_actions = decl.get("actions")
    if raw_actions is None:
        raw_actions = []
    elif not isinstance(raw_actions, list):
        raise AutomationRefusal("bad_automation_declaration",
                                "actions must be a list, got %s"
                                % type(raw_actions).__name__)
    grants = decl.get("grants") or []
    if not isinstance(grants, list):
        raise AutomationRefusal("bad_automation_declaration",
                                "grants must be a list, got %s" % type(grants).__name__)
    grants = [str(g) for g in grants]

    rows, events, audit = [], [], []
    seen = set()
    for i, raw in enumerate(raw_actions):
        act = sanitize_action(raw, i, grants)
        if act["id"] in seen:
            raise AutomationRefusal("bad_automation_action",
                                    "actions[%d]: duplicate id %r" % (i, act["id"]))
        seen.add(act["id"])
        rows.append(action_row(act))
        entry = {"action_id": act["id"], "kind": act["kind"],
                 "schedule": act["schedule"], "permission": act["permission"],
                 "permission_gate": "granted",
                 "status": "ready — declared and audited; execution not connected "
                           "(grant needed: %s)" % GRANT_RUN}
        audit.append(entry)
        events.append({"event": "automation.action_declared", "feature": FEATURE_ID,
                       "version": VERSION, "action_id": act["id"],
                       "kind": act["kind"], "schedule": act["schedule"],
                       "permission_gate": "granted"})

    # Aggregate execution block: transport-blocked, named, preserved for
    # resume (L-2026-10-16-004) — never a staged "ran" claim.
    events.append({"event": "automation.execution_blocked", "feature": FEATURE_ID,
                   "version": VERSION, "actions_declared": len(audit),
                   "transport": "BLOCKED", "transport_name": EXECUTION_TRANSPORT,
                   "connection": EXECUTION_TRANSPORT,
                   "grant_needed": GRANT_RUN,
                   "reason": "not connected — connect a scheduler runner to enable; "
                             "actions are declared and audited; nothing is ever "
                             "claimed run"})

    if rows:
        panel = '<div class="am-actions">%s</div>' % "".join(rows)
    else:
        panel = ('<p class="am-fine">No automatic actions declared yet — '
                 'declare them in the contract and they appear here, '
                 'permission-gated and audited.</p>')

    html_out = (
        '<section class="am" data-feature="automation" data-automation-status="built">'
        '<div class="am-head"><h2>Automation</h2>'
        '<p class="am-fine">Naya operates this page through declared automatic actions. '
        'Each action is permission-gated, and every action is logged to the build receipt.</p>'
        '<p class="am-fine">Execution: not connected — connect a scheduler runner to enable. '
        'Schedules are declared and audited; nothing runs.</p></div>'
        '%s</section>' % panel
    )
    return html_out, events, audit
