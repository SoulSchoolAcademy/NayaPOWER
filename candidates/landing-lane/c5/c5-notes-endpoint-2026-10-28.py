#!/usr/bin/env python3
"""C5 NOTES ENDPOINT — workspace prototype (2026-10-28). NOT live.

Implements the guard logic of c5-notes-endpoint-2026-10-28.md against an
injected store. The service layer holds NO note data: every read and
write goes through the store. A MemoryNoteStore stands in for the SQL
layer in tests; the landing implementer replaces it with the §5 SQL
shape (read entries, client_id pre-check, length-guarded append,
verify by re-read). This module proves the guard logic, NOT the
transport, and it is never presented as live.

Conventions (mirroring B1 serve-ready):
  serve_list()   -> (200, envelope) | (404, error) | (503, error)
  serve_append() -> (200, envelope) | (400, error) | (503, error)
  A 503 body carries NO notes key, by construction. Never a snapshot.

No file I/O, no network, no module-global note state. Stdlib only.
"""

import uuid
from datetime import datetime, timezone


class NotesUnavailable(Exception):
    """The record did not answer (read, append, or verify failed)."""


class InvalidNote(Exception):
    """Validation failure; carries the offending field name."""

    def __init__(self, field):
        super().__init__(field)
        self.field = field


class UnknownItem(Exception):
    """The read succeeded and the item_key is not in the store."""


def _now_z():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def new_client_id():
    """One client_id per note, generated once by the caller."""
    return str(uuid.uuid4())


class MemoryNoteStore:
    """In-memory store implementing the C5 store contract.

    Keys: item_key string, or None for the project feed (hub-row array).
    Values: lists of note dicts in stored order. The append_guarded
    method enforces the length guard exactly as the SQL layer must:
    it refuses the write when the length moved since the caller's read.
    """

    def __init__(self):
        self._feeds = {}

    def read(self, item_key):
        # Project feed (None) always exists (the hub row). A string
        # key that was never created is unknown, not empty.
        if item_key is not None and item_key not in self._feeds:
            raise UnknownItem(item_key)
        return [dict(n) for n in self._feeds.get(item_key, [])]

    def create_item(self, item_key):
        """Register an item_key as known (empty feed). Landing-side
        equivalent: the row exists in work_items."""
        self._feeds.setdefault(item_key, [])

    def append_guarded(self, item_key, note, expected_len):
        current = self._feeds.get(item_key, [])
        if len(current) != expected_len:
            return False  # length guard refused: a race, not a success
        self._feeds.setdefault(item_key, []).append(dict(note))
        return True


class FaultyStore:
    """Wraps a store to simulate transport failures for tests.

    fail_reads: every read raises NotesUnavailable.
    fail_append_after_land: the first append lands the write, then
      raises (lost-response simulation). Subsequent calls behave.
    race_hook: callable invoked between the service's read and its
      guarded append; used to inject a racing entry.
    """

    def __init__(self, inner, fail_reads=False,
                 fail_append_after_land=False, race_hook=None):
        self._inner = inner
        self.fail_reads = fail_reads
        self.fail_append_after_land = fail_append_after_land
        self.race_hook = race_hook
        self._landed_once = False

    def read(self, item_key):
        if self.fail_reads:
            raise NotesUnavailable("read failed")
        return self._inner.read(item_key)

    def create_item(self, item_key):
        return self._inner.create_item(item_key)

    def append_guarded(self, item_key, note, expected_len):
        if self.race_hook is not None:
            hook, self.race_hook = self.race_hook, None
            hook()
        ok = self._inner.append_guarded(item_key, note, expected_len)
        if self.fail_append_after_land and not self._landed_once:
            self._landed_once = True
            raise NotesUnavailable("response lost after landing")
        return ok


def _validate(from_alias, note_text, client_id):
    if not from_alias or not str(from_alias).strip():
        raise InvalidNote("from")
    if not note_text or not str(note_text).strip():
        raise InvalidNote("note")
    if not client_id or not str(client_id).strip():
        raise InvalidNote("client_id")


MAX_GUARD_RETRIES = 5


def append_note(store, item_key, from_alias, note_text, client_id):
    """Guarded append (spec §4). Returns (note, duplicate, position).

    Raises InvalidNote, UnknownItem, NotesUnavailable. Never appends
    twice for one client_id. Every retry is a new decision: on a
    length-guard refusal the whole algorithm re-runs from a fresh read,
    bounded at MAX_GUARD_RETRIES refusals (then 503) so sustained
    contention cannot spin forever.
    """
    _validate(from_alias, note_text, client_id)
    guard_retries = 0
    while True:
        try:
            entries = store.read(item_key)
        except UnknownItem:
            raise
        except NotesUnavailable:
            raise
        for existing in entries:
            if existing.get("client_id") == client_id:
                pos = entries.index(existing) + 1
                return dict(existing), True, pos
        note = {"at": _now_z(), "from": from_alias,
                "note": note_text, "client_id": client_id}
        try:
            ok = store.append_guarded(item_key, note, len(entries))
        except NotesUnavailable:
            # Lost response: the write may have landed. Re-read once;
            # a present note means DONE, never re-sent.
            entries = store.read(item_key)
            for existing in entries:
                if existing.get("client_id") == client_id:
                    return dict(existing), False, entries.index(existing) + 1
            raise NotesUnavailable("append response lost, note absent")
        if not ok:
            # Length guard refused (a race). New decision: re-read,
            # bounded so sustained contention ends in 503, not a spin.
            guard_retries += 1
            if guard_retries > MAX_GUARD_RETRIES:
                raise NotesUnavailable("guard refused repeatedly")
            continue
        try:
            verify = store.read(item_key)
        except NotesUnavailable:
            raise
        if (len(verify) == len(entries) + 1
                and verify[-1].get("client_id") == client_id):
            return dict(note), False, len(verify)
        # Verify mismatch: re-read once more (lost-response rule).
        verify = store.read(item_key)
        for existing in verify:
            if existing.get("client_id") == client_id:
                return dict(existing), False, verify.index(existing) + 1
        raise NotesUnavailable("append not verified")


def list_notes(store, item_key):
    """Feed read in stored order. Returns the note list (copies)."""
    return store.read(item_key)


def serve_list(store, item_key):
    """HTTP-shaped list: (status, body). 503 carries no notes key."""
    try:
        notes = list_notes(store, item_key)
    except UnknownItem:
        return 404, {"error": "unknown_item"}
    except NotesUnavailable:
        return 503, {"error": "notes_unavailable"}
    return 200, {"notes": notes, "count": len(notes), "item": item_key}


def serve_append(store, payload):
    """HTTP-shaped append: (status, body)."""
    item_key = payload.get("item")
    try:
        note, duplicate, position = append_note(
            store, item_key, payload.get("from"),
            payload.get("note"), payload.get("client_id"))
    except InvalidNote as exc:
        return 400, {"error": "invalid_note", "detail": exc.field}
    except UnknownItem:
        return 404, {"error": "unknown_item"}
    except NotesUnavailable:
        return 503, {"error": "notes_unavailable"}
    return 200, {"note": note, "position": position, "duplicate": duplicate}
