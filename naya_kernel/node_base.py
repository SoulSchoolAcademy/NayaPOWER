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
