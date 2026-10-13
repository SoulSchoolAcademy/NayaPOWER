"""Fail-closed reader guard for the NayaPOWER brain index layer (B-51 class).

B-51 (Shawn, filed P0): "a wrong answer with no error signal is worse than no
answer at all, because it teaches confidently." The committed index
(BRAIN/NAYAPOWER-BRAIN-INDEX.json) is only trustworthy while the local corpus
still agrees with the manifest it was regenerated against
(BRAIN/REAL-TREE.json: path -> git blob SHA, written by
tools/regenerate_brain_index.py from the committed git tree). The old reader
(json.loads of the file, zero comparison) served stale answers silently.

This module closes the READER side: before any consumer trusts the index, it
must prove the corpus agrees. Two distinct, tamper-evident refusal signals:

  FRESH    - every corpus file's bytes match the manifest's recorded blob SHA
             AND the receipt files on disk match the committed git tree.
             Verdict receipt includes the corpus fingerprint and whether the
             manifest's basis commit is the current HEAD, so a reader can tell
             "index regenerated against exactly this corpus" apart from "index
             regenerated against an older corpus".
  STALE    - corpus bytes drifted from the manifest (file edited, added to the
             manifest list, or deleted). Fix: tools/regenerate_brain_index.py.
  TAMPERED - the receipt/index files on disk differ from the committed git
             tree: the index was hand-edited instead of regenerated-and-
             committed. Fix: discard the local edits, regenerate.

Anything that cannot be verified (not a git checkout, missing manifest) also
refuses — there is no silent fallback. Loud error, never a quiet default.

P-011 scope note: this closes the reader side only. It does not repair the
writer-side drift (that is regenerate_brain_index.py's job), it does not fix
B-51's path-mismatch vector (wrong checkout entirely — see brain_registry's
root_override contract), and it does not attest semantic correctness of the
index contents — only that the corpus the index describes is the corpus on
disk, and that the index file itself is the committed one.

Refusal-class precedence (w85 spec, after Theta's w83 IV probes): the tamper
check runs BEFORE the staleness check, and a hand-removed
`receipt_basis_commit` still reads TAMPERED, not UNVERIFIABLE — because the
receipt files are compared against the COMMITTED git tree, and the on-disk
manifest no longer matches it. A manifest with a removed key IS verifiable
(the committed copy exists and differs), so UNVERIFIABLE would be a false
claim. The missing-basis state only legitimately arises when the key was
NEVER committed: then the seal is intact, nothing was broken, and the guard
returns FRESH with `basis_matches_head=False` — it never asserts agreement
it cannot verify. Tamper-by-hand-edit beats stale-by-drift beats
missing-basis, in that order, because a broken seal is a stronger claim than
a drifted corpus, and an absent basis is no claim at all.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

MANIFEST_REL = "BRAIN/REAL-TREE.json"
INDEX_REL = "BRAIN/NAYAPOWER-BRAIN-INDEX.json"

# The index layer is self-referential by design (see regenerate_brain_index.py):
# the receipt files describe the corpus, so they are checked against the
# committed tree rather than against their own content.
RECEIPT_FILES = (
    "BRAIN/NAYAPOWER-BRAIN-INDEX.json",
    "BRAIN/REAL-TREE.json",
    "BRAIN/REAL-TREE.md",
)

FRESH = "FRESH"
STALE = "STALE"
TAMPERED = "TAMPERED"


class BrainIndexGuardError(RuntimeError):
    """Base: the guard refused to let a consumer trust the brain index."""


class StaleBrainIndexError(BrainIndexGuardError):
    """Corpus bytes no longer match the index manifest (regen needed)."""


class TamperedBrainIndexError(BrainIndexGuardError):
    """Receipt/index files on disk differ from the committed git tree."""


class UnverifiableBrainIndexError(BrainIndexGuardError):
    """Cannot verify at all (not a git checkout / missing manifest): refuse."""


def _git(root: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        raise subprocess.CalledProcessError(proc.returncode, args, proc.stdout, proc.stderr)
    return proc.stdout.strip()


def _hash_files(root: Path, relpaths: list[str]) -> dict[str, str | None]:
    """git blob SHA for each path's bytes on disk; None when missing/unreadable.

    One git process via --stdin-paths (1257-file corpus in ~1s). Missing paths
    never reach git (it would exit 128 and misalign the output stream); they
    map to None, which can never equal a recorded blob SHA and therefore
    reads as drift, not as absence.
    """
    existing = [rel for rel in relpaths if (root / rel).is_file()]
    out: dict[str, str | None] = {rel: None for rel in relpaths}
    if existing:
        proc = subprocess.run(
            ["git", "-C", str(root), "hash-object", "--stdin-paths", "--"],
            input="\n".join(str(root / rel) for rel in existing),
            capture_output=True, text=True,
        )
        shas = proc.stdout.split()
        if proc.returncode != 0 or len(shas) != len(existing):
            # Partial output is untrustworthy: fall back to per-file hashing.
            for rel in existing:
                try:
                    out[rel] = _git(root, "hash-object", "--", str(root / rel))
                except subprocess.CalledProcessError:
                    out[rel] = None
        else:
            out.update(dict(zip(existing, shas)))
    return out


def corpus_fingerprint(root: Path | str, manifest: dict) -> str:
    """Deterministic sha256 over the corpus: sorted 'path:blob_sha' lines.

    Self-referential receipt entries (no blob SHA) are excluded: they are
    regen output, not corpus input, and are verified against the committed
    tree instead.

    Accepts a str or Path root (w85 fix: `inspect_index` coerced its root but
    this public entry point did not, raising TypeError on str roots).
    """
    root = Path(root)
    entries = [f for f in manifest["files"] if f.get("blob_sha")]
    blobs = _hash_files(root, [f["path"] for f in entries])
    lines = sorted(f"{f['path']}:{blobs.get(f['path'])}" for f in entries)
    return hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()


def inspect_index(root: Path | str) -> dict:
    """Verify the brain index is safe to read. Returns a verdict receipt.

    Raises StaleBrainIndexError / TamperedBrainIndexError /
    UnverifiableBrainIndexError on anything but FRESH. Never returns a verdict
    for an unverified state — the receipt is the proof, and the proof only
    exists when the corpus was actually compared.
    """
    root = Path(root)
    try:
        head_sha = _git(root, "rev-parse", "HEAD")
    except subprocess.CalledProcessError as e:
        raise UnverifiableBrainIndexError(
            f"{root} is not a git checkout (no HEAD): cannot verify the brain "
            f"index, refusing to read it. Fix: read from a real checkout."
        ) from e

    manifest_path = root / MANIFEST_REL
    if not manifest_path.is_file():
        raise UnverifiableBrainIndexError(
            f"missing manifest {MANIFEST_REL}: no corpus baseline to compare "
            f"against, refusing to read the index."
        )
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        entries = manifest["files"]
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        raise UnverifiableBrainIndexError(
            f"manifest {MANIFEST_REL} is unreadable: refusing to read the index."
        ) from e

    # Tamper check FIRST: the receipt files must be the committed ones. A
    # hand-edited index must read as TAMPERED, never as STALE.
    tampered: list[str] = []
    for rel in RECEIPT_FILES:
        try:
            committed = _git(root, "rev-parse", f"HEAD:{rel}")
        except subprocess.CalledProcessError:
            committed = None
        local = _hash_files(root, [rel]).get(rel)
        if local != committed:
            tampered.append(rel)
    if tampered:
        raise TamperedBrainIndexError(
            f"index layer files diverge from the committed git tree: "
            f"{', '.join(tampered)}. The index was edited on disk instead of "
            f"regenerated-and-committed. Fix: discard local edits and run "
            f"tools/regenerate_brain_index.py."
        )

    # Staleness check: every corpus file's bytes vs the manifest's blob SHA.
    # Self-referential receipt entries (no blob SHA — fixed-point design) are
    # skipped here: they are covered by the tamper check above, not by the
    # corpus comparison. Without the skip, a legitimate regen would always
    # read as STALE, making FRESH unattainable by design.
    corpus_entries = [f for f in entries if f.get("blob_sha")]
    blobs = _hash_files(root, [f["path"] for f in corpus_entries])
    stale = sorted(
        f["path"] for f in corpus_entries
        if blobs.get(f["path"]) != f.get("blob_sha")
    )
    if stale:
        shown = ", ".join(stale[:10]) + (" ..." if len(stale) > 10 else "")
        raise StaleBrainIndexError(
            f"corpus drifted under the committed index ({len(stale)} file(s): "
            f"{shown}). The index no longer describes the corpus on disk. "
            f"Fix: tools/regenerate_brain_index.py [--check]."
        )

    basis = manifest.get("receipt_basis_commit")
    return {
        "verdict": FRESH,
        "corpus_fingerprint": corpus_fingerprint(root, manifest),
        "receipt_basis_commit": basis,
        "basis_matches_head": basis == head_sha,
        "file_count": len(entries),
        "checked_paths": len(entries) + len(RECEIPT_FILES),
    }


def load_index_failclosed(root: Path | str, relpath: str = INDEX_REL) -> dict:
    """Read the brain index, or refuse loudly. No silent fallback, ever."""
    inspect_index(root)
    return json.loads((Path(root) / relpath).read_text(encoding="utf-8"))
