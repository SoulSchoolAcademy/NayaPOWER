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
    capture_id: str | None = None
    lifecycle_state: str = "ACTIVE"
    superseded_by_capture_id: str | None = None
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
        res.capture_id = doc.get("capture_id")
        res.lifecycle_state = str(doc.get("lifecycle_state", "ACTIVE")).upper()
        res.superseded_by_capture_id = doc.get("superseded_by_capture_id")

    mv = _machine_view(doc, res.violations, res.advisories)

    if res.lifecycle_state not in {"ACTIVE", "SUPERSEDED"}:
        res.violations.append(
            f"lifecycle_state must be 'ACTIVE' or 'SUPERSEDED', got {res.lifecycle_state!r}"
        )

    # Historical correction law: persisted R1 intelligence is immutable. A
    # superseded capture may preserve the exact historical raw-source defect,
    # but only when it points to a conformant successor. check_dir() verifies
    # that cross-capture relationship and the successor's SUPERSEDES edge.
    raw = mv.get("raw_source_separate_from_distillation", None)
    if res.lifecycle_state == "SUPERSEDED":
        if not isinstance(res.superseded_by_capture_id, str) or not res.superseded_by_capture_id.strip():
            res.violations.append(
                "SUPERSEDED capture requires superseded_by_capture_id"
            )
        if not isinstance(doc.get("supersession_reason"), str) or not doc.get("supersession_reason", "").strip():
            res.violations.append("SUPERSEDED capture requires supersession_reason")
        if raw is None:
            res.advisories.append(
                "historical superseded capture preserves missing "
                "machine_view.raw_source_separate_from_distillation; successor "
                "must carry the corrected typed boundary"
            )
        elif raw is not True:
            res.violations.append(
                "if present on a SUPERSEDED capture, "
                "machine_view.raw_source_separate_from_distillation must be "
                f"boolean true, got {raw!r}"
            )
    elif raw is not True:
        # Typed boolean. `is True` deliberately rejects 1, "true", "yes", truthy junk.
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
    """Check every capture and close the supersession relation fail-closed.

    A historical malformed capture cannot self-exempt merely by declaring
    SUPERSEDED. Its named successor must exist in the same canonical capture
    directory, must itself conform, must remain ACTIVE, and must carry an
    explicit SUPERSEDES connection back to the historical capture/Smart Note.
    """
    files = sorted(Path(directory).glob("SMART-NOTE-*.json"))
    results = [check_capture(f) for f in files]
    by_capture_id = {r.capture_id: r for r in results if r.capture_id}
    file_by_capture_id = {r.capture_id: f for r, f in zip(results, files) if r.capture_id}

    for res in results:
        if res.lifecycle_state != "SUPERSEDED":
            continue
        target_id = str(res.superseded_by_capture_id or "").strip()
        successor = by_capture_id.get(target_id)
        if successor is None:
            res.violations.append(
                f"superseded_by_capture_id target not found: {target_id!r}"
            )
        elif successor.lifecycle_state == "SUPERSEDED":
            res.violations.append(
                f"supersession target {target_id!r} is itself SUPERSEDED"
            )
        elif not successor.conformant:
            res.violations.append(
                f"supersession target {target_id!r} is non-conformant"
            )
        else:
            try:
                successor_doc = json.loads(
                    file_by_capture_id[target_id].read_text(encoding="utf-8")
                )
            except (OSError, ValueError):
                successor_doc = {}
            connections = successor_doc.get("intelligence", {}).get("connections", [])
            needles = {
                str(res.capture_id or "").lower(),
                str(res.smart_note_id or "").lower(),
            }
            has_edge = False
            for edge in connections if isinstance(connections, list) else []:
                if not isinstance(edge, dict):
                    continue
                rel = str(edge.get("type") or edge.get("relationship_type") or "").upper()
                target = str(edge.get("target") or edge.get("target_block_id") or "").lower()
                if rel == "SUPERSEDES" and any(n and n in target for n in needles):
                    has_edge = True
                    break
            if not has_edge:
                res.violations.append(
                    f"supersession target {target_id!r} must carry an explicit "
                    "SUPERSEDES edge to the historical capture or Smart Note ID"
                )
        res.conformant = not res.violations

    return results


def failures_only(results: list[ConformanceResult]) -> list[ConformanceResult]:
    return [r for r in results if not r.conformant]


