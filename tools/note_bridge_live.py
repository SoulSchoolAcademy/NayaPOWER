#!/usr/bin/env python3
"""
Note-to-Behavior Bridge — live corpus wiring (v2).

Replaces the prototype's hardcoded in-memory corpus with the LIVE Smart Note
corpus at BRAIN/05-MEMORY/SMART-NOTES/. Retrieval runs over every note parsed
from disk; machine-checkable constraints come from an explicitly curated map
(CURATED_CONSTRAINTS) covering notes whose operational rules are crisp enough
to falsify. Curated != comprehensive: the loader reports exactly how many
notes carry constraints and how many do not.

Pipeline (same as prototype):
    ACTION PROPOSED
        -> retrieve_for_action() : keyword match over LIVE notes
        -> extract_constraints()  : curated machine-readable rules
        -> gate_action()          : ALLOW / MODIFY / BLOCK
        -> record_outcome()       : log note -> retrieval -> decision -> outcome
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from note_bridge import (
    SmartNote,
    retrieve_for_action,
    extract_constraints,
    gate_action,
    record_outcome,
    get_outcome_log,
    clear_outcome_log,
)

DEFAULT_CORPUS_ROOT = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "BRAIN", "05-MEMORY", "SMART-NOTES",
)

_STOPWORDS = frozenset("""
a an the and or of to in on for with is are was were be been being it its
this that these those as at by from into through over under up down out off
not no nor can will just don should now then than so such very more most
other some any all each every own same he she they we you i me him her them
us my your his their our what which who whom whose when where why how
do does did doing have has had having not but if because until while
against between into through during before after above below
""".split())


# ============================================================================
# CURATED CONSTRAINTS — hand-derived, explicitly marked.
# Only notes verified to exist on disk are listed. Each entry was read by a
# human (Naya 4) and reduced to a machine-checkable rule. This map is the
# honest boundary: retrieval covers the whole corpus; gating covers these.
# ============================================================================

CURATED_CONSTRAINTS = {
    "SN-003": [
        {"pattern": r"\b(create|new|separate|parallel|second|another)\b.*\b(brain|store|substrate|pipeline|database|memory)\b",
         "action": "BLOCK",
         "reason": "SN-003: Do not create parallel brains/stores. Use the existing canonical substrate.",
         "severity": "high"},
    ],
    "SN-0408": [
        {"pattern": r"\b(delete|remove|cleanup|trash|drop|purge)\b",
         "action": "BLOCK",
         "reason": "SN-0408: Never delete until fully understood. Deletion requires explicit human director approval.",
         "severity": "high"},
    ],
    "SN-0460": [
        {"pattern": r"(candidat\w*|test\w*)\s*(-+>|\bto\b)\s*ratified",
         "action": "BLOCK",
         "reason": "SN-0460: RATIFIED may only be entered from VERIFIED. Direct CANDIDATE/TESTING -> RATIFIED jumps are rejected.",
         "severity": "high"},
    ],
}


# ============================================================================
# LIVE CORPUS LOADER
# ============================================================================

def _extract_sn_id(path: str, text: str) -> str:
    # 1. Header table: | Smart Note | SN-XXXX |
    m = re.search(r"\|\s*Smart Note\s*\|\s*([A-Za-z0-9\-]+)\s*\|", text)
    if m:
        return m.group(1).strip().upper()
    # 2. Directory name: .../SN-0460/... or .../SN-NET-POWER-MAGIC-001/...
    for part in path.split(os.sep):
        if re.match(r"(?i)^SN-[A-Za-z0-9\-]+$", part):
            return part.upper()
    # 3. Filename: IB-SMART-NOTE-20261006-sn0460-...
    m = re.search(r"[Ss][Nn][-_]?([A-Za-z0-9\-]+)", os.path.basename(path))
    if m:
        return ("SN-" + m.group(1)).upper().replace("_", "-")
    return "SN-UNKNOWN"


def _extract_section(text: str, heading: str) -> str:
    m = re.search(
        r"^##\s*" + re.escape(heading) + r"\s*$\n(.*?)(?=^##\s|\Z)",
        text, re.M | re.S,
    )
    return m.group(1).strip() if m else ""


def _extract_title(text: str, path: str) -> str:
    m = re.search(r"^#\s+(.+)$", text, re.M)
    if m:
        t = m.group(1).strip()
        # Strip the IB- prefix for readability
        t = re.sub(r"^IB-SMART-NOTE-\d+-", "", t)
        return t.replace("-", " ").strip() or t
    base = os.path.basename(path)
    return re.sub(r"^IB-SMART-NOTE-\d+-", "", base).replace(".md", "").replace("-", " ")


def _extract_keywords(title: str, nutshell: str, body: str, limit: int = 40) -> list:
    text = f"{title} {nutshell} {body[:2000]}".lower()
    words = re.findall(r"[a-z][a-z0-9\-]{2,}", text)
    seen = []
    for w in words:
        w = w.strip("-")
        if w and w not in _STOPWORDS and w not in seen:
            seen.append(w)
        if len(seen) >= limit:
            break
    return seen


def parse_note_file(path: str) -> dict:
    """Parse one live Smart Note file. Never guesses; returns None on failure."""
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            text = f.read()
    except OSError:
        return None
    if not text.strip():
        return None
    sn_id = _extract_sn_id(path, text)
    title = _extract_title(text, path)
    nutshell = _extract_section(text, "IN A NUTSHELL")
    if not nutshell:
        # Fallback: first non-header paragraph
        paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
        for p in paras:
            if not p.startswith("#") and not p.startswith("|") and len(p) > 40:
                nutshell = p[:600]
                break
    # Category from path: .../SMART-NOTES/2026/10/06/<CATEGORY...>/SN-XXXX/...
    parts = path.split(os.sep)
    try:
        i = parts.index("SMART-NOTES")
        # skip year/month/day numeric parts
        cats = [p for p in parts[i + 1:] if p and not re.match(r"^\d{4}$|^\d{2}$", p)
                and not p.startswith("SN-") and not p.endswith(".md")]
        category = "/".join(cats[:3]) if cats else "UNCATEGORIZED"
    except ValueError:
        category = "UNCATEGORIZED"
    m = re.search(r"\|\s*Truth state\s*\|\s*([A-Za-z]+)\s*\|", text)
    truth_state = m.group(1).upper() if m else "UNKNOWN"
    keywords = _extract_keywords(title, nutshell, text)
    return {
        "id": sn_id,
        "title": title,
        "keywords": keywords,
        "category": category,
        "nutshell": nutshell[:800],
        "naya_note": nutshell[:800],
        "truth_state": truth_state,
        "path": path,
    }


def load_live_corpus(root: str = None) -> tuple:
    """
    Load every parseable Smart Note from the live corpus.
    Returns (notes, report) where report = {total_files, parsed, failed,
    with_constraints, constraint_ids}.
    """
    root = os.path.abspath(root or DEFAULT_CORPUS_ROOT)
    notes = []
    failed = []
    files = []
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            if fn.startswith("IB-SMART-NOTE-") and fn.endswith(".md"):
                files.append(os.path.join(dirpath, fn))
    for fp in sorted(files):
        parsed = parse_note_file(fp)
        if parsed is None:
            failed.append(fp)
            continue
        constraints = CURATED_CONSTRAINTS.get(parsed["id"], [])
        notes.append(SmartNote(
            id=parsed["id"],
            title=parsed["title"],
            keywords=parsed["keywords"],
            category=parsed["category"],
            nutshell=parsed["nutshell"],
            naya_note=parsed["naya_note"],
            constraints=[dict(c, curated=True) for c in constraints],
        ))
    with_c = [n.id for n in notes if n.constraints]
    report = {
        "total_files": len(files),
        "parsed": len(notes),
        "failed": len(failed),
        "failed_paths": failed,
        "with_constraints": len(with_c),
        "constraint_ids": sorted(set(with_c)),
        "corpus_root": root,
    }
    return notes, report


def build_live_corpus(root: str = None):
    """Drop-in replacement for the prototype's build_corpus()."""
    notes, _ = load_live_corpus(root)
    return notes


def gate_action_live(action_description: str, root: str = None):
    """Gate an action against the LIVE corpus. Returns (decision, report)."""
    notes, report = load_live_corpus(root)
    decision = gate_action(action_description, notes)
    return decision, report


if __name__ == "__main__":
    import json
    action = " ".join(sys.argv[1:]) or "Create a new separate brain store for this project"
    decision, report = gate_action_live(action)
    print(json.dumps({
        "verdict": decision.verdict,
        "notes_retrieved": decision.notes_retrieved,
        "violations": decision.violations,
        "guidance": decision.guidance,
        "explanation": decision.explanation,
        "corpus_report": {k: v for k, v in report.items() if k != "failed_paths"},
    }, indent=2))
