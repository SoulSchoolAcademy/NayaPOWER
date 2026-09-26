"""Deterministic integrity auditor for the NayaPOWER contract library.

PURPOSE
The contract stack is only governing if it is enforceable. A registry written in
prose is an assertion. This module is the machine-checkable substrate that proves
structural claims about the library from the repository itself, so a cold Naya
does not have to infer which artifact governs.

It answers, deterministically:
  1. Do two artifacts share a contract NAME but diverge in content?
  2. Do two artifacts claim the same contract ID in the same scope?
  3. Are declared specialized boundaries actually ratified?
  4. Are stubs being mistaken for normative contracts?
  5. Is a governed noun defined in more than one place? (operating law S6)
  6. Is library-wide authority ambiguous between top-level documents?
  7. Which contract artifacts are never referenced by the library's own index?

It deliberately does NOT choose a winner, delete anything, or rewrite contract
content. Reconciliation is an authority decision under operating law S13.

BASELINE MODEL
The library already carries known defects. A gate that fails on merge would block
every unrelated pull request, and silently passing would hide the debt. So each
finding is reduced to a stable fingerprint and compared against a recorded
baseline:
  - finding NOT in baseline  -> NEW_DRIFT   -> non-zero exit (gate fails)
  - finding IN baseline      -> KNOWN_DEBT  -> reported, does not fail
Debt therefore cannot grow silently, and clearing the baseline becomes a visible,
reviewable act rather than an accident.

Run:  python -B .naya/runtime/contract_library_integrity.py
      python -B .naya/runtime/contract_library_integrity.py --json
Exit: 0 = no new drift, 1 = new drift detected, 2 = audit could not run.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CONTRACTS = REPO / ".naya" / "contracts"
BASELINE = CONTRACTS / "CONTRACT-LIBRARY-INTEGRITY-BASELINE.json"
REPORT = REPO / ".naya" / "contract-library-integrity-report.json"

CONTRACT_SUFFIXES = {".md", ".json"}
NORMATIVE_MARKERS = ("MUST", "MUST NOT", "SHALL", "SHALL NOT", "REQUIRED")
STUB_MAX_BYTES = 1024

# Operating law S6 "exact-noun law": these must not be collapsed into each other.
# A noun defined by more than one artifact is not automatically wrong, but it is
# unresolvable without an authority decision, so it must be visible.
GOVERNED_NOUNS: dict[str, tuple[str, ...]] = {
    "SMART_LINK": ("SMART-LINK", "SMART_LINK"),
    "INTELLIGENT_BLOCK": ("INTELLIGENT-BLOCK", "INTELLIGENT_BLOCK"),
    "MEMBER_LEVEL": ("MEMBER-LEVEL-CONTRACT", "MEMBER_LEVEL"),
    "SMART_LEDGER_EVENT": ("SMART-LEDGER-EVENT", "SMART_LEDGER_EVENT"),
    "VALUE_EVENT": ("VALUE-EVENT", "VALUE_EVENT"),
    "VERIFICATION_RECEIPT": ("VERIFICATION-RECEIPT", "VERIFICATION_RECEIPT"),
}

# Documents that assert library-wide authority make precedence ambiguous if >1.
AUTHORITY_CLAIM_MARKERS = (
    "all contracts in",
    "governs this library",
    "supreme governing",
    "constitutional law",
    "precedence",
)

ID_PREFIX_RE = re.compile(r"^(\d{2})-")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO).as_posix()
    except ValueError:
        # Auditing a tree outside the repo (e.g. a test fixture) is supported.
        return path.as_posix()


def contract_files(root: Path | None = None) -> list[Path]:
    base = root or CONTRACTS
    if not base.is_dir():
        return []
    return [
        p
        for p in sorted(base.rglob("*"))
        if p.is_file() and p.suffix.lower() in CONTRACT_SUFFIXES
    ]


def finding(kind: str, detail: str, locations: list[str], severity: str = "ERROR") -> dict:
    """Build a finding with a stable fingerprint.

    The fingerprint deliberately excludes file CONTENT hashes so that editing a
    contract does not silently reset its debt record, but includes the location
    set so that moving or adding a conflicting artifact is treated as new drift.
    """
    locs = sorted(set(locations))
    digest = hashlib.sha256(
        (kind + "|" + "|".join(locs)).encode("utf-8")
    ).hexdigest()[:16]
    return {
        "kind": kind,
        "severity": severity,
        "fingerprint": digest,
        "locations": locs,
        "detail": detail,
    }


def check_same_name_divergent_content(files: list[Path]) -> list[dict]:
    """Two artifacts, one contract name, different bytes."""
    by_stem: dict[str, list[Path]] = defaultdict(list)
    for p in files:
        # Per-directory README.md files are navigational indexes, one per boundary
        # by design. They are not competing definitions of a contract named "README".
        if p.name == "README.md":
            continue
        by_stem[p.stem].append(p)
    out: list[dict] = []
    for stem, group in sorted(by_stem.items()):
        if len(group) < 2:
            continue
        hashes = {_sha256(p) for p in group}
        locs = [_rel(p) for p in group]
        if len(hashes) > 1:
            out.append(
                finding(
                    "SAME_NAME_DIVERGENT_CONTENT",
                    f"contract name {stem!r} is defined by {len(group)} artifacts with "
                    f"{len(hashes)} distinct contents; no canonical copy is designated",
                    locs,
                )
            )
        else:
            out.append(
                finding(
                    "SAME_NAME_DUPLICATE_COPY",
                    f"contract name {stem!r} has {len(group)} byte-identical copies; "
                    "one should be designated canonical",
                    locs,
                    severity="WARN",
                )
            )
    return out


def check_id_collisions(files: list[Path]) -> list[dict]:
    """Two artifacts claiming the same NN- contract id in the same directory."""
    out: list[dict] = []
    by_dir: dict[Path, list[Path]] = defaultdict(list)
    for p in files:
        by_dir[p.parent].append(p)
    for directory, group in sorted(by_dir.items()):
        by_prefix: dict[str, list[Path]] = defaultdict(list)
        for p in group:
            m = ID_PREFIX_RE.match(p.name)
            if m:
                by_prefix[m.group(1)].append(p)
        for prefix, colliding in sorted(by_prefix.items()):
            if len(colliding) > 1:
                out.append(
                    finding(
                        "CONTRACT_ID_COLLISION",
                        f"contract id {prefix}- is claimed by {len(colliding)} artifacts in "
                        f"{_rel(directory)}",
                        [_rel(p) for p in colliding],
                    )
                )
    return out


def check_unratified_boundaries(root: Path) -> list[dict]:
    """A declared boundary directory that contains no actual contract."""
    out: list[dict] = []
    if not root.is_dir():
        return out
    for d in sorted(p for p in root.iterdir() if p.is_dir()):
        contents = [p for p in d.rglob("*") if p.is_file() and p.name != "README.md"]
        if not contents:
            readme = d / "README.md"
            out.append(
                finding(
                    "UNRATIFIED_BOUNDARY",
                    f"boundary {d.name}/ declares itself in README.md but contains no "
                    "substantive contract; every Naya resolving this boundary finds nothing",
                    [_rel(readme)] if readme.is_file() else [_rel(d) + "/"],
                )
            )
    return out


def check_stub_contracts(files: list[Path]) -> list[dict]:
    """Small non-README markdown with no normative language is not a contract."""
    out: list[dict] = []
    for p in files:
        if p.suffix.lower() != ".md" or p.name == "README.md":
            continue
        if p.stat().st_size >= STUB_MAX_BYTES:
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        if any(marker in text for marker in NORMATIVE_MARKERS):
            continue
        out.append(
            finding(
                "STUB_NOT_NORMATIVE",
                f"{_rel(p)} is {p.stat().st_size} B and contains no MUST/SHALL language; "
                "it cannot govern behavior and should not be cited as a contract",
                [_rel(p)],
                severity="WARN",
            )
        )
    return out


def check_multi_defined_nouns(files: list[Path]) -> list[dict]:
    """A governed noun defined by more than one artifact."""
    out: list[dict] = []
    for noun, tokens in sorted(GOVERNED_NOUNS.items()):
        matches = [p for p in files if any(tok in p.name.upper() for tok in tokens)]
        if len(matches) > 1:
            out.append(
                finding(
                    "MULTI_DEFINED_NOUN",
                    f"governed noun {noun} is defined by {len(matches)} artifacts; "
                    "operating law S6 forbids silent collapse, so an authority decision is required",
                    [_rel(p) for p in matches],
                )
            )
    return out


def check_authority_ambiguity(files: list[Path], root: Path) -> list[dict]:
    """More than one top-level document claiming library-wide authority."""
    claimants: list[Path] = []
    for p in files:
        if p.parent != root or p.suffix.lower() != ".md":
            continue
        text = p.read_text(encoding="utf-8", errors="replace").lower()
        if any(marker in text for marker in AUTHORITY_CLAIM_MARKERS):
            claimants.append(p)
    if len(claimants) > 1:
        out = [
            finding(
                "AUTHORITY_AMBIGUITY",
                f"{len(claimants)} top-level documents assert library-wide authority; "
                "precedence between them is not machine-decidable",
                [_rel(p) for p in claimants],
            )
        ]
        return out
    return []


def check_unreferenced(files: list[Path], root: Path) -> list[dict]:
    """Contract artifacts never mentioned by the library index or a registry."""
    index_texts: list[str] = []
    for candidate in ("README.md",):
        p = root / candidate
        if p.is_file():
            index_texts.append(p.read_text(encoding="utf-8", errors="replace"))
    for p in files:
        if "REGISTRY" in p.stem.upper() and p.suffix.lower() == ".md":
            index_texts.append(p.read_text(encoding="utf-8", errors="replace"))
    if not index_texts:
        return []
    blob = "\n".join(index_texts)
    out: list[dict] = []
    for p in files:
        if p.name == "README.md" or "REGISTRY" in p.stem.upper():
            continue
        # This auditor's own baseline is a machine artifact, not a contract, and
        # it must not list itself as undiscovered governance debt.
        if p.name == BASELINE.name:
            continue
        if p.name not in blob:
            out.append(
                finding(
                    "UNREFERENCED_CONTRACT",
                    f"{_rel(p)} is not named by the library index or any registry, so no "
                    "cold Naya would discover it as governing",
                    [_rel(p)],
                    severity="WARN",
                )
            )
    return out


def audit(root: Path | None = None) -> dict:
    base = root or CONTRACTS
    files = contract_files(base)
    if not files:
        raise RuntimeError(f"contract library not found at {base}")
    findings: list[dict] = []
    findings += check_same_name_divergent_content(files)
    findings += check_id_collisions(files)
    findings += check_unratified_boundaries(base)
    findings += check_stub_contracts(files)
    findings += check_multi_defined_nouns(files)
    findings += check_authority_ambiguity(files, base)
    findings += check_unreferenced(files, base)
    findings.sort(key=lambda f: (f["kind"], f["fingerprint"]))
    return {
        "contract_root": _rel(base),
        "contract_file_count": len(files),
        "findings": findings,
    }


def load_baseline() -> set[str]:
    if not BASELINE.is_file():
        return set()
    try:
        data = json.loads(BASELINE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return set()
    return {entry["fingerprint"] for entry in data.get("known_findings", [])}


def render(report: dict, baseline: set[str]) -> tuple[int, str]:
    lines: list[str] = []
    new_drift: list[dict] = []
    known: list[dict] = []
    for f in report["findings"]:
        (known if f["fingerprint"] in baseline else new_drift).append(f)

    lines.append(f"contract library: {_rel(CONTRACTS)}")
    lines.append(f"contract artifacts scanned: {report['contract_file_count']}")
    lines.append("")
    if known:
        lines.append(f"KNOWN DEBT (recorded in baseline, not failing): {len(known)}")
        for f in known:
            lines.append(f"  [KNOWN] {f['kind']}")
            lines.append(f"          {f['detail']}")
            for loc in f["locations"]:
                lines.append(f"          - {loc}")
        lines.append("")
    if new_drift:
        lines.append(f"NEW DRIFT (not in baseline, gate fails): {len(new_drift)}")
        for f in new_drift:
            lines.append(f"  [DRIFT] {f['kind']}  severity={f['severity']}")
            lines.append(f"          {f['detail']}")
            for loc in f["locations"]:
                lines.append(f"          - {loc}")
        lines.append("")
    if not new_drift:
        lines.append("CONTRACT_LIBRARY_NO_NEW_DRIFT")
    else:
        lines.append("CONTRACT_LIBRARY_NEW_DRIFT")
    return (1 if new_drift else 0), "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true", help="write the machine-readable report")
    ap.add_argument(
        "--update-baseline",
        action="store_true",
        help="record current findings as known debt (an explicit, reviewable act)",
    )
    ap.add_argument("root", nargs="?", help="contract root directory to audit")
    args = ap.parse_args()

    try:
        base = Path(args.root).resolve() if args.root else CONTRACTS
        report = audit(base)
    except RuntimeError as exc:
        print(f"AUDIT_COULD_NOT_RUN: {exc}")
        return 2

    if args.update_baseline:
        payload = {
            "purpose": (
                "Known structural debt in the contract library at a point in time. "
                "This is NOT an assertion that these findings are correct or accepted "
                "semantics; it is a record so the gate blocks NEW drift while the "
                "reconciliation decision stays with the director."
            ),
            "contract_root": report["contract_root"],
            "known_findings": [
                {
                    "fingerprint": f["fingerprint"],
                    "kind": f["kind"],
                    "severity": f["severity"],
                    "locations": f["locations"],
                    "detail": f["detail"],
                }
                for f in report["findings"]
            ],
        }
        BASELINE.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        print(f"BASELINE_UPDATED: {BASELINE.relative_to(REPO).as_posix()} "
              f"({len(report['findings'])} findings recorded)")

    baseline = load_baseline()
    code, text = render(report, baseline)
    print(text)

    if args.json:
        known = {f["fingerprint"] for f in report["findings"]} & baseline
        report["known_debt"] = sorted(known)
        report["new_drift"] = sorted(
            f["fingerprint"] for f in report["findings"] if f["fingerprint"] not in baseline
        )
        REPORT.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        print(f"report written: {_rel(REPORT)}")
    return code


if __name__ == "__main__":
    sys.exit(main())
