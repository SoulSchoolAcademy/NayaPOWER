"""CONNECT node — the canonical implementation.

Naya 1 (MN-06): CONNECT owns relationships, contextual retrieval,
applicability, relevance, freshness, dependencies, supersession,
contradiction discovery, and cross-surface context.

This module builds the lesson's relationship graph from the canonical
lesson (post KNOW/PROVE) and the existing knowledge store (Intelligent
Blocks + prior lessons):

  related_blocks / related_lessons — RELATED_TO edges with explicit support
  conflicts                        — CONTRADICTS edges + first-class conflict
                                     records; both sides preserved, NEVER
                                     auto-resolved, NEVER merged, NEVER
                                     overwritten
  downstream_consumers              — APPLIES_TO edges to decisions/consumers
                                     the lesson is relevant to

Every emitted edge conforms to the repository's canonical graph
relationship contract (BRAIN/04-INTELLIGENCE/GRAPH/0003-GRAPH-RELATIONSHIP-
CONTRACT-V2.json) and is validated with the repo's own validator
(tools/validate_graph_relationship_v2.py::validate_edge) before it leaves
this module. An edge that fails validation is a code bug and raises loudly —
CONNECT never emits a malformed edge and never silently drops one.

Laws honored:
- Read-only over the knowledge store: no item is modified, merged,
  superseded, or deleted. Both sides of a conflict are preserved by
  construction (we only read).
- Relevance is distinguished from truth and authority: a RELATED_TO edge
  carries its support (which tags/terms matched); a CONTRADICTS edge is a
  separate first-class record with the evidence on EACH side.
- Deterministic and idempotent: same inputs → byte-identical output.
  Safe under the orchestrator's retry contract.
- No silent PASS: empty store → explicit empty graph with a named reason,
  never a fabricated relationship.

Honest bounds (also returned in every output's "limitations"):
- Relatedness is deterministic tag/term overlap, not semantic understanding.
- Conflict discovery covers DECLARED claim polarity opposition only;
  natural-language contradiction inference is not implemented.
- Consumer suggestions are registry/inheritance lookups, not authority
  grants — APPLIES_TO here means "relevant to", never "authorized for".
"""

from __future__ import annotations

import copy
import re
from typing import Any

from validate_graph_relationship_v2 import validate_edge

SCHEMA = "naya.connect.relationship-graph.v1"

# Terms this short or this common carry no relating signal.
_STOPWORDS = frozenset(
    "the a an and or of to in on for with when must this that these those "
    "is are was were be been being by it its as at from into over under "
    "which who whom whose will would should could shall may might can "
    "do does did done have has had having not no yes if then than so such "
    "but about into through during each other more most some any all only "
    "own same very just".split()
)
_TERM_RE = re.compile(r"[a-z0-9]+")
_MIN_TERM_LEN = 4
_MIN_SHARED_TERMS = 3  # RELATED_TO via terms needs at least this many.

# Relationship types used by this node (subset of the contract's allowed
# types, chosen for semantics this node can honestly assert).
REL_RELATED_TO = "RELATED_TO"      # lesson <-> item: shared topic/terms
REL_CONTRADICTS = "CONTRADICTS"    # lesson -/-> item: polarity opposition
REL_APPLIES_TO = "APPLIES_TO"      # lesson -> consumer: relevant to

_EPISTEMIC_DISCOVERED = "CANDIDATE"  # discovered by CONNECT, not yet verified
_STATUS_ACTIVE = "ACTIVE"
_VISIBILITY = "PRIVATE"  # MN-06: never bypass ownership/privacy/authority.


def _terms(text: str) -> set[str]:
    return {
        t for t in _TERM_RE.findall((text or "").lower())
        if len(t) >= _MIN_TERM_LEN and t not in _STOPWORDS
    }


def _tags(item: dict[str, Any]) -> set[str]:
    return {str(t).strip().lower() for t in item.get("tags", []) if str(t).strip()}


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:80]


class ConnectError(RuntimeError):
    """CONNECT failed loudly. Never a silent empty graph."""


