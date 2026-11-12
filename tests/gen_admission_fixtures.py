"""Generate shared parity fixtures: (name, input) -> Python reference verdict."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from learning_admission_gate import ADMISSION_SCHEMA, admit_candidate
from test_learning_admission_gate import valid_candidate


def vc(**overrides):
    return valid_candidate(**overrides)


CASES = [
    ("valid", vc()),
    ("schema_mismatch", vc(schema="WRONG")),
    ("missing_falsification", vc(falsification_condition="")),
    ("no_named_task", vc(task="")),
    ("criterion_not_independent", vc(criterion_independent_of_lesson=False)),
    ("no_criterion", vc(success_criterion="")),
    ("heuristic_measurement", vc(measurement={"method": "vibes", "detail": "felt right"})),
    ("method_machine", vc(measurement={"method": "machine"})),
    ("method_different_seat", vc(measurement={"method": "different_seat"})),
    ("method_deterministic", vc(measurement={"method": "deterministic"})),
    ("doer_equals_scorer", vc(doer="naya-5", scorer="naya-5")),
    ("tautological_arms", vc(arms={
        "treatment": {"observable": "", "measured_at": "2026-10-09T10:00:00Z"},
        "control": {"observable": "", "measured_at": "2026-10-09T10:05:00Z"},
    })),
    ("indistinguishable_arms", vc(arms={
        "treatment": {"observable": "does the thing", "measured_at": "2026-10-09T10:00:00Z"},
        "control": {"observable": "does the thing", "measured_at": "2026-10-09T10:05:00Z"},
    })),
    ("non_experiment_unmeasured", vc(arms={
        "treatment": {"observable": "retries writes", "measured_at": ""},
        "control": {"observable": "no retry", "measured_at": ""},
    })),
    ("null_false_flag", vc(asserts_behavioral_change=False)),
    ("null_without_arms_rejected", vc(
        asserts_behavioral_change=False,
        arms={
            "treatment": {"observable": "retries writes", "measured_at": ""},
            "control": {"observable": "no retry", "measured_at": ""},
        },
    )),
    ("honest_null_outcome", vc(outcome="null")),
    ("chain_test_artifact", {
        "schema": ADMISSION_SCHEMA,
        "claim": "Almost there",
        "provenance": "USER",
        "verification_method": "PENDING_OUTCOME_VERIFICATION",
    }),
    ("non_object", "just a string"),
    ("b1b_costumed_tautology", vc(
        claim="Applying the lesson changes behavior.",
        falsification_condition="if applying the lesson did not change behavior",
    )),
    ("b1b_costumed_criterion", vc(
        claim="Applying the lesson changes behavior.",
        success_criterion="The claim is wrong if applying the lesson does not change behavior.",
    )),
    ("b5_post_hoc", vc(criterion_registered_at="2026-10-09T11:00:00Z")),
    ("b5_missing_registered_at", vc(criterion_registered_at="")),
    ("b5_unparseable_registered_at", vc(criterion_registered_at="sometime yesterday")),
    ("b5_unparseable_measured_at", vc(arms={
        "treatment": {"observable": "retries writes", "measured_at": "yesterday"},
        "control": {"observable": "no retry", "measured_at": "2026-10-09T10:05:00Z"},
    })),
    ("b5_null_with_post_hoc", vc(outcome="null", criterion_registered_at="2026-10-09T11:00:00Z")),
    ("b2b_null_string", vc(outcome="null")),
    ("b2b_null_case_insensitive", vc(outcome="NULL", asserts_behavioral_change=False)),
    ("b6b_case_variant", vc(doer="Naya-5", scorer="naya-5 ")),
    ("b6b_distinct_seats", vc(doer="Naya-5", scorer="NAYA-2")),
    ("missing_claim", vc(claim="")),
    ("null_arms", vc(arms=None)),
    ("empty_dict", {}),
    ("null_input", None),
    ("list_input", [1, 2, 3]),
    # Edge: naive timestamps (assumed UTC), boundary equality on registration
    ("naive_timestamps", vc(
        criterion_registered_at="2026-10-09T09:00:00",
        arms={
            "treatment": {"observable": "retries each failed write up to 3x with backoff", "measured_at": "2026-10-09T10:00:00"},
            "control": {"observable": "fails the write immediately, no retry", "measured_at": "2026-10-09T10:05:00"},
        },
    )),
    ("registered_exactly_at_first_measured", vc(criterion_registered_at="2026-10-09T10:00:00Z")),
    # Near-miss paraphrase (should NOT trip the 0.75 threshold)
    ("unrelated_falsification", vc(
        falsification_condition="If the database disk fills up, writes fail regardless of retry logic.",
    )),
]

out = []
for name, inp in CASES:
    r = admit_candidate(inp)
    out.append({
        "name": name,
        "input": inp,
        "expected": {
            "admitted": r.admitted,
            "admitted_as": r.admitted_as,
            "reasons": list(r.reasons),
        },
    })

dest = Path(__file__).resolve().parent / "admission_gate_fixtures.json"
dest.write_text(json.dumps(out, indent=2), encoding="utf-8")
print(f"wrote {len(out)} fixtures to {dest}")
