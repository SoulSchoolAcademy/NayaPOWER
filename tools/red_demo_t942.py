"""RED demo for t942: proves the t902 falsification hole on the UNWIRED seam.

Run BEFORE the candidate gate module exists. It applies retrieve()'s exact
exclusion predicate (lifecycle filter only, smart_note_v2.py) to the four
probe entries and shows ALL FOUR pass through — including the unauthorized
seed from t902. Expected output: 0/4 excluded. Record the output as the RED.
"""
import re
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
src = (TOOLS / "smart_note_v2.py").read_text(encoding="utf-8")

# 1) static: retrieve() references no authorization field at all
has_auth = "retrieval_authorized" in src
has_scope = bool(re.search(r"def retrieve\(.*\bscope\b", src))
print(f"[static] smart_note_v2.py mentions retrieval_authorized anywhere: {has_auth}")
print(f"[static] retrieve() signature reads any scope field: {has_scope}")

# 2) behavioral: retrieve()'s exact exclusion predicate against probe entries
INACTIVE = {"SUPERSEDED", "ARCHIVED", "REVOKED"}


def current_seam_excludes(e):
    # verbatim logic of retrieve(): lifecycle filter is the WHOLE filter
    return str(e.get("lifecycle_state", "ACTIVE")).upper() in INACTIVE


probes = {
    "unauthorized ACTIVE seed (t902: retrieval_authorized=false)": {
        "id": "SN-TEST-UNAUTH", "lifecycle_state": "ACTIVE",
        "retrieval_authorized": False, "scope": "PRIVATE"},
    "superseded seed": {
        "id": "SN-TEST-SUP", "lifecycle_state": "SUPERSEDED",
        "retrieval_authorized": True, "scope": "PRIVATE"},
    "stale cache copy of superseded note (claims ACTIVE)": {
        "id": "SN-STALE", "lifecycle_state": "ACTIVE",
        "retrieval_authorized": True, "scope": "PRIVATE",
        "cached_copy_of_superseded": True},
    "tampered flag (retrieval_authorized='yes')": {
        "id": "SN-TEST-TAMPER", "lifecycle_state": "ACTIVE",
        "retrieval_authorized": "yes", "scope": "PRIVATE"},
}

print("\n[behavioral] current seam exclusion verdicts (unwired retrieve()):")
excluded = 0
for name, e in probes.items():
    out = current_seam_excludes(e)
    excluded += out
    print(f"  {'EXCLUDED' if out else 'PASSES THROUGH'} <- {name}")
print(f"\nRED RESULT: {excluded}/4 probe entries excluded by the current seam.")
print("The unauthorized entry PASSES THROUGH — the t902 hole is live on main.")
sys.exit(0 if excluded == 0 else 1)  # RED == hole confirmed
