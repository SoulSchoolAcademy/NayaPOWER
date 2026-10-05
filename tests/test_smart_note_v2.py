import json
import re
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("smart_note_v2", ROOT / "tools" / "smart_note_v2.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def test_general_capture_discovery_is_not_filename_hardcoded():
    assert mod.changed_capture(["README.md", ".naya/capture/ANY-NAME.json"]) == [".naya/capture/ANY-NAME.json"]

def test_capture_discovery_returns_batch_sorted_not_aborted():
    # Problem A repair (GAP-20): a batch is discovered, never aborted. The
    # proof workflow processes each capture in sorted order, each with its
    # own SMART-NOTE-<capture_id> identity. This test fails on the pre-repair
    # code (SystemExit SMART_NOTE_CAPTURE_BATCH_NOT_YET_SUPPORTED).
    assert mod.changed_capture([
        ".naya/capture/c.json",
        "README.md",
        ".naya/capture/a.json",
        ".naya/capture/b.json",
    ]) == [".naya/capture/a.json", ".naya/capture/b.json", ".naya/capture/c.json"]

def test_capture_discovery_dedupes_and_ignores_non_captures():
    assert mod.changed_capture([
        ".naya/capture/b.json",
        ".naya/capture/b.json",
        ".naya/capture/x.md",
        "BRAIN/05-MEMORY/SMART-NOTES/a.md",
    ]) == [".naya/capture/b.json"]

def test_capture_discovery_empty_when_no_captures():
    assert mod.changed_capture(["README.md", "tools/x.py"]) == []

def test_machine_registry_contains_exact_private_block_pointer():
    reg = json.loads((ROOT / ".naya/memory/smart-notes/index.json").read_text())
    entry = next(e for e in reg["entries"] if e["intelligent_block_id"] == "IB-SMART-NOTE-20260929-b8f141805fa0d7ae")
    assert entry["scope"] == "PRIVATE"
    # D2 (smart-link generator, #1406): PRIVATE-scope notes are ACTIVE_AUTH_GATED, never bare ACTIVE.
    assert entry["smart_link_status"] == "ACTIVE_AUTH_GATED"
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
    assert entry["smart_link_status"] == "ACTIVE_AUTH_GATED"  # D2: PRIVATE scope, see above
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
    assert 'e.get("smart_link_status") in {"ACTIVE", "ACTIVE_AUTH_GATED", "READY"}' in workflow
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

def test_live_workflow_honors_private_publication_authorization_without_bare_active():
    """A PRIVATE canonical Block may publish an explicitly authorized derived view,
    but its Smart Link status remains ACTIVE_AUTH_GATED rather than bare ACTIVE."""
    workflow = (ROOT / ".github/workflows/live-intelligence-commit-proof.yml").read_text()
    assert 'expected_status="ACTIVE_AUTH_GATED" if e.get("scope")=="PRIVATE" else "ACTIVE"' in workflow
    assert '{"ACTIVE", "ACTIVE_AUTH_GATED", "READY"}' in workflow
    # Preserve the fail-closed private path: publication is decided by the canonical
    # projector, not by weakening PRIVATE into public inside the workflow.
    assert 'elif e.get("scope")=="PRIVATE":' in workflow
    assert 'assert e["projection_status"]=="PRIVATE_RENDER_VERIFIED"' in workflow
    assert 'assert e["smart_link_status"]=="PENDING_PRIVATE_PROJECTION"' in workflow


# --- Problem B regression: concurrent registry writers must not lose updates ---
# 2026-10-05: update_registry() did read-modify-write with no lock; two
# concurrent writers both allocated the same SN and the last writer won,
# dropping the other's entry. The registry_transaction (flock + atomic
# commit) serializes writers. These tests pin the fix.

def _problem_b_fresh_module(tmp_path):
    """Load smart_note_v2 with ROOT pointed at an isolated temp dir."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "smart_note_v2_isolated", ROOT / "tools" / "smart_note_v2.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    m.ROOT = tmp_path
    m.REGISTRY = tmp_path / ".naya" / "memory" / "smart-notes" / "index.json"
    m.BRAIN_SMART_NOTE_ROOT = tmp_path / "BRAIN" / "05-MEMORY" / "SMART-NOTES"
    return m

def _problem_b_inputs(m, tmp_path, ib_id):
    capture = {"title": f"Note {ib_id}", "category": "SMART_NOTE",
               "source": {"captured_at": "2026-10-05T00:00:00Z"}}
    block = {"intelligent_block_id": ib_id,
             "content": {"lesson": json.dumps({"lesson": f"lesson-{ib_id}"})},
             "understanding_state": "CANDIDATE", "owner_scope": "PRIVATE"}
    verify = {"persisted": {"block": block,
              "event": {"id": "e1"}, "lineage": {"id": "l1"},
              "relationship": {"relationship_id": "r1"},
              "index": {"id": "i1"}, "checkpoint": {"id": "c1"},
              "receipt": {"id": "rc1"}}}
    proj = tmp_path / "proj.md"
    proj.write_text("# test", encoding="utf-8")
    return capture, verify, proj

def test_concurrent_registry_writers_lose_no_updates(tmp_path):
    import threading
    m = _problem_b_fresh_module(tmp_path)
    errors = []
    def writer(ib):
        try:
            cap, ver, proj = _problem_b_inputs(m, tmp_path, ib)
            m.update_registry(cap, ver, proj)
        except Exception as e:  # noqa: BLE001 — collected, asserted below
            errors.append(repr(e))
    threads = [threading.Thread(target=writer, args=(f"IB-RACE-{i}",))
               for i in range(10)]
    for t in threads: t.start()
    for t in threads: t.join()
    assert not errors, errors
    reg = json.loads(m.REGISTRY.read_text(encoding="utf-8"))
    entries = reg["entries"]
    assert len(entries) == 10, f"lost update: {len(entries)}/10 entries"
    sn_ids = [e["smart_note_id"] for e in entries]
    assert len(sn_ids) == len(set(sn_ids)), "duplicate Smart Note IDs allocated"
    # Registry is valid JSON after every concurrent commit (atomic write).
    assert reg["schema"] == "naya.smart-note-projection-index.v1"

def test_concurrent_promotions_serialize_without_loss(tmp_path):
    import threading
    m = _problem_b_fresh_module(tmp_path)
    for i in range(3):
        cap, ver, proj = _problem_b_inputs(m, tmp_path, f"IB-PROM-{i}")
        m.update_registry(cap, ver, proj)
    reg = json.loads(m.REGISTRY.read_text(encoding="utf-8"))
    sn_ids = [e["smart_note_id"] for e in reg["entries"]]
    types = ["behavioral_test", "independent_verification", "reproduction"]
    bundle = [{"type": types[i % 3], "source": "s", "content_hash": f"h{i}",
               "gatherer": f"g{i}", "gathered_at": "2026-10-05T00:00:00Z"}
              for i in range(3)]
    errors = []
    def promoter(sn_id):
        try:
            m.promote_note(sn_id, bundle, "tester")
        except Exception as e:  # noqa: BLE001
            errors.append(repr(e))
    threads = [threading.Thread(target=promoter, args=(s,)) for s in sn_ids]
    for t in threads: t.start()
    for t in threads: t.join()
    assert not errors, errors
    reg2 = json.loads(m.REGISTRY.read_text(encoding="utf-8"))
    verified = [e for e in reg2["entries"] if e.get("truth_state") == "VERIFIED"]
    assert len(verified) == 3, f"promotion lost: {len(verified)}/3 verified"

def test_idempotent_recapture_keeps_smart_note_id(tmp_path):
    """Re-capturing the same intelligent block returns its SN (no sequence burn)."""
    m = _problem_b_fresh_module(tmp_path)
    cap, ver, proj = _problem_b_inputs(m, tmp_path, "IB-IDEMPOTENT")
    first = m.update_registry(cap, ver, proj)
    second = m.update_registry(cap, ver, proj)
    assert first["smart_note_id"] == second["smart_note_id"]
    reg = json.loads(m.REGISTRY.read_text(encoding="utf-8"))
    assert len(reg["entries"]) == 1


# --- Projection-path race regression: concurrent projectors must derive ---
# --- directories from authoritative reservations, never advisory pre-reads --
# 2026-10-05: projection_path() allocated an advisory SN *before* the
# registry transaction, so N concurrent projectors could pick the same SN
# directory and collide/clobber. reserve_smart_note_id() closes it: the
# directory is derived from the authoritatively reserved ID. These tests
# pin the fix at the projection seam (not the registry seam).

def _race_capture(ib_id):
    return {
        "title": f"Race note {ib_id}",
        "category": "SMART_NOTE",
        "topic": "CONCURRENCY",
        "subtopic": "PROJECTION_RACE",
        "source": {"captured_at": "2026-10-05T00:00:00Z"},
        "projection": {},
    }

def _race_verify(ib_id):
    lesson = json.dumps({"essence": f"essence-{ib_id}", "lesson": f"lesson-{ib_id}"})
    return {"persisted": {"block": {
        "intelligent_block_id": ib_id,
        "content": {"lesson": lesson},
        "understanding_state": "CANDIDATE",
        "owner_scope": "PUBLIC",
    }, "event": {"id": "e"}, "lineage": {"id": "l"},
      "relationship": {"relationship_id": "r"}, "index": {"id": "i"},
      "checkpoint": {"id": "c"}, "receipt": {"id": "rc"}}}

def test_concurrent_projectors_derive_distinct_directories(tmp_path):
    """N concurrent projectors → N distinct SN directories, zero clobbering."""
    import threading
    m = _problem_b_fresh_module(tmp_path)
    N = 20
    errors = []
    results = {}
    lock = threading.Lock()
    def projector(i):
        try:
            ib = f"IB-PROJ-RACE-{i:03d}"
            cap, ver = _race_capture(ib), _race_verify(ib)
            sn = m.reserve_smart_note_id(cap, ib)
            p = m.render(cap, ver, sn_id=sn)
            entry = m.update_registry(cap, ver, p, sn_id=sn)
            with lock:
                results[ib] = (sn, str(p), entry["smart_note_id"])
        except Exception as e:  # noqa: BLE001 — collected, asserted below
            with lock:
                errors.append(repr(e))
    threads = [threading.Thread(target=projector, args=(i,)) for i in range(N)]
    for t in threads: t.start()
    for t in threads: t.join()
    assert not errors, errors
    assert len(results) == N, f"projector lost: {len(results)}/{N}"
    sns = [v[0] for v in results.values()]
    assert len(set(sns)) == N, f"SN collision among projectors: {sns}"
    dirs = {str(Path(v[1]).parent) for v in results.values()}
    assert len(dirs) == N, "projected directories collided"
    for ib, (sn, p, entry_sn) in results.items():
        assert sn == entry_sn, "registry entry SN must match the reserved SN"
        text = Path(p).read_text(encoding="utf-8")
        assert ib in text, f"file content clobbered for {ib}"
        assert f"/{sn}/" in p.replace("\\", "/")
    reg = json.loads(m.REGISTRY.read_text(encoding="utf-8"))
    assert len(reg["entries"]) == N, f"registry lost entries: {len(reg['entries'])}/{N}"

def test_concurrent_duplicate_projections_converge_on_existing_sn(tmp_path):
    """Concurrent re-projections of the SAME block converge: one entry,
    stable SN (existing wins), zero errors."""
    import threading
    m = _problem_b_fresh_module(tmp_path)
    ib = "IB-PROJ-DUP"
    errors = []
    entry_sns = []
    lock = threading.Lock()
    def projector():
        try:
            cap, ver = _race_capture(ib), _race_verify(ib)
            sn = m.reserve_smart_note_id(cap, ib)
            p = m.render(cap, ver, sn_id=sn)
            entry = m.update_registry(cap, ver, p, sn_id=sn)
            with lock:
                entry_sns.append(entry["smart_note_id"])
        except Exception as e:  # noqa: BLE001
            with lock:
                errors.append(repr(e))
    threads = [threading.Thread(target=projector) for _ in range(5)]
    for t in threads: t.start()
    for t in threads: t.join()
    assert not errors, errors
    reg = json.loads(m.REGISTRY.read_text(encoding="utf-8"))
    assert len(reg["entries"]) == 1, "duplicate projections must converge to one entry"
    final_sn = reg["entries"][0]["smart_note_id"]
    assert all(s == final_sn for s in entry_sns), "entry SN must be stable across racers"
    assert reg["entries"][0]["projection_path"].endswith(f"/{final_sn}/{ib}.md")

def test_reserve_is_idempotent_for_known_block(tmp_path):
    """Re-reserving a known block returns its SN without burning sequence."""
    m = _problem_b_fresh_module(tmp_path)
    ib = "IB-PROJ-IDEM"
    cap, ver = _race_capture(ib), _race_verify(ib)
    first = m.reserve_smart_note_id(cap, ib)
    p = m.render(cap, ver, sn_id=first)
    m.update_registry(cap, ver, p, sn_id=first)
    seq_before = json.loads(m.REGISTRY.read_text(encoding="utf-8"))["sequence_policy"]["next_sequence"]
    second = m.reserve_smart_note_id(cap, ib)
    assert second == first, "re-reserve must return the existing SN"
    seq_after = json.loads(m.REGISTRY.read_text(encoding="utf-8"))["sequence_policy"]["next_sequence"]
    assert seq_after == seq_before, "re-reserve must not burn a sequence number"

def test_render_with_reserved_sn_id_uses_reserved_directory(tmp_path):
    m = _problem_b_fresh_module(tmp_path)
    ib = "IB-PROJ-DIR"
    cap, ver = _race_capture(ib), _race_verify(ib)
    sn = m.reserve_smart_note_id(cap, ib)
    p = m.render(cap, ver, sn_id=sn)
    ps = str(p).replace("\\", "/")
    assert f"/{sn}/" in ps, "rendered directory must derive from the reserved SN"
    assert ps.startswith(str(m.BRAIN_SMART_NOTE_ROOT).replace("\\", "/"))

def test_projection_path_advisory_fallback_unchanged(tmp_path):
    """Without sn_id=, projection_path keeps its advisory behavior."""
    m = _problem_b_fresh_module(tmp_path)
    cap = _race_capture("IB-PROJ-ADV")
    p = m.projection_path(cap, "IB-PROJ-ADV")
    assert "/SN-001/" in str(p).replace("\\", "/")


# --- Correction lifecycle: superseded intelligence remains provenance, not active retrieval ---
def test_registry_records_capture_lifecycle_metadata(tmp_path):
    m = _problem_b_fresh_module(tmp_path)
    cap, ver, proj = _problem_b_inputs(m, tmp_path, "IB-HISTORICAL")
    cap["lifecycle_state"] = "SUPERSEDED"
    cap["superseded_by_capture_id"] = "capture-r2"
    cap["supersession_reason"] = "Corrected by R2."
    entry = m.update_registry(cap, ver, proj)
    assert entry["lifecycle_state"] == "SUPERSEDED"
    assert entry["superseded_by_capture_id"] == "capture-r2"
    assert entry["supersession_reason"] == "Corrected by R2."


def test_retrieve_ignores_superseded_registry_entries(tmp_path, monkeypatch):
    old_page = tmp_path / "old.md"
    new_page = tmp_path / "new.md"
    old_page.write_text("# Old\n\n## IN A NUTSHELL\n\nold answer", encoding="utf-8")
    new_page.write_text("# New\n\n## IN A NUTSHELL\n\nactive answer", encoding="utf-8")
    registry_path = tmp_path / "index.json"
    registry_path.write_text(json.dumps({
        "entries": [
            {
                "smart_note_id": "SN-346",
                "intelligent_block_id": "IB-OLD",
                "title": "Nonstop Loop",
                "category": "SYSTEM_INTELLIGENCE",
                "topic": "GOVERNANCE",
                "subtopic": "OPERATING_CODE",
                "captured_at": "2026-10-05T23:59:59Z",
                "projection_path": "old.md",
                "lifecycle_state": "SUPERSEDED",
            },
            {
                "smart_note_id": "SN-0355",
                "intelligent_block_id": "IB-R2",
                "title": "Nonstop Loop",
                "category": "SYSTEM_INTELLIGENCE",
                "topic": "GOVERNANCE",
                "subtopic": "OPERATING_CODE",
                "captured_at": "2026-10-05T00:00:00Z",
                "projection_path": "new.md",
                "lifecycle_state": "ACTIVE",
            },
        ]
    }), encoding="utf-8")
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "REGISTRY", registry_path)
    result = mod.retrieve("nonstop loop governance")
    assert result["retrieved"]["smart_note_id"] == "SN-0355"
    assert result["retrieved"]["intelligent_block_id"] == "IB-R2"
    assert result["explanation"] == "active answer"
