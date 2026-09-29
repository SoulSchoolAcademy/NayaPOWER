from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ACTIVATION = ROOT / "NAYA-ACTIVATION"
CURRENT_REALITY = ACTIVATION / "CURRENT-REALITY"
SUPERSEDED = "SOURCE-PRECEDENCE-AND-NAVIGATION-RECONCILIATION-2026-09-28.md"


def _current_precedence_path() -> Path:
    candidates = sorted(CURRENT_REALITY.glob("SOURCE-PRECEDENCE-AND-NAVIGATION-RECONCILIATION-*.md"))
    assert candidates, "current source-precedence reconciliation is missing"
    return candidates[-1]


def test_cold_activation_locators_point_to_current_precedence_and_not_stale_snapshots():
    current = _current_precedence_path()
    current_ref = current.relative_to(ACTIVATION).as_posix()

    activation_map = (ACTIVATION / "00-ACTIVATION-KIT-MAP-V1.md").read_text(encoding="utf-8")
    current_state = (CURRENT_REALITY / "CURRENT-STATE.md").read_text(encoding="utf-8")

    assert "SOURCE-PRECEDENCE-AND-NAVIGATION-RECONCILIATION-*.md" in activation_map
    assert SUPERSEDED not in activation_map
    assert current.name in current_state
    assert SUPERSEDED not in current_state


def test_dynamic_current_reality_locators_do_not_stamp_a_stale_main_sha():
    for name in ("CURRENT-STATE.md", "ACTIVE-WORK.md", "NEXT-ACTION.md"):
        content = (CURRENT_REALITY / name).read_text(encoding="utf-8")
        assert "Verified against main @" not in content
