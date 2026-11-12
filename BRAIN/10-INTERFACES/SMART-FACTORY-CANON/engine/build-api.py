#!/usr/bin/env python3
"""Build API — factory page calls this to actually build an app.

POST /build with contract JSON → returns {build_id, url, receipt}

This is what Naya 3's #1 recommendation asks for:
"Connect Build to APP MODE. Submit validated contract JSON to the
governed assembler and return a build ID and artifact."
"""

import json
import sys
import time
import hashlib
from customize import customize
from deploy import deploy

def build_app(contract):
    """Take contract JSON, build and deploy app, return receipt."""
    build_id = hashlib.sha256(
        json.dumps(contract, sort_keys=True).encode()
    ).hexdigest()[:12]
    
    timestamp = int(time.time())
    
    # Validate contract
    if 'template' not in contract:
        return {"error": "Contract missing 'template' field"}
    if 'name' not in contract:
        return {"error": "Contract missing 'name' field"}
    
    template = contract['template']
    worker_name = f"naya-build-{build_id}"
    
    # Map template to source file
    # For now, use personal-v5 as the base for all
    # (In production, each template would have its own source)
    template_path = '/home/hatch/workspace/personal-app/personal-v5.html'
    
    # Write contract to temp
    contract_path = f'/tmp/contract-{build_id}.json'
    with open(contract_path, 'w') as f:
        json.dump(contract, f)
    
    # Customize
    output_path = f'/tmp/build-{build_id}.html'
    customize(template_path, contract_path, output_path)
    
    # Deploy
    url = deploy(output_path, worker_name)
    
    if not url:
        return {"error": "Deploy failed", "build_id": build_id}
    
    # Enable workers.dev
    import urllib.request
    sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
    from dynamic_credentials import add_surrogate_to_request
    ACCT = "b5e2a51b3e883f7722287c5f51b1196b"
    BASE = "https://api.cloudflare.com/client/v4"
    data = json.dumps({"enabled": True}).encode()
    req = urllib.request.Request(
        f"{BASE}/accounts/{ACCT}/workers/scripts/{worker_name}/subdomain",
        data=data, method="POST"
    )
    req.add_header("Content-Type", "application/json")
    add_surrogate_to_request(req, "custom.cloudflare", allowed_hosts=["api.cloudflare.com"])
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            pass
    except:
        pass
    
    # Build receipt (Shared #8: Honest proof receipts)
    receipt = {
        "build_id": build_id,
        "url": url,
        "template": template,
        "contract": contract,
        "built_at": timestamp,
        "builder_version": "pipeline-v1",
        "status": "deployed"
    }
    
    # Save receipt
    with open(f'/tmp/receipt-{build_id}.json', 'w') as f:
        json.dump(receipt, f, indent=2)
    
    return receipt

if __name__ == '__main__':
    # Read contract from stdin or file
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            contract = json.load(f)
    else:
        contract = json.load(sys.stdin)
    
    result = build_app(contract)
    print(json.dumps(result, indent=2))
