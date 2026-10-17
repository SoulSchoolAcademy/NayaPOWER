#!/usr/bin/env python3
"""D28 assumption-audit gate — Naya 2 wire lane, 2026-10-11.

Wires the D28 independent fairness-assumption audit protocol
(drift_canary/fairness_audit.py, PR #2306) to the fairness CI path.

WHAT IT GUARDS
  Every fairness verdict that rests on named assumptions (notably
  FAIRNESS_QUALIFIED_WITH_ASSUMPTIONS from tools/fairness_eligibility.py)
  must rest on assumptions that survive the D28 independent audit:
  independently justified (G1), satisfiable (G2), minimal (G3),
  non-circular (G4). A rigged assumption — one that deletes a genuine
  scheduler failure from the model without naming the exclusion — must
  never silently carry a qualification.

TRIGGER
  CI workflow .github/workflows/fairness-assumption-audit.yml runs this
  gate on every PR touching the fairness path, the D27 registry, the D28
  module, or the audit manifest below. It also runs on pushes to main.

WHAT IT BLOCKS
  exit 1 — a real violation: an audit that returns REJECTED /
  REDUNDANT_ASSUMPTIONS / CLAIM_NOT_ESTABLISHED, a manifest entry that
  refuses to bind (missing justification fields — the gate never invents
  them), an assumption id unknown to the D27 registry, or evidence that
  does not resolve.
  exit 2 — the gate itself is broken (unreadable/corrupt manifest):
  fail-closed, never a silent pass.

DORMANT, NEVER THEATER
  exit 0 with an explicit DORMANT verdict when there is nothing to audit:
  the D28 module or the D27 registry is absent on this tree, or the audit
  manifest registers zero audits. Dormant never claims "audited".

THE MANIFEST (tools/fairness_audit_manifest.json)
  The handoff artifact. Each entry fully specifies one audit: the D27
  assumption ids, the justification fields D28 requires (owner, status,
  justification, justification_evidence — the gate REFUSES to invent
  them), the model footprint, and the claim context. The fairness lane
  fills entries in as justification evidence lands; the day the first
  entry lands, enforcement activates with zero new wiring.

FAILURE MODE IF THE WIRING BREAKS
  If this gate stops running (workflow deleted, step skipped), the
  fairness path falls back to today's behavior: qualifications resting
  on unaudited assumptions. That regression is visible: the gate's
  absence is itself detectable (no D28_AUDIT_GATE verdict line in CI).
  The gate never alters a verdict — it only refuses to let an unaudited
  or dishonestly-audited assumption set pass.

Stdlib only.
"""
from __future__ import annotations

import json
import os
import sys

# Make sibling tools/ imports work regardless of the caller's cwd
# (mirrors the convention in tools/merge_queue_fairness.py, which does
# `from fairness_assumptions import ...` with tools/ on the path).
_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_HERE)
for _p in (_HERE, _REPO_ROOT):
    if _p not in sys.path:
        sys.path.insert(0, _p)

MANIFEST_NAME = "fairness_audit_manifest.json"

# Verdict line prefix — greppable in CI logs.
TAG = "D28_AUDIT_GATE"

# Exit codes: 0 pass-or-dormant, 1 violation blocked, 2 gate broken.
EXIT_OK = 0
EXIT_VIOLATION = 1
EXIT_BROKEN = 2

REQUIRED_AUDIT_KEYS = (
    "audit_id",
    "assumption_ids",
    "owner",
    "status",
    "justification",
    "justification_evidence",
    "claim",
)


def _say(verdict: str, detail: str) -> None:
    print(f"{TAG}: {verdict} {detail}")


def _load_manifest(path: str):
    """Returns (manifest_dict, error). error is None on success."""
    if not os.path.exists(path):
        return None, "no manifest file"
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        return None, f"unreadable manifest: {exc}"
    if not isinstance(data, dict) or not isinstance(data.get("audits"), list):
        return None, "manifest must be {\"audits\": [...]}"
    return data, None


def _load_audit_module():
    try:
        from drift_canary import fairness_audit  # noqa: F401
        return fairness_audit
    except ImportError:
        return None


def _load_registry():
    """The D27 assumption registry: id -> object with .id/.statement."""
    for modname in ("fairness_assumptions", "tools.fairness_assumptions"):
        try:
            mod = __import__(modname, fromlist=["ASSUMPTIONS"])
            reg = getattr(mod, "ASSUMPTIONS", None)
            if isinstance(reg, dict):
                return reg
        except ImportError:
            continue
    return None


