#!/usr/bin/env python3
"""D32 evidence-bounded uncertainty-propagation gate - wire the engine onto the
drift-canary governance-verification path.

The D32 mechanism (drift_canary/uncertainty_propagation.py, owner naya2) is the
uncertainty law as executable machinery: a downstream claim can never become
more certain, broader, or more causally specific than its admissible evidence
supports - but uncertainty in one upstream source must not invalidate a
genuinely independent, sufficient alternative. Uncertainty propagates only
along the claims and evidence dependencies that actually require it.

The fraud this law exists to prevent (the mechanism's sharpest case): a
"possible" causal hypothesis copied through a summary, index entry, or
successor package comes back "verified" - uncertainty laundered into
certainty by derivation alone. The real engine refuses: derive_modality
NEVER upgrades modality; only new admissible evidence - a new assessment,
not a derivation - can upgrade. The twin fraud: a conflict on P is used to
license an arbitrary conclusion about an unrelated Q. The real engine keeps
Q at UNDETERMINED - reasoning stays nonexplosive.

This gate puts that mechanism on a live operating path: every uncertainty
scenario registered in tools/d32_uncertainty_manifest.json is cold-executed
against the REAL D32 engine (drift_canary.uncertainty_propagation). The
scenario is rebuilt from the claim's own model bytes, and the claimant's
asserted post-propagation standings must match the engine's recomputed
standings exactly. A scenario the law refuses - an upgraded modality, a
conclusion licensed from an unrelated conflict, an independent claim
invalidated by someone else's observation gap - is BLOCKED.

Sabotage resistance: before judging anything, the gate runs three fixed
canary probes through the loaded engine - (1) derive_modality("possible",
"summarize") must stay "possible"; (2) nonexplosive_check(True, q) must
leave q UNDETERMINED; (3) UncertaintyAnnotation(kind="invented") must
RAISE (the engine refuses invented vocabulary). A neutered or substituted
engine that upgrades, explodes, or accepts invented kinds fails the canary
and the gate fails closed - the gate never certifies through a blind engine.

OPERATING PATH (what this protects and how to verify it stays connected):
  Path: the drift-canary governance-verification CI path - any PR
  touching drift_canary/uncertainty_propagation.py, this gate, its
  manifest, or its tests.
  Trigger: the uncertainty gate check on pull_request / push-to-main.
  Block: check red (exit 1 VIOLATION or exit 2 BROKEN) blocks the merge path.
  Defect class: uncertainty laundered into certainty by derivation;
  conclusions licensed from unrelated conflicts; independent claims
  invalidated by someone else's observation gap; invented uncertainty
  vocabulary smuggled past the kind discipline.
  Verify-still-connected: `python tools/d32_uncertainty_gate.py --json`
  must exit 0 DORMANT on a claim-free tree; registering the manifest's
  worked _example as a claim must exit 1 naming asserted=verified
  actual=possible; scenarios present with the mechanism deleted must
  exit 2. If the workflow file disappears from .github/workflows/,
  the path is unwired - re-add it.

Exit contract (the whole point of the gate):
  0  PASS     - every registered scenario's asserted standings certified
                by the cold engine, exactly.
  0  DORMANT  - manifest absent or registers zero scenarios. Explicit,
                never a false green: the gate says "nothing to judge".
  1  VIOLATION- a scenario BLOCKED: the engine's recomputed standing
                diverges from the claimant's asserted one. The mechanism's
                own words name the divergence.
  2  BROKEN   - fail-closed: manifest corrupt, unknown modality / verdict /
                kind / relationship / coverage values, malformed scenario
                shape, an asserted claim the engine cannot construct,
                scenarios exist but the mechanism is absent or fails the
                canary. The gate never invents the engine and never
                defaults an unknown.

The gate never pre-computes the outcome - the engine's own functions are
the authority, exactly as a real uncertainty boundary must be the
authority over its own propagation.

Directive: D32 (Evidence-Bounded Uncertainty Propagation; mechanism on
main drift_canary/uncertainty_propagation.py), owner naya2. Wired by the
Naya 2 night-shift BUILD lane. No merge - the merge lane owns it.
"""

import argparse
import importlib
import json
import sys
from pathlib import Path

EXIT_PASS = 0
EXIT_VIOLATION = 1
EXIT_BROKEN = 2

DEFAULT_MANIFEST = Path(__file__).resolve().parent / \
    "d32_uncertainty_manifest.json"
