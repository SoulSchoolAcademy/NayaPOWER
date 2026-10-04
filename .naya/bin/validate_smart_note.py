#!/usr/bin/env python3
"""Smart Note conformance gate — the Law Is the Code, enforced at merge.

Fails the PR when any Smart Note capture or view violates the canonical law:
  1. Every capture JSON under .naya/capture/ must be schema naya.smart-note-capture.v2,
     with the governance keys present and true.
  2. Every generated projection (human .md, AI .ai.md, machine .machine.json)
     must live under the canonical brain path:
     BRAIN/05-MEMORY/SMART-NOTES/<yyyy>/<mm>/<dd>/... — nowhere else. Invented
     locations (e.g. .naya/preview/) are refused, as is any new markdown under
     .naya/ and any non-.machine.json under the brain notes tree.
  3. One capture JSON per PR (batch guard).
  4. smart_note_id must not already exist on main (identity collision guard).

Usage: validate_smart_note.py <changed-file> [<changed-file> ...]
Exit 0 = conformant. Exit 1 = violation (message explains the exact breach).
"""
import json
import re
import subprocess
import sys

REQUIRED_TOP = [
    "schema", "smart_note_id", "capture_id", "canonical_intent",
    "category", "topic", "subtopic", "title", "source", "intelligence",
]
BRAIN_RE = re.compile(
    r"^BRAIN/05-MEMORY/SMART-NOTES/\d{4}/\d{2}/\d{2}/.+"
    r"/SN-\d{3,4}/IB-SMART-NOTE-\d{8}-sn\d+-[a-z0-9-]+"
    r"\.(md|ai\.md|machine\.json)$"
)


def fail(msg):
    print(f"CONFORMANCE-GATE FAIL: {msg}")
    sys.exit(1)


def repo_rel(path):
    """Repo-relative path for classification (handles absolute or relative input)."""
    for anchor in (".naya/capture/", ".naya/", "BRAIN/05-MEMORY/SMART-NOTES/"):
        i = path.find(anchor)
        if i != -1:
            return path[i:]
    return path


def is_new(path):
    """True if the path does not exist on origin/main (i.e. added by this PR)."""
    rel = repo_rel(path)
    r = subprocess.run(["git", "cat-file", "-e", f"origin/main:{rel}"],
                       capture_output=True, timeout=30)
    return r.returncode != 0


def check_capture(path):
    try:
        with open(path, encoding="utf-8") as fh:
            d = json.load(fh)
    except Exception as ex:
        fail(f"{path}: not valid JSON ({ex})")
    for k in REQUIRED_TOP:
        if k not in d:
            fail(f"{path}: missing required field '{k}'")
    if d.get("schema") != "naya.smart-note-capture.v2":
        fail(f"{path}: schema must be naya.smart-note-capture.v2, got {d.get('schema')!r}")
    mv = d.get("intelligence", {}).get("machine_view", {})
    if mv.get("raw_source_separate_from_distillation") is not True:
        fail(f"{path}: machine_view.raw_source_separate_from_distillation must be true")
    if mv.get("automatic_truth_ceiling") != "CANDIDATE":
        fail(f"{path}: machine_view.automatic_truth_ceiling must be CANDIDATE")
    sid = d.get("smart_note_id", "")
    if not re.fullmatch(r"SN-\d{3,4}", sid or ""):
        fail(f"{path}: smart_note_id must match SN-NNN(N), got {sid!r}")
    return sid


def id_exists_on_main(sid):
    """True if smart_note_id already appears in main's captures or brain notes."""
    try:
        out = subprocess.run(
            ["git", "grep", "-l", sid, "origin/main", "--",
             ".naya/capture/", "BRAIN/05-MEMORY/SMART-NOTES/"],
            capture_output=True, text=True, timeout=60)
    except Exception:
        return False
    return bool(out.stdout.strip())


def main(files):
    rels = [repo_rel(f) for f in files]
    pair = dict(zip(rels, files))  # rel -> real path for opening
    captures = [r for r in rels
                if r.startswith(".naya/capture/") and r.endswith(".json")]
    views = [r for r in rels
             if re.search(r"IB-SMART-NOTE-.*\.(md|ai\.md|machine\.json)$", r)]
    # Placement law, part 1: no NEW markdown under .naya/ except READMEs.
    # .naya/ is machine territory (captures, specs, memory). Human views do not
    # live there — this refuses the entire invented-location class (e.g. the
    # .naya/preview/ failure), not just one directory name.
    for r in rels:
        if (r.startswith(".naya/") and r.endswith(".md")
                and not r.endswith("/README.md") and is_new(r)):
            fail(f"{r}: new markdown under .naya/ is refused — human views live "
                 f"only at BRAIN/05-MEMORY/SMART-NOTES/<yyyy>/<mm>/<dd>/...")
    # Placement law, part 1b: no NEW json under BRAIN/ except .machine.json.
    # The brain's machine truth is the generated machine projection — never a
    # hand-placed capture copy.
    for r in rels:
        if (r.startswith("BRAIN/05-MEMORY/SMART-NOTES/") and r.endswith(".json")
                and not r.endswith(".machine.json") and is_new(r)):
            fail(f"{r}: only generated .machine.json projections live in the brain — "
                 f"capture JSONs belong in .naya/capture/")

    # Batch guard: one authored capture per PR.
    if len(captures) > 1:
        fail(f"batch guard: {len(captures)} capture JSONs in one PR "
             f"({', '.join(captures)}); one capture per PR.")

    # Placement law, part 2: human views live ONLY at the canonical brain path.
    for v in views:
        if not BRAIN_RE.match(v):
            fail(f"{v}: human views must live at "
                 f"BRAIN/05-MEMORY/SMART-NOTES/<yyyy>/<mm>/<dd>/.../SN-NNN/IB-SMART-NOTE-....md "
                 f"— invented locations are refused.")

    # Schema + governance + identity for each capture.
    for c in captures:
        sid = check_capture(pair[c])
        if id_exists_on_main(sid):
            fail(f"{c}: smart_note_id {sid} already exists on main "
                 f"(first claim stands — renumber).")

    print(f"CONFORMANCE-GATE PASS: {len(captures)} capture(s), "
          f"{len(views)} view(s) conformant.")


if __name__ == "__main__":
    main(sys.argv[1:])