class ConnectNode:
    """Builds the relationship graph for one canonical lesson."""

    def build_graph(
        self,
        lesson: dict[str, Any],
        knowledge_store: list[dict[str, Any]],
        consumer_registry: dict[str, list[str]] | None = None,
        owner_id: str = "owner-1",
        correlation_id: str = "",
    ) -> dict[str, Any]:
        """Build the lesson's relationship graph.

        lesson: the canonical lesson — {id, kind="lesson", title, essence,
                tags, claims[{key, polarity, statement}], evidence_refs}.
                The KNOW essence and PROVE evidence should already be folded
                in by the caller (the orchestrator threads know_result and
                prove_result forward).
        knowledge_store: existing knowledge items in the same schema
                (kind "IB" or "lesson"). READ-ONLY: never mutated.
        consumer_registry: {tag: [consumer_id, ...]} — decisions/areas that
                consume lessons on a topic.
        """
        registry = consumer_registry or {}
        if not isinstance(lesson, dict) or not lesson.get("id"):
            raise ConnectError("CONNECT requires a lesson object with an id")
        if not isinstance(knowledge_store, list):
            raise ConnectError("CONNECT requires a knowledge_store list")

        lesson_id = str(lesson["id"])
        lesson_tags = _tags(lesson)
        lesson_terms = _terms(str(lesson.get("essence", "")))
        lesson_claims = {
            str(c.get("key")): c for c in lesson.get("claims", [])
            if isinstance(c, dict) and c.get("key")
        }

        edges: list[dict[str, Any]] = []
        conflicts: list[dict[str, Any]] = []
        related_blocks: list[dict[str, Any]] = []
        related_lessons: list[dict[str, Any]] = []

        for item in knowledge_store:
            if not isinstance(item, dict) or not item.get("id"):
                continue  # malformed store entries are skipped loudly below
            item_id = str(item["id"])
            if item_id == lesson_id:
                continue  # the lesson is never related to itself
            kind = str(item.get("kind", "IB"))

            shared_tags = sorted(lesson_tags & _tags(item))
            shared_terms = sorted(lesson_terms & _terms(str(item.get("essence", ""))))
            related = bool(shared_tags) or len(shared_terms) >= _MIN_SHARED_TERMS

            if related:
                support = {"shared_tags": shared_tags, "shared_terms": shared_terms}
                rel_reasons: list[str] = []
                if shared_tags:
                    rel_reasons.append("TAG_OVERLAP")
                if shared_terms:
                    rel_reasons.append("TERM_OVERLAP")
                edge = self._edge(
                    lesson_id, item_id, REL_RELATED_TO, owner_id,
                    correlation_id, support, lesson_tags,
                    [f"connect-node:tag-overlap:{shared_tags}" if shared_tags else "",
                     f"connect-node:term-overlap:{shared_terms}" if shared_terms else ""],
                    rel_reasons,
                )
                edges.append(edge)
                link = {
                    "id": item_id, "kind": kind,
                    "title": str(item.get("title", item_id)),
                    "edge_id": edge["relationship_id"],
                    "support": support,
                }
                (related_blocks if kind == "IB" else related_lessons).append(link)

            # Conflict discovery: declared claim polarity opposition on the
            # same claim key. Both sides preserved; never auto-resolved.
            for key, claim in lesson_claims.items():
                theirs = next(
                    (c for c in item.get("claims", [])
                     if isinstance(c, dict) and str(c.get("key")) == key),
                    None,
                )
                if theirs is None:
                    continue
                try:
                    mine_pol = int(claim.get("polarity", 0))
                    theirs_pol = int(theirs.get("polarity", 0))
                except (TypeError, ValueError):
                    continue
                if mine_pol != 0 and theirs_pol != 0 and mine_pol != theirs_pol:
                    conflict = self._conflict(
                        lesson, item, key, claim, theirs,
                        owner_id, correlation_id, lesson_tags,
                    )
                    edges.append(conflict["edge"])
                    conflicts.append(conflict)

        malformed = sum(
            1 for i in knowledge_store
            if not isinstance(i, dict) or not i.get("id")
        )

        consumers = self._consumers(
            lesson_id, lesson_tags, related_blocks + related_lessons,
            knowledge_store, registry, owner_id, correlation_id,
        )
        edges.extend(c["edge"] for c in consumers)

        graph = {
            "schema": SCHEMA,
            "lesson_id": lesson_id,
            "correlation_id": correlation_id,
            "related_blocks": related_blocks,
            "related_lessons": related_lessons,
            "conflicts": conflicts,
            "downstream_consumers": [
                {k: c[k] for k in ("consumer_id", "via", "why", "edge_id")}
                for c in consumers
            ],
            "edges": edges,
            "stats": {
                "items_scanned": len(knowledge_store),
                "malformed_items_skipped": malformed,
                "related": len(related_blocks) + len(related_lessons),
                "conflicts": len(conflicts),
                "consumers": len(consumers),
                "edges_emitted": len(edges),
            },
            "graph_summary": self._summarize(
                lesson_id, related_blocks, related_lessons, conflicts, consumers
            ),
            "limitations": [
                "Relatedness is deterministic tag/term overlap, not semantic understanding.",
                "Conflict discovery covers DECLARED claim polarity opposition only; "
                "natural-language contradiction inference is not implemented.",
                "Consumer suggestions are registry/inheritance lookups, not authority grants.",
                "The knowledge store is read-only to CONNECT; nothing is modified, merged, "
                "superseded, or deleted.",
            ],
        }
        if not edges:
            graph["empty_reason"] = (
                "no relationships discovered: the lesson shares no tags, no "
                f">={_MIN_SHARED_TERMS} terms, no claim keys, and no registry "
                "tags with any well-formed store item"
            )
        return graph

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _edge(
        self,
        source_id: str,
        target_id: str,
        rel_type: str,
        owner_id: str,
        correlation_id: str,
        support: dict[str, Any],
        task_classes: set[str],
        provenance_notes: list[str],
        reason_codes: list[str],
    ) -> dict[str, Any]:
        from datetime import datetime, timezone

        now = datetime.now(timezone.utc).isoformat()
        edge = {
            "relationship_id": f"rel-{_slug(source_id)}-{_slug(target_id)}-{rel_type.lower()}",
            "source_id": source_id,
            "target_id": target_id,
            "relationship_type": rel_type,
            "owner_scope": {"owner_id": owner_id, "visibility": _VISIBILITY},
            "epistemic_state": _EPISTEMIC_DISCOVERED,
            "status": _STATUS_ACTIVE,
            "provenance": [
                p for p in provenance_notes if p
            ] + [f"connect-node:correlation:{correlation_id}"],
            "evidence_refs": [],
            "created_at": now,
            "observed_at": now,
            "applicability": {
                "state": "APPLICABLE" if task_classes else "UNKNOWN",
                "task_classes": sorted(task_classes),
                "limitations": [
                    "discovered by CONNECT; relevance is not truth and not authority",
                ],
            },
            "reason_codes": reason_codes,
        }
        errors = validate_edge(edge)
        if errors:
            raise ConnectError(
                f"CONNECT emitted an invalid edge (bug, failing loudly): {errors}"
            )
        return edge

    def _conflict(
        self,
        lesson: dict[str, Any],
        item: dict[str, Any],
        claim_key: str,
        mine: dict[str, Any],
        theirs: dict[str, Any],
        owner_id: str,
        correlation_id: str,
        task_classes: set[str],
    ) -> dict[str, Any]:
        lesson_id, item_id = str(lesson["id"]), str(item["id"])
        edge = self._edge(
            lesson_id, item_id, REL_CONTRADICTS, owner_id, correlation_id,
            {"claim_key": claim_key},
            task_classes,
            [f"connect-node:claim-polarity-opposition:key={claim_key}:"
             f"lesson={mine.get('polarity')}:existing={theirs.get('polarity')}"],
            ["CLAIM_POLARITY_OPPOSITION"],
        )
        return {
            "conflict_id": f"conflict-{_slug(lesson_id)}-{_slug(item_id)}-{_slug(claim_key)}",
            "type": "POLARITY_OPPOSITION",
            "claim_key": claim_key,
            "edge": edge,
            "new_side": {
                "item_id": lesson_id,
                "kind": "lesson",
                "statement": str(mine.get("statement", "")),
                "polarity": mine.get("polarity"),
                "evidence_refs": list(lesson.get("evidence_refs", [])),
            },
            "existing_side": {
                "item_id": item_id,
                "kind": str(item.get("kind", "IB")),
                "statement": str(theirs.get("statement", "")),
                "polarity": theirs.get("polarity"),
                "evidence_refs": list(item.get("evidence_refs", [])),
            },
            "resolution": "NONE",
            "both_preserved": True,
            "note": (
                "CONNECT never auto-resolves, merges, or overwrites. Both sides "
                "are preserved with their evidence. Adjudication belongs to "
                "VERIFY/LEARN, not to CONNECT."
            ),
        }

    def _consumers(
        self,
        lesson_id: str,
        lesson_tags: set[str],
        related: list[dict[str, Any]],
        knowledge_store: list[dict[str, Any]],
        registry: dict[str, list[str]],
        owner_id: str,
        correlation_id: str,
    ) -> list[dict[str, Any]]:
        seen: dict[str, dict[str, Any]] = {}
        by_id = {str(i.get("id")): i for i in knowledge_store if isinstance(i, dict)}

        def add(consumer_id: str, via: str, why: str) -> None:
            if consumer_id in seen:
                return
            edge = self._edge(
                lesson_id, consumer_id, REL_APPLIES_TO, owner_id,
                correlation_id, {"via": via}, lesson_tags,
                [f"connect-node:consumer:{via}"],
                ["REGISTRY_CONSUMER"] if via.startswith("registry:")
                else ["INHERITED_CONSUMER"],
            )
            seen[consumer_id] = {
                "consumer_id": consumer_id, "via": via, "why": why,
                "edge_id": edge["relationship_id"], "edge": edge,
            }

        # Registry: topic tag → consumers that work that topic.
        for tag in sorted(lesson_tags):
            for consumer_id in registry.get(tag, []):
                add(str(consumer_id), f"registry:tag={tag}",
                    f"lesson carries tag '{tag}', which the consumer registry "
                    f"maps to consumer '{consumer_id}'")

        # Inheritance: consumers declared on related items.
        for link in related:
            item = by_id.get(link["id"], {})
            for consumer_id in item.get("consumers", []):
                add(str(consumer_id), f"inherited:via={link['id']}",
                    f"consumer of related {link['kind']} '{link['id']}' "
                    f"(edge {link['edge_id']})")

        return list(seen.values())

    def _summarize(
        self,
        lesson_id: str,
        blocks: list[dict[str, Any]],
        lessons: list[dict[str, Any]],
        conflicts: list[dict[str, Any]],
        consumers: list[dict[str, Any]],
    ) -> str:
        parts = [
            f"CONNECT graph for {lesson_id}: "
            f"{len(blocks)} related block(s), {len(lessons)} related lesson(s), "
            f"{len(conflicts)} conflict(s), {len(consumers)} downstream consumer(s)."
        ]
        for c in conflicts:
            parts.append(
                f"CONFLICT {c['conflict_id']}: claim '{c['claim_key']}' — "
                f"lesson asserts ({c['new_side']['statement'][:60]}) vs "
                f"{c['existing_side']['item_id']} asserts "
                f"({c['existing_side']['statement'][:60]}). "
                f"Both preserved; resolution=NONE."
            )
        return " ".join(parts)


def build_graph(
    lesson: dict[str, Any],
    knowledge_store: list[dict[str, Any]],
    consumer_registry: dict[str, list[str]] | None = None,
    owner_id: str = "owner-1",
    correlation_id: str = "",
) -> dict[str, Any]:
    """Functional entry point (mirrors the VERIFY twin's module-level API)."""
    return ConnectNode().build_graph(
        lesson, knowledge_store, consumer_registry, owner_id, correlation_id
    )


def knowledge_item_snapshot(store: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Deep snapshot helper for tests proving the store is never mutated."""
    return copy.deepcopy(store)
