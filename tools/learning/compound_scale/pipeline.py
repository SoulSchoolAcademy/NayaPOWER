"""The five pipeline stages: capture -> distill -> inject -> verify -> compound.

Capture emits learning-event-candidate/v1 records (the same schema the
error-signal loop uses), so candidates from any capture source flow through
one canonical path. Distill is a real extractive function, not a lookup:
it scores the note's sentences and returns the best one-liner. Inject loads
the distilled lesson from the PERSISTED store (the canonical path every
subject, including cold successors, goes through). Verify runs the four
arms. Compound records the lesson and proves durability across a fresh
process boundary.
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

import fixtures
import gates
import subjects

SCHEMA = "learning-event-candidate/v1"

_IMPERATIVES = {
    "write", "use", "run", "check", "never", "always", "quote", "record",
    "build", "re-verify", "rehearse", "clear", "provide", "add", "keep",
    "make", "do", "don't", "do not", "prefer", "choose", "take",
}


def distill(note: str) -> str:
    """Extractive distillation: the note's 'Rule:' sentence is the
    distilled principle (the capture convention in this system puts the
    durable rule in exactly one 'Rule:' sentence). Falls back to
    imperative-scoring when no Rule sentence exists. Deterministic. A
    note with no clear rule yields a vague principle — and the
    Understanding gate fails it honestly."""
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", note.strip())
                 if s.strip()]
    if not sentences:
        return ""
    for s in sentences:
        m = re.match(r"(?i)^rule\s*:\s*(.+)$", s, re.DOTALL)
        if m:
            return m.group(1).strip()
    def score(s: str) -> float:
        words = set(re.findall(r"[a-z'-]+", s.lower()))
        imp = len(words & _IMPERATIVES)
        concrete = len(re.findall(r"`[^`]+`", s)) + len(re.findall(r'"[^"]+"', s))
        return imp * 2.0 + concrete * 1.5 + len(words) * 0.02
    best = max(sentences, key=score)
    best = re.split(r"(?<=[.!?])\s+", best.strip())[0]
    return best


# ------------------------------------------------------------------ capture
def capture(lesson: dict, store_path: Path) -> dict:
    """Write a learning-event-candidate/v1 record to the store."""
    issued = _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds")
    digest = hashlib.sha256(
        f"{lesson['id']}:{issued}:{lesson['capture']['note'][:40]}".encode()
    ).hexdigest()[:10]
    event = {
        "schema": SCHEMA,
        "event_id": f"le-{issued[:10].replace('-', '')}-{digest}",
        "issued_utc": issued,
        "lesson_id": lesson["id"],
        "lesson_name": lesson["name"],
        "note": lesson["capture"]["note"],
        "source": lesson["capture"]["source"],
        "adversarial_probe": bool(lesson.get("adversarial")),
    }
    store_path.parent.mkdir(parents=True, exist_ok=True)
    with store_path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(event, ensure_ascii=False) + "\n")
    return event


# ------------------------------------------------------------------ distill
def distill_lesson(lesson: dict, events_path: Path) -> dict:
    """Run the real distill() on the lesson's note; persist the result."""
    principle = distill(lesson["capture"]["note"])
    record = {
        "lesson_id": lesson["id"],
        "principle": principle,
        "expected_principle": lesson["distill"]["principle"],
        "operative_action": lesson["distill"]["operative_action"],
        "matches_expected": principle == lesson["distill"]["principle"],
    }
    dp = events_path.parent / "distilled.jsonl"
    with dp.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    return record


# ------------------------------------------------------------------- inject
def inject(store_dir: Path, lesson_id: str, registry: dict) -> dict:
    """Canonical inject path: read the DISTILLED principle from the
    persisted store (never from memory) and build the subject's rule."""
    dp = Path(store_dir) / "distilled.jsonl"
    principle = None
    for line in dp.read_text(encoding="utf-8").splitlines():
        rec = json.loads(line)
        if rec["lesson_id"] == lesson_id:
            principle = rec["principle"]
    if principle is None:
        raise RuntimeError(f"no distilled lesson {lesson_id} in store")
    lesson = next(l for l in registry["lessons"] if l["id"] == lesson_id)
    return {
        "name": lesson["name"],
        "applies_to": lesson["rule"]["applies_to"],
        "procedure": lesson["rule"]["procedure"],
        "principle": principle,
        "receipt": {"file": lesson["truth"]["receipt_file"],
                    "quote": lesson["truth"]["receipt_quote"]},
    }


# ------------------------------------------------------------------- verify
def verify(lesson: dict, store_dir: Path, registry: dict,
           workdir: Path) -> dict:
    """Run the four arms for one lesson."""
    rule = inject(store_dir, lesson["id"], registry)
    arms = {}
    for arm in subjects.ARMS:
        arms[arm] = subjects.run_arm(lesson, arm, rule, workdir)
    return arms


# ------------------------------------------------------------------ compound
def compound(lesson: dict, arms: dict, gate_scores: dict, verdict: float,
             ledger_path: Path) -> dict:
    """Record the lesson outcome in the compound ledger."""
    entry = {
        "lesson_id": lesson["id"],
        "lesson_name": lesson["name"],
        "adversarial": bool(lesson.get("adversarial")),
        "gate_scores": gate_scores,
        "verdict": verdict,
        "proven": verdict >= 7.0,
        "recorded_utc": _dt.datetime.now(_dt.timezone.utc).isoformat(
            timespec="seconds"),
    }
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    with ledger_path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry


def durability_check(lesson: dict, store_dir: Path, registry_path: Path,
                     workdir: Path) -> tuple[bool, str]:
    """Durability across a REAL process boundary: a fresh python process
    loads the persisted store + registry and re-runs the treatment arm."""
    pkgdir = Path(__file__).resolve().parent
    code = (
        "import json, sys; "
        f"sys.path.insert(0, {str(pkgdir)!r}); "
        "import pipeline, subjects; "
        f"registry = json.load(open({str(registry_path)!r})); "
        f"lesson = next(l for l in registry['lessons'] if l['id'] == {lesson['id']!r}); "
        f"rule = pipeline.inject({str(store_dir)!r}, {lesson['id']!r}, registry); "
        f"res = subjects.run_arm(lesson, 'treatment', rule, {str(workdir)!r}); "
        "print(json.dumps({'passed': res['passed'], 'reason': res['reason']}))"
    )
    proc = subprocess.run([sys.executable, "-c", code], capture_output=True,
                          text=True, cwd="/tmp")
    if proc.returncode != 0:
        return False, f"fresh process failed: {proc.stderr.strip()[:200]}"
    try:
        res = json.loads(proc.stdout.strip().splitlines()[-1])
    except (json.JSONDecodeError, IndexError):
        return False, f"unparseable fresh-process output: {proc.stdout[:200]}"
    return bool(res["passed"]), res["reason"]
