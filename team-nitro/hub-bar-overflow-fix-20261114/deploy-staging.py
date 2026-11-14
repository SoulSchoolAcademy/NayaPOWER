#!/usr/bin/env python3
"""Deploy the FIXED Hub shell to the STAGING worker naya-public-blog-staging
(proof only — never live). Modeled on hub-shell-bars-20261113/
deploy-shell-bars-staging.py: stage HUB/app from main, overlay the fixed
shell + the FRESH live feed, deploy with the PHASE-1 worker and the
PHASE-1-ONLY run_worker_first (base 8 + /robots.txt, /sitemap.xml,
/images, /images/*). No phase-2 patterns. The worker script is main's
HUB/hub-worker.js, asserted to be the phase-1 worker (sha 8ee4f859) —
if it moved, STOP.
"""
import hashlib
import sys

sys.path.insert(0, "/home/hatch/workspace/factory-pipeline")
import deploy_hub_assets as dha

WD = "/home/hatch/workspace/team-nitro/hub-bar-overflow-fix-20261114/work"
FIXED = WD + "/index-fixed.html"
FEED = WD + "/feed-live-fresh.json"
STAGING = WD + "/staging-assets"

BASE8 = ["/smart-notes", "/smart-notes/*", "/s/*",
         "/notes/*", "/note", "/note/*", "/sw.js",
         "/service-worker.js"]
PHASE1_EXTRA = ["/robots.txt", "/sitemap.xml", "/images", "/images/*"]
dha.RUN_WORKER_FIRST = list(BASE8) + PHASE1_EXTRA
print("run_worker_first:", dha.RUN_WORKER_FIRST)

fixed = open(FIXED, "rb").read()
assert hashlib.sha256(fixed).hexdigest() == "7d25f59105996fa0c40bde4d3b17a8c5e727e95861fc442b344c9f5ed840797d"
print(f"fixed shell: {len(fixed)} B sha 7d25f591...")

staging_dir, script_path, main_sha = dha.stage_hub_assets(FIXED, FEED, STAGING)
print(f"staged from main {str(main_sha)[:12]} -> {staging_dir}")

script = open(script_path, "rb").read()
print(f"script {script_path}: {len(script)} bytes, sha256 {hashlib.sha256(script).hexdigest()}")
assert len(script) == 49174, "phase-1 worker size moved — STOP"
assert hashlib.sha256(script).hexdigest() == \
    "8ee4f8594a694b851e614348e7edf44baf882d6ccefab9d3cdc474707ab192d6", \
    "phase-1 worker sha moved — STOP"

dha.deploy_worker_with_assets("naya-public-blog-staging", staging_dir, script_path)
print("OK fixed shell deployed to naya-public-blog-staging")
print("workers.dev: https://naya-public-blog-staging.nayapower.workers.dev/")
