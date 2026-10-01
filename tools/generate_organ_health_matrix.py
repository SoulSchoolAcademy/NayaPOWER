#!/usr/bin/env python3
"""generate_organ_health_matrix.py — canonical nine-organ health matrix generator V1.

Emits ``BRAIN/03-KERNEL/0006-ORGAN-HEALTH-MATRIX-V1.json`` conforming to
``BRAIN/03-KERNEL/SCHEMA/ORGAN-HEALTH-MATRIX-SCHEMA.json``, per
``BRAIN/03-KERNEL/0005-NINE-ORGAN-HEALTH-MATRIX-SPEC-V1.md`` (spec V1).

Evidence (primary only, all pinned to the exact stamped SHA):
  1. Runtime registry ``0003-RUNTIME-REGISTRY-V1.json`` (organ order, bindings).
  2. Organism contract ``0004-NINE-NODE-ORGANISM-CONTRACT-V1.json``
     (envelope fields, proof ladder).
  3. CI check runs on the exact SHA (``kernel-tests`` -> UNIT,
     ``chain-readiness-gate`` -> INTEGRATION, ``current-truth-resolver`` ->
     truth coherence cap, ``independent-verification`` -> OUTCOME assist).
  4. Proof workflow runs on the exact SHA (``live-<organ>-proof`` -> BEHAVIORAL).
  5. Optional human-gated receipts: --production-receipt (PRODUCTION),
     --continuity-receipt (SUCCESSOR), --acceptance-records (OUTCOME per organ).

Fail-closed (spec §4, §7): the generator REFUSES (exit 2, reason on stderr)
rather than emit a matrix when
  - the registry's ``node_order`` or any contract ``proof_ladder`` disagrees
    with the canonical lists,
  - STRUCTURAL or CONTRACT cannot be proven for any organ from the canonical
    files,
  - the stamped SHA is malformed,
  - (live mode) the stamp is stale relative to the main tip and --allow-stale
    was not passed.

A rung is PROVEN only on primary, green evidence on the exact stamped SHA.
Missing evidence -> UNKNOWN. The organ's claim is a ladder prefix: a rung
above a missing rung is recorded in rung_evidence but never claimed
(spec §4.6 "missing_rung is the very next rung not proven"). Failing required
CI (kernel-tests, chain-readiness-gate, current-truth-resolver) caps every
organ at CONTRACT (CAPPED_BY_CI). PRODUCTION/SUCCESSOR are human-gated: UNKNOWN_NOT_DISPATCHED /
UNKNOWN_NOT_QUALIFIED unless valid receipts are supplied. CI alone can never
claim them.

Modes:
  offline (default): evidence supplied as JSON files
      --check-runs FILE       {"check_runs":[{"name","conclusion","id",...}]}
      --workflow-runs FILE    {"workflow_runs":[{"name","conclusion","id","head_branch",...}]}
      --unit-coverage FILE    {"KNOW": true, ...}  (operator-supplied organ
                              coverage evidence; recorded as a ref)
  live (--live): the generator fetches check runs, workflow runs, and the repo
      tree at the stamped SHA itself via the gh-api helper, and scans the
      tree for organ-scoped test files (UNIT coverage). Requires --gh-api.

Exit codes: 0 = matrix emitted; 2 = refused (fail-closed); 1 = usage error.
"""

from __future__ import annotations

import argparse
import base64
import datetime as _dt
import json
import os
import re
import subprocess
import sys
from pathlib import Path

REPO = "SoulSchoolAcademy/NayaPOWER"

ORGANS = ["SELF", "LAW", "ACT", "KNOW", "PROVE", "CONNECT", "VERIFY", "LEARN", "EVOLVE"]
RUNGS = [
    "STRUCTURAL", "CONTRACT", "UNIT", "INTEGRATION",
    "BEHAVIORAL", "OUTCOME", "PRODUCTION", "SUCCESSOR",
]
MISSING_RUNG_ENUM = ["UNIT", "INTEGRATION", "BEHAVIORAL", "OUTCOME", "PRODUCTION", "SUCCESSOR"]
RUNG_EVIDENCE_STATUSES = ["PROVEN", "UNKNOWN", "UNKNOWN_NOT_DISPATCHED",
                          "UNKNOWN_NOT_QUALIFIED", "CAPPED_BY_CI"]

