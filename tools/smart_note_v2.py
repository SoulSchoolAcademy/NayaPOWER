#!/usr/bin/env python3
from __future__ import annotations
import argparse, contextlib, fcntl, hashlib, json, os, re, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRAIN_SMART_NOTE_ROOT = ROOT / "BRAIN" / "05-MEMORY" / "SMART-NOTES"
REGISTRY = ROOT / ".naya" / "memory" / "smart-notes" / "index.json"

def slug(s):
    x = re.sub(r"[^a-z0-9]+", "-", str(s).lower()).strip("-")
    return x or "uncategorized"

def load_json(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))

class PreservationMigrationError(ValueError):
    """Raised when a Smart Note migration would destroy governed state."""


PROTECTED_MIGRATION_SEGMENTS = {
    "provenance", "restoration_provenance", "ratification", "falsifier",
    "falsification", "measurement", "measurement_contract", "successor",
    "successor_effect",
}


def _path_exists(document, path):
    current = document
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            return False
        current = current[part]
    return True


def _path_get(document, path):
    current = document
    for part in path.split("."):
        current = current[part]
    return current


def _path_delete(document, path):
    parts = path.split(".")
    current = document
    for part in parts[:-1]:
        current = current[part]
    del current[parts[-1]]


def _deep_merge_preserving_unknown(existing, patch):
    """Merge declared patch values while retaining unknown keys recursively."""
    import copy
    if not isinstance(existing, dict) or not isinstance(patch, dict):
        return copy.deepcopy(patch)
    merged = copy.deepcopy(existing)
    for key, value in patch.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge_preserving_unknown(merged[key], value)
        else:
            merged[key] = copy.deepcopy(value)
    return merged


def _flatten_paths(value, prefix=""):
    """Return deterministic leaf paths for migration receipts."""
    if not isinstance(value, dict):
        return {prefix} if prefix else set()
    paths = set()
    for key, child in value.items():
        path = f"{prefix}.{key}" if prefix else str(key)
        if isinstance(child, dict):
            paths.update(_flatten_paths(child, path) or {path})
        else:
            paths.add(path)
    return paths


def _protected_migration_path(path):
    return any(part.lower() in PROTECTED_MIGRATION_SEGMENTS for part in path.split("."))


def migrate_preserving_fields(existing_capture, patch, explicit_removals=None):
    """Apply a monotonic Smart Note migration without dropping unknown fields."""
    if not isinstance(existing_capture, dict) or not isinstance(patch, dict):
        raise PreservationMigrationError("CAPTURE_AND_PATCH_MUST_BE_OBJECTS")
    removals = list(explicit_removals or [])
    document = _deep_merge_preserving_unknown(existing_capture, patch)

    for item in removals:
        if not isinstance(item, dict):
            raise PreservationMigrationError("REMOVAL_MANIFEST_ENTRY_INVALID")
        path = str(item.get("path") or "").strip()
        reason = str(item.get("reason") or "").strip()
        authority = str(item.get("authority") or "").strip()
        if not path or not reason or not authority:
            raise PreservationMigrationError("EXPLICIT_REMOVAL_REQUIRES_PATH_REASON_AUTHORITY")
        if _protected_migration_path(path):
            raise PreservationMigrationError(f"PROTECTED_FIELD_REMOVAL:{path}")
        if not _path_exists(document, path):
            raise PreservationMigrationError(f"REMOVAL_TARGET_NOT_FOUND:{path}")
        _path_delete(document, path)

    before = _flatten_paths(existing_capture)
    after = _flatten_paths(document)
    patch_paths = _flatten_paths(patch)
    changed = sorted(
        path for path in (before & after & patch_paths)
        if _path_get(existing_capture, path) != _path_get(document, path)
    )
    added = sorted(after - before)
    removed = sorted(before - after)
    declared_removed = {str(item["path"]).strip() for item in removals}
    undeclared = sorted(set(removed) - declared_removed)
    if undeclared:
        raise PreservationMigrationError("EXPLICIT_REMOVAL_REQUIRED:" + ",".join(undeclared))

    receipt = {
        "schema": "naya.smart-note-migration-receipt.v1",
        "changed_paths": changed,
        "added_paths": added,
        "removed_paths": removed,
        "removals": [{
            "path": str(item["path"]).strip(),
            "reason": str(item["reason"]).strip(),
            "authority": str(item["authority"]).strip(),
        } for item in removals],
    }
    return {"document": document, "receipt": receipt}


