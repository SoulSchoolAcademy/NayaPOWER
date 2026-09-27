from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
HUB = ROOT / "NAYANET" / "HUB" / "index.html"


def test_readme_points_to_current_system_truth():
    text = README.read_text(encoding="utf-8")
    assert "SYSTEM CURRENT TRUTH — 2026-09-26" in text
    assert "Nine Master Node kernel" in text
    assert "RUNTIME: BLOCKED" in text
    assert "N9 behavioral proof: NOT PROVEN" in text
    assert "NAYAPOWER-DAILY-INTELLIGENCE-REPORT-2026-09-26.md" in text


def test_hub_front_page_is_current_truth_surface():
    text = HUB.read_text(encoding="utf-8")
    assert "NAYA-HUB-CURRENT-TRUTH-2026-09-26" in text
    assert "NayaNET — Intelligent Hub · Current System Truth" in text
    assert "STRUCTURAL KERNEL: VERIFIED" in text
    assert "RUNTIME KERNEL: NOT PROVEN" in text
    assert "N9 BEHAVIORAL PROOF: NOT PROVEN" in text
    assert "NEXT: OWNER-SCOPED RUNTIME PROOF" in text
    assert "<title>NayaNET — Intelligent Hub V7 · 509 AAA</title>" not in text
