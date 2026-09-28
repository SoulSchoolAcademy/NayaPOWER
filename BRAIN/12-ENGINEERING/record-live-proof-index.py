#!/usr/bin/env python3
"""Record a canonical pointer to a live proof run's evidence.

THE GAP THIS CLOSES
-------------------
The evidence that NayaPOWER works lives in GitHub Actions run logs and
artifacts. A cold Naya arriving tomorrow cannot reconstruct "what was proved"
from the repository - it would have to be told, or go spelunking through a run
id. That is exactly the failure the North Star forbids: intelligence that is not
preserved and governed in canonical form.

This does NOT copy the receipts into a second source of truth. It records
POINTERS and VERDICTS: the run, the exact canonical commit it executed, the
sha256 of each artifact, and what each artifact actually establishes - plus,
critically, what it does NOT establish.

Rules:
  * Regenerate from real downloaded artifacts. Never hand-write.
  * Every artifact digest is of the real bytes.
  * Every claim recorded here is re-checkable from the artifact bytes alone.
  * Limits are recorded alongside claims. A proof that hides its boundary is
    not evidence, it is marketing.

Usage:
  python BRAIN/12-ENGINEERING/record-live-proof-index.py <artifacts-dir> \
      --run-id <id> --head-sha <sha> [--notes "..."]
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "evidence" / "live-proof-index.json"


def digest(path: Path) -> tuple:
    raw = path.read_bytes()
    return hashlib.sha256(raw).hexdigest(), len(raw)


def find(root: Path, name: str) -> Path:
    hits = sorted(root.rglob(name))
    if not hits:
        raise SystemExit(f"error: artifact {name} not found under {root}. Refusing to index a partial run.")
    return hits[0]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("artifacts")
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--head-sha", required=True)
    ap.add_argument("--notes", default="")
    args = ap.parse_args()
    root = Path(args.artifacts).resolve()
    if not root.is_dir():
        print(f"error: {root} is not a directory")
        return 2

    def J(name):
        return json.loads(find(root, name).read_text(encoding="utf-8"))

    cs = J("cold-successor-receipt.json")
    csv = J("cold-successor-receipt-verified.json")
    cr = J("causal-learning-experiment-receipt.json")
    gv = J("cold-graph-independent-verification.json")
    gp = J("cold-graph-behavior-pair.json")
    lc = J("live-connect-runtime-receipt.json")

    ab = cs["authority_boundary"]
    basis = cr["independent_verification_basis"]
    recomp = basis["recomputed_from_authoritative_state"]
    lv = gv.get("verification", gv)

    artifacts = {}
    for p in sorted(root.rglob("*.json")):
        d, n = digest(p)
        artifacts[p.name] = {"digest_sha256": d, "bytes": n}

    index = {
        "schema": "NAYAPOWER_LIVE_PROOF_INDEX_V1",
        "run_id": args.run_id,
        "head_sha": args.head_sha,
        "recorded_from": "gh run download artifacts; digests are of the real artifact bytes",
        "notes": args.notes,
        "artifacts": artifacts,
        "establishes": {
            "connect_authority_boundary": {
                "artifact": "live-connect-runtime-receipt.json",
                "behavior": lc["receipt"]["behavior"],
                "authority_boundary": lc["receipt"]["authority_boundary"],
                "establishes": "CONNECT enumerates relationships and explicitly records that it does "
                               "NOT authorize a consequential action; blocked_by LAW, executed false.",
                "does_not_establish": "It does not establish that any other function respects this boundary.",
            },
            "cold_successor_continuity": {
                "artifact": "cold-successor-receipt.json",
                "cold_start": cs["cold_start"],
                "authority_boundary": ab,
                "reconstructed_lesson": cs["reconstruction"]["retrieved_lesson"],
                "verified_relationship_count": cs["reconstruction"]["verified_relationship_count"],
                "independent_recheck": {"artifact": "cold-successor-receipt-verified.json",
                                        "successor_grant_count": csv.get("successor_grant_count")},
                "establishes": "A cold runtime, given no local state and no intelligence content, "
                               "reconstructed the retained lesson, its lineage and its VERIFIED "
                               "relationships, and inherited ZERO authority.",
                "does_not_establish": "It does not establish that the successor then performed a real "
                                      "task end-to-end. That is the recorded next_action.",
            },
            "causal_learning_influence": {
                "artifact": "causal-learning-experiment-receipt.json",
                "executor_runtime_jti": cr.get("executor_runtime_jti"),
                "verifier_runtime_jti": cr.get("verifier_runtime_jti"),
                "independent_verification_basis": basis,
                "establishes": "On a bounded paired experiment, a second OIDC runtime recomputed the "
                               "causal verdict from authoritative state and did not trust the executor.",
                "does_not_establish": cr.get("limitations"),
            },
            "graph_context_behavioural_influence": {
                "artifact": "cold-graph-independent-verification.json",
                "control_behavior": gp["control"]["behavior"],
                "treatment_behavior": gp["treatment"]["behavior"],
                "independent_verification": lv,
                "establishes": "With only graph context differing, a cold Naya changed behaviour from "
                               "requiring direct canonical intelligence to applying contextualized "
                               "VERIFIED intelligence, independently re-read from persisted receipts.",
                "does_not_establish": "One held-out task. This is NOT evidence of generalized "
                                      "intelligence, and must never be reported as such.",
            },
        },
        "how_to_verify": (
            "Download the artifacts for this run and recompute each digest with "
            "`sha256sum`. Every claim in 'establishes' is re-checkable from the artifact bytes. "
            "Regenerate this file with record-live-proof-index.py; never hand-edit it."
        ),
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
    print(f"recorded live proof index -> {OUT.relative_to(REPO).as_posix()}")
    print(f"  run     : {index['run_id']}")
    print(f"  head sha: {index['head_sha']}")
    print(f"  artifacts indexed: {len(artifacts)}")
    for name, v in index["establishes"].items():
        print(f"  - {name}: {v['does_not_establish']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
