#!/usr/bin/env python3
"""D62 pumping-witness integrity gate — wire the verifier onto the fairness path.

The D62 mechanism (drift_canary/pumping_witness.py, PR #2318) is the
pumping-witness integrity law (AER-LIVE-7): assert an unbounded fairness-debt
upper bound ONLY from a minimized, independently-verified entry-cycle-exit
certificate — independently reachable entry, positively debt-producing and
arbitrarily repeatable cycle, valid exit after every finite repetition. The
dangerous false witness is the cycle that repeats only twice: a self-loop on
the scheduler state quietly consuming a finite recovery token each traversal.
The naive shape-only checker declares it unbounded; the real verifier rejects
it with the minimal counterexample at the third repetition. And the
quantifiers stay separate: a pumping witness proves the unbounded peak (for
every bound, some history exceeds it), never a proven violation (every
history breaches it) — any attempt to upgrade a witness to a BREACH fails
closed as a starvation accusation.

This gate puts that mechanism on a live operating path: every unbounded-debt
claim registered in tools/d62_pumping_witness_manifest.json is cold-verified
by the REAL D62 verifier, reconstructed from the claim's own certificate
bytes. A claim whose certificate the verifier rejects — the two-token
defect, a mandatory reset inside the cycle, an unreachable exit, a
non-minimal certificate, malformed bytes — is BLOCKED. A claim that asserts
BREACH from a pumping witness is BLOCKED as quantifier confusion. The gate
also dogfoods the mechanism's own integrity: upgrade_to_breach must refuse
on every accepted verdict, or the gate fails closed.

OPERATING PATH (what this protects and how to verify it stays connected):
  Path: the fairness CI path — any PR touching drift_canary/pumping_witness.py,
  the debt-bound machinery (D60/D61), this gate, its manifest, or its tests.
  Trigger: the d62-pumping-witness-gate check on pull_request / push-to-main.
  Block: check red (exit 1 VIOLATION or exit 2 BROKEN) blocks the merge path.
  Defect class: unbounded-debt upper bounds asserted without a minimized
  independently-verified certificate, and witness-to-breach upgrades
  (starvation accusations).
  Verify-still-connected: `python tools/d62_pumping_witness_gate.py --json`
  must exit 0 DORMANT on a claim-free tree; registering the manifest's
  worked example must exit 1 naming repetition 3; deleting the mechanism
  with claims present must exit 2. If the workflow file disappears from
  .github/workflows/, the path is unwired — re-add it.

Exit contract (the whole point of the gate):
  0  PASS     — every registered claim certified by the cold verifier.
  0  DORMANT  — manifest absent or registers zero claims. Explicit, never a
                false green: the gate says "nothing to judge".
  1  VIOLATION— a claim BLOCKED: the verifier rejects its certificate (the
                mechanism names the minimal counterexample), its certificate
                bytes are malformed, or it asserts BREACH from a witness
                (quantifier confusion — never a starvation accusation).
  2  BROKEN   — fail-closed: manifest corrupt, claim fields unparseable, an
                unknown assertion value, claims exist but the mechanism is
                absent, or the mechanism's quantifier separation is broken
                (upgrade_to_breach failed to refuse). The gate never invents
                the verifier and never defaults an unknown.

The gate never invents fields: unknown assertions, malformed shapes, or
missing keys are BROKEN, not defaulted.

Directive: D62 (Minimal, Independently Verified Unbounded-Cycle Witnesses,
AER-LIVE-7, #2175 / 6102470813), owner naya2. Wired by the night-shift WIRE
lane. No merge — the merge lane owns it.
"""

from __future__ import annotations

import argparse
import base64
import binascii
import json
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOLS_DIR.parent
DEFAULT_MANIFEST = TOOLS_DIR / "d62_pumping_witness_manifest.json"

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
     "asserts", "certificate_b64"})
