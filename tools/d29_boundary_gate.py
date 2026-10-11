"""D29 boundary-claims gate (WIRE lane, night shift 2026-10-11).

Cold-judges every registered boundary claim against the REAL D29
mechanism (drift_canary/d29_boundary.py).

D29 - the accountability law: every failure gets assigned to the
component that actually controls it. A component cannot convert its own
failure into another component's assumption. The independent verifier
classifies from EVIDENCE ALONE; component narrative labels are never an
input to the verdict.

Exit codes:
  0  PASS, or explicit DORMANT when the manifest registers zero claims
     (dormant is stated, never a silent pass).
  1  VIOLATION: a registered claim contradicts the mechanism's own
     verdict/controller for the claimed scenario.
  2  BROKEN (fail-closed): manifest corrupt, claim malformed, mechanism
     missing, mechanism API surface changed, canary probe failed, or the
     mechanism's ledger cross-check contradicts its verdict. The gate
     never passes on a neutered mechanism.
"""

import argparse
import importlib.util
import json
import os
import sys

MECHANISM_REL = "drift_canary/d29_boundary.py"
MANIFEST_REL = "tools/d29_boundary_manifest.json"

# Fixed canary probes: (case, rounds, false_blame, expected_verdict,
# expected_controller). The probes deliberately use parameterizations no
# manifest claim relies on: the (B, 7) probe catches masquerade engines
# keyed to manifest-claimed scenarios, and the false-blame labels on
# (A, 6) prove narrative never enters the verdict.
CANARY_PROBES = (
    ("A", 6,
     (("SCHEDULER", "DATABASE_UNAVAILABLE", 1),
      ("WORKER", "WORKER_TIMEOUT", 2)),
     "ENVIRONMENT_BLOCKER", "ENVIRONMENT"),
    ("B", 7, (), "SCHEDULER_STARVATION", "SCHEDULER"),
    ("C", 6, (), "WORKER_NONPROGRESS", "WORKER"),
)

# The mechanism surface the gate depends on. A mechanism missing any of
# these is not the D29 mechanism this gate was proven against.
REQUIRED_API = (
    "VERDICTS", "CONTROLLERS", "CASES", "ComponentReport",
    "run_case", "verify_against_ledger", "classify_boundary",
)


class GateError(Exception):
    """Base class for fail-closed gate errors."""


class MechanismMissing(GateError):
    """The mechanism cannot be loaded or is not the D29 mechanism."""


class ManifestBroken(GateError):
    """The manifest is corrupt or a claim is malformed."""


def _repo_root():
    # tools/d29_boundary_gate.py -> repo root is two levels up.
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _module_name_for(rel_path):
    name = rel_path.replace("\\", "/")
    if name.endswith(".py"):
        name = name[:-3]
    return name.replace("/", ".")


def _load_mechanism(repo_root, mechanism_rel):
    """Load the real D29 mechanism module.

    Uses a sys.modules-pre-registered import so the module's dataclass
    decorators resolve against the imported module object (not a
    half-initialized one), and so the package-relative imports inside
    the mechanism (``from drift_canary.fairness import ...``) resolve.
    On any load failure the pre-registration is removed and
    MechanismMissing is raised - the gate never judges against a broken
    import.

    Test seam: if the derived module name is already present in
    sys.modules, that module object is used as-is (fake-mechanism
    injection for the gate's own test suite). The API-surface check
    still applies to injected modules.
    """
    module_name = _module_name_for(mechanism_rel)
    if module_name in sys.modules:
        mod = sys.modules[module_name]
    else:
        abs_path = os.path.join(repo_root, mechanism_rel.replace("/", os.sep))
        if not os.path.isfile(abs_path):
            raise MechanismMissing(
                "mechanism file not found: " + mechanism_rel)
        spec = importlib.util.spec_from_file_location(module_name, abs_path)
        if spec is None or spec.loader is None:
            raise MechanismMissing(
                "cannot build import spec for: " + mechanism_rel)
        mod = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = mod
        if repo_root not in sys.path:
            sys.path.insert(0, repo_root)
        try:
            spec.loader.exec_module(mod)
        except Exception as exc:
            sys.modules.pop(module_name, None)
            raise MechanismMissing(
                "mechanism import failed: " + str(exc))
    missing = [a for a in REQUIRED_API if not hasattr(mod, a)]
    if missing:
        raise MechanismMissing(
            "mechanism API surface changed; missing: " + ", ".join(missing))
    return mod


