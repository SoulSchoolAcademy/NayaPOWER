"""CANDIDATE — retrieval-side authorization gate for the retrieval seam.

Status: CANDIDATE, NOT WIRED, NOT RATIFIED.
Spec: BRAIN/00-SPEC/0007-RETRIEVAL-AUTHORIZATION-GATE-SPEC-V1.md (Lane 8, t912).
Closes: Lane 5 t902 falsification — unauthorized (retrieval_authorized=false)
lessons are surfaced today; retrieve() has no authorization mechanism.

DO NOT import this module from any production code path. Wiring it into
tools/smart_note_v2.py::retrieve() is an authority/privacy change and is
BLOCKED until Shawn (the Human Director) gives his word. This module exists
so the gate can be tested, probed adversarially, and reviewed BEFORE any
wiring decision.

Design (mirrors spec 0007 section 4):
  * Per-entry visibility verdict, evaluated BEFORE scoring (same placement as
    the lifecycle filter — exclusion by filter, not ranking, per t902 A2).
  * Visibility rule mirrors render()'s projection rule: public publication
    scopes are open; PRIVATE notes require an authenticated private surface.
  * retrieval_authorized is a STRICT tri-state with a defined writer contract:
    only the exact boolean True authorizes; only the exact boolean False
    denies. Anything else (missing, string, int, None) is UNKNOWN and fails
    closed. This resolves spec 0007's B7 (the phantom field) by DEFINING the
    field before any wire: a field with no writer is attacker-controlled, so
    the writer is defined HERE as part of the candidate.
  * Supersession chains are respected via the registry (source of truth):
    a stale cached copy claiming ACTIVE cannot resurrect a superseded note.
  * Verdicts are silent-exclusion codes (spec 4.3): reasons name a code, never
    note content, ids, or existence-sensitive detail.

Stdlib only. No I/O, no logging of withheld note ids.
"""

STATUS = "CANDIDATE — NOT WIRED — NOT RATIFIED"

# Mirrors retrieve()'s lifecycle filter (smart_note_v2.py) — the exclusion
# vocabulary the corpus already honors.
INACTIVE_LIFECYCLE = frozenset({"SUPERSEDED", "ARCHIVED", "REVOKED"})

# Spec 0007 section 4.2 — the publication-scope vocabulary render() uses.
PUBLIC_PUBLICATION_SCOPE = frozenset({"PUBLIC", "COLLECTIVE", "PUBLIC_DERIVED_VIEW"})

# Example of a bound private-surface caller context (spec 4.1 / 4.4.2).
# A bare dict is a CLAIM, not proof — runtime binding is a wiring-time
# requirement, not something this candidate can provide.
PRIVATE_CALLER = {"surface": "private_authenticated", "identity": "<named party>"}

_AUTHORIZED = "AUTHORIZED"
_DENIED = "DENIED"
_UNKNOWN = "UNKNOWN"

_MISSING = object()


def _entry_key(entry):
    """Best-effort registry key for an entry; None when unidentifiable."""
    if not isinstance(entry, dict):
        return None
    for field in ("id", "note_id", "smart_link"):
        value = entry.get(field)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def authorization_state(entry):
    """Strict tri-state for the retrieval_authorized field.

    Only the exact boolean True authorizes; only the exact boolean False
    denies. Everything else — missing, None, "yes", 1, "true" — is UNKNOWN.
    The writer contract is defined here (spec 0007 B7): fields with no writer
    are attacker-controlled defaults, so truthy-but-not-True values are
    NEVER treated as authorization.
    """
    if not isinstance(entry, dict):
        return _UNKNOWN
    value = entry.get("retrieval_authorized", _MISSING)
    if value is True:
        return _AUTHORIZED
    if value is False:
        return _DENIED
    return _UNKNOWN


