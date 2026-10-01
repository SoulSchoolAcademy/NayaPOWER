"""Active Awesomeness: activation installs the Awesome Code as operating personality.

Covers the wiring, not the content's legal status: both 100-trait drafts are
CANDIDATE until Shawn ratifies one. These tests pin the mechanism —
Core Code inlined at boot, full profile by canonical pointer reference,
machine-checkable, fail-closed.
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "tools" / "verify_activation_personality.py"
POINTER = ROOT / "BRAIN/03-KERNEL/0005-AWESOME-CODE-PROFILE-POINTER-V1.json"
PERSONALITY = ROOT / "NAYA-ACTIVATION/KERNEL/PERSONALITY.md"
RECEIPT_TEMPLATE = ROOT / "NAYA-ACTIVATION/ACTIVATION-RECEIPT-TEMPLATE.json"

CORE_LINES = [
    "Be awesome every day of your life.",
    "Know who you are.",
    "Know why you are.",
    "Be all you can be.",
    "Be you.",
    "Be aware.",
    "Produce nothing but awesomeness.",
    "Don't worry about the rest — it's all bullshit.",
]


def _pointer():
    return json.loads(POINTER.read_text(encoding="utf-8"))


def _run(repo: Path, *extra):
    return subprocess.run(
        [sys.executable, str(VERIFY), "--repo", str(repo), *extra],
        capture_output=True, text=True, timeout=60,
    )


def _fixture_tree(tmp_path: Path, *, status="CANDIDATE", ratified=None,
                  tamper_lines=False, drop_personality=False) -> Path:
    """Minimal repo tree the verifier accepts: pointer + personality doc."""
    repo = tmp_path / "repo"
    (repo / "BRAIN/03-KERNEL").mkdir(parents=True)
    lines = list(CORE_LINES)
    if tamper_lines:
        lines[0] = "Be mediocre every day of your life."
    pointer = {
        "status": status,
        "core_code": {
            "lines": lines,
            # NOTE: sha stays the true one on purpose for the tamper test,
            # so lines-vs-sha self-consistency fails.
            "sha256": _pointer()["core_code"]["sha256"],
        },
        "ratified_profile": ratified,
    }
    (repo / "BRAIN/03-KERNEL/0005-AWESOME-CODE-PROFILE-POINTER-V1.json").write_text(
        json.dumps(pointer), encoding="utf-8")
    if not drop_personality:
        (repo / "NAYA-ACTIVATION/KERNEL").mkdir(parents=True)
        (repo / "NAYA-ACTIVATION/KERNEL/PERSONALITY.md").write_text(
            "\n".join(CORE_LINES) + "\n", encoding="utf-8")
    return repo


# --- positive: the real tree -------------------------------------------------

def test_personality_doc_inlines_core_code_verbatim():
    text = PERSONALITY.read_text(encoding="utf-8")
    for line in _pointer()["core_code"]["lines"]:
        assert line in text, f"PERSONALITY.md missing verbatim Core Code line: {line!r}"


def test_pointer_core_code_matches_shawns_eight_lines():
    assert _pointer()["core_code"]["lines"] == CORE_LINES


def test_pointer_is_candidate_with_null_ratified_profile():
    """Current truth: no profile ratified yet. Update deliberately on ratification."""
    p = _pointer()
    assert p["status"] == "CANDIDATE"
    assert p["ratified_profile"] is None


def test_verify_script_passes_on_real_tree():
    r = _run(ROOT)
    assert r.returncode == 0, r.stdout + r.stderr
    assert r.stdout.startswith("PASS")


def test_receipt_template_has_personality_block():
    template = json.loads(RECEIPT_TEMPLATE.read_text(encoding="utf-8"))
    block = template["personality"]
    assert block["profile_pointer"] == "BRAIN/03-KERNEL/0005-AWESOME-CODE-PROFILE-POINTER-V1.json"
    assert block["core_code_sha256"] is None  # filled at activation
    assert block["profile_status"] is None


def test_kit_map_boot_order_includes_personality_at_kernel():
    kit_map = (ROOT / "NAYA-ACTIVATION/00-ACTIVATION-KIT-MAP-V1.md").read_text(encoding="utf-8")
    assert "PERSONALITY" in kit_map or "personality" in kit_map


def test_who_doc_references_personality():
    who = (ROOT / "NAYA-ACTIVATION/KERNEL/WHO.md").read_text(encoding="utf-8")
    assert "PERSONALITY.md" in who


# --- negative: fail closed ----------------------------------------------------

def test_missing_pointer_fails_closed(tmp_path):
    repo = _fixture_tree(tmp_path)
    (repo / "BRAIN/03-KERNEL/0005-AWESOME-CODE-PROFILE-POINTER-V1.json").unlink()
    r = _run(repo)
    assert r.returncode == 1
    assert "FAIL" in r.stdout


def test_unknown_pointer_status_fails_closed(tmp_path):
    repo = _fixture_tree(tmp_path, status="BOGUS")
    r = _run(repo)
    assert r.returncode == 1
    assert "unknown" in r.stdout.lower()


def test_tampered_core_code_lines_fail_closed(tmp_path):
    repo = _fixture_tree(tmp_path, tamper_lines=True)
    r = _run(repo)
    assert r.returncode == 1
    assert "sha256" in r.stdout.lower()


def test_missing_personality_doc_fails_closed(tmp_path):
    repo = _fixture_tree(tmp_path, drop_personality=True)
    r = _run(repo)
    assert r.returncode == 1
    assert "FAIL" in r.stdout


def test_ratified_without_profile_fails_closed(tmp_path):
    repo = _fixture_tree(tmp_path, status="RATIFIED", ratified=None)
    r = _run(repo)
    assert r.returncode == 1
    assert "FAIL" in r.stdout


def test_ratified_profile_hash_mismatch_fails_closed(tmp_path):
    repo = _fixture_tree(tmp_path)
    profile = repo / "profiles" / "awesome-v1.md"
    profile.parent.mkdir(parents=True)
    profile.write_text("tampered content", encoding="utf-8")
    pointer_path = repo / "BRAIN/03-KERNEL/0005-AWESOME-CODE-PROFILE-POINTER-V1.json"
    pointer = json.loads(pointer_path.read_text(encoding="utf-8"))
    pointer["status"] = "RATIFIED"
    pointer["ratified_profile"] = {
        "id": "awesome-v1",
        "path": "profiles/awesome-v1.md",
        "version": "1",
        "sha256": "0" * 64,  # wrong on purpose
    }
    pointer_path.write_text(json.dumps(pointer), encoding="utf-8")
    r = _run(repo)
    assert r.returncode == 1
    assert "mismatch" in r.stdout.lower()


def test_ratified_profile_missing_file_fails_closed(tmp_path):
    repo = _fixture_tree(tmp_path)
    pointer_path = repo / "BRAIN/03-KERNEL/0005-AWESOME-CODE-PROFILE-POINTER-V1.json"
    pointer = json.loads(pointer_path.read_text(encoding="utf-8"))
    pointer["status"] = "RATIFIED"
    pointer["ratified_profile"] = {
        "id": "awesome-v1", "path": "profiles/awesome-v1.md",
        "version": "1", "sha256": "0" * 64,
    }
    pointer_path.write_text(json.dumps(pointer), encoding="utf-8")
    r = _run(repo)
    assert r.returncode == 1
    assert "missing" in r.stdout.lower()


def test_receipt_with_mismatched_core_code_hash_is_rejected(tmp_path):
    repo = _fixture_tree(tmp_path)
    receipt = {
        "personality": {
            "core_code_sha256": "0" * 64,
            "profile_pointer": "BRAIN/03-KERNEL/0005-AWESOME-CODE-PROFILE-POINTER-V1.json",
            "profile_id": None, "profile_version": None,
            "profile_sha256": None, "profile_status": "CANDIDATE",
        }
    }
    receipt_path = tmp_path / "receipt.json"
    receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
    r = _run(repo, "--receipt", str(receipt_path))
    assert r.returncode == 1
    assert "core_code_sha256" in r.stdout


def test_receipt_claiming_ratified_profile_while_candidate_is_rejected(tmp_path):
    repo = _fixture_tree(tmp_path)
    receipt = {
        "personality": {
            "core_code_sha256": _pointer()["core_code"]["sha256"],
            "profile_pointer": "BRAIN/03-KERNEL/0005-AWESOME-CODE-PROFILE-POINTER-V1.json",
            "profile_id": "sneaky", "profile_version": "9",
            "profile_sha256": "f" * 64, "profile_status": "CANDIDATE",
        }
    }
    receipt_path = tmp_path / "receipt.json"
    receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
    r = _run(repo, "--receipt", str(receipt_path))
    assert r.returncode == 1
    assert "CANDIDATE" in r.stdout


def test_valid_candidate_receipt_passes(tmp_path):
    repo = _fixture_tree(tmp_path)
    receipt = {
        "personality": {
            "core_code_sha256": _pointer()["core_code"]["sha256"],
            "profile_pointer": "BRAIN/03-KERNEL/0005-AWESOME-CODE-PROFILE-POINTER-V1.json",
            "profile_id": None, "profile_version": None,
            "profile_sha256": None, "profile_status": "CANDIDATE",
        }
    }
    receipt_path = tmp_path / "receipt.json"
    receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
    r = _run(repo, "--receipt", str(receipt_path))
    assert r.returncode == 0, r.stdout + r.stderr
    assert r.stdout.startswith("PASS")
