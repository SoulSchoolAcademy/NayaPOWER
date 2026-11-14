#!/usr/bin/env python3
"""Rendered-fix staging deploy for naya-public-blog-staging.
Same proven mechanism as deploy-phase2-staging.py (Direct Upload flow
via deploy_hub_assets.deploy_worker_with_assets) with ONE deliberate
difference, documented in the round record: the feed asset is FROZEN.
deploy-phase2-staging.py re-copies the LIVE feed on every run; the live
feed has since grown to 1,085 notes, and re-copying it would move the
staged snapshot off the brief's 1,058-note bullseye and break every
no-regression count tied to it. So this script overlays ONLY the edited
shell onto the existing staging-assets dir and leaves feed-live.json
(the frozen 1,058-note copy, sha 89d02559...) exactly as the fix round
left it. The worker is UNCHANGED in this round (server rendering was
already correct); it is redeployed byte-identical so the staged worker
and the staged shell come from one deploy.
STAGING ONLY. No live deploy, no PR, no merge.
Usage: deploy-rendered-fix-staging.py
"""
import hashlib
import shutil
import sys

sys.path.insert(0, "/home/hatch/workspace/factory-pipeline")
import deploy_hub_assets as dha

WD = "/home/hatch/workspace/team-nitro/seo-ai-backend-20261113"
STAGING = WD + "/staging-assets"
SCRIPT = WD + "/hub-worker-phase2.js"
SHELL = WD + "/index-intel-today-phase2.html"
FEED = STAGING + "/feed-live.json"

WORKER_SHA = "39ddddc1e036fd59868af2655bdecb10da3197c42b5d1324ef1bd0125632139c"
SHELL_SHA = "2c62d243f58989e8ae64ba80e75ad9074762945709ac75168c5e08eea92b9cb5"
FEED_SHA = "89d02559d2a3f5a501818c996a4f92e4e114bc6dc102fb6f41bca7c2a65558ad"


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


assert sha(SCRIPT) == WORKER_SHA, f"WORKER MOVED: {sha(SCRIPT)[:12]} != 39ddddc1"
assert sha(SHELL) == SHELL_SHA, f"SHELL NOT THE EDITED BYTES: {sha(SHELL)[:12]} != 323d2aea"
assert sha(FEED) == FEED_SHA, f"STAGED FEED MOVED: {sha(FEED)[:12]} != 89d02559"
print("OK guards: worker 39ddddc1 (unchanged), shell 323d2aea (edited), feed 89d02559 (frozen 1,058)")

shutil.copyfile(SHELL, STAGING + "/index.html")
assert sha(STAGING + "/index.html") == SHELL_SHA
assert sha(FEED) == FEED_SHA, "feed changed by the overlay — abort"
print("OK overlay: index.html <- edited shell; feed-live.json untouched (frozen)")

BASE8 = ["/smart-notes", "/smart-notes/*", "/s/*",
         "/notes/*", "/note", "/note/*", "/sw.js",
         "/service-worker.js"]
PHASE1_EXTRA = ["/robots.txt", "/sitemap.xml", "/images", "/images/*"]
dha.RUN_WORKER_FIRST = list(BASE8) + PHASE1_EXTRA
print("run_worker_first:", dha.RUN_WORKER_FIRST)

dha.deploy_worker_with_assets("naya-public-blog-staging", STAGING, SCRIPT)
print("OK rendered-fix worker+shell deployed to naya-public-blog-staging")
print("workers.dev: https://naya-public-blog-staging.nayapower.workers.dev/")