ASSERTIONS = ("PROVEN_UNBOUNDED", "BREACH")


class GateBroken(Exception):
    """Fail-closed: the gate cannot trust its inputs. Exit 2."""


class MechanismMissing(Exception):
    """The D62 verifier is absent. Exit 2 when claims exist, else DORMANT."""


def _load_mechanism():
    """Import the REAL D62 verifier. Never synthesized, never defaulted.

    Verifies the required API surface so a neutered module cannot silently
    pass as the mechanism.
    """
    try:
        import drift_canary.pumping_witness as mech
    except ImportError as exc:
        raise MechanismMissing(f"D62 mechanism not importable: {exc}")
    for attr in ("verify_pumping_witness", "independent_verify",
                 "certificate_to_json", "certificate_from_json",
                 "upgrade_to_breach", "PumpingWitnessCertificate",
                 "PumpingStep", "PumpingWitnessError",
                 "StarvationAccusationError", "CertificateSerializationError",
                 "PROVEN_UNBOUNDED", "WITNESS_REJECTED", "UNRESOLVED",
                 "fixtures_aer_live_007"):
        if not hasattr(mech, attr):
            raise MechanismMissing(
                f"mechanism missing required API: {attr}")
    return mech


def _load_manifest(path):
    """Load the claims manifest. Returns None when the file is absent.

    Raises GateBroken on anything untrustworthy: bad JSON, wrong shape,
    duplicate ids, claims missing required keys.
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
        if cid in seen:
            raise GateBroken(f"duplicate claim id: {cid!r}")
        seen.add(cid)
    return data


def _as_nonempty_str(value, what):
    if not isinstance(value, str) or not value.strip():
        raise GateBroken(f"{what} must be a non-empty string, "
                         f"got {value!r} (never defaulted)")
    return value


def _decode_certificate_b64(raw, claim_id):
    """Decode the claim's certificate bytes. Malformed base64 is BROKEN
    (the manifest is untrustworthy); decodable-but-garbage bytes are a
    VIOLATION at judge time (the claim's evidence fails closed)."""
    if not isinstance(raw, str) or not raw.strip():
        raise GateBroken(
            f"claim {claim_id}: certificate_b64 must be a non-empty string")
    try:
        return base64.b64decode(raw, validate=True)
    except (binascii.Error, ValueError) as exc:
        raise GateBroken(
            f"claim {claim_id}: certificate_b64 is not valid base64: {exc}")


def judge_claim(claim, mech):
    """Judge one claim against the real cold verifier. Returns a result dict."""
    claim_id = claim["id"]
    obligation_id = _as_nonempty_str(claim["obligation_id"],
                                     f"claim {claim_id} obligation_id")
    claimant = _as_nonempty_str(claim["claimant"],
                                f"claim {claim_id} claimant")
    evidence_ref = _as_nonempty_str(claim["evidence_ref"],
                                    f"claim {claim_id} evidence_ref")
    asserts = claim["asserts"]
    if asserts not in ASSERTIONS:
        raise GateBroken(
            f"claim {claim_id}: unknown asserts {asserts!r} (never defaulted)")
    payload = _decode_certificate_b64(claim["certificate_b64"], claim_id)

    try:
        verdict = mech.independent_verify(payload)
    except mech.CertificateSerializationError as exc:
        return {
            "id": claim_id, "obligation_id": obligation_id,
            "asserted": asserts, "actual": "UNVERIFIABLE",
            "verdict": "violation",
            "reason": (f"certificate bytes malformed — the cold verifier "
                       f"fails closed, never guesses: {exc}"),
        }
    except mech.PumpingWitnessError as exc:
        # Any other fail-closed refusal from the mechanism: the claim's
        # evidence cannot be certified — blocked, never passed.
        return {
            "id": claim_id, "obligation_id": obligation_id,
            "asserted": asserts, "actual": "UNVERIFIABLE",
            "verdict": "violation",
            "reason": f"verifier refused the certificate: {exc}",
        }

    result = {
        "id": claim_id,
        "obligation_id": obligation_id,
        "claimant": claimant,
        "evidence_ref": evidence_ref,
        "asserted": asserts,
        "actual": verdict.peak_status,
        "accepted": verdict.accepted,
        "breach_verdict": verdict.breach_verdict,
        "fingerprint": verdict.certificate_fingerprint,
        "failure": verdict.failure,
    }

    # Quantifier separation, mechanical and first: a pumping witness is
    # never a starvation accusation. Dogfood the mechanism's own refusal —
    # if upgrade_to_breach ever stops refusing, the mechanism's integrity
    # is broken and the gate fails closed.
    try:
        mech.upgrade_to_breach(verdict)
    except mech.StarvationAccusationError:
        pass
    except Exception as exc:  # noqa: BLE001 — any other outcome is a break
        raise GateBroken(
            f"claim {claim_id}: mechanism integrity broken — "
            f"upgrade_to_breach did not refuse: {exc!r}")
    else:
        raise GateBroken(
            f"claim {claim_id}: mechanism integrity broken — "
            "upgrade_to_breach returned instead of refusing")

    if asserts == "BREACH":
        result["verdict"] = "violation"
        result["reason"] = (
            "quantifier confusion BLOCKED: a pumping witness proves the "
            "unbounded peak (for every bound, some history exceeds it), "
            "never a proven violation (every history breaches it). "
            "Asserting BREACH from a witness is a starvation accusation — "
            "the mechanism refuses it, and so does this gate.")
        return result

    if not verdict.accepted:
        result["verdict"] = "violation"
        result["reason"] = (
            f"certificate REJECTED by the cold verifier: {verdict.failure} — "
            "an unbounded-debt upper bound asserted without a minimized "
            "independently-verified certificate is the exact defect D62 "
            "exists to prevent")
        return result

    if verdict.breach_verdict != mech.UNRESOLVED:
        result["verdict"] = "violation"
        result["reason"] = (
            f"verifier answered the breach question ({verdict.breach_verdict}) "
            "— the pumping witness must always answer UNRESOLVED; "
            "quantifiers stay separate")
        return result

    result["verdict"] = "certified"
    result["reason"] = (
        f"cold verifier ACCEPTED: minimized certificate, peak "
        f"{verdict.peak_status}, breach {verdict.breach_verdict}, "
        f"fingerprint {verdict.certificate_fingerprint[:16]}…")
    return result


def _finish(exit_code, verdict, reason, results, as_json):
    payload = {"verdict": verdict, "reason": reason, "claims": results}
    if as_json:
        print(json.dumps(payload, indent=2))
    else:
        print(f"D62 pumping-witness gate: {verdict} — {reason}")
        for r in results:
            line = (f"  [{r['verdict']}] {r['id']}: asserted={r['asserted']} "
                    f"actual={r['actual']}")
            if r.get("reason"):
                line += f" — {r['reason']}"
            print(line)
    return exit_code


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Judge unbounded-debt claims against the D62 "
                    "pumping-witness verifier.")
    parser.add_argument("--manifest",
                        default=str(DEFAULT_MANIFEST),
                        help="path to d62_pumping_witness_manifest.json")
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
            results.append(judge_claim(entry, mech))
    except GateBroken as exc:
        return _finish(EXIT_BROKEN, "BROKEN", str(exc), results, args.as_json)
    violations = [r for r in results if r["verdict"] == "violation"]
    if violations:
        return _finish(EXIT_VIOLATION, "VIOLATION",
                       f"{len(violations)}/{len(results)} claim(s) blocked",
                       results, args.as_json)
    return _finish(EXIT_PASS, "PASS",
                   f"{len(results)} claim(s) certified by the D62 verifier",
                   results, args.as_json)


if __name__ == "__main__":
    sys.exit(main())