def _load_manifest(manifest_path):
    try:
        with open(manifest_path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError) as exc:
        raise ManifestBroken("manifest unreadable: " + str(exc))
    if not isinstance(data, dict):
        raise ManifestBroken("manifest root must be an object")
    claims = data.get("claims", [])
    if not isinstance(claims, list):
        raise ManifestBroken("manifest 'claims' must be a list")
    return claims


def _build_false_blame(mod, entries, claim_id):
    reports = []
    for i, entry in enumerate(entries or ()):
        if not isinstance(entry, dict):
            raise ManifestBroken(
                "claim " + claim_id + ": false_blame entry "
                + str(i) + " must be an object")
        component = entry.get("component", "")
        label = entry.get("label", "")
        seq = entry.get("seq", i)
        if not component or not label:
            raise ManifestBroken(
                "claim " + claim_id + ": false_blame entry "
                + str(i) + " needs component and label")
        reports.append(mod.ComponentReport(
            component=component, label=label, seq=seq))
    return tuple(reports)


def _validate_claim(mod, claim, index):
    where = "claim index " + str(index)
    if not isinstance(claim, dict):
        raise ManifestBroken(where + ": must be an object")
    claim_id = claim.get("id", where)
    case = claim.get("case")
    if case not in tuple(mod.CASES):
        raise ManifestBroken(
            "claim " + str(claim_id) + ": unknown case " + repr(case)
            + "; known: " + ", ".join(mod.CASES))
    rounds = claim.get("rounds", 6)
    if not isinstance(rounds, int) or isinstance(rounds, bool) or rounds < 1:
        raise ManifestBroken(
            "claim " + str(claim_id) + ": rounds must be a positive int")
    verdict = claim.get("claimed_verdict")
    if verdict not in tuple(mod.VERDICTS):
        raise ManifestBroken(
            "claim " + str(claim_id) + ": unknown claimed_verdict "
            + repr(verdict))
    controller = claim.get("claimed_controller")
    if controller not in tuple(mod.CONTROLLERS):
        raise ManifestBroken(
            "claim " + str(claim_id) + ": unknown claimed_controller "
            + repr(controller))
    return claim_id, case, rounds, verdict, controller


def _run_canary(mod):
    """Fixed canary probes against the loaded mechanism.

    Returns a list of failure strings (empty = canary healthy). The
    canary runs BEFORE any manifest judgment: a tampered or blind
    mechanism fails closed here and no claim is ever judged against it.
    """
    failures = []
    for case, rounds, blame, exp_verdict, exp_controller in CANARY_PROBES:
        fb = tuple(
            mod.ComponentReport(component=c, label=lab, seq=s)
            for c, lab, s in blame)
        try:
            result = mod.run_case(case, rounds=rounds, false_blame=fb)
            got = (result.verdict, result.record.controller)
            ledger_ok, ledger_reason = mod.verify_against_ledger(result)
        except Exception as exc:
            failures.append(
                "canary " + case + "/" + str(rounds)
                + " raised: " + str(exc))
            continue
        if got != (exp_verdict, exp_controller):
            failures.append(
                "canary " + case + "/" + str(rounds) + ": expected "
                + exp_verdict + "/" + exp_controller + ", mechanism gave "
                + str(got[0]) + "/" + str(got[1])
                + " - mechanism tampered or blind")
        elif not ledger_ok:
            failures.append(
                "canary " + case + "/" + str(rounds)
                + ": verdict matches but the mechanism contradicts its own "
                "ledger cross-check: " + str(ledger_reason))
    return failures


