"""AER-LIVE-9: Dependency-Ordered Invariant Verification (spec).

Shawn's law (SN-0815, ratified 2026-10-10): Verify prerequisites in
dependency order. Diagnose failures in causal execution order. Preserve
three-valued results: true, false, undetermined. Minimized
counterexamples must remain reachable and executable under the original
model.

Key distinctions:
- Verification order: topological (prerequisites first)
- Diagnosis order: causal (what actually failed first in execution)
- These are DIFFERENT. Do not conflate.

Three-valued logic:
- TRUE: proven
- FALSE: proven false with reachable counterexample
- UNDETERMINED: insufficient evidence (never collapses to FALSE)

F1 vs F6 honesty gate:
- F1: LAW expiry proven → minimal counterexample with expiry
- F6: LAW timing evidence missing → UNDETERMINED, no fabricated counterexample

SPEC ONLY. Not wired into kernel/, KNOW, LAW, ACT, or any live path.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class TriValue(Enum):
    TRUE = "TRUE"
    FALSE = "FALSE"
    UNDETERMINED = "UNDETERMINED"


@dataclass(frozen=True)
class Invariant:
    name: str
    # Names of invariants that must be verified before this one
    prerequisites: tuple = ()
    value: TriValue = TriValue.UNDETERMINED
    # For FALSE: reachable counterexample
    counterexample: Optional[str] = None


def topological_order(invariants: list) -> list:
    """Order invariants so prerequisites come first.

    Simple topological sort. Assumes no cycles (cycles handled by
    AER-LIVE-10 SCC logic, not here).
    """
    by_name = {inv.name: inv for inv in invariants}
    visited = set()
    order = []

    def visit(name):
        if name in visited:
            return
        visited.add(name)
        inv = by_name[name]
        for pre in inv.prerequisites:
            visit(pre)
        order.append(name)

    for inv in invariants:
        visit(inv.name)
    return order


@dataclass(frozen=True)
class Diagnosis:
    """Causal diagnosis (different from verification order)."""
    primary_failure: str  # the actual first failure in execution order
    dependent_failures: tuple = ()
    counterexample_reachable: bool = True


def diagnose_causal(invariants: list,
                    execution_order: list) -> Optional[Diagnosis]:
    """Diagnose in causal execution order, not verification order.

    Finds the earliest failure in execution order, then identifies
    which other failures are dependent consequences vs independent.
    """
    by_name = {inv.name: inv for inv in invariants}
    # Find earliest FALSE in execution order
    for name in execution_order:
        inv = by_name.get(name)
        if inv and inv.value == TriValue.FALSE:
            # Collect dependent failures (those listing this as prerequisite)
            dependents = tuple(
                i.name for i in invariants
                if name in i.prerequisites and i.value == TriValue.FALSE
            )
            return Diagnosis(
                primary_failure=name,
                dependent_failures=dependents,
                counterexample_reachable=inv.counterexample is not None,
            )
    return None


# F1 vs F6 honesty gate
def f1_law_expiry_proven() -> Diagnosis:
    """F1: LAW expiry proven → minimal counterexample."""
    invs = [
        Invariant("temporal", (), TriValue.FALSE, "TIME-11: LAW expired"),
        Invariant("authority", ("temporal",), TriValue.FALSE, None),
    ]
    # Authority failed BECAUSE temporal failed (dependent)
    d = diagnose_causal(invs, ["temporal", "authority"])
    assert d.primary_failure == "temporal"
    assert "authority" in d.dependent_failures
    return d


def f6_law_timing_missing() -> TriValue:
    """F6: LAW timing evidence missing → UNDETERMINED, no fabrication."""
    inv = Invariant("temporal", (), TriValue.UNDETERMINED, None)
    # Must NOT produce a counterexample
    assert inv.counterexample is None
    return inv.value
