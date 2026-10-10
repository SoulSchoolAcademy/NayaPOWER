#!/usr/bin/env python3
"""
GATE 1 — Activation Checklist Verifier (Operating Code V2, Domain 4).

Audit provision (BRAIN/01-GOVERNANCE/0008-OPERATING-CODE-V2-ENCODING-AUDIT.md,
Domain 4, class ENCODE): "Bake it in at activation — Gate: activation
checklist is machine-verified. All 14 lessons + V2 loaded = activation
complete. Missing = not activated."

The gap this closes: tools/activation_gate.py guards the DELIVERY boundary
(HTML pages bound to receipts; its closed-world registry covers only
design_contract + blocks_catalog) and kernel/protocol/cold_start_gate.py
guards boot sequence (read receipt, identity, authority, navigation, next
action). NOTHING machine-verified that the activating agent actually loaded
the 14 thinking-pattern lessons (PR #2059:
NAYA-ACTIVATION/thinking-curriculum.json) and Operating Code V2
(BRAIN/01-GOVERNANCE/0008-OPERATING-CODE-V2.*, PR #2087). This verifier is
that checklist, fail-closed.

Two modes:
  1. --self-audit (default): verify the canonical artifacts THEMSELVES are
     present, complete, and current —
       - NAYA-ACTIVATION/thinking-curriculum.json: exactly 14 lessons,
         ids == {L1..L14}, required fields present, curriculum marked
         mandatory, per-lesson pass threshold >= 7, and every lesson's
         fingerprint matches the pinned CURRICULUM pins (drift in lesson
         content = a deliberate re-pin, never silent).
       - NAYA-ACTIVATION/THINKING-CURRICULUM-V1.md: the human twin
         enumerates the same 14 lesson ids (machine/human twin consistency).
       - V2 files (3): all present; each sha256 matches the pinned V2 pins;
         the machine twin parses and carries id == "OPERATING-CODE-V2".
  2. --checklist PATH: verify an agent's activation checklist CLAIM against
     the canonical bytes (recomputed, never trusted):
       - claim.lessons must name exactly the 14 canonical lesson ids, each
         with sha256 == sha256(canonical lesson bytes).
       - claim.v2 must fingerprint the 3 V2 files with matching sha256.
     Adversarial closures: fake lesson ids -> LESSON_NOT_REGISTERED;
     fewer than 14 -> LESSON_MISSING (partial loading); wrong hash ->
     LESSON_FINGERPRINT_MISMATCH (forged/stale content); V2 hash drift ->
     V2_STALE; V2 file absent -> V2_MISSING.

Honest boundary (evidence law): this gate proves the claim is COMPLETE and
BYTE-FAITHFUL to canonical sources, and that the canonical sources are
intact and current. It does not prove the agent internalized the lessons —
behavioral proof (novel problem, blind scored >= 7 per the curriculum's
verification protocol) is the RITUAL side of the same provision and lives
outside this machine gate. Score claims inside a checklist are read as
self-attested, never as verified proof.

Wiring point: kernel/protocol/cold_start_gate.py is the boot sequence this
checklist belongs to (activation is not complete until the checklist
verifies). The pure predicate check_checklist() is importable so the cold
start gate can fold its verdict in without duplicating the registry.

Exit codes: 0 = CHECKLIST-VERIFIED | 1 = REJECT (fail closed) |
            2 = tool error (canonical artifacts unreadable — fail closed).
"""

import argparse
import hashlib
import json
import os
import re
import sys

# ---------------------------------------------------------------------------
# Canonical locations (repo-relative)
# ---------------------------------------------------------------------------

CURRICULUM_JSON = "NAYA-ACTIVATION/thinking-curriculum.json"
CURRICULUM_HUMAN_MD = "NAYA-ACTIVATION/THINKING-CURRICULUM-V1.md"

