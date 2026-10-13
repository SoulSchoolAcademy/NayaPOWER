"""hive-learning-law.py — THE HIVE LEARNING LAW (Naya 5, 2026-10-13).

Machine-enforced components. Fail closed everywhere. Part of the code,
part of who we are. Same pattern as the Naya Contract.

  1. PROOF GATE    - no lesson promotes without all 7 fields, a specific
                     falsifier, and a duplicate check. B-48 is structurally
                     impossible (stance check: a lesson cannot disavow its
                     own trigger and promote as guidance).
  2. ADOPTION CHECKER - automates the verification we did manually: a
                     MECHANIZED lesson's check_ref must exist and, when it
                     names a test, that test must PASS. Otherwise NOT_ADOPTED.
  3. VELOCITY TRACKER - measures learning rate from lesson history; flags
                     DEGRADED when adoption drops below the bar.
  4. SURPRISE SIGNAL SCHEMA - the machine contract for what workers emit
                     at the NOTICE step: fixed fields, validated, fail-closed.
  5. BYTE INTEGRITY  - tamper with the law, it refuses to run. The file
                     hashes its own bytes at import (LAW_SHA256 line blanked,
                     newlines normalized). Mismatch -> SystemExit.

The 7 fields: trigger, principle, enforcement, evidence, falsifier,
               provenance, trial.

The falsifier is the Popperian tooth: every lesson must name what would
prove it WRONG, specifically. A lesson that cannot be falsified cannot
be tested; a lesson that cannot be tested cannot promote.

Lifecycle (compact): new_lesson -> admit (intake triage) -> promote
(proof gate) -> mechanize (check_ref) -> [reinforce | sweep -> RETIRED].
rewrite() spawns a successor; drop() ends with reason. MECHANIZED never
decays — the building stands.

Usage:
  python3 hive-learning-law.py --check      # integrity + self-test
  python3 hive-learning-law.py --pin        # print the blessed SHA256
  python3 hive-learning-law.py --sweep store.json
"""

import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

LAW_VERSION = "1"
LAW_SHA256 = "c27675aebfc71967423f60159fc34d4229e3c21976cc1424ccc00db158c6ef40"  # PINNED 2026-10-13 via --pin

REPO_ROOT = Path(__file__).resolve().parent

STATES = ("CANDIDATE", "VERIFIED", "MECHANIZED",
          "REWRITTEN", "DROPPED", "RETIRED")

DEFAULT_HALF_LIFE_DAYS = 30.0
RETIRE_BELOW = 0.15
DUPLICATE_COVERAGE_BAR = 0.7  # coverage >= this -> already known

# ---------------------------------------------------------------- byte integrity

_PIN_LINE_RE = re.compile(rb'(?m)^LAW_SHA256\s*=\s*"[0-9a-f]+"\s*(#.*)?$')


def _law_bytes():
    raw = Path(__file__).read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return _PIN_LINE_RE.sub(b'LAW_SHA256 = "PINNED"', raw)


def law_digest():
    return hashlib.sha256(_law_bytes()).hexdigest()


def check_integrity():
    """Refuse to run when the law's bytes were tampered with.

    Lawful re-pin after edits: HIVE_LAW_REPIN=1 ... --pin (explicit,
    auditable; the re-pinned hash is committed and reviewed)."""
    if os.environ.get("HIVE_LAW_REPIN") == "1":
        return "REPIN-MODE"
    if LAW_SHA256 == "0" * 64:
        return "UNPINNED (development)"
    if law_digest() != LAW_SHA256:
        raise SystemExit(
            "HIVE-LEARNING-LAW TAMPERED: byte integrity check failed — "
            "refusing to run")
    return "OK"


check_integrity()  # import-time: tamper -> refuse. No import, no law.


class HiveLearningError(Exception):
    """The machine refusing is the law working."""


class AdmissionRefused(HiveLearningError):
    pass


class ProofGateRefused(HiveLearningError):
    pass


class MechanizeRefused(HiveLearningError):
    pass


class SignalRejected(HiveLearningError):
    pass


# ---------------------------------------------------------------- stance gate
# B-48, self-contained: the law cannot depend on another file's unmerged
# function. Same rule as the retrieval-path guard in tools/smart_note_v2.py
# (_phrase_disavowed — the runtime twin); this is the canonical gate.