SPEC_VERSION = "1"
GENERATOR_VERSION = "1.0.0"
ARTIFACT_REL = "BRAIN/03-KERNEL/0006-ORGAN-HEALTH-MATRIX-V1.json"
REGISTRY_REL = "BRAIN/03-KERNEL/0003-RUNTIME-REGISTRY-V1.json"
CONTRACT_REL = "BRAIN/03-KERNEL/0004-NINE-NODE-ORGANISM-CONTRACT-V1.json"
SCHEMA_REL = "BRAIN/03-KERNEL/SCHEMA/ORGAN-HEALTH-MATRIX-SCHEMA.json"

# Check-name aliases, most specific first. Names are normalized (lowercase,
# separators stripped) before comparison. The matched ACTUAL check name and id
# are recorded in refs so the mapping is auditable, not asserted.
CHECK_ALIASES = {
    "unit": ["kernel-tests", "kernel_tests", "kerneltests", "test"],
    "integration": ["chain-readiness-gate", "chain_readiness_gate",
                    "collective-chain-readiness-gate", "chain-gate", "chain_gate"],
    "truth": ["current-truth-resolver", "current_truth_resolver",
              "resolve-current-truth", "truth-resolver", "truth_resolver"],
    "outcome": ["independent-verification", "independent_verification"],
}
# Checks whose failure/cancel caps every organ at CONTRACT (spec §4.3).
CAP_CHECKS = ("unit", "integration", "truth")
BAD_CONCLUSIONS = {"failure", "cancelled", "timed_out", "action_required", "stale"}


class Refused(Exception):
    """Fail-closed refusal: the generator will not emit a matrix."""


def _norm(name: str) -> str:
    return re.sub(r"[\s_\-]+", "", (name or "").lower())


def _tokens(name: str) -> set:
    return set(t for t in re.split(r"[^a-z0-9]+", (name or "").lower()) if t)


def match_check(checks: list[dict], kind: str) -> dict | None:
    """Return the best-matching check run dict for a check kind, or None."""
    for alias in CHECK_ALIASES[kind]:
        want = _norm(alias)
        for c in checks:
            if _norm(c.get("name", "")) == want:
                return c
    return None


def organ_test_paths(tree_paths: list[str], organ: str) -> list[str]:
    """Organ-scoped test files: path tokens contain the organ name AND a test token."""
    o = organ.lower()
    hits = []
    for p in tree_paths:
        toks = _tokens(p)
        if o in toks and ("test" in toks or "tests" in toks):
            hits.append(p)
    return sorted(hits)


def live_proof_run(runs: list[dict], organ: str, sha: str) -> dict | None:
    """A live-<organ>-proof workflow run, success, on the exact SHA, on main."""
    o = organ.lower()
    for r in runs:
        toks = _tokens(r.get("name", "")) | _tokens(r.get("path", ""))
        if "live" in toks and "proof" in toks and o in toks:
            if r.get("conclusion") == "success" and r.get("head_sha", "").lower() == sha.lower():
                if r.get("head_branch", "main") == "main":
                    return r
    return None


def _run_gh(gh_api: str, method: str, path: str) -> dict:
    try:
        out = subprocess.run([gh_api, method, path], capture_output=True, text=True,
                             check=False, timeout=120)
    except OSError as e:
        raise Refused(f"live evidence helper failed to execute ({method} {path}): {e}")
    if out.returncode != 0:
        raise Refused(f"live evidence fetch failed ({method} {path}): {out.stderr.strip()[:300]}")
    try:
        return json.loads(out.stdout)
    except json.JSONDecodeError:
        raise Refused(f"live evidence fetch returned non-JSON ({method} {path})")


