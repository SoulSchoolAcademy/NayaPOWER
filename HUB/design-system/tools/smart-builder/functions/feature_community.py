#!/usr/bin/env python3
"""feature.community — "Community" (Smart Builder feature breaker).

Capability contract (functions/registry.json):
  id: feature.community, version 1.0.0, status tracked in the registry.
  activated_by: contract.features.community — the CONTRACT flips the
  breaker; the module never hand-wires itself into a page.
  depends_on: ["systems.community"]
  requires: authenticated_identity, comment_service, moderation_rules
  permissions: community.comment, community.post (commenting is a
  permission question — the UI is the capability, the grant is the key)
  events: community.comment.posted, community.comment.removed
  acceptance: comment_appears, abuse_path_exists,
  private_page_no_public_comments
  connected: [{action: "post to community", grant: "nayanet"}]
  ready: community UI, local threads

Activation input (from the contract, which carries the intake's data):
  contract.features.community = {
      "enabled": True,
      "threads": [
          {"id": "welcome", "title": "Say hello",
           "posts": [{"author": "Ada", "text": "First!"}]},
      ]
  }
  thread.id: non-empty string (required — the thread's stable key).
  thread.title: non-empty string (required — a thread without a title
  is a thread nobody can find).
  post.author: non-empty string (required — an anonymous post is a lie
  about the community).
  post.text: non-empty string (required — an empty post renders nothing,
  honestly absent rather than faked).

Behavior:
  - Not declared (or enabled falsy) -> render nothing. The page refuses
    to render a community the contract did not declare.
  - Declared + registry says anything else -> CommunityRefusal(
    'feature_not_built'). The contract never advertises a capability as
    operational unless the registry says it is built.
  - comment_appears: every declared post renders, byte-identical and
    HTML-escaped. A post that the declaration lists but the page drops
    silently is a community that cannot be trusted.
  - private_page_no_public_comments: a private page renders NO comment
    UI and NO public posts — an honest note says comments stay off on
    private pages. Privacy outranks community, always.
  - abuse_path_exists: every rendered post carries a report affordance
    naming the moderation rules. A community without an abuse path is
    a community without a conscience — it does not ship.
  - The "post to community" action is the connected action (grant:
    nayanet — strict boolean, the consent-line refinement): the live
    post affordance renders ONLY when the nayanet connection is ON and
    the community.comment + community.post permissions are granted.
    Otherwise an honest gated block names exactly what is missing in
    human words. Never a dead post button, never a faked thread.
  - Receipt hooks -> the section carries data-receipt-events with the
    registry's own events (community.comment.posted,
    community.comment.removed) so the runtime can persist receipts. A
    claim of "posted" without a receipt is a hope.
  - Threads are local (ready: "local threads"): posts come from the
    contract's own declaration. There is no remote fetch, no invented
    membership, no seeded strangers.

Judgment, named: the resolver enforces the three requirements
(authenticated_identity, comment_service, moderation_rules) and the two
permissions (community.comment, community.post) BEFORE this module is
ever called — resolve() fails closed on requirement_unmet /
permission_denied with the human words. Inside the module, the nayanet
grant is the finer control (the connected action), checked with the
strict boolean the connect module uses. The privacy dial is checked
first: a private contract short-circuits to the honest private note —
the acceptance criterion private_page_no_public_comments is a veto,
not a render path. data-consent is "connected" ONLY on the live post
affordance; every other surface says "ready". The verifier asserts this.

Acceptance (registry: comment_appears, abuse_path_exists,
private_page_no_public_comments) is exercised in
functions/tests/test_feature_community.py.

Stdlib only. Pure functions — same declaration + same context -> same
bytes, always.
"""
import html as htmlmod

VERSION = "1.0.0"
FEATURE_ID = "feature.community"
# aliases the assembler imports
FEATURE_COMMUNITY_ID = FEATURE_ID
FEATURE_COMMUNITY_VERSION = VERSION

# Commenting is a permission question. The human words match the
# resolver's PERMISSION_EXPLAIN['community.comment' / 'community.post']
# byte-for-byte — two surfaces, one truth.
COMMENT_PERMISSION = "community.comment"
COMMENT_PERMISSION_HUMAN = "let visitors comment in your community"
POST_PERMISSION = "community.post"
POST_PERMISSION_HUMAN = "let visitors post in your community"

