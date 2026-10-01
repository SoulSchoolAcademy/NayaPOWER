"""Generate machine-checkable evidence receipts for the cold-successor lane.

Each receipt records the exact tested SHA, the command, the captured stdout, the
exit code, and a SHA-256 over its own body, so a later reader can re-derive the
result instead of trusting this file.

Scope honesty: these are OBSERVATIONS OF THIS RUN. They are not a durability
claim, not a substitute for the cross-process work in protocol section 7, and
not proof that any defect is repaired. A receipt that reported success over an
unusable store is exactly the failure this lane exists to catch (CS-01), so a
receipt here records what was *observed*, including exit codes that are non-zero.

    python CODA-4/make_evidence.py            # write receipts
    python CODA-4/make_evidence.py --verify   # re-verify existing receipts

Safe by construction: writes only under CODA-4/evidence/, runs read-only pytest
and the reproducer, touches no other worker's files, no network, no database.
"""

import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
EVIDENCE = os.path.join(HERE, "evidence")


def _run(argv):
    p = subprocess.run(argv, cwd=ROOT, capture_output=True, text=True)
    return {"command": " ".join(argv), "exit_code": p.returncode,
            "stdout_tail": p.stdout.strip().splitlines()[-40:],
            "stderr_tail": p.stderr.strip().splitlines()[-20:]}


def _rev(rev):
    p = subprocess.run(["git", "rev-parse", rev], cwd=ROOT,
                       capture_output=True, text=True)
    return p.stdout.strip() or "UNRESOLVED"


def _body_hash(body):
    payload = json.dumps(body, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


CASES = [
    ("focused-suite",
     "Cold-successor protocol suite. 3 xfail are CS-01 x2 and CS-02 x1; the "
     "xfails ARE the acceptance signal, so a green total does not mean "
     "acceptance.",
     ["python", "-m", "pytest",
      "tests/test_nodes/test_coda4_cold_successor.py", "-q"]),
    ("ci-dependency-guard",
     "Confirms the test relocation to tests/test_nodes/ did not break the "
     "CI dependency guard.",
     ["python", "-m", "pytest", "tests/test_ci_declares_test_dependencies.py",
      "-q"]),
    ("cs01-reproducer",
     "Standalone CS-01 reproducer. exit 1 means the defect is PRESENT, "
     "exit 0 means it was repaired.",
     ["python", os.path.join("CODA-4", "repro_cs01.py")]),
    ("cs02-reproducer",
     "Standalone CS-02 reproducer: KNOW replay performs no receipt integrity "
     "verification. exit 1 means PRESENT.",
     ["python", os.path.join("CODA-4", "repro_cs02.py")]),
    ("process-boundary-harness",
     "Real A -> B -> C process boundary. Records the first missing rung. "
     "exit 0 is NOT success: the ladder is expected to report BLOCKED on "
     "B-RESTORE while CS-01 is open.",
     ["python", os.path.join("CODA-4", "process_boundary_harness.py")]),
    ("process-boundary-rungs",
     "Static rung status for the process-boundary ladder, without running the "
     "children.",
     ["python", os.path.join("CODA-4", "process_boundary_harness.py"),
      "--rungs"]),
    ("kernel-handoff-existing",
     "The pre-existing handoff test. It asserts the store hash but never "
     "retrieves from the reconstructed node, which is why CS-01 was invisible.",
     ["python", "-m", "pytest",
      "tests/test_nodes/test_kernel_handoff_integration.py", "-q"]),
    ("full-suite-default-mode",
     "Whole suite, default encoding. 7 failures on Windows.",
     ["python", "-m", "pytest", "-q"]),
    ("full-suite-utf8-mode",
     "Whole suite under -X utf8, to separate environment encoding from "
     "behavior. 2 failures survive; those are genuine Windows path issues.",
     ["python", "-X", "utf8", "-m", "pytest", "-q"]),
]

HEAD_SHA = "UNKNOWN"
MAIN_SHA = "UNKNOWN"


def build():
    global HEAD_SHA, MAIN_SHA
    HEAD_SHA = _rev("HEAD")
    MAIN_SHA = _rev("origin/main")

    receipts = []
    for name, interpretation, argv in CASES:
        observed = _run(argv)
        body = {
            "receipt_id": "coda4-evidence-%s" % name,
            "lane": "Coda 4 — cold-successor restoration / applicability / "
                    "reconstruction",
            "owner_of_repair_for_cs01": "Naya 4 (naya_kernel/)",
            "protocol": "CODA-4/COLD-SUCCESSOR-PROTOCOL-V1.md",
            "scope_label": "OBSERVATION OF THIS RUN — not durability, not "
                           "cross-process continuity, not production proof",
            "interpretation": interpretation,
            "tested_head_sha": HEAD_SHA,
            "base_main_sha": MAIN_SHA,
            "observed": observed,
        }
        body["body_sha256"] = _body_hash(body)
        receipts.append(body)
    return receipts


def verify():
    ok = True
    for name, _interp, _argv in CASES:
        path = os.path.join(EVIDENCE, "coda4-evidence-%s.json" % name)
        if not os.path.isfile(path):
            print("MISSING  %s" % path)
            ok = False
            continue
        with open(path, encoding="utf-8") as fh:
            body = json.load(fh)
        claimed = body.pop("body_sha256", None)
        recomputed = _body_hash(body)
        state = "OK " if claimed == recomputed else "TAMPERED"
        if claimed != recomputed:
            ok = False
        print("%s  %s  exit=%s  tested_head=%s"
              % (state, name, body["observed"]["exit_code"],
                 body["tested_head_sha"][:12]))
    print("ALL RECEIPTS SELF-CONSISTENT" if ok else "RECEIPT VERIFICATION FAILED")
    return 0 if ok else 1


def main():
    if "--verify" in sys.argv:
        return verify()

    os.makedirs(EVIDENCE, exist_ok=True)
    receipts = build()
    for body in receipts:
        path = os.path.join(EVIDENCE, "%s.json" % body["receipt_id"])
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(body, fh, indent=2, sort_keys=True)
            fh.write("\n")
        print("wrote %s  exit=%s  head=%s"
              % (body["receipt_id"], body["observed"]["exit_code"],
                 body["tested_head_sha"][:12]))
    print("\nhead=%s  base=%s" % (HEAD_SHA, MAIN_SHA))
    print("These are observations of one run. CS-01 is still open.")
    return 0


if __name__ == "__main__":
    sys.exit(main())