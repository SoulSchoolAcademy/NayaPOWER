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

L3 (2026-11-11): process_build() reads the project's PI record keyed by
the contract's project_id from the PI store (project-intelligence/state/
state.json) BEFORE template selection and merges vision / goal / mission /
about / name / title / tagline / notes / links into the contract — the
citizen's typed contract values win where both exist. Every PI field is
ledgered APPLIED (from PI) or NOT-APPLIED (PI empty) in the receipt.
No project_id: the read is skipped honestly, the build proceeds as today.

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
import importlib.util
import subprocess
import tempfile
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
PROCESSOR_TAG = "factory-r1-cured-v1 + GT-028 contract gate (canon standard-feature contracts govern builds) + L3 PI read (project-intelligence)"

# --- L3: the processor reads Project Intelligence ---------------------------
# The PI store of record on this machine is the PI state file — the same
# state.json the PI render (project-intelligence/generator/render.py) reads
# to build the Living List. The live path is the PI Supabase tables; no PI
# Supabase connection is registered on this VM, so the live read is NOT
# attempted here — the gap is named in the lane record, never claimed.
# PI_STATE_PATH may be overridden by environment for tests only, so a test
# build can point at a copy of the store carrying a known project record
# without touching the live PI state.
PI_STATE_PATH = os.environ.get(
    "PI_STATE_PATH",
    os.path.join(os.path.expanduser("~"), "workspace",
                 "project-intelligence", "state", "state.json"))
# The merge fields — exactly these names, shared with lanes L1 and L2.
# vision / goal / mission / about are the Step 1 fields; name / title /
# tagline are the identity fields; notes / links are what the citizen
# already fed into PI. Never invent a field name.
PI_MERGE_FIELDS = ("vision", "goal", "mission", "about", "name", "title",
                   "tagline", "notes", "links")

# --- GT-028: canon standard-feature contracts -------------------------------
# The canon contracts + checker live in the repo at
# BRAIN/10-INTERFACES/SMART-FACTORY-CANON/engine/ (PR #2888, certified by Chi,
# R1-CERT-2888.md). At build time the gate reads them from the repo clone's
# origin/main ref via `git show` (immune to the clone's working-tree state);
# if that read fails it falls back to the vendored snapshot in canon/ beside
# this file (see canon/PROVENANCE.json). If neither source loads, the build
# FAILS HONESTLY — there is no unchecked deploy path.
CANON_ENGINE_REL = "BRAIN/10-INTERFACES/SMART-FACTORY-CANON/engine"
REPO_CLONE = os.path.expanduser("~/workspace/nayapower-repo")
CANON_SNAPSHOT_DIR = os.path.join(HERE, "canon")

# GT-028 contract gate mode.
# Advisory mode (STRICT=False): the gate scores every build and records the
# full contract_check block in the receipt (pass and fail alike), but never
# blocks deploy — the dialect-reconciliation canon PR (GT-028 half 2) is not
# yet merged through the dock, and the live flagships' features are
# dialect-mismatched, not defective. A gate that stops the flow is a defect
# (Shawn's Balanced Machine law). Only when the reconciled canon PR has merged
# through the dock AND the reconciled contracts make the live flagships score
# 13/13 may this flip back to True: strict mode then fails the build honestly
# (no deploy) on any failed feature. A gate that cannot run at all (canon
# unavailable/invalid) always fails the build honestly, in either mode.
CONTRACT_GATE_STRICT = True


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


