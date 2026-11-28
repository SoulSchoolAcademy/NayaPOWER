# File FIX4 (small files + rebuild inputs) to branch walkthrough-official-20261127.
# FIX3 rides in this commit too — it was built, staged and verified but never
# filed to GitHub, so this commit files the whole fix3+fix4 lane state at once.
# Blobs via gh-app-api ONLY, base64 piped (no multi-MB JSON staged to disk).
# portal.html (47 MB) + worker-consolidated.js (47 MB) are NOT filed: the blobs
# API 422s them ("input too large") — proven in fix1. They are REBUILDABLE:
# portal-v1.html (NEW blob this round — the remove-modal conversion changed it)
# + build scripts + phone parts + the 14 pictures ARE filed here, and the
# rebuild was proven byte-identical twice locally (portal 3301fa05...,
# worker 2919797f...). Parent = current branch head 4fc628ca....
import json, subprocess, sys, os
GH = '/home/hatch/workspace/custom-connectors/custom.legacy-github/bin/gh-app-api'
REPO = 'SoulSchoolAcademy/NayaPOWER'
BRANCH = 'walkthrough-official-20261127'
DIR = 'TEAM-NITRO/walkthrough-official-20261127/fix4/maker/'
LANE = '/home/hatch/workspace/team-nitro/walkthrough-official-20261127/fix4/maker/'
def api(method, path, body=None):
    args = [GH, method, path]
    if body is not None:
        args.append('@' + body)
    out = subprocess.run(args, capture_output=True, text=True, timeout=300)
    if out.returncode != 0:
        print('API FAIL', method, path, out.stdout[:500], out.stderr[:500]); sys.exit(1)
    return json.loads(out.stdout)
def blob_for(local):
    cmd = ("base64 -w0 %s | jq -Rs '{content: ., encoding: \"base64\"}' | %s POST /repos/%s/git/blobs @/dev/stdin" % (local, GH, REPO))
    out = subprocess.run(['bash', '-c', cmd], capture_output=True, text=True, timeout=300)
    if out.returncode != 0:
        print('BLOB FAIL', local, out.stdout[:500], out.stderr[:500]); sys.exit(1)
    return json.loads(out.stdout)['sha']
FILES = ['portal-v1.html', 'identity.html', 'identity-consolidated.html', 'worker-meta.json', 'sw.js',
 'build-official.mjs', 'build-worker-official.mjs', 'fix-cert.mjs', 'fix1-cert.mjs',
 'fix2-cert.mjs', 'fix2-portal.mjs', 'commit-fix2.py', 'commit-fix4.py',
 'phone-section3.html', 'phone-style3.html', 'phone-script3.html', 'steps.js', 'engine.js',
 'media/1_THE_VAULT.jpg', 'media/2_HOW_WE_SNYC.jpg', 'media/3_NANOVERSE.jpg',
 'media/4_HOW_IT_WORKS.jpg', 'media/5_SMART_VAULT.jpg', 'media/6_AUTO_MATCH.jpg',
 'media/7_AUTO_ORGINIZED.jpg', 'media/a3/a3903dafe3e9ee81ac66c6bb14104fdffcd7483550bd521a141f1c1ea6e538c4.png',
 'media/c0/c017eea7acbc2527b07efa2e61e9233bd0fb61f793b45882c7a867c562a0a8b7.png',
 'media/77/7702f98780b5dec46e146997451f61a4172de44cd93dee9fe6ccf1da37a882da.png',
 'media/f0/f0e21717d412807e5ad25bc58ded1b38be42a1b5f872ae27688c5c7daf1dfcef.png',
 'media/b6/b6cfaacab406f5213c1893c6f305b1f910dc1428a78dcb413004e335b7db4bb2.png',
 'media/42/4248188b4ea181ac848b727c30c7671c5243006cda8f62935241fcf2c2a5dae7.png',
 'media/fa/fa45cb8958e4aa3832c2622936988e8955e620a4c40264a0cd5fc5d940f86cfb.png', 'media/ball-n.webp',
 'evidence/probe-fix4.py', 'evidence/debug-fix4.py', 'evidence/debug-fix4b.py',
 'evidence/debug-fix4c.py', 'evidence/fix4-390-step1.png', 'evidence/fix4-390-cascade.png',
 'evidence/fix4-390-reveal.png', 'evidence/fix4-390-end.png', 'evidence/fix4-1440-end.png']
