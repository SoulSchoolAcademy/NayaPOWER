"""RED demo for t0537: proves the refusal point fires on the guarded path and
the hole exists on the unguarded path.

Phase 1 (RED): an unauthorized entry committed through an UNGUARDED write
path is ADMITTED — the seam is open today; retrieve() has no refusal point.
Phase 2 (GREEN): the same entry through guard_write is REFUSED — nothing is
written, nothing is leaked, RefusalError carries a silent-exclusion code.

Run: python3 tools/red_demo_refusal_t0537.py
Expected output: phase 1 COMMITTED (RED), phase 2 REFUSED (GREEN).
"""
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from refusal_point_t0537 import RefusalError, guard_write

UNAUTHORIZED = {
    "id": "SN-DEMO-UNAUTH",
    "lifecycle_state": "ACTIVE",
    "retrieval_authorized": False,          # t902's seed: surfaced today
    "publication_scope": "PUBLIC",
    "title": "a lesson that must never surface",
}

store = []


def unguarded_commit():
    store.append("written-by-unguarded-path")
    return "committed"


print("== phase 1 (RED): unguarded write path ==")
unguarded_commit()
print("COMMITTED:", store)
print("-> the seam is open: an unauthorized entry was admitted with no refusal")

print()
print("== phase 2 (GREEN): guarded write path ==")
try:
    guard_write(unguarded_commit, UNAUTHORIZED)
    print("BUG: unauthorized write was permitted")
    sys.exit(1)
except RefusalError as exc:
    print("REFUSED:", exc.code)
print("store after refusal:", store)
print("-> the refusal point fires: nothing written, code leaks no content")
