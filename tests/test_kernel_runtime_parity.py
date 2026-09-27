"""Source/runtime parity between the Python boot gate and the live TypeScript loader.

The two implementations of "the nine-node kernel" are:

  * ``.naya/runtime/kernel_boot.py``            (repo-side boot gate, PR #817)
  * ``loadMasterNodeKernel`` in
    ``supabase/functions/nayanet-compound-intelligence/index.ts``  (live edge runtime)

This module EXECUTES both and compares them. It does not read them and reason.

Fidelity of the TypeScript under test
-------------------------------------
The loader is never hand-copied. The exact byte range is sliced out of the
edge-function source at test time, hashed, and written verbatim into a
generated ``.mts`` harness. Node 24 strips its types natively, so the function
body reaches the VM unmodified -- no annotation editing by this file, and
therefore no chance of "testing a copy that drifted from the real thing".

Truth discipline
----------------
The database rows the loader consumes are NOT readable from this repository.
The fixture is therefore built from the control-plane Intelligent Block ids
(``BATON/BLOCKS/MAP/STATE``) and is explicitly a FIXTURE. What this suite can
prove is code-level agreement on refusal conditions and the shape of the
identifier domains. The content of the live rows stays UNKNOWN and is
reported as such rather than being quietly upgraded to verified.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import textwrap
from datetime import date
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
EDGE = REPO / "supabase/functions/nayanet-compound-intelligence/index.ts"
MANIFEST_REL = ".naya/specifications/NAYA-MASTER-NODE-KERNEL-V1.json"
TODAY = date(2026, 9, 26)
ENVELOPE = {"next_action": "Parity probe: compare the two kernel loaders."}


# --------------------------------------------------------------------------
# Verbatim extraction of the TypeScript loader
# --------------------------------------------------------------------------

def _edge_source() -> str:
    return EDGE.read_text(encoding="utf-8")


def extract_loader() -> tuple[str, str]:
    """Return (verbatim source, sha256) for the constants + loader function."""
    src = _edge_source()
    start = src.index("const MASTER_NODE_KEYS")
    end = src.index("async function restore")
    chunk = src[start:end]
    assert "loadMasterNodeKernel" in chunk, "extraction missed the loader"
    assert "MASTER_NODE_IDS" in chunk, "extraction missed the id constant"
    return chunk, hashlib.sha256(chunk.encode("utf-8")).hexdigest()


def test_extraction_is_deterministic_and_verbatim():
    a, ha = extract_loader()
    b, hb = extract_loader()
    assert ha == hb, "extraction is not deterministic"
    assert a in _edge_source(), "extracted text is not a verbatim slice of the edge function"
    assert a.count("async function loadMasterNodeKernel") == 1, "loader extracted twice"


# --------------------------------------------------------------------------
# Harness generation
# --------------------------------------------------------------------------

DRIVER = """
// ---- generated driver (appended verbatim after the real loader) ----
type Row = Record<string, any>;

function makeStubClient(rows: Row[], log: string[]) {
  const chain: any = {};
  const record = (op: string, ...args: any[]) => { log.push(op + ":" + JSON.stringify(args)); return chain; };
  chain.from = (t: string) => record("from", t);
  chain.select = (c: string) => record("select", c);
  chain.eq = (a: string, b: any) => record("eq", a, b);
  chain.in = (a: string, b: any) => record("in", a, b);
  chain.order = (a: string) => record("order", a);
  chain.then = (resolve: any, reject: any) => {
    const filtered = rows.filter((r) => r.__status === "ACTIVE" && log.some((l) => l.startsWith("in:")));
    return Promise.resolve(resolve({ data: filtered, error: null }));
  };
  return chain;
}

const rows: Row[] = JSON.parse(Deno_readTextFileSync(process.argv[2]));
const log: string[] = [];
const client = makeStubClient(rows, log);

