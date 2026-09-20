#!/usr/bin/env python3
"""Build a deterministic, rebuildable relationship graph from canonical events.

The event store remains authoritative. This graph is a derived index and can
always be deleted and rebuilt from canonical Note Events.
"""
from __future__ import annotations
import json
from collections import defaultdict
from pathlib import Path

import smart_notes_v3 as brain

MEMORY = Path(__file__).resolve().parent
GRAPH = MEMORY / "RELATIONSHIP-GRAPH.json"

RELATIONSHIP_KEYS = ("related", "depends_on", "supersedes", "superseded_by", "source_events")


def build() -> dict:
    events = [e for _, e in brain.load_events() if not e.get("__parse_error__")]
    known = {e["event_id"] for e in events}
    edges = set()
    adjacency = defaultdict(set)
    for event in events:
        source = event["event_id"]
        relationships = brain.relationship_map(event)
        for key in RELATIONSHIP_KEYS:
            values = brain.normalize_targets(relationships.get(key, []))
            for target in values:
                if target in known and target != source:
                    a, b = sorted((source, target))
                    edges.add((a, b, key))
                    adjacency[source].add(target)
                    adjacency[target].add(source)
    graph = {
        "schema_version": 1,
        "status": "DERIVED",
        "source": ".naya/memory/events",
        "event_count": len(events),
        "edge_count": len(edges),
        "nodes": sorted(known),
        "edges": [
            {"a": a, "b": b, "relationship": relationship}
            for a, b, relationship in sorted(edges)
        ],
        "neighbors": {k: sorted(v) for k, v in sorted(adjacency.items())},
    }
    GRAPH.write_text(json.dumps(graph, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return graph


if __name__ == "__main__":
    result = build()
    print(f"GREEN — relationship graph rebuilt: {result['event_count']} nodes / {result['edge_count']} edges")
