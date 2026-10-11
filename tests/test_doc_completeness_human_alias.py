"""Regression tests for canonical plain-Markdown human protocol forms."""
import json

from tools.doc_completeness_check import check_law_triple


def _write_triple(tmp_path, base: str, human_name: str | None = None):
    (tmp_path / f"{base}.md").write_text("# Human protocol\n\nThe operating procedure.\n", encoding="utf-8")
    (tmp_path / f"{base}.ai.md").write_text("# AI protocol\n\nRead and follow.\n", encoding="utf-8")
    (tmp_path / f"{base}.machine.json").write_text(
        json.dumps({"contract": base, "version": "1.0"}), encoding="utf-8"
    )
    if human_name:
        (tmp_path / human_name).write_text("# Explicit human form\n", encoding="utf-8")


def test_plain_markdown_can_be_human_form_with_ai_and_machine_siblings(tmp_path):
    _write_triple(tmp_path, "NAYA-PROTOCOL-V1")
    failures, _warnings = check_law_triple(tmp_path)
    assert not any("NAYA-PROTOCOL-V1: human form missing" in item for item in failures)


def test_explicit_human_form_still_passes(tmp_path):
    _write_triple(tmp_path, "EXAMPLE-LAW", "EXAMPLE-LAW.human.md")
    failures, _warnings = check_law_triple(tmp_path)
    assert failures == []


def _write_ai_machine_pair(tmp_path, base: str, human_target: str | None):
    (tmp_path / f"{base}.ai.md").write_text("# AI protocol\n\nRead and follow.\n", encoding="utf-8")
    contract = {"contract": base, "version": "1.0"}
    if human_target is not None:
        contract["canonical_human"] = human_target
    (tmp_path / f"{base}.machine.json").write_text(
        json.dumps(contract), encoding="utf-8"
    )


def test_machine_declared_external_human_form_passes(tmp_path):
    # The canonical human form lives outside the governance dir (ratified root
    # PROTOCOL.md pattern); the machine contract declares and it exists.
    external = tmp_path / "PROTOCOL.md"
    external.write_text("# The protocol\n", encoding="utf-8")
    gov = tmp_path / "gov"
    gov.mkdir()
    _write_ai_machine_pair(gov, "NAYA-PROTOCOL-V1", "../PROTOCOL.md")
    failures, _warnings = check_law_triple(gov)
    assert not any("NAYA-PROTOCOL-V1: human form missing" in item for item in failures)


def test_machine_declared_missing_human_form_still_fails(tmp_path):
    # Declared but nonexistent human source must not count.
    gov = tmp_path / "gov"
    gov.mkdir()
    _write_ai_machine_pair(gov, "NAYA-PROTOCOL-V1", "../MISSING.md")
    failures, _warnings = check_law_triple(gov)
    assert any("NAYA-PROTOCOL-V1: human form missing" in item for item in failures)
