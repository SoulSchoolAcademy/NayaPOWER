"""CANDIDATE — refusal-point contract for the retrieval-authorization gate.

Status: CANDIDATE, NOT WIRED, NOT RATIFIED.
Spec: BRAIN/00-SPEC/0007-RETRIEVAL-AUTHORIZATION-GATE-SPEC-V1.md (Lane 8, t912).
Gate module: tools/retrieval_authorization_gate.py (Lane 5, t942; candidate
    ACCEPTED by Lane 1's independent four-way experiment, t952).
Packet: docs/retrieval-auth-wire-packet-t0537.md — AWAITING-SHAWN (Lane 9, t0537).

This module is the on-disk counterpart to the enforcement verdict Lane 9
named missing at t0531 ("a score and no mouth"): the refusal point where an
authorization verdict becomes a MECHANICAL refusal. It is a contract plus a
reference guard, not a wiring — no production code imports it. Installing
these guards at the hook locations below is a protected human gate:
Shawn's word only.

THE CONTRACT
------------
WRITE PATH — the disposition/index commit point: any code path that makes a
note entry retrievable by, or projectable to, a surface beyond its
authorization. Live instances on main tip dbe06f9e733 (all in
tools/smart_note_v2.py):
    W1  _update_registry_locked (line 545) — the registry index write. An
        entry committed here becomes visible to retrieve()'s corpus filter.
    W2  render (line 454) — the projection commit. A PUBLIC projection of a
        PRIVATE-scope note is exactly the write the ACTIVE_AUTH_GATED label
        names (spec 0007, section 3.2).

EXIT PROTOCOL — refusal is a raised RefusalError. The guarded commit is NEVER
invoked on refusal: nothing is written, nothing is leaked (refusal codes are
silent-exclusion codes naming a reason code — never note content, ids, or
existence-sensitive detail, per spec 0007 section 4.3). The __main__ harness
exits 2 on refusal and 0 on permit: exit non-zero blocks the disposition
close (the FP-003 falsifier-suite rule — a disposition cannot close over a
refused write).

HOOK LOCATION — where the wiring installs the guard (on Shawn's word):
    H1  read side: retrieve (line 810), at the lifecycle filter (line ~753):
        guard_disclose wraps the per-entry visibility verdict before scoring.
        Default caller None = unauthenticated public = most restrictive.
    H2  write side: _update_registry_locked (line 545), before the entry is
        appended to registry["entries"]: guard_write.
    H3  projection side: render (line 454), before a PRIVATE-scope note is
        committed to a public projection path: guard_write.

Stdlib only. No I/O except __main__.
"""

from retrieval_authorization_gate import retrieval_visible, PRIVATE_CALLER

STATUS = "CANDIDATE — NOT WIRED — NOT RATIFIED"

# __main__ exit codes: the exit protocol in one number.
EXIT_PERMITTED = 0
EXIT_REFUSED = 2
EXIT_MALFORMED_INPUT = 3


class RefusalError(Exception):
    """Raised when the refusal predicate fires.

    Carries the silent-exclusion code (never note content or ids).
    """

    def __init__(self, code):
        super().__init__("REFUSED: %s" % code)
        self.code = code


def refusal_predicate(entry, caller=None, registry_index=None):
    """The refusal predicate: does this write/disclosure get refused?

    Returns (refused: bool, code: str). VISIBLE verdicts from the candidate
    gate map to (False, "PERMITTED:..."); every other verdict maps to
    (True, <silent-exclusion code>). Malformed input fails closed and never
    raises — refusal is a decision, not an exception path.
    """
    try:
        visible, reason = retrieval_visible(
            entry, caller=caller, registry_index=registry_index
        )
    except Exception:
        # The gate contract says it never raises, but a refusal point must
        # not depend on that promise: an exploding predicate refuses.
        return True, "FAIL_CLOSED:predicate-error"
    if visible:
        return False, "PERMITTED:" + str(reason)
    return True, str(reason)


def guard_write(commit, entry, caller=None, registry_index=None):
    """Guard the WRITE path: commit() runs only if the predicate permits.

    commit is a zero-arg callable performing the actual write (wiring-time
    callers pass a closure). On refusal: raise RefusalError, commit is NEVER
    invoked, nothing is written. On permit: return commit()'s result.
    """
    refused, code = refusal_predicate(
        entry, caller=caller, registry_index=registry_index
    )
    if refused:
        raise RefusalError(code)
    return commit()


def guard_disclose(read, entry, caller=None, registry_index=None):
    """Guard the READ (disclosure) path: read() runs only if permitted.

    read is a zero-arg callable performing the actual content fetch (the
    winner's explanation read in retrieve()). On refusal: raise RefusalError,
    read is NEVER invoked, no content is touched. On permit: return read().
    """
    refused, code = refusal_predicate(
        entry, caller=caller, registry_index=registry_index
    )
    if refused:
        raise RefusalError(code)
    return read()


def main(argv):
    """CLI harness: attempt a guarded null-write from a JSON packet.

    Packet: {"entry": {...}, "caller": {...}|null, "registry": {...}|null,
             "action": "write"|"disclose"}.
    Exit 0 = permitted (null-write ran). Exit 2 = refused (nothing ran).
    Exit 3 = malformed packet. The non-zero exit is the disposition-blocker:
    a disposition cannot close over a refused write.
    """
    import json
    import sys

    if len(argv) != 2:
        print("usage: refusal_point_t0537.py <packet.json>", file=sys.stderr)
        return EXIT_MALFORMED_INPUT
    try:
        with open(argv[1], "r", encoding="utf-8") as f:
            packet = json.load(f)
        entry = packet["entry"]
        action = packet.get("action", "write")
    except Exception as exc:
        print("MALFORMED PACKET: %s" % exc, file=sys.stderr)
        return EXIT_MALFORMED_INPUT
    caller = packet.get("caller")
    registry = packet.get("registry")
    ran = []

    def null_sink():
        ran.append(True)
        return "written"

    guard = guard_write if action == "write" else guard_disclose
    refused, code = refusal_predicate(entry, caller=caller, registry_index=registry)
    if refused:
        print("REFUSED %s" % code)
        return EXIT_REFUSED
    # Predicate and guard must agree: run the guard to prove the sink path.
    result = guard(null_sink, entry, caller=caller, registry_index=registry)
    print("PERMITTED %s (sink: %s)" % (code, result))
    return EXIT_PERMITTED


if __name__ == "__main__":
    import sys

    sys.exit(main(sys.argv))
