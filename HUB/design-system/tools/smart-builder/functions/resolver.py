#!/usr/bin/env python3
"""Function resolver — the capability-activation flow.

One call any Naya uses to activate a function:

    resolve(function_id, context) -> activation receipt
    resolve(function_id, context) -> raises ResolverRefusal (stays blocked)

Gates, in order:
  1. unknown function_id            -> ResolverRefusal('unknown_function')  (fail closed)
  2. registry status != 'built'     -> ResolverRefusal('not_implemented')
  3. requires[] not all available   -> ResolverRefusal('requirement_unmet', missing=[...])
  4. permissions[] not all granted  -> ResolverRefusal('permission_denied', missing=[...])
  5. all pass                       -> dispatch to the feature module when one
                                       exists, else a generic activation receipt.

Product law honored at gate 4: enabled by default must not mean connected
or publicly shared without consent. A permission block explains precisely
what is needed, in human words — it never pretends the feature works.

Structured errors follow the CoverRefusal pattern: ResolverRefusal carries
code / function / detail / missing, machine-readable via as_dict().

Stdlib only. Pure apart from reading functions/registry.json once.
"""
import json
import os
import sys

RESOLVER_VERSION = "1.0.0"

_HERE = os.path.dirname(os.path.abspath(__file__))
_REGISTRY_PATH = os.path.join(_HERE, "registry.json")


class ResolverRefusal(Exception):
    """Structured refusal: the resolver declined to activate a function.

    code:     machine-readable failure class.
    function: the function_id that was refused (None for unknown_function).
    detail:   human-readable explanation of precisely what is needed.
    missing:  list of unmet requirements or ungranted permissions.
    """
    def __init__(self, code, function=None, detail="", missing=None):
        label = ("%s " % function) if function else ""
        super().__init__("%s%s: %s" % (label, code, detail))
        self.code = code
        self.function = function
        self.detail = detail
        self.missing = list(missing or [])

    def as_dict(self):
        d = {"code": self.code, "detail": self.detail}
        if self.function:
            d["function"] = self.function
        if self.missing:
            d["missing"] = self.missing
        return d


# Human words for every permission in the registry. Used when a permission
# block must explain precisely what is needed — the Builder shows this, and
# never pretends the feature works without the grant.
PERMISSION_EXPLAIN = {
    "answers.ask": "ask Naya questions against your knowledge base",
    "bars.render": "render the smart navigation bars",
    "broadcast.send": "send broadcasts to everyone related to the page",
    "community.comment": "let visitors comment in your community",
    "community.post": "let visitors post in your community",
    "connect.accept": "accept connection requests from visitors",
    "connect.request": "send connection requests on your behalf",
    "contacts.read": "read your contacts",
    "feed.publish": "publish posts to your personal feed",
    "list.create": "create and organize Smart Lists",
    "list.share": "share lists with others",
    "mail.compose": "compose mail in Smart Mail",
    "mail.send": "send mail through Smart Mail",
    "media.upload": "upload media (photos) into the page's media store",
    "reports.read": "read your Intelligence Today reports",
    "scheduler.create": "create scheduled posts and automations",
    "space.create": "create Smart Spaces",
    "space.join": "join you to Smart Spaces",
    "tabs.navigate": "navigate between your pages via smart tabs",
}

# Human words for every requirement in the registry.
REQUIREMENT_EXPLAIN = {
    "answer_service": "an answer service wired to your knowledge base",
    "audience_rules": "audience rules deciding who may see what",
    "authenticated_identity": "a signed-in identity for the page owner",
    "comment_service": "a comment service for the community",
    "consent_records": "consent records for the people involved",
    "contact_store": "a contact store holding your people",
    "data_authorization": "data authorization for the rows it reads",
    "delivery_receipts": "delivery receipts proving mail landed",
    "feed_service": "a feed service to publish into",
    "github_kb_sync": "GitHub knowledge-base sync",
    "identity_directory": "an identity directory for connections",
    "list_store": "a list store holding your lists",
    "media_store": "a media store holding the page's uploads",
    "membership_rules": "membership rules for the space",
    "message_service": "a message service to carry the mail",
    "moderation_rules": "moderation rules for community content",
    "navigation_service": "a navigation service across your pages",
    "object_index": "an object index of the things lists organize",
    "page_registry": "a page registry listing your pages",
    "recipient_authorization": "recipient authorization to receive mail",
    "report_pipeline": "a report pipeline producing Intelligence Today",
    "scheduler_service": "a scheduler service to run automations",
    "space_service": "a space service backing Smart Spaces",
}


def _explain_permission(p):
    return PERMISSION_EXPLAIN.get(p, "permission '%s'" % p)


def _explain_requirement(q):
    return REQUIREMENT_EXPLAIN.get(q, "requirement '%s'" % q)


def _load_registry():
    with open(_REGISTRY_PATH, encoding="utf-8") as f:
        data = json.load(f)
    index = {}

    def walk(o):
        if isinstance(o, dict):
            if "id" in o and "status" in o:
                index[o["id"]] = o
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    walk(data)
    return index


