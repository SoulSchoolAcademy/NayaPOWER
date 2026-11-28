# File FIX2 (small files + rebuild inputs) to branch walkthrough-official-20261127.
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
DIR = 'TEAM-NITRO/walkthrough-official-20261127/fix2/maker/'
LANE = '/home/hatch/workspace/team-nitro/walkthrough-official-20261127/fix2/maker/'
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
 'fix2-cert.mjs', 'fix2-portal.mjs', 'commit-fix2.py',
 'phone-section3.html', 'phone-style3.html', 'phone-script3.html', 'steps.js', 'engine.js',
 'media/1_THE_VAULT.jpg', 'media/2_HOW_WE_SNYC.jpg', 'media/3_NANOVERSE.jpg',
 'media/4_HOW_IT_WORKS.jpg', 'media/5_SMART_VAULT.jpg', 'media/6_AUTO_MATCH.jpg',
 'media/7_AUTO_ORGINIZED.jpg', 'media/a3/a3903dafe3e9ee81ac66c6bb14104fdffcd7483550bd521a141f1c1ea6e538c4.png',
 'media/c0/c017eea7acbc2527b07efa2e61e9233bd0fb61f793b45882c7a867c562a0a8b7.png',
 'media/77/7702f98780b5dec46e146997451f61a4172de44cd93dee9fe6ccf1da37a882da.png',
 'media/f0/f0e21717d412807e5ad25bc58ded1b38be42a1b5f872ae27688c5c7daf1dfcef.png',
 'media/b6/b6cfaacab406f5213c1893c6f305b1f910dc1428a78dcb413004e335b7db4bb2.png',
 'media/42/4248188b4ea181ac848b727c30c7671c5243006cda8f62935241fcf2c2a5dae7.png',
 'media/fa/fa45cb8958e4aa3832c2622936988e8955e620a4c40264a0cd5fc5d940f86cfb.png',
 'evidence/probe-fix2.py', 'evidence/probe-fix2.log', 'evidence/debug-deal.py', 'evidence/debug-deal.log',
 'evidence/fix2-390-cert.png', 'evidence/fix2-390-cert-para.png', 'evidence/fix2-390-g1.png',
 'evidence/fix2-390-end.png', 'evidence/fix2-390-dealplain.png', 'evidence/fix2-390-zoom.png',
 'evidence/fix2-390-remove.png', 'evidence/fix2-1440-g1.png', 'evidence/fix2-1440-end.png']
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
open('/tmp/fix2-tree.json', 'w').write(json.dumps({'base_tree': base_tree, 'tree': entries}))
tree = api('POST', '/repos/%s/git/trees' % REPO, '/tmp/fix2-tree.json')
print('tree:', tree['sha'])
msg = ("Official walkthrough FIX2 2026-11-27 (staged only, nothing live)\n\n"
 "Fix-back pass on the fix1 checker's GOES BACK 9.0/10 (F1 + no-pop-ups law):\n"
 "F1: certificate paragraph under ENTER read 'ur alias' at 390 in the\n already-claimed state (D3 tiles pushed it into the bottom corner crests;\n D4 covered #hubNote only) — the D4 margin treatment applied to\n .cert-benefit (24px each side); re-proved at 390 in the taken state\n (paragraph x=43, 'Yo' point-test lands on the paragraph, not a crest).\n"
 "No-pop-ups law: the install veil element + ALL its show-code (openModal,\n installX/installGo, veil CSS, timers, beforeinstallprompt) DELETED from\n the certificate — not guarded. Grep over shipped bytes: 0 hits for\n installVeil/openModal/veil.hidden. Only the service-worker registration\n survives (not install UI); manifest link stays (browser-native).\n"
 "Remove-account confirm (#fpRemoveModal) converted to a full-screen\n in-frame view on the #fpStory pattern: opaque fullscreen, content\n centred in the frame (no floating card), clear round x close in view,\n Esc closes. Proved live via the returning flow (two saved accounts).\n"
 "Re-proved LIVE: complete() POST 200 + /me 200 (end screen READY),\n 'Choose plan' click lands on naya-model-pricing, #dealPlain opens\n fullscreen from the deal view (mirror-link tap) with the whole letter\n as plain text, #fpZoom opens fullscreen on a showcase-image tap.\n ROUTE FOUND (documented in the maker report): the deal view (stage)\n has NO tap entry in the shipped build — story never enters it,\n ?stage= is disabled, nothing calls enterStage(); only\n window.__fpStage.enter() enters it, and the letter view itself is only\n reachable via the exposed state API. The eye #dealEyeMain is hidden in\n every reachable state, so it is not a live opener.\n"
 "Keepers re-proven: veil gone, 1440 trio 360px unclipped, Tuesday gold\n tiles ticking, hubNote 24/24, slide header every phone, 23 steps in\n order, no Skip, gender no default, no church/Spotify, picture map\n byte-exact, video direct file only, end whole both widths, 44 answer\n keys, 0 page errors.\n\n"
 "Staged: https://official-walkthrough-staging.nayapower.workers.dev/ — portal\n 47,432,462 B sha 3301fa05..., cert 306,117 B sha 58574945..., worker\n deployment 9da60c33... on official-walkthrough-staging (HTTP 200),\n staged bytes == local bytes for / and /identity.html. Probe: 0 FAILs\n at 390x844 + 1440x900 (probe-fix2.py in this lane).\n"
 "portal.html + worker-consolidated.js (47 MB each) STILL not filed — the\n blobs API 422s them ('input too large', proven in fix1). INSTEAD the\n rebuild inputs ARE filed here (NEW portal-v1.html blob this round —\n the remove-modal conversion changed it, sha 88346f9d...) and the rebuild\n was proven byte-identical twice locally: portal 47,432,462 B sha\n 3301fa05..., worker 47,764,626 B sha 2919797f... (build-official.mjs +\n build-worker-official.mjs; pictures read from workspace/user/media_library\n — copy media/ there first).\n")
open('/tmp/fix2-commit.json', 'w').write(json.dumps({'message': msg, 'tree': tree['sha'], 'parents': [parent]}))
commit = api('POST', '/repos/%s/git/commits' % REPO, '/tmp/fix2-commit.json')
print('commit:', commit['sha'])
open('/tmp/fix2-ref.json', 'w').write(json.dumps({'sha': commit['sha'], 'force': False}))
ref = api('PATCH', '/repos/%s/git/refs/heads/%s' % (REPO, BRANCH), '/tmp/fix2-ref.json')
print('ref now:', ref['object']['sha'])
print('COMMIT DONE', commit['sha'])
