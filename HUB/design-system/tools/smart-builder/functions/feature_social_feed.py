#!/usr/bin/env python3
"""feature.social_feed — "Personal social feed" (Smart Builder feature breaker).

Capability contract (functions/registry.json):
  id: feature.social_feed, version 1.0.0, status tracked in the registry.
  activated_by: contract.features.social_feed — the CONTRACT flips the
  breaker; the module never hand-wires itself into a page.

Activation input (from the contract, which carries the intake's answers):
  contract.features.social_feed = {
      "enabled": true,
      "title": "Fresh from the oven",  # optional
      "audience": "public",             # public | members | private;
                                     # omitted -> the privacy dial decides
      "posts": [                        # optional, max 50
          {"text": "...", "url": "https://...", "time": "2026-10-17",
           "audience": "public"}        # omitted -> the feed's audience
      ],
      "live": true,                    # optional: live updates via connection
      "feed_url": "https://..."        # live feed endpoint (needs connection)
  }
READY vs CONNECTED (consent line, product rule 21:41Z) — two distinct
states, never conflated:
  READY (default): the snapshot posts from the contract render with zero
      grants. Installed, working, usable immediately.
  CONNECTED (explicit consent only): "live": true — live updates via the
      network connection. Activates ONLY on the recorded grant
      contract.connections.network == true (the user's explicit opt-in).
      The grant is mirrored in the build receipt for audit. Requesting
      live updates without the grant is a structured refusal naming the
      missing grant — never a crash, never a staged auto-refresh that
      pretends to work.
The section's copy never says "connected" when the feature is merely ready.

Contract-level settings this module consumes (resolved in decl_for):
  contract["privacy"] = "private" | "network" | "public" (default "private").
      Validated; anything else -> SocialFeedRefusal('bad_privacy_dial').
      When the declaration omits audience, the dial decides:
      private->private, network->members, public->public. A post that omits
      its audience inherits the feed's resolved audience. Explicit choices
      always win — public is a legitimate first-class choice, never framed
      as a violation, never warned against.
  contract["connections"] = {"muse":..,"github":..,"network":..,"nayanet":..}
      (default all false; missing block = all false). Malformed block ->
      SocialFeedRefusal('bad_connections_block').

Behavior:
  - Not declared (or enabled falsy) -> render nothing. The page refuses
    to render a feed the contract did not declare.
  - THREE-STATE (product rule 21:32Z): explicit true/false honored exactly;
    an omitted flag follows assembler default policy (opt-in today). The
    module never hardcodes an on/off default — it renders the resolved
    state the assembler hands it.
  - DAY-ONE (product rule 21:34Z): a minimal contract (no optional blocks,
    no connections, no privacy set) renders a useful section with zero errors.
  - Declared + registry says built -> feed section with the visible posts.
    The snapshot posts come from the contract — no grant needed (READY).
  - "live": true is an explicit opt-in and a CONNECTED capability
    (grant: contract.connections.network):
      - grant absent -> SocialFeedRefusal('grant_required') naming
        connections.network. Ready but not connected; the build refuses
        rather than staging a fake live feed.
      - grant present + feed_url -> the snapshot plus a real "view live
        feed" anchor (sanitized, verified href) and an honest
        "Connected via the network" status line.
      - grant present, no feed_url -> honest "no live feed URL configured"
        state (the grant exists, so "connected" is accurate here).
    The grant mirror goes in the build receipt (social_feed.live.connected).
  - Declared + registry says anything else ->
    SocialFeedRefusal('feature_not_built'). The contract never advertises a
    capability as operational unless the registry says it is built.
  - Privacy law of this module (private_post_not_leaked — acceptance):
    a post renders ONLY when the post's audience AND the feed's audience
    are both "public". Anything else is dropped from the render — never
    leaked onto a page the audience cannot see.
  - No posts visible -> honest empty state ("Nothing posted yet"), never
    an empty list pretending to be a feed.
  - Hostile post/feed URLs -> SocialFeedRefusal('unsafe_post_url' /
    'unsafe_feed_url'), fail closed. Allowed: absolute http(s) URLs only —
    every href verified (lesson L-2026-10-17-002).
  - Overlong text / bad shapes -> structured refusals, never silent
    truncation or improvisation.
  - All rendered text is HTML-escaped.

Stdlib only. Pure functions — same declaration -> same bytes, always.
"""
import html as htmlmod
from urllib.parse import urlparse

