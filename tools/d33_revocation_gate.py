#!/usr/bin/env python3
"""D33 selective-revocation gate — wire the engine onto the
drift-canary governance-verification path.

The D33 mechanism (drift_canary/d33_revocation.py, PR #2212) is the
correction law as executable machinery: revoke an ineligible evidence
source's right to support a claim, then independently recompute every
materially dependent conclusion — without deleting the source,
assuming its observations false, or revoking unrelated conclusions.
History is preserved; eligibility is versioned; qualifications are
recomputed under one consistent evidence-policy snapshot.

The fraud this law exists to prevent (the mechanism's sharpest case):
claim C is supported by (E1^E3) v (E2^E4) v (E3^E4)[staging]. E1 is
revoked. The naive checker certifies C as REQUALIFIED via E2^E4 — but
E2 was secretly DERIVED from E1, so that path was never independent.
The real engine DOWNGRADEs C to staging-only: the surviving evidence
covers only part of the claimed scope, so the claim narrows
explicitly — never a fractional confidence, never a blind pass.

This gate puts that mechanism on a live operating path: every
revocation scenario registered in tools/d33_revocation_manifest.json
is cold-executed against the REAL D33 engine
(drift_canary/d33_revocation.RevocationEngine). The scenario — sources,
derivation edges, claims with explicit AND/OR support sets, one
revocation event — is rebuilt from the claim's own model bytes, and
the claimant's asserted post-revocation verdicts must match the
engine's recomputed verdicts exactly (verdict AND covered scope). A
scenario the law refuses — a masquerading derivation, a claim left
standing on revoked evidence, an independently-sufficient conclusion
wrongly revoked — is BLOCKED.

Sabotage resistance: before judging anything, the gate runs a fixed
canary probe (the masquerade fixture) through the loaded engine and
requires DOWNGRADED-over-staging. A neutered or substituted engine
that cannot tell the masquerade from independence fails the canary and
the gate fails closed — the gate never certifies through a blind
engine.

OPERATING PATH (what this protects and how to verify it stays connected):
  Path: the drift-canary governance-verification CI path — any PR
  touching drift_canary/d33_revocation.py, this gate, its manifest,
  or its tests.
  Trigger: the revocation gate check on pull_request / push-to-main.
  Block: check red (exit 1 VIOLATION or exit 2 BROKEN) blocks the merge path.
  Defect class: stale or inflated qualifications surviving an evidence
  revocation — masquerading derivations certified as independent,
  revoked evidence still supporting claims, blanket revocations
  destroying independently-sufficient conclusions.
  Verify-still-connected: `python tools/d33_revocation_gate.py --json`
  must exit 0 DORMANT on a claim-free tree; registering the manifest's
  worked _example as a claim must exit 1 naming asserted=REQUALIFIED
  actual=DOWNGRADED; scenarios present with the mechanism deleted must
  exit 2. If the workflow file disappears from .github/workflows/,
  the path is unwired — re-add it.

Exit contract (the whole point of the gate):
  0  PASS     — every registered scenario's asserted verdicts certified
                by the cold engine (verdict and covered scope, exactly).
  0  DORMANT  — manifest absent or registers zero scenarios. Explicit,
                never a false green: the gate says "nothing to judge".
  1  VIOLATION— a scenario BLOCKED: the engine's recomputed verdict or
                covered scope diverges from the claimant's asserted one.
                The mechanism's own words name the divergence.
  2  BROKEN   — fail-closed: manifest corrupt, unknown verdict / scope /
                assessment / kind values, malformed scenario shape, an
                asserted claim the engine cannot construct, scenarios
                exist but the mechanism is absent or fails the canary.
                The gate never invents the engine and never defaults
                an unknown.

The gate never pre-computes the outcome — the engine's
QualificationRecord is the authority, exactly as a real revocation
boundary must be the authority over its own requalification.

Directive: D33 (Selective Evidence Revocation and Claim
Requalification; mechanism PR #2212), owner naya4. Wired by the Naya 2
night-shift WIRE lane. No merge — the merge lane owns it.
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
    "d33_revocation_manifest.json"
MECHANISM_MODULE = "drift_canary.d33_revocation"

# The workflow runs this script as `python tools/...` (script dir on
# sys.path, not the repo root). The mechanism lives at the repo root —
# append it so the gate imports the REAL engine wherever it runs from.
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.append(str(REPO_ROOT))

VERDICTS = (
    "UNAFFECTED",
    "REQUALIFIED",
    "DOWNGRADED",
    "INSUFFICIENT_DATA",
    "SUSPENDED",
    "REVOKED",
)
SCOPES = ("staging", "production")
# "unassessed" is deliberately absent: the engine RAISES on it (it
# refuses to revoke what was never assessed). A scenario asking the
# gate to judge an unjudgeable revocation is malformed, not a verdict.
ASSESSMENTS = (
    "confirmed_compromised",
    "possibly_compromised",
    "expired",
)
KINDS = ("certification", "observational")
COVERAGES = ("complete", "gap")


class GateBroken(Exception):
    """The manifest or the mechanism is untrustworthy — fail closed."""


class MechanismMissing(Exception):
    """Scenarios are registered but the D33 engine is absent."""


def _load_mechanism():
    try:
        return importlib.import_module(MECHANISM_MODULE)
    except Exception as exc:
        raise MechanismMissing(
            "D33 mechanism %r not importable: %s" % (MECHANISM_MODULE, exc))


def _canary_probe(d33):
    """Fixed masquerade fixture through the loaded engine.

    Claim C: (E1^E3) v (E2^E4) v (E3^E4)[staging], E2 secretly derived
    from E1. Revoke E1 (confirmed compromised). The REAL engine must
    DOWNGRADE C to staging-only. Anything else means the loaded engine
    is not the D33 mechanism — fail closed.
    """
    eng = d33.RevocationEngine()
    full = frozenset({d33.STAGING, d33.PRODUCTION})
    staging_only = frozenset({d33.STAGING})
    for sid in ("E1", "E2", "E3", "E4", "E5"):
        eng.register_source(d33.EvidenceSource(
            source_id=sid, observed_content="canary-" + sid, scope=full))
    eng.add_derivation("E2", "E1")
    eng.register_claim(d33.Claim(
        claim_id="C",
        paths=(d33.SupportPath(sources=frozenset({"E1", "E3"}), scope=full),
               d33.SupportPath(sources=frozenset({"E2", "E4"}), scope=full),
               d33.SupportPath(sources=frozenset({"E3", "E4"}),
                               scope=staging_only)),
        scope=full, min_paths=1))
    eng.register_claim(d33.Claim(
        claim_id="D",
        paths=(d33.SupportPath(sources=frozenset({"E5"}), scope=full),)))
    eng.revoke("E1", "canary: answer key exposed",
               assessment=d33.CONFIRMED_COMPROMISED)
    rec_c = eng.qualification("C")
    rec_d = eng.qualification("D")
    if rec_c.verdict != d33.DOWNGRADED or rec_c.covered_scope != staging_only:
        raise GateBroken(
            "canary FAILED: masquerade not caught "
            "(verdict=%s scope=%s); loaded engine is not the D33 mechanism"
            % (rec_c.verdict, sorted(rec_c.covered_scope)))
    if rec_d.verdict != d33.UNAFFECTED:
        raise GateBroken(
            "canary FAILED: unrelated claim disturbed "
            "(verdict=%s); loaded engine is not the D33 mechanism"
            % rec_d.verdict)
    return True


def _req_str(mapping, key, where):
    val = mapping.get(key)
    if not isinstance(val, str) or not val:
        raise GateBroken("%s: %r must be a non-empty string" % (where, key))
    return val


def _scope_set(values, where):
    if not isinstance(values, list) or not values:
        raise GateBroken("%s: scope must be a non-empty list" % where)
    for v in values:
        if v not in SCOPES:
            raise GateBroken(
                "%s: unknown scope %r (want one of %s)"
                % (where, v, ", ".join(SCOPES)))
    return frozenset(values)


def _build_engine(d33, name, spec):
    """Rebuild one scenario's engine from the claim's own model bytes."""
    where = "scenario %r" % name
    eng = d33.RevocationEngine()

    sources = spec.get("sources")
    if not isinstance(sources, list) or not sources:
        raise GateBroken(where + ": 'sources' must be a non-empty list")
    for i, s in enumerate(sources):
        sw = "%s source[%d]" % (where, i)
        if not isinstance(s, dict):
            raise GateBroken(sw + ": must be an object")
        sid = _req_str(s, "source_id", sw)
        content = s.get("observed_content", "observation-log-" + sid)
        if not isinstance(content, str):
            raise GateBroken(sw + ": observed_content must be a string")
        scope = _scope_set(s.get("scope", ["staging", "production"]), sw)
        coverage = s.get("coverage", "complete")
        if coverage not in COVERAGES:
            raise GateBroken(
                sw + ": unknown coverage %r" % (coverage,))
        eng.register_source(d33.EvidenceSource(
            source_id=sid, observed_content=content,
            scope=scope, coverage=coverage))

    for i, pair in enumerate(spec.get("derivations", [])):
        dw = "%s derivation[%d]" % (where, i)
        if (not isinstance(pair, list) or len(pair) != 2
                or not all(isinstance(x, str) for x in pair)):
            raise GateBroken(dw + ": must be [derived_id, origin_id]")
        try:
            eng.add_derivation(pair[0], pair[1])
        except (ValueError, KeyError) as exc:
            raise GateBroken(dw + ": engine refused: %s" % exc)

    claims = spec.get("claims")
    if not isinstance(claims, list) or not claims:
        raise GateBroken(where + ": 'claims' must be a non-empty list")
    for i, c in enumerate(claims):
        cw = "%s claim[%d]" % (where, i)
        if not isinstance(c, dict):
            raise GateBroken(cw + ": must be an object")
        cid = _req_str(c, "claim_id", cw)
        raw_paths = c.get("paths")
        if not isinstance(raw_paths, list) or not raw_paths:
            raise GateBroken(cw + ": 'paths' must be a non-empty list")
        paths = []
        for j, p in enumerate(raw_paths):
            pw = "%s path[%d]" % (cw, j)
            if not isinstance(p, dict):
                raise GateBroken(pw + ": must be an object")
            srcs = p.get("sources")
            if (not isinstance(srcs, list) or not srcs
                    or not all(isinstance(x, str) for x in srcs)):
                raise GateBroken(pw + ": sources must be a non-empty list")
            paths.append(d33.SupportPath(
                sources=frozenset(srcs),
                scope=_scope_set(p.get("scope", ["staging", "production"]),
                                 pw)))
        scope = _scope_set(c.get("scope", ["staging", "production"]), cw)
        min_paths = c.get("min_paths", 1)
        if not isinstance(min_paths, int) or min_paths < 1:
            raise GateBroken(cw + ": min_paths must be a positive int")
        kind = c.get("kind", "certification")
        if kind not in KINDS:
            raise GateBroken(cw + ": unknown kind %r" % (kind,))
        req_comp = c.get("requires_completeness", False)
        if not isinstance(req_comp, bool):
            raise GateBroken(cw + ": requires_completeness must be boolean")
        deps = c.get("depends_on", [])
        if (not isinstance(deps, list)
                or not all(isinstance(x, str) for x in deps)):
            raise GateBroken(cw + ": depends_on must be a list of strings")
        try:
            eng.register_claim(d33.Claim(
                claim_id=cid, paths=tuple(paths), scope=scope,
                min_paths=min_paths, kind=kind,
                requires_completeness=req_comp,
                depends_on=tuple(deps)))
        except (ValueError, KeyError) as exc:
            raise GateBroken(cw + ": engine refused: %s" % exc)
    return eng


def _apply_revocation(d33, eng, name, spec):
    where = "scenario %r revocation" % name
    rev = spec.get("revocation")
    if not isinstance(rev, dict):
        raise GateBroken(where + ": must be an object")
    source_id = _req_str(rev, "source_id", where)
    reason = rev.get("reason", "")
    if not isinstance(reason, str):
        raise GateBroken(where + ": reason must be a string")
    assessment = rev.get("assessment", "confirmed_compromised")
    if assessment not in ASSESSMENTS:
        raise GateBroken(
            where + ": unknown assessment %r (want one of %s)"
            % (assessment, ", ".join(ASSESSMENTS)))
    const = {"confirmed_compromised": d33.CONFIRMED_COMPROMISED,
             "possibly_compromised": d33.POSSIBLY_COMPROMISED,
             "expired": "expired"}[assessment]
    try:
        return eng.revoke(source_id, reason, assessment=const)
    except (ValueError, KeyError) as exc:
        raise GateBroken(where + ": engine refused revocation: %s" % exc)


def _judge_scenario(d33, name, spec):
    """Returns (verdict, detail). verdict in PASS/VIOLATION; BROKEN raises."""
    eng = _build_engine(d33, name, spec)
    _apply_revocation(d33, eng, name, spec)
    asserted = spec.get("asserted")
    if not isinstance(asserted, dict) or not asserted:
        raise GateBroken(
            "scenario %r: 'asserted' must be a non-empty object" % name)
    for cid, claim in asserted.items():
        cw = "scenario %r asserted %r" % (name, cid)
        if not isinstance(claim, dict):
            raise GateBroken(cw + ": must be an object")
        want_verdict = claim.get("verdict")
        if want_verdict not in VERDICTS:
            raise GateBroken(
                cw + ": unknown verdict %r" % (want_verdict,))
        want_scope = _scope_set(claim.get("covered_scope", []), cw)
        try:
            rec = eng.qualification(cid)
        except KeyError:
            raise GateBroken(
                cw + ": claim not registered in scenario")
        if rec.verdict != want_verdict or rec.covered_scope != want_scope:
            return ("VIOLATION",
                    "scenario %r claim %r: asserted=%s over %s but the "
                    "engine recomputed actual=%s over %s (%s)"
                    % (name, cid, want_verdict, sorted(want_scope),
                       rec.verdict, sorted(rec.covered_scope), rec.reason))
    return ("PASS", "scenario %r: all %d asserted verdicts certified"
            % (name, len(asserted)))


def judge_manifest(manifest_path):
    """Judge every registered scenario. Returns (exit_code, report dict)."""
    try:
        with open(manifest_path) as fh:
            manifest = json.load(fh)
    except FileNotFoundError:
        return (EXIT_PASS, {"status": "DORMANT",
                            "reason": "manifest absent: nothing to judge"})
    except json.JSONDecodeError as exc:
        return (EXIT_BROKEN, {"status": "BROKEN",
                              "reason": "manifest corrupt: %s" % exc})
    if not isinstance(manifest, dict):
        return (EXIT_BROKEN, {"status": "BROKEN",
                              "reason": "manifest must be a JSON object"})
    scenarios = manifest.get("scenarios", {})
    if not isinstance(scenarios, dict):
        return (EXIT_BROKEN, {"status": "BROKEN",
                              "reason": "'scenarios' must be an object"})
    # Worked examples (keys starting with _) document the fraud and the
    # honest case; they are never live claims.
    live = {k: v for k, v in scenarios.items() if not k.startswith("_")}
    if not live:
        return (EXIT_PASS, {"status": "DORMANT",
                            "reason": "zero registered scenarios: "
                                      "nothing to judge"})

    try:
        d33 = _load_mechanism()
    except MechanismMissing as exc:
        return (EXIT_BROKEN, {"status": "BROKEN", "reason": str(exc)})
    try:
        _canary_probe(d33)
    except GateBroken as exc:
        return (EXIT_BROKEN, {"status": "BROKEN", "reason": str(exc)})
    except Exception as exc:
        return (EXIT_BROKEN, {"status": "BROKEN",
                              "reason": "canary crashed: %s: %s"
                              % (type(exc).__name__, exc)})

    judged = []
    for name in sorted(live):
        spec = live[name]
        if not isinstance(spec, dict):
            return (EXIT_BROKEN, {"status": "BROKEN",
                                  "reason": "scenario %r must be an object"
                                  % name})
        try:
            verdict, detail = _judge_scenario(d33, name, spec)
        except GateBroken as exc:
            return (EXIT_BROKEN, {"status": "BROKEN", "reason": str(exc)})
        except Exception as exc:
            return (EXIT_BROKEN, {"status": "BROKEN",
                                  "reason": "scenario %r crashed the gate: "
                                  "%s: %s" % (name, type(exc).__name__, exc)})
        judged.append({"scenario": name, "verdict": verdict,
                       "detail": detail})
        if verdict == "VIOLATION":
            return (EXIT_VIOLATION, {"status": "VIOLATION",
                                     "reason": detail,
                                     "judged": judged})
    return (EXIT_PASS, {"status": "PASS",
                        "reason": "%d scenario(s) certified by the engine"
                        % len(judged),
                        "judged": judged})


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="D33 selective-revocation wire gate")
    ap.add_argument("--manifest", default=str(DEFAULT_MANIFEST),
                    help="path to the revocation manifest JSON")
    ap.add_argument("--json", action="store_true",
                    help="emit the report as JSON")
    args = ap.parse_args(argv)
    code, report = judge_manifest(args.manifest)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print("D33-GATE %s: %s" % (report["status"], report["reason"]))
        for j in report.get("judged", []):
            print("  [%s] %s" % (j["verdict"], j["scenario"]))
    return code


if __name__ == "__main__":
    sys.exit(main())
