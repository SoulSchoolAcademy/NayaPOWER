#!/usr/bin/env python3
"""feature.social_feed — "Personal social feed" (Smart Builder feature breaker).

Capability contract (functions/registry.json):
  id: feature.social_feed, version 1.0.0, status tracked in the registry.
  activated_by: contract.features.social_feed — the CONTRACT flips the breaker;
  the module never hand-wires itself into a page.

Activation input (from the contract, which carries the intake's data):
  contract.features.social_feed = {
      "enabled": True,
      "posts": [
          {"title": "Launch day", "body": "We opened the doors.",
           "visibility": "network",  # private default
           "draft": False,
           "failed": False},
      ]
  }
  visibility: 'private' | 'network' | 'public', default 'private'.
  draft: bool, default False — drafts live in the local drafts tray
         (READY — works with zero grants: reading your own drafts is a
         local act).

Behavior:
  - Not declared (or enabled falsy) -> render nothing. The page refuses
    to render posts the contract did not declare.
  - Declared + registry says built -> the feed panel: the feed UI with
    published posts, the drafts tray (local draft posts — READY), and the
    publish action per post. Publish is a CONNECTED action: it renders as
    a live publish button ONLY when the publish authorization holds —
    feed.publish granted AND the NayaNET connection ON — otherwise an
    honest gated block naming exactly what is missing in human words.
    Never a dead button, never silent.
  - Declared + registry says anything else -> FeedRefusal('feature_not_built').
    The contract never advertises a capability as operational unless the
    registry says it is built.
  - Private posts stay private: a private post renders NO publish
    affordance at all — publishing a private post is not a gated state,
    it is an absent one. A "Private — only you see this" line stands in
    its place. The panel never says "connected" for a private-only feed.
  - Failed posts stay honest: a post with failed=True renders an honest
    failure line naming the failure — the feed never swallows a failure
    silently (acceptance: failure_state_visible).
  - Malformed posts (missing title/body, wrong shape, bad visibility) ->
    FeedRefusal('bad_social_feed_post'), never silently dropped.
  - Receipt hooks -> the feed block carries data-receipt-events with the
    registry's own events (feed.post.published, feed.post.failed) so the
    runtime can persist receipts. A claim of "published" without a
    receipt is a hope.

Judgment, named: page-level privacy (context['privacy']) stays
informational — each post's own visibility (private/network/public) is
the finer, per-post control and governs publishing, mirroring how the
space module treats per-space visibility. Publish is the only runtime
connected action; composing and drafting are contract-time or local acts,
so feed publishing gates at the connected affordance and the resolver
gate. A private page with a public post allows publishing; a public page
with a private post never does.

Acceptance (registry: post_appears_for_audience, private_post_not_leaked,
failure_state_visible) is exercised in
functions/tests/test_feature_social_feed.py.

Stdlib only. Pure functions — same declaration + same context -> same
bytes, always.
"""
import html as htmlmod

VERSION = "1.0.0"
FEATURE_ID = "feature.social_feed"
# aliases the assembler imports
FEATURE_SOCIAL_FEED_ID = FEATURE_ID
FEATURE_SOCIAL_FEED_VERSION = VERSION

# The connected publish action fires only on this recorded grant
# (strict boolean — the consent-line refinement: grant = True, not truthy).
PUBLISH_GRANT = "nayanet"

VISIBILITIES = ("private", "network", "public")

# Human words for publish-gate reasons, so the gated block speaks plainly.
GRANT_WORDS = {
    "permission": "your permission to publish posts",
    "nayanet": "the NayaNET connection switched on for this page",
}