# The connected action's grant: strict boolean, the consent-line
# refinement. The human words match the connect module's GRANT_WORDS.
POST_GRANT = "nayanet"
POST_GRANT_HUMAN = "the NayaNET connection switched on for this page"

MODERATION_HUMAN = "moderation rules for community content"


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


def _nonempty_str(value):
    return isinstance(value, str) and bool(value.strip())


def sanitize_post(post):
    """Validate one post. Returns {'author', 'text'}.
    Raises CommunityRefusal('bad_post') for anything malformed — a
    community that swallows a bad post silently is a community that
    cannot be trusted."""
    if not isinstance(post, dict):
        raise CommunityRefusal(
            "bad_post",
            "each post must be an object, got %s" % type(post).__name__)
    author = post.get("author")
    if not _nonempty_str(author):
        raise CommunityRefusal(
            "bad_post",
            "post needs a non-empty string author, got %r" % (author,))
    text = post.get("text")
    if not _nonempty_str(text):
        raise CommunityRefusal(
            "bad_post",
            "post needs a non-empty string text, got %r" % (text,))
    return {"author": author.strip(), "text": text.strip()}


def sanitize_thread(thread):
    """Validate one thread. Returns {'id', 'title', 'posts'}.
    Raises CommunityRefusal('bad_thread') for anything malformed."""
    if not isinstance(thread, dict):
        raise CommunityRefusal(
            "bad_thread",
            "each thread must be an object, got %s" % type(thread).__name__)
    tid = thread.get("id")
    if not _nonempty_str(tid):
        raise CommunityRefusal(
            "bad_thread",
            "thread needs a non-empty string id, got %r" % (tid,))
    title = thread.get("title")
    if not _nonempty_str(title):
        raise CommunityRefusal(
            "bad_thread",
            "thread needs a non-empty string title, got %r" % (title,))
    raw_posts = thread.get("posts") or []
    if not isinstance(raw_posts, list):
        raise CommunityRefusal(
            "bad_thread",
            "thread posts must be a list, got %s" % type(raw_posts).__name__)
    return {"id": tid.strip(), "title": title.strip(),
            "posts": [sanitize_post(p) for p in raw_posts]}


def decl_for(contract):
    """Extract the community declaration from a contract, or None.

    Accepts the PLUMBING.md breaker convention
    (contract.features.community):
      - dict  -> the declaration (task shape: enabled/threads)
      - True  -> enabled with empty fields
      - falsy / absent / features-not-a-dict -> None (not declared)
      - anything else truthy -> CommunityRefusal(
        'bad_community_declaration')
    """
    feats = contract.get("features") if isinstance(contract, dict) else None
    if not isinstance(feats, dict):
        return None  # contract-page contracts carry features as a list
    if "community" not in feats:
        return None
    decl = feats["community"]
    if not decl:
        return None
    if decl is True:
        return {"enabled": True}
    if isinstance(decl, dict):
        return decl
    raise CommunityRefusal(
        "bad_community_declaration",
        "contract.features.community must be an object or true, "
        "got %s" % type(decl).__name__)


def _granted_permissions(context):
    ctx = context or {}
    return list(ctx.get("granted_permissions") or [])


def can_comment(context):
    """Evaluate the comment/post authorization. Returns (allowed, missing):
    allowed only when community.comment + community.post are granted AND
    the nayanet connection is strictly ON (the connected action)."""
    missing = []
    granted = _granted_permissions(context)
    if COMMENT_PERMISSION not in granted:
        missing.append(COMMENT_PERMISSION_HUMAN)
    if POST_PERMISSION not in granted:
        missing.append(POST_PERMISSION_HUMAN)
    connections = (context or {}).get("connections") or {}
    if connections.get(POST_GRANT) is not True:
        missing.append(POST_GRANT_HUMAN)
    return (len(missing) == 0, missing)


