#!/usr/bin/env python3
"""D58 eligibility gate — Naya 2 wire lane, 2026-10-11.

Wires the D58 independent eligibility proof for every scheduling
opportunity (drift_canary/eligibility_proof.py, PR #2311) to the fairness
CI path.

WHAT IT GUARDS
  drift_canary/fairness.py's FairnessLedger.record_round trusts
  SchedulingEvent.eligible — the scheduler's own flag — when accruing
  fairness debt. Trace consistency does not prove the eligibility
  booleans were true. Every scheduling opportunity a fairness-bound
  claim COUNTS must rest on a D58 independent eligibility receipt: all
  six components (AUTHORIZATION, OUTSTANDING_WORK, READY_DEPENDENCIES,
  SCHEDULABLE_CAPACITY, APPLICABLE_OPPORTUNITY, CONSISTENT_ORDERING)
  independently established. The scheduler's flag is assessed as a claim
  (HIDDEN_OPPORTUNITY / FALSE_CLAIM / CONSISTENT / DEFERRED), never used
  as evidence — tainted origins are refused.

TRIGGER
  CI workflow .github/workflows/d58-eligibility-gate.yml runs this gate
  on every PR touching the eligibility path, the FairnessLedger, or the
  manifest below. It also runs on pushes to main.

WHAT IT BLOCKS
  exit 1 — a real violation: an opportunity the claim counts whose D58
  verdict is not ELIGIBLE (UNDETERMINED counts nothing; INELIGIBLE counts
  nothing), a HIDDEN_OPPORTUNITY (scheduler hid a genuine opportunity from
  the bound) or FALSE_CLAIM (scheduler asserted eligibility the evidence
  refutes), evidence backed by a tainted origin (scheduler_flag,
  worker_trace, worker_assertion, self_report, unattested), an unknown
  evidence component, or a manifest entry the gate refuses to bind — the
  gate never invents missing evidence fields.
  exit 2 — the gate itself is broken (unreadable/corrupt manifest):
  fail-closed, never a silent pass.

DORMANT, NEVER THEATER
  exit 0 with an explicit DORMANT verdict when there is nothing to
  verify: the D58 module is absent on this tree, or the manifest
  registers zero opportunities. Dormant never claims "verified".

THE MANIFEST (tools/d58_eligibility_manifest.json)
  The handoff artifact. Each entry fully specifies one counted
  opportunity: the six evidence components with status, detail, and
  declared origin — the gate binds them through the real D58 prover and
  REFUSES to invent what is not declared. The fairness lane registers
  entries as independent evidence lands; the day the first entry lands,
  enforcement activates with zero new wiring.

FAILURE MODE IF THE WIRING BREAKS
  If this gate stops running (workflow deleted, step skipped), the
  fairness path falls back to today's behavior: fairness debt accrues on
  the scheduler's flag alone. That regression is visible: the gate's
  absence is itself detectable (no D58_ELIGIBILITY_GATE verdict line in
  CI). The gate never alters a ledger — it only refuses to let an
  unverified or dishonestly-verified eligibility claim pass.

Stdlib only.
"""
from __future__ import annotations

import json
import os
import sys

# Make sibling tools/ imports work regardless of the caller's cwd.
_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_HERE)
for _p in (_HERE, _REPO_ROOT):
    if _p not in sys.path:
        sys.path.insert(0, _p)

MANIFEST_NAME = "d58_eligibility_manifest.json"

# Verdict line prefix — greppable in CI logs.
TAG = "D58_ELIGIBILITY_GATE"

# Exit codes: 0 pass-or-dormant, 1 violation blocked, 2 gate broken.
EXIT_OK = 0
EXIT_VIOLATION = 1
EXIT_BROKEN = 2

REQUIRED_ENTRY_KEYS = (
    "opportunity_id",
    "obligation_id",
    "round_seq",
    "components",
)

REQUIRED_COMPONENT_KEYS = ("status", "detail", "origin")


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
    if not isinstance(data, dict) or not isinstance(data.get("opportunities"), list):
        return None, 'manifest must be {"opportunities": [...]}'
    return data, None


def _load_proof_module():
    try:
        from drift_canary import eligibility_proof
        return eligibility_proof
    except ImportError:
        return None