_REGISTRY = None


def registry_index():
    """The registry as id -> entry. Loaded once; the registry is the
    authority on what is built — the resolver never invents it."""
    global _REGISTRY
    if _REGISTRY is None:
        _REGISTRY = _load_registry()
    return _REGISTRY


def _module_for(function_id):
    """Import the built feature module for a function, or None.

    Modules live beside this file (functions/feature_cover.py) and are
    stdlib-only. Unknown modules are a registry/code drift, not a
    fail-open: the caller treats None as 'no module bound'.
    """
    table = {
        "feature.cover": ("feature_cover", "render_cover", "decl_for"),
        "feature.smart_mail": ("feature_smart_mail", "render_smart_mail",
                               "decl_for"),
        "feature.smart_list": ("feature_smart_list", "render_smart_list",
                               "decl_for"),
        "feature.space": ("feature_space", "render_smart_space",
                          "decl_for"),
        "feature.social_feed": ("feature_social_feed", "render_social_feed",
                                "decl_for"),
        "feature.connect": ("feature_connect", "render_connect",
                            "decl_for"),
    }
    if function_id not in table:
        return None
    mod_name, render_name, decl_name = table[function_id]
    if _HERE not in sys.path:
        sys.path.insert(0, _HERE)
    try:
        mod = __import__(mod_name)
    except ImportError:
        return None
    render = getattr(mod, render_name, None)
    decl_fn = getattr(mod, decl_name, None)
    if render is None:
        return None
    return mod, render, decl_fn


def _human_list(items, explain):
    if len(items) == 1:
        return explain(items[0])
    return ", ".join(explain(i) for i in items[:-1]) + " and " + explain(items[-1])


def resolve(function_id, context):
    """Activate a function, or stay blocked with a structured reason.

    context: dict with
      'contract'            the page contract (features declared here)
      'connections'         {'muse': bool, 'github': bool, ...} (informational)
      'privacy'             'private' | 'network' | 'public' (informational)
      'granted_permissions' [ ... ]  permissions the customer has granted
      'available'           [ ... ]  requirements already satisfied

    Returns {'activated': True, 'function': id, 'events': [...], 'output': ...}
    on success; raises ResolverRefusal otherwise. Never pretends.
    """
    if not isinstance(context, dict):
        raise ResolverRefusal("bad_context", function_id,
                              "context must be a dict, got %s"
                              % type(context).__name__)
    index = registry_index()
    entry = index.get(function_id)
    if entry is None:
        raise ResolverRefusal(
            "unknown_function", None,
            "no function %r in the registry — refusing closed; unknown "
            "capabilities never activate" % (function_id,))
    name = entry.get("name") or function_id
    status = entry.get("status")

    if status != "built":
        raise ResolverRefusal(
            "not_implemented", function_id,
            "%s (%s) is specified in the registry but not built yet — "
            "it stays off until a builder implements it and the registry "
            "says 'built'" % (name, function_id))

    requires = list(entry.get("requires") or [])
    available = list(context.get("available") or [])
    missing_req = [q for q in requires if q not in available]
    if missing_req:
        raise ResolverRefusal(
            "requirement_unmet", function_id,
            "%s (%s) cannot activate: it needs %s, which %s not "
            "available. Wire %s first — the Builder will not pretend it "
            "works without %s." % (
                name, function_id,
                _human_list(missing_req, _explain_requirement),
                "is" if len(missing_req) == 1 else "are",
                _human_list(missing_req, lambda q: "'%s'" % q),
                "it" if len(missing_req) == 1 else "them"),
            missing=missing_req)

    permissions = list(entry.get("permissions") or [])
    granted = list(context.get("granted_permissions") or [])
    missing_perm = [p for p in permissions if p not in granted]
    if missing_perm:
        raise ResolverRefusal(
            "permission_denied", function_id,
            "%s (%s) is ready but stays off: it needs your permission to "
            "%s. Grant %s to activate it. Enabled by default does not mean "
            "connected without your consent — until you grant it, the "
            "feature is present but dormant, never faked." % (
                name, function_id,
                _human_list(missing_perm, _explain_permission),
                _human_list(missing_perm, lambda p: "'%s'" % p)),
            missing=missing_perm)

    events = list(entry.get("events") or [])
    bound = _module_for(function_id)
    if bound is None:
        # Built, requirements met, permissions granted — but no module is
        # bound yet. The capability is real; there is simply no renderer.
        return {"activated": True, "function": function_id,
                "events": events, "output": None,
                "note": "no module bound; capability ready, nothing to render"}

    mod, render, decl_fn = bound
    contract = context.get("contract") or {}
    decl = decl_fn(contract) if decl_fn else None
    refusal_cls = getattr(mod, "CoverRefusal", None) or getattr(
        mod, "ResolverRefusal", None)
    try:
        output = render(decl, status, context=context)
    except Exception as e:
        code = getattr(e, "code", "module_refused")
        detail = getattr(e, "detail", str(e))
        raise ResolverRefusal(code, function_id, detail)
    return {"activated": True, "function": function_id,
            "events": events, "output": output}
