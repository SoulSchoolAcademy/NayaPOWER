#!/usr/bin/env python3
"""feature.notifications — "Invitations and notifications" (Smart Builder feature breaker).

Capability contract (functions/registry.json):
  id: feature.notifications, version 1.0.0, status tracked in the registry.
  activated_by: contract.features.notifications — the CONTRACT flips the breaker;
  the module never hand-wires itself into a page.
  Built on PR #2747's not_wired declaration: label "Invitations and
  notifications", default_enabled true, required true.

Activation input (from the contract):
  contract.features.notifications = {
      "enabled": True,
      "audience": "subscribers",          # owner | subscribers | visitors
      "events": [                          # page events that may notify
          {"name": "new_post", "message": "Mara posted an update", "permission": "notify.new_post"}
      ],
      "grants": ["notify.new_post"]        # permissions the owner granted
  }

Behavior:
  - Not declared (or enabled falsy) -> render nothing. The page refuses
    to wire notifications the contract did not declare.
  - Declared + registry says built -> an opt-in panel: one row per declared
    event, preferences stored on the visitor's device. Each event is
    permission-gated: a listed event whose permission is not in grants is a
    structured refusal (notification_permission_denied), never silently wired.
  - Declared + registry says anything else ->
    NotificationsRefusal('feature_not_built'). The contract never advertises
    a capability as operational unless the registry says it is built.
  - READY vs CONNECTED (Naya 3's consent-line refinement, 21:41Z): declaring
    events and the opt-in panel is READY (local, no grant needed); delivery is
    CONNECTED and needs the recorded grant 'transport.notify.send'. Without it
    the module shows the honest ready-not-connected state — never a fabricated
    send, never silent.
  - HONESTY (the hard rule): there is no delivery transport in this module,
    and the module never stages one. The receipt carries a delivery manifest
    with transport "BLOCKED — no push/mail delivery transport wired" and the
    page says so in plain words: preferences save on this device; nothing is
    ever claimed sent (cf. lesson L-2026-10-16-004 — transport-blocked is its
    own failure class, never a content failure, and state is preserved for
    intelligent resume).
  - Unknown event names, bad audiences, empty messages, malformed
    declarations -> structured refusals, fail closed. Events the contract did
    not list are never wired (undeclared events are ignored by construction).
  - Interactive elements bind only to DOM that exists: script sits directly
    after the markup, runs on DOMContentLoaded, and no-ops when its root
    section is absent (L-2026-10-17-004).

Stdlib only. Pure functions — same declaration -> same bytes, always.
"""
import html as htmlmod

VERSION = "1.0.0"
FEATURE_ID = "feature.notifications"
# aliases the assembler imports
FEATURE_NOTIFICATIONS_ID = FEATURE_ID
FEATURE_NOTIFICATIONS_VERSION = VERSION

# The page events this module knows how to wire. Anything else is refused —
# the module never improvises a binding it was not built for.
EVENT_CATALOG = ("new_post", "new_note", "new_comment", "broadcast", "mention")
AUDIENCES = ("owner", "subscribers", "visitors")
# The named BLOCKED transport: honesty, not a placeholder.
DELIVERY_TRANSPORT = "push/mail delivery transport"
# READY vs CONNECTED (Naya 3's consent-line refinement, 21:41Z): configuring
# events + the opt-in panel is READY (local, no grant needed); delivery is
# CONNECTED and needs this recorded grant.
GRANT_SEND = "transport.notify.send"