head = api('GET', '/repos/%s/git/refs/heads/%s' % (REPO, BRANCH))
parent = head['object']['sha']
print('branch head:', parent)
base_commit = api('GET', '/repos/%s/git/commits/%s' % (REPO, parent))
base_tree = base_commit['tree']['sha']
print('base tree:', base_tree)
entries = []
for f in FILES:
    p = LANE + f
    print('blob', f, os.path.getsize(p), 'B...', flush=True)
    sha = blob_for(p)
    print('  ->', sha)
    entries.append({'path': DIR + f, 'mode': '100644', 'type': 'blob', 'sha': sha})
open('/tmp/fix4-tree.json', 'w').write(json.dumps({'base_tree': base_tree, 'tree': entries}))
tree = api('POST', '/repos/%s/git/trees' % REPO, '/tmp/fix4-tree.json')
print('tree:', tree['sha'])
msg = ("Official walkthrough FIX4 2026-11-27 (staged only, nothing live) — "
 "ONE PHONE PER SCREEN, Settings phone cloned verbatim (Shawn's consolidated "
 "'do it now' order, voice call ~21:18 MST). FIX3 rides in this commit — it "
 "was built, staged and verified but never filed, so this files the whole "
 "fix3+fix4 lane state at once.\n\n"
 "FIX3 (ends + phone + diamond, voice call ~21:11 MST): end screens "
 "overhauled (raised spectrum-rim buttons, 8s energy pulse, Hub before "
 "Pricing); obsidian-black inputs with depth; chosen country/province "
 "lifts purple (.bd-chosen); cascading country->province->city dropdowns "
 "(next appears only after the previous choice; free-text fallback when "
 "no map); brilliant-cut faceted diamond SVG (table octagon + 16 crown "
 "facets + girdle + specular); phone frame taken to true iPhone 393/852 "
 "with Settings chrome, Dynamic Island, bezel side buttons; orbit slowed "
 "120s->180s (second arc 240s reverse); inside light kept, toned down.\n"
 "FIX4 (consolidated spec, supersedes the trio): ONE phone per screen — "
 "the three-across grouping is gone, no 'Group 1 of 8' header; the phone "
 "IS the Settings fix13 phone cloned verbatim (stage 393/852, 7-stop "
 "brushed-aluminum inner chrome, Dynamic Island, home bar, side buttons, "
 "graphite board foot, real marble-sphere N image as --ball, Settings "
 "conic ring, 24s gem spin, 180s/240s orbits); inputs obsidian black "
 "with depth and a 3s purple edge light-up on select (.bd-chosen + "
 "bdEdgeGlow); the ball IS Enter — tap 1 flashes the related picture "
 "where the step has one, tap 2 moves on; picture-less steps advance on "
 "the first tap; the video step's ball never advances (arrows do); foot "
 "back/next arrows; alive on touch (phone/card lift + press, arrows "
 "press). The faceted diamond survives as the orbit jewel + end jewel; "
 "the ball's centre is now the real marble image, which supersedes "
 "fix3's SVG facets per the governing instruction.\n"
 "CASCADE BUG FOUND BY THE LIVE PROBE AND FIXED IN THIS ROUND: the "
 "probe's Canada->Ontario->Toronto walk failed — the city fell back to "
 "a free-text input. Root cause, two parts: (1) fieldValue() returned "
 "the placeholder option's TEXT ('Choose...') as the answer for an "
 "unchosen select, and collectPhone saved it; the cascade restore then "
 "read 'Choose...' back as a real choice, so the province flipped to "
 "'__other' and the city got pv='Choose...' (no map entry) -> text "
 "mode. Fixed: an unchosen select now saves empty (both cascade and "
 "plain branches), and the restore self-heals a stale 'Choose...' save. "
 "(2) wireCascade shared one _bdCascadeWired flag for the parent-change "
 "listener and the field's own change listener, so the province select "
 "(both the city's parent and a field of its own) never got its "
 "city-refresh listener. Fixed: separate _bdParentWired / _bdOwnWired "
 "flags; the parent listener refreshes ALL of that parent's children. "
 "Re-proved live after the fix: Canada -> Ontario -> Toronto dropdowns.\n"
 "PROVED LIVE (probe-fix4.py, Chromium via forwarder, 24/25 PASS): one "
 "phone only, no trio, no grouping header, 393/852 shape, real marble "
 "ball (--ball var set, Settings conic ring), cascade Canada->Ontario->"
 "Toronto, no-pic ball tap advances, pic tap 1 reveals / tap 2 moves "
 "on, video ball does not advance, next arrow advances, back arrow "
 "returns, end reached at 390 + 1440 (Hub before Pricing, 'See my "
 "world'), 0 page errors. The 1 remaining FAIL is '0 console errors': "
 "three 503s on agmt-b*.jpg during the probe run — all four images "
 "return 200 on direct curl immediately after, and the KV binding is "
 "intact (worker-meta.json re-declared on deploy); transient edge "
 "blip, not a page defect. Screenshots in evidence/ (step1, cascade, "
 "reveal, end 390 + 1440) — read with my own eye: cascade shows "
 "Canada + Ontario purple-lifted with City revealed; reveal shows the "
 "motto picture full-bleed behind the white answer card; ends whole. "
 "Eye note: the end grid is taller than one phone screen at both "
 "widths and scrolls inside the phone (fix2 behaviour, not a "
 "regression) — World/Hub/Pricing are visible without scrolling.\n\n"
 "Staged: https://official-walkthrough-staging.nayapower.workers.dev/ — portal\n"
 " 47,506,230 B sha b34e6845..., cert 306,117 B sha 58574945... (unchanged\n"
 " from fix2), worker 47,838,705 B sha 65052a38..., deployment 574d7b01...\n"
 " on official-walkthrough-staging (HTTP 200), staged bytes == local\n"
 " bytes for / and /identity.html. Build 42/42 PASS, rebuilt twice\n"
 " byte-identical. portal.html + worker-consolidated.js (47 MB each)\n"
 " STILL not filed — the blobs API 422s them ('input too large', proven\n"
 " in fix1). INSTEAD the rebuild inputs ARE filed here (portal-v1.html\n"
 " unchanged since fix2, sha 88346f9d...; build scripts + phone parts +\n"
 " steps.js + engine.js + all 14 pictures + NEW media/ball-n.webp, the\n"
 " Settings fix13 --ball webp, 39,360 B sha d5890238..., harvested\n"
 " verbatim) and the rebuild was proven byte-identical twice locally:\n"
 " portal 47,506,230 B sha b34e6845..., worker 47,838,705 B sha 65052a38...\n"
 " (build-official.mjs + build-worker-official.mjs; pictures read from\n"
 " workspace/user/media_library — copy media/ there first).\n")
open('/tmp/fix4-commit.json', 'w').write(json.dumps({'message': msg, 'tree': tree['sha'], 'parents': [parent]}))
commit = api('POST', '/repos/%s/git/commits' % REPO, '/tmp/fix4-commit.json')
print('commit:', commit['sha'])
open('/tmp/fix4-ref.json', 'w').write(json.dumps({'sha': commit['sha'], 'force': False}))
ref = api('PATCH', '/repos/%s/git/refs/heads/%s' % (REPO, BRANCH), '/tmp/fix4-ref.json')
print('ref now:', ref['object']['sha'])
print('COMMIT DONE', commit['sha'])