def migrate_capture_file(existing_path, patch_path, output_path, receipt_path, explicit_removals=None):
    """Apply the canonical preservation migration to JSON files and persist its receipt."""
    existing = load_json(existing_path)
    patch = load_json(patch_path)
    result = migrate_preserving_fields(existing, patch, explicit_removals=explicit_removals)
    Path(output_path).write_text(
        json.dumps(result["document"], indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    Path(receipt_path).write_text(
        json.dumps(result["receipt"], indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return result

def _registry_lock_path(registry_path):
    rp = Path(registry_path)
    return rp.parent / (rp.stem + ".lock")

def _atomic_write_json(path, obj):
    """Write JSON atomically: temp file in the same directory + os.replace.

    Readers never observe a torn file, even if the writer crashes mid-write.
    """
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(p.parent), prefix=p.stem + ".", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, p)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise

@contextlib.contextmanager
def registry_transaction(registry_path=None):
    """Exclusive read-modify-write transaction on the Smart Note registry.

    Holds an flock(LOCK_EX) across the whole transaction so concurrent
    writers serialize; the commit is atomic (temp + os.replace). Yields
    the in-memory registry dict; on clean exit the (possibly mutated)
    dict is committed. On exception the lock releases with no write.
    """
    rp = Path(registry_path) if registry_path else REGISTRY
    rp.parent.mkdir(parents=True, exist_ok=True)
    lock_path = _registry_lock_path(rp)
    with open(lock_path, "w") as lf:
        fcntl.flock(lf.fileno(), fcntl.LOCK_EX)
        try:
            if rp.exists():
                registry = json.loads(rp.read_text(encoding="utf-8"))
            else:
                registry = {"schema": "naya.smart-note-projection-index.v1",
                            "version": "1.0",
                            "source_of_truth": "runtime_intelligent_block",
                            "entries": []}
            yield registry
            _atomic_write_json(rp, registry)
        finally:
            fcntl.flock(lf.fileno(), fcntl.LOCK_UN)

def changed_capture(paths, *, existing_only=False):
    """Return the sorted, deduplicated list of changed Smart Note capture paths.

    A commit may carry more than one capture (batch). The discovery seam is
    intentionally batch-capable: the caller processes each capture in sorted
    order, each with its own identity (``SMART-NOTE-<capture_id>``). Failing
    closed on a batch would silently shelve valuable intelligence; fail-fast
    instead on any *individual* capture that is malformed, downstream.

    Git diffs also report deleted capture paths. At runtime those files no
    longer exist and therefore are not ingestible intelligence. Set
    ``existing_only=True`` at the workflow/CLI boundary so deletions are
    ignored rather than misclassified as malformed capture failures.
    """
    hits = []
    for raw in paths:
        normalized = str(raw).replace("\\", "/")
        p = Path(normalized)
        if normalized.startswith(".naya/capture/") and p.suffix == ".json":
            if existing_only and not p.is_file():
                continue
            hits.append(normalized)
    return sorted(set(hits))

EDGE_VOCABULARY = {
    "DERIVED_FROM","SUPPORTS","CONTRADICTS","DEPENDS_ON","IMPLEMENTS","GOVERNS",
    "AUTHORIZED_BY","USED_BY","CAUSED","RESULTED_IN","VERIFIED_BY","LEARNED_FROM",
    "SUPERSEDES","SUCCEEDS","RELATED_TO","CONTEXTUALIZES","INVALIDATES","REFINES",
    "CORRECTS","ENABLES","PRODUCES","APPLIES_TO",
}


def resolve_runtime_connections(capture, registry):
    """Resolve declared Smart Note relationships to canonical owner-scoped IB IDs.

    Human-facing targets may begin with a stable Smart Note ID (for example
    "SN-014 — The Compounding Imperative") or name an exact Intelligent Block ID.
    Unresolved prose and unknown relationship types fail closed by omission.
    """
    by_sn = {str(e.get("smart_note_id", "")).upper(): e.get("intelligent_block_id")
             for e in registry.get("entries", []) if e.get("smart_note_id") and e.get("intelligent_block_id")}
    known_ib = {str(e.get("intelligent_block_id")) for e in registry.get("entries", []) if e.get("intelligent_block_id")}
    out = []
    seen = set()
    for raw in capture.get("intelligence", {}).get("connections", []) or []:
        if not isinstance(raw, dict):
            continue
        rel = str(raw.get("relationship_type") or raw.get("type") or "").strip().upper()
        target = str(raw.get("target_block_id") or raw.get("target") or "").strip()
        if rel not in EDGE_VOCABULARY or not target:
            continue
        resolved = target if target in known_ib else None
        if resolved is None:
            m = re.match(r"^(SN-\d{3,})\b", target, flags=re.IGNORECASE)
            if m:
                resolved = by_sn.get(m.group(1).upper())
        if not resolved:
            continue
        key = (resolved, rel)
        if key in seen:
            continue
        seen.add(key)
        out.append({"target_block_id": resolved, "relationship_type": rel})
    return out

def _assert_smart_note_id_available(sn_id, ib, entries):
    """Fail closed if sn_id is already owned by any different block."""
    conflicts = sorted({
        str(e.get("intelligent_block_id"))
        for e in entries
        if str(e.get("smart_note_id") or "").strip().upper() == sn_id
        and e.get("intelligent_block_id") != ib
    })
    if conflicts:
        raise SystemExit(
            "SMART_NOTE_ID_COLLISION:"
            f"{sn_id}:owned_by={','.join(conflicts)}:requested_by={ib}"
        )


def _allocate_from_registry(capture, ib, registry):
    """Pure SN allocation against an already-loaded registry.

    Call inside a registry_transaction so the read-allocate-write is atomic.
    Idempotent: a re-capture of the same intelligent block returns its
    existing SN instead of consuming a new sequence number.

    Explicit IDs are claims, not authority: an explicit SN already owned by
    another Intelligent Block fails closed. Automatic allocation also skips
    occupied IDs so a stale next_sequence pointer cannot reissue an existing
    human-facing Smart Note identity.
    """
    entries = registry.get("entries", [])
    explicit = str(capture.get("smart_note_id") or "").strip().upper()
    if re.fullmatch(r"SN-\d{3,}", explicit):
        _assert_smart_note_id_available(explicit, ib, entries)
        return explicit

    existing = next(
        (e for e in entries
         if e.get("intelligent_block_id") == ib and e.get("smart_note_id")),
        None,
    )
    if existing:
        return existing["smart_note_id"]

    occupied = {
        int(m.group(1))
        for e in entries
        for m in [re.fullmatch(r"SN-(\d+)", str(e.get("smart_note_id") or "").strip().upper())]
        if m
    }
    seq = int(registry.get("sequence_policy", {}).get("next_sequence", 1))
    while seq in occupied:
        seq += 1
    return f"SN-{seq:03d}"

def allocate_smart_note_id(capture, ib):
    """Advisory SN allocation outside a transaction (e.g. projection_path).

    Takes a brief read of the registry. The authoritative allocation happens
    inside update_registry's transaction; a concurrent writer may advance the
    sequence between this advisory read and the commit, so callers must treat
    the result as advisory, not reserved.
    """
    if REGISTRY.exists():
        registry = load_json(REGISTRY)
    else:
        registry = {"entries": []}
    return _allocate_from_registry(capture, ib, registry)

def reserve_smart_note_id(capture, ib, registry_path=None):
    """Authoritatively reserve a Smart Note ID for (capture, ib).

    The allocation read and the sequence advance commit atomically inside
    one registry_transaction, so concurrent projectors can never receive
    the same sequence number. Pass the result as sn_id= to
    projection_path()/render()/update_registry() so the projected
    directory is derived from the authoritative allocation instead of an
    advisory pre-read (this closes the projection-path race that the
    Problem B registry-transaction fix deliberately left open).

    A reservation that is never projected leaves a harmless gap: the
    sequence guarantees uniqueness, never reuse — not contiguity.
    Re-reserving a known intelligent block returns its existing SN
    without burning a sequence number.
    """
    with registry_transaction(registry_path) as registry:
        sn_id = _allocate_from_registry(capture, ib, registry)
        seq_match = re.fullmatch(r"SN-(\d+)", sn_id)
        if seq_match:
            policy = registry.setdefault("sequence_policy", {"human_id_format": "SN-###"})
            policy["next_sequence"] = max(int(policy.get("next_sequence", 1)),
                                          int(seq_match.group(1)) + 1)
            policy["purpose"] = ("Stable human-facing Smart Note identity. IB-ID remains canonical "
                                 "machine identity; capture timestamp remains provenance.")
        return sn_id

def projection_path(capture, ib, root=None, sn_id=None):
    # root resolves at call time (not def time) so test harnesses that
    # re-point BRAIN_SMART_NOTE_ROOT get the live value.
    if root is None:
        root = BRAIN_SMART_NOTE_ROOT
    captured = str(capture.get("captured_at_utc") or capture.get("source", {}).get("captured_at_utc") or capture["source"]["captured_at"])
    date = captured[:10]
    y, m, d = date.split("-")
    meta = capture.get("projection", {})
    cat = (meta.get("category_slug") or slug(capture.get("category", "smart-note"))).upper()
    topic = (meta.get("topic_slug") or slug(capture.get("topic", "general"))).upper()
    sub = (meta.get("subtopic_slug") or slug(capture.get("subtopic", "general"))).upper()
    if sn_id is None:
        sn_id = allocate_smart_note_id(capture, ib)
    return Path(root) / y / m / d / cat / topic / sub / sn_id / (ib + ".md")


def view_text(value, key, *, primary_key):
    if isinstance(value, dict):
        return str(value.get(key, "") or "")
    if isinstance(value, str):
        return value if key == primary_key else ""
    return ""

def connection_lines(values):
    lines = []
    for value in values or []:
        if isinstance(value, dict):
            rel_type = str(value.get("type") or "").strip()
            target = str(value.get("target") or "").strip()
            if rel_type and target:
                lines.append(f"- **{rel_type}** → {target}")
            elif target:
                lines.append("- " + target)
        elif isinstance(value, str):
            lines.append("- " + value)
    return lines

def render(capture, verify, private_root=None, sn_id=None):
    block = verify["persisted"]["block"]
    ib = block["intelligent_block_id"]
    intelligence = json.loads(block["content"]["lesson"])
    scope = str(block.get("owner_scope", "PRIVATE")).upper()
    projection_meta = capture.get("projection", {})
    public_authorized = bool(projection_meta.get("human_director_authorized_publication")) or str(projection_meta.get("publication_scope", "")).upper() in {"PUBLIC", "COLLECTIVE", "PUBLIC_DERIVED_VIEW"}
    if scope == "PRIVATE" and not public_authorized:
        if not private_root:
            raise SystemExit("PRIVATE_PROJECTION_REQUIRES_AUTHENTICATED_PRIVATE_SURFACE")
        p = projection_path(capture, ib, Path(private_root), sn_id=sn_id)
    else:
        p = projection_path(capture, ib, sn_id=sn_id)
    p.parent.mkdir(parents=True, exist_ok=True)
    if verify.get("supersession_proof"):
        proof = {
            "proof_type": "SUPERSESSION_RECONCILIATION",
            "prior_lineage_preserved": True,
            "prior_lineage": verify["supersession_proof"].get("prior_lineage", {}),
            "prior_intelligent_block_id": verify["supersession_proof"].get("prior_intelligent_block_id"),
            "current_intelligent_block_id": block["intelligent_block_id"],
            "current_block_row_id": block["block_id"],
            "content_hash": verify["supersession_proof"].get("content_hash"),
        }
    else:
        proof = {
            "event_id": verify["persisted"]["event"]["id"],
            "lineage_id": verify["persisted"]["lineage"]["id"],
            "relationship_id": verify["persisted"]["relationship"]["relationship_id"],
            "index_id": verify["persisted"]["index"]["id"],
            "checkpoint_id": verify["persisted"]["checkpoint"]["id"],
            "receipt_id": verify["persisted"]["receipt"]["id"],
        }
    lines = [
        "# " + capture["title"], "",
        "**Intelligent Block:** " + ib,
        "**Truth state:** " + str(block["understanding_state"]),
        "**Scope:** " + str(block["owner_scope"]),
        "**Captured:** " + str(capture["source"]["captured_at"]),
        "**Canonical intent:** " + str(capture.get("canonical_intent", "CAPTURE_DURABLE_INTELLIGENCE")), "",
        "> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.", "",
        "## ✦ IN A NUTSHELL", "", intelligence.get("essence", ""), "",
        "## 🩷 HUMAN NOTE", "", view_text(intelligence.get("human_view"), "meaning", primary_key="meaning"), "", view_text(intelligence.get("human_view"), "why_it_matters", primary_key="meaning"), "",
        "## 🟣 CHILD NOTE", "", view_text(intelligence.get("simple_view"), "child", primary_key="child"), "",
        "## 🔵 GRANDMA NOTE", "", view_text(intelligence.get("simple_view"), "grandma", primary_key="child"), "",
        "## 🟠 NAYA NOTE", "", view_text(intelligence.get("naya_view"), "purpose", primary_key="purpose"), "", view_text(intelligence.get("naya_view"), "architectural_rule", primary_key="purpose"), "",
        "## 🟢 MACHINE NOTE", "", "~~~json", json.dumps(intelligence.get("machine_view", {}), indent=2, ensure_ascii=False), "~~~", "",
        "## 🟢 LEARNING LESSON", "", intelligence.get("learning_lesson", "Experience becomes compounding intelligence only when retained meaning can be retrieved, applied, observed, verified, and used to improve what happens next."), "",
        "## 🟡 WHAT IT MEANS", "", intelligence.get("priority", ""), "",
        "## ⚪ WHAT'S IN IT FOR YOU", "", "Less repetition, less lost knowledge, faster comprehension, stronger continuity, and a direct Smart Link showing exactly what Naya preserved.", ""
    ]
    lines += [
        "", "## 🟨 HOW TO APPLY / HOW TO USE", "", view_text(intelligence.get("human_view"), "simple_rule", primary_key="meaning") or intelligence.get("applicability", ""), "",
        "## 🔗 HOW IT CONNECTS", "", *connection_lines(intelligence.get("connections", [])), "",
        "## 🧭 KEY DECISIONS / PRINCIPLES", "", *["- " + x for x in intelligence.get("decisions", [])], "",
        "## 🧾 PROOF / PROVENANCE", "", "~~~json", json.dumps(proof, indent=2), "~~~", "",
        "## ⚠️ TRUTH BOUNDARY / UNCERTAINTY", "", intelligence.get("uncertainty", ""), "",
        "## ➜ NEXT ACTION / SUCCESS CONDITION", "", "Keep this intelligence retrievable, apply it only when relevant and authorized, verify resulting outcomes, and compound only what evidence supports.", ""
    ]
    p.write_text("\n".join(lines), encoding="utf-8")
    return p

def _canonical_content_hash(lesson: str) -> str:
    """Hash the canonical JSON form of the lesson, matching the workflow reader.

    The live-intelligence-commit-proof workflow recomputes
    sha256(json.dumps(capture["intelligence"], sort_keys=True,
    separators=(",", ":"), ensure_ascii=False)). The persisted lesson string
    is JSON encoding the same intelligence object, but the database may store
    it with different key order or spacing. Canonicalizing before hashing
    makes the writer's content_hash invariant to serialization differences,
    so exact-match reconciliation works regardless of how the lesson string
    was serialized. Non-JSON lessons (plain strings) hash as-is.
    """
    try:
        canonical = json.dumps(json.loads(lesson), sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    except (ValueError, TypeError):
        canonical = lesson
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def update_registry(capture, verify, projection, sn_id=None):
    # The whole read-allocate-modify-write runs inside one exclusive
    # transaction: concurrent writers serialize, the commit is atomic.
    # (Problem B fix — the pre-lock code lost updates under concurrency.)
    # sn_id, when reserved upstream via reserve_smart_note_id(), makes the
    # recorded entry agree with the projected directory (projection-path
    # race fix); without it the authoritative allocation happens here.
    with registry_transaction() as registry:
        return _update_registry_locked(capture, verify, projection, registry, sn_id=sn_id)

def _update_registry_locked(capture, verify, projection, registry, sn_id=None):
    block = verify["persisted"]["block"]
    ib = block["intelligent_block_id"]
    if sn_id is None:
        sn_id = _allocate_from_registry(capture, ib, registry)
    else:
        # Reserved upstream. Preserve the idempotent re-capture invariant:
        # an existing entry for this IB keeps its SN (and projection path);
        # the reserved number becomes a harmless sequence gap. An explicit
        # smart_note_id in the capture still wins, as before.
        explicit = str(capture.get("smart_note_id") or "").strip().upper()
        existing = next((e for e in registry.get("entries", [])
                         if e.get("intelligent_block_id") == ib and e.get("smart_note_id")), None)
        if (not re.fullmatch(r"SN-\d{3,}", explicit) and existing is not None
                and existing["smart_note_id"] != sn_id):
            sn_id = existing["smart_note_id"]
            if existing.get("projection_path"):
                projection = ROOT / existing["projection_path"]
    normalized_sn_id = str(sn_id or "").strip().upper()
    if re.fullmatch(r"SN-\d{3,}", normalized_sn_id):
        _assert_smart_note_id_available(
            normalized_sn_id, ib, registry.get("entries", [])
        )
    entry = {
        "smart_note_id": sn_id,
        "intelligent_block_id": block["intelligent_block_id"],
        "content_hash": _canonical_content_hash(block["content"]["lesson"]),
        "title": capture["title"],
        "captured_at": capture["source"]["captured_at"],
        "category": capture.get("category", "SMART_NOTE"),
        "topic": capture.get("topic", ""),
        "subtopic": capture.get("subtopic", ""),
        "truth_state": block["understanding_state"],
        "lifecycle_state": str(capture.get("lifecycle_state", "ACTIVE")).upper(),
        "superseded_by_capture_id": capture.get("superseded_by_capture_id"),
        "supersession_reason": capture.get("supersession_reason"),
        "scope": block["owner_scope"],
        "projection_path": str(projection.relative_to(ROOT)).replace("\\\\", "/") if str(projection).startswith(str(ROOT)) else None,
        "projection_status": "GITHUB_BRAIN_PUBLISHED" if str(projection).startswith(str(BRAIN_SMART_NOTE_ROOT)) else "PRIVATE_RENDER_VERIFIED",
        "smart_link_status": ("ACTIVE_AUTH_GATED" if str(block.get("owner_scope", "PRIVATE")).upper() == "PRIVATE" else "ACTIVE") if str(projection).startswith(str(BRAIN_SMART_NOTE_ROOT)) else "PENDING_PRIVATE_PROJECTION",
        "smart_link": ("https://github.com/SoulSchoolAcademy/NayaPOWER/blob/main/" + str(projection.relative_to(ROOT)).replace("\\", "/")) if str(projection).startswith(str(BRAIN_SMART_NOTE_ROOT)) else None,
        "publication_scope": capture.get("projection", {}).get("publication_scope", "PRIVATE"),
        "keywords": ["smart note","capture","intelligent block","future naya","superbrain","intent","memory","reusable intelligence"],
        "provenance": {
            "event_id": verify["persisted"]["event"]["id"],
            "lineage_id": verify["persisted"]["lineage"]["id"],
            "relationship_id": verify["persisted"]["relationship"]["relationship_id"],
            "runtime_index_id": verify["persisted"]["index"]["id"],
            "checkpoint_id": verify["persisted"]["checkpoint"]["id"],
            "receipt_id": verify["persisted"]["receipt"]["id"],
        },
    }
    registry["entries"] = [e for e in registry.get("entries", []) if e.get("intelligent_block_id") != entry["intelligent_block_id"]] + [entry]
    registry["entries"] = sorted(registry["entries"], key=lambda x: (x.get("smart_note_id",""), x.get("intelligent_block_id","")))
    seq_match = re.fullmatch(r"SN-(\d+)", sn_id)
    if seq_match:
        policy = registry.setdefault("sequence_policy", {"human_id_format":"SN-###"})
        policy["next_sequence"] = max(int(policy.get("next_sequence", 1)), int(seq_match.group(1)) + 1)
        policy["purpose"] = "Stable human-facing Smart Note identity. IB-ID remains canonical machine identity; capture timestamp remains provenance."
    # No direct write: registry_transaction commits atomically on clean exit.
    return entry

# Truth-state authority rank for retrieval tie-breaking. Higher = more
# authoritative. Rank breaks ties on keyword relevance only — relevance
# dominates (see retrieve()). The map covers the full elevation ladder
# (CANDIDATE < TESTING < VERIFIED < RATIFIED < ACTIVE < LEARNED) so higher
# truth states outrank lower ones at equal relevance. Unknown/missing
# truth_state ranks 0 (neutral) so legacy entries without the field behave
# exactly as before.
TRUTH_STATE_RANK = {"LEARNED": 4, "ACTIVE": 3, "RATIFIED": 2, "VERIFIED": 1}

def _stem(word):
    """Normalize common English inflections so 'compounding' matches 'compound'.

    Conservative: only strips unambiguous suffixes, never shortens below
    4 chars, applied identically to query and haystack so matches are
    preserved. (Retrieval 10/10 track, 2026-10-06.)
    """
    if len(word) <= 4:
        return word
    for suffix in ("ing", "ed", "es", "ly", "ion"):
        if word.endswith(suffix) and len(word) > len(suffix) + 3:
            return word[:-len(suffix)]
    if word.endswith("s") and not word.endswith("ss") and len(word) > 5:
        return word[:-1]
    return word


def _field_words(text):
    """Tokenize text into a set of stemmed lowercase words."""
    return set(_stem(w) for w in re.findall(r"[a-z0-9]+", text.lower()))

def _nutshell_text(projection_path):
    """Return a note's IN A NUTSHELL lesson text for retrieval matching.

    Unreadable projection files yield '' during matching so one broken path
    cannot poison ranking for the whole corpus. (The winner's explanation
    read below stays strict: a broken winning path surfaces loudly.)
    """
    try:
        note = (ROOT / str(projection_path)).read_text(encoding="utf-8")
    except (OSError, TypeError):
        return ""
    m = re.search(r"##(?:\s+[^\n]*)?IN A NUTSHELL\n\n(.+?)(?:\n\n##|$)", note, re.S | re.I)
    return m.group(1).strip() if m else ""

def retrieve(query):
    registry = load_json(REGISTRY)
    q_raw = re.findall(r"[a-z0-9]+", query.lower())
    q = set(_stem(w) for w in q_raw)
    q_phrase = " ".join(q_raw)
    ranked = []
    inactive = {"SUPERSEDED", "ARCHIVED", "REVOKED"}
    # Field weights (retrieval 10/10 track, 2026-10-06): a query term in the
    # title is stronger relevance evidence than in keywords. Weights were
    # chosen so the #1630 boundary tests still hold: relevance dominates,
    # authority breaks ties, zero-relevance never wins.
    for e in registry.get("entries", []):
        if str(e.get("lifecycle_state", "ACTIVE")).upper() in inactive:
            continue
        title = e.get("title", "")
        nutshell = _nutshell_text(e.get("projection_path", ""))
        keywords = " ".join(e.get("keywords", []))
        taxonomy = " ".join([e.get("category", ""), e.get("topic", ""), e.get("subtopic", "")])
        # Lesson-content matching (retrieval track, 2026-10-06): capture stamps
        # every note with the same generic keywords, so the metadata haystack
        # cannot distinguish lessons. Content-word queries ("declaring intent
        # before acting") retrieved wrong notes. Include each note's own
        # distilled lesson (NUTSHELL) in the haystack.
        score = 0.0
        score += len(q & _field_words(title)) * 3.0
        score += len(q & _field_words(nutshell)) * 2.0
        score += len(q & _field_words(keywords)) * 1.5
        score += len(q & _field_words(taxonomy)) * 1.0
        # Phrase bonus: the query as an exact phrase in title or lesson
        # content is strong relevance signal (not just scattered words).
        if q_phrase and (q_phrase in title.lower() or q_phrase in nutshell.lower()):
            score += 2.0
        if score <= 0:
            # Authority never promotes irrelevance: a note matching zero
            # query terms cannot win on truth-state rank alone.
            continue
        rank = TRUTH_STATE_RANK.get(str(e.get("truth_state", "")).upper(), 0)
        # Boundary (investigated 2026-10-06, Naya 4): relevance dominates,
        # authority breaks ties. An additive authority bonus was built and
        # FALSIFIED on the live corpus: RATIFIED+2 promoted SN-016
        # ("Judgment Rule") over SN-041 ("Discernment-to-Compounding") for
        # the query "compounding proof" — true but irrelevant intelligence
        # wearing authority is misdirection, and it is worse than a
        # relevant CANDIDATE whose uncertainty is visible. A 1-2 keyword
        # gap at these score magnitudes (1-3) is signal, not noise.
        ranked.append((score, rank, e))
    ranked.sort(key=lambda z: (z[0], z[1], z[2].get("captured_at","")), reverse=True)
    if not ranked:
        raise SystemExit("NO_RELEVANT_INTELLIGENCE")
    e = ranked[0][2]
    note = (ROOT / e["projection_path"]).read_text(encoding="utf-8")
    m = re.search(r"##(?:\s+[^\n]*)?IN A NUTSHELL\n\n(.+?)(?:\n\n##|$)", note, re.S | re.I)
    explanation = m.group(1).strip() if m else ""
    return {"query":query,"retrieved":e,"explanation":explanation,"source":"repository_projection_index","original_conversation_supplied":False}

def held_out(retrieved):
    task = "A future developer proposes creating one new Naya Node for every important conversation and storing the raw transcript as the canonical brain memory. Decide the architecture."
    control = {"task":task,"context":"No Smart Note intelligence supplied.","decision":"INSUFFICIENT_CANONICAL_CONTEXT","creates_new_node":None,"raw_transcript_is_canonical":None}
    note = (ROOT / retrieved["retrieved"]["projection_path"]).read_text(encoding="utf-8")
    low = note.lower()
    keep_block = ("do not create naya nodes per note" in low) or ("does not become a master node" in low) or ("do not create another naya node" in low)
    raw_separate = ("raw_source_separate_from_distillation" in low and "true" in low) or ("transcript" in low and "not intelligence" in low)
    treatment = {
        "task":task,
        "context_intelligent_block_id":retrieved["retrieved"]["intelligent_block_id"],
        "decision":"USE_INTELLIGENT_BLOCK_AND_SEPARATE_SOURCE" if keep_block and raw_separate else "UNRESOLVED",
        "creates_new_node":False if keep_block else None,
        "raw_transcript_is_canonical":False if raw_separate else None,
        "reason":"Retrieved Smart Note requires Intelligent Blocks as durable units and preserves raw source separately from distilled intelligence."
    }
    return {"schema":"naya.smart-note-held-out-behavior.v1","control":control,"treatment":treatment,"behavior_changed":control["decision"] != treatment["decision"] and treatment["decision"] == "USE_INTELLIGENT_BLOCK_AND_SEPARATE_SOURCE","task_was_not_original_capture_prompt":True}

# ============================================================================
# PROMOTION WRITER
# ============================================================================
# Implements the CANDIDATE -> VERIFIED state transition for the Smart Note
# epistemic ladder.
#
# CONTEXT (NayaPOWER Final Exam, 2026-10-04): The write path hardcodes every
# block to CANDIDATE. The governed read path refuses CANDIDATE. No code
# anywhere transitioned between them. The entire KNOW/LEARN machinery was
# decorative until this function existed.
#
# DESIGN PRINCIPLES:
# 1. No self-certification: the promoter cannot be the sole evidence gatherer.
# 2. No circular evidence: a note cannot verify itself.
# 3. Every decision is auditable: a second party can re-verify from the
#    receipt alone, without trusting the promoter.
# 4. Fail closed: any threshold miss = stay CANDIDATE + refusal record.
# ============================================================================

from datetime import datetime, timezone

PROMOTION_THRESHOLD_VERSION = "v1"

# Valid evidence types. Each represents a distinct way of knowing.
EVIDENCE_TYPES = {
    "independent_verification",  # A second party independently checked the claim
    "behavioral_test",           # A test demonstrated the claimed behavior
    "human_ratification",        # The Human Director explicitly ratified
    "cross_reference",           # External source corroborates the claim
    "reproduction",              # An independent party reproduced the result
}

# --- Threshold definitions (v1) ---
# Each threshold is documented with its rationale. These are the initial
# values; they are versioned (PROMOTION_THRESHOLD_VERSION) so tightening or
# loosening them is an explicit, auditable change.

THRESHOLDS_V1 = {
    # Minimum number of evidence items. Rationale: one item is a single point
    # of failure. Two is the minimum for corroboration.
    "min_evidence_count": 2,

    # Minimum distinct gatherers. Rationale: prevents a single party from
    # manufacturing consensus with themselves.
    "min_distinct_gatherers": 2,

    # The promoter may not be among the gatherers. Rationale: this is the
    # anti-self-certification rule. The exam found `independent_verification:
    # true` as a hardcoded literal — this rule makes that impossible.
    "promoter_may_not_gather": True,

    # Minimum distinct evidence types. Rationale: prevents gaming by
    # submitting the same weak evidence type twice.
    "min_distinct_types": 2,

    # Maximum age of evidence in days. Rationale: stale evidence may not
    # reflect current truth. 90 days is a judgment call — long enough for
    # durable knowledge, short enough to catch drift.
    "max_evidence_age_days": 90,

    # Every evidence item must carry a content hash. Rationale: without it,
    # the evidence cannot be independently verified from the receipt.
    "require_content_hash": True,
}

# Where promotion receipts and refusals are stored, relative to repo root.
PROMOTION_LOG_DIR = Path(".naya") / "memory" / "smart-notes" / "promotions"


def _utc_now():
    return datetime.now(timezone.utc).isoformat()


def _hash_receipt(receipt):
    """Compute the integrity hash of a receipt (excluding its own hash field)."""
    clean = {k: v for k, v in receipt.items() if k != "receipt_hash"}
    canonical = json.dumps(clean, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _parse_ts(ts):
    """Parse an ISO timestamp, return datetime or None."""
    try:
        dt = datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except (ValueError, TypeError):
        return None


def validate_evidence_bundle(note_id, evidence, promoter):
    """Run all threshold checks. Returns (passed: bool, failures: list).

    Each failure is a dict with 'check' and 'detail'. Empty failures = pass.
    """
    failures = []
    note_id_up = str(note_id).upper()

    # Check 1: non-empty bundle
    if not evidence:
        failures.append({
            "check": "non_empty_bundle",
            "detail": "Evidence bundle is empty. Promotion requires at least "
                      f"{THRESHOLDS_V1['min_evidence_count']} evidence items.",
        })
        return False, failures  # Cannot evaluate further

    # Check 2: minimum count
    if len(evidence) < THRESHOLDS_V1["min_evidence_count"]:
        failures.append({
            "check": "min_evidence_count",
            "detail": f"Found {len(evidence)} items, need "
                      f"{THRESHOLDS_V1['min_evidence_count']}.",
        })

    # Check 3: content hashes present
    if THRESHOLDS_V1["require_content_hash"]:
        missing = [i for i, e in enumerate(evidence) if not e.get("content_hash")]
        if missing:
            failures.append({
                "check": "content_hash_required",
                "detail": f"Evidence items at indices {missing} lack content_hash.",
            })

    # Check 4: valid evidence types
    bad_types = [(i, e.get("type")) for i, e in enumerate(evidence)
                 if str(e.get("type", "")).lower() not in EVIDENCE_TYPES]
    if bad_types:
        failures.append({
            "check": "valid_evidence_types",
            "detail": f"Invalid types at indices {[i for i, _ in bad_types]}: "
                      f"{[t for _, t in bad_types]}. Valid: {sorted(EVIDENCE_TYPES)}.",
        })

    # Check 5: type diversity
    types = {str(e.get("type", "")).lower() for e in evidence if e.get("type")}
    if len(types) < THRESHOLDS_V1["min_distinct_types"]:
        failures.append({
            "check": "type_diversity",
            "detail": f"Found {len(types)} distinct types, need "
                      f"{THRESHOLDS_V1['min_distinct_types']}.",
        })

    # Check 6: gatherer independence (no self-certification)
    gatherers = {str(e.get("gatherer", "")).strip() for e in evidence if e.get("gatherer")}
    gatherers.discard("")
    promoter_norm = str(promoter).strip()
    if THRESHOLDS_V1["promoter_may_not_gather"] and promoter_norm in gatherers:
        failures.append({
            "check": "no_self_certification",
            "detail": f"Promoter '{promoter_norm}' is also an evidence gatherer. "
                      "The promoter cannot certify their own promotion.",
        })
    if len(gatherers) < THRESHOLDS_V1["min_distinct_gatherers"]:
        failures.append({
            "check": "gatherer_independence",
            "detail": f"Found {len(gatherers)} distinct gatherers, need "
                      f"{THRESHOLDS_V1['min_distinct_gatherers']}.",
        })

    # Check 7: no self-referential evidence
    now = datetime.now(timezone.utc)
    for i, e in enumerate(evidence):
        ref = str(e.get("note_ref", "")).upper()
        if ref and (ref == note_id_up or ref.replace("-", "") == note_id_up.replace("-", "")):
            failures.append({
                "check": "no_self_reference",
                "detail": f"Evidence item {i} cites the note being promoted "
                          f"({e.get('note_ref')}). Circular evidence rejected.",
            })

    # Check 8: evidence freshness
    max_age = THRESHOLDS_V1["max_evidence_age_days"]
    for i, e in enumerate(evidence):
        ts = _parse_ts(e.get("gathered_at"))
        if ts is None:
            failures.append({
                "check": "evidence_freshness",
                "detail": f"Evidence item {i} has unparseable timestamp: "
                          f"{e.get('gathered_at')}.",
            })
        elif (now - ts).days > max_age:
            failures.append({
                "check": "evidence_freshness",
                "detail": f"Evidence item {i} is {(now - ts).days} days old, "
                          f"max is {max_age}.",
            })

    return (len(failures) == 0), failures


def _write_record(record, note_id, kind):
    """Write a promotion receipt or refusal record. Returns the file path."""
    log_dir = ROOT / PROMOTION_LOG_DIR
    log_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    safe_id = re.sub(r"[^A-Za-z0-9-]", "_", str(note_id))
    path = log_dir / f"{ts}-{safe_id}-{kind}.json"
    path.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def promote_note(note_id, evidence_bundle, promoter, registry_path=None):
    """Attempt to promote a CANDIDATE note to VERIFIED.

    Args:
        note_id: Smart Note ID (e.g. "SN-012") or Intelligent Block ID.
        evidence_bundle: List of evidence dicts. Each must have:
            type, source, content_hash, gatherer, gathered_at.
            Optional: note_ref (for cross-references).
        promoter: Identity string of the party requesting promotion.
        registry_path: Path to index.json. Defaults to the canonical registry.

    Returns:
        dict with: promoted (bool), receipt_or_refusal, record_path.

    Side effects on PASS:
        - Registry entry truth_state: CANDIDATE -> VERIFIED
        - Promotion receipt written to .naya/memory/smart-notes/promotions/
    Side effects on FAIL:
        - Refusal record written (note stays CANDIDATE)
    """
    reg_path = Path(registry_path) if registry_path else REGISTRY
    if not reg_path.exists():
        raise SystemExit(f"PROMOTION_REGISTRY_NOT_FOUND: {reg_path}")

    registry = json.loads(reg_path.read_text(encoding="utf-8"))
    entries = registry.get("entries", [])

    # Find the note by SN ID or IB ID
    nid_up = str(note_id).upper()
    entry = None
    for e in entries:
        if str(e.get("smart_note_id", "")).upper() == nid_up:
            entry = e
            break
    if entry is None:
        for e in entries:
            if str(e.get("intelligent_block_id", "")).upper() == nid_up:
                entry = e
                break
    if entry is None:
        raise SystemExit(f"PROMOTION_NOTE_NOT_FOUND: {note_id}")

    current_state = str(entry.get("truth_state", "CANDIDATE")).upper()
    if current_state != "CANDIDATE":
        # Already promoted (or ratified) — refuse to re-promote
        refusal = {
            "schema": "naya.promotion-refusal.v1",
            "note_id": entry.get("smart_note_id"),
            "intelligent_block_id": entry.get("intelligent_block_id"),
            "promoter": promoter,
            "refused_at": _utc_now(),
            "threshold_version": PROMOTION_THRESHOLD_VERSION,
            "reason_code": "NOT_CANDIDATE",
            "reason_detail": f"Note is already {current_state}. Only CANDIDATE notes can be promoted.",
            "failed_checks": [{"check": "is_candidate", "detail": f"truth_state is {current_state}"}],
        }
        refusal["receipt_hash"] = _hash_receipt(refusal)
        rp = _write_record(refusal, entry.get("smart_note_id"), "refusal")
        return {"promoted": False, "record": refusal, "record_path": str(rp)}

    # Run threshold checks
    passed, failures = validate_evidence_bundle(
        entry.get("smart_note_id"), evidence_bundle, promoter
    )

    if not passed:
        # Map failures to a reason code (first critical failure wins)
        code_map = {
            "non_empty_bundle": "EMPTY_EVIDENCE",
            "no_self_certification": "SELF_CERTIFICATION",
            "no_self_reference": "SELF_REFERENTIAL",
            "gatherer_independence": "INSUFFICIENT_INDEPENDENCE",
            "evidence_freshness": "STALE_EVIDENCE",
        }
        reason_code = "INSUFFICIENT_EVIDENCE"
        for f in failures:
            if f["check"] in code_map:
                reason_code = code_map[f["check"]]
                break
        refusal = {
            "schema": "naya.promotion-refusal.v1",
            "note_id": entry.get("smart_note_id"),
            "intelligent_block_id": entry.get("intelligent_block_id"),
            "promoter": promoter,
            "refused_at": _utc_now(),
            "threshold_version": PROMOTION_THRESHOLD_VERSION,
            "reason_code": reason_code,
            "reason_detail": "; ".join(f["detail"] for f in failures),
            "failed_checks": failures,
        }
        refusal["receipt_hash"] = _hash_receipt(refusal)
        rp = _write_record(refusal, entry.get("smart_note_id"), "refusal")
        return {"promoted": False, "record": refusal, "record_path": str(rp)}

    # PASS — promote
    gatherers = sorted({str(e.get("gatherer", "")).strip() for e in evidence_bundle if e.get("gatherer")})
    receipt = {
        "schema": "naya.promotion-receipt.v1",
        "note_id": entry.get("smart_note_id"),
        "intelligent_block_id": entry.get("intelligent_block_id"),
        "old_state": "CANDIDATE",
        "new_state": "VERIFIED",
        "promoter": promoter,
        "promoted_at": _utc_now(),
        "threshold_version": PROMOTION_THRESHOLD_VERSION,
        "thresholds_applied": THRESHOLDS_V1,
        "evidence_hashes": [e.get("content_hash") for e in evidence_bundle],
        "evidence_count": len(evidence_bundle),
        "evidence_types": sorted({str(e.get("type", "")).lower() for e in evidence_bundle}),
        "gatherers": gatherers,
    }
    receipt["receipt_hash"] = _hash_receipt(receipt)

    # Update registry inside an exclusive transaction (Problem B fix):
    # re-read under the lock, re-find the entry, mutate, atomic commit.
    # Concurrent promotions serialize; the VERIFIED mutation is idempotent.
    with registry_transaction(reg_path) as locked_registry:
        locked_entry = None
        for e in locked_registry.get("entries", []):
            if str(e.get("smart_note_id", "")).upper() == nid_up:
                locked_entry = e
                break
        if locked_entry is None:
            for e in locked_registry.get("entries", []):
                if str(e.get("intelligent_block_id", "")).upper() == nid_up:
                    locked_entry = e
                    break
        if locked_entry is None:
            raise SystemExit(f"PROMOTION_NOTE_NOT_FOUND: {note_id}")
        locked_entry["truth_state"] = "VERIFIED"
        locked_entry["promotion_receipt"] = {
            "promoted_at": receipt["promoted_at"],
            "promoter": promoter,
            "receipt_hash": receipt["receipt_hash"],
            "threshold_version": PROMOTION_THRESHOLD_VERSION,
        }

    rp = _write_record(receipt, entry.get("smart_note_id"), "receipt")
    return {"promoted": True, "record": receipt, "record_path": str(rp)}


def verify_receipt(receipt, evidence_bundle):
    """Independently re-verify a promotion receipt.

    A second party calls this with the receipt and the original evidence
    bundle. Returns (valid: bool, detail: str).

    This is the audit function — it recomputes the decision from the
    receipt's recorded inputs, without trusting the promoter.
    """
    # 1. Receipt integrity
    if receipt.get("receipt_hash") != _hash_receipt(receipt):
        return False, "Receipt hash mismatch — receipt has been tampered with."

    # 2. Schema version
    if receipt.get("schema") != "naya.promotion-receipt.v1":
        return False, f"Unknown receipt schema: {receipt.get('schema')}"

    # 3. Evidence hashes match
    bundle_hashes = [e.get("content_hash") for e in evidence_bundle]
    if bundle_hashes != receipt.get("evidence_hashes"):
        return False, "Evidence bundle does not match receipt's recorded hashes."

    # 4. Re-run threshold checks with receipt's recorded promoter
    passed, failures = validate_evidence_bundle(
        receipt.get("note_id"), evidence_bundle, receipt.get("promoter")
    )
    if not passed:
        return False, f"Re-validation failed: {[f['check'] for f in failures]}"

    # 5. State transition is valid
    if receipt.get("old_state") != "CANDIDATE" or receipt.get("new_state") != "VERIFIED":
        return False, "Invalid state transition in receipt."

    return True, "Receipt verified: promotion was valid under recorded thresholds."


def audit_registry(root=None, registry_path=None, capture_dir=None, brain_root=None):
    """Reconcile captures, the machine registry, and published Brain projections.

    Reconciles bidirectionally so a green publish run cannot hide drift. The
    publish path only ever proves the single note it just handled; it never
    compares every historical capture against the registry. That gap lets a
    fully green run coexist with a corrupted registry, which is why this audit
    exists as a separate whole-surface check.

    Hashing reuses _canonical_content_hash so this stays a single authority
    rather than a second, independently drifting hash implementation.
    """
    root = Path(root) if root else ROOT
    registry_p = Path(registry_path) if registry_path else root / ".naya" / "memory" / "smart-notes" / "index.json"
    cap_dir = Path(capture_dir) if capture_dir else root / ".naya" / "capture"
    brain = Path(brain_root) if brain_root else root / "BRAIN" / "05-MEMORY" / "SMART-NOTES"

    defects = {
        "unparseable_captures": [],
        "captures_missing_intelligence": [],
        "captures_unregistered_by_hash": [],
        "entries_without_hash": [],
        "entries_with_stale_hash": [],
        "duplicate_smart_note_ids": [],
        "published_entries_missing_projection_path": [],
        "registry_projection_paths_absent": [],
        "published_pages_without_registry_entry": [],
        "duplicate_published_page_paths": [],
    }

    registry = load_json(registry_p) if registry_p.exists() else {"entries": []}
    entries = registry.get("entries", [])

    def hash_of(data):
        return _canonical_content_hash(json.dumps(data["intelligence"], sort_keys=True, separators=(",", ":"), ensure_ascii=False))

    capture_by_hash = {}
    if cap_dir.exists():
        for p in sorted(cap_dir.glob("*.json")):
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
            except ValueError:
                defects["unparseable_captures"].append(p.name)
                continue
            if not isinstance(data.get("intelligence"), dict):
                defects["captures_missing_intelligence"].append(p.name)
                continue
            capture_by_hash[hash_of(data)] = p.name

    entry_hashes = {}
    for e in entries:
        sn = e.get("smart_note_id") or e.get("intelligent_block_id") or "<unknown>"
        h = e.get("content_hash")
        if not h:
            defects["entries_without_hash"].append(sn)
            continue
        entry_hashes.setdefault(h, []).append(sn)
        if h not in capture_by_hash:
            defects["entries_with_stale_hash"].append({"smart_note_id": sn, "content_hash": h})

    for h, names in entry_hashes.items():
        if len(names) > 1:
            defects["duplicate_smart_note_ids"].append(sorted(names))

    for h, name in capture_by_hash.items():
        if h not in entry_hashes:
            defects["captures_unregistered_by_hash"].append(name)

    for e in entries:
        sn = e.get("smart_note_id") or e.get("intelligent_block_id") or "<unknown>"
        published = e.get("projection_status") == "GITHUB_BRAIN_PUBLISHED"
        pp = e.get("projection_path")
        if published and not pp:
            defects["published_entries_missing_projection_path"].append(sn)
        if pp and not (root / pp).exists():
            defects["registry_projection_paths_absent"].append({"smart_note_id": sn, "projection_path": pp})

    pages_by_name = {}
    if brain.exists():
        for p in sorted(brain.rglob("*.md")):
            pages_by_name.setdefault(p.name, []).append(str(p.relative_to(root)).replace("\\", "/"))
    for name, paths in sorted(pages_by_name.items()):
        if len(paths) > 1:
            defects["duplicate_published_page_paths"].append({"page": name, "paths": paths})

    known_pages = {f"{e.get('intelligent_block_id')}.md" for e in entries if e.get("intelligent_block_id")}
    for name, paths in sorted(pages_by_name.items()):
        if name not in known_pages:
            defects["published_pages_without_registry_entry"].append({"page": name, "paths": paths})

    counts = {k: len(v) for k, v in defects.items()}
    return {
        "ok": sum(counts.values()) == 0,
        "counts": counts,
        "defect_total": sum(counts.values()),
        "defects": defects,
        "surfaces": {
            "captures_on_disk": len(capture_by_hash),
            "registry_entries": len(entries),
            "published_pages_on_disk": sum(len(v) for v in pages_by_name.values()),
        },
    }


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("discover"); d.add_argument("paths", nargs="*")
    mg = sub.add_parser("migrate"); mg.add_argument("--existing", required=True); mg.add_argument("--patch", required=True); mg.add_argument("--out", required=True); mg.add_argument("--receipt", required=True)
    pr = sub.add_parser("project"); pr.add_argument("--capture", required=True); pr.add_argument("--verify", required=True); pr.add_argument("--private-root")
    r = sub.add_parser("retrieve"); r.add_argument("--query", required=True); r.add_argument("--out")
    h = sub.add_parser("held-out"); h.add_argument("--retrieval", required=True); h.add_argument("--out", required=True)
    pm = sub.add_parser("promote"); pm.add_argument("--note", required=True); pm.add_argument("--evidence", required=True); pm.add_argument("--promoter", required=True); pm.add_argument("--registry"); pm.add_argument("--out")
    a = sub.add_parser("audit"); a.add_argument("--root"); a.add_argument("--quiet", action="store_true")
    args = ap.parse_args()
    if args.cmd == "audit":
        report = audit_registry(root=args.root)
        print(json.dumps(report, indent=2, ensure_ascii=False) if not args.quiet else ("ok" if report["ok"] else f"DRIFT:{report['defect_total']}"))
        raise SystemExit(0 if report["ok"] else 1)
    if args.cmd == "migrate":
        x = migrate_capture_file(args.existing, args.patch, args.out, args.receipt)
        print(json.dumps({"output": args.out, "receipt": args.receipt, "removed_paths": x["receipt"]["removed_paths"]}, ensure_ascii=False))
        return
    if args.cmd == "discover":
        for path in changed_capture(args.paths, existing_only=True):
            print(path)
        return
    if args.cmd == "project":
        cap = load_json(args.capture); ver = load_json(args.verify)
        block = ver["persisted"]["block"]
        ib = block["intelligent_block_id"]
        # Reserve the SN authoritatively BEFORE rendering: the projected
        # directory is derived from the reserved ID, so concurrent
        # projectors can never pick the same directory (projection-path
        # race). The reservation commits inside its own short transaction;
        # rendering itself stays concurrent (no lock held across file I/O).
        sn_id = reserve_smart_note_id(cap, ib)
        p = render(cap, ver, args.private_root, sn_id=sn_id)
        published = str(p).startswith(str(BRAIN_SMART_NOTE_ROOT))
        entry = update_registry(cap, ver, p, sn_id=sn_id) if published else {
            "intelligent_block_id": ib,
            "smart_note_id": sn_id,
            "scope": block.get("owner_scope"),
            "projection_status": "PRIVATE_RENDER_VERIFIED",
            "smart_link_status": "PENDING_PRIVATE_PROJECTION",
            "private_render_path": str(p)
        }
        print(json.dumps({"projection_path":str(p),"entry":entry}, ensure_ascii=False)); return
    if args.cmd == "retrieve":
        x = retrieve(args.query)
        if args.out:
            Path(args.out).write_text(json.dumps(x, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(json.dumps(x, ensure_ascii=False)); return
    if args.cmd == "held-out":
        x = held_out(load_json(args.retrieval))
        Path(args.out).write_text(json.dumps(x, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(json.dumps(x, ensure_ascii=False)); return
    if args.cmd == "promote":
        bundle = load_json(args.evidence)
        # Accept either a raw list or {"evidence": [...]}
        ev = bundle.get("evidence", bundle) if isinstance(bundle, dict) else bundle
        x = promote_note(args.note, ev, args.promoter, args.registry)
        if args.out:
            Path(args.out).write_text(json.dumps(x["record"], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(json.dumps({"promoted": x["promoted"], "reason": x["record"].get("reason_code", "PROMOTED"), "record_path": x["record_path"]}, ensure_ascii=False)); return

if __name__ == "__main__":
    main()