V2_FILES = (
    "BRAIN/01-GOVERNANCE/0008-OPERATING-CODE-V2.human.md",
    "BRAIN/01-GOVERNANCE/0008-OPERATING-CODE-V2.ai.md",
    "BRAIN/01-GOVERNANCE/0008-operating-code-v2.machine.json",
)
V2_MACHINE_JSON = V2_FILES[2]

EXPECTED_LESSON_IDS = frozenset("L%d" % i for i in range(1, 15))
REQUIRED_LESSON_FIELDS = ("lesson_id", "title", "slug", "what_it_is",
                          "test_problem", "rubric", "pass_threshold")
LESSON_ID_RE = re.compile(r"^L(1[0-4]|[1-9])$")
HUMAN_LESSON_HEADER_RE = re.compile(r"^### C\d+ \u2014 (L\d+):", re.MULTILINE)
SHA64_RE = re.compile(r"^[a-fA-F0-9]{64}$")

# ---------------------------------------------------------------------------
# Pins. Content-addressed trust roots, mirroring DESIGN_GATE_PIN in
# tools/activation_gate.py: a drift in lesson content or V2 bytes is a
# deliberate re-pin (code change), never a silent pass.
# ---------------------------------------------------------------------------

# Pinned 2026-10-10 from origin/main @
# 93030048d421686c917af6e872277f1985255ede (PR #2059 curriculum, intact).
# Lesson fingerprint = sha256 of canonical lesson bytes:
#   json.dumps(lesson, sort_keys=True, separators=(",", ":"),
#              ensure_ascii=True).encode("utf-8")
CURRICULUM_PIN_SOURCE = (
    "origin/main @ 93030048d421686c917af6e872277f1985255ede "
    "(PR #2059, thinking-curriculum.json v1.0)")
CURRICULUM_LESSON_PINS = {
    "L1":  "1a2ac735e21bad785bf46ee63932ca6720b64234ae6673ea1910b9640169862b",
    "L2":  "599437f64d9f084ae899e519bbe3d6b86b195b6e956fb8a0427c5bdc04e90e27",
    "L3":  "5b138e9f64a84add11acb12c8bfbb279bac1005c15be63c0e6899903af78bd58",
    "L4":  "9f3cc6aa77cf65b64ea63f1ab619c86658ebeac6efcee4e877df5e33c98c647d",
    "L5":  "0612fcb425a4d4593e2c27eb78876b340323123818d05e25c5713b7a3ec4ec06",
    "L6":  "27a3674c52144b74badbbc55dbc13590f38291d55b97df52d7c83013106d61f9",
    "L7":  "672813143d3bb1e9ff26e7b0ab3dfe3c9de08050b714f693fe0f975559fd9010",
    "L8":  "acde7986abceaee28424a354146f5af8b36a5f3a8730e9266795a7320cc8cdf6",
    "L9":  "937877e0b3543cdf3589f3291e49494a739ef42ab3aa4c0ca7e5f1495e31d0da",
    "L10": "fc93fed723f2a1229d2c58311ca87539d3133ce8d5792dbf9de78a94da202e5f",
    "L11": "8b2e72d3a93aaaef26af88ef599dd9dc451feab014838b6949c36f839388c837",
    "L12": "1473412ab4467b25672eb2704ad7df75b2c62a412f7f950660d08c5a096bac7f",
    "L13": "f329555f352b163bce0c77fdb30ce70b990e403865f56750073e2619fd6bc796",
    "L14": "4a9962ac4aa6e686472499e781a9a068e1d3e16169c543e7f94ecd1d68624364",
}

# Pinned 2026-10-10 from origin/brain-build/operating-code-v2 @
# 8a93355173141bd8b1d8ab40e2a21dac91610fb4 (PR #2087, OPEN/unmerged).
# Until #2087 merges, run with --v2-root pointing at a checkout of that
# branch (or pass --v2-expect to re-pin deliberately). After merge, re-pin
# to the main-tip bytes — the pin source string must name the new ref.
V2_PIN_SOURCE = (
    "origin/brain-build/operating-code-v2 @ "
    "8a93355173141bd8b1d8ab40e2a21dac91610fb4 (PR #2087, unmerged 2026-10-10)")
