#!/usr/bin/env python3
"""Completeness Gate — Gate 3 of 7 (Operating Code V2).

Every Smart Note PR is checked for form-completeness, canonical placement,
and ownership. Missing applicable form or stranded placement = FAIL (blocked);
unowned or code-form gap = flagged (warning).

THE FOUR FORMS, mapped to how Smart Notes actually exist on main (2026-10-10):
notes are single-file Intelligent-Block projections
(`IB-SMART-NOTE-<date>-<sn>-<slug>.md`); the four forms live as SECTIONS,
not sibling files (606 notes surveyed: 598/606 carry all sections).

  human   -> `HUMAN NOTE` section with substantive prose
  ai      -> `NAYA NOTE` section with substantive prose
  machine -> `MACHINE NOTE` section containing a parseable JSON payload
  code    -> the note's SN id is referenced from an enforcement surface
             (tools/, kernel/, tests/, ...). "Where applicable": a missing
             code reference is a WARNING, never a block.

CANONICAL PLACEMENT: note files live under
  BRAIN/05-MEMORY/SMART-NOTES/<YYYY>/<MM>/<DD>/...
with a well-formed date partition. A note-named file anywhere else is
"stranded" = FAIL, except explicit allowlist locations (trial/evidence
corpora, capture staging).

OWNER: an identifiable owner — an explicit `**Owner:**` / `| Owner |` field,
or a seat signature (Naya 1-5, Coda 1-4, Codex, Shawn / Human Director) in the
header/provenance block. Unowned = flagged (warning), never a block.

Relationship to existing seams (surveyed 2026-10-10 — no duplication):
  - tools/note_enforcement_check.py REPORTS enforcement impact per commit and
    explicitly never fails. Opposite contract (report vs block); not extended.
  - tools/doc_completeness_check.py checks the .ai/.human/.machine triple for
    governance laws (BRAIN/01-GOVERNANCE) and the .naya/capture JSON corpus.
    Different corpus and file pattern; this gate owns the SMART-NOTES tree.

Usage:
  python3 tools/completeness_gate.py [--changed-only] [--strict] [--json]
                                     [--path NOTE.md] [--root DIR]
  --changed-only : check only note files changed vs origin/main (the CI mode;
                   pre-existing debt is reported by full scans, not blocking)
  --strict       : warnings become failures
  --json         : machine-readable output
  --path         : check one note file instead of scanning
  --root         : repo root override (tests use a fixture tree)

Exit codes: 0 = pass (warnings allowed); 1 = fail.
Stdlib only.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    # One canonical definition of "what a Smart Note file looks like".
    from note_enforcement_check import NOTE_MARKERS
except Exception:  # standalone copy; keep the shared convention
    NOTE_MARKERS = ("SMART-NOTE-", "SMART_NOTE_", "IB-SMART-NOTE-")

ROOT = Path(__file__).resolve().parents[1]
NOTES_ROOT = ROOT / "BRAIN" / "05-MEMORY" / "SMART-NOTES"

# Note-named files may legitimately live here without being "stranded".
ALLOWLIST_PREFIXES = ("evidence/", ".naya/capture/")

# Enforcement surfaces consulted for the code form ("where applicable").
CODE_DIRS = (
    "tools/",
    "kernel/",
    "tests/",
    "orchestrator/",
    "supabase/functions/",
    ".github/workflows/",
    "BRAIN/01-GOVERNANCE/",
)

MIN_PROSE = 50  # same bar as tools/doc_completeness_check.py

SECTION_RES = {
    # `## HUMAN NOTE`, `## 🩷 HUMAN NOTE`, `## HUMAN NOTE — ...`
    "human": re.compile(r"^#+\s*[^\w\n]*HUMAN NOTE\b", re.M),
    "ai": re.compile(r"^#+\s*[^\w\n]*NAYA NOTE\b", re.M),
    "machine": re.compile(r"^#+\s*[^\w\n]*MACHINE NOTE\b", re.M),
}

OWNER_FIELD_RES = (
    re.compile(r"^\s*(?:\*\*Owner:\*\*|\bOwner:)\s*(.+?)\s*$", re.M),
    re.compile(r"^\s*\|\s*Owner\s*\|\s*(.+?)\s*\|", re.M),
)
SEAT_RE = re.compile(
    r"\b(?:Naya|Coda)\s*[ _-]?[1-5]\b|\bCodex\b|\bShawn(?:\s+Vibert)?\b"
    r"|\bHuman Director\b",
    re.I,
)
PROVENANCE_LINE_RE = re.compile(
    r"(?i)^\s*(?:\*\*)?(Provenance|Authority|Source|Captured by|Author"
    r"|Relayed by)(?:\*\*)?\s*[:|]"
)


def is_note_file(path: Path) -> bool:
    return path.suffix == ".md" and any(m in path.name for m in NOTE_MARKERS)


def norm_id(raw: str) -> str:
    return re.sub(r"[^A-Z0-9]", "", raw.upper())


def extract_note_id(path: Path) -> str | None:
    """SN id from the SN-* parent dir, else from the filename. Normalized."""
    m = re.match(r"(?i)^SN-(.+)$", path.parent.name)
    if m:
        return norm_id("SN-" + m.group(1))
    return filename_note_id(path)


def filename_note_id(path: Path) -> str | None:
    """SN id parsed from the filename alone (for dir/file agreement checks).

    Only the numeric token right after the `sn` marker counts
    (e.g. `...-sn0282-do-it-now-doctrine.md` -> SN0282); the trailing slug
    is not part of the id. Filenames without an sn token (hash-style)
    defer to the SN-* parent dir.
    """
    m = re.search(r"(?i)(?:^|[-_])sn[-_]?([0-9]{2,6})(?![0-9])", path.name)
    if m:
        return norm_id("SN-" + m.group(1))
    return None


def section_body(text: str, kind: str) -> str | None:
    rx = SECTION_RES[kind]
    m = rx.search(text)
    if not m:
        return None
    rest = text[m.end():]
    # Form sections are ##-level; ### subsections belong to the form.
    nxt = re.search(r"^#{1,2}[ \t]", rest, re.M)
    return rest[: nxt.start()] if nxt else rest


def substantive(body: str | None) -> bool:
    if not body:
        return False
    return len(re.sub(r"\s+", " ", body).strip()) >= MIN_PROSE


def machine_payload_ok(body: str | None) -> tuple[bool, str]:
    """The machine form is usable only if its JSON payload parses."""
    if body is None:
        return False, "MACHINE NOTE section missing"
    idx = body.find("{")
    if idx < 0:
        return False, "MACHINE NOTE has no JSON payload"
    try:
        obj, _ = json.JSONDecoder().raw_decode(body, idx)
    except Exception as e:
        return False, f"MACHINE NOTE JSON unparseable: {e}"
    if not isinstance(obj, dict):
        return False, "MACHINE NOTE payload is not a JSON object"
    return True, ""


def find_owner(text: str) -> tuple[str | None, str]:
    """Returns (owner_label, evidence). None label = unowned."""
    for rx in OWNER_FIELD_RES:
        m = rx.search(text)
        if m and m.group(1).strip():
            return m.group(1).strip()[:80], "explicit Owner field"
    header = "\n".join(text.splitlines()[:40])
    prov = "\n".join(
        ln for ln in text.splitlines() if PROVENANCE_LINE_RE.match(ln)
    )
    m = SEAT_RE.search(header) or SEAT_RE.search(prov)
    if m:
        return m.group(0).strip(), "seat signature in header/provenance"
    return None, ""


def check_forms(path: Path, text: str) -> tuple[list[str], list[str], dict]:
    failures, warnings, forms = [], [], {}
    human = section_body(text, "human")
    if human is None:
        failures.append("human form missing (no HUMAN NOTE section)")
        forms["human"] = False
    elif not substantive(human):
        failures.append("human form not substantive (< %d chars prose)" % MIN_PROSE)
        forms["human"] = False
    else:
        forms["human"] = True

    ai = section_body(text, "ai")
    if ai is None:
        failures.append("AI form missing (no NAYA NOTE section)")
        forms["ai"] = False
    elif not substantive(ai):
        failures.append("AI form not substantive (< %d chars prose)" % MIN_PROSE)
        forms["ai"] = False
    else:
        forms["ai"] = True

    ok, why = machine_payload_ok(section_body(text, "machine"))
    forms["machine"] = ok
    if not ok:
        failures.append("machine form missing: " + why)

    forms["code"] = None  # filled by run() once code refs are known
    return failures, warnings, forms


def check_placement(rel: str, path: Path) -> tuple[list[str], list[str]]:
    """rel: posix path relative to repo root. Returns (failures, warnings)."""
    failures, warnings = [], []
    if rel.startswith(ALLOWLIST_PREFIXES):
        return failures, warnings  # legitimate non-canonical copy
    try:
        tree_rel = Path(rel).relative_to(NOTES_ROOT.relative_to(ROOT).as_posix())
    except ValueError:
        failures.append(
            "stranded: note file outside BRAIN/05-MEMORY/SMART-NOTES/ "
            "(canonical placement required)"
        )
        return failures, warnings
    parts = tree_rel.parts
    if len(parts) < 4:
        failures.append(f"path too shallow for date partition: {rel}")
        return failures, warnings
    y, mo, d = parts[0], parts[1], parts[2]
    date_ok = (
        re.fullmatch(r"(19|20)\d{2}", y) is not None
        and re.fullmatch(r"(0[1-9]|1[0-2])", mo) is not None
        and re.fullmatch(r"(0[1-9]|[12][0-9]|3[01])", d) is not None
    )
    if not date_ok:
        failures.append(f"malformed date partition <YYYY>/<MM>/<DD>: {y}/{mo}/{d}")
    # SN-* dir vs filename id agreement is hygiene, not placement: warn only.
    dir_id = norm_id(path.parent.name) if path.parent.name.upper().startswith("SN") else None
    file_id = filename_note_id(path)
    if dir_id and file_id and dir_id != file_id:
        warnings.append(
            f"SN dir/file id mismatch: dir={path.parent.name} file-id={file_id}"
        )
    return failures, warnings


def collect_code_refs(root: Path) -> set[str]:
    """SN ids referenced from enforcement surfaces (one grep, cached per run)."""
    dirs = [str(root / d) for d in CODE_DIRS if (root / d).exists()]
    if not dirs:
        return set()
    try:
        out = subprocess.run(
            ["grep", "-rhoiE", "SN-?[A-Za-z0-9-]{2,40}", *dirs],
            capture_output=True,
            text=True,
            timeout=120,
        )
    except Exception:
        return set()
    return {norm_id(tok) for tok in out.stdout.split() if norm_id(tok).startswith("SN")}


def check_note(path: Path, root: Path, code_refs: set[str]) -> dict:
    rel = path.relative_to(root).as_posix()
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        return {"note": rel, "failures": [f"unreadable: {e}"], "warnings": [],
                "owner": None, "forms": {}}
    failures, warnings, forms = check_forms(path, text)
    pf, pw = check_placement(rel, path)
    failures.extend(pf)
    warnings.extend(pw)

    owner, evidence = find_owner(text)
    if owner is None:
        warnings.append("unowned: no identifiable owner (author seat)")
    forms["code"] = None
    note_id = extract_note_id(path)
    if note_id is not None:
        if note_id in code_refs:
            forms["code"] = True
        else:
            forms["code"] = False
            warnings.append(
                f"code form gap: no enforcement-surface reference to {note_id} "
                "(where applicable — warning only)"
            )
    return {"note": rel, "failures": failures, "warnings": warnings,
            "owner": {"id": owner, "evidence": evidence} if owner else None,
            "forms": forms}


def changed_note_files(root: Path) -> list[Path]:
    out = subprocess.run(
        ["git", "diff", "--name-only", "origin/main...HEAD"],
        capture_output=True,
        text=True,
        cwd=root,
    )
    files = []
    for line in out.stdout.splitlines():
        p = root / line.strip()
        if p.is_file() and is_note_file(p):
            files.append(p)
    return sorted(files)


def run(root: Path, paths: list[Path] | None = None) -> dict:
    if paths is None:
        notes_root = root / "BRAIN" / "05-MEMORY" / "SMART-NOTES"
        if notes_root.exists():
            paths = sorted(p for p in notes_root.rglob("*.md") if is_note_file(p))
        else:
            # fixture trees / ad-hoc roots: any note-named .md counts
            paths = sorted(p for p in root.rglob("*.md") if is_note_file(p))
    code_refs = collect_code_refs(root)
    notes = [check_note(p, root, code_refs) for p in paths]
    return {
        "notes_checked": len(notes),
        "failures": sum(len(n["failures"]) for n in notes),
        "warnings": sum(len(n["warnings"]) for n in notes),
        "notes": notes,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--changed-only", action="store_true")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--path", default=None, help="check a single note file")
    ap.add_argument("--root", default=str(ROOT), help="repo root override")
    args = ap.parse_args(argv)
    root = Path(args.root).resolve()

    if args.path:
        p = Path(args.path)
        if not p.is_absolute():
            p = root / p
        paths = [p] if p.is_file() else []
        if not paths:
            print(f"no such file: {args.path}", file=sys.stderr)
            return 2
    elif args.changed_only:
        paths = changed_note_files(root)
    else:
        paths = None

    report = run(root, paths)
    failed = report["failures"] > 0 or (args.strict and report["warnings"] > 0)

    if args.json:
        report["strict"] = args.strict
        report["verdict"] = "FAIL" if failed else "PASS"
        print(json.dumps(report, indent=2))
        return 1 if failed else 0

    print("SMART NOTE COMPLETENESS GATE")
    print("=" * 78)
    print("human=section+prose | ai=section+prose | machine=section+parseable JSON")
    print("code=referenced from enforcement surface (warning only) | placement+owner")
    print("=" * 78)
    print(f"notes checked : {report['notes_checked']}")
    print(f"failures      : {report['failures']}")
    print(f"warnings      : {report['warnings']}")
    for n in report["notes"]:
        for f in n["failures"]:
            print(f"  FAIL  {n['note']}: {f}")
        for w in n["warnings"]:
            print(f"  WARN  {n['note']}: {w}")
    if args.strict and report["warnings"] and not report["failures"]:
        print("STRICT: warnings promoted to failures")
    print("=" * 78)
    print("VERDICT:", "FAIL (blocked)" if failed else "PASS")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