def judge(repo_root, manifest_path, mechanism_rel=MECHANISM_REL):
    """Judge every manifest claim against the real mechanism.

    Returns (exit_code, report_dict).
    """
    report = {
        "verdict": "BROKEN",
        "mechanism": _module_name_for(mechanism_rel),
        "canary": "not-run",
        "claims_checked": 0,
        "violations": [],
        "notes": [],
    }
    try:
        mod = _load_mechanism(repo_root, mechanism_rel)
        report["mechanism"] = mod.__name__
    except MechanismMissing as exc:
        report["notes"].append(str(exc))
        return 2, report
    canary_failures = _run_canary(mod)
    if canary_failures:
        report["canary"] = "FAILED"
        report["notes"].extend(canary_failures)
        report["notes"].append(
            "canary failed: refusing to judge claims against a "
            "tampered or blind mechanism")
        return 2, report
    report["canary"] = "ok"
    try:
        claims = _load_manifest(manifest_path)
    except ManifestBroken as exc:
        report["notes"].append(str(exc))
        return 2, report
    if not claims:
        report["verdict"] = "DORMANT"
        report["notes"].append(
            "manifest registers zero claims: DORMANT (explicit, not a "
            "pass). The first registered claim activates enforcement.")
        return 0, report
    violations = []
    try:
        for index, claim in enumerate(claims):
            claim_id, case, rounds, claimed_verdict, claimed_controller = \
                _validate_claim(mod, claim, index)
            fb = _build_false_blame(mod, claim.get("false_blame"), claim_id)
            result = mod.run_case(case, rounds=rounds, false_blame=fb)
            ok, reason = mod.verify_against_ledger(result)
            if not ok:
                raise GateError(
                    "claim " + str(claim_id) + ": mechanism contradicts "
                    "its own ledger cross-check: " + str(reason))
            got_verdict = result.verdict
            got_controller = result.record.controller
            report["claims_checked"] += 1
            if (got_verdict, got_controller) != \
                    (claimed_verdict, claimed_controller):
                violations.append({
                    "id": claim_id,
                    "case": case,
                    "rounds": rounds,
                    "claimed": claimed_verdict + "/" + claimed_controller,
                    "mechanism": got_verdict + "/" + got_controller,
                    "mechanism_reason": getattr(result, "detail", ""),
                })
    except ManifestBroken as exc:
        report["notes"].append(str(exc))
        return 2, report
    except GateError as exc:
        report["notes"].append(str(exc))
        return 2, report
    except Exception as exc:
        report["notes"].append(
            "mechanism raised during judgment: " + str(exc))
        return 2, report
    report["violations"] = violations
    if violations:
        report["verdict"] = "VIOLATION"
        return 1, report
    report["verdict"] = "PASS"
    report["notes"].append(
        str(report["claims_checked"]) + " claim(s) match the mechanism's "
        "own verdicts.")
    return 0, report


def _print_report(report):
    print("d29-boundary-gate: " + report["verdict"])
    print("  mechanism: " + str(report.get("mechanism")))
    print("  canary: " + str(report.get("canary")))
    print("  claims checked: " + str(report.get("claims_checked")))
    for v in report.get("violations", ()):
        print("  VIOLATION " + str(v["id"]) + " (case " + str(v["case"])
              + ", rounds " + str(v["rounds"]) + "): claimed "
              + str(v["claimed"]) + " but mechanism says "
              + str(v["mechanism"]))
        if v.get("mechanism_reason"):
            print("    mechanism reason: " + str(v["mechanism_reason"])[:200])
    for note in report.get("notes", ()):
        print("  note: " + str(note)[:220])


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="D29 boundary-claims gate: cold-judge registered "
                    "boundary claims against the real D29 mechanism.")
    parser.add_argument("--manifest", default=None,
                        help="path to the boundary-claims manifest "
                             "(default: tools/d29_boundary_manifest.json "
                             "under the repo root)")
    parser.add_argument("--mechanism", default=MECHANISM_REL,
                        help="repo-relative path of the D29 mechanism "
                             "module (default: " + MECHANISM_REL + ")")
    parser.add_argument("--json", action="store_true",
                        help="emit the report as JSON")
    args = parser.parse_args(argv)
    repo_root = _repo_root()
    manifest_path = args.manifest or os.path.join(repo_root, MANIFEST_REL)
    code, report = judge(repo_root, manifest_path, args.mechanism)
    if args.json:
        print(json.dumps(report, indent=2, default=str))
    else:
        _print_report(report)
    return code


if __name__ == "__main__":
    sys.exit(main())
