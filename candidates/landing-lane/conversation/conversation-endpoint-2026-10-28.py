"""Conversation endpoint class — workspace prototype (NOT live).

Merged completion-list item 2: record-backed Conversation control per block.
Spec: conversation-endpoint-2026-10-28.md. Tests:
test-conversation-endpoint-2026-10-28.py.

Design, in one paragraph: the service is pure logic over a four-operation
store interface (get_messages / find_by_id / max_seq / insert). The
production adapter (gated) will implement the same four operations against
the block_conversation_messages table; this file's InMemoryStore proves the
logic with fixtures. Append is guarded: validate -> read state -> insert
only when absent -> verify by re-read -> return. A retry carrying the same
client message_id returns the stored message with duplicate=True and writes
nothing. A store failure is always ConversationUnavailable (HTTP 503
mapping); never a snapshot, never an empty list masquerading as an outage.

Stdlib only. No network, no secrets, no record writes.
"""

import uuid
from dataclasses import dataclass, asdict
from datetime import datetime, timezone

MAX_BODY_CHARS = 8000
MAX_ALIAS_CHARS = 64
DEFAULT_LIMIT = 100
MAX_LIMIT = 500

STORE_UNAVAILABLE = "conversation_store_unavailable"


class ConversationUnavailable(Exception):
    """The store did not answer, or a write failed verification.

    Maps to HTTP 503 {"error": "conversation_store_unavailable"}.
    """

    def __init__(self, detail="store unavailable"):
        super().__init__(detail)
        self.error = STORE_UNAVAILABLE
        self.detail = detail


class ValidationError(Exception):
    """Append input failed validation. Maps to HTTP 400."""

    def __init__(self, detail):
        super().__init__(detail)
        self.error = "invalid_message"
        self.detail = detail


@dataclass(frozen=True)
class Message:
    message_id: str
    block_key: str
    seq: int
    author_alias: str
    body: str
    created_at: str

    def to_dict(self):
        return asdict(self)


def _now_z():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


class ConversationStore:
    """Four-operation store interface. Production adapter must match it."""

    def get_messages(self, block_key):
        """Return [Message] for block_key in seq order. Raise on outage."""
        raise NotImplementedError

    def find_by_id(self, block_key, message_id):
        """Return Message or None. Raise on outage."""
        raise NotImplementedError

    def max_seq(self, block_key):
        """Return highest seq in block_key, or 0 when empty. Raise on outage."""
        raise NotImplementedError

    def insert(self, message):
        """Persist message. Raise on outage."""
        raise NotImplementedError


class InMemoryStore(ConversationStore):
    """Fixture store: dict per block, plus a (block, id) index.

    Single-process and serialized by construction; it proves the service
    logic, not concurrent writers (production needs UNIQUE(block_key, seq)
    plus conflict-as-new-decision — see spec §3).
    """

    def __init__(self):
        self._by_block = {}
        self._by_id = {}

    def get_messages(self, block_key):
        return list(self._by_block.get(block_key, []))

    def find_by_id(self, block_key, message_id):
        return self._by_id.get((block_key, message_id))

    def max_seq(self, block_key):
        msgs = self._by_block.get(block_key, [])
        return max((m.seq for m in msgs), default=0)

    def insert(self, message):
        self._by_block.setdefault(message.block_key, []).append(message)
        self._by_id[(message.block_key, message.message_id)] = message


class FailingStore(ConversationStore):
    """Simulates a store outage: every operation raises."""

    def get_messages(self, block_key):
        raise ConversationUnavailable("simulated outage on read")

    def find_by_id(self, block_key, message_id):
        raise ConversationUnavailable("simulated outage on lookup")

    def max_seq(self, block_key):
        raise ConversationUnavailable("simulated outage on max_seq")

    def insert(self, message):
        raise ConversationUnavailable("simulated outage on insert")


class UnverifiableStore(InMemoryStore):
    """Simulates a write that cannot be verified: insert drops the row,
    so the service's re-read finds nothing and must refuse success."""

    def insert(self, message):
        return None  # pretend to accept, persist nothing


