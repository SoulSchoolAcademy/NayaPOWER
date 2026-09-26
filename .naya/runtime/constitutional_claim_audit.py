"""Repo-wide audit of artifacts that SELF-DECLARE constitutional authority.

PURPOSE
There are two existing gates, and between them they still cannot see the most
dangerous failure mode in the repository:

  * ``contract_library_integrity.py``  audits the *structure* of the contract
    library, scoped to ``.naya/contracts/``.
  * ``contract_registry_conformance.py`` audits the *claims the registry makes
    about the world*, scoped to the registry, the constitutional law, and
    ``.naya/contracts/``.

Neither one looks outside ``.naya/contracts/``. So an artifact can live anywhere
else in the tree, declare itself ``CANONICAL / CONSTITUTIONAL / ACTIVE``, and
both gates report green. That is not hypothetical. As of 2026-09-26 at least
nine tracked artifacts under ``.naya/codex/`` and ``.naya/`` do exactly that,
with no supersession chain and no authority grant.

Under Contract 00 V2 section 2.1 that is a ``CONFLICTED`` state. Under section
16 a status with no recorded authority grant is not a status at all. A
constitution that cannot detect a rival constitution is not governing anything.

This module closes exactly that gap and nothing else. It answers, from
repository evidence only:

  1. Which artifacts self-declare canonical/constitutional authority?
  2. Do two or more of them claim to be *simultaneously in force* with no
     supersession chain resolving precedence?
  3. Do they declare supersession at all?
  4. Are they mapped in the canonical contract registry (V2 section 2.1)?
  5. Do their status declarations use the section 16 status vocabulary?

WHAT THIS MODULE DOES NOT DO
It grants no authority, ratifies nothing, supersedes nothing, and does not
decide which claimant is correct. Resolution is a Human Director decision.
This module only makes an invisible conflict machine-visible and fail-closed.

SCOPE / NON-DUPLICATION
Complementary to the two gates above, not a replacement for either. Detection
only. It deliberately does not attempt to parse, rank, or reconcile the
substance of competing constitutional claims.

FAIL-CLOSED BASELINE MODEL
Known debt is reduced to a stable fingerprint and compared against
``.naya/contracts/CONSTITUTIONAL-CLAIM-AUDIT-BASELINE.json``:
    finding NOT in baseline -> NEW_DRIFT  -> exit 1 (gate fails)
    finding IN baseline     -> KNOWN_DEBT -> reported, does not fail
The report states ``conforming: false`` while any debt exists, so this gate can
never be mistaken for a clean bill of health on constitutional authority.

SCAN BOUND
Status declarations are read from the first ``SCAN_MAX_LINES`` lines of each
tracked markdown artifact, because authority self-declarations are header
matter. The bound is a deliberate, documented trade-off: it keeps the audit
cheap and deterministic, at the cost of not detecting a claim buried deep in a
document body. A body-buried claim is not a governance surface.

Run:  python -B .naya/runtime/constitutional_claim_audit.py
      python -B .naya/runtime/constitutional_claim_audit.py --json
Exit: 0 = no new drift, 1 = new drift, 2 = audit could not run.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO_DEFAULT = Path(__file__).resolve().parents[2]

REGISTRY_RELPATH = ".naya/control-plane/CANONICAL-CONTRACT-REGISTRY.md"
# Deliberately NOT under .naya/contracts/. This audit is a machine artifact, not
# a contract. Putting it in the contract library would make the merged
# contract-library integrity gate (PR #799) report a new UNREFERENCED_CONTRACT
# finding for this gate's own baseline, which would be self-inflicted noise in
# someone else's gate.
BASELINE_RELPATH = ".naya/CONSTITUTIONAL-CLAIM-AUDIT-BASELINE.json"
REPORT_RELPATH = ".naya/constitutional-claim-audit-report.json"

# Authority self-declaration is header matter; reading deeper buys nothing.
SCAN_MAX_LINES = 120

DENY_DIRS = frozenset(
    {
        ".git",
        "node_modules",
        "dist",
        "build",
        ".next",
        "coverage",
        "__pycache__",
        "vendor",
        ".venv",
        "venv",
        "site-packages",
    }
)

# Contract 00 V2 section 16 status vocabulary. A status outside this set is not
# a status; it is a claim.
STATUS_VOCABULARY = frozenset(
    {
        "DRAFT",
        "PROPOSED",
        "RATIFIED",
        "ACTIVE",
        "SUPERSEDED",
        "RETIRED",
        "CONFLICTED",
    }
)

# Tokens asserting supreme or canonical authority. Kept deliberately tight:
# a loose vocabulary turns a governance gate into a word-frequency counter.
AUTHORITY_TOKENS = ("CANONICAL", "CONSTITUTIONAL", "SUPREME", "GOVERNING")

# Tokens asserting the claim is in force right now.
ACTIVE_TOKENS = ("ACTIVE", "IN-FORCE", "IN FORCE", "BINDING")

# A self-declaration only matters on the governance surface. Scanning every
# markdown file in the tree finds "ACTIVE" in project reports, receipts and
# changelogs, which are not constitutional claims. An earlier revision of this
# module scanned repo-wide and produced 533 findings, of which the overwhelming
# majority were that noise. Narrowing to the governance surface yields findings
# that each name a real competing authority claim.
GOVERNANCE_SURFACE_RE = re.compile(
    r"(?i)(constitution|constitutional|amendment|charter|operating[-_ ]law"
    r"|covenant|governance|master[-_ ]synthesis)"
)

STATUS_LINE_RE = re.compile(r"(?i)\bstatus\b\s*\**\s*[:\-]?\s*(?P<value>[^\n]+)")
SUPERSESSION_RE = re.compile(
    r"(?i)\b(supersedes|supersede|superseded\s+by|replaces|replaced\s+by|superseding)\b"
)


def _rel(path: Path, repo: Path) -> str:
    """Repository-relative POSIX path, tolerant of paths outside the repo."""
    try:
        return path.resolve().relative_to(repo.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def finding(kind: str, detail: str, locations: list[str], severity: str = "ERROR") -> dict:
    """Build a finding with a stable fingerprint.

    Identical construction to ``contract_library_integrity.finding`` so the two
    gates' baselines stay comparable. The fingerprint excludes file content, so
    editing a claimant does not silently reset its debt record, but includes the
    location set, so adding or moving a rival claimant is new drift.
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