class FeedRefusal(Exception):
    """Structured refusal: the social-feed breaker declined to activate.

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
    """Validate one feed post. Returns {'title', 'body', 'visibility',
    'draft', 'failed'}. Raises FeedRefusal('bad_social_feed_post') for
    anything malformed — a feed that swallows a bad post silently is a
    feed that cannot be trusted."""
    if not isinstance(post, dict):
        raise FeedRefusal("bad_social_feed_post",
                          "each post must be an object, got %s"
                          % type(post).__name__)
    title = post.get("title")
    if not _nonempty_str(title):
        raise FeedRefusal("bad_social_feed_post",
                          "post needs a non-empty string title, got %r"
                          % (title,))
    body = post.get("body")
    if not _nonempty_str(body):
        raise FeedRefusal("bad_social_feed_post",
                          "post %r needs a non-empty string body, got %r"
                          % (title, body))
    vis = post.get("visibility") or "private"
    if vis not in VISIBILITIES:
        raise FeedRefusal("bad_social_feed_post",
                          "post visibility must be one of %s, got %r"
                          % (list(VISIBILITIES), vis))
    draft = post.get("draft")
    if draft not in (None, True, False):
        raise FeedRefusal("bad_social_feed_post",
                          "post draft flag must be a boolean, got %r"
                          % (draft,))
    failed = post.get("failed")
    if failed not in (None, True, False):
        raise FeedRefusal("bad_social_feed_post",
                          "post failed flag must be a boolean, got %r"
                          % (failed,))
    return {"title": title.strip(), "body": body.strip(),
            "visibility": vis, "draft": bool(draft),
            "failed": bool(failed)}


def decl_for(contract):
    """Extract the social-feed declaration from a contract, or None.

    Accepts the PLUMBING.md breaker convention
    (contract.features.social_feed):
      - dict  -> the declaration (task shape: enabled/posts)
      - True  -> enabled with empty fields
      - falsy / absent / features-not-a-dict -> None (not declared)
      - anything else truthy -> FeedRefusal('bad_social_feed_declaration')
    """
    feats = contract.get("features") if isinstance(contract, dict) else None
    if not isinstance(feats, dict):
        return None  # contract-page contracts carry features as a list
    if "social_feed" not in feats:
        return None
    decl = feats["social_feed"]
    if not decl:
        return None
    if decl is True:
        return {"enabled": True}
    if isinstance(decl, dict):
        return decl
    raise FeedRefusal("bad_social_feed_declaration",
                      "contract.features.social_feed must be an object or true, "
                      "got %s" % type(decl).__name__)


def can_publish(context):
    """Evaluate the publish authorization for a post.

    Returns (allowed, missing). allowed is True only when the publish grant
    holds: feed.publish granted AND the NayaNET connection strictly ON.
    Private posts are not a grant question — they never render a publish
    affordance at all (private_post_not_leaked), so callers check
    visibility first; this gate answers only the authorization question.
    """
    missing = []
    ctx = context or {}
    granted = list(ctx.get("granted_permissions") or [])
    if "feed.publish" not in granted:
        missing.append(GRANT_WORDS["permission"])
    connections = ctx.get("connections") or {}
    if connections.get(PUBLISH_GRANT) is not True:
        missing.append(GRANT_WORDS["nayanet"])
    return (len(missing) == 0, missing)


def _publish_block(allowed, missing):
    """The connected action: a live publish button only when authorized,
    otherwise an honest gated block naming what is missing. The two are
    visually distinct and the verifier asserts data-consent honesty."""
    if allowed:
        return (
            '<div class="feed-publish" data-consent="connected" '
            'data-publish-grant="nayanet">'
            '<button type="button" class="feed-publish-btn">Publish to network</button>'
            '<div class="feed-receipts" data-receipt-events='
            '"feed.post.published feed.post.failed">'
            '<span class="feed-receipts-note">Receipts are recorded for '
            'every publish.</span></div>'
            '</div>')
    reasons = "".join("<li>%s</li>" % esc(r) for r in missing)
    return (
        '<div class="feed-publish feed-publish-gated" data-consent="ready">'
        '<p class="feed-gated-title">Publishing is ready but off.</p>'
        '<p class="feed-gated-why">To publish this post, the page needs:</p>'
        '<ul class="feed-gated-list">%s</ul>'
        '<p class="feed-gated-note">Your drafts are safe here — publishing waits '
        'for the grant.</p>'
        '</div>' % reasons)


def _post_html(post, context):
    """Render one post. Private posts render NO publish affordance —
    publishing is not a state a private post can be in (acceptance:
    private_post_not_leaked). Failed posts render the honest failure line."""
    vis = post["visibility"]
    badge = '<span class="feed-visibility feed-visibility-%s">%s</span>' \
        % (esc(vis), esc(vis))
    body = ('<article class="feed-post" data-visibility="%s">'
            '<h3 class="feed-post-title">%s</h3>%s'
            '<p class="feed-post-body">%s</p>'
            % (esc(vis), esc(post["title"]), badge, esc(post["body"])))
    if post["failed"]:
        body += ('<p class="feed-post-failed">This post failed to publish — '
                 'nothing went out, and nothing was hidden from you.</p>')
    if vis == "private":
        action = ('<p class="feed-private-note">Private — only you see this, '
                  'never publishable from here.</p>')
    else:
        allowed, missing = can_publish(context)
        action = _publish_block(allowed, missing)
    return body + action + '</article>'


def _drafts_html(drafts, context):
    if not drafts:
        return ""
    return ('<div class="feed-drafts"><h3>Drafts</h3>%s</div>'
            % "".join(_post_html(p, context) for p in drafts))


def render_social_feed(decl, registry_status, context=None):
    """Render the social-feed panel. Returns '' when the contract did not
    declare social_feed; raises FeedRefusal otherwise.

    registry_status: the registry's status string for feature.social_feed.
    Rendering is proof the registry says 'built' — the page carries
    data-feed-status="built" as the binding.
    context: resolved contract context {'connections': {...}, 'privacy': ...,
    'granted_permissions': [...], 'available': [...], 'identity': {...}}.
    """
    if decl is None or not decl.get("enabled"):
        return ""  # not declared -> refuse to render posts
    if registry_status != "built":
        raise FeedRefusal(
            "feature_not_built",
            "contract declares social_feed but registry status is %r "
            "(contract never activates an unbuilt capability)" % (registry_status,))

    posts = [sanitize_post(p) for p in (decl.get("posts") or [])]
    drafts = [p for p in posts if p["draft"]]
    live = [p for p in posts if not p["draft"]]
    # data-consent on the panel mirrors the assembler contract: "connected"
    # ONLY when a grant-active publish affordance renders; else "ready".
    any_live_publish = any(
        p["visibility"] != "private" and can_publish(context)[0]
        for p in posts)
    consent_word = "connected" if any_live_publish else "ready"
    return (
        '<section class="social-feed" data-feature="social_feed" '
        'data-feed-status="built" data-consent="%s">'
        '<h2 class="feed-title">Social Feed</h2>'
        '<div class="feed-posts">%s</div>'
        '%s'
        '</section>'
        % (consent_word,
           "".join(_post_html(p, context) for p in live),
           _drafts_html(drafts, context))
    )
