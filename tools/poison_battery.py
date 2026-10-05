"""Poison classes 5-7: provenance, lesson content, authority inheritance.

Extends the truth-state closure (PR #1468) to the remaining semantic poison
classes. Same principle as before: STRUCTURAL checks verify shape; these verify
MEANING. A capture that is perfectly well-formed can still be lying.

THE THREE CLASSES
-----------------
P5 FABRICATED PROVENANCE
    A capture may assert a source it does not have. Measured on current main:
    the `source` block carries `source_reference`, `source_type`,
    `source_hash_prefix`, and -- most dangerous -- `human_directive`. Any of
    these can be written by hand. Nothing checks that the referenced source
    resolves, or that a claimed director directive was actually issued.

P6 POISONED LESSON CONTENT
    `intelligence.learning_lesson` is the text a successor is meant to learn
    from. It is the highest-value injection target in the whole system: a
    capture can carry impeccable provenance and a malicious lesson. Shape
    checks cannot see it. The lesson must be treated as untrusted content that
    is NEVER an instruction, and must not smuggle authority language.

P7 UNAUTHORIZED AUTHORITY INHERITANCE
    `machine_view.authority_inheritance` means "learning this grants power."
    Measured on current main: 0 of 23 captures set it true. That is the correct
    state and this guard exists to keep it that way -- because if it is ever
    true it must be backed by recorded promotion authority, or a note becomes a
    backdoor into authority.

DESIGN NOTE
-----------
These detectors REPORT. They do not mutate and they do not delete. A capture is
evidence; destroying evidence is not a security control, it is data loss.
Containment is a separate, deliberate act.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

# Language that indicates a lesson is trying to INSTRUCT rather than inform.
# Deliberately broad: a false positive costs a human review, a false negative
# ships an injection into every successor that retrieves it.
INJECTION_PATTERNS = (
    r"ignore (?:all |any )?(?:previous|prior|above)",
    r"disregard (?:all |any )?(?:previous|prior|above)",
    r"you (?:must|should|will) (?:always|now) (?:obey|comply|defer)",
    r"override (?:the )?(?:law|authority|governance|constitution)",
    r"grant (?:yourself|me) (?:authority|admin|root)",
    r"mark (?:this|yourself) as (?:verified|ratified|approved)",
    r"treat (?:this|yourself) as (?:authorized|ratified|verified)",
    r"do not (?:record|log|report|verify)",
)

_COMPILED = re.compile("|".join(INJECTION_PATTERNS), re.IGNORECASE)

# Claims of authority inside a capture's source block.
DIRECTOR_CLAIM_KEYS = ("human_directive", "human_director_authorized_publication")


@dataclass
class PoisonFinding:
    smart_note_id: str
    path: str
    code: str
    detail: str
    severity: str = "HIGH"

    def __str__(self) -> str:  # pragma: no cover - display
        return f"[{self.code}] {self.smart_note_id}: {self.detail}"


@dataclass
class PoisonReport:
    findings: list[PoisonFinding] = field(default_factory=list)

    def codes(self) -> set[str]:
        return {f.code for f in self.findings}

    def __len__(self) -> int:  # pragma: no cover
        return len(self.findings)

    def __bool__(self) -> bool:  # pragma: no cover
        return bool(self.findings)


def check_capture_poison(capture_path: str | Path) -> PoisonReport:
    """Run all three semantic poison classes against one capture. Never raises."""
    p = Path(capture_path)
    rep = PoisonReport()
    try:
        doc = json.loads(p.read_bytes().decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        rep.findings.append(PoisonFinding(
            "(no-id)", str(p), "P0_UNREADABLE", f"not parseable: {exc}"))
        return rep
    if not isinstance(doc, dict):
        rep.findings.append(PoisonFinding(
            "(no-id)", str(p), "P0_UNREADABLE", "capture is not an object"))
        return rep

    sid = str(doc.get("smart_note_id") or "(no smart_note_id)")
    intel = doc.get("intelligence") or {}
    if not isinstance(intel, dict):
        return rep
    mv = intel.get("machine_view") or {}
    src = doc.get("source") or {}
    if not isinstance(mv, dict) or not isinstance(src, dict):
        return rep

    # ---- P5 FABRICATED PROVENANCE -------------------------------------
    # MEASURED on current main: the governance key
    # `raw_source_separate_from_distillation` lives in
    # `intelligence.machine_view` for 19 captures, in `source` for 0, and in
    # BOTH for 1. `intelligence.machine_view` is therefore authoritative --
    # it is also where the SN-002 conformance gate reads it.
    #
    # An earlier version of this check read `source` and produced 19 false
    # positives, i.e. I built the same two-sources-of-truth bug I have been
    # warning about, on the same day I fixed one. Reading the authoritative
    # location; DISAGREEMENT is now itself reported rather than silently
    # resolved, because a key that disagrees between two places is a finding.
    key_mv = mv.get("raw_source_separate_from_distillation")
    key_src = src.get("raw_source_separate_from_distillation")
    if key_mv is not True:
        rep.findings.append(PoisonFinding(
            sid, str(p), "P5_RAW_SOURCE_NOT_SEPARATED",
            "intelligence.machine_view.raw_source_separate_from_distillation "
            "is not boolean true"))
    if key_src is not None and key_src != key_mv:
        rep.findings.append(PoisonFinding(
            sid, str(p), "P5_KEY_LOCATION_DISAGREEMENT",
            f"raw_source_separate_from_distillation disagrees between "
            f"machine_view ({key_mv!r}) and source ({key_src!r})",
            severity="MEDIUM"))
    if not (src.get("source_reference") or src.get("raw_source")):
        rep.findings.append(PoisonFinding(
            sid, str(p), "P5_PROVENANCE_MISSING",
            "no source_reference and no raw_source: provenance is asserted nowhere"))
    for key in DIRECTOR_CLAIM_KEYS:
        if src.get(key):
            rep.findings.append(PoisonFinding(
                sid, str(p), "P5_DIRECTOR_CLAIM_UNVERIFIED",
                f"source asserts {key!r}; a self-asserted director claim is not "
                "evidence of director authority", severity="HIGH"))
    # ---- P6 POISONED LESSON CONTENT ------------------------------------
    lesson = intel.get("learning_lesson")
    if isinstance(lesson, str) and lesson.strip():
        m = _COMPILED.search(lesson)
        if m:
            rep.findings.append(PoisonFinding(
                sid, str(p), "P6_LESSON_INJECTION",
                f"learning_lesson contains instruction-like language: {m.group(0)!r}. "
                "A lesson informs; it must never instruct."))

    # ---- P7 UNAUTHORIZED AUTHORITY INHERITANCE --------------------------
    if mv.get("authority_inheritance") is True:
        rep.findings.append(PoisonFinding(
            sid, str(p), "P7_AUTHORITY_INHERITANCE_UNAUTHORIZED",
            "authority_inheritance is true with no recorded promotion authority; "
            "learning this note would grant power"))

    return rep


def check_dir_poison(directory: str | Path) -> PoisonReport:
    """Run every capture in a directory. Sorted for deterministic output."""
    out = PoisonReport()
    for f in sorted(Path(directory).glob("SMART-NOTE-*.json")):
        out.findings.extend(check_capture_poison(f).findings)
    return out