#!/usr/bin/env python3
"""Canonical lineage/playback projection over existing evidence objects.

No new persistence: callers supply existing receipt/event/block records and get
a deterministic, auditable causal path for replay.
"""
from __future__ import annotations
from typing import Any

ORDER=("source","event","evidence","verification","result","receipt","learning","block","checkpoint","successor")

def build_lineage(*, source: dict, event: dict|None=None, evidence: list[dict]|None=None,
                  verification: dict|None=None, result: dict|None=None, receipt: dict|None=None,
                  learning: list[dict]|None=None, block: dict|None=None,
                  checkpoint: dict|None=None, successor: dict|None=None) -> dict:
    objects={"source":source,"event":event,"evidence":evidence or [],
             "verification":verification,"result":result,"receipt":receipt,
             "learning":learning or [],"block":block,"checkpoint":checkpoint,"successor":successor}
    present=[k for k in ORDER if objects[k]]
    gaps=[k for k in ORDER if k in {"source","event","receipt"} and not objects[k]]
    return {"schema":"NAYAPOWER_LINEAGE_PLAYBACK_V1","status":"COMPLETE" if not gaps else "PARTIAL",
            "ordered_stages":present,"gaps":gaps,"objects":objects}

def playback(lineage: dict) -> list[dict]:
    """Return only existing lineage stages; never invent missing transitions."""
    return [{"stage":stage,"present":stage in lineage.get("ordered_stages",[]),
             "object":lineage.get("objects",{}).get(stage)}
            for stage in ORDER]