VERSION = "1.0.0"
FEATURE_ID = "feature.social_feed"
# aliases the assembler imports
FEATURE_SOCIAL_FEED_ID = FEATURE_ID
FEATURE_SOCIAL_FEED_VERSION = VERSION
FEATURE_VERSION = VERSION  # uniform interface for the assembler

AUDIENCES = ("public", "members", "private")
PRIVACY_LEVELS = ("private", "network", "public")
CONNECTION_KEYS = ("muse", "github", "network", "nayanet")
# Privacy dial -> default feed audience. "network" (visible to the network,
# not the open web) maps to members: the network's members, no further.
PRIVACY_TO_AUDIENCE = {"private": "private", "network": "members",
                       "public": "public"}

MAX_TITLE = 120
MAX_POSTS = 50
MAX_POST_TEXT = 2000
MAX_TIME = 64


class SocialFeedRefusal(Exception):
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


# Uniform interface for the assembler's additive registration block.
Refusal = SocialFeedRefusal


def esc(s):
    return htmlmod.escape(str(s), quote=True)


def clean_text(s, field, max_len, too_long_code):
    """Text fields are escaped at render; control characters and overlong
    input are refused, never silently stripped or truncated."""
    if not isinstance(s, str):
        raise SocialFeedRefusal("unsafe_post_text",
                                "%s: not a string (%s)"
                                % (field, type(s).__name__))
    if any(ord(c) < 0x20 and c not in "\n\t" for c in s):
        raise SocialFeedRefusal("unsafe_post_text",
                                "%s: control characters in text" % field)
    if len(s) > max_len:
        raise SocialFeedRefusal(too_long_code,
                                "%s: %d chars, max %d"
                                % (field, len(s), max_len))
    return s


def sanitize_post_url(url):
    """Allowlist post links: absolute http(s) only. Returns the cleaned URL,
    None when absent, raises SocialFeedRefusal('unsafe_post_url') otherwise."""
    if url is None:
        return None
    if not isinstance(url, str):
        raise SocialFeedRefusal("unsafe_post_url",
                                "not a string (%s)" % type(url).__name__)
    u = url.strip()
    if not u:
        return None
    if any(ord(c) < 0x20 for c in u):
        raise SocialFeedRefusal("unsafe_post_url",
                                "control characters in URL")
    p = urlparse(u)
    scheme = (p.scheme or "").lower()
    if scheme not in ("http", "https"):
        reason = "relative URLs are not allowed" if not scheme \
            else "disallowed scheme %r" % p.scheme
        raise SocialFeedRefusal("unsafe_post_url", reason)
    if not p.hostname:
        raise SocialFeedRefusal("unsafe_post_url", "URL has no host")
    if any(c.isspace() for c in p.hostname):
        raise SocialFeedRefusal("unsafe_post_url", "whitespace in host")
    return u


def sanitize_feed_url(url):
    """Allowlist live-feed endpoints: absolute http(s) only. Returns the
    cleaned URL, None when absent, raises
    SocialFeedRefusal('unsafe_feed_url') otherwise — every href verified
    (lesson L-2026-10-17-002)."""
    if url is None:
        return None
    if not isinstance(url, str):
        raise SocialFeedRefusal("unsafe_feed_url",
                                "not a string (%s)" % type(url).__name__)
    u = url.strip()
    if not u:
        return None
    if any(ord(c) < 0x20 for c in u):
        raise SocialFeedRefusal("unsafe_feed_url",
                                "control characters in URL")
    p = urlparse(u)
    scheme = (p.scheme or "").lower()
    if scheme not in ("http", "https"):
        reason = "relative URLs are not allowed" if not scheme \
            else "disallowed scheme %r" % p.scheme
        raise SocialFeedRefusal("unsafe_feed_url", reason)
    if not p.hostname:
        raise SocialFeedRefusal("unsafe_feed_url", "URL has no host")
    if any(c.isspace() for c in p.hostname):
        raise SocialFeedRefusal("unsafe_feed_url", "whitespace in host")
    return u


