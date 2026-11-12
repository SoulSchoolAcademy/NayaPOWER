#!/usr/bin/env python3
"""Tests for tools/mechanism_registry.py — the wiring guard.

Negative controls are the point: a gate tool that nothing in the tree
invokes MUST come back UNWIRED (the #1627 lesson — merged bytes with
zero call sites are not enforcement), a drifted committed registry
MUST fail --check, and a workflow-invoked tool MUST come back wired.
If the registry were mutated to call everything wired, the UNWIRED
tests below fail.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import mechanism_registry as mr


def write(root, rel, text):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


TOOL = '"""Guards the demo thing."""\nprint("ok")\n'


def fixture(root):
    # A gate tool invoked by a workflow, and a check tool invoked by nobody.
    write(root, "tools/activation_gate.py", TOOL)
    write(root, "tools/check_lonely.py", TOOL)
    write(root, ".github/workflows/demo-gate.yml",
          "name: Demo Gate\non:\n  pull_request:\n    branches: [main]\njobs:\n"
          "  gate:\n    runs-on: ubuntu-latest\n    steps:\n"
          "      - run: python3 tools/activation_gate.py\n")


def by_file(registry):
    return {r["owner_file"]: r for r in registry["mechanisms"]}


def test_workflow_invoked_tool_is_wired(tmp_path):
    root = str(tmp_path)
    fixture(root)
    recs = by_file(mr.build_registry(root))
    assert recs["tools/activation_gate.py"]["wired"] is True
    assert ".github/workflows/demo-gate.yml" in \
        recs["tools/activation_gate.py"]["call_sites"]


def test_uninvoked_tool_is_unwired(tmp_path):
    root = str(tmp_path)
    fixture(root)
    registry = mr.build_registry(root)
    recs = by_file(registry)
    assert recs["tools/check_lonely.py"]["wired"] is False
    assert registry["summary"]["unwired"] >= 1
    assert "tools/check_lonely.py" in registry["summary"]["unwired_files"]


def test_workflow_record_carries_triggers(tmp_path):
    root = str(tmp_path)
    fixture(root)
    recs = by_file(mr.build_registry(root))
    wf = recs[".github/workflows/demo-gate.yml"]
    assert wf["kind"] == "workflow"
    assert wf["wired"] is True
    assert "on: pull_request" in wf["call_sites"]


def test_docstring_is_the_guards_line(tmp_path):
    root = str(tmp_path)
    fixture(root)
    recs = by_file(mr.build_registry(root))
    assert recs["tools/check_lonely.py"]["guards"] == "Guards the demo thing."


def test_doc_mention_is_not_a_call_site(tmp_path):
    root = str(tmp_path)
    fixture(root)
    write(root, "NOTES.md", "see tools/check_lonely.py for details\n")
    recs = by_file(mr.build_registry(root))
    assert recs["tools/check_lonely.py"]["wired"] is False
    assert "NOTES.md" in recs["tools/check_lonely.py"]["doc_refs"]


def test_own_test_reference_is_not_wiring(tmp_path):
    # The #1627 lesson: a gate only its own test invokes is NOT enforced.
    root = str(tmp_path)
    fixture(root)
    write(root, "tools/test_check_lonely.py",
          "import check_lonely\ncheck_lonely.main()\n")
    recs = by_file(mr.build_registry(root))
    rec = recs["tools/check_lonely.py"]
    assert rec["wired"] is False
    assert rec["call_sites"] == []
    assert "tools/test_check_lonely.py" in rec["test_refs"]


def test_check_mode_passes_then_detects_drift(tmp_path):
    root = str(tmp_path)
    fixture(root)
    assert mr.main(["--root", root, "--write"]) == 0
    assert mr.main(["--root", root, "--check"]) == 0
    write(root, "tools/check_newcomer.py", TOOL)  # tree moved, registry didn't
    assert mr.main(["--root", root, "--check"]) == 1


def test_written_registry_is_valid_json_with_summary(tmp_path):
    root = str(tmp_path)
    fixture(root)
    assert mr.main(["--root", root, "--write"]) == 0
    data = json.load(open(os.path.join(root, mr.REGISTRY_REL), encoding="utf-8"))
    assert data["schema"] == mr.SCHEMA
    assert data["summary"]["total"] == len(data["mechanisms"]) >= 3
