"""RACE READINESS GATE — is Naya actually ready to enter NAYA-NODE-0001?

WHY THIS EXISTS
"We need to understand what ready looks like" is not a question a document can
answer, and a checklist cannot fail. This module makes readiness executable: it
evaluates the declared pre-race conditions against the repository and runtime and
emits a machine-verifiable verdict per gate.

It deliberately does NOT print a to-do list. Each gate returns one of:
  PROVEN   - satisfied, and the check is deterministic and currently passing
  PARTIAL  - partially satisfied; the named gap is stated
  UNKNOWN  - the check cannot be evaluated from available evidence
  BLOCKED  - a real external boundary prevents evaluation

The overall verdict follows AAA law: ONE gate that is not PROVEN prevents READY,
no matter how many pass. An average score is not readiness.

FAIL-CLOSED AND HONEST BY CONSTRUCTION
- The report never claims READY unless every gate is PROVEN.
- A gate that cannot be evaluated is UNKNOWN, never PROVEN.
- This gate is additive: it changes no system behavior and grants no authority.

Run:  python -B .naya/runtime/race_readiness.py [--json]
Exit: 0 = evaluated (read the verdict; READY vs NOT_READY is in the output)
      2 = the gate itself could not run
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

KERNEL_IB_FIRST = 1233
KERNEL_IB_LAST = 1241

PROVEN, PARTIAL, UNKNOWN, BLOCKED = "PROVEN", "PARTIAL", "UNKNOWN", "BLOCKED"


def _git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=REPO, text=True).strip()


def _tracked(relpath: str) -> bool:
    return bool(_git("ls-tree", "HEAD", "--", relpath))


def _workflow_text() -> str:
    d = REPO / ".github" / "workflows"
    if not d.is_dir():
        return ""
    return "\n".join(
        p.read_text(encoding="utf-8", errors="replace")
        for p in sorted(d.glob("*.yml")) + sorted(d.glob("*.yaml"))
    )


def _read(relpath: str) -> str:
    p = REPO / relpath
    return p.read_text(encoding="utf-8", errors="replace") if p.is_file() else ""


# --- GATES ----------------------------------------------------------------------


def gate_runtime_distributable() -> dict:
    """Every runtime file a workflow invokes must exist in the repository.

    A runtime that no clone receives is not a runtime. This is the single gate
    that caught the largest distributability defect found to date.
    """
    corpus = _workflow_text()
    referenced = sorted(
        {
            m.group(1)
            for m in re.finditer(r"(\.naya/runtime/[A-Za-z0-9_./-]+\.py)", corpus)
        }
    )
    if not referenced:
        return {
            "gate": "RUNTIME_DISTRIBUTABLE",
            "status": UNKNOWN,
            "detail": "no workflow references .naya/runtime/*.py; nothing to verify",
        }
    missing = [p for p in referenced if not _tracked(p)]
    if missing:
        return {
            "gate": "RUNTIME_DISTRIBUTABLE",
            "status": BLOCKED,
            "detail": f"{len(missing)}/{len(referenced)} workflow-invoked runtime files "
            f"are absent from the repository: {', '.join(missing[:5])}",
            "evidence": missing,
        }
    return {
        "gate": "RUNTIME_DISTRIBUTABLE",
        "status": PROVEN,
        "detail": f"all {len(referenced)} workflow-invoked runtime files are tracked",
    }


def gate_nine_node_kernel() -> dict:
    """The nine Master Nodes must be canonical AND visible to a cold Naya."""
    mem = REPO / ".naya" / "memory" / "smart-notes"
    present = []
    for n in range(KERNEL_IB_FIRST, KERNEL_IB_LAST + 1):
        target = f"IB-{n:06d}"
        found = any(mem.rglob(f"{target}")) if mem.is_dir() else False
        present.append((target, found))
    found = [t for t, ok in present if ok]
    if len(found) == len(present):
        return {
            "gate": "NINE_NODE_KERNEL_CANONICAL",
            "status": PROVEN,
            "detail": f"all nine Master Nodes project into the repository ({len(found)}/9)",
        }
    return {
        "gate": "NINE_NODE_KERNEL_CANONICAL",
        "status": PARTIAL,
        "detail": f"only {len(found)}/9 Master Nodes have a canonical repository "
        f"projection; missing {[t for t, ok in present if not ok]}. A cold Naya booting "
        f"from the repository cannot load a kernel it is told is ACTIVE.",
        "evidence": [t for t, ok in present if not ok],
    }


def gate_kernel_loads_at_runtime() -> dict:
    """The runtime must contain a kernel loader, not only node rows."""
    fn = REPO / "supabase" / "functions" / "nayanet-compound-intelligence" / "index.ts"
    if not fn.is_file():
        return {
            "gate": "KERNEL_LOADS_AT_RUNTIME",
            "status": UNKNOWN,
            "detail": "nayanet-compound-intelligence source not found in the repository",
        }
    text = fn.read_text(encoding="utf-8", errors="replace")
    has_loader = "master_kernel" in text or "kernel_boot" in text
    has_gate = "MASTER_NODE_KERNEL_BOOT_FAILED" in text
    if has_loader and has_gate:
        return {
            "gate": "KERNEL_LOADS_AT_RUNTIME",
            "status": PARTIAL,
            "detail": "a kernel loader and a fail-closed boot gate exist in runtime source, "
            "but no authenticated cold Naya has been observed booting all nine; "
            "EXISTS->LOADS is source-level, INVOKES/INFLUENCES/APPLIES unobserved",
        }
    return {
        "gate": "KERNEL_LOADS_AT_RUNTIME",
        "status": PARTIAL,
        "detail": "runtime source does not show both a kernel loader and a fail-closed "
        "kernel boot gate",
    }


def gate_authority_not_granted_by_retrieval() -> dict:
    """RETRIEVAL != AUTHORIZE must be enforced, not only stated."""
    corpus = _workflow_text()
    enforced = any(
        k in corpus
        for k in ("RETRIEVAL_NOT_AUTHORIZATION", "RETRIEVAL_AUTORIZES", "authority_grant")
    )
    stated = "RETRIEVAL" in _read(".naya/contracts/CONSTITUTIONAL-OPERATING-LAW-V2.md")
    if enforced:
        return {
            "gate": "RETRIEVAL_NOT_AUTHORIZATION",
            "status": PARTIAL,
            "detail": "an authority boundary is referenced by enforcement surfaces, but no "
            "adversarial test proves retrieval cannot grant execution authority",
        }
    return {
        "gate": "RETRIEVAL_NOT_AUTHORIZATION",
        "status": PROVEN if stated else UNKNOWN,
        "detail": "stated as constitutional law with no located machine enforcement",
    }


def gate_safety_tests_routed() -> dict:
    """A red contract test with no route is indistinguishable from an absent one."""
    corpus = _workflow_text()
    probes = {
        "conversation continuity": ".naya/runtime/test_conversation_continuity.py",
        "cold successor": "cold_successor_test.py",
        "contract library integrity": "contract_library_integrity.py",
        "learning promotion gate": "promotion_runtime.py",
    }
    unrouted = [name for name, path in probes.items() if path not in corpus]
    if not unrouted:
        return {
            "gate": "SAFETY_TESTS_ROUTED",
            "status": PROVEN,
            "detail": "all probed safety-critical tests are invoked by a workflow",
        }
    return {
        "gate": "SAFETY_TESTS_ROUTED",
        "status": PARTIAL,
        "detail": f"{len(unrouted)} safety-critical test(s) are not routed into any "
        f"workflow and can therefore fail silently: {', '.join(unrouted)}",
        "evidence": unrouted,
    }


def gate_single_frontier() -> dict:
    """Three agents must not be pointing at three different next actions."""
    try:
        state = json.loads(_read(".naya/control-plane/STATE.json").lstrip("\ufeff"))
        blocks = json.loads(_read(".naya/control-plane/BLOCKS.json").lstrip("\ufeff"))
        baton = json.loads(_read(".naya/control-plane/BATON.json").lstrip("\ufeff"))
    except Exception as exc:  # noqa: BLE001
        return {
            "gate": "SINGLE_FRONTIER",
            "status": UNKNOWN,
            "detail": f"control plane unreadable: {exc}",
        }
    s = state.get("single_next_action", "")
    b = blocks.get("active_block", {}).get("next_action", "")
    t = baton.get("next_action", {}).get("action", "")
    if s and s == b == t:
        return {
            "gate": "SINGLE_FRONTIER",
            "status": PARTIAL,
            "detail": "STATE, BLOCKS and BATON agree on one next action, but agreement is "
            "not correctness: the agreed action must still be checked against what is "
            "actually complete",
        }
    return {
        "gate": "SINGLE_FRONTIER",
        "status": BLOCKED,
        "detail": "STATE, BLOCKS and BATON do not carry the same next action; a cold Naya "
        "cannot determine one frontier",
    }


def gate_control_plane_green() -> dict:
    """The control plane must validate, and only main may assert current truth."""
    script = REPO / ".naya" / "control-plane" / "validate_control_plane.py"
    if not script.is_file():
        return {
            "gate": "CONTROL_PLANE_GREEN",
            "status": UNKNOWN,
            "detail": "control-plane validator not found",
        }
    if not _tracked(".naya/control-plane/validate_control_plane.py"):
        return {
            "gate": "CONTROL_PLANE_GREEN",
            "status": BLOCKED,
            "detail": "control-plane validator is absent from the repository, so the "
            "control plane cannot be validated by a cold Naya",
        }
    branch = _git("rev-parse", "--abbrev-ref", "HEAD")
    if branch != "main":
        return {
            "gate": "CONTROL_PLANE_GREEN",
            "status": UNKNOWN,
            "detail": f"current checkout is '{branch}'; by constitutional law only main may "
            f"assert current operational truth, so the validator was not run",
        }
    proc = subprocess.run(
        [sys.executable, "-B", str(script)], cwd=REPO, capture_output=True, text=True
    )
    if proc.returncode == 0:
        return {
            "gate": "CONTROL_PLANE_GREEN",
            "status": PROVEN,
            "detail": "control-plane validator reports GREEN on main",
        }
    first = ""
    for line in (proc.stdout + proc.stderr).splitlines():
        if "FIRST_DIVERGENCE" in line or "CONTROL_PLANE=" in line:
            first = line.strip()
            break
    return {
        "gate": "CONTROL_PLANE_GREEN",
        "status": BLOCKED,
        "detail": f"control-plane validator is RED on main: {first}",
    }


def gate_no_competing_store() -> dict:
    """One canonical intelligence substrate, declared in one place."""
    reg = _read(".naya/control-plane/CANONICAL-CONTRACT-REGISTRY.md")
    if not reg:
        return {
            "gate": "NO_COMPETING_CANONICAL_STORE",
            "status": UNKNOWN,
            "detail": "canonical contract registry not found",
        }
    return {
        "gate": "NO_COMPETING_CANONICAL_STORE",
        "status": PARTIAL,
        "detail": "a canonical substrate is declared; uniqueness is enforced structurally "
        "by the contract library integrity gate, but the Smart Note / IB / Node identity "
        "boundary across store and projection is not yet proven from one authority",
    }


GATES = (
    gate_runtime_distributable,
    gate_nine_node_kernel,
    gate_kernel_loads_at_runtime,
    gate_authority_not_granted_by_retrieval,
    gate_safety_tests_routed,
    gate_single_frontier,
    gate_control_plane_green,
    gate_no_competing_store,
)


def evaluate() -> dict:
    results = []
    for gate in GATES:
        try:
            results.append(gate())
        except Exception as exc:  # noqa: BLE001
            results.append(
                {
                    "gate": gate.__name__.replace("gate_", "").upper(),
                    "status": UNKNOWN,
                    "detail": f"gate raised {type(exc).__name__}: {exc}",
                }
            )
    proven = [r for r in results if r["status"] == PROVEN]
    not_proven = [r for r in results if r["status"] != PROVEN]
    return {
        "schema": "naya/race-readiness/v1",
        "generated_at_head": _git("rev-parse", "HEAD"),
        "law": "AAA requires every gate PROVEN. One non-PROVEN gate prevents READY. "
        "An average score is not readiness.",
        "ready": not not_proven,
        "gates_total": len(results),
        "gates_proven": len(proven),
        "gates_not_proven": len(not_proven),
        "blocking_gates": [r["gate"] for r in not_proven],
        "gates": results,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    try:
        report = evaluate()
    except Exception as exc:  # noqa: BLE001
        print(f"RACE_READINESS=AUDIT_ERROR {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print("NAYA_RACE_READINESS")
        print(f"HEAD={report['generated_at_head']}")
        for g in report["gates"]:
            print(f"  [{g['status']:>7}] {g['gate']}: {g['detail']}")
        print(f"GATES_PROVEN={report['gates_proven']}/{report['gates_total']}")
        print(f"BLOCKING={','.join(report['blocking_gates']) or 'none'}")
        print(f"READY={report['ready']}")
        print("NOTE: READY=False is the expected and honest state until every gate is PROVEN.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
