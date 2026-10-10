"""LEARN node: the inheritance mechanism.

Shawn's law: verified lessons are frozen at 10 and every new Naya is BORN
with them — not taught, inherited.

LEARN does three things:
1. ADMIT: takes a VERIFY-admitted lesson and freezes it into the durable
   knowledge set with full provenance (what it is, why it's trusted, what
   version, what it supersedes). ONLY lessons VERIFY admitted as CANDIDATE
   are admitted. Rejected lessons, NOT_VERIFIED nulls, and raw candidates
   are refused LOUDLY — they can never enter the usable set.
2. SERVE: given a fresh decision context, retrieves applicable lessons BY
   INTENT (situation overlap, not ID lookup). The lesson arrives without
   the original instruction being repeated. Every serving is recorded.
3. INHERIT: the store is durable and file-based. A new LearnNode(store_path)
   loads every admitted lesson — a new Naya is born with them. The fresh
   instance never saw the admission; it inherits the frozen result.

What this is NOT:
- Not a database lookup by ID. serve() matches on intent signature overlap.
- Not a candidate store. Candidates are never servable (proven by test).
- Not the application proof. LEARN admits + serves with the record; whether
  a decision actually APPLIED the lesson is WO4/WO5b territory (the serving
  record is the handoff point).
- Not semantic understanding. Intent matching is structured keyword/domain
  overlap with a scored threshold — honest, testable, and explicit about
  what it is.

Laws honored here:
- Only admitted lessons enter. Admission is checked, not claimed.
- Lessons are frozen (immutable) once admitted. Corrections arrive as new
  versions that supersede; history is never rewritten.
- No silent anything. Refusals name the reason. Ignored store files are
  reported, not silently skipped.
- Idempotent admit: admitting the same lesson twice yields one record.
- Atomic writes: a crash can never leave a half-written lesson.
"""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


LEARN_SCHEMA = "NAYAPOWER_LEARN_ADMITTED_LESSON_V1"

# The only VERIFY outcome LEARN accepts. A NOT_VERIFIED null is honest
# negative evidence, but it is not a lesson to inherit and apply — it
# belongs in the verification record, not the active lesson set.
# A REJECTED candidate failed the gate. Anything else never saw the gate.
REQUIRED_ADMITTED_AS = "CANDIDATE"

# Intent-match threshold: a lesson is served when the weighted overlap
# between the decision context's intent and the lesson's intent signature
# reaches this score (0.0–1.0).
SERVE_THRESHOLD = 0.5


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def _atomic_write(path: Path, payload: dict) -> None:
    """Write-temp-then-rename. A crash can never leave a half-written file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, sort_keys=True)
            f.write("\n")
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def _atomic_write_bytes(path: Path, payload: bytes) -> None:
    """Atomic write for raw bytes (Smart App release artifacts)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(payload)
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def _safe_filename(value: str) -> str:
    return "".join(c for c in value if c.isalnum() or c in ("_", "-", "."))


# --------------------------------------------------------------------------
# Records
# --------------------------------------------------------------------------

@dataclass
class AdmittedLesson:
    """A frozen lesson in the usable knowledge set."""

    schema: str
    lesson_id: str
    version: int
    lesson_text: str
    intent_signature: dict[str, Any]
    provenance: dict[str, Any]
    supersedes: str | None
    superseded_by: str | None
    frozen: bool
    status: str  # ACTIVE | SUPERSEDED
    admitted_at: str
    checksum: str
    # Optional: when this lesson IS a qualified Smart App (PR #2086 preflight
    # format), the package metadata lives here and the exact release bytes
    # live in <store>/smart_apps/<artifact_id>.v<version>/release.bin.
    # The content_sha256 in smart_app MUST match the stored bytes — verified
    # by verify_smart_app(), never claimed.
    smart_app: dict[str, Any] | None = None

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "AdmittedLesson":
        return cls(
            schema=d["schema"],
            lesson_id=d["lesson_id"],
            version=d["version"],
            lesson_text=d["lesson_text"],
            intent_signature=d["intent_signature"],
            provenance=d["provenance"],
            supersedes=d.get("supersedes"),
            superseded_by=d.get("superseded_by"),
            frozen=d["frozen"],
            status=d["status"],
            admitted_at=d["admitted_at"],
            checksum=d["checksum"],
            smart_app=d.get("smart_app"),
        )