def _validate_audit_entry(entry, idx):
    """Fail-closed validation of one manifest entry. Returns error or None."""
    if not isinstance(entry, dict):
        return f"audits[{idx}] must be an object"
    for key in REQUIRED_AUDIT_KEYS:
        if key not in entry or entry[key] in (None, "", [], ()):
            return (
                f"audits[{idx}] missing required key '{key}': the gate "
                f"refuses to invent justification fields"
            )
    if not isinstance(entry["assumption_ids"], list) or not all(
        isinstance(i, str) and i for i in entry["assumption_ids"]
    ):
        return f"audits[{idx}].assumption_ids must be a non-empty list of ids"
    if not isinstance(entry["justification_evidence"], list):
        return f"audits[{idx}].justification_evidence must be a list"
    for j, ev in enumerate(entry["justification_evidence"]):
        if not isinstance(ev, dict) or not ev.get("name") or not ev.get("produced_by"):
            return (
                f"audits[{idx}].justification_evidence[{j}] needs "
                f"'name' and 'produced_by'"
            )
    claim = entry["claim"]
    if not isinstance(claim, dict):
        return f"audits[{idx}].claim must be an object"
    for ckey in ("claim_id", "property_claimed", "scheduler_id",
                 "qualification_artifact"):
        if not claim.get(ckey):
            return f"audits[{idx}].claim missing '{ckey}'"
    return None


def run_gate(manifest_path: str) -> int:
    manifest, merr = _load_manifest(manifest_path)
    if manifest is None:
        if merr == "no manifest file":
            _say("DORMANT", "no audit manifest on this tree; no audit performed")
            return EXIT_OK
        _say("BROKEN", merr)
        return EXIT_BROKEN

    audit_mod = _load_audit_module()
    registry = _load_registry()
    if audit_mod is None or registry is None:
        missing = []
        if audit_mod is None:
            missing.append("D28 audit module (drift_canary/fairness_audit.py)")
        if registry is None:
            missing.append("D27 registry (tools/fairness_assumptions.py)")
        _say("DORMANT", f"mechanism not present on this tree: {', '.join(missing)}; "
                        f"no audit performed")
        return EXIT_OK

    audits = manifest["audits"]
    if not audits:
        _say("DORMANT",
             f"0 audits registered ({len(registry)} assumptions in registry); "
             f"no audit performed")
        return EXIT_OK

    for idx, entry in enumerate(audits):
        err = _validate_audit_entry(entry, idx)
        if err:
            _say("VIOLATION", err)
            return EXIT_VIOLATION
        audit_id = entry["audit_id"]

        # Every named assumption must resolve in the D27 registry.
        for aid in entry["assumption_ids"]:
            if aid not in registry:
                _say("VIOLATION",
                     f"{audit_id}: assumption '{aid}' unknown to the D27 "
                     f"registry — phantom assumptions never carry a verdict")
                return EXIT_VIOLATION

        # Bind through from_d27: it REFUSES to invent justification fields.
        bound = []
        try:
            for aid in entry["assumption_ids"]:
                bound.append(audit_mod.from_d27(
                    registry[aid],
                    owner=entry["owner"],
                    status=entry["status"],
                    justification=entry["justification"],
                    justification_evidence=tuple(
                        ev["name"] for ev in entry["justification_evidence"]),
                    model_constraint=entry.get("model_constraint", "NONE"),
                    in_qualification_scope=entry.get("in_qualification_scope", True),
                ))
        except Exception as exc:  # from_d27 raises AuditInputError on refusal
            _say("VIOLATION", f"{audit_id}: binding refused: {exc}")
            return EXIT_VIOLATION

        # Independent evidence ledger: the prover does not control it.
        ledger = audit_mod.EvidenceLedger()
        try:
            for ev in entry["justification_evidence"]:
                ledger.record(audit_mod.EvidenceRecord(
                    name=ev["name"],
                    produced_by=ev["produced_by"],
                    produced_at=ev.get("produced_at", ""),
                    summary=ev.get("summary", ""),
                ))
        except Exception as exc:
            _say("VIOLATION", f"{audit_id}: ledger rejected evidence: {exc}")
            return EXIT_VIOLATION

        claim = entry["claim"]
        qclaim = audit_mod.QualificationClaim(
            claim_id=claim["claim_id"],
            property_claimed=claim["property_claimed"],
            scheduler_id=claim["scheduler_id"],
            qualification_artifact=claim["qualification_artifact"],
            prover_policy=claim.get("prover_policy", "STRONG"),
            excluded_behaviors=tuple(claim.get("excluded_behaviors", ())),
        )
        try:
            verdict = audit_mod.audit_assumption_set(
                tuple(bound), qclaim, ledger,
                model_depth=int(entry.get("model_depth", 12)))
        except Exception as exc:
            _say("VIOLATION", f"{audit_id}: audit raised: {exc}")
            return EXIT_VIOLATION

        if verdict.kind != "AUDIT_PASSED":
            _say("VIOLATION",
                 f"{audit_id}: {verdict.kind} at {verdict.failed_gate or verdict.kind}: "
                 f"{verdict.reason}")
            return EXIT_VIOLATION
        _say("PASS", f"{audit_id}: AUDIT_PASSED at depth {verdict.model_depth}")

    _say("PASS", f"all {len(audits)} registered audits passed")
    return EXIT_OK


def main(argv) -> int:
    manifest_path = (argv[1] if len(argv) > 1
                     else os.path.join(_HERE, MANIFEST_NAME))
    return run_gate(manifest_path)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