def _post_html(post):
    """Render one post: byte-identical content, HTML-escaped (XSS probe
    territory), with the abuse-path report affordance. The caller
    guarantees the post passed sanitize_post."""
    return (
        '<article class="community-post">'
        '<p class="community-post-author">%s</p>'
        '<p class="community-post-text">%s</p>'
        '<button type="button" class="community-report-btn" '
        'data-abuse-path="report" '
        'title="Report this post under the community moderation rules">'
        'Report</button>'
        '</article>' % (esc(post["author"]), esc(post["text"])))


def _thread_html(thread, privacy):
    """Render one thread. privacy='private' is vetoed upstream — this
    function never renders posts on a private page."""
    posts = "".join(_post_html(p) for p in thread["posts"])
    return (
        '<section class="community-thread" data-thread-id="%s">'
        '<h3 class="community-thread-title">%s</h3>'
        '<div class="community-posts" data-receipt-events='
        '"community.comment.posted community.comment.removed">%s</div>'
        '</section>' % (esc(thread["id"]), esc(thread["title"]), posts))


def _post_box_html(context):
    """The connected action: a live post affordance ONLY when the
    comment/post permissions are granted and the nayanet grant is ON.
    Otherwise an honest gated block naming what is missing, in human
    words. Never a dead post button."""
    allowed, missing = can_comment(context)
    if allowed:
        return (
            '<div class="community-post-box" data-consent="connected" '
            'data-community-grant="nayanet">'
            '<form class="community-post-form">'
            '<label class="community-post-label">Join the conversation'
            '</label>'
            '<input type="text" class="community-post-name" '
            'placeholder="Your name" />'
            '<textarea class="community-post-input" '
            'placeholder="Say something kind"></textarea>'
            '<button type="button" class="community-post-btn">'
            'Post to community</button>'
            '</form>'
            '<div class="community-receipts" data-receipt-events='
            '"community.comment.posted community.comment.removed">'
            '<span class="community-receipts-note">Receipts are recorded '
            'for every comment posted and removed.</span></div>'
            '</div>')
    reasons = "".join("<li>%s</li>" % esc(r) for r in missing)
    return (
        '<div class="community-post-box community-post-gated" '
        'data-consent="ready">'
        '<p class="community-gated-title">Posting is ready but off.</p>'
        '<p class="community-gated-why">To post in the community, the page '
        'needs:</p>'
        '<ul class="community-gated-list">%s</ul>'
        '<p class="community-gated-note">The threads stay readable; posting '
        'waits for the grant.</p>'
        '</div>' % reasons)


def render_community(decl, registry_status, context=None):
    """Render the community panel. Returns '' when the contract did not
    declare community; raises CommunityRefusal otherwise.

    registry_status: the registry's status string for feature.community.
    Rendering is proof the registry says 'built' — the section carries
    data-community-status="built" as the binding.
    context: resolved contract context {'connections': {...}, 'privacy': ...,
    'granted_permissions': [...], 'available': [...], 'identity': {...}}.
    """
    if decl is None or not decl.get("enabled"):
        return ""  # not declared -> refuse to render a community
    if registry_status != "built":
        raise CommunityRefusal(
            "feature_not_built",
            "contract declares community but registry status is %r "
            "(contract never activates an unbuilt capability)"
            % (registry_status,))

    # private_page_no_public_comments: privacy is a veto, not a render
    # path. A private page renders no comment UI and no public posts.
    privacy = (context or {}).get("privacy")
    if privacy == "private":
        return (
            '<section class="community" data-feature="community" '
            'data-community-status="built" data-consent="ready">'
            '<h2 class="community-title">Community</h2>'
            '<p class="community-private-note">Comments stay off on '
            'private pages — the community appears when the page is '
            'shared.</p>'
            '</section>')

    threads = [sanitize_thread(t) for t in (decl.get("threads") or [])]
    if not threads:
        body = ('<p class="community-empty">No conversations yet — the '
                'first post starts the community.</p>')
    else:
        body = "".join(_thread_html(t, privacy) for t in threads)
    return (
        '<section class="community" data-feature="community" '
        'data-community-status="built" data-consent="ready">'
        '<h2 class="community-title">Community</h2>'
        '<div class="community-threads">%s</div>%s'
        '</section>' % (body, _post_box_html(context)))
