#!/usr/bin/env python3
"""D64 dependency-order verification gate — wire the engine onto the
drift-canary governance-verification path.

The D64 mechanism (drift_canary/dependency_ordered_verification.py,
PR #2323) is the dependency-ordered verification law as executable
machinery (AER-LIVE-9): governance invariants are verified
prerequisites-first in a canonical topological order, but failures are
diagnosed in the order they actually happened (execution order) —
verification order and causal order are two different jobs. Three
verdicts, never two: PROVEN_TRUE needs a named proof and PROVEN_TRUE
transitive prerequisites; PROVEN_FALSE needs a valid, replaying,
minimal witness or a falsified prerequisite; UNDETERMINED carries no
witness and no proof and never collapses into FALSE. Every claimed
failure must replay as a real, minimal, checkable step sequence under
the original model — or the claim dies (a failed witness kills the
certificate and demotes the invariant to UNDETERMINED, never to
PROVEN_FALSE). Cycles get declared joint invariants deferred to
AER-LIVE-10 — never an invented ordering. Declared layers flow forward
only. The cold verifier rebuilds the certificate from bytes alone and
re-runs every check; anything malformed fails closed.

The frauds this law exists to prevent (the naive checker in the
mechanism demonstrates all three, and the mechanism's tests prove it
wrong): (1) the spec's visited-set topological sort silently returns a
prerequisite-violating order on cyclic graphs — no cycle detection;
(2) the primary failure diagnosed in VERIFICATION order instead of the
execution order where it actually happened first; (3) UNDETERMINED
collapsed into FALSE — invented failure (F6: timing stays UNDETERMINED
when the LAW-effective-time evidence is missing; the naive checker
declares it PROVEN_FALSE with primary "timing").

This gate puts that mechanism on a live operating path: every
verification claim registered in
tools/d64_dependency_order_manifest.json is cold-judged by the REAL
D64 engine, reconstructed from the claim's own certificate bytes via
independent_verify. The claimant asserts a verdict summary (VERIFIED
with primary/dependent failures and per-invariant verdicts, or
REJECTED); the gate recomputes the engine's judgment from the bytes
and demands byte-exact agreement. A claim the law refuses — a
certificate rejected for an invented ordering, a bad witness, an
unsound TRUE, an unproven FALSE, a collapsed UNDETERMINED, a
misdiagnosed primary, malformed certificate bytes, or a
cross-obligation certificate — is BLOCKED. The gate also dogfoods the
mechanism's own integrity on every judged verdict: accepted verdicts
carry no failure, rejected verdicts name their reason, the verification
order is re-proven as a valid topological order over the certificate's
own prerequisite graph (the gate's own Kahn pass — no invented
ordering survives), no DEFERRED invariant rides as a failure, and the
serialization roundtrip is byte-stable.

OPERATING PATH (what this protects and how to verify it stays connected):
  Path: the drift-canary governance-verification CI path — any PR
  touching drift_canary/dependency_ordered_verification.py, this gate,
  its manifest, or its tests.
  Trigger: the dependency-order-verification check on pull_request /
  push-to-main.
  Block: check red (exit 1 VIOLATION or exit 2 BROKEN) blocks the merge path.
  Defect class: verification claims over dependency-order certificates
  that the D64 law refuses — invented topological orderings, wrong-order
  diagnoses, UNDETERMINED collapsed to FALSE, unsound TRUE, unproven
  FALSE, failed witnesses claimed as verdicts, uncovered cycles,
  spurious joints, backward layering, malformed certificates,
  cross-obligation certificates.
  Verify-still-connected: `python tools/d64_dependency_order_gate.py
  --json` must exit 0 DORMANT on a claim-free tree; registering the
  manifest's worked AE-EXAMPLE claim must exit 1 naming the collapsed
  F6 verdicts; claims present with the mechanism deleted must exit 2.
  If the workflow file disappears from .github/workflows/, the path is
  unwired — re-add it.

Exit contract (the whole point of the gate):
  0  PASS     — every registered claim certified by the cold engine.
  0  DORMANT  — manifest absent or registers zero claims. Explicit, never a
                false green: the gate says "nothing to judge".
  1  VIOLATION— a claim BLOCKED: the law refuses it (independent_verify
                rejects, or the claimant's asserted verdict summary
                diverges from the engine's recomputed judgment — the
                collapse/wrong-primary/invented-verdict frauds live here).
                The mechanism's own words name the refusal.
  2  BROKEN   — fail-closed: manifest corrupt, claim fields untrustworthy,
                an unknown assertion value, claims exist but the mechanism
                is absent, or the mechanism's own verdict invariants broke
                (topo-order dogfood failed). The gate never invents the
                engine and never defaults an unknown.

The gate never invents fields: unknown assertions, malformed shapes, or
missing keys are BROKEN, not defaulted. Claim CONTENT refused by the law is
VIOLATION, not BROKEN — the distinction is whose trust broke: the
manifest's (BROKEN) or the claim's (VIOLATION).

Structural note: the gate compares the certificate's own obligation_id
against the claim's obligation_id — a cross-obligation certificate is
refused. Judgment is structurally bound to the claim's obligation.

Directive: D64 (Dependency-Ordered Invariant Verification, AER-LIVE-9,
Naya 3's intel #2175/6102689568), owner naya2. Wired by the night-shift
WIRE lane. No merge — the merge lane owns it.
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
    "d64_dependency_order_manifest.json"
MECHANISM_MODULE = "drift_canary.dependency_ordered_verification"

# The workflow runs this script as `python tools/...` (script dir on
# sys.path, not the repo root). The mechanism lives at the repo root —
# append it so the gate imports the REAL engine wherever it runs from.
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.append(str(REPO_ROOT))

ASSERT_VERIFIED = "VERIFIED"
ASSERT_REJECTED = "REJECTED"
KNOWN_ASSERTS = (ASSERT_VERIFIED, ASSERT_REJECTED)

VERDICT_VALUES = ("PROVEN_TRUE", "PROVEN_FALSE", "UNDETERMINED", "DEFERRED")


class GateBroken(Exception):
    """The manifest or the mechanism is untrustworthy — fail closed."""


class MechanismMissing(Exception):
    """Claims are registered but the D64 engine is absent."""


def _load_mechanism():
    try:
        return importlib.import_module(MECHANISM_MODULE)
    except Exception as exc:
        raise MechanismMissing(
            f"D64 mechanism {MECHANISM_MODULE!r} not importable: {exc}")


def _load_manifest(path):
    """Fail-closed loader. Returns None when absent (DORMANT), the data
    when present, raises GateBroken on anything untrustworthy."""
    p = Path(path)
    if not p.exists():
        return None
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:
        raise GateBroken(f"manifest {p} is not valid JSON: {exc}")
    if not isinstance(data, dict):
        raise GateBroken(
            f"manifest {p} must be a JSON object, got "
            f"{type(data).__name__}")
    claims = data.get("claims", None)
    if not isinstance(claims, list):
        raise GateBroken(
            f"manifest {p}: 'claims' must be a list, got "
            f"{type(claims).__name__}")
    seen = set()
    for i, entry in enumerate(claims):
        if not isinstance(entry, dict):
            raise GateBroken(
                f"manifest {p}: claim[{i}] must be an object, got "
                f"{type(entry).__name__}")
        cid = entry.get("id")
        if not isinstance(cid, str) or not cid:
            raise GateBroken(
                f"manifest {p}: claim[{i}] has no usable 'id'")
        if cid in seen:
            raise GateBroken(
                f"manifest {p}: duplicate claim id {cid!r} — refusing "
                f"to judge an ambiguous register")
        seen.add(cid)
    return data


def _check_claim_shape(entry, manifest_path):
    """Structural trust of the claim's fields. Raises GateBroken on
    anything the gate cannot trust — never defaulted."""
    cid = entry.get("id")
    loc = f"manifest {manifest_path}: claim {cid!r}"
    obligation_id = entry.get("obligation_id")
    if not isinstance(obligation_id, str) or not obligation_id:
        raise GateBroken(f"{loc}: 'obligation_id' must be a non-empty "
                         f"string")
    asserts = entry.get("asserts")
    if asserts not in KNOWN_ASSERTS:
        raise GateBroken(
            f"{loc}: 'asserts' must be one of {KNOWN_ASSERTS}, got "
            f"{asserts!r} — the gate never defaults an unknown assertion")
    certificate = entry.get("certificate")
    if not isinstance(certificate, dict):
        raise GateBroken(
            f"{loc}: 'certificate' must be a JSON object, got "
            f"{type(certificate).__name__}")
    asserted_verdict = None
    if asserts == ASSERT_VERIFIED:
        asserted_verdict = entry.get("verdict")
        if not isinstance(asserted_verdict, dict):
            raise GateBroken(
                f"{loc}: asserting {ASSERT_VERIFIED} requires a 'verdict' "
                f"object with primary_failures, dependent_failures and "
                f"invariant_verdicts")
        for key in ("primary_failures", "dependent_failures"):
            val = asserted_verdict.get(key)
            if not isinstance(val, list) or \
                    not all(isinstance(x, str) for x in val):
                raise GateBroken(
                    f"{loc}: 'verdict.{key}' must be a list of strings")
        inv_verdicts = asserted_verdict.get("invariant_verdicts")
        if not isinstance(inv_verdicts, dict) or not inv_verdicts or \
                not all(isinstance(k, str) and v in VERDICT_VALUES
                        for k, v in inv_verdicts.items()):
            raise GateBroken(
                f"{loc}: 'verdict.invariant_verdicts' must be a non-empty "
                f"map of name -> one of {VERDICT_VALUES}")
    return obligation_id, asserts, certificate, asserted_verdict


def _topo_order_valid(cert_dict, verification_order, deferred_names):
    """The gate's own Kahn pass: every non-deferred invariant's
    non-deferred prerequisites must precede it. Returns (ok, reason)."""
    prereq = {}
    for inv in cert_dict.get("invariants", []):
        name = inv.get("name")
        pres = inv.get("prerequisites", [])
        if not isinstance(name, str) or not isinstance(pres, list):
            return False, "certificate invariant shape untrustworthy"
        prereq[name] = [p for p in pres if p not in deferred_names]
    live = [n for n in prereq if n not in deferred_names]
    seen = set()
    for name in verification_order:
        if name in deferred_names:
            return False, (f"verification order names deferred invariant "
                           f"{name!r}")
        if name not in prereq:
            return False, (f"verification order names unknown invariant "
                           f"{name!r}")
        for p in prereq[name]:
            if p not in seen:
                return False, (f"invented ordering: {name!r} verified "
                               f"before its prerequisite {p!r}")
        seen.add(name)
    if set(live) != set(verification_order):
        missing = sorted(set(live) - set(verification_order))
        extra = sorted(set(verification_order) - set(live))
        return False, (f"verification order does not cover the live "
                       f"invariants (missing={missing}, extra={extra})")
    return True, ""


def _dogfood_verdict(claim_id, verdict, cert_dict, payload, mech):
    """Mechanism-integrity checks on every judged verdict. The law's own
    invariants, recomputed by the gate. Raises GateBroken on any break."""
    if verdict.accepted and verdict.failure is not None:
        raise GateBroken(
            f"claim {claim_id}: mechanism integrity broken — accepted "
            f"verdict carries a failure ({verdict.failure!r})")
    if not verdict.accepted and not verdict.failure:
        raise GateBroken(
            f"claim {claim_id}: mechanism integrity broken — rejected "
            f"verdict names no reason")
    # The verification order must be a real topological order over the
    # certificate's own prerequisite graph — recomputed here, never
    # trusted from the mechanism's word alone.
    deferred = {iv.name for iv in verdict.invariant_verdicts
                if iv.verdict == "DEFERRED"}
    ok, reason = _topo_order_valid(cert_dict,
                                   list(verdict.verification_order),
                                   deferred)
    if not ok:
        raise GateBroken(
            f"claim {claim_id}: mechanism integrity broken — {reason}")
    # No deferred invariant may ride as a failure.
    failures = set(verdict.primary_failures) | \
        set(verdict.dependent_failures)
    bad = failures & deferred
    if bad:
        raise GateBroken(
            f"claim {claim_id}: mechanism integrity broken — deferred "
            f"invariants judged as failures: {sorted(bad)}")
    # Serialization roundtrip must be byte-stable: what the cold
    # verifier parses is exactly the claim's canonical bytes.
    reserialized = json.dumps(json.loads(payload.decode("utf-8")),
                              sort_keys=True,
                              separators=(",", ":")).encode("utf-8")
    if reserialized != payload:
        raise GateBroken(
            f"claim {claim_id}: mechanism integrity broken — certificate "
            f"serialization roundtrip is not byte-stable")


def _judge_claim(entry, mech, manifest_path):
    """Cold-judge one claim against the REAL D64 engine. Returns a result
    dict with verdict 'pass' or 'violation'. Raises GateBroken when the
    manifest or the mechanism is untrustworthy (fail-closed)."""
    claim_id = entry.get("id")
    obligation_id, asserts, certificate, asserted_verdict = \
        _check_claim_shape(entry, manifest_path)
    # Structural binding: the certificate must speak about the claim's
    # own obligation — a cross-obligation certificate is refused. A
    # certificate that binds no obligation at all is malformed content
    # and goes to the law for refusal (below), not to the binding check.
    cert_obligation = certificate.get("obligation_id")
    if isinstance(cert_obligation, str) and \
            cert_obligation != obligation_id:
        return {"id": claim_id, "verdict": "violation",
                "asserted": asserts, "actual": "REJECTED",
                "reason": f"cross-obligation certificate: certificate "
                          f"binds {cert_obligation!r}, claim binds "
                          f"{obligation_id!r}"}
    payload = json.dumps(certificate, sort_keys=True,
                         separators=(",", ":")).encode("utf-8")
    try:
        verdict = mech.independent_verify(payload)
    except Exception as exc:
        # The law refuses the claim's content: malformed bytes, bad
        # shape, a failed witness, an uncovered cycle, an unsound TRUE,
        # an unproven FALSE — the mechanism's own words name it.
        return {"id": claim_id, "verdict": "violation",
                "asserted": asserts, "actual": "REJECTED",
                "reason": f"the D64 law refuses this certificate: "
                          f"{type(exc).__name__}: {exc}"}
    # Dogfood the mechanism on every judged verdict — a broken engine
    # fails closed, never certifies.
    _dogfood_verdict(claim_id, verdict, certificate, payload, mech)

    engine_verdicts = {iv.name: iv.verdict
                       for iv in verdict.invariant_verdicts}
    if not verdict.accepted:
        if asserts == ASSERT_VERIFIED:
            return {"id": claim_id, "verdict": "violation",
                    "asserted": asserts, "actual": "REJECTED",
                    "reason": f"claim asserts VERIFIED but the D64 law "
                              f"rejects the certificate: {verdict.failure}"}
        return {"id": claim_id, "verdict": "pass",
                "asserted": asserts, "actual": "REJECTED",
                "reason": f"honest rejection record: {verdict.failure}"}
    # The law accepts the certificate. The claimant's asserted summary
    # must match the engine's recomputed judgment exactly — this is
    # where the collapse / wrong-primary / invented-verdict frauds die.
    if asserts == ASSERT_REJECTED:
        return {"id": claim_id, "verdict": "violation",
                "asserted": asserts, "actual": "VERIFIED",
                "reason": "claim records REJECTED but the D64 law "
                          "accepts the certificate — invented refusal"}
    divergences = []
    if list(verdict.primary_failures) != \
            asserted_verdict["primary_failures"]:
        divergences.append(
            f"primary_failures: asserted "
            f"{asserted_verdict['primary_failures']} but the law judges "
            f"{list(verdict.primary_failures)} (causal diagnosis runs in "
            f"execution order, never verification order)")
    if list(verdict.dependent_failures) != \
            asserted_verdict["dependent_failures"]:
        divergences.append(
            f"dependent_failures: asserted "
            f"{asserted_verdict['dependent_failures']} but the law judges "
            f"{list(verdict.dependent_failures)}")
    asserted_map = asserted_verdict["invariant_verdicts"]
    if set(asserted_map) != set(engine_verdicts) or \
            any(asserted_map[n] != engine_verdicts[n]
                for n in engine_verdicts):
        wrong = sorted(
            n for n in set(asserted_map) | set(engine_verdicts)
            if asserted_map.get(n) != engine_verdicts.get(n))
        divergences.append(
            f"invariant_verdicts diverge on {wrong}: asserted "
            f"{ {n: asserted_map.get(n) for n in wrong} } but the law "
            f"judges { {n: engine_verdicts.get(n) for n in wrong} } "
            f"(UNDETERMINED never collapses to FALSE; a failed witness "
            f"demotes to UNDETERMINED, never to a verdict)")
    if divergences:
        return {"id": claim_id, "verdict": "violation",
                "asserted": asserts, "actual": "VERIFIED",
                "reason": "claimed verdict summary is not what the law "
                          "judges — " + " | ".join(divergences)}
    return {"id": claim_id, "verdict": "pass",
            "asserted": asserts, "actual": "VERIFIED",
            "reason": "claimant's summary matches the cold engine "
                      "verdict exactly"}


def _finish(exit_code, verdict, reason, results, as_json):
    payload = {"verdict": verdict, "reason": reason, "claims": results}
    if as_json:
        print(json.dumps(payload, indent=2))
    else:
        print(f"D64 dependency-order verification gate: {verdict} — "
              f"{reason}")
        for r in results:
            line = (f"  [{r['verdict']}] {r['id']}: asserted={r['asserted']} "
                    f"actual={r['actual']}")
            if r.get("reason"):
                line += f" — {r['reason']}"
            print(line)
    return exit_code


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Judge dependency-order verification claims against "
                    "the D64 engine.")
    parser.add_argument("--manifest",
                        default=str(DEFAULT_MANIFEST),
                        help="path to d64_dependency_order_manifest.json")
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="machine-readable output")
    args = parser.parse_args(argv)

    try:
        data = _load_manifest(args.manifest)
    except GateBroken as exc:
        return _finish(EXIT_BROKEN, "BROKEN", str(exc), [], args.as_json)
    if data is None:
        return _finish(EXIT_PASS, "DORMANT",
                       "manifest absent: nothing to judge (explicit)",
                       [], args.as_json)
    claims = data["claims"]
    if not claims:
        return _finish(EXIT_PASS, "DORMANT",
                       "manifest registers zero claims: nothing to judge "
                       "(explicit, not a false green)",
                       [], args.as_json)
    try:
        mech = _load_mechanism()
    except MechanismMissing as exc:
        return _finish(EXIT_BROKEN, "BROKEN",
                       f"{exc}: {len(claims)} claim(s) registered but cannot "
                       "be certified — refusing to pass on defaults",
                       [], args.as_json)
    results = []
    try:
        for entry in claims:
            results.append(_judge_claim(entry, mech, args.manifest))
    except GateBroken as exc:
        return _finish(EXIT_BROKEN, "BROKEN", str(exc), results,
                       args.as_json)
    violations = [r for r in results if r["verdict"] == "violation"]
    if violations:
        return _finish(EXIT_VIOLATION, "VIOLATION",
                       f"{len(violations)}/{len(results)} claim(s) blocked",
                       results, args.as_json)
    return _finish(EXIT_PASS, "PASS",
                   f"{len(results)} claim(s) certified by the D64 engine",
                   results, args.as_json)


if __name__ == "__main__":
    sys.exit(main())