MECHANISM_MODULE = "drift_canary.uncertainty_propagation"

# The workflow runs this script as `python tools/...` (script dir on
# sys.path, not the repo root). The mechanism lives at the repo root -
# append it so the gate imports the REAL engine wherever it runs from.
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.append(str(REPO_ROOT))

SCENARIO_TYPES = (
    "modality_derivation",
    "nonexplosion",
    "observation_limit",
    "edge_propagation",
)

DERIVATIONS = (
    "copy", "summarize", "index", "repeat", "cite",
    "project", "handover", "new_admissible_evidence",
)

# propagate_observation_limit speaks its own standings vocabulary, not
# REGION_VERDICTS: a gap invalidates only dependent inferences.
OBS_LIMIT_STANDINGS = (
    "UNAFFECTED",
    "PRESERVED_VIA_INDEPENDENT_EVIDENCE",
    "UNDETERMINED",
)


class GateBroken(Exception):
    """The manifest or the mechanism is untrustworthy - fail closed."""


class MechanismMissing(Exception):
    """Scenarios are registered but the D32 engine is absent."""


def _load_mechanism():
    try:
        return importlib.import_module(MECHANISM_MODULE)
    except Exception as exc:
        raise MechanismMissing(
            "D32 mechanism %r not importable: %s" % (MECHANISM_MODULE, exc))


def _canary_probe(u):
    """Three fixed probes through the loaded engine.

    (1) A "possible" cause summarized must stay "possible" - derivation
    never upgrades modality. (2) A conflict on P must leave unrelated Q
    UNDETERMINED - reasoning never explodes. (3) An invented uncertainty
    kind must be refused - the vocabulary is closed. Anything else means
    the loaded engine is not the D32 mechanism - fail closed.
    """
    mod, rule = u.derive_modality("possible", "summarize")
    if mod != "possible":
        raise GateBroken(
            "canary FAILED: derivation upgraded modality "
            "(possible -> %s via %s); loaded engine is not the D32 "
            "mechanism" % (mod, rule))
    standing, q, reason = u.nonexplosive_check(True, "CANARY-Q")
    if standing != "UNDETERMINED" or q != "CANARY-Q":
        raise GateBroken(
            "canary FAILED: conflict on P licensed %s for unrelated Q "
            "(%s); loaded engine is not the D32 mechanism"
            % (standing, reason))
    try:
        u.UncertaintyAnnotation(
            kind="invented_kind", proposition="canary",
            scope_region="global", detail="canary")
    except (AssertionError, ValueError):
        pass
    else:
        raise GateBroken(
            "canary FAILED: engine accepted an invented uncertainty kind; "
            "the kind discipline is broken - loaded engine is not the "
            "D32 mechanism")
    return True


def _req_str(mapping, key, where):
    val = mapping.get(key)
    if not isinstance(val, str) or not val:
        raise GateBroken("%s: %r must be a non-empty string" % (where, key))
    return val


def _modality(u, value, where):
    if value not in u.MODALITIES:
        raise GateBroken(
            "%s: unknown modality %r (want one of %s)"
            % (where, value, ", ".join(u.MODALITIES)))
    return value


def _verdict(u, value, where):
    if value not in u.REGION_VERDICTS:
        raise GateBroken(
            "%s: unknown verdict %r (want one of %s)"
            % (where, value, ", ".join(u.REGION_VERDICTS)))
    return value


def _relationship(u, value, where):
    if value not in u.PROPAGATION_SEMANTICS:
        raise GateBroken(
            "%s: unknown relationship %r" % (where, value))
    return value


def _coverage_state(u, value, where):
    if value not in u.COVERAGE_STATES:
        raise GateBroken(
            "%s: unknown coverage state %r (want one of %s)"
            % (where, value, ", ".join(u.COVERAGE_STATES)))
    return value


def _judge_modality_derivation(u, name, spec):
    where = "scenario %r" % name
    src = _modality(u, _req_str(spec, "source_modality", where), where)
    derivation = _req_str(spec, "derivation", where)
    if derivation not in DERIVATIONS and not derivation.startswith("unknown_"):
        raise GateBroken(
            "%s: unknown derivation %r (derivations: %s; unknown_* "
            "treated as copy by the engine)"
            % (where, derivation, ", ".join(DERIVATIONS)))
    asserted = _modality(u, _req_str(spec, "asserted_modality", where), where)
    try:
        actual, rule = u.derive_modality(src, derivation)
    except (AssertionError, ValueError) as exc:
        raise GateBroken(where + ": engine refused: %s" % exc)
    if actual != asserted:
        return ("VIOLATION",
                "scenario %r: asserted modality=%s but the engine "
                "recomputed modality=%s (%s)" % (name, asserted, actual, rule))
    return ("PASS", "modality %s via %s certified (%s)"
            % (actual, derivation, rule))


