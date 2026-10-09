from pathlib import Path

from _freshness_guard import (
    FAMILY_GLOB,
    assert_surface_fresh,
    newest_sibling,
)

ROOT = Path(__file__).resolve().parents[1]
ACTIVATION = ROOT / "NAYA-ACTIVATION"
CURRENT_REALITY = ACTIVATION / "CURRENT-REALITY"


def test_cold_activation_locators_point_to_current_precedence_and_not_stale_snapshots():
    current = newest_sibling(CURRENT_REALITY, FAMILY_GLOB)
    current_ref = current.relative_to(ACTIVATION).as_posix()

    activation_map = (ACTIVATION / "00-ACTIVATION-KIT-MAP-V1.md").read_text(encoding="utf-8")
    current_state = (CURRENT_REALITY / "CURRENT-STATE.md").read_text(encoding="utf-8")

    # Negative (derived): neither surface may name any superseded sibling.
    assert_surface_fresh(ACTIVATION / "00-ACTIVATION-KIT-MAP-V1.md", CURRENT_REALITY, FAMILY_GLOB)
    assert_surface_fresh(CURRENT_REALITY / "CURRENT-STATE.md", CURRENT_REALITY, FAMILY_GLOB)

    # Positive: the map uses the dynamic family pointer; CURRENT-STATE names
    # the newest dated reconciliation on disk.
    assert FAMILY_GLOB in activation_map
    assert current.name in current_state


def test_dynamic_current_reality_locators_do_not_stamp_a_stale_main_sha():
    for name in ("CURRENT-STATE.md", "ACTIVE-WORK.md", "NEXT-ACTION.md"):
        content = (CURRENT_REALITY / name).read_text(encoding="utf-8")
        assert "Verified against main @" not in content
