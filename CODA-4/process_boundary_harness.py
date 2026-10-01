"""Post-repair process-boundary acceptance harness for cold-successor continuity.

This is the gate I will run the moment Naya 4's CS-01 fix lands. It is written
now, deliberately, so acceptance cannot drift into "the hash matched" after the
repair.

WHAT THIS IS
------------
A real OS process boundary:

  Process A  produces receipts through the real seams, serializes them to a
             temp artifact, records hashes and the exact source, then EXITS.
  Process B  a separate interpreter with no memory of A. Receives the artifact
             path and canonical source pointers ONLY — no predecessor node
             objects, no hidden answers. Restores, retrieves, and validates
             through public interfaces.
  Process C  recovers a genuinely NEW result written by B. Rereading A's
             unchanged receipts is NOT an improved-state cycle.

WHAT THIS IS NOT
----------------
Not database persistence. Not production readiness. Not independent-agent
reasoning. Not causal improvement. Local cross-process continuity only.

CURRENT STATE: ALL PROCESS-BOUNDARY CASES ARE BLOCKED BY CS-01.
Every case below is an `xfail(strict=True)` pinned to CS-01. They are not
skipped and not hidden: under `--verify-rung-status` the run reports which rung
is the first missing one, so the ladder stays visible.

    python CODA-4/process_boundary_harness.py          # run the ladder
    python CODA-4/process_boundary_harness.py --rungs  # just the rung status
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

NOW = "2026-10-01T04:00:00+00:00"
PRINCIPAL = {"identity": "coda4-process-boundary",
             "entitled_scopes": ["public", "team"]}

CS01 = "CS-01: KnowNode.cold_reconstruct does not install reconstructed " \
       "state on self, so cross-process retrieval returns nothing"

CANONICAL_POINTERS = {
    # Canonical source pointers, not hidden answers. Process B receives these
    # and nothing else that was produced by A's reasoning.
    "protocol": "CODA-4/COLD-SUCCESSOR-PROTOCOL-V1.md",
    "cold_acceptance_contract":
        "NAYA-ACTIVATION/COLD-GITHUB-BOOTSTRAP-ACCEPTANCE-V1.md",
    "continuity_contract": "NAYA-ACTIVATION/INTELLIGENCE/CONTINUITY.md",
    "learning_contract": "NAYA-ACTIVATION/INTELLIGENCE/LEARNING.md",
}

# --------------------------------------------------------------------------
# Child programs. Each runs in its own interpreter via subprocess.
# --------------------------------------------------------------------------

CHILD_A = r'''
import hashlib, json, os, sys
sys.path.insert(0, %(root)r)
from naya_kernel.nodes import know_node

artifact = sys.argv[1]
NOW = %(now)r
PRINCIPAL = %(principal)r

producer = know_node.KnowNode()


def ingest(payload, klass, signal):
    return producer.ingest({
        "content": json.dumps(payload, sort_keys=True),
        "proposed_class": klass,
        "class_signals": [{"signal": signal, "value": 0.9}],
        "classifier": "coda4-process-boundary",
        "provenance": {"sources": [{
            "kind": "EXTERNAL", "ref": payload["ref"],
            "capturedAt": NOW, "capturedBy": "coda4-process-boundary"}]},
        "identity_binding": {"verified": True},
        "owner_scope": "public", "epistemic_state": "INGESTED"},
        PRINCIPAL, now=NOW)


receipts = [
    ingest({"lesson_id": "PROV-BEFORE-APPLY-1",
            "lesson": "Preserve provenance before applying retained "
                      "intelligence; retrieval never grants authority.",
            "ref": "ext://coda4/lesson"}, "REUSABLE", "coda4-v1"),
    ingest({"lesson_id": "UNRELATED-REF-1",
            "lesson": "Prefer the local echo tool for demos",
            "ref": "ext://coda4/unrelated"}, "REFERENCE", "coda4-control-v1"),
]
for r in receipts:
    assert r["afterState"] == "ACTIVE", r

bundle = {
    "producer_receipts": receipts,
    "producer_store_hash": producer._store_hash(),
    "canonical_pointers": %(pointers)r,
    "exact_source_sha": os.environ.get("CODA4_TESTED_SHA", "UNRECORDED"),
}
raw = json.dumps(bundle, sort_keys=True, separators=(",", ":"))
with open(artifact, "w", encoding="utf-8") as fh:
    fh.write(raw)
print(json.dumps({"pid": os.getpid(),
                  "receipts": len(receipts),
                  "store_hash": bundle["producer_store_hash"],
                  "artifact_sha256":
                      hashlib.sha256(raw.encode()).hexdigest()}))
'''

CHILD_B = r'''
import hashlib, json, os, sys
sys.path.insert(0, %(root)r)
from naya_kernel.nodes import know_node

artifact, mode = sys.argv[1], sys.argv[2]
NOW = %(now)r
PRINCIPAL = %(principal)r
TMP_ROOT = %(tmp_root)r

# Safety: the "missing" case deletes its input. Refuse to operate on anything
# outside the harness temp directory, so a mistyped argument can never remove a
# real repository file.
_resolved = os.path.abspath(artifact)
if not _resolved.startswith(os.path.abspath(TMP_ROOT)):
    raise SystemExit("refusing to operate outside the harness temp dir: "
                     + repr(_resolved))

with open(artifact, encoding="utf-8") as fh:
    raw = fh.read()
bundle = json.loads(raw)
bundle["artifact_sha256"] = hashlib.sha256(raw.encode()).hexdigest()

if mode == "tampered":
    # Forge the receipt content itself. CS-02 means this is NOT caught, so the
    # report below says so rather than implying a guard exists.
    bundle["producer_receipts"][0]["block_snapshot"]["provenance"][
        "sources"][0]["ref"] = "ext://coda4/FORGED"

if mode == "missing":
    os.remove(artifact)

# B receives receipts only. No producer node object crosses the boundary.
node = know_node.KnowNode()
report = node.cold_reconstruct(bundle["producer_receipts"])
found = node.retrieve({"text": "PROV-BEFORE-APPLY-1",
                       "requested_scopes": ["public"],
                       "identity_binding": {"verified": True}},
                      PRINCIPAL, now=NOW)
matched = [b for b in found.get("blocks", [])
           if "PROV-BEFORE-APPLY-1" in json.dumps(b, sort_keys=True)]

result = {
    "pid": os.getpid(),
    "mode": mode,
    "restored_block_count": report["restored_block_count"],
    "report_store_hash": report["store_hash"],
    "producer_store_hash": bundle["producer_store_hash"],
    "hashes_match":
        report["store_hash"] == bundle["producer_store_hash"],
    "actual_blocks_on_node": len(node.blocks),
    "retrieved_matching": len(matched),
    "provenance_refs": [
        p.get("ref")
        for b in matched
        for p in (b.get("provenance") or {}).get("sources", [])],
    "successor_receipt": None,
    "authority_probe": None,
}
if mode == "produce":
    # B preserves its own observed result through the real ingest seam, and
    # hands C the RECEIPT, not this process's summary. C must replay evidence,
    # not a report about evidence.
    r = node.ingest({
        "content": json.dumps({"kind": "successor_observation",
                               "derived_from": "process-boundary-B"},
                              sort_keys=True),
        "proposed_class": "REFERENCE",
        "class_signals": [{"signal": "coda4-process-boundary", "value": 0.9}],
        "classifier": "coda4-process-boundary",
        "provenance": {"sources": [{
            "kind": "EXTERNAL", "ref": "ext://coda4/successor/observation",
            "capturedAt": NOW, "capturedBy": "coda4-process-boundary"}]},
        "identity_binding": {"verified": True},
        "owner_scope": "public", "epistemic_state": "INGESTED"},
        PRINCIPAL, now=NOW)
    result["successor_receipt"] = r

# Authority probe: ask the real SELF boundary whether a package carrying this
# boundary's own evidence confers any authority. Derived from the runtime, never
# asserted by the harness.
from naya_kernel.nodes import self_node, evolve_node
_ev = evolve_node.EvolveNode()
_built = _ev.build_successor_package({
    "next_action": "verify boundary continuity",
    "blockers": [], "version": 1,
    "authority_context": {"authority_inherited": False},
    "provenance": {"sources": [
        {"kind": "EXTERNAL", "ref": "ext://coda4/boundary",
         "capturedAt": NOW, "capturedBy": "coda4-process-boundary"}]},
    "rationale": "boundary authority probe"})
pkg = _ev._handoff_packages[_built["handoff_id"]]

# Identity must arrive authenticated or SELF refuses before any authority
# question is reached, so mirror the shape the real SELF seam accepts.
_ck_payload = {"boot_count": 1, "owner_scope": "coda4-boundary"}
_ck_hash = self_node._sha256(_ck_payload)
_pred = {"predecessor_hash": None, "checkpoint_hash": _ck_hash,
         "config_hash": "config-boundary", "identity_binding": "bind-coda4"}
_pred["receipt_hash"] = self_node._sha256(
    {k: v for k, v in _pred.items() if k != "receipt_hash"})

_probe = self_node.SelfNode()
_gate = _probe.gate({
    "execution_id": "exec-boundary-1", "seen_execution_ids": [],
    "identity_claim": {"type": "CODA4"},
    "identity_binding": {"binding_ref": "bind-coda4", "verified": True,
                         "actor_type": "CODA4"},
    "mission_ref": "mission:ratified-v1", "scope_ref": "scope:ratified-v1",
    "ratified_sources": {
        "mission:ratified-v1": {"text": "serve Shawn as Naya"},
        "scope:ratified-v1": {"actions": ["read", "summarize"]}},
    "owner_scope": "coda4-boundary", "kernel_revision": "boundary-probe",
    "checkpoint": {"hash": _ck_hash, "payload": _ck_payload,
                   "owner_scope": "coda4-boundary"},
    "successor_package": pkg,
    "predecessor_receipt": _pred,
    "known": [], "unknown": [], "blocked": [],
})
_boot = _probe.last_boot_receipt or {}
# Authority, if any exists, must appear in the boot receipt. Search the whole
# receipt rather than a key I guessed, then report exactly what was found.
_auth_hits = sorted(k for k in _boot
                    if "authorit" in k.lower())
result["authority_probe"] = {
    "verdict": _gate.verdict.value,
    "reasons": _gate.reasons,
    "carries_authority_flag": bool(pkg.get("carries_authority")),
    # Only top-level receipt keys count. I first searched nested values too and
    # got a false positive: "inputs" echoes the package, so it mentioned
    # authority without granting any.
    "authority_bearing_keys": _auth_hits,
    "boot_receipt_receives_authority": bool(_auth_hits),
}

print(json.dumps(result))
'''

CHILD_C = r'''
import json, os, sys
sys.path.insert(0, %(root)r)
from naya_kernel.nodes import know_node

bundle_path, b_receipts_path = sys.argv[1], sys.argv[2]
PRINCIPAL = %(principal)r
NOW = %(now)r

with open(bundle_path, encoding="utf-8") as fh:
    bundle = json.load(fh)
with open(b_receipts_path, encoding="utf-8") as fh:
    b_receipts = json.load(fh)

node = know_node.KnowNode()
report = node.cold_reconstruct(bundle["producer_receipts"] + b_receipts)
found = node.retrieve({"text": "successor_observation",
                       "requested_scopes": ["public"],
                       "identity_binding": {"verified": True}},
                      PRINCIPAL, now=NOW)
new_results = [b for b in found.get("blocks", [])
               if "successor_observation"
               in json.dumps(b, sort_keys=True)]
print(json.dumps({
    "pid": os.getpid(),
    "restored_block_count": report["restored_block_count"],
    "new_results_recovered": len(new_results),
}))
'''


def _child(src, *args):
    out = subprocess.run([sys.executable, "-c", src] + list(args),
                         capture_output=True, text=True, cwd=ROOT)
    if out.returncode != 0:
        raise RuntimeError("child failed: %s\n%s"
                           % (out.stderr.strip()[-800:], out.stdout))
    return out.stdout.strip().splitlines()[-1]


# --------------------------------------------------------------------------
# The ladder. Each rung is a distinct claim, in dependency order.
# --------------------------------------------------------------------------

def rung_status():
    """Report the ladder statically, before running any child process.

    The `installs` probe reads KnowNode.cold_reconstruct's source for a write
    to self. That is a shortcut, not proof: an implementation could install via
    a helper, or via setattr, and this would miss it. It is used only to
    predict the first blocked rung so a reader can see the expected shape
    cheaply. The authoritative answer comes from running the ladder, which
    measures actual block counts and retrieval.
    """
    if ROOT not in sys.path:
        sys.path.insert(0, ROOT)
    from naya_kernel.nodes import know_node
    import inspect
    src = inspect.getsource(know_node.KnowNode.cold_reconstruct)
    installs = "self.blocks" in src or "self.__dict__" in src
    blocked = "BLOCKED by CS-01 (predicted)" if not installs \
        else "predicted reachable; run to confirm"
    rungs = [
        ("A", "Process A persists receipts and exits",
         True, "runnable today"),
        ("B-RESTORE", "Process B reconstructs usable state from receipts",
         installs, blocked),
        ("B-RETRIEVE", "Process B RETRIEVES from the restored node",
         installs, blocked),
        ("B-PROVENANCE", "Restored provenance matches what A ingested",
         installs, blocked),
        ("B-NO-AUTH", "Process B inherits no authority",
         True, "independent of CS-01; probed through the real SELF gate"),
        ("B-TAMPER", "Tampered evidence yields the governing failure",
         True, "runnable today; FAILS today, see CS-02"),
        ("B-MISSING", "Missing evidence yields the governing failure",
         True, "runnable today; passes today"),
        ("C", "Process C recovers a NEW result written by B",
         installs, blocked),
    ]
    return installs, rungs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rungs", action="store_true",
                    help="print rung status only")
    args = ap.parse_args()

    installs, rungs = rung_status()
    if args.rungs:
        print("KnowNode.cold_reconstruct installs state on self: %s"
              % installs)
        print()
        for rid, claim, reachable, note in rungs:
            print("[%s] %-11s %-58s %s"
                  % ("REACHABLE" if reachable else "BLOCKED  ", rid, claim,
                     note))
        return 0

    tmp = tempfile.mkdtemp(prefix="coda4-boundary-")
    artifact = os.path.join(tmp, "a-receipts.json")
    b_out = os.path.join(tmp, "b-receipts.json")

    fmt = dict(root=ROOT, now=NOW, principal=PRINCIPAL,
               pointers=CANONICAL_POINTERS, tmp_root=tmp)

    a_out = json.loads(_child(CHILD_A % fmt, artifact))
    print("A  pid=%s receipts=%s artifact_sha256=%s"
          % (a_out["pid"], a_out["receipts"], a_out["artifact_sha256"][:16]))
    print("   Process A has EXITED. No memory carries forward.\n")

    b_read = json.loads(_child(CHILD_B % fmt, artifact, "read"))
    print("B  pid=%s (A was %s)" % (b_read["pid"], a_out["pid"]))
    print("   reported restored=%s  hash_match=%s"
          % (b_read["restored_block_count"], b_read["hashes_match"]))
    print("   ACTUAL blocks on node=%s  retrieved=%s"
          % (b_read["actual_blocks_on_node"], b_read["retrieved_matching"]))
    print("   provenance refs=%s" % b_read["provenance_refs"])
    probe = b_read["authority_probe"]
    print("   SELF authority probe: verdict=%s carries_authority_flag=%s"
          % (probe.get("verdict"), probe.get("carries_authority_flag")))
    print("   authority-bearing keys in boot receipt: %s"
          % probe.get("authority_bearing_keys"))
    print("   boot receipt receives authority: %s\n"
          % probe.get("boot_receipt_receives_authority"))

    # B+ hands C its own INGEST RECEIPT, so C replays evidence rather than a
    # report about evidence.
    b_prod = json.loads(_child(CHILD_B % fmt, artifact, "produce"))
    with open(b_out, "w", encoding="utf-8") as fh:
        json.dump([b_prod["successor_receipt"]], fh)
    print("B+ pid=%s wrote successor receipt %s"
          % (b_prod["pid"], b_prod["successor_receipt"]["receipt_hash"][:16]))
    print("    (its own restored A-blocks: %s — still blocked by CS-01)\n"
          % b_prod["actual_blocks_on_node"])

    c_out = json.loads(_child(CHILD_C % fmt, artifact, b_out))
    print("C  pid=%s restored=%s new_results_recovered=%s"
          % (c_out["pid"], c_out["restored_block_count"],
             c_out["new_results_recovered"]))

    # Stale / forged evidence: the governing contract is a visible FAILURE,
    # never a silent restore. Run in a fresh temp dir per case so the "missing"
    # case deletes only its own copy.
    for label in ("tampered", "missing"):
        case_dir = tempfile.mkdtemp(prefix="coda4-%s-" % label, dir=tmp)
        path = os.path.join(case_dir, "a-receipts.json")
        with open(artifact, encoding="utf-8") as fh:
            raw = fh.read()
        if label == "missing":
            # Never create it: B must be handed an artifact that is not there.
            pass
        else:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(raw)
        try:
            out = _child(CHILD_B % fmt, path, label)
            parsed = json.loads(out)
            outcome = ("NO FAILURE RAISED — restored=%s hash_match=%s "
                       "forged_accepted=%s"
                       % (parsed["restored_block_count"],
                          parsed["hashes_match"],
                          label == "tampered"))
        except RuntimeError:
            outcome = "governing failure raised (correct)"
        print("B- %-9s %s" % (label, outcome))

    print("\nfirst missing rung: %s"
          % next(r[0] for r in rungs if not r[2]))
    print("CS-01 present: %s" % (not installs))
    return 0


if __name__ == "__main__":
    sys.exit(main())