def _judge_nonexplosion(u, name, spec):
    where = "scenario %r" % name
    conflict = spec.get("conflict_on_p")
    if not isinstance(conflict, bool):
        raise GateBroken(where + ": 'conflict_on_p' must be boolean")
    q = _req_str(spec, "unrelated_q", where)
    asserted = _verdict(u, _req_str(spec, "asserted_q_standing", where), where)
    actual, actual_q, reason = u.nonexplosive_check(conflict, q)
    if actual_q != q:
        raise GateBroken(
            "%s: engine renamed the unrelated claim %r -> %r"
            % (where, q, actual_q))
    if actual != asserted:
        return ("VIOLATION",
                "scenario %r: asserted Q standing=%s but the engine "
                "recomputed standing=%s (%s)" % (name, asserted, actual, reason))
    return ("PASS", "Q stays %s under conflict_on_p=%s (%s)"
            % (actual, conflict, reason))


def _judge_observation_limit(u, name, spec):
    where = "scenario %r" % name
    raw_claims = spec.get("claims")
    if not isinstance(raw_claims, list) or not raw_claims:
        raise GateBroken(where + ": 'claims' must be a non-empty list")
    claims = []
    for i, c in enumerate(raw_claims):
        cw = "%s claim[%d]" % (where, i)
        if not isinstance(c, dict):
            raise GateBroken(cw + ": must be an object")
        cid = _req_str(c, "claim_id", cw)
        depends = c.get("depends_on_gap")
        if not isinstance(depends, bool):
            raise GateBroken(cw + ": 'depends_on_gap' must be boolean")
        verif = c.get("verifiable_elsewhere")
        if not isinstance(verif, bool):
            raise GateBroken(cw + ": 'verifiable_elsewhere' must be boolean")
        claims.append((cid, depends, verif))
    raw_gap = spec.get("gap")
    if not isinstance(raw_gap, dict):
        raise GateBroken(where + ": 'gap' must be an object")
    gap = u.ObservationCoverage(
        source=_req_str(raw_gap, "source", where + " gap"),
        event_type=_req_str(raw_gap, "event_type", where + " gap"),
        resource=raw_gap.get("resource", "any"),
        interval=_req_str(raw_gap, "interval", where + " gap"),
        state=_coverage_state(
            u, _req_str(raw_gap, "state", where + " gap"), where + " gap"),
    )
    asserted = spec.get("asserted")
    if not isinstance(asserted, dict) or not asserted:
        raise GateBroken(
            where + ": 'asserted' must be a non-empty object")
    actual = u.propagate_observation_limit(tuple(claims), gap)
    for cid, want in asserted.items():
        cw = "%s asserted %r" % (where, cid)
        if not isinstance(want, str) or want not in OBS_LIMIT_STANDINGS:
            raise GateBroken(
                "%s: unknown observation-limit standing %r (want one of %s)"
                % (cw, want, ", ".join(OBS_LIMIT_STANDINGS)))
        want_standing = want
        if cid not in actual:
            raise GateBroken(cw + ": claim not in scenario")
        got, reason = actual[cid]
        if got != want_standing:
            return ("VIOLATION",
                    "scenario %r claim %r: asserted standing=%s but the "
                    "engine recomputed standing=%s (%s)"
                    % (name, cid, want_standing, got, reason))
    return ("PASS", "%d claim standings certified" % len(asserted))