def supersession_head(entry, registry_index):
    """Resolve a superseded_by chain to its head entry.

    Returns the head entry dict, or None when the chain is dangling or
    cyclic (fail closed — never guess which member is current).
    """
    if not isinstance(entry, dict) or not isinstance(registry_index, dict):
        return None
    seen = set()
    current = entry
    current_key = _entry_key(current)
    while True:
        target_key = current.get("superseded_by")
        if not target_key or not isinstance(target_key, str):
            return current  # no pointer: current IS the head candidate
        target_key = target_key.strip()
        if not target_key:
            return current
        if current_key is not None:
            if current_key in seen:
                return None  # cycle
            seen.add(current_key)
        target = registry_index.get(target_key)
        if not isinstance(target, dict):
            return None  # dangling pointer: fail closed
        current = target
        current_key = _entry_key(current)
        if current_key is not None and current_key in seen:
            return None  # cycle through the target


def _private_surface(caller):
    """True only for an explicit authenticated private surface claim."""
    if not isinstance(caller, dict):
        return False
    if caller.get("surface") != "private_authenticated":
        return False
    identity = caller.get("identity")
    return isinstance(identity, str) and identity.strip() != ""


def _resolve_record(entry, registry_index):
    """Pick the authoritative record: the registry's copy when a registry
    is provided and the entry is found there (stale-cache protection);
    otherwise the caller's own copy. Returns (record, from_registry)."""
    if registry_index is None or not isinstance(registry_index, dict):
        return entry, False
    key = _entry_key(entry)
    found = registry_index.get(key) if key else None
    if isinstance(found, dict):
        return found, True
    return entry, False


def retrieval_visible(entry, caller=None, registry_index=None):
    """Composite visibility verdict for one registry entry.

    Returns (visible: bool, reason: str). Malformed input fails closed and
    never raises. Reasons are silent-exclusion codes (spec 4.3) — they name
    a code, never note content or ids.

    Order: lifecycle -> supersession (registry as truth) -> authorization
    tri-state -> scope rule. An explicit denial overrides even a PUBLIC
    publication scope.
    """
    if not isinstance(entry, dict):
        return False, "FAIL_CLOSED:malformed-entry"

    record, _from_registry = _resolve_record(entry, registry_index)

    # 1. Lifecycle filter (mirrors retrieve()'s existing filter exactly).
    lifecycle = str(record.get("lifecycle_state", "ACTIVE")).upper()
    if lifecycle in INACTIVE_LIFECYCLE:
        return False, "EXCLUDED:lifecycle-%s" % lifecycle.lower()

    # 2. Supersession chain (registry is the source of truth).
    if record.get("superseded_by"):
        if registry_index is None or not isinstance(registry_index, dict):
            # No registry to resolve against: a supersession pointer that
            # cannot be resolved is not current — fail closed.
            return False, "FAIL_CLOSED:unresolvable-supersession"
        key = _entry_key(record)
        head = supersession_head(record, registry_index)
        if head is None:
            return False, "FAIL_CLOSED:supersession-unresolvable"
        if _entry_key(head) != key:
            return False, "EXCLUDED:superseded-chain"
        # else: this entry IS the head — continue to authorization
    elif registry_index is not None and isinstance(registry_index, dict):
        # Entry carries no pointer but a registry was provided: an entry
        # that cannot be found there at all, while carrying a supersession
        # pointer, was handled above. An entry simply absent from the
        # registry is evaluated on its own fields (corpus-filter usage);
        # the fail-closed unknown-provenance case is the dangling pointer.
        pass

    # 3. Authorization tri-state (strict; unknown fails closed).
    auth = authorization_state(record)
    if auth == _DENIED:
        return False, "EXCLUDED:retrieval-authorized-false"
    if auth != _AUTHORIZED:
        return False, "FAIL_CLOSED:unknown-authorization-state"

    # 4. Scope rule (spec 4.2 — mirrors render()'s projection rule).
    # Private by default: missing scope == PRIVATE.
    publication_scope = str(record.get("publication_scope") or "").upper()
    if publication_scope in PUBLIC_PUBLICATION_SCOPE:
        return True, "VISIBLE:publication-scope"
    if _private_surface(caller):
        return True, "VISIBLE:private-surface"
    return False, "EXCLUDED:private-scope-requires-authenticated-surface"


def filter_corpus(entries, caller=None, registry_index=None):
    """Return the visible subset of a corpus, in original order.

    Silent exclusion: nothing is logged about withheld entries.
    """
    if not isinstance(entries, (list, tuple)):
        return []
    return [e for e in entries
            if retrieval_visible(e, caller=caller, registry_index=registry_index)[0]]
