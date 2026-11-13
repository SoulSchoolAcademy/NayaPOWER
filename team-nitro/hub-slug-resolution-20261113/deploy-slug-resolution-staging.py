#!/usr/bin/env python3
"""Hub Slug Resolution staging deploy for naya-public-blog-staging.
Modeled on ~/workspace/team-nitro/hub-shell-rebake-v2-20261113/deploy-v2-staging.py.
Reuses deploy_hub_assets.py's proven three-phase flow, with the
PHASE-1-ONLY run_worker_first override: the base 8 patterns from
HUB/wrangler.toml PLUS /robots.txt, /sitemap.xml, /images, /images/*.
No phase-2 patterns (/feed, /cluster, /api/seo, /api/intel-today/tags).
The staged asset set is this round's staging dir (staging-assets), built by
deploy_hub_assets.py stage from the fixed shell (index-intel-today.html)
+ the refreshed feed-live.json.
The script deployed is hub-worker-phase1.js (49,174 B, sha 8ee4f859...),
UNCHANGED — read, never edited, never replaced by main's HUB/hub-worker.js.
STAGING ONLY. No live deploy, no PR, no merge.
Usage: deploy-slug-resolution-staging.py
"""
import hashlib
import sys

sys.path.insert(0, "/home/hatch/workspace/factory-pipeline")
import deploy_hub_assets as dha

WD = "/home/hatch/workspace/team-nitro/hub-slug-resolution-20261113"
STAGING = WD + "/staging-assets"
SCRIPT = "/home/hatch/workspace/team-nitro/public-blog-seo-20261112/hub-worker-phase1.js"

BASE8 = ["/smart-notes", "/smart-notes/*", "/s/*",
         "/notes/*", "/note", "/note/*", "/sw.js",
         "/service-worker.js"]
PHASE1_EXTRA = ["/robots.txt", "/sitemap.xml", "/images", "/images/*"]
dha.RUN_WORKER_FIRST = list(BASE8) + PHASE1_EXTRA
print("run_worker_first:", dha.RUN_WORKER_FIRST)

script_bytes = open(SCRIPT, "rb").read()
print(f"script {SCRIPT}: {len(script_bytes)} bytes, sha256 "
      f"{hashlib.sha256(script_bytes).hexdigest()}")
assert len(script_bytes) == 49174, "phase-1 worker size moved — STOP"
assert hashlib.sha256(script_bytes).hexdigest() == \
    "8ee4f8594a694b851e614348e7edf44baf882d6ccefab9d3cdc474707ab192d6", \
    "phase-1 worker sha moved — STOP"

dha.deploy_worker_with_assets("naya-public-blog-staging", STAGING, SCRIPT)
print("OK slug-resolution shell deployed to naya-public-blog-staging")
print("workers.dev: https://naya-public-blog-staging.nayapower.workers.dev/")
