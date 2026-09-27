#!/usr/bin/env python3
"""Phase 2 BOOT: fail-closed integrity check for the nine Master Nodes.

Why this exists
---------------
The North Star (SS8, SS46, SS47) defines nine Master Contract Intelligence
Nodes as the *semantic kernel*, and requires that a consequential cold boot
loads them and verifies kernel integrity. The acceptance test established
that no repo-resident node manifest or node-retrieval runtime exists, so a
cold Naya currently cannot prove its operating model is intact.

This module makes that failure mode explicit and deterministic instead of
silent. It does NOT invent the kernel. It refuses when the kernel cannot be
proven, and that refusal is the evidence.

Governing invariants honoured
-----------------------------
* SS21  A Node is intelligence, not authority. This loader NEVER grants
        authority. It returns intelligence state only; authority remains
        the exclusive property of the authorization system.
* SS5   One system, one canonical substrate. No interface may create an
        independent kernel; this module resolves a single canonical source.
* SS46  A missing, conflicted, stale, or enforcement-disconnected kernel
        component MUST be surfaced explicitly. Never silently assume intact.
* SS30  UNKNOWN != VERIFIED. An absent source is UNKNOWN, and UNKNOWN is
        never reported as a pass.
* Layer A (LAW) fail-closed: prohibited or unauthorized states return
        boot_permitted=False rather than degrading to a partial boot.

Exit/decision contract
----------------------
    report.conclusive    -- did we obtain enough evidence to decide?
    report.boot_permitted-- may a consequential action proceed?
    report.authority     -- ALWAYS "NONE". Loading intelligence confers
                            no permission whatsoever.
"""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterable, Sequence

REPO = Path(__file__).resolve().parents[2]

# --- SS8: the canonical semantic kernel -------------------------------------
# node_id is the stable machine identity. name is the ratified human identity.
# owns is the declared semantic responsibility (SS8). These are transcribed
# from the ratified North Star; they are the *expected* kernel, never evidence
# that the kernel exists.
MASTER_NODES: tuple[dict[str, Any], ...] = (
    {"node_id": "MN-01", "name": "Constitution, Mission & Scope",
     "owns": ("constitutional_law", "mission", "values", "scope",
              "authority_boundaries", "privacy_defaults")},
    {"node_id": "MN-02", "name": "Identity & Continuity",
     "owns": ("identity", "memory_continuity", "cold_restoration",
              "successor_continuity", "handoff", "baton_semantics")},
    {"node_id": "MN-03", "name": "Execution & Authorization",
     "owns": ("execution_protocol", "authorization", "consent", "scope",
              "human_ratification", "fail_closed_execution")},
    {"node_id": "MN-04", "name": "Intelligence Atom",
     "owns": ("intelligent_events", "naya_nodes", "intelligent_blocks",
              "smart_notes", "canonical_identity", "lifecycle")},
    {"node_id": "MN-05", "name": "Provenance, Evidence & Ledger",
     "owns": ("source_lineage", "provenance", "evidence",
              "historical_reconstruction", "smart_ledger", "attribution")},
    {"node_id": "MN-06", "name": "Retrieval, Applicability & Smart Links",
     "owns": ("contextual_retrieval", "applicability", "freshness",
              "relevance", "supersession", "smart_links", "retrieval_evidence")},
    {"node_id": "MN-07", "name": "Verification, Safety & Governed Action",
     "owns": ("causal_verification", "verified_ai_action", "refusal",
              "revocation", "replay", "acceptance", "safety_boundaries")},
    {"node_id": "MN-08", "name": "Learning, Reconciliation & Compounding",
     "owns": ("outcome_learning", "reconciliation", "candidate_learning",
              "promotion", "compounding", "measurable_improvement")},
    {"node_id": "MN-09", "name": "NayaNET Architecture, Hub & Production Proof",
     "owns": ("one_system_architecture", "hub", "interfaces", "deployment",
              "source_build_runtime_parity", "production_proof")},
)

EXPECTED_KERNEL_VERSION = "1.0.0"
EXPECTED_SEQUENCE: tuple[str, ...] = tuple(n["node_id"] for n in MASTER_NODES)

# A node is boot-eligible only in these states (SS25 claims ACTIVE / VERIFIED).
ELIGIBLE_STATUS = frozenset({"ACTIVE", "VERIFIED", "ACTIVE/VERIFIED"})

# SS17: intelligence is temporal. A node older than this is STALE, not usable.
MAX_AGE_DAYS = 180


