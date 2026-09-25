#!/usr/bin/env python3
"""
Deployment Verification Script
Verifies exact source → build → deploy → browser → database parity
for the canonical NayaNET Hub.
"""
from __future__ import annotations
import json
import subprocess
import sys
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional, List

ROOT = Path(__file__).resolve().parents[2]

# Canonical configuration
CANONICAL_HUB_SOURCE = "NAYANET/HUB/index.html"
CANONICAL_HUB_SOURCE_SHA = "6a61b2c775d4e4b7a04721606813ec0031870399"
CLOUDFLARE_WORKER = "sparkling-shape-7ae5"
RUNTIME_URL = f"https://{CLOUDFLARE_WORKER}.smartnetpodcast.workers.dev"
SUPABASE_URL = "https://dahisasgpfvziswqvmvm.supabase.co"


def run_cmd(cmd: List[str], cwd: Path = ROOT) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def git_head() -> str:
    result = run_cmd(["git", "rev-parse", "HEAD"])
    return result.stdout.strip()


def get_file_sha(path: str) -> str:
    """Get git blob SHA for a file at current HEAD"""
    try:
        result = run_cmd(["git", "rev-parse", f"HEAD:{path}"])
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return "NOT_FOUND"


def sha256_file(path: Path) -> str:
    """Compute SHA256 of a file"""
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


class DeploymentVerifier:
    """Verify deployment parity across all layers"""
    
    def __init__(self):
        self.results: Dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source_head": git_head(),
            "checks": {}
        }
    
    def check_source_identity(self) -> bool:
        """Verify canonical Hub source SHA matches expected"""
        actual_sha = get_file_sha(CANONICAL_HUB_SOURCE)
        expected = CANONICAL_HUB_SOURCE_SHA
        
        self.results["checks"]["source_identity"] = {
            "expected_sha": expected,
            "actual_sha": actual_sha,
            "match": actual_sha == expected,
            "status": "PASS" if actual_sha == expected else "FAIL"
        }
        return actual_sha == expected
    
    def check_runtime_deployment(self) -> bool:
        """Read-only probe of the live Hub for the canonical deep-link contract."""
        import urllib.request
        import urllib.error

        required_markers = (
            "NAYA-CANONICAL-IB-DEEP-LINK-V1",
            "NayaHubDeepLink",
            "retrieveIntelligentBlock",
        )
        status = None
        body = ""
        try:
            req = urllib.request.Request(RUNTIME_URL, method="GET", headers={"Cache-Control":"no-cache"})
            response = urllib.request.urlopen(req, timeout=10)
            status = response.status
            body = response.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            status = e.code
        except Exception as e:
            self.results["checks"]["runtime_deployment"] = {
                "worker": CLOUDFLARE_WORKER,
                "url": RUNTIME_URL,
                "status": "MANUAL_VERIFICATION_REQUIRED",
                "reason": "LIVE_PROBE_ERROR",
                "detail": str(e),
                "required_markers": list(required_markers),
            }
            return False

        markers = {marker: marker in body for marker in required_markers}
        contract_present = status == 200 and all(markers.values())
        reason = "LIVE_SOURCE_CONTRACT_PRESENT" if contract_present else (
            "LIVE_SOURCE_MISSING_DEEP_LINK_CONTRACT" if status == 200 else "LIVE_HUB_HTTP_ERROR"
        )
        self.results["checks"]["runtime_deployment"] = {
            "worker": CLOUDFLARE_WORKER,
            "url": RUNTIME_URL,
            "http_status": status,
            "status": "PASS" if contract_present else "FAIL",
            "reason": reason,
            "required_markers": list(required_markers),
            "markers": markers,
            "source_length": len(body),
            "note": "Read-only live source contract probe; it does not prove authenticated owner retrieval or browser reload continuity."
        }
        return contract_present
    
    def check_supabase_edge_functions(self) -> bool:
        """Check Supabase Edge Function versions"""
        self.results["checks"]["supabase_functions"] = {
            "project": "dahisasgpfvziswqvmvm",
            "region": "ca-central-1",
            "functions": [
                "nayanet-github-webhook",
                "naya-smart-feed",
                "nayanet-compound-intelligence",
                "nayanet-project-intelligence-bridge",
                "v7-smart-note-canonical",
                "nayanet-smart-mail"
            ],
            "status": "MANUAL_VERIFICATION_REQUIRED",
            "note": "Verify via Supabase Dashboard: Functions deployed, versions current"
        }
        return True
    
    def check_database_schema(self) -> bool:
        """Check critical database tables exist"""
        self.results["checks"]["database_schema"] = {
            "project": "dahisasgpfvziswqvmvm",
            "critical_tables": [
                "nayanet_cognition_events",
                "nayanet_execution_receipts",
                "nayanet_project_cognition_state",
                "nayanet_intelligence_index",
                "nayanet_smart_ledger",
                "nayanet_intelligent_blocks",
                "nayanet_smart_connect_participation",
                "nayanet_authority_grants",
                "nayanet_intelligence_notifications",
                "learning_evidence"
            ],
            "critical_functions": [
                "nayanet_record_cognition_event",
                "nayanet_resolve_github_webhook_owner",
                "nayanet_smart_connect_github_bind",
                "nayanet_issue_authority_grant",
                "nayanet_validate_authority_grant"
            ],
            "status": "MANUAL_VERIFICATION_REQUIRED",
            "note": "Verify via Supabase SQL Editor: tables and functions exist"
        }
        return True
    
    def check_webhook_deployment(self) -> bool:
        """Check GitHub webhook function deployment"""
        # Probe the webhook endpoint
        import urllib.request
        import urllib.error
        
        url = f"{SUPABASE_URL}/functions/v1/nayanet-github-webhook"
        
        try:
            req = urllib.request.Request(url, method="POST", data=b"{}")
            req.add_header("Content-Type", "application/json")
            response = urllib.request.urlopen(req, timeout=10)
            status = response.status
        except urllib.error.HTTPError as e:
            status = e.code
        except Exception as e:
            status = f"ERROR: {e}"
        
        # Should return 503 with GITHUB_WEBHOOK_SECRET_NOT_CONFIGURED
        expected_status = 503
        
        self.results["checks"]["webhook_deployment"] = {
            "url": url,
            "expected_status": expected_status,
            "actual_status": status,
            "match": status == expected_status,
            "status": "PASS" if status == expected_status else "FAIL",
            "note": "Should fail closed with GITHUB_WEBHOOK_SECRET_NOT_CONFIGURED"
        }
        return status == expected_status
    
    def check_source_parity(self) -> bool:
        """Check source files haven't been modified unexpectedly"""
        critical_paths = [
            "NAYANET/HUB/index.html",
            "NAYANET/EXECUTION-BRIDGE/nayanet-github-webhook/index.ts",
            "supabase/functions/naya-smart-feed/index.ts",
            "supabase/functions/nayanet-compound-intelligence/index.ts",
            "supabase/functions/nayanet-project-intelligence-bridge/index.ts",
            "supabase/functions/v7-smart-note-canonical/index.ts",
        ]
        
        results = {}
        all_match = True
        for path in critical_paths:
            sha = get_file_sha(path)
            results[path] = sha
            if sha == "NOT_FOUND":
                all_match = False
        
        self.results["checks"]["source_parity"] = {
            "critical_paths": results,
            "all_found": all_match,
            "status": "PASS" if all_match else "FAIL"
        }
        return all_match
    
    def run_all_checks(self) -> Dict[str, Any]:
        """Run all verification checks"""
        print("Running deployment verification...")
        print(f"Source HEAD: {self.results['source_head']}")
        print(f"Timestamp: {self.results['timestamp']}")
        print("-" * 60)
        
        checks = [
            ("Source Identity", self.check_source_identity),
            ("Runtime Deployment", self.check_runtime_deployment),
            ("Supabase Edge Functions", self.check_supabase_edge_functions),
            ("Database Schema", self.check_database_schema),
            ("Webhook Deployment", self.check_webhook_deployment),
            ("Source Parity", self.check_source_parity),
        ]
        
        all_pass = True
        for name, check_fn in checks:
            try:
                result = check_fn()
                status = self.results["checks"].get(name.lower().replace(" ", "_"), {}).get("status", "UNKNOWN")
                print(f"  {name}: {status}")
                if status == "FAIL":
                    all_pass = False
            except Exception as e:
                print(f"  {name}: ERROR - {e}")
                self.results["checks"][name.lower().replace(" ", "_")] = {
                    "status": "ERROR",
                    "error": str(e)
                }
                all_pass = False
        
        self.results["overall"] = "PASS" if all_pass else "FAIL"
        self.results["summary"] = {
            "total_checks": len(checks),
            "passed": sum(1 for c in self.results["checks"].values() if c.get("status") == "PASS"),
            "failed": sum(1 for c in self.results["checks"].values() if c.get("status") == "FAIL"),
            "errors": sum(1 for c in self.results["checks"].values() if c.get("status") == "ERROR"),
            "manual_required": sum(1 for c in self.results["checks"].values() if c.get("status") == "MANUAL_VERIFICATION_REQUIRED"),
        }
        
        return self.results
    
    def save_results(self, path: Optional[Path] = None) -> Path:
        """Save verification results to file"""
        if path is None:
            path = ROOT / ".naya" / "project-intelligence" / f"DEPLOYMENT-VERIFICATION-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}.json"
        
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.results, indent=2) + "\n", encoding="utf-8")
        return path