V2_FILE_PINS = {
    "BRAIN/01-GOVERNANCE/0008-OPERATING-CODE-V2.human.md":
        "b83595c71f42615d22b5e2b49972acc9cb309ef0ce893f12f2979f32716423ec",
    "BRAIN/01-GOVERNANCE/0008-OPERATING-CODE-V2.ai.md":
        "afedf3b6cf23851063499c581e3ff6a74eb0444f11e82c2f8868a29ebf732d16",
    "BRAIN/01-GOVERNANCE/0008-operating-code-v2.machine.json":
        "1c12d07a4abb5e35803324515e3d0024daa04ece02942e09713008edb9543e79",
}


def _sha256_hex(data):
    return hashlib.sha256(bytes(data)).hexdigest()


def canonical_lesson_bytes(lesson):
    """Deterministic serialization of one lesson dict -> bytes."""
    return json.dumps(lesson, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("utf-8")


def lesson_fingerprint(lesson):
    return _sha256_hex(canonical_lesson_bytes(lesson))


# ---------------------------------------------------------------------------
# Canonical artifact loading (trusted local checkout; unreadable = tool error)
# ---------------------------------------------------------------------------

def _read_bytes(root, rel):
    path = os.path.join(root, *rel.split("/"))
    with open(path, "rb") as f:
        return f.read()


def load_canonical(repo_root, v2_root=None):
    """Load canonical artifacts. Returns (canonical, error).

    canonical = {"lessons": {lesson_id: lesson_dict},
                 "lesson_hashes": {lesson_id: sha256},
                 "curriculum": <full curriculum dict>,
                 "human_md": <text>,
                 "v2_hashes": {rel_path: sha256},
                 "v2_machine": <parsed machine.json>}
    """
    v2_root = v2_root or repo_root
    try:
        raw = _read_bytes(repo_root, CURRICULUM_JSON)
    except OSError as e:
        return None, "cannot read canonical curriculum %s: %s" % (CURRICULUM_JSON, e)
    try:
        curriculum = json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError) as e:
        return None, "canonical curriculum is not valid JSON: %s" % e
    try:
        human_md = _read_bytes(repo_root, CURRICULUM_HUMAN_MD).decode(
            "utf-8", errors="replace")
    except OSError as e:
        return None, "cannot read human curriculum twin %s: %s" % (CURRICULUM_HUMAN_MD, e)

    lessons = {}
    hashes = {}
    for entry in curriculum.get("lessons", []) or []:
        if isinstance(entry, dict) and entry.get("lesson_id"):
            lessons[entry["lesson_id"]] = entry
            hashes[entry["lesson_id"]] = lesson_fingerprint(entry)

    v2_hashes = {}
    v2_machine = None
    for rel in V2_FILES:
        try:
            blob = _read_bytes(v2_root, rel)
        except OSError as e:
            return None, "cannot read V2 file %s: %s" % (rel, e)
        v2_hashes[rel] = _sha256_hex(blob)
        if rel == V2_MACHINE_JSON:
            try:
                v2_machine = json.loads(blob.decode("utf-8"))
            except (ValueError, UnicodeDecodeError) as e:
                return None, "V2 machine twin is not valid JSON: %s" % e

    return {"lessons": lessons, "lesson_hashes": hashes,
            "curriculum": curriculum, "human_md": human_md,
            "v2_hashes": v2_hashes, "v2_machine": v2_machine}, ""


# ---------------------------------------------------------------------------
# Pure predicates — no I/O
# ---------------------------------------------------------------------------