@dataclass
class ServingRecord:
    """Proof that lessons were provided to a decision context."""

    serve_id: str
    served_at: str
    decision_correlation_id: str
    context_intent: dict[str, Any]
    lessons_served: list[dict[str, Any]]  # [{lesson_id, version, match_score, provenance}]
    lessons_considered: int
    lessons_below_threshold: int

    def to_dict(self) -> dict:
        return asdict(self)


class LearnAdmissionRefused(Exception):
    """Raised when admit() is called with anything but a VERIFY-admitted lesson."""

    def __init__(self, reason_code: str, detail: str):
        super().__init__(f"LEARN_ADMISSION_REFUSED [{reason_code}]: {detail}")
        self.reason_code = reason_code
        self.detail = detail


# Reason codes for refusal (machine-readable, like the VERIFY gate).
NOT_A_VERIFY_RESULT = "NOT_A_VERIFY_RESULT"
VERIFY_DID_NOT_ADMIT = "VERIFY_DID_NOT_ADMIT"
NOT_A_LESSON_CANDIDATE = "NOT_A_LESSON_CANDIDATE"
LESSON_ID_REQUIRED = "LESSON_ID_REQUIRED"
LESSON_TEXT_REQUIRED = "LESSON_TEXT_REQUIRED"
INTENT_SIGNATURE_REQUIRED = "INTENT_SIGNATURE_REQUIRED"
# Smart App package reason codes (PR #2086 preflight subset).
SMART_APP_VERSION_INVALID = "SMART_APP_VERSION_INVALID"
SMART_APP_HASH_INVALID = "SMART_APP_HASH_INVALID"
SMART_APP_HASH_MISMATCH = "SMART_APP_HASH_MISMATCH"
SMART_APP_PROOF_MISSING = "SMART_APP_PROOF_MISSING"
SMART_APP_BYTES_REQUIRED = "SMART_APP_BYTES_REQUIRED"


# --------------------------------------------------------------------------
# Intent matching
# --------------------------------------------------------------------------

def _normalize_terms(value: Any) -> set[str]:
    """Lowercased token set from a string or list of strings."""
    if isinstance(value, str):
        items = [value]
    elif isinstance(value, (list, tuple)):
        items = [str(i) for i in value]
    else:
        return set()
    terms: set[str] = set()
    for item in items:
        for tok in item.lower().replace("/", " ").replace("-", " ").split():
            tok = "".join(c for c in tok if c.isalnum())
            if tok:
                terms.add(tok)
    return terms


def intent_match_score(lesson_signature: dict[str, Any], context_intent: dict[str, Any]) -> float:
    """Weighted intent overlap between a lesson and a decision context.

    0.0 = no overlap, 1.0 = full overlap. This is structured keyword/domain
    matching — NOT semantic understanding. The score is honest about that:
    it measures declared-intent overlap, nothing more.
    """
    if not isinstance(lesson_signature, dict) or not isinstance(context_intent, dict):
        return 0.0

    score = 0.0
    weight_total = 0.0

    # Domain overlap (weight 0.4): is this lesson for this kind of work?
    lesson_domains = _normalize_terms(lesson_signature.get("domains"))
    context_domains = _normalize_terms(context_intent.get("domains"))
    if lesson_domains or context_domains:
        weight_total += 0.4
        if lesson_domains and context_domains:
            overlap = lesson_domains & context_domains
            union = lesson_domains | context_domains
            score += 0.4 * (len(overlap) / len(union))

    # Situation overlap (weight 0.4): does this situation match?
    lesson_situations = _normalize_terms(lesson_signature.get("situations"))
    context_situation = _normalize_terms(context_intent.get("situation"))
    context_keywords = _normalize_terms(context_intent.get("situation_keywords"))
    context_terms = context_situation | context_keywords
    if lesson_situations or context_terms:
        weight_total += 0.4
        if lesson_situations and context_terms:
            overlap = lesson_situations & context_terms
            # Recall-oriented: what fraction of the lesson's situations appear
            # in the context? A lesson covering this situation should fire.
            score += 0.4 * (len(overlap) / len(lesson_situations))

    # Decision-type overlap (weight 0.2): does this lesson inform this decision?
    lesson_decisions = _normalize_terms(lesson_signature.get("decision_types"))
    context_decision = _normalize_terms(context_intent.get("decision_type"))
    if lesson_decisions or context_decision:
        weight_total += 0.2
        if lesson_decisions and context_decision and (lesson_decisions & context_decision):
            score += 0.2

    if weight_total == 0.0:
        return 0.0
    # Normalize by the weights actually in play.
    return round(score / weight_total if weight_total else 0.0, 4)


