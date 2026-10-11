#!/usr/bin/env python3
"""D36 revocation-ordering gate — wire the RLQ engine onto the
drift-canary governance-verification path.

The D36 mechanism (drift_canary/revocation_linearization.py, on main)
is the linearization law as executable machinery: an evidence
revocation has ONE authoritative commit point, and every later
certification, projection publication, and consequential action must
respect the new eligibility state. Cached history can never restore
an older authority; independent support may establish a newer
qualification.

The fraud this law exists to prevent (the mechanism's sharpest case):
claim C is validated VALID at T1 on evidence E1. E1 is revoked at T2
(R commits). At T3 an action authorized by the T1 validation attempts
to execute — the T1 validation is DEAD, so the action is REJECTED and
revalidation is mandatory, not advisory. A naive boundary that honors
the cached T1 verdict would EXECUTE on revoked authority. Likewise a
publication built pre-R and published post-R must die with
STALE_DEPENDENCY, and the fence is synchronous — there is no
stale-certification window at the commit tick.

This gate puts that mechanism on a live operating path: every
revocation-ordering scenario registered in
tools/d36_revocation_ordering_manifest.json is cold-executed against
the REAL D36 engine (drift_canary.revocation_linearization.
AuthoritativeState). The scenario — evidence registrations,
qualifications with explicit support manifests, revocation events,
read-time validations, action commits, projection publications — is
rebuilt from the claim's own model bytes in declared order, and the
claimant's asserted outcomes must match the engine's verdicts exactly.
A scenario the law refuses — a post-revocation action asserted
AUTHORIZED, a stale pre-R publication asserted COMMITTED, a cached
validation asserted sufficient — is BLOCKED.

Sabotage resistance: before judging anything, the gate runs a fixed
canary probe (the sharpest sequence: VALID -> R commits -> action
REJECTED + validation UNQUALIFIED -> independent requalification ->
action AUTHORIZED; plus the R<P stale-publication kill) through the
loaded engine. A neutered or substituted engine that cannot tell a
dead validation from a live one fails the canary and the gate fails
closed — the gate never certifies through a blind engine.

OPERATING PATH (what this protects and how to verify it stays connected):
  Path: the drift-canary governance-verification CI path — any PR
  touching drift_canary/revocation_linearization.py, this gate, its
  manifest, or its tests.
  Trigger: the revocation-ordering gate check on pull_request /
  push-to-main.
  Block: check red (exit 1 VIOLATION or exit 2 BROKEN) blocks the merge path.
  Defect class: stale authority surviving an evidence revocation —
  post-revocation actions executing on dead validations, pre-R
  publications committing post-R, cached verdicts honored without a
  fresh read.
  Verify-still-connected: `python tools/d36_revocation_ordering_gate.py --json`
  must exit 0 DORMANT on a claim-free tree; a manifest asserting a
  post-revocation AUTHORIZED must exit 1 naming
  asserted=AUTHORIZED actual=REJECTED; scenarios present with the
  mechanism deleted must exit 2. If the workflow file disappears from
  .github/workflows/, the path is unwired — re-add it.

Exit contract (the whole point of the gate):
  0  PASS     — every registered scenario's asserted outcomes certified
                by the cold engine, exactly.
  0  DORMANT  — the manifest registers zero scenarios. Explicit, never
                a false green: the gate says "nothing to judge". The
                fixed canary still runs every run.
  1  VIOLATION— a scenario BLOCKED: the engine's verdict diverges from
                the claimant's asserted outcome. The engine's own words
                name the divergence.
  2  BROKEN   — fail-closed: manifest corrupt, unknown outcome /
                revision values, malformed scenario shape, an op the
                engine refuses, scenarios exist but the mechanism is
                absent or fails the canary. The gate never invents the
                engine and never defaults green.

The gate never pre-computes the outcome — the engine's
AuthoritativeState is the authority, exactly as a real revocation
boundary must be the authority over its own ordering.

Directive: D36 (Exact Revocation Ordering and Stale-Proof Prevention;
mechanism on main), owner naya5. Wired by the Naya 2 night-shift WIRE
lane. No merge — the merge lane owns it.
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
    "d36_revocation_ordering_manifest.json"
MECHANISM_MODULE = "drift_canary.revocation_linearization"

# The workflow runs this script as `python tools/...` (script dir on
# sys.path, not the repo root). The mechanism lives at the repo root —
# append it so the gate imports the REAL engine wherever it runs from.
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.append(str(REPO_ROOT))

VALIDATE_VERDICTS = (
    "CURRENT_QUALIFIED",
    "CURRENT_UNQUALIFIED",
    "CURRENT_STATE_UNAVAILABLE",
)
ACT_OUTCOMES = (
    "AUTHORIZED",
    "AUTHORIZED_VIA_GATEWAY",
    "REJECTED",
)
PUBLISH_VERDICTS = (
    "COMMITTED",
    "STALE_DEPENDENCY",
    "QUALIFICATION_NOT_ESTABLISHED",
    "WRITE_CONFLICT",
)

OP_NAMES = (
    "register_evidence",
    "register_qualification",
    "revoke",
    "register_projection",
    "validate",
    "act",
    "publish",
)


class GateBroken(Exception):
    """The manifest or the mechanism is untrustworthy — fail closed."""


class MechanismMissing(Exception):
    """Scenarios are registered but the D36 engine is absent."""


def _load_mechanism():
    try:
        return importlib.import_module(MECHANISM_MODULE)
    except Exception as exc:
        raise MechanismMissing(
            "D36 mechanism %r not importable: %s" % (MECHANISM_MODULE, exc))


def _canary_probe(rlq):
    """Fixed sharpest-sequence fixture through the loaded engine.

    T1: C validated VALID on E1. T2: E1 revoked (R commits). T3: the
    action authorized by the T1 validation is REJECTED and a fresh
    read is UNQUALIFIED — the T1 validation is dead. T4/T5: independent
    E2 requalifies C. T6: the action, re-authorized on fresh validation,
    is AUTHORIZED. Plus R<P: a publication built pre-R is rejected
    post-R with STALE_DEPENDENCY, and the fence is synchronous.
    """
    st = rlq.AuthoritativeState()
    e1 = st.register_evidence("E1", scope="blind-cert", purpose="certification",
                              policy_revision="LAW-v3", provenance="canary-fx")
    st.register_qualification("C", verdict="REQUALIFIED",
                              support_manifest={"E1": e1.eligibility_revision},
                              scope="blind-cert", purpose="certification",
                              policy_revision="LAW-v3")
    v1, _ = st.validate_current("C", "certification")
    if v1 != rlq.CURRENT_QUALIFIED:
        raise GateBroken("canary FAILED at T1: expected CURRENT_QUALIFIED, "
                         "got %s; loaded engine is not the D36 mechanism" % v1)
    st.commit_revocation("E1", "canary: key compromise", "blind-cert",
                         "certification", "LAW-v3", "canary-verifier")
    o3, _ = st.commit_action("ACT-1", ["C"], law_authorization=True)
    if o3 != "REJECTED":
        raise GateBroken("canary FAILED at T3: post-revocation action "
                         "expected REJECTED, got %s; the fence is blind" % o3)
    v3, _ = st.validate_current("C", "certification")
    if v3 != rlq.CURRENT_UNQUALIFIED:
        raise GateBroken("canary FAILED at T3: fresh read expected "
                         "CURRENT_UNQUALIFIED, got %s" % v3)
    # R<P: publication built pre-R dies post-R.
    st.register_projection("P-CAN", artifact_id="art-can",
                           claim_deps={"C": st.claims["C"].qualification_revision},
                           evidence_deps={"E1": e1.eligibility_revision})
    head = st.projections["P-CAN"]
    stale = rlq.ProjectionCandidate(
        projection_id="P-CAN",
        expected_head_revision=head.projection_revision,
        artifact_id="art-can-stale",
        claim_deps={"C": st.claims["C"].qualification_revision},
        evidence_manifest={"E1": e1.eligibility_revision},
        policy_revision="LAW-v3",
        asserted_claims={"C": "REQUALIFIED"},
        intended_uses=("certification",),
        fencing_token=head.fencing_token,
    )
    pv, _ = st.publish_projection(stale)
    if pv != rlq.STALE_DEPENDENCY:
        raise GateBroken("canary FAILED at R<P: stale publication expected "
                         "STALE_DEPENDENCY, got %s" % pv)
    # T4/T5/T6: independent support requalifies; fresh action executes.
    e2 = st.register_evidence("E2", scope="blind-cert", purpose="certification",
                              policy_revision="LAW-v3", provenance="canary-fx2")
    st.register_qualification("C", verdict="REQUALIFIED",
                              support_manifest={"E2": e2.eligibility_revision},
                              scope="blind-cert", purpose="certification",
                              policy_revision="LAW-v3")
    v5, _ = st.validate_current("C", "certification")
    if v5 != rlq.CURRENT_QUALIFIED:
        raise GateBroken("canary FAILED at T5: requalified claim expected "
                         "CURRENT_QUALIFIED, got %s" % v5)
    o6, _ = st.commit_action("ACT-1", ["C"], law_authorization=True)
    if o6 != "AUTHORIZED":
        raise GateBroken("canary FAILED at T6: fresh-authorized action "
                         "expected AUTHORIZED, got %s" % o6)
    return True


def _req_str(mapping, key, where):
    val = mapping.get(key)
    if not isinstance(val, str) or not val:
        raise GateBroken("%s: %r must be a non-empty string" % (where, key))
    return val


def _req_bool(mapping, key, where, default=False):
    val = mapping.get(key, default)
    if not isinstance(val, bool):
        raise GateBroken("%s: %r must be a boolean" % (where, key))
    return val


def _ev_rev(st, eid, spec, where):
    """Resolve an evidence revision pin: int (possibly stale) or
    "current" (the engine's live revision at this step)."""
    if spec == "current":
        rec = st.evidence.get(eid)
        if rec is None:
            raise GateBroken("%s: evidence %r not registered" % (where, eid))
        return rec.eligibility_revision
    if isinstance(spec, int) and not isinstance(spec, bool) and spec >= 0:
        return spec
    raise GateBroken("%s: evidence revision for %r must be a non-negative "
                     "int or \"current\", got %r" % (where, eid, spec))


def _claim_rev(st, cid, spec, where):
    if spec == "current":
        rec = st.claims.get(cid)
        if rec is None:
            raise GateBroken("%s: claim %r not registered" % (where, cid))
        return rec.qualification_revision
    if isinstance(spec, int) and not isinstance(spec, bool) and spec >= 0:
        return spec
    raise GateBroken("%s: claim revision for %r must be a non-negative "
                     "int or \"current\", got %r" % (where, cid, spec))


def _head_rev(st, pid, spec, where):
    if spec == "head":
        rec = st.projections.get(pid)
        if rec is None:
            raise GateBroken("%s: projection %r not registered" % (where, pid))
        return rec.projection_revision
    if isinstance(spec, int) and not isinstance(spec, bool) and spec >= 0:
        return spec
    raise GateBroken("%s: expected_head_revision must be a non-negative "
                     "int or \"head\", got %r" % (where, spec))


def _fencing(st, pid, spec, where):
    if spec == "head":
        rec = st.projections.get(pid)
        if rec is None:
            raise GateBroken("%s: projection %r not registered" % (where, pid))
        return rec.fencing_token
    if isinstance(spec, int) and not isinstance(spec, bool) and spec >= 0:
        return spec
    raise GateBroken("%s: fencing_token must be a non-negative int or "
                     "\"head\", got %r" % (where, spec))


def _support_map(st, raw, where):
    if not isinstance(raw, dict) or not raw:
        raise GateBroken("%s: support must be a non-empty object "
                         "mapping evidence_id to revision" % where)
    return {eid: _ev_rev(st, eid, spec, where)
            for eid, spec in raw.items()}


def _checked_call(where, fn, *args, **kwargs):
    """Engine ops/checks must not blow up on well-formed scenarios —
    an exception is a broken gate input or a broken engine: fail closed."""
    try:
        return fn(*args, **kwargs)
    except GateBroken:
        raise
    except Exception as exc:
        raise GateBroken("%s: engine raised %s: %s"
                         % (where, type(exc).__name__, exc))


def _run_steps(rlq, name, steps):
    """Replay one scenario's steps against a fresh engine. Returns the
    list of violation strings (empty == certified)."""
    where0 = "scenario %r" % name
    if not isinstance(steps, list) or not steps:
        raise GateBroken(where0 + ": 'steps' must be a non-empty list")
    st = rlq.AuthoritativeState()
    violations = []
    for i, step in enumerate(steps):
        where = "%s step[%d]" % (where0, i)
        if not isinstance(step, dict):
            raise GateBroken(where + ": must be an object")
        op = step.get("op")
        if op not in OP_NAMES:
            raise GateBroken(where + ": unknown op %r (want one of %s)"
                             % (op, ", ".join(OP_NAMES)))

        if op == "register_evidence":
            _checked_call(
                where, st.register_evidence,
                _req_str(step, "evidence_id", where),
                scope=_req_str(step, "scope", where),
                purpose=_req_str(step, "purpose", where),
                policy_revision=_req_str(step, "policy_revision", where),
                provenance=_req_str(step, "provenance", where))

        elif op == "register_qualification":
            _checked_call(
                where, st.register_qualification,
                _req_str(step, "claim_id", where),
                verdict=_req_str(step, "verdict", where),
                support_manifest=_support_map(
                    st, step.get("support"), where + " support"),
                scope=_req_str(step, "scope", where),
                purpose=_req_str(step, "purpose", where),
                policy_revision=_req_str(step, "policy_revision", where))

        elif op == "revoke":
            _checked_call(
                where, st.commit_revocation,
                _req_str(step, "evidence_id", where),
                _req_str(step, "reason", where),
                _req_str(step, "scope", where),
                _req_str(step, "purpose", where),
                _req_str(step, "policy_revision", where),
                _req_str(step, "provenance", where))

        elif op == "register_projection":
            claim_deps = step.get("claim_deps")
            evidence_deps = step.get("evidence_deps")
            if not isinstance(claim_deps, dict) or not claim_deps:
                raise GateBroken(where + ": claim_deps must be a non-empty object")
            if not isinstance(evidence_deps, dict) or not evidence_deps:
                raise GateBroken(where + ": evidence_deps must be a non-empty object")
            _checked_call(
                where, st.register_projection,
                _req_str(step, "projection_id", where),
                artifact_id=_req_str(step, "artifact_id", where),
                claim_deps={cid: _claim_rev(st, cid, spec, where)
                            for cid, spec in claim_deps.items()},
                evidence_deps={eid: _ev_rev(st, eid, spec, where)
                               for eid, spec in evidence_deps.items()})

        elif op == "validate":
            asserted = step.get("asserted")
            if asserted not in VALIDATE_VERDICTS:
                raise GateBroken(where + ": asserted must be one of %s, got %r"
                                 % (", ".join(VALIDATE_VERDICTS), asserted))
            actual, _ = _checked_call(
                where, st.validate_current,
                _req_str(step, "claim_id", where),
                _req_str(step, "intended_use", where),
                mode=step.get("mode", "certification"))
            if actual != asserted:
                violations.append(
                    "%s: validate claim %r: asserted=%s actual=%s"
                    % (where, step["claim_id"], asserted, actual))

        elif op == "act":
            asserted = step.get("asserted")
            if asserted not in ACT_OUTCOMES:
                raise GateBroken(where + ": asserted must be one of %s, got %r"
                                 % (", ".join(ACT_OUTCOMES), asserted))
            required = step.get("required_claims")
            if (not isinstance(required, list) or not required
                    or not all(isinstance(c, str) for c in required)):
                raise GateBroken(where + ": required_claims must be a "
                                         "non-empty list of strings")
            actual, _ = _checked_call(
                where, st.commit_action,
                _req_str(step, "action_id", where),
                required,
                law_authorization=_req_bool(step, "law_authorization", where),
                external=_req_bool(step, "external", where, default=False))
            if actual != asserted:
                violations.append(
                    "%s: act %r: asserted=%s actual=%s"
                    % (where, step["action_id"], asserted, actual))

        elif op == "publish":
            asserted = step.get("asserted")
            if asserted not in PUBLISH_VERDICTS:
                raise GateBroken(where + ": asserted must be one of %s, got %r"
                                 % (", ".join(PUBLISH_VERDICTS), asserted))
            pid = _req_str(step, "projection_id", where)
            claim_deps = step.get("claim_deps")
            evidence_manifest = step.get("evidence_manifest")
            if not isinstance(claim_deps, dict) or not claim_deps:
                raise GateBroken(where + ": claim_deps must be a non-empty object")
            if not isinstance(evidence_manifest, dict) or not evidence_manifest:
                raise GateBroken(where + ": evidence_manifest must be a "
                                         "non-empty object")
            asserted_claims = step.get("asserted_claims")
            if (not isinstance(asserted_claims, dict) or not asserted_claims
                    or not all(isinstance(k, str) and isinstance(v, str)
                               for k, v in asserted_claims.items())):
                raise GateBroken(where + ": asserted_claims must be a "
                                         "non-empty string->string object")
            intended_uses = step.get("intended_uses")
            if (not isinstance(intended_uses, list) or not intended_uses
                    or not all(isinstance(u, str) for u in intended_uses)):
                raise GateBroken(where + ": intended_uses must be a non-empty "
                                         "list of strings")
            candidate = rlq.ProjectionCandidate(
                projection_id=pid,
                expected_head_revision=_head_rev(
                    st, pid, step.get("expected_head_revision"), where),
                artifact_id=_req_str(step, "artifact_id", where),
                claim_deps={cid: _claim_rev(st, cid, spec, where)
                            for cid, spec in claim_deps.items()},
                evidence_manifest={eid: _ev_rev(st, eid, spec, where)
                                   for eid, spec in evidence_manifest.items()},
                policy_revision=_req_str(step, "policy_revision", where),
                asserted_claims=dict(asserted_claims),
                intended_uses=tuple(intended_uses),
                fencing_token=_fencing(st, pid, step.get("fencing_token"), where),
            )
            actual, _ = _checked_call(where, st.publish_projection, candidate)
            if actual != asserted:
                violations.append(
                    "%s: publish %r: asserted=%s actual=%s"
                    % (where, pid, asserted, actual))

    return violations


def _load_manifest(path):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except FileNotFoundError:
        return {"scenarios": []}
    except (json.JSONDecodeError, OSError) as exc:
        raise GateBroken("manifest unreadable: %s" % exc)
    if not isinstance(data, dict):
        raise GateBroken("manifest must be a JSON object")
    scenarios = data.get("scenarios", [])
    if not isinstance(scenarios, list):
        raise GateBroken("manifest 'scenarios' must be a list")
    seen = set()
    for i, sc in enumerate(scenarios):
        where = "scenario[%d]" % i
        if not isinstance(sc, dict):
            raise GateBroken(where + ": must be an object")
        name = sc.get("name")
        if not isinstance(name, str) or not name:
            raise GateBroken(where + ": 'name' must be a non-empty string")
        if name in seen:
            raise GateBroken("duplicate scenario name %r" % name)
        seen.add(name)
    return data


def run_gate(manifest_path):
    """Returns (exit_code, report_dict)."""
    try:
        rlq = _load_mechanism()
    except MechanismMissing as exc:
        # Zero scenarios + absent mechanism: nothing registered, nothing
        # to judge — but the absence is still worth naming loudly.
        try:
            data = _load_manifest(manifest_path)
            if not data["scenarios"]:
                return EXIT_PASS, {"status": "DORMANT",
                                   "note": "mechanism absent, zero scenarios"}
        except GateBroken:
            pass
        return EXIT_BROKEN, {"status": "BROKEN", "error": str(exc)}
    try:
        _canary_probe(rlq)
    except GateBroken as exc:
        return EXIT_BROKEN, {"status": "BROKEN", "error": str(exc)}
    try:
        data = _load_manifest(manifest_path)
    except GateBroken as exc:
        return EXIT_BROKEN, {"status": "BROKEN", "error": str(exc)}
    scenarios = data["scenarios"]
    if not scenarios:
        return EXIT_PASS, {"status": "DORMANT",
                           "detail": "canary passed; zero scenarios registered"}
    all_violations = []
    try:
        for sc in scenarios:
            all_violations.extend(
                _run_steps(rlq, sc["name"], sc.get("steps")))
    except GateBroken as exc:
        return EXIT_BROKEN, {"status": "BROKEN", "error": str(exc)}
    if all_violations:
        return EXIT_VIOLATION, {"status": "VIOLATION",
                                "violations": all_violations}
    return EXIT_PASS, {"status": "PASS",
                       "scenarios": len(scenarios)}


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="D36 revocation-ordering claims gate")
    ap.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    ap.add_argument("--json", action="store_true",
                    help="print the report as JSON")
    args = ap.parse_args(argv)
    code, report = run_gate(args.manifest)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(report["status"])
        for key in ("violations", "error", "detail", "note"):
            if key in report:
                val = report[key]
                if isinstance(val, list):
                    for v in val:
                        print(" -", v)
                else:
                    print(" %s: %s" % (key, val))
    return code


if __name__ == "__main__":
    sys.exit(main())
