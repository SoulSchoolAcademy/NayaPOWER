import importlib.util, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("selector", ROOT/"tools"/"validate_graph_selector_v2.py")
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
FIXTURE=json.loads((ROOT/"BRAIN/04-INTELLIGENCE/GRAPH/0004-GRAPH-SELECTOR-V2-ACCEPTANCE.json").read_text(encoding="utf-8"))
TASK=FIXTURE["task"]; TYPES=FIXTURE["allowed_relationship_types"]

def case(name):
    return next(x for x in FIXTURE["cases"] if x["name"]==name)

def test_all_predeclared_selector_cases_match():
    for c in FIXTURE["cases"]:
        selected, reason=mod.evaluate(c["edge"], TASK, TYPES)
        assert selected is c["expect_selected"], c["name"]
        if "expect_reason" in c:
            assert reason == c["expect_reason"], c["name"]

def test_expired_fails_closed():
    assert mod.evaluate(case("expired_edge")["edge"], TASK, TYPES) == (False,"TEMPORALLY_INVALID")

def test_superseded_fails_closed():
    assert mod.evaluate(case("superseded_edge")["edge"], TASK, TYPES) == (False,"STATUS_NOT_ACTIVE")

def test_missing_consent_fails_closed():
    assert mod.evaluate(case("shared_without_consent")["edge"], TASK, TYPES) == (False,"CONSENT_REQUIRED")

def test_unknown_applicability_fails_closed():
    assert mod.evaluate(case("unknown_applicability")["edge"], TASK, TYPES) == (False,"APPLICABILITY_UNKNOWN")

def test_unrelated_task_fails_closed():
    assert mod.evaluate(case("unrelated_task_class")["edge"], TASK, TYPES) == (False,"TASK_CLASS_MISMATCH")

def test_valid_edge_is_selected():
    assert mod.evaluate(case("valid_private_applicable")["edge"], TASK, TYPES) == (True,"SELECTED")