BASELINE_PATH = Path(".naya/conformance-baseline.json")


def load_baseline(path: str | Path | None = None) -> set[str]:
    """Load the grandfathered legacy-capture exemption set (filenames).

    A missing baseline is an empty set, which means nothing is exempt. That is
    the safe direction: it fails closed rather than silently allowing drift.
    """
    p = Path(path) if path else BASELINE_PATH
    if not p.is_file():
        return set()
    try:
        doc = json.loads(p.read_bytes().decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return set()
    exempt = doc.get("exempt")
    return set(exempt) if isinstance(exempt, list) else set()


def ratchet_violations(
    results: list[ConformanceResult],
    baseline: set[str] | None = None,
) -> list[ConformanceResult]:
    """Failures that are NOT grandfathered.

    The ratchet: new and changed captures must conform. Pre-existing debt named
    in the baseline is reported but does not block. The baseline can only ever
    shrink, so the debt is monotonic and cannot quietly grow.
    """
    exempt = load_baseline() if baseline is None else baseline
    out = []
    for r in results:
        if r.conformant:
            continue
        name = Path(r.path).name
        if name in exempt:
            continue
        out.append(r)
    return out


def stale_baseline_entries(
    results: list[ConformanceResult],
    baseline: set[str] | None = None,
) -> set[str]:
    """Baseline entries that now CONFORM -- the repair landed, drop them.

    A baseline that never shrinks stops being a ratchet and becomes a
    permanent exemption. This is how the debt gets retired.
    """
    exempt = load_baseline() if baseline is None else baseline
    return {
        Path(r.path).name
        for r in results
        if r.conformant and Path(r.path).name in exempt
    }


def _main(argv: list[str] | None = None) -> int:
    """CLI so this can be a real gate rather than a script nobody runs.

    --check   blocking. Exit 1 if any capture fails governance conformance.
    --report  advisory. Always exits 0; prints the same findings.

    Default is --report, because flipping main's CI to blocking is a
    consequence that belongs to the Human Director, not to the tool's author.
    Once the five known captures are backfilled, change the CI step to --check
    and this becomes fail-closed against the whole drift class.
    """
    import argparse

    ap = argparse.ArgumentParser(
        prog="sn002_conformance",
        description="Mechanical SN-002 capture conformance gate.",
    )
    ap.add_argument("--check", action="store_true",
                    help="blocking: exit 1 if any capture fails")
    ap.add_argument("--report", action="store_true",
                    help="advisory (default): always exit 0")
    ap.add_argument("--dir", default=".naya/capture")
    ap.add_argument("--ratchet", action="store_true",
                    help="block only on non-grandfathered failures")
    args = ap.parse_args(argv)
    blocking = bool(args.check) or bool(args.ratchet)

    results = check_dir(args.dir)
    if not results:
        print(f"no captures found in {args.dir}")
        return 1 if blocking else 0

    bad = failures_only(results)
    print(f"SN-002 capture conformance: {len(results) - len(bad)}/{len(results)} pass")

    for r in bad:
        print(f"  FAIL {r.smart_note_id or '(no smart_note_id)'}  {r.path}")
        for v in r.violations:
            print(f"        - {v}")
        for a in r.advisories:
            print(f"        ~ {a}")

    if args.ratchet:
        ungrand = ratchet_violations(results)
        stale = stale_baseline_entries(results)
        if stale:
            print("BASELINE ENTRIES NOW CONFORM (drop them to retire the debt):")
            for n in sorted(stale):
                print(f"  * {n}")
        print(f"ratchet: {len(ungrand)} non-grandfathered failure(s), "
              f"{len(bad) - len(ungrand)} grandfathered")
        for r in ungrand:
            label = r.smart_note_id or "(no smart_note_id)"
            print(f"  BLOCKED {label}  {r.path}")
            for v in r.violations:
                print(f"          - {v}")
        if ungrand:
            print("RATCHET FAIL: a capture outside the baseline is non-conformant")
            return 1
        print("RATCHET PASS")
        return 0

    if blocking and bad:
        print(f"FAIL: {len(bad)} capture(s) non-conformant")
        return 1
    if bad:
        print(f"advisory: {len(bad)} capture(s) non-conformant (not blocking)")
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())