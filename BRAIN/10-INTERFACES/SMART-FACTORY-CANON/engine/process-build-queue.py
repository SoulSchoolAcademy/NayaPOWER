#!/usr/bin/env python3
"""Cured Build Queue Processor — factory-r1 (R1 proposal, NOT the live file).

Polls Supabase build_queue, builds apps HONORING the contract, updates status.

THE CURE vs the live processor (~/workspace/factory-pipeline/process-build-queue.py):
  BEFORE: base template hardcoded to personal-v5.html for every build;
          contract.name replaced one demo string; contract.idea hit a bare
          `pass`; template / pieces / functions / vision / do / behave /
          rules were never read. Every app was the personal page renamed.
  AFTER:  the base template is selected from the contract's chosen template
          via templates-registry.json (unknown or missing-base templates
          FAIL the build honestly — personal is never silently substituted);
          every contract field is applied where the base has a real slot
          and logged NOT-APPLIED with a reason where it does not (see
          customize.py); the receipt carries the full applied/not-applied
          ledger; deploy goes through deploy.py (CSS brace gate).

Modes:
  (no args)        poll 'pending' builds, oldest first, limit 5 (live parity)
  --only <id>      process exactly that one build row, whatever its status
                   (test mode — used for the R1 test-flagged row only)
"""

import json
import os
import re
import sys
import time
import hashlib
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import add_surrogate_to_request
from customize_contract import apply_contract
from deploy import deploy

SUPABASE_URL = "https://dahisasgpfvziswqvmvm.supabase.co"
ACCT = "b5e2a51b3e883f7722287c5f51b1196b"
CF_BASE = "https://api.cloudflare.com/client/v4"
REGISTRY_PATH = os.path.join(HERE, "templates-registry.json")
BUILDS_DIR = os.path.join(HERE, "builds")
PROCESSOR_TAG = "factory-r1-cured-v1 (R1 proposal — not yet swapped in)"


def sb_request(method, path, data=None):
    url = SUPABASE_URL + path
    headers = {
        'Content-Type': 'application/json',
        'Prefer': 'return=representation',
    }
    req_data = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=req_data, method=method, headers=headers)
    add_surrogate_to_request(req, "custom.supabase-anon",
                             allowed_hosts=["dahisasgpfvziswqvmvm.supabase.co"])
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def load_registry():
    with open(REGISTRY_PATH) as f:
        return json.load(f)


def normalize_template(raw):
    """'Personal' -> 'personal', 'Smart List' -> 'smart-list'."""
    return re.sub(r"\s+", "-", str(raw or "").strip().lower())


def slugify(text):
    slug = re.sub(r"[^a-z0-9]+", "-", str(text or "").lower()).strip("-")
    return slug[:30] or "app"


def enable_subdomain(worker_name):
    """Enable workers.dev for the worker (same step the old pipeline ran)."""
    url = f"{CF_BASE}/accounts/{ACCT}/workers/scripts/{worker_name}/subdomain"
    req = urllib.request.Request(
        url, data=json.dumps({"enabled": True}).encode(), method='POST',
        headers={'Content-Type': 'application/json'})
    add_surrogate_to_request(req, "custom.cloudflare",
                             allowed_hosts=["api.cloudflare.com"])
    with urllib.request.urlopen(req, timeout=30):
        pass


def fail_build(build_id, receipt):
    receipt.setdefault('build_id', build_id)
    receipt.setdefault('built_at', time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))
    receipt['processor'] = PROCESSOR_TAG
    sb_request('PATCH', f'/rest/v1/build_queue?id=eq.{build_id}',
               {'status': 'failed', 'receipt': receipt})
    print(f"Build {build_id} FAILED honestly: {receipt.get('error')}")