def sanitize_audience(a, field):
    """Validate an explicit audience. Omitted audiences never reach here —
    decl_for fills them from the privacy dial (feed level) or the feed's
    resolved audience (post level) first."""
    if not isinstance(a, str) or a.strip().lower() not in AUDIENCES:
        raise SocialFeedRefusal("bad_feed_audience",
                                "%s: must be one of %s, got %r"
                                % (field, "/".join(AUDIENCES), a))
    return a.strip().lower()


def resolve_privacy(contract):
    """The privacy dial: contract['privacy'], default 'private'. Anything
    outside the fixed vocabulary is a structured refusal — fail closed."""
    p = contract.get("privacy", "private")
    if p is None:
        return "private"
    if not isinstance(p, str) or p not in PRIVACY_LEVELS:
        raise SocialFeedRefusal("bad_privacy_dial",
                                "contract.privacy must be one of %s, got %r"
                                % ("/".join(PRIVACY_LEVELS), p))
    return p


def resolve_connections(contract):
    """The connections block: missing block = all false. A malformed block
    is a structured refusal — the module never guesses at connectivity."""
    c = contract.get("connections", None)
    if c is None:
        return {k: False for k in CONNECTION_KEYS}
    if not isinstance(c, dict):
        raise SocialFeedRefusal("bad_connections_block",
                                "contract.connections must be an object, got %s"
                                % type(c).__name__)
    return {k: bool(c.get(k, False)) for k in CONNECTION_KEYS}


def sanitize_post(p, idx, default_audience):
    """Validate one post. Returns a cleaned dict. Anything malformed is a
    structured refusal — the feed never improvises a post. A post that
    omits its audience inherits the feed's resolved audience (an explicit
    audience always wins)."""
    if not isinstance(p, dict):
        raise SocialFeedRefusal("bad_post",
                                "post %d: must be an object, got %s"
                                % (idx, type(p).__name__))
    text = p.get("text")
    if not isinstance(text, str) or not text.strip():
        raise SocialFeedRefusal("bad_post",
                                "post %d: text is required" % idx)
    aud = p.get("audience")
    aud = default_audience if aud is None else sanitize_audience(
        aud, "posts[%d].audience" % idx)
    return {
        "text": clean_text(text, "posts[%d].text" % idx,
                            MAX_POST_TEXT, "post_text_too_long"),
        "url": sanitize_post_url(p.get("url")),
        "time": clean_text(str(p.get("time") or ""), "posts[%d].time" % idx,
                            MAX_TIME, "post_time_too_long")
        if p.get("time") is not None else "",
        "audience": aud,
    }


