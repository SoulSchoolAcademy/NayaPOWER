import importlib.util, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("rec",ROOT/"tools"/"validate_graph_reconciliation_v2.py")
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
DATA=json.loads((ROOT/"BRAIN/04-INTELLIGENCE/GRAPH/0005-GRAPH-RECONCILIATION-V2-ACCEPTANCE.json").read_text(encoding="utf-8"))

def case(name):
    return next(x for x in DATA["cases"] if x["name"]==name)

def test_all_reconciliation_cases_match_predeclared_expectations():
    for c in DATA["cases"]:
        got=mod.reconcile(c["edges"],c["task_class"])
        assert got["status"]==c["expect_status"],c["name"]
        assert sorted(got["selected"])==sorted(c["expect_selected"]),c["name"]
        assert sorted(got["excluded"])==sorted(c["expect_excluded"]),c["name"]

def test_unresolved_contradiction_is_not_silently_ranked():
    c=case("unresolved_current_contradiction_surfaces_conflict")
    assert mod.reconcile(c["edges"],c["task_class"])["status"]=="UNRESOLVED_CONFLICT"

def test_expired_edge_is_excluded():
    c=case("expired_edge_excluded")
    got=mod.reconcile(c["edges"],c["task_class"])
    assert "REL-EXPIRED" in got["excluded"]
    assert "REL-CURRENT" in got["selected"]

def test_superseded_edge_is_excluded_but_new_edge_survives():
    c=case("superseding_edge_wins_current_without_deleting_history")
    got=mod.reconcile(c["edges"],c["task_class"])
    assert got["selected"]==["REL-NEW"]
    assert "REL-OLD" in got["excluded"]

def test_unrelated_task_has_no_transfer():
    c=case("unrelated_arithmetic_refuses_graph_transfer")
    got=mod.reconcile(c["edges"],c["task_class"])
    assert got["status"]=="NO_APPLICABLE_CONTEXT"
    assert got["selected"]==[]

def test_five_task_classes_are_predeclared():
    assert DATA["task_classes"]==[
        "provenance_sensitive","repository_correction","learning_reuse","conflict_resolution","contextual_retrieval"
    ]