class KernelIntegrityError(RuntimeError):
    """Raised when a consequential boot is attempted on an unproven kernel."""


@dataclass(frozen=True)
class Finding:
    check: str
    status: str          # PASS | FAIL | UNKNOWN
    detail: str
    evidence: tuple[str, ...] = ()

    @property
    def blocking(self) -> bool:
        return self.status in ("FAIL", "UNKNOWN")


@dataclass
class KernelBootReport:
    conclusive: bool = False
    boot_permitted: bool = False
    authority: str = "NONE"          # SS21/SS30: never granted here.
    source: str = "NONE"
    kernel_version: str = "UNKNOWN"
    loaded: list[str] = field(default_factory=list)
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

    def to_dict(self) -> dict:
        return {
            "schema": "naya.kernel-boot-report/1",
            "conclusive": self.conclusive,
            "boot_permitted": self.boot_permitted,
            "authority": self.authority,
            "source": self.source,
            "kernel_version": self.kernel_version,
            "loaded": list(self.loaded),
            "findings": [
                {"check": f.check, "status": f.status, "detail": f.detail,
                 "evidence": list(f.evidence)}
                for f in self.findings
            ],
            "unresolved": list(self.unresolved),
            "next_action": self.next_action,
        }


# --- sources ----------------------------------------------------------------
# A source returns raw kernel records, or raises. It never returns a default
# kernel: fabricating nodes would be the exact failure this module prevents.

def receiver_source() -> list[dict]:
    """Canonical receiver (Supabase). Requires operator-provisioned credentials.

    Fails closed. We do not embed credentials, read .env files, or accept
    tokens from the environment of an untrusted process.
    """
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
    if not url or not key:
        raise PermissionError(
            "canonical receiver credentials absent "
            "(SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY); "
            "kernel state is UNKNOWN, not empty and not assumed intact"
        )
    raise NotImplementedError(
        "receiver transport is not implemented in-repo; "
        "an authorized operator must supply the transport"
    )


def repo_mirror_source(root: Path | None = None) -> list[dict]:
    """Read a committed canonical kernel mirror, if one exists.

    This exists so kernel integrity is testable and so a future merge of
    receiver-derived state has a deterministic landing format. Absence of the
    mirror is a legitimate UNKNOWN, not a fabricated empty kernel.
    """
    base = (root or REPO) / ".naya/control-plane/MASTER-NODE-KERNEL.json"
    if not base.is_file():
        raise FileNotFoundError(
            f"no canonical kernel mirror at {base.relative_to(root or REPO)}"
        )
    payload = json.loads(base.read_text(encoding="utf-8"))
    nodes = payload.get("nodes")
    if not isinstance(nodes, list):
        raise ValueError("kernel mirror has no 'nodes' list")
    return nodes


# --- SS46 integrity checks --------------------------------------------------

def _check_presence(report: KernelBootReport, nodes: Sequence[dict]) -> None:
    seen = [str(n.get("node_id", "")) for n in nodes]
    report.loaded = [n for n in seen if n]
    missing = [nid for nid in EXPECTED_SEQUENCE if nid not in seen]
    extra = [nid for nid in seen if nid not in EXPECTED_SEQUENCE]
    if missing or extra or len(seen) != len(EXPECTED_SEQUENCE):
        detail = f"expected {len(EXPECTED_SEQUENCE)} nodes {EXPECTED_SEQUENCE}"
        if missing:
            detail += f"; MISSING {missing}"
        if extra:
            detail += f"; UNEXPECTED {extra}"
        if not missing and not extra:
            detail += f"; DUPLICATED ids in {seen}"
        report.add("NODE_PRESENCE", "FAIL", detail, (report.source,))
    else:
        report.add("NODE_PRESENCE", "PASS",
                   f"all {len(EXPECTED_SEQUENCE)} Master Nodes present",
                   (report.source,))


def _check_version(report: KernelBootReport, nodes: Sequence[dict]) -> None:
    versions = {str(n.get("kernel_version", "")) for n in nodes}
    if versions == {EXPECTED_KERNEL_VERSION}:
        report.add("KERNEL_VERSION", "PASS", f"version {EXPECTED_KERNEL_VERSION}")
        return
    report.add("KERNEL_VERSION", "FAIL",
               f"expected {EXPECTED_KERNEL_VERSION}, found {sorted(versions)}")