def process_build(build):
    build_id = build['id']
    contract = build.get('contract') or {}
    print(f"Processing build {build_id}...")
    sb_request('PATCH', f'/rest/v1/build_queue?id=eq.{build_id}',
               {'status': 'building'})

    ledger = []
    try:
        # --- (a) template selection: the contract chooses, or the build
        #         fails honestly. NEVER a silent personal substitution. ---
        raw_template = contract.get('template')
        tkey = normalize_template(raw_template)
        registry = load_registry()
        entry = registry.get('templates', {}).get(tkey)
        if entry is None:
            reason = (registry.get('missing', {}).get(tkey)
                      or f"template '{raw_template}' is not in the registry")
            ledger.append({"field": "template", "status": "NOT-APPLIED",
                           "reason": reason})
            fail_build(build_id, {
                'error': f"template not buildable: {reason}",
                'template_requested': raw_template,
                'not_applied': ledger,
            })
            return
        base_path = os.path.join(HERE, entry['file'])
        with open(base_path, 'rb') as f:
            base_bytes = f.read()
        base_md5 = hashlib.md5(base_bytes).hexdigest()
        if base_md5 != entry['md5']:
            raise Exception(
                f"template base drift: {entry['file']} md5 {base_md5} "
                f"!= registry {entry['md5']}")
        html = base_bytes.decode('utf-8')
        ledger.append({
            "field": "template", "status": "APPLIED",
            "detail": f"base = contract's chosen template '{tkey}' "
                      f"({entry['file']}, md5 {base_md5[:12]}…, "
                      f"source: {entry['source']})",
        })

        # --- (b)+(c) branding + pieces, every field ledgered ------------
        html, field_ledger = apply_contract(html, contract,
                                            entry.get('base_identity'))
        ledger.extend(field_ledger)

        # --- (d) worker name from the contract's slug -------------------
        handle = contract.get('handle') or slugify(contract.get('name'))
        handle = slugify(handle)
        worker_name = f"naya-app-{handle}-{build_id[:8]}"

        # --- evidence artifact + gated deploy ---------------------------
        os.makedirs(BUILDS_DIR, exist_ok=True)
        artifact = os.path.join(BUILDS_DIR, f"{build_id}.html")
        with open(artifact, 'w') as f:
            f.write(html)

        url = deploy(artifact, worker_name)   # deploy.py: CSS gate inside
        if not url:
            fail_build(build_id, {
                'error': 'deploy blocked/failed (see deploy.py output — CSS gate or Cloudflare)',
                'template': tkey,
                'applied': [e for e in ledger if e['status'] == 'APPLIED'],
                'not_applied': [e for e in ledger if e['status'] == 'NOT-APPLIED'],
            })
            return
        enable_subdomain(worker_name)

        # --- (e) full status writeback ----------------------------------
        receipt = {
            'build_id': build_id,
            'worker': worker_name,
            'url': url,
            'contract_handle': handle,
            'template': tkey,
            'template_base': {
                'file': entry['file'], 'md5': base_md5,
                'source': entry['source'], 'body_note': entry['body_note'],
            },
            'applied': [e for e in ledger if e['status'] == 'APPLIED'],
            'not_applied': [e for e in ledger if e['status'] == 'NOT-APPLIED'],
            'built_at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            'processor': PROCESSOR_TAG,
        }
        sb_request('PATCH', f'/rest/v1/build_queue?id=eq.{build_id}', {
            'status': 'done',
            'result_url': url,
            'receipt': receipt,
        })
        print(f"Build {build_id} done: {url}")
        print(f"  applied: {[e['field'] for e in receipt['applied']]}")
        print(f"  NOT-APPLIED: {[e['field'] for e in receipt['not_applied']]}")

    except Exception as e:
        print(f"Build {build_id} failed: {e}")
        fail_build(build_id, {
            'error': str(e),
            'applied': [x for x in ledger if x['status'] == 'APPLIED'],
            'not_applied': [x for x in ledger if x['status'] == 'NOT-APPLIED'],
        })


def main():
    if '--only' in sys.argv:
        build_id = sys.argv[sys.argv.index('--only') + 1]
        rows = sb_request('GET', f'/rest/v1/build_queue?id=eq.{build_id}')
        if not rows:
            print(f"No build row with id {build_id}")
            sys.exit(1)
        process_build(rows[0])
        return
    builds = sb_request(
        'GET', '/rest/v1/build_queue?status=eq.pending&order=created_at.asc&limit=5')
    print(f"Found {len(builds)} pending builds")
    for build in builds:
        process_build(build)


if __name__ == '__main__':
    main()
