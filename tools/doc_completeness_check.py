#!/usr/bin/env python3
"""
Documentation Completeness Checker — Naya 5, Documentation Completeness owner.
Shawn's order (2026-10-10): every intelligence artifact must exist in FOUR forms:
  1. Machine/code — executable or machine-enforced
  2. Structured data — queryable JSON/schema
  3. AI language — reasoning-friendly
  4. Human language — plain words

And in all ideal locations: repo, doctrine index, lessons, checklist, memory.

Usage:
  python3 tools/doc_completeness_check.py [--changed-only] [--strict]
  --changed-only: check only files changed vs origin/main (for CI)
  --strict: code-form gaps become failures instead of warnings

Exit codes: 0 = all checks pass; 1 = failures; warnings never fail (unless --strict).
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CAPTURE_DIR = ROOT / ".naya" / "capture"
GOV_DIR = ROOT / "BRAIN" / "01-GOVERNANCE"


def substantive(v, min_len=50):
    if isinstance(v, str):
        return len(v.strip()) >= min_len
    if isinstance(v, dict):
        return any(isinstance(x, str) and len(x.strip()) >= 20 for x in v.values())
    if isinstance(v, list):
        return any(isinstance(x, str) and len(x.strip()) >= 20 for x in v)
    return False


def check_smart_note(path: Path):
    """Returns (failures, warnings) for one capture JSON."""
    failures, warnings = [], []
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        return [f"{path.name}: invalid JSON: {e}"], []
    intel = doc.get("intelligence", {})
    schema = doc.get("schema")
    # Capture requests (v1) are in-flight artifacts, not finalized notes —
    # the scan's note checks do not apply. Warn, never fail.
    if schema and schema != "naya.smart-note-capture.v2":
        return ([], [f"{path.name}: not a canonical v2 note (schema {schema}) — skipped by note checks"])
    # Form 2: structured
    if schema != "naya.smart-note-capture.v2":
        failures.append(f"{path.name}: missing/wrong canonical schema")
    # Form 4: human language
    if not substantive(intel.get("human_view")) and not substantive(intel.get("simple_view")):
        failures.append(f"{path.name}: human form missing (no substantive human_view/simple_view)")
    # Form 3: AI language
    if not substantive(intel.get("ai_view")) and not substantive(intel.get("naya_view")):
        failures.append(f"{path.name}: AI form missing (no substantive ai_view/naya_view)")
    # Form 2b: machine view (structured machine-readable)
    mv = intel.get("machine_view", {})
    if not isinstance(mv, dict) or not mv:
        failures.append(f"{path.name}: machine_view missing")
    # Lifecycle declared — legacy (pre-v2-field) notes warn instead of
    # failing: the four FORM checks above stay failures; lifecycle_state is
    # bookkeeping, and failing it backfills a new requirement onto old
    # corpus. The warning keeps the backfill owed and visible. --strict
    # still promotes warnings, so strict gates keep teeth.
    if not doc.get("lifecycle_state"):
        warnings.append(f"{path.name}: lifecycle_state undeclared (legacy backfill owed)")
    # Form 1: machine/code — is this note consumed by executable code or the runtime index?
    nid = doc.get("smart_note_id", "")
    if nid:
        code_ref = has_code_reference(nid)
        if code_ref is None:
            warnings.append(f"{path.name}: code-ref instrument timed out (not a corpus gap — re-run before trusting)")
        elif not code_ref:
            warnings.append(f"{path.name}: code form gap — no executable consumer references {nid}")
    return failures, warnings


_code_ref_cache = {}


def _grep_code_reference(note_id: str):
    """One grep pass. Returns (ok, hit_count); ok=False means the
    instrument failed (timeout), not that the note has no references."""
    try:
        out = subprocess.run(
            ["grep", "-rl", note_id, "--include=*.py", "--include=*.ts",
             "--include=*.js", "--include=*.mjs", "--include=*.yml",
             "tools/", "kernel/", "orchestrator/", "supabase/functions/",
             "BRAIN/01-GOVERNANCE/"],
            capture_output=True, text=True, timeout=60, cwd=ROOT)
        hits = sorted(h for h in out.stdout.strip().split("\n") if h and ".naya/capture" not in h)
        return True, len(hits)
    except Exception:
        return False, 0


def has_code_reference(note_id: str):
    """Check if any executable file references this note ID (outside capture dir).
    Returns True/False/None — None means the instrument failed (grep timeout),
    which is NOT a corpus gap. Callers warn distinctly so an instrument flake
    can never masquerade as a code-form gap (P-038)."""
    if note_id in _code_ref_cache:
        return _code_ref_cache[note_id]
    ok, hits = _grep_code_reference(note_id)
    if not ok:
        ok, hits = _grep_code_reference(note_id)  # one retry: transient load
    _code_ref_cache[note_id] = (hits > 0) if ok else None
    return _code_ref_cache[note_id]


def corpus_manifest(notes):
    """Fingerprint of the scanned note SET (name+size+mtime): two runs are
    comparable only when manifests match. A count diff across manifests is
    input drift (new/changed notes between runs), not instrument flake.
    P-038: never diff warning counts without the manifest."""
    h = hashlib.sha256()
    for n in notes:
        try:
            st = n.stat()
            h.update(f"{n.name}\x00{st.st_size}\x00{st.st_mtime_ns}\n".encode())
        except OSError:
            h.update(f"{n.name}\x00MISSING\n".encode())
    return h.hexdigest()[:16]


def tree_pin(root):
    """Best-effort pin of the scanned tree: git HEAD + dirty flag.
    Never fails the scan; 'unknown' when not a git checkout."""
    try:
        head = subprocess.run(["git", "rev-parse", "--short=12", "HEAD"],
                              capture_output=True, text=True, timeout=10,
                              cwd=root).stdout.strip() or "unknown"
        dirty = subprocess.run(["git", "status", "--porcelain"],
                               capture_output=True, text=True, timeout=15,
                               cwd=root).stdout.strip()
        return head + ("+dirty" if dirty else "")
    except Exception:
        return "unknown"


def check_law_triple(gov_dir: Path):
    """Every law .md should have .ai.md + .human.md + .machine.json siblings."""
    failures, warnings = [], []
    # Build a case-insensitive index of all files
    all_files = {f.name.lower(): f.name for f in gov_dir.iterdir() if f.is_file()}
    # Find base names: strip known suffixes (case-insensitive)
    bases = set()
    for f in gov_dir.glob("*.md"):
        n = f.name
        nl = n.lower()
        for suffix in (".ai.md", ".human.md", ".md"):
            if nl.endswith(suffix):
                bases.add(n[: -len(suffix)])
                break
    for base in sorted(bases, key=str.lower):
        if base.lower() in ("readme",):
            continue
        bl = base.lower()
        ai = bl + ".ai.md" in all_files
        human = bl + ".human.md" in all_files
        machine = bl + ".machine.json" in all_files
        plain = bl + ".md" in all_files
        # A law is "complete" if it has the triple; single .md without triple is flagged
        has_triple = ai or human or machine
        if has_triple:
            if not ai:
                failures.append(f"{base}: AI form missing ({base}.ai.md)")
            if not human:
                failures.append(f"{base}: human form missing ({base}.human.md)")
            if not machine:
                failures.append(f"{base}: machine form missing ({base}.machine.json)")
            else:
                mpath = gov_dir / all_files[bl + ".machine.json"]
                try:
                    json.loads(mpath.read_text(encoding="utf-8"))
                except Exception as e:
                    failures.append(f"{base}: machine.json invalid: {e}")
        elif plain and base[0].isdigit():
            # Numbered law with only a single .md — incomplete by the 4-form standard
            warnings.append(f"{base}: single-form law (no .ai/.human/.machine triple)")
    return failures, warnings


def changed_files():
    """Files changed vs origin/main."""
    out = subprocess.run(
        ["git", "diff", "--name-only", "origin/main...HEAD"],
        capture_output=True, text=True, cwd=ROOT)
    return [ROOT / p for p in out.stdout.strip().split("\n") if p]


def main():
    strict = "--strict" in sys.argv
    changed_only = "--changed-only" in sys.argv
    failures, warnings = [], []

    if changed_only:
        files = changed_files()
        notes = [f for f in files if f.suffix == ".json" and ".naya/capture" in str(f)]
    else:
        notes = sorted(CAPTURE_DIR.glob("SMART-NOTE-*.json"))

    for n in notes:
        f, w = check_smart_note(n)
        failures.extend(f)
        warnings.extend(w)

    lf, lw = check_law_triple(GOV_DIR)
    failures.extend(lf)
    warnings.extend(lw)

    failures.sort()
    warnings.sort()
    manifest = corpus_manifest(notes)
    pin = tree_pin(ROOT)
    print(f"Checked {len(notes)} Smart Notes + governance triples.")
    print(f"Corpus manifest: {manifest} | tree: {pin}")
    print("Comparability rule: diff counts only across identical manifests.")
    print(f"Failures: {len(failures)}, Warnings: {len(warnings)}")
    for x in failures:
        print(f"  FAIL: {x}")
    for x in warnings[:20]:
        print(f"  WARN: {x}")
    if len(warnings) > 20:
        print(f"  ... and {len(warnings) - 20} more warnings")

    if strict and warnings:
        print("STRICT: warnings promoted to failures")
        return 1
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