def iter_markdown(repo: Path):
    """Yield markdown artifacts, pruning build/vendor noise. No git dependency."""
    for dirpath, dirnames, filenames in os.walk(repo):
        dirnames[:] = sorted(d for d in dirnames if d not in DENY_DIRS)
        for name in sorted(filenames):
            if name.lower().endswith((".md", ".markdown")):
                yield Path(dirpath) / name


def read_head(path: Path) -> str:
    """First SCAN_MAX_LINES lines, decoded leniently. Missing file -> empty."""
    try:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            return "".join(handle.readline() for _ in range(SCAN_MAX_LINES))
    except OSError:
        return ""


def claim_of(head: str) -> dict | None:
    """Extract an authority self-declaration from a document head, if present.

    A claim is a status line whose value contains at least one authority or
    in-force token. Returns None when the artifact makes no such declaration,
    which is the normal and healthy case.
    """
    for match in STATUS_LINE_RE.finditer(head):
        value = match.group("value")
        upper = value.upper()
        authority = sorted({t for t in AUTHORITY_TOKENS if t in upper})
        active = sorted({t for t in ACTIVE_TOKENS if t in upper})
        if not authority and not active:
            continue
        return {
            "value": value.strip(),
            "authority_tokens": authority,
            "active_tokens": active,
            "supreme": bool(authority) and bool(active),
            "vocabulary_ok": any(
                re.search(rf"\b{re.escape(s)}\b", upper) for s in STATUS_VOCABULARY
            ),
        }
    return None


def is_governance_surface(path: Path, rel: str) -> bool:
    """True when this artifact is itself a governance instrument, not a record.

    Two independent signals, either sufficient: the filename declares a
    governance instrument (constitution, amendment, charter, operating law,
    covenant, governance), or the artifact is a contract in the contract
    library. Everything else is out of scope by construction.
    """
    return bool(GOVERNANCE_SURFACE_RE.search(path.stem)) or rel.startswith(
        ".naya/contracts/"
    )


def collect_claims(repo: Path) -> dict[str, dict]:
    """Map artifact stem -> claim record for every self-declaring artifact."""
    claims: dict[str, dict] = {}
    for path in iter_markdown(repo):
        rel = _rel(path, repo)
        if not is_governance_surface(path, rel):
            continue
        head = read_head(path)
        claim = claim_of(head)
        if claim is None:
            continue
        claim["path"] = rel
        claim["supersedes"] = _supersession_targets(head, path.stem, repo)
        claims[path.stem] = claim
    return claims


