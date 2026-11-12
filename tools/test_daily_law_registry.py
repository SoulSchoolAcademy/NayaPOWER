"""Tests for tools/generate_daily_law_registry.py (GT-010).

Negative controls (required):
  * --check FAILS when the prose source moves without regenerating
    (a planted law entry must turn the check red, with cure lines);
  * an L-number cited in prose without its own entry bullet is counted
    absent — never fabricated into a record;
  * a field the source entry does not carry stays null — never invented.
Plus the two source shapes (id-first and titled heads), the duplicate-id
merge rule (later mention wins per-field), determinism (byte-identical
re-generation), and the delta fold-in (embedded fingerprint == the delta
build's own fingerprint).
"""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_daily_law_registry as reg  # noqa: E402

AGENTS_FIXTURE = """# AGENTS.md (fixture)

## Distilled lessons — fixture batch (distillation v2, iteration 1)

- **L101 [F6] NEW FILING (promoted):** a widget defaults to the safe mode. Rule: every mode default is the safe mode. Falsifier: an unset default that publishes. Confidence: high. Guardrail owner: fixture lane.
- **L102 [F1] — the period-head shape parses.** Rule: split on the bold span, not the colon. Falsifier: this record missing from the registry.
- **The Titled Law (L103 — Shawn, 2026-10-10 — STANDING):** fix what is broken instead of describing it. Falsifier: a known defect reported instead of repaired.
- **L101 [F6] PROMOTED (2nd instance):** restated with a declared change. Declared behavior change (Lesson Law): from now on, we file the change with the lesson.
- **WP-101 (1/3) NEW FILING [F9]:** a win worth repeating. Rule: name why it worked.
- **L105 [F2] NEW FILING:** a fifth record so the numbering range has a gap. Rule: gaps are counted honestly.
- A bullet with no id at all — must be ignored by the parser.
- Prose citing L104 and L102 inline; L104 has no entry of its own.
"""


@pytest.fixture()
def gov_dir(tmp_path):
    gov = tmp_path / "gov"
    gov.mkdir()
    for num, title in (("0001", "Fixture Law One"), ("0002", "Fixture Law Two")):
        (gov / f"{num}-FIXTURE-V1.machine.json").write_text(json.dumps({
            "title": title, "statement": f"statement {num}",
            "falsifier": f"falsifier {num}", "owner": "fixture",
        }))
        (gov / f"{num}-FIXTURE-V1.human.md").write_text("# fixture\n")
        (gov / f"{num}-FIXTURE-V1.ai.md").write_text("# fixture\n")
    return gov


@pytest.fixture()
def agents_file(tmp_path):
    p = tmp_path / "AGENTS.md"
    p.write_text(AGENTS_FIXTURE)
    return p


def test_parse_shapes_and_fields():
    records, _stats = reg.parse_agents_md(AGENTS_FIXTURE)
    by_id = {r["id"]: r for r in records}
    assert by_id["L101"]["family"] == "F6"
    assert by_id["L101"]["rule"] == "every mode default is the safe mode."
    assert by_id["L101"]["falsifier"] == "an unset default that publishes."
    assert by_id["L101"]["owner"] == "fixture lane."
    assert by_id["L102"]["title"] == "the period-head shape parses."
    assert by_id["L103"]["title"] == "The Titled Law"
    assert by_id["L103"]["rule"].startswith("fix what is broken")
    assert by_id["WP-101"]["kind"] == "win-pattern"


def test_fields_never_invented():
    records, _ = reg.parse_agents_md(AGENTS_FIXTURE)
    by_id = {r["id"]: r for r in records}
    # L102's source carries no owner/confidence/behavior-change labels.
    assert by_id["L102"]["owner"] is None
    assert by_id["L102"]["confidence"] is None
    assert by_id["L102"]["behavior_change"] is None


def test_duplicate_id_merges_later_wins():
    records, _ = reg.parse_agents_md(AGENTS_FIXTURE)
    by_id = {r["id"]: r for r in records}
    assert by_id["L101"]["mentions"] == 2
    # the 2nd instance's declared behavior change lands; the 1st's fields persist
    assert "file the change with the lesson" in by_id["L101"]["behavior_change"]
    assert by_id["L101"]["falsifier"] == "an unset default that publishes."


def test_absent_numbers_counted_never_fabricated():
    records, stats = reg.parse_agents_md(AGENTS_FIXTURE)
    ids = {r["id"] for r in records}
    assert "L104" not in ids
    assert "L104" in stats["absent_lesson_numbers"]


def test_build_registry_folds_delta(gov_dir, agents_file):
    registry, problems = reg.build_registry(agents_file.read_text(), gov_dir)
    assert problems == []
    assert registry["counts"]["governance_sets"] == 2
    delta_mod = reg.load_delta_module()
    delta, _ = delta_mod.build_delta(gov_dir)
    assert (registry["generated_from"]["governance_delta"]["source_fingerprint_sha256"]
            == delta["generated_from"]["source_fingerprint_sha256"])
    assert registry["counts"]["daily_law_records"] == 5  # L101, L102, L103, L105, WP-101


def test_deterministic_render(gov_dir, agents_file):
    a, _ = reg.build_registry(agents_file.read_text(), gov_dir)
    b, _ = reg.build_registry(agents_file.read_text(), gov_dir)
    assert reg.render_json(a) == reg.render_json(b)
    assert reg.render_human(a) == reg.render_human(b)


def test_check_passes_then_fails_on_prose_edit(gov_dir, agents_file, tmp_path):
    out = gov_dir / "DAILY-LAW-REGISTRY.machine.json"
    human = gov_dir / "DAILY-LAW-REGISTRY.human.md"
    argv = ["--agents-md", str(agents_file), "--gov", str(gov_dir)]
    assert reg.main(argv) == 0
    assert out.exists() and human.exists()
    # freshness: unchanged sources -> check green
    assert reg.main(argv + ["--check"]) == 0
    # NEGATIVE CONTROL: plant a new law in the prose; check must go red
    agents_file.write_text(AGENTS_FIXTURE + (
        "\n- **L199 [F1] NEW FILING:** planted. Rule: planted entries fail the check. "
        "Falsifier: the check stays green.\n"))
    assert reg.main(argv + ["--check"]) == 1
    # and regenerating restores green with the new record present
    assert reg.main(argv) == 0
    data = json.loads(out.read_text())
    assert any(r["id"] == "L199" for r in data["daily_laws"])
    assert reg.main(argv + ["--check"]) == 0
