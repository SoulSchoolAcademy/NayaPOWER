#!/usr/bin/env python3
"""feature.scheduler — "Scheduled posts" (Smart Builder feature breaker).

Capability contract (functions/registry.json):
  id: feature.scheduler, version 1.0.0, status tracked in the registry.
  activated_by: contract.features.scheduler — the CONTRACT flips the breaker;
  the module never hand-wires itself into a page.
  requires: authenticated_identity, scheduler_service, feed_service
  permissions: scheduler.create
  events: scheduler.job.created (build — the job spec is created here),
          scheduler.job.fired, scheduler.job.failed (runtime)

Activation input (from the contract):
  contract.features.scheduler = {
      "enabled": true,
      "cadence": "daily",            # hourly | daily | weekly | monthly
      "time": "08:00",               # HH:MM 24h (ignored for hourly)
      "timezone": "America/New_York",
      "weekday": 0,                  # weekly only, 0=Monday (default 0)
      "monthday": 1,                 # monthly only (default 1)
      "topic": "daily intelligence", # what gets posted
      "manage_endpoint": "https://... (scheduler service, optional)",
      "delivery": "nayanet",         # optional: nayanet|queued_locally.
                                     # "nayanet" without the grant refuses.
  }

Honest scope:
  - The builder module does NOT run the schedule (no I/O, no timers).
    It renders the schedule card and embeds the validated, machine-readable
    job spec (<script type="application/json" data-scheduler-spec>) that the
    runtime scheduler service consumes. Publishing, firing, canceling, and
    missed-job reporting belong to that service — the spec is the binding.
  - The card shows the rule ("Every day · 08:00 America/New_York"), never a
    build-time "next run" timestamp: same declaration -> same bytes, always
    (determinism). next_run() is a pure, unit-tested helper for the runtime.
  - Cancel: a working cancel control ONLY when the contract declares
    manage_endpoint (real POST to the declared service). No endpoint ->
    no cancel button. Never a dead control (Shawn's function law).

Behavior (three-state, Shawn's 21:32Z default-on rule):
  - Omitted -> assembler policy (scheduler is not a standard feature,
    so omitted = off). The module never hardcodes a default.
  - Explicit false -> off: no render, no claim.
  - Explicit true + registry built -> schedule card + job spec.
  - NayaNET connection missing -> the card still renders (the schedule is
    real) but spec.delivery = "queued_locally" and the card says so.
    No transport without its connection; never pretend delivery (21:34Z).
  - Declared + registry says anything else -> SchedulerRefusal('feature_not_built').
  - Bad cadence/time/timezone/declaration -> SchedulerRefusal('bad_scheduler_declaration'),
    fail closed. Hostile manage_endpoint -> SchedulerRefusal('unsafe_scheduler_endpoint').

Stdlib only. Pure functions — same declaration -> same bytes, always.
"""
import hashlib
import html as htmlmod
import json
import re
from datetime import datetime, timedelta
from urllib.parse import urlparse

VERSION = "1.0.0"
FEATURE_ID = "feature.scheduler"
# aliases the assembler imports
FEATURE_SCHEDULER_ID = FEATURE_ID
FEATURE_SCHEDULER_VERSION = VERSION

CADENCES = ("hourly", "daily", "weekly", "monthly")
TIME_RE = re.compile(r"^([01]\d|2[0-3]):([0-5]\d)$")
# Build event recorded in the manifest receipt when the job spec renders.
JOB_CREATED_EVENT = "scheduler.job.created"

# Connections (Shawn's 21:34Z day-one rule), refined 21:41Z into the
# READY vs CONNECTED split (automation: logged local actions = ready;
# acting on external services = connected):
#   ready     = schedule card renders; job spec created and queued locally.
#               The card says nothing is sent.
#   connected = the scheduler service delivers posts to the NayaNET feed.
# The contract may declare "delivery": "nayanet" to demand connected
# delivery explicitly — without the grant that is a structured
# grant_required refusal, never a silent downgrade.
NEEDS_CONNECTION = "nayanet"
GRANT = "connections.nayanet"
READINESS = {
    "ready": "Schedule card renders; job spec created and queued locally. "
             "The card says nothing is sent.",
    "connected": "The scheduler service delivers posts to the NayaNET feed "
                 "on the schedule.",
    "grant": GRANT,
}


