#!/usr/bin/env python3
"""Smart Connect — open doors mechanism, reference implementation (B-47).

Synthetic only: in-memory state + JSONL evidence ledger in a scratch dir.
Zero production writes, zero DB, zero dashboard actions.

Guarantees:
  G1 open doors — registration never refuses; dead door -> registry reroutes.
  G2 instant capture — lesson intake has no gate (Law 4: "smart note this" means it's in).
  G3 no free compound — a compound is recorded ONLY when a distillation ran
       (Law 6: a number without proof is a lie).
  G4 visible in one cycle — feedback per connection after one cycle.
  G5 seam — intake UX lives elsewhere (B-44); this module owns registry + cycle + feedback.
  G6 approval law — ELEVATE compounds propose to canonical index; intake ledger is not canon.

Builder hardening (wave 14, from Host's wave-12 adversarial finding):
  - run_cycle's ELEVATE stage never assumes canonical_id: a MERGED lesson
    without one is skipped and recorded in cycle.flags — no KeyError, no fake compound.
  - Untrusted inputs (unknown connection_id, no open doors) raise ValueError,
    never bare AssertionError and never silent creation.
  - Re-submission of identical text resolves to the existing lesson
    (duplicate: true); it does not inflate lesson stats.

Spec: BRAIN/10-INTERFACES/SMART-CONNECT-OPEN-DOORS.ai.md
"""
import hashlib
import json
import os
import re
from datetime import datetime, timezone

MERGE_SIMILARITY = 0.7  # Jaccard over normalized token sets — PROVISIONAL, tune against real corpus
ELEVATE_MIN_CLUSTER = 2  # lessons merged -> cluster eligible for ELEVATE proposal
TERMS_VERSION = "L253-v1"


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _essence(text: str):
    toks = re.findall(r"[a-z0-9]+", text.lower())
    return sorted(set(toks))


def _jaccard(a, b):
    sa, sb = set(a), set(b)
    if not sa and not sb:
        return 1.0
    return len(sa & sb) / len(sa | sb)


def _id(prefix, *parts):
    h = hashlib.sha256("|".join(parts).encode()).hexdigest()[:8]
    return f"{prefix}-{h}"


