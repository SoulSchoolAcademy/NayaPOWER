"""Duplicate Detector — Operating Code V2, Gate 7.

WHY THIS EXISTS
---------------
The Smart Apps principle: solve once at 10, freeze, never rebuild. Rebuilding
an already-solved problem is the most expensive duplicate — it costs a whole
build, not a renumber. The registry (tools/solved_problem_registry.json) lists
problems already solved at 10 and frozen at their canonical location.

Run BEFORE building anything new:

    python3 tools/duplicate_detector.py --work "build a scanner for conflicting claims before building"

Verdicts:

    CLEAR           — no solved problem matches this work; build.
    FLAG            — a solved problem overlaps; STOP and take it to
                      consolidation review. The flag is mandatory; a human
                      decides (consolidate / extend the canonical seam /
                      justify the rebuild). This gate never auto-blocks.
    ENVIRONMENT FAILURE — the registry could not be read or is invalid;
                      do NOT treat as clear. UNKNOWN != CLEAR.

Matching is keyword-based and deliberately recall-biased, like
tools/board_claim_scan.py: a false positive costs a minute of reading; a
missed duplicate costs a rebuild.

WHY THIS IS A NEW FILE (not an extension of board_claim_scan.py)
----------------------------------------------------------------
board_claim_scan.py answers "is someone ALREADY CLAIMING this work?" against
LIVE state (open PRs + newest board comments). Its domain is concurrent
work-in-progress; its verdict is COLLISION (stop, coordinate).

This tool answers "was this problem ALREADY SOLVED and frozen?" against a
STATIC registry of solved problems. Different data source, different verdict
semantics (FLAG-for-human-consolidation-review, never auto-block), different
failure modes. Merging them would create exactly the duplicate-mechanism
defect this gate exists to prevent.

The tokenizer discipline is intentionally mirrored (compounds, versioned
tokens, bigrams, recall-biased thresholds) — a shared discipline, not a
shared code path. A shared import would couple two independent gates: a
refactor of one gate's matcher must never silently change the other gate's
verdicts. tools/protocol/engineering_gates.py's no_duplicate_systems gate
was also considered and rejected as the seam: it matches SYMBOL NAMES in
code, not problem descriptions — a rebuild under new names would sail
through it unflagged.

Stdlib only.
"""

import argparse
import json
import re
import sys
from pathlib import Path

DEFAULT_REGISTRY = Path(__file__).with_name("solved_problem_registry.json")

STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "to", "in", "on", "for", "with",
    "pr", "issue", "merge", "merged", "open", "closed", "fix", "feat",
    "docs", "repair", "build", "new", "from", "this", "that", "is",
    "it", "its", "as", "at", "by", "be", "are", "was", "were", "has",
    "have", "had", "will", "would", "can", "could", "should", "may",
    "not", "no", "so", "if", "but", "than", "then", "when", "which",
    "who", "what", "how", "why", "all", "any", "each", "every", "both",
}

# Words that describe the REQUEST or the registry mechanics, never the work
# itself. Deliberately NOT included: gate, scan, claim, check — those are
# work identifiers in this domain (see registry aliases).
DOMAIN_STOPWORDS = {
    "solved", "solve", "solves", "solving", "solution",
    "frozen", "freeze", "freezes", "freezing",
    "canonical",
    "registry", "registries",
    "mechanism", "mechanisms",
    "build", "builds", "building", "built", "rebuild", "rebuilds",
    "rebuilding", "rebuilt",
    "new", "proposed", "proposal",
    "problem", "problems",
    "entry", "entries",
    "consolidate", "consolidation", "consolidated",
    "detector", "detect", "detects", "detected", "detection",
    "tool", "tools",
    "work", "works", "working",
    "seat", "seats", "team", "teams", "naya", "coda", "shawn", "lane",
    "want", "wants", "need", "needs", "before", "start", "starting",
}

REQUIRED_ENTRY_KEYS = {"id", "problem", "canonical", "frozen"}


def _normalize_word(word):
    # Light plural folding for recall: "repairs" -> "repair", "prs" -> "pr".
    # Same treatment on both sides, so false conflations are symmetric.
    if len(word) > 2 and word.endswith("s") and not word.endswith(("ss", "us", "is")):
        return word[:-1]
    return word


def tokens(text):
    words = re.findall(r"[a-z0-9]+", text.lower())
    words = [_normalize_word(w) for w in words]
    compounds = re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)+", text.lower())
    kept = [w for w in words if w not in STOPWORDS and w not in DOMAIN_STOPWORDS]
    toks = {w for w in kept if len(w) > 2}
    toks.update(w for w in kept if re.fullmatch(r"v\d+", w))
    toks.update(c for c in compounds if len(c) > 4)
    toks.update(f"{a} {b}" for a, b in zip(kept, kept[1:]) if len(a) > 1 and len(b) > 1)
    return toks