def fetch_live(gh_api: str, sha: str, allow_stale: bool) -> tuple[list, list, list, bool]:
    """Return (check_runs, workflow_runs, tree_paths, stale_stamp)."""
    tip = _run_gh(gh_api, "GET", f"/repos/{REPO}/git/refs/heads/main")
    tip_sha = tip["object"]["sha"]
    stale = tip_sha.lower() != sha.lower()
    if stale and not allow_stale:
        raise Refused(
            f"stale stamp: stamped_sha {sha[:8]} != main tip {tip_sha[:8]} "
            "(spec §4.7 — re-evaluate before any decision use; pass --allow-stale "
            "to emit a stale-marked matrix)"
        )
    checks = _run_gh(gh_api, "GET", f"/repos/{REPO}/commits/{sha}/check-runs?per_page=100").get("check_runs", [])
    runs = _run_gh(
        gh_api, "GET",
        f"/repos/{REPO}/actions/runs?branch=main&head_sha={sha}&per_page=100",
    ).get("workflow_runs", [])
    tree = _run_gh(gh_api, "GET", f"/repos/{REPO}/git/trees/{sha}?recursive=1").get("tree", [])
    paths = [t["path"] for t in tree if t.get("type") == "blob"]
    return checks, runs, paths, stale


def load_json(path: str | None, what: str) -> dict | None:
    if not path:
        return None
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise Refused(f"cannot load {what} from {path}: {e}")


def sha_ok(sha: str) -> bool:
    return bool(re.fullmatch(r"[0-9a-f]{40}", (sha or "").lower()))


NEXT_PROOF = {
    "UNIT": "kernel-tests check run success on {sha} with organ-scoped tests for {organ}",
    "INTEGRATION": "chain-readiness-gate check run success on {sha} covering {organ}",
    "BEHAVIORAL": "live-{o}-proof workflow run success on {sha} (bounded runtime, organ contract scope)",
    "OUTCOME": "independent-verification success on {sha} + VERIFY acceptance record referencing {organ}",
    "PRODUCTION": "Governed Production Promotion run success on {sha} + migration verification receipts (human dispatch)",
    "SUCCESSOR": "cold-successor qualification run success on {sha} (human-chartered)",
}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Nine-organ health matrix generator V1 (fail-closed).")
    ap.add_argument("--repo", default=".", help="repo root containing BRAIN/ (default: .)")
    ap.add_argument("--sha", default=None, help="stamped SHA (default: git HEAD of --repo)")
    ap.add_argument("--out", default=None, help="output path (default: <repo>/BRAIN/03-KERNEL/0006-ORGAN-HEALTH-MATRIX-V1.json)")
    ap.add_argument("--evaluator", default="naya-2-build-loop")
    ap.add_argument("--generator-version", default=GENERATOR_VERSION)
    ap.add_argument("--live", action="store_true", help="fetch evidence from GitHub via gh-api")
    ap.add_argument("--gh-api", default=os.path.expanduser("~/workspace/naya/bin/gh-api"))
    ap.add_argument("--allow-stale", action="store_true", help="live mode: emit even if stamped_sha != main tip (marks stale_stamp)")
    ap.add_argument("--check-runs", default=None)
    ap.add_argument("--workflow-runs", default=None)
    ap.add_argument("--tree-paths", default=None, help='JSON {"paths":[...]} for UNIT organ-test scan (offline)')
    ap.add_argument("--unit-coverage", default=None, help='JSON {"KNOW": true,...} operator-supplied coverage (offline)')
    ap.add_argument("--acceptance-records", default=None, help='JSON {"KNOW": ["ref",...], ...}')
    ap.add_argument("--production-receipt", default=None)
    ap.add_argument("--continuity-receipt", default=None)
    args = ap.parse_args(argv)

    repo = Path(args.repo)
    try:
        return _run(args, repo)
    except Refused as e:
        sys.stderr.write(f"REFUSED: {e}\n")
        return 2