def _supersession_targets(head: str, own_stem: str, repo: Path) -> list[str]:
    """Artifacts this document claims to supersede, restricted to real files.

    Only counts as a supersession edge when the document actually uses
    supersession language AND names an artifact that exists in the tree. A bare
    word "supersede" in a template section is not an authority grant.
    """
    if not SUPERSESSION_RE.search(head):
        return []
    stems = {p.stem for p in iter_markdown(repo)}
    stems.discard(own_stem)
    named = []
    for candidate in sorted(stems):
        if len(candidate) < 8:
            continue
        if re.search(rf"(?i)\b{re.escape(candidate)}\b", head):
            named.append(candidate)
    return named


def registry_referenced_paths(repo: Path) -> set[str] | None:
    """Paths the canonical contract registry maps, or None if it is absent."""
    registry = repo / REGISTRY_RELPATH
    if not registry.is_file():
        return None
    text = registry.read_text(encoding="utf-8", errors="replace")
    return {
        m.replace("\\", "/")
        for m in re.findall(r"[A-Za-z0-9_./-]+\.(?:md|markdown|json|ya?ml)", text)
    }


def audit(repo: Path) -> dict:
    """Run every check and return the report payload."""
    claims = collect_claims(repo)
    supreme = {stem: c for stem, c in claims.items() if c["supreme"]}
    findings: list[dict] = []

    # 1. Unreachable registry fails closed: V2 section 2.1 mapping is impossible.
    referenced = registry_referenced_paths(repo)
    if referenced is None:
        findings.append(
            finding(
                "REGISTRY_UNREACHABLE",
                f"canonical contract registry {REGISTRY_RELPATH} does not exist; "
                "constitutional self-declarations cannot be mapped and cannot be "
                "disambiguated",
                [REGISTRY_RELPATH],
            )
        )

    # 2. Non-vocabulary status. Scoped to supreme claims: the section 16 status
    #    set is closed, and an in-force constitutional claim is exactly where
    #    inventing a private status word does the most damage.
    for stem, claim in sorted(supreme.items()):
        if not claim["vocabulary_ok"]:
            findings.append(
                finding(
                    "NON_VOCABULARY_STATUS",
                    f"{claim['path']} declares status {claim['value']!r} using no "
                    "Contract 00 V2 section 16 status token; a claim outside the "
                    "status vocabulary is not a lifecycle state",
                    [claim["path"]],
                )
            )

    # 3. Unmapped constitutional claim: V2 section 2.1 mapping obligation.
    if referenced is not None:
        for stem, claim in sorted(supreme.items()):
            if not any(claim["path"].endswith(ref) for ref in referenced):
                findings.append(
                    finding(
                        "UNMAPPED_AUTHORITY_CLAIM",
                        f"{claim['path']} self-declares as in-force constitutional "
                        "authority ({claim['value']!r}) but is not mapped in "
                        f"{REGISTRY_RELPATH}; precedence between competing "
                        "constitutional claims is not machine-decidable",
                        [claim["path"], REGISTRY_RELPATH],
                    )
                )

    # 4. Concurrent unresolvable supreme claims. Scoping matters: a lone
    #    constitution has nothing to supersede, so demanding a supersession
    #    target from it would be a false positive. Supersession is only owed
    #    once a rival claim exists.
    superseded: set[str] = set()
    for claim in supreme.values():
        superseded.update(claim["supersedes"])
    survivors = sorted(stem for stem in supreme if stem not in superseded)
    if len(survivors) > 1:
        for stem in survivors:
            claim = supreme[stem]
            if not claim["supersedes"]:
                findings.append(
                    finding(
                        "MISSING_SUPERSESSION",
                        f"{claim['path']} self-declares as in-force constitutional "
                        f"authority ({claim['value']!r}) while rival constitutional "
                        "claims exist, and names no artifact it supersedes; it "
                        "cannot be ordered against them",
                        [claim["path"]],
                    )
                )
        findings.append(
            finding(
                "CONCURRENT_SUPREME_CLAIM",
                f"{len(survivors)} artifacts self-declare as simultaneously "
                "in-force canonical/constitutional law with no supersession chain "
                "resolving precedence: " + ", ".join(supreme[s]["path"] for s in survivors),
                [supreme[s]["path"] for s in survivors],
            )
        )

    findings.sort(key=lambda f: (f["kind"], f["fingerprint"]))
    unmapped = sorted(
        c["path"] for c in supreme.values()
        if referenced is not None
        and not any(c["path"].endswith(ref) for ref in referenced)
    )
    return {
        "schema": "naya.constitutional-claim-audit/1",
        "registry": REGISTRY_RELPATH,
        "artifacts_scanned": sum(1 for _ in iter_markdown(repo)),
        "self_declaring_artifacts": sorted(c["path"] for c in claims.values()),
        "supreme_claims": sorted(c["path"] for c in supreme.values()),
        "unmapped_supreme_claims": unmapped,
        "findings": findings,
    }


