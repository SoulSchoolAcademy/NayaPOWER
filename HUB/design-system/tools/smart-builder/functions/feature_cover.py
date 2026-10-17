#!/usr/bin/env python3
"""feature.cover — "Cover + picture" (Smart Builder feature breaker).

Capability contract (functions/registry.json):
  id: feature.cover, version 1.0.0, status tracked in the registry.
  activated_by: contract.features.cover — the CONTRACT flips the breaker;
  the module never hand-wires itself into a page.

Activation input (from the contract, which carries the intake's uploads):
  contract.features.cover = {
      "enabled": true,
      "photo_url": "https://... (owner's picture, optional)",
      "cover_url": "https://... (cover photo, optional)",
      "name": "Morning Crumb",
      "tagline": "Warm bread · order ahead"
  }

Behavior:
  - Not declared (or enabled falsy) -> render nothing. The page refuses
    to render cover the contract did not declare.
  - Declared + registry says built -> personal header HTML.
  - Declared + registry says anything else -> CoverRefusal('feature_not_built').
    The contract never advertises a capability as operational unless the
    registry says it is built.
  - Unsafe image URLs -> CoverRefusal('unsafe_cover_url'), fail closed.
    Allowed: absolute http(s) URLs, and data: URLs that are images.
    Rejected: javascript:, vbscript:, file:, ftp:, non-image data:,
    relative URLs, anything with control characters.
  - Declared but URLs absent -> graceful fallback: initials avatar +
    gradient cover banner, never an <img> with an empty src.

Stdlib only. Pure functions — same declaration -> same bytes, always.
"""
import html as htmlmod
from urllib.parse import urlparse

VERSION = "1.0.0"
FEATURE_ID = "feature.cover"
# aliases the assembler imports
FEATURE_COVER_ID = FEATURE_ID
FEATURE_COVER_VERSION = VERSION


class CoverRefusal(Exception):
    """Structured refusal: the cover breaker declined to activate.

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


def sanitize_image_url(url, field):
    """Allowlist image URLs. Returns the cleaned URL, None when absent,
    raises CoverRefusal('unsafe_cover_url') for anything hostile."""
    if url is None:
        return None
    if not isinstance(url, str):
        raise CoverRefusal("unsafe_cover_url",
                           "%s: not a string (%s)" % (field, type(url).__name__))
    u = url.strip()
    if not u:
        return None
    if any(ord(c) < 0x20 for c in u):
        raise CoverRefusal("unsafe_cover_url",
                           "%s: control characters in URL" % field)
    p = urlparse(u)
    scheme = (p.scheme or "").lower()
    if scheme in ("http", "https"):
        if not p.hostname:
            raise CoverRefusal("unsafe_cover_url",
                               "%s: %s URL has no host" % (field, scheme))
        if any(c.isspace() for c in p.hostname):
            raise CoverRefusal("unsafe_cover_url",
                               "%s: whitespace in host" % field)
        return u
    if scheme == "data":
        mediatype = u[5:].split(",", 1)[0].split(";")[0].strip().lower()
        if mediatype.startswith("image/") and "," in u:
            return u
        raise CoverRefusal("unsafe_cover_url",
                           "%s: data: URL is not an image" % field)
    reason = "relative URLs are not allowed" if not scheme \
        else "disallowed scheme %r" % p.scheme
    raise CoverRefusal("unsafe_cover_url", "%s: %s" % (field, reason))


def decl_for(contract):
    """Extract the cover declaration from a contract, or None.

    Accepts the PLUMBING.md breaker convention (contract.features.cover):
      - dict  -> the declaration (task shape: enabled/photo_url/cover_url/…)
      - True  -> enabled with empty fields
      - falsy / absent / features-not-a-dict -> None (not declared)
      - anything else truthy -> CoverRefusal('bad_cover_declaration')
    """
    feats = contract.get("features") if isinstance(contract, dict) else None
    if not isinstance(feats, dict):
        return None  # contract-page contracts carry features as a list
    if "cover" not in feats:
        return None
    decl = feats["cover"]
    if not decl:
        return None
    if decl is True:
        return {"enabled": True}
    if isinstance(decl, dict):
        return decl
    raise CoverRefusal("bad_cover_declaration",
                       "contract.features.cover must be an object or true, "
                       "got %s" % type(decl).__name__)


def initials_for(name):
    """Graceful identity fallback: first letters of the first two words."""
    words = [w for w in str(name or "").split() if w]
    letters = "".join(w[0] for w in words[:2]).upper()
    return letters or "N"


def render_cover(decl, registry_status, context=None):
    """Render the personal header. Returns '' when the contract did not
    declare cover; raises CoverRefusal otherwise.

    registry_status: the registry's status string for feature.cover.
    Rendering is proof the registry says 'built' — the page carries
    data-cover-status="built" as the binding.
    context: resolved contract context {'connections': {...}, 'privacy': ...}.
    Connections stay OPT-IN inside modules: cover needs no connection, so
    it ignores context today; connection-gated modules must render UI +
    an honest "connect to enable" when their connection is off — never
    blocked, never faked.
    """
    if decl is None or not decl.get("enabled"):
        return ""  # not declared -> refuse to render cover
    if registry_status != "built":
        raise CoverRefusal(
            "feature_not_built",
            "contract declares cover but registry status is %r "
            "(contract never activates an unbuilt capability)" % (registry_status,))

    name = str(decl.get("name") or "").strip()
    if not name:
        # centralized identity: one person, one connected smart world. The
        # contract's identity block resolves once in the assembler; modules
        # fall back to it, templates never redefine it.
        ident = (context or {}).get("identity") or {}
        name = str(ident.get("name") or "").strip()
    tagline = str(decl.get("tagline") or "").strip()
    display_name = name or "Your page"
    alt_owner = name or "the owner"

    photo = sanitize_image_url(decl.get("photo_url"), "photo_url")
    cover = sanitize_image_url(decl.get("cover_url"), "cover_url")

    if photo:
        ava = ('<img class="cover-ava" src="%s" alt="Portrait of %s" '
               'loading="lazy">' % (esc(photo), esc(alt_owner)))
    else:
        ava = ('<div class="cover-ava cover-ava-fallback" role="img" '
               'aria-label="Portrait of %s">%s</div>'
               % (esc(alt_owner), esc(initials_for(name))))
    if cover:
        banner = ('<img class="cover-photo" src="%s" alt="Cover photo for %s" '
                  'loading="lazy">' % (esc(cover), esc(alt_owner)))
    else:
        banner = ('<div class="cover-photo cover-photo-fallback" '
                  'aria-hidden="true"></div>')

    tag = ('<p class="cover-tagline">%s</p>' % esc(tagline)) if tagline else ""
    return (
        '<div class="cover" data-feature="cover" data-cover-status="built">'
        '<div class="cover-banner">%s'
        '<div class="cover-scrim" aria-hidden="true"></div></div>'
        '<div class="cover-id">%s'
        '<div class="cover-who"><h1 class="cover-name">%s</h1>%s</div>'
        '</div></div>'
        % (banner, ava, esc(display_name), tag)
    )
