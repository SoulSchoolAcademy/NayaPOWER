"""Shared node interface for the nine-node kernel (CANDIDATE — NOT RATIFIED).

Every kernel node module MUST subclass NodeBase and implement every method.
Small and strict by design: the interface is the contract surface the
overnight build loop will fill in per the ratified spec of each node.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List


class GateVerdict(str, Enum):
    """Four-valued gate outcomes collapse to PASS / FAIL / NEED_EVIDENCE here.

    NEED_EVIDENCE is the mechanical form of "not yet proven": a gate that
    cannot reach PASS on the evidence in `state` must not silently become
    PASS. (UNKNOWN, BLOCKED, IMPLEMENTED never count as VERIFIED.)
    """

    PASS = "PASS"
    FAIL = "FAIL"
    NEED_EVIDENCE = "NEED_EVIDENCE"


@dataclass
class GateResult:
    verdict: GateVerdict
    reasons: List[str] = field(default_factory=list)


@dataclass
class ManifestEntry:
    node_id: str
    version: str
    responsibilities: List[str]


# ---------------------------------------------------------------------------
# Ratified Decision Value Calculus V2.1 binding (FLAG-001 step 4).
#
# V2.1 was ratified 2026-09-30 by the Human Director (PR #1186 82793cc,
# PR #1190 ade50c06, PR #1192 79b29496 — verified against live main). The
# binding identifies the ratified artifacts by git blob SHA at main
# a726a837, so any verifier with the repo can re-derive the exact content:
#   git cat-file -p bc9edc9092436481be7255c00f099d69bd2a95e7  # spec
#   git cat-file -p cac79b6595ca651d8a110b71f25fff9fe50e67bc  # executable
# LEARN/EVOLVE receipts and CONNECT's calculus posture bind
# CALCULUS_V21_SPEC_HASH as the ratified V2.1 config hash. The kernel
# modules remain CANDIDATE code; the calculus they bind is RATIFIED law.
# ---------------------------------------------------------------------------
CALCULUS_V21_VERSION = "V2.1"
CALCULUS_V21_SPEC_HASH = "bc9edc9092436481be7255c00f099d69bd2a95e7"
CALCULUS_V21_EXECUTABLE_HASH = "cac79b6595ca651d8a110b71f25fff9fe50e67bc"
CALCULUS_V21_RATIFIED_AT_MAIN = "a726a837"


class NodeBase(ABC):
    """Strict interface every kernel node must implement."""

    @abstractmethod
    def manifest_entry(self) -> ManifestEntry:
        """Return (node_id, version, responsibilities) for the node manifest."""
        raise NotImplementedError

    @abstractmethod
    def gate(self, state: Dict[str, Any]) -> GateResult:
        """Evaluate this node's gate on `state`; never invent PASS."""
        raise NotImplementedError

    @abstractmethod
    def persisted_transitions(self) -> List[str]:
        """Name every state transition this node persists (receipted)."""
        raise NotImplementedError

    @abstractmethod
    def evidence_hooks(self) -> List[str]:
        """Name the evidence sources this node reads/writes."""
        raise NotImplementedError

    @abstractmethod
    def authority_checks(self) -> List[str]:
        """Name the authority validations this node performs before acting."""
        raise NotImplementedError

    @abstractmethod
    def cold_reconstruct(self, receipts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Rebuild this node's durable state from receipts alone (cold start)."""
        raise NotImplementedError