def _judge_edge_propagation(u, name, spec):
    where = "scenario %r" % name
    parent_status = _verdict(
        u, _req_str(spec, "parent_status", where), where)
    relationship = _relationship(
        u, _req_str(spec, "relationship", where), where)
    parent_modality = _modality(
        u, _req_str(spec, "parent_modality", where), where)
    scope_restriction = spec.get("scope_restriction", "")
    if not isinstance(scope_restriction, str):
        raise GateBroken(where + ": 'scope_restriction' must be a string")
    asserted = spec.get("asserted_child")
    if not isinstance(asserted, dict):
        raise GateBroken(where + ": 'asserted_child' must be an object")
    want_status = _verdict(
        u, _req_str(asserted, "status", where + " asserted_child"),
        where + " asserted_child")
    want_modality = _modality(
        u, _req_str(asserted, "modality", where + " asserted_child"),
        where + " asserted_child")
    try:
        actual_status, actual_modality, rule = u.propagate_along_edge(
            parent_status, relationship,
            parent_modality=parent_modality,
            scope_restriction=scope_restriction)
    except (AssertionError, ValueError) as exc:
        raise GateBroken(where + ": engine refused: %s" % exc)
    if actual_status != want_status or actual_modality != want_modality:
        return ("VIOLATION",
                "scenario %r: asserted child=(%s, %s) but the engine "
                "recomputed child=(%s, %s) (%s)"
                % (name, want_status, want_modality,
                   actual_status, actual_modality, rule))
    return ("PASS", "edge %s certified (%s)" % (relationship, rule))


_JUDGES = {
    "modality_derivation": _judge_modality_derivation,
    "nonexplosion": _judge_nonexplosion,
    "observation_limit": _judge_observation_limit,
    "edge_propagation": _judge_edge_propagation,
}


def _judge_scenario(u, name, spec):
    """Returns (verdict, detail). verdict in PASS/VIOLATION; BROKEN raises."""
    if not isinstance(spec, dict):
        raise GateBroken("scenario %r: must be an object" % name)
    stype = spec.get("type")
    if stype not in _JUDGES:
        raise GateBroken(
            "scenario %r: unknown type %r (want one of %s)"
            % (name, stype, ", ".join(SCENARIO_TYPES)))
    return _JUDGES[stype](u, name, spec)


def _load_manifest(path):
    try:
        with open(path) as fh:
            data = json.load(fh)
    except FileNotFoundError:
        return {}
    except (json.JSONDecodeError, OSError) as exc:
        raise GateBroken("manifest %s unreadable: %s" % (path, exc))
    if not isinstance(data, dict):
        raise GateBroken("manifest %s: top level must be an object" % path)
    scenarios = data.get("scenarios", {})
    if not isinstance(scenarios, dict):
        raise GateBroken("manifest %s: 'scenarios' must be an object" % path)
    # Worked examples (leading underscore) are documentation, never judged.
    live = {k: v for k, v in scenarios.items() if not k.startswith("_")}
    return live


def run_gate(manifest_path=None):
    """Returns (exit_code, payload_dict). Never raises on bad input."""
    manifest_path = Path(manifest_path or DEFAULT_MANIFEST)
    try:
        live = _load_manifest(manifest_path)
    except GateBroken as exc:
        return (EXIT_BROKEN, {"status": "BROKEN", "reason": str(exc)})
    if not live:
        return (EXIT_PASS, {"status": "DORMANT",
                            "reason": "no live scenarios registered"})
    try:
        u = _load_mechanism()
    except MechanismMissing as exc:
        return (EXIT_BROKEN, {"status": "BROKEN", "reason": str(exc)})
    try:
        _canary_probe(u)
    except GateBroken as exc:
        return (EXIT_BROKEN, {"status": "BROKEN", "reason": str(exc)})
    except Exception as exc:
        return (EXIT_BROKEN, {"status": "BROKEN",
                              "reason": "canary probe crashed: %s" % exc})
    judged = []
    for name, spec in live.items():
        try:
            verdict, detail = _judge_scenario(u, name, spec)
        except GateBroken as exc:
            return (EXIT_BROKEN, {"status": "BROKEN", "reason": str(exc)})
        except Exception as exc:
            return (EXIT_BROKEN, {"status": "BROKEN",
                                  "reason": "scenario %r crashed: %s"
                                  % (name, exc)})
        if verdict == "VIOLATION":
            return (EXIT_VIOLATION, {"status": "VIOLATION",
                                    "scenario": name, "detail": detail})
        judged.append({"scenario": name, "detail": detail})
    return (EXIT_PASS, {"status": "PASS", "judged": judged})


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="D32 uncertainty-propagation wire gate")
    ap.add_argument("--manifest", default=None)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    code, payload = run_gate(args.manifest)
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(payload["status"] + ": " +
              payload.get("detail", payload.get("reason", "")))
    return code


if __name__ == "__main__":
    sys.exit(main())
