#!/usr/bin/env python3
"""Phase-2 staging deploy for naya-public-blog-staging.
Reuses deploy_hub_assets.py's proven three-phase flow, with the
PHASE-1 run_worker_first set (base 8 + /robots.txt, /sitemap.xml,
/images, /images/*) — no new patterns are needed: /s/*, /robots.txt
and /sitemap.xml are already claimed by the worker.
The staged asset set is a FRESH copy of the phase-1 staging-assets
dir, with TWO overlays: index.html <- the phase-2 edited shell and
feed-live.json <- the live feed file (1,058 notes, same revision).
The phase-1 staging-assets dir is never modified.
The script deployed is hub-worker-phase2.js (the built phase-2 worker).
STAGING ONLY. No live deploy, no PR, no merge.
Usage: deploy-phase2-staging.py
"""
import json, shutil, sys, os

sys.path.insert(0, "/home/hatch/workspace/factory-pipeline")
import deploy_hub_assets as dha

WD = "/home/hatch/workspace/team-nitro/seo-ai-backend-20261113"
P1_STAGING = "/home/hatch/workspace/team-nitro/public-blog-seo-20261112/staging-assets"
STAGING = WD + "/staging-assets"
SCRIPT = WD + "/hub-worker-phase2.js"
SHELL = WD + "/index-intel-today-phase2.html"
LIVE_FEED = "/home/hatch/workspace/factory-pipeline/hub-feed-live.json"

BASE8 = ["/smart-notes", "/smart-notes/*", "/s/*",
         "/notes/*", "/note", "/note/*", "/sw.js",
         "/service-worker.js"]
PHASE1_EXTRA = ["/robots.txt", "/sitemap.xml", "/images", "/images/*"]
dha.RUN_WORKER_FIRST = list(BASE8) + PHASE1_EXTRA
print("run_worker_first:", dha.RUN_WORKER_FIRST)

if os.path.exists(STAGING):
    shutil.rmtree(STAGING)
shutil.copytree(P1_STAGING, STAGING)
print(f"OK staging assets copied from phase-1 dir ({P1_STAGING})")
live = json.load(open(LIVE_FEED, encoding="utf-8"))
print(f"live feed: {live.get('count')} notes, {live.get('generated_from')}")
shutil.copyfile(SHELL, STAGING + "/index.html")
shutil.copyfile(LIVE_FEED, STAGING + "/feed-live.json")
print("OK overlays: index.html <- phase-2 shell, feed-live.json <- live feed")

dha.deploy_worker_with_assets("naya-public-blog-staging", STAGING, SCRIPT)
print("OK phase-2 worker deployed to naya-public-blog-staging")
print("workers.dev: https://naya-public-blog-staging.nayapower.workers.dev/")