def _check_status(report: KernelBootReport, nodes: Sequence[dict]) -> None:
    bad = []
    for node in nodes:
        nid = node.get("node_id")
        status = str(node.get("status", "")).upper()
        verified = bool(node.get("verified"))
        if status not in ELIGIBLE_STATUS or not verified:
            bad.append(f"{nid}(status={status or 'ABSENT'},verified={verified})")
    if bad:
        report.add("NODE_STATUS", "FAIL",
                   f"not ACTIVE/VERIFIED: {bad}")
    else:
        report.add("NODE_STATUS", "PASS",
                   f"{len(nodes)} nodes ACTIVE and VERIFIED")


def _check_relationships(report: KernelBootReport, nodes: Sequence[dict]) -> None:
    """SS25/SS8: the nine nodes are linearly related as a semantic sequence."""
    by_id = {str(n.get("node_id")): n for n in nodes}
    problems: list[str] = []
    for idx, nid in enumerate(EXPECTED_SEQUENCE):
        node = by_id.get(nid)
        if node is None:
            continue
        rels = node.get("relationships") or {}
        if not isinstance(rels, dict):
            problems.append(f"{nid}.relationships is not an object")
            continue
        declared_next = rels.get("next")
        if idx == len(EXPECTED_SEQUENCE) - 1:
            if declared_next not in (None, "", "NONE", None):
                problems.append(f"{nid} is terminal but declares next={declared_next!r}")
        else:
            if declared_next != EXPECTED_SEQUENCE[idx + 1]:
                problems.append(
                    f"{nid}.relationships.next={declared_next!r}, "
                    f"expected {EXPECTED_SEQUENCE[idx + 1]!r}")
    if problems:
        report.add("NODE_RELATIONSHIPS", "FAIL", "; ".join(problems))
    else:
        report.add("NODE_RELATIONSHIPS", "PASS",
                   "linear semantic sequence intact MN-01 -> MN-09")


def _check_governance_bindings(report: KernelBootReport,
                               nodes: Sequence[dict]) -> None:
    """SS20: ContractClause <-> Rule <-> Node <-> Code <-> Test."""
    unbound = [
        str(n.get("node_id")) for n in nodes
        if not (n.get("governance_bindings") or [])
    ]
    if unbound:
        report.add("GOVERNANCE_BINDINGS", "FAIL",
                   f"nodes with no contract/rule binding: {unbound}")
    else:
        report.add("GOVERNANCE_BINDINGS", "PASS",
                   "every node bound to at least one governance rule")


def _check_enforcement_coverage(report: KernelBootReport,
                                nodes: Sequence[dict]) -> None:
    """A node that governs but is not machine-enforced is documentation."""
    unenforced = [
        str(n.get("node_id")) for n in nodes
        if (n.get("enforcement_point") in (None, "", "NONE"))
    ]
    if unenforced:
        report.add("ENFORCEMENT_COVERAGE", "FAIL",
                   f"nodes with no deterministic enforcement point: {unenforced}")
    else:
        report.add("ENFORCEMENT_COVERAGE", "PASS",
                   "every node declares a deterministic enforcement point")


def _check_conflicts(report: KernelBootReport, nodes: Sequence[dict]) -> None:
    conflicted = [
        f"{n.get('node_id')}:{c}" for n in nodes
        for c in (n.get("conflicts") or [])
    ]
    if conflicted:
        report.add("NODE_CONFLICTS", "FAIL", f"declared conflicts {conflicted}")
    else:
        report.add("NODE_CONFLICTS", "PASS", "no intra-kernel conflict declared")


def _check_freshness(report: KernelBootReport, nodes: Sequence[dict],
                     now_days: float) -> None:
    """SS17: truth can persist while applicability decays. Stale != broken."""
    from datetime import date, timedelta
    today = date(2026, 9, 26) + timedelta(days=now_days)
    stale: list[str] = []
    unknown_date: list[str] = []
    for node in nodes:
        raw = node.get("observed_at")
        if not raw:
            unknown_date.append(str(node.get("node_id")))
            continue
        try:
            observed = date.fromisoformat(str(raw)[:10])
        except ValueError:
            unknown_date.append(str(node.get("node_id")))
            continue
        if (today - observed).days > MAX_AGE_DAYS:
            stale.append(f"{node.get('node_id')}({(today - observed).days}d)")
    if stale:
        report.add("NODE_FRESHNESS", "FAIL",
                   f"stale beyond {MAX_AGE_DAYS}d: {stale}")
    elif unknown_date:
        report.add("NODE_FRESHNESS", "UNKNOWN",
                   f"no observed_at for {unknown_date}")
    else:
        report.add("NODE_FRESHNESS", "PASS", f"all nodes within {MAX_AGE_DAYS}d")


