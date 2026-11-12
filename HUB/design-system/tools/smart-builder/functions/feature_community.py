#!/usr/bin/env python3
"""feature.community — "Community" (Smart Builder feature breaker).

Capability contract (functions/registry.json):
  id: feature.community, version 1.0.0, status tracked in the registry.
  activated_by: contract.features.community — the CONTRACT flips the breaker;
  the module never hand-wires itself into a page.

THREE-STATE INTERFACE (Shawn 21:32Z):
  explicit true  -> on. With no details: the honest idle shell (day-one
                   working, zero errors) — never a staged thread.
  explicit false -> off: no render, no claim, no error.
  omitted        -> the assembler applies its policy (community keeps the
                   legacy default-off; the module hardcodes nothing).

Activation input (from the contract):
  contract.features.community = {
      "enabled": true,
      "title": "The conversation",      # optional
      "service": "hub-community",       # REQUIRED when a thread/form renders:
                                        # the comment service binding
                                        # (registry requires: comment_service)
      "moderation": "owner-moderated",  # REQUIRED when a thread/form renders:
                                        # the moderation policy binding
                                        # (registry requires: moderation_rules)
      "seed_comments": [                # optional: local thread content
          {"author": "Ana", "text": "First in line every morning.", "when": "today"}
      ],
      "comment_endpoint": "https://community.example.com/post",  # optional:
                                        # the publish path. Wiring it claims a
                                        # connected capability at network/public
                                        # dials -> the grant must be recorded.
      "report_target": "mailto:owner@example.com",  # REQUIRED when a thread
                                        # renders: the abuse path (registry
                                        # acceptance: abuse_path_exists)
  }

Behavior:
  - Not declared / explicit false / policy-off -> render nothing.
  - Declared + registry says built -> community section HTML.
  - Declared + registry says anything else -> CommunityRefusal('feature_not_built').
  - All declared inputs are validated always (fail closed on hostile input),
    even when the dial suppresses parts of the render.
  - PRIVACY DIAL (contract.privacy, default private):
      private -> gated shell only: no seeds, no form, no public thread
                 (registry acceptance: private_page_no_public_comments).
      network -> the NayaNET conversation; public -> open to the world
                 (first-class, never framed as a violation).
  - CONSENT LINE: local drafting/display is READY (zero grants). Publishing
    across a boundary is CONNECTED:
      * comment_endpoint wired at network dial without the recorded nayanet
        grant -> CommunityRefusal('missing_grant') naming "nayanet".
      * comment_endpoint wired at public dial without the recorded network
        grant -> CommunityRefusal('missing_grant') naming "network".
      * no endpoint wired at network/public without the grant -> the honest
        local state: seeds show locally + a plain-words note naming the
        missing connection. Never a refusal, never staged.
    The page carries data-mode="gated"|"idle"|"local"|"connected",
    data-privacy, and data-grant when connected; copy never conflates
    ready with connected.
  - A thread/form renders only with service + moderation + report_target
    bound, else CommunityRefusal('missing_service_binding'/'no_abuse_path').
    The bare idle shell needs none of them (nothing interactive to abuse).
  - Seed comments are plain text, always escaped: no HTML rides in.
  - comment_endpoint must be absolute https; report_target mailto: or
    absolute https. Hostile -> CommunityRefusal('unsafe_community_url').
  - Build-time events: none. The registry's community events
    (community.comment.posted / .removed) are visitor-lifecycle events.

Returns (html, meta); meta = {"mode": ..., "consent": "ready"|"connected"}.
Stdlib only. Pure functions — same declaration -> same bytes, always.
"""
import html as htmlmod
import re
from urllib.parse import urlparse

VERSION = "1.0.0"
FEATURE_ID = "feature.community"
# aliases the assembler imports
FEATURE_COMMUNITY_ID = FEATURE_ID
FEATURE_COMMUNITY_VERSION = VERSION

MAX_SEED_COMMENTS = 50  # fail closed: a contract declaring more is malformed

_EMAIL_RE = re.compile(r"^mailto:[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+$")
# dial -> grant that gates publishing across that boundary
# (private publishes nowhere: the gated shell needs no grant)
_DIAL_GRANT = {"network": "nayanet", "public": "network"}
_LOCAL_NOTE = {
    "network": "Not connected to NayaNET — showing the local conversation.",
    "public": "Not connected to the network — showing the local conversation.",
}
_AUDIENCE_LINE = {
    "network": "Visible to your NayaNET network.",
    "public": "Open to the world.",
}