def _load_canon():
    """Load (checker_module, canon_registry, provenance) for the GT-028 gate.

    Primary: repo clone origin/main via git show. Fallback: vendored snapshot
    in CANON_SNAPSHOT_DIR. Raises RuntimeError if neither source loads — the
    caller fails the build honestly rather than deploying unchecked.
    """
    checker_bytes = registry_bytes = None
    provenance = {}
    try:
        ref = subprocess.run(['git', '-C', REPO_CLONE, 'rev-parse', 'origin/main'],
                             capture_output=True, text=True, timeout=30)
        if ref.returncode != 0:
            raise RuntimeError(ref.stderr.strip() or 'rev-parse failed')
        ref = ref.stdout.strip()
        blobs = {}
        for name in ('check_standard_features.py', 'templates-registry.json'):
            r = subprocess.run(
                ['git', '-C', REPO_CLONE, 'show',
                 f'origin/main:{CANON_ENGINE_REL}/{name}'],
                capture_output=True, timeout=30)
            if r.returncode != 0:
                raise RuntimeError(f'git show {name} failed')
            blobs[name] = r.stdout
        checker_bytes = blobs['check_standard_features.py']
        registry_bytes = blobs['templates-registry.json']
        provenance = {'source': 'repo clone origin/main (git show)',
                      'canon_ref': ref}
    except Exception:
        checker_bytes = registry_bytes = None
    if checker_bytes is None:
        try:
            with open(os.path.join(CANON_SNAPSHOT_DIR,
                                   'check_standard_features.py'), 'rb') as f:
                checker_bytes = f.read()
            with open(os.path.join(CANON_SNAPSHOT_DIR,
                                   'templates-registry.json'), 'rb') as f:
                registry_bytes = f.read()
            with open(os.path.join(CANON_SNAPSHOT_DIR,
                                   'PROVENANCE.json')) as f:
                snap = json.load(f)
            provenance = {'source': 'vendored snapshot (factory-pipeline/canon)',
                          'canon_ref': snap.get('canon_ref')}
        except Exception as e:
            raise RuntimeError(
                f'canon contracts unavailable (git show and snapshot both '
                f'failed): {e}')
    provenance['checker_sha256'] = hashlib.sha256(checker_bytes).hexdigest()
    provenance['registry_sha256'] = hashlib.sha256(registry_bytes).hexdigest()
    tmp = tempfile.NamedTemporaryFile('wb', suffix='.py',
                                      prefix='canon-checker-', delete=False)
    try:
        tmp.write(checker_bytes)
        tmp.close()
        spec = importlib.util.spec_from_file_location(
            'canon_check_standard_features', tmp.name)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    finally:
        try:
            os.unlink(tmp.name)
        except OSError:
            pass
    registry = json.loads(registry_bytes.decode('utf-8'))
    return module, registry, provenance


def run_contract_gate(html, build_id):
    """Score the built artifact against the canon standard-feature contracts.

    Returns the receipt-ready gate block (per-feature PASS/FAIL + provenance).
    Raises RuntimeError if the gate itself cannot run.
    """
    try:
        checker, registry, provenance = _load_canon()
        errors = checker.validate_contracts(registry)
        if errors:
            raise RuntimeError('canon contracts invalid: ' + '; '.join(errors))
        report = checker.evaluate(
            html.encode('utf-8'),
            {'source': f'build_queue artifact {build_id}'}, registry)
    except RuntimeError:
        raise
    except Exception as e:
        raise RuntimeError(f'contract gate could not run: {e}')
    gate = {
        'contract_version': report.get('contract_version'),
        'canon': provenance,
        'score': report['score'],
        'features': [{
            'code': f['code'], 'id': f['id'], 'status': f['status'],
            'failed_required_checks': f['failed_required_checks'],
            'failed_any_groups': f['failed_any_groups'],
        } for f in report['features']],
    }
    try:  # full per-check evidence beside the artifact
        with open(os.path.join(BUILDS_DIR, f'{build_id}.contract.json'),
                  'w') as fh:
            json.dump(report, fh, indent=2)
    except Exception:
        pass
    return gate


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


def _pi_value_present(value):
    """True when a PI value is real content, not an empty string/list."""
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict)):
        return bool(value)
    return True


def _pi_field(record, field):
    """One merge field out of a PI project record, harvested from the
    shapes the PI store actually carries today.

    L1's project shape carries the fields as top-level keys; the store's
    current work-item shape carries the same meaning under neighbouring
    keys, so the read checks those too — never a second store, just the
    one record read two honest ways:
      notes: 'notes', else the item 'body' (the notes the citizen wrote)
      links: 'links', else 'sources', else the face's links, else 'proof'
      about: 'about', else 'body'
      name:  'name', else 'alias'
      title: 'title' (work items carry it; project records may too)
    """
    if not isinstance(record, dict):
        return None
    if field in record and _pi_value_present(record.get(field)):
        return record[field]
    face = record.get('face') if isinstance(record.get('face'), dict) else {}
    if field == 'notes':
        return record.get('body') or None
    if field == 'links':
        return (record.get('sources') or face.get('links')
                or record.get('proof') or None)
    if field == 'about':
        return record.get('body') or None
    if field == 'name':
        return record.get('alias') or None
    return None