class ConversationService:
    def __init__(self, store):
        self.store = store

    # ---- read side: open/list (creates nothing) ----

    def open_conversation(self, block_key, after_seq=None, limit=DEFAULT_LIMIT):
        self._validate_block_key(block_key)
        if limit is None:
            limit = DEFAULT_LIMIT
        if not isinstance(limit, int) or limit < 1 or limit > MAX_LIMIT:
            raise ValidationError("limit must be an integer in 1..500")
        if after_seq is not None and (
            not isinstance(after_seq, int) or after_seq < 0
        ):
            raise ValidationError("after_seq must be a non-negative integer")
        try:
            messages = self.store.get_messages(block_key)
        except ConversationUnavailable:
            raise
        except Exception as exc:  # any store failure is an outage, not data
            raise ConversationUnavailable(str(exc)) from exc
        ordered = sorted(messages, key=lambda m: m.seq)
        # count and participants are BLOCK-wide (unfiltered): the face uses
        # them to show "N messages" and to page further. Only the message
        # page itself is sliced by after_seq/limit.
        total = len(ordered)
        participants = []
        for m in ordered:
            if m.author_alias not in participants:
                participants.append(m.author_alias)
        if after_seq is not None:
            ordered = [m for m in ordered if m.seq > after_seq]
        page = ordered[:limit]
        return {
            "block_key": block_key,
            "messages": [m.to_dict() for m in page],
            "participants": participants,
            "count": total,
        }

    # ---- write side: guarded append ----

    def append_message(self, block_key, message_id, author_alias, body):
        self._validate_block_key(block_key)
        message_id = self._validate_message_id(message_id)
        self._validate_alias(author_alias)
        self._validate_body(body)
        try:
            existing = self.store.find_by_id(block_key, message_id)
        except ConversationUnavailable:
            raise
        except Exception as exc:
            raise ConversationUnavailable(str(exc)) from exc
        if existing is not None:
            # Retry of an already-stored send: return it, write nothing.
            return {"message": existing.to_dict(), "duplicate": True}
        try:
            seq = self.store.max_seq(block_key) + 1
        except ConversationUnavailable:
            raise
        except Exception as exc:
            raise ConversationUnavailable(str(exc)) from exc
        candidate = Message(
            message_id=message_id,
            block_key=block_key,
            seq=seq,
            author_alias=author_alias,
            body=body,
            created_at=_now_z(),
        )
        try:
            self.store.insert(candidate)
        except ConversationUnavailable:
            raise
        except Exception as exc:
            raise ConversationUnavailable(str(exc)) from exc
        # Verify by re-read: a write whose verification is unknown is not
        # a success, and is never reported as one.
        try:
            stored = self.store.find_by_id(block_key, message_id)
        except ConversationUnavailable:
            raise
        except Exception as exc:
            raise ConversationUnavailable(str(exc)) from exc
        if stored is None or stored != candidate:
            raise ConversationUnavailable(
                "verification failed: stored message did not read back"
            )
        return {"message": stored.to_dict(), "duplicate": False}

    # ---- validation helpers ----

    @staticmethod
    def _validate_block_key(block_key):
        if not isinstance(block_key, str) or not block_key.strip():
            raise ValidationError("block_key must be a non-empty string")

    @staticmethod
    def _validate_message_id(message_id):
        if not isinstance(message_id, str):
            raise ValidationError("message_id must be a UUID string")
        try:
            parsed = uuid.UUID(message_id)
        except (ValueError, AttributeError):
            raise ValidationError("message_id must be a valid UUID")
        return str(parsed)

    @staticmethod
    def _validate_alias(author_alias):
        if (
            not isinstance(author_alias, str)
            or not author_alias.strip()
            or len(author_alias) > MAX_ALIAS_CHARS
        ):
            raise ValidationError(
                "author_alias must be a non-empty string of at most 64 chars"
            )

    @staticmethod
    def _validate_body(body):
        if not isinstance(body, str) or not body.strip():
            raise ValidationError("body must be non-empty text")
        if len(body) > MAX_BODY_CHARS:
            raise ValidationError("body must be at most 8000 chars")