def _run(args, repo: Path) -> int:
    registry_p = repo / REGISTRY_REL
    contract_p = repo / CONTRACT_REL
    schema_p = repo / SCHEMA_REL
    for p, what in ((registry_p, "registry"), (contract_p, "contract"), (schema_p, "schema")):
        if not p.is_file():
            raise Refused(f"canonical {what} not found at {p}")

    registry = json.loads(registry_p.read_text(encoding="utf-8"))
    contract = json.loads(contract_p.read_text(encoding="utf-8"))

    # --- consistency law (§7): canonical lists must match the spec exactly ---
    if registry.get("node_order") != ORGANS:
        raise Refused(
            f"registry node_order {registry.get('node_order')} != canonical {ORGANS}; "
            "registry is canonical — spec must be amended before any matrix is emitted"
        )
    nodes = contract.get("nodes", {})
    for organ in ORGANS:
        ladder = (nodes.get(organ) or {}).get("proof_ladder")
        if ladder != RUNGS:
            raise Refused(
                f"contract proof_ladder for {organ} is {ladder}, expected {RUNGS}; "
                "contract is canonical — spec must be amended before any matrix is emitted"
            )
    required_fields = ((contract.get("universal_envelope") or {}).get("required_fields")) or []
    if not required_fields:
        raise Refused("contract universal_envelope.required_fields is empty — cannot evaluate CONTRACT rung")

    # --- stamped SHA ---
    sha = (args.sha or "").lower()
    if not sha:
        r = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"],
                           capture_output=True, text=True)
        sha = (r.stdout.strip() or "").lower()
    if not sha_ok(sha):
        raise Refused(f"stamped_sha {sha!r} is not a 40-hex SHA (schema demands exact SHA)")

    # --- evidence ---
    stale_stamp = False
    gate_coverage: list[dict] = []
    if args.live:
        checks, runs, tree_paths, stale_stamp = fetch_live(args.gh_api, sha, args.allow_stale)
        unit_coverage = None
    else:
        checks = (load_json(args.check_runs, "check-runs") or {}).get("check_runs", [])
        runs = (load_json(args.workflow_runs, "workflow-runs") or {}).get("workflow_runs", [])
        tree_paths = (load_json(args.tree_paths, "tree-paths") or {}).get("paths", [])
        unit_coverage = load_json(args.unit_coverage, "unit-coverage")
    acceptance = load_json(args.acceptance_records, "acceptance-records") or {}
    prod_receipt = load_json(args.production_receipt, "production-receipt")
    cont_receipt = load_json(args.continuity_receipt, "continuity-receipt")

    matched = {kind: match_check(checks, kind) for kind in CHECK_ALIASES}
    ci_state = {}
    for kind in ("unit", "integration", "truth"):
        c = matched[kind]
        ci_state[c["name"] if c else CHECK_ALIASES[kind][0]] = (c.get("conclusion") if c else "absent")

    # fail-closed cap (§4.3): failing required CI caps every organ at CONTRACT.
    cap = False
    cap_reasons = []
    for kind in CAP_CHECKS:
        c = matched[kind]
        if c and (c.get("conclusion") in BAD_CONCLUSIONS):
            cap = True
            cap_reasons.append(f"{c['name']}={c['conclusion']} (check_run {c.get('id')}) on {sha[:8]}")

    # --- per-organ evaluation ---
    organ_entries = []
    for organ in ORGANS:
        node = nodes[organ]
        rung_evidence: list[dict] = []

        # STRUCTURAL: node entry in contract + presence in registry node_order.
        structural = organ in nodes and organ in (registry.get("node_order") or [])
        if not structural:
            raise Refused(f"{organ}: STRUCTURAL unprovable (missing from contract or registry node_order)")
        rung_evidence.append({
            "rung": "STRUCTURAL", "status": "PROVEN",
            "refs": [f"repo:{CONTRACT_REL}#nodes.{organ}@{sha[:8]}",
                     f"repo:{REGISTRY_REL}#node_order@{sha[:8]}"],
        })

        # CONTRACT: every universal-envelope required field present in the node entry.
        missing_fields = [f for f in required_fields if f not in node]
        if missing_fields:
            raise Refused(
                f"{organ}: CONTRACT unprovable — node entry missing required envelope "
                f"fields {missing_fields} (spec §2.1: missing one field ⇒ CONTRACT not reached)"
            )
        rung_evidence.append({
            "rung": "CONTRACT", "status": "PROVEN",
            "refs": [f"repo:{CONTRACT_REL}#nodes.{organ}+universal_envelope.required_fields@{sha[:8]}"],
        })

        # UNIT: kernel-tests green on SHA + organ-scoped tests present.
        u = matched["unit"]
        if cap:
            rung_evidence.append({"rung": "UNIT", "status": "CAPPED_BY_CI",
                                  "refs": [f"ci:{r}" for r in cap_reasons] or ["ci:cap"]})
            unit_proven = False
        elif u is None:
            rung_evidence.append({"rung": "UNIT", "status": "UNKNOWN", "refs": []})
            unit_proven = False
        elif u.get("conclusion") != "success":
            # Present but not green and not a failing conclusion (e.g.
            # "skipped", "in_progress"): missing evidence of success, not a
            # cap. UNKNOWN, consistent with the INTEGRATION branch.
            rung_evidence.append({"rung": "UNIT", "status": "UNKNOWN",
                                  "refs": [f"check_run:{u.get('id')}:{u.get('name')}={u.get('conclusion')}"]})
            unit_proven = False
        else:
            test_hits = organ_test_paths(tree_paths, organ)
            covered = bool(test_hits) or bool(unit_coverage and unit_coverage.get(organ))
            refs = [f"check_run:{u.get('id')}:{u.get('name')}=success@{sha[:8]}"]
            if test_hits:
                refs += [f"repo:{p}@{sha[:8]}" for p in test_hits[:10]]
                if len(test_hits) > 10:
                    refs.append(f"repo:+{len(test_hits) - 10}-more-organ-test-paths")
            if unit_coverage and unit_coverage.get(organ):
                refs.append("operator:unit-coverage.json")
            rung_evidence.append({"rung": "UNIT",
                                  "status": "PROVEN" if covered else "UNKNOWN",
                                  "refs": refs})
            unit_proven = covered

        # INTEGRATION: chain-readiness-gate green on SHA exercises the nine-node chain.
        g = matched["integration"]
        if cap:
            rung_evidence.append({"rung": "INTEGRATION", "status": "CAPPED_BY_CI",
                                  "refs": [f"ci:{r}" for r in cap_reasons] or ["ci:cap"]})
            integration_proven = False
        elif g is None or g.get("conclusion") != "success":
            rung_evidence.append({
                "rung": "INTEGRATION", "status": "UNKNOWN",
                "refs": ([f"check_run:{g.get('id')}:{g.get('name')}={g.get('conclusion')}"] if g else []),
            })
            integration_proven = False
        else:
            rung_evidence.append({
                "rung": "INTEGRATION", "status": "PROVEN",
                "refs": [f"check_run:{g.get('id')}:{g.get('name')}=success@{sha[:8]}",
                         f"repo:{REGISTRY_REL}#next_node_after_*@{sha[:8]}"],
            })
            integration_proven = True
        if integration_proven:
            gate_coverage.append({"gate": g["name"], "check_run_id": g.get("id"),
                                  "covers": list(ORGANS)})

        # BEHAVIORAL: live-<organ>-proof workflow run success on SHA.
        pr = live_proof_run(runs, organ, sha)
        if cap:
            rung_evidence.append({"rung": "BEHAVIORAL", "status": "CAPPED_BY_CI",
                                  "refs": [f"ci:{r}" for r in cap_reasons] or ["ci:cap"]})
            behavioral_proven = False
        elif pr:
            rung_evidence.append({
                "rung": "BEHAVIORAL", "status": "PROVEN",
                "refs": [f"workflow_run:{pr.get('id')}:{pr.get('name')}=success@{sha[:8]}"],
            })
            behavioral_proven = True
        else:
            rung_evidence.append({"rung": "BEHAVIORAL", "status": "UNKNOWN", "refs": []})
            behavioral_proven = False

        # OUTCOME: independent-verification green on SHA + VERIFY acceptance record.
        v = matched["outcome"]
        acc_refs = acceptance.get(organ) or []
        if cap:
            rung_evidence.append({"rung": "OUTCOME", "status": "CAPPED_BY_CI",
                                  "refs": [f"ci:{r}" for r in cap_reasons] or ["ci:cap"]})
            outcome_proven = False
        elif v is not None and v.get("conclusion") == "success" and acc_refs:
            rung_evidence.append({
                "rung": "OUTCOME", "status": "PROVEN",
                "refs": [f"check_run:{v.get('id')}:{v.get('name')}=success@{sha[:8]}"] + acc_refs,
            })
            outcome_proven = True
        else:
            rung_evidence.append({
                "rung": "OUTCOME", "status": "UNKNOWN",
                "refs": ([f"check_run:{v.get('id')}:{v.get('name')}={v.get('conclusion')}"] if v else []),
            })
            outcome_proven = False

        # PRODUCTION: human-gated. Receipt required; CI alone never claims it.
        if cap:
            rung_evidence.append({"rung": "PRODUCTION", "status": "CAPPED_BY_CI",
                                  "refs": [f"ci:{r}" for r in cap_reasons] or ["ci:cap"]})
            production_proven = False
        elif (prod_receipt and prod_receipt.get("promotion_run_id")
              and prod_receipt.get("dispatched_by") and prod_receipt.get("migration_receipts")):
            rung_evidence.append({
                "rung": "PRODUCTION", "status": "PROVEN",
                "refs": [f"promotion_run:{prod_receipt['promotion_run_id']}@{sha[:8]}",
                         f"human_dispatch:{prod_receipt['dispatched_by']}"]
                + [f"migration_receipt:{m}" for m in prod_receipt["migration_receipts"]],
            })
            production_proven = True
        else:
            rung_evidence.append({"rung": "PRODUCTION", "status": "UNKNOWN_NOT_DISPATCHED", "refs": []})
            production_proven = False

        # SUCCESSOR: human-chartered. Receipt required.
        if cap:
            rung_evidence.append({"rung": "SUCCESSOR", "status": "CAPPED_BY_CI",
                                  "refs": [f"ci:{r}" for r in cap_reasons] or ["ci:cap"]})
            successor_proven = False
        elif (cont_receipt and cont_receipt.get("qualification_run_id")
              and cont_receipt.get("chartered_by")):
            rung_evidence.append({
                "rung": "SUCCESSOR", "status": "PROVEN",
                "refs": [f"continuity_qualification:{cont_receipt['qualification_run_id']}@{sha[:8]}",
                         f"human_charter:{cont_receipt['chartered_by']}"],
            })
            successor_proven = True
        else:
            rung_evidence.append({"rung": "SUCCESSOR", "status": "UNKNOWN_NOT_QUALIFIED", "refs": []})
            successor_proven = False

        # Spec §4.6 / §2 "highest-first claim order": the organ's claim is a
        # PREFIX of the ladder. current_rung is the highest rung with every
        # rung below it PROVEN; missing_rung is the very next rung not
        # proven. Evidence for rungs above a gap stays recorded honestly in
        # rung_evidence but cannot be claimed until the gap closes — a green
        # INTEGRATION never hides a missing UNIT.
        prefix: list[str] = []
        for rung in RUNGS:
            status = next(e["status"] for e in rung_evidence if e["rung"] == rung)
            if status == "PROVEN":
                prefix.append(rung)
            else:
                break
        current_rung = prefix[-1] if prefix else "UNKNOWN"
        idx = RUNGS.index(current_rung) if current_rung in RUNGS else -1
        missing_rung = RUNGS[idx + 1] if idx + 1 < len(RUNGS) else None
        next_proof = (NEXT_PROOF[missing_rung].format(sha=sha, organ=organ, o=organ.lower())
                      if missing_rung else None)

        blockers = []
        if cap_reasons:
            blockers.append("required CI failing on stamped SHA: " + "; ".join(cap_reasons))
        if missing_rung in ("PRODUCTION",):
            blockers.append("human-only: Governed Production Promotion dispatch by Shawn required")
        if missing_rung == "SUCCESSOR":
            blockers.append("human-chartered: cold-successor qualification under the continuity charter")
        if missing_rung == "UNIT" and u is not None and u.get("conclusion") == "success":
            blockers.append(f"no organ-scoped test evidence for {organ} on stamped SHA")
        if missing_rung == "BEHAVIORAL":
            blockers.append(f"no live-{organ.lower()}-proof workflow run on stamped SHA")

        organ_entries.append({
            "organ": organ,
            "current_rung": current_rung,
            "missing_rung": missing_rung,
            "next_proof": next_proof,
            "blockers": blockers,
            "rung_evidence": rung_evidence,
        })

    matrix = {
        "schema": "naya/organ-health-matrix/v1",
        "spec_version": SPEC_VERSION,
        "stamped_sha": sha,
        "evaluated_at": _dt.datetime.now(_dt.timezone.utc).isoformat().replace("+00:00", "Z"),
        "evaluator": args.evaluator,
        "generator_version": args.generator_version,
        "ci_state_at_stamp": ci_state,
        "gate_coverage": gate_coverage,
        "stale_stamp": stale_stamp,
        "organs": organ_entries,
    }

    _self_validate(matrix)

    out = Path(args.out) if args.out else repo / ARTIFACT_REL
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(matrix, indent=1) + "\n", encoding="utf-8")
    sys.stdout.write(f"emitted {out} (stamped_sha={sha[:8]}, stale={stale_stamp})\n")
    return 0


