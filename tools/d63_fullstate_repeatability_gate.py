#!/usr/bin/env python3
"""D63 full-state repeatability gate — wire the engine onto the fairness path.

The D63 mechanism (drift_canary/full_state_repeatability.py, PR #2320) is
the full-state closure of D62's repeatability claim (AER-LIVE-8): a
repeatability certificate proves arbitrary repetition only when the
inductive invariant holds over the FULL state — authority, budgets,
resources, time, lifecycle, evidence, obligations — at every repetition.
A cycle that preserves debt but violates authority is not repeatable.
The verifier names the first violated component at the exact repetition —
the minimal counterexample. The flagship fraud: the authority token
expires after 50 traversals, so the naive debt-gain-only checker wrongly
declares the cycle repeatable; D63 rejects it at repetition 51.
Repeatability is a model property, never a production authorization —
upgrade_to_authorization always refuses with ProductionAuthorizationError.

This gate puts that mechanism on a live operating path: every
repeatability claim registered in
tools/d63_fullstate_repeatability_manifest.json is cold-judged by the REAL
D63 engine, reconstructed from the claim's own certificate bytes via
independent_verify. A claim the law refuses — REPEATABLE asserted over a
certificate whose invariant breaks (authority expiry, budget drain, zero
debt gain, finite retries, broken entry, unaffordable exit), malformed
certificate bytes, or a cross-obligation certificate — is BLOCKED. The
gate also dogfoods the mechanism's own integrity: every judged verdict
must carry authorization == UNDETERMINED, accepted verdicts must be
REPEATABLE with no failure, rejected verdicts NOT_REPEATABLE with a named
minimal counterexample, the serialization roundtrip must be byte-stable,
and upgrade_to_authorization must refuse (a grant where the law says
refusal means the mechanism is broken — fail closed, never certify).

OPERATING PATH (what this protects and how to verify it stays connected):
  Path: the fairness CI path — any PR touching
  drift_canary/full_state_repeatability.py, drift_canary/fairness.py, this
  gate, its manifest, or its tests.
  Trigger: the fullstate-repeatability-gate check on pull_request /
  push-to-main.
  Block: check red (exit 1 VIOLATION or exit 2 BROKEN) blocks the merge path.
  Defect class: arbitrary-repetition claims over full-state certificates
  that the D63 law refuses — authority expiry at repetition 51,
  budget drain at repetition 20, zero debt gain, finite-retries CONTROL
  rejection, broken entry, unaffordable exit, malformed certificates,
  cross-obligation certificates, repeatability presented as production
  authorization.
  Verify-still-connected: `python tools/d63_fullstate_repeatability_gate.py
  --json` must exit 0 DORMANT on a claim-free tree; registering the
  manifest's worked AE-EXAMPLE claim must exit 1 naming the repetition-51
  authority break; claims present with the mechanism deleted must exit 2.
  If the workflow file disappears from .github/workflows/, the path is
  unwired — re-add it.

Exit contract (the whole point of the gate):
  0  PASS     — every registered claim certified by the cold engine.
  0  DORMANT  — manifest absent or registers zero claims. Explicit, never a
                false green: the gate says "nothing to judge".
  1  VIOLATION— a claim BLOCKED: the law refuses it (independent_verify
                names NOT_REPEATABLE with the minimal counterexample, the
                certificate bytes are malformed, or the certificate binds a
                different obligation). The mechanism's own words name the
                refusal.
  2  BROKEN   — fail-closed: manifest corrupt, claim fields untrustworthy,
                an unknown assertion value, claims exist but the mechanism
                is absent, or the mechanism's own verdict invariants broke
                (receipt coherence dogfood failed). The gate never invents
                the engine and never defaults an unknown.

The gate never invents fields: unknown assertions, malformed shapes, or
missing keys are BROKEN, not defaulted. Claim CONTENT refused by the law is
VIOLATION, not BROKEN — the distinction is whose trust broke: the
manifest's (BROKEN) or the claim's (VIOLATION).

Structural note: the gate compares the certificate's own obligation_id
against the claim's obligation_id — a cross-obligation certificate is
refused. Judgment is structurally bound to the claim's obligation.

Directive: D63 (Full-State Invariants for Repeatable Cycle Proofs,
AER-LIVE-8, Naya 3's intel #2175/6102503850), owner naya2. Wired by the
night-shift WIRE lane. No merge — the merge lane owns it.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOLS_DIR.parent
DEFAULT_MANIFEST = TOOLS_DIR / "d63_fullstate_repeatability_manifest.json"

# The mechanism lives in the drift_canary package at the repo root. The
# workflow runs this script as `python tools/...` (script dir on sys.path,
# not the repo root), so the root is appended explicitly. Appended — not
# prepended — so a test/battery overlay earlier on sys.path (or PYTHONPATH)
# keeps winning; the repo root is the fallback, never an override.
if str(REPO_ROOT) not in sys.path:
    sys.path.append(str(REPO_ROOT))

EXIT_PASS = 0
EXIT_VIOLATION = 1
EXIT_BROKEN = 2

REQUIRED_CLAIM_KEYS = frozenset(
    {"id", "obligation_id", "claimant", "evidence_ref",
     "asserts", "certificate"})
ASSERTIONS = ("REPEATABLE", "NOT_REPEATABLE")

# API surface the gate depends on. A neutered module that lacks any of
# these cannot silently pass as the mechanism.
MECH_ATTRS = (
    "RepeatabilityCertificate", "RepeatabilityVerdict",
    "verify_full_state_repeatability", "independent_verify",
    "certificate_to_json", "certificate_from_json",
    "upgrade_to_authorization", "fixtures_aer_live_008",
    "FullStateRepeatabilityError", "CertificateShapeError",
    "NonMinimalCertificateError", "ProductionAuthorizationError",
    "CertificateSerializationError",
    "REPEATABLE", "NOT_REPEATABLE", "UNDETERMINED",
)


class GateBroken(Exception):
    """Fail-closed: the gate cannot trust its inputs. Exit 2."""


class MechanismMissing(Exception):
    """The D63 engine is absent. Exit 2 when claims exist, else DORMANT."""


def _load_mechanism():
    """Import the REAL D63 engine. Never synthesized, never defaulted.

    Verifies the required API surface so a neutered module cannot silently
    pass as the mechanism.
    """
    try:
        import drift_canary.full_state_repeatability as mech
    except ImportError as exc:
        raise MechanismMissing(f"D63 mechanism not importable: {exc}")
    for attr in MECH_ATTRS:
        if not hasattr(mech, attr):
            raise MechanismMissing(
                f"mechanism missing required API: {attr}")
    return mech


def _load_manifest(path):
    """Load the claims manifest. Returns None when the file is absent.

    Raises GateBroken on anything untrustworthy: bad JSON, wrong shape,
    duplicate ids, claims missing required keys, non-string identity
    fields, unknown assertions, non-dict certificate. Value semantics
    (certificate validity, verdict correctness) belong to the mechanism at
    judge time — the manifest loader checks structure, never law.
    """
    p = Path(path)
    if not p.is_file():
        return None
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:
        raise GateBroken(f"manifest is not valid JSON: {exc}")
    if not isinstance(data, dict) or not isinstance(data.get("claims"), list):
        raise GateBroken("manifest must be an object with a 'claims' list")
    seen = set()
    for entry in data["claims"]:
        if not isinstance(entry, dict):
            raise GateBroken("every claim must be an object")
        missing = REQUIRED_CLAIM_KEYS - set(entry.keys())
        if missing:
            raise GateBroken(
                f"claim missing required keys: {sorted(missing)}")
        cid = entry["id"]
        _as_nonempty_str(cid, "claim id")
        if cid in seen:
            raise GateBroken(f"duplicate claim id: {cid!r}")
        seen.add(cid)
        for key in ("obligation_id", "claimant", "evidence_ref"):
            _as_nonempty_str(entry[key], f"claim {cid} {key}")
        asserts = entry["asserts"]
        if asserts not in ASSERTIONS:
            raise GateBroken(
                f"claim {cid}: unknown asserts {asserts!r} (never defaulted)")
        if not isinstance(entry["certificate"], dict):
            raise GateBroken(f"claim {cid}: certificate must be an object")
    return data


def _as_nonempty_str(value, what):
    if not isinstance(value, str) or not value.strip():
        raise GateBroken(f"{what} must be a non-empty string, "
                         f"got {value!r} (never defaulted)")
    return value


def _judge_bytes(claim, mech):
    """Cold-judge one claim's certificate against the REAL D63 engine.

    Returns a result dict. VIOLATION (exit 1) when the law refuses the
    claim — the mechanism's own words name the refusal. GateBroken when
    the engine's own invariants break (BROKEN at the caller).
    """
    claim_id = claim["id"]
    obligation_id = claim["obligation_id"]
    asserts = claim["asserts"]

    # Rebuild the certificate from the claim's own bytes. Malformed bytes
    # are the claim's fault — the law refuses them (VIOLATION), not the
    # manifest's (BROKEN).
    payload = json.dumps(claim["certificate"], sort_keys=True).encode("utf-8")
    try:
        cert = mech.certificate_from_json(payload)
    except mech.FullStateRepeatabilityError as exc:
        return {
            "id": claim_id, "obligation_id": obligation_id,
            "asserted": asserts, "actual": "UNJUDGEABLE",
            "verdict": "violation",
            "reason": (f"the law refuses the claim's certificate bytes: "
                       f"{type(exc).__name__}: {exc}"),
        }

    # Structural obligation binding: the certificate's own obligation_id
    # must match the claim's — cross-obligation judgment is refused.
    if cert.obligation_id != obligation_id:
        return {
            "id": claim_id, "obligation_id": obligation_id,
            "asserted": asserts, "actual": "UNJUDGEABLE",
            "verdict": "violation",
            "reason": (f"cross-obligation certificate refused: certificate "
                       f"binds {cert.obligation_id!r}, claim asserts "
                       f"{obligation_id!r}"),
        }

    # Cold verification by the REAL engine. Its fail-closed refusals
    # (malformed certificate, non-minimal certificate) mean the claim is
    # unjudgeable — BLOCKED.
    try:
        verdict = mech.independent_verify(payload)
    except mech.FullStateRepeatabilityError as exc:
        return {
            "id": claim_id, "obligation_id": obligation_id,
            "asserted": asserts, "actual": "UNJUDGEABLE",
            "verdict": "violation",
            "reason": (f"the law refuses to verify this claim: "
                       f"{type(exc).__name__}: {exc}"),
        }

    # Dogfood the mechanism's own integrity on every judged verdict. A
    # verdict that breaks these invariants means the ENGINE is broken —
    # fail closed (GateBroken), never certify.
    _dogfood_verdict_coherence(verdict, cert, payload, mech, claim_id)

    # The verdict answers the claim's assertion.
    if verdict.repeatability != asserts:
        return {
            "id": claim_id, "obligation_id": obligation_id,
            "asserted": asserts, "actual": verdict.repeatability,
            "verdict": "violation",
            "reason": (f"independent verifier REFUSED the claim: "
                       f"asserted {asserts}, engine answered "
                       f"{verdict.repeatability} — minimal counterexample: "
                       f"{verdict.failure}"),
        }

    return {
        "id": claim_id, "obligation_id": obligation_id,
        "claimant": claim["claimant"], "evidence_ref": claim["evidence_ref"],
        "asserted": asserts, "actual": verdict.repeatability,
        "authorization": verdict.authorization,
        "certificate_fingerprint": verdict.certificate_fingerprint,
        "verdict": "certified",
        "reason": (f"cold engine CERTIFIED: verdict "
                   f"{verdict.repeatability}, authorization "
                   f"{verdict.authorization} (never a production grant)"),
    }


def _dogfood_verdict_coherence(verdict, cert, payload, mech, claim_id):
    """Re-check the mechanism's verdict invariants on every judged verdict.

    The mechanism's own __post_init__ asserts these; this is the gate's
    explicit statement of what it depends on. A verdict that violates them
    means the ENGINE is broken — fail closed (GateBroken), never certify.
    The mechanical separation is dogfooded too: upgrade_to_authorization
    must refuse, or the gate fails closed.
    """
    if verdict.authorization != mech.UNDETERMINED:
        raise GateBroken(
            f"claim {claim_id}: mechanism integrity broken — verdict "
            f"answers the authorization question "
            f"({verdict.authorization!r}), which repeatability never does")
    if verdict.accepted:
        if verdict.repeatability != mech.REPEATABLE or verdict.failure is not None:
            raise GateBroken(
                f"claim {claim_id}: mechanism integrity broken — accepted "
                f"verdict is not clean REPEATABLE "
                f"(repeatability={verdict.repeatability!r}, "
                f"failure={verdict.failure!r})")
    else:
        if verdict.repeatability != mech.NOT_REPEATABLE or not verdict.failure:
            raise GateBroken(
                f"claim {claim_id}: mechanism integrity broken — rejected "
                f"verdict names no minimal counterexample "
                f"(repeatability={verdict.repeatability!r}, "
                f"failure={verdict.failure!r})")
    # Serialization roundtrip must be byte-stable: the cold verifier's
    # reconstruction is exactly the claim's bytes.
    reserialized = mech.certificate_to_json(cert)
    if reserialized != payload:
        raise GateBroken(
            f"claim {claim_id}: mechanism integrity broken — certificate "
            f"serialization roundtrip is not byte-stable")
    # Mechanical separation: a repeatability verdict is never a production
    # authorization. If upgrade_to_authorization ever returns instead of
    # raising, the mechanism's core refusal is gone — fail closed.
    try:
        mech.upgrade_to_authorization(verdict)
    except mech.ProductionAuthorizationError:
        pass  # the law holds: repeatability is not authorization
    else:
        raise GateBroken(
            f"claim {claim_id}: mechanism integrity broken — "
            f"upgrade_to_authorization GRANTED production authorization "
            f"from a repeatability verdict")


def _finish(exit_code, verdict, reason, results, as_json):
    payload = {"verdict": verdict, "reason": reason, "claims": results}
    if as_json:
        print(json.dumps(payload, indent=2))
    else:
        print(f"D63 full-state repeatability gate: {verdict} — {reason}")
        for r in results:
            line = (f"  [{r['verdict']}] {r['id']}: asserted={r['asserted']} "
                    f"actual={r['actual']}")
            if r.get("reason"):
                line += f" — {r['reason']}"
            print(line)
    return exit_code


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Judge full-state repeatability claims against the "
                    "D63 engine.")
    parser.add_argument("--manifest",
                        default=str(DEFAULT_MANIFEST),
                        help="path to d63_fullstate_repeatability_manifest.json")
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
            results.append(_judge_bytes(entry, mech))
    except GateBroken as exc:
        return _finish(EXIT_BROKEN, "BROKEN", str(exc), results, args.as_json)
    violations = [r for r in results if r["verdict"] == "violation"]
    if violations:
        return _finish(EXIT_VIOLATION, "VIOLATION",
                       f"{len(violations)}/{len(results)} claim(s) blocked",
                       results, args.as_json)
    return _finish(EXIT_PASS, "PASS",
                   f"{len(results)} claim(s) certified by the D63 engine",
                   results, args.as_json)


if __name__ == "__main__":
    sys.exit(main())
