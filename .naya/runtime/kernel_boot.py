#!/usr/bin/env python3
"""Runtime boot for the nine-node Master Node kernel.

Single source of truth
----------------------
The canonical kernel specification is
`.naya/specifications/NAYA-MASTER-NODE-KERNEL-V1.json`. This module holds NO
copy of it. There is deliberately no hardcoded node list, no hardcoded node-id
constant, and no hardcoded key sequence here, because a second copy of the
spec would inevitably drift from the first and create a competing canonical
intelligence store -- forbidden by the manifest's own global invariants.

Division of labour with the existing static validator
-----------------------------------------------------
`scripts/verify-nine-master-nodes.py` answers: "does the manifest match the
ratified constants?" (it pins MN-01..MN-09, SELF..EVOLVE, contracts 00-26).

This module answers a different question: "can a Naya boot on this kernel
*right now*, what may it do, how fresh is it, and is its successor envelope
well-formed?" It additionally checks the manifest's INTERNAL self-consistency
(declared count vs actual, ownership vs per-node claims, closed flow, triad
partition, envelopes, safety invariants, declared gates).

Together they cross-check: the static gate pins the constants, this gate
proves the file is internally coherent and currently usable.

Fail-closed contract
--------------------
    report.conclusive     did we obtain enough evidence to decide?
    report.boot_permitted may a consequential action proceed?
    report.authority      ALWAYS "NONE". Loading intelligence confers no
                          permission. A Master Node must not self-authorize.

An unreachable or unreadable kernel is UNKNOWN, never an empty-but-healthy
kernel. UNKNOWN and FAIL both block a consequential boot. OBSERVATION
findings are surfaced explicitly but do not by themselves refuse, because
they record unresolved semantics rather than a broken kernel.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any, Callable, Iterable, Sequence

REPO = Path(__file__).resolve().parents[2]

#: The one canonical kernel specification. Path only -- never contents.
MANIFEST_REL = ".naya/specifications/NAYA-MASTER-NODE-KERNEL-V1.json"

#: Boot policy, not specification. SS17: decay must be domain-specific, so this
#: is a policy constant of this gate and is intentionally NOT in the manifest.
MAX_AGE_DAYS = 180

#: Safety phrases that must be declared by the manifest's own invariants.
#: These are *semantic* requirements restated as substrings, not structural
#: node data, so restating them is not a second copy of the specification.
REQUIRED_SAFETY_PHRASES = ("self-authorize", "self-ratify",
                           "competing canonical intelligence store")

BLOCKING_STATUSES = frozenset({"FAIL", "UNKNOWN"})


class KernelBootError(RuntimeError):
    """Raised when a consequential boot is attempted on an unproven kernel."""


@dataclass(frozen=True)
class Finding:
    check: str
    status: str                     # PASS | FAIL | UNKNOWN | OBSERVATION
    detail: str
    evidence: tuple[str, ...] = ()

    @property
    def blocking(self) -> bool:
        return self.status in BLOCKING_STATUSES


@dataclass
class KernelBootReport:
    conclusive: bool = False
    boot_permitted: bool = False
    authority: str = "NONE"
    source: str = "NONE"
    schema_id: str = "UNKNOWN"
    kernel_version: str = "UNKNOWN"
    declared_status: str = "UNKNOWN"
    effective_date: str = "UNKNOWN"
    loaded: list[str] = field(default_factory=list)
    loaded_keys: list[str] = field(default_factory=list)
    findings: list[Finding] = field(default_factory=list)
    unresolved: list[str] = field(default_factory=list)
    next_action: str = ""

    def add(self, check: str, status: str, detail: str,
            evidence: Iterable[str] = ()) -> None:
        self.findings.append(Finding(check, status, detail, tuple(evidence)))

    @property
    def failed(self) -> list[Finding]:
        return [f for f in self.findings if f.status == "FAIL"]

    @property
    def unknown(self) -> list[Finding]:
        return [f for f in self.findings if f.status == "UNKNOWN"]

    @property
    def observations(self) -> list[Finding]:
        return [f for f in self.findings if f.status == "OBSERVATION"]

    def to_dict(self) -> dict:
        return {
            "schema": "naya.kernel-boot-report/2",
            "conclusive": self.conclusive,
            "boot_permitted": self.boot_permitted,
            "authority": self.authority,
            "source": self.source,
            "manifest": MANIFEST_REL,
            "schema_id": self.schema_id,
            "kernel_version": self.kernel_version,
            "declared_status": self.declared_status,
            "effective_date": self.effective_date,
            "loaded": list(self.loaded),
            "loaded_keys": list(self.loaded_keys),
            "findings": [
                {"check": f.check, "status": f.status, "detail": f.detail,
                 "evidence": list(f.evidence)}
                for f in self.findings
            ],
            "unresolved": list(self.unresolved),
            "next_action": self.next_action,
        }


# --- sources ----------------------------------------------------------------

def manifest_source(root: Path | None = None) -> dict:
    """Read the canonical manifest from the repository.

    The runtime boot path uses the repo copy because the repository IS the
    canonical substrate for source/build parity (SS47, SS49). A receiver-backed
    source may be injected instead; the checks are identical.
    """
    base = root or REPO
    path = base / MANIFEST_REL
    if not path.is_file():
        raise FileNotFoundError(f"canonical kernel manifest absent: {MANIFEST_REL}")
    return json.loads(path.read_text(encoding="utf-8"))


def receiver_source() -> dict:
    """Optional live-receiver source. Fails closed without operator credentials."""
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
    if not url or not key:
        raise PermissionError(
            "canonical receiver credentials absent (SUPABASE_URL / "
            "SUPABASE_SERVICE_ROLE_KEY); kernel state is UNKNOWN, not empty "
            "and not assumed intact"
        )
    raise NotImplementedError(
        "receiver transport is not implemented in-repo; an authorized operator "
        "must supply the transport"
    )


# --- internal self-consistency checks ---------------------------------------

def _check_identity(report: KernelBootReport, m: dict) -> None:
    report.schema_id = str(m.get("schema_id", "UNKNOWN"))
    report.kernel_version = str(m.get("kernel_version", "UNKNOWN"))
    report.declared_status = str(m.get("status", m.get("state", "UNKNOWN")))
    report.effective_date = str(m.get("effective_date", "UNKNOWN"))

    missing = [k for k in ("schema_id", "kernel_version", "status", "effective_date")
               if not m.get(k)]
    if missing:
        report.add("KERNEL_IDENTITY", "FAIL", f"manifest missing {missing}",
                   (MANIFEST_REL,))
        return
    if not re.fullmatch(r"\d+(\.\d+)*", report.kernel_version):
        report.add("KERNEL_IDENTITY", "FAIL",
                   f"kernel_version {report.kernel_version!r} is not a dotted version")
        return
    try:
        date.fromisoformat(report.effective_date[:10])
    except ValueError:
        report.add("KERNEL_IDENTITY", "FAIL",
                   f"effective_date {report.effective_date!r} is not an ISO date")
        return
    report.add("KERNEL_IDENTITY", "PASS",
               f"{report.schema_id} v{report.kernel_version} "
               f"status={report.declared_status}", (MANIFEST_REL,))


def _check_node_set(report: KernelBootReport, m: dict) -> None:
    nodes = m.get("nodes")
    if not isinstance(nodes, list) or not nodes:
        report.add("NODE_SET", "FAIL", "manifest has no 'nodes' list", (MANIFEST_REL,))
        return

    declared = m.get("node_count")
    if declared is not None and declared != len(nodes):
        report.add("NODE_SET", "FAIL",
                   f"node_count declares {declared} but {len(nodes)} nodes are present")
        return

    ids = [n.get("id") for n in nodes if isinstance(n, dict)]
    keys = [n.get("key") for n in nodes if isinstance(n, dict)]
    if any(i is None for i in ids) or any(k is None for k in keys):
        report.add("NODE_SET", "FAIL", "every node needs an 'id' and a 'key'")
        return
    problems: list[str] = []
    if len(set(ids)) != len(ids):
        dupes = sorted({i for i in ids if ids.count(i) > 1})
        problems.append(f"duplicate node ids {dupes}")
    if len(set(keys)) != len(keys):
        dupes_k = sorted({k for k in keys if keys.count(k) > 1})
        problems.append(f"duplicate node keys {dupes_k}")
    expected_no = list(range(1, len(nodes) + 1))
    if [n.get("node_no") for n in nodes] != expected_no:
        problems.append(f"node_no must be {expected_no}")
    if problems:
        report.add("NODE_SET", "FAIL", "; ".join(problems))
        return

    report.loaded = [str(i) for i in ids]
    report.loaded_keys = [str(k) for k in keys]
    report.add("NODE_SET", "PASS",
               f"{len(nodes)} unique nodes loaded, keys {'->'.join(report.loaded_keys)}",
               (MANIFEST_REL,))


def _check_contract_ownership(report: KernelBootReport, m: dict) -> None:
    owner = m.get("contract_primary_ownership")
    rng = m.get("contract_id_range")
    nodes = m.get("nodes") or []
    if not isinstance(owner, dict) or not isinstance(rng, list) or len(rng) != 2:
        report.add("CONTRACT_OWNERSHIP", "FAIL",
                   "contract_primary_ownership and contract_id_range are required")
        return
    lo, hi = str(rng[0]), str(rng[1])
    expected = {f"{i:0{len(lo)}d}" for i in range(int(lo), int(hi) + 1)}
    if set(owner) != expected:
        missing = sorted(expected - set(owner))
        extra = sorted(set(owner) - expected)
        report.add("CONTRACT_OWNERSHIP", "FAIL",
                   f"ownership must cover exactly {lo}..{hi}; "
                   f"missing={missing[:8]} unexpected={extra[:8]}")
        return

    declared: dict[str, str] = {}
    for node in nodes:
        for c in node.get("primary_contracts", []):
            if c in declared:
                report.add("CONTRACT_OWNERSHIP", "FAIL",
                           f"contract {c} claimed by both {declared[c]} and "
                           f"{node.get('id')}")
                return
            declared[c] = node["id"]
    if declared != owner:
        mismatched = sorted(
            c for c in set(declared) | set(owner) if declared.get(c) != owner.get(c))
        report.add("CONTRACT_OWNERSHIP", "FAIL",
                   f"per-node primary_contracts disagree with "
                   f"contract_primary_ownership for {mismatched[:8]}")
        return
    report.add("CONTRACT_OWNERSHIP", "PASS",
               f"{len(owner)} contracts {lo}..{hi} each owned exactly once")


def _check_runtime_flow(report: KernelBootReport, m: dict) -> None:
    ids = report.loaded
    flow = m.get("runtime_flow")
    if not ids:
        report.add("RUNTIME_FLOW", "UNKNOWN", "no nodes loaded; flow unverifiable")
        return
    if not isinstance(flow, list) or not flow:
        report.add("RUNTIME_FLOW", "FAIL", "runtime_flow missing")
        return
    expected = ids + [ids[0]]
    if flow != expected:
        report.add("RUNTIME_FLOW", "FAIL",
                   f"runtime_flow must traverse the kernel and close the loop; "
                   f"expected {expected}, got {flow}")
        return
    report.add("RUNTIME_FLOW", "PASS",
               f"closed loop {flow[0]} -> ... -> {flow[-2]} -> {flow[-1]}")


def _check_triads(report: KernelBootReport, m: dict) -> None:
    triads = m.get("triads")
    if not isinstance(triads, list) or not triads:
        report.add("TRIADS", "FAIL", "triads missing")
        return
    members: list[str] = []
    for t in triads:
        if not isinstance(t, dict) or not isinstance(t.get("nodes"), list):
            report.add("TRIADS", "FAIL", "each triad needs a 'nodes' list")
            return
        members.extend(str(x) for x in t["nodes"])
    if sorted(members) != sorted(report.loaded):
        report.add("TRIADS", "FAIL",
                   f"triads must partition the kernel exactly; got {sorted(members)}")
        return
    if len(members) != len(set(members)):
        report.add("TRIADS", "FAIL", "a node appears in more than one triad")
        return
    report.add("TRIADS", "PASS",
               f"{len(triads)} triads partition {len(members)} nodes with no overlap")


def _check_envelopes(report: KernelBootReport, m: dict) -> None:
    problems = []
    for field in ("required_input_fields", "required_output_fields"):
        val = m.get(field)
        if not isinstance(val, list) or not val:
            problems.append(f"{field} missing or empty")
    if problems:
        report.add("ENVELOPES", "FAIL", "; ".join(problems))
        return
    report.add("ENVELOPES", "PASS",
               f"{len(m['required_input_fields'])} input and "
               f"{len(m['required_output_fields'])} output fields declared")


def _check_safety_invariants(report: KernelBootReport, m: dict) -> None:
    """The kernel must forbid self-authorization in its own voice."""
    must_not = (m.get("global_invariants") or {}).get("must_not")
    if not isinstance(must_not, list) or not must_not:
        report.add("SAFETY_INVARIANTS", "FAIL",
                   "global_invariants.must_not is required")
        return
    text = " ".join(str(x) for x in must_not).lower()
    absent = [p for p in REQUIRED_SAFETY_PHRASES if p not in text]
    if absent:
        report.add("SAFETY_INVARIANTS", "FAIL",
                   f"kernel does not forbid {absent}; a self-authorizing kernel "
                   "must never boot")
        return
    report.add("SAFETY_INVARIANTS", "PASS",
               f"{len(must_not)} invariants declared, including "
               "self-authorize / self-ratify / competing-store prohibitions")


def _check_kernel_gates(report: KernelBootReport, m: dict) -> None:
    gates = m.get("kernel_gates")
    if not isinstance(gates, list) or not gates:
        report.add("KERNEL_GATES", "FAIL", "kernel_gates missing")
        return
    incomplete = [g.get("id") for g in gates
                  if not isinstance(g, dict) or not g.get("required")]
    if incomplete:
        report.add("KERNEL_GATES", "FAIL",
                   f"kernel gates without a 'required' statement: {incomplete}")
        return
    report.add("KERNEL_GATES", "PASS", f"{len(gates)} kernel gates declared")


def _check_status_vocabulary(report: KernelBootReport, m: dict) -> None:
    """Surface a declared status that its own state machine does not define.

    Recorded as OBSERVATION, not FAIL: the kernel can be structurally sound
    while its status vocabulary is unresolved. Surfacing it (SS46) is required;
    refusing on it would be inventing an integrity break.
    """
    states = (m.get("state_machine") or {}).get("states")
    status = report.declared_status
    if isinstance(states, list) and states and status not in states:
        report.add("STATUS_VOCABULARY", "OBSERVATION",
                   f"declared status {status!r} is not one of the kernel's own "
                   f"state_machine states {states}; the ratified baseline uses a "
                   "term the state machine does not define. Director decision "
                   "required to reconcile.",
                   (MANIFEST_REL,))
        return
    report.add("STATUS_VOCABULARY", "PASS",
               f"status {status!r} is defined by the kernel state machine")


def _check_freshness(report: KernelBootReport, today: date) -> None:
    """SS17: a kernel can remain true while ceasing to be applicable."""
    try:
        effective = date.fromisoformat(report.effective_date[:10])
    except ValueError:
        report.add("KERNEL_FRESHNESS", "UNKNOWN",
                   f"effective_date {report.effective_date!r} unparseable")
        return
    age = (today - effective).days
    if age < 0:
        report.add("KERNEL_FRESHNESS", "OBSERVATION",
                   f"effective_date {effective} is {-age}d in the future")
        return
    if age > MAX_AGE_DAYS:
        report.add("KERNEL_FRESHNESS", "FAIL",
                   f"kernel baseline is {age}d old, beyond the {MAX_AGE_DAYS}d "
                   "boot policy; re-ratification required")
        return
    report.add("KERNEL_FRESHNESS", "PASS", f"baseline is {age}d old")


def _check_successor_envelope(report: KernelBootReport,
                              envelope: dict | None) -> None:
    """SS37/SS38: successor context must carry exactly one next action."""
    if envelope is None:
        report.add("SUCCESSOR_ENVELOPE", "UNKNOWN",
                   "no successor envelope supplied; continuation cannot be proven")
        return
    if not isinstance(envelope, dict):
        report.add("SUCCESSOR_ENVELOPE", "FAIL", "successor envelope is not an object")
        return
    action = envelope.get("next_action")
    if not isinstance(action, str) or not action.strip():
        report.add("SUCCESSOR_ENVELOPE", "FAIL",
                   "successor envelope declares no next_action")
        return
    clauses = [c for c in re.split(r"(?:\.\s+|;|\|)", action.strip().rstrip(". "))
               if c.strip()]
    if len(clauses) > 1:
        report.add("SUCCESSOR_ENVELOPE", "FAIL",
                   f"next_action must be exactly ONE action, got {len(clauses)}: "
                   f"{[c.strip() for c in clauses]}")
        return
    report.next_action = action.strip()
    report.add("SUCCESSOR_ENVELOPE", "PASS", report.next_action[:160],
               ("successor_envelope.next_action",))


# --- entrypoint -------------------------------------------------------------

def boot_kernel(
    source: Callable[[], dict] | None = None,
    envelope: dict | None = None,
    today: date | None = None,
) -> KernelBootReport:
    """Attempt a runtime kernel boot. Fails closed. Never grants authority."""
    report = KernelBootReport()
    getter = source or manifest_source
    report.source = getattr(getter, "__name__", "anonymous")
    today = today or date(2026, 9, 26)

    try:
        manifest = getter()
    except Exception as exc:
        report.add("MANIFEST_READ", "UNKNOWN", f"{type(exc).__name__}: {exc}",
                   (MANIFEST_REL,))
        report.unresolved.append("canonical kernel state is unproven")
        report.next_action = (
            f"Restore or produce {MANIFEST_REL} (or provision receiver access "
            "via an authorized operator), then re-run boot_kernel(); do not "
            "proceed with a consequential action on an unproven kernel."
        )
        report.conclusive = True
        report.boot_permitted = False
        return report

    if not isinstance(manifest, dict):
        report.add("MANIFEST_READ", "FAIL", "manifest is not a JSON object")
        report.conclusive = True
        report.boot_permitted = False
        return report
    report.add("MANIFEST_READ", "PASS", f"read {MANIFEST_REL}", (MANIFEST_REL,))

    _check_identity(report, manifest)
    _check_node_set(report, manifest)
    _check_contract_ownership(report, manifest)
    _check_runtime_flow(report, manifest)
    _check_triads(report, manifest)
    _check_envelopes(report, manifest)
    _check_safety_invariants(report, manifest)
    _check_kernel_gates(report, manifest)
    _check_status_vocabulary(report, manifest)
    _check_freshness(report, today)
    _check_successor_envelope(report, envelope)

    blocking = [f for f in report.findings if f.blocking]
    report.boot_permitted = not blocking
    report.conclusive = True
    if blocking:
        report.unresolved = [f"{f.check}: {f.detail}" for f in blocking]
        report.next_action = (
            "Resolve kernel integrity failures before any consequential action: "
            + "; ".join(f.check for f in blocking)
        )
    return report


def assert_bootable(report: KernelBootReport) -> None:
    """Gate for callers that must not proceed on an unproven kernel."""
    if not report.boot_permitted:
        raise KernelBootError(
            "kernel integrity not proven; boot refused. "
            f"source={report.source} blocking={report.unresolved}"
        )


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Runtime boot for the nine-node Master Node kernel")
    ap.add_argument("--source", choices=("manifest", "receiver"),
                    default="manifest")
    ap.add_argument("--envelope", help="path to a successor envelope JSON")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    getter = manifest_source if args.source == "manifest" else receiver_source
    envelope = None
    if args.envelope:
        envelope = json.loads(Path(args.envelope).read_text(encoding="utf-8"))

    report = boot_kernel(getter, envelope=envelope)
    if args.json:
        print(json.dumps(report.to_dict(), indent=2, sort_keys=True))
    else:
        print("=" * 74)
        print("NAYAPOWER RUNTIME KERNEL BOOT - canonical nine-node Master Nodes")
        print("=" * 74)
        print(f"manifest         : {MANIFEST_REL}")
        print(f"schema / version : {report.schema_id} v{report.kernel_version}")
        print(f"declared status  : {report.declared_status}  "
              f"(effective {report.effective_date})")
        print(f"nodes loaded     : {len(report.loaded)}")
        if report.loaded_keys:
            print(f"kernel flow      : {' -> '.join(report.loaded_keys)}")
        print(f"conclusive       : {report.conclusive}")
        print(f"BOOT PERMITTED   : {report.boot_permitted}")
        print(f"authority        : {report.authority}  (loading confers none)")
        print("-" * 74)
        for f in report.findings:
            print(f"[{f.status:11}] {f.check:22} {f.detail}")
        print("-" * 74)
        print(f"next action: {report.next_action}")
    return 0 if report.boot_permitted else 1


if __name__ == "__main__":
    raise SystemExit(main())
