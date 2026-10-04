import json
import re
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("smart_note_v2", ROOT / "tools" / "smart_note_v2.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def test_general_capture_discovery_is_not_filename_hardcoded():
    assert mod.changed_capture(["README.md", ".naya/capture/ANY-NAME.json"]) == ".naya/capture/ANY-NAME.json"

def test_capture_discovery_fails_closed_on_batch():
    try:
        mod.changed_capture([".naya/capture/a.json", ".naya/capture/b.json"])
    except SystemExit as e:
        assert "BATCH_NOT_YET_SUPPORTED" in str(e)
    else:
        raise AssertionError("expected fail-closed batch rejection")

def test_machine_registry_contains_exact_private_block_pointer():
    reg = json.loads((ROOT / ".naya/memory/smart-notes/index.json").read_text())
    entry = next(e for e in reg["entries"] if e["intelligent_block_id"] == "IB-SMART-NOTE-20260929-b8f141805fa0d7ae")
    assert entry["scope"] == "PRIVATE"
    assert entry["smart_link_status"] == "ACTIVE"
    assert entry["provenance"]["receipt_id"] == "faa4345a-aacd-43f2-ab2f-a991b9681979"

def test_nia_language_has_primary_command_and_safe_ceiling():
    nia = json.loads((ROOT / "BRAIN/00-SPEC/NIA-LANGUAGE-INTENT-V1.json").read_text())
    assert nia["primary_capture_command"] == "Smart Note this"
    assert nia["primary_capture_intent"] == "CAPTURE_DURABLE_INTELLIGENCE"
    assert nia["maximum_automatic_capture_state"] == "CANDIDATE"
    assert nia["safety"]["may_grant_authority"] is False

def test_historical_checkpoint_binding_uses_object_local_receipt_semantics():
    reg = json.loads((ROOT / ".naya/memory/smart-notes/index.json").read_text())
    entry = next(e for e in reg["entries"] if e["intelligent_block_id"] == "IB-SMART-NOTE-20260929-b8f141805fa0d7ae")
    assert entry["provenance"]["checkpoint_semantics"] == "MUTABLE_PROJECT_STATE_POINTER"
    assert entry["provenance"]["historical_checkpoint_binding"] == "EXECUTION_RECEIPT_EVIDENCE"
    workflow = (ROOT / ".github/workflows/live-intelligence-commit-proof.yml").read_text()
    assert "RECEIPT_OBJECT_LOCAL_SNAPSHOT" in workflow

def test_smart_note_command_is_standing_authority_for_same_note_lifecycle():
    nia = (ROOT / "BRAIN/00-SPEC/0006-NIA-LANGUAGE-INTENT-CONTRACT-V1.md").read_text()
    assert "No second `DEPLOY` confirmation is required" in nia
    assert "One command, one complete Smart Note lifecycle" in nia
    assert "does **not** authorize unrelated product releases" in nia

def test_registered_smart_link_is_active_and_exact():
    reg = json.loads((ROOT / ".naya/memory/smart-notes/index.json").read_text())
    entry = next(e for e in reg["entries"] if e["intelligent_block_id"] == "IB-SMART-NOTE-20260929-b8f141805fa0d7ae")
    assert entry["smart_link_status"] == "ACTIVE"
    assert entry["projection_status"] == "GITHUB_BRAIN_PUBLISHED"
    assert entry["smart_link"].startswith("https://github.com/SoulSchoolAcademy/NayaPOWER/blob/main/BRAIN/05-MEMORY/SMART-NOTES/")
    assert entry["smart_note_id"] == "SN-001"
    assert entry["canonical_brain_path"].endswith("/SN-001/IB-SMART-NOTE-20260929-b8f141805fa0d7ae.md")

def test_human_smart_note_projection_lives_in_brain_memory_hierarchy():
    entry_path = ROOT / "BRAIN/05-MEMORY/SMART-NOTES/2026/09/29/SYSTEM-INTELLIGENCE/SMART-NOTE-SYSTEM/OFFICIAL-SMART-NOTE-FORMAT/SN-001/IB-SMART-NOTE-20260929-b8f141805fa0d7ae.md"
    assert entry_path.exists()
    text = entry_path.read_text()
    for section in [
        "IN A NUTSHELL", "HUMAN NOTE", "CHILD NOTE", "GRANDMA NOTE", "NAYA NOTE",
        "MACHINE NOTE", "LEARNING LESSON", "WHAT IT MEANS", "WHAT'S IN IT FOR YOU",
        "HOW TO APPLY / HOW TO USE", "HOW IT CONNECTS", "PROOF / PROVENANCE", "TRUTH BOUNDARY"
    ]:
        assert section in text
    assert "IB-SMART-NOTE-20260929-b8f141805fa0d7ae" in text

def test_projection_generator_targets_brain_and_preserves_private_default():
    assert "BRAIN_SMART_NOTE_ROOT" in mod.__dict__
    assert str(mod.BRAIN_SMART_NOTE_ROOT).endswith("BRAIN/05-MEMORY/SMART-NOTES")
    private_capture = {
        "source": {"captured_at": "2026-09-29"},
        "category": "SYSTEM_INTELLIGENCE",
        "topic": "SMART_NOTE_SYSTEM",
        "subtopic": "OFFICIAL_FORMAT",
        "projection": {}
    }
    p = mod.projection_path(private_capture, "IB-TEST")
    assert "BRAIN/05-MEMORY/SMART-NOTES/2026/09/29" in str(p).replace("\\", "/")
    assert "/SN-" in str(p).replace("\\", "/")

def test_sn002_is_registered_to_live_canonical_runtime():
    reg = json.loads((ROOT / ".naya/memory/smart-notes/index.json").read_text())
    entry = next(e for e in reg["entries"] if e.get("smart_note_id") == "SN-002")
    assert entry["intelligent_block_id"] == "IB-SMART-NOTE-20260929-sn002-smart-note-node-flow"
    assert entry["provenance"]["receipt_id"] == "102d900e-1dc0-44ce-bde4-9d8d668f4d60"
    assert entry["proven_relationship"]["source_id"] == "NAYA-KERNEL-KNOW"
    assert entry["proven_relationship"]["relationship_type"] == "PRODUCES"
    assert entry["proof_boundary"]["universal_nine_node_binding"] == "NOT_PROVEN"

def _max_allocated_sn_number():
    reg = json.loads((ROOT / ".naya/memory/smart-notes/index.json").read_text())
    nums = [int(m.group(1)) for e in reg.get("entries", [])
            for m in [re.fullmatch(r"SN-(\d+)", str(e.get("smart_note_id", "")))] if m]
    return reg, max(nums) if nums else 0




def test_explicit_smart_note_id_is_honored():
    capture = {"smart_note_id": "SN-013", "source": {"captured_at": "2026-09-30"}}
    assert mod.allocate_smart_note_id(capture, "IB-EXPLICIT") == "SN-013"

def test_sequence_policy_advances_after_sn002():
    reg, maxn = _max_allocated_sn_number()
    assert reg["sequence_policy"]["next_sequence"] == maxn + 1
    assert mod.allocate_smart_note_id({"source": {"captured_at": "2026-09-29"}}, "IB-NEW") == f"SN-{maxn + 1:03d}"


def test_projection_workflow_publishes_active_verified_public_projection():
    workflow = (ROOT / ".github/workflows/live-intelligence-commit-proof.yml").read_text()
    assert 'e.get("smart_link_status") in {"ACTIVE", "READY"}' in workflow
    assert 'e.get("smart_link_status")=="READY"' not in workflow


def test_projection_workflow_does_not_allocate_intelligent_block_identity():
    workflow = (ROOT / ".github/workflows/live-intelligence-commit-proof.yml").read_text()
    assert 'ib="IB-SMART-NOTE-"+capture["capture_id"]' not in workflow
    assert '"intelligent_block_id"' in workflow


def test_projection_workflow_stages_brain_projection_and_registry():
    workflow = (ROOT / ".github/workflows/live-intelligence-commit-proof.yml").read_text()
    assert "git add BRAIN/05-MEMORY/SMART-NOTES .naya/memory/smart-notes" in workflow


def test_sequence_policy_advances_past_sn003():
    reg, maxn = _max_allocated_sn_number()
    assert reg["sequence_policy"]["next_sequence"] == maxn + 1
    assert mod.allocate_smart_note_id({"source": {"captured_at": "2026-09-29"}}, "IB-NEW") == f"SN-{maxn + 1:03d}"


def test_live_intelligence_proof_is_capture_triggered_not_arbitrary_main_push():
    workflow = (ROOT / ".github/workflows/live-intelligence-commit-proof.yml").read_text()
    assert '".naya/capture/**"' in workflow

def _verify_for_lesson(lesson, block_id="IB-SN004-TEST"):
    return {
        "persisted": {
            "block": {
                "intelligent_block_id": block_id,
                "content": {"lesson": json.dumps(lesson)},
                "owner_scope": "PRIVATE",
                "understanding_state": "CANDIDATE",
            },
            "event": {"id": "EV-SN004"},
            "lineage": {"id": "LIN-SN004"},
            "relationship": {"relationship_id": "REL-SN004"},
            "index": {"id": "IDX-SN004"},
            "checkpoint": {"id": "CP-SN004"},
            "receipt": {"id": "REC-SN004"},
        }
    }


def _private_sn004_capture():
    return {
        "title": "SN-004 regression",
        "source": {"captured_at": "2026-09-29"},
        "projection": {},
        "category": "SYSTEM_INTELLIGENCE",
        "topic": "NAYA_STANDING_LAW",
        "subtopic": "ACT_FIRST_AUTONOMY",
    }


def test_renderer_accepts_persisted_sn004_string_views_without_inventing_relationship_types(tmp_path):
    legacy = {
        "essence": "legacy essence",
        "human_view": "legacy human view",
        "simple_view": "legacy simple view",
        "naya_view": "legacy naya view",
        "machine_view": {"automatic_truth_ceiling": "CANDIDATE"},
        "connections": ["legacy untyped connection"],
        "decisions": ["preserve evidence"],
        "priority": "legacy priority",
        "uncertainty": "legacy uncertainty",
    }
    original = json.loads((ROOT / ".naya/capture/SMART-NOTE-20260929-sn004-shawn-standing-law.json").read_text())["intelligence"]
    # These meaning fields are unchanged from the original persisted SN-004.
    legacy["learning_lesson"] = original["learning_lesson"]
    legacy["applicability"] = original["applicability"]
    verify = _verify_for_lesson(legacy)
    before = json.dumps(verify, sort_keys=True)
    path = mod.render(_private_sn004_capture(), verify, private_root=tmp_path)
    rendered = path.read_text()
    assert legacy["learning_lesson"] in rendered
    assert legacy["applicability"] in rendered
    assert "**Truth state:** CANDIDATE" in rendered
    assert json.dumps(verify, sort_keys=True) == before
    assert "legacy human view" in rendered
    assert "legacy simple view" in rendered
    assert "legacy naya view" in rendered
    assert "- legacy untyped connection" in rendered
    assert "**RELATED_TO**" not in rendered
    assert str(path).startswith(str(tmp_path))


def test_renderer_preserves_current_structured_sn004_shape(tmp_path):
    capture = json.loads((ROOT / ".naya/capture/SMART-NOTE-20260929-sn004-shawn-standing-law.json").read_text())
    intelligence = capture["intelligence"]
    path = mod.render(_private_sn004_capture(), _verify_for_lesson(intelligence, "IB-SN004-STRUCTURED"), private_root=tmp_path)
    rendered = path.read_text()
    assert intelligence["human_view"]["meaning"] in rendered
    assert intelligence["simple_view"]["child"] in rendered
    assert intelligence["naya_view"]["purpose"] in rendered
    assert "**SUPPORTS**" in rendered
    assert intelligence["learning_lesson"] in rendered
    assert intelligence["human_view"]["simple_rule"] in rendered
    # The structured rule wins over the applicability fallback.
    assert intelligence["applicability"] not in rendered


def test_private_projection_still_fails_closed_without_authenticated_private_surface():
    try:
        mod.render(
            _private_sn004_capture(),
            _verify_for_lesson({"essence": "private", "connections": [], "decisions": []}, "IB-PRIVATE-DENIED"),
        )
    except SystemExit as exc:
        assert str(exc) == "PRIVATE_PROJECTION_REQUIRES_AUTHENTICATED_PRIVATE_SURFACE"
    else:
        raise AssertionError("expected private projection to fail closed")


def test_registry_reconciles_exact_persisted_lesson_with_complete_runtime_refs(tmp_path, monkeypatch):
    import hashlib

    capture = _private_sn004_capture()
    intelligence = {"essence": "Retain exact meaning", "human_view": "Read before acting"}
    # Same serialization used by the workflow's capture reconciliation.
    lesson = json.dumps(intelligence, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    verify = _verify_for_lesson(intelligence, "IB-CANONICAL-REUSE")
    verify["persisted"]["block"]["content"]["lesson"] = lesson
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "REGISTRY", tmp_path / "index.json")
    monkeypatch.setattr(mod, "BRAIN_SMART_NOTE_ROOT", tmp_path / "BRAIN")
    projection = tmp_path / "BRAIN" / "note.md"
    mod.update_registry(capture, verify, projection)
    registry = json.loads(mod.REGISTRY.read_text())
    digest = hashlib.sha256(lesson.encode()).hexdigest()
    # Exercise the actual workflow consumer's lookup and reference names.
    exact = next((entry for entry in registry["entries"]
                  if entry.get("content_hash") == digest), None)
    assert exact is not None, "The persisted note must be reusable by exact content hash"
    assert exact["intelligent_block_id"] == "IB-CANONICAL-REUSE"
    refs = exact["provenance"]
    assert refs["event_id"] == verify["persisted"]["event"]["id"]
    assert refs["lineage_id"] == verify["persisted"]["lineage"]["id"]
    assert refs["relationship_id"] == verify["persisted"]["relationship"]["relationship_id"]
    assert refs["runtime_index_id"] == verify["persisted"]["index"]["id"]
    assert refs["checkpoint_id"] == verify["persisted"]["checkpoint"]["id"]
    assert refs["receipt_id"] == verify["persisted"]["receipt"]["id"]
    assert exact["truth_state"] == "CANDIDATE"
    changed_digest = hashlib.sha256((lesson + " ").encode()).hexdigest()
    assert all(entry.get("content_hash") != changed_digest for entry in registry["entries"])


def test_registry_hash_survives_noncanonical_lesson_serialization(tmp_path, monkeypatch):
    """The writer's content_hash must match the workflow reader's digest even when
    the persisted lesson string is valid JSON with different key order/spacing
    than the canonical form (e.g. as re-serialized by the database)."""
    import hashlib

    capture = _private_sn004_capture()
    intelligence = {"essence": "Retain exact meaning", "human_view": "Read before acting"}
    # Deliberately non-canonical: reversed key order + spaces, same object.
    lesson = json.dumps(intelligence, sort_keys=False, separators=(", ", ": "), ensure_ascii=False)
    assert lesson != json.dumps(intelligence, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    verify = _verify_for_lesson(intelligence, "IB-NONCANONICAL")
    verify["persisted"]["block"]["content"]["lesson"] = lesson
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "REGISTRY", tmp_path / "index.json")
    monkeypatch.setattr(mod, "BRAIN_SMART_NOTE_ROOT", tmp_path / "BRAIN")
    projection = tmp_path / "BRAIN" / "note.md"
    mod.update_registry(capture, verify, projection)
    registry = json.loads(mod.REGISTRY.read_text())
    # The workflow reader's formula: canonical JSON of capture["intelligence"].
    reader_digest = hashlib.sha256(
        json.dumps(intelligence, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    ).hexdigest()
    exact = next((entry for entry in registry["entries"]
                  if entry.get("content_hash") == reader_digest), None)
    assert exact is not None, "content_hash must equal the reader's canonical digest"
    assert exact["intelligent_block_id"] == "IB-NONCANONICAL"


def test_registry_hash_plain_string_lesson_is_stable(tmp_path, monkeypatch):
    """Non-JSON lessons (plain strings) hash as-is and remain stable."""
    import hashlib

    capture = _private_sn004_capture()
    verify = _verify_for_lesson({"x": 1}, "IB-PLAIN")
    verify["persisted"]["block"]["content"]["lesson"] = "Preserve provenance before applying retained intelligence."
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "REGISTRY", tmp_path / "index.json")
    monkeypatch.setattr(mod, "BRAIN_SMART_NOTE_ROOT", tmp_path / "BRAIN")
    projection = tmp_path / "BRAIN" / "note.md"
    mod.update_registry(capture, verify, projection)
    registry = json.loads(mod.REGISTRY.read_text())
    expected = hashlib.sha256(
        "Preserve provenance before applying retained intelligence.".encode()).hexdigest()
    assert registry["entries"][0]["content_hash"] == expected


def test_resolve_runtime_connections_maps_smart_note_ids_to_canonical_blocks():
    registry = {"entries": [
        {"smart_note_id": "SN-003", "intelligent_block_id": "IB-CONTINUATION"},
        {"smart_note_id": "SN-014", "intelligent_block_id": "IB-COMPOUNDING"},
    ]}
    capture = {"intelligence": {"connections": [
        {"type": "SUPPORTS", "target": "SN-014 — The Compounding Imperative"},
        {"type": "REFINES", "target": "SN-003 — Continuation Engine"},
        {"type": "MADE_UP_EDGE", "target": "SN-014"},
        {"type": "SUPPORTS", "target": "unresolved prose"},
        {"type": "SUPPORTS", "target": "SN-014 — duplicate"},
    ]}}
    assert mod.resolve_runtime_connections(capture, registry) == [
        {"target_block_id": "IB-COMPOUNDING", "relationship_type": "SUPPORTS"},
        {"target_block_id": "IB-CONTINUATION", "relationship_type": "REFINES"},
    ]


def test_live_capture_threads_only_resolved_connections_to_writer():
    workflow = (ROOT / ".github/workflows/live-intelligence-commit-proof.yml").read_text()
    assert "resolve_runtime_connections(capture,registry)" in workflow
    assert '"p_connections":resolved_connections' in workflow


def test_prime_judgment_law_is_locked_into_agent_operating_contracts_and_capture():
    agents = (ROOT / "AGENTS.md").read_text()
    master = (ROOT / ".naya/MASTER-DIRECTOR-ULTRA-OPTIMIZATION-V1.md").read_text()
    protocol = (ROOT / "BRAIN/04-INTELLIGENCE/0005-SMART-NODE-INTELLIGENT-BLOCK-PROTOCOL-V1.md").read_text()
    cold = (ROOT / "NAYA-ACTIVATION/00-MASTER-COLD-NAYA-ACTIVATION.md").read_text()
    capture = json.loads((ROOT / ".naya/capture/SMART-NOTE-20260930-sn016-prime-judgment-rule.json").read_text())
    assert "PRIME JUDGMENT LAW — JUDGMENT BEFORE BLIND OBEDIENCE" in agents
    assert "I was told to" in agents
    assert "Prime Judgment Rule — Judgment Before Blind Obedience" in master
    assert "## 22. Prime Judgment Law — Judgment Before Blind Obedience" in protocol
    assert "instruction is not proof of correctness" in cold.lower()
    assert capture["smart_note_id"] == "SN-016"
    assert capture["intelligence"]["machine_view"]["instruction_is_proof"] is False
    assert capture["intelligence"]["machine_view"]["human_authority_preserved"] is True
    assert capture["intelligence"]["machine_view"]["automatic_truth_ceiling"] == "CANDIDATE"


def test_renderer_emits_ai_note_section_from_ai_view(tmp_path):
    lesson = {
        "essence": "ai note essence",
        "ai_view": {
            "instruction": "AI operating instruction for seats",
            "primary_evaluation": "cold successor applies it unaided",
        },
        "machine_view": {"automatic_truth_ceiling": "CANDIDATE"},
    }
    verify = _verify_for_lesson(lesson, block_id="IB-AINOTE-TEST")
    path = mod.render(_private_sn004_capture(), verify, private_root=tmp_path)
    rendered = path.read_text()
    assert "## 🤖 AI NOTE" in rendered
    assert "AI operating instruction for seats" in rendered
    assert "cold successor applies it unaided" in rendered


def test_smart_note_validation_rejects_invented_preview_path():
    with pytest.raises(SystemExit, match="SMART_NOTE_INVENTED_LOCATION"):
        mod.validate_changed_paths([".naya/preview/IB-SMART-NOTE-20261004-wrong.md"])


def test_smart_note_validation_rejects_projection_outside_brain():
    with pytest.raises(SystemExit, match="SMART_NOTE_PROJECTION_OUTSIDE_BRAIN"):
        mod.validate_changed_paths(["notes/IB-SMART-NOTE-20261004-wrong.md"])


def test_smart_note_front_doors_point_to_canonical_brain_path():
    capture_readme = (mod.ROOT / ".naya/capture/README.md").read_text(encoding="utf-8")
    activation_readme = (mod.ROOT / "NAYA-ACTIVATION/README.md").read_text(encoding="utf-8")
    agents = (mod.ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert "BRAIN/05-MEMORY/SMART-NOTES/YYYY/MM/DD" in capture_readme
    assert ".naya/memory/smart-notes/YYYY" not in capture_readme
    assert "SMART-NOTE-OPERATING-CONTRACT-V1.md" in activation_readme
    assert "SMART-NOTE-OPERATING-CONTRACT-V1.md" in agents