class NotificationsRefusal(Exception):
    """Structured refusal: the notifications breaker declined to activate.

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
    """Extract the notifications declaration from a contract, or None.

    Accepts the PLUMBING.md breaker convention (contract.features.notifications):
      - dict  -> the declaration (task shape: enabled/audience/events/grants)
      - True  -> enabled with empty fields
      - falsy / absent / features-not-a-dict -> None (not declared)
      - anything else truthy -> NotificationsRefusal('bad_notifications_declaration')
    """
    feats = contract.get("features") if isinstance(contract, dict) else None
    if not isinstance(feats, dict):
        return None  # contract-page contracts carry features as a list
    if "notifications" not in feats:
        return None
    decl = feats["notifications"]
    if not decl:
        return None
    if decl is True:
        return {"enabled": True}
    if isinstance(decl, dict):
        return decl
    raise NotificationsRefusal("bad_notifications_declaration",
                               "contract.features.notifications must be an object or true, "
                               "got %s" % type(decl).__name__)


def sanitize_event(ev, i, grants):
    """Validate one declared event. Returns (name, message, permission)
    or raises. The permission gate is enforced here: ungranted -> refused."""
    if not isinstance(ev, dict):
        raise NotificationsRefusal("bad_notification_event",
                                   "events[%d]: must be an object, got %s"
                                   % (i, type(ev).__name__))
    name = str(ev.get("name") or "").strip()
    if name not in EVENT_CATALOG:
        raise NotificationsRefusal("bad_notification_event",
                                   "events[%d]: unknown event %r (catalog: %s)"
                                   % (i, name, "/".join(EVENT_CATALOG)))
    message = ev.get("message")
    if not isinstance(message, str) or not message.strip():
        raise NotificationsRefusal("bad_notification_event",
                                   "events[%d]: message must be a non-empty string" % i)
    if len(message) > 300:
        raise NotificationsRefusal("bad_notification_event",
                                   "events[%d]: message too long" % i)
    permission = str(ev.get("permission") or "").strip()
    if not permission:
        raise NotificationsRefusal("bad_notification_event",
                                   "events[%d]: permission is required" % i)
    if permission not in grants:
        raise NotificationsRefusal("notification_permission_denied",
                                   "events[%d]: permission %r not granted — "
                                   "the event is not wired" % (i, permission))
    return name, message.strip(), permission


# The opt-in script: binds ONLY to elements rendered above it
# (L-2026-10-17-004). Preferences persist on this device; the script never
# touches the network and never claims a notification was sent.
OPTIN_SCRIPT = """<script>
(function(){
  function ready(fn){if(document.readyState!=='loading'){fn();}else{document.addEventListener('DOMContentLoaded',fn);}}
  ready(function(){
    var root=document.querySelector('[data-feature="notifications"]');
    if(!root){return;}
    var form=document.getElementById('nt-optin');
    if(!form){return;}
    var status=document.getElementById('nt-status');
    var KEY='naya.notifications.prefs.v1';
    function load(){try{return JSON.parse(localStorage.getItem(KEY)||'{}');}catch(e){return{};}}
    function apply(){
      var prefs=load();
      var boxes=form.querySelectorAll('input[type="checkbox"][data-event]');
      for(var i=0;i<boxes.length;i++){boxes[i].checked=!!prefs[boxes[i].getAttribute('data-event')];}
    }
    apply();
    form.addEventListener('submit',function(ev){
      ev.preventDefault();
      var prefs={};
      var boxes=form.querySelectorAll('input[type="checkbox"][data-event]');
      for(var i=0;i<boxes.length;i++){prefs[boxes[i].getAttribute('data-event')]=boxes[i].checked;}
      try{localStorage.setItem(KEY,JSON.stringify(prefs));}catch(e){}
      if(status){status.textContent='Saved on this device. Delivery: not connected — connect a delivery transport to enable sending.';}
    });
  });
})();
</script>"""


def optin_row(name, message, permission):
    return (
        '<label class="nt-row">'
        '<input type="checkbox" data-event="%s" data-permission="%s">'
        '<span class="nt-msg">%s</span>'
        '<span class="nt-perm">%s</span>'
        '</label>' % (esc(name), esc(permission), esc(message), esc(permission))
    )


def render_notifications(decl, registry_status, context=None):
    """Render the notifications opt-in panel. Returns (html, events).

    Raises NotificationsRefusal unless the registry says 'built' — rendering
    is proof the registry says built; the section carries
    data-notifications-status="built" as the binding. The receipt's delivery
    manifest names the BLOCKED transport explicitly (never staged).

    context: resolved contract context (connections+privacy+identity),
    plumbed for interface uniformity; the module's permission gates read
    the declaration's own grants (fail closed, tested).
    """
    if decl is None or not decl.get("enabled"):
        return "", []  # not declared -> refuse to wire notifications
    if registry_status != "built":
        raise NotificationsRefusal(
            "feature_not_built",
            "contract declares notifications but registry status is %r "
            "(contract never activates an unbuilt capability)" % (registry_status,))

    audience = str(decl.get("audience") or "").strip().lower()
    if not audience:
        audience = "subscribers"  # PR #2747 default: on for the audience
    if audience not in AUDIENCES:
        raise NotificationsRefusal("bad_notification_audience",
                                   "audience %r not in %s" % (audience, "/".join(AUDIENCES)))

    raw_events = decl.get("events")
    if raw_events is None:
        raw_events = []
    elif not isinstance(raw_events, list):
        raise NotificationsRefusal("bad_notifications_declaration",
                                   "events must be a list, got %s"
                                   % type(raw_events).__name__)
    grants = decl.get("grants") or []
    if not isinstance(grants, list):
        raise NotificationsRefusal("bad_notifications_declaration",
                                   "grants must be a list, got %s" % type(grants).__name__)
    grants = [str(g) for g in grants]

    rows, events = [], []
    seen = set()
    for i, raw in enumerate(raw_events):
        name, message, permission = sanitize_event(raw, i, grants)
        if name in seen:
            raise NotificationsRefusal("bad_notification_event",
                                       "events[%d]: duplicate event %r" % (i, name))
        seen.add(name)
        rows.append(optin_row(name, message, permission))
        events.append({"event": "notification.wired", "feature": FEATURE_ID,
                       "version": VERSION, "name": name,
                       "audience": audience, "permission": permission,
                       "permission_gate": "granted"})

    # The delivery manifest: transport-blocked, named, preserved for resume
    # (L-2026-10-16-004) — never a staged "sent" claim.
    events.append({"event": "notification.delivery_blocked", "feature": FEATURE_ID,
                   "version": VERSION,
                   "transport": "BLOCKED",
                   "transport_name": DELIVERY_TRANSPORT,
                   "connection": DELIVERY_TRANSPORT,
                   "grant_needed": GRANT_SEND,
                   "reason": "not connected — connect a delivery transport to enable "
                             "sending; preferences save on this device only; nothing "
                             "is ever claimed sent"})

    if rows:
        panel = (
            '<form class="nt-optin" id="nt-optin">'
            '<div class="nt-rows">%s</div>'
            '<button type="submit" class="nt-save" id="nt-save">Save preferences</button>'
            '<p class="nt-status" id="nt-status" aria-live="polite"></p>'
            '</form>' % "".join(rows)
        )
    else:
        panel = ('<p class="nt-fine">No notification events declared yet — '
                 'declare them in the contract and they appear here.</p>')

    html_out = (
        '<section class="nt" data-feature="notifications" data-notifications-status="built">'
        '<div class="nt-head"><h2>Notifications</h2>'
        '<p class="nt-fine">Choose what you would like to hear about%s.</p>'
        '<p class="nt-fine">Delivery: not connected — connect a delivery transport '
        'to enable sending. Preferences save on this device; nothing leaves the page.</p></div>'
        '%s%s</section>'
        % (" for " + esc(audience) if rows else "", panel, OPTIN_SCRIPT)
    )
    return html_out, events