def check_canonical_integrity(canonical):
    """The checklist itself is intact: 14 lessons, fields, pins, twin
    consistency, V2 present and current. Returns violations list."""
    v = []
    curriculum = canonical["curriculum"]
    lessons = canonical["lessons"]

    # --- curriculum shape ---
    if curriculum.get("mandatory") is not True:
        v.append("CURRICULUM_NOT_MANDATORY: thinking curriculum is not "
                 "flagged mandatory — the gate has nothing to enforce")
    min_score = (curriculum.get("pass_policy") or {}).get("per_lesson_minimum")
    if not isinstance(min_score, (int, float)) or min_score < 7:
        v.append("CURRICULUM_PASS_POLICY_WEAK: per-lesson minimum is %r, "
                 "expected >= 7" % (min_score,))

    got_ids = set(lessons)
    for fake in sorted(got_ids - EXPECTED_LESSON_IDS):
        v.append("CURRICULUM_UNKNOWN_LESSON: %r is not one of the 14 "
                 "canonical lesson ids" % fake)
    for missing in sorted(EXPECTED_LESSON_IDS - got_ids):
        v.append("CURRICULUM_LESSON_MISSING: canonical lesson %s absent "
                 "from the curriculum" % missing)

    # --- per-lesson structure + pin match (drift = deliberate re-pin) ---
    for lid in sorted(EXPECTED_LESSON_IDS & got_ids):
        lesson = lessons[lid]
        for field in REQUIRED_LESSON_FIELDS:
            if field not in lesson or lesson[field] in (None, "", [], {}):
                v.append("CURRICULUM_LESSON_INCOMPLETE: %s missing %r"
                         % (lid, field))
        if not LESSON_ID_RE.match(str(lesson.get("lesson_id", ""))):
            v.append("CURRICULUM_LESSON_ID_MALFORMED: %r" % (lid,))
        want = CURRICULUM_LESSON_PINS.get(lid, "")
        got = canonical["lesson_hashes"].get(lid, "")
        if not want or got.lower() != want.lower():
            v.append("CURRICULUM_STALE: lesson %s bytes differ from the "
                     "pinned fingerprint (pin source: %s) — re-pin "
                     "deliberately or restore canonical bytes"
                     % (lid, CURRICULUM_PIN_SOURCE))

    # --- human/machine twin consistency ---
    md_ids = set(HUMAN_LESSON_HEADER_RE.findall(canonical["human_md"]))
    for missing in sorted(EXPECTED_LESSON_IDS - md_ids):
        v.append("TWIN_DIVERGED: human curriculum doc does not enumerate "
                 "lesson %s" % missing)

    # --- V2 presence, currency, machine-twin validity ---
    for rel in V2_FILES:
        want = V2_FILE_PINS.get(rel, "")
        got = canonical["v2_hashes"].get(rel, "")
        if not got:
            v.append("V2_MISSING: %s absent" % rel)
        elif not want or got.lower() != want.lower():
            v.append("V2_STALE: %s bytes differ from the pinned V2 "
                     "fingerprint (pin source: %s)" % (rel, V2_PIN_SOURCE))
    machine = canonical.get("v2_machine")
    if not isinstance(machine, dict) or machine.get("id") != "OPERATING-CODE-V2":
        v.append("V2_MACHINE_TWIN_INVALID: machine.json does not identify "
                 "as OPERATING-CODE-V2")
    return v


def check_claim(canonical, claim):
    """An agent's activation checklist claim vs canonical bytes.

    claim = {"lessons": [{"lesson_id", "sha256"}], "v2": {rel_path: sha256}}
    The claim is UNTRUSTED input: ids must be canonical, hashes must equal
    recomputed canonical bytes. Returns violations list."""
    v = []
    if not isinstance(claim, dict):
        return ["CLAIM_MALFORMED: checklist claim is not an object"]

    entries = claim.get("lessons")
    if not isinstance(entries, list):
        return ["CLAIM_MALFORMED: claim.lessons must be a list"]
    seen = {}
    for i, e in enumerate(entries):
        if not isinstance(e, dict):
            v.append("CLAIM_MALFORMED: lessons entry %d not an object" % i)
            continue
        lid = e.get("lesson_id")
        if not isinstance(lid, str) or not LESSON_ID_RE.match(lid):
            v.append("LESSON_NOT_REGISTERED: entry %d lesson_id %r is not "
                     "a canonical lesson id" % (i, lid))
            continue
        if lid in seen:
            v.append("LESSON_DUPLICATE: %s claimed twice (counting twice "
                     "is not loading twice)" % lid)
            continue
        seen[lid] = e
        if lid not in EXPECTED_LESSON_IDS:
            v.append("LESSON_NOT_REGISTERED: %r is not one of the 14 "
                     "canonical lessons" % lid)
            continue
        want = canonical["lesson_hashes"].get(lid, "")
        got = e.get("sha256", "")
        if not isinstance(got, str) or not SHA64_RE.match(got):
            v.append("LESSON_FINGERPRINT_MALFORMED: %s sha256 not 64-hex" % lid)
        elif got.lower() != want.lower():
            v.append("LESSON_FINGERPRINT_MISMATCH: %s claim does not match "
                     "canonical lesson bytes (forged or stale content)" % lid)
    for missing in sorted(EXPECTED_LESSON_IDS - set(seen)):
        v.append("LESSON_MISSING: %s not in the checklist — partial "
                 "loading is not activation" % missing)

    v2claim = claim.get("v2")
    if not isinstance(v2claim, dict):
        v.append("CLAIM_MALFORMED: claim.v2 must be an object of "
                 "{rel_path: sha256}")
    else:
        for rel in V2_FILES:
            want = canonical["v2_hashes"].get(rel, "")
            got = v2claim.get(rel, "")
            if not isinstance(got, str) or not SHA64_RE.match(got):
                v.append("V2_FINGERPRINT_MALFORMED: %s" % rel)
            elif got.lower() != want.lower():
                v.append("V2_STALE: claimed V2 fingerprint for %s does not "
                         "match current V2 bytes" % rel)
    return v


def check_checklist(canonical, claim=None):
    """Full Gate-1 predicate. canonical from load_canonical(); claim None =
    self-audit only. Returns (verdict, violations)."""
    violations = check_canonical_integrity(canonical)
    if claim is not None:
        violations = violations + check_claim(canonical, claim)
    if violations:
        return "REJECT", violations
    return "CHECKLIST-VERIFIED", []


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _default_repo_root():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(here)  # tools/ -> repo root


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Gate 1 — Activation Checklist Verifier: machine-verify "
                    "all 14 thinking lessons + Operating Code V2. Fail closed.")
    ap.add_argument("--repo-root", default=_default_repo_root(),
                    help="checkout holding NAYA-ACTIVATION/ (default: repo "
                         "root above tools/)")
    ap.add_argument("--v2-root", default="",
                    help="checkout holding the V2 files (default: --repo-root). "
                         "Point at the operating-code-v2 branch checkout "
                         "until PR #2087 merges.")
    ap.add_argument("--checklist", default="",
                    help="agent activation checklist claim JSON to verify "
                         "(default: self-audit of canonical artifacts only)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    canonical, err = load_canonical(args.repo_root,
                                    args.v2_root or args.repo_root)
    if canonical is None:
        return _emit("TOOL-ERROR", [err], args, 2)

    claim = None
    if args.checklist:
        try:
            with open(args.checklist, encoding="utf-8") as f:
                claim = json.load(f)
        except (OSError, ValueError) as e:
            return _emit("TOOL-ERROR",
                         ["cannot read checklist claim: %s" % e], args, 2)

    verdict, violations = check_checklist(canonical, claim)
    return _emit(verdict, violations, args, 0 if verdict == "CHECKLIST-VERIFIED" else 1)


def _emit(verdict, violations, args, code):
    if args.json:
        print(json.dumps({"verdict": verdict, "violations": violations,
                          "gate": "activation-checklist-v1",
                          "curriculum_pin_source": CURRICULUM_PIN_SOURCE,
                          "v2_pin_source": V2_PIN_SOURCE}))
    else:
        print("%s: %s" % (verdict,
                          "; ".join(violations) if violations else "ok"))
    return code


if __name__ == "__main__":
    sys.exit(main())
