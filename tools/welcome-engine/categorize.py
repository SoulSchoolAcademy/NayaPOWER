#!/usr/bin/env python3
"""
Mail/Post Auto-Categorization — B7 of the auto-match completion plan
(2026-10-25), SN-0845 build (4): the library files itself. A thread
about a project lives with that project; a post about a topic is filed
with the space that owns that topic. Nobody files by hand.

    item (mail thread / post) -> engine vector -> score() against every
    space/project in the corpus -> filed with the best match, or
    honestly UNFILED, or REFUSED on privacy.

ITEM SHAPE (built against the closest real shapes in the repo — see the
build report): a plain dict merging the two shapes the repo already
carries, plus the one flag SN-0845's privacy law requires.

  Mail — public.v7_mail_threads + v7_mail_messages
  (supabase/migrations/20260906005326_v7_intelligent_hub_...sql):
      {"id": <thread id>, "kind": "mail",
       "subject": <v7_mail_threads.subject>,
       "body": <v7_mail_messages.body of the thread's messages>,
       "topics": [<declared topic>, ...],          # optional
       "visibility": "public"}

  Post — the room-feed/v1 item (HUB/FEEDS/emit_hub_feeds.py; every
  feed item carries exactly id / title / topics / kind, topics >= 1):
      {"id": <item id>, "kind": "post",
       "title": <title>, "body": <text>,           # body optional
       "topics": [<declared topic>, ...],
       "visibility": "public"}

  Either kind may also declare any of the engine's other fields
  ("goals", "offers", "needs", "wants") directly; declared fields pass
  through verbatim. An item is PUBLIC only when it says so:
  visibility == "public" (or the boolean spelling "public": True).
  Anything else — "private", any other value, or no flag at all — is
  not public. Default is refuse.

VECTOR BUILD (public items only — see PRIVACY):
  topics <- declared topics + phrases extracted from the title/subject
  goals  <- phrases extracted from the body, unless goals are declared
  offers / needs / wants <- declared only; content invents none.
  Extraction is the Welcome Engine's own extract_phrases — no second
  phrase splitter. The subject/title declares what an item IS ABOUT;
  the body declares what it is FOR. Those are two genuinely different
  texts, so a filed item's two signals are independent in the same
  sense two citizens' topics and goals are.

FILING BAR (the engine's own surfacing rule, unchanged): the best
candidate files only when smart_match.score() says surface — >= 2
independent signals. There is no second threshold and no force-filing:
below the bar the item is UNFILED with the reason named (no candidate /
best score below the bar / single-signal only), never silently dropped.

PRIVACY BY CONSTRUCTION (SN-0845: "Private content never feeds the
matcher"; SN-0848: matching uses declared and public signals only):
the public check is the FIRST thing categorize() does, before any
vector is built and before the corpus is touched. A non-public item's
topics, subject, and body are never read by the scorer — the refusal
is structural, not a post-filter on scored results. The vector builder
itself also refuses a non-public item, so no future caller can build
one by reaching past categorize().
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from smart_match import FIELDS, score, _clean
from welcome_engine import extract_phrases

FILEABLE_KINDS = ("space", "project")
ITEM_KINDS = ("mail", "post")


def is_public(item):
    """The one privacy gate. Public must be declared, in either of the
    two spellings the item shape carries; everything else is not
    public. A non-dict item is not public."""
    if not isinstance(item, dict):
        return False
    if item.get("visibility") is not None:
        return item.get("visibility") == "public"
    return item.get("public") is True


def _texts(item):
    """(headline, body) for either kind: mail files by subject, posts
    by title; both may carry a body."""
    headline = item.get("subject") if item.get("kind") == "mail" else item.get("title")
    if not isinstance(headline, str):
        headline = item.get("title") or item.get("subject")
    body = item.get("body")
    return (headline if isinstance(headline, str) else "",
            body if isinstance(body, str) else "")


def item_vector(item):
    """The item's 5-field engine vector. PUBLIC ITEMS ONLY — this
    builder is part of the privacy construction: it raises on a
    non-public item rather than vectorizing private content."""
    if not is_public(item):
        raise ValueError("privacy: item_vector refuses a non-public item")
    headline, body = _texts(item)
    vec = {f: [] for f in FIELDS}
    declared = item.get("topics")
    if isinstance(declared, (list, tuple)):
        vec["topics"].extend(t for t in declared if isinstance(t, str))
    elif isinstance(declared, str) and declared.strip():
        vec["topics"].append(declared)
    vec["topics"].extend(extract_phrases(headline))
    if isinstance(item.get("goals"), (list, tuple, str)):
        vec["goals"].extend(_clean({"goals": item.get("goals")})["goals"])
    else:
        vec["goals"].extend(extract_phrases(body))
    for f in ("offers", "needs", "wants"):
        if f in item:
            vec[f] = _clean({f: item.get(f)})[f]
    return {f: sorted(set(vec[f])) for f in FIELDS}


def _candidates(corpus):
    """{alias: (kind, vector)} for the corpus's spaces/projects only —
    content files with a place, never with a citizen. Accepts B2's
    corpus dict ({"entities": {alias: {"kind", "vector", ...}}}) or a
    plain {alias: vector} mapping (kind then unknown -> "space")."""
    if not isinstance(corpus, dict):
        return {}
    entities = corpus.get("entities") if isinstance(corpus.get("entities"), dict) else corpus
    out = {}
    for alias, ent in (entities or {}).items():
        if isinstance(ent, dict) and isinstance(ent.get("vector"), dict):
            kind = ent.get("kind")
            if kind in FILEABLE_KINDS:
                out[alias] = (kind, ent["vector"])
            elif kind is None and "entities" not in corpus:
                out[alias] = ("space", ent["vector"])
        elif isinstance(ent, dict):
            out[alias] = ("space", ent)  # plain {alias: vector} mapping
    return out


def categorize(item, corpus):
    """File one item. Returns exactly one of:
      filed:   {"status", "item_id", "item_kind", "alias", "kind",
                "score", "reasons", "signal_coverage_percent",
                "signals", "calibrated"}
      unfiled: {"status", "item_id", "item_kind", "reason",
                "best_alias", "best_score"}   (best_* None if no candidate)
      refused: {"status", "item_id", "item_kind", "reason"}
                — no score fields at all: nothing was scored.
    """
    item_id = item.get("id") if isinstance(item, dict) else None
    item_kind = item.get("kind") if isinstance(item, dict) else None

    # PRIVACY FIRST — before any vector, any corpus read, any scoring.
    if not is_public(item):
        return {"status": "refused", "item_id": item_id, "item_kind": item_kind,
                "reason": "privacy: item is not flagged public; private "
                          "content is never categorized or scored"}

    vec = item_vector(item)
    candidates = _candidates(corpus)
    if not any(vec[f] for f in FIELDS):
        return {"status": "unfiled", "item_id": item_id, "item_kind": item_kind,
                "reason": "no candidate: item carries no declared or "
                          "derived topics to file by",
                "best_alias": None, "best_score": None}
    if not candidates:
        return {"status": "unfiled", "item_id": item_id, "item_kind": item_kind,
                "reason": "no candidate: corpus carries no space or "
                          "project to file with",
                "best_alias": None, "best_score": None}

    best_alias, best_kind, best = None, None, None
    for alias in sorted(candidates):
        kind, cvec = candidates[alias]
        r = score(vec, cvec)
        if best is None or r["rank"] > best["rank"] or \
                (r["rank"] == best["rank"] and alias < best_alias):
            best_alias, best_kind, best = alias, kind, r

    if best["surface"]:
        return {"status": "filed", "item_id": item_id, "item_kind": item_kind,
                "alias": best_alias, "kind": best_kind,
                "score": best["score"], "reasons": best["reasons"],
                "signal_coverage_percent": best["signal_coverage_percent"],
                "signals": best["signals"], "calibrated": best["calibrated"]}
    if len(best["signals"]) == 1:
        reason = (f"single-signal only: best match {best_alias} scored "
                  f"{best['score']}% on {best['signals'][0]} alone; filing "
                  f"needs >= 2 independent signals")
    elif best["score"] == 0:
        reason = (f"no candidate: no space or project shares any signal "
                  f"with this item (best score 0%)")
    else:
        reason = (f"best score {best['score']}% below bar: best match "
                  f"{best_alias} did not clear the >= 2-signal surfacing bar")
    return {"status": "unfiled", "item_id": item_id, "item_kind": item_kind,
            "reason": reason, "best_alias": best_alias,
            "best_score": best["score"]}


def categorize_many(items, corpus):
    """Batch filing, honesty preserved per item: every input lands in
    exactly one of filed / unfiled / refused, in input order within
    each list. Nothing is force-filed and nothing is dropped."""
    out = {"filed": [], "unfiled": [], "refused": []}
    for item in items or []:
        r = categorize(item, corpus)
        out[r["status"]].append(r)
    return out
