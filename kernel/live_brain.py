"""Executable, governed brain kernel V1.

This is the first small runtime bridge from the canonical BRAIN registry/graph
into durable behavior. It deliberately keeps persistence local and explicit so
behavior can be proven without inventing a second intelligence store.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
import uuid
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Iterable

from .value_calculus import ResourceCost, ValueProfile, calculate_value


NODE_NAMES = (
    "SELF", "LAW", "ACT", "KNOW", "PROVE",
    "CONNECT", "VERIFY", "LEARN", "EVOLVE",
)
NODE_IDS = tuple(f"NAYA-KERNEL-{name}" for name in NODE_NAMES)


@dataclass(frozen=True)
class MemoryRecord:
    object_id: str
    owner_id: str
    content: str
    provenance: str
    epistemic_state: str
    supersedes: str | None = None


@dataclass(frozen=True)
class CausalVerification:
    claim_id: str
    input_fingerprint: str
    intelligence_ids: tuple[str, ...]
    decision_fingerprint: str
    action_id: str
    observation: str
    outcome: str
    evidence_ids: tuple[str, ...]
    control_outcome: str
    treatment_outcome: str

    def verdict(self) -> str:
        if not self.evidence_ids:
            return "NOT_PROVEN"
        try:
            control = float(self.control_outcome)
            treatment = float(self.treatment_outcome)
        except ValueError:
            return "NOT_PROVEN"
        if treatment <= control:
            return "NOT_PROVEN"
        if not self.intelligence_ids or not self.action_id:
            return "NOT_PROVEN"
        return "VERIFIED"


class FileBrainStore:
    """Durable SQLite store used for behavioral proof and local runtime."""

    def __init__(self, path: str | Path):
        self.path = str(path)
        self.db = sqlite3.connect(self.path)
        self.db.row_factory = sqlite3.Row
        self._schema()

    def _schema(self) -> None:
        self.db.executescript(
            """
            CREATE TABLE IF NOT EXISTS memory (
                object_id TEXT PRIMARY KEY,
                owner_id TEXT NOT NULL,
                content TEXT NOT NULL,
                provenance TEXT NOT NULL,
                epistemic_state TEXT NOT NULL,
                supersedes TEXT
            );
            CREATE TABLE IF NOT EXISTS learning (
                lesson_id TEXT PRIMARY KEY,
                source_event_id TEXT NOT NULL,
                claimed_effect TEXT NOT NULL,
                prior_outcome REAL NOT NULL,
                later_outcome REAL,
                behavioral_change INTEGER NOT NULL DEFAULT 0,
                state TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS successors (
                successor_id TEXT PRIMARY KEY,
                parent_id TEXT NOT NULL,
                mission TEXT NOT NULL,
                authority_inherited INTEGER NOT NULL
            );
            CREATE TABLE IF NOT EXISTS value_receipts (
                receipt_id TEXT PRIMARY KEY,
                event_id TEXT NOT NULL,
                outcome_id TEXT NOT NULL,
                item_id TEXT NOT NULL,
                payload TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS relationships (
                relationship_id TEXT PRIMARY KEY,
                source_id TEXT NOT NULL,
                target_id TEXT NOT NULL,
                relationship_type TEXT NOT NULL,
                provenance TEXT NOT NULL,
                epistemic_state TEXT NOT NULL
            );
            """
        )
        self.db.commit()

    def persist(self, record: MemoryRecord) -> None:
        self.db.execute(
            """
            INSERT INTO memory(object_id, owner_id, content, provenance, epistemic_state, supersedes)
            VALUES(?,?,?,?,?,?)
            ON CONFLICT(object_id) DO UPDATE SET
              owner_id=excluded.owner_id,
              content=excluded.content,
              provenance=excluded.provenance,
              epistemic_state=excluded.epistemic_state,
              supersedes=excluded.supersedes
            """,
            (record.object_id, record.owner_id, record.content, record.provenance,
             record.epistemic_state, record.supersedes),
        )
        self.db.commit()

    def search(self, query: str, owner_id: str) -> list[MemoryRecord]:
        terms = [t for t in query.lower().split() if t]
        rows = self.db.execute(
            "SELECT * FROM memory WHERE owner_id=? AND epistemic_state != 'SUPERSEDED'",
            (owner_id,),
        ).fetchall()
        scored = []
        for row in rows:
            hay = row["content"].lower()
            score = sum(term in hay for term in terms)
            if score:
                scored.append((score, row))
        scored.sort(key=lambda item: (-item[0], item[1]["object_id"]))
        return [
            MemoryRecord(
                row["object_id"], row["owner_id"], row["content"],
                row["provenance"], row["epistemic_state"], row["supersedes"],
            )
            for _, row in scored
        ]

    def add_relationships(self, edges: Iterable[dict[str, Any]]) -> None:
        for edge in edges:
            self.db.execute(
                """
                INSERT OR REPLACE INTO relationships
                (relationship_id, source_id, target_id, relationship_type, provenance, epistemic_state)
                VALUES(?,?,?,?,?,?)
                """,
                (
                    edge["relationship_id"], edge["source_id"], edge["target_id"],
                    edge["type"], json.dumps(edge["provenance"], sort_keys=True),
                    edge.get("epistemic_state", "UNKNOWN"),
                ),
            )
        self.db.commit()

    def neighbors(self, object_id: str) -> list[dict[str, Any]]:
        rows = self.db.execute(
            """SELECT * FROM relationships
               WHERE source_id=? OR target_id=?
               ORDER BY relationship_id""",
            (object_id, object_id),
        ).fetchall()
        return [dict(row) for row in rows]

    def record_learning(self, lesson_id: str, source_event_id: str,
                        claimed_effect: str, prior_outcome: float) -> dict[str, Any]:
        self.db.execute(
            """INSERT OR REPLACE INTO learning
               (lesson_id, source_event_id, claimed_effect, prior_outcome,
                later_outcome, behavioral_change, state)
               VALUES(?,?,?,?,?,?,?)""",
            (lesson_id, source_event_id, claimed_effect, prior_outcome, None, 0, "CANDIDATE"),
        )
        self.db.commit()
        return self.learning(lesson_id)

    def verify_learning(self, lesson_id: str, later_outcome: float,
                        behavioral_change: bool) -> dict[str, Any]:
        row = self.db.execute(
            "SELECT * FROM learning WHERE lesson_id=?", (lesson_id,)
        ).fetchone()
        if row is None:
            raise KeyError(lesson_id)
        improvement = later_outcome - row["prior_outcome"]
        state = "VERIFIED" if behavioral_change and improvement > 0 else "REJECTED"
        self.db.execute(
            """UPDATE learning SET later_outcome=?, behavioral_change=?, state=?
               WHERE lesson_id=?""",
            (later_outcome, int(behavioral_change), state, lesson_id),
        )
        self.db.commit()
        result = self.learning(lesson_id)
        result["improvement"] = improvement
        return result

    def learning(self, lesson_id: str) -> dict[str, Any]:
        row = self.db.execute(
            "SELECT * FROM learning WHERE lesson_id=?", (lesson_id,)
        ).fetchone()
        if row is None:
            raise KeyError(lesson_id)
        return dict(row)

    def add_successor(self, successor_id: str, parent_id: str,
                      mission: str, authority_inherited: bool) -> dict[str, Any]:
        self.db.execute(
            "INSERT INTO successors VALUES(?,?,?,?)",
            (successor_id, parent_id, mission, int(authority_inherited)),
        )
        self.db.commit()
        return dict(self.db.execute(
            "SELECT * FROM successors WHERE successor_id=?", (successor_id,)
        ).fetchone())

    def record_value_receipt(self, receipt: dict[str, Any]) -> None:
        self.db.execute(
            "INSERT OR REPLACE INTO value_receipts VALUES(?,?,?,?,?)",
            (
                receipt["receipt_id"], receipt["event_id"], receipt["outcome_id"],
                receipt["item_id"], json.dumps(receipt, sort_keys=True),
            ),
        )
        self.db.commit()

    def close(self) -> None:
        self.db.close()


class GovernedBrain:
    def __init__(self, root: Path, registry: dict[str, Any],
                 graph: dict[str, Any], store: FileBrainStore):
        self.root = root
        self.registry = registry
        self.graph = graph
        self.store = store

    @classmethod
    def from_repository(cls, root: Path, store: FileBrainStore | None = None):
        registry = json.loads(
            (root / "BRAIN/03-KERNEL/0003-RUNTIME-REGISTRY-V1.json").read_text()
        )
        graph = json.loads(
            (root / "BRAIN/04-INTELLIGENCE/GRAPH/0001-KERNEL-GRAPH-SEED-V1.json").read_text()
        )
        if tuple(registry["node_ids"]) != NODE_IDS:
            raise ValueError("runtime registry does not match canonical nine-node identity")
        store = store or FileBrainStore(":memory:")
        store.add_relationships(graph["edges"])
        return cls(root, registry, graph, store)

    @property
    def node_names(self) -> tuple[str, ...]:
        return tuple(self.registry["node_order"])

    def persist(self, record: MemoryRecord) -> None:
        if not record.object_id or not record.owner_id or not record.provenance:
            raise ValueError("identity, owner and provenance are required")
        self.store.persist(record)

    def retrieve(self, query: str, owner_id: str) -> list[MemoryRecord]:
        # Retrieval is deliberately owner-scoped and never changes authorization.
        return self.store.search(query, owner_id)

    def related(self, object_id: str) -> list[dict[str, Any]]:
        return self.store.neighbors(object_id)

    def authorize(self, action_id: str, owner_id: str, capability: str,
                  authority: dict[str, Any] | None) -> dict[str, Any]:
        if not authority:
            raise PermissionError("missing_authority")
        if authority.get("owner_id") != owner_id:
            raise PermissionError("wrong_owner")
        if authority.get("revoked") is True:
            raise PermissionError("authority_revoked")
        if authority.get("expired") is True:
            raise PermissionError("authority_expired")
        if capability not in authority.get("capabilities", []):
            raise PermissionError("out_of_scope")
        return {"action_id": action_id, "authorized": True, "owner_id": owner_id}

    def record_value(
        self,
        event_id: str,
        outcome_id: str,
        item_id: str,
        dimensions: dict[str, float | None],
        profile: ValueProfile,
        verified_value: float,
        resources: ResourceCost,
        verification_state: str = "VERIFIED",
    ) -> dict[str, Any]:
        result = calculate_value(
            dimensions=dimensions,
            profile=profile,
            verification_state=verification_state,
            verified_value=verified_value,
            resources=resources,
        )
        receipt = {
            "receipt_type": "NAYA-VALUE-RECEIPT",
            "event_id": event_id,
            "outcome_id": outcome_id,
            "item_id": item_id,
            **result,
        }
        receipt["receipt_id"] = hashlib.sha256(
            json.dumps(receipt, sort_keys=True).encode()
        ).hexdigest()[:20]
        self.store.record_value_receipt(receipt)
        return receipt

    def record_learning(self, **kwargs) -> dict[str, Any]:
        return self.store.record_learning(**kwargs)

    def verify_learning(self, lesson_id: str, later_outcome: float,
                        behavioral_change: bool) -> dict[str, Any]:
        return self.store.verify_learning(lesson_id, later_outcome, behavioral_change)

    def create_successor(self, parent_id: str, mission: str) -> dict[str, Any]:
        successor_id = f"NAYA-SUCCESSOR-{uuid.uuid4().hex[:12].upper()}"
        return self.store.add_successor(
            successor_id, parent_id, mission, authority_inherited=False
        )

    def proof_receipt(self, claim: str, evidence: list[str],
                      verdict: str, **extra: Any) -> dict[str, Any]:
        payload = {
            "receipt_type": "NAYA-BRAIN-PROOF",
            "claim": claim,
            "evidence": evidence,
            "verdict": verdict,
            **extra,
        }
        payload["receipt_id"] = hashlib.sha256(
            json.dumps(payload, sort_keys=True).encode()
        ).hexdigest()[:20]
        return payload

    def close(self) -> None:
        self.store.close()
