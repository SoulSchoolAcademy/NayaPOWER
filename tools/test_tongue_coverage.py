#!/usr/bin/env python3
"""Tests for tools/check_tongue_coverage.py — the three-tongue guard.

Negative controls are the point: a human-only fixture MUST be flagged,
a malformed machine tongue MUST come back INVALID (never MISSING —
the file exists, machines just can't read it), and a triplet-complete
fixture MUST pass clean. If the checker were mutated to always pass,
the flagging tests below fail.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import check_tongue_coverage as tc


def gov(root, name, text="x"):
    d = os.path.join(root, "BRAIN", "01-GOVERNANCE")
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, name), "w", encoding="utf-8") as fh:
        fh.write(text)


def triplet(root, stem="0001-DEMO-LAW-V1"):
    gov(root, f"{stem}.human.md")
    gov(root, f"{stem}.ai.md")
    gov(root, f"{stem.lower()}.machine.json", "{}")


def test_complete_triplet_passes(tmp_path):
    root = str(tmp_path)
    triplet(root)
    report = tc.audit(root)
    assert report["works_total"] == 1
    assert report["works_complete"] == 1
    assert report["gaps"] == []
    assert report["invalid"] == []
    assert tc.main(["--root", root]) == 0


def test_human_only_work_is_flagged(tmp_path):
    root = str(tmp_path)
    gov(root, "0002-HUMAN-ONLY-V1.md")
    report = tc.audit(root)
    assert report["works_complete"] == 0
    missing = {(g["work"], g["missing_tongue"]) for g in report["gaps"]}
    assert ("BRAIN/01-GOVERNANCE/0002-human-only-v1", "ai") in missing
    assert ("BRAIN/01-GOVERNANCE/0002-human-only-v1", "machine") in missing
    assert tc.main(["--root", root]) == 1
    lines = tc.defect_lines(report)
    assert all(l.startswith("MISSING: ") and " — CURE: " in l and "(owner: " in l
               for l in lines)


def test_malformed_machine_json_is_invalid_not_missing(tmp_path):
    root = str(tmp_path)
    gov(root, "0003-BROKEN-V1.human.md")
    gov(root, "0003-BROKEN-V1.ai.md")
    gov(root, "0003-broken-v1.machine.json", "{not json")
    report = tc.audit(root)
    assert len(report["invalid"]) == 1
    assert report["invalid"][0]["path"].endswith("0003-broken-v1.machine.json")
    # The machine tongue exists, so it must NOT also be reported missing.
    assert [g for g in report["gaps"] if g["missing_tongue"] == "machine"] == []
    lines = tc.defect_lines(report)
    assert any(l.startswith("INVALID: ") for l in lines)
    assert tc.main(["--root", root]) == 1


def test_machine_only_work_flags_human_and_ai(tmp_path):
    root = str(tmp_path)
    gov(root, "naya-dream-v1.machine.json", "{}")
    report = tc.audit(root)
    missing = {g["missing_tongue"] for g in report["gaps"]}
    assert missing == {"human", "ai"}


def test_case_mixed_triplet_groups_as_one_work(tmp_path):
    root = str(tmp_path)
    gov(root, "0021-NAYA-OATH-V1.human.md")
    gov(root, "0021-NAYA-OATH-V1.ai.md")
    gov(root, "0021-naya-oath-v1.machine.json", "{}")
    report = tc.audit(root)
    assert report["works_total"] == 1
    assert report["works_complete"] == 1


def test_audit_snapshot_is_exempt_not_flagged(tmp_path):
    root = str(tmp_path)
    gov(root, "DOC-COMPLETENESS-AUDIT-2026-10-10.md")
    report = tc.audit(root)
    assert report["works_total"] == 0
    assert len(report["exempt"]) == 1


def test_list_mode_emits_fix_queue_as_json(tmp_path, capsys):
    root = str(tmp_path)
    gov(root, "0002-HUMAN-ONLY-V1.md")
    assert tc.main(["--root", root, "--list"]) == 1
    data = json.loads(capsys.readouterr().out)
    assert data["gaps"] and data["works_total"] == 1
