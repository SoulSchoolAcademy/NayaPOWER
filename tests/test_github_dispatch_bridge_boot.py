from pathlib import Path


def test_github_dispatch_bridge_has_single_projection_selector():
    source = (Path(__file__).resolve().parents[1] / "NAYANET" / "EXECUTION-BRIDGE" / "nayanet-github-dispatch" / "index.ts").read_text(encoding="utf-8")
    marker = 'const isProjection=operation==="project_smart_note";'
    assert source.count(marker) == 1, "duplicate projection selector causes the Edge Function to fail at startup"
