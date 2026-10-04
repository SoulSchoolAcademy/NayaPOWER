"""Coda 1: mechanical SN-002 capture conformance gate.

WHY THIS EXISTS
---------------
Measured 2026-10-04. Phase 1 calls for "mechanical SN-002 conformance" as the
repair for the RED cold-successor captures. It did not exist:
`tools/smart_note_v2.py` offers discover/project/retrieve/held-out/promote and
NONE of them validate. Running `discover` against a known-good capture, a
known-broken capture, and a newly authored one returns identical output and
exit 0 -- it does not discriminate.

The only raw-source check anywhere is inside `held_out()`, and it is a
substring match over the RENDERED MARKDOWN:

    raw_separate = ("raw_source_separate_from_distillation" in low and "true" in low) \\
                or ("transcript" in low and "not intelligence" in low)

That is a false-pass surface: prose containing the words satisfies it, and a
conformant capture whose field the renderer drops would fail it. A false-pass
surface is worse than no gate because it manufactures confidence.

WHAT THIS GATE DOES INSTEAD
---------------------------
Asserts TYPED values on the CAPTURE JSON. No substring matching, no reliance on
the renderer.

  machine_view.raw_source_separate_from_distillation  is True   (bool, not truthy)
  machine_view.automatic_truth_ceiling               == "CANDIDATE"

Also enforces schema identity and the required structural keys, so a capture
cannot pass by omitting the machine_view entirely.

ADditive only. Touches no runtime, no workflow, no existing capture.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

CAPTURE_SCHEMA = "naya.smart-note-capture.v2"
CEILING_REQUIRED = "CANDIDATE"

REQUIRED_TOP_KEYS = (
    "schema", "smart_note_id", "capture_id", "title", "category",
    "topic", "subtopic", "canonical_intent", "source", "projection",
    "intelligence",
)
REQUIRED_INTELLIGENCE_KEYS = (
    "essence", "human_view", "simple_view", "naya_view", "ai_view",
    "machine_view", "decisions", "connections", "uncertainty",
    "applicability", "learning_lesson", "successor_effect",
)


@dataclass
class ConformanceResult:
    """Outcome of one capture check. Never raises: reports.

    TWO DISTINCT VERDICTS, deliberately separated.

    `violations` are BLOCKING: governance conformance. These are what the
    cold-successor comprehension gate actually asserts on, and their absence is
    the measured cause of the RED captures.

    `advisories` are NON-BLOCKING: structural completeness against fields added
    later (notably `ai_view`, absent in 13 of 19 historical captures, and
    `successor_effect`, absent in 7). Those captures predate the fields. Folding
    them into the blocking verdict would fail every historical capture for a
    reason unrelated to the defect, and a gate that rejects everything is as
    useless as one that accepts everything.
    """

    path: str
    smart_note_id: str | None = None
    conformant: bool = False
    violations: list[str] = field(default_factory=list)
    advisories: list[str] = field(default_factory=list)

    def __bool__(self) -> bool:  # pragma: no cover - trivial
        return self.conformant

    @property
    def status(self) -> str:
        return "PASS" if self.conformant else "FAIL"


def _machine_view(doc: Any, v: list[str], adv: list[str]) -> dict:
    if not isinstance(doc, dict):
        v.append("capture is not a JSON object")
        return {}
    for key in REQUIRED_TOP_KEYS:
        if key not in doc:
            v.append(f"missing required top-level key: {key}")
    if doc.get("schema") != CAPTURE_SCHEMA:
        v.append(f"schema must be {CAPTURE_SCHEMA!r}, got {doc.get('schema')!r}")
    intel = doc.get("intelligence")
    if not isinstance(intel, dict):
        v.append("intelligence must be a JSON object")
        return {}
    for key in REQUIRED_INTELLIGENCE_KEYS:
        if key not in intel:
            adv.append(
                f"structural: intelligence.{key} absent (field postdates this "
                "capture; non-blocking)"
            )
    mv = intel.get("machine_view")
    if not isinstance(mv, dict):
        v.append("machine_view must be a JSON object (cannot pass by omission)")
        return {}
    return mv


def check_capture(path: str | Path) -> ConformanceResult:
    """Check one capture file. Reports; never raises on malformed input."""
    p = Path(path)
    res = ConformanceResult(path=str(p))
    try:
        doc = json.loads(p.read_bytes().decode("utf-8"))
    except UnicodeDecodeError as exc:
        res.violations.append(f"not valid UTF-8: {exc}")
        return res
    except json.JSONDecodeError as exc:
        res.violations.append(f"not valid JSON: {exc}")
        return res

    if isinstance(doc, dict):
        res.smart_note_id = doc.get("smart_note_id")

    mv = _machine_view(doc, res.violations, res.advisories)

    # Typed boolean. `is True` deliberately rejects 1, "true", "yes", truthy junk.
    raw = mv.get("raw_source_separate_from_distillation", None)
    if raw is not True:
        res.violations.append(
            "machine_view.raw_source_separate_from_distillation must be the "
            f"boolean true, got {raw!r} (type {type(raw).__name__})"
        )

    ceiling = mv.get("automatic_truth_ceiling", None)
    if ceiling != CEILING_REQUIRED:
        res.violations.append(
            f"machine_view.automatic_truth_ceiling must be "
            f"{CEILING_REQUIRED!r}, got {ceiling!r}"
        )

    res.conformant = not res.violations
    return res


def check_dir(directory: str | Path) -> list[ConformanceResult]:
    """Check every capture in a directory, sorted for deterministic output."""
    return [
        check_capture(f)
        for f in sorted(Path(directory).glob("SMART-NOTE-*.json"))
    ]


def failures_only(results: list[ConformanceResult]) -> list[ConformanceResult]:
    return [r for r in results if not r.conformant]