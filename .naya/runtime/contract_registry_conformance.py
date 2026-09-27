"""Deterministic conformance auditor for the CANONICAL CONTRACT REGISTRY itself.

PURPOSE
`.naya/control-plane/CANONICAL-CONTRACT-REGISTRY.md` is the map a cold Naya is
supposed to read to learn which contract governs what. At the moment it is prose.
Prose cannot fail, so it cannot govern.

This module makes the registry's own claims checkable against the repository. It
answers, deterministically and only from repository evidence:

  1. Are all six constitutional truth-model equations still present in the
     constitutional law?            (always enforced, never baselined)
  2. Does every artifact path the registry cites actually exist?
  3. Is every registry status drawn from one evidence-bound vocabulary?
  4. When the registry claims an acceptance test, does that test exist AND run in
     a workflow?  A contract is not complete because a file exists.
  5. Does the registry ever understate reality, by calling something UNPROVEN
     while a real implementation and a routed gate already exist?
  6. Does any artifact claim RATIFIED without a recorded human ratification?
  7. Can a cold Naya actually reach the registry from the canonical boot path?
  8. Does the contract library index still describe the actual tree?

SCOPE / NON-DUPLICATION
`.naya/runtime/contract_library_integrity.py` audits the *structure of the
contract library* (duplicate nouns, ID collisions, unreferenced contracts,
authority ambiguity) against a recorded baseline. This module audits the
*registry's claims about the world*. They are different questions and neither
substitutes for the other.

FAIL-CLOSED BASELINE MODEL
Matching the existing integrity gate, known debt is reduced to a stable
fingerprint and compared against `.naya/contracts/CONTRACT-REGISTRY-CONFORMANCE-BASELINE.json`:
  finding NOT in baseline -> NEW_DRIFT  -> exit 1 (gate fails)
  finding IN baseline     -> KNOWN_DEBT -> reported, does not fail
The report never claims conformance while debt exists. It reports
`conforming: false` until every finding is cleared, so the gate cannot be
mistaken for a green light on the contract system.

Run:  python -B .naya/runtime/contract_registry_conformance.py
      python -B .naya/runtime/contract_registry_conformance.py --json
Exit: 0 = no new drift, 1 = new drift, 2 = audit could not run.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

REPO_DEFAULT = Path(__file__).resolve().parents[2]

REGISTRY_RELPATH = ".naya/control-plane/CANONICAL-CONTRACT-REGISTRY.md"
CONSTITUTION_RELPATH = ".naya/contracts/00-NAYANET-CONSTITUTIONAL-CONTRACT-LAW.md"
LIBRARY_INDEX_RELPATH = ".naya/contracts/README.md"
BASELINE_RELPATH = ".naya/contract-registry-conformance-baseline.json"
REPORT_RELPATH = ".naya/contract-registry-conformance-report.json"

# Constitutional law section 6, "The following equations are mandatory".
CONSTITUTIONAL_EQUATIONS: tuple[str, ...] = (
    "UNKNOWN \u2260 PASS",
    "BLOCKED \u2260 PASS",
    "IMPLEMENTED \u2260 VERIFIED",
    "VERIFIED \u2260 PRODUCTION-PROVEN",
    "LEARNING LABEL \u2260 VERIFIED LEARNING",
    "DOCUMENT EXISTS \u2260 INTELLIGENCE PROVEN",
)

# Constitutional law section 6 state list. MISSING is deliberately absent upstream;
# its absence is itself a finding, not something this gate silently repairs.
CONSTITUTIONAL_STATES: tuple[str, ...] = (
    "UNKNOWN",
    "PROPOSED",
    "PENDING",
    "IMPLEMENTED",
    "TESTED",
    "VERIFIED",
    "PRODUCTION-PROVEN",
    "LEARNED",
    "COMPOUNDED",
)
STATES_THE_SYSTEM_MUST_BE_ABLE_TO_DISTINGUISH: tuple[str, ...] = (
    "VERIFIED",
    "PENDING",
    "MISSING",
    "CONFLICTED",
    "UNKNOWN",
)

# Evidence-bound registry status vocabulary.
STATUS_VOCABULARY: frozenset[str] = frozenset(
    {
        "PARTIAL",
        "UNPROVEN",
        "PROVEN",
        "VERIFIED",
        "CANONICAL",
        "RATIFIED",
        "PROPOSED",
        "MISSING",
        "CONFLICTED",
        "BLOCKED",
        "UNKNOWN",
        "HISTORICAL",
    }
)

# Files that constitute the canonical cold-Naya boot path.
BOOT_PATHS: tuple[str, ...] = (
    "SUPERBRAIN/AI-BOOT/START-HERE.md",
    ".naya/TEAM-NAYA/00-START-HERE-FOR-EVERY-NAYA.md",
    ".naya/contracts/README.md",
)

# Registry entries that are known to UNDERSTATE reality: the registry says no
# implementation exists while a real implementation and a routed gate already do.
# Declared as data, verified at runtime, so fixing either side clears the finding.
UNPROVEN_CLAIM_CONTRADICTIONS: tuple[dict, ...] = (
    {
        "entry": "CC-017",
        "claim": "no implementation",
        "implementation": ".naya/runtime/portable_authorization.py",
        "gate": ".github/workflows/verify-stream-b-cross-process-intelligence-authorization.yml",
    },
)

RATIFIED_CLAIM_RE = re.compile(r"\*\*Status:?\*\*:?\s*RATIFIED|\bStatus\b[^\n]{0,40}\bRATIFIED\b", re.IGNORECASE)
TEST_LIKE_PREFIXES = ("tests/", "tools/", ".naya/tests/", "test/")
REGISTRY_ENTRY_RE = re.compile(r"^###\s+(CC-\d{3})[::]\s*(.+?)\s*$", re.MULTILINE)
CELL_RE = re.compile(r"^\|\s*\*\*(?P<key>[^*|]+)\*\*\s*\|(?P<value>.*?)\|\s*$", re.MULTILINE)
PATH_RE = re.compile(r"`([A-Za-z0-9_./-]+\.(?:md|json|py|ts|tsx|yml|yaml|sql|html))`")
WORKFLOWS_RELPATH = ".github/workflows"


class AuditError(RuntimeError):
    """The audit could not be performed; the gate must not pass on absence of evidence."""


def _finding(code: str, severity: str, subject: str, detail: str) -> dict:
    # Some findings carry a volatile magnitude (how many artifacts are unindexed).
    # The magnitude is reported but excluded from the fingerprint, so ordinary growth
    # of known debt is visible without failing the gate on every legitimate addition.
    # A change in WHICH defect exists is still new drift.
    fingerprint_detail = detail.split("|")[0]
    fingerprint = hashlib.sha256(
        "|".join((code, severity, subject, fingerprint_detail)).encode("utf-8")
    ).hexdigest()[:16]
    return {
        "code": code,
        "severity": severity,
        "subject": subject,
        "detail": detail,
        "fingerprint": fingerprint,
    }


def path_exists(root: Path, relpath: str) -> bool:
    return (root / relpath.strip().strip("/")).is_file()


def read_text(root: Path, relpath: str) -> str:
    target = root / relpath
    if not target.is_file():
        raise AuditError(f"required source missing: {relpath}")
    return target.read_text(encoding="utf-8", errors="replace")


def constitutional_equations_missing(law_text: str) -> list[str]:
    normalized = re.sub(r"\s+", " ", law_text)
    return [eq for eq in CONSTITUTIONAL_EQUATIONS if eq not in normalized]


def truth_model_section(law_text: str) -> str:
    """Return the constitutional Truth Model section, not the whole document.

    Scoping matters: a state named somewhere else in a 900-line law does not make
    the state definable at truth-model level.
    """
    start = re.search(r"^##\s*\d*\.?\s*Truth Model\s*$", law_text, re.MULTILINE | re.IGNORECASE)
    if not start:
        return ""
    rest = law_text[start.end() :]
    end = re.search(r"^##\s", rest, re.MULTILINE)
    return rest[: end.start()] if end else rest


def ratification_record_for(root: Path, artifact_relpath: str, text: str) -> str | None:
    """Return a recorded human ratification artifact, or None.

    A contract may only claim RATIFIED when a distinct ratification record exists.
    Self-assertion inside the contract itself is never sufficient.
    """
    if not RATIFIED_CLAIM_RE.search(text):
        return None
    candidate = artifact_relpath.replace(".md", "") + ".RATIFICATION.md"
    ratification = root / candidate
    if ratification.is_file():
        return candidate
    ratifications = root / ".naya" / "ratifications"
    if ratifications.is_dir():
        stem = Path(artifact_relpath).stem
        for record in sorted(ratifications.glob("*.md")):
            if stem in record.read_text(encoding="utf-8", errors="replace"):
                return str(record.relative_to(root)).replace("\\", "/")
    return None


def workflow_corpus(root: Path) -> str:
    directory = root / WORKFLOWS_RELPATH
    if not directory.is_dir():
        return ""
    parts = []
    for workflow in sorted(directory.glob("*.yml")) + sorted(directory.glob("*.yaml")):
        parts.append(workflow.read_text(encoding="utf-8", errors="replace"))
    return "\n".join(parts)


def is_routed(root: Path, test_relpath: str) -> bool:
    """True when some workflow actually references this test/script path."""
    if not test_relpath:
        return False
    needle = Path(test_relpath).as_posix()
    return needle in workflow_corpus(root)


def parse_registry(registry_text: str) -> list[dict]:
    entries: list[dict] = []
    matches = list(REGISTRY_ENTRY_RE.finditer(registry_text))
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(registry_text)
        body = registry_text[start:end]
        cells = {m.group("key").strip().lower(): m.group("value").strip() for m in CELL_RE.finditer(body)}
        status_raw = cells.get("status", "")
        status_match = re.search(r"\*\*([A-Z\-]+)\*\*", status_raw)
        entries.append(
            {
                "id": match.group(1),
                "name": match.group(2).strip(),
                "status": status_match.group(1) if status_match else "",
                "status_text": status_raw,
                "acceptance_text": cells.get("acceptance", ""),
                "body_text": body,
                "paths": sorted({m.group(1) for m in PATH_RE.finditer(body)}),
                "claims_no_implementation": bool(
                    re.search(
                        r"no implementation|not wired|contract only|unproven",
                        body,
                        re.IGNORECASE,
                    )
                ),
            }
        )
    return entries


def implementation_signals(root: Path) -> set[str]:
    """Runtime + test artifacts that constitute real, existing implementation."""
    signals: set[str] = set()
    for base in (root / ".naya" / "runtime", root / "tests", root / "tools", root / "supabase" / "functions"):
        if not base.is_dir():
            continue
        for path in base.rglob("*.py"):
            signals.add(str(path.relative_to(root)).replace("\\", "/"))
    return signals


def audit(root: Path = REPO_DEFAULT) -> dict:
    root = Path(root)
    try:
        registry_text = read_text(root, REGISTRY_RELPATH)
        law_text = read_text(root, CONSTITUTION_RELPATH)
        library_index = read_text(root, LIBRARY_INDEX_RELPATH)
    except AuditError as exc:
        raise AuditError(str(exc)) from exc

    findings: list[dict] = []
    entries = parse_registry(registry_text)
    truth_section = truth_model_section(law_text)

    if not truth_section:
        findings.append(
            _finding(
                "TRUTH_MODEL_SECTION_MISSING",
                "ERROR",
                CONSTITUTION_RELPATH,
                "the constitutional Truth Model section could not be located; the required "
                "state set cannot be verified",
            )
        )

    # 1. Constitutional truth model is always enforced and never baselined.
    for equation in constitutional_equations_missing(law_text):
        findings.append(
            _finding(
                "CONSTITUTIONAL_EQUATION_MISSING",
                "ERROR",
                equation,
                "mandatory truth-model equation absent from the constitutional law",
            )
        )

    # 8. The library index must still describe the tree.
    contracts_dir = root / ".naya" / "contracts"
    tree_files = sorted(
        str(p.relative_to(root)).replace("\\", "/")
        for p in contracts_dir.rglob("*")
        if p.is_file()
        and p.suffix in {".md", ".json"}
        # This gate's own audit artifacts are not library contracts; counting them
        # would make the library index permanently self-contradicting.
        and p.name != Path(BASELINE_RELPATH).name
    )
    unindexed = [p for p in tree_files if Path(p).name not in library_index]
    if unindexed:
        names = ", ".join(Path(p).name for p in unindexed[:4])
        findings.append(
            _finding(
                "LIBRARY_INDEX_LAGS_TREE",
                "WARN",
                LIBRARY_INDEX_RELPATH,
                f"{len(unindexed)} contract artifact(s) absent from the library index"
                f" | examples: {names}",
            )
        )

    # 7. Reachability from the canonical cold-Naya boot path.
    boot_hits = [p for p in BOOT_PATHS if path_exists(root, p) and REGISTRY_RELPATH.split("/")[-1] in read_text(root, p)]
    if not boot_hits:
        findings.append(
            _finding(
                "REGISTRY_UNREACHABLE_FROM_BOOT",
                "ERROR",
                REGISTRY_RELPATH,
                "no canonical boot path references the registry; a cold Naya following "
                "the mandatory boot sequence cannot discover it",
            )
        )

    signals = implementation_signals(root)
    cited_paths_checked = 0

    for entry in entries:
        entry_id = entry["id"]
        test_like = [p for p in entry["paths"] if p.startswith(TEST_LIKE_PREFIXES)]

        # 4a. An acceptance claim with no executable acceptance path at all.
        if entry["acceptance_text"] and not test_like:
            findings.append(
                _finding(
                    "ACCEPTANCE_CLAIM_UNENFORCED",
                    "WARN",
                    entry_id,
                    "entry defines acceptance criteria but cites no executable acceptance "
                    "artifact, so the criteria cannot be checked by any gate",
                )
            )

        # 3. One evidence-bound status vocabulary.
        if entry["status"] and entry["status"] not in STATUS_VOCABULARY:
            findings.append(
                _finding(
                    "REGISTRY_STATUS_VOCABULARY",
                    "ERROR",
                    entry_id,
                    f"status {entry['status']!r} is outside the evidence-bound vocabulary",
                )
            )

        for relpath in entry["paths"]:
            cited_paths_checked += 1

            # 2. Cited paths must exist. A registry that cites a phantom artifact
            #    is worse than one that cites nothing.
            if not path_exists(root, relpath):
                findings.append(
                    _finding(
                        "CITED_PATH_MISSING",
                        "ERROR",
                        relpath,
                        f"{entry_id} cites an artifact that does not exist in the repository",
                    )
                )
                continue

            # 4b. An acceptance test that exists but is never run is not enforcement.
            if relpath in test_like and not is_routed(root, relpath):
                findings.append(
                    _finding(
                        "ACCEPTANCE_CLAIM_UNENFORCED",
                        "WARN",
                        relpath,
                        f"{entry_id} cites this acceptance test but no workflow runs it",
                    )
                )

            # 6. RATIFIED requires a recorded human ratification artifact.
            if relpath.endswith(".md") and relpath.startswith(".naya/contracts/"):
                text = read_text(root, relpath)
                if ratification_record_for(root, relpath, text) is None:
                    findings.append(
                        _finding(
                            "RATIFICATION_UNPROVEN",
                            "ERROR",
                            relpath,
                            "artifact claims RATIFIED with no separate recorded human "
                            "ratification record; technical proof is not ratification",
                        )
                    )

        # 5. The registry must not understate real implementation.
        for declared in UNPROVEN_CLAIM_CONTRADICTIONS:
            if declared["entry"] != entry_id or not entry["claims_no_implementation"]:
                continue
            implementation_exists = path_exists(root, declared["implementation"])
            gate_exists = path_exists(root, declared["gate"])
            if implementation_exists and gate_exists:
                findings.append(
                    _finding(
                        "UNPROVEN_CLAIM_CONTRADICTED",
                        "ERROR",
                        entry_id,
                        f"registry states '{declared['claim']}' while {declared['implementation']} "
                        f"exists and {declared['gate']} runs it",
                    )
                )

    # 5c. Declared contradictions are checked even if the entry text drifts, so a
    #     silent softening of the claim cannot hide the contradiction.
    for declared in UNPROVEN_CLAIM_CONTRADICTIONS:
        entry = next((e for e in entries if e["id"] == declared["entry"]), None)
        if entry is None:
            continue
        if (
            path_exists(root, declared["implementation"])
            and path_exists(root, declared["gate"])
            and not entry["claims_no_implementation"]
            and "UNPROVEN" not in entry["status"].upper()
        ):
            findings.append(
                _finding(
                    "UNPROVEN_CLAIM_CONTRADICTED",
                    "ERROR",
                    declared["entry"],
                    f"registry no longer records the contradiction with {declared['implementation']} "
                    f"while that implementation and {declared['gate']} still exist",
                )
            )

    # 5b. The truth-state vocabulary the system must be able to distinguish.
    for state in STATES_THE_SYSTEM_MUST_BE_ABLE_TO_DISTINGUISH:
        if state not in truth_section:
            findings.append(
                _finding(
                    "TRUTH_STATE_VOCABULARY_DRIFT",
                    "ERROR",
                    state,
                    "state is not definable at truth-model level in the constitutional law; "
                    "the required state set cannot be enforced",
                )
            )

    ids = [e["id"] for e in entries]
    # The same defect can be reachable from several registry entries. Report it once
    # so a gate does not cry wolf four times for one problem, but never hide the count.
    unique: dict[str, dict] = {}
    suppressed = 0
    for finding in sorted(findings, key=lambda f: (f["code"], f["subject"])):
        if finding["fingerprint"] in unique:
            suppressed += 1
            continue
        unique[finding["fingerprint"]] = finding
    ordered = sorted(unique.values(), key=lambda f: (f["code"], f["subject"]))
    report = {
        "schema": "naya/contract-registry-conformance/v1",
        "generated_from": {
            "registry": REGISTRY_RELPATH,
            "constitution": CONSTITUTION_RELPATH,
            "library_index": LIBRARY_INDEX_RELPATH,
            "boot_paths": list(BOOT_PATHS),
        },
        "registry_entries": len(entries),
        "registry_ids_unique": len(ids) == len(set(ids)),
        "cited_paths_checked": cited_paths_checked,
        "constitutional_equations_present": len(CONSTITUTIONAL_EQUATIONS)
        - len(constitutional_equations_missing(law_text)),
        "constitutional_equations_required": len(CONSTITUTIONAL_EQUATIONS),
        "conforming": not unique,
        "duplicate_findings_suppressed": suppressed,
        "findings": ordered,
    }
    # Self-describing: the report always states its own drift position, so no caller
    # can read a report and mistake known debt for a clean bill of health.
    result = classify(report, load_baseline(root))
    report["new_drift"] = result["new_drift"]
    report["known_debt"] = result["known_debt"]
    return report


def classify(report: dict, baseline_fingerprints: set[str]) -> dict:
    new = [f for f in report["findings"] if f["fingerprint"] not in baseline_fingerprints]
    known = [f for f in report["findings"] if f["fingerprint"] in baseline_fingerprints]
    return {
        "new_drift": len(new),
        "known_debt": len(known),
        "new_findings": new,
        "conforming": not report["findings"],
    }


def load_baseline(root: Path) -> set[str]:
    baseline_path = root / BASELINE_RELPATH
    if not baseline_path.is_file():
        return set()
    data = json.loads(baseline_path.read_text(encoding="utf-8"))
    return {entry["fingerprint"] for entry in data.get("findings", []) if "fingerprint" in entry}


def write_baseline(root: Path, report: dict) -> None:
    payload = {
        "schema": "naya/contract-registry-conformance-baseline/v1",
        "note": (
            "Known debt of the canonical contract registry. A finding in this file is "
            "reported but does not fail the gate. A finding NOT in this file is new drift "
            "and fails. Clearing an entry here is a deliberate, reviewable act."
        ),
        "findings": report["findings"],
    }
    (root / BASELINE_RELPATH).write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write-baseline", action="store_true")
    parser.add_argument("--root", default=str(REPO_DEFAULT))
    args = parser.parse_args()
    root = Path(args.root)

    try:
        report = audit(root)
    except AuditError as exc:
        print(f"CONTRACT_REGISTRY_CONFORMANCE=AUDIT_ERROR {exc}", file=sys.stderr)
        return 2

    if args.write_baseline:
        write_baseline(root, report)
        print(f"BASELINE_WRITTEN {BASELINE_RELPATH} findings={len(report['findings'])}")
        return 0

    result = classify(report, load_baseline(root))
    report["new_drift"] = result["new_drift"]
    report["known_debt"] = result["known_debt"]

    if args.json:        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print("CONTRACT_REGISTRY_CONFORMANCE=REPORTED")
        print(f"REGISTRY={REGISTRY_RELPATH}")
        print(f"REGISTRY_ENTRIES={report['registry_entries']}")
        print(f"REGISTRY_IDS_UNIQUE={report['registry_ids_unique']}")
        print(f"CITED_PATHS_CHECKED={report['cited_paths_checked']}")
        print(
            "CONSTITUTIONAL_EQUATIONS="
            f"{report['constitutional_equations_present']}/{report['constitutional_equations_required']}"
        )
        for code in sorted({f["code"] for f in report["findings"]}):
            count = sum(1 for f in report["findings"] if f["code"] == code)
            print(f"FINDING {code} x{count}")
        print(f"KNOWN_DEBT={report['known_debt']}")
        print(f"NEW_DRIFT={report['new_drift']}")
        print(f"CONFORMING={report['conforming']}")
        if result["new_findings"]:
            print("NEW_DRIFT_DETAIL:")
            for finding in result["new_findings"]:
                print(f"  {finding['severity']} {finding['code']} {finding['subject']}")

    (root / REPORT_RELPATH).write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return 1 if result["new_drift"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