def decl_for(contract):
    """Extract the social_feed declaration from a contract, or None.

    Accepts the PLUMBING.md breaker convention
    (contract.features.social_feed):
      - dict  -> the declaration (enabled/title/audience/posts/live)
      - True  -> enabled with empty fields (private-by-default fallback)
      - falsy / absent / features-not-a-dict -> None (not declared)
      - anything else truthy -> SocialFeedRefusal('bad_social_feed_declaration')

    When declared, the privacy dial fills an omitted audience (and an
    omitted post audience inherits the feed's resolved audience); the
    connections block is resolved. Both ride the returned decl — render
    consumes them and never re-reads the contract.
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
        decl = {"enabled": True}
    if not isinstance(decl, dict):
        raise SocialFeedRefusal("bad_social_feed_declaration",
                                "contract.features.social_feed must be an "
                                "object or true, got %s" % type(decl).__name__)
    decl = dict(decl)  # copy: resolved contract-level settings ride along
    if decl.get("audience") is None:
        # Privacy dial decides the default; explicit audience always wins.
        decl["audience"] = PRIVACY_TO_AUDIENCE[resolve_privacy(contract)]
    else:
        resolve_privacy(contract)  # validate the dial even when unused
    feed_audience = decl["audience"]
    posts = decl.get("posts")
    if isinstance(posts, list):
        fixed = []
        for p in posts:
            if isinstance(p, dict) and p.get("audience") is None:
                p = dict(p)
                p["audience"] = feed_audience
            fixed.append(p)
        decl["posts"] = fixed
    decl["_connections"] = resolve_connections(contract)
    return decl


def render_post(p):
    link = (' <a href="%s">Read more</a>' % esc(p["url"])) if p["url"] else ""
    time = ('<span class="feed-time">%s</span>' % esc(p["time"])) \
        if p["time"] else ""
    return ('<article class="feed-post"><p>%s%s</p>%s</article>'
            % (esc(p["text"]), link, time))


def render_social_feed(decl, registry_status, context=None):
    """Render the feed section.

    Returns (html, connected): html is '' when the contract did not declare
    social_feed; connected lists the CONNECTED capabilities actually wired,
    each as {"event", "grant"} for the receipt's grant mirror.
    Raises SocialFeedRefusal on anything the contract must not get.

    registry_status: the registry's status string for feature.social_feed.
    Rendering is proof the registry says 'built' — the page carries
    data-social_feed-status="built" as the binding.
    """
    if decl is None or not decl.get("enabled"):
        return "", []  # not declared -> refuse to render a feed
    if registry_status != "built":
        raise SocialFeedRefusal(
            "feature_not_built",
            "contract declares social_feed but registry status is %r "
            "(contract never activates an unbuilt capability)" % (registry_status,))

    title = clean_text(str(decl.get("title") if decl.get("title") is not None
                           else "Updates"), "title", MAX_TITLE,
                       "feed_title_too_long")
    audience = sanitize_audience(decl.get("audience"), "audience")
    raw_posts = decl.get("posts")
    if raw_posts is None:
        raw_posts = []
    if not isinstance(raw_posts, list):
        raise SocialFeedRefusal("bad_post", "posts must be a list, got %s"
                                % type(raw_posts).__name__)
    if len(raw_posts) > MAX_POSTS:
        raise SocialFeedRefusal("too_many_posts",
                                "%d posts, max %d"
                                % (len(raw_posts), MAX_POSTS))
    posts = [sanitize_post(p, i, audience) for i, p in enumerate(raw_posts)]

    # private_post_not_leaked: a post reaches the page ONLY when the post
    # itself AND the feed are both explicitly public. Everything else is
    # dropped from the render — silently is correct here, because the
    # alternative (rendering, or refusing the whole feed) either leaks or
    # breaks the page over one mislabeled post.
    visible = [p for p in posts
               if audience == "public" and p["audience"] == "public"]

    if visible:
        body = "".join(render_post(p) for p in visible)
    elif audience != "public":
        body = ('<p class="breaker-sub">This feed is %s — posts appear for '
                'its audience inside the Hub, never on this public page.</p>'
                % esc(audience))
    else:
        body = ('<p class="breaker-sub">Nothing posted yet — your world, '
                'live, soon.</p>')

    # Live updates are a CONNECTED capability: they activate ONLY on the
    # recorded grant. Requesting them without the grant is a structured
    # refusal naming the missing grant — the consent line is a hard line,
    # never a staged auto-refresh that pretends to work.
    live_html = ""
    connected = []
    if decl.get("live"):
        conns = decl.get("_connections") or {}
        furl = sanitize_feed_url(decl.get("feed_url"))
        if not conns.get("network"):
            raise SocialFeedRefusal(
                "grant_required",
                "feature.social_feed live updates are ready but not "
                "connected: they need the grant contract.connections.network "
                "(the user's explicit opt-in)")
        if furl:
            live_html = ('<p class="breaker-sub">Connected via the network — '
                         '<a href="%s">view the live feed</a>.</p>'
                         % esc(furl))
            connected.append({"event": "social_feed.live.connected",
                              "grant": "connections.network"})
        else:
            live_html = ('<p class="breaker-sub">The network is connected, '
                         'but no live feed URL is configured.</p>')

    return (
        '<section class="breaker breaker-feed" data-feature="social_feed" '
        'data-social_feed-status="built" aria-label="%s">'
        '<h3 class="breaker-title">%s</h3>%s%s</section>'
        % (esc(title), esc(title), body, live_html)
    ), connected
