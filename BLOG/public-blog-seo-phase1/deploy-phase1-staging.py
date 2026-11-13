#!/usr/bin/env python3
"""Phase-1 staging deploy for naya-public-blog-staging.
Reuses deploy_hub_assets.py's proven three-phase flow, with the
PHASE-1-ONLY run_worker_first override: the base 8 patterns from
HUB/wrangler.toml PLUS /robots.txt, /sitemap.xml, /images, /images/*.
Those four are the phase-1 config delta — without them the assets
layer answers those paths with the SPA-fallback shell before the
worker ever runs (the root cause of the live robots/sitemap fault).
No phase-2 patterns (/feed, /cluster, /api/seo, /api/intel-today/tags)
are added by this deploy.
The staged asset set is the existing staging-assets dir, UNCHANGED
except feed-live.json, which is refreshed from the live feed file so
the staged proof renders the current feed revision.
The script deployed is hub-worker-phase1.js (the built phase-1 worker).
STAGING ONLY. No live deploy, no PR, no merge.
Usage: deploy-phase1-staging.py
"""
import json
import shutil
import sys

sys.path.insert(0, "/home/hatch/workspace/factory-pipeline")
import deploy_hub_assets as dha

WD = "/home/hatch/workspace/team-nitro/public-blog-seo-20261112"
STAGING = WD + "/staging-assets"
SCRIPT = WD + "/hub-worker-phase1.js"
LIVE_FEED = "/home/hatch/workspace/factory-pipeline/hub-feed-live.json"

BASE8 = ["/smart-notes", "/smart-notes/*", "/s/*",
         "/notes/*", "/note", "/note/*", "/sw.js",
         "/service-worker.js"]
PHASE1_EXTRA = ["/robots.txt", "/sitemap.xml", "/images", "/images/*"]
dha.RUN_WORKER_FIRST = list(BASE8) + PHASE1_EXTRA
print("run_worker_first:", dha.RUN_WORKER_FIRST)

# Refresh the staged feed from the live feed file (data, not code).
live = json.load(open(LIVE_FEED, encoding="utf-8"))
staged = json.load(open(STAGING + "/feed-live.json", encoding="utf-8"))
print(f"staged feed: {staged.get('count')} notes, {staged.get('generated_from')}")
print(f"live feed:   {live.get('count')} notes, {live.get('generated_from')}")
shutil.copyfile(LIVE_FEED, STAGING + "/feed-live.json")
print("OK staged feed-live.json refreshed from live feed")

dha.deploy_worker_with_assets("naya-public-blog-staging", STAGING, SCRIPT)
print("OK phase-1 worker deployed to naya-public-blog-staging")
print("workers.dev: https://naya-public-blog-staging.nayapower.workers.dev/")