class OpenDoors:
    """The Smart Connect registry + one-cycle distillation loop."""

    def __init__(self, evidence_dir):
        self.evidence_dir = evidence_dir
        os.makedirs(evidence_dir, exist_ok=True)
        self.doors = {}        # door_id -> {door_id, name, protocol, open: bool}
        self.connections = {}  # connection_id -> {...}
        self.lessons = {}      # lesson_id -> {...}
        self.compounds = {}    # compound_id -> {...}
        self.cycles = []       # cycle records
        self._events = []

    # ---- G1: doors ----
    def register_door(self, door_id, name, protocol):
        self.doors[door_id] = {"door_id": door_id, "name": name,
                               "protocol": protocol, "open": True}
        return self.doors[door_id]

    def close_door(self, door_id, reason):
        # A door may close only for harm (Law 11) — and the closure is recorded.
        if door_id not in self.doors:
            raise ValueError(f"unknown door: {door_id}")
        self.doors[door_id]["open"] = False
        self.doors[door_id]["closed_reason"] = reason

    def register_connection(self, name, door_id):
        # G1: never refuse. Dead door -> reroute to any open door.
        if door_id not in self.doors or not self.doors[door_id]["open"]:
            open_doors = [d for d, v in self.doors.items() if v["open"]]
            if not open_doors:
                raise ValueError("no open doors — every door closed, closure must be recorded")
            door_id = open_doors[0]
        conn_id = _id("conn", name, door_id, _now())
        self.connections[conn_id] = {"connection_id": conn_id, "name": name,
                                     "door_id": door_id, "opened_at": _now(),
                                     "terms_version": TERMS_VERSION,
                                     "stats": {"lessons": 0, "compounds": 0}}
        self._log("connection.registered", self.connections[conn_id])
        return self.connections[conn_id]

    # ---- G2: instant capture ----
    def append_lesson(self, connection_id, text, door_id=None):
        # Seam contract: lesson_intake.append(connection_id, text, door_id).
        if connection_id not in self.connections:
            raise ValueError(f"unknown connection: {connection_id}")
        essence = _essence(text)
        lesson_id = _id("les", connection_id, "|".join(essence))
        if lesson_id in self.lessons:
            # Polarity: identical re-submission lands on the one content-addressed
            # record — no second lesson, no stat inflation, marked duplicate.
            lesson = self.lessons[lesson_id]
            lesson["duplicate"] = True
            return lesson
        lesson = {"lesson_id": lesson_id, "connection_id": connection_id,
                  "text": text, "essence": essence, "captured_at": _now(),
                  "status": "INTAKE", "door_id": door_id or self.connections[connection_id]["door_id"]}
        self.lessons[lesson_id] = lesson
        self.connections[connection_id]["stats"]["lessons"] += 1
        self._log("lesson.captured", {"lesson_id": lesson_id, "status": "INTAKE"})
        return lesson

    # ---- the cycle: distill -> compound -> publish ----
    def run_cycle(self):
        cycle_id = f"cyc-{len(self.cycles) + 1:03d}"
        at = _now()
        merged, elevated = 0, 0
        flags = []
        intake = [l for l in self.lessons.values() if l["status"] == "INTAKE"]

        # Distill: MERGE — cluster near-duplicate intakes.
        clusters = []
        used = set()
        for i, li in enumerate(intake):
            if li["lesson_id"] in used:
                continue
            cluster = [li]
            used.add(li["lesson_id"])
            for lj in intake[i + 1:]:
                if lj["lesson_id"] in used:
                    continue
                if _jaccard(li["essence"], lj["essence"]) >= MERGE_SIMILARITY:
                    cluster.append(lj)
                    used.add(lj["lesson_id"])
            clusters.append(cluster)

        for cluster in clusters:
            if len(cluster) < 2:
                continue  # no merge happened — the lesson stays INTAKE
            canonical = min(cluster, key=lambda l: l["captured_at"])
            for l in cluster:
                l["status"] = "MERGED"
                l["canonical_id"] = canonical["lesson_id"]
            cmp_id = _id("cmp", "merge", "|".join(sorted(l["lesson_id"] for l in cluster)), at)
            self.compounds[cmp_id] = {
                "compound_id": cmp_id, "kind": "MERGE",
                "lesson_ids": sorted(l["lesson_id"] for l in cluster),
                "canonical_id": canonical["lesson_id"],
                "resulting_artifact": f"living-note:{canonical['lesson_id']}",
                "cycle": cycle_id, "at": at}
            merged += 1
            for l in cluster:
                cid = l["connection_id"]
                self.connections[cid]["stats"]["compounds"] += 1
                self._log("compound.recorded", self.compounds[cmp_id])

        # Distill: ELEVATE — merged clusters propose to the canonical index.
        merged_lessons = [l for l in self.lessons.values() if l["status"] == "MERGED"]
        canon_groups = {}
        for l in merged_lessons:
            # Fail closed: a MERGED lesson with no canonical_id is corrupted state.
            # Skip and flag — never KeyError, never fake a compound.
            canonical_id = l.get("canonical_id")
            if canonical_id is None:
                flags.append({"kind": "missing_canonical_id",
                              "lesson_id": l["lesson_id"],
                              "detail": "MERGED lesson without canonical_id; skipped, no compound"})
                continue
            canon_groups.setdefault(canonical_id, []).append(l)
        for canon_id, group in canon_groups.items():
            if len(group) >= ELEVATE_MIN_CLUSTER and not any(
                    c["kind"] == "ELEVATE" and c["canonical_id"] == canon_id
                    for c in self.compounds.values()):
                cmp_id = _id("cmp", "elevate", canon_id, at)
                self.compounds[cmp_id] = {
                    "compound_id": cmp_id, "kind": "ELEVATE",
                    "lesson_ids": sorted(l["lesson_id"] for l in group),
                    "canonical_id": canon_id,
                    # G6: a proposal to the approval system, NOT canon yet.
                    "resulting_artifact": f"law-proposal:{canon_id}",
                    "cycle": cycle_id, "at": at}
                elevated += 1
                for l in group:
                    l["status"] = "ELEVATED"
                self._log("compound.recorded", self.compounds[cmp_id])

        cycle = {"cycle_id": cycle_id, "at": at,
                 "intake_processed": len(intake), "merged": merged,
                 "elevated": elevated, "compounds_total": len(self.compounds),
                 "flags": flags}
        self.cycles.append(cycle)
        self._log("cycle.completed", cycle)
        self._persist()
        return cycle

    # ---- G4: feedback ----
    def feedback_for(self, connection_id):
        if connection_id not in self.connections:
            raise ValueError(f"unknown connection: {connection_id}")
        my_lessons = [l for l in self.lessons.values() if l["connection_id"] == connection_id]
        my_lesson_ids = {l["lesson_id"] for l in my_lessons}
        my_compound_ids = {c["compound_id"] for c in self.compounds.values()
                           if any(lid in my_lesson_ids for lid in c["lesson_ids"])}
        return {"connection_id": connection_id,
                "lessons": [l["lesson_id"] for l in my_lessons],
                "compounds": sorted(my_compound_ids),
                "compound_count": self.connections[connection_id]["stats"]["compounds"],
                "cycles_run": len(self.cycles)}

    def _log(self, kind, payload):
        self._events.append({"kind": kind, "at": _now(), "payload": payload})

    def _persist(self):
        ledger = os.path.join(self.evidence_dir, "ledger.jsonl")
        with open(ledger, "a") as f:
            for e in self._events:
                f.write(json.dumps(e) + "\n")
        self._events.clear()
        state = os.path.join(self.evidence_dir, "state.json")
        with open(state, "w") as f:
            json.dump({"doors": self.doors, "connections": self.connections,
                       "lessons": self.lessons, "compounds": self.compounds,
                       "cycles": self.cycles}, f, indent=1)


if __name__ == "__main__":
    print("smart_connect.py is a library; run the proof gate: pytest tests/test_smart_connect_open_doors.py")