# --------------------------------------------------------------------------
# LearnNode
# --------------------------------------------------------------------------

class LearnNode:
    """The inheritance mechanism: admit VERIFY-passed lessons, serve by intent.

    The store is a directory:
      <store>/lessons/<lesson_id>.v<version>.json   — frozen admitted lessons
      <store>/servings.jsonl                        — append-only serving log
      <store>/quarantine/                           — files that failed validation

    A new LearnNode on an existing store inherits every admitted lesson.
    """

    def __init__(self, store_path: str | Path):
        self.store_path = Path(store_path)
        self.lessons_dir = self.store_path / "lessons"
        self.quarantine_dir = self.store_path / "quarantine"
        self.servings_log = self.store_path / "servings.jsonl"
        self.smart_apps_dir = self.store_path / "smart_apps"
        self.lessons_dir.mkdir(parents=True, exist_ok=True)
        self.quarantine_dir.mkdir(parents=True, exist_ok=True)
        self.smart_apps_dir.mkdir(parents=True, exist_ok=True)
        # Inheritance: load everything already admitted. A new instance is
        # born with the lessons — it never saw the admissions happen.
        self._lessons: dict[str, AdmittedLesson] = {}
        self.ignored_files: list[str] = []
        self._load()

    # -- loading (inheritance) ------------------------------------------

    def _load(self) -> None:
        for path in sorted(self.lessons_dir.glob("*.json")):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError) as exc:
                self._quarantine(path, f"unreadable: {exc}")
                continue
            lesson = self._validate_stored(data, path.name)
            if lesson is None:
                continue
            # Verify the checksum: the file must be exactly what admit() wrote.
            if not self._checksum_ok(lesson):
                self._quarantine(path, "checksum mismatch: file was modified after admission")
                continue
            key = f"{lesson.lesson_id}.v{lesson.version}"
            self._lessons[key] = lesson

    def _validate_stored(self, data: dict, filename: str) -> AdmittedLesson | None:
        """A stored file is only loadable if it carries full admission proof.

        This is the negative-test seam: a raw candidate dropped into the
        store has no admission provenance and is NOT loaded — therefore
        never served.
        """
        if not isinstance(data, dict):
            self._quarantine_name(filename, "not a JSON object")
            return None
        if data.get("schema") != LEARN_SCHEMA:
            self._quarantine_name(filename, f"schema != {LEARN_SCHEMA} (no admission proof)")
            return None
        if data.get("frozen") is not True:
            self._quarantine_name(filename, "not frozen (no admission proof)")
            return None
        provenance = data.get("provenance")
        if not isinstance(provenance, dict):
            self._quarantine_name(filename, "no provenance (no admission proof)")
            return None
        if provenance.get("admitted_by") != "VERIFY":
            self._quarantine_name(filename, "not admitted by VERIFY")
            return None
        if provenance.get("admitted_as") != REQUIRED_ADMITTED_AS:
            self._quarantine_name(filename, f"admitted_as != {REQUIRED_ADMITTED_AS}")
            return None
        try:
            return AdmittedLesson.from_dict(data)
        except (KeyError, TypeError) as exc:
            self._quarantine_name(filename, f"malformed lesson record: {exc}")
            return None

    def _quarantine(self, path: Path, reason: str) -> None:
        dest = self.quarantine_dir / f"{path.name}.quarantined"
        try:
            path.rename(dest)
        except OSError:
            pass
        self.ignored_files.append(f"{path.name}: {reason}")

    def _quarantine_name(self, filename: str, reason: str) -> None:
        src = self.lessons_dir / filename
        if src.exists():
            self._quarantine(src, reason)
        else:
            self.ignored_files.append(f"{filename}: {reason}")

    @staticmethod
    def _checksum_ok(lesson: AdmittedLesson) -> bool:
        return lesson.checksum == LearnNode._checksum_for(lesson)

    @staticmethod
    def _checksum_for(lesson: AdmittedLesson) -> str:
        canonical = json.dumps(
            {
                "lesson_id": lesson.lesson_id,
                "version": lesson.version,
                "lesson_text": lesson.lesson_text,
                "intent_signature": lesson.intent_signature,
                "provenance": lesson.provenance,
                "supersedes": lesson.supersedes,
                "admitted_at": lesson.admitted_at,
                "smart_app": lesson.smart_app,
            },
            sort_keys=True,
        )
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:32]

    # -- admission ------------------------------------------------------

    def admit(
        self,
        verify_result: dict[str, Any],
        lesson: dict[str, Any],
        smart_app_package: dict[str, Any] | None = None,
        release_bytes: bytes | None = None,
    ) -> dict[str, Any]:
        """Freeze a VERIFY-admitted lesson into the usable knowledge set.

        verify_result: the VERIFY stage output {admitted, admitted_as, ...}.
        lesson: {lesson_id, lesson_text, intent_signature, version?, supersedes?}.
        smart_app_package: optional #2086 preflight package {artifact_id,
            version, content_sha256, independent_proof_refs, observed_quality,
            ...}. When present, release_bytes MUST be provided and the
            content_sha256 MUST match — the preflight subset is checked here,
            never claimed.
        release_bytes: the exact Smart App release bytes (stored immutably).

        Refuses LOUDLY (LearnAdmissionRefused) unless the lesson was admitted
        by VERIFY as a CANDIDATE. Idempotent: re-admitting the same lesson
        version returns the existing receipt.
        """
        self._check_verify_result(verify_result)
        lesson_id, version, lesson_text, intent_sig, supersedes = self._check_lesson(lesson)
        smart_app_meta = self._check_smart_app(smart_app_package, release_bytes, lesson_id, version)

        key = f"{lesson_id}.v{version}"
        existing = self._lessons.get(key)
        if existing is not None:
            # Idempotent: the same lesson admitted twice yields one record.
            return self._admission_receipt(existing, duplicate=True)

        admitted_at = _utcnow()
        provenance = {
            "admitted_by": "VERIFY",
            "admitted_as": verify_result["admitted_as"],
            "admitted_at": admitted_at,
            "verify_correlation_id": verify_result.get("correlation_id", ""),
            "verify_reason_codes": list(verify_result.get("reason_codes", [])),
            "falsification_condition": verify_result.get("falsification_condition", ""),
            "doer": verify_result.get("doer", ""),
            "scorer": verify_result.get("scorer", ""),
            "measurement_method": verify_result.get("measurement_method", ""),
        }
        record = AdmittedLesson(
            schema=LEARN_SCHEMA,
            lesson_id=lesson_id,
            version=version,
            lesson_text=lesson_text,
            intent_signature=intent_sig,
            provenance=provenance,
            supersedes=supersedes,
            superseded_by=None,
            frozen=True,
            status="ACTIVE",
            admitted_at=admitted_at,
            checksum="",
            smart_app=smart_app_meta,
        )
        record.checksum = self._checksum_for(record)

        # Supersession: the new version retires the old, history preserved.
        if supersedes:
            self._supersede(supersedes, lesson_id, version)

        filename = f"{_safe_filename(lesson_id)}.v{version}.json"
        _atomic_write(self.lessons_dir / filename, record.to_dict())
        self._lessons[key] = record

        # Store the Smart App release bytes immutably (content-addressed).
        if smart_app_meta is not None and release_bytes is not None:
            self._store_release_bytes(smart_app_meta["artifact_id"], version, release_bytes)

        return self._admission_receipt(record, duplicate=False)

    def _check_verify_result(self, verify_result: Any) -> None:
        if not isinstance(verify_result, dict):
            raise LearnAdmissionRefused(NOT_A_VERIFY_RESULT, "verify_result is not an object")
        if verify_result.get("admitted") is not True:
            codes = verify_result.get("reason_codes", [])
            raise LearnAdmissionRefused(
                VERIFY_DID_NOT_ADMIT,
                f"VERIFY did not admit this lesson (admitted={verify_result.get('admitted')}, codes={codes})",
            )
        if verify_result.get("admitted_as") != REQUIRED_ADMITTED_AS:
            raise LearnAdmissionRefused(
                NOT_A_LESSON_CANDIDATE,
                f"VERIFY admitted_as={verify_result.get('admitted_as')!r}; "
                f"LEARN only inherits {REQUIRED_ADMITTED_AS} lessons",
            )

    def _check_lesson(self, lesson: Any) -> tuple[str, int, str, dict, str | None]:
        if not isinstance(lesson, dict):
            raise LearnAdmissionRefused(LESSON_TEXT_REQUIRED, "lesson is not an object")
        lesson_id = lesson.get("lesson_id")
        if not isinstance(lesson_id, str) or not lesson_id.strip():
            raise LearnAdmissionRefused(LESSON_ID_REQUIRED, "lesson.lesson_id is required")
        lesson_text = lesson.get("lesson_text")
        if not isinstance(lesson_text, str) or not lesson_text.strip():
            raise LearnAdmissionRefused(LESSON_TEXT_REQUIRED, "lesson.lesson_text is required")
        intent_sig = lesson.get("intent_signature")
        if not isinstance(intent_sig, dict) or not intent_sig:
            raise LearnAdmissionRefused(INTENT_SIGNATURE_REQUIRED, "lesson.intent_signature is required")
        version = lesson.get("version", 1)
        if not isinstance(version, int) or version < 1:
            raise LearnAdmissionRefused(LESSON_ID_REQUIRED, "lesson.version must be a positive int")
        supersedes = lesson.get("supersedes")
        if supersedes is not None and (not isinstance(supersedes, str) or not supersedes.strip()):
            raise LearnAdmissionRefused(LESSON_ID_REQUIRED, "lesson.supersedes must be a lesson_id or null")
        return lesson_id.strip(), version, lesson_text.strip(), intent_sig, supersedes

    # -- Smart App package (PR #2086 preflight subset) --------------------

    def _check_smart_app(
        self,
        package: dict[str, Any] | None,
        release_bytes: bytes | None,
        lesson_id: str,
        version: int,
    ) -> dict[str, Any] | None:
        """Validate the #2086 preflight subset. Returns the frozen metadata.

        Checks: semantic version format, content_sha256 format + matches the
        actual release bytes, independent_proof_refs non-empty, observed
        verification status. Never claims external proof — the metadata
        records what was presented; verify_smart_app() re-checks the bytes.
        """
        import re

        if package is None:
            if release_bytes is not None:
                raise LearnAdmissionRefused(
                    SMART_APP_BYTES_REQUIRED,
                    "release_bytes provided without a smart_app_package",
                )
            return None
        if not isinstance(package, dict):
            raise LearnAdmissionRefused(SMART_APP_VERSION_INVALID, "smart_app_package must be an object")
        if release_bytes is None:
            raise LearnAdmissionRefused(
                SMART_APP_BYTES_REQUIRED,
                "smart_app_package provided without release_bytes",
            )
        if not isinstance(release_bytes, (bytes, bytearray)):
            raise LearnAdmissionRefused(SMART_APP_BYTES_REQUIRED, "release_bytes must be bytes")

        # Semantic version (PR #2086: strict x.y.z).
        pkg_version = package.get("version")
        if not isinstance(pkg_version, str) or not re.fullmatch(
            r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)", pkg_version
        ):
            raise LearnAdmissionRefused(
                SMART_APP_VERSION_INVALID,
                f"smart_app_package.version={pkg_version!r} is not semantic x.y.z",
            )

        # Content hash: format + MUST match the actual bytes.
        claimed_hash = package.get("content_sha256")
        if not isinstance(claimed_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", claimed_hash):
            raise LearnAdmissionRefused(
                SMART_APP_HASH_INVALID,
                "smart_app_package.content_sha256 must be a 64-char hex SHA256",
            )
        actual_hash = hashlib.sha256(bytes(release_bytes)).hexdigest()
        if actual_hash != claimed_hash:
            raise LearnAdmissionRefused(
                SMART_APP_HASH_MISMATCH,
                f"content_sha256 mismatch: claimed {claimed_hash[:16]}..., "
                f"actual {actual_hash[:16]}... — the bytes are not what the package claims",
            )

        # Independent proof refs: at least one, non-empty strings.
        proof_refs = package.get("independent_proof_refs")
        if (
            not isinstance(proof_refs, list)
            or not proof_refs
            or any(not isinstance(r, str) or not r.strip() for r in proof_refs)
        ):
            raise LearnAdmissionRefused(
                SMART_APP_PROOF_MISSING,
                "smart_app_package.independent_proof_refs must be a non-empty list of references",
            )

        # Freeze the preflight-relevant metadata (not the entire package —
        # the lesson record carries what the serving decision needs).
        return {
            "artifact_id": str(package.get("artifact_id", lesson_id)),
            "version": pkg_version,
            "content_sha256": claimed_hash,
            "independent_proof_refs": [str(r) for r in proof_refs],
            "observed_quality": package.get("observed_quality", {}),
            "owner_scope": str(package.get("owner_scope", "PRIVATE")),
            "human_job": str(package.get("human_job", "")),
        }

    def _smart_app_dir(self, artifact_id: str, version: int) -> Path:
        safe = _safe_filename(artifact_id)
        return self.store_path / "smart_apps" / f"{safe}.v{version}"

    def _store_release_bytes(self, artifact_id: str, version: int, release_bytes: bytes) -> None:
        """Store the exact release bytes immutably (content-addressed)."""
        dest_dir = self._smart_app_dir(artifact_id, version)
        dest_dir.mkdir(parents=True, exist_ok=True)
        _atomic_write_bytes(dest_dir / "release.bin", bytes(release_bytes))

    def get_smart_app_bytes(self, lesson_id: str, version: int = 1) -> bytes | None:
        """Return the exact stored release bytes for reuse. None if not a Smart App."""
        lesson = self._lessons.get(f"{lesson_id}.v{version}")
        if lesson is None or not lesson.smart_app:
            return None
        path = self._smart_app_dir(lesson.smart_app["artifact_id"], version) / "release.bin"
        if not path.exists():
            return None
        return path.read_bytes()

    def verify_smart_app(self, lesson_id: str, version: int = 1) -> dict[str, Any]:
        """Re-verify a Smart App: stored bytes MUST match the frozen hash.

        This is the cold-agent trust check — run BEFORE reuse. The hash is
        recomputed from the actual bytes; a mismatch fails closed.
        """
        lesson = self._lessons.get(f"{lesson_id}.v{version}")
        if lesson is None:
            return {"verified": False, "reason": "lesson not found"}
        if not lesson.smart_app:
            return {"verified": False, "reason": "lesson is not a Smart App"}
        stored = self.get_smart_app_bytes(lesson_id, version)
        if stored is None:
            return {"verified": False, "reason": "release bytes missing from store"}
        actual = hashlib.sha256(stored).hexdigest()
        claimed = lesson.smart_app["content_sha256"]
        if actual != claimed:
            return {
                "verified": False,
                "reason": "content hash mismatch — stored bytes differ from the qualified release",
                "claimed": claimed,
                "actual": actual,
            }
        return {
            "verified": True,
            "artifact_id": lesson.smart_app["artifact_id"],
            "version": lesson.smart_app["version"],
            "content_sha256": claimed,
            "independent_proof_refs": lesson.smart_app["independent_proof_refs"],
        }

    def _supersede(self, old_lesson_id: str, new_lesson_id: str, new_version: int) -> None:
        """Mark the superseded lesson SUPERSEDED. History is preserved, not deleted."""
        for key, old in list(self._lessons.items()):
            if old.lesson_id == old_lesson_id and old.status == "ACTIVE":
                old.superseded_by = f"{new_lesson_id}.v{new_version}"
                old.status = "SUPERSEDED"
                filename = f"{_safe_filename(old.lesson_id)}.v{old.version}.json"
                # Re-freeze with the supersession marker (checksum covers content,
                # superseded_by is a lifecycle marker stored alongside).
                data = old.to_dict()
                _atomic_write(self.lessons_dir / filename, data)
                self._lessons[key] = old

    @staticmethod
    def _admission_receipt(record: AdmittedLesson, duplicate: bool) -> dict[str, Any]:
        receipt: dict[str, Any] = {
            "admitted": True,
            "duplicate": duplicate,
            "lesson_id": record.lesson_id,
            "version": record.version,
            "frozen": record.frozen,
            "status": record.status,
            "admitted_at": record.admitted_at,
            "checksum": record.checksum,
            "provenance": record.provenance,
            "supersedes": record.supersedes,
        }
        if record.smart_app:
            receipt["smart_app"] = {
                "artifact_id": record.smart_app["artifact_id"],
                "version": record.smart_app["version"],
                "content_sha256": record.smart_app["content_sha256"],
            }
        return receipt

    # -- serving (inheritance in action) --------------------------------

    def serve(self, decision_context: dict[str, Any]) -> dict[str, Any]:
        """Serve applicable lessons to a fresh decision context, by intent.

        decision_context: {correlation_id, intent: {domains, situation,
        situation_keywords, decision_type}}.

        Returns the applicable ACTIVE lessons ranked by intent-match score,
        each with its full provenance, and records the serving. Lessons the
        context never saw arrive here without the original instruction being
        repeated — that is the inheritance.
        """
        if not isinstance(decision_context, dict):
            raise ValueError("decision_context must be an object")
        correlation_id = decision_context.get("correlation_id", "")
        intent = decision_context.get("intent", {})
        if not isinstance(intent, dict):
            raise ValueError("decision_context.intent must be an object")

        considered = 0
        below_threshold = 0
        served: list[dict[str, Any]] = []

        for lesson in self._lessons.values():
            if lesson.status != "ACTIVE":
                continue
            considered += 1
            score = intent_match_score(lesson.intent_signature, intent)
            if score >= SERVE_THRESHOLD:
                entry: dict[str, Any] = {
                    "lesson_id": lesson.lesson_id,
                    "version": lesson.version,
                    "lesson_text": lesson.lesson_text,
                    "match_score": score,
                    "provenance": lesson.provenance,
                    "checksum": lesson.checksum,
                }
                # Smart App lessons carry the #2086 package metadata so the
                # cold agent can verify the hash and reuse the exact bytes.
                if lesson.smart_app:
                    entry["smart_app"] = lesson.smart_app
                served.append(entry)
            else:
                below_threshold += 1

        served.sort(key=lambda s: s["match_score"], reverse=True)

        record = ServingRecord(
            serve_id=f"srv_{hashlib.sha256(f'{correlation_id}{_utcnow()}'.encode()).hexdigest()[:16]}",
            served_at=_utcnow(),
            decision_correlation_id=correlation_id,
            context_intent=intent,
            lessons_served=served,
            lessons_considered=considered,
            lessons_below_threshold=below_threshold,
        )
        self._append_serving(record)

        return {
            "served": served,
            "serve_id": record.serve_id,
            "served_at": record.served_at,
            "lessons_considered": considered,
            "lessons_below_threshold": below_threshold,
        }

    def _append_serving(self, record: ServingRecord) -> None:
        self.servings_log.parent.mkdir(parents=True, exist_ok=True)
        with open(self.servings_log, "a", encoding="utf-8") as f:
            f.write(json.dumps(record.to_dict(), sort_keys=True) + "\n")

    # -- inspection (not the serving path) ------------------------------

    def get_lesson(self, lesson_id: str, version: int = 1) -> AdmittedLesson | None:
        return self._lessons.get(f"{lesson_id}.v{version}")

    def list_lessons(self, status: str | None = None) -> list[AdmittedLesson]:
        lessons = list(self._lessons.values())
        if status is not None:
            lessons = [l for l in lessons if l.status == status]
        return sorted(lessons, key=lambda l: (l.lesson_id, l.version))

    def servings(self) -> list[dict]:
        """All recorded servings (the application handoff log)."""
        if not self.servings_log.exists():
            return []
        records = []
        for line in self.servings_log.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                records.append(json.loads(line))
        return records

    def active_lesson_count(self) -> int:
        return sum(1 for l in self._lessons.values() if l.status == "ACTIVE")