def load_registry(path):
    """Load and strictly validate the registry. Any defect is fatal:
    a gate that cannot read its registry must not report CLEAR."""
    try:
        data = json.loads(Path(path).read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"REGISTRY_UNREADABLE: {path}: {exc}")
    if not isinstance(data, dict) or not isinstance(data.get("problems"), list):
        raise RuntimeError("REGISTRY_SCHEMA: top-level 'problems' list missing")
    if not data["problems"]:
        raise RuntimeError("REGISTRY_SCHEMA: registry has zero entries")
    seen_ids = set()
    for i, entry in enumerate(data["problems"]):
        if not isinstance(entry, dict):
            raise RuntimeError(f"REGISTRY_SCHEMA: entry {i} is not an object")
        missing = REQUIRED_ENTRY_KEYS - set(entry)
        if missing:
            raise RuntimeError(f"REGISTRY_SCHEMA: entry {i} missing keys {sorted(missing)}")
        eid = entry["id"]
        if not isinstance(eid, str) or not eid:
            raise RuntimeError(f"REGISTRY_SCHEMA: entry {i} has invalid id")
        if eid in seen_ids:
            raise RuntimeError(f"REGISTRY_SCHEMA: duplicate entry id {eid}")
        seen_ids.add(eid)
        if not isinstance(entry["problem"], str) or len(entry["problem"]) < 20:
            raise RuntimeError(f"REGISTRY_SCHEMA: entry {eid} problem prose too short")
        if not isinstance(entry["canonical"], str) or not entry["canonical"]:
            raise RuntimeError(f"REGISTRY_SCHEMA: entry {eid} canonical path invalid")
    return data["problems"]


def entry_text(entry):
    aliases = entry.get("aliases") or []
    return f"{entry['problem']} {' '.join(aliases)}"


def scan(work, entries):
    """Recall-biased overlap scan. Returns (flags, advisories).

    FLAG: a shared compound identifier (SP-001, smart-note-v2), a versioned
    bigram ("ask v9"), >= 2 shared bigram phrases, or >= 3 shared distinctive
    unigrams. Advisory: >= 2 shared tokens of any kind.
    """
    work_toks = tokens(work)
    flags = []
    advisories = []
    for entry in entries:
        entry_toks = tokens(entry_text(entry))
        shared = work_toks & entry_toks
        shared_compounds = {t for t in shared if "-" in t}
        shared_bigrams = {t for t in shared if " " in t}
        shared_unigrams = shared - shared_compounds - shared_bigrams
        versioned_bigrams = {t for t in shared_bigrams if re.search(r"v\d+", t)}
        if (shared_compounds or versioned_bigrams
                or len(shared_bigrams) >= 2 or len(shared_unigrams) >= 3):
            flags.append((entry, sorted(shared)))
        elif len(shared) >= 2:
            advisories.append((entry, sorted(shared)))
    return flags, advisories


def main(argv):
    ap = argparse.ArgumentParser(
        description="Gate 7: flag proposed work that duplicates a frozen solved problem."
    )
    ap.add_argument("--work", required=True,
                    help="Description of the work you intend to build.")
    ap.add_argument("--registry", default=str(DEFAULT_REGISTRY),
                    help="Path to solved_problem_registry.json.")
    args = ap.parse_args(argv)

    try:
        entries = load_registry(args.registry)
    except Exception as exc:  # noqa: BLE001 — environment failure is a verdict
        print(f"ENVIRONMENT FAILURE: {exc} — could not read registry; do NOT treat as clear.")
        return 3

    flags, advisories = scan(args.work, entries)

    print(f"work: {args.work}")
    print(f"registry: {args.registry} ({len(entries)} solved problems)")
    if flags:
        print("VERDICT: FLAG — possible duplicate of a frozen solved problem.")
        print("Do not rebuild. Take this to consolidation review: extend the")
        print("canonical seam, or justify the rebuild to the human director.")
        for entry, shared in flags:
            print(f"  - [{entry['id']}] {entry['canonical']} (shared: {', '.join(shared)})")
        return 2
    print("VERDICT: CLEAR — no solved problem matches this work.")
    if advisories:
        print("advisories (weak matches, skim before building):")
        for entry, shared in advisories[:5]:
            print(f"  - [{entry['id']}] {entry['canonical']} (shared: {', '.join(shared)})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