def load_baseline(repo: Path) -> set[str]:
    """Recorded debt fingerprints. Absent baseline means zero known debt."""
    path = repo / BASELINE_RELPATH
    if not path.is_file():
        return set()
    data = json.loads(path.read_text(encoding="utf-8"))
    return {entry["fingerprint"] for entry in data.get("known_findings", [])}


def render(report: dict, baseline: set[str]) -> tuple[int, str]:
    """Split findings into known debt and new drift, and render the summary."""
    known: list[dict] = []
    new_drift: list[dict] = []
    for entry in report["findings"]:
        (known if entry["fingerprint"] in baseline else new_drift).append(entry)

    lines = [
        "CONTRACTUAL AUTHORITY SELF-DECLARATION AUDIT",
        f"artifacts scanned      : {report['artifacts_scanned']}",
        f"governance-surface claims: {len(report['self_declaring_artifacts'])}",
        f"supreme (in-force) claims: {len(report['supreme_claims'])}",
        f"unmapped in registry     : {len(report['unmapped_supreme_claims'])}",
        f"KNOWN DEBT (recorded in baseline, not failing): {len(known)}",
    ]
    for entry in known:
        lines.append(f"  [KNOWN] {entry['kind']} {entry['fingerprint']}")
        lines.append(f"          {entry['detail']}")
    lines.append(f"NEW DRIFT (not in baseline, gate fails): {len(new_drift)}")
    for entry in new_drift:
        lines.append(f"  [NEW] {entry['kind']} {entry['fingerprint']}")
        lines.append(f"        {entry['detail']}")
    if not new_drift:
        lines.append("CONSTITUTIONAL_CLAIMS_NO_NEW_DRIFT")
    else:
        lines.append("CONSTITUTIONAL_CLAIMS_NEW_DRIFT")
    if report["findings"]:
        lines.append(
            "NOTE: known debt is NOT a pass. Constitutional authority remains "
            "unreconciled and requires a Human Director decision."
        )
    return (1 if new_drift else 0), "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repo", type=Path, default=REPO_DEFAULT)
    ap.add_argument("--json", action="store_true", help="write the machine-readable report")
    ap.add_argument(
        "--update-baseline",
        action="store_true",
        help="record current findings as known debt (requires explicit human invocation)",
    )
    args = ap.parse_args()
    repo: Path = args.repo.resolve()
    if not repo.is_dir():
        print(f"CONSTITUTIONAL_CLAIMS_AUDIT_ERROR: repo not found: {repo}", file=sys.stderr)
        return 2

    try:
        report = audit(repo)
    except Exception as exc:  # fail closed: an unrunnable audit is not a pass
        print(f"CONSTITUTIONAL_CLAIMS_AUDIT_ERROR: {exc}", file=sys.stderr)
        return 2

    if args.update_baseline:
        payload = {
            "registry": REGISTRY_RELPATH,
            "scan_max_lines": SCAN_MAX_LINES,
            "known_findings": report["findings"],
        }
        (repo / BASELINE_RELPATH).write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        print(
            f"BASELINE_UPDATED: {BASELINE_RELPATH} "
            f"({len(report['findings'])} findings recorded as known debt)"
        )
        return 0

    baseline = load_baseline(repo)
    code, text = render(report, baseline)
    print(text)

    if args.json:
        known = sorted(f["fingerprint"] for f in report["findings"] if f["fingerprint"] in baseline)
        report["known_debt"] = known
        report["new_drift"] = sorted(
            f["fingerprint"] for f in report["findings"] if f["fingerprint"] not in baseline
        )
        report["conforming"] = not report["findings"]
        (repo / REPORT_RELPATH).write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        print(f"REPORT: {REPORT_RELPATH}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
