"""D34 cache-invalidation claims gate (WIRE lane, Naya 2).

Cold-judges every registered D34 scenario against the REAL
drift_canary.d34_cache_invalidation.IntelligenceStore — never a
reimplementation. A claim the D34 memory law refuses blocks the PR.

Exit contract:
  0  PASS     — every live scenario's asserted outcomes match the engine
  0  DORMANT  — zero live scenarios registered (explicit, never a false green)
  1  VIOLATION— a scenario asserts an outcome the engine refuses
  2  BROKEN   — fail-closed: manifest missing/corrupt, mechanism missing or
                tampered, canary probe failed (a blind engine never passes)

Fixed canary probes run before any judging:
  C1 stale-as-current refused — revoke E1, serve its CURRENT projection on
     an authority route: the engine must answer REFUSE_STALE.
  C2 generation-bound compare-and-swap — refresh at a stale generation must
     raise StaleGenerationError (a delayed refresh may never republish an
     earlier PASS over a later revocation).
  C3 ACT commit-boundary re-check — authorize_act at a stale generation must
     answer REFUSED (TOCTOU close).
A neutered engine fails a canary -> exit 2, never a blind pass.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

# The mechanism lives at the repo root. When CI runs
# `python tools/d34_cache_invalidation_gate.py`, Python puts tools/ on
# sys.path, not the repo root — so anchor the root explicitly. This also
# pins the "live tree" the gate judges: the checkout's own bytes.
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.append(str(REPO_ROOT))

MANIFEST_DEFAULT = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "d34_cache_invalidation_manifest.json",
)

# The D34 vocabularies the gate speaks. The engine's own constants are
# asserted identical at import; the gate never invents competing words.
SERVE_DECISIONS = ("SERVE_CURRENT", "SERVE_HISTORICAL", "REFUSE_STALE")
ACT_DECISIONS = ("AUTHORIZED", "REFUSED")
PROJECTION_STATUSES = (
    "CURRENT", "REVALIDATION_REQUIRED", "REFRESH_PENDING", "HISTORICAL_ONLY",
)
VERDICTS = (
    "UNAFFECTED", "REQUALIFIED", "DOWNGRADED",
    "INSUFFICIENT_DATA", "SUSPENDED", "REVOKED",
)
SOURCE_STATUSES = ("ELIGIBLE", "SUSPENDED", "REVOKED", "EXPIRED")
SURFACES = (
    "cached_summary", "smart_note", "index_entry",
    "successor_package", "historical_receipt",
)
AUTHORITY_ROUTES = (
    "know_retrieval", "connect_expansion", "summary_generation",
    "note_capture", "successor_activation", "learn_promotion",
    "consequential_act",
)
ALL_ROUTES = AUTHORITY_ROUTES + ("index_lookup",)


class GateBroken(Exception):
    """Fail-closed: the gate cannot judge honestly."""


class Violation(Exception):
    """A judged claim the D34 law refuses."""

    def __init__(self, scenario_id, op_index, detail):
        super().__init__(
            "scenario=%s op#%d: %s" % (scenario_id, op_index, detail)
        )
        self.scenario_id = scenario_id
        self.op_index = op_index
        self.detail = detail


def _import_mechanism():
    """Import the REAL D34 engine from the live tree. Any tampering with
    the import surface fails closed."""
    try:
        from drift_canary import d34_cache_invalidation as d34
    except Exception as exc:
        raise GateBroken("cannot import drift_canary.d34_cache_invalidation "
                         "from the live tree: %r" % (exc,))
    required = (
        "IntelligenceStore", "StaleGenerationError",
        "SERVE_CURRENT", "SERVE_HISTORICAL", "REFUSE_STALE",
        "ACT_AUTHORIZED", "ACT_REFUSED",
        "CURRENT", "REVALIDATION_REQUIRED", "REFRESH_PENDING",
        "HISTORICAL_ONLY",
        "UNAFFECTED", "REQUALIFIED", "DOWNGRADED",
        "INSUFFICIENT_DATA", "SUSPENDED", "REVOKED",
        "ELIGIBLE",
        "KNOW_RETRIEVAL", "INDEX_LOOKUP",
        "CACHED_SUMMARY", "SMART_NOTE", "INDEX_ENTRY",
        "SUCCESSOR_PACKAGE", "HISTORICAL_RECEIPT",
    )
    missing = [name for name in required if not hasattr(d34, name)]
    if missing:
        raise GateBroken("mechanism tampered: missing names %s" % (missing,))
    # Vocabulary identity: the gate's words must BE the engine's words.
    for name in ("SERVE_CURRENT", "SERVE_HISTORICAL", "REFUSE_STALE"):
        if getattr(d34, name) != name:
            raise GateBroken("serve-decision vocabulary drift: %s" % (name,))
    for name in ("CURRENT", "REVALIDATION_REQUIRED", "REFRESH_PENDING",
                 "HISTORICAL_ONLY"):
        if getattr(d34, name) != name:
            raise GateBroken("projection-status vocabulary drift: %s"
                             % (name,))
    if getattr(d34, "ACT_AUTHORIZED") != "AUTHORIZED":
        raise GateBroken("ACT vocabulary drift: ACT_AUTHORIZED")
    if getattr(d34, "ACT_REFUSED") != "REFUSED":
        raise GateBroken("ACT vocabulary drift: ACT_REFUSED")
    return d34


def load_manifest(path):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            manifest = json.load(fh)
    except FileNotFoundError:
        raise GateBroken("manifest not found: %s" % (path,))
    except json.JSONDecodeError as exc:
        raise GateBroken("manifest corrupt (not JSON): %s: %s" % (path, exc))
    if not isinstance(manifest, dict):
        raise GateBroken("manifest must be a JSON object")
    scenarios = manifest.get("scenarios", [])
    if not isinstance(scenarios, list):
        raise GateBroken("manifest 'scenarios' must be a list")
    return manifest


def _resolve_generation(store, value):
    if value == "current":
        return store.generation
    if isinstance(value, int) and value >= 0:
        return value
    raise GateBroken("bad generation reference: %r" % (value,))


def _as_frozenset(value, what):
    if isinstance(value, (list, tuple, set, frozenset)):
        return frozenset(value)
    raise GateBroken("bad %s: %r (need a list)" % (what, value))


def _apply_op(d34, store, scenario_id, index, op):
    """Replay one scenario op against the real store. Returns an
    assertion failure string, or None when the op's assertion holds."""
    if not isinstance(op, dict) or "op" not in op:
        raise GateBroken("scenario=%s op#%d malformed: %r"
                         % (scenario_id, index, op))
    kind = op["op"]

    if kind == "register_source":
        source_id = op["source_id"]
        scope = _as_frozenset(op.get("scope", ["staging", "production"]),
                              "scope")
        store.register_source(source_id, scope=scope)
        return None

    if kind == "register_claim":
        paths = []
        for entry in op["paths"]:
            srcs, scope = entry
            paths.append((_as_frozenset(srcs, "path sources"),
                          _as_frozenset(scope, "path scope")))
        store.register_claim(
            op["claim_id"], paths,
            scope=_as_frozenset(op.get("scope", ["staging", "production"]),
                                "scope"),
            min_paths=int(op.get("min_paths", 1)),
            kind=op.get("kind", "certification"),
        )
        return None

    if kind == "add_projection":
        surface = op["surface"]
        if surface not in SURFACES:
            raise GateBroken("scenario=%s op#%d unknown surface %r"
                             % (scenario_id, index, surface))
        store.add_projection(
            op["projection_id"], surface,
            _as_frozenset(op["claim_dependencies"], "claim_dependencies"),
            content=op.get("content", ""),
        )
        return None

    if kind == "commit":
        new_status = op["new_status"]
        if new_status not in SOURCE_STATUSES:
            raise GateBroken("scenario=%s op#%d unknown source status %r"
                             % (scenario_id, index, new_status))
        store.commit_eligibility_change(op["source_id"], new_status,
                                        op.get("reason", ""))
        return None

    if kind == "serve":
        route = op["route"]
        if route not in ALL_ROUTES:
            raise GateBroken("scenario=%s op#%d unknown route %r"
                             % (scenario_id, index, route))
        asserted = op["assert"]
        if asserted not in SERVE_DECISIONS:
            raise GateBroken("scenario=%s op#%d bad serve assertion %r"
                             % (scenario_id, index, asserted))
        result = store.serve(op["projection_id"], route)
        if result.decision != asserted:
            return ("serve %s on %s: asserted=%s actual=%s (%s)"
                    % (op["projection_id"], route, asserted,
                       result.decision, result.annotation))
        return None

    if kind == "refresh":
        expected = _resolve_generation(store, op["expected_generation"])
        asserted = op.get("assert", "ok")
        try:
            store.refresh_projection(op["projection_id"], expected)
        except d34.StaleGenerationError as exc:
            if asserted == "StaleGenerationError":
                return None
            return ("refresh %s: asserted ok but StaleGenerationError: %s"
                    % (op["projection_id"], exc))
        if asserted == "StaleGenerationError":
            return ("refresh %s: asserted StaleGenerationError but the "
                    "engine published it (generation CAS broken)"
                    % (op["projection_id"],))
        return None

    if kind == "authorize_act":
        seen = _resolve_generation(store, op["seen_generation"])
        asserted = op["assert"]
        if asserted not in ACT_DECISIONS:
            raise GateBroken("scenario=%s op#%d bad ACT assertion %r"
                             % (scenario_id, index, asserted))
        actual = store.authorize_act(
            _as_frozenset(op["claim_dependencies"], "claim_dependencies"),
            seen)
        if actual != asserted:
            return ("authorize_act: asserted=%s actual=%s "
                    "(TOCTOU close held)" % (asserted, actual))
        return None

    if kind == "assert_claim_verdict":
        asserted = op["assert"]
        if asserted not in VERDICTS:
            raise GateBroken("scenario=%s op#%d bad verdict assertion %r"
                             % (scenario_id, index, asserted))
        actual = store.claims[op["claim_id"]].verdict
        if actual != asserted:
            return ("claim %s: asserted verdict=%s actual=%s"
                    % (op["claim_id"], asserted, actual))
        return None

    if kind == "assert_projection_status":
        asserted = op["assert"]
        if asserted not in PROJECTION_STATUSES:
            raise GateBroken("scenario=%s op#%d bad status assertion %r"
                             % (scenario_id, index, asserted))
        actual = store.projections[op["projection_id"]].status
        if actual != asserted:
            return ("projection %s: asserted status=%s actual=%s"
                    % (op["projection_id"], asserted, actual))
        return None

    if kind == "reconcile":
        asserted = op.get("assert", [])
        actual = store.reconcile()
        if sorted(actual) != sorted(asserted):
            return ("reconcile: asserted violations=%r actual=%r"
                    % (asserted, actual))
        return None

    raise GateBroken("scenario=%s op#%d unknown op %r"
                     % (scenario_id, index, kind))