def read_pi_record(project_id, state_path=None):
    """Read one project's PI record from the PI store, keyed by project_id.

    Returns {'record': dict|None, 'source': str, 'found': bool,
             'error': str|None}. The lookup follows the shapes the store
    carries: L1's 'projects' (dict keyed by project_id, or list of
    project records) first, then the current 'items' list by id, then a
    single-project file. A missing store or an unreadable file is
    reported in 'error' — never raised — so the build can proceed
    exactly as today with the ledger saying why PI gave nothing.
    """
    path = state_path or PI_STATE_PATH
    try:
        with open(path) as f:
            state = json.load(f)
    except Exception as e:
        return {'record': None,
                'source': f'PI store {path}',
                'found': False,
                'error': f'PI store unreadable: {e}'}
    if not isinstance(state, dict):
        return {'record': None, 'source': f'PI store {path}',
                'found': False,
                'error': 'PI store is not a JSON object'}
    projects = state.get('projects')
    if isinstance(projects, dict) and project_id in projects:
        return {'record': projects[project_id],
                'source': f'PI store {path} (projects[{project_id!r}])',
                'found': True, 'error': None}
    if isinstance(projects, list):
        for p in projects:
            if isinstance(p, dict) and (
                    p.get('project_id') == project_id
                    or p.get('id') == project_id):
                return {'record': p,
                        'source': f'PI store {path} (projects list)',
                        'found': True, 'error': None}
    items = state.get('items')
    if isinstance(items, list):
        for item in items:
            if isinstance(item, dict) and (
                    item.get('project_id') == project_id
                    or item.get('id') == project_id):
                return {'record': item,
                        'source': f'PI store {path} (items list, id)',
                        'found': True, 'error': None}
    if state.get('project_id') == project_id:
        return {'record': state, 'source': f'PI store {path} (whole file)',
                'found': True, 'error': None}
    return {'record': None, 'source': f'PI store {path}',
            'found': False,
            'error': None}


def merge_pi_into_contract(contract, pi_record, project_id):
    """Merge a PI record into the contract and ledger every field.

    PRECEDENCE RULE (stated in the record, applied here): the citizen's
    typed contract values win where both exist — a PI value only fills a
    field the contract does not already carry. Every field ends with a
    ledger entry: APPLIED (from PI) when PI supplied the value,
    NOT-APPLIED with the reason when PI was empty or the contract won.
    No silent drops: a field the read touches is always ledgered.
    """
    ledger = []
    for field in PI_MERGE_FIELDS:
        pi_value = _pi_field(pi_record, field)
        if contract.get(field) and _pi_value_present(contract.get(field)):
            if _pi_value_present(pi_value):
                ledger.append({
                    "field": f"pi.{field}", "status": "NOT-APPLIED",
                    "reason": ("PI has a value, but the contract already "
                               "carries one — the citizen's typed contract "
                               "wins (precedence rule). PI value stays in "
                               "PI, not applied to this build."),
                })
            else:
                ledger.append({
                    "field": f"pi.{field}", "status": "NOT-APPLIED",
                    "reason": ("contract already carries a value and PI "
                               "has nothing for this field."),
                })
            continue
        if not _pi_value_present(pi_value):
            ledger.append({
                "field": f"pi.{field}", "status": "NOT-APPLIED",
                "reason": "PI empty for this field — nothing to fill from.",
            })
            continue
        contract[field] = pi_value
        preview = pi_value if isinstance(pi_value, str) else json.dumps(pi_value)
        ledger.append({
            "field": f"pi.{field}", "status": "APPLIED",
            "detail": (f"from PI (project {project_id}), merged into the "
                       f"contract: {str(preview)[:80]} (page placement "
                       f"is the customizer's ledger, not this entry)"),
        })
    return ledger


