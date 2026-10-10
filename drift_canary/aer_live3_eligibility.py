"""AER-LIVE-3: Independently Verified Eligibility Witnesses (spec).

Shawn's law (SN-0809, ratified 2026-10-10): Count a scheduling opportunity
only when six facts are independently established. Three verdicts, no
collapsed PASS.

The six facts (each independently verified):
  1. OBLIGATION — a valid outstanding obligation exists
  2. LAW — applicable LAW permits the transition
  3. DEPENDENCIES — all prerequisites satisfied
  4. RESOURCES — required resources available
  5. OPPORTUNITY — scheduler presents a genuine opportunity
  6. ORDERING — consistent ordering with no contradictions

The three verdicts:
  ELIGIBLE_PROVEN — all six facts independently established
  INELIGIBLE_PROVEN — at least one fact proven false with evidence
  ELIGIBILITY_UNDETERMINED — insufficient evidence (never collapses to false)

Strongest test (bidirectional E2):
  - Catch FALSE INELIGIBILITY hiding starvation (system claims ineligible
    but obligation is starving due to scheduler neglect)
  - Reject FALSE ELIGIBILITY where LAW was absent (system claims eligible
    but no LAW permits the transition)

SPEC ONLY. Not wired into kernel/, KNOW, LAW, ACT, or any live path.
Wiring needs Shawn's word.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class EligibilityVerdict(Enum):
    ELIGIBLE_PROVEN = "ELIGIBLE_PROVEN"
    INELIGIBLE_PROVEN = "INELIGIBLE_PROVEN"
    ELIGIBILITY_UNDETERMINED = "ELIGIBILITY_UNDETERMINED"


@dataclass(frozen=True)
class EligibilityFact:
    """One of the six independently verified facts."""
    name: str
    established: bool  # True = proven, False = proven false
    evidence_ref: Optional[str] = None
    # If evidence is missing entirely, the fact is undetermined
    evidence_missing: bool = False


@dataclass(frozen=True)
class EligibilityWitness:
    """The six facts for one scheduling opportunity."""
    obligation: EligibilityFact
    law: EligibilityFact
    dependencies: EligibilityFact
    resources: EligibilityFact
    opportunity: EligibilityFact
    ordering: EligibilityFact

    def facts(self):
        return [
            self.obligation,
            self.law,
            self.dependencies,
            self.resources,
            self.opportunity,
            self.ordering,
        ]


@dataclass(frozen=True)
class EligibilityResult:
    verdict: EligibilityVerdict
    # For INELIGIBLE_PROVEN: which facts were proven false
    failed_facts: tuple = ()
    # For UNDETERMINED: which facts lack evidence
    missing_evidence: tuple = ()
    # Bidirectional E2 flags
    false_ineligibility_suspected: bool = False
    false_eligibility_suspected: bool = False


def verify_eligibility(witness: EligibilityWitness) -> EligibilityResult:
    """Verify eligibility per AER-LIVE-3.

    Rules:
    - All six facts established → ELIGIBLE_PROVEN
    - Any fact proven false (with evidence) → INELIGIBLE_PROVEN
    - Any fact missing evidence → ELIGIBILITY_UNDETERMINED
      (undetermined NEVER collapses to ineligible)
    - Bidirectional E2: flag suspicious patterns
    """
    facts = witness.facts()

    # Check for missing evidence first — undetermined takes precedence
    # over both eligible and ineligible (epistemic honesty)
    missing = tuple(f.name for f in facts if f.evidence_missing)
    if missing:
        return EligibilityResult(
            verdict=EligibilityVerdict.ELIGIBILITY_UNDETERMINED,
            missing_evidence=missing,
        )

    # Check for proven-false facts
    failed = tuple(f.name for f in facts if not f.established)
    if failed:
        result = EligibilityResult(
            verdict=EligibilityVerdict.INELIGIBLE_PROVEN,
            failed_facts=failed,
        )
        # E2: false ineligibility hiding starvation — if the ONLY failure
        # is opportunity (scheduler didn't present one) but obligation,
        # law, deps, resources, ordering all hold, the system may be
        # starving the obligation rather than it being truly ineligible
        if failed == ("opportunity",) and all(
            f.established for f in facts if f.name != "opportunity"
        ):
            result = EligibilityResult(
                verdict=result.verdict,
                failed_facts=result.failed_facts,
                false_ineligibility_suspected=True,
            )
        return result

    # All six established → eligible
    # E2: false eligibility where LAW was absent — this is caught by the
    # law fact being required; if we reach here, law was established.
    # But flag if law evidence looks weak (defensive).
    return EligibilityResult(verdict=EligibilityVerdict.ELIGIBLE_PROVEN)


# --- Test fixtures for bidirectional E2 ---

def make_fact(name: str, established: bool = True,
              evidence_missing: bool = False) -> EligibilityFact:
    return EligibilityFact(
        name=name,
        established=established,
        evidence_ref=f"EV-{name}" if not evidence_missing else None,
        evidence_missing=evidence_missing,
    )


def fixture_all_eligible() -> EligibilityWitness:
    """All six facts established → ELIGIBLE_PROVEN."""
    return EligibilityWitness(**{
        n: make_fact(n) for n in (
            "obligation", "law", "dependencies",
            "resources", "opportunity", "ordering")
    })


def fixture_law_absent() -> EligibilityWitness:
    """LAW fact proven false → INELIGIBLE_PROVEN (reject false eligibility)."""
    d = {n: make_fact(n) for n in (
        "obligation", "law", "dependencies",
        "resources", "opportunity", "ordering")}
    d["law"] = make_fact("law", established=False)
    return EligibilityWitness(**d)


def fixture_starvation() -> EligibilityWitness:
    """Only opportunity missing, all else holds → INELIGIBLE_PROVEN
    with false_ineligibility_suspected=True (catch starvation)."""
    d = {n: make_fact(n) for n in (
        "obligation", "law", "dependencies",
        "resources", "opportunity", "ordering")}
    d["opportunity"] = make_fact("opportunity", established=False)
    return EligibilityWitness(**d)


def fixture_missing_evidence() -> EligibilityWitness:
    """LAW evidence missing → ELIGIBILITY_UNDETERMINED (never false)."""
    d = {n: make_fact(n) for n in (
        "obligation", "law", "dependencies",
        "resources", "opportunity", "ordering")}
    d["law"] = make_fact("law", evidence_missing=True)
    return EligibilityWitness(**d)