def judge_scenario(d34, scenario):
    """Replay one scenario against the real engine. Returns the list of
    assertion failures (empty == the engine's word matches the claim)."""
    if not isinstance(scenario, dict) or "id" not in scenario:
        raise GateBroken("scenario malformed: %r" % (scenario,))
    scenario_id = scenario["id"]
    ops = scenario.get("ops", [])
    if not isinstance(ops, list):
        raise GateBroken("scenario=%s 'ops' must be a list" % (scenario_id,))
    store = d34.IntelligenceStore()
    failures = []
    for index, op in enumerate(ops):
        failure = _apply_op(d34, store, scenario_id, index, op)
        if failure is not None:
            failures.append("op#%d: %s" % (index, failure))
    return failures


def run_canaries(d34):
    """Fixed sharpest-sequence probes, run before any judging. A neutered
    or blind engine fails here -> GateBroken (exit 2), never a blind pass."""
    # C1: stale-as-current must be refused on an authority route.
    store = d34.IntelligenceStore()
    store.register_source("E1")
    store.register_claim("K1", [(frozenset({"E1"}),
                                 frozenset({"staging", "production"}))])
    store.add_projection("P1", d34.CACHED_SUMMARY, ["K1"], content="v1")
    before = store.serve("P1", d34.KNOW_RETRIEVAL)
    if before.decision != d34.SERVE_CURRENT:
        raise GateBroken("canary C1 setup broken: fresh projection not "
                         "servable: %s" % (before.decision,))
    store.commit_eligibility_change("E1", d34.REVOKED,
                                    reason="canary: confirmed compromised")
    after = store.serve("P1", d34.KNOW_RETRIEVAL)
    if after.decision != d34.REFUSE_STALE:
        raise GateBroken(
            "canary C1 FAILED: stale projection served as %s after "
            "revocation (engine is blind to staleness)" % (after.decision,))

    # C2: generation-bound compare-and-swap on refresh.
    stale_gen = store.generation - 1
    try:
        store.refresh_projection("P1", stale_gen)
    except d34.StaleGenerationError:
        pass
    else:
        raise GateBroken("canary C2 FAILED: refresh at stale generation "
                         "published (CAS broken — a delayed refresh could "
                         "republish an earlier PASS over a later revocation)")

    # C3: ACT commit-boundary re-check (TOCTOU close).
    seen = store.generation - 1
    if store.authorize_act(["K1"], seen) != d34.ACT_REFUSED:
        raise GateBroken("canary C3 FAILED: ACT authorized at a stale "
                         "generation (TOCTOU close broken)")


def judge_manifest(d34, manifest):
    """Returns (verdict, detail) with verdict in PASS/DORMANT/VIOLATION."""
    scenarios = manifest.get("scenarios", [])
    live = [s for s in scenarios
            if not (isinstance(s, dict) and s.get("id", "").startswith("_"))]
    if not live:
        return "DORMANT", "zero live scenarios registered"
    for scenario in live:
        failures = judge_scenario(d34, scenario)
        if failures:
            sid = scenario.get("id", "?")
            raise Violation(sid, -1, "; ".join(failures))
    return "PASS", "%d live scenario(s) match the engine's word" % (len(live),)


def main(argv):
    manifest_path = argv[1] if len(argv) > 1 else MANIFEST_DEFAULT
    try:
        d34 = _import_mechanism()
        manifest = load_manifest(manifest_path)
        run_canaries(d34)
        verdict, detail = judge_manifest(d34, manifest)
    except Violation as exc:
        print("D34-GATE VIOLATION: %s" % (exc,))
        return 1
    except GateBroken as exc:
        print("D34-GATE BROKEN (fail-closed): %s" % (exc,))
        return 2
    print("D34-GATE %s: %s" % (verdict, detail))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