def _validate_entry(entry, idx):
    """Fail-closed validation of one manifest entry. Returns error or None."""
    if not isinstance(entry, dict):
        return f"opportunities[{idx}] must be an object"
    for key in REQUIRED_ENTRY_KEYS:
        if key not in entry or entry[key] in (None, ""):
            return (
                f"opportunities[{idx}] missing required key '{key}': the "
                f"gate refuses to invent evidence fields"
            )
    if not isinstance(entry["round_seq"], int):
        return f"opportunities[{idx}].round_seq must be an integer"
    comps = entry["components"]
    if not isinstance(comps, dict) or not comps:
        return f"opportunities[{idx}].components must be a non-empty object"
    for cname, comp in comps.items():
        if not isinstance(comp, dict):
            return f"opportunities[{idx}].components['{cname}'] must be an object"
        for ckey in REQUIRED_COMPONENT_KEYS:
            if ckey not in comp or comp[ckey] in (None, ""):
                return (
                    f"opportunities[{idx}].components['{cname}'] missing "
                    f"'{ckey}': the gate refuses to invent evidence"
                )
        if comp["status"] not in ("PROVEN", "REFUTED", "UNKNOWN"):
            return (
                f"opportunities[{idx}].components['{cname}'].status must be "
                f"PROVEN|REFUTED|UNKNOWN, got '{comp['status']}'"
            )
    flag = entry.get("scheduler_flag", None)
    if flag is not None and not isinstance(flag, bool):
        return f"opportunities[{idx}].scheduler_flag must be true/false or absent"
    return None


def run_gate(manifest_path: str) -> int:
    manifest, merr = _load_manifest(manifest_path)
    if manifest is None:
        if merr == "no manifest file":
            _say("DORMANT", "no eligibility manifest on this tree; nothing verified")
            return EXIT_OK
        _say("BROKEN", merr)
        return EXIT_BROKEN

    proof_mod = _load_proof_module()
    if proof_mod is None:
        _say("DORMANT", "D58 eligibility module (drift_canary/eligibility_proof.py) "
                        "not present on this tree; nothing verified")
        return EXIT_OK

    opportunities = manifest["opportunities"]
    if not opportunities:
        _say("DORMANT", "0 opportunities registered; nothing verified")
        return EXIT_OK

    for idx, entry in enumerate(opportunities):
        err = _validate_entry(entry, idx)
        if err:
            _say("VIOLATION", err)
            return EXIT_VIOLATION
        opp_id = entry["opportunity_id"]

        # Bind through the real D58 prover: it REFUSES tainted origins,
        # rejects unknown components, and defaults missing components to
        # UNDETERMINED — the gate invents nothing.
        try:
            source = {
                cname: proof_mod.Evidence(
                    status=comp["status"],
                    detail=comp["detail"],
                    origin=comp["origin"],
                )
                for cname, comp in entry["components"].items()
            }
            prover = proof_mod.EligibilityProver(source)
            receipt = prover.prove(
                opportunity_id=entry["opportunity_id"],
                obligation_id=entry["obligation_id"],
                round_seq=entry["round_seq"],
                scheduler_flag=entry.get("scheduler_flag", None),
            )
        except Exception as exc:  # UnknownComponentError / TaintedOriginError / asserts
            _say("VIOLATION", f"{opp_id}: prover refused the binding: {exc}")
            return EXIT_VIOLATION

        # The scheduler's flag is a claim; the assessment is checked first
        # so a flag lie is named as what it is, not buried under the
        # verdict. (A HIDDEN_OPPORTUNITY receipt is ELIGIBLE; a FALSE_CLAIM
        # receipt is INELIGIBLE — both must be reported by name.)
        if receipt.flag_assessment == proof_mod.HIDDEN_OPPORTUNITY:
            _say("VIOLATION",
                 f"{opp_id}: HIDDEN_OPPORTUNITY — the scheduler recorded "
                 f"eligible=false on a genuinely eligible opportunity; the "
                 f"fairness bound under-counts")
            return EXIT_VIOLATION
        if receipt.flag_assessment == proof_mod.FALSE_CLAIM:
            _say("VIOLATION",
                 f"{opp_id}: FALSE_CLAIM — the scheduler asserted "
                 f"eligible=true on an opportunity the evidence refutes; the "
                 f"fairness bound over-counts")
            return EXIT_VIOLATION

        # D58: only ELIGIBLE receipts count toward a fairness bound.
        if receipt.verdict != proof_mod.ELIGIBLE:
            _say("VIOLATION",
                 f"{opp_id}: verdict {receipt.verdict} — a fairness-bound "
                 f"claim counts only ELIGIBLE opportunities; "
                 f"refuted={list(receipt.refuted)} "
                 f"unknown={list(receipt.unknown)} "
                 f"recovery={list(receipt.recovery_obligation)}")
            return EXIT_VIOLATION

        _say("PASS", f"{opp_id}: ELIGIBLE, flag {receipt.flag_assessment}")

    _say("PASS", f"all {len(opportunities)} registered opportunities verified ELIGIBLE")
    return EXIT_OK


def main(argv) -> int:
    manifest_path = (argv[1] if len(argv) > 1
                     else os.path.join(_HERE, MANIFEST_NAME))
    return run_gate(manifest_path)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
