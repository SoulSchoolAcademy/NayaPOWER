#!/usr/bin/env python3
"""Issuance e2e under the PRODUCTION permission set (round-4, A4 lesson).

Round-3's 30/30 CI proof ran under the proof workflow's `actions: write`
token — it proved a different permission configuration than the delivery
workflow ships with. The delivery workflow grants exactly
`contents: read, pull-requests: read, actions: read`, and verify_issuance()'s
two Actions-API calls 403 without the Actions permission (round-3 finding:
every lawful delivery -> ISSUANCE_UNVERIFIABLE -> REJECT).

This script IS the re-proof: it runs in a CI job whose GITHUB_TOKEN carries
exactly the delivery workflow's permission set and exercises the real
verify_issuance() against the live API:
  1. genuine mint artifact bytes -> issuance genuine ([])
  2. one byte flipped -> ISSUANCE_BYTES_MISMATCH (forgery still caught)
  3. neither may return ISSUANCE_UNVERIFIABLE (the 403 symptom)

It finds the latest successful mint run with a live receipt artifact at
runtime, so the proof self-renews (artifacts expire; runs don't).

Exit 0 = proven. Exit 1 = NOT proven (fail closed, loud).
"""

import io
import json
import os
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from activation_gate import (  # noqa: E402 — the exact production code path
    verify_issuance, _api, _download_bytes, _sha256_hex, _normalize_repo,
    MINT_WORKFLOW_PATH, MINT_ARTIFACT_PREFIX)


def main():
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if not token:
        print("PERM-PROOF: FAIL — no GITHUB_TOKEN (cannot prove anything without the production token)")
        return 1
    repo = _normalize_repo(os.environ.get("GITHUB_REPOSITORY", ""))
    if not repo or "/" not in repo:
        print("PERM-PROOF: FAIL — no GITHUB_REPOSITORY")
        return 1
    truth = {"repository": repo}

    # 1. latest successful mint runs (Actions API — needs actions:read)
    try:
        runs = _api("GET", "/repos/%s/actions/workflows/%s/runs?status=success&per_page=10"
                    % (repo, "activation-mint.yml"), token)
    except RuntimeError as e:
        print("PERM-PROOF: FAIL — cannot list mint runs under this permission set: %s" % e)
        print("  (HTTP 403 here == the round-3 production break is still present)")
        return 1

    genuine_bytes = None
    attested_run_id = None
    tried = 0
    for r in (runs.get("workflow_runs") or []):
        if r.get("conclusion") != "success" or r.get("event") != "workflow_dispatch":
            continue
        if r.get("path") != MINT_WORKFLOW_PATH:
            continue
        tried += 1
        try:
            arts = _api("GET", "/repos/%s/actions/runs/%s/artifacts" % (repo, r["id"]), token)
        except RuntimeError:
            continue
        for a in arts.get("artifacts", []) or []:
            if not str(a.get("name", "")).startswith(MINT_ARTIFACT_PREFIX):
                continue
            try:
                blob = _download_bytes(a.get("archive_download_url", ""), token)
                z = zipfile.ZipFile(io.BytesIO(blob))
                names = [n for n in z.namelist() if os.path.basename(n) == "receipt.json"]
                if not names:
                    continue
                genuine_bytes = z.read(names[0])
                attested_run_id = r["id"]
                break
            except Exception:
                continue
        if genuine_bytes:
            break
        if tried >= 5:
            break

    if not genuine_bytes:
        print("PERM-PROOF: FAIL — no successful mint run with a live receipt artifact "
              "(tried %d runs; artifacts expire — dispatch the mint workflow to renew the proof)" % tried)
        return 1

    print("PERM-PROOF: attested run %s, genuine artifact %d bytes" % (attested_run_id, len(genuine_bytes)))
    receipt = json.loads(genuine_bytes)
    if not isinstance(receipt.get("attestation"), dict) or not receipt["attestation"].get("run_id"):
        print("PERM-PROOF: FAIL — artifact receipt carries no attestation")
        return 1

    # 2. genuine bytes -> issuance genuine. ANY ISSUANCE_UNVERIFIABLE here
    #    means the Actions API calls 403'd under this permission set.
    v = verify_issuance(receipt, genuine_bytes, truth, token)
    print("PERM-PROOF: genuine bytes -> %s" % (v if v else "[] (issuance genuine)"))
    if any("ISSUANCE_UNVERIFIABLE" in x for x in v):
        print("PERM-PROOF: FAIL — ISSUANCE_UNVERIFIABLE under the production permission set "
              "(the Actions API calls are still 403ing: the round-3 break is NOT fixed)")
        return 1
    if v:
        print("PERM-PROOF: FAIL — genuine issuance rejected: %s" % v[:2])
        return 1

    # 3. one byte flipped -> still caught (the permission fix must not
    #    weaken forgery detection).
    tampered = bytearray(genuine_bytes)
    tampered[len(tampered) // 2] ^= 0x01
    tampered = bytes(tampered)
    v2 = verify_issuance(receipt, tampered, truth, token)
    print("PERM-PROOF: tampered bytes -> %s" % (v2[:1] if v2 else "[]"))
    if not any("ISSUANCE_BYTES_MISMATCH" in x for x in v2):
        print("PERM-PROOF: FAIL — tampered bytes not caught: %s" % v2[:2])
        return 1

    print("PERM-PROOF: PASS — issuance e2e holds under the production permission set "
          "(contents:read, pull-requests:read, actions:read): genuine accepted, forgery caught, no 403")
    return 0


if __name__ == "__main__":
    sys.exit(main())
