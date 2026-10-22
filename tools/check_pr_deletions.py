#!/usr/bin/env python3
"""No-silent-deletion gate: every deleted file must be declared.

Compares BASE_SHA...HEAD_SHA. For each file with deletion status, the
deletion must be DECLARED through at least one declaration channel:

  1. PR body — a `## Deletions` or `## Drop rationale` section naming the
     file (full path or basename) with a reason.
  2. Any new commit message in BASE_SHA...HEAD_SHA (merge commits included)
     — the same section convention, OR a prose paragraph that names the file
     (full path or basename) together with a rationale cue
     ("superseded by", "replaced by", ... — see RATIONALE_CUES).
  3. Explicit waiver — a `Waived-Deletions:` trailer in the PR body or any
     new commit message listing the path. Waived deletions PASS but are
     named in the output: the waiver is auditable, never silent.

Channel 2 closes the #2600 artifact class (2026-10-15): a deletion
documented with rationale in the merge commit message — but with no
`## Deletions` section in the PR body — ate a FAILURE. A documented,
behaviorally-required deletion is not a silent deletion.

This still kills the stale-head trap: a PR built on an old base that
silently drops files added to main after the base shows those drops as
deletions here, and an unmentioned drop still fails the gate. Mentioning a
path without a rationale cue also fails — the gate demands a reason, not a
passing reference.

Exit 0 = clean. Exit 1 = undeclared deletions.
"""
import os
import re
import subprocess
import sys

SECTION_RE = re.compile(r"^##\s+(deletions|drop rationale)\s*$",
                        re.IGNORECASE | re.MULTILINE)
NEXT_SECTION_RE = re.compile(r"^##\s+", re.MULTILINE)
WAIVER_RE = re.compile(r"^waived-deletions\s*:\s*(.+)$",
                       re.IGNORECASE | re.MULTILINE)

# A prose paragraph declares a deletion only when it names the path AND
# carries one of these rationale cues. The list is deliberately narrow: each
# cue reads as a reason for the drop. A bare mention ("see X for the old
# battery") does not declare.
RATIONALE_CUES = (
    "superseded by", "supersedes",
    "replaced by", "replaces",
    "renamed to", "moved to",
    "consolidated into", "merged into",
    "deleted because", "removed because", "retired because",
    "drop rationale", "deletion rationale",
    "no longer needed", "obsolete",
    "in favor of", "duplicate of",
)


def run_git(args):
    return subprocess.run(["git"] + args, capture_output=True, text=True)


def section_bodies(text):
    """Bodies of all `## Deletions` / `## Drop rationale` sections."""
    bodies = []
    for m in SECTION_RE.finditer(text or ""):
        rest = text[m.end():]
        nxt = NEXT_SECTION_RE.search(rest)
        bodies.append(rest[:nxt.start()] if nxt else rest)
    return bodies


def waiver_paths(text):
    """Paths listed in `Waived-Deletions:` trailers (comma-separated)."""
    paths = []
    for m in WAIVER_RE.finditer(text or ""):
        paths.extend(p.strip().strip("`\"'") for p in m.group(1).split(","))
    return [p for p in paths if p]


def paragraphs(text):
    """Prose paragraphs, with declared sections and waiver trailers removed
    so section prose is not double-counted as free prose."""
    stripped = SECTION_RE.sub("", text or "")
    stripped = WAIVER_RE.sub("", stripped)
    return [p for p in re.split(r"\n\s*\n", stripped) if p.strip()]


def names_mentioned(candidates, text):
    low = (text or "").lower()
    return [c for c in candidates if c.lower() in low]


def commit_messages(base, head):
    """Raw bodies of every new commit in BASE_SHA...HEAD_SHA (merge commits
    included). Empty string if the log cannot be read — the PR body channel
    still applies."""
    out = run_git(["log", "--format=%B%x1e", f"{base}...{head}"])
    return out.stdout if out.returncode == 0 else ""


def check(base, head, pr_body):
    """Gate logic. Returns (ok: bool, report: list[str]). No process exit —
    unit-testable."""
    diff = run_git(["diff", "--diff-filter=D", "--name-only", "-z",
                    f"{base}...{head}"])
    if diff.returncode != 0:
        return True, [f"git diff failed ({diff.stderr.strip()}); skipping."]
    deleted = [p for p in diff.stdout.split("\0") if p]
    if not deleted:
        return True, ["No deletions. Clean."]

    channels = [pr_body or "", commit_messages(base, head)]
    section_text = "\n".join(
        b for t in channels for b in section_bodies(t))
    waived = [w for t in channels for w in waiver_paths(t)]
    paras = [p for t in channels for p in paragraphs(t)]

    declared_via = {}
    undeclared = []
    for path in deleted:
        candidates = [path, os.path.basename(path)]
        if names_mentioned(candidates, section_text):
            declared_via[path] = "section"
            continue
        if any(w.lower() in (path.lower(), os.path.basename(path).lower())
               for w in waived):
            declared_via[path] = "waiver"
            continue
        hit = False
        for p in paras:
            pl = p.lower()
            if ((path.lower() in pl or os.path.basename(path).lower() in pl)
                    and any(cue in pl for cue in RATIONALE_CUES)):
                hit = True
                break
        if hit:
            declared_via[path] = "prose+rationale"
            continue
        undeclared.append(path)

    lines = [f"DECLARED ({how}): {path}"
             for path, how in declared_via.items()]
    if undeclared:
        lines.append(
            f"DELETION GATE FAILED: {len(undeclared)} undeclared "
            f"deletion(s): {', '.join(undeclared[:10])}. "
            f"Total deleted in this PR: {len(deleted)}.")
        lines.append(
            "Fix: declare each deletion under `## Deletions` (in the PR body "
            "or a commit message — merge messages count), write the reason "
            "in prose next to the file path, or add a `Waived-Deletions:` "
            "trailer naming the path. If the deletion is a stale-head "
            "accident, rebase onto current main instead.")
        return False, lines
    lines.append(f"Deletion check OK: {len(deleted)} deletion(s), all declared.")
    return True, lines


def main():
    base = os.environ.get("BASE_SHA", "")
    head = os.environ.get("HEAD_SHA", "")
    body = os.environ.get("PR_BODY") or ""
    if not base or not head:
        print("No base/head SHAs provided; skipping deletion check.")
        return
    ok, lines = check(base, head, body)
    print("\n".join(lines))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
