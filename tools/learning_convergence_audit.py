#!/usr/bin/env python3
"""Learning convergence audit (convergence items B / C / D).

Two stage systems describe the same learning, and until this run nothing
checked whether they agree:

  * the learn-clock (T0..T7) — clock rows in learn-clock.jsonl carry the
    stage sequence; meta rows in learn-lessons.jsonl carry the per-stage
    typed evidence the tail wire (learn_clock_tail.py) enforces at emit.
  * the evidence ladder (E0..E7) — tools/learning_evidence_ladder.py
    computes the EARNED level from observable evidence bundles.

This module is a READ-ONLY cross-check over one lesson's rows in both
logs. It never writes, never emits, never promotes. Per lesson:

  (B) LINEAGE — is the full chain reconstructable? Clock stages must be
      contiguous 0..max with no gaps, no duplicate (lesson, stage) rows,
      non-decreasing clock timestamps, and a 1:1 join to meta rows
      (every clock row has exactly one meta row; every non-probe meta
      row has a clock row). T6_PROBE meta rows are probe history, never
      a T6. Meta `ts` is NOT compared to clock `ts`: pre-fix rows carry
      write-time in meta `ts` (P-003); clock rows carry event time.
  (C) EVIDENCE — does each stage's meta row carry its typed contract?
      Only stages that HAVE a meta row are evaluated (stages without one
      are B's jurisdiction: CLOCK_WITHOUT_META). C_stages_checked records
      exactly which stages were evaluated and C_coverage is FULL or
      PARTIAL:<unchecked>, so a PASS is never misread as complete
      evidence.
      T0: title + evidence. T1/T2: evidence. T3: one-sentence principle
      + enforcement >= 20 chars + evidence. T4: 64-hex brief_hash +
      principle_ids including this lesson + evidence. T5:
      changed_decision >= 10 chars + evidence. T6: judge != author
      (Inviolable, casefold) + verdict PASS + evidence. T7: pr > 0 +
      40-hex merge_sha + evidence. Same thresholds as the tail wire.
  (D) RECEIPT — durable application receipt linked to outcome + IV:
      PASS iff T6 clock+meta exist with (C) PASS at T6 and latency
      (T6 ts - T0 ts) computable; PARTIAL if T5 exists without T6;
      ABSENT if no T5. A FAIL / NO-TRANSFER-MEASURED T6_PROBE with no
      T6 is correctly unverified, never counted as verified.
  (E) CROSS-CHECK — the ladder's earned level from the clock's evidence,
      built STRICTLY (nothing synthesized from prose): capture_receipt
      from a T1 row with evidence; comprehension / application /
      outcome / transfer / successor_use / retention / mastery have NO
      producer in the clock's meta contracts (the wire records no
      control_receipt, treatment_receipt, retrieval_ref, task_ref,
      applier, or measured_effect), so they are absent by construction.
      Earned is therefore E0 iff T1 exists, else UNPROVEN. A lesson at
      T6 whose ladder earned level is below E3 is flagged DIVERGENCE:
      the two systems disagree about verification. That flag is the
      convergence hole made mechanical — it is not a failure of either
      system, it is the named-next: the T6 meta contract must carry the
      control/treatment receipts the ladder needs for E1 before the
      systems can agree.

Bulk-write signal: >= 3 distinct lessons sharing one identical clock
(stage, ts) is reported as BULK_TS (a signal, never a verdict) — the
live log's five T2 rows all stamped 04:47:00Z are the example: one
triage pass, recorded in bulk.

Malformed JSONL lines are counted, never fatal. Missing input files
are a hard error (exit 2): an audit of nothing is not a pass.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

try:
    from learning_evidence_ladder import evaluate as ladder_evaluate
except Exception as _ladder_import_error:  # pragma: no cover - missing sidecar
    ladder_evaluate = None
    _LADDER_IMPORT_ERROR = str(_ladder_import_error)
else:
    _LADDER_IMPORT_ERROR = ""

SCHEMA = "NAYANET_LEARNING_CONVERGENCE_AUDIT_V1"
CLOCK_DIR = Path.home() / "workspace" / "_scratch" / "learn-clock"

_HEX = set("0123456789abcdefABCDEF")
_STAGE_NAMES = {
    0: "T0_EVENT",
    1: "T1_CAPTURED",
    2: "T2_TRIAGED",
    3: "T3_DISTILLED",
    4: "T4_INJECTED",
    5: "T5_APPLIED",
    6: "T6_VERIFIED",
    7: "T7_COMPOUNDED",
}


def _parse_ts(value):
    """ISO-8601 -> aware datetime, or None (fail-closed, never raises)."""
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        dt = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except ValueError:
        return None
    return dt


def _nonempty(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _is_hex(value, n) -> bool:
    return (
        isinstance(value, str)
        and len(value) == n
        and all(c in _HEX for c in value)
    )


def _one_sentence(value) -> bool:
    """Tail-wire rule: exactly one terminator group, trailing."""
    if not _nonempty(value):
        return False
    groups = re.findall(r"[.!?]+", value)
    return len(groups) == 1 and value.rstrip().endswith(groups[0])


def _read_jsonl(path: Path):
    rows = []
    malformed = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            malformed += 1
    return rows, malformed


def _stage_contract(stage: int, meta: dict, lesson_id: str):
    """Return a failure reason string, or '' when the contract holds."""
    if stage == 0:
        if not _nonempty(meta.get("title")):
            return "T0 missing title"
        if not _nonempty(meta.get("evidence")):
            return "T0 missing evidence"
        return ""
    if stage in (1, 2):
        if not _nonempty(meta.get("evidence")):
            return f"T{stage} missing evidence"
        return ""
    if stage == 3:
        if not _one_sentence(meta.get("principle")):
            return "T3 principle must be exactly one sentence"
        if not _nonempty(meta.get("enforcement")) or len(str(meta.get("enforcement"))) < 20:
            return "T3 enforcement must name what breaks (>= 20 chars)"
        if not _nonempty(meta.get("evidence")):
            return "T3 missing evidence"
        return ""
    if stage == 4:
        if not _is_hex(meta.get("brief_hash"), 64):
            return "T4 brief_hash must be 64 hex chars"
        ids = meta.get("principle_ids")
        if not isinstance(ids, list) or not ids:
            return "T4 principle_ids required (at least one LC- id)"
        if lesson_id not in ids:
            return f"T4 principle_ids must include this lesson {lesson_id}"
        if not _nonempty(meta.get("evidence")):
            return "T4 missing evidence"
        return ""
    if stage == 5:
        if not _nonempty(meta.get("changed_decision")) or len(str(meta.get("changed_decision"))) < 10:
            return "T5 changed_decision too short to be a quoted decision"
        if not _nonempty(meta.get("evidence")):
            return "T5 missing evidence"
        return ""
    if stage == 6:
        judge = meta.get("judge_seat")
        author = meta.get("author_seat")
        if not _nonempty(judge) or not _nonempty(author):
            return "T6 requires judge_seat + author_seat"
        if str(judge).casefold() == str(author).casefold():
            return "T6 judge_seat must differ from author_seat (Inviolable)"
        if meta.get("verdict") != "PASS":
            return "T6 verdict must be PASS (FAIL / NO-TRANSFER emits no T6)"
        if not _nonempty(meta.get("evidence")):
            return "T6 missing evidence"
        return ""
    if stage == 7:
        pr = meta.get("pr")
        if not isinstance(pr, int) or isinstance(pr, bool) or pr <= 0:
            return "T7 pr must be a merged PR number"
        if not _is_hex(meta.get("merge_sha"), 40):
            return "T7 merge_sha must be 40 hex chars"
        if not _nonempty(meta.get("evidence")):
            return "T7 missing evidence"
        return ""
    return f"unknown stage {stage}"


def _audit_lesson(lesson_id, clock_rows, meta_rows, probe_rows):
    """Audit one lesson. clock_rows/meta_rows keyed by stage; probe_rows
    are T6_PROBE meta rows (never a T6)."""
    failures_b = []
    failures_c = []

    # ---- (B) lineage ----
    stages = sorted(clock_rows)
    if not stages:
        failures_b.append("NO_CLOCK_ROWS")
    else:
        if stages != list(range(0, stages[-1] + 1)):
            missing = [s for s in range(0, stages[-1] + 1) if s not in stages]
            failures_b.append(f"GAP: missing clock stages {missing}")
        parsed = []
        for s in stages:
            dt = _parse_ts(clock_rows[s].get("ts"))
            if dt is None:
                failures_b.append(f"TS_UNPARSEABLE: T{s} ts={clock_rows[s].get('ts')!r}")
            parsed.append((s, dt))
        for (s0, d0), (s1, d1) in zip(parsed, parsed[1:]):
            if d0 is not None and d1 is not None and d1 < d0:
                failures_b.append(f"TS_REGRESSION: T{s1} ts before T{s0} ts")
        for s in stages:
            if s not in meta_rows:
                failures_b.append(f"CLOCK_WITHOUT_META: T{s} has no meta row")
        for s in sorted(meta_rows):
            if s not in clock_rows:
                failures_b.append(f"META_WITHOUT_CLOCK: orphan meta row T{s}")

    # ---- (C) evidence contracts ----
    # C only evaluates stages that HAVE meta rows; stages without one are
    # B's jurisdiction (CLOCK_WITHOUT_META). Record the checked set so a
    # PASS is never misread as "evidence complete": coverage says exactly
    # which clock stages were checked and which were not.
    checked_c = []
    for s in stages:
        if s in meta_rows:
            checked_c.append(s)
            reason = _stage_contract(s, meta_rows[s], lesson_id)
            if reason:
                failures_c.append(reason)
    unchecked_c = [s for s in stages if s not in meta_rows]
    c_coverage = "FULL" if not unchecked_c else f"PARTIAL: T{',T'.join(map(str, unchecked_c))} unchecked (no meta row)"

    # ---- (D) receipt ----
    probes = [
        {"verdict": p.get("verdict"), "judge_seat": p.get("judge_seat"),
         "author_seat": p.get("author_seat"), "ts": p.get("ts")}
        for p in probe_rows
    ]
    latency_min = None
    if 6 in clock_rows and 6 in meta_rows and not any(
        f.startswith("T6 ") for f in failures_c
    ):
        t0 = _parse_ts(clock_rows[0].get("ts")) if 0 in clock_rows else None
        t6 = _parse_ts(clock_rows[6].get("ts"))
        if t0 is not None and t6 is not None:
            latency_min = round((t6 - t0).total_seconds() / 60.0, 2)
        receipt = "PASS" if latency_min is not None else "PARTIAL"
        if latency_min is None:
            failures_c.append("T6 latency not computable (unparseable T0/T6 ts)")
    elif 5 in clock_rows:
        receipt = "PARTIAL"
    else:
        receipt = "ABSENT"

    # ---- (E) ladder cross-check (strict: nothing synthesized) ----
    evidence = {}
    if 1 in clock_rows and 1 in meta_rows and _nonempty(meta_rows[1].get("evidence")):
        evidence["capture_receipt"] = {
            "intelligent_block_id": lesson_id,
            "captured_at": clock_rows[1].get("ts"),
        }
    # comprehension / application_receipt / outcome / transfer /
    # successor_use / retention / mastery: NO producer in the clock's
    # meta contracts — deliberately left absent, never synthesized.
    if ladder_evaluate is not None:
        result = ladder_evaluate(
            {"id": lesson_id, "claimed_level": "E0_EXPOSED", "evidence": evidence}
        )
        earned = result.get("earned_level")
        e_first_unproven = (result.get("unproven") or [""])[0]
    else:  # pragma: no cover - missing sidecar
        earned = "UNKNOWN"
        e_first_unproven = f"ladder import failed: {_LADDER_IMPORT_ERROR}"

    divergence = ""
    if 6 in clock_rows and earned not in ("E3_INDEPENDENT", "E4_TRANSFER",
                                          "E5_CAN_TEACH", "E6_RETAINED", "E7_MASTERED"):
        divergence = (
            f"clock claims T6_VERIFIED but ladder earns {earned}: "
            "T6 meta carries no control/treatment receipts (E1), no "
            "retrieval_ref/task_ref/applier (E2), no measured_effect (E3)"
        )

    return {
        "lesson_id": lesson_id,
        "max_clock_stage": stages[-1] if stages else None,
        "max_clock_stage_name": _STAGE_NAMES.get(stages[-1]) if stages else None,
        "B_lineage": "PASS" if not failures_b else "FAIL",
        "B_failures": failures_b,
        "C_evidence": "PASS" if not failures_c else "FAIL",
        "C_failures": failures_c,
        "C_stages_checked": checked_c,
        "C_coverage": c_coverage,
        "D_receipt": receipt,
        "D_latency_min": latency_min,
        "D_probes": probes,
        "E_earned": earned,
        "E_first_unproven": e_first_unproven,
        "E_e1_producer": "NONE — no clock stage emits control_receipt/treatment_receipt",
        "E_divergence": divergence,
    }


def audit(clock_path: Path, meta_path: Path) -> dict:
    """Run the convergence audit over both logs. Pure: reads only."""
    clock_all, clock_malformed = _read_jsonl(Path(clock_path))
    meta_all, meta_malformed = _read_jsonl(Path(meta_path))

    clock_by_lesson: dict[str, dict[int, dict]] = {}
    clock_dupes: list[str] = []
    for row in clock_all:
        lid = row.get("lesson_id")
        stage = row.get("stage")
        if not isinstance(lid, str) or not isinstance(stage, int) or isinstance(stage, bool):
            clock_dupes.append(f"MALFORMED_CLOCK_ROW: {str(row)[:120]}")
            continue
        bucket = clock_by_lesson.setdefault(lid, {})
        if stage in bucket:
            clock_dupes.append(f"DUPLICATE_CLOCK: {lid} T{stage}")
        bucket.setdefault(stage, row)

    meta_by_lesson: dict[str, dict[int, dict]] = {}
    probes_by_lesson: dict[str, list[dict]] = {}
    meta_dupes: list[str] = []
    for row in meta_all:
        lid = row.get("lesson_id")
        stage = row.get("stage")
        if not isinstance(lid, str):
            meta_dupes.append(f"MALFORMED_META_ROW: {str(row)[:120]}")
            continue
        if stage == "T6_PROBE":
            probes_by_lesson.setdefault(lid, []).append(row)
            continue
        if not isinstance(stage, int) or isinstance(stage, bool):
            meta_dupes.append(f"MALFORMED_META_ROW: {str(row)[:120]}")
            continue
        bucket = meta_by_lesson.setdefault(lid, {})
        if stage in bucket:
            meta_dupes.append(f"DUPLICATE_META: {lid} T{stage}")
        bucket.setdefault(stage, row)

    lesson_ids = sorted(set(clock_by_lesson) | set(meta_by_lesson) | set(probes_by_lesson))
    lessons = []
    for lid in lesson_ids:
        entry = _audit_lesson(
            lid,
            clock_by_lesson.get(lid, {}),
            meta_by_lesson.get(lid, {}),
            probes_by_lesson.get(lid, []),
        )
        # Duplicate rows are lineage failures attached to the lesson.
        dup_here = [d for d in clock_dupes + meta_dupes if d.startswith(("DUPLICATE",)) and lid in d]
        if dup_here:
            entry["B_lineage"] = "FAIL"
            entry["B_failures"] = sorted(set(entry["B_failures"]) | set(dup_here))
        lessons.append(entry)

    # Bulk-write signal: >= 3 distinct lessons, same (stage, ts).
    bulk_groups: dict[tuple, set] = {}
    for row in clock_all:
        if isinstance(row.get("stage"), int) and isinstance(row.get("ts"), str):
            bulk_groups.setdefault((row["stage"], row["ts"]), set()).add(row.get("lesson_id"))
    bulk_ts = [
        {"stage": s, "ts": ts, "lessons": sorted(lids), "count": len(lids)}
        for (s, ts), lids in sorted(bulk_groups.items())
        if len(lids) >= 3
    ]

    return {
        "schema": SCHEMA,
        "clock_rows": len(clock_all),
        "meta_rows": len(meta_all),
        "malformed_lines": {"clock": clock_malformed, "meta": meta_malformed},
        "global_anomalies": [d for d in clock_dupes + meta_dupes if d.startswith("MALFORMED")],
        "lessons": lessons,
        "summary": {
            "lessons": len(lessons),
            "B_pass": sum(1 for e in lessons if e["B_lineage"] == "PASS"),
            "C_pass": sum(1 for e in lessons if e["C_evidence"] == "PASS"),
            "D_pass": sum(1 for e in lessons if e["D_receipt"] == "PASS"),
            "D_partial": sum(1 for e in lessons if e["D_receipt"] == "PARTIAL"),
            "D_absent": sum(1 for e in lessons if e["D_receipt"] == "ABSENT"),
            "E_earned_distribution": {
                lvl: sum(1 for e in lessons if e["E_earned"] == lvl)
                for lvl in sorted({e["E_earned"] for e in lessons})
            },
            "E_divergences": [e["lesson_id"] for e in lessons if e["E_divergence"]],
            "bulk_ts_signals": bulk_ts,
        },
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="learning convergence audit (B/C/D)")
    ap.add_argument("--clock", default=str(CLOCK_DIR / "learn-clock.jsonl"))
    ap.add_argument("--meta", default=str(CLOCK_DIR / "learn-lessons.jsonl"))
    args = ap.parse_args(argv)
    clock_path, meta_path = Path(args.clock), Path(args.meta)
    for p in (clock_path, meta_path):
        if not p.is_file():
            print(json.dumps({"error": f"missing input file: {p}"}), file=sys.stderr)
            return 2
    print(json.dumps(audit(clock_path, meta_path), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