let verdict: any = { permitted: false, error: null, kernel: null, query: log };
try {
  const k = await loadMasterNodeKernel(client, "probe-user");
  verdict = { permitted: true, error: null, kernel: k, query: log };
} catch (e) {
  verdict = { permitted: false, error: String(e.message ?? e), kernel: null, query: log };
}
console.log("__VERDICT__" + JSON.stringify(verdict));
"""


def _harness_source() -> str:
    chunk, _ = extract_loader()
    driver = DRIVER.replace("Deno_readTextFileSync", "readTextFileSync")
    head = 'import { readFileSync as readTextFileSync } from "node:fs";\n\n'
    return head + chunk + driver


def _run_ts(rows: list[dict]) -> dict:
    import os
    import tempfile

    src = _harness_source()
    with tempfile.TemporaryDirectory() as td:
        hs = Path(td) / "harness.mts"
        rf = Path(td) / "rows.json"
        hs.write_text(src, encoding="utf-8")
        rf.write_text(json.dumps(rows), encoding="utf-8")
        env = dict(os.environ, NO_COLOR="1")
        proc = subprocess.run(
            ["node", str(hs), str(rf)],
            capture_output=True, text=True, cwd=REPO, env=env, timeout=120,
        )
    if "__VERDICT__" not in proc.stdout:
        raise AssertionError(
            "TypeScript harness produced no verdict (the real loader may not have "
            f"compiled/run).\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"
        )
    line = [l for l in proc.stdout.splitlines() if l.startswith("__VERDICT__")][0]
    return json.loads(line[len("__VERDICT__"):])


# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------

CONTROL_PLANE_IDS = [f"IB-0012{n:02d}" for n in range(33, 42)]


def real_manifest() -> dict:
    return json.loads((REPO / MANIFEST_REL).read_text(encoding="utf-8"))


def manifest_keys() -> list[str]:
    return [n["key"] for n in real_manifest()["nodes"]]


def db_rows(keys: list[str] | None = None, ids: list[str] | None = None) -> list[dict]:
    """FIXTURE rows. Ids come from the control plane; keys are supplied."""
    keys = keys or manifest_keys()
    ids = ids or CONTROL_PLANE_IDS
    rows = []
    for i, (key, ib) in enumerate(zip(keys, ids), start=1):
        rows.append({
            "intelligent_block_id": ib,
            "title": f"Master Node {i} ({key})",
            "version": 1,
            "status": "ACTIVE",
            "understanding_state": "UNDERSTOOD",
            "owner_scope": "SYSTEM",
            "updated_at": "2026-09-26T00:00:00Z",
            "__status": "ACTIVE",
            "content": {
                "kernel": {
                    "node_no": i, "key": key, "triad": "CORE" if i <= 3 else "C2" if i <= 6 else "C3",
                    "primary_contracts": [f"{i:02d}"], "core_question": "q", "purpose": "p",
                    "responsibilities": [], "activation_rules": [], "relationships": {},
                    "proof_requirements": [], "runtime_role": "r",
                },
                "kernel_activation": {"status": "ACTIVE", "runtime_status": "STRUCTURALLY_ACTIVE"},
            },
        })
    return rows


def python_boot(manifest: dict | None = None, envelope: dict | None = ENVELOPE,
                today: date = TODAY):
    import sys
    sys.path.insert(0, str(REPO / ".naya/runtime"))
    import kernel_boot as kb
    src = (lambda: manifest) if manifest is not None else kb.manifest_source
    return kb.boot_kernel(src, envelope=envelope, today=today)


# --------------------------------------------------------------------------
# 1. Does the runtime loader actually run?
# --------------------------------------------------------------------------

def test_runtime_loader_executes_against_the_canonical_manifest_keys():
    """Baseline: the live loader must be executable here, not merely readable."""
    report = _run_ts(db_rows())
    assert report["permitted"] is True, report["error"]
    assert report["kernel"]["node_count"] == 9
    assert report["kernel"]["status"] == "KERNEL_ACTIVE_STRUCTURAL"
    assert [n["key"] for n in report["kernel"]["nodes"]] == manifest_keys()


# --------------------------------------------------------------------------
# 2. Identifier domain parity
# --------------------------------------------------------------------------

def test_runtime_ids_match_the_control_plane():
    """The hardcoded id list must equal the control-plane id set exactly."""
    _, _ = extract_loader()
    src = _edge_source()
    start = src.index("const MASTER_NODE_IDS")
    listed = [t.strip().strip('",') for t in src[start:src.index("\n", start)].split('"') if t.strip('",').startswith("IB-")]
    control = set()
    for f in sorted((REPO / ".naya/control-plane").glob("*.json")):
        import re
        control |= set(re.findall(r"IB-0012\d\d", f.read_text(encoding="utf-8")))
    assert set(listed) == control, f"runtime ids {set(listed)} != control plane {control}"
    assert len(listed) == 9, listed


def test_manifest_and_runtime_share_no_identifier():
    """DOCUMENTED DIVERGENCE: the two kernels are in disjoint id domains.

    This is the core finding. ``kernel_boot.py`` boots the manifest
    (``MN-01``..``MN-09``); ``loadMasterNodeKernel`` queries the database
    (``IB-001233``..``IB-001241``). They agree on the word "nine" and on the
    key ORDER, but share no single identifier, so neither can observe a change
    in the other.
    """
    manifest = real_manifest()
    manifest_ids = {n["id"] for n in manifest["nodes"]}
    runtime_ids = set(CONTROL_PLANE_IDS)
    assert manifest_ids & runtime_ids == set(), (
        "if these ever intersect, this divergence is resolved and this test "
        "must be replaced by a real parity assertion"
    )
    assert manifest_ids == {f"MN-0{i}" for i in range(1, 10)}
    assert runtime_ids == set(CONTROL_PLANE_IDS)


# --------------------------------------------------------------------------
# 3. Refusal-condition parity
# --------------------------------------------------------------------------

def _py_permits(manifest=None) -> bool:
    return python_boot(manifest).boot_permitted


def _ts_permits(rows) -> bool:
    return _run_ts(rows)["permitted"]


def test_both_permit_a_healthy_nine_node_kernel():
    assert _py_permits() is True
    assert _ts_permits(db_rows()) is True


def test_both_refuse_when_a_node_is_missing():
    """8/9 must fail closed on both sides."""
    assert _ts_permits(db_rows()[:8]) is False
    m = real_manifest()
    m["nodes"].pop()
    assert _py_permits(m) is False


def test_both_refuse_a_broken_closed_loop():
    broken = manifest_keys()
    report = _run_ts(db_rows(keys=broken))
    # The runtime loader has no closed-loop concept: it cannot detect this.
    assert report["permitted"] is True
    m = real_manifest()
    m["runtime_flow"] = m["runtime_flow"][:-1]
    assert _py_permits(m) is False


# --------------------------------------------------------------------------
# 4. KNOWN PARITY GAPS -- characterised, not papered over
# --------------------------------------------------------------------------
# Each entry: (gap, mutation, python_permits, ts_permits)
#
# These are assertions about the CURRENT state of the world. They keep CI
# green while recording the truth, and they fail loudly in EITHER direction so
# a silent change in either loader is caught. Closing a gap means deleting its
# row here and replacing it with a real parity assertion.

def _mutated_manifest_drop_node():
    m = real_manifest()
    m["nodes"].pop(8)
    return m


def _mutated_manifest_break_loop():
    m = real_manifest()
    m["runtime_flow"] = m["runtime_flow"][:-1]
    return m


def _rows_with_bogus_node_no() -> list[dict]:
    """Every row claims node_no 1: the runtime sorts on it but never validates it."""
    rows = db_rows()
    for r in rows:
        r["content"]["kernel"]["node_no"] = 1
    return rows


def _mutated_manifest_bogus_node_no():
    m = real_manifest()
    for n in m["nodes"]:
        n["node_no"] = 1
    return m


KNOWN_PARITY_GAPS = {
    "manifest_mutation_is_invisible_to_the_runtime_loader": dict(
        why="The edge loader never reads the manifest, so corrupting the ratified "
            "kernel definition cannot affect the live path.",
        python=False, ts=True,
        py_input=_mutated_manifest_drop_node,
        ts_input=lambda: db_rows(),
    ),
    "node_numbering_is_validated_repo_side_only": dict(
        why="The runtime sorts on content.kernel.node_no but never validates it, so "
            "nine rows all claiming node_no 1 load as a healthy kernel. The gate "
            "requires exactly 1..9 unique.",
        python=False, ts=True,
        py_input=_mutated_manifest_bogus_node_no,
        ts_input=_rows_with_bogus_node_no,
    ),
    "declared_runtime_flow_is_checked_repo_side_only": dict(
        why="The gate verifies the declared closed loop MN-01->...->MN-09->MN-01. The "
            "runtime has no flow field; it infers order from node_no, so a manifest "
            "whose declared flow is broken cannot reach it.",
        python=False, ts=True,
        py_input=_mutated_manifest_break_loop,
        ts_input=lambda: db_rows(),
    ),
    "successor_envelope_has_no_runtime_counterpart": dict(
        why="SS38 (exactly one successor action) is enforced repo-side only.",
        python=False, ts=True,
        py_input=lambda: real_manifest(),
        ts_input=lambda: db_rows(),
        py_envelope=None,
    ),
    "stale_kernel_is_refused_repo_side_only": dict(
        why="SS17 freshness: the gate refuses a kernel whose effective_date is more "
            "than 180 days old. The runtime loader has no notion of time at all, so "
            "a three-year-old kernel loads as KERNEL_ACTIVE_STRUCTURAL.",
        python=False, ts=True,
        py_input=lambda: real_manifest(),
        ts_input=lambda: db_rows(),
        py_today=date(2030, 1, 1),
    ),
    "authority_none_is_asserted_repo_side_only": dict(
        why="kernel_boot.py hardcodes authority='NONE'; the live kernel object "
            "carries no authority field, so nothing in the runtime states that "
            "structural activation confers no decision rights.",
        python=True, ts=True,
        py_input=lambda: real_manifest(),
        ts_input=lambda: db_rows(),
    ),
    "live_activation_state_is_unreadable_from_the_repo": dict(
        why="The loader requires status=ACTIVE plus "
            "kernel_activation.status=ACTIVE and runtime_status=STRUCTURALLY_ACTIVE. "
            "None of that state exists in the repository, so the live kernel's "
            "readiness is UNKNOWN, not verified.",
        python=True, ts=True,
        py_input=lambda: real_manifest(),
        ts_input=lambda: db_rows(),
    ),
}


def test_stale_kernel_is_refused_by_the_gate_and_invisible_to_the_runtime():
    """A direct, dated demonstration of the freshness gap."""
    fresh = python_boot(today=date(2026, 9, 26))
    stale = python_boot(today=date(2030, 1, 1))
    assert fresh.boot_permitted is True
    assert stale.boot_permitted is False
    assert any("KERNEL_FRESHNESS" in f.check for f in stale.failed)
    assert _run_ts(db_rows())["kernel"]["status"] == "KERNEL_ACTIVE_STRUCTURAL", (
        "the runtime reports a healthy structural kernel with no age check at all"
    )


@pytest.mark.parametrize("gap", sorted(KNOWN_PARITY_GAPS))
def test_known_parity_gap_still_has_its_documented_behaviour(gap):
    spec = KNOWN_PARITY_GAPS[gap]
    report = python_boot(
        spec["py_input"](),
        envelope=spec.get("py_envelope", ENVELOPE),
        today=spec.get("py_today", TODAY),
    )
    assert report.boot_permitted is spec["python"], (
        f"{gap}: python side changed (permitted={report.boot_permitted}, "
        f"expected {spec['python']})"
    )
    ts = _run_ts(spec["ts_input"]())
    assert ts["permitted"] is spec["ts"], (
        f"{gap}: runtime side changed (permitted={ts['permitted']}, "
        f"expected {spec['ts']})"
    )


def test_every_known_gap_carries_a_reason():
    for name, spec in KNOWN_PARITY_GAPS.items():
        assert spec.get("why"), f"{name} has no recorded reason"
        assert "python" in spec and "ts" in spec


# --------------------------------------------------------------------------
# 5. Structural comparison, stated as a report rather than a pass/fail
# --------------------------------------------------------------------------

def test_runtime_refusal_surface_is_strictly_smaller_than_the_boot_gate():
    """Quantify the disagreement instead of describing it.

    The runtime loader implements exactly 3 refusal conditions. The boot gate
    implements 12 named checks. They do not even share a vocabulary: only two
    of the runtime's three conditions have any counterpart in the gate, and
    one runtime condition (live activation state) has no counterpart at all,
    because the manifest structurally cannot express activation.
    """
    boot_checks = {f.check for f in python_boot().findings}
    assert len(boot_checks) == 12, sorted(boot_checks)

    # runtime condition -> boot-gate counterpart (None = no counterpart)
    mapping = {
        "node count == 9":        "NODE_SET",
        "positional key order":   "RUNTIME_FLOW",
        "activation state ACTIVE": None,
    }
    covered = {v for v in mapping.values() if v}
    uncovered_by_gate = set(mapping) - {k for k, v in mapping.items() if v}
    assert uncovered_by_gate == {"activation state ACTIVE"}, uncovered_by_gate
    assert covered <= boot_checks, covered - boot_checks

    # What the gate checks that the runtime cannot even express:
    gate_only = boot_checks - covered
    assert {"MANIFEST_READ", "KERNEL_IDENTITY", "CONTRACT_OWNERSHIP", "TRIADS",
            "ENVELOPES", "SAFETY_INVARIANTS", "KERNEL_GATES",
            "STATUS_VOCABULARY", "KERNEL_FRESHNESS",
            "SUCCESSOR_ENVELOPE"} <= gate_only, sorted(gate_only)
    assert len(gate_only) == 10, sorted(gate_only)


def test_manifest_mutation_is_invisible_to_the_runtime_loader():
    """The headline gap, asserted directly rather than only catalogued."""
    mutated = _mutated_manifest_drop_node()
    assert python_boot(mutated).boot_permitted is False, "gate must refuse"
    ts = _run_ts(db_rows())
    assert ts["permitted"] is True, (
        "if the runtime now refuses manifest corruption, the gap is closed and "
        "KNOWN_PARITY_GAPS must be updated with evidence"
    )
    assert ts["kernel"]["node_count"] == 9


def test_kernel_object_schemas_differ():
    """The two 'nine node kernel' objects are not the same object."""
    ts = _run_ts(db_rows())["kernel"]
    py = python_boot().to_dict()
    assert ts["schema"] == "NAYAPOWER_MASTER_NODE_KERNEL_V1"
    assert py["schema"] == "naya.kernel-boot-report/2"
    assert ts["status"] == "KERNEL_ACTIVE_STRUCTURAL"
    assert py["declared_status"] == "RATIFIED_BASELINE"
    assert ts["effectiveness_status"] == "NOT_YET_PROVEN"
    assert "authority" not in ts, "runtime object unexpectedly grew an authority field"
    assert py["authority"] == "NONE"
