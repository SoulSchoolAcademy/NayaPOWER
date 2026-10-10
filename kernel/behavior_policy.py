"""NayaPOWER behavior policy store v1: verified lessons become behavior.

A versioned JSON store mapping situation -> lesson-prescribed behavior.
Every mutation creates a NEW immutable version; all prior versions are
retained on disk. Rollback to any prior version creates a new version that
restores the old policies — rollback is itself versioned, so the audit trail
is append-only and the store is always reversible.

On-disk layout (single JSON file):
    {
      "schema": "naya.self.behavior-policy.v1",
      "store_checksum": "SHA256-...",
      "current_version": 2,
      "versions": [
        {"version": 0, "created_at": ..., "kind": "genesis",
         "policies": {}, "note": "..."},
        {"version": 1, "created_at": ..., "kind": "integrate",
         "lesson_id": "...", "situation": "...",
         "policies": {...}, "note": "..."},
        ...
      ]
    }

Decisions consult the CURRENT version via advise(): a situation with an
integrated lesson returns the lesson-prescribed behavior; anything else
returns the caller's default. That before/after delta is the behavioral
proof that a verified lesson changed a decision.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA = "naya.self.behavior-policy.v1"

KIND_GENESIS = "genesis"
KIND_INTEGRATE = "integrate"
KIND_ROLLBACK = "rollback"


class BehaviorPolicyError(ValueError):
    """Raised when the policy store cannot serve or mutate valid state."""


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _checksum(versions: list[dict[str, Any]]) -> str:
    encoded = json.dumps(versions, sort_keys=True, separators=(",", ":")).encode()
    return "SHA256-" + hashlib.sha256(encoded).hexdigest()


class BehaviorPolicyStore:
    """Versioned, reversible situation -> behavior store backed by one JSON file."""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        if self.path.exists():
            self._doc = self._load()
        else:
            self._doc = {
                "schema": SCHEMA,
                "current_version": 0,
                "versions": [
                    {
                        "version": 0,
                        "created_at": _now_iso(),
                        "kind": KIND_GENESIS,
                        "policies": {},
                        "note": "empty genesis: no lessons integrated",
                    }
                ],
                "store_checksum": "",
            }
            self._persist()

    # --- reads -----------------------------------------------------------

    @property
    def current_version(self) -> int:
        return int(self._doc["current_version"])

    def policies(self, version: int | None = None) -> dict[str, dict[str, Any]]:
        """Policies at a version (current when version is None)."""
        return dict(self._version_entry(version)["policies"])

    def get(self, situation: str, version: int | None = None) -> dict[str, Any] | None:
        """Lesson-prescribed policy for a situation, or None when absent."""
        return self.policies(version).get(situation)

    def advise(self, situation: str, default_behavior: str) -> dict[str, Any]:
        """Decision seam: what behavior applies in this situation right now?

        Returns the lesson-prescribed behavior when a lesson is integrated for
        the situation, otherwise the caller's default. Callers log the
        `source` field — "lesson:<id>" vs "default" — to prove the behavioral
        delta in before/after transcripts.
        """
        entry = self.get(situation)
        if entry is None:
            return {
                "behavior": default_behavior,
                "source": "default",
                "situation": situation,
                "policy_version": self.current_version,
            }
        return {
            "behavior": entry["behavior"],
            "source": f"lesson:{entry['lesson_id']}",
            "situation": situation,
            "policy_version": self.current_version,
        }

    def history(self) -> list[dict[str, Any]]:
        """One summary per version, oldest first. History is never rewritten."""
        return [
            {
                "version": v["version"],
                "created_at": v["created_at"],
                "kind": v["kind"],
                "lesson_id": v.get("lesson_id"),
                "situation": v.get("situation"),
                "policy_count": len(v["policies"]),
                "note": v.get("note", ""),
            }
            for v in self._doc["versions"]
        ]

    # --- mutations (each creates a new version) ---------------------------

    def integrate(
        self,
        situation: str,
        behavior: str,
        lesson_id: str,
        *,
        note: str = "",
    ) -> int:
        """Integrate a verified lesson's prescribed behavior for a situation.

        Creates a new version; prior versions are untouched. Returns the new
        version number.
        """
        if not situation or not situation.strip():
            raise BehaviorPolicyError("situation_required")
        if not behavior or not behavior.strip():
            raise BehaviorPolicyError("behavior_required")
        if not lesson_id or not lesson_id.strip():
            raise BehaviorPolicyError("lesson_id_required")
        policies = self.policies()
        policies[situation] = {
            "behavior": behavior,
            "lesson_id": lesson_id,
            "integrated_at": _now_iso(),
        }
        return self._new_version(
            kind=KIND_INTEGRATE,
            policies=policies,
            lesson_id=lesson_id,
            situation=situation,
            note=note or f"integrated lesson {lesson_id} for situation '{situation}'",
        )

    def rollback(self, target_version: int, *, note: str = "") -> int:
        """Revert to a prior version's policies.

        Creates a NEW version restoring the target's policies — rollback is
        reversible (history keeps the versions it undoes). Raises when the
        target version does not exist.
        """
        target = self._version_entry(target_version)  # raises on unknown
        return self._new_version(
            kind=KIND_ROLLBACK,
            policies=dict(target["policies"]),
            note=note or f"rolled back to version {target_version}",
            extra={"restored_version": target_version},
        )

    # --- internals --------------------------------------------------------

    def _version_entry(self, version: int | None) -> dict[str, Any]:
        version = self.current_version if version is None else version
        for entry in self._doc["versions"]:
            if entry["version"] == version:
                return entry
        raise BehaviorPolicyError(f"unknown_policy_version:{version}")

    def _new_version(
        self,
        *,
        kind: str,
        policies: dict[str, dict[str, Any]],
        lesson_id: str | None = None,
        situation: str | None = None,
        note: str = "",
        extra: dict[str, Any] | None = None,
    ) -> int:
        new_version = self.current_version + 1
        entry: dict[str, Any] = {
            "version": new_version,
            "created_at": _now_iso(),
            "kind": kind,
            "policies": policies,
            "note": note,
        }
        if lesson_id is not None:
            entry["lesson_id"] = lesson_id
        if situation is not None:
            entry["situation"] = situation
        if extra:
            entry.update(extra)
        self._doc["versions"].append(entry)
        self._doc["current_version"] = new_version
        self._persist()
        return new_version

    def _persist(self) -> None:
        self._doc["store_checksum"] = _checksum(self._doc["versions"])
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(self._doc, sort_keys=True, indent=2) + "\n", encoding="utf-8"
        )

    def _load(self) -> dict[str, Any]:
        try:
            doc = json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise BehaviorPolicyError("policy_store_corrupt") from exc
        if not isinstance(doc, dict) or doc.get("schema") != SCHEMA:
            raise BehaviorPolicyError("policy_store_schema_mismatch")
        versions = doc.get("versions")
        if not isinstance(versions, list) or not versions:
            raise BehaviorPolicyError("policy_store_no_versions")
        if doc.get("store_checksum") != _checksum(versions):
            # Tampered or truncated store: isolate, never silently absorb.
            raise BehaviorPolicyError("policy_store_integrity_failed")
        if int(doc.get("current_version", -1)) != int(versions[-1]["version"]):
            raise BehaviorPolicyError("policy_store_tip_mismatch")
        return doc
