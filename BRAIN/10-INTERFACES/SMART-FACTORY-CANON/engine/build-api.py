#!/usr/bin/env python3
"""Build API — the factory page's direct-build door (R1b cure).

POST /build with contract JSON → returns {build_id, url, receipt}

This is what Naya 3's #1 recommendation asks for:
"Connect Build to APP MODE. Submit validated contract JSON to the
governed assembler and return a build ID and artifact."

R1b cure (2026-10-22, Lane D — Factory Contracts). The queue door was
cured in R1; this direct door was not. Two defects are cured here:

1. LEGACY CUSTOMIZER — this module imported the legacy ``customize``
   module, which silently drops contract fields it cannot place. It now
   applies the contract through ``customize_contract.apply_contract``,
   whose receipt ledger names every field APPLIED or NOT-APPLIED with
   the reason. Silent drops are structurally impossible on this door too.
2. HARDCODED BASE — the base was a machine-local absolute path
   (``/home/hatch/workspace/personal-app/personal-v5.html``) used for
   every template key. The template key now resolves through
   ``templates-registry.json`` — the file the engine actually reads —
   the base bytes are md5/byte-verified against the registry before
   use, and a key listed in the registry's ``missing`` map (or an
   unknown key) fails honestly WITHOUT deploying anything.
"""

import hashlib
import json
import os
import re
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from customize_contract import apply_contract  # noqa: E402

REGISTRY_PATH = os.path.join(HERE, "templates-registry.json")


class BuildError(Exception):
    """A contract that must not build; the message is the honest reason."""


def load_registry(registry_path=REGISTRY_PATH):
    with open(registry_path) as f:
        return json.load(f)


def resolve_template(template_key, registry=None):
    """Resolve a contract template key to verified base bytes.

    Returns (entry, html_text). Raises BuildError — with the registry's
    own note for `missing` keys — when the key cannot build."""
    registry = registry if registry is not None else load_registry()
    key = str(template_key or "").strip().lower()
    if not key:
        raise BuildError("Contract missing 'template' field")

    missing = registry.get("missing", {})
    if key in missing:
        raise BuildError(
            f"template {key!r} has no base yet (registry.missing): "
            f"{missing[key]}"
        )

    entry = registry.get("templates", {}).get(key)
    if entry is None:
        raise BuildError(
            f"unknown template {key!r}: not in templates-registry.json "
            f"(available: {', '.join(sorted(registry.get('templates', {})))})"
        )

    path = os.path.join(HERE, entry["file"])
    if not os.path.exists(path):
        raise BuildError(
            f"registry template file missing on disk: {entry['file']}"
        )
    with open(path, "rb") as f:
        body = f.read()
    observed_md5 = hashlib.md5(body).hexdigest()
    if entry.get("md5") and observed_md5 != entry["md5"]:
        raise BuildError(
            f"template base drift for {key!r}: file md5 {observed_md5} "
            f"!= registry md5 {entry['md5']} — refusing to build on "
            f"unverified bytes"
        )
    if entry.get("bytes") and len(body) != entry["bytes"]:
        raise BuildError(
            f"template base drift for {key!r}: file is {len(body)} bytes, "
            f"registry says {entry['bytes']}"
        )
    return entry, body.decode("utf-8")


def _enable_subdomain(worker_name):
    """Best-effort workers.dev enable (unchanged behavior from v1:
    a failure here never fails the build)."""
    import urllib.request

    sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
    from dynamic_credentials import add_surrogate_to_request

    acct = "b5e2a51b3e883f7722287c5f51b1196b"
    base = "https://api.cloudflare.com/client/v4"
    data = json.dumps({"enabled": True}).encode()
    req = urllib.request.Request(
        f"{base}/accounts/{acct}/workers/scripts/{worker_name}/subdomain",
        data=data, method="POST",
    )
    req.add_header("Content-Type", "application/json")
    add_surrogate_to_request(
        req, "custom.cloudflare", allowed_hosts=["api.cloudflare.com"]
    )
    try:
        with urllib.request.urlopen(req, timeout=30):
            pass
        return True
    except Exception:
        return False


def build_app(contract, deploy_fn=None, enable_subdomain_fn=None):
    """Take contract JSON, build and deploy app, return receipt.

    deploy_fn / enable_subdomain_fn are injectable so the door's logic
    (registry resolution, honest failure, ledger) is testable without
    touching Cloudflare."""
    build_id = hashlib.sha256(
        json.dumps(contract, sort_keys=True).encode()
    ).hexdigest()[:12]

    if "template" not in contract:
        return {"error": "Contract missing 'template' field"}
    if "name" not in contract:
        return {"error": "Contract missing 'name' field"}

    try:
        entry, html = resolve_template(contract["template"])
    except BuildError as exc:
        return {"error": str(exc), "build_id": build_id,
                "template": contract.get("template")}

    html, ledger = apply_contract(
        html, contract, entry.get("base_identity") or {}
    )

    handle = str(contract.get("handle") or "").strip().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", handle).strip("-")
    worker_name = f"naya-app-{slug}" if slug else f"naya-build-{build_id}"

    if deploy_fn is None:
        from deploy import deploy as deploy_fn  # lazy: credentials seam
    if enable_subdomain_fn is None:
        enable_subdomain_fn = _enable_subdomain

    with tempfile.TemporaryDirectory(prefix=f"naya-build-{build_id}-") as tmp:
        output_path = os.path.join(tmp, "index.html")
        with open(output_path, "w") as f:
            f.write(html)
        url = deploy_fn(output_path, worker_name)

    if not url:
        return {"error": "Deploy failed", "build_id": build_id}

    enable_subdomain_fn(worker_name)

    not_applied = [row["field"] for row in ledger
                   if row.get("status") == "NOT-APPLIED"]

    # Build receipt (Shared #8: Honest proof receipts) — now carrying the
    # application ledger so no contract field can vanish silently.
    receipt = {
        "build_id": build_id,
        "url": url,
        "worker": worker_name,
        "template": contract["template"],
        "template_file": entry["file"],
        "template_md5": entry.get("md5"),
        "contract": contract,
        "ledger": ledger,
        "not_applied": not_applied,
        "built_at": int(time.time()),
        "builder_version": "pipeline-v2-registry",
        "status": "deployed",
    }
    return receipt


if __name__ == "__main__":
    # Read contract from stdin or file
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            contract = json.load(f)
    else:
        contract = json.load(sys.stdin)

    result = build_app(contract)
    print(json.dumps(result, indent=2))