def _self_validate(matrix: dict) -> None:
    """Mirror the machine schema's key constraints; refuse on violation."""
    if matrix["schema"] != "naya/organ-health-matrix/v1":
        raise Refused("self-validation: schema id mismatch")
    if matrix["spec_version"] != SPEC_VERSION:
        raise Refused("self-validation: spec_version mismatch")
    if not sha_ok(matrix["stamped_sha"]):
        raise Refused("self-validation: stamped_sha not 40-hex")
    organs = matrix["organs"]
    if len(organs) != 9 or [o["organ"] for o in organs] != ORGANS:
        raise Refused("self-validation: organs must be the 9 canonical organs in order")
    for o in organs:
        if o["current_rung"] not in (["UNKNOWN"] + RUNGS):
            raise Refused(f"self-validation: bad current_rung for {o['organ']}")
        if o["missing_rung"] not in MISSING_RUNG_ENUM + [None]:
            raise Refused(f"self-validation: bad missing_rung for {o['organ']}")
        if (o["missing_rung"] is None) != (o["next_proof"] is None):
            raise Refused(f"self-validation: missing_rung/next_proof must be null together for {o['organ']}")
        if o["current_rung"] == "SUCCESSOR" and o["missing_rung"] is not None:
            raise Refused(f"self-validation: SUCCESSOR reached but missing_rung set for {o['organ']}")
        ev = o["rung_evidence"]
        if [e["rung"] for e in ev] != RUNGS:
            raise Refused(f"self-validation: rung_evidence must cover all 8 rungs for {o['organ']}")
        for e in ev:
            if e["status"] not in RUNG_EVIDENCE_STATUSES:
                raise Refused(f"self-validation: bad rung_evidence status for {o['organ']}/{e['rung']}")
            if not isinstance(e["refs"], list):
                raise Refused(f"self-validation: refs must be a list for {o['organ']}/{e['rung']}")


if __name__ == "__main__":
    sys.exit(main())
