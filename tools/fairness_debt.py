#!/usr/bin/env python3
"""Fairness debt ledger — Group 5 (Fairness & Liveness), D58-D65.

D26 Link 2: FAIR SERVICE — "Given the opportunity, was service fair?"
When an eligible work item is not serviced in a window where it had
opportunity, fairness debt accrues. Debt is bounded: a continuously eligible
item must be serviced within the bound (weak fairness). When evidence is
missing for a window, the bound WIDENS by a documented rule instead of
pretending the window was clean — unknown evidence never becomes a PASS.

If debt exceeds the (possibly widened) bound, the ledger produces a WITNESS:
the specific item, the specific window range, the accrued debt, and the bound.
A witness is falsifiable evidence, not a vibe.

Every output carries one of D26's four explicit verdict levels.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set

from fairness_eligibility import VERDICT_LEVELS

# Bound-widening rule: each window with missing evidence doubles the bound
# for items in that window. The rule is multiplicative and documented here so
# a reviewer can reproduce the widening by hand. Rationale: one missing window
# means we cannot prove the item was unserved OR served; doubling (not
# dropping) the bound is the conservative direction — it delays the violation
# verdict rather than manufacturing one from ignorance.
MISSING_EVIDENCE_WIDEN_FACTOR = 2


@dataclass
class DebtWitness:
    """Falsifiable evidence that a fairness bound was violated."""
    item_id: str
    window_start: str
    window_end: str
    debt: int
    bound: int
    widenings: int  # how many missing-evidence windows widened the bound
    verdict_level: str = "MODEL_CHECK_PASSED_IN_SCOPE"

    def __post_init__(self) -> None:
        if self.verdict_level not in VERDICT_LEVELS:
            raise ValueError(f"invalid verdict level: {self.verdict_level!r}")

    def describe(self) -> str:
        return (
            f"FAIRNESS DEBT VIOLATION: item {self.item_id!r} accrued debt "
            f"{self.debt} over windows [{self.window_start}..{self.window_end}], "
            f"exceeding bound {self.bound} "
            f"({self.widenings} missing-evidence widenings applied). "
            f"[{self.verdict_level}]"
        )


@dataclass
class DebtStatus:
    item_id: str
    debt: int
    bound: int
    widenings: int
    violated: bool
    witness: Optional[DebtWitness]
    verdict_level: str

    def __post_init__(self) -> None:
        if self.verdict_level not in VERDICT_LEVELS:
            raise ValueError(f"invalid verdict level: {self.verdict_level!r}")


class FairnessDebtLedger:
    """Tracks per-item fairness debt across scheduling windows.

    Protocol per window:
      record_window(window_id, eligible, serviced, evidence_present=True)
    - eligible: item ids independently proven eligible this window
    - serviced: item ids actually serviced this window
    - evidence_present: False when the window log is missing/incomplete

    Debt rule: eligible and not serviced -> debt += 1. Serviced -> debt = 0.
    Bound rule: base_bound per item; each missing-evidence window multiplies
    the bound by MISSING_EVIDENCE_WIDEN_FACTOR for items in that window.
    """

    def __init__(self, base_bound: int = 3) -> None:
        if base_bound < 1:
            raise ValueError("base_bound must be >= 1")
        self.base_bound = base_bound
        self._debt: Dict[str, int] = {}
        self._widenings: Dict[str, int] = {}
        self._window_log: List[Dict] = []
        self._violation_windows: Dict[str, List[str]] = {}

    def record_window(
        self,
        window_id: str,
        eligible: Set[str],
        serviced: Set[str],
        evidence_present: bool = True,
    ) -> None:
        entry = {
            "window_id": window_id,
            "eligible": sorted(eligible),
            "serviced": sorted(serviced),
            "evidence_present": evidence_present,
        }
        self._window_log.append(entry)
        for item in eligible:
            self._debt.setdefault(item, 0)
            self._widenings.setdefault(item, 0)
            if not evidence_present:
                # Missing evidence: widen the bound, do NOT accrue debt we
                # cannot prove. Unknown is unknown, not a violation.
                self._widenings[item] += 1
                continue
            if item in serviced:
                self._debt[item] = 0
                self._violation_windows.pop(item, None)
            else:
                self._debt[item] += 1
                self._violation_windows.setdefault(item, []).append(window_id)

    def bound_for(self, item_id: str) -> int:
        widenings = self._widenings.get(item_id, 0)
        return self.base_bound * (MISSING_EVIDENCE_WIDEN_FACTOR ** widenings)

    def check(self, item_id: str) -> DebtStatus:
        debt = self._debt.get(item_id, 0)
        bound = self.bound_for(item_id)
        widenings = self._widenings.get(item_id, 0)
        violated = debt > bound
        witness: Optional[DebtWitness] = None
        if violated:
            windows = self._violation_windows.get(item_id, [])
            witness = DebtWitness(
                item_id=item_id,
                window_start=windows[0] if windows else "<unknown>",
                window_end=windows[-1] if windows else "<unknown>",
                debt=debt,
                bound=bound,
                widenings=widenings,
            )
        # Level: the ledger is a model over recorded windows. When any window
        # lacked evidence, the verdict is qualified by that assumption.
        level = (
            "FAIRNESS_QUALIFIED_WITH_ASSUMPTIONS"
            if widenings > 0
            else "MODEL_CHECK_PASSED_IN_SCOPE"
        )
        return DebtStatus(
            item_id=item_id,
            debt=debt,
            bound=bound,
            widenings=widenings,
            violated=violated,
            witness=witness,
            verdict_level=level,
        )

    def check_all(self) -> List[DebtStatus]:
        return [self.check(item) for item in sorted(self._debt)]

    def violations(self) -> List[DebtWitness]:
        out = []
        for item in self._debt:
            st = self.check(item)
            if st.violated and st.witness:
                out.append(st.witness)
        return out

    def window_count(self) -> int:
        return len(self._window_log)