def process_build(build):
    build_id = build['id']
    contract = build.get('contract') or {}
    print(f"Processing build {build_id}...")
    sb_request('PATCH', f'/rest/v1/build_queue?id=eq.{build_id}',
               {'status': 'building'})

    ledger = []
    # The PI read block, filled below before template selection; defined
    # here so every receipt path (including the except path) can carry it.
    pi_read = {'project_id': contract.get('project_id'),
               'source': None, 'status': 'not-run',
               'reason': 'PI read had not run when the build ended.'}
    try:
        # --- (a0) THE PROCESSOR READS PI (L3) -------------------------
        # After the contract is loaded, BEFORE template selection: read
        # the project's PI record keyed by the contract's project_id and
        # merge it into the contract. A build with rich PI and a build
        # with empty PI must never again build identically — the receipt
        # says which fields PI supplied. No project_id: the read is
        # skipped honestly and the build proceeds exactly as today.
        project_id = contract.get('project_id')
        if not project_id:
            pi_read = {
                'project_id': None,
                'source': None,
                'status': 'skipped',
                'reason': ('contract carries no project_id (an old build, '
                           'or a build from before the flow carries it) — '
                           'PI read skipped honestly; build proceeds '
                           'exactly as today.'),
            }
            ledger.append({
                "field": "pi.read", "status": "NOT-APPLIED",
                "reason": pi_read['reason'],
            })
        else:
            project_id = str(project_id)
            pi = read_pi_record(project_id)
            pi_read = {
                'project_id': project_id,
                'source': pi['source'],
                'status': ('unavailable' if pi['error']
                           else 'found' if pi['found'] else 'not-found'),
                'reason': (pi['error'] or
                           (f"PI record for project {project_id} found."
                            if pi['found'] else
                            f"no PI record for project {project_id} in "
                            f"the PI store — PI empty for this project.")),
            }
            if pi['error'] or not pi['found']:
                for field in PI_MERGE_FIELDS:
                    ledger.append({
                        "field": f"pi.{field}", "status": "NOT-APPLIED",
                        "reason": pi_read['reason'],
                    })
            else:
                ledger.extend(
                    merge_pi_into_contract(contract, pi['record'],
                                           project_id))

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
                'pi_read': pi_read,
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
        worker_name = f"naya-app-{handle}"

        # --- evidence artifact ------------------------------------------
        os.makedirs(BUILDS_DIR, exist_ok=True)
        artifact = os.path.join(BUILDS_DIR, f"{build_id}.html")
        with open(artifact, 'w') as f:
            f.write(html)

        # --- GT-028 contract gate ---------------------------------------
        # Advisory mode (CONTRACT_GATE_STRICT=False): every build is scored
        # against the canon contracts and the full contract_check block lands
        # in the receipt, but the gate never blocks deploy. Strict mode
        # (flag flips after the dialect-reconciliation canon PR merges and the
        # live flagships score full) fails the build honestly here instead.
        # A gate that cannot run at all always fails the build honestly —
        # that path is handled by the outer except via fail_build. ---
        gate = run_contract_gate(html, build_id)
        if (CONTRACT_GATE_STRICT
                and gate['score']['passed'] != gate['score']['total']):
            failed = [f for f in gate['features'] if f['status'] != 'PASS']
            names = "; ".join(
                f"{f['code']} {f['id']} (failed: "
                + ", ".join(f['failed_required_checks']
                            + [f"any:{g}" for g in f['failed_any_groups']])
                + ")" for f in failed)
            fail_build(build_id, {
                'error': (f"contract gate: {gate['score']['passed']}/"
                          f"{gate['score']['total']} standard features "
                          f"pass — {names}"),
                'template': tkey,
                'pi_read': pi_read,
                'contract_check': gate,
                'applied': [e for e in ledger if e['status'] == 'APPLIED'],
                'not_applied': [e for e in ledger
                                if e['status'] == 'NOT-APPLIED'],
            })
            return

        url = deploy(artifact, worker_name)   # deploy.py: CSS gate inside
        if not url:
            fail_build(build_id, {
                'error': 'deploy blocked/failed (see deploy.py output — CSS gate or Cloudflare)',
                'template': tkey,
                'pi_read': pi_read,
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
            'pi_read': pi_read,
            'applied': [e for e in ledger if e['status'] == 'APPLIED'],
            'not_applied': [e for e in ledger if e['status'] == 'NOT-APPLIED'],
            'contract_check': gate,
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
            'pi_read': pi_read,
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