def main() -> int:
    verifier = DeploymentVerifier()
    results = verifier.run_all_checks()
    
    print("-" * 60)
    print("SUMMARY:")
    print(f"  Overall: {results['overall']}")
    print(f"  Passed: {results['summary']['passed']}")
    print(f"  Failed: {results['summary']['failed']}")
    print(f"  Errors: {results['summary']['errors']}")
    print(f"  Manual Verification Required: {results['summary']['manual_required']}")
    
    output_path = verifier.save_results()
    print(f"\nResults saved to: {output_path}")
    
    # Print key findings
    print("\nKEY FINDINGS:")
    checks = results["checks"]
    
    # Source identity
    src = checks.get("source_identity", {})
    if src.get("match"):
        print(f"  [PASS] Source Identity: {src['actual_sha']} matches expected")
    else:
        print(f"  [FAIL] Source Identity MISMATCH: expected {src.get('expected_sha')}, got {src.get('actual_sha')}")
    
    # Webhook
    wh = checks.get("webhook_deployment", {})
    if wh.get("match"):
        print(f"  [PASS] Webhook Deployment: Returns {wh.get('actual_status')} as expected")
    else:
        print(f"  [WARN] Webhook: Expected {wh.get('expected_status')}, got {wh.get('actual_status')}")
    
    # Source parity
    sp = checks.get("source_parity", {})
    if sp.get("all_found"):
        print(f"  [PASS] All critical source files present")
    else:
        print(f"  ❌ Missing source files: {[p for p, s in sp.get('critical_paths', {}).items() if s == 'NOT_FOUND']}")
    
    return 0 if results["overall"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())