_STANCE_MARKERS = frozenset({
    "avoid", "reject", "abandon", "wrong", "incorrect", "bad",
    "harmful", "dangerous", "instead", "rather",
    "superseded", "deprecated", "obsolete", "failed", "failure",
})
_STANCE_NEGATIONS = frozenset({
    "do not", "does not", "did not", "will not", "can not", "cannot",
    "should not", "must not", "is not", "are not", "was not", "were not",
    "never", "not recommended", "not advisable",
})
_STANCE_CONTRACTIONS = {
    "don't": "do not", "doesn't": "does not", "didn't": "did not",
    "won't": "will not", "can't": "can not", "cannot": "can not",
    "shouldn't": "should not", "mustn't": "must not", "isn't": "is not",
    "aren't": "are not", "never": "never",
}
_STANCE_CLAUSE_RE = re.compile(
    r"[.!?;]+|\bbut\b|\bhowever\b|\balthough\b|\bthough\b|\bwhereas\b")


def _lesson_disavows_trigger(trigger, principle, enforcement):
    """True when the lesson's text disavows its own trigger phrase.

    Clause-bounded: disavowal in one clause doesn't taint a clean mention
    in another. A lesson that disavows its trigger cannot promote as
    guidance — B-48, structurally impossible."""
    text = f"{principle} {enforcement}".lower()
    for w, exp in _STANCE_CONTRACTIONS.items():
        text = re.sub(r"\b" + re.escape(w) + r"\b", exp, text)
    phrase = trigger.lower().split()
    n = len(phrase)
    if n == 0:
        return False
    for clause in _STANCE_CLAUSE_RE.split(text):
        toks = re.findall(r"[a-z0-9']+", clause)
        for i in range(len(toks) - n + 1):
            if toks[i:i + n] != phrase:
                continue
            lo, hi = max(0, i - 5), min(len(toks), i + n + 4)
            window = toks[lo:hi]
            if any(m in window for m in _STANCE_MARKERS):
                return True
            wtext = " ".join(window)
            if any(neg in wtext for neg in _STANCE_NEGATIONS):
                # "do not forget / hesitate" is encouragement, not disavowal
                if "do not forget" in wtext or "do not hesitate" in wtext:
                    continue
                return True
    return False

_TRIAGE_MOD = None


def _load_sibling(name):
    p = REPO_ROOT / "tools" / f"{name}.py"
    if not p.exists():
        return None
    spec = importlib.util.spec_from_file_location(name, p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _triage_mod():
    global _TRIAGE_MOD
    if _TRIAGE_MOD is None:
        _TRIAGE_MOD = _load_sibling("intake_triage")
    return _TRIAGE_MOD


# ---------------------------------------------------------------- surprise signal schema

SURPRISE_SIGNAL_FIELDS = (
    "signal_id", "emitted_at", "emitted_by",
    "observed", "expected", "decision_ref", "context",
)


def validate_surprise_signal(sig):
    """Machine contract for what workers emit at NOTICE. Fail closed."""
    if not isinstance(sig, dict):
        raise SignalRejected("signal must be a dict")
    for f in SURPRISE_SIGNAL_FIELDS:
        if f not in sig or sig[f] is None or (
                isinstance(sig[f], str) and not sig[f].strip()):
            raise SignalRejected(f"missing or empty field: {f}")
    if sig["observed"] == sig["expected"]:
        raise SignalRejected("observed == expected: not a surprise")
    try:
        datetime.fromisoformat(sig["emitted_at"])
    except (ValueError, TypeError):
        raise SignalRejected("emitted_at is not ISO-8601")
    return {f: sig[f] for f in SURPRISE_SIGNAL_FIELDS}


# ---------------------------------------------------------------- lifecycle

def _now_iso():
    return datetime.now(timezone.utc).isoformat()


def _log(lesson, event, detail=None):
    entry = {"at": _now_iso(), "event": event}
    if detail is not None:
        entry["detail"] = detail
    lesson["history"].append(entry)


def new_lesson(trigger, principle, enforcement="", evidence=None,
               falsifier="", provenance=None,
               half_life_days=DEFAULT_HALF_LIFE_DAYS):
    if not trigger or not trigger.strip():
        raise HiveLearningError("a lesson needs a trigger")
    if not principle or not principle.strip():
        raise HiveLearningError("a lesson needs a principle")
    now = _now_iso()
    return {
        "lesson_id": "hla-" + uuid.uuid4().hex[:12],
        "trigger": trigger.strip(),
        "principle": principle.strip(),
        "enforcement": (enforcement or "").strip(),
        "evidence": list(evidence or []),
        "falsifier": (falsifier or "").strip(),
        "provenance": dict(provenance or {}),
        "state": "CANDIDATE",
        "confidence": 0.5,
        "half_life_days": float(half_life_days),
        "admitted_at": now,
        "last_reinforced_at": now,
        "trial": None,
        "check_ref": None,
        "triage": None,
        "history": [{"at": now, "event": "created"}],
    }


def admit(lesson, existing_lesson_texts=()):
    triage_mod = _triage_mod()
    if triage_mod is None:
        raise AdmissionRefused("intake triage unavailable — fail closed")
    text = " ".join((lesson["trigger"], lesson["principle"],
                     lesson["enforcement"])).strip()
    verdict = triage_mod.triage(text, existing_lesson_texts)
    if verdict["verdict"] == "DROP":
        raise AdmissionRefused("intake refused: " + "; ".join(verdict["reasons"]))
    lesson["triage"] = verdict
    _log(lesson, "admitted", {"verdict": verdict["verdict"]})
    return lesson


def record_trial(lesson, control, treatment, delta, notes=""):
    lesson["trial"] = {
        "control": control, "treatment": treatment,
        "delta": delta, "notes": notes, "at": _now_iso(),
    }
    _log(lesson, "trial_recorded", {"delta": delta})
    return lesson


# ---------------------------------------------------------------- proof gate

PROOF_GATE_FIELDS = ("trigger", "principle", "enforcement", "evidence",
                     "falsifier", "provenance", "trial")

_NULL_FALSIFIERS = frozenset(
    {"nothing", "n/a", "na", "none", "unknown", "tbd", "todo", "nil"})


def _nonempty(v):
    if v is None:
        return False
    if isinstance(v, str):
        return bool(v.strip())
    if isinstance(v, (list, dict)):
        return len(v) > 0
    return True


def _check_seven_fields(lesson):
    missing = [f for f in PROOF_GATE_FIELDS if not _nonempty(lesson.get(f))]
    if missing:
        raise ProofGateRefused(f"missing or empty fields: {missing}")


def _check_falsifier(lesson):
    f = (lesson.get("falsifier") or "").strip()
    if len(f) < 12:
        raise ProofGateRefused("falsifier not specific (< 12 chars)")
    if f.lower() in _NULL_FALSIFIERS:
        raise ProofGateRefused(f"falsifier is a null claim: {f!r}")


def _check_duplicate(lesson, existing_lesson_texts):
    triage_mod = _triage_mod()
    if triage_mod is None:
        raise ProofGateRefused("duplicate check unavailable — fail closed")
    text = " ".join((lesson["trigger"], lesson["principle"])).strip()
    cov = triage_mod._max_coverage(text, existing_lesson_texts)
    if cov >= DUPLICATE_COVERAGE_BAR:
        raise ProofGateRefused(f"duplicate: coverage {cov:.2f} >= bar")


def _check_stance(lesson):
    """B-48 structurally impossible: a lesson that disavows its own trigger
    cannot promote as guidance."""
    if _lesson_disavows_trigger(lesson["trigger"],
                                lesson["principle"],
                                lesson["enforcement"]):
        raise ProofGateRefused(
            "B-48: lesson disavows its own trigger — cannot promote as guidance")


def _positive_delta(delta):
    if isinstance(delta, bool):
        return delta
    if isinstance(delta, (int, float)) and not isinstance(delta, bool):
        return delta > 0
    return False


def _check_trial(lesson):
    t = lesson.get("trial")
    if not isinstance(t, dict):
        raise ProofGateRefused("trial missing")
    if not _positive_delta(t.get("delta")):
        raise ProofGateRefused(f"no behavioral delta ({t.get('delta')!r})")


def proof_gate(lesson, existing_lesson_texts=()):
    """All checks run; every failure is named; any failure refuses."""
    failures = []
    for name, fn in (
            ("seven_fields", _check_seven_fields),
            ("falsifier", _check_falsifier),
            ("trial", _check_trial)):
        try:
            fn(lesson)
        except ProofGateRefused as e:
            failures.append(f"{name}: {e}")
    try:
        _check_duplicate(lesson, existing_lesson_texts)
    except ProofGateRefused as e:
        failures.append(f"duplicate: {e}")
    try:
        _check_stance(lesson)
    except ProofGateRefused as e:
        failures.append(f"stance: {e}")
    if failures:
        raise ProofGateRefused("; ".join(failures))
    return True


def promote(lesson, existing_lesson_texts=()):
    if lesson["state"] != "CANDIDATE":
        raise ProofGateRefused(f"only CANDIDATE promotes (is {lesson['state']})")
    proof_gate(lesson, existing_lesson_texts)
    lesson["state"] = "VERIFIED"
    lesson["confidence"] = min(1.0, lesson["confidence"] + 0.3)
    reinforce(lesson)
    _log(lesson, "promoted")
    return lesson


def mechanize(lesson, check_ref):
    if lesson["state"] != "VERIFIED":
        raise MechanizeRefused(f"only VERIFIED mechanizes (is {lesson['state']})")
    if not check_ref:
        raise MechanizeRefused("mechanize needs a check reference")
    lesson["check_ref"] = check_ref
    lesson["state"] = "MECHANIZED"
    lesson["confidence"] = 1.0
    _log(lesson, "mechanized", {"check_ref": check_ref})
    return lesson


def reinforce(lesson):
    lesson["last_reinforced_at"] = _now_iso()
    if lesson["state"] in ("VERIFIED", "MECHANIZED"):
        lesson["confidence"] = min(1.0, lesson["confidence"] + 0.1)
    _log(lesson, "reinforced")
    return lesson


def rewrite(lesson, new_principle, new_trigger=None, new_enforcement=None,
            new_falsifier=None):
    lesson["state"] = "REWRITTEN"
    _log(lesson, "rewritten")
    child = new_lesson(
        new_trigger or lesson["trigger"], new_principle,
        new_enforcement if new_enforcement is not None else lesson["enforcement"],
        evidence=list(lesson["evidence"]),
        falsifier=new_falsifier if new_falsifier is not None else lesson["falsifier"],
        provenance={**lesson["provenance"], "rewrites": lesson["lesson_id"]},
        half_life_days=lesson["half_life_days"],
    )
    _log(child, "created_as_rewrite", {"of": lesson["lesson_id"]})
    return child


def drop(lesson, reason):
    lesson["state"] = "DROPPED"
    _log(lesson, "dropped", {"reason": reason})
    return lesson


def confidence(lesson, now_iso=None):
    if lesson["state"] == "MECHANIZED":
        return 1.0
    hl = lesson["half_life_days"]
    if hl <= 0:
        return lesson["confidence"]
    now = datetime.fromisoformat(now_iso) if now_iso else datetime.now(timezone.utc)
    last = datetime.fromisoformat(lesson["last_reinforced_at"])
    age_days = max(0.0, (now - last).total_seconds() / 86400.0)
    return round(lesson["confidence"] * 0.5 ** (age_days / hl), 4)


def sweep(lessons, now_iso=None, retire_below=RETIRE_BELOW):
    retired = []
    for lesson in lessons:
        if lesson["state"] in ("DROPPED", "RETIRED", "REWRITTEN", "MECHANIZED"):
            continue
        if confidence(lesson, now_iso) < retire_below:
            lesson["state"] = "RETIRED"
            _log(lesson, "retired_by_decay")
            retired.append(lesson)
    return retired


def save(path, lessons):
    Path(path).write_text(json.dumps(lessons, indent=2), encoding="utf-8")


def load(path):
    p = Path(path)
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else []


# ---------------------------------------------------------------- adoption checker

def check_adoption(lesson, pytest_timeout=120):
    """Automates tonight's manual verification: is the enforcement REAL?

    A MECHANIZED lesson claims its behavior is machinery. ADOPTED iff the
    check_ref exists — and when it names a test (path::test), that test
    PASSES right now. Anything else is NOT_ADOPTED. Fail closed."""
    if lesson["state"] != "MECHANIZED":
        return ("NOT_ADOPTED", [f"state is {lesson['state']}, not MECHANIZED"])
    ref = lesson.get("check_ref")
    if not ref:
        return ("NOT_ADOPTED", ["no check_ref"])
    if "::" in ref:
        path, _, test = ref.partition("::")
        if not test:
            return ("NOT_ADOPTED", [f"malformed check_ref: {ref}"])
        try:
            r = subprocess.run(
                [sys.executable, "-m", "pytest", f"{path}::{test}", "-q"],
                capture_output=True, text=True, timeout=pytest_timeout,
                cwd=str(REPO_ROOT))
        except Exception as e:  # timeout, missing pytest, ... -> fail closed
            return ("NOT_ADOPTED", [f"check could not run: {e}"])
        if r.returncode == 0:
            return ("ADOPTED", [f"check passed: {ref}"])
        tail = (r.stdout + r.stderr).strip().splitlines()[-3:]
        return ("NOT_ADOPTED", [f"check FAILED: {ref}"] + tail)
    p = Path(ref)
    if not p.is_absolute():
        p = REPO_ROOT / p
    if p.exists():
        return ("ADOPTED", [f"check_ref present: {ref}"])
    return ("NOT_ADOPTED", [f"check_ref missing: {ref}"])


# ---------------------------------------------------------------- velocity tracker

def _event_at(lesson, event):
    for h in reversed(lesson.get("history", [])):
        if h.get("event") == event:
            return datetime.fromisoformat(h["at"])
    return None


def learning_velocity(lessons, window_days=7.0, min_adoptions_per_day=1.0,
                      now_iso=None):
    """Learning rate from lesson history. DEGRADED when adoption drops."""
    now = datetime.fromisoformat(now_iso) if now_iso else datetime.now(timezone.utc)
    cutoff = now.timestamp() - window_days * 86400.0
    promotions = sum(1 for l in lessons
                     if (_event_at(l, "promoted") or datetime.min.replace(tzinfo=timezone.utc)).timestamp() >= cutoff)
    adoptions = sum(1 for l in lessons
                    if (_event_at(l, "mechanized") or datetime.min.replace(tzinfo=timezone.utc)).timestamp() >= cutoff)
    latencies = []
    for l in lessons:
        pa, ad = _event_at(l, "promoted"), _event_at(l, "admitted")
        if pa and ad and pa.timestamp() >= cutoff:
            latencies.append((pa - ad).total_seconds() / 3600.0)
    latencies.sort()
    median_lat = latencies[len(latencies) // 2] if latencies else None
    adoptions_per_day = adoptions / window_days
    reasons = []
    if adoptions_per_day < min_adoptions_per_day:
        reasons.append(f"adoptions/day {adoptions_per_day:.2f} < bar {min_adoptions_per_day}")
    return {
        "window_days": window_days,
        "promotions": promotions,
        "promotions_per_day": round(promotions / window_days, 2),
        "adoptions": adoptions,
        "adoptions_per_day": round(adoptions_per_day, 2),
        "median_admit_to_promote_hours": round(median_lat, 2) if median_lat is not None else None,
        "status": "DEGRADED" if reasons else "OK",
        "reasons": reasons,
    }


# ---------------------------------------------------------------- master entry

def check_hive_learning_law():
    """Master entry, contract pattern: integrity + live self-test."""
    integrity = check_integrity()
    # Self-test: the gate must refuse an empty lesson and admit a full one.
    try:
        proof_gate(new_lesson("t", "p"))
        selftest = "BROKEN: gate admitted an empty lesson"
    except ProofGateRefused:
        selftest = "OK: gate refuses incomplete lessons"
    return {"law": "hive-learning-law", "version": LAW_VERSION,
            "sha256": law_digest(), "integrity": integrity,
            "proof_gate_selftest": selftest}


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="The Hive Learning Law.")
    ap.add_argument("--pin", action="store_true",
                    help="print the blessed SHA256 for LAW_SHA256")
    ap.add_argument("--check", action="store_true",
                    help="integrity + self-test")
    ap.add_argument("--sweep", metavar="STORE",
                    help="retire decayed lessons in a store file")
    ap.add_argument("--velocity", metavar="STORE",
                    help="report learning velocity for a store file")
    args = ap.parse_args()
    if args.pin:
        print(law_digest())
    elif args.sweep:
        lessons = load(args.sweep)
        retired = sweep(lessons)
        save(args.sweep, lessons)
        print(json.dumps({"swept": len(lessons), "retired": len(retired)}, indent=2))
    elif args.velocity:
        print(json.dumps(learning_velocity(load(args.velocity)), indent=2))
    else:  # --check or default
        print(json.dumps(check_hive_learning_law(), indent=2))