class SchedulerRefusal(Exception):
    """Structured refusal: the scheduler breaker declined to activate.

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


def safe_json_for_script(obj):
    """Embed JSON inside <script>: no sequence may break out of the
    element. \\u-escapes are valid JSON and parse back clean."""
    return (json.dumps(obj, indent=2, ensure_ascii=False, sort_keys=True)
            .replace("<", "\\u003c").replace(">", "\\u003e")
            .replace("&", "\\u0026"))


def sha16(b):
    return hashlib.sha256(b).hexdigest()[:16]


def clean_text(s, field):
    t = str(s or "").strip()
    if any(ord(c) < 0x20 and c not in ("\t", "\n", "\r") for c in t):
        raise SchedulerRefusal("bad_scheduler_declaration",
                               "%s: control characters in text" % field)
    return t


def sanitize_endpoint(url, field):
    """Allowlist the scheduler-service endpoint. Absolute http(s) only."""
    if url is None:
        return None
    if not isinstance(url, str):
        raise SchedulerRefusal("unsafe_scheduler_endpoint",
                               "%s: not a string (%s)"
                               % (field, type(url).__name__))
    u = url.strip()
    if not u:
        return None
    if any(ord(c) < 0x20 for c in u):
        raise SchedulerRefusal("unsafe_scheduler_endpoint",
                               "%s: control characters in URL" % field)
    p = urlparse(u)
    scheme = (p.scheme or "").lower()
    if scheme in ("http", "https"):
        if not p.hostname:
            raise SchedulerRefusal("unsafe_scheduler_endpoint",
                                   "%s: %s URL has no host" % (field, scheme))
        if any(c.isspace() for c in p.hostname):
            raise SchedulerRefusal("unsafe_scheduler_endpoint",
                                   "%s: whitespace in host" % field)
        return u
    reason = "relative URLs are not allowed" if not scheme \
        else "disallowed scheme %r (scheduler service must be http(s))" % p.scheme
    raise SchedulerRefusal("unsafe_scheduler_endpoint",
                           "%s: %s" % (field, reason))


def validate_timezone(name):
    """IANA timezone name, validated via zoneinfo when tzdata is present.
    Without tzdata the box cannot verify — accept a plausible name rather
    than refuse (fail open on the check, never on the claim)."""
    tz = str(name or "").strip()
    if not tz:
        raise SchedulerRefusal("bad_scheduler_declaration",
                               "timezone is required")
    if not re.match(r"^[A-Za-z0-9_+\-/]+$", tz):
        raise SchedulerRefusal("bad_scheduler_declaration",
                               "timezone %r is not a plausible zone name" % tz)
    try:
        from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
    except ImportError:
        return tz  # pragma: no cover — zoneinfo is stdlib since 3.9
    try:
        ZoneInfo("UTC")
    except Exception:
        return tz  # tzdata missing: cannot verify, accept the plausible name
    try:
        ZoneInfo(tz)
    except ZoneInfoNotFoundError:
        raise SchedulerRefusal("bad_scheduler_declaration",
                               "unknown timezone %r" % tz)
    return tz


def decl_for(contract):
    """Extract the scheduler declaration from a contract, or None.

    Three-state interface (Shawn's 21:32Z default-on rule):
      - features not a dict (contract-page) -> None: no breakers at all.
      - key absent -> None: OMITTED. The assembler applies its policy
        (registry-marked standard features default on); the module never
        hardcodes a default.
      - True -> {"enabled": True}: explicit ON.
      - dict -> itself: explicit; on iff decl.get("enabled") is truthy.
      - other falsy (False/None/0/"") -> {"enabled": False}: explicit OFF.
        Off renders nothing and claims nothing.
      - other truthy -> SchedulerRefusal('bad_scheduler_declaration').
    """
    feats = contract.get("features") if isinstance(contract, dict) else None
    if not isinstance(feats, dict):
        return None  # contract-page contracts carry features as a list
    if "scheduler" not in feats:
        return None  # omitted -> assembler policy applies
    decl = feats["scheduler"]
    if decl is True:
        return {"enabled": True}
    if isinstance(decl, dict):
        return decl
    if not decl:
        return {"enabled": False}  # explicit off: no render, no claim
    raise SchedulerRefusal("bad_scheduler_declaration",
                           "contract.features.scheduler must be an object, "
                           "true, or false, got %s" % type(decl).__name__)


def validated_spec(decl):
    """Validate the declaration into the canonical, machine-readable job
    spec the runtime scheduler service consumes. Raises SchedulerRefusal
    on anything malformed — fail closed, never improvise a schedule."""
    cadence = str(decl.get("cadence") or "").strip().lower()
    if cadence not in CADENCES:
        raise SchedulerRefusal(
            "bad_scheduler_declaration",
            "cadence must be one of %s, got %r" % ("/".join(CADENCES),
                                                   decl.get("cadence")))
    t = str(decl.get("time") or "").strip()
    if cadence == "hourly":
        hour, minute = 0, 0  # hourly fires on the hour; time is ignored
    else:
        m = TIME_RE.match(t)
        if not m:
            raise SchedulerRefusal(
                "bad_scheduler_declaration",
                "time must be HH:MM (24h), got %r" % decl.get("time"))
        hour, minute = int(m.group(1)), int(m.group(2))
    tz = validate_timezone(decl.get("timezone"))
    weekday = decl.get("weekday", 0)
    if cadence == "weekly":
        if not isinstance(weekday, int) or not 0 <= weekday <= 6:
            raise SchedulerRefusal("bad_scheduler_declaration",
                                   "weekday must be 0..6 (Monday=0)")
    monthday = decl.get("monthday", 1)
    if cadence == "monthly":
        if not isinstance(monthday, int) or not 1 <= monthday <= 28:
            raise SchedulerRefusal("bad_scheduler_declaration",
                                   "monthday must be 1..28")
    topic = clean_text(decl.get("topic"), "topic") or "scheduled post"
    endpoint = sanitize_endpoint(decl.get("manage_endpoint"), "manage_endpoint")
    spec = {
        "feature": FEATURE_ID,
        "version": VERSION,
        "cadence": cadence,
        "time": "%02d:%02d" % (hour, minute),
        "timezone": tz,
        "topic": topic,
    }
    if cadence == "weekly":
        spec["weekday"] = weekday
    if cadence == "monthly":
        spec["monthday"] = monthday
    if endpoint:
        spec["manage_endpoint"] = endpoint
    spec["job_id"] = sha16(json.dumps(spec, sort_keys=True).encode())
    return spec


def granted(ctx):
    """The grant: contract.connections.nayanet == true (strict)."""
    conns = (ctx or {}).get("connections", {}) or {}
    return conns.get(NEEDS_CONNECTION) is True


def delivery_for(decl, ctx):
    """READY vs CONNECTED delivery for this declaration.

    - contract "delivery": "nayanet" without the grant -> grant_required.
    - contract "delivery": "queued_locally" -> queued, even with the grant.
    - absent -> connected iff the grant is held, else queued_locally.
    """
    want = decl.get("delivery")
    if want is None:
        return "nayanet" if granted(ctx) else "queued_locally"
    want = str(want).strip().lower()
    if want not in ("nayanet", "queued_locally"):
        raise SchedulerRefusal("bad_scheduler_declaration",
                               "delivery must be nayanet|queued_locally, got %r"
                               % decl.get("delivery"))
    if want == "nayanet" and not granted(ctx):
        raise SchedulerRefusal(
            "grant_required",
            "delivery nayanet (connected) requires grant %s — connect "
            "NayaNET, or drop the delivery demand to queue locally" % GRANT)
    return want


def mode_for(decl, ctx):
    """READY vs CONNECTED for this declaration. Called after a successful
    render, so the grant_required path cannot trigger here."""
    return "connected" if delivery_for(decl, ctx) == "nayanet" else "ready"


def next_run(spec, now):
    """Pure: the next fire time strictly after `now` for a validated spec.
    `now` must be timezone-aware. The runtime uses this; the build never
    embeds a computed timestamp (determinism)."""
    from zoneinfo import ZoneInfo
    tz = ZoneInfo(spec["timezone"])
    now = now.astimezone(tz)
    hour, minute = (int(x) for x in spec["time"].split(":"))
    cadence = spec["cadence"]
    if cadence == "hourly":
        cand = now.replace(minute=0, second=0, microsecond=0)
        return cand if cand > now else cand + timedelta(hours=1)
    cand = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if cadence == "daily":
        return cand if cand > now else cand + timedelta(days=1)
    if cadence == "weekly":
        days_ahead = (spec.get("weekday", 0) - now.weekday()) % 7
        cand = cand + timedelta(days=days_ahead)
        return cand if cand > now else cand + timedelta(weeks=1)
    # monthly: monthday clamped to 28 by validation, so always a real day
    md = spec.get("monthday", 1)
    if now.day < md or (now.day == md and cand > now):
        return now.replace(day=md, hour=hour, minute=minute,
                           second=0, microsecond=0)
    y, m = (now.year + 1, 1) if now.month == 12 else (now.year, now.month + 1)
    return now.replace(year=y, month=m, day=md, hour=hour, minute=minute,
                       second=0, microsecond=0)


def rule_line(spec):
    """Human rule: 'Every day · 08:00 America/New_York'. No timestamps."""
    cad = {"hourly": "Every hour", "daily": "Every day",
           "weekly": "Every week", "monthly": "Every month"}[spec["cadence"]]
    extra = ""
    if spec["cadence"] == "weekly":
        extra = " · " + ["Mon", "Tue", "Wed", "Thu",
                         "Fri", "Sat", "Sun"][spec["weekday"]]
    if spec["cadence"] == "monthly":
        extra = " · day %d" % spec["monthday"]
    when = "" if spec["cadence"] == "hourly" \
        else " · %s %s" % (spec["time"], spec["timezone"])
    return "%s%s%s" % (cad, extra, when)


def render_scheduler(decl, registry_status, context=None):
    """Render the scheduler card + machine-readable job spec. Returns ''
    when the contract did not declare scheduler (omitted non-standard,
    explicit off, or disabled); raises SchedulerRefusal otherwise.

    registry_status: the registry's status string for feature.scheduler.
    context: {"connections": {...}, "privacy": ...} from the assembler.

    Connections: without NayaNET the card still renders (the schedule is
    real) but delivery is queued_locally and the card says so — never
    pretend delivery.
    """
    if decl is None or not decl.get("enabled"):
        return ""  # not declared / explicit off -> no render, no claim
    if registry_status != "built":
        raise SchedulerRefusal(
            "feature_not_built",
            "contract declares scheduler but registry status is %r "
            "(contract never activates an unbuilt capability)"
            % (registry_status,))

    spec = validated_spec(decl)
    # Delivery honesty (READY vs CONNECTED): no transport without its
    # connection. An explicit nayanet demand without the grant refuses.
    spec["delivery"] = delivery_for(decl, context)
    # The job id covers the full effective spec, delivery included: the
    # same rule with a different delivery is a different job.
    spec["job_id"] = sha16(json.dumps(
        {k: v for k, v in spec.items() if k != "job_id"},
        sort_keys=True).encode())
    connected = spec["delivery"] == "nayanet"
    endpoint = spec.get("manage_endpoint")

    if endpoint:
        # Wired: a real cancel control posting to the declared scheduler
        # service. cancel_works is the service's acceptance; this is its
        # contract binding.
        manage = (
            '<form class="sched-manage" method="post" action="%s/cancel">'
            '<input type="hidden" name="job_id" value="%s">'
            '<button type="submit" class="sched-cancel">Cancel schedule</button>'
            '</form>' % (esc(endpoint.rstrip("/")), esc(spec["job_id"]))
        )
    else:
        manage = ""  # no endpoint -> no cancel button. Never a dead control.

    queue_note = "" if connected else (
        '<p class="sched-queue">Not connected to NayaNET — posts queue '
        'locally until you connect. Nothing is sent yet.</p>'
    )

    return (
        '<section class="sched-card" data-feature="scheduler" '
        'data-scheduler-status="built" data-job-id="%s" data-cadence="%s" '
        'data-mode="%s" data-grant="%s" data-delivery="%s">'
        '<div class="sched-head"><h2>Scheduled posts</h2>'
        '<p class="sched-rule">%s</p>'
        '<p class="sched-topic">Posting: %s</p></div>%s%s'
        '<script type="application/json" data-scheduler-spec>%s</script>'
        '</section>'
        % (esc(spec["job_id"]), esc(spec["cadence"]),
           "connected" if connected else "ready", esc(GRANT),
           esc(spec["delivery"]),
           esc(rule_line(spec)), esc(spec["topic"]), queue_note, manage,
           safe_json_for_script(spec))
    )
