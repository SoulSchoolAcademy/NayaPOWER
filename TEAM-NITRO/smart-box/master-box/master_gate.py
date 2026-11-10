#!/usr/bin/env python3
"""master_gate.py - the permission model as code, for the master box.

The master/collective Smart Box (owner ``collective``, kind ``master``)
extends the Smart Box gate (``gate.py``, verbatim) with the permission
model Shawn settled 01:31Z Nov 10 (MEMORY.md, THE PERMISSION MODEL -
CORRECTED, which supersedes the 01:24Z framing):

    Mail and instant messages: NEVER read - no toggle, no exception.
        That is the line.
    Naya Notes: ADJUSTABLE - the owner's choice. On or off; who sees
        them - your team, select people, a group, which pages - or
        private. We SUGGEST allowing your NIAs to read them (they read
        each other's notes, and they can turn your Naya Notes into
        Smart Notes for you) - but only if you want. If you don't want
        them read, you can say so: she can make notes for you and still
        not read them.
    Smart Notes: shared by definition - that is what makes them Smart
        Notes, the official notes to the collective - but your identity
        is your choice (anonymous, alias, or in your name).
    Team NIAs have full permission to access, because we're a team. A
        Naya not part of the team gets no permission. Users may give
        more or less permission to another user - controlled in
        Settings, the level of privacy.
    Private communication stays private: nobody is listening, and
        anything you note, nobody is looking at it unless you choose
        to make it a smart note.

The content-kind line runs BEFORE the gate, because the gate alone
cannot see what kind of thing it is being asked about:

    may_touch_master_box(block, actor, action, content_kind,
                         key_registry=None) -> "ALLOW" / "DENY"

    "mail" / "message"  -> DENY, always, for every actor, every
                           action. No toggle, no exception. The
                           master box never holds mail, so there is
                           nothing to allow.
    "personal-box-content" -> DENY, always. The master box holds
                           personal boxes by id only, never their
                           contents. A read of a personal box's
                           contents through the master box is a
                           denial by construction.
    "naya-note"         -> DENY by default. ALLOW (read only) only
                           when the owner opened that note to that
                           actor by name (``body_open_to`` on the
                           block) - the owner's Settings choice,
                           recorded, never assumed. The gate's own
                           rule 2 already says this for raw bodies;
                           this line makes the default explicit for
                           the master box: no opening recorded means
                           no read, even for a team Naya with a live
                           key.
    "smart-note"        -> the gate decides (``may_share`` verbatim):
                           the owner, a public smart note anyone may
                           read, a team Naya with a live collective
                           key organizing / retrieving for the
                           collective, sharing only what is public.

Team membership is the key registry, not a hardcoded roster: a team
Naya is one the collective owner minted a live key for
(``KeyRegistry.mint("collective", naya_id)``). A Naya with no live
collective key - non-team, or no key at all - denies on every keyed
path, exactly as ``gate.py`` denies. No roster is invented here; the
registry IS the roster, and it is minted one seat at a time, on the
record, in the master box's own ``keys.jsonl``.

``SETTINGS_SHAPE`` is the Settings shape as data - a spec of the
privacy levels, not a build of Settings. It records what the levels
are so a fresh agent recovers them from the master box alone.

Standard library only. No credentials, no secrets, no key material.
This file never reads mail, messages, or Naya Notes - it only decides
whether a read may happen, and for mail and messages the answer is
always no.
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_PARENT = os.path.dirname(_HERE)
for _path in (_HERE, _PARENT):
    if _path not in sys.path:
        sys.path.insert(0, _path)

from gate import ALLOW, DENY, KeyRegistry, may_share  # noqa: E402,F401

MASTER_OWNER = "collective"

CONTENT_KINDS = ("smart-note", "naya-note", "mail", "message",
                 "personal-box-content")

# The Settings shape, as data (a spec of the levels, not a build of
# Settings). Harvested from MEMORY.md (01:31Z Nov 10, corrected
# permission model) and the notification spec §4 (Oct 27 toggles,
# unchanged). A fresh agent recovers the privacy levels from this
# dict alone.
SETTINGS_SHAPE = {
    "mail_and_messages": {
        "readable": False,
        "toggle": None,
        "rule": "NEVER read - no toggle, no exception. That is the line.",
    },
    "naya_notes": {
        "readable": "owner choice",
        "default": "private - not read",
        "options": ["private", "team", "select people", "group",
                    "pages"],
        "suggestion": "Allow your NIAs to read them, so they read "
                      "each other's notes and can turn your Naya "
                      "Notes into Smart Notes for you - only if you "
                      "want.",
        "rule": "If you do not want them read, you can say so: she "
                "can make notes for you and still not read them.",
    },
    "smart_notes": {
        "shared": True,
        "rule": "Shared by definition - that is what makes them "
                "Smart Notes, the official notes to the collective.",
        "identity": ["anonymous", "alias", "in your name"],
    },
    "scope": ["whole NayaNET", "one project", "one page",
              "several pages"],
    "channels": {
        "in_system": "ON",
        "email": "OFF until an email is entered AND turned on",
        "sounds": "OFF",
    },
    "team_access": "Team NIAs have full permission to access, "
                   "because we're a team. A Naya not part of the "
                   "team gets no permission.",
    "privacy_control": "Users may give more or less permission to "
                       "another user - controlled in Settings, the "
                       "level of privacy.",
    "private_communication": "Private communication stays private: "
                             "nobody is listening, and anything you "
                             "note, nobody is looking at it unless "
                             "you choose to make it a smart note.",
}


def is_team_naya(actor, key_registry=None):
    """True only when the actor holds a live collective key.

    The registry is the roster: a live key minted by the collective
    owner for this Naya. No registry, no live key, or a key for
    another owner all come back False - and False always means DENY
    further down.
    """
    if key_registry is None:
        return False
    for key in actor.get("keys") or []:
        if key_registry.check(key.key_id, MASTER_OWNER,
                              actor.get("id")):
            return True
    return False


def may_touch_master_box(block, actor, action, content_kind,
                         key_registry=None):
    """ALLOW or DENY for a touch on the master box. Default DENY.

    The content-kind line runs first, before the gate: mail, messages,
    and personal-box contents deny for every actor, every action, no
    exception. Naya Notes deny by default and allow (read only) only
    on the owner's recorded opening. Smart Notes fall through to the
    gate (``may_share`` verbatim), which needs a live collective key
    for every keyed path.
    """
    if not isinstance(block, dict) or not isinstance(actor, dict):
        return DENY
    if content_kind not in CONTENT_KINDS:
        return DENY

    # The inviolable line: mail and messages are NEVER read through
    # the master box - no toggle, no exception, not even by the owner.
    if content_kind in ("mail", "message"):
        return DENY

    # The mother never enters a personal box: the master box holds
    # personal boxes by id only, so their contents are never here to
    # be read. Any read of them through this box denies.
    if content_kind == "personal-box-content":
        return DENY

    # Naya Notes are adjustable, per the owner's choice (01:31Z Nov
    # 10). Default is DENY. The owner's recorded opening
    # (``body_open_to``) is the only thing that opens one - and it
    # opens a read, never organize / share / retrieve on its own.
    if content_kind == "naya-note":
        if action == "read" and actor.get("id") in (
                block.get("body_open_to") or []):
            return ALLOW
        return DENY

    # Smart Notes: the gate decides. A team Naya needs a live
    # collective key; anyone may read a public smart note; the owner
    # (the collective itself) may do anything with its own blocks.
    return may_share(block, actor, action, key_registry=key_registry)


def check_master_box_integrity(blocks):
    """The master box holds collective intelligence only.

    Returns a list of violations (empty = clean). Every block must
    be owned by ``collective``; every block's ``raw`` must name its
    content kind, and that kind must be ``smart-note`` (collective
    intelligence) or ``manifest`` (the children list, ids only).
    No mail, no message, no Naya Note content, no personal-box
    content may be present - the check is by kind and by owner, not
    by scanning words, because the permission rules themselves
    legitimately NAME mail and Naya Notes in plain words.
    """
    violations = []
    for block in blocks:
        block_id = block.get("id", "")
        owner = (block.get("who") or {}).get("owner")
        if owner != MASTER_OWNER:
            violations.append("%s: owner is %r, not collective"
                              % (block_id, owner))
        raw = block.get("raw") or {}
        kind = raw.get("content_kind") if isinstance(raw, dict) else None
        if kind not in ("smart-note", "manifest"):
            violations.append(
                "%s: content_kind is %r, not smart-note/manifest"
                % (block_id, kind))
        if not block_id.startswith(MASTER_OWNER + ":"):
            violations.append("%s: id is not namespaced collective:"
                              % block_id)
    return violations