def _check_next_action(report: KernelBootReport, payload: dict) -> None:
    """SS37/SS38: successor context must name exactly one next action."""
    if not isinstance(payload, dict):
        report.add("NEXT_ACTION", "UNKNOWN", "kernel payload is not an object")
        return
    action = payload.get("next_action")
    if not isinstance(action, str) or not action.strip():
        report.add("NEXT_ACTION", "FAIL", "kernel declares no next_action")
        return
    # SS38 / ONE-NEXT-ACTION LAW: exactly one action. A trailing period is
    # punctuation, not a second action; ". " or ";" or "|" starts another.
    clauses = [c for c in re.split(r"(?:\.\s+|;|\|)", action.strip().rstrip(". "))
               if c.strip()]
    if len(clauses) > 1:
        report.add("NEXT_ACTION", "FAIL",
                   f"next_action must be exactly ONE action, got {len(clauses)}: "
                   f"{[c.strip() for c in clauses]}")
        return
    report.add("NEXT_ACTION", "PASS", action[:160], ("payload.next_action",))
    report.next_action = action.strip()


# --- entrypoint -------------------------------------------------------------

def boot_kernel(
    source: Callable[[], Sequence[dict]] | None = None,
    payload: dict | None = None,
    now_days: float = 0.0,
) -> KernelBootReport:
    """Attempt a consequential kernel boot. Fails closed.

    Returns a report whose ``boot_permitted`` is True only when every SS46
    check passed on real retrieved evidence. Never grants authority (SS21).
    """
    report = KernelBootReport()
    getter = source or receiver_source
    report.source = getattr(getter, "__name__", "anonymous")

    try:
        raw = getter()
    except Exception as exc:
        # UNKNOWN, never PASS and never an empty-but-healthy kernel.
        report.add("KERNEL_SOURCE", "UNKNOWN",
                   f"{type(exc).__name__}: {exc}")
        report.unresolved.append("canonical kernel state is unproven")
        report.next_action = (
            "Provision canonical receiver access (SUPABASE_URL + "
            "SUPABASE_SERVICE_ROLE_KEY) via an authorized operator, then re-run "
            "kernel_boot.boot_kernel(); do not proceed with a consequential "
            "action on an unproven kernel."
        )
        report.conclusive = True          # we conclusively know we cannot boot
        report.boot_permitted = False
        return report

    nodes = [n for n in raw if isinstance(n, dict)]
    report.add("KERNEL_SOURCE", "PASS",
               f"retrieved {len(nodes)} raw node records")

    _check_presence(report, nodes)
    _check_version(report, nodes)
    _check_status(report, nodes)
    _check_relationships(report, nodes)
    _check_governance_bindings(report, nodes)
    _check_enforcement_coverage(report, nodes)
    _check_conflicts(report, nodes)
    _check_freshness(report, nodes, now_days)
    _check_next_action(report, payload if payload is not None else {})

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
        raise KernelIntegrityError(
            "kernel integrity not proven; boot refused. "
            f"source={report.source} blocking={report.unresolved}"
        )


def main(argv: Sequence[str] | None = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description="Fail-closed nine-node kernel boot")
    ap.add_argument("--source", choices=("receiver", "repo-mirror"),
                    default="receiver")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    getter = receiver_source if args.source == "receiver" else repo_mirror_source
    report = boot_kernel(getter)
    if args.json:
        print(json.dumps(report.to_dict(), indent=2, sort_keys=True))
    else:
        print("=" * 72)
        print("NAYAPOWER PHASE 2 BOOT - NINE MASTER NODE KERNEL INTEGRITY")
        print("=" * 72)
        print(f"source          : {report.source}")
        print(f"kernel version  : {report.kernel_version}")
        print(f"nodes loaded    : {len(report.loaded)}/{len(EXPECTED_SEQUENCE)}")
        print(f"conclusive      : {report.conclusive}")
        print(f"BOOT PERMITTED  : {report.boot_permitted}")
        print(f"authority       : {report.authority}  (loading confers none)")
        print("-" * 72)
        for f in report.findings:
            print(f"[{f.status:7}] {f.check:22} {f.detail}")
        print("-" * 72)
        print(f"next action: {report.next_action}")
    return 0 if report.boot_permitted else 1


if __name__ == "__main__":
    raise SystemExit(main())