class CommunityRefusal(Exception):
    """Structured refusal: the community breaker declined to activate.

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


def default_ctx():
    """Assembler context when the caller passes none: most private,
    zero grants — the fail-closed default."""
    return {"privacy": "private",
            "connections": {"muse": False, "github": False,
                            "network": False, "nayanet": False}}


def _check_https_url(u, field):
    if any(ord(c) < 0x20 for c in u):
        raise CommunityRefusal("unsafe_community_url",
                               "%s: control characters in URL" % field)
    p = urlparse(u)
    if (p.scheme or "").lower() != "https" or not p.hostname:
        raise CommunityRefusal("unsafe_community_url",
                               "%s: must be an absolute https URL" % field)
    if any(c.isspace() for c in p.hostname):
        raise CommunityRefusal("unsafe_community_url",
                               "%s: whitespace in host" % field)
    return u


def sanitize_community_url(url, field, allow_mailto=False):
    """Allowlist community URLs. Returns the cleaned URL, None when absent,
    raises CommunityRefusal('unsafe_community_url') for anything hostile."""
    if url is None:
        return None
    if not isinstance(url, str):
        raise CommunityRefusal("unsafe_community_url",
                               "%s: not a string (%s)" % (field, type(url).__name__))
    u = url.strip()
    if not u:
        return None
    if allow_mailto and _EMAIL_RE.match(u):
        return u
    return _check_https_url(u, field)


def decl_for(contract):
    """Extract the community declaration: the three-state interface.

      False            -> {"enabled": False}: explicit opt-out.
      None/falsy/absent-> None: omitted -> assembler policy (default-off).
      True             -> {"enabled": True}: on; with no details the idle
                          shell renders (day-one working, zero errors).
      dict             -> as-is; a dict without "enabled" counts as on,
                          "enabled": false counts as off.
      other truthy     -> CommunityRefusal('bad_community_declaration').
    """
    feats = contract.get("features") if isinstance(contract, dict) else None
    if not isinstance(feats, dict):
        return None  # contract-page contracts carry features as a list
    if "community" not in feats:
        return None
    decl = feats["community"]
    if decl is False:
        return {"enabled": False}
    if not decl:
        return None
    if decl is True:
        return {"enabled": True}
    if isinstance(decl, dict):
        return decl
    raise CommunityRefusal("bad_community_declaration",
                           "contract.features.community must be an object, "
                           "true, or false — got %s" % type(decl).__name__)


def seed_comments_for(decl):
    """Seed comments: plain text, validated shape. Raises on malformed."""
    raw = decl.get("seed_comments") or []
    if not isinstance(raw, list):
        raise CommunityRefusal("bad_seed_comment",
                               "seed_comments must be a list, got %s"
                               % type(raw).__name__)
    if len(raw) > MAX_SEED_COMMENTS:
        raise CommunityRefusal("too_many_comments",
                               "%d seed comments declared, max %d"
                               % (len(raw), MAX_SEED_COMMENTS))
    out = []
    for i, item in enumerate(raw):
        if not isinstance(item, dict):
            raise CommunityRefusal("bad_seed_comment",
                                   "seed comment #%d: must be an object, got %s"
                                   % (i, type(item).__name__))
        author = str(item.get("author") or "").strip()
        text = str(item.get("text") or "").strip()
        when = str(item.get("when") or "").strip()
        if not text:
            raise CommunityRefusal("bad_seed_comment",
                                   "seed comment #%d: empty text" % i)
        out.append((author or "A visitor", text, when))
    return out


def _shell_open(privacy, service):
    return ('<section class="community" data-feature="community" '
            'data-community-status="built" data-community-service="%s" '
            'data-privacy="%s"'
            % (esc(service), esc(privacy)))


def render_community(decl, registry_status, context=None):
    """Render the community section. Returns (html, meta).

    html is '' when the contract did not declare community or opted out;
    raises CommunityRefusal otherwise. meta = {"mode": ..., "consent": ...}.
    registry_status: the registry's status string — rendering is proof the
    registry says 'built' (data-community-status="built" is the binding).
    """
    ctx = context or default_ctx()
    privacy = ctx["privacy"]
    grants = ctx["connections"]
    if decl is None or decl.get("enabled") is False:
        return "", {"mode": "off", "consent": "ready"}
    if registry_status != "built":
        raise CommunityRefusal(
            "feature_not_built",
            "contract declares community but registry status is %r "
            "(contract never activates an unbuilt capability)" % (registry_status,))

    # Validate everything declared, always — fail closed on hostile input
    # even when the dial suppresses parts of the render.
    seeds = seed_comments_for(decl)
    endpoint = sanitize_community_url(decl.get("comment_endpoint"),
                                      "comment_endpoint")
    report_target = sanitize_community_url(decl.get("report_target"),
                                           "report_target", allow_mailto=True)
    service = str(decl.get("service") or "").strip()
    moderation = str(decl.get("moderation") or "").strip()
    title = str(decl.get("title") or "").strip() or "The conversation"

    if privacy == "private":
        # Gated shell: private pages show no public comments, no thread,
        # no form (registry acceptance: private_page_no_public_comments).
        # The abuse path rides along when declared — members still report.
        report = ('<p class="community-report">See something wrong? '
                  '<a href="%s">Report it</a>.</p>' % esc(report_target)
                  if report_target else "")
        html = (_shell_open(privacy, service) +
                ' data-mode="gated" aria-label="Community">'
                '<h2 class="community-title">%s</h2>'
                '<p class="community-gated">This conversation is open to '
                'members. Sign in to join it.</p>'
                '%s</section>' % (esc(title), report))
        return html, {"mode": "gated", "consent": "ready"}

    if not seeds and not endpoint:
        # Idle shell: enabled but nothing configured — a useful day-one
        # render, zero errors. Nothing interactive, so no service, no
        # moderation, no abuse path required.
        html = (_shell_open(privacy, service) +
                ' data-mode="idle" aria-label="Community">'
                '<h2 class="community-title">%s</h2>'
                '<p class="community-empty">The conversation opens here — '
                'the owner hasn\'t wired it yet.</p>'
                '</section>' % esc(title))
        return html, {"mode": "idle", "consent": "ready"}

    # A thread or publish path renders: the registry's requirements bind.
    if not service or not moderation:
        raise CommunityRefusal(
            "missing_service_binding",
            "community renders a thread but declares no comment service / "
            "moderation rules — the registry requires both; a thread with "
            "no service and no moderation is staged, not wired")
    if not report_target:
        raise CommunityRefusal(
            "no_abuse_path",
            "community renders a thread but declares no abuse-report target — "
            "the abuse path is an acceptance criterion "
            "(registry: abuse_path_exists)")

    # Consent line: publishing across the dial's boundary is CONNECTED.
    # A wired endpoint without the recorded grant is a connected capability
    # claimed without a grant -> structured refusal naming the grant.
    # Without a wired endpoint the page stays honestly local.
    grant = _DIAL_GRANT[privacy]
    connected = bool(grants.get(grant))
    if endpoint and not connected:
        raise CommunityRefusal(
            "missing_grant",
            "community wires a publish path for the %s audience but the %s "
            "grant is not recorded (contract.connections.%s) — publishing "
            "across that boundary is a connected capability"
            % (privacy, grant, grant))

    thread = "".join(
        '<article class="community-comment">'
        '<header><span class="community-author">%s</span>'
        '%s</header>'
        '<p class="community-text">%s</p></article>'
        % (esc(author),
           ('<time class="community-when">%s</time>' % esc(when)) if when else "",
           esc(text))
        for author, text, when in seeds)
    if not thread:
        thread = '<p class="community-empty">No comments yet.</p>'
    thread = '<div class="community-thread">%s</div>' % thread

    form = ""
    if endpoint:
        # The form renders only when a real endpoint is wired AND the
        # boundary grant is recorded — a comment form that posts nowhere,
        # or publishes without its grant, is never shipped.
        form = (
            '<form class="community-form" action="%s" method="post">'
            '<label>Your name<input type="text" name="author" required '
            'autocomplete="nickname" maxlength="60"></label>'
            '<label>Your comment<textarea name="text" required maxlength="2000" '
            'rows="3"></textarea></label>'
            '<button type="submit" class="naya-btn">'
            '<span class="nb-label">Post comment</span></button>'
            '</form>' % esc(endpoint))

    if connected:
        mode, consent = "connected", "connected"
        tail = ('<p class="community-moderation">Moderated: %s. %s</p>'
                % (esc(moderation), _AUDIENCE_LINE[privacy]))
        grant_attr = ' data-grant="%s"' % esc(grant)
    else:
        # Honest local state: seeds show locally; the publish path stays
        # unwired and the missing connection is named in plain words —
        # never a refusal for the dial alone, never staged.
        mode, consent = "local", "ready"
        tail = ('<p class="community-moderation">Moderated: %s. %s</p>'
                % (esc(moderation), _LOCAL_NOTE[privacy]))
        grant_attr = ""
    report = ('<p class="community-report">See something wrong? '
              '<a href="%s">Report it</a>.</p>' % esc(report_target))

    html = (_shell_open(privacy, service) +
            ' data-mode="%s"%s aria-label="Community">'
            '<h2 class="community-title">%s</h2>'
            '%s%s%s%s</section>'
            % (mode, grant_attr, esc(title), thread, form, tail, report))
    return html, {"mode": mode, "consent": consent